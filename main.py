from leetcode_client import fetch_problem, fetch_daily_problem
from groq_solver import solve_problem
from github_client import push_solution
from leetcode_submitter import submit_solution

MAX_RETRIES = 5  # ask Groq to fix if wrong answer

def run_problem(problem: dict):
    print(f"   {problem['title']} | {problem['difficulty']}")

    solution = None
    result = None

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
            break
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
            if attempt == MAX_RETRIES:
                print("   ⚠️  Max retries reached. Pushing best attempt anyway.")

    # Push to GitHub regardless, with result in the header comment
    print(f"\n📤 Pushing to GitHub...")
    push_solution(problem, solution, result)

def run(args: list[str]):
    if "--daily" in args:
        print("\n" + "="*50)
        print("📋 LeetCode Daily Challenge")
        try:
            problem = fetch_daily_problem()
            run_problem(problem)
        except Exception as e:
            print(f"Error fetching daily problem: {e}")
            raise
    else:
        for arg in args:
            try:
                num = int(arg)
            except ValueError:
                print(f"Invalid problem number: {arg}")
                continue
            print("\n" + "="*50)
            print(f"📋 Problem #{num}")
            try:
                problem = fetch_problem(num)
                run_problem(problem)
            except Exception as e:
                print(f"Error processing problem #{num}: {e}")
                continue

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])