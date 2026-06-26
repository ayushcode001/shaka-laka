# 860. Design Circular Queue
# Difficulty  : Medium
# Tags        : Array, Linked List, Design, Queue
# LeetCode    : https://leetcode.com/problems/design-circular-queue/
# Status      : Accepted
# Runtime     : 8 ms (beats 43.5%)
# Memory      : 20 MB (beats 26.5%)
# Solved on   : 2026-06-26
# ─────────────────────────────────────────────────────────────

# Approach: We will use a circular array to implement the queue. The array will have a fixed size, and we will use two pointers, one for the front and one for the rear of the queue. When the rear pointer reaches the end of the array, it will wrap around to the beginning.
# Time Complexity: O(1) for all operations
# Space Complexity: O(k) where k is the size of the queue

class MyCircularQueue:
    def __init__(self, k: int):
        self.k = k
        self.queue = [None] * k
        self.front = 0
        self.rear = 0
        self.size = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.queue[self.rear] = value
        self.rear = (self.rear + 1) % self.k
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.k
        self.size -= 1
        return True

    def Front(self) -> int:
        if self.isEmpty():
            return -1
        return self.queue[self.front]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self.queue[(self.rear - 1) % self.k]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.k

class Solution:
    def test_circular_queue(self):
        my_circular_queue = MyCircularQueue(3)
        print(my_circular_queue.enQueue(1))  # return True
        print(my_circular_queue.enQueue(2))  # return True
        print(my_circular_queue.enQueue(3))  # return True
        print(my_circular_queue.enQueue(4))  # return False
        print(my_circular_queue.Rear())     # return 3
        print(my_circular_queue.isFull())   # return True
        print(my_circular_queue.deQueue())  # return True
        print(my_circular_queue.enQueue(4)) # return True
        print(my_circular_queue.Rear())     # return 4

solution = Solution()
solution.test_circular_queue()