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

    # Step 1: Submit
    url = f"{BASE}/problems/{title_slug}/submit/"
    payload = {
        "lang": "python3",
        "question_id": question_id,
        "typed_code": code,
    }
    resp = session.post(url, json=payload)
    resp.raise_for_status()
    submission_id = resp.json().get("submission_id")

    if not submission_id:
        raise ValueError(f"No submission_id returned: {resp.text}")

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
        result["error"] = data.get("full_compile_error") \
                       or data.get("full_runtime_error") \
                       or data.get("last_testcase")

    return result