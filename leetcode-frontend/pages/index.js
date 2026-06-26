import Head from "next/head";
import { useState } from "react";
import styles from "src/styles/Home.module.css";

export default function Home() {
  const [count, setCount] = useState("1");
  const [problems, setProblems] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null); // { type: 'success' | 'error', message: string }
  const [workflowStatus, setWorkflowStatus] = useState(null); // { status: string, conclusion: string, url: string }

  const pollWorkflowStatus = async (runId) => {
    try {
      const res = await fetch(`/api/status?runId=${runId}`);
      if (res.ok) {
        const data = await res.json();
        setWorkflowStatus({
          status: data.status,
          conclusion: data.conclusion,
          url: data.html_url
        });

        if (data.status === "completed") {
          setLoading(false);
          if (data.conclusion === "success") {
            setStatus({
              type: "success",
              message: "Bot finished solving and solutions were pushed to GitHub!"
            });
          } else {
            setStatus({
              type: "error",
              message: "Workflow failed on GitHub. Please check the run logs."
            });
          }
          return;
        }
      }
    } catch (err) {
      console.error("Error polling workflow status:", err);
    }

    // Poll again after 4 seconds
    setTimeout(() => pollWorkflowStatus(runId), 4000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus(null);
    setWorkflowStatus(null);

    // Basic Validation
    if (!problems.trim()) {
      setStatus({ type: "error", message: "Please specify at least one LeetCode problem number." });
      setLoading(false);
      return;
    }

    // Clean up input: split by space/comma, filter out non-numbers
    const parsed = problems
      .trim()
      .split(/[\s,]+/)
      .map(p => p.trim())
      .filter(p => /^\d+$/.test(p));

    if (parsed.length === 0) {
      setStatus({ type: "error", message: "Invalid problem numbers. Please enter only numeric digits separated by spaces." });
      setLoading(false);
      return;
    }

    try {
      const res = await fetch("/api/trigger", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          count: parseInt(count, 10) || 1,
          problems: parsed.join(" "),
        }),
      });

      const data = await res.json();
      if (res.ok) {
        setStatus({
          type: "success",
          message: data.message || "LeetCode Solver Workflow triggered successfully! Tracking status...",
        });
        if (data.runId) {
          setWorkflowStatus({ status: "queued", conclusion: null, url: null });
          pollWorkflowStatus(data.runId);
        } else {
          setLoading(false);
        }
      } else {
        setStatus({
          type: "error",
          message: data.error || "Failed to trigger the workflow. Please check your credentials.",
        });
        setLoading(false);
      }
    } catch (err) {
      setStatus({ type: "error", message: err.message || "An unexpected error occurred." });
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>LeetCode Auto-Solver Dashboard</title>
        <meta name="description" content="Manage and trigger your automated LeetCode solver bot" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
      </Head>

      {/* Decorative Background Glows */}
      <div className={styles.glow1}></div>
      <div className={styles.glow2}></div>

      <main className={styles.main}>
        <div className={styles.glassCard}>
          <div className={styles.header}>
            <div className={styles.botBadge}>
              <span className={styles.statusDot}></span>
              <span>System Online</span>
            </div>
            <h1 className={styles.title}>
              LeetCode <span className={styles.gradientText}>Solver Bot</span>
            </h1>
          </div>

          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.inputGroup}>
              <label className={styles.label}>
                1. How many problems to solve today?
              </label>
              <div className={styles.numberInputWrapper}>
                <input
                  type="number"
                  min="1"
                  max="50"
                  value={count}
                  onChange={(e) => setCount(e.target.value)}
                  className={styles.input}
                  required
                />
              </div>
            </div>

            <div className={styles.inputGroup}>
              <label className={styles.label}>
                2. Enter problem numbers (space-separated)
              </label>
              <input
                type="text"
                placeholder="e.g. 1 42 206"
                value={problems}
                onChange={(e) => setProblems(e.target.value)}
                className={styles.input}
                required
              />
              <span className={styles.helperText}>
                Example: <code>1</code> for Two Sum, <code>42</code> for Trapping Rain Water.
              </span>
            </div>

            {status && (
              <div className={status.type === "success" ? styles.successBox : styles.errorBox}>
                <span className={styles.statusIcon}>
                  {status.type === "success" ? "✓" : "⚠"}
                </span>
                <p className={styles.statusMessage}>{status.message}</p>
              </div>
            )}

            {workflowStatus && (
              <div className={
                workflowStatus.status === "completed"
                  ? (workflowStatus.conclusion === "success" ? styles.successBox : styles.errorBox)
                  : styles.infoBox
              }>
                <span className={styles.statusIcon}>
                  {workflowStatus.status === "completed"
                    ? (workflowStatus.conclusion === "success" ? "✓" : "⚠")
                    : "●"}
                </span>
                <div className={styles.statusDetails}>
                  <p className={styles.statusMessage}>
                    {workflowStatus.status === "completed"
                      ? (workflowStatus.conclusion === "success"
                          ? "Workflow completed successfully! All solved problems have been pushed to GitHub."
                          : "Workflow failed on GitHub. Please check the logs.")
                      : `GitHub Workflow: ${workflowStatus.status}...`}
                  </p>
                  {workflowStatus.url && (
                    <a href={workflowStatus.url} target="_blank" rel="noreferrer" className={styles.statusLink}>
                      View Run on GitHub Actions →
                    </a>
                  )}
                </div>
              </div>
            )}

            <button type="submit" disabled={loading} className={styles.submitBtn}>
              {loading ? (
                <div className={styles.loadingSpinner}>
                  <div className={styles.spinner}></div>
                  <span>Triggering bot...</span>
                </div>
              ) : (
                "Initiate Solve Sequence"
              )}
            </button>
          </form>
        </div>
      </main>

      <footer className={styles.footer}>
        Powered by Groq &amp; GitHub Actions • <a href="https://github.com/ayushcode001/shaka-laka" target="_blank" rel="noreferrer">shaka-laka Repository</a>
      </footer>
    </div>
  );
}
