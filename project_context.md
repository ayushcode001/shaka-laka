# Project Context: Shaka Laka

## 1. Project Overview
**Shaka Laka** is an autonomous LeetCode Solver Bot and Web Dashboard. It integrates an automated solver engine with a modern Next.js user interface, utilizing GitHub Actions as a compute runner.

- **Purpose**: Automates fetching, solving, submitting, and committing LeetCode problems. It solves problems using the `llama-3.3-70b-versatile` model via the Groq API, validates solutions by polling LeetCode's judging API, handles compiler/runtime errors via adaptive retry feedback loops, and pushes successful solutions to the GitHub repository.
- **Tech Stack**:
  - **Backend/Scripting**: Python 3.11+, using `requests` (API integration), `beautifulsoup4` (HTML cleaning), `groq` (LLM solver client), and `playwright` (cookie refresher browser automation).
  - **Frontend UI**: Next.js 16/React 19 web dashboard styled with pure CSS Modules (glassmorphism/dark mode theme).
  - **CI/CD & Integration**: GitHub Actions workflow dispatches for execution, and Vercel for hosting the web dashboard.

## 2. Directory Structure

```text
.
├── .github
│   └── workflows
│       ├── daily.yml
│       └── solve.yml
├── .gitignore
├── README.md
├── config.py
├── github_client.py
├── groq_solver.py
├── leetcode-frontend
│   ├── .gitignore
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── README.md
│   ├── eslint.config.mjs
│   ├── jsconfig.json
│   ├── next.config.mjs
│   ├── package.json
│   ├── pages
│   │   ├── _app.js
│   │   ├── _document.js
│   │   ├── api
│   │   │   ├── status.js
│   │   │   └── trigger.js
│   │   └── index.js
│   ├── public
│   └── styles
│       ├── Home.module.css
│       └── globals.css
├── leetcode_client.py
├── leetcode_submitter.py
├── main.py
├── refresh_cookies.py
├── requirements.txt
├── solutions
│   ├── 0001_two_sum.py
│   ├── 0023_merge_k_sorted_lists.py
│   ├── 0075_sort_colors.py
│   ├── 0232_implement_queue_using_stacks.py
│   ├── 0239_sliding_window_maximum.py
│   └── 0860_design_circular_queue.py
└── vercel.json
```

## 3. Environment & Dependencies

### Python Dependencies (`requirements.txt`)
```text
requests
groq
python-dotenv
playwright
beautifulsoup4
```

### Frontend Dependencies (`leetcode-frontend/package.json`)
```json
{
  "name": "leetcode-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint"
  },
  "dependencies": {
    "next": "16.2.9",
    "react": "19.2.4",
    "react-dom": "19.2.4"
  },
  "devDependencies": {
    "eslint": "^9",
    "eslint-config-next": "16.2.9"
  }
}

```

## 4. Core Configuration

### vercel.json
```json
{
  "buildCommand": "cd leetcode-frontend && npm run build",
  "outputDirectory": "leetcode-frontend/.next",
  "framework": "nextjs"
}

```

### leetcode-frontend/next.config.mjs
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
  reactStrictMode: true,
};

export default nextConfig;

```

### leetcode-frontend/eslint.config.mjs
```javascript
import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";

const eslintConfig = defineConfig([
  ...nextVitals,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
  ]),
]);

export default eslintConfig;

```

### leetcode-frontend/jsconfig.json
```json
{
  "compilerOptions": {
    "paths": {
      "src/*": ["./*"]
    }
  }
}

```


## 5. Codebase Context

### /.github/workflows/solve.yml
GitHub Actions workflow to run the solver bot on-demand with problem inputs.

```yaml
name: LeetCode Solver Bot

on:
  workflow_dispatch:
    inputs:
      problems:
        description: 'Problem numbers to solve (space-separated, e.g. "1 42 206")'
        required: true
        default: '1'

