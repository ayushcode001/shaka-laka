# 1256. Rank Transform of an Array
# Difficulty  : Easy
# Tags        : Array, Hash Table, Sorting
# LeetCode    : https://leetcode.com/problems/rank-transform-of-an-array/
# Status      : Accepted
# Runtime     : 31 ms (beats 93.3%)
# Memory      : 37.8 MB (beats 21.8%)
# Solved on   : 2026-07-12
# ─────────────────────────────────────────────────────────────

# Approach: We will use a hash table to store the rank of each unique element in the array. 
#           The rank will be determined by sorting the unique elements and then assigning 
#           the rank based on the index in the sorted list. 
# Time Complexity: O(n log n) due to sorting
# Space Complexity: O(n) for storing the hash table and the sorted list

class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        # Create a hash table to store the rank of each unique element
        rank_hash = {}
        
        # Create a sorted list of unique elements
        sorted_arr = sorted(set(arr))
        
        # Assign the rank to each unique element
        for i, num in enumerate(sorted_arr):
            rank_hash[num] = i + 1
        
        # Replace each element in the array with its rank
        return [rank_hash[num] for num in arr]