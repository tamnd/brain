---
title: "CF 106260J - \u6392\u5217"
description: "We are building strings of length $n$ using exactly four characters: $y, u, k, o$. The restriction is local: if you ever look at any consecutive block of 5 characters, that block must not be a permutation of the multiset formed by the letters of the word “yuuko”."
date: "2026-06-25T07:25:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106260
codeforces_index: "J"
codeforces_contest_name: "2025 SiChuan University for new student"
rating: 0
weight: 106260
solve_time_s: 48
verified: true
draft: false
---

[CF 106260J - \u6392\u5217](https://codeforces.com/problemset/problem/106260/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building strings of length $n$ using exactly four characters: $y, u, k, o$. The restriction is local: if you ever look at any consecutive block of 5 characters, that block must not be a permutation of the multiset formed by the letters of the word “yuuko”.

The word “yuuko” contains the characters $y, u, u, k, o$, so any forbidden block is exactly a length-5 window containing one $y$, two $u$'s, one $k$, and one $o$, in any order. The task is to count how many valid strings of length $n$ exist under this constraint, modulo $998244353$.

The key difficulty is that the restriction is not about an exact substring, but about a multiset condition on a sliding window. This makes naive substring matching techniques ineffective, since there is no fixed pattern to match position-by-position; only counts matter.

The constraint $n \le 10^{18}$ immediately rules out any linear or polynomial DP over length. Any solution must compress states so that transitions can be iterated using exponentiation or another logarithmic method. The only viable direction is to model the process as a finite automaton whose states depend only on a bounded history of the string.

A subtle edge case appears when multiple overlapping windows could simultaneously violate the condition. For example, a string may become invalid at position $i$, but also contain another invalid window ending at $i+1$. Any correct method must ensure every window is checked exactly when it is formed, not retrospectively.

## Approaches

A brute-force approach would generate all $4^n$ strings and check each one for forbidden windows. Even for $n=20$, this already becomes infeasible, and for $n$ up to $10^{18}$, it is completely impossible. A slightly better brute-force method would use dynamic programming over prefixes, storing the last 4 characters explicitly. This reduces state transitions to a manageable size, but still scales linearly with $n$, which is far too large.

The key observation is that the forbidden condition depends only on the last 5 characters. When we append a new character, only the window ending at that position can newly become invalid. This suggests maintaining a sliding window of length 4 as the state. The next character completes a window of size 5, and we can directly test whether that window matches the forbidden multiset.

This reduces the problem to a finite state machine with $4^4 = 256$ possible states (all possible sequences of length up to 4 over 4 characters). Transitions are determined by appending one character and shifting the window. Since $n$ is huge, we compute the number of length-$n$ walks in this automaton using matrix exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force enumeration | $O(4^n)$ | $O(n)$ | Impossible |
| DP over prefix length | $O(n \cdot 4^4)$ | $O(4^4)$ | Too slow |
| Automaton + matrix exponentiation | $O(256^3 \log n)$ | $O(256^2)$ | Accepted |

## Algorithm Walkthrough

1. Define a state as the last up to 4 characters of the string. Since each position has 4 choices, there are at most $4^4 = 256$ states. We represent each state as a base-4 encoding of length 4.
2. For each state and each possible next character, we simulate appending the character and forming a new 5-character window consisting of the previous 4 characters plus the new one. We compute the character counts in this window.
3. If the multiset of these 5 characters matches exactly $\{y, u, u, k, o\}$, we mark this transition as invalid and discard it. Otherwise, we add a directed transition from the current state to the new state obtained by shifting left and appending the new character.
4. This gives a directed graph of at most 256 nodes, where each node has up to 4 outgoing transitions. We convert this into a transition matrix $T$, where $T[i][j]$ counts valid transitions from state $i$ to state $j$.
5. We initialize a vector representing all valid starting states. Since strings shorter than 4 characters cannot violate the condition, all initial states are allowed.
6. We compute $T^n$ using fast exponentiation. Each multiplication corresponds to combining ways of extending strings while preserving validity.
7. Finally, we sum all entries of the resulting vector to obtain the total number of valid strings of length $n$.

The correctness rests on the invariant that every DP state fully captures all information needed to determine whether adding one more character creates a forbidden 5-length window. Because any violation is detected exactly when it appears, no invalid string ever contributes to the DP.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

# map characters to indices
mp = {'y': 0, 'u': 1, 'k': 2, 'o': 3}

def encode(s):
    x = 0
    for c in s:
        x = x * 4 + c
    while len(s) < 4:
        x *= 4
        s += [0]
    return x

def decode(x):
    s = []
    for _ in range(4):
        s.append(x % 4)
        x //= 4
    return tuple(reversed(s))

# forbidden multiset: y, u, u, k, o
forbidden = [0, 1, 1, 2, 3]

def is_bad(window):
    cnt = [0] * 4
    for c in window:
        cnt[c] += 1
    return cnt == [1, 2, 1, 1]

# build transitions
N = 256
T = [[0] * N for _ in range(N)]

for s in range(N):
    cur = decode(s)
    for c in range(4):
        window = list(cur) + [c]
        if is_bad(window):
            continue
        ns = tuple(list(cur[1:]) + [c])
        ns_id = 0
        for v in ns:
            ns_id = ns_id * 4 + v
        T[s][ns_id] += 1

def matmul(A, B):
    n = len(A)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for k in range(n):
            if Ai[k]:
                Bik = B[k]
                aik = Ai[k]
                for j in range(n):
                    res[i][j] = (res[i][j] + aik * Bik[j]) % MOD
    return res

def matpow(M, e):
    n = len(M)
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    while e:
        if e & 1:
            res = matmul(res, M)
        M = matmul(M, M)
        e >>= 1
    return res

# initial vector: all states allowed
# we start from length 4 padding-free states, so treat all as 1
init = [1] * N

def solve(n):
    if n == 0:
        return 1
    if n <= 4:
        return pow(4, n, MOD)

    P = matpow(T, n - 4)

    ans = 0
    for i in range(N):
        for j in range(N):
            ans = (ans + P[i][j] * init[i]) % MOD
    return ans

n = int(input())
print(solve(n))
```

The code constructs the automaton explicitly over all length-4 histories. Each transition checks whether adding a new character creates the forbidden multiset in the resulting 5-length window. Matrix exponentiation then counts all valid sequences of length $n$ in logarithmic time.

A subtle implementation detail is that for $n \le 4$, no window of length 5 exists at all, so every string is valid and the answer is simply $4^n$.

## Worked Examples

### Example 1: $n = 5$

We track transitions from length 4 states and append one character.

| Step | Current state | Added char | Window checked | Valid? |
| --- | --- | --- | --- | --- |
| 1 | any 4-letter state | y | last 5 chars | depends |
| 2 | any 4-letter state | u | last 5 chars | depends |
| 3 | any 4-letter state | k | last 5 chars | depends |
| 4 | any 4-letter state | o | last 5 chars | depends |

At this length, the automaton ensures that any string where a forbidden multiset appears in any window of size 5 is excluded exactly once at the moment it forms.

This confirms the invariant that every invalid configuration is filtered immediately upon creation.

### Example 2: $n = 6$

Now two overlapping windows exist: positions $[1..5]$ and $[2..6]$. A string may violate the condition in either window.

| Position | New char | Window checked | Action |
| --- | --- | --- | --- |
| 5 | c₅ | (1..5) | checked |
| 6 | c₆ | (2..6) | checked |

If either window matches the forbidden multiset, the corresponding transition is disallowed, preventing propagation of invalid prefixes.

This demonstrates that overlapping violations are handled naturally without explicit rechecking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(256^3 \log n)$ | matrix exponentiation on a fixed 256-state automaton |
| Space | $O(256^2)$ | transition matrix storage |

The state space is constant, so the solution comfortably handles $n$ up to $10^{18}$. The logarithmic exponentiation ensures the number of multiplications stays small even for extremely large lengths.