jobs:
  solve:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run solver
        run: python main.py ${{ github.event.inputs.problems }}
        env:
          GROQ_API_KEY:        ${{ secrets.GROQ_API_KEY }}
          GITHUB_TOKEN:        ${{ secrets.GITHUB_TOKEN }}
          GITHUB_USERNAME:     ${{ github.repository_owner }}
          GITHUB_REPO:         ${{ github.event.repository.name }}
          LEETCODE_SESSION:    ${{ secrets.LEETCODE_SESSION }}
          LEETCODE_CSRF_TOKEN: ${{ secrets.LEETCODE_CSRF_TOKEN }}

```

### /.github/workflows/daily.yml
GitHub Actions workflow scheduled daily to fetch and solve the LeetCode Daily Challenge.

```yaml
name: LeetCode Daily Challenge Solver

on:
  schedule:
    - cron: '0 7 * * *'
  workflow_dispatch:

jobs:
  solve-daily:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run solver
        run: python main.py --daily
        env:
          GROQ_API_KEY:        ${{ secrets.GROQ_API_KEY }}
          GITHUB_TOKEN:        ${{ secrets.GITHUB_TOKEN }}
          GITHUB_USERNAME:     ${{ github.repository_owner }}
          GITHUB_REPO:         ${{ github.event.repository.name }}
          LEETCODE_SESSION:    ${{ secrets.LEETCODE_SESSION }}
          LEETCODE_CSRF_TOKEN: ${{ secrets.LEETCODE_CSRF_TOKEN }}

```

### /config.py
Loads environment variables via dotenv and exports credentials for Groq, GitHub, and LeetCode API.

```python
# config.py
from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME") or os.getenv("GITHUB_REPOSITORY_OWNER")

repo_env = os.getenv("GITHUB_REPO")
if not repo_env:
    repo_full = os.getenv("GITHUB_REPOSITORY")
    if repo_full and "/" in repo_full:
        repo_env = repo_full.split("/")[-1]
GITHUB_REPO = repo_env

LEETCODE_SESSION    = os.getenv("LEETCODE_SESSION")
LEETCODE_CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN")
```

### /groq_solver.py
Uses Groq SDK to request code solutions from llama-3.3-70b-versatile, including initial code generation and retry loop iterations.

```python
from groq import Groq
from bs4 import BeautifulSoup
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

PROMPT_TEMPLATE = """
You are an expert competitive programmer. Solve this LeetCode problem in Python.

Problem #{id}: {title}
Difficulty: {difficulty}
Tags: {tags}

Description:
{content}

Code Template:
Use the following starting template code exactly (keep the exact class name and function signature):
{code_template}

Requirements:
- Complete the starting template code with the optimal implementation
- Add a comment block at the top with:
  # Approach: (brief explanation)
  # Time Complexity: O(?)
  # Space Complexity: O(?)
- Code must be clean, well-commented, and handle all edge cases
- Use the most optimal approach possible

Return ONLY the Python code. No markdown, no backticks, no explanation outside the code.
"""

RETRY_PROMPT = """
Your previous solution for LeetCode #{id}: "{title}" failed.

Failure reason: {status}
Error / failed test case:
{error}

Your previous (wrong) solution:
{previous_code}

Code Template to follow:
{code_template}

Fix the solution. Think carefully about the edge case that failed and make sure you adhere to the expected class name and method signatures in the Code Template.
Return ONLY the corrected Python code. No markdown, no backticks.
"""

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def solve_problem(problem: dict, previous_result: dict = None, previous_code: str = None) -> str:
    code_template = problem.get("codeSnippet") or "class Solution:\n    pass"
    if previous_result and previous_result.get("status") != "Accepted" and previous_code:
        prompt = RETRY_PROMPT.format(
            id=problem.get("questionId", "?"),
            title=problem["title"],
            status=previous_result.get("status", "Wrong Answer"),
            error=previous_result.get("error") or previous_result.get("last_testcase") or "Unknown error",
            previous_code=previous_code,
            code_template=code_template
        )
    else:
        tags = ", ".join(t["name"] for t in problem.get("topicTags", []))
        prompt = PROMPT_TEMPLATE.format(
            id=problem.get("questionId", "?"),
            title=problem["title"],
            difficulty=problem["difficulty"],
            tags=tags or "N/A",
            content=clean_html(problem.get("content", "")),
            code_template=code_template
        )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2048
    )

    code = response.choices[0].message.content.strip()

    # Strip markdown fences if model adds them anyway
    if code.startswith("```"):
        lines = code.splitlines()
        code = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

    return code.strip()

