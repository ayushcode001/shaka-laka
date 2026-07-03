# 23. Merge k Sorted Lists
# Difficulty  : Hard
# Tags        : Linked List, Divide and Conquer, Heap (Priority Queue), Merge Sort
# LeetCode    : https://leetcode.com/problems/merge-k-sorted-lists/
# Status      : Accepted
# Runtime     : 11 ms (beats 54.9%)
# Memory      : 22.9 MB (beats 45.9%)
# Solved on   : 2026-07-04
# ─────────────────────────────────────────────────────────────

# Approach: We will use a min-heap to store the current smallest node from each linked list. This approach ensures that we always select the smallest node to add to our result list, thus maintaining the sorted order.
# Time Complexity: O(N log k), where N is the total number of nodes across all linked lists and k is the number of linked lists. This is because we perform a heap operation for each node.
# Space Complexity: O(k), as we need to store k nodes in the heap at any given time.

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Create a min-heap to store the current smallest node from each linked list
        min_heap = []
        
        # Add the head of each linked list to the min-heap
        for i, node in enumerate(lists):
            if node:
                # Store a tuple containing the node's value, the list index, and the node itself
                # This allows us to break ties based on the list index
                heapq.heappush(min_heap, (node.val, i, node))
        
        # Create a dummy node to serve as the head of our result list
        dummy = ListNode()
        current = dummy
        
        # Continue until the min-heap is empty
        while min_heap:
            # Extract the smallest node from the min-heap
            val, list_index, node = heapq.heappop(min_heap)
            
            # Add the extracted node to our result list
            current.next = node
            current = current.next
            
            # If the extracted node has a next node, add it to the min-heap
            if node.next:
                heapq.heappush(min_heap, (node.next.val, list_index, node.next))
        
        # Return the next node of the dummy node, which is the head of our result list
        return dummy.next