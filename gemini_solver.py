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

Requirements:
- Write a complete Python solution inside a class Solution
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

Fix the solution. Think carefully about the edge case that failed.
Return ONLY the corrected Python code. No markdown, no backticks.
"""

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def solve_problem(problem: dict, previous_result: dict = None, previous_code: str = None) -> str:
    if previous_result and previous_result.get("status") != "Accepted" and previous_code:
        prompt = RETRY_PROMPT.format(
            id=problem.get("questionId", "?"),
            title=problem["title"],
            status=previous_result.get("status", "Wrong Answer"),
            error=previous_result.get("error") or previous_result.get("last_testcase") or "Unknown error",
            previous_code=previous_code
        )
    else:
        tags = ", ".join(t["name"] for t in problem.get("topicTags", []))
        prompt = PROMPT_TEMPLATE.format(
            id=problem.get("questionId", "?"),
            title=problem["title"],
            difficulty=problem["difficulty"],
            tags=tags or "N/A",
            content=clean_html(problem.get("content", ""))
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