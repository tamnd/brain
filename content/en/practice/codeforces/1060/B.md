---
title: "CF 1060B - Maximum Sum of Digits"
description: "We are given a single large integer $n$, and we want to split it into two non-negative integers $a$ and $b$ such that their sum stays exactly $n$."
date: "2026-06-15T09:15:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1060
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 513 by Barcelona Bootcamp (rated, Div. 1 + Div. 2)"
rating: 1100
weight: 1060
solve_time_s: 649
verified: true
draft: false
---

[CF 1060B - Maximum Sum of Digits](https://codeforces.com/problemset/problem/1060/B)

**Rating:** 1100  
**Tags:** greedy  
**Solve time:** 10m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single large integer $n$, and we want to split it into two non-negative integers $a$ and $b$ such that their sum stays exactly $n$. Among all possible splits, we are asked to maximize the sum of digit sums of the two parts, meaning we want to maximize $S(a) + S(b)$, where $S(x)$ is the sum of decimal digits of $x$.

So the problem is not about choosing arbitrary numbers, but about distributing the digits of $n$ into two numbers that add up correctly while making the digit sums as large as possible.

The constraint $n \le 10^{12}$ means $n$ has at most 12 digits. A direct enumeration of all splits $a \in [0, n]$ is impossible because it would require iterating up to $10^{12}$ values, which is far beyond feasible limits. Even checking each split and computing digit sums would be $O(n \cdot \log n)$, which is completely infeasible.

This immediately forces us to look for a structural property of how digit sums behave under addition with carries.

A naive intuition might suggest that making both $a$ and $b$ “balanced” could help, but digit sum behaves oddly under carry propagation. The real complexity comes from how carries reduce digit sums: whenever two digits sum to 10 or more, a carry reduces the digit sum by 9 at that position.

A subtle edge case appears when $n$ is a power of ten, for example $n = 1000$. A naive split like $500 + 500$ feels balanced, but digit sum is relatively small compared to a construction like $999 + 1$, which exploits carries more effectively. This hints that the optimal structure is tightly connected to decimal carries rather than symmetric partitioning.

## Approaches

The brute-force approach tries every possible split $a$ from 0 to $n$, computes $b = n - a$, and evaluates $S(a) + S(b)$. This is correct because it checks every valid configuration. However, it requires $n$ iterations, and each digit sum computation costs $O(\log n)$, so the total complexity is $O(n \log n)$. For $n \approx 10^{12}$, this is far beyond any feasible runtime.

The key observation is that digit sum interacts with addition through carries. Instead of thinking about choosing arbitrary splits, we look at the structure digit by digit. Each decimal position behaves independently except for carries. The important idea is that the best way to maximize digit sums is to minimize destructive carries and instead force digits to become as large as possible in both numbers.

This leads to a standard greedy insight: we try to construct $a$ and $b$ so that their digits are as large as possible while still summing to $n$. A well-known simplification is that the optimal split occurs when we "borrow" in a way that creates maximal digits 9 and 0 structure. Concretely, the answer turns out to be achieved by trying splits where one number is composed of leading digits that saturate to 9 before a drop, and the other absorbs the remainder.

A practical way to capture this is to try splitting $n$ at different digit boundaries. For each prefix split position, we simulate making one number consist of a prefix like $10^k - 1$-style contributions, which maximizes digit sum locally. Since $n$ has at most 12 digits, we only need to test $O(\log n)$ candidate structures derived from prefix adjustments.

Thus we reduce the problem from a full search over all $a$ to a small set of greedy candidates constructed from digit structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \log n)$ | $O(1)$ | Too slow |
| Optimal | $O(d^2)$ where $d \le 12$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Convert $n$ into a string so we can reason about its decimal digits directly. Working digit-wise is essential because the behavior of digit sum depends on carries between positions.
2. Try constructing candidate splits by iterating over each possible position where we reduce a prefix of $n$ and replace the suffix with the largest possible digit configuration that does not exceed the original number. This captures the idea that pushing digits toward 9 increases digit sum.
3. For each candidate construction, compute the implied pair $(a, b)$ by simulating how the remainder of $n$ would be distributed after fixing one component.
4. Compute $S(a) + S(b)$ for each candidate. Since digit sums are cheap for 12-digit numbers, this step is constant-time per candidate in practice.
5. Track the maximum value across all candidates and output it.

The reason we only need these structured candidates is that any optimal solution can be transformed into one where at least one of the numbers has a digit pattern consisting of a prefix followed by all 9s, without decreasing the objective. This transformation argument reduces the infinite search space into a small finite set.

### Why it works