```

### /github_client.py
Interacts with GitHub's REST API to save and commit accepted solution files to the repository.

```python
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
```

### /leetcode_client.py
Communicates with LeetCode's GraphQL API to fetch metadata and starting templates for a given problem.

```python
import requests

LEETCODE_GQL = "https://leetcode.com/graphql"

def fetch_problem(problem_number: int) -> dict:
    query = """
    query getProblem($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        titleSlug
        content
        difficulty
        exampleTestcases
        topicTags { name }
        codeSnippets {
          lang
          langSlug
          code
        }
      }
    }
    """
    # First, get the slug from problem number
    slug = get_slug_by_number(problem_number)
    
    resp = requests.post(LEETCODE_GQL, json={
        "query": query,
        "variables": {"titleSlug": slug}
    }, headers={"Content-Type": "application/json"})
    
    data = resp.json()["data"]["question"]
    snippets = data.get("codeSnippets") or []
    python_snippet = next((s["code"] for s in snippets if s["langSlug"] == "python3"), None)
    data["codeSnippet"] = python_snippet
    return data

def fetch_daily_problem() -> dict:
    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        date
        link
        question {
          questionId
          questionFrontendId
          title
          titleSlug
          difficulty
          content
          topicTags { name }
          codeSnippets {
            lang
            langSlug
            code
          }
        }
      }
    }
    """
    resp = requests.post(LEETCODE_GQL, json={
        "query": query
    }, headers={"Content-Type": "application/json"})
    
    data = resp.json()["data"]["activeDailyCodingChallengeQuestion"]["question"]
    snippets = data.get("codeSnippets") or []
    python_snippet = next((s["code"] for s in snippets if s["langSlug"] == "python3"), None)
    data["codeSnippet"] = python_snippet
    return data

def get_slug_by_number(number: int) -> str:
    query = """
    query problemsetQuestionList($skip: Int!) {
      problemsetQuestionList: questionList(
        categorySlug: ""
        limit: 1
        skip: $skip
        filters: {}
      ) {
        questions: data { titleSlug questionFrontendId }
      }
    }
    """
    # Search by offset (problems are roughly ordered)
    # Better: use a pre-built slug map or search by frontendId
    resp = requests.post(LEETCODE_GQL, json={
        "query": query,
        "variables": {"skip": number - 1}
    }, headers={"Content-Type": "application/json"})
    
    questions = resp.json()["data"]["problemsetQuestionList"]["questions"]
    return questions[0]["titleSlug"]
```

### /leetcode_submitter.py
Submits code solutions directly to LeetCode's judge endpoint and polls until a final verdict is parsed.

```python
import requests
import time
from config import LEETCODE_SESSION, LEETCODE_CSRF_TOKEN

BASE = "https://leetcode.com"

def get_session() -> requests.Session:
    s = requests.Session()
    s.cookies.set("LEETCODE_SESSION", LEETCODE_SESSION, domain="leetcode.com")
    s.cookies.set("csrftoken", LEETCODE_CSRF_TOKEN, domain="leetcode.com")
    s.headers.update({
        "x-csrftoken": LEETCODE_CSRF_TOKEN,
        "Referer": "https://leetcode.com",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    })
    return s

def submit_solution(title_slug: str, question_id: str, code: str) -> dict:
    session = get_session()

    def attempt_submit():
        # Warm up session by visiting the problem page
        problem_url = f"{BASE}/problems/{title_slug}/"
        session.get(problem_url)
        
        # Get fresh csrf token from response cookies
        new_csrf = session.cookies.get("csrftoken")
        if new_csrf:
            session.headers.update({"x-csrftoken": new_csrf})
            
        # Add 2-second delay to avoid rate limiting
        time.sleep(2.0)

        # Submit
        url = f"{BASE}/problems/{title_slug}/submit/"
        payload = {
            "lang": "python3",
            "question_id": question_id,
            "typed_code": code,
        }
        
        post_headers = {
            "Referer": problem_url,
            "Origin": BASE
        }
        
        resp = session.post(url, json=payload, headers=post_headers)
        resp.raise_for_status()
        return resp.json().get("submission_id")

    try:
        submission_id = attempt_submit()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            print("   403 Forbidden: Session/Token expired or missing. Retrying in 5 seconds...")
            time.sleep(5.0)
            submission_id = attempt_submit()
        else:
            raise

    if not submission_id:
        raise ValueError("No submission_id returned")

    print(f"   Submitted! ID: {submission_id}. Waiting for result...")

    # Step 2: Poll for result (LeetCode judges asynchronously)
    return poll_result(session, submission_id)

def poll_result(session: requests.Session, submission_id: int, 
                max_attempts: int = 20, delay: float = 2.0) -> dict:
    check_url = f"{BASE}/submissions/detail/{submission_id}/check/"

    for attempt in range(max_attempts):
        time.sleep(delay)
        resp = session.get(check_url)
        data = resp.json()

        state = data.get("state")
        if state == "SUCCESS":
            return parse_result(data)
        elif state == "PENDING" or state == "STARTED":
            print(f"   Judging... ({attempt + 1}/{max_attempts})")
            continue
        else:
            return {"status": "UNKNOWN", "raw": data}

    return {"status": "TIMEOUT", "message": "Judge took too long"}

def parse_result(data: dict) -> dict:
    status = data.get("status_msg", "Unknown")
    result = {
        "status": status,
        "runtime": data.get("status_runtime", "N/A"),
        "memory": data.get("status_memory", "N/A"),
        "runtime_percentile": data.get("runtime_percentile"),
        "memory_percentile": data.get("memory_percentile"),
        "total_testcases": data.get("total_testcases"),
        "passed_testcases": data.get("total_correct"),
    }

    if status != "Accepted":
        error_details = []
        if data.get("full_compile_error"):
            error_details.append(f"Compile Error:\n{data.get('full_compile_error')}")
        if data.get("full_runtime_error"):
            error_details.append(f"Runtime Error:\n{data.get('full_runtime_error')}")
        if status == "Wrong Answer":
            error_details.append("Wrong Answer:")
            if data.get("last_testcase"):
                error_details.append(f"  Input: {data.get('last_testcase')}")
            if data.get("code_output"):
                error_details.append(f"  Output: {data.get('code_output')}")
            if data.get("expected_output"):
                error_details.append(f"  Expected: {data.get('expected_output')}")
        
        # Fallback to general fields if nothing else matched
        if not error_details:
            error_details.append(f"Status: {status}")
            if data.get("last_testcase"):
                error_details.append(f"Last testcase: {data.get('last_testcase')}")
                
        result["error"] = "\n".join(error_details)

    return result
```

### /main.py
Entry point of the CLI solver bot. Manages problem list iteration, solve-and-submit retry loops, and pushes solutions to GitHub.

```python
from leetcode_client import fetch_problem, fetch_daily_problem
from groq_solver import solve_problem
from github_client import push_solution
from leetcode_submitter import submit_solution

import sys

MAX_RETRIES = 5  # ask Groq to fix if wrong answer

def run_problem(problem: dict):
    print(f"   {problem['title']} | {problem['difficulty']}")

    solution = None
    result = None
    success = False

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n🤖 Solving (attempt {attempt})...")
        solution = solve_problem(problem, previous_result=result, previous_code=solution)
        print(f"🚀 Submitting to LeetCode...")
        result = submit_solution(
            title_slug=problem["titleSlug"],
            question_id=problem["questionId"],
            code=solution
        )

        status = result["status"]
        print(f"\n{'✅' if status == 'Accepted' else '❌'} Result: {status}")

        if status == "Accepted":
            print(f"   Runtime : {result['runtime']} (beats {result['runtime_percentile']:.1f}%)")
            print(f"   Memory  : {result['memory']} (beats {result['memory_percentile']:.1f}%)")
            success = True
            break
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
            if attempt == MAX_RETRIES:
                print("   ⚠️  Max retries reached. Pushing best attempt anyway.")

    # Push to GitHub regardless, with result in the header comment
    print(f"\n📤 Pushing to GitHub...")
    push_solution(problem, solution, result)

    if not success:
        raise ValueError(f"Failed to solve problem: LeetCode status was {result.get('status', 'Unknown')}")

def run(args: list[str]):
    if not args:
        print("No arguments provided. Usage: python main.py <problem_id> or python main.py --daily")
        sys.exit(1)

    has_errors = False
    if "--daily" in args:
        print("\n" + "="*50)
        print("📋 LeetCode Daily Challenge")
        try:
            problem = fetch_daily_problem()
            run_problem(problem)
        except Exception as e:
            print(f"Error fetching/solving daily problem: {e}")
            has_errors = True
    else:
        for arg in args:
            try:
                num = int(arg)
            except ValueError:
                print(f"Invalid problem number: {arg}")
                has_errors = True
                continue
            print("\n" + "="*50)
            print(f"📋 Problem #{num}")
            try:
                problem = fetch_problem(num)
                run_problem(problem)
            except Exception as e:
                print(f"Error processing problem #{num}: {e}")
                has_errors = True
                continue

    if has_errors:
        sys.exit(1)

if __name__ == "__main__":
    run(sys.argv[1:])
```

### /refresh_cookies.py
Automation script using Playwright to handle LeetCode login and capture session tokens to bypass API expiration.

```python
"""
Run this script every 2-3 weeks to refresh your LeetCode session cookies.
It will print the new values — update them in your .env file and GitHub secrets.

