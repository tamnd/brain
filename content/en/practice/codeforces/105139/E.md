---
title: "CF 105139E - Spicy or Grilled?"
description: "Each test case describes a simple catering plan for a programming contest. There are $n$ contestants in total. Exactly $x$ of them choose a grilled chicken burger set, while the remaining $n - x$ choose a spicy chicken burger set."
date: "2026-06-27T16:57:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105139
codeforces_index: "E"
codeforces_contest_name: "The 2024 International Collegiate Programming Contest in Hubei Province, China"
rating: 0
weight: 105139
solve_time_s: 36
verified: true
draft: false
---

[CF 105139E - Spicy or Grilled?](https://codeforces.com/problemset/problem/105139/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a simple catering plan for a programming contest. There are $n$ contestants in total. Exactly $x$ of them choose a grilled chicken burger set, while the remaining $n - x$ choose a spicy chicken burger set. The price of a spicy set is $a$, and the price of a grilled set is $b$. The task is to compute the total cost of preparing food for all contestants.

The structure is purely additive: every contestant contributes exactly one fixed cost depending on their choice, so the total cost is determined by counting how many fall into each category and multiplying by the corresponding price.

The constraints allow up to $10^4$ test cases, and each test case uses values up to $10^4$. This immediately implies that any solution must run in constant time per test case. Even a linear scan per test case would be unnecessary overhead, but still technically safe; however, anything involving nested loops over $n$ would be far beyond limits if $T$ is large.

The only subtle issue in problems of this form is integer overflow in languages with fixed-width integers, but in Python this is not a concern. Another possible mistake is swapping the counts or misinterpreting which group corresponds to which price. A concrete failure case would be $n = 5, x = 5, a = 10, b = 1$. The correct answer is $0 \cdot 10 + 5 \cdot 1 = 5$. A mistaken implementation might incorrectly apply $a$ to the grilled group, producing $50$, which is clearly wrong.

## Approaches

A direct approach is to simulate each contestant individually. For each of the $n$ contestants, we decide whether they are among the $x$ grilled ones and add either $a$ or $b$ to the running total. This works because it mirrors the problem definition exactly. However, it performs $n$ operations per test case, leading to $T \cdot n$ operations in the worst case. With both values up to $10^4$, this can reach $10^8$ operations, which is unnecessary for such a simple arithmetic problem.

The key observation is that we never need to know the identity of individual contestants. Only the counts matter. Once we recognize that exactly $x$ people pay $b$ and exactly $n - x$ people pay $a$, the entire problem collapses into a single expression. This removes all iteration and reduces each test case to a constant number of arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n)$ per test case | $O(1)$ | Too slow |
| Direct Formula | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $T$. Each test case is independent, so no state is carried between them.
2. For each test case, read integers $n, x, a, b$. These fully determine the composition of costs.
3. Compute the number of spicy sets as $n - x$. This is the complement of the grilled group.
4. Compute the total cost as $(n - x) \cdot a + x \cdot b$. This directly follows from summing contributions of each group.
5. Output the computed value immediately for the test case before moving to the next one.

### Why it works

The algorithm relies on the fact that the total cost is a linear sum over independent items. Each contestant contributes exactly one term to the sum, and the value of that term depends only on a binary classification: spicy or grilled. Since the counts of each class are fixed and disjoint, replacing individual summation with multiplication preserves exact equality. No hidden dependencies or ordering effects exist, so aggregation into counts does not lose information.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x, a, b = map(int, input().split())
        spicy = n - x
        total = spicy * a + x * b
        print(total)

if __name__ == "__main__":
    solve()
```

The solution reads each test case and applies the derived formula directly. The only implementation detail that matters is correctly computing $n - x$ for the spicy group. The multiplication order is irrelevant in Python due to its large integer support, but in fixed-width integer languages, using 64-bit integers would be necessary.

## Worked Examples

### Example 1

Input:

```
n = 600, x = 200, a = 27, b = 26
```

We compute the number of spicy sets as 400 and grilled sets as 200.

| Step | spicy | grilled | expression | total |
| --- | --- | --- | --- | --- |
| init | - | - | - | 0 |
| compute counts | 400 | 200 | - | 0 |
| add spicy cost | 400 | 200 | 400 × 27 | 10800 |
| add grilled cost | 400 | 200 | 200 × 26 | 5200 |
| final | 400 | 200 | sum | 16000 |

This confirms the formula correctly aggregates both groups independently.

### Example 2

Input:

```
n = 5, x = 0, a = 10, b = 3
```

| Step | spicy | grilled | expression | total |
| --- | --- | --- | --- | --- |
| init | - | - | - | 0 |
| compute counts | 5 | 0 | - | 0 |
| add spicy cost | 5 | 0 | 5 × 10 | 50 |
| add grilled cost | 5 | 0 | 0 × 3 | 0 |
| final | 5 | 0 | sum | 50 |

This case checks the boundary condition where no one chooses grilled food.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each test case is evaluated using a constant number of arithmetic operations |
| Space | $O(1)$ | Only a few integers are stored regardless of input size |

The constraints allow up to $10^4$ test cases, and a constant-time solution per case is easily fast enough. The algorithm performs only a few multiplications and additions per test case, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod  # placeholder to avoid lint issues
    # inline solution
    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n, x, a, b = map(int, sys.stdin.readline().split())
        out.append(str((n - x) * a + x * b))
    return "\n".join(out)

# provided sample (interpreted)
assert run("3\n600 200 27 26\n750 0 26 27\n750 750 1 1\n") == "16000\n19500\n750"

# minimum case
assert run("1\n1 0 5 7\n") == "5"

# all grilled
assert run("1\n10 10 3 9\n") == "90"

# all spicy
assert run("1\n10 0 3 9\n") == "30"

# mixed boundary
assert run("1\n5 2 10 1\n") == "42"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all grilled | 90 | x = n boundary |
| all spicy | 30 | x = 0 boundary |
| mixed case | 42 | correct split computation |
| sample set | multiple | multi-test handling |

## Edge Cases

When $x = 0$, nobody chooses grilled sets. The formula reduces to $n \cdot a$. The algorithm computes $n - x = n$, so the spicy group correctly absorbs all participants, and the grilled term vanishes.

When $x = n$, everyone chooses grilled sets. The spicy count becomes zero, and the total becomes $n \cdot b$. The subtraction step ensures the spicy contribution is exactly zero without special casing.

When $n = 1$, the formula still behaves consistently since either $x = 0$ or $x = 1$, and exactly one term contributes. The algorithm does not require branching, which avoids edge-case conditionals and keeps the implementation uniform.
