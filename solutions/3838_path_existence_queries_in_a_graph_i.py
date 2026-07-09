# 3838. Path Existence Queries in a Graph I
# Difficulty  : Medium
# Tags        : Array, Hash Table, Binary Search, Union-Find, Graph Theory
# LeetCode    : https://leetcode.com/problems/path-existence-queries-in-a-graph-i/
# Status      : Accepted
# Runtime     : 318 ms (beats 31.7%)
# Memory      : 50.8 MB (beats 28.6%)
# Solved on   : 2026-07-09
# ─────────────────────────────────────────────────────────────

from typing import List

class Solution:
    # Approach: We use a union-find data structure to keep track of the connected components in the graph.
    # Time Complexity: O(n * m * alpha(n)) where n is the number of nodes, m is the number of queries, and alpha(n) is the inverse Ackermann function.
    # Space Complexity: O(n + m) where n is the number of nodes and m is the number of queries.
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[bool]:
        class UnionFind:
            def __init__(self, n):
                self.parent = list(range(n))
                self.rank = [0] * n

            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])
                return self.parent[x]

            def union(self, x, y):
                root_x, root_y = self.find(x), self.find(y)
                if root_x != root_y:
                    if self.rank[root_x] > self.rank[root_y]:
                        self.parent[root_y] = root_x
                    elif self.rank[root_x] < self.rank[root_y]:
                        self.parent[root_x] = root_y
                    else:
                        self.parent[root_y] = root_x
                        self.rank[root_x] += 1

        uf = UnionFind(n)
        for i in range(n - 1):
            if nums[i + 1] - nums[i] <= maxDiff:
                uf.union(i, i + 1)

        result = []
        for u, v in queries:
            result.append(uf.find(u) == uf.find(v))

        return result