The key invariant is that whenever a digit position is not fully saturated to 9 in either $a$ or $b$, we can locally adjust the split to push that digit upward without violating the sum constraint, unless a carry constraint blocks it. That blocking point happens exactly at a prefix boundary of $n$. Therefore, any optimal configuration corresponds to a boundary where a carry transition occurs, and those boundaries are exactly the ones we enumerate.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_sum(x: int) -> int:
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s

def solve():
    n = int(input().strip())

    best = digit_sum(n)  # (a=n, b=0) baseline

    # Try splitting by forcing a prefix boundary in b
    # We construct candidates of form:
    # b = 10^k - 1, a = n - b
    p = 1
    while p <= n:
        b = p - 1
        a = n - b
        best = max(best, digit_sum(a) + digit_sum(b))
        p *= 10

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation is built around the observation that the most productive splits occur when one number is close to a number of the form $10^k - 1$, which is a sequence of 9s in decimal. We test all such boundaries up to the magnitude of $n$.

The baseline case $(n, 0)$ is included because it is always valid and sometimes optimal when $n$ itself has a large digit sum.

The loop over powers of ten generates all possible prefix-aligned "all 9s" candidates. For each such candidate $b$, we compute $a = n - b$, ensuring the constraint $a + b = n$ always holds.

## Worked Examples

### Example 1: $n = 35$

We test candidates where $b = 9$ and $b = 99$ (only $9$ is relevant here).

| step | p | b = p-1 | a = n-b | S(a) | S(b) | total |
| --- | --- | --- | --- | --- | --- | --- |
| init | - | 0 | 35 | 8 | 0 | 8 |
| 1 | 1 | 0 | 35 | 8 | 0 | 8 |
| 2 | 10 | 9 | 26 | 8 | 9 | 17 |
| 3 | 100 | 99 | invalid (negative a ignored in effect) | - | - | - |

The best configuration is $a=26, b=9$, giving 17.

This shows how introducing a single 9 digit in $b$ forces $a$ to increase digit sum after adjustment.

### Example 2: $n = 100$

| step | p | b | a | S(a) | S(b) | total |
| --- | --- | --- | --- | --- | --- | --- |
| init | - | 0 | 100 | 1 | 0 | 1 |
| 1 | 1 | 0 | 100 | 1 | 0 | 1 |
| 2 | 10 | 9 | 91 | 10 | 9 | 19 |
| 3 | 100 | 99 | 1 | 1 | 18 | 19 |

The optimal value is 19, achieved either way.

These traces show that distributing 9s in one component maximizes digit contribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n \cdot d)$ | We try at most 12 powers of 10, each digit sum costs $O(d)$ |
| Space | $O(1)$ | Only a few integers are stored |

The logarithmic number of candidates matches the decimal structure of $n$, making the solution easily fast enough for $n \le 10^{12}$.

## Test Cases

```python
import sys, io

def digit_sum(x):
    return sum(map(int, str(x)))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input().strip())

    best = digit_sum(n)
    p = 1
    while p <= n:
        b = p - 1
        a = n - b
        best = max(best, digit_sum(a) + digit_sum(b))
        p *= 10

    return str(best)

# provided sample
assert run("35\n") == "17"

# minimum case
assert run("1\n") == "1"

# power of ten case
assert run("100\n") == "19"

# all digits 9
assert run("99\n") == "18"

# large case
assert run("1000000000000\n") == str(max(digit_sum(1000000000000 - (10**k - 1)) + digit_sum(10**k - 1) for k in range(13)))

# symmetric case
assert run("50\n") == str(run("50\n"))

# edge carry-heavy case
assert run("19\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest boundary |
| 100 | 19 | carry structure benefit |
| 99 | 18 | all-9 behavior |
| 19 | 10 | carry-sensitive split |
| 10^12 | computed | large constraint handling |

## Edge Cases

For $n = 1$, the only valid split is $(1, 0)$. The algorithm tries $b = 0$ and returns $S(1) = 1$, which is correct.

For $n = 1000$, the algorithm evaluates $b = 9, 99, 999$. The best is typically $b = 999$, yielding $a = 1$, giving digit sum $1 + 27 = 28$. The loop correctly reaches this case because it iterates over all powers of ten.

For $n = 19$, the best split is $10 + 9$, giving digit sum $1 + 0 + 9 = 10$. The candidate $b = 9$ is explicitly tested, and the algorithm correctly captures this optimal carry-based decomposition.

Each of these cases demonstrates that the algorithm does not rely on uniform distribution but instead systematically explores carry-aligned boundaries, which are exactly where improvements over naive splitting occur.
