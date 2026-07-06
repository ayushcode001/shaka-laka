# 1222. Remove Covered Intervals
# Difficulty  : Medium
# Tags        : Array, Sorting
# LeetCode    : https://leetcode.com/problems/remove-covered-intervals/
# Status      : Accepted
# Runtime     : 0 ms (beats 100.0%)
# Memory      : 19.7 MB (beats 47.9%)
# Solved on   : 2026-07-06
# ─────────────────────────────────────────────────────────────

# Approach: Sort the intervals based on their start value and then compare the end values to determine if an interval is covered.
# Time Complexity: O(n log n) due to sorting
# Space Complexity: O(n) for sorting in the worst case

class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # Sort the intervals based on their start value and then compare the end values
        intervals.sort(key=lambda x: (x[0], -x[1]))
        
        # Initialize the count of remaining intervals and the end value of the previous interval
        count = 0
        prev_end = -1
        
        # Iterate over the sorted intervals
        for _, end in intervals:
            # If the current interval is not covered by the previous one, increment the count and update the previous end value
            if end > prev_end:
                count += 1
                prev_end = end
        
        # Return the count of remaining intervals
        return count