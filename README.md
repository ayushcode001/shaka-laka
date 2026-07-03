# Shaka Laka

An autonomous agent system that fetches LeetCode problems, solves them using Groq API, submits to LeetCode, handles retries on failures, and commits the solutions to a GitHub repository.

## Features
- **Auto-Solve by Problem Number**: Trigger solving sequences for one or more specific LeetCode problem IDs from CLI or UI.
- **Daily Challenge Streak**: Automated mode to fetch and solve LeetCode's active Daily Challenge problem to maintain your streak.
- **Retry Loop**: Retries up to 5 times on compiler, runtime, or incorrect answer verdicts, using detailed feedback to refine the solution.
- **Pushes to GitHub**: Automatically commits accepted solutions under the `solutions/` folder with rich headers containing metadata like runtime and memory beats percentages.
- **Web Dashboard**: Modern glassmorphic web frontend to monitor system status and trigger dispatches on-demand.

## Tech Stack
- **Languages**: Python 3.11, JavaScript (ES6)
- **AI Core**: Groq SDK (`llama-3.3-70b-versatile` model)
- **API integration**: LeetCode GraphQL & Submission REST API, GitHub REST API
- **Automation**: Playwright (for automated cookie refreshing)
- **CI/CD & Hosting**: GitHub Actions (runners), Vercel (frontend deployment)
- **Frameworks**: Next.js 16, React 19

## Project Structure
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
│   ├── README.md
│   ├── eslint.config.mjs
│   ├── jsconfig.json
│   ├── next.config.mjs
│   ├── package.json
│   ├── pages
│   │   ├── _app.js
│   │   ├── _document.js
│   │   ├── api
│   │   │   ├── daily.js
│   │   │   └── status.js
│   │   └── index.js
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
│   ├── 0239_sliding_window_maximum.py
│   └── 0860_design_circular_queue.py
└── vercel.json
```

## Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ayushcode001/shaka-laka.git
   cd shaka-laka
   ```
2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```
3. **Activate environment & Install dependencies:**
   - On Windows:
     ```powershell
     .\venv\Scripts\activate
     pip install -r requirements.txt
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     pip install -r requirements.txt
     ```
4. **Fill Environment variables:**
   Create a `.env` file in the root directory (see **Environment Variables** below).
5. **Run Locally:**
   - To solve specific problems:
     ```bash
     python main.py 1 42
     ```
   - To solve the daily challenge:
     ```bash
     python main.py --daily
     ```

## Environment Variables
Create a `.env` file in the root of the project with the following configuration:

| Variable | Description |
| :--- | :--- |
| `GROQ_API_KEY` | API Key for accessing Llama models on Groq. |
| `GITHUB_TOKEN` | Personal Access Token (PAT) with `repo` and `workflow` permissions. |
| `GITHUB_USERNAME` | Your GitHub account username. |
| `GITHUB_REPO` | Target repository name (`shaka-laka`). |
| `LEETCODE_EMAIL` | Email used to sign in to LeetCode (only for cookie refresh). |
| `LEETCODE_PASSWORD` | Password for LeetCode login (only for cookie refresh). |
| `LEETCODE_SESSION` | Session cookie value extracted from LeetCode. |
| `LEETCODE_CSRF_TOKEN`| CSRF token extracted from LeetCode. |

> Note: To automate fetching session cookies, run `python refresh_cookies.py`.

## Usage
- Run solver for specific problems:
  ```bash
  python main.py <problem_number1> <problem_number2> ...
  ```
- Run solver for daily challenge:
  ```bash
  python main.py --daily
  ```

## Frontend
The dashboard UI allows triggering the solver bot workflows remotely.

### Run Locally:
```bash
cd leetcode-frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### Deploy to Vercel:
The project is configured for easy deployment on Vercel using the root `vercel.json` settings. Add the following Environment Variables on Vercel to allow workflow triggers:
- `GITHUB_TOKEN`
- `GITHUB_USERNAME`
- `GITHUB_REPO`

## GitHub Actions
Workflows run inside GitHub Actions and use repository secrets for solver execution.

### Workflows:
- **`solve.yml`**: Dispatched manually or via frontend to solve specified space-separated problem IDs.
- **`daily.yml`**: Scheduled via cron to run automatically every day at 00:30 UTC. Can also be triggered manually.

### Required Secrets:
Go to **Settings > Secrets and variables > Actions** and add:
- `GROQ_API_KEY`
- `LEETCODE_SESSION`
- `LEETCODE_CSRF_TOKEN`
- `GITHUB_TOKEN`
- `GITHUB_USERNAME`
- `GITHUB_REPO`