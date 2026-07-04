# 98. Validate Binary Search Tree
# Difficulty  : Medium
# Tags        : Tree, Depth-First Search, Binary Search Tree, Binary Tree
# LeetCode    : https://leetcode.com/problems/validate-binary-search-tree/
# Status      : Accepted
# Runtime     : 0 ms (beats 100.0%)
# Memory      : 20.8 MB (beats 73.6%)
# Solved on   : 2026-07-04
# ─────────────────────────────────────────────────────────────

# Approach: We will use a recursive approach to validate the binary search tree. 
#           For each node, we will check if its value is within the valid range 
#           defined by its ancestors. If it is, we will recursively check its 
#           left and right subtrees.
# Time Complexity: O(n), where n is the number of nodes in the tree, since we visit each node once.
# Space Complexity: O(h), where h is the height of the tree, due to the recursive call stack.

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node, low, high):
            # Base case: an empty tree is a valid BST
            if not node:
                return True
            
            # If the current node's value is not within the valid range, return False
            if node.val <= low or node.val >= high:
                return False
            
            # Recursively validate the left and right subtrees with updated valid ranges
            return (validate(node.left, low, node.val) and 
                    validate(node.right, node.val, high))
        
        # Initialize the valid range for the root node
        return validate(root, float('-inf'), float('inf'))