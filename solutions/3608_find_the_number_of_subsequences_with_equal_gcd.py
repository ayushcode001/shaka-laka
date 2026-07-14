# 3608. Find the Number of Subsequences With Equal GCD
# Difficulty  : Hard
# Tags        : Array, Math, Dynamic Programming, Number Theory
# LeetCode    : https://leetcode.com/problems/find-the-number-of-subsequences-with-equal-gcd/
# Status      : Wrong Answer
# Runtime     : N/A
# Memory      : N/A
# Solved on   : 2026-07-14
# ─────────────────────────────────────────────────────────────

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        count = 0

        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        for mask1 in range(1, 1 << n):
            for mask2 in range(1, 1 << n):
                if mask1 & mask2 == mask1:
                    gcd_val1 = 0
                    gcd_val2 = 0
                    for i in range(n):
                        if (mask1 & (1 << i)) > 0:
                            if gcd_val1 == 0:
                                gcd_val1 = nums[i]
                            else:
                                gcd_val1 = gcd(gcd_val1, nums[i])
                    for i in range(n):
                        if (mask2 & (1 << i)) > 0:
                            if gcd_val2 == 0:
                                gcd_val2 = nums[i]
                            else:
                                gcd_val2 = gcd(gcd_val2, nums[i])
                    if gcd_val1 == gcd_val2:
                        count += 1

        return count % MOD