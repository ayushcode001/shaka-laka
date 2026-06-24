export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { count, problems } = req.body;

  if (!problems || typeof problems !== 'string') {
    return res.status(400).json({ error: 'Problem numbers are required (space-separated string)' });
  }

  const token = process.env.GITHUB_TOKEN;
  const owner = process.env.GITHUB_USERNAME;
  const repo = process.env.GITHUB_REPO;
  const workflowId = 'solve.yml';

  if (!token || !owner || !repo) {
    return res.status(500).json({ error: 'Missing GitHub configuration variables on the server (.env.local)' });
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
      return res.status(200).json({ message: 'GitHub workflow successfully triggered!' });
    } else {
      const errorText = await response.text();
      return res.status(response.status).json({ error: `GitHub API error: ${errorText}` });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message || 'Unknown internal error' });
  }
}
