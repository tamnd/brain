---
title: "LeetCode 03xx"
description: "LeetCode practice notes for problems 300 through 399, including A dynamic programming and patience sorting solution for finding the longest strictly increasing subsequence in an array."
tags: ["leetcode", "algorithms", "practice"]
weight: 3
---

# LeetCode 03xx

| # | Title | Difficulty | Description |
|---|---|---|---|
| 300 | [LeetCode 300: Longest Increasing Subsequence](0300.md) | Medium | A dynamic programming and patience sorting solution for finding the longest strictly increasing subsequence in an array. |
| 301 | [LeetCode 301: Remove Invalid Parentheses](0301.md) | Hard | A clear explanation of Remove Invalid Parentheses using BFS to guarantee the minimum number of removals. |
| 302 | [LeetCode 302: Smallest Rectangle Enclosing Black Pixels](0302.md) | Hard | A clear explanation of Smallest Rectangle Enclosing Black Pixels using binary search on rows and columns. |
| 303 | [LeetCode 303: Range Sum Query - Immutable](0303.md) | Easy | A clear explanation of Range Sum Query - Immutable using prefix sums for constant-time range queries. |
| 304 | [LeetCode 304: Range Sum Query 2D - Immutable](0304.md) | Medium | A clear explanation of Range Sum Query 2D - Immutable using a 2D prefix sum matrix for constant-time rectangle queries. |
| 305 | [LeetCode 305: Number of Islands II](0305.md) | Hard | A clear explanation of Number of Islands II using Union-Find to dynamically merge connected land cells. |
| 306 | [LeetCode 306: Additive Number](0306.md) | Medium | A clear explanation of Additive Number using split enumeration and deterministic checking. |
| 307 | [LeetCode 307: Range Sum Query - Mutable](0307.md) | Medium | A clear explanation of Range Sum Query - Mutable using a Fenwick Tree for efficient updates and range sums. |
| 308 | [LeetCode 308: Range Sum Query 2D - Mutable](0308.md) | Hard | A clear explanation of Range Sum Query 2D - Mutable using a 2D Fenwick Tree for efficient updates and rectangle sum queries. |
| 309 | [LeetCode 309: Best Time to Buy and Sell Stock with Cooldown](0309.md) | Medium | A clear explanation of Best Time to Buy and Sell Stock with Cooldown using dynamic programming states. |
| 310 | [LeetCode 310: Minimum Height Trees](0310.md) | Medium | A clear explanation of Minimum Height Trees using leaf trimming to find the center of a tree. |
| 311 | [LeetCode 311: Sparse Matrix Multiplication](0311.md) | Medium | A clear explanation of Sparse Matrix Multiplication using non-zero entries to avoid wasted work. |
| 312 | [LeetCode 312: Burst Balloons](0312.md) | Hard | A clear explanation of Burst Balloons using interval dynamic programming and the last-burst idea. |
| 313 | [LeetCode 313: Super Ugly Number](0313.md) | Medium | A clear explanation of Super Ugly Number using dynamic programming with one pointer per prime. |
| 314 | [LeetCode 314: Binary Tree Vertical Order Traversal](0314.md) | Medium | A clear explanation of Binary Tree Vertical Order Traversal using BFS with column indices. |
| 315 | [LeetCode 315: Count of Smaller Numbers After Self](0315.md) | Hard | A clear explanation of Count of Smaller Numbers After Self using coordinate compression and a Fenwick Tree. |
| 316 | [LeetCode 316: Remove Duplicate Letters](0316.md) | Medium | A clear explanation of Remove Duplicate Letters using a greedy monotonic stack. |
| 317 | [LeetCode 317: Shortest Distance from All Buildings](0317.md) | Hard | A clear explanation of Shortest Distance from All Buildings using BFS from each building with distance and reach accumulation. |
| 318 | [LeetCode 318: Maximum Product of Word Lengths](0318.md) | Medium | A clear explanation of Maximum Product of Word Lengths using bit masks to test disjoint character sets efficiently. |
| 319 | [LeetCode 319: Bulb Switcher](0319.md) | Medium | A clear explanation of Bulb Switcher using divisor parity and perfect squares. |
| 320 | [LeetCode 320: Generalized Abbreviation](0320.md) | Medium | A clear explanation of Generalized Abbreviation using backtracking to choose whether each character is kept or abbreviated. |
| 321 | [LeetCode 321: Create Maximum Number](0321.md) | Hard | A clear explanation of Create Maximum Number using monotonic stacks for subsequences and greedy merging. |
| 322 | [LeetCode 322: Coin Change](0322.md) | Medium | A clear explanation of Coin Change using dynamic programming for minimum coin count. |
| 323 | [LeetCode 323: Number of Connected Components in an Undirected Graph](0323.md) | Medium | A clear explanation of counting connected components using Union-Find and graph traversal. |
| 324 | [LeetCode 324: Wiggle Sort II](0324.md) | Medium | A clear explanation of Wiggle Sort II using sorting, median splitting, and virtual indexing. |
| 325 | [LeetCode 325: Maximum Size Subarray Sum Equals k](0325.md) | Medium | A clear explanation of Maximum Size Subarray Sum Equals k using prefix sums and earliest-index hashing. |
| 326 | [LeetCode 326: Power of Three](0326.md) | Easy | A clear explanation of the Power of Three problem using repeated division and integer arithmetic. |
| 327 | [LeetCode 327: Count of Range Sum](0327.md) | Hard | A clear explanation of Count of Range Sum using prefix sums and merge sort counting. |
| 328 | [LeetCode 328: Odd Even Linked List](0328.md) | Medium | A clear explanation of Odd Even Linked List using in-place pointer rewiring. |
| 329 | [LeetCode 329: Longest Increasing Path in a Matrix](0329.md) | Hard | A clear explanation of Longest Increasing Path in a Matrix using DFS with memoization. |
| 330 | [LeetCode 330: Patching Array](0330.md) | Hard | A clear explanation of Patching Array using a greedy smallest-missing-sum invariant. |
| 331 | [LeetCode 331: Verify Preorder Serialization of a Binary Tree](0331.md) | Medium | A clear explanation of verifying preorder serialization using slot counting without reconstructing the tree. |
| 332 | [LeetCode 332: Reconstruct Itinerary](0332.md) | Hard | A clear explanation of Reconstruct Itinerary using a directed graph and Hierholzer's algorithm. |
| 333 | [LeetCode 333: Largest BST Subtree](0333.md) | Medium | A clear explanation of Largest BST Subtree using postorder traversal and subtree state propagation. |
| 334 | [LeetCode 334: Increasing Triplet Subsequence](0334.md) | Medium | A clear explanation of Increasing Triplet Subsequence using greedy tracking of two minimum values. |
| 335 | [LeetCode 335: Self Crossing](0335.md) | Hard | A clear explanation of Self Crossing using constant-space checks for the only possible crossing patterns. |
| 336 | [LeetCode 336: Palindrome Pairs](0336.md) | Hard | A clear explanation of Palindrome Pairs using reversed-word lookup and palindrome split checks. |
| 337 | [LeetCode 337: House Robber III](0337.md) | Medium | A clear explanation of House Robber III using tree dynamic programming with rob and skip states. |
| 338 | [LeetCode 338: Counting Bits](0338.md) | Easy | A clear explanation of Counting Bits using dynamic programming and bit manipulation. |
| 339 | [LeetCode 339: Nested List Weight Sum](0339.md) | Medium | A clear explanation of Nested List Weight Sum using depth-first search over a nested structure. |
| 340 | [LeetCode 340: Longest Substring with At Most K Distinct Characters](0340.md) | Medium | A clear explanation of Longest Substring with At Most K Distinct Characters using a sliding window and character counts. |
| 341 | [LeetCode 341: Flatten Nested List Iterator](0341.md) | Medium | A clear explanation of Flatten Nested List Iterator using lazy stack-based flattening. |
| 342 | [LeetCode 342: Power of Four](0342.md) | Easy | A clear explanation of Power of Four using bit manipulation and binary properties. |
| 343 | [LeetCode 343: Integer Break](0343.md) | Medium | A clear explanation of Integer Break using dynamic programming, with a note on the greedy math solution. |
| 344 | [LeetCode 344: Reverse String](0344.md) | Easy | A clear explanation of Reverse String using two pointers and in-place swaps. |
| 345 | [LeetCode 345: Reverse Vowels of a String](0345.md) | Easy | A clear explanation of Reverse Vowels of a String using two pointers and selective swaps. |
| 346 | [LeetCode 346: Moving Average from Data Stream](0346.md) | Easy | A clear explanation of Moving Average from Data Stream using a queue and rolling sum. |
| 347 | [LeetCode 347: Top K Frequent Elements](0347.md) | Medium | A clear explanation of Top K Frequent Elements using frequency counting and bucket sort. |
| 348 | [LeetCode 348: Design Tic-Tac-Toe](0348.md) | Medium | A clear explanation of Design Tic-Tac-Toe using row, column, and diagonal counters for constant-time winner checks. |
| 349 | [LeetCode 349: Intersection of Two Arrays](0349.md) | Easy | A clear explanation of Intersection of Two Arrays using hash sets for uniqueness and fast lookup. |
| 350 | [LeetCode 350: Intersection of Two Arrays II](0350.md) | Easy | A clear explanation of Intersection of Two Arrays II using frequency counting. |
| 351 | [LeetCode 351: Android Unlock Patterns](0351.md) | Medium | A clear explanation of Android Unlock Patterns using backtracking, a jump table, and symmetry optimization. |
| 352 | [LeetCode 352: Data Stream as Disjoint Intervals](0352.md) | Hard | A clear explanation of maintaining disjoint sorted intervals from a stream using insertion and merging. |
| 353 | [LeetCode 353: Design Snake Game](0353.md) | Medium | A clear explanation of implementing Snake Game with a deque for body order and a set for constant-time collision checks. |
| 354 | [LeetCode 354: Russian Doll Envelopes](0354.md) | Hard | A clear explanation of solving Russian Doll Envelopes using sorting and longest increasing subsequence. |
| 355 | [LeetCode 355: Design Twitter](0355.md) | Medium | A clear explanation of implementing a simplified Twitter using hash maps, sets, timestamps, and a heap. |
| 356 | [LeetCode 356: Line Reflection](0356.md) | Medium | A clear explanation of checking whether 2D points are symmetric around a vertical line using min and max x-coordinates. |
| 357 | [LeetCode 357: Count Numbers with Unique Digits](0357.md) | Medium | A clear explanation of counting numbers with unique digits using combinatorics. |
| 358 | [LeetCode 358: Rearrange String k Distance Apart](0358.md) | Hard | A clear explanation of rearranging a string so equal characters are at least k positions apart using a heap and cooldown queue. |
| 359 | [LeetCode 359: Logger Rate Limiter](0359.md) | Easy | A clear explanation of designing a logger that prints each message at most once every 10 seconds using a hash map. |
| 360 | [LeetCode 360: Sort Transformed Array](0360.md) | Medium | A clear explanation of sorting values after applying a quadratic function using two pointers. |
| 361 | [LeetCode 361: Bomb Enemy](0361.md) | Medium | A clear explanation of finding the best bomb placement in a grid using cached row and column segment counts. |
| 362 | [LeetCode 362: Design Hit Counter](0362.md) | Medium | A clear explanation of designing a hit counter for the last 5 minutes using a queue with compressed timestamps. |
| 363 | [LeetCode 363: Max Sum of Rectangle No Larger Than K](0363.md) | Hard | A clear explanation of reducing a 2D rectangle problem to a 1D prefix-sum problem with binary search. |
| 364 | [LeetCode 364: Nested List Weight Sum II](0364.md) | Medium | A clear explanation of computing inverse depth weighted sum using level-order traversal. |
| 365 | [LeetCode 365: Water and Jug Problem](0365.md) | Medium | A clear explanation of solving the Water and Jug Problem using Bézout's identity and greatest common divisor. |
| 366 | [LeetCode 366: Find Leaves of Binary Tree](0366.md) | Medium | A clear explanation of grouping binary tree nodes by the round in which they become leaves using postorder DFS. |
| 367 | [LeetCode 367: Valid Perfect Square](0367.md) | Easy | A clear explanation of checking whether an integer is a perfect square using binary search without sqrt. |
| 368 | [LeetCode 368: Largest Divisible Subset](0368.md) | Medium | A clear explanation of finding the largest subset where every pair is divisible using sorting, dynamic programming, and parent reconstruction. |
| 369 | [LeetCode 369: Plus One Linked List](0369.md) | Medium | A clear explanation of adding one to a number stored as a linked list using the rightmost non-nine digit. |
| 370 | [LeetCode 370: Range Addition](0370.md) | Medium | A clear explanation of applying many range updates efficiently using a difference array and prefix sums. |
| 371 | [LeetCode 371: Sum of Two Integers](0371.md) | Medium | A clear explanation of adding two integers without using plus or minus by using XOR, AND, carry, and a 32-bit mask. |
| 372 | [LeetCode 372: Super Pow](0372.md) | Medium | A clear explanation of computing large modular exponentiation using fast power, modular arithmetic, and digit decomposition. |
| 373 | [LeetCode 373: Find K Pairs with Smallest Sums](0373.md) | Medium | A clear explanation of finding the k smallest pair sums from two sorted arrays using a min heap and best-first search. |
| 374 | [LeetCode 374: Guess Number Higher or Lower](0374.md) | Easy | A clear explanation of finding the picked number using binary search and the guess API. |
| 375 | [LeetCode 375: Guess Number Higher or Lower II](0375.md) | Medium | A clear explanation of finding the minimum guaranteed cost using interval dynamic programming. |
| 376 | [LeetCode 376: Wiggle Subsequence](0376.md) | Medium | A clear explanation of the Wiggle Subsequence problem using dynamic programming intuition and an optimized greedy solution. |
| 377 | [LeetCode 377: Combination Sum IV](0377.md) | Medium | A clear explanation of Combination Sum IV using dynamic programming to count ordered combinations that sum to a target. |
| 378 | [LeetCode 378: Kth Smallest Element in a Sorted Matrix](0378.md) | Medium | A clear explanation of finding the kth smallest value in a row-sorted and column-sorted matrix using binary search on values. |
| 379 | [LeetCode 379: Design Phone Directory](0379.md) | Medium | A clear explanation of designing a phone directory that can allocate, check, and release numbers efficiently. |
| 380 | [LeetCode 380: Insert Delete GetRandom O(1)](0380.md) | Medium | A clear explanation of designing a randomized set with average O(1) insert, remove, and getRandom operations. |
| 381 | [LeetCode 381: Insert Delete GetRandom O(1) - Duplicates Allowed](0381.md) | Hard | A clear explanation of designing a randomized multiset with average O(1) insert, remove, and getRandom operations. |
| 382 | [LeetCode 382: Linked List Random Node](0382.md) | Medium | A clear explanation of selecting a random linked list node with equal probability using reservoir sampling. |
| 383 | [LeetCode 383: Ransom Note](0383.md) | Easy | A clear explanation of checking whether one string can be constructed from another using character frequency counting. |
| 384 | [LeetCode 384: Shuffle an Array](0384.md) | Medium | A clear explanation of shuffling an array uniformly using the Fisher-Yates algorithm while supporting reset. |
| 385 | [LeetCode 385: Mini Parser](0385.md) | Medium | A clear explanation of parsing a serialized nested integer string using a stack. |
| 386 | [LeetCode 386: Lexicographical Numbers](0386.md) | Medium | A clear explanation of generating numbers from 1 to n in lexicographical order using an iterative DFS-style traversal. |
| 387 | [LeetCode 387: First Unique Character in a String](0387.md) | Easy | A clear explanation of finding the first non-repeating character in a string using character frequency counting. |
| 388 | [LeetCode 388: Longest Absolute File Path](0388.md) | Medium | A clear explanation of computing the longest absolute path to a file from a serialized file system string using path lengths by depth. |
| 389 | [LeetCode 389: Find the Difference](0389.md) | Easy | A clear explanation of finding the extra character added to a shuffled string using counting and XOR. |
| 390 | [LeetCode 390: Elimination Game](0390.md) | Medium | A clear explanation of finding the last remaining number after alternating left-to-right and right-to-left eliminations. |
| 391 | [LeetCode 391: Perfect Rectangle](0391.md) | Hard | A clear explanation of checking whether many small axis-aligned rectangles form one exact rectangular cover using area and corner parity. |
| 392 | [LeetCode 392: Is Subsequence](0392.md) | Easy | A clear explanation of checking whether one string is a subsequence of another using two pointers. |
| 393 | [LeetCode 393: UTF-8 Validation](0393.md) | Medium | A clear explanation of validating a byte sequence as UTF-8 using bit masks and a continuation-byte counter. |
| 394 | [LeetCode 394: Decode String](0394.md) | Medium | A clear explanation of decoding nested repeat expressions using a stack. |
| 395 | [LeetCode 395: Longest Substring with At Least K Repeating Characters](0395.md) | Medium | A clear explanation of finding the longest substring where every character appears at least k times using divide and conquer. |
| 396 | [LeetCode 396: Rotate Function](0396.md) | Medium | A clear explanation of maximizing the rotation function using a recurrence instead of simulating every rotation. |
| 397 | [LeetCode 397: Integer Replacement](0397.md) | Medium | A clear explanation of reducing an integer to 1 with the fewest operations using greedy bit decisions. |
| 398 | [LeetCode 398: Random Pick Index](0398.md) | Medium | A clear explanation of picking a uniformly random index for a target value using reservoir sampling, with an alternative hash map approach. |
| 399 | [LeetCode 399: Evaluate Division](0399.md) | Medium | A clear explanation of solving division equations using graph traversal and weighted edges. |
