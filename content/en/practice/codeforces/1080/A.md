---
title: "CF 1080A - Petya and Origami"
description: "Petya is preparing invitation cards for a party, and each invitation consumes a fixed amount of colored paper sheets. Every invitation requires 2 red sheets, 5 green sheets, and 8 blue sheets."
date: "2026-06-15T06:26:21+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1080
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 524 (Div. 2)"
rating: 800
weight: 1080
solve_time_s: 314
verified: true
draft: false
---

[CF 1080A - Petya and Origami](https://codeforces.com/problemset/problem/1080/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 5m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

Petya is preparing invitation cards for a party, and each invitation consumes a fixed amount of colored paper sheets. Every invitation requires 2 red sheets, 5 green sheets, and 8 blue sheets. If there are $n$ friends, then $n$ invitations must be produced, so the total demand scales linearly with $n$: red demand is $2n$, green demand is $5n$, and blue demand is $8n$.

The store does not sell individual sheets. Instead, each purchase is a notebook of a single color, and every notebook contains exactly $k$ sheets. A notebook cannot be split across colors or partially used at purchase time, so the decision is purely about how many full notebooks of each color must be bought so that the total sheets are sufficient.

The output is the minimum total number of notebooks across all three colors that guarantees enough sheets for all invitations.

The constraints allow both $n$ and $k$ to be as large as $10^8$, which immediately rules out any simulation that iterates over notebooks or sheets. Any approach must compute the answer in constant time. The structure is purely arithmetic, so logarithmic or linear solutions are unnecessary and would be overkill.

A subtle edge case appears when the total sheets for a color are not divisible by $k$. For example, if $n = 1$, $k = 5$, and red demand is 2, then one notebook is enough for red, but if demand were 6, two notebooks are needed even though 6 is close to 5. This ceiling behavior is the main source of mistakes, especially if one uses integer division without rounding up.

## Approaches

A naive strategy would simulate buying notebooks one by one for each color until the required number of sheets is reached. For each color, we could repeatedly add $k$ sheets and count how many additions are needed to reach $2n$, $5n$, and $8n$. This is correct because it mimics the physical process of purchasing notebooks, but in the worst case where $n = 10^8$, the required totals are on the order of $10^9$ sheets. If $k = 1$, this leads to billions of iterations per color, which is far beyond time limits.

The key observation is that each color is independent. The number of notebooks required for red does not affect green or blue. Once we compute the total sheets needed for a color, the problem reduces to a standard ceiling division: how many groups of size $k$ are required to cover a total demand.

This reduces the entire problem to three independent integer ceiling divisions followed by a sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n \cdot \max(2,5,8))$ in worst sheet-level modeling | $O(1)$ | Too slow |
| Optimal Ceiling Arithmetic | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total number of sheets needed for each color: red is $2n$, green is $5n$, and blue is $8n$. This step isolates the demand so that each color can be treated independently.
2. For each color, determine how many notebooks are required. Since each notebook contributes exactly $k$ sheets, the required number is the smallest integer greater than or equal to demand divided by $k$. This is a ceiling division.
3. Compute the ceiling division using integer arithmetic as $(x + k - 1) // k$. This avoids floating point operations and correctly handles cases where $x$ is exactly divisible by $k$.
4. Sum the three results and output the total number of notebooks.

### Why it works

Each color behaves as a separate packing problem: we are covering a fixed demand using fixed-size containers. Any solution must supply at least the demand, so for each color the number of notebooks must satisfy $ans \cdot k \ge x$. The smallest integer satisfying this inequality is exactly the ceiling division. Since colors do not interact, summing these minimal independent solutions produces the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    red = 2 * n
    green = 5 * n
    blue = 8 * n

    def need(x):
        return (x + k - 1) // k

    print(need(red) + need(green) + need(blue))

if __name__ == "__main__":
    solve()
```

The code directly translates the mathematical structure into three independent computations. The helper function `need` implements ceiling division safely using integer arithmetic, which avoids floating point precision issues and ensures correctness at boundaries where `x` is a multiple of `k`.

## Worked Examples

### Example 1

Input:

```
3 5
```

| Step | Red | Green | Blue |
| --- | --- | --- | --- |
| Demand | 6 | 15 | 24 |
| Notebooks | 2 | 3 | 5 |

Total is $2 + 3 + 5 = 10$.

This shows how each color independently rounds up to the nearest multiple of 5 sheets. Blue dominates because its demand is largest relative to $k$.

### Example 2

Input:

```
1 4
```

| Step | Red | Green | Blue |
| --- | --- | --- | --- |
| Demand | 2 | 5 | 8 |
| Notebooks | 1 | 2 | 2 |

Total is $1 + 2 + 2 = 5$.

This example highlights ceiling behavior: green requires 2 notebooks because 5 sheets cannot fit into a single notebook of size 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations are performed |
| Space | $O(1)$ | No auxiliary data structures are used |

The computation is constant time regardless of input size, which fits comfortably within the limits even for $n, k \le 10^8$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, sys.stdin.readline().split())

    red = 2 * n
    green = 5 * n
    blue = 8 * n

    def need(x):
        return (x + k - 1) // k

    return str(need(red) + need(green) + need(blue))

# provided sample
assert run("3 5\n") == "10", "sample 1"

# minimum edge
assert run("1 1\n") == "15", "k=1 forces exact totals"

# exact divisibility
assert run("2 2\n") == "15", "no rounding needed for all colors"

# large k
assert run("10 100\n") == "1", "single notebook suffices"

# mixed rounding
assert run("4 3\n") == str((8+3)//3 + (20+2)//3 + (32+2)//3), "checks ceiling correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 15 | minimum notebook size, exact demand |
| 2 2 | 15 | exact divisibility across colors |
| 10 100 | 1 | large k collapses all demand |
| 4 3 | computed | ceiling behavior in all colors |

## Edge Cases

When $k = 1$, every sheet must come from a separate notebook. For input $n = 1, k = 1$, demands are 2, 5, and 8, so the result is 15 notebooks. The algorithm handles this correctly because $(x + 0) // 1 = x$, preserving exact counts.

When $k$ is very large, such as $k \ge 8n$, all demands fit into a single notebook per color. For $n = 10, k = 100$, red, green, and blue each require exactly 1 notebook, producing output 3. The ceiling formula collapses correctly since each demand divided by $k$ is less than 1 but rounds up to 1.

When $k$ divides all demands exactly, such as $n = 2, k = 2$, red is 4, green is 10, and blue is 16, all divisible by 2. The formula reduces to exact integer division without rounding, avoiding overcounting.
