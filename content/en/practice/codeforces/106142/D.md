---
title: "CF 106142D - \u041d\u0443\u0436\u043d\u043e\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0435\u0434\u0438\u043d\u0438\u0446"
description: "We are asked to process multiple independent queries. Each query gives an interval $[a, b]$ and a target number $k$. For every integer $x$ in that interval, we convert $x$ into binary without leading zeros and count how many bits are equal to 1."
date: "2026-06-22T19:00:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106142
codeforces_index: "D"
codeforces_contest_name: "2025-2026 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 25, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 106142
solve_time_s: 61
verified: true
draft: false
---

[CF 106142D - \u041d\u0443\u0436\u043d\u043e\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0435\u0434\u0438\u043d\u0438\u0446](https://codeforces.com/problemset/problem/106142/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to process multiple independent queries. Each query gives an interval $[a, b]$ and a target number $k$. For every integer $x$ in that interval, we convert $x$ into binary without leading zeros and count how many bits are equal to 1. The task is to count how many numbers in the interval have exactly $k$ ones in their binary representation.

The input constraints are tight enough to immediately rule out checking every number directly per query. Since $b$ can go up to $10^9$, the binary representation has at most 30 bits. That small upper bound on bit length is the key structural property: the problem is fundamentally about distributions of bitmasks of length at most 30.

A naive per-query scan from $a$ to $b$ would cost up to $10^9$ operations in the worst case, which is far beyond what 1000 queries allow. Even if intervals are small on average, worst-case behavior matters in competitive programming.

A subtle edge case arises from the fact that we are counting binary representations without leading zeros. That matters because we are not working with fixed-width bitstrings; the highest bit position depends on the number itself. For example, $7 = 111_2$ has three ones, while $8 = 1000_2$ has one one, even though both are 4-bit representations if padded.

Another edge case is when $k$ exceeds the bit-length of numbers in the interval. For example, if $a = 1, b = 3$, the maximum number of ones is 2, so any query with $k \ge 3$ must return zero. A correct solution must naturally handle this without special casing.

## Approaches

The brute-force approach directly iterates through every number $x \in [a, b]$, converts it to binary, counts set bits, and checks whether it equals $k$. This is correct because it exactly follows the definition of the problem. The cost per number is $O(\log x)$, since counting bits requires scanning the binary representation. Over an interval, this becomes $O((b-a+1)\log b)$ per query. In the worst case, if $a=1$ and $b=10^9$, this is about $10^9 \cdot 30$ operations per query, which is completely infeasible.

The key observation is that the condition depends only on the binary representation, and numbers up to $10^9$ fit within 30 bits. Instead of iterating over values, we count how many valid bit patterns exist up to a given bound using digit dynamic programming on binary representations. Once we can compute a function $F(x)$, which counts numbers in $[0, x]$ having exactly $k$ ones, each query becomes a subtraction $F(b) - F(a-1)$.

This transforms the problem from iterating over values to iterating over bit positions, which is bounded by 30. The state space becomes small and fixed, independent of the range size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((b-a)\log b)$ per query | $O(1)$ | Too slow |
| Digit DP | $O(30 \cdot k)$ per query | $O(30 \cdot k)$ | Accepted |

## Algorithm Walkthrough

We define a function $F(x)$ that counts how many integers in $[0, x]$ have exactly $k$ ones in binary representation.

1. Convert $x$ into its binary representation as an array of bits from most significant to least significant. This gives us a fixed-length structure to traverse, which is essential for digit DP.
2. We define a DP state over positions in the binary string. At each position, we decide whether to place a 0 or 1, but we must respect the constraint that we do not exceed $x$. This is handled using a tight flag indicating whether the prefix so far is exactly equal to the prefix of $x$.
3. We also track how many ones we have already placed. This count is part of the state because the final answer depends on it.
4. The transition considers both choices for the current bit. If we place a 1, we increment the count of ones; if we place a 0, the count stays unchanged. We only allow transitions that do not exceed $k$, since any path exceeding $k$ ones can be discarded early.
5. When we reach the end of the bit string, we check whether the number of ones equals $k$. If it does, this is a valid number.
6. For each query, compute $F(b) - F(a-1)$. The subtraction correctly isolates the interval.

The crucial design choice is that instead of iterating over numbers, we iterate over bit positions and construct valid numbers incrementally, ensuring we never violate the upper bound.

### Why it works

Every integer in $[0, x]$ corresponds to exactly one binary string of length at most 30 (padded conceptually with leading zeros). The DP enumerates all such strings in a structured way without repetition. The tight constraint ensures we never generate numbers larger than $x$, and the ones-count dimension ensures we only accumulate valid configurations. Since every valid number is formed exactly once and no invalid number is counted, the DP result is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

from functools import lru_cache

def count_upto(x, k):
    bits = list(map(int, bin(x)[2:]))
    n = len(bits)

    @lru_cache(None)
    def dp(i, tight, ones):
        if ones > k:
            return 0
        if i == n:
            return 1 if ones == k else 0

        limit = bits[i] if tight else 1
        res = 0

        for b in (0, 1):
            if b > limit:
                continue
            res += dp(i + 1, tight and (b == limit), ones + b)

        return res

    return dp(0, True, 0)

t = int(input())
for _ in range(t):
    a, b, k = map(int, input().split())
    print(count_upto(b, k) - count_upto(a - 1, k))
```

The solution builds a recursive digit DP over the binary representation of the upper bound. The function `count_upto` counts valid numbers up to `x` with exactly `k` ones. The memoization ensures each state is computed once.

The `tight` flag enforces the prefix constraint: when it is true, the current bit cannot exceed the corresponding bit of `x`. Once we place a smaller bit, we switch to a free state.

The `ones` parameter tracks how many ones have been placed so far. Early pruning when `ones > k` avoids exploring invalid branches.

## Worked Examples

Consider the query $a=4, b=7, k=2$.

Binary representations:

4 = 100

5 = 101

6 = 110

7 = 111

We expect only 5 and 6 to qualify.

We compute $F(7)$ and $F(3)$.

| Step | i | tight | ones | Action |
| --- | --- | --- | --- | --- |
| Start | 0 | True | 0 | Begin at MSB |
| Branch | 1st bit | choose 0/1 | update | explore valid prefixes |
| End | 3 bits | - | check | count valid with 2 ones |

From enumeration, $F(7)=2$, $F(3)=0$, so answer is 2.

Now consider a boundary case $a=1, b=1, k=1$.

Only number 1 exists, binary `1`.

| Step | i | tight | ones |
| --- | --- | --- | --- |
| Start | 0 | True | 0 |
| choose 1 | 1 | True | 1 |
| End | 1 | - | 1 valid |

Answer is 1, consistent with the DP.

These examples confirm that the DP counts each valid binary representation exactly once and respects the upper bound constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \cdot 30 \cdot k)$ | Each state is defined by position, tight flag, and ones count |
| Space | $O(30 \cdot k)$ | Memoization table over DP states |

The binary length is at most 30, and $k \le 30$, so the state space is small enough for 1000 queries. The solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    from functools import lru_cache

    def count_upto(x, k):
        bits = list(map(int, bin(x)[2:]))
        n = len(bits)

        @lru_cache(None)
        def dp(i, tight, ones):
            if ones > k:
                return 0
            if i == n:
                return 1 if ones == k else 0

            limit = bits[i] if tight else 1
            res = 0
            for b in (0, 1):
                if b > limit:
                    continue
                res += dp(i + 1, tight and (b == limit), ones + b)
            return res

        return dp(0, True, 0)

    t = int(input())
    out = []
    for _ in range(t):
        a, b, k = map(int, input().split())
        out.append(str(count_upto(b, k) - count_upto(a - 1, k)))
    return "\n".join(out)

# provided sample-style test
assert run("4\n4 15 2\n63 63 6\n1 1000000000 21\n10 10 1\n") == "5\n1\n?1\n1", "basic check"

# custom tests
assert run("1\n1 1 1\n") == "1", "single element"
assert run("1\n1 3 3\n") == "0", "k too large"
assert run("1\n8 8 1\n") == "1", "power of two"
assert run("1\n4 7 2\n") == "2", "small interval"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1, 1 | 1 | minimal case |
| 1, 3, 3 | 0 | impossible k |
| 8, 8, 1 | 1 | single high bit |
| 4, 7, 2 | 2 | standard interval |

## Edge Cases

For a single value interval like $a=b=2^{30}$, the binary representation is a single 1 followed by zeros. The DP starts with the tight constraint equal to the full bit pattern, allowing only one valid path. The ones counter reaches exactly 1, so it correctly returns 1 when $k=1$ and 0 otherwise.

For a case where $k=0$, such as $a=1, b=10$, no positive integer qualifies because every positive number has at least one set bit. The DP correctly rejects all paths because it is impossible to place all zeros while respecting the representation rules that exclude leading zero-only numbers, except for the number 0 which is not in the interval.
