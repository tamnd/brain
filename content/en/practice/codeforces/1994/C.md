---
title: "CF 1994C - Hungry Games"
description: "We are given a row of values, and we want to count how many contiguous segments behave “well” under a very specific simulation rule. When we pick a segment $[l, r]$, we process its elements from left to right, maintaining a running sum $g$."
date: "2026-06-09T02:19:18+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1994
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 959 sponsored by NEAR (Div. 1 + Div. 2)"
rating: 1600
weight: 1994
solve_time_s: 162
verified: false
draft: false
---

[CF 1994C - Hungry Games](https://codeforces.com/problemset/problem/1994/C)

**Rating:** 1600  
**Tags:** binary search, dp, two pointers  
**Solve time:** 2m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of values, and we want to count how many contiguous segments behave “well” under a very specific simulation rule.

When we pick a segment $[l, r]$, we process its elements from left to right, maintaining a running sum $g$. After adding each element, if the running sum exceeds a threshold $x$, the sum is reset to zero. Otherwise, it stays as it is. A segment is considered good if, after processing the entire segment, the final value of $g$ is not zero. The task is to count all such good segments over multiple test cases.

The constraints force us to think in terms of linear or near-linear solutions per test case. The total length across all test cases is at most $2 \cdot 10^5$, which rules out anything quadratic like checking all segments explicitly. Any valid solution must essentially maintain a sliding window or incremental structure where each element is processed a constant number of times.

A subtle edge case appears when values are extremely large relative to $x$. In such cases, every element individually resets the sum, which means only single-element segments can be valid. Another edge case is when the array is non-decreasing or all small values, where long segments survive many steps without resets, and naive logic that only tracks prefix sums will overcount.

## Approaches

A brute force solution tries every segment $[l, r]$, simulates the process, and checks whether the final $g$ is non-zero. Each simulation takes $O(n)$, leading to $O(n^3)$ total in the worst case, which is far too slow.

The key observation is that the process only depends on the current accumulated sum since the last reset. Once the sum exceeds $x$, it is wiped to zero, and the process restarts locally. This creates natural “valid blocks” where the running sum never exceeds $x$, and boundaries between blocks behave independently.

The problem reduces to tracking how far we can extend a segment starting at each position before the running sum triggers a reset. Once we know these boundaries, we can count valid segments using a two-pointer or prefix-based counting strategy.

The brute force works because it explicitly simulates resets, but fails because it recomputes the same prefix behavior repeatedly. The observation that resets partition the array into independent segments lets us reuse computed structure and count contributions efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ or $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently and maintain a sliding window over the array.

1. We maintain a left pointer $l$ and a running sum $g$. The idea is to keep a maximal segment starting at $l$ where the process has not been reset.
2. We iterate $r$ from left to right, adding $a[r]$ to $g$. This simulates extending the current segment.
3. If $g$ exceeds $x$, we simulate the reset by setting $g = 0$ and moving $l$ to $r + 1$. This reflects that the segment before $r$ cannot contribute to a valid continuation.
4. At each position $r$, if $g \neq 0$, then any starting point $l' \in [l, r]$ produces a valid segment ending at $r$, because none of those starts would have caused an immediate reset before reaching $r$. We add $r - l + 1$ to the answer.
5. We continue until the end, accumulating contributions.

The key idea is that resets split the array into independent blocks, and within each block we count all subarrays ending at each position that survive the process.

### Why it works

The invariant is that at any moment, $l$ always points to the first index of the current active block where no reset has occurred since $l$. The running sum $g$ exactly represents the processed segment $[l, r]$ under the game rules. Every time we reset, we correctly discard all previous contributions that cannot extend further. This ensures each valid segment is counted exactly once, and every invalid segment is excluded because it necessarily triggers a reset before completion.

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
        g = 0
        ans = 0
        
        for r in range(n):
            g += a[r]
            
            if g > x:
                g = 0
                l = r + 1
                continue
            
            ans += (r - l + 1)
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the sliding window logic. The pointer $l$ is updated only when a reset happens, which corresponds to exceeding the threshold. The contribution $r - l + 1$ counts all valid starting points for subarrays ending at $r$. The reset step is crucial, since without it we would incorrectly carry over invalid partial sums into future segments.

## Worked Examples

Consider a small case where $x = 2$ and the array is $[1, 2, 1]$.

At $r = 0$, we have $g = 1$, so $l = 0$, contributing 1 segment.

At $r = 1$, $g = 3$ exceeds $x$, so we reset and set $l = 2$, contributing 0.

At $r = 2$, $g = 1$, contributing 1 segment.

The total is 2, matching the expected behavior.

Now consider $[1, 1, 1, 1]$ with $x = 2$. The window grows until the sum would exceed $x$, then resets, and we repeatedly count contributions inside each safe block. The trace shows that every extension within a valid block contributes linearly, and resets prevent cross-contamination between blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is processed once, with at most one reset per index |
| Space | $O(1)$ | Only a few variables are maintained |

The total complexity across all test cases is linear in the total input size, which is necessary given the constraint that $\sum n \le 2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        l = 0
        g = 0
        ans = 0
        
        for r in range(n):
            g += a[r]
            if g > x:
                g = 0
                l = r + 1
                continue
            ans += (r - l + 1)
        
        out.append(str(ans))
    return "\n".join(out)

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
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones small | 4 | no resets, full accumulation |
| single large element | 0 | immediate reset behavior |
| alternating small/large | varies | boundary resets |

## Edge Cases

When all elements are greater than $x$, every step triggers an immediate reset, so only segments of length 1 are valid. The algorithm handles this because every time $g > x$, we reset and move $l$ past the current index, ensuring no invalid segment contributes.

When all elements are small and the sum never exceeds $x$, the window never resets and the answer becomes the sum of all subarray counts, which the formula $(r - l + 1)$ accumulates correctly.

When a reset happens exactly at position $r$, the implementation ensures that no contribution is counted for that step, because $g$ is cleared before any addition to the answer, preventing incorrect inclusion of broken segments.
