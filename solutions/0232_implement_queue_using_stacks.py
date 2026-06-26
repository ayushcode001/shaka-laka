# 232. Implement Queue using Stacks
# Difficulty  : Easy
# Tags        : Stack, Design, Queue
# LeetCode    : https://leetcode.com/problems/implement-queue-using-stacks/
# Status      : Accepted
# Runtime     : 0 ms (beats 100.0%)
# Memory      : 19.5 MB (beats 50.8%)
# Solved on   : 2026-06-26
# ─────────────────────────────────────────────────────────────

# Approach: We use two stacks to implement a queue. The first stack is used to store new elements and the second stack is used to store the elements in the correct order for a queue. 
# Time Complexity: O(1) amortized for push, pop, peek, and empty operations.
# Space Complexity: O(n) where n is the number of elements in the queue.

class MyQueue:

    def __init__(self):
        # Initialize two empty stacks
        self.stack1 = []
        self.stack2 = []

    def push(self, x: int) -> None:
        # Push the new element onto the first stack
        self.stack1.append(x)

    def pop(self) -> int:
        # If the second stack is empty, we need to move all elements from the first stack to the second stack
        if not self.stack2:
            while self.stack1:
                # Pop the top element from the first stack and push it onto the second stack
                self.stack2.append(self.stack1.pop())
        # If the second stack is still empty after moving elements, the queue is empty
        if not self.stack2:
            raise IndexError("Cannot pop from an empty queue")
        # Pop and return the top element from the second stack
        return self.stack2.pop()

    def peek(self) -> int:
        # If the second stack is empty, we need to move all elements from the first stack to the second stack
        if not self.stack2:
            while self.stack1:
                # Pop the top element from the first stack and push it onto the second stack
                self.stack2.append(self.stack1.pop())
        # If the second stack is still empty after moving elements, the queue is empty
        if not self.stack2:
            raise IndexError("Cannot peek an empty queue")
        # Return the top element from the second stack without removing it
        return self.stack2[-1]

    def empty(self) -> bool:
        # Check if both stacks are empty
        return not (self.stack1 or self.stack2)