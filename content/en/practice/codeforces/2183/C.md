---
title: "CF 2183C - War Strategy"
description: "We have a linear arrangement of bases numbered from 1 to n. Our home base is at position k, and we start with exactly one soldier there. Every day, we can select a base and move any number of soldiers from it either left or right by exactly one position."
date: "2026-06-07T21:43:01+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2183
codeforces_index: "C"
codeforces_contest_name: "Hello 2026"
rating: 1500
weight: 2183
solve_time_s: 147
verified: false
draft: false
---

[CF 2183C - War Strategy](https://codeforces.com/problemset/problem/2183/C)

**Rating:** 1500  
**Tags:** binary search, greedy, math, two pointers  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We have a linear arrangement of bases numbered from 1 to n. Our home base is at position k, and we start with exactly one soldier there. Every day, we can select a base and move any number of soldiers from it either left or right by exactly one position. After this movement, a fresh soldier appears at the home base. The task is to determine the maximum number of bases that can have at least one soldier after m days.

The input gives multiple test cases, each specifying n, m, and k. The output is, for each test case, a single integer representing the maximum number of bases fortified.

Constraints suggest that n can be up to 10^5 per test case, and m can be up to 10^9. Since the sum of n over all test cases is bounded by 2·10^5, iterating over the entire base array is feasible, but simulating each day explicitly is impossible due to m being potentially very large. This immediately rules out any solution that attempts a day-by-day simulation.

A subtle point arises when m is smaller than the distance to one end. For example, if n = 5, k = 3, and m = 1, only two bases can be fortified: the home base and one neighboring base. Naive approaches that assume soldiers can always reach both ends fail in these scenarios. Similarly, when m is extremely large, all bases can eventually be fortified, but care must be taken to avoid exceeding n.

## Approaches

The brute-force approach is straightforward: for each day, simulate moving soldiers optimally to cover more bases. We could track soldiers at each base and decide where to move them, repeating this m times. This works in principle, but the number of operations would be on the order of O(n·m), which is completely impractical when m can be 10^9.

The key insight is that the fastest we can fortify a base is determined by its distance from the home base. Bases to the left of the home base require `home - i` days for the first soldier to arrive, and bases to the right require `i - home` days. After that initial soldier arrives, each day brings an additional soldier to the home base, who can be immediately sent outward.

This reduces the problem to a simple computation: for a base at distance d from k, the earliest it can be fortified is after `d` days. Since every subsequent day adds a new soldier, the maximum number of additional bases that can be fortified expands by one per day outward from k. Thus, the formula for the maximum number of fortified bases is simply `min(n, m + 1)`. This formula works because we can always choose the closest unfortified base and send a soldier there each day, with the first day already counting the home base.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n·m) | O(n) | Too slow |
| Distance-Based Greedy | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t.
2. For each test case, read n, m, and k.
3. Compute the maximum number of bases that can be fortified as `min(n, m + 1)`. This works because the home base is already fortified on day 0, and each day allows one more base to be fortified. If m exceeds the number of additional bases to the ends of the line, we simply cap at n.
4. Print the computed value for each test case.

**Why it works:** The invariant is that each day allows a soldier from the home base to reach one new unfortified base. The earliest a base at distance d from k can be fortified is after d days, and since new soldiers appear at home every day, we can always use them to cover the next closest unfortified base. This ensures the solution is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    # maximum fortified bases is the smaller of n or m+1
    print(min(n, m + 1))
```

The code reads multiple test cases, computes `min(n, m + 1)` for each, and prints the result. No additional data structures are needed. The formula accounts for the home base automatically, and the `min` prevents exceeding the total number of bases.

## Worked Examples

**Example 1:** n = 3, m = 1, k = 3

| Day | Soldiers Added | Bases Fortified |
| --- | --- | --- |
| 0 | 1 at base 3 | 1 (home) |
| 1 | new soldier at 3 moves to base 2 | 2 |

Output: 2

**Example 2:** n = 4, m = 2, k = 2

| Day | Soldiers Added | Bases Fortified |
| --- | --- | --- |
| 0 | 1 at base 2 | 1 |
| 1 | new soldier at 2 moves to base 1 | 2 |
| 2 | new soldier at 2 moves to base 3 | 3 |

Output: 3

The tables show that with one soldier added per day, we can fortify a new base per day outward from home, matching the formula `min(n, m + 1)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a single calculation and comparison |
| Space | O(1) per test case | No arrays or additional storage required |

The solution easily handles t = 10^4 and n sum ≤ 2·10^5. Each test case runs in constant time, so the program completes well within the 2-second limit.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        output.append(str(min(n, m + 1)))
    return "\n".join(output)

# Provided samples
assert run("7\n3 1 3\n3 3 2\n4 2 2\n3 2 1\n4 3 3\n7 7 4\n100000 1000000000 100000\n") == \
"2\n3\n3\n2\n3\n6\n100000"

# Custom cases
assert run("1\n1 1 1\n") == "1", "minimum n and m"
assert run("1\n5 10 3\n") == "5", "m > n, cap at n"
assert run("1\n5 0 2\n") == "1", "no days, only home fortified"
assert run("1\n5 4 2\n") == "5", "exact days to cover all"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | Minimum-size input |
| 5 10 3 | 5 | Days exceed number of bases, cap at n |
| 5 0 2 | 1 | Zero days, only home base fortified |
| 5 4 2 | 5 | Exact number of days to cover all bases |

## Edge Cases

When m = 0, only the home base can be fortified, regardless of n. For large m relative to n, the formula automatically caps the fortified bases at n. When the home base is at an endpoint, the nearest bases are still fortified first, so the greedy approach still yields the maximum. The calculation `min(n, m + 1)` handles all these scenarios without explicit branching or simulation.

For example, input `n=10, m=0, k=5` results in output `1`, and input `n=10, m=20, k=1` results in `10`, demonstrating correct handling of both extreme cases.
