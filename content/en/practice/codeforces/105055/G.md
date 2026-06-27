---
title: "CF 105055G - Genie in the Lamp"
description: "We are given a string of length $N$ consisting of three kinds of characters: fixed opening parentheses, fixed closing parentheses, and wildcard positions written as ?. Each wildcard can independently be replaced by either ( or )."
date: "2026-06-28T00:23:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "G"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 31
verified: true
draft: false
---

[CF 105055G - Genie in the Lamp](https://codeforces.com/problemset/problem/105055/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of length $N$ consisting of three kinds of characters: fixed opening parentheses, fixed closing parentheses, and wildcard positions written as `?`. Each wildcard can independently be replaced by either `(` or `)`.

After replacing all wildcards, we obtain a standard parenthesis string. Such a string is valid if it can be interpreted as a correct sequence of matched parentheses, meaning that prefixes never have more closing than opening brackets and the total number of opening and closing brackets is equal.

The task is to count how many assignments of the question marks produce a valid balanced sequence, and output this count modulo $10^9 + 7$.

The constraint $N \le 3000$ immediately rules out brute forcing all $2^{\#?}$ assignments. In the worst case, the string is all question marks, so there are $2^{3000}$ possibilities, which is far beyond feasible enumeration. Even checking one assignment takes $O(N)$, so brute force is completely infeasible.

This pushes us toward a dynamic programming solution that builds valid prefixes incrementally.

A subtle failure case for naive reasoning is assuming that only the total number of `(` and `)` matters. For example, strings like `"())("` have equal counts but are invalid due to prefix imbalance. Another pitfall is greedily matching pairs from left to right without considering future choices; wildcards can repair or break balance later, so local decisions are unsafe.

## Approaches

A brute force approach would iterate over all $2^k$ replacements of question marks, construct the resulting string, and check if it is balanced using a stack or a counter scan. This is correct because it directly tests the definition of validity. However, if $k = N$, this already requires $2^{3000}$ configurations, and each validity check costs $O(N)$, leading to exponential time that cannot run.

The key observation is that validity of a parenthesis prefix depends only on how many unmatched opening parentheses we currently have. As we scan left to right, we only need to track the current balance, defined as:

$$\text{balance} = \#(\text{open}) - \#(\text{close})$$

A sequence is valid if this balance never becomes negative and ends at zero.

This suggests dynamic programming over positions and balance. At each index, we consider transitions depending on whether the character is fixed or a wildcard. From a state $(i, b)$, we move to $i+1$ and update $b$ by +1 or -1 depending on the chosen character.

This reduces the problem to counting paths in a layered graph of size $O(N^2)$, since balance ranges from $0$ to $N$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^k \cdot N)$ | $O(N)$ | Too slow |
| DP over position and balance | $O(N^2)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We define a DP array where `dp[b]` represents the number of ways to process the prefix up to the current position such that the current balance is exactly $b$, and the prefix is valid (never negative balance).

We process characters from left to right.

1. Initialize `dp[0] = 1`. This represents the empty prefix having zero balance in exactly one way.
2. For each character in the string, we build a new DP array `ndp` initially all zeros.
3. If the current character is `(`, every state with balance $b$ transitions to $b+1$. We only allow this if $b+1 \le N$. This reflects that we have no choice: the character must increase balance.
4. If the current character is `)`, every state with balance $b > 0$ transitions to $b-1$. States with $b = 0$ are invalid for this transition because we cannot close an unmatched prefix.
5. If the current character is `?`, we consider both transitions: treat it as `(` and as `)`. The first increases balance, the second decreases balance if possible.
6. After processing each character, we replace `dp` with `ndp`.
7. After processing all characters, the answer is `dp[0]`, since a valid complete sequence must end with zero balance.

The key reason this works is that balance fully characterizes whether a prefix is valid; no other historical information is required.

### Why it works

At any prefix, every valid partial assignment is uniquely described by its position and current balance. Any two partial sequences with the same position and balance have identical future extension possibilities because future validity depends only on not going negative and ending at zero. Thus, the DP partitions all valid constructions into disjoint equivalence classes indexed by balance, and transitions preserve correctness and completeness.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n = int(input().strip())
s = input().strip()

dp = [0] * (n + 2)
dp[0] = 1

for ch in s:
    ndp = [0] * (n + 2)
    if ch == '(':
        for b in range(n):
            if dp[b]:
                ndp[b + 1] = (ndp[b + 1] + dp[b]) % MOD
    elif ch == ')':
        for b in range(1, n + 1):
            if dp[b]:
                ndp[b - 1] = (ndp[b - 1] + dp[b]) % MOD
    else:
        for b in range(n + 1):
            if dp[b]:
                ndp[b + 1] = (ndp[b + 1] + dp[b]) % MOD
                if b > 0:
                    ndp[b - 1] = (ndp[b - 1] + dp[b]) % MOD
    dp = ndp

print(dp[0])
```

The DP array is sized $n+2$ to safely accommodate transitions without boundary checks at every step. Each character update constructs a fresh array to avoid overwriting states that are still needed in the same iteration.

The critical implementation detail is ensuring we never allow negative balance transitions, which is enforced by starting the `)` loop from balance 1 and by checking `b > 0` in wildcard cases.

## Worked Examples

### Example 1

Input:

```
4
()(?
```

We track DP states as balance distributions.

| step | char | dp states (non-zero) |
| --- | --- | --- |
| 0 | init | {0: 1} |
| 1 | `(` | {1: 1} |
| 2 | `)` | {0: 1} |
| 3 |  |  |