Usage:
    python refresh_cookies.py

Requires:
    pip install playwright python-dotenv
    playwright install chromium
"""

import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

LEETCODE_EMAIL    = os.getenv("LEETCODE_EMAIL")
LEETCODE_PASSWORD = os.getenv("LEETCODE_PASSWORD")


def refresh_cookies():
    if not LEETCODE_EMAIL or not LEETCODE_PASSWORD:
        print("ERROR: Add LEETCODE_EMAIL and LEETCODE_PASSWORD to your .env file first.")
        return

    print("Launching browser and logging into LeetCode...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False so you can see it
        context = browser.new_context()
        page    = context.new_page()

        page.goto("https://leetcode.com/accounts/login/", wait_until="networkidle")
        time.sleep(2)

        # Fill credentials
        page.fill('input[name="login"]', LEETCODE_EMAIL)
        page.fill('input[name="password"]', LEETCODE_PASSWORD)
        time.sleep(1)

        print("Please solve the Cloudflare Turnstile captcha in the browser window if prompted...")
        page.click('button[type="submit"]', timeout=60000)

        # Wait for redirect to home
        try:
            page.wait_for_url("https://leetcode.com/", timeout=15000)
        except Exception:
            print("Login may have failed or took too long. Check the browser window.")
            browser.close()
            return

        print("Login successful. Extracting cookies...")
        time.sleep(2)

        cookies = context.cookies()

        session_cookie = next((c for c in cookies if c["name"] == "LEETCODE_SESSION"), None)
        csrf_cookie    = next((c for c in cookies if c["name"] == "csrftoken"), None)

        browser.close()

    if not session_cookie or not csrf_cookie:
        print("Could not find cookies. Try again or copy them manually from the browser.")
        return

    print("\n" + "="*60)
    print("Copy these into your .env file and GitHub Actions secrets:")
    print("="*60)
    print(f"\nLEETCODE_SESSION={session_cookie['value']}")
    print(f"\nLEETCODE_CSRF_TOKEN={csrf_cookie['value']}")
    print("\n" + "="*60)

    # Optionally auto-write back to .env
    update = input("\nAuto-update your .env file? (y/n): ").strip().lower()
    if update == "y":
        _update_env("LEETCODE_SESSION",    session_cookie["value"])
        _update_env("LEETCODE_CSRF_TOKEN", csrf_cookie["value"])
        print(".env updated successfully.")


def _update_env(key: str, value: str):
    env_path = ".env"
    with open(env_path, "r") as f:
        lines = f.readlines()

    updated = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    refresh_cookies()
```

### /leetcode-frontend/pages/_app.js
Main entry component for Next.js application that imports global styles.

```javascript
import "src/styles/globals.css";

export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

```

### /leetcode-frontend/pages/_document.js
Custom Next.js Document template defining core HTML structure.

```javascript
import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}

```

### /leetcode-frontend/pages/api/status.js
API route to query and return the execution status of a specific GitHub Actions workflow run.

```javascript
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

```

### /leetcode-frontend/pages/api/trigger.js
API route to dispatch a new GitHub Actions workflow run for selected problem numbers.

```javascript
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

```

### /leetcode-frontend/pages/index.js
Main glassmorphic React dashboard component to trigger solving runs and poll status.

```javascript
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

```

### /leetcode-frontend/styles/Home.module.css
Styles for the landing dashboard, featuring dark mode, animations, and glassmorphic elements.

```css
/* Home.module.css */

.container {
  min-height: 100vh;
  background-color: #0b0c10;
  color: #e2e8f0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem 1rem;
}

/* Background Glowing Effects (Subtle Mint/Emerald/Teal, NO Blue-Violet) */
.glow1 {
  position: absolute;
  top: 15%;
  left: 25%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(20, 184, 166, 0.04) 0%, rgba(0, 0, 0, 0) 70%);
  border-radius: 50%;
  z-index: 1;
  filter: blur(50px);
  animation: floatGlow 12s ease-in-out infinite alternate;
}

.glow2 {
  position: absolute;
  bottom: 15%;
  right: 25%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(14, 165, 233, 0.03) 0%, rgba(0, 0, 0, 0) 70%);
  border-radius: 50%;
  z-index: 1;
  filter: blur(50px);
  animation: floatGlow 15s ease-in-out infinite alternate-reverse;
}

@keyframes floatGlow {
  0% {
    transform: translate(0, 0) scale(1);
  }
  100% {
    transform: translate(20px, 20px) scale(1.05);
  }
}

.main {
  z-index: 2;
  width: 100%;
  max-width: 480px;
}

/* Modern Minimalistic Card with High-End Glassmorphism */
.glassCard {
  background: rgba(17, 18, 23, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 3rem 2.5rem;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5), 
              inset 0 1px 0 rgba(255, 255, 255, 0.02);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.glassCard:hover {
  background: rgba(17, 18, 23, 0.55);
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.6), 
              inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

/* Header styling */
.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 2.5rem;
}

.botBadge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #a1a1aa;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  padding: 0.35rem 0.8rem;
  border-radius: 100px;
  margin-bottom: 1.25rem;
  transition: all 0.2s ease;
}

.statusDot {
  width: 6px;
  height: 6px;
  background-color: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 5px rgba(16, 185, 129, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
  }
}

.title {
  font-family: 'Outfit', sans-serif;
  font-size: 2.25rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.03em;
  color: #ffffff;
}

.gradientText {
  background: linear-gradient(135deg, #ffffff 30%, #a1a1aa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Form Styles */
.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.inputGroup {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #a1a1aa;
}

.input {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 0.8rem 1rem;
  color: #ffffff;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  width: 100%;
  box-sizing: border-box;
}

.input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.04);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2);
}

.numberInputWrapper {
  max-width: 100px;
}

.helperText {
  font-size: 0.72rem;
  color: #52525b;
}

.helperText code {
  color: #a1a1aa;
  background: rgba(255, 255, 255, 0.03);
  padding: 0.1rem 0.25rem;
  border-radius: 4px;
}

/* Stark White Minimalistic Submit Button */
.submitBtn {
  margin-top: 0.75rem;
  background: #ffffff;
  border: none;
  border-radius: 8px;
  color: #000000;
  font-size: 0.95rem;
  font-weight: 600;
  padding: 0.95rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05);
}

.submitBtn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.12);
}

.submitBtn:active:not(:disabled) {
  transform: translateY(0);
}

.submitBtn:disabled {
  background: #18181b;
  border: 1px solid rgba(255, 255, 255, 0.03);
  color: #52525b;
  cursor: not-allowed;
  box-shadow: none;
}

.loadingSpinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-top-color: #000000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Toast / Status Box (Sleek Bordered Boxes) */
.successBox,
.errorBox {
  display: flex;
  gap: 0.75rem;
  padding: 0.85rem 1.1rem;
  border-radius: 8px;
  font-size: 0.825rem;
  line-height: 1.5;
  border: 1px solid;
}

.successBox {
  background: rgba(16, 185, 129, 0.02);
  border-color: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.errorBox {
  background: rgba(239, 68, 68, 0.02);
  border-color: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.infoBox {
  display: flex;
  gap: 0.75rem;
  padding: 0.85rem 1.1rem;
  border-radius: 8px;
  font-size: 0.825rem;
  line-height: 1.5;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.01);
  color: #a1a1aa;
}

.statusDetails {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.statusLink {
  color: #ffffff;
  text-decoration: underline;
  font-size: 0.75rem;
  align-self: flex-start;
  transition: color 0.2s ease;
}

.statusLink:hover {
  color: #a1a1aa;
}

.statusIcon {
  font-weight: bold;
  font-size: 1rem;
}

.statusMessage {
  margin: 0;
}

/* Footer styling */
.footer {
  margin-top: 3rem;
  font-size: 0.75rem;
  color: #3f3f46;
  z-index: 2;
  text-align: center;
}

.footer a {
  color: #52525b;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer a:hover {
  color: #a1a1aa;
}

```

### /leetcode-frontend/styles/globals.css
Global application CSS stylesheet.

```css
:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

html,
body {
  max-width: 100vw;
  overflow-x: hidden;
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

a {
  color: inherit;
  text-decoration: none;
}

@media (prefers-color-scheme: dark) {
  html {
    color-scheme: dark;
  }
}

```

### /leetcode-frontend/AGENTS.md
Custom Next.js instructions and guidelines for agent reasoning.

```markdown
<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

```

### /leetcode-frontend/CLAUDE.md
Reference pointer referring back to AGENTS.md.

```markdown
@AGENTS.md

```

### /solutions/0001_two_sum.py
Accepted Python 3 solution for LeetCode Problem #1: Two Sum.

```python
# 1. Two Sum
# Difficulty  : Easy
# Tags        : Array, Hash Table
# LeetCode    : https://leetcode.com/problems/two-sum/
# Status      : Accepted
# Runtime     : 0 ms (beats 100.0%)
# Memory      : 20.5 MB (beats 41.4%)
# Solved on   : 2026-06-25
# ─────────────────────────────────────────────────────────────

# Approach: We use a hash table to store the numbers we have seen so far and their indices. This allows us to check if the complement of the current number (i.e., the number that needs to be added to it to get the target) is in the hash table in constant time.
# Time Complexity: O(n)
# Space Complexity: O(n)
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], i]
            num_to_index[num] = i
        return []
```

### /solutions/0023_merge_k_sorted_lists.py
Accepted Python 3 solution for LeetCode Problem #23: Merge k Sorted Lists.

```python
# 23. Merge k Sorted Lists
# Difficulty  : Hard
# Tags        : Linked List, Divide and Conquer, Heap (Priority Queue), Merge Sort
# LeetCode    : https://leetcode.com/problems/merge-k-sorted-lists/
# Status      : Accepted
# Runtime     : 11 ms (beats 54.9%)
# Memory      : 22.9 MB (beats 45.9%)
# Solved on   : 2026-07-04
# ─────────────────────────────────────────────────────────────

# Approach: We will use a min-heap to store the current smallest node from each linked list. This approach ensures that we always select the smallest node to add to our result list, thus maintaining the sorted order.
# Time Complexity: O(N log k), where N is the total number of nodes across all linked lists and k is the number of linked lists. This is because we perform a heap operation for each node.
# Space Complexity: O(k), as we need to store k nodes in the heap at any given time.

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Create a min-heap to store the current smallest node from each linked list
        min_heap = []
        
        # Add the head of each linked list to the min-heap
        for i, node in enumerate(lists):
            if node:
                # Store a tuple containing the node's value, the list index, and the node itself
                # This allows us to break ties based on the list index
                heapq.heappush(min_heap, (node.val, i, node))
        
        # Create a dummy node to serve as the head of our result list
        dummy = ListNode()
        current = dummy
        
        # Continue until the min-heap is empty
        while min_heap:
            # Extract the smallest node from the min-heap
            val, list_index, node = heapq.heappop(min_heap)
            
            # Add the extracted node to our result list
            current.next = node
            current = current.next
            
            # If the extracted node has a next node, add it to the min-heap
            if node.next:
                heapq.heappush(min_heap, (node.next.val, list_index, node.next))
        
        # Return the next node of the dummy node, which is the head of our result list
        return dummy.next
```

### /solutions/0239_sliding_window_maximum.py
Accepted Python 3 solution for LeetCode Problem #239: Sliding Window Maximum.

```python
# 239. Sliding Window Maximum
# Difficulty  : Hard
# Tags        : Array, Queue, Sliding Window, Heap (Priority Queue), Monotonic Queue
# LeetCode    : https://leetcode.com/problems/sliding-window-maximum/
# Status      : Accepted
# Runtime     : 639 ms (beats 5.0%)
# Memory      : 34.5 MB (beats 94.9%)
# Solved on   : 2026-06-26
# ─────────────────────────────────────────────────────────────

# Approach: We use a deque to store the indices of the elements in the current window. 
# The deque is maintained in such a way that the front always contains the index of the maximum element in the current window.
# Time Complexity: O(n)
# Space Complexity: O(n)

class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        # Initialize an empty list to store the maximum values
        max_values = []
        
        # Initialize a deque to store the indices of the elements in the current window
        window = []
        
        # Iterate over the list of numbers
        for i, num in enumerate(nums):
            # Remove the indices of the elements that are out of the current window
            while window and window[0] <= i - k:
                window.pop(0)
            
            # Remove the indices of the elements that are smaller than the current element
            while window and nums[window[-1]] < num:
                window.pop()
            
            # Add the index of the current element to the window
            window.append(i)
            
            # If the window is full, add the maximum value to the list of maximum values
            if i >= k - 1:
                max_values.append(nums[window[0]])
        
        # Return the list of maximum values
        return max_values
```

### /solutions/0860_design_circular_queue.py
Accepted Python 3 solution for LeetCode Problem #860: Design Circular Queue.

```python
# 860. Design Circular Queue
# Difficulty  : Medium
# Tags        : Array, Linked List, Design, Queue
# LeetCode    : https://leetcode.com/problems/design-circular-queue/
# Status      : Accepted
# Runtime     : 8 ms (beats 43.5%)
# Memory      : 20 MB (beats 26.5%)
# Solved on   : 2026-06-26
# ─────────────────────────────────────────────────────────────

# Approach: We will use a circular array to implement the queue. The array will have a fixed size, and we will use two pointers, one for the front and one for the rear of the queue. When the rear pointer reaches the end of the array, it will wrap around to the beginning.
# Time Complexity: O(1) for all operations
# Space Complexity: O(k) where k is the size of the queue

class MyCircularQueue:
    def __init__(self, k: int):
        self.k = k
        self.queue = [None] * k
        self.front = 0
        self.rear = 0
        self.size = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.queue[self.rear] = value
        self.rear = (self.rear + 1) % self.k
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.k
        self.size -= 1
        return True

    def Front(self) -> int:
        if self.isEmpty():
            return -1
        return self.queue[self.front]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self.queue[(self.rear - 1) % self.k]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.k

class Solution:
    def test_circular_queue(self):
        my_circular_queue = MyCircularQueue(3)
        print(my_circular_queue.enQueue(1))  # return True
        print(my_circular_queue.enQueue(2))  # return True
        print(my_circular_queue.enQueue(3))  # return True
        print(my_circular_queue.enQueue(4))  # return False
        print(my_circular_queue.Rear())     # return 3
        print(my_circular_queue.isFull())   # return True
        print(my_circular_queue.deQueue())  # return True
        print(my_circular_queue.enQueue(4)) # return True
        print(my_circular_queue.Rear())     # return 4

solution = Solution()
solution.test_circular_queue()
```

