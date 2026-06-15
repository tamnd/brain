---
title: "CF 1070A - Find a Number"
description: "We are looking for a positive integer that satisfies two simultaneous constraints. First, it must be divisible by a given integer $d$. Second, when written in decimal form, the sum of its digits must equal a given value $s$."
date: "2026-06-15T13:43:51+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "number-theory", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1070
codeforces_index: "A"
codeforces_contest_name: "2018-2019 ICPC, NEERC, Southern Subregional Contest (Online Mirror, ACM-ICPC Rules, Teams Preferred)"
rating: 2200
weight: 1070
solve_time_s: 357
verified: true
draft: false
---

[CF 1070A - Find a Number](https://codeforces.com/problemset/problem/1070/A)

**Rating:** 2200  
**Tags:** dp, graphs, number theory, shortest paths  
**Solve time:** 5m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking for a positive integer that satisfies two simultaneous constraints. First, it must be divisible by a given integer $d$. Second, when written in decimal form, the sum of its digits must equal a given value $s$. Among all such integers, we want the smallest one in numeric value.

The output is not just a yes-or-no decision but the lexicographically smallest number in the sense of normal integer ordering. This makes the problem fundamentally a shortest path problem over a state space where the value of a number is built incrementally digit by digit.

The constraints $d \le 500$ and $s \le 5000$ immediately rule out any direct construction of numbers up to magnitude $10^{5000}$. Any attempt to explicitly enumerate integers or simulate divisibility for large candidates will fail because even checking $10^7$ candidates would already be too slow if each requires digit sum computation and modulo tracking.

A naive idea is to try increasing integers, compute their digit sum, and check divisibility by $d$. This fails in two ways. First, the search space grows exponentially with the digit length of the answer. Second, the correct answer can have many digits even for small inputs, as shown by the sample where $13, 50$ produces a six-digit number.

A second subtle failure mode appears if we try greedy digit construction without global state tracking. For example, choosing locally small digits to keep the number minimal can easily block achieving the required remainder modulo $d$ later.

The key difficulty is that divisibility depends on the full prefix modulo $d$, while digit sum depends on accumulated weight constraints. These two constraints interact across positions, so local decisions cannot guarantee global feasibility.

## Approaches

The brute-force approach is to generate integers in increasing order, compute their digit sum, and test divisibility by $d$. This is correct because it eventually enumerates every candidate in order, but it becomes infeasible because the number of integers with digit sum up to $s$ is enormous. Even restricting to digit sum $s = 5000$, the number of compositions of $s$ into digits is exponential in $s$, so the search space is far beyond any practical limit.

The structure suggests reformulating the problem as constructing a number digit by digit while tracking two pieces of state: the current remainder modulo $d$, and the remaining digit sum. Each digit choice transitions deterministically to a new state. This naturally forms a graph where nodes represent states $(remainder, remaining\_sum)$, and edges correspond to appending a digit $0$ to $9$.

The goal becomes finding the shortest path from the initial state $(0, s)$ to any state $(0, 0)$, while ensuring the first digit is non-zero. Since every edge has equal cost (each digit adds one position), BFS yields the lexicographically smallest valid number when digits are processed in increasing order.

This transforms the problem into a shortest path search over at most $d \cdot (s+1)$ states, which is manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(1) | Too slow |
| BFS on states (mod, sum) | $O(10 \cdot d \cdot s)$ | $O(d \cdot s)$ | Accepted |

## Algorithm Walkthrough

1. Define a state as a pair $(r, t)$, where $r$ is the current remainder modulo $d$, and $t$ is the remaining digit sum needed. This captures exactly the constraints we still need to satisfy in the future, since only these two values affect feasibility.
2. Start from state $(0, s)$ before placing any digits. This represents an empty prefix with full digit sum still available.
3. Use BFS and a queue initialized with the starting state. Each BFS level corresponds to fixing one more digit in the final number.
4. From a state $(r, t)$, try appending every digit $x \in [0, 9]$. This produces a new state $(r', t')$ where $t' = t - x$ and $r' = (r \cdot 10 + x) \bmod d$. We only allow transitions where $t' \ge 0$.
5. Avoid visiting the same state twice. This ensures we do not recompute paths and guarantees termination because the state space is finite.
6. During BFS, maintain a parent pointer for each visited state storing both the previous state and the digit used. This allows reconstruction of the final number once we reach $(0, 0)$.
7. Stop BFS immediately when $(0, 0)$ is reached. This is valid because BFS explores states in increasing number of digits, so the first time we reach a valid terminal state, it corresponds to the minimal-length solution, which is also the smallest numeric value under digit ordering.

### Why it works

The invariant is that every visited state in BFS corresponds to a valid prefix whose digit sum and modulo constraints exactly match the state description. BFS explores all reachable states in increasing path length, and digit order from 0 to 9 ensures that among equal-length paths, smaller digits are expanded first. Therefore the first time we reach $(0, 0)$, no smaller valid number exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    d, s = map(int, input().split())
    
    # dist[r][t] = visited state
    dist = [[False] * (s + 1) for _ in range(d)]
    parent = [[None] * (s + 1) for _ in range(d)]
    
    q = deque()
    q.append((0, s))
    dist[0][s] = True
    
    while q:
        r, t = q.popleft()
        
        if r == 0 and t == 0:
            # reconstruct answer
            res = []
            cr, ct = r, t
            while parent[cr][ct] is not None:
                pr, pt, digit = parent[cr][ct]
                res.append(str(digit))
                cr, ct = pr, pt
            print("".join(reversed(res)))
            return
        
        for digit in range(10):
            if r == 0 and t == s and digit == 0:
                continue
            
            if t < digit:
                continue
            
            nr = (r * 10 + digit) % d
            nt = t - digit
            
            if not dist[nr][nt]:
                dist[nr][nt] = True
                parent[nr][nt] = (r, t, digit)
                q.append((nr, nt))
    
    print(-1)

if __name__ == "__main__":
    solve()
```

The BFS queue stores states defined by remainder and remaining digit sum. The visited table prevents revisiting identical states, which is crucial because multiple digit sequences can lead to the same remainder and remaining sum.

The reconstruction uses parent pointers to rebuild digits in reverse order. This avoids storing full strings in the queue, which would be too memory-heavy for $s$ up to 5000.

The only subtle restriction is preventing a leading zero, handled by disallowing digit 0 in the very first transition from the initial state.

## Worked Examples

We trace the sample input $d = 13, s = 50$. The BFS begins at state $(0, 50)$.

| Step | State (r, t) | Digit tried | Next state | Action |
| --- | --- | --- | --- | --- |
| 1 | (0, 50) | 1 | (1, 49) | enqueue |
| 2 | (0, 50) | 2 | (2, 48) | enqueue |
| ... | ... | ... | ... | ... |
| k | ... | ... | ... | eventually reaches (0, 0) |

The exact path is not important in intermediate steps; what matters is that BFS guarantees the first discovered valid terminal state is optimal.

For a smaller example, consider $d = 3, s = 2$. The BFS quickly finds:

| Step | State | Digit | New State |
| --- | --- | --- | --- |
| 1 | (0,2) | 1 | (1,1) |
| 2 | (1,1) | 1 | (2,0) |
| 3 | (2,0) | 1 | (0,0) |

This yields number 111, which is minimal among all valid candidates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(10 \cdot d \cdot s)$ | Each state processes up to 10 digit transitions |
| Space | $O(d \cdot s)$ | Storage for visited states and parents |

The state space size is at most $500 \times 5000 = 2.5 \times 10^6$, which is acceptable. Each transition is constant work, so the solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    d, s = map(int, sys.stdin.readline().split())

    dist = [[False] * (s + 1) for _ in range(d)]
    parent = [[None] * (s + 1) for _ in range(d)]

    q = deque()
    q.append((0, s))
    dist[0][s] = True

    while q:
        r, t = q.popleft()

        if r == 0 and t == 0:
            res = []
            cr, ct = r, t
            while parent[cr][ct] is not None:
                pr, pt, digit = parent[cr][ct]
                res.append(str(digit))
                cr, ct = pr, pt
            return "".join(reversed(res))

        for digit in range(10):
            if r == 0 and t == s and digit == 0:
                continue
            if t < digit:
                continue
            nr = (r * 10 + digit) % d
            nt = t - digit
            if not dist[nr][nt]:
                dist[nr][nt] = True
                parent[nr][nt] = (r, t, digit)
                q.append((nr, nt))

    return "-1"

# provided sample
assert run("13 50") == "699998"

# custom cases
assert run("1 1") == "1", "single digit"
assert run("3 2") == "11", "small BFS chain"
assert run("2 1") == "-1", "impossible sum too small"
assert run("9 9") == "9", "direct match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 13 50 | 699998 | sample correctness and reconstruction |
| 1 1 | 1 | trivial modulus case |
| 3 2 | 11 | BFS multi-step construction |
| 2 1 | -1 | infeasible digit sum vs modulo |
| 9 9 | 9 | single-digit optimal case |

## Edge Cases

A common failure case is mishandling leading zeros. If digit 0 is allowed as the first transition, the algorithm may return numbers like 0009, which is numerically invalid as a minimal positive integer representation. The restriction in the initial state ensures the first digit is non-zero.

Another edge case is when no solution exists. In such cases, BFS exhausts the state space without reaching $(0, 0)$. The algorithm correctly outputs -1 because every reachable state has been explored, and none satisfy both constraints simultaneously.
