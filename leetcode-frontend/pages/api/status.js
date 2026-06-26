export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { runId } = req.query;
  if (!runId) {
    return res.status(400).json({ error: 'Missing runId parameter' });
  }

  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
  const owner = process.env.GITHUB_USERNAME || process.env.GH_USERNAME;
  const repo = process.env.GITHUB_REPO || process.env.GH_REPO;

  if (!token || !owner || !repo) {
    return res.status(500).json({ error: 'Missing GitHub configuration variables (GITHUB_TOKEN/GH_TOKEN, GITHUB_USERNAME/GH_USERNAME, GITHUB_REPO/GH_REPO)' });
  }

  try {
    const response = await fetch(
      `https://api.github.com/repos/${owner}/${repo}/actions/runs/${runId}`,
      {
        headers: {
          'Accept': 'application/vnd.github+json',
          'Authorization': `Bearer ${token}`,
          'X-GitHub-Api-Version': '2022-11-28',
          'User-Agent': 'leetcode-frontend-status'
        }
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      return res.status(response.status).json({ error: `GitHub API error: ${errorText}` });
    }

    const data = await response.json();
    return res.status(200).json({
      status: data.status,
      conclusion: data.conclusion,
      html_url: data.html_url
    });
  } catch (error) {
    return res.status(500).json({ error: error.message || 'Unknown internal error' });
  }
}
