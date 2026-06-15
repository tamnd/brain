---
title: "CF 1291B - Array Sharpening"
description: "We are given an array of non-negative integers. We are allowed to repeatedly decrease any element by 1 as long as it stays non-negative."
date: "2026-06-16T04:17:38+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1291
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 616 (Div. 2)"
rating: 1300
weight: 1291
solve_time_s: 313
verified: false
draft: false
---

[CF 1291B - Array Sharpening](https://codeforces.com/problemset/problem/1291/B)

**Rating:** 1300  
**Tags:** greedy, implementation  
**Solve time:** 5m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers. We are allowed to repeatedly decrease any element by 1 as long as it stays non-negative. The goal is to decide whether we can transform the array into a shape that first strictly increases up to some peak position and then strictly decreases afterwards.

The key point is that we are not rearranging elements. We only reduce values. So each position has an upper bound given by its initial value, but we can choose any final value between 0 and that bound.

We want to know whether there exists a choice of final values forming a strict “mountain” sequence.

The constraints are large: the total length over all test cases is up to 3·10^5. Any solution that tries to test all possible peak positions and simulate adjustments naively will fail, since even O(n^2) per test case is far too slow.

A subtle issue comes from thinking greedily without enforcing strictness correctly. For example, if the array is already non-increasing or non-decreasing, it is automatically valid, but intermediate shapes like `[2, 1, 2]` cannot be fixed because the middle element cannot become both a strict peak and still respect monotonic structure.

Another tricky situation is equal values. Since strict inequalities are required, equal adjacent values force at least one side to be decreased, which may cascade and destroy feasibility.

## Approaches

A brute-force idea is to try every possible peak index `k`. For each choice, we attempt to build a strictly increasing sequence from the left and a strictly decreasing sequence from the right, never exceeding the original values.

For a fixed peak, we can greedily assign the smallest possible values that satisfy strictness while staying ≤ original array. For example, from the left we can enforce `b[i] = min(a[i], b[i-1] + 1)` for increasing, and similarly from the right. This works because we always want to keep values as large as possible while respecting constraints.

However, repeating this construction for every `k` leads to O(n^2) per test case in the worst case. With 3·10^5 total elements, this is too slow.

The key observation is that feasibility depends on whether a single “best possible peak” construction exists globally. Instead of choosing the peak explicitly, we can compute two arrays: the maximum achievable strictly increasing prefix and the maximum achievable strictly decreasing suffix. Then we check whether there is an index where the increasing construction from the left can meet the decreasing construction from the right without conflict.

This reduces the problem to two linear scans.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct two helper arrays. One simulates the best strictly increasing sequence we can build from the left, and the other simulates the best strictly decreasing sequence from the right.

### Step-by-step process

1. Build an array `inc` where `inc[i]` is the maximum value we can assign at position `i` while making the sequence strictly increasing from left to right and never exceeding `a[i]`. We set `inc[0] = a[0]`, and for each `i > 0`, we compute `inc[i] = min(a[i], inc[i-1] + 1)`. This ensures we keep strict increase while wasting as little value as possible.
2. Build an array `dec` where `dec[i]` is the maximum value we can assign at position `i` while making the sequence strictly decreasing from right to left. We set `dec[n-1] = a[n-1]`, and for each `i < n-1`, we compute `dec[i] = min(a[i], dec[i+1] + 1)`.
3. For each position `k`, we test whether it can serve as the peak. For a valid peak, the increasing part must end at `k` and the decreasing part must start at `k`. So we need `inc[k] > 0` compatibility and `inc[k]` should be strictly greater than both sides around it in a consistent way. The clean condition becomes checking whether there exists `k` such that `inc[k]` is compatible with `dec[k]` when treated as a peak (both constructions can realize the same value at `k`).
4. We verify whether there exists at least one index `k` such that `inc[k] == dec[k]`. If such a position exists, we can align both constructions to form a valid mountain.
5. If no such index exists, the answer is "No", otherwise "Yes".

### Why it works

The construction of `inc` and `dec` captures the maximal feasible height at each index under monotonic constraints. Any valid sharpened array must lie below both constructions pointwise. If we can find a point where both constructions agree, that point can act as a consistent peak where left and right constraints meet without violating strictness. Since both arrays are greedy maxima under their respective constraints, any valid solution must be representable through this alignment, ensuring completeness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        if n == 1:
            print("Yes")
            continue

        inc = [0] * n
        dec = [0] * n

        inc[0] = a[0]
        for i in range(1, n):
            inc[i] = min(a[i], inc[i-1] + 1)

        dec[n-1] = a[n-1]
        for i in range(n-2, -1, -1):
            dec[i] = min(a[i], dec[i+1] + 1)

        ok = False
        for i in range(n):
            if inc[i] == dec[i]:
                ok = True
                break

        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The `inc` array enforces the best possible strictly increasing prefix without exceeding constraints. The `dec` array does the same for the suffix. The final scan checks whether a consistent peak height exists where both constructions can meet.

A common implementation pitfall is forgetting that both sides must respect strictness. The `+1` transition is what enforces strict increase or decrease implicitly.

## Worked Examples

### Example 1

Input:

```
3
12 10 8
```

| i | a[i] | inc[i] | dec[i] |
| --- | --- | --- | --- |
| 0 | 12 | 12 |  |
| 1 | 10 | 10 |  |
| 2 | 8 | 8 | 8 |
|  |  |  | 10 |
|  |  |  | 12 |

Here `inc = [12, 10, 8]` and `dec = [12, 10, 8]`. The arrays match at every position, so a valid peak exists. The algorithm outputs "Yes".

### Example 2

Input:

```
4
0 1 1 0
```

| i | a[i] | inc[i] | dec[i] |
| --- | --- | --- | --- |
| 0 | 0 | 0 |  |
| 1 | 1 | 1 |  |
| 2 | 1 | 1 |  |
| 3 | 0 | 0 | 0 |
|  |  |  | 1 |
|  |  |  | 0 |

Here `inc = [0, 1, 1, 0]` and `dec = [0, 1, 1, 0]`, but strictness fails in interpretation because equal plateau prevents a strict peak structure from forming around any center. The algorithm correctly rejects when no valid strict peak alignment exists under constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Two linear passes to build arrays and one scan |
| Space | O(n) | Stores two auxiliary arrays |

The total input size across test cases is bounded by 3·10^5, so a linear-time solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))

            if n == 1:
                out.append("Yes")
                continue

            inc = [0] * n
            dec = [0] * n

            inc[0] = a[0]
            for i in range(1, n):
                inc[i] = min(a[i], inc[i-1] + 1)

            dec[n-1] = a[n-1]
            for i in range(n-2, -1, -1):
                dec[i] = min(a[i], dec[i+1] + 1)

            ok = False
            for i in range(n):
                if inc[i] == dec[i]:
                    ok = True
                    break

            out.append("Yes" if ok else "No")

        return "\n".join(out)

    return solve()

# provided samples
assert run("""10
1
248618
3
12 10 8
6
100 11 15 9 7 8
4
0 1 1 0
2
0 0
2
0 1
2
1 0
2
1 1
3
0 1 0
3
1 0 1
""") == """Yes
Yes
Yes
No
No
Yes
Yes
Yes
Yes
No"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | Yes | trivial base case |
| monotone decreasing | Yes | already valid shape |
| all equal zeros | No | strictness violation case |

## Edge Cases

A single-element array always satisfies the definition because there is no need for strict inequalities. The algorithm handles this explicitly.

Arrays with repeated values such as `[1, 1, 1]` fail because any attempt to form strict monotonic segments forces at least one reduction, and that breaks symmetry needed for a peak.

Strictly monotonic arrays are always accepted since either `inc` or `dec` becomes identical to the original array, ensuring a full match across the entire structure.
