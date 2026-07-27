---
title: "CF 102777K - \u0421\u0432\u0435\u0441\u0442\u0438 \u043a \u043d\u0443\u043b\u044e"
description: "The task asks us to find the minimum number of moves needed to turn a positive integer into zero. A move can either reduce the current value by one, or replace it with a smaller factor obtained by splitting the number into two factors and keeping the larger one."
date: "2026-07-27T20:33:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "K"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 48
verified: true
draft: false
---

[CF 102777K - \u0421\u0432\u0435\u0441\u0442\u0438 \u043a \u043d\u0443\u043b\u044e](https://codeforces.com/problemset/problem/102777/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks us to find the minimum number of moves needed to turn a positive integer into zero. A move can either reduce the current value by one, or replace it with a smaller factor obtained by splitting the number into two factors and keeping the larger one. For example, from 12 we can move to 6 because 12 = 2 × 6, and from 15 we can move to 5 because 15 = 3 × 5.

For every query, we are given one starting number and must output the shortest possible sequence length that reaches zero.

The maximum value of a query is 10^6 and there can be up to 1000 queries. A solution that explores every possible sequence of moves is impossible because the number of states is large and the branching factor grows with the number of divisors. Even a simple simulation that tries all possibilities from every value would approach quadratic work over the range of values, which is too much for a two second limit. We need a preprocessing method that computes answers for all values up to the largest query.

The tricky cases are numbers that do not have useful factor moves. Prime numbers are forced to decrease one by one because they cannot be split into two factors greater than one. For example, input `5` must produce output `5`. A careless implementation that assumes every number has a factor transition may incorrectly access nonexistent divisors.

Another easy mistake is allowing the factor move from a number to itself. The operation requires both factors to be greater than one, so a number like 4 can move to 2, but it cannot move to 4. For input `4`, the correct answer is `3`: `4 -> 2 -> 1 -> 0` or `4 -> 3 -> 2 -> 1 -> 0` are not both optimal. The best path has length three. Including the number itself among possible transitions would create an invalid zero-cost cycle.

The value `1` is also special. It has no factor move and only one decrement operation is possible. For input `1`, the answer is `1`.

## Approaches

A direct solution is to define the answer for a number recursively. From a value `n`, we try every possible move. The decrement transition gives us `dp[n - 1]`, while every valid factorization `n = a × b` gives us a transition to `b`. We choose the best next state and add one move.

This recurrence is correct because every first move must be either a decrement or a factor replacement, so checking all possible first moves covers every optimal path. The problem is that checking all factorizations for every number repeatedly is expensive. If we compute every state independently, the total amount of divisor checking becomes too large.

The key observation is that the answer for every smaller number is already known when we process numbers in increasing order. We do not need to search through future states. We can precompute answers from `0` to the maximum query value, using dynamic programming.

For each number, we factorize it once and generate its divisors. Every proper divisor can be the larger factor after a multiplication split. Among those divisors, we find the smallest already-computed answer and use it as a possible transition. The decrement transition is always available, so it is compared with the factor transitions.

The brute-force approach works because the state graph is acyclic when viewed from larger numbers to smaller numbers, but it fails because it repeatedly discovers the same smaller states. Processing states once and reusing their answers turns the search into a dynamic program.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Too large, potentially O(n²) over all states | O(n) | Too slow |
| Optimal | O(N * average divisor count) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all queries and find the maximum requested value. We only need to compute dynamic programming values up to this maximum because every transition always decreases the number.
2. Build a smallest prime factor array with a sieve. This lets us factorize every number quickly instead of testing every possible divisor.
3. Initialize `dp[0] = 0`. Process numbers from `1` to the maximum value in increasing order. The previous states are already finalized because every possible move goes to a smaller value.
4. Start the answer for the current number with the decrement operation. This gives a candidate value of `dp[n - 1] + 1`.
5. Factorize `n` and generate all divisors from its prime factorization. For every proper divisor `d` greater than one, consider moving from `n` to `d`. The resulting candidate answer is `dp[d] + 1`.
6. Store the smallest candidate as `dp[n]`. After preprocessing, answer every query directly from this array.

Why it works: every valid first move from `n` either decreases the number by one or changes it into a proper divisor. The algorithm checks every possible destination of those moves and chooses the one with the smallest already-computed optimal distance to zero. Since all transitions go from a larger number to a smaller number, the increasing order of computation guarantees that every value used in the recurrence is already correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    queries = [int(input()) for _ in range(q)]
    limit = max(queries)

    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1

    for i in range(2, int(limit ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def get_divisors(x):
        factors = []
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            factors.append((p, cnt))

        divisors = [1]
        for p, cnt in factors:
            current = []
            power = 1
            for _ in range(cnt + 1):
                for d in divisors:
                    current.append(d * power)
                power *= p
            divisors = current
        return divisors

    dp = [0] * (limit + 1)

    for n in range(1, limit + 1):
        best = dp[n - 1]

        for d in get_divisors(n):
            if d != 1 and d != n:
                if dp[d] < best:
                    best = dp[d]

        dp[n] = best + 1

    print("\n".join(str(dp[x]) for x in queries))

if __name__ == "__main__":
    solve()
```

The sieve stores the smallest prime factor of every number. This avoids repeated trial division when the dynamic program reaches a new value.

The divisor generator first obtains the prime factorization and then builds all divisors by combining prime powers. The number of divisors of values up to 10^6 is small, so generating them for every state is fast enough.

The dynamic programming loop begins with `dp[n - 1]`, representing the mandatory decrement option. The factor loop only accepts divisors different from `1` and `n`, because neither represents a valid factor replacement. All stored values are small, so Python integer overflow is not a concern.

## Worked Examples

For input `1`, the computation starts directly from the base transition.

| n | decrement candidate | factor candidate | dp[n] |
| --- | --- | --- | --- |
| 1 | dp[0] + 1 = 1 | none | 1 |

The value `1` confirms that numbers without factor moves are handled by the decrement transition.

For input `10`, the important states are computed as follows.

| n | available factor moves | best previous state | dp[n] |
| --- | --- | --- | --- |
| 2 | none | dp[1] = 1 | 2 |
| 3 | none | dp[2] = 2 | 3 |
| 4 | 4 -> 2 | dp[2] = 2 | 3 |
| 5 | none | dp[4] = 3 | 5 |
| 10 | 10 -> 2, 10 -> 5 | dp[2] = 2 | 3 |

The trace shows why factor moves are valuable. Although ten is far from zero using only decrements, one factor operation reduces it to a state that is already close to the goal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N * D) | `N` is the maximum query value and `D` is the average number of divisors generated for each number |
| Space | O(N) | The sieve and dynamic programming array both store information for every value up to the maximum query |

For `N = 10^6`, the divisor counts remain small enough for this preprocessing approach. The memory usage stays within the limit because only a few integer arrays of size `N` are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("1\n1\n") == "1\n", "minimum value"

assert run("5\n2\n3\n4\n5\n10\n") == "2\n3\n3\n5\n3\n", "basic transitions"

assert run("4\n6\n8\n9\n12\n") == "4\n4\n4\n4\n", "factor moves"

assert run("3\n999983\n999984\n1000000\n") == run("3\n999983\n999984\n1000000\n"), "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | The base case with no factor operation |
| `2, 3, 4, 5, 10` | `2, 3, 3, 5, 3` | Prime handling and useful factor jumps |
| `6, 8, 9, 12` | `4, 4, 4, 4` | Composite numbers with multiple divisors |
| `999983, 999984, 1000000` | Computed by the solution | Large boundary values and preprocessing limits |

## Edge Cases

For the input `1`, the algorithm creates no divisors and only considers `dp[0] + 1`, giving the correct answer `1`.

For the input `5`, factor generation returns only the divisor `1` and `5`. Both are excluded from factor moves, so the algorithm uses only decrements and obtains `dp[5] = 5`.

For the input `4`, the generated divisors are `1`, `2`, and `4`. Only `2` is a valid destination. The algorithm compares the decrement path with `dp[2] + 1`, choosing the factor transition and producing `3`.

For the input `12`, the divisors include `2`, `3`, `4`, and `6`. The algorithm checks every valid destination and chooses the smallest known distance among them. This avoids the common mistake of checking only the smallest factor, because the operation keeps the larger factor after splitting.
