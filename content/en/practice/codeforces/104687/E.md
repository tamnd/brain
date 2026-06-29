---
title: "CF 104687E - \u0421\u0442\u0440\u043e\u043a\u0430-1"
description: "We are given a binary string, only consisting of zeros and ones. We measure disorder using inversions: every pair of positions where a one appears before a zero contributes one unit."
date: "2026-06-29T08:46:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "E"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 55
verified: true
draft: false
---

[CF 104687E - \u0421\u0442\u0440\u043e\u043a\u0430-1](https://codeforces.com/problemset/problem/104687/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string, only consisting of zeros and ones. We measure disorder using inversions: every pair of positions where a one appears before a zero contributes one unit. The task is to reduce this inversion count as much as possible, with the extra freedom of performing at most one operation that swaps two neighboring characters.

So we start with a fixed configuration of zeros and ones, we may optionally pick one adjacent pair and swap it once, and we want to know the smallest inversion count achievable among all such choices, including the choice of doing nothing.

The string length is at most 100, which already suggests that even quadratic behavior per candidate operation is acceptable. Anything cubic or worse is also technically fine here, but we should aim for a clean quadratic solution since the structure is simple.

A naive pitfall appears when assuming that swapping a local pair only affects inversions involving those two characters in an obvious linear way without carefully recomputing. For example, in a string like `1010`, swapping the middle `10` to `01` changes not only the inversion formed by that pair but also how those characters interact with others on both sides. Any approach that tries to update inversion count with an overly local heuristic tends to miss these cross effects.

Another subtle issue is forgetting the option of doing no swap at all. In some cases the initial string is already optimal, for example `000111`, where any swap would only increase disorder.

## Approaches

The direct way to think about the problem is to try every valid state we can reach. There are only two kinds: the original string, and all strings obtained by swapping one adjacent pair. For each such string, we can compute the inversion count from scratch by scanning all pairs and counting how many times a `1` precedes a `0`.

This works because the constraints are tiny, but it is redundant. If the string has length n, then there are n-1 possible swaps. Computing inversions from scratch for one string takes O(n²), so the total becomes O(n³). This is still borderline acceptable for n ≤ 100, but it wastes structure.

The key observation is that swapping two adjacent elements does not globally reshape the string. Only the relative order of the swapped elements with respect to the rest of the array changes. Everything else remains identical. That means we do not need to recompute everything from scratch if we are willing to reason carefully about how inversion contributions change.

However, in practice the cleanest implementation for n ≤ 100 is still to recompute inversions in O(n) or O(n²) per swap candidate. The structure is small enough that simplicity wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force recompute all pairs for each swap | O(n³) | O(1) | Accepted for constraints |
| Recompute inversions per swap in O(n) or O(n²) | O(n²) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the answer as the minimum between doing no operation and doing exactly one swap at some position.

1. Compute the inversion count of the original string. This is our baseline answer. Every pair (i, j) with i < j contributes if the character at i is 1 and at j is 0.
2. Initialize the answer with this baseline value. This corresponds to the choice of not performing any swap.
3. For every index i from 0 to n − 2, consider swapping characters at positions i and i + 1. Construct the resulting string after this swap. The reason we explicitly rebuild the string is that n is small and correctness is more important than micro-optimization.
4. For each swapped configuration, compute its inversion count from scratch by scanning all pairs (j, k) with j < k and counting when a 1 precedes a 0. This gives the exact cost of that swap choice without relying on fragile incremental reasoning.
5. Update the answer with the minimum over all swap positions and the original configuration.

The final stored value is the best achievable inversion count.

### Why it works

Any valid final configuration is either the original string or differs from it by exactly one adjacent transposition. Since we enumerate all such possibilities and compute their exact inversion counts, no reachable state is missed. Because inversion counting is recomputed exactly rather than approximated, there is no risk of undercounting or overcounting due to local assumptions. The algorithm is exhaustive over the reachable state space defined by the operation constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def inversion_count(s):
    n = len(s)
    cnt = 0
    for i in range(n):
        if s[i] == '1':
            for j in range(i + 1, n):
                if s[j] == '0':
                    cnt += 1
    return cnt

def solve():
    s = input().strip()
    n = len(s)

    best = inversion_count(s)

    s = list(s)
    for i in range(n - 1):
        s[i], s[i + 1] = s[i + 1], s[i]
        best = min(best, inversion_count(s))
        s[i], s[i + 1] = s[i + 1], s[i]

    print(best)

if __name__ == "__main__":
    solve()
```

The solution first defines a direct inversion counter that scans all ordered pairs and counts occurrences of a `1` followed by a `0`. This is used both for the initial configuration and for every swapped variant.

The main loop tries each adjacent swap exactly once, performs it in place, evaluates the resulting inversion count, and then restores the original string. The restore step is essential; forgetting it would accumulate multiple swaps and break the constraint of “at most one operation”.

## Worked Examples

### Example 1

Input:

`01101`

We track baseline and swap candidates.

| State | String | Inversion count |
| --- | --- | --- |
| initial | 01101 | 2 |
| swap i=0 | 10101 | 3 |
| swap i=1 | 00101 | 1 |
| swap i=2 | 01001 | 2 |
| swap i=3 | 01110 | 1 |

The best result is 1, achieved by swapping positions 1 and 2. This shows that a local improvement can propagate globally because moving a zero left reduces multiple future inversions at once.

### Example 2

Input:

`11100`

| State | String | Inversion count |
| --- | --- | --- |
| initial | 11100 | 6 |
| swap i=0 | 11100 | 6 |
| swap i=1 | 11100 | 6 |
| swap i=2 | 11010 | 5 |
| swap i=3 | 11001 | 4 |

The best result is 4, achieved by swapping near the boundary between ones and zeros. This demonstrates that beneficial swaps typically occur at the interface between blocks of identical characters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) worst-case, effectively O(n²) in practice | n swaps, each recomputing inversions in O(n²) |
| Space | O(1) | only in-place string manipulation |

With n ≤ 100, the worst-case operation count is about 10⁶, which is comfortably within limits for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    # re-run solution
    input = sys.stdin.readline

    def inversion_count(s):
        n = len(s)
        cnt = 0
        for i in range(n):
            if s[i] == '1':
                for j in range(i + 1, n):
                    if s[j] == '0':
                        cnt += 1
        return cnt

    s = input().strip()
    n = len(s)
    best = inversion_count(s)
    s = list(s)
    for i in range(n - 1):
        s[i], s[i + 1] = s[i + 1], s[i]
        best = min(best, inversion_count(s))
        s[i], s[i + 1] = s[i + 1], s[i]
    return str(best)

# provided sample
assert run("01101\n") == "1"

# all zeros
assert run("0000\n") == "0"

# all ones
assert run("1111\n") == "0"

# single beneficial swap
assert run("10\n") == "0"

# no beneficial swap
assert run("0011\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 01101 | 1 | sample correctness |
| 0000 | 0 | no inversions case |
| 1111 | 0 | all ones, no zeros |
| 10 | 0 | minimal inversion removable |
| 0011 | 0 | swap does not worsen optimal |

## Edge Cases

For a fully sorted string like `000111`, the initial inversion count is zero. Any adjacent swap would introduce at least one inversion because it creates a local `10` pattern. The algorithm evaluates the original string first, so the answer remains zero even if all swaps are worse.

For a fully reversed string like `111000`, inversions are maximized initially. Swapping near the boundary, such as positions 2 and 3, reduces multiple cross-block inversions at once. The algorithm explicitly evaluates these boundary swaps and captures the improvement because it recomputes the full inversion count after each swap rather than assuming local effects.
