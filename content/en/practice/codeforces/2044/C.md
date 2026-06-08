---
title: "CF 2044C - Hard Problem"
description: "We are asked to assign monkeys to seats in a classroom with exactly two rows of m seats each. The monkeys come in three categories: a monkeys that will only sit in the first row, b monkeys that will only sit in the second row, and c monkeys that have no preference."
date: "2026-06-08T09:22:43+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2044
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 993 (Div. 4)"
rating: 800
weight: 2044
solve_time_s: 92
verified: true
draft: false
---

[CF 2044C - Hard Problem](https://codeforces.com/problemset/problem/2044/C)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to assign monkeys to seats in a classroom with exactly two rows of `m` seats each. The monkeys come in three categories: `a` monkeys that will only sit in the first row, `b` monkeys that will only sit in the second row, and `c` monkeys that have no preference. Each seat can hold only one monkey. The goal is to maximize the total number of monkeys seated.

The input gives `t` test cases. Each test case specifies the number of seats per row `m` and the counts `a`, `b`, `c`. The output for each test case is a single integer, the maximum number of monkeys that can be seated.

Given the constraints, each of `m`, `a`, `b`, and `c` can be as large as $10^8$, and there can be up to $10^4$ test cases. This immediately rules out any solution that iterates over all seats or all monkeys individually. We need a direct arithmetic computation per test case.

Non-obvious edge cases include situations where the number of row-specific monkeys exceeds the number of seats, or when the combined number of row-specific monkeys is less than the total seats, leaving room for flexible seating with the `c` monkeys. For instance, if `m = 3`, `a = 6`, `b = 1`, `c = 1`, the first row can only take 3 of the `a` monkeys, leaving the remaining `a` monkeys unseated. The second row has 3 seats, only 1 `b` monkey and 1 `c` monkey, for a total of 2. A careless approach might attempt to "move" monkeys between rows against their preferences, yielding an incorrect total.

## Approaches

The brute-force approach would try to seat each monkey one by one, checking row preference and seat availability. This is correct in principle but far too slow because the total number of monkeys can reach $3 \cdot 10^8$ and iterating over each monkey would take far too long.

The key insight is that this is a purely arithmetic problem. Each row can hold at most `m` monkeys, so the number of monkeys seated in row 1 is the minimum of `a + c` and `m`, and in row 2 it is the minimum of `b + remaining_c` and `m`. However, a simpler and equivalent calculation is to seat as many as possible in each row individually: row 1 can seat up to `m` monkeys, prioritizing `a` first, then any leftover from `c`. The same applies to row 2. Since the `c` monkeys are flexible, the maximum total is `min(a + c, m) + min(b + c, m)`, but we must be careful not to double-count `c`. The proper formula is to seat `a` up to `m`, `b` up to `m`, then use the remaining capacity in each row for `c` monkeys. This reduces the solution to a simple constant-time computation per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a + b + c) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the values `m`, `a`, `b`, `c`.
3. Compute the number of available seats in the first row after placing the `a` monkeys: `space1 = max(0, m - a)`. This represents the seats that can accommodate flexible monkeys.
4. Compute the number of available seats in the second row after placing the `b` monkeys: `space2 = max(0, m - b)`.
5. The number of `c` monkeys that can be seated is limited by the total remaining space: `c_used = min(c, space1 + space2)`.
6. The total number of seated monkeys is `min(a, m) + min(b, m) + c_used`. This ensures we never exceed the row capacities and respect all monkey preferences.
7. Print the total for each test case.

Why it works: We are always filling each row to its maximum capacity while respecting the row-specific constraints. Flexible monkeys fill only the remaining seats after row-specific monkeys are seated. This guarantees we are maximizing the number of seated monkeys without violating any preferences. Since every operation is arithmetic, the solution is fast enough even for the largest inputs.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    m, a, b, c = map(int, input().split())
    row1 = min(a, m)
    row2 = min(b, m)
    remaining_c = min(c, (m - row1) + (m - row2))
    print(row1 + row2 + remaining_c)
```

The code first reads the number of test cases. For each test case, we calculate the number of monkeys that can be seated in each row by limiting the row-specific monkeys to the row capacity. Then, we compute how many flexible monkeys (`c`) can fit in the remaining seats and sum these numbers. Using `min` ensures we never exceed capacities. Using `max(0, ...)` is unnecessary here because `min(c, ...)` naturally handles the case where the remaining space is zero.

## Worked Examples

Sample Input 2:

```
3 6 1 1
```

| Step | a | b | c | row1 | row2 | remaining_c | total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Initial | 6 | 1 | 1 | min(6,3)=3 | min(1,3)=1 | min(1,(3-3)+(3-1))=min(1,2)=1 | 3+1+1=5 |

This confirms that even if `a` exceeds `m`, only `m` monkeys can be seated in that row, and flexible monkeys fill the remaining available seats.

Sample Input 1:

```
10 5 5 10
```

| Step | a | b | c | row1 | row2 | remaining_c | total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Initial | 5 | 5 | 10 | min(5,10)=5 | min(5,10)=5 | min(10,(10-5)+(10-5))=min(10,10)=10 | 5+5+10=20 |

This confirms that the remaining flexible monkeys are distributed to fill all available space.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | All operations are arithmetic and constant-time. |
| Space | O(1) | Only a few integer variables are stored per test case. |

Given up to $10^4$ test cases, this gives a total of $O(10^4)$ operations, well within the 1-second time limit. Memory usage is minimal and safe for the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        m, a, b, c = map(int, input().split())
        row1 = min(a, m)
        row2 = min(b, m)
        remaining_c = min(c, (m - row1) + (m - row2))
        output.append(str(row1 + row2 + remaining_c))
    return "\n".join(output)

# Provided samples
assert run("5\n10 5 5 10\n3 6 1 1\n15 14 12 4\n1 1 1 1\n420 6 9 69\n") == "20\n5\n30\n2\n84"

# Custom tests
assert run("1\n1 1 1 1\n") == "2", "All equal and minimum"
assert run("1\n100000000 100000000 100000000 100000000\n") == "200000000", "Maximum inputs"
assert run("1\n3 3 3 3\n") == "6", "Equal distribution, row limits"
assert run("1\n5 0 0 10\n") == "10", "All flexible monkeys"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 2 | Minimum inputs, all equal |
| 100000000 100000000 100000000 100000000 | 200000000 | Maximum inputs handled |
| 3 3 3 3 | 6 | Correct handling of exact row limits |
| 5 0 0 10 | 10 | All flexible monkeys can fill rows |

## Edge Cases

If `a` exceeds `m` and `b` is small, the remaining flexible monkeys fill the second row. For `m = 3, a = 6, b = 1, c = 1`, row1 seats 3 monkeys, row2 seats 1 monkey, and 1 flexible monkey fills the remaining seat in row2. The total is `3 + 1 + 1 = 5`. The algorithm correctly calculates `row1 = min(6
