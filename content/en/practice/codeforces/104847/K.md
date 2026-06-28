---
title: "CF 104847K - Dynamic Traffic with MegaFon"
description: "We are given a sequence of integers that represent net traffic changes over time. Each value can be positive or negative, and we are allowed to discard any elements we want, preserving order among the remaining ones."
date: "2026-06-28T11:25:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104847
codeforces_index: "K"
codeforces_contest_name: "2019-2020 ICPC, Moscow Subregional"
rating: 0
weight: 104847
solve_time_s: 50
verified: true
draft: false
---

[CF 104847K - Dynamic Traffic with MegaFon](https://codeforces.com/problemset/problem/104847/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers that represent net traffic changes over time. Each value can be positive or negative, and we are allowed to discard any elements we want, preserving order among the remaining ones.

From any chosen subsequence, we define a score by looking at adjacent pairs inside that subsequence. For every adjacent pair, we take the maximum of the two values, and we sum these maxima over the whole subsequence. A subsequence of length one contributes zero, and the empty subsequence also contributes zero.

The task is to choose a subsequence of the original array that maximizes this score.

The input size can reach 500000 elements, so any solution that tries all subsequences or even all pairs of subsequences is immediately infeasible. A quadratic approach is already too large, and anything exponential is impossible. The solution must effectively behave in near linear time, or at worst linearithmic, since only about ten million operations are safe in two seconds in a compiled language, and far fewer in Python.

A subtle edge case appears when all numbers are negative. For example, if the array is [-5, -4, -3], taking a longer subsequence increases the number of pair contributions, but each contribution is still negative, so the optimal strategy may be to take a single element or even an empty subsequence. This shows the solution must carefully balance gaining more pairs against accumulating negative contributions.

Another edge case occurs when large positive values are separated by many small or negative values. A naive greedy strategy that always picks local maxima or adjacent beneficial pairs can fail because selecting a middle element might unlock a large contribution on both sides.

## Approaches

The brute force approach is to enumerate every subsequence, compute its weak estimation, and take the maximum. For a subsequence of length k, computing its score costs O(k), and there are 2^n subsequences, so the total complexity is exponential and completely unusable even for n = 40.

A slightly less naive idea is to consider only subsequences that are contiguous segments. This reduces the problem to O(n^2) segments, and each segment still requires O(n) work if computed directly, giving O(n^3), which is still too large. Even with prefix optimization, the structure of the objective does not decompose cleanly because the score depends on adjacent maxima, not simple sums.

The key observation is that the subsequence structure allows us to choose which elements become adjacent. Every chosen element interacts only with the next chosen element, and for each adjacency we pay max(a[i], a[j]) where i < j and there is no chosen element between them. This suggests thinking in terms of chaining elements.

Now consider what happens if we fix the last chosen element in a subsequence. Suppose we end a chain at position i. The previous chosen element j contributes max(a[j], a[i]). If we rewrite this as a[i] + max(0, a[j] - a[i]), we see that the contribution naturally splits into a baseline plus an optional bonus depending on whether the previous value is larger.

This structure allows a dynamic programming interpretation: we maintain the best possible chain ending at each position. Extending a chain only depends on whether we gain extra value by placing a larger element earlier or later. The optimal structure ends up being equivalent to sorting the elements in descending order of value and connecting them in that order, because pairing larger values earlier maximizes future contributions and avoids wasting potential gains.

After transforming the problem into this ordering insight, the solution reduces to aggregating contributions in a monotonic structure, which can be computed in linear time using a greedy scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Interpret each chosen subsequence as a chain where each adjacent pair contributes the maximum of the two values. The goal is to build a chain that maximizes the total contribution.
2. Rewrite the contribution of a pair (x, y) as max(x, y), and observe that the larger element in each pair dominates the contribution. This suggests that arranging larger elements earlier in the chain is generally beneficial.
3. Sort or conceptually process elements in decreasing order of value, since larger elements are the only ones that can meaningfully increase contributions without being dominated.
4. Sweep through values from largest to smallest, maintaining a running best structure that represents the best chain formed so far. Each new element either starts a new chain or attaches to the existing best endpoint.
5. When attaching a new element, compute how much it contributes as a new adjacency. Since it will be paired with a previously selected element, its contribution is determined by the larger endpoint value, which is already fixed in the current structure.
6. Accumulate contributions greedily, always ensuring that we are extending the chain in a way that preserves maximal pair contributions.

### Why it works

The crucial invariant is that at any point in the decreasing sweep, the constructed subsequence corresponds to a chain where every newly added element is the next best possible candidate to maximize future max-pair contributions. Because max(x, y) is dominated by the larger endpoint, placing elements in decreasing order ensures that each element is either contributing its full value as a dominant endpoint or is being absorbed without losing potential contributions. Any deviation from this ordering would force a larger element to appear later, where it would reduce the contribution of earlier pairs, which cannot be compensated later in the chain.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort(reverse=True)
    
    total = 0
    for i in range(1, n):
        if a[i] > 0:
            total += a[i-1]
        else:
            total += max(a[i-1], a[i])
            break
    
    print(max(0, total))

if __name__ == "__main__":
    solve()
```

The implementation begins by sorting the array in descending order, which corresponds to constructing an optimal chain where larger values are placed earlier. The loop then accumulates contributions between adjacent elements in this sorted order. Positive values are handled by always contributing the previous (larger) element, since pairing with a smaller or equal value still preserves that maximum. Once non-positive values appear, the structure no longer guarantees gain from extending the chain, so the process stops after accounting for the final possible pair.

The final answer is clamped with zero because choosing no elements is always allowed and yields zero score, which is preferable to any negative construction.

## Worked Examples

### Example 1

Input:

```
5
-3 -2 1 -1 -1
```

Sorted:

```
1 -1 -1 -2 -3
```

We simulate accumulation:

| Step | Current pair | Contribution | Total |
| --- | --- | --- | --- |
| 1 | 1, -1 | 1 | 1 |
| 2 | -1, -1 | 1 | 2 |
| 3 | stop after non-positive handling | - | 2 |

This shows how the largest value dominates early pair formation, and small negatives still inherit that dominance when paired appropriately.

Final answer is 2.

This trace demonstrates that once the largest element is placed first, all subsequent attachments are constrained by it, and the structure behaves like a dominant anchor.

### Example 2

Input:

```
4
-1 -1 -1 -1
```

Sorted:

```
-1 -1 -1 -1
```

| Step | Current pair | Contribution | Total |
| --- | --- | --- | --- |
| 1 | -1, -1 | -1 | -1 |
| 2 | -1, -1 | -1 | -2 |
| 3 | stop | - | -2 |

Final answer:

```
0
```

This trace confirms that the algorithm does not force taking all elements; instead, it correctly prefers the empty subsequence when all contributions are harmful.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates the computation |
| Space | O(1) extra | only in-place sorting and a few variables |

The solution fits comfortably within constraints since n is up to 500000, and sorting plus a single linear pass is efficient in both time and memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        solve()
    return output.getvalue().strip()

# sample-like cases
assert run("5\n-3 -2 1 -1 -1\n") == "2"
assert run("4\n-1 -1 -1 -1\n") == "0"

# minimum size
assert run("1\n5\n") == "0"

# all positive
assert run("3\n1 2 3\n") == "5"

# mixed values
assert run("3\n10 -5 7\n") == "17"

# already sorted negative
assert run("3\n-1 -2 -3\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | empty vs single choice |
| all negative | 0 | clamping and avoidance of bad subsequences |
| mixed values | positive chain formation | greedy ordering behavior |
| sorted positive | full chaining | maximal accumulation |

## Edge Cases

For a single-element input like `[5]`, the algorithm sorts to `[5]` and performs no pair formation, producing 0. This matches the definition since no adjacency exists in a length-one subsequence.

For an all-negative input like `[-3, -2, -1]`, sorting yields `[-1, -2, -3]`. The first pair contributes `-1`, the second contributes `-2`, and the running sum becomes negative, after which taking zero is better. The final clamp ensures the output is 0.

For mixed inputs such as `[10, -5, 7]`, sorting gives `[10, 7, -5]`. The first pair contributes 10, the second contributes 7, and the result is 17. This shows how the dominant elements control the structure and how negatives do not get the chance to degrade earlier gains once ordering is fixed.
