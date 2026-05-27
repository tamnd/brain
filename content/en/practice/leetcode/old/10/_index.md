---
title: "LeetCode 10xx"
description: "LeetCode practice notes for problems 1000 through 1100, covering interval DP, sliding window, binary search, greedy, SQL, and more."
tags: ["leetcode", "algorithms", "practice"]
weight: 10
---

# LeetCode 10xx

| # | Title | Difficulty | Description |
|---|---|---|---|
| 1000 | [LeetCode 1000: Minimum Cost to Merge Stones](1000.md) | Hard | A clear explanation of merging consecutive stone piles with minimum cost using interval dynamic programming. |
| 1001 | [LeetCode 1001: Grid Illumination](1001.md) | Hard | A clear explanation of simulating lamp illumination on a grid using hash maps for rows, columns, and diagonals. |
| 1002 | [LeetCode 1002: Find Common Characters](1002.md) | Easy | A clear explanation of finding characters that appear in all words using minimum frequency counts. |
| 1003 | [LeetCode 1003: Check If Word Is Valid After Substitutions](1003.md) | Medium | A clear explanation of validating a string by repeatedly removing 'abc' substrings using a stack. |
| 1004 | [LeetCode 1004: Max Consecutive Ones III](1004.md) | Medium | A clear explanation of finding the longest subarray of ones by flipping at most k zeros using a sliding window. |
| 1005 | [LeetCode 1005: Maximize Sum Of Array After K Negations](1005.md) | Easy | A clear explanation of maximizing array sum after exactly k negations using a greedy strategy. |
| 1006 | [LeetCode 1006: Clumsy Factorial](1006.md) | Medium | A clear explanation of computing the clumsy factorial by simulating cyclic operators with a stack. |
| 1007 | [LeetCode 1007: Minimum Domino Rotations For Equal Row](1007.md) | Medium | A clear explanation of finding minimum rotations to make all tops or bottoms equal using a greedy candidate check. |
| 1008 | [LeetCode 1008: Construct Binary Search Tree from Preorder Traversal](1008.md) | Medium | A clear explanation of reconstructing a BST from its preorder traversal using value range bounds. |
| 1009 | [LeetCode 1009: Complement of Base 10 Integer](1009.md) | Easy | A clear explanation of finding the complement of a number by XORing with a bitmask of the same bit length. |
| 1010 | [LeetCode 1010: Pairs of Songs With Total Durations Divisible by 60](1010.md) | Medium | A clear explanation of counting song pairs whose total duration is divisible by 60 using remainder frequency counting. |
| 1011 | [LeetCode 1011: Capacity To Ship Packages Within D Days](1011.md) | Medium | A clear explanation of finding the minimum ship capacity to deliver all packages within D days using binary search. |
| 1012 | [LeetCode 1012: Numbers With Repeated Digits](1012.md) | Hard | A clear explanation of counting numbers up to n with at least one repeated digit using digit DP and combinatorics. |
| 1013 | [LeetCode 1013: Partition Array Into Three Parts With Equal Sum](1013.md) | Easy | A clear explanation of checking if an array can be split into three contiguous parts with equal sum using a greedy two-pass approach. |
| 1014 | [LeetCode 1014: Best Sightseeing Pair](1014.md) | Medium | A clear explanation of maximizing the sightseeing score by tracking the best left value seen so far in a single pass. |
| 1015 | [LeetCode 1015: Smallest Integer Divisible by K](1015.md) | Medium | A clear explanation of finding the smallest repunit divisible by K by tracking remainders to detect cycles. |
| 1016 | [LeetCode 1016: Binary String With Substrings Representing 1 To N](1016.md) | Medium | A clear explanation of checking whether a binary string contains all binary representations of integers from 1 to n. |
| 1017 | [LeetCode 1017: Convert to Base -2](1017.md) | Medium | A clear explanation of converting a non-negative integer to its base negative-two representation. |
| 1018 | [LeetCode 1018: Binary Prefix Divisible By 5](1018.md) | Easy | A clear explanation of checking divisibility of binary prefixes by 5 using running remainder tracking. |
| 1019 | [LeetCode 1019: Next Greater Node In Linked List](1019.md) | Medium | A clear explanation of finding the next greater value for each node in a linked list using a monotonic stack. |
| 1020 | [LeetCode 1020: Number of Enclaves](1020.md) | Medium | A clear explanation of counting land cells unreachable from the grid border using BFS from boundary land cells. |
| 1021 | [LeetCode 1021: Remove Outermost Parentheses](1021.md) | Easy | A clear explanation of removing outermost parentheses from each primitive decomposition by tracking nesting depth. |
| 1022 | [LeetCode 1022: Sum of Root To Leaf Binary Numbers](1022.md) | Easy | A clear explanation of summing root-to-leaf binary numbers in a binary tree using DFS with accumulated values. |
| 1023 | [LeetCode 1023: Camelcase Matching](1023.md) | Medium | A clear explanation of checking camelCase pattern matching by verifying uppercase consistency with a two-pointer approach. |
| 1024 | [LeetCode 1024: Video Stitching](1024.md) | Medium | A clear explanation of finding the minimum number of video clips to cover a time range using a greedy interval covering approach. |
| 1025 | [LeetCode 1025: Divisor Game](1025.md) | Easy | A clear explanation of why Alice wins the divisor game if and only if n is even, proven by mathematical induction. |
| 1026 | [LeetCode 1026: Maximum Difference Between Node and Ancestor](1026.md) | Medium | A clear explanation of finding the maximum ancestor-node difference in a binary tree by tracking min and max along each root-to-leaf path. |
| 1027 | [LeetCode 1027: Longest Arithmetic Subsequence](1027.md) | Medium | A clear explanation of finding the longest arithmetic subsequence in an array using dynamic programming with difference hash maps. |
| 1028 | [LeetCode 1028: Recover a Tree From Preorder Traversal](1028.md) | Hard | A clear explanation of reconstructing a binary tree from a depth-encoded preorder traversal string using a stack. |
| 1029 | [LeetCode 1029: Two City Scheduling](1029.md) | Medium | A clear explanation of minimizing total travel cost for two-city scheduling using a greedy refund approach after sending everyone to city A. |
| 1030 | [LeetCode 1030: Matrix Cells in Distance Order](1030.md) | Easy | A clear explanation of sorting matrix cells by Chebyshev distance from a given center cell using BFS. |
| 1031 | [LeetCode 1031: Maximum Sum of Two Non-Overlapping Subarrays](1031.md) | Medium | A clear explanation of finding two non-overlapping subarrays with maximum combined sum using prefix sums and running maximums. |
| 1032 | [LeetCode 1032: Stream of Characters](1032.md) | Hard | A clear explanation of efficiently querying a stream of characters against a word list using an Aho-Corasick trie. |
| 1033 | [LeetCode 1033: Moving Stones Until Consecutive](1033.md) | Easy | A clear explanation of finding the minimum and maximum moves to make three stones consecutive by analyzing gap cases. |
| 1034 | [LeetCode 1034: Coloring A Border](1034.md) | Medium | A clear explanation of coloring the border of a connected component in a grid using BFS. |
| 1035 | [LeetCode 1035: Uncrossed Lines](1035.md) | Medium | A clear explanation of maximizing uncrossed connecting lines between two arrays using longest common subsequence dynamic programming. |
| 1036 | [LeetCode 1036: Escape a Large Maze](1036.md) | Hard | A clear explanation of determining if a source can reach a target in a very large grid with blocked cells using BFS with a cell count limit. |
| 1037 | [LeetCode 1037: Valid Boomerang](1037.md) | Easy | A clear explanation of checking if three points form a boomerang (non-collinear) using the cross product. |
| 1038 | [LeetCode 1038: Binary Search Tree to Greater Sum Tree](1038.md) | Medium | A clear explanation of converting a BST to a greater sum tree by accumulating values in reverse inorder traversal. |
| 1039 | [LeetCode 1039: Minimum Score Triangulation of Polygon](1039.md) | Medium | A clear explanation of minimizing the total score of triangulating a polygon using interval dynamic programming. |
| 1040 | [LeetCode 1040: Moving Stones Until Consecutive II](1040.md) | Medium | A clear explanation of finding minimum and maximum moves to make stones consecutive using a sliding window. |
| 1041 | [LeetCode 1041: Robot Bounded In Circle](1041.md) | Medium | A clear explanation of determining if a robot stays in a bounded circle by checking position and direction after one instruction cycle. |
| 1042 | [LeetCode 1042: Flower Planting With No Adjacent](1042.md) | Medium | A clear explanation of assigning 4 flower types to garden nodes with no adjacent conflicts using greedy graph coloring. |
| 1043 | [LeetCode 1043: Partition Array for Maximum Sum](1043.md) | Medium | A clear explanation of maximizing array sum by partitioning into subarrays of at most k elements, each filled with their maximum value, using dynamic programming. |
| 1044 | [LeetCode 1044: Longest Duplicate Substring](1044.md) | Hard | A clear explanation of finding the longest duplicate substring using binary search on length combined with Rabin-Karp rolling hash. |
| 1045 | [LeetCode 1045: Customers Who Bought All Products](1045.md) | Medium | A clear explanation of finding customers who purchased every product in the catalog using GROUP BY and HAVING with COUNT DISTINCT. |
| 1046 | [LeetCode 1046: Last Stone Weight](1046.md) | Easy | A clear explanation of simulating stone smashing to find the last remaining weight using a max heap. |
| 1047 | [LeetCode 1047: Remove All Adjacent Duplicates In String](1047.md) | Easy | A clear explanation of eliminating adjacent duplicate character pairs from a string using a stack. |
| 1048 | [LeetCode 1048: Longest String Chain](1048.md) | Medium | A clear explanation of finding the longest word chain where each word is formed by inserting one letter into the previous word, using dynamic programming. |
| 1049 | [LeetCode 1049: Last Stone Weight II](1049.md) | Medium | A clear explanation of minimizing the last stone weight by splitting stones into two groups using 0/1 knapsack dynamic programming. |
| 1050 | [LeetCode 1050: Actors and Directors Who Cooperated At Least Three Times](1050.md) | Easy | A clear explanation of finding actor-director pairs with at least three collaborations using GROUP BY and HAVING. |
| 1051 | [LeetCode 1051: Height Checker](1051.md) | Easy | A clear explanation of counting students not in the expected height order by comparing the array to its sorted version. |
| 1052 | [LeetCode 1052: Grumpy Bookstore Owner](1052.md) | Medium | A clear explanation of maximizing satisfied customers by choosing the best window for the owner to not be grumpy using a sliding window. |
| 1053 | [LeetCode 1053: Previous Permutation With One Swap](1053.md) | Medium | A clear explanation of finding the lexicographically largest permutation smaller than the given array using at most one swap. |
| 1054 | [LeetCode 1054: Distant Barcodes](1054.md) | Medium | A clear explanation of rearranging barcodes so no two adjacent barcodes are equal using a greedy max-heap approach. |
| 1055 | [LeetCode 1055: Shortest Way to Form String](1055.md) | Medium | A clear explanation of finding the minimum number of subsequences of source needed to form target using greedy two-pointer scanning. |
| 1056 | [LeetCode 1056: Confusing Number](1056.md) | Easy | A clear explanation of checking if a number becomes a different valid number when rotated 180 degrees. |
| 1057 | [LeetCode 1057: Campus Bikes](1057.md) | Medium | A clear explanation of greedily assigning bikes to workers based on Manhattan distance, prioritizing by distance then worker then bike index. |
| 1058 | [LeetCode 1058: Minimize Rounding Error to Meet Target](1058.md) | Medium | A clear explanation of minimizing total rounding error when rounding prices to meet a target sum using a greedy approach. |
| 1059 | [LeetCode 1059: All Paths from Source Lead to Destination](1059.md) | Medium | A clear explanation of verifying that all paths from a source node lead to a destination using DFS with cycle detection. |
| 1060 | [LeetCode 1060: Missing Element in Sorted Array](1060.md) | Medium | A clear explanation of finding the k-th missing number in a sorted array using binary search on the missing count. |
| 1061 | [LeetCode 1061: Lexicographically Smallest Equivalent String](1061.md) | Medium | A clear explanation of finding the lexicographically smallest equivalent string using Union-Find with canonical representatives. |
| 1062 | [LeetCode 1062: Longest Repeating Substring](1062.md) | Medium | A clear explanation of finding the longest substring that appears at least twice using binary search on length with rolling hash. |
| 1063 | [LeetCode 1063: Number of Valid Subarrays](1063.md) | Hard | A clear explanation of counting subarrays where the leftmost element is not larger than any other element, using a monotonic stack. |
| 1064 | [LeetCode 1064: Fixed Point](1064.md) | Easy | A clear explanation of finding the smallest index where arr[i] equals i using binary search on a sorted distinct array. |
| 1065 | [LeetCode 1065: Index Pairs of a String](1065.md) | Easy | A clear explanation of finding all index pairs where a word from the list appears in a text string using a trie. |
| 1066 | [LeetCode 1066: Campus Bikes II](1066.md) | Medium | A clear explanation of finding the minimum total Manhattan distance to assign bikes to workers using bitmask dynamic programming. |
| 1067 | [LeetCode 1067: Digit Count in Range](1067.md) | Hard | A clear explanation of counting the occurrences of a specific digit in all numbers from 1 to n using digit dynamic programming. |
| 1068 | [LeetCode 1068: Product Sales Analysis I](1068.md) | Easy | A clear explanation of retrieving product names and their sale years using a JOIN between Sales and Product tables. |
| 1069 | [LeetCode 1069: Product Sales Analysis II](1069.md) | Easy | A clear explanation of computing total quantity sold per product using GROUP BY and SUM aggregation. |
| 1070 | [LeetCode 1070: Product Sales Analysis III](1070.md) | Medium | A clear explanation of finding the first year each product was sold using a self-join or window function. |
| 1071 | [LeetCode 1071: Greatest Common Divisor of Strings](1071.md) | Easy | A clear explanation of finding the longest string that divides both strings using the GCD of their lengths. |
| 1072 | [LeetCode 1072: Flip Columns For Maximum Number of Equal Rows](1072.md) | Medium | A clear explanation of finding the maximum number of rows that can be made all-equal by flipping columns, using row pattern normalization. |
| 1073 | [LeetCode 1073: Adding Negative Numbers](1073.md) | Easy | A clear explanation of adding two non-positive integers represented as arrays of digits. |
| 1074 | [LeetCode 1074: Number of Submatrices That Sum to Target](1074.md) | Hard | A clear explanation of counting submatrices with a given sum using 2D prefix sums combined with the subarray sum equals k technique. |
| 1075 | [LeetCode 1075: Project Employees I](1075.md) | Easy | A clear explanation of computing the average years of experience per project using JOIN and AVG aggregation. |
| 1076 | [LeetCode 1076: Project Employees II](1076.md) | Easy | A clear explanation of finding the project with the most employees using GROUP BY, COUNT, and a subquery for the maximum. |
| 1077 | [LeetCode 1077: Project Employees III](1077.md) | Medium | A clear explanation of finding the most experienced employee(s) for each project using a window function or correlated subquery. |
| 1078 | [LeetCode 1078: Occurrences After Bigram](1078.md) | Easy | A clear explanation of finding all words that follow a two-word sequence in a text string. |
| 1079 | [LeetCode 1079: Letter Tile Possibilities](1079.md) | Medium | A clear explanation of counting all distinct non-empty sequences from a set of letter tiles using backtracking with frequency counting. |
| 1080 | [LeetCode 1080: Insufficient Nodes in Root to Leaf Paths](1080.md) | Medium | A clear explanation of pruning tree nodes where all root-to-leaf paths through them have sum less than a limit, using post-order DFS. |
| 1081 | [LeetCode 1081: Smallest Subsequence of Distinct Characters](1081.md) | Medium | A clear explanation of finding the lexicographically smallest subsequence with all distinct characters using a greedy stack approach. |
| 1082 | [LeetCode 1082: Sales Analysis I](1082.md) | Easy | A clear explanation of finding the best seller(s) by total price using GROUP BY, SUM, and a subquery for the maximum. |
| 1083 | [LeetCode 1083: Sales Analysis II](1083.md) | Easy | A clear explanation of finding buyers who bought an iPhone but not an iPad using JOIN and NOT IN filtering. |
| 1084 | [LeetCode 1084: Sales Analysis III](1084.md) | Easy | A clear explanation of finding products sold only in the first quarter of 2019 using GROUP BY with date range conditions. |
| 1085 | [LeetCode 1085: Sum of Digits in the Minimum Number](1085.md) | Easy | A clear explanation of checking if the digit sum of the array minimum is odd or even. |
| 1086 | [LeetCode 1086: High Five](1086.md) | Easy | A clear explanation of computing each student's top-5 average score using sorting and grouping. |
| 1087 | [LeetCode 1087: Brace Expansion](1087.md) | Medium | A clear explanation of generating all strings from a brace expansion pattern in lexicographic order using backtracking. |
| 1088 | [LeetCode 1088: Confusing Number II](1088.md) | Hard | A clear explanation of counting confusing numbers up to n using digit backtracking with rotation validation. |
| 1089 | [LeetCode 1089: Duplicate Zeros](1089.md) | Easy | A clear explanation of duplicating zeros in-place in an array without using extra space by working backwards. |
| 1090 | [LeetCode 1090: Largest Values From Labels](1090.md) | Medium | A clear explanation of selecting the maximum sum subset under item and label count constraints using a greedy approach. |
| 1091 | [LeetCode 1091: Shortest Path in Binary Matrix](1091.md) | Medium | A clear explanation of finding the shortest path from top-left to bottom-right in a binary matrix using BFS. |
| 1092 | [LeetCode 1092: Shortest Common Supersequence](1092.md) | Hard | A clear explanation of finding the shortest string containing both input strings as subsequences using LCS dynamic programming. |
| 1093 | [LeetCode 1093: Statistics from a Large Sample](1093.md) | Medium | A clear explanation of computing statistical measures (minimum, maximum, mean, median, mode) from a frequency count array. |
| 1094 | [LeetCode 1094: Car Pooling](1094.md) | Medium | A clear explanation of determining if a car can transport all passengers using a difference array for passenger count tracking. |
| 1095 | [LeetCode 1095: Find in Mountain Array](1095.md) | Hard | A clear explanation of finding a target in a mountain array using three binary searches on the interface API. |
| 1096 | [LeetCode 1096: Brace Expansion II](1096.md) | Hard | A clear explanation of generating all strings from a brace expansion expression using recursive parsing and set union/concatenation. |
| 1097 | [LeetCode 1097: Game Play Analysis V](1097.md) | Hard | A clear explanation of finding the fraction of players retained the day after their first login using self-join and window functions. |
| 1098 | [LeetCode 1098: Unpopular Books](1098.md) | Medium | A clear explanation of finding books with fewer than 10 sales in the last year that were not sold in the last year using LEFT JOIN and GROUP BY. |
| 1099 | [LeetCode 1099: Two Sum Less Than K](1099.md) | Easy | A clear explanation of finding the maximum sum of two numbers less than k using a two-pointer approach on a sorted array. |
| 1100 | [LeetCode 1100: Find K-Length Substrings With No Repeated Characters](1100.md) | Medium | A clear explanation of counting substrings of length k with all unique characters using a sliding window. |
