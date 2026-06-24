import base64
import requests
from datetime import datetime
from config import GITHUB_TOKEN, GITHUB_REPO, GITHUB_USERNAME

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}
BASE = "https://api.github.com"

def format_solution(problem: dict, code: str, result: dict = None) -> str:
    status   = result.get("status", "Not submitted") if result else "Not submitted"
    runtime  = result.get("runtime", "N/A")          if result else "N/A"
    memory   = result.get("memory", "N/A")           if result else "N/A"
    rt_pct   = result.get("runtime_percentile")      if result else None
    mem_pct  = result.get("memory_percentile")       if result else None
    tags     = ", ".join(t["name"] for t in problem.get("topicTags", []))
    solved   = datetime.now().strftime("%Y-%m-%d")

    rt_str  = f"{runtime} (beats {rt_pct:.1f}%)" if rt_pct else runtime
    mem_str = f"{memory} (beats {mem_pct:.1f}%)" if mem_pct else memory

    header = f"""# {problem['questionId']}. {problem['title']}
# Difficulty  : {problem['difficulty']}
# Tags        : {tags or 'N/A'}
# LeetCode    : https://leetcode.com/problems/{problem['titleSlug']}/
# Status      : {status}
# Runtime     : {rt_str}
# Memory      : {mem_str}
# Solved on   : {solved}
# ─────────────────────────────────────────────────────────────

"""
    return header + code


def get_file_sha(path: str) -> str | None:
    url = f"{BASE}/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{path}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None


def ensure_solutions_folder():
    """Create solutions/.gitkeep if the folder doesn't exist yet."""
    path = "solutions/.gitkeep"
    if get_file_sha(path) is None:
        content = base64.b64encode(b"").decode()
        url = f"{BASE}/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{path}"
        requests.put(url, json={
            "message": "chore: init solutions folder",
            "content": content
        }, headers=HEADERS)


def push_solution(problem: dict, code: str, result: dict = None):
    ensure_solutions_folder()

    problem_id = str(problem["questionId"]).zfill(4)
    slug       = problem["titleSlug"].replace("-", "_")
    filename   = f"solutions/{problem_id}_{slug}.py"
    full_code  = format_solution(problem, code, result)

    sha     = get_file_sha(filename)
    content = base64.b64encode(full_code.encode()).decode()

    status_emoji = "✅" if (result and result.get("status") == "Accepted") else "❌"
    commit_msg   = f"{status_emoji} {problem_id}. {problem['title']} [{problem['difficulty']}]"

    payload = {
        "message": commit_msg,
        "content": content,
        "committer": {
            "name": "LeetCode Bot",
            "email": "leetcode-bot@users.noreply.github.com"
        }
    }
    if sha:
        payload["sha"] = sha

    url  = f"{BASE}/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{filename}"
    resp = requests.put(url, json=payload, headers=HEADERS)

    if resp.status_code in (200, 201):
        print(f"   Pushed → {filename}")
    else:
        print(f"   GitHub push failed: {resp.status_code} — {resp.text}")
        resp.raise_for_status()