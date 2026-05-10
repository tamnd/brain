---
title: "LeetCode 01xx"
description: "LeetCode practice notes for problems 100 through 174, including A detailed guide to solving Same Tree with recursive DFS and structural comparison."
tags: ["leetcode", "algorithms", "practice"]
weight: 1
---

# LeetCode 01xx

| # | Title | Difficulty | Description |
|---|---|---|---|
| 100 | [LeetCode 100: Same Tree](0100.md) | Easy | A detailed guide to solving Same Tree with recursive DFS and structural comparison. |
| 101 | [LeetCode 101: Symmetric Tree](0101.md) | Easy | A clear explanation of checking whether a binary tree is symmetric using mirror recursion. |
| 102 | [LeetCode 102: Binary Tree Level Order Traversal](0102.md) | Medium | A clear explanation of binary tree level order traversal using breadth-first search and a queue. |
| 103 | [LeetCode 103: Binary Tree Zigzag Level Order Traversal](0103.md) | Medium | A clear explanation of zigzag level order traversal using breadth-first search and alternating level direction. |
| 104 | [LeetCode 104: Maximum Depth of Binary Tree](0104.md) | Easy | A clear explanation of finding the maximum depth of a binary tree using recursive depth-first search. |
| 105 | [LeetCode 105: Construct Binary Tree from Preorder and Inorder Traversal](0105.md) | Medium | A clear explanation of rebuilding a binary tree from preorder and inorder traversals using recursion and an index map. |
| 106 | [LeetCode 106: Construct Binary Tree from Inorder and Postorder Traversal](0106.md) | Medium | A clear explanation of rebuilding a binary tree from inorder and postorder traversals using recursion and an index map. |
| 107 | [LeetCode 107: Binary Tree Level Order Traversal II](0107.md) | Medium | A clear explanation of returning binary tree levels from bottom to top using breadth-first search. |
| 108 | [LeetCode 108: Convert Sorted Array to Binary Search Tree](0108.md) | Easy | A clear explanation of building a height-balanced binary search tree from a sorted array using divide and conquer. |
| 109 | [LeetCode 109: Convert Sorted List to Binary Search Tree](0109.md) | Medium | A clear explanation of converting a sorted linked list into a height-balanced binary search tree using slow and fast pointers. |
| 110 | [LeetCode 110: Balanced Binary Tree](0110.md) | Easy | A clear explanation of checking whether a binary tree is height-balanced using bottom-up depth-first search. |
| 111 | [LeetCode 111: Minimum Depth of Binary Tree](0111.md) | Easy | A clear explanation of finding the minimum depth of a binary tree using breadth-first search. |
| 112 | [LeetCode 112: Path Sum](0112.md) | Easy | A clear explanation of checking whether a binary tree has a root-to-leaf path whose values add up to a target sum. |
| 113 | [LeetCode 113: Path Sum II](0113.md) | Medium | A clear explanation of finding all root-to-leaf paths whose values add up to a target sum using depth-first search and backtracking. |
| 114 | [LeetCode 114: Flatten Binary Tree to Linked List](0114.md) | Medium | A clear explanation of flattening a binary tree into a linked list in preorder traversal order using recursive depth-first search. |
| 115 | [LeetCode 115: Distinct Subsequences](0115.md) | Hard | A clear explanation of counting distinct subsequences using dynamic programming. |
| 116 | [LeetCode 116: Populating Next Right Pointers in Each Node](0116.md) | Medium | A clear explanation of connecting next pointers in a perfect binary tree using constant extra space. |
| 117 | [LeetCode 117: Populating Next Right Pointers in Each Node II](0117.md) | Medium | A clear explanation of connecting next pointers in any binary tree using constant extra space. |
| 118 | [LeetCode 118: Pascal's Triangle](0118.md) | Easy | A clear explanation of generating Pascal's Triangle row by row using dynamic programming. |
| 119 | [LeetCode 119: Pascal's Triangle II](0119.md) | Easy | A clear explanation of generating a single row of Pascal's Triangle using in-place dynamic programming. |
| 120 | [LeetCode 120: Triangle](0120.md) | Medium | A clear explanation of finding the minimum path sum in a triangle using bottom-up dynamic programming. |
| 121 | [LeetCode 121: Best Time to Buy and Sell Stock](0121.md) | Easy | A clear explanation of finding the maximum profit from one stock transaction using a single pass. |
| 122 | [LeetCode 122: Best Time to Buy and Sell Stock II](0122.md) | Medium | A clear explanation of maximizing stock profit with unlimited transactions using a greedy single-pass method. |
| 123 | [LeetCode 123: Best Time to Buy and Sell Stock III](0123.md) | Hard | A clear explanation of maximizing stock profit with at most two transactions using dynamic programming. |
| 124 | [LeetCode 124: Binary Tree Maximum Path Sum](0124.md) | Hard | A clear explanation of finding the maximum path sum in a binary tree using bottom-up depth-first search. |
| 125 | [LeetCode 125: Valid Palindrome](0125.md) | Easy | A clear explanation of checking whether a string is a palindrome after ignoring non-alphanumeric characters and case. |
| 126 | [LeetCode 126: Word Ladder II](0126.md) | Hard | Find all shortest word transformation sequences using BFS to build shortest-path parents, then backtracking to reconstruct every answer. |
| 127 | [LeetCode 127: Word Ladder](0127.md) | Hard | Use breadth-first search to find the shortest transformation sequence length between two words. |
| 128 | [LeetCode 128: Longest Consecutive Sequence](0128.md) | Medium | Find the longest run of consecutive integers in an unsorted array using a hash set and sequence-start detection. |
| 129 | [LeetCode 129: Sum Root to Leaf Numbers](0129.md) | Medium | Compute the sum of all numbers formed by root-to-leaf paths using depth-first search and decimal accumulation. |
| 130 | [LeetCode 130: Surrounded Regions](0130.md) | Medium | Capture surrounded O regions by marking border-connected O cells first, then flipping the remaining O cells. |
| 131 | [LeetCode 131: Palindrome Partitioning](0131.md) | Medium | Generate all ways to split a string so that every piece is a palindrome, using backtracking with palindrome precomputation. |
| 132 | [LeetCode 132: Palindrome Partitioning II](0132.md) | Hard | Find the minimum number of cuts needed to split a string into palindromic substrings using palindrome precomputation and dynamic programming. |
| 133 | [LeetCode 133: Clone Graph](0133.md) | Medium | Create a deep copy of a connected undirected graph using DFS and a hash map from original nodes to cloned nodes. |
| 134 | [LeetCode 134: Gas Station](0134.md) | Medium | Find the unique starting gas station index using a greedy scan with total fuel balance and current tank balance. |
| 135 | [LeetCode 135: Candy](0135.md) | Hard | Compute the minimum candies needed using two greedy passes, one from the left and one from the right. |
| 136 | [LeetCode 136: Single Number](0136.md) | Easy | Find the only number that appears once using the XOR operator, while every other number appears exactly twice. |
| 137 | [LeetCode 137: Single Number II](0137.md) | Medium | Find the number that appears once when every other number appears three times using bit counting or finite-state bit manipulation. |
| 138 | [LeetCode 138: Copy List with Random Pointer](0138.md) | Medium | Create a deep copy of a linked list with next and random pointers using hash maps or interleaved node cloning. |
| 139 | [LeetCode 139: Word Break](0139.md) | Medium | Decide whether a string can be segmented into dictionary words using dynamic programming over prefixes. |
| 140 | [LeetCode 140: Word Break II](0140.md) | Hard | Return all valid sentences formed by inserting spaces into a string so every word belongs to the dictionary, using DFS with memoization. |
| 141 | [LeetCode 141: Linked List Cycle](0141.md) | Easy | Detect whether a linked list contains a cycle using Floyd’s tortoise and hare two-pointer algorithm. |
| 142 | [LeetCode 142: Linked List Cycle II](0142.md) | Medium | Find the node where a linked list cycle begins using Floyd’s tortoise and hare algorithm with cycle entry mathematics. |
| 143 | [LeetCode 143: Reorder List](0143.md) | Medium | Reorder a singly linked list in-place by finding the middle, reversing the second half, and merging the two halves alternately. |
| 144 | [LeetCode 144: Binary Tree Preorder Traversal](0144.md) | Easy | Return the preorder traversal of a binary tree using recursion or an explicit stack. |
| 145 | [LeetCode 145: Binary Tree Postorder Traversal](0145.md) | Easy | Return the postorder traversal of a binary tree using recursion or an iterative stack-based approach. |
| 146 | [LeetCode 146: LRU Cache](0146.md) | Medium | Design an LRU cache with O(1) get and put operations using a hash map and doubly linked list. |
| 147 | [LeetCode 147: Insertion Sort List](0147.md) | Medium | Sort a singly linked list using insertion sort by splicing each node into a growing sorted list. |
| 148 | [LeetCode 148: Sort List](0148.md) | Medium | Sort a singly linked list in ascending order using merge sort with fast and slow pointers. |
| 149 | [LeetCode 149: Max Points on a Line](0149.md) | Hard | Find the maximum number of points lying on the same straight line using slope counting and normalization. |
| 150 | [LeetCode 150: Evaluate Reverse Polish Notation](0150.md) | Medium | Evaluate an arithmetic expression written in Reverse Polish Notation using a stack. |
| 151 | [LeetCode 151: Reverse Words in a String](0151.md) | Medium | A clear explanation of reversing word order while removing extra spaces. |
| 152 | [LeetCode 152: Maximum Product Subarray](0152.md) | Medium | A detailed explanation of tracking both maximum and minimum products while scanning the array. |
| 153 | [LeetCode 153: Find Minimum in Rotated Sorted Array](0153.md) | Medium | A clear explanation of finding the minimum element in a rotated sorted array using binary search. |
| 154 | [LeetCode 154: Find Minimum in Rotated Sorted Array II](0154.md) | Hard | A clear explanation of finding the minimum element in a rotated sorted array that may contain duplicates. |
| 155 | [LeetCode 155: Min Stack](0155.md) | Medium | A clear explanation of designing a stack that can return the current minimum element in constant time. |
| 156 | [LeetCode 156: Binary Tree Upside Down](0156.md) | Medium | A clear explanation of flipping a binary tree upside down by rewiring pointers from the left spine. |
| 157 | [LeetCode 157: Read N Characters Given Read4](0157.md) | Easy | A clear explanation of implementing read using the given read4 API and copying only the needed characters. |
| 158 | [LeetCode 158: Read N Characters Given read4 II - Call Multiple Times](0158.md) | Hard | A clear explanation of implementing read with read4 when read may be called multiple times. |
| 159 | [LeetCode 159: Longest Substring with At Most Two Distinct Characters](0159.md) | Medium | A clear explanation of finding the longest substring with at most two distinct characters using a sliding window. |
| 160 | [LeetCode 160: Intersection of Two Linked Lists](0160.md) | Easy | A clear explanation of finding the node where two singly linked lists intersect using two pointers. |
| 161 | [LeetCode 161: One Edit Distance](0161.md) | Medium | A clear explanation of checking whether two strings are exactly one edit apart using a linear scan. |
| 162 | [LeetCode 162: Find Peak Element](0162.md) | Medium | A clear explanation of finding any peak element using binary search on the slope of the array. |
| 163 | [LeetCode 163: Missing Ranges](0163.md) | Easy | A clear explanation of finding all missing ranges inside an inclusive interval by scanning sorted unique numbers. |
| 164 | [LeetCode 164: Maximum Gap](0164.md) | Medium | A clear explanation of finding the maximum adjacent gap in sorted order using buckets and the pigeonhole principle. |
| 165 | [LeetCode 165: Compare Version Numbers](0165.md) | Medium | A clear explanation of comparing version strings revision by revision while ignoring leading zeros. |
| 166 | [LeetCode 166: Fraction to Recurring Decimal](0166.md) | Medium | A clear explanation of converting a fraction into decimal form and detecting repeating fractional parts with a hash map. |
| 167 | [LeetCode 167: Two Sum II - Input Array Is Sorted](0167.md) | Medium | A clear explanation of finding two numbers in a sorted array using two pointers and constant extra space. |
| 168 | [LeetCode 168: Excel Sheet Column Title](0168.md) | Easy | A clear explanation of converting a positive integer into an Excel column title using bijective base 26. |
| 169 | [LeetCode 169: Majority Element](0169.md) | Easy | A clear explanation of finding the element that appears more than half the time using Boyer-Moore voting. |
| 170 | [LeetCode 170: Two Sum III - Data Structure Design](0170.md) | Easy | A clear explanation of designing a data structure that supports add and find operations for pair sums. |
| 171 | [LeetCode 171: Excel Sheet Column Number](0171.md) | Easy | A clear explanation of converting an Excel column title into its numeric index using base 26 accumulation. |
| 172 | [LeetCode 172: Factorial Trailing Zeroes](0172.md) | Medium | A clear explanation of counting trailing zeroes in n! by counting factors of 5 instead of computing the factorial directly. |
| 173 | [LeetCode 173: Binary Search Tree Iterator](0173.md) | Medium | A clear explanation of designing an iterator over a BST using controlled inorder traversal with a stack. |
| 174 | [LeetCode 174: Dungeon Game](0174.md) | Hard | A clear explanation of computing the minimum initial health needed to survive a dungeon using reverse dynamic programming. |
