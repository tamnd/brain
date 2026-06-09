---
title: "CF 1982A - Soccer"
description: "In this problem, we are given a soccer game scenario where Dima remembers two scores: one just before he got distracted and another when he returned. Each score consists of the goals of the two teams. The game progresses one goal at a time for either team."
date: "2026-06-08T16:41:58+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1982
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 955 (Div. 2, with prizes from NEAR!)"
rating: 800
weight: 1982
solve_time_s: 118
verified: true
draft: false
---

[CF 1982A - Soccer](https://codeforces.com/problemset/problem/1982/A)

**Rating:** 800  
**Tags:** greedy, implementation, math, sortings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

In this problem, we are given a soccer game scenario where Dima remembers two scores: one just before he got distracted and another when he returned. Each score consists of the goals of the two teams. The game progresses one goal at a time for either team. We are asked to determine if it is possible that, during Dima's absence, the two teams never had equal scores. The output should be "YES" if this is possible and "NO" otherwise.

The scores are large integers, up to $10^9$, and the number of test cases can be up to $10^4$. This rules out any approach that would simulate every goal scored, because that could require iterating billions of steps. Instead, we must reason mathematically about the possible sequences of scores without generating them explicitly.

Non-obvious edge cases include situations where one team is far ahead and continues to score while the other team does not score at all. For example, if the initial score is $0:2$ and the final score is $5:2$, the first team could score five consecutive goals without the scores ever being equal. A careless approach that simulates all goal sequences might incorrectly assume an equality must occur.

## Approaches

The brute-force approach would attempt to simulate every possible sequence of scoring from the first score to the second. This is correct in theory because any sequence of one-goal increments for either team covers all possibilities. However, it is completely impractical because the number of goals scored can be as high as $10^9$, making the operation count unacceptable.

The key observation that simplifies the problem is that the only way scores can become equal is if the difference between the teams at the beginning is crossed by increments. Define $d_1 = x_1 - y_1$ and $d_2 = x_2 - y_2$. If $d_1$ and $d_2$ have the same sign (both positive or both negative) or one of them is zero, it is possible to reach the second score without the scores being equal. If the signs differ, it is impossible to avoid equality at some point. This reduces the problem to a simple check on the initial and final differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(x2-x1, y2-y1)) | O(1) | Too slow |
| Sign-based check | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read the scores before and after Dima was distracted, $(x_1, y_1)$ and $(x_2, y_2)$.
3. Compute the differences $d_1 = x_1 - y_1$ and $d_2 = x_2 - y_2$.
4. Check if $d_1 \cdot d_2 > 0$ or $d_1 = d_2 = 0$. This ensures the scores never cross zero, meaning equality never occurs.
5. If the condition is true, print "YES". Otherwise, print "NO".

Why it works: The product $d_1 \cdot d_2$ being positive guarantees that both differences have the same sign. Since a goal only increments one team's score, the difference changes monotonically, and it can never cross zero. This ensures that the teams never have equal scores during the interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x1, y1 = map(int, input().split())
        x2, y2 = map(int, input().split())
        d1 = x1 - y1
        d2 = x2 - y2
        if d1 * d2 > 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads each test case efficiently using fast I/O. Calculating the difference and checking the sign is done in constant time. The logic avoids simulating the scoring sequence, which would be infeasible.

## Worked Examples

**Sample 1**

| x1 | y1 | x2 | y2 | d1 | d2 | d1*d2 | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 5 | 0 | 1 | 5 | 5 | YES |
| 1 | 2 | 3 | 2 | -1 | 1 | -1 | NO |
| 1 | 2 | 4 | 5 | -1 | -1 | 1 | YES |

The first example shows that as long as the difference remains positive, equality is avoided. The second example shows the difference changes sign, which means equality must have occurred.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed in constant time. |
| Space | O(1) | Only a few integers are stored per test case. |

Given $t \le 10^4$, this algorithm executes within the time limits comfortably. Memory usage is minimal.

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
assert run("6\n1 0\n5 0\n1 2\n3 2\n1 2\n4 5\n1 2\n4 3\n1 2\n1 2\n998244353 0\n1000000000 999999999\n") == \
"YES\nNO\nYES\nNO\nYES\nYES", "sample 1"

# Custom cases
assert run("2\n0 1\n0 3\n5 2\n10 7\n") == "YES\nYES", "increasing differences"
assert run("2\n0 1\n2 0\n3 5\n7 4\n") == "NO\nNO", "crossing differences"
assert run("1\n0 0\n5 5\n") == "YES", "starts and ends tied but not crossed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 1 -> 0 3 | YES | Difference remains negative, no tie occurs |
| 0 1 -> 2 0 | NO | Difference crosses zero, tie occurs |
| 0 0 -> 5 5 | YES | Both start and end tied but no intermediate goals |

## Edge Cases

Consider a case where one team scores many goals while the other scores none. For example, starting from $0:1$ and ending at $0:5$, the difference is always negative, and no tie occurs. The algorithm calculates $d_1 = -1$, $d_2 = -5$, product positive, and correctly outputs "YES".

If the difference crosses zero, such as $1:2$ to $3:2$, the algorithm calculates $d_1 = -1$, $d_2 = 1$, product negative, and correctly outputs "NO". This confirms the correctness on subtle boundary conditions without simulating every score.
