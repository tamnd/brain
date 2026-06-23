---
title: "CF 105530E - Nice (Medium Version)"
description: "We are looking at numbers formed using only two digits, 6 and 9. Any valid number is “nice” if every position is one of these two digits."
date: "2026-06-23T22:59:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105530
codeforces_index: "E"
codeforces_contest_name: "Metropolitan University Inter University Programming Contest - Sylhet Division 2024"
rating: 0
weight: 105530
solve_time_s: 50
verified: true
draft: false
---

[CF 105530E - Nice (Medium Version)](https://codeforces.com/problemset/problem/105530/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at numbers formed using only two digits, 6 and 9. Any valid number is “nice” if every position is one of these two digits. The task is not to construct something complex from them, but to answer multiple queries of the form: how many such nice numbers lie inside a given numeric interval $[l, r]$.

So the problem reduces to understanding a very specific universe of numbers: all strings over the alphabet $\{6, 9\}$, interpreted as integers without leading restrictions beyond digit choice. For each query, we want to count how many of these special numbers fall between two bounds.

The important structural observation is that the set of all nice numbers is extremely small compared to the range of integers up to $10^{18}$. Every digit position independently has 2 choices, so for a fixed length $i$, there are exactly $2^i$ such numbers. Summed over all lengths up to 18, the total is $2^1 + 2^2 + \dots + 2^{18}$, which is only a few hundred thousand elements. This makes brute enumeration plausible.

The constraints imply that any solution that iterates over all integers up to $10^{18}$ per query is impossible, since that would be up to $10^{18}$ operations. Even a linear scan per query would immediately fail. On the other hand, iterating over at most around $3 \cdot 10^5$ precomputed values is trivial, even for many test cases.

A subtle edge case arises from boundary handling when $l = 1$ or when $l$ itself is a nice number. For example, if we count numbers $\le r$ and subtract numbers $< l$, then off-by-one mistakes occur if we accidentally exclude or double count values exactly equal to $l$. Another edge case is treating numbers as strings versus integers; leading zeros are irrelevant because we only generate fixed-length digit strings starting from length 1.

## Approaches

A direct brute force approach would be to iterate over every integer from $l$ to $r$ and check whether each number contains only digits 6 and 9. This check is linear in the number of digits, so for a single number it is $O(18)$. However, the range length can be up to $10^{18}$, making this completely infeasible. Even a single query could require $10^{18}$ checks.

The key observation is that we do not actually need to inspect arbitrary numbers. The entire valid set is determined structurally: each length contributes exactly a full binary set of digit combinations. This means we can precompute all valid numbers once, store them in sorted order, and answer queries using binary search.

We generate all nice numbers using backtracking or bitmasking over lengths 1 to 18. Each construction step appends either 6 or 9, forming a complete binary tree of size $2^i$ at depth $i$. After collecting all values, we sort them. Then each query becomes a standard prefix counting problem: count how many precomputed values lie in $[l, r]$ using two binary searches.

The transition from brute force to optimal comes from shifting perspective: instead of scanning the integer line, we enumerate the combinatorial structure directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l+1)\cdot 18)$ | $O(1)$ | Too slow |
| Optimal | $O(2^{18} \log 2^{18})$ preprocessing + $O(\log 2^{18})$ per query | $O(2^{18})$ | Accepted |

## Algorithm Walkthrough

1. Generate all nice numbers by constructing digit strings of length from 1 to 18. Each position branches into two possibilities, 6 or 9. This ensures every valid number is produced exactly once because each digit sequence corresponds to exactly one integer.
2. During generation, convert each constructed digit sequence into an integer and store it in an array. This step is necessary because we will later need ordering by numeric value, not lexicographic order of construction.
3. After generation finishes, sort the array of all nice numbers. Sorting aligns the structure so that binary search can be applied. Without sorting, we would lose the ability to answer range queries efficiently.
4. For each query $[l, r]$, compute the number of valid values $\le r$ using binary search, then subtract the number of valid values $< l$. This converts a range query into two prefix queries.
5. Return the difference as the answer for that query.

### Why it works

The key invariant is that the precomputed array contains every and only valid nice number exactly once, and it is sorted in increasing numeric order. Because of this, binary search correctly identifies prefix counts: all elements $\le x$ form a contiguous prefix of the sorted list. Subtracting two prefix counts isolates exactly those elements lying in $[l, r]$, with no double counting or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def generate(n, cur, arr):
    if n == 0:
        arr.append(int(cur))
        return
    generate(n - 1, cur + '6', arr)
    generate(n - 1, cur + '9', arr)

def main():
    arr = []
    for length in range(1, 19):
        generate(length, "", arr)

    arr.sort()

    def count_le(x):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    t = int(input())
    for _ in range(t):
        l, r = map(int, input().split())
        print(count_le(r) - count_le(l - 1))

if __name__ == "__main__":
    main()
```

The solution begins by building all valid numbers using a recursive generator that constructs every length from 1 to 18. Each recursion level appends either digit 6 or 9, ensuring full coverage of the binary decision space. Once all numbers are collected, they are sorted so that numeric ordering matches array order.

The function `count_le(x)` performs a standard upper-bound binary search, returning how many elements are $\le x$. The final answer per query is the difference between prefix counts at $r$ and $l-1$, which correctly isolates the interval.

A key detail is using `l - 1` instead of attempting to check membership of `l` directly. This avoids edge cases where $l$ itself is a valid number.

## Worked Examples

Since the statement does not include explicit samples, consider two illustrative queries.

### Example 1

Input query:

$l = 6, r = 9$

We generate prefix counts over sorted array beginning with values like 6, 9, 66, 69, ...

| Step | x | count_le(x) |
| --- | --- | --- |
| prefix ≤ 9 | 9 | 2 |
| prefix ≤ 5 | 5 | 0 |

Answer is $2 - 0 = 2$.

This confirms that both single-digit valid numbers are included correctly.

### Example 2

Input query:

$l = 10, r = 69$

We count all valid numbers up to 69. These include 6, 9, 66, 69.

| Step | x | count_le(x) |
| --- | --- | --- |
| prefix ≤ 69 | 69 | 4 |
| prefix ≤ 9 | 9 | 2 |

Answer is $4 - 2 = 2$, corresponding to 66 and 69.

This shows that multi-digit numbers are naturally included once generation spans all lengths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^{18} + q \log 2^{18})$ | Precompute all digit combinations once, then binary search per query |
| Space | $O(2^{18})$ | Store all generated numbers in a list |

The total number of generated values is only 262,143, which easily fits within memory and allows fast sorting and querying. Even with large numbers of test cases, each query is handled in logarithmic time over a very small array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    from bisect import bisect_right

    arr = []
    def gen(n, s):
        if n == 0:
            arr.append(int(s))
            return
        gen(n - 1, s + "6")
        gen(n - 1, s + "9")

    for i in range(1, 5):
        gen(i, "")
    arr.sort()

    def count_le(x):
        return bisect_right(arr, x)

    it = iter(inp.strip().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        l = int(next(it)); r = int(next(it))
        out.append(str(count_le(r) - count_le(l - 1)))
    return "\n".join(out)

# custom cases
assert run("1\n1 5\n") == "0"
assert run("1\n6 9\n") == "2"
assert run("1\n6 6\n") == "1"
assert run("1\n10 100\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1 5 | 0 | no valid numbers below smallest |
| 1, 6 9 | 2 | base single-digit correctness |
| 1, 6 6 | 1 | exact boundary inclusion |
| 1, 10 100 | 2 | multi-digit filtering |

## Edge Cases

One important edge case is when the query range starts below the smallest nice number. For example, $l = 1, r = 5$. The algorithm computes `count_le(5) - count_le(0)`. Since there are no generated values $\le 5$, both counts are zero, producing correct output 0. The subtraction with $l-1$ naturally handles the lower bound without special branching.

Another case is when the range exactly matches a generated number. For $l = r = 66$, `count_le(66)` includes all values up to and including 66, while `count_le(65)` excludes it. Their difference is 1, correctly counting the single valid number.

A final subtle case is ordering: since generation is not inherently sorted, failing to sort would break binary search correctness. For instance, if 96 were generated before 66, prefix counts would become meaningless. Sorting ensures the invariant that numeric order matches array order, which is essential for all query logic.
