# 239. Sliding Window Maximum
# Difficulty  : Hard
# Tags        : Array, Queue, Sliding Window, Heap (Priority Queue), Monotonic Queue
# LeetCode    : https://leetcode.com/problems/sliding-window-maximum/
# Status      : Accepted
# Runtime     : 639 ms (beats 5.0%)
# Memory      : 34.5 MB (beats 94.9%)
# Solved on   : 2026-06-26
# ─────────────────────────────────────────────────────────────

# Approach: We use a deque to store the indices of the elements in the current window. 
# The deque is maintained in such a way that the front always contains the index of the maximum element in the current window.
# Time Complexity: O(n)
# Space Complexity: O(n)

class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        # Initialize an empty list to store the maximum values
        max_values = []
        
        # Initialize a deque to store the indices of the elements in the current window
        window = []
        
        # Iterate over the list of numbers
        for i, num in enumerate(nums):
            # Remove the indices of the elements that are out of the current window
            while window and window[0] <= i - k:
                window.pop(0)
            
            # Remove the indices of the elements that are smaller than the current element
            while window and nums[window[-1]] < num:
                window.pop()
            
            # Add the index of the current element to the window
            window.append(i)
            
            # If the window is full, add the maximum value to the list of maximum values
            if i >= k - 1:
                max_values.append(nums[window[0]])
        
        # Return the list of maximum values
        return max_values