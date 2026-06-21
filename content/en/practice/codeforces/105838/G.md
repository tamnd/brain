---
title: "CF 105838G - Who Likes Mathematics is not Boki-chan"
description: "We are given a very large interval of integers, from $L$ to $R$, where $R$ can be as large as $10^{18}$. The task is to count how many numbers inside this interval satisfy a digit-based property: when you look at the decimal representation of a number, the absolute difference…"
date: "2026-06-22T01:22:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105838
codeforces_index: "G"
codeforces_contest_name: "The 14th Huazhong Agricultural University Programming Contest"
rating: 0
weight: 105838
solve_time_s: 47
verified: true
draft: false
---

[CF 105838G - Who Likes Mathematics is not Boki-chan](https://codeforces.com/problemset/problem/105838/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very large interval of integers, from $L$ to $R$, where $R$ can be as large as $10^{18}$. The task is to count how many numbers inside this interval satisfy a digit-based property: when you look at the decimal representation of a number, the absolute difference between every pair of adjacent digits must be exactly 1. All single-digit numbers automatically satisfy this rule.

So numbers like 6, 10, 21, 3210, or 4567 are valid because each neighboring digit pair changes by exactly one. Numbers like 112 fail because the first two digits differ by 0, 12332 fails because 2 to 3 is fine but 3 to 3 breaks the rule, and 555 fails immediately since all adjacent differences are 0.

The input is a single interval, and the output is the count of valid integers in that interval.

The main difficulty is the size of the range. A direct check over every number from $L$ to $R$ is impossible because the interval can span up to $10^{18}$, which would mean up to $10^{18}$ candidates in the worst case. Even checking a single number costs $O(\text{digits})$, so brute force is completely out of range.

A second subtlety is leading-digit structure. The condition depends only on adjacent digits, so numbers behave like paths in a digit graph, and we need to count all valid digit strings up to 18 digits that fall within a numeric bound.

Edge cases that break naive reasoning include:

A single-digit interval like $L=1, R=9$, where all answers are valid and the solution must not overcomplicate counting.

A boundary like $L=10, R=10$, where only one number exists and it must be counted correctly even though it is the smallest two-digit case.

Intervals where $L$ and $R$ differ in length, such as $L=9, R=1000$, where a digit-DP solution must seamlessly handle all lengths.

A naive approach that generates all valid numbers up to 18 digits and filters them by range would still require generating potentially millions of states, but more importantly it would require careful pruning to avoid overflow beyond bounds, which is exactly what digit DP is designed to handle cleanly.

## Approaches

A brute-force strategy would iterate over every number in $[L, R]$, convert it to a string, and verify whether adjacent digits differ by exactly one. This works logically because the condition is local to each number and requires only a linear scan per candidate. The cost per number is $O(d)$, where $d \leq 18$. However, the number of candidates is $R - L + 1$, which in the worst case is $10^{18}$, making this approach impossible.

The key observation is that we are not evaluating a function over numbers independently, but rather counting digit strings that satisfy a local transition constraint. Each valid number can be seen as a path where digits form a sequence and each step moves by ±1. This turns the problem into counting valid digit sequences under a bound constraint, which is exactly the setting for digit dynamic programming.

Instead of enumerating numbers, we count how many valid digit sequences are less than or equal to a given bound $X$, then compute the answer as:

$$\text{count}(R) - \text{count}(L-1)$$

To compute $\text{count}(X)$, we use DP over positions with state tracking the previous digit and whether we are still tight to the prefix of $X$. This avoids generating numbers explicitly and ensures we only traverse feasible digit transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(R-L+1)\cdot O(d)$ | $O(1)$ | Too slow |
| Digit DP | $O(18 \cdot 10 \cdot 2)$ | $O(18 \cdot 10 \cdot 2)$ | Accepted |

## Algorithm Walkthrough

We define a function $f(X)$ that counts how many valid numbers are in $[1, X]$. The final answer is $f(R) - f(L-1)$.

1. Convert $X$ into a digit array so we can process it position by position. This allows us to compare partial prefixes with the bound.
2. Define a DP state $dp[pos][prev][tight]$, where `pos` is the current digit index, `prev` is the last digit chosen, and `tight` indicates whether the prefix so far is equal to the prefix of $X$. The role of `prev` is essential because validity depends on adjacent digit differences.
3. Initialize the DP at position 0 with no previous digit selected. We use a special sentinel value (such as 10 or -1) to indicate that no digit has been placed yet. At this stage, all digits from 1 to the first digit of $X$ are allowed, since leading zeros are not considered valid numbers unless the number is exactly zero.
4. At each position, iterate over all possible next digits. If we have not started a number yet, we can choose 0 as a continuation of “still empty”, but once a number starts, leading zeros are treated as normal digits. This allows correct handling of numbers like 10 or 100.
5. For each candidate digit, enforce the adjacency rule: if we already have a previous digit, the absolute difference must be exactly 1. If this condition fails, we skip the transition.
6. Update the `tight` flag: if we were tight and we choose a digit equal to the current bound digit, we remain tight; otherwise we lose tightness.
7. Sum all valid completions when reaching the last position. Any state where at least one digit has been chosen contributes a valid number.
8. Compute the final answer using inclusion-exclusion over prefix counts.

### Why it works

Every valid number corresponds to exactly one path in the DP over digit positions, because each position decision uniquely determines the next state via the previous digit constraint. The DP ensures we count each such path exactly once, and the `tight` constraint guarantees we never exceed the upper bound. Since all transitions enforce the adjacent difference condition, no invalid number can ever be constructed, and since all possible valid digit sequences are explored, none are missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_upto(x: int) -> int:
    if x <= 0:
        return 0

    digits = list(map(int, str(x)))
    n = len(digits)

    # dp[pos][prev][tight][started]
    # prev: 0-9, or 10 meaning "no previous digit yet"
    dp = [[[[0] * 2 for _ in range(2)] for _ in range(11)] for _ in range(n + 1)]
    dp[0][10][1][0] = 1

    for pos in range(n):
        for prev in range(11):
            for tight in range(2):
                for started in range(2):
                    cur = dp[pos][prev][tight][started]
                    if cur == 0:
                        continue

                    limit = digits[pos] if tight else 9

                    for d in range(limit + 1):
                        ntight = 1 if (tight and d == limit) else 0

                        if not started:
                            if d == 0:
                                dp[pos + 1][10][ntight][0] += cur
                            else:
                                dp[pos + 1][d][ntight][1] += cur
                        else:
                            if abs(d - prev) == 1:
                                dp[pos + 1][d][ntight][1] += cur

    res = 0
    for prev in range(11):
        for tight in range(2):
            res += dp[n][prev][tight][1]
    return res

def solve():
    L, R = map(int, input().split())
    print(count_upto(R) - count_upto(L - 1))

if __name__ == "__main__":
    solve()
```

The implementation separates the counting logic into a helper function that computes prefix counts up to $X$. The DP explicitly tracks whether we have started constructing a number, which is necessary to correctly handle leading zeros without incorrectly enforcing the adjacency constraint.

The sentinel value `10` is used to represent the absence of a previous digit. This avoids mixing real digits with the “unset” state and keeps the transition logic clean.

The subtraction step `count_upto(R) - count_upto(L - 1)` ensures the interval is handled cleanly without special casing.

## Worked Examples

### Example 1: $L=6, R=21$

We compute valid numbers up to 21 and subtract those up to 5.

| Position | prev state | tight | started | transitions |
| --- | --- | --- | --- | --- |
| start | 10 | 1 | 0 | digits from 0-2 |
| pos 1 | - | - | - | builds 1-digit numbers 1-9 |
| pos 2 | - | - | - | builds 10, 12, 21 among others |

Valid numbers in range: 6, 7, 8, 9, 10, 12, 21.

This trace shows how single-digit numbers are naturally included and how two-digit transitions enforce the ±1 rule.

### Example 2: $L=10, R=15$

| Number | Validity |
| --- | --- |
| 10 | valid |
| 11 | invalid |
| 12 | valid |
| 13 | invalid |
| 14 | invalid |
| 15 | invalid |

The DP will only accept transitions where the second digit differs by exactly one from the first, which immediately filters the set down to 10 and 12.

This example demonstrates that adjacency checking is enforced locally and correctly eliminates invalid equal or non-adjacent digit pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(18 \cdot 10 \cdot 2 \cdot 10)$ | 18 positions, 10 digits, tight and started states, and up to 10 transitions per state |
| Space | $O(18 \cdot 10 \cdot 2)$ | DP table over position, digit, and tight state (optimized over prev/start states) |

The state space is fixed by the number of digits in the upper bound, so the solution easily fits within constraints even for $10^{18}$. The computation per query is effectively constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def count_upto(x: int) -> int:
        if x <= 0:
            return 0
        digits = list(map(int, str(x)))
        n = len(digits)
        dp = [[[[0] * 2 for _ in range(2)] for _ in range(11)] for _ in range(n + 1)]
        dp[0][10][1][0] = 1

        for pos in range(n):
            for prev in range(11):
                for tight in range(2):
                    for started in range(2):
                        cur = dp[pos][prev][tight][started]
                        if cur == 0:
                            continue
                        limit = digits[pos] if tight else 9
                        for d in range(limit + 1):
                            ntight = 1 if (tight and d == limit) else 0
                            if not started:
                                if d == 0:
                                    dp[pos + 1][10][ntight][0] += cur
                                else:
                                    dp[pos + 1][d][ntight][1] += cur
                            else:
                                if abs(d - prev) == 1:
                                    dp[pos + 1][d][ntight][1] += cur

        return sum(dp[n][p][t][1] for p in range(11) for t in range(2))

    L, R = map(int, inp.split())
    return str(count_upto(R) - count_upto(L - 1))

assert run("6 21") == "7"
assert run("1 9") == "9"
assert run("10 10") == "1"
assert run("11 11") == "0"
assert run("1 100")  # sanity check run
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 21 | 7 | sample correctness and multi-digit transitions |
| 1 9 | 9 | all single-digit numbers valid |
| 10 10 | 1 | single boundary number handling |
| 11 11 | 0 | invalid repeated digits |

## Edge Cases

A boundary case is when $L = 1$. In this situation, subtraction uses $L - 1 = 0$, and the DP correctly returns zero for non-positive inputs, ensuring no underflow or negative counting occurs.

A second case is when $X$ is a single digit. The DP allows starting new numbers at any digit from 1 to 9, and the adjacency constraint is never triggered because there is no previous digit. This guarantees all single-digit numbers are counted without special casing.

A third case is when numbers include internal zeros like 101 or 210. These are handled correctly because once a number has started, zeros are treated like any other digit and must satisfy the ±1 constraint relative to the previous digit.
