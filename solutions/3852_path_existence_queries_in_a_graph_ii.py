# 3852. Path Existence Queries in a Graph II
# Difficulty  : Hard
# Tags        : Array, Two Pointers, Binary Search, Dynamic Programming, Greedy, Bit Manipulation, Graph Theory, Sorting
# LeetCode    : https://leetcode.com/problems/path-existence-queries-in-a-graph-ii/
# Status      : Time Limit Exceeded
# Runtime     : N/A
# Memory      : N/A
# Solved on   : 2026-07-10
# ─────────────────────────────────────────────────────────────

from collections import deque
from typing import List

class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[int]:
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if abs(nums[i] - nums[j]) <= maxDiff:
                    graph[i].append(j)
                    graph[j].append(i)

        result = []
        for u, v in queries:
            if u == v:
                result.append(0)
                continue

            queue = deque([(u, 0)])
            visited = {u}
            while queue:
                node, distance = queue.popleft()
                if node == v:
                    result.append(distance)
                    break
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, distance + 1))
                        visited.add(neighbor)
            else:
                result.append(-1)

        return result