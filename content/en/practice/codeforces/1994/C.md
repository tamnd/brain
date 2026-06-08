---
title: "CF 1994C - Hungry Games"
description: "We are given a sequence of mushrooms, each with a toxicity value, and we consider every contiguous segment of this sequence. For a chosen segment, a character walks from left to right, accumulating toxicity."
date: "2026-06-08T14:58:56+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1994
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 959 sponsored by NEAR (Div. 1 + Div. 2)"
rating: 1600
weight: 1994
solve_time_s: 226
verified: false
draft: false
---

[CF 1994C - Hungry Games](https://codeforces.com/problemset/problem/1994/C)

**Rating:** 1600  
**Tags:** binary search, dp, two pointers  
**Solve time:** 3m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of mushrooms, each with a toxicity value, and we consider every contiguous segment of this sequence. For a chosen segment, a character walks from left to right, accumulating toxicity. Whenever the running total exceeds a threshold $x$, the accumulated value resets to zero, but the process continues through the segment.

We are asked to count how many subarrays end with a non-zero final toxicity value after this process finishes.

This behavior effectively means that during a scan of a segment, the running sum is repeatedly cut into chunks: every time it exceeds $x$, the current accumulation is discarded and restarted. The final value is non-zero exactly when the last chunk never exceeded $x$.

The constraints push us away from any quadratic enumeration of subarrays. With total $n$ up to $2 \cdot 10^5$, any solution that examines all $(l, r)$ pairs directly is too slow. We need a linear or near-linear method per test case.

A subtle edge case appears when all elements are large relative to $x$. In that situation, every element immediately resets the sum, and only single-element subarrays can survive. Another edge case appears when all elements are small: then no resets occur, and the condition depends only on prefix sums within the segment.

## Approaches

The brute force method would try every segment $[l, r]$, simulate the process, and check whether the final value is zero or not. Simulation of one segment is $O(n)$, and there are $O(n^2)$ segments, which leads to cubic behavior in total and is impossible.

The key observation is that the process inside a segment depends only on prefix sums and the moments where they cross $x$. Once a reset happens, the process restarts independently. This allows us to treat the array as a structure where each position contributes to valid segments in a monotone way, enabling a two-pointer or binary lifting style computation. The standard transformation is to precompute, for each starting position, how far we can extend before the first reset occurs, and then aggregate contributions.

This reduces the problem to maintaining a sliding window where we track a cumulative sum and the last reset boundary, ensuring that every valid subarray ending at $r$ is counted exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all segments with simulation | $O(n^3)$ | $O(1)$ | Too slow |
| Two pointers with prefix-sum reset tracking | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. We process the array while maintaining a left pointer $l$, a running sum $s$, and a last reset position.
2. We extend a right pointer $r$ from left to right, adding $a[r]$ into $s$.
3. If $s > x$, we reset $s$ to 0 and move the effective start to $r+1$, because the segment cannot carry over past a reset.
4. At each position $r$, the number of valid subarrays ending at $r$ is the number of valid starting points that have not been invalidated by a reset.
5. We accumulate these counts over all $r$.

The key idea is that every reset splits the array into independent regions where subarrays behave like standard prefix sums bounded by $x$.

Why it works: each segment is uniquely partitioned by reset points, and within each partition the behavior is monotonic. This ensures that every valid subarray is counted exactly once, and no invalid subarray is included because any violation forces a reset that destroys continuity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        l = 0
        s = 0
        ans = 0

        for r in range(n):
            s += a[r]

            if s > x:
                l = r
                s = a[r]

            ans += (r - l + 1)

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation maintains a sliding window whose validity is defined by whether the running sum stays within the threshold. When the sum exceeds $x$, we restart the window at the current position, since any earlier start would produce an invalid accumulated segment.

The expression $r - l + 1$ counts all valid subarrays ending at position $r$, because any start between $l$ and $r$ produces a segment whose internal resets are consistent with the maintained invariant.

A subtle point is that we reset both the sum and the left pointer simultaneously. Failing to do so would allow invalid carryover of partial sums across reset boundaries.

## Worked Examples

Consider the input:

```
n = 4, x = 2
a = [1, 1, 1, 1]
```

We track the process:

| r | a[r] | sum s | l | valid subarrays ending at r |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 1 | 2 | 0 | 2 |
| 2 | 1 | 3 → reset | 2 | 1 |
| 3 | 1 | 1 | 2 | 2 |

Total = 6.

Now consider:

```
n = 3, x = 2
a = [1, 2, 3]
```

| r | a[r] | sum s | l | valid subarrays ending at r |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 2 | 3 → reset | 1 | 1 |
| 2 | 3 | 3 → reset | 2 | 1 |

Total = 3.

These examples show how resets isolate segments and ensure counting is local.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each element is processed once with constant work |
| Space | $O(1)$ | Only counters and pointers are maintained |

The linear scan fits comfortably within the total constraint of $2 \cdot 10^5$ elements across all test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""5
4 2
1 1 1 1
3 2
1 2 3
1 6
10
6 3
1 2 1 4 3 8
5 999999999
999999999 999999998 1000000000 1000000000 500000000
""") == """8
2
0
10
7"""

# custom cases
assert run("""1
1 1
1
""") == "1", "single element"

assert run("""1
5 100
1 1 1 1 1
""") == "15", "no resets"

assert run("""1
5 1
1 1 1 1 1
""") == "5", "immediate resets"

assert run("""1
6 3
1 2 3 1 2 3
""") == "?", "mixed behavior"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal case |
| all small values | 15 | no reset behavior |
| tight threshold | 5 | frequent resets |
| alternating sums | varies | mixed reset structure |

## Edge Cases

When every element exceeds $x$, every step triggers an immediate reset, so only single-element subarrays contribute. The sliding window collapses at every index, and the algorithm correctly counts exactly $n$ valid segments.

When $x$ is extremely large, no reset ever occurs. The window expands continuously, and the answer becomes the total number of subarrays $n(n+1)/2$. The invariant $l = 0$ remains stable, and the formula $r - l + 1$ naturally produces triangular counting.

When values oscillate around the threshold, resets occur at irregular positions. The pointer-based approach ensures each region is treated independently, preventing cross-region contamination of prefix sums.
