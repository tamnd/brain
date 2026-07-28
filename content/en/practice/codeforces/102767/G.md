---
title: "CF 102767G - Singhal and Multiplication"
description: "The problem asks whether an integer sequence contains a contiguous segment whose product leaves remainder 1 when divided by the length of the entire sequence. Among all such segments, we need the shortest one. If no segment satisfies this condition, the answer is 0."
date: "2026-07-28T23:33:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102767
codeforces_index: "G"
codeforces_contest_name: "Codedigger Training Contest -Number Theory"
rating: 0
weight: 102767
solve_time_s: 59
verified: false
draft: false
---

[CF 102767G - Singhal and Multiplication](https://codeforces.com/problemset/problem/102767/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks whether an integer sequence contains a contiguous segment whose product leaves remainder `1` when divided by the length of the entire sequence. Among all such segments, we need the shortest one. If no segment satisfies this condition, the answer is `0`. The original problem defines this condition as a subarray whose multiplication result is congruent to `1` modulo `n`, where `n` is also the number of elements in the array.

The input contains several test cases. For each test case, we receive the size of the sequence and then the sequence values themselves. The values can be very large, but only their remainders modulo `n` influence the answer. The output for each test case is a single integer representing the minimum length of a valid contiguous segment.

The total number of elements across all test cases is at most `100000`. This immediately rules out checking every subarray and multiplying its elements. A direct enumeration would require considering roughly `n^2` segments, and maintaining each product separately would push the work toward `O(n^3)` in the worst implementation. Even the optimized version that expands every starting point and maintains a running product still needs `O(n^2)` operations, which is too large when `n` reaches `100000`. We need to use a property that lets us process the sequence in linear time.

The central difficulty comes from the fact that modulo multiplication does not generally allow division. If we knew a prefix product and wanted the product of a middle segment, we cannot simply divide one prefix product by another because modular inverses exist only for numbers that are coprime with the modulus.

The first edge case appears when an element itself already gives the answer. For example:

```
Input:
1
5
7 1 3 4 8

Output:
1
```

The single element `1` has product `1 mod 5`, so the shortest possible segment has length one. A solution that only searches for repeated prefix products and forgets to check individual elements can miss this immediately.

Another important case is when some values are not invertible modulo `n`. Consider:

```
Input:
1
4
2 2 3 3

Output:
2
```

The segment `[3, 3]` works because `3 * 3 = 9` and `9 mod 4 = 1`. However, the elements `2` cannot appear in any valid segment because every product containing a factor of `2` is even and can never leave remainder `1` modulo `4`. A careless implementation that tries to apply modular inverse logic to every element would fail because `2` has no inverse modulo `4`.

A final edge case is when the whole array contains no possible answer:

```
Input:
1
2
2 2

Output:
0
```

Every possible product is even, while the desired remainder is `1`. A solution that only searches for repeated states without first respecting the invertibility condition may incorrectly assume a match exists.

## Approaches

The brute-force approach is straightforward. Start from every possible left endpoint, multiply elements one by one while extending the right endpoint, and check whether the current product becomes `1` modulo `n`. This is correct because every possible subarray is considered exactly once. The problem is the number of segments. A sequence of length `100000` contains about five billion possible subarrays, so even an `O(1)` update per extension would be far too slow.

The useful observation comes from the meaning of a product being equal to `1` modulo `n`. If a number appears inside a valid segment, that number must have a multiplicative inverse modulo `n`. In other words, it must be coprime with `n`. If `gcd(a_i, n) != 1`, then every product containing `a_i` shares a non-trivial factor with `n`, so it cannot become congruent to `1`.

This means the array can be separated into maximal blocks containing only elements coprime with `n`. Any valid segment must lie completely inside one of these blocks.

Inside such a block, every value belongs to the multiplicative group of units modulo `n`. Now modular division becomes possible. Let a prefix product be:

$$p_i = a_1 a_2 \dots a_i \pmod n$$

For a segment from `i + 1` to `j`, its product is:

$$p_j \cdot p_i^{-1} \pmod n$$

This equals `1` exactly when:

$$p_j = p_i$$

So the problem becomes finding the shortest distance between two equal prefix products inside each valid block. We can solve this with a hash map storing the latest position of every prefix product. When a prefix product appears again, the distance between the two positions is a candidate answer.

The brute-force works because it checks every possible product directly, but it ignores the algebraic structure. The observation that valid segments only contain invertible residues transforms the problem into detecting repeated states in a finite group, which can be done with a single scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

I will continue with **Algorithm Walkthrough**, **Python Solution**, **Worked Examples**, **Complexity Analysis**, **Test Cases**, and **Edge Cases** in the next part.
