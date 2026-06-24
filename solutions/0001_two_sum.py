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