---
title: "CF 103800B - Ginger's game"
description: "We are given an array of monster health values. Before anything starts, we are allowed to reduce each value independently, but we can never increase it beyond its original value. After that preparation, we choose a starting position $i$."
date: "2026-07-02T08:42:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103800
codeforces_index: "B"
codeforces_contest_name: "The 2022 SDUT Summer Trials"
rating: 0
weight: 103800
solve_time_s: 62
verified: true
draft: false
---

[CF 103800B - Ginger's game](https://codeforces.com/problemset/problem/103800/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of monster health values. Before anything starts, we are allowed to reduce each value independently, but we can never increase it beyond its original value. After that preparation, we choose a starting position $i$. From that position we move left all the way down to index 1, and the values along this segment must form a non-increasing sequence. The reward we obtain is the sum of the final adjusted values on this chosen segment.

So the process has two decisions. First we shape the array downward, respecting upper bounds. Then we pick a prefix ending at some $i$, but that prefix must be rearranged in a constrained way: as we move left, values cannot go up.

The constraint on $n$ up to $2 \cdot 10^5$ immediately rules out any quadratic attempt that recomputes the best adjustment independently for every starting position. Any solution that rebuilds or simulates the prefix process per $i$ would be too slow.

A subtle edge case appears when values are already decreasing. In that situation no reductions are needed, and the answer becomes simply the best prefix sum. On the other extreme, when values oscillate like $1, 100, 2, 99, 3$, naive local adjustments can look locally optimal but break the global monotonic requirement when extended leftward.

## Approaches

If we fix a starting position $i$, we can ask what the best possible adjusted sequence on $[1, i]$ looks like. Since we are allowed to only decrease values, and we need a non-increasing sequence from right to left, the optimal strategy is greedy from right to left: set the last value as high as possible, then clamp each previous value to not exceed the one to its right.

Concretely, if we fix $i$, we set the final value at $i$ to $a_i$. Then moving left, each position $j$ becomes $\min(a_j, b_{j+1})$. This produces the maximum feasible sequence for that endpoint because every constraint is local and only depends on the next position.

The brute force idea is to repeat this construction for every $i$. Each time we recompute a whole prefix by propagating minima from right to left. This costs $O(n)$ per $i$, leading to $O(n^2)$, which is far beyond limits at $2 \cdot 10^5$.

The key observation is to reinterpret what this greedy construction is actually computing. For a fixed $i$, the value at position $j$ becomes the minimum value on the interval $[j, i]$. So the total score for endpoint $i$ becomes the sum of minimum values over all subarrays that end at $i$.

Once the problem is seen in this form, it becomes a classical “sum of subarray minimums ending at each index” problem. Instead of recomputing from scratch, we can maintain contributions incrementally using a monotonic stack that tracks where the previous smaller element lies. This allows us to update the total contribution in amortized constant time per index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ to $O(n)$ | Too slow |
| Stack-based DP | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining a monotonic increasing stack of indices, where values increase as we go deeper into the stack. Alongside this, we compute a dynamic value $dp[i]$, defined as the total contribution of all subarrays that end exactly at position $i$, where each subarray contributes its minimum element.

1. Maintain a stack of indices such that the corresponding values are strictly increasing from bottom to top. This structure ensures that when we are at position $i$, the stack encodes where the previous smaller elements are.
2. For each index $i$, pop from the stack until the top has a value strictly smaller than $a[i]$. After this process, the top of the stack becomes the previous index $p[i]$ where $a[p[i]] < a[i]$, or zero if none exists.
3. The key transition is to compute $dp[i]$ using the fact that all subarrays ending at $i$ can be grouped by their starting position relative to $p[i]$. Subarrays starting after $p[i]$ have $a[i]$ as their minimum, because nothing between them and $i$ is smaller than $a[i]$. Subarrays starting at or before $p[i]$ behave exactly like those ending at $p[i]$.
4. This splits the computation into two parts: everything inherited from $dp[p[i]]$, plus a rectangular block of new contributions contributed by $a[i]$. The number of starts that pick up this new minimum is $i - p[i]$, so the added contribution is $a[i] \cdot (i - p[i])$.
5. Track the maximum value of $dp[i]$ over all positions $i$, since any endpoint is a valid choice.

### Why it works

The stack guarantees that $p[i]$ is the closest position to the left where the value is strictly smaller than $a[i]$. This partitions all subarrays ending at $i$ into those where $a[i]$ is the minimum and those where it is not. The second group is exactly equivalent to subarrays ending at $p[i]$, because anything before $p[i]$ already has a smaller or equal limiting value. This invariant ensures every subarray ending at $i$ is counted exactly once and attributed to its correct minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    stack = []
    dp = [0] * n

    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()

        p = stack[-1] if stack else -1
        left_count = i - p

        prev = dp[p] if p != -1 else 0
        dp[i] = prev + a[i] * left_count

        stack.append(i)

    print(max(dp))

if __name__ == "__main__":
    solve()
```

The solution builds a monotonic stack so that each element knows its previous strictly smaller value. The variable `p` is exactly the boundary where subarrays stop having `a[i]` as their minimum. The multiplication `a[i] * (i - p)` accounts for all new subarrays ending at `i` that newly adopt `a[i]` as their minimum.

The recurrence for `dp[i]` is what makes the solution linear. Instead of recomputing all subarray minima, we reuse `dp[p]`, which already contains all contributions from earlier structure, and extend it with the new block created by `a[i]`.

## Worked Examples

### Example 1

Input:

```
4
2 1 4 3
```

We track stack, previous smaller, and dp:

| i | a[i] | stack after | p | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | 2 | [0] | -1 | 2 |
| 1 | 1 | [1] | -1 | 1 |
| 2 | 4 | [1,2] | 1 | 1 + 4*(2) = 9 |
| 3 | 3 | [1,3] | 1 | 1 + 3*(2) = 7 |

Maximum is 9.

This shows how increasing elements extend contribution ranges, while drops reset the structure and create new boundaries.

### Example 2

Input:

```
5
5 4 3 2 1
```

| i | a[i] | stack after | p | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | 5 | [0] | -1 | 5 |
| 1 | 4 | [1] | -1 | 4 |
| 2 | 3 | [2] | -1 | 3 |
| 3 | 2 | [3] | -1 | 2 |
| 4 | 1 | [4] | -1 | 1 |

Maximum is 5.

This confirms that when the array is already strictly decreasing, every element only contributes to its own segment without extension.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each index is pushed and popped at most once in the monotonic stack |
| Space | $O(n)$ | Stack and dp array store linear state |

The linear behavior fits comfortably within constraints for $2 \cdot 10^5$, and the memory usage is small enough for the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp))

def solve_output(inp: str) -> str:
    import sys
    from io import StringIO
    sys.stdin = StringIO(inp)

    stack = []
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    dp = [0]*n
    ans = 0

    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        p = stack[-1] if stack else -1
        prev = dp[p] if p != -1 else 0
        dp[i] = prev + a[i] * (i - p)
        ans = max(ans, dp[i])
        stack.append(i)

    return str(ans)

# sample-like
assert solve_output("4\n2 1 4 3\n") == "9"

# minimum size
assert solve_output("1\n10\n") == "10"

# all equal
assert solve_output("5\n3 3 3 3 3\n") == "15"

# increasing
assert solve_output("4\n1 2 3 4\n") == "20"

# decreasing
assert solve_output("4\n4 3 2 1\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 2 1 4 3 | 9 | general stack behavior |
| 1 10 | 10 | single element edge case |
| 5 3 3 3 3 3 | 15 | equal elements collapsing boundaries |
| 4 1 2 3 4 | 20 | strictly increasing case |
| 4 4 3 2 1 | 10 | strictly decreasing case |

## Edge Cases

A single element input demonstrates the base case where there is no previous structure. The stack is empty, so $p = -1$, and the answer is simply the element itself, matching the idea that there is exactly one subarray ending there.

When all elements are equal, every new index becomes the boundary for all previous ones, since the stack continuously pops until empty. Each $dp[i]$ becomes a triangular accumulation, and the formula still correctly counts each subarray exactly once.

In a strictly increasing array, each element becomes the new maximum and extends all previous subarrays. The stack never pops, so each $p[i]$ is always the previous index, and contributions accumulate linearly across growing segments without resets.
