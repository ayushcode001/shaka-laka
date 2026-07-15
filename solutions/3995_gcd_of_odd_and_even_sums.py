# 3995. GCD of Odd and Even Sums
# Difficulty  : Easy
# Tags        : Math, Number Theory
# LeetCode    : https://leetcode.com/problems/gcd-of-odd-and-even-sums/
# Status      : Accepted
# Runtime     : 0 ms (beats 100.0%)
# Memory      : 19.3 MB (beats 53.0%)
# Solved on   : 2026-07-15
# ─────────────────────────────────────────────────────────────

# Approach: The problem can be solved by first calculating the sum of the smallest n positive odd numbers and the sum of the smallest n positive even numbers. 
# Then, we can use the math.gcd function to find the greatest common divisor of these two sums.
# Time Complexity: O(1)
# Space Complexity: O(1)
class Solution:
    def gcdOfOddEvenSums(self, n: int) -> int:
        # Calculate the sum of the smallest n positive odd numbers
        sumOdd = n ** 2
        
        # Calculate the sum of the smallest n positive even numbers
        sumEven = n * (n + 1)
        
        # Import the math module for the gcd function
        import math
        
        # Return the GCD of sumOdd and sumEven
        return math.gcd(sumOdd, sumEven)