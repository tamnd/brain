---
title: "CF 104314B - Inequalities"
description: "We are given a row that alternates between empty positions and fixed comparison symbols. There are $N+1$ positions that must be filled with distinct numbers from 1 to $N+1$, and between every two neighboring positions there is exactly one constraint, either “<” or “”, which must…"
date: "2026-07-01T19:39:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104314
codeforces_index: "B"
codeforces_contest_name: "XXV Interregional Programming Olympiad, Vologda SU, 2023"
rating: 0
weight: 104314
solve_time_s: 72
verified: true
draft: false
---

[CF 104314B - Inequalities](https://codeforces.com/problemset/problem/104314/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row that alternates between empty positions and fixed comparison symbols. There are $N+1$ positions that must be filled with distinct numbers from 1 to $N+1$, and between every two neighboring positions there is exactly one constraint, either “<” or “>”, which must be satisfied by the two numbers placed next to it.

The task is to determine whether we can assign a permutation of size $N+1$ to these positions so that every inequality holds. If it is possible, we must output one valid permutation; otherwise we output -1.

The constraints allow $N$ up to $10^5$, so any solution must run in linear or near-linear time. Anything involving backtracking over permutations is immediately impossible because even $O(N!)$ or $O(2^N)$ approaches explode. Even $O(N^2)$ constructions would be too slow since $10^5$ squared is already far beyond limits.

A subtle failure case appears when a greedy construction chooses local minima or maxima without respecting future constraints. For example, if we try to always place the smallest possible number whenever we see a “<”, we may block later “>” chains that require a previously large value in the middle.

Another edge case is long alternating chains like “< > < > < …”. Many naive greedy strategies fail here because they do not correctly distribute values across peaks and valleys, even though a valid solution always exists.

## Approaches

A brute-force interpretation is to try all permutations of numbers 1 to $N+1$ and check whether each one satisfies the inequalities. This is correct because it directly tests the definition of validity, but it requires generating $(N+1)!$ permutations, and even checking one permutation costs $O(N)$, making the total complexity astronomically large.

The structure of the problem is actually governed by relative ordering rather than absolute values. Each inequality chain forces a pattern of increasing and decreasing segments. If we look at a segment of consecutive “<” signs, the numbers must strictly increase along that segment. Similarly, a segment of consecutive “>” signs forces a strictly decreasing structure. The key observation is that the permutation can be built incrementally by deciding which positions behave like “valleys” and which behave like “peaks”.

Instead of assigning numbers directly, we reverse the perspective: think of inserting numbers from 1 to $N+1$ in increasing order and deciding where each number should go so that all constraints remain valid. A classic way to satisfy such inequality chains is to process blocks of consecutive “>” signs by assigning decreasing values over that block, which naturally requires a stack-like reversal of order.

We scan the sequence and break it into maximal segments where the inequality is “>”. Whenever we encounter such a segment, we know the corresponding block in the permutation must be assigned in reverse order. This leads to a construction where we append indices normally, but reverse segments whenever needed.

The brute-force works because it explicitly tests correctness, but fails due to factorial growth. The observation that the structure decomposes into monotone runs allows us to construct a valid permutation in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((N+1)! \cdot N)$ | $O(N)$ | Too slow |
| Optimal | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We build the answer using a greedy scan over the inequality string, grouping positions into blocks that must be reversed.

1. Initialize an empty list `res` that will hold the final permutation.
2. Iterate through positions from 0 to $N$, treating each position as a boundary between numbers.
3. Whenever we encounter a position where the current segment of inequalities contains only “>”, we accumulate indices into a temporary buffer.
4. As soon as we hit a “<” or reach the end, we flush the buffer. Flushing means appending the collected indices in reverse order to `res`.
5. Continue this process until all positions are processed, ensuring that every maximal “>” chain is reversed exactly once.

The reason we only reverse on “>” segments is that a chain of “>” forces decreasing values from left to right. If we assign increasing indices naturally, we would violate the constraint, so we flip the order locally.

### Why it works

Each maximal segment of consecutive “>” constraints enforces a strictly decreasing ordering on the values placed in that segment. By collecting indices in forward order and then reversing them when outputting, we ensure that larger numbers appear earlier in that segment and smaller numbers appear later, satisfying all inequalities. Between segments, the transition points correspond exactly to “<”, which preserve natural increasing order across block boundaries. This guarantees every constraint is satisfied independently and the global permutation remains valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().split()
    
    res = []
    i = 0
    
    while i <= n:
        j = i
        while j < n and s[j] == '>':
            j += 1
        
        # we have a segment [i, j]
        # for '>' segment, we reverse
        for k in range(j, i - 1, -1):
            res.append(k + 1)
        
        i = j + 1
    
    print(*res)

if __name__ == "__main__":
    solve()
```

The code follows the idea of scanning consecutive “>” segments and reversing indices inside each such block. The expression `k + 1` converts zero-based positions into the required permutation values.

The key implementation detail is handling the boundary correctly: when we finish a “>” segment, we must include both endpoints in reversed order. Off-by-one errors typically arise here, especially in deciding whether the segment ends at `j` or `j-1`.

## Worked Examples

### Example 1

Input:

```
2
< >
```

We process positions 0 to 2.

| i | j | segment type | action | res |
| --- | --- | --- | --- | --- |
| 0 | 0 | "<" | append [1] | [1] |
| 1 | 1 | ">" segment ends immediately | reverse [2,1]? local block | [1,3,2] |

This trace shows how the single “>” forces the pair (3,2) in reversed order, while the “<” allows increasing placement at the start.

The resulting permutation satisfies both constraints: 1 < 3 and 3 > 2.

### Example 2

Input:

```
3
> < <
```

We process step by step.

| i | j | segment | action | res |
| --- | --- | --- | --- | --- |
| 0 | 1 | ">" | reverse [1,2] | [2,1] |
| 2 | 2 | "<" | append [3] | [2,1,3] |
| 3 | 3 | "<" | append [4] | [2,1,3,4] |

This demonstrates that a decreasing prefix is correctly handled, while the remaining positions follow natural increasing order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each index is visited once and appended once |
| Space | $O(N)$ | Output array stores $N+1$ values |

The linear scan is sufficient for $N \le 10^5$, and no extra data structures beyond the output list are needed, so both memory and time constraints are comfortably satisfied.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("2\n< >\n") == "1 3 2"

# minimum case
assert run("1\n<\n") == "1 2"

# simple decreasing
assert run("1\n>\n") == "2 1"

# alternating pattern
assert run("3\n> < >\n") in ["2 1 4 3", "3 1 4 2"]

# all increasing
assert run("4\n< < < <\n") == "1 2 3 4 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n< | 1 2 | smallest valid increasing case |
| 1\n> | 2 1 | single inversion |
| 3\n> < > | 2 1 4 3 (or equivalent valid form) | alternating structure |
| 4\n< < < < | 1 2 3 4 5 | fully increasing chain |

## Edge Cases

One edge case is a fully decreasing prefix like “> > > >”. The algorithm collects the entire prefix as a single segment and reverses it, producing a strictly decreasing sequence at the start. For input:

```
4
> > > >
```

The scan forms one segment covering all indices 0 to 4, and the output becomes [5, 4, 3, 2, 1], which satisfies all constraints.

Another edge case is when there are no “>” signs at all:

```
3
< < <
```

Here no reversal occurs, so the indices are appended in natural order, producing [1, 2, 3, 4], which correctly satisfies all inequalities.

A mixed boundary case like “< > > <” shows that the algorithm correctly splits into independent monotone blocks, ensuring no interaction between segments that would otherwise force contradictory ordering.
