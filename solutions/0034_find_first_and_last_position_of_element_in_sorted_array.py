# 34. Find First and Last Position of Element in Sorted Array
# Difficulty  : Medium
# Tags        : Array, Binary Search
# LeetCode    : https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
# Status      : Accepted
# Runtime     : 0 ms (beats 100.0%)
# Memory      : 20.7 MB (beats 27.3%)
# Solved on   : 2026-07-04
# ─────────────────────────────────────────────────────────────

# Approach: We use binary search to find the first and last occurrence of the target in the sorted array.
# Time Complexity: O(log n)
# Space Complexity: O(1)

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def find_first(nums, target):
            left, right = 0, len(nums) - 1
            first_pos = -1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    first_pos = mid
                    right = mid - 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return first_pos

        def find_last(nums, target):
            left, right = 0, len(nums) - 1
            last_pos = -1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    last_pos = mid
                    left = mid + 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return last_pos

        first_pos = find_first(nums, target)
        last_pos = find_last(nums, target)
        return [first_pos, last_pos]