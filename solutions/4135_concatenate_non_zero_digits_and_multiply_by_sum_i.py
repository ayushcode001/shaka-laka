# 4135. Concatenate Non-Zero Digits and Multiply by Sum I
# Difficulty  : Easy
# Tags        : Math
# LeetCode    : https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-i/
# Status      : Accepted
# Runtime     : 0 ms (beats 100.0%)
# Memory      : 19.2 MB (beats 51.2%)
# Solved on   : 2026-07-07
# ─────────────────────────────────────────────────────────────

# Approach: The problem can be solved by first extracting the non-zero digits from the given integer, 
# then calculating the sum of these digits, and finally multiplying the concatenated non-zero digits by the sum.
# Time Complexity: O(log n) because we are processing each digit of the number once.
# Space Complexity: O(log n) because in the worst case, we might have to store all the digits of the number.

class Solution:
    def sumAndMultiply(self, n: int) -> int:
        # Convert the integer to a string to easily extract each digit
        str_n = str(n)
        
        # Initialize an empty string to store the non-zero digits
        non_zero_digits = ""
        
        # Initialize a variable to store the sum of the non-zero digits
        sum_of_digits = 0
        
        # Iterate over each character (digit) in the string
        for digit in str_n:
            # Check if the digit is not zero
            if digit != '0':
                # Append the non-zero digit to the string
                non_zero_digits += digit
                # Add the integer value of the digit to the sum
                sum_of_digits += int(digit)
        
        # If there are no non-zero digits, return 0
        if non_zero_digits == "":
            return 0
        # Otherwise, return the product of the concatenated non-zero digits and the sum of the digits
        else:
            # Convert the string of non-zero digits back to an integer
            x = int(non_zero_digits)
            # Return the product of x and the sum of the digits
            return x * sum_of_digits