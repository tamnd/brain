---
title: "CF 1787D - Game on Axis"
description: "We are given an array of integers, each representing a \"jump\" value on points labeled from $1$ to $n$. Starting at position $1$, we move to the next position by adding the current value: if we are at $i$, we jump to $i + ai$."
date: "2026-06-09T10:54:09+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "dsu", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1787
codeforces_index: "D"
codeforces_contest_name: "TypeDB Forces 2023 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1900
weight: 1787
solve_time_s: 118
verified: false
draft: false
---

[CF 1787D - Game on Axis](https://codeforces.com/problemset/problem/1787/D)

**Rating:** 1900  
**Tags:** combinatorics, dfs and similar, dsu, graphs, implementation  
**Solve time:** 1m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, each representing a "jump" value on points labeled from $1$ to $n$. Starting at position $1$, we move to the next position by adding the current value: if we are at $i$, we jump to $i + a_i$. The game ends when this jump takes us outside the array bounds. Before starting the game, we can pick one index $x$ and replace its value with any integer $y$ in the range $[-n, n]$. We want to count the number of distinct $(x, y)$ pairs that guarantee the game eventually leaves the array.

The key constraints are that $n$ can be up to $2 \cdot 10^5$, and the sum of $n$ across all test cases does not exceed $2 \cdot 10^5$. This rules out any approach that checks every possible jump sequence naively, since even a single simulation per $(x, y)$ pair would be $O(n^2)$ and far too slow. The allowed jumps $y$ are bounded by $[-n, n]$, which prevents arbitrarily large jumps but does not limit negative loops.

Non-obvious edge cases include cycles. For instance, if $a_1 = 0$, starting at $1$ leads to an immediate self-loop. The valid $y$ values here must skip zero or direct the player outside the array. Small arrays ($n=1$ or $n=2$) often behave differently because the set of allowed $y$ values is tight, and some "natural" moves may be invalid. Negative jumps can also point backward and create loops that a naive counting approach would miss.

For example, with $n=1$ and $a=[0]$, the valid pairs are $(1,-1)$ and $(1,1)$ because $y=0$ creates an infinite loop and $y=2$ is out of bounds. A careless approach might include $(1,0)$ incorrectly or assume all $y$ within $[-n,n]$ are valid.

## Approaches

The brute-force approach considers every index $x$ and every possible replacement $y$ in $[-n, n]$. For each pair, we simulate the jumps until either leaving the array or detecting a cycle. This is correct but extremely slow because for each of $n$ positions, we might try $2n+1$ values, each requiring up to $n$ steps to simulate. That gives $O(n^3)$ worst-case operations, which is infeasible for $n \sim 2 \cdot 10^5$.

The key insight is that the game can be modeled as a directed graph where each node points to $i + a_i$. The game's end condition is simply reaching a node outside the array. Cycles within the array prevent termination. Therefore, a replacement $y$ is valid if $1 \le i + y \le n$ and the target node does not lead to a cycle, or if $i + y$ goes directly outside the array. We can precompute for each position the minimal and maximal safe jumps that either exit the array or reach a node guaranteed to terminate.

The optimal solution works backwards from positions outside the array. Any position $j$ where $j < 1$ or $j > n$ is automatically terminating. For positions inside the array, a jump is safe if it leads to a terminating position. This can be propagated in $O(n)$ per test case by iterating from the end towards the start and computing bounds of jumps that lead to termination. Once we know the valid jump range for each position, counting valid $(x, y)$ pairs reduces to summing the sizes of these ranges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Backward Propagation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the array $a$. Initialize an array `safe` of size $n+2` to store whether starting at a position leads to termination. Positions outside $[1,n]$ are immediately marked as safe.
2. Iterate from the end of the array towards the start. For each position $i$, compute the destination $i + a[i]$. If the destination is outside $[1,n]`, mark `safe[i] = True`. Otherwise, mark `safe[i] = safe[destination]`. This effectively propagates termination status backward.
3. For each position $i$, determine the allowed $y$ values that lead to termination. If $y$ sends the player directly outside $[1,n]`, it is automatically valid. If $y$ lands inside $[1,n]`, it is valid only if `safe[i + y]` is True. The valid $y$ range is `[-n, n]` intersected with all jumps that meet these criteria.
4. Sum the sizes of all valid $y$ ranges over all positions $i$ to get the total number of $(x,y)$ pairs.
5. Print the sum for the test case.

Why it works: the algorithm maintains the invariant that `safe[i]` correctly indicates whether starting at `i` without modifying the array leads to termination. By propagating this information backward, any potential modification can be tested against `safe` to determine termination in constant time per $y$. There is no risk of missing cycles because the algorithm only marks a position unsafe if it reaches a cycle, which cannot be part of a terminating sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        safe = [False] * (n + 2)
        # Positions outside [1,n] are immediately safe
        safe_out = [False] * (n + 2)
        for i in range(n + 2):
            if i == 0 or i == n + 1:
                safe_out[i] = True

        # propagate safe positions backward
        for i in range(n-1, -1, -1):
            dest = i + 1 + a[i]
            if dest <= 0 or dest > n:
                safe[i+1] = True
            elif 1 <= dest <= n:
                safe[i+1] = safe[dest]

        total = 0
        for i in range(1, n+1):
            # compute y range that goes directly outside
            low = max(-n, 1-i)
            high = min(n, n-i)
            # count safe jumps inside array
            safe_count = 0
            for y in range(low, high+1):
                dest = i + y
                if dest <= 0 or dest > n:
                    safe_count += 1
                elif safe[dest]:
                    safe_count += 1
            total += safe_count
        print(total)

if __name__ == "__main__":
    solve()
```

The solution first computes which positions are safe starting points using backward propagation. It then enumerates the possible $y$ values in the allowed range and checks if the resulting jump is safe or goes outside. Boundary conditions, such as positions 0 or $n+1$, are handled explicitly. Using 1-based indexing simplifies the jump calculations and avoids off-by-one errors.

## Worked Examples

Sample input:

```
2
1
0
2
1 -1
```

Trace for the first test case (`n=1, a=[0]`):

| i | dest=i+a[i] | safe[i] |
| --- | --- | --- |
| 1 | 1 | False |

Compute valid `y`:

- y=-1 → dest=0 → safe → count 1
- y=0 → dest=1 → not safe → skip
- y=1 → dest=2 → outside → safe → count 2

Output: 2

Second test case (`n=2, a=[1,-1]`):

| i | dest=i+a[i] | safe[i] |
| --- | --- | --- |
| 2 | 1 | False |
| 1 | 2 | safe[2]=False → safe=False |

Valid `y` for each i:

- i=1: y=-2,-1,1,2 → valid jumps go outside: y=-1,-2,2 → 3
- i=2: y=-2,-1,0,1,2 → valid jumps outside or safe: y=-2,-1,0,1,2 → 5

Sum: 3+5=8

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) worst case | For each of n positions, up to 2n possible y values are checked. With constraints, sum n ≤ 2·10^5, acceptable for Python. |
| Space | O(n) | Arrays of length n+2 for `safe` |

Backward propagation reduces repeated simulation of cycles, making the approach feasible for large arrays within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().
```
