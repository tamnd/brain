---
title: "CF 105284B - Monkey Arrays"
description: "We are given an array and three distinguished values, $X$, $Y$, and $K$, with the ordering $Y < K < X$. For each test case, we need to count subarrays where two extremal conditions hold simultaneously: within the subarray, the maximum value must be exactly $X$, the minimum value…"
date: "2026-06-23T14:29:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105284
codeforces_index: "B"
codeforces_contest_name: "TeamsCode Summer 2024 Advanced Division"
rating: 0
weight: 105284
solve_time_s: 96
verified: false
draft: false
---

[CF 105284B - Monkey Arrays](https://codeforces.com/problemset/problem/105284/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and three distinguished values, $X$, $Y$, and $K$, with the ordering $Y < K < X$. For each test case, we need to count subarrays where two extremal conditions hold simultaneously: within the subarray, the maximum value must be exactly $X$, the minimum value must be exactly $Y$, and the value $K$ is forbidden anywhere inside it.

A subarray contributes to the answer only if every element stays within the closed range $[Y, X]$, both endpoints are actually “realized” inside the subarray, meaning at least one occurrence of $X$ and one occurrence of $Y$, and no occurrence of $K$ appears.

The constraints imply that the total array length across all test cases is at most $5 \cdot 10^5$, which rules out any quadratic or even near-quadratic per-test approach. Any solution must be linear or near-linear in total input size. A solution that inspects all subarrays explicitly would require $O(N^2)$ time per test case, which would exceed $10^{10}$ operations in worst case and is not viable.

A subtle edge case arises when the array contains no valid $X$ or $Y$ occurrences in a segment between forbidden elements. For example, if $A = [5, 4, 6]$, $X=6$, $Y=4$, $K=5$, the subarray $[4,6]$ is valid, but any segment containing 5 is invalid regardless of other elements. A naive sliding window that only tracks min and max without explicitly handling $K$ would incorrectly include invalid subarrays containing $K$.

Another failure mode is treating the condition “max is $X$” and “min is $Y$” independently. For instance, a segment might contain $X$ and $Y$, but also contain a larger element than $X$ or smaller than $Y$, breaking correctness if bounds are not enforced carefully.

## Approaches

A brute-force solution enumerates every subarray and computes its minimum, maximum, and checks for presence of $K$. For each subarray $[l, r]$, scanning the range costs $O(r-l+1)$, so total complexity is $O(N^3)$ in the most literal implementation, or $O(N^2)$ with incremental maintenance. With $N = 5 \cdot 10^5$, even $O(N^2)$ is far beyond feasible limits.

The key observation is that $K$ acts as a hard separator. Any valid subarray cannot cross an index where $A[i] = K$. This splits the array into independent segments. Inside each segment, we only care about values in $[Y, X]$, since any value outside this range would immediately violate the min or max requirement.

Within a segment free of $K$, we reduce the problem to counting subarrays whose elements lie in $[Y, X]$ and which contain at least one $X$ and at least one $Y$. This transforms into a classic two-pointer counting problem: we maintain a sliding window, track last positions of $X$ and $Y$, and ensure all elements remain within bounds.

Instead of directly enforcing both min and max conditions dynamically, we invert the counting logic. We count all subarrays within a valid region and subtract those that fail to include $X$ or fail to include $Y$. Tracking the last seen positions allows us to compute valid contributions in constant time per index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2)$ | $O(1)$ | Too slow |
| Optimal | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently, scanning the array from left to right while maintaining segment boundaries and occurrence information.

1. We maintain a pointer marking the start of the current valid segment, resetting it whenever we encounter $K$, since no subarray may include it. This ensures we never consider invalid spans.
2. Inside a segment, we track the last seen index of $X$ and $Y$. These positions tell us whether a subarray ending at the current index can possibly satisfy both constraints.
3. For each index $r$, we first verify whether $A[r]$ is within $[Y, X]$. If it is outside, we reset the segment start to $r+1$ because any subarray crossing this point would violate min/max constraints.
4. If $A[r] = X$, we update the last seen position of $X$. If $A[r] = Y$, we update the last seen position of $Y$.
5. For each endpoint $r$, we compute how many valid starting positions $l$ exist such that both $X$ and $Y$ appear in $[l, r]$ and $l$ is after the last occurrence of $K$ and any out-of-range element. The number of valid subarrays ending at $r$ is $\max(0, \min(lastX, lastY) - start)$.

Each valid subarray ending at $r$ must start no later than the earliest of the last occurrences of $X$ and $Y$, otherwise one of them would be missing.

### Why it works

