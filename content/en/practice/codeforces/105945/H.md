---
title: "CF 105945H - Loose Subsequences"
description: "We are given a string and asked to count how many different non-empty subsequences we can form under a spacing restriction on positions."
date: "2026-06-22T15:57:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105945
codeforces_index: "H"
codeforces_contest_name: "The 2025 Jiangsu Collegiate Programming Contest, The 2025 Guangdong Provincial Collegiate Programming Contest"
rating: 0
weight: 105945
solve_time_s: 69
verified: true
draft: false
---

[CF 105945H - Loose Subsequences](https://codeforces.com/problemset/problem/105945/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string and asked to count how many different non-empty subsequences we can form under a spacing restriction on positions. A subsequence is obtained by picking characters from the string while keeping their original order, but we are not allowed to pick characters that are too close to each other in the original string. More precisely, if we pick two consecutive chosen positions, their indices must differ by more than $k$. This means every selected character must be at least $k+1$ positions after the previous selected character.

The output is the number of distinct resulting strings among all such valid subsequences, taken modulo 998244353.

The input size is large in total, with the sum of string lengths up to $10^6$. This immediately rules out any solution that enumerates subsequences explicitly, since even without constraints there are exponentially many subsequences. Any acceptable solution must be linear or near-linear in total length.

A less obvious observation is that the actual letters in the string do not affect the count of distinct subsequences under this constraint. The restriction depends only on which positions are chosen, not on character values. Since each chosen set of positions uniquely determines a subsequence string, counting distinct subsequences becomes equivalent to counting valid index sets.

A common failure case appears if one tries to apply standard distinct subsequence DP that depends on character last occurrences. For example, in a string like `aaaaa`, naive thinking might try to merge contributions by character, but the spacing constraint breaks that structure. The constraint is positional, so character-based DP collapses incorrectly.

Another edge case arises when $k = 0$. Then any two consecutive chosen positions must differ by at least 1, which imposes no restriction beyond the subsequence rule itself. The correct answer should reduce to counting all non-empty subsequences, which is $2^n - 1$. Any recurrence that accidentally uses an incorrect boundary such as including the current position in prefix sums will overcount or create self-dependence.

## Approaches

The brute-force approach is straightforward: generate all subsequences and check whether each satisfies the spacing rule. For each subsequence, we verify adjacent chosen indices in linear time. Since there are $2^n$ subsequences, this becomes completely infeasible even for $n = 30$, let alone $10^6$. The failure comes from enumerating subsets of positions, which grows exponentially.

The key insight is to stop thinking in terms of characters and instead think in terms of valid choices of last element. Every valid subsequence can be uniquely described by its last chosen position. If we fix a position $i$ as the last element, everything before it must form a valid subsequence ending at some position $j \le i-k-1$. This creates a clean recurrence over prefix ranges rather than combinatorial structure.

This transforms the problem into a simple dynamic programming over positions with prefix sums. We maintain the number of valid subsequences ending at or before each index, and use range sums to ensure the spacing constraint is respected.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Prefix DP | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We index the string from 1 to $n$. Let $dp[i]$ denote the number of valid subsequences whose last chosen position is exactly $i$. Let $pref[i]$ be the sum of $dp[1..i]$.

1. For each position $i$, consider starting a new subsequence consisting only of $S[i]$. This contributes 1 valid subsequence ending at $i$.
2. Any longer subsequence ending at $i$ must come from some previous ending position $j$, where the spacing rule enforces $i - j > k$, equivalently $j \le i - k - 1$. This ensures the last gap is valid, and earlier gaps are already enforced by earlier states.
3. Therefore, we set $dp[i] = 1 + pref[i-k-1]$, treating $pref[x] = 0$ when $x \le 0$.
4. We update the prefix sum: $pref[i] = pref[i-1] + dp[i]$.
5. The final answer is $pref[n]$, which aggregates all valid subsequences ending anywhere.

### Why it works

Every valid subsequence has a unique last chosen position $i$. Once $i$ is fixed, the remaining prefix is any valid subsequence whose last position respects the spacing constraint with $i$. The recurrence partitions all valid subsequences by this last position without overlap. Since each subsequence is counted exactly once at its terminal index, no duplication occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()

        dp = [0] * (n + 1)
        pref = [0] * (n + 1)

        for i in range(1, n + 1):
            j = i - k - 1
            if j >= 1:
                dp[i] = (1 + pref[j]) % MOD
            else:
                dp[i] = 1

            pref[i] = (pref[i - 1] + dp[i]) % MOD

        print(pref[n] % MOD)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the recurrence. The only subtlety is handling indices where $i-k-1$ becomes non-positive, in which case there is no valid previous subsequence to extend. The prefix array ensures range sums are computed in constant time.

A second subtle point is that the string itself is never used. Although it is provided in the input, the number of valid subsequences depends only on the structure of allowed index selections, not on character identities. This is why the solution ignores `s` entirely.

## Worked Examples

Consider an example with $n = 5, k = 1$. We compute valid subsequences where chosen positions must differ by at least 2.

| i | dp[i] computation | dp[i] | pref[i] |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 1 + pref[1] | 2 | 4 |
| 4 | 1 + pref[2] | 3 | 7 |
| 5 | 1 + pref[3] | 5 | 12 |

The final answer is 12. This reflects that later positions have more freedom to combine with earlier valid subsequences, but only those far enough away.

Now consider $n = 4, k = 2$, where positions must differ by at least 3.

| i | dp[i] computation | dp[i] | pref[i] |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 1 | 1 | 3 |
| 4 | 1 + pref[1] | 2 | 5 |

Only position 4 can extend earlier subsequences, and only those ending at position 1 are close enough to matter. This shows how the constraint effectively limits interaction range.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | Each position is processed once with O(1) prefix lookup |
| Space | $O(n)$ | Arrays for dp and prefix sums |

Since the sum of $n$ over all test cases is $10^6$, the solution runs comfortably within limits using a single linear pass per test.

## Test Cases

```python
import sys, io

MOD = 998244353

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()

        dp = [0] * (n + 1)
        pref = [0] * (n + 1)

        for i in range(1, n + 1):
            j = i - k - 1
            if j >= 1:
                dp[i] = (1 + pref[j]) % MOD
            else:
                dp[i] = 1
            pref[i] = (pref[i - 1] + dp[i]) % MOD

        out.append(str(pref[n] % MOD))
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# minimum case
assert run("1\n1 0\na\n") == "1"

# all equal letters, k=0 => 2^n - 1 = 7 for n=3
assert run("1\n3 0\naaa\n") == "7"

# strict spacing
assert run("1\n4 2\nabcd\n") == "5"

# larger simple case
assert run("1\n5 1\nabcde\n") == "12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1,k=0 | 1 | minimal subsequence count |
| aaa,k=0 | 7 | full subsequence growth |
| abcd,k=2 | 5 | strong spacing constraint |
| abcde,k=1 | 12 | intermediate overlap behavior |

## Edge Cases

When $k = 0$, the recurrence reduces to classical subsequence counting. For example with $n = 3$, we have dp values $1, 2, 4$, giving total 7. The formula still works because $i-k-1 = i-1$, so each position correctly extends all previous subsequences.

When $k \ge n$, no two positions can be chosen together. Every dp entry becomes 1, since no extensions are possible. For example with $n = 4, k = 5$, the answer is 4, corresponding to choosing each single position individually.

For very small $n$, such as $n = 1$, the algorithm correctly returns 1 regardless of $k$, since the only subsequence is the single character.
