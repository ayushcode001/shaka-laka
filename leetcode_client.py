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