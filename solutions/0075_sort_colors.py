# 75. Sort Colors
# Difficulty  : Medium
# Tags        : Array, Two Pointers, Sorting
# LeetCode    : https://leetcode.com/problems/sort-colors/
# Status      : Accepted
# Runtime     : 0 ms (beats 100.0%)
# Memory      : 19.3 MB (beats 60.4%)
# Solved on   : 2026-06-27
# ─────────────────────────────────────────────────────────────

# Approach: We will use the Dutch National Flag algorithm, a three-way partitioning algorithm that works by maintaining four sections: 
#           - The section before the first pointer (p0) will contain all the 0s.
#           - The section between the two pointers (p0 and p2) will contain all the 1s.
#           - The section after the second pointer (p2) will contain all the 2s.
# Time Complexity: O(n), where n is the number of elements in the array.
# Space Complexity: O(1), as we are only using a constant amount of space.

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # Initialize two pointers, one at the start and one at the end of the array
        p0, p2 = 0, len(nums) - 1
        # Initialize the current pointer
        i = 0
        
        # Continue the process until the current pointer meets the second pointer
        while i <= p2:
            # If the current element is 0, swap it with the element at the first pointer and move both pointers forward
            if nums[i] == 0:
                nums[p0], nums[i] = nums[i], nums[p0]
                p0 += 1
                i += 1
            # If the current element is 2, swap it with the element at the second pointer and move the second pointer backward
            elif nums[i] == 2:
                nums[p2], nums[i] = nums[i], nums[p2]
                p2 -= 1
            # If the current element is 1, just move the current pointer forward
            else:
                i += 1