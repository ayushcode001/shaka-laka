export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { count, problems } = req.body;

  if (!problems || typeof problems !== 'string') {
    return res.status(400).json({ error: 'Problem numbers are required (space-separated string)' });
  }

  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
  const owner = process.env.GITHUB_USERNAME || process.env.GH_USERNAME;
  const repo = process.env.GITHUB_REPO || process.env.GH_REPO;
  const workflowId = 'solve.yml';

  if (!token || !owner || !repo) {
    return res.status(500).json({ error: 'Missing GitHub configuration variables on the server (GITHUB_TOKEN/GH_TOKEN, GITHUB_USERNAME/GH_USERNAME, GITHUB_REPO/GH_REPO)' });
  }

  try {
    const response = await fetch(
      `https://api.github.com/repos/${owner}/${repo}/actions/workflows/${workflowId}/dispatches`,
      {
        method: 'POST',
        headers: {
          'Accept': 'application/vnd.github+json',
          'Authorization': `Bearer ${token}`,
          'X-GitHub-Api-Version': '2022-11-28',
          'Content-Type': 'application/json',
          'User-Agent': 'leetcode-frontend-trigger'
        },
        body: JSON.stringify({
          ref: 'main',
          inputs: {
            problems: problems.trim()
          }
        })
      }
    );

    if (response.ok) {
      // Wait a brief moment for GitHub to register the new run
      await new Promise((resolve) => setTimeout(resolve, 1500));

      const runsResponse = await fetch(
        `https://api.github.com/repos/${owner}/${repo}/actions/workflows/${workflowId}/runs?event=workflow_dispatch&per_page=1`,
        {
          headers: {
            'Accept': 'application/vnd.github+json',
            'Authorization': `Bearer ${token}`,
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'leetcode-frontend-trigger'
          }
        }
      );

      let runId = null;
      if (runsResponse.ok) {
        const runsData = await runsResponse.json();
        if (runsData.workflow_runs && runsData.workflow_runs.length > 0) {
          runId = runsData.workflow_runs[0].id;
        }
      }

      return res.status(200).json({ 
        message: 'GitHub workflow successfully triggered!', 
        runId: runId
      });
    } else {
      const errorText = await response.text();
      return res.status(response.status).json({ error: `GitHub API error: ${errorText}` });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message || 'Unknown internal error' });
  }
}
