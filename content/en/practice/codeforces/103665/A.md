---
title: "CF 103665A - \u0420\u0435\u0448\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447"
description: "Two contestants are tracking how many programming problems they solve over time. Each of them already has some number of solved problems, and then they continue solving at a constant daily rate."
date: "2026-07-02T21:43:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103665
codeforces_index: "A"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2018"
rating: 0
weight: 103665
solve_time_s: 50
verified: true
draft: false
---

[CF 103665A - \u0420\u0435\u0448\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447](https://codeforces.com/problemset/problem/103665/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

Two contestants are tracking how many programming problems they solve over time. Each of them already has some number of solved problems, and then they continue solving at a constant daily rate. The task is to determine, after a fixed number of days, who ends up with a larger total count, or whether they tie.

Concretely, one person starts with an initial count `a` and increases it by `x` each day for `c` days. The other starts with `b` and increases it by `y` each day for the same number of days. We are asked to compare the final totals:

the first value becomes `a + x * c`, and the second becomes `b + y * c`, and we output which is larger.

The constraints are extremely small, all inputs are between 1 and 10. This immediately removes any need for performance considerations beyond constant time arithmetic. Even an approach that recomputes the totals in a loop over `c` days is trivial here because the maximum number of iterations is 10.

The only subtle issue is ensuring that the comparison is done after correctly accumulating both linear progressions. A typical mistake is to compare daily rates `x` and `y` without considering initial values, or to accidentally multiply incorrectly like `(a + x) * c` instead of `a + x * c`.

There are no hidden edge cases in terms of overflow or large input size, but conceptually the boundary case is when both totals are equal. For example, if `a = 3, x = 2, b = 5, y = 1, c = 2`, then both end at 7, and the output must be a draw.

## Approaches

The brute-force interpretation simulates the process day by day. Starting from `a` and `b`, we repeatedly add `x` and `y` for `c` iterations. This is straightforward and mirrors the story exactly. After each day, we update both counters. After `c` days, we compare the results.

This works correctly because it directly models the process described. However, even though it is already efficient for this problem, it is not the cleanest representation of the structure. The key observation is that both sequences are arithmetic progressions with constant step size. Instead of simulating all steps, we can compute the final value in closed form using a single multiplication.

The reason this simplification works is that repeated addition of a constant value is equivalent to multiplication. Doing `x` added `c` times is exactly `x * c`, and similarly for `y`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(c) | O(1) | Accepted |
| Direct Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute both final results and compare them directly.

1. Read the five integers `a, x, b, y, c`. These define initial scores, daily growth rates, and the number of days over which growth occurs.
2. Compute the final score for the first person as `a + x * c`. This represents starting from `a` and adding `x` once per day for `c` days.
3. Compute the final score for the second person as `b + y * c`, applying the same logic.
4. Compare the two final values. If the first is larger, the first person wins. If the second is larger, the second person wins. Otherwise, they are equal.
5. Output the corresponding string `"Feefa"`, `"Foofa"`, or `"Draw"`.

### Why it works

Each person’s progression is linear with constant increment per day. The total after `c` days depends only on the initial value and the sum of identical increments. Since addition is associative and commutative, grouping the daily increments into a single multiplication does not change the result. The comparison of final totals is therefore equivalent to comparing the full day-by-day simulation outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input())
x = int(input())
b = int(input())
y = int(input())
c = int(input())

first = a + x * c
second = b + y * c

if first > second:
    print("Feefa")
elif second > first:
    print("Foofa")
else:
    print("Draw")
```

The code follows the direct formula approach. Each input is read separately as required by the statement format. The multiplication is done once per participant, ensuring constant time computation.

The only subtle point is to ensure correct operator precedence and grouping. Writing `a + x * c` is correct because multiplication is evaluated before addition, but parentheses can be added for clarity without changing meaning.

## Worked Examples

### Example 1

Input:

```
3
2
5
1
2
```

We track both values:

| Step | Feefa value | Foofa value |
| --- | --- | --- |
| initial | 3 | 5 |
| after 2 days | 3 + 2·2 = 7 | 5 + 1·2 = 7 |

Both totals are equal, so the output is `"Draw"`.

This example shows that different starting values and growth rates can balance out exactly after a small number of steps.

### Example 2

Input:

```
1
3
2
1
4
```

| Step | Feefa value | Foofa value |
| --- | --- | --- |
| initial | 1 | 2 |
| after 4 days | 1 + 3·4 = 13 | 2 + 1·4 = 6 |

Feefa clearly ends with a larger total, so the correct output is `"Feefa"`.

This demonstrates that a higher daily rate dominates even if the initial value is smaller.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations is performed |
| Space | O(1) | Only a few integer variables are stored |

The constraints are small enough that even repeated simulation would be fast, but the constant-time formula is the most direct and clean representation of the process.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    a = int(input())
    x = int(input())
    b = int(input())
    y = int(input())
    c = int(input())

    first = a + x * c
    second = b + y * c

    if first > second:
        return "Feefa"
    elif second > first:
        return "Foofa"
    else:
        return "Draw"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("3\n2\n5\n1\n2\n") == "Draw"
assert run("1\n3\n2\n1\n4\n") == "Feefa"

# custom cases
assert run("1\n1\n1\n1\n10\n") == "Draw", "all equal growth"
assert run("10\n1\n1\n1\n1\n") == "Feefa", "initial dominance"
assert run("1\n1\n10\n1\n1\n") == "Foofa", "single day comparison"
assert run("2\n2\n2\n3\n5\n") == "Foofa", "different rates over multiple days"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal growth | Draw | symmetric parameters |
| initial dominance | Feefa | initial value impact |
| single day comparison | Foofa | rate vs base tradeoff |
| different rates over multiple days | Foofa | cumulative growth effect |

## Edge Cases

A key edge case is when both participants end with the same total. For example, `a = 3, x = 2, b = 5, y = 1, c = 2` leads to both ending at 7. The algorithm computes both expressions independently and correctly identifies equality, producing `"Draw"`.

Another subtle case is when one participant starts behind but has a higher daily rate. For instance, `a = 1, x = 3, b = 2, y = 1, c = 4` results in final values `13` and `6`. The formula captures the accumulated advantage correctly because it aggregates all daily increments rather than comparing only initial values.

Even though the problem size is tiny, these cases reinforce that the solution must compare full linear growth, not intermediate or per-day snapshots.
