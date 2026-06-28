---
title: "CF 104761C - \u0414\u0435\u043b\u0438\u043c\u043e\u0441\u0442\u044c \u043d\u0430 2023"
description: "We are given two distinct digits, call them $A$ and $B$, each between 0 and 9. From only these two digits, we are allowed to construct any positive integer by concatenating them in any order and any length, as long as we do not use any other digit."
date: "2026-06-29T02:23:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104761
codeforces_index: "C"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Regional Contest"
rating: 0
weight: 104761
solve_time_s: 66
verified: false
draft: false
---

[CF 104761C - \u0414\u0435\u043b\u0438\u043c\u043e\u0441\u0442\u044c \u043d\u0430 2023](https://codeforces.com/problemset/problem/104761/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two distinct digits, call them $A$ and $B$, each between 0 and 9. From only these two digits, we are allowed to construct any positive integer by concatenating them in any order and any length, as long as we do not use any other digit. The task is to output any such number that is divisible by 2023, and it must also satisfy a size constraint of being at most 100 digits and must not start with zero.

The core difficulty is not building numbers from digits, but finding one that hits a specific divisibility condition under a very large search space. Even if we fix a length, there are $2^n$ possible strings, so brute force over all strings is impossible beyond very small lengths.

The important structural constraint is that the target modulus is fixed and small: 2023. This immediately suggests that we should think in terms of remainders modulo 2023, since any number longer than 2023+1 digits must eventually repeat a remainder pattern.

A naive edge case that can easily mislead implementation is when one of the digits is 0. For example, if $A = 0$ and $B = 7$, a careless construction might try to start with 0, producing invalid leading zeros like 0077..., which is disallowed even though numerically valid. Another subtle case is when one digit is 0 and the other is small; greedy constructions like repeating the nonzero digit may fail to ever hit a multiple of 2023 even though a valid mixed pattern exists.

## Approaches

A brute-force idea is to generate all strings over the alphabet $\{A, B\}$ in increasing length and test each one for divisibility by 2023. For each generated string, we compute its value modulo 2023 and check whether it is zero. This is correct because it exhausts all candidates.

However, the number of candidates grows exponentially with length. For length 50, we already have $2^{50}$ possibilities, which is far beyond any feasible computation. Even computing modulo incrementally does not help if we still enumerate all strings.

The key observation is that we do not care about the actual number, only its remainder modulo 2023. Every time we append a digit, the new remainder depends only on the previous remainder and the appended digit. This transforms the problem into a graph problem over states $0 \ldots 2022$, where each state represents a remainder, and transitions correspond to appending either digit $A$ or digit $B$.

This gives a directed graph with at most 2023 nodes, each having two outgoing edges. We want to find any path starting from a valid initial digit (nonzero leading digit) that reaches remainder 0. Since the graph is finite, a BFS guarantees we will either find a solution or exhaust all states. Because a solution is guaranteed to exist in the intended construction space, BFS will find one efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| BFS on remainders | $O(2023)$ | $O(2023)$ | Accepted |

## Algorithm Walkthrough

We model each state as a pair consisting of a remainder modulo 2023 and the string constructed so far. Instead of storing full strings for every state, we store parent pointers to reconstruct the answer at the end.

1. We initialize a BFS queue with all valid starting digits. If a digit is zero, it cannot be used as the first character, so we only start from nonzero digits. Each starting digit contributes an initial remainder equal to that digit modulo 2023. This ensures we never produce invalid leading zeros.
2. For each state in the queue, we consider appending digit $A$ and digit $B$. If the current remainder is $r$, then the new remainder after appending digit $d$ is $(10r + d) \bmod 2023$. This recurrence captures exactly how decimal numbers grow.
3. If we reach remainder 0 at any point, we stop immediately. The path from the start state to this state defines a valid number divisible by 2023.
4. To reconstruct the number, we follow stored parent pointers backward from the zero state until we reach the start. We then reverse the sequence of digits.
5. We output the reconstructed string.

The key design choice is storing only predecessors instead of full strings, which keeps memory bounded and allows efficient reconstruction.

### Why it works

Each BFS state represents exactly one reachable remainder with a specific digit sequence. Every extension step preserves correctness of the remainder computation because decimal concatenation is faithfully modeled by $10r + d$. BFS explores states in increasing number of digits, so the first time we reach remainder 0 corresponds to a valid construction. Since there are only 2023 possible remainders, if a solution exists within the allowed digit alphabet, BFS will encounter it without needing to explore exponential-length strings explicitly.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

MOD = 2023

def solve():
    A, B = map(int, input().split())
    digits = [A, B]

    # store visited remainders
    prev = [-1] * MOD
    prev_digit = [-1] * MOD
    visited = [False] * MOD

    q = deque()

    # initialize with valid starting digits (no leading zero)
    for d in digits:
        if d == 0:
            continue
        r = d % MOD
        if not visited[r]:
            visited[r] = True
            prev[r] = -2  # start marker
            prev_digit[r] = d
            q.append(r)

    # BFS over remainder states
    while q:
        r = q.popleft()

        if r == 0:
            break

        for d in digits:
            nr = (r * 10 + d) % MOD
            if not visited[nr]:
                visited[nr] = True
                prev[nr] = r
                prev_digit[nr] = d
                q.append(nr)

    if not visited[0]:
        return ""

    # reconstruct answer
    res = []
    cur = 0
    while prev[cur] != -2:
        res.append(str(prev_digit[cur]))
        cur = prev[cur]

    res.append(str(prev_digit[cur]))
    return "".join(reversed(res))

if __name__ == "__main__":
    print(solve())
```

The BFS is implemented purely on remainders, which keeps the state space small. The arrays `prev` and `prev_digit` allow reconstruction without storing full strings. The marker `-2` distinguishes root states from intermediate ones.

A subtle implementation point is initi