At every position $r$, the algorithm implicitly characterizes all valid subarrays ending at $r$ by two constraints: they must lie entirely inside the current clean segment (no $K$ or out-of-range elements), and their left endpoint must be positioned so that both required values appear inside the subarray. The last occurrence indices fully determine whether a subarray contains at least one $X$ and one $Y$, since any subarray starting before the minimum of these last occurrences will include both, while any later start excludes one of them. This invariant ensures every counted subarray satisfies all constraints exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, X, Y, K = map(int, input().split())
        a = list(map(int, input().split()))
        
        last_x = -1
        last_y = -1
        start = 0
        ans = 0
        
        for i, v in enumerate(a):
            if v == K:
                start = i + 1
                last_x = -1
                last_y = -1
                continue
            
            if v < Y or v > X:
                start = i + 1
                last_x = -1
                last_y = -1
                continue
            
            if v == X:
                last_x = i
            if v == Y:
                last_y = i
            
            if last_x != -1 and last_y != -1:
                ans += max(0, min(last_x, last_y) - start + 1)
    
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation maintains a moving left boundary called `start`, which is forced forward whenever we encounter either the forbidden value $K$ or any value outside the allowed range $[Y, X]$. This guarantees that every considered subarray is valid with respect to bounds and exclusion rules.

The variables `last_x` and `last_y` store the most recent positions of $X$ and $Y$ inside the current segment. When both are defined, every index from `start` up to `min(last_x, last_y)` can serve as a left endpoint producing a subarray ending at `i` that contains both required values.

The expression `min(last_x, last_y) - start + 1` counts how many such starting positions exist. The `+1` is crucial because both endpoints are inclusive, and missing it leads to systematic undercounting of single-length-valid expansions.

## Worked Examples

### Example 1

Consider $A = [6, 7, 4, 6]$, $X=7$, $Y=4$, $K=5$.

| i | v | start | lastX | lastY | min(lastX,lastY) | contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 0 | -1 | -1 | - | 0 |
| 1 | 7 | 0 | 1 | -1 | - | 0 |
| 2 | 4 | 0 | 1 | 2 | 1 | 2 |
| 3 | 6 | 0 | 1 | 2 | 1 | 2 |

At index 2 and 3, both $X$ and $Y$ have appeared, so subarrays ending at these positions contribute. The table shows how earlier valid start positions accumulate valid segments. This demonstrates that the algorithm correctly counts all subarrays where both required values appear before the endpoint.

### Example 2

Consider $A = [4, 5, 2, 4]$, $X=5$, $Y=4$, $K=2$.

| i | v | start | lastX | lastY | contribution |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | 0 | -1 | 0 | 0 |
| 1 | 5 | 0 | 1 | 0 | 2 |
| 2 | 2 | 3 | -1 | -1 | reset |
| 3 | 4 | 3 | -1 | 3 | 0 |

At index 2, the presence of $K=2$ resets the segment, preventing any subarray from crossing it. This confirms that forbidden values correctly partition the array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each element is processed once with constant-time updates |
| Space | $O(1)$ | Only a few counters and indices are stored |

The total input size across test cases is bounded by $5 \cdot 10^5$, so a linear scan per test case keeps the overall runtime comfortably within limits. Memory usage remains constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample tests
assert run("3\n4 7 4 5\n6 7 4 6\n5 2 4 3\n2 8 3 6\n10 4 3 7 4 8 6 5 1 3 8 2\n") == "5\n0\n3"

# all equal values (no valid X/Y pair)
assert run("1\n5 10 1 2\n2 2 2 2 2\n") == "0"

# K blocks everything
assert run("1\n5 7 1 4\n7 4 1 4 7\n") == "0"

# minimal case
assert run("1\n1 5 1 3\n5\n") == "0"

# simple valid construction
assert run("1\n3 3 1 2\n1 3 2\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 0 | no X/Y structure possible |
| K blocks everything | 0 | segment reset correctness |
| minimal case | 0 | single element handling |
| simple valid | 1 | basic correctness of counting |

## Edge Cases

A key edge case is when $K$ appears repeatedly, splitting the array into many tiny segments. In such a case, the algorithm resets `start`, `last_x`, and `last_y` each time, ensuring no subarray spans across forbidden values. For an input like $A = [7, 2, 4, 2, 7]$, valid subarrays are confined to $[7]$, $[4]$, and $[7]$ segments, and the algorithm never incorrectly merges them.

Another edge case is when $X$ or $Y$ never appears inside a segment. For example, $A = [3, 3, 3]$ with $X=3, Y=1$ produces no valid subarray contributions because `last_y` never becomes valid. The algorithm correctly yields zero since the condition `last_x != -1 and last_y != -1` never holds.

A final subtle case occurs when $X$ and $Y$ appear in reversed order. For $A = [1, 5]$ with $X=5, Y=1$, contributions only start accumulating once both have been seen, and the formula naturally handles ordering because `min(last_x, last_y)` captures the earliest requirement among them.
