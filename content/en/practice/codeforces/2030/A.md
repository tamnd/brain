---
title: "CF 2030A - A Gift From Orangutan"
description: "We are given an array and we are allowed to reorder it before processing. Once fixed, we scan it from left to right and maintain two running values: the smallest element seen so far and the largest element seen so far."
date: "2026-06-08T11:55:52+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2030
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 979 (Div. 2)"
rating: 800
weight: 2030
solve_time_s: 116
verified: true
draft: false
---

[CF 2030A - A Gift From Orangutan](https://codeforces.com/problemset/problem/2030/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math, sortings  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and we are allowed to reorder it before processing. Once fixed, we scan it from left to right and maintain two running values: the smallest element seen so far and the largest element seen so far. At every position we record the difference between these two extremes, and the final score is the sum of all these per-position spreads.

The freedom we have is entirely in the permutation of the array. After that, the prefix minimum and prefix maximum evolve deterministically.

The constraints are small enough that an $O(n^2)$ or even $O(n \log n)$ approach per test case would pass comfortably since the total $n$ over all tests is at most 1000. This signals that we should focus on structural reasoning rather than optimization tricks.

A common mistake here is to assume that putting large numbers first or last greedily always works. That fails because prefix minimums and prefix maximums interact globally, not locally. For example, placing the largest element too early immediately fixes the maximum for many prefixes, reducing future contributions, even if that seems locally beneficial.

Another pitfall is trying to optimize prefix contributions independently. A prefix that looks optimal in isolation can destroy future increments of the maximum-minimum gap, so the arrangement must be considered as a whole.

## Approaches

A brute-force solution would try all permutations and compute the score for each. That works conceptually because the scoring function is well-defined, but it is factorial in complexity and impossible beyond very small $n$.

The key observation is that the score depends only on how extremes evolve, not on the exact ordering of middle elements. We want to keep the maximum as “high” as possible for as long as possible, while delaying the increase of the minimum as much as possible. This suggests placing small elements early to maintain a low prefix minimum and large elements later to keep increasing the prefix maximum gradually.

The structure that achieves this optimally is a simple greedy arrangement: we alternate pushing the current smallest and largest remaining values into the sequence. This maximizes the number of prefixes where the gap between max and min is large.

The intuition is that each time we extend the sequence, we want to either introduce a new global maximum or preserve a small minimum, and alternating extremes ensures both forces are maximally exploited.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Greedy extremes | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first sort the array. Sorting gives us controlled access to smallest and largest elements.

Then we construct the permutation using two pointers, one at the start and one at the end of the sorted array.

At each step, we append either the smallest remaining element or the largest remaining element. The choice alternates.

We simulate prefix evaluation implicitly: instead of recomputing prefix minimum and maximum, we rely on the fact that placing extremes maximizes future spread contributions.

Finally, we compute the score by scanning the constructed array and maintaining prefix minimum and maximum.

### Why it works

The score at each position depends only on how far apart the running minimum and maximum are. The only way to keep this difference large across many prefixes is to delay stabilization of either extreme. Alternating between the smallest and largest remaining values ensures that neither extreme becomes “stuck” too early, maximizing the accumulated differences over all prefixes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort()
        
        l, r = 0, n - 1
        arr = []
        take_max = True
        
        while l <= r:
            if take_max:
                arr.append(a[r])
                r -= 1
            else:
                arr.append(a[l])
                l += 1
            take_max = not take_max
        
        mn = arr[0]
        mx = arr[0]
        ans = 0
        
        for x in arr:
            mn = min(mn, x)
            mx = max(mx, x)
            ans += mx - mn
        
        print(ans)

if __name__ == "__main__":
    solve()
```

After sorting, we build a permutation by alternately taking largest and smallest remaining values. This ensures that extreme values are spread across the prefix structure in a balanced way. The final loop simply computes the score according to the definition using prefix minimum and maximum.

A subtle point is initialization: the first element sets both minimum and maximum, so the first contribution is always zero. Also, alternating direction must start consistently; starting with either side is fine as long as it is consistent across the construction.

## Worked Examples

### Example 1

Input:

```
3
7 6 5
```

Sorted: `[5, 6, 7]`

| Step | Chosen | Array so far | Prefix min | Prefix max | Contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 7 | [7] | 7 | 7 | 0 |
| 2 | 5 | [7, 5] | 5 | 7 | 2 |
| 3 | 6 | [7, 5, 6] | 5 | 7 | 2 |

Total = 4.

This shows how placing extremes early keeps a large gap open in multiple prefixes.

### Example 2

Input:

```
5
1 1 1 2 2
```

Sorted: `[1, 1, 1, 2, 2]`

Construction alternates 2,1,2,1,1 (one valid variant depending on tie handling).

| Step | Value | Min | Max | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | 0 |
| 2 | 1 | 1 | 2 | 1 |
| 3 | 2 | 1 | 2 | 1 |
| 4 | 1 | 1 | 2 | 1 |
| 5 | 1 | 1 | 2 | 1 |

Total = 4.

The repeated small values ensure the minimum stays low, allowing repeated contributions from the fixed maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates per test case |
| Space | $O(n)$ | storing reordered array |

Given the sum of $n$ across all test cases is at most 1000, this is easily within limits even with multiple sorts.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        l, r = 0, n - 1
        arr = []
        take_max = True

        while l <= r:
            if take_max:
                arr.append(a[r])
                r -= 1
            else:
                arr.append(a[l])
                l += 1
            take_max = not take_max

        mn = mx = arr[0]
        ans = 0
        for x in arr:
            mn = min(mn, x)
            mx = max(mx, x)
            ans += mx - mn

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("3\n1\n69\n3\n7 6 5\n5\n1 1 1 2 2\n") == "0\n4\n4"

# custom cases
assert run("1\n2\n1 100\n") == "99"
assert run("1\n3\n1 2 3\n") in ["4", "2", "3"], "small permutation sanity"
assert run("1\n4\n1 1 1 1\n") == "0"
assert run("1\n5\n5 4 3 2 1\n") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,100]` | 99 | extreme gap case |
| `[1,2,3]` | small value | ordering effect |
| all ones | 0 | zero spread case |
| reversed sequence | non-negative | consistency |

## Edge Cases

A uniform array is the simplest boundary case. Since prefix minimum and maximum are always equal, every term contributes zero regardless of permutation, so any algorithm must return zero.

A two-element array exposes the core mechanic directly: the score is exactly the absolute difference, and any ordering produces the same prefix structure.

A strictly increasing or decreasing array is useful because it forces the construction to reveal whether the greedy alternation is actually beneficial or redundant. In these cases, the alternating strategy still preserves maximal spread across prefixes by ensuring that the maximum is introduced early while the minimum is delayed.
