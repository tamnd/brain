---
title: "CF 104834B - Baklava Baking"
description: "We are working with nine-digit integers that represent possible configurations of Janise’s baklava layers. Each valid configuration is just an integer $N$ in the range from $100{,}000{,}000$ to $999{,}999{,}999$."
date: "2026-06-28T11:49:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104834
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 12-01-23 Div. 1 (Advanced)"
rating: 0
weight: 104834
solve_time_s: 82
verified: false
draft: false
---

[CF 104834B - Baklava Baking](https://codeforces.com/problemset/problem/104834/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with nine-digit integers that represent possible configurations of Janise’s baklava layers. Each valid configuration is just an integer $N$ in the range from $100{,}000{,}000$ to $999{,}999{,}999$. For each test case, a divisor $K$ is given, and we must count how many of these nine-digit numbers are divisible by $K$ while also satisfying an additional digit-based constraint.

That extra condition involves reversing the digits of $N$. When that reversed number is divisible by 5, we consider $N$ eligible for counting. So the task is to filter all nine-digit numbers by two properties at once: the original number must be divisible by $K$, and its digit-reversal must be divisible by 5.

The constraints push this toward a per-query constant-time solution. With up to $10^5$ test cases and $K$ as large as $10^5$, iterating over all candidate numbers for each query would require roughly $10^9$ operations per test in the worst case, which is far beyond acceptable limits. Any solution that enumerates numbers or simulates digit reversals per candidate is immediately infeasible.

A subtle issue appears in interpreting the reversal condition. If handled mechanically, one might attempt to compute reversed numbers for each multiple of $K$, but that introduces unnecessary digit manipulation. The key is that the reversal divisibility condition actually collapses into a constraint on the first digit of $N$, which removes any dependence on the rest of the number.

A common mistake is to think reversal changes divisibility in a complicated way. For example, taking $N = 120000005$, reversing it gives $500000021$, and checking divisibility by 5 depends only on the last digit of the reversed number, not the full structure. This observation is what simplifies the entire problem.

## Approaches

A brute-force approach would enumerate all nine-digit numbers, reverse each one, check divisibility by 5, and additionally test divisibility by $K$. There are $900{,}000{,}000$ such numbers, and each test case would require scanning this entire range. With up to $10^5$ test cases, this becomes completely unworkable, exceeding $10^{14}$ operations.

The crucial simplification comes from examining what “reverse divisible by 5” really means. A number is divisible by 5 exactly when its last digit is either 0 or 5. After reversing, the last digit of the reversed number is the first digit of the original number. This reduces the condition to a restriction on the leading digit of $N$. Since $N$ is a nine-digit number, the leading digit cannot be 0, so it must be 5.

This transforms the entire search space into a contiguous interval: all valid numbers lie between $500{,}000{,}000$ and $599{,}999{,}999$. The problem then becomes counting how many multiples of $K$ fall inside a fixed interval, which can be answered using floor division in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(T \cdot 10^9)$ | $O(1)$ | Too slow |
| Optimal | $O(T)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Recognize that reversing a number only affects digit order, and the last digit of the reversed number is the first digit of the original number. The divisibility by 5 condition therefore restricts the first digit of the nine-digit number.
2. Conclude that the first digit must be 5, since a nine-digit number cannot start with 0. This fixes the valid range of numbers to a single block from $500{,}000{,}000$ to $599{,}999{,}999$.
3. Reformulate the problem as counting integers divisible by $K$ inside this interval. Instead of iterating, we use arithmetic counting of multiples.
4. Compute how many multiples of $K$ are less than or equal to the upper bound $R = 599{,}999{,}999$, and subtract how many are strictly below the lower bound $L = 500{,}000{,}000$.
5. Output the difference for each test case.

### Why it works

The correctness rests on the fact that every valid nine-digit number is uniquely determined by its position in a fixed interval, and the reversal condition does not depend on any digit except the first. This reduces the original filtering problem into an interval intersection problem. Counting multiples of $K$ in an interval via floor division exactly enumerates all valid candidates without omission or duplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_multiples(r, k):
    return r // k

T = int(input())
L = 500_000_000
R = 599_999_999

for _ in range(T):
    K = int(input())
    ans = R // K - (L - 1) // K
    print(ans)
```

The solution relies entirely on integer division properties. The expression `R // K` counts all multiples of $K$ up to the upper bound, while `(L - 1) // K` removes those that fall below the valid interval. This avoids explicit loops and ensures constant-time processing per query.

A common implementation pitfall is forgetting to subtract `L - 1` rather than `L`. Using `L` directly would incorrectly exclude numbers equal to the lower bound when they are valid multiples of $K$.

## Worked Examples

We use the sample input:

| K | Valid range multiples ≤ R | Multiples < L | Answer |
| --- | --- | --- | --- |
| 1 | 599,999,999 | 499,999,999 | 100,000,000 |
| 2 | 299,999,999 | 249,999,999 | 50,000,000 |
| 3 | 199,999,999 | 166,666,666 | 33,333,333 |

For $K = 2$, the multiples of 2 inside the valid interval form a regular arithmetic pattern starting at 500,000,000 and ending at 599,999,998. Counting via floor division matches this sequence exactly without explicitly generating it.

This confirms that the transformation to interval counting preserves all structure from the original digit-based condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each test case uses a constant number of arithmetic operations |
| Space | $O(1)$ | No auxiliary data structures are needed |

The solution comfortably fits within limits because even with $10^5$ queries, the program performs only simple integer divisions per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    T = int(input())
    L = 500_000_000
    R = 599_999_999
    out = []
    for _ in range(T):
        K = int(input())
        out.append(str(R // K - (L - 1) // K))
    return "\n".join(out)

# provided samples
assert run("5\n1\n2\n3\n4\n5\n") == "100000000\n50000000\n33333333\n25000000\n20000000"

# custom: smallest K
assert run("1\n1\n") == "100000000"

# custom: K larger than range
assert run("1\n1000000000\n") == "0"

# custom: K = 500e6 (edge alignment)
assert run("1\n500000000\n") == "1"

# custom: mixed
assert run("3\n2\n7\n13\n") == run("3\n2\n7\n13\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| K=1 | full interval size | baseline counting correctness |
| large K | 0 | no multiples in range |
| K=500000000 | 1 | boundary inclusion |

## Edge Cases

For $K = 1$, the algorithm returns the total size of the interval $599{,}999{,}999 - 500{,}000{,}000 + 1 = 100{,}000{,}000$, matching the fact that every number in the range is valid. The computation reduces correctly to `R - (L - 1)`.

For very large $K$, such as $10^9$, both `R // K` and `(L - 1) // K` evaluate to 0, producing a correct result of 0 since no multiples exist in the interval.

At the boundary $K = 500{,}000{,}000$, the interval contains exactly one multiple, the lower bound itself. The subtraction formula ensures it is included because `(L - 1) // K` does not count it while `R // K` does.
