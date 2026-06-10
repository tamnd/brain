---
title: "CF 1426A - Floor Number"
description: "The problem asks us to find the floor number of a given apartment in a building with a slightly unusual layout. The first floor always has exactly two apartments, and every subsequent floor has the same number of apartments, which is given by $x$."
date: "2026-06-11T05:49:15+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1426
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 674 (Div. 3)"
rating: 800
weight: 1426
solve_time_s: 328
verified: false
draft: false
---

[CF 1426A - Floor Number](https://codeforces.com/problemset/problem/1426/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 5m 28s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to find the floor number of a given apartment in a building with a slightly unusual layout. The first floor always has exactly two apartments, and every subsequent floor has the same number of apartments, which is given by $x$. Apartment numbers start from $1$ on the first floor and increase sequentially as you move up the building. Given an apartment number $n$ and the number of apartments per floor $x$ after the first, the task is to compute which floor contains apartment $n$.

The input consists of multiple test cases, and for each test case, we are given $n$ and $x$. The constraints are small - $n$ and $x$ are at most $1000$, and there can be up to $1000$ test cases. This indicates that any solution that runs in $O(t)$ or $O(t \cdot 1)$ per test case is perfectly acceptable. Since the operations per test case are simple arithmetic calculations, there is no risk of exceeding time limits.

The edge cases to be aware of are apartments on the first floor, specifically $n = 1$ or $n = 2$. A careless implementation that always applies a formula for subsequent floors may miscalculate these cases. Another potential pitfall is when $n$ lands exactly at the boundary between two floors. For example, if $x = 3$, apartments $3$, $4$, and $5$ occupy the second floor, so an apartment $n = 5$ must correctly be identified as being on the second floor, not the third.

## Approaches

The naive approach is to simulate the floors one by one, counting apartments until reaching $n$. Start with two apartments on the first floor and then add $x$ apartments for each next floor, incrementing a floor counter until the current floor contains apartment $n$. While this is correct, it is slightly verbose for a problem with simple arithmetic and unnecessary for the constraints.

The optimal approach uses a simple formula. If $n \le 2$, the apartment is on the first floor. Otherwise, subtract the first-floor apartments and compute how many full subsequent floors are needed. This can be expressed as $(n - 3) // x + 2$, using integer division. The reasoning is that $n - 2$ apartments remain after the first floor. Dividing by $x$ gives the number of additional floors above the first, and we add $1$ to account for the first floor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | O(n) per test case | O(1) | Correct but unnecessary |
| Formula | O(1) per test case | O(1) | Optimal and accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$ and $x$.
3. Check if $n$ is $1$ or $2$. If so, output floor $1$ directly.
4. Otherwise, subtract $2$ from $n$ to account for the first floor.
5. Compute the number of additional floors as $(n - 3) // x + 2$. The subtraction by $1$ inside the division ensures correct floor rounding for exact multiples of $x$.
6. Output the computed floor number.

Why it works: The formula partitions the apartments into the first floor of two, then consecutive floors of size $x$. Integer division ensures that any apartment that is part of a partially filled last floor rounds correctly to that floor number. The edge case $n \le 2$ is handled separately to avoid negative division.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        if n <= 2:
            print(1)
        else:
            # subtract first floor, then compute which floor
            floor = (n - 3) // x + 2
            print(floor)

if __name__ == "__main__":
    solve()
```

The first conditional handles the first-floor edge case. For all other apartments, subtracting $3$ and adding $2$ in the formula correctly aligns the apartment number with the floor number. Integer division ensures that apartments at the end of a floor are counted on the correct floor.

## Worked Examples

Sample input:

```
n = 7, x = 3
```

Subtract the first floor:

```
n_remaining = 7 - 2 = 5
```

Compute additional floors:

```
(7 - 3) // 3 + 2 = 4 // 3 + 2 = 1 + 2 = 3
```

The result matches the expected output. Another example:

```
n = 1, x = 5
```

Since n <= 2, the first floor is returned.

| n | x | floor calculation | output |
| --- | --- | --- | --- |
| 7 | 3 | (7-3)//3+2 = 3 | 3 |
| 1 | 5 | first floor = 1 | 1 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is handled in constant time |
| Space | O(1) | Only a few integers are used per test case |

With $t \le 1000$ and $n, x \le 1000$, this solution executes comfortably within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n7 3\n1 5\n22 5\n987 13\n") == "3\n1\n5\n77", "sample 1"

# Custom cases
assert run("3\n2 10\n3 1\n5 2\n") == "1\n2\n2", "edge cases first and small x"
assert run("2\n1000 50\n51 50\n") == "21\n2", "large n and boundary floor"
assert run("1\n4 1\n") == "3", "small x, multiple floors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 10, 3 1, 5 2 | 1,2,2 | Edge cases with first floor and small x |
| 1000 50, 51 50 | 21,2 | Large n, multiple floors, boundary |
| 4 1 | 3 | Minimum x, multiple floors |

## Edge Cases

The critical edge case is when $n$ falls on the first floor. The solution correctly identifies apartments $1$ and $2$ as being on floor $1$. Another subtle case occurs when $n$ lands exactly at the last apartment of a floor after the first; the integer division formula automatically places it on the correct floor. For example, $n = 5$, $x = 3$: subtract the first floor (2 apartments) → remaining 3 apartments. Then $(5-3)//3 + 2 = 2$ correctly identifies floor 2.
