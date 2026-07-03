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