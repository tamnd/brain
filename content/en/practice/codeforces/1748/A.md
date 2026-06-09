---
title: "CF 1748A - The Ultimate Square"
description: "We are given a sequence of rectangular wooden blocks. The i-th block always has height 1, and its length grows slowly with i according to the rule ⌈i/2⌉."
date: "2026-06-09T15:27:30+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1748
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 833 (Div. 2)"
rating: 800
weight: 1748
solve_time_s: 200
verified: true
draft: false
---

[CF 1748A - The Ultimate Square](https://codeforces.com/problemset/problem/1748/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 3m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of rectangular wooden blocks. The i-th block always has height 1, and its length grows slowly with i according to the rule ⌈i/2⌉. So blocks come in pairs of equal width: indices 1 and 2 both have width 1, indices 3 and 4 both have width 2, indices 5 and 6 both have width 3, and so on.

We are allowed to pick any subset of these blocks and place them without rotation. Each block contributes a horizontal strip of height 1 and fixed width. The goal is to assemble these strips into a solid square of size s × s for the maximum possible integer s.

The key restriction is that blocks cannot be rotated, so each block contributes exactly a 1-by-w rectangle.

The input size is large: n can be up to 10^9 and there are up to 10^4 test cases. This immediately rules out any approach that iterates over all blocks or simulates construction. Any solution must depend only on n and use closed-form reasoning.

A subtle edge case appears when n is small. For n = 1 or n = 2, all blocks have width 1, so only a 1 × 1 square is possible. A naive approach that assumes width growth starts immediately from 2 would incorrectly overestimate the answer. Another pitfall is assuming we need to use all blocks, while in fact we are selecting only a subset that fits into the square packing constraint.

## Approaches

If we try a direct construction approach, we would simulate building rows of the square. Each row requires width s, and we would greedily pick available blocks whose widths sum to at least s. For each candidate s, this would require scanning all blocks or maintaining a multiset of widths.

Even checking a single s costs O(n), and since s can be as large as roughly √n, this leads to about O(n√n) or worse per test case, which is impossible for n up to 10^9.

The key observation is that block widths are extremely structured. Every integer width w appears exactly twice, and all widths ≤ k appear exactly 2k times in the prefix of blocks.

So instead of thinking in terms of individual blocks, we aggregate by width. For a given n, we can compute how many full width-groups we have. If k = ⌊n/2⌋, then we fully include widths from 1 to k, each contributing two blocks. If n is odd, we additionally have one more block of width k+1.

This transforms the problem into a pure counting problem: how large a square can we form using a multiset where each width w appears up to twice (except possibly the last one partially)?

Now the next insight is geometric: to build a square of side s, we need to select strips whose total height is at least s (always true since we can pick at most s rows), and more importantly we need to pack each row to length s. This reduces to checking how many total horizontal “unit height strips” we can allocate per width level.

A simpler way to see it is to reverse the viewpoint: instead of assembling a square, consider the maximum possible s such that we can assign each of the s rows a total width of at least s. Since all rows are identical in requirement, we are really asking whether total available “area contribution” from widths can support s × s.

The total area contributed by all blocks is:

sum_{i=1..n} ⌈i/2⌉.

This sum can be computed in closed form by pairing indices. For each k, we get two blocks of width k contributing 2k total area, until possibly the last incomplete pair.

Thus:

If n = 2m, total area = 2(1 + 2 + ... + m) = m(m+1)

If n = 2m + 1, total area = m(m+1) + (m+1) = (m+1)^2

So the total area is either m(m+1) or (m+1)^2. Since we want the largest square s × s that fits in area, we suspect s is roughly √(area). However, this is not sufficient alone, because structure might restrict packing.

The crucial final observation is that this construction is tight: widths are non-decreasing and sufficiently balanced that any feasible packing depends only on total area, and the optimal square side becomes exactly:

s = ⌊√(sum of first n widths)⌋.

Computing this reduces the entire problem to a constant-time arithmetic formula per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Construction | O(n√n) | O(n) | Too slow |
| Prefix Sum + Square Root Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

### Key idea

We compute the total sum of widths contributed by the first n blocks, then take the largest integer s such that s² ≤ sum.

### Steps

1. Split n into pairs of indices by computing m = n // 2.

This groups blocks (1,2), (3,4), ..., each pair sharing the same width.
2. Compute total contribution from full pairs: m(m+1).

This comes from 2(1 + 2 + ... + m), since each width k appears twice.
3. If n is odd, add the contribution of the last block, which has width m+1.
4. Let total be the computed sum.
5. The answer is the largest integer s such that s² ≤ total, i.e. floor(sqrt(total)).

### Why it works

The construction is monotone in widths, meaning larger widths appear only after smaller ones and always in sufficient multiplicity. This prevents pathological packing restrictions where area exists but cannot be arranged into a square. Because every width level contributes full 1-height strips, the limiting factor becomes purely the total available area, and no additional combinatorial constraint reduces feasibility. Therefore the maximal square side is determined exactly by the area bound.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

t = int(input())
for _ in range(t):
    n = int(input())
    m = n // 2
    total = m * (m + 1)
    if n % 2 == 1:
        total += (m + 1)
    print(int(math.isqrt(total)))
```

The implementation directly follows the derived formula. The integer square root is used to avoid floating-point precision issues. The computation of total is done in O(1) using arithmetic series formulas.

Care must be taken that the intermediate multiplication m(m+1) can be large, so Python’s arbitrary precision integers are appropriate here.

## Worked Examples

### Example 1: n = 5

| Step | Value of m | Pair contribution | Extra block | Total |
| --- | --- | --- | --- | --- |
| Compute | 2 | 2(1+2)=6 | width 3 | 9 |

Now we compute s = ⌊√9⌋ = 3.

This matches the construction where blocks of widths 1,1,2,2,3 can form a 3 × 3 square.

### Example 2: n = 2

| Step | Value of m | Pair contribution | Extra block | Total |
| --- | --- | --- | --- | --- |
| Compute | 1 | 2(1)=2 | none | 2 |

Now s = ⌊√2⌋ = 1.

We cannot form a 2 × 2 square because total available width is insufficient, so the result is 1.

These examples show that the square side is governed entirely by aggregated width sum, not by individual block arrangement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only arithmetic operations and one square root |
| Space | O(1) | No auxiliary structures |

The solution easily handles 10^4 test cases since each case is constant work.

## Test Cases

```python
import sys, io, math

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        m = n // 2
        total = m * (m + 1)
        if n % 2 == 1:
            total += (m + 1)
        out.append(str(math.isqrt(total)))
    return "\n".join(out)

# provided samples
assert solve("3\n2\n5\n197654321\n") == "1\n3\n98827161"

# custom cases
assert solve("1\n1\n") == "1", "minimum n"
assert solve("1\n2\n") == "1", "small even case"
assert solve("1\n6\n") == str(math.isqrt(3*4)), "even structured case"
assert solve("1\n7\n") == str(math.isqrt(16)), "odd boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 1 | 1 | minimum edge case |
| n = 2 | 1 | smallest even case |
| n = 6 | sqrt-based value | consistency of pairing formula |
| n = 7 | sqrt-based value | odd-length handling |

## Edge Cases

For n = 1, we have only one block of width 1. The formula gives m = 0, total = 1, and the answer is 1. The algorithm handles this correctly because the odd-case addition contributes the single block.

For n = 2, both blocks have width 1. We get m = 1, total = 2, and the square root is 1. Even though two blocks exist, they cannot form side 2 because total area is insufficient.

For large odd n, say n = 10^9, the algorithm computes m = 5×10^8 and safely evaluates the quadratic expression in Python integers. The monotone structure ensures no overflow or structural packing failure occurs, and the square root remains correct.
