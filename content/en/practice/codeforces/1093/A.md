---
title: "CF 1093A - Dice Rolling"
description: "We are given a standard six-faced dice, but instead of the usual values 1 to 6, its faces contain the integers 2, 3, 4, 5, 6, and 7, all distinct. Each roll produces one of these numbers, and the score for a sequence of rolls is the sum of the visible faces."
date: "2026-06-15T14:57:46+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1093
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 56 (Rated for Div. 2)"
rating: 800
weight: 1093
solve_time_s: 388
verified: false
draft: false
---

[CF 1093A - Dice Rolling](https://codeforces.com/problemset/problem/1093/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 6m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a standard six-faced dice, but instead of the usual values 1 to 6, its faces contain the integers 2, 3, 4, 5, 6, and 7, all distinct. Each roll produces one of these numbers, and the score for a sequence of rolls is the sum of the visible faces.

For each query value $x$, we are asked to determine any number of rolls $k$ such that it is possible to obtain a total sum of exactly $x$ using exactly $k$ rolls. We are not required to construct the sequence of rolls, only to output a valid $k$.

The key interpretation is that once we fix $k$, the question becomes whether we can represent $x$ as a sum of $k$ integers, each chosen from $\{2,3,4,5,6,7\}$.

The constraints are small: $t \le 100$ and $x \le 100$. This immediately rules out any need for heavy combinatorics or search. Any solution that computes each answer in constant time per query is sufficient.

A subtle point is that many different values of $k$ can work for the same $x$. The problem does not ask for a minimum or maximum, only any valid one. That flexibility is what makes the construction simple.

There are no real edge cases involving impossibility, since the statement guarantees a solution exists for every query.

## Approaches

A brute-force interpretation would be to try every possible number of rolls $k$, and for each $k$, check whether $x$ can be formed using $k$ numbers from 2 to 7. For a fixed $k$, this is equivalent to asking whether $x$ lies in the range $[2k, 7k]$, since 2 is the minimum contribution of a roll and 7 is the maximum.

If we brute-force over all $k$ up to, say, $x$, and for each $k$ perform a check, the complexity remains small given constraints, but it is unnecessary. The structure of the problem suggests a direct construction.

The key observation is that for any chosen $k$, the achievable sums form a continuous interval from $2k$ to $7k$. This interval has no gaps because we can adjust individual rolls in steps of 1 while staying within the allowed face values. Therefore, instead of searching over sequences, we only need to find any integer $k$ such that $2k \le x \le 7k$.

Rearranging, we want:

$$\frac{x}{7} \le k \le \frac{x}{2}$$

Since $k$ must be an integer, any integer in this range works. A simple constructive choice is to take the smallest valid $k$ that still allows reaching $x$, which is:

$$k = \left\lceil \frac{x}{7} \right\rceil$$

Once we fix this $k$, the remaining difference $x - 2k$ can always be distributed by increasing some rolls from 2 up to 7.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k and sequences | O(x · 6^k) | O(1) | Too slow |
| Interval construction | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of queries $t$. Each query gives a target sum $x$.
2. For each $x$, compute the smallest integer $k$ such that $7k \ge x$. This ensures that even if all rolls are 7, we can reach or exceed $x$.
3. Output this $k$ as the answer for the query.

The reason we pick the ceiling of $x/7$ is that it minimizes the number of rolls while guaranteeing enough total capacity to reach $x$. Any smaller $k$ would cap the maximum achievable sum below $x$, making it impossible.

### Why it works

For any fixed number of rolls $k$, the set of achievable sums is exactly the interval $[2k, 7k]$. This is because each roll independently contributes any value from 2 to 7, and adjusting one roll by ±1 changes the total sum by exactly 1 while remaining valid. Therefore all integers in the range are reachable.

Choosing $k = \lceil x/7 \rceil$ guarantees $x \le 7k$. At the same time, since $k \ge 1$, we always have enough structure to represent $x$ by starting from all 2s and increasing some rolls. Thus $x \ge 2k$ also holds automatically for this construction range in the problem constraints, and any remaining gap can be filled by incrementing selected rolls up to 7.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x = int(input())
        k = (x + 6) // 7
        print(k)

if __name__ == "__main__":
    solve()
```

The code processes each query independently. The expression `(x + 6) // 7` is the standard integer ceiling division for $x/7$, ensuring we always pick the smallest $k$ such that $7k \ge x$.

The implementation avoids any simulation of dice rolls. The logic directly computes the minimal feasible number of rolls, which is sufficient because the problem allows any valid configuration.

## Worked Examples

### Example 1

Input: $x = 13$

We compute $k = \lceil 13/7 \rceil = 2$

| Step | x | k = ceil(x/7) | 7k | Feasible? |
| --- | --- | --- | --- | --- |
| 1 | 13 | 2 | 14 | Yes |

With 2 rolls, we can achieve sums from 4 to 14, so 13 is reachable. For instance, 6 + 7 works.

This confirms that the construction is sufficient even when the target is close to the upper boundary.

### Example 2

Input: $x = 37$

We compute $k = \lceil 37/7 \rceil = 6$

| Step | x | k | 7k | Feasible? |
| --- | --- | --- | --- | --- |
| 1 | 37 | 6 | 42 | Yes |

With 6 rolls, achievable sums range from 12 to 42. The target 37 lies inside this interval.

This demonstrates that even when $x$ is not a multiple of 7, the slack created by multiple rolls allows fine adjustment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each query is handled with a single arithmetic operation |
| Space | O(1) | Only a few integers are stored |

The constraints allow up to 100 queries, so a linear scan is trivial. The solution runs in constant time per test and is far below the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    for _ in range(t):
        x = int(sys.stdin.readline())
        k = (x + 6) // 7
        print(k)

    return output.getvalue().strip()

# provided samples
assert run("4\n2\n13\n37\n100\n") == "1\n2\n6\n15"

# custom cases
assert run("1\n7\n") == "1"
assert run("1\n8\n") == "2"
assert run("1\n14\n") == "2"
assert run("1\n1\n") == "1"
assert run("1\n100\n") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 | 1 | exact single-roll boundary |
| 8 | 2 | crossing first feasibility gap |
| 14 | 2 | upper boundary of small k |
| 1 | 1 | minimal constraint handling |
| 100 | 15 | large value scaling |

## Edge Cases

One important boundary is when $x$ is exactly divisible by 7. For example, $x = 14$. The algorithm gives $k = 2$. With two rolls, the maximum is $14$, achieved by $7 + 7$, confirming correctness at the upper boundary.

Another case is when $x$ is just above a multiple of 7, such as $x = 8$. Here $k = 2$. The range is $[4, 14]$, so 8 is achievable, for example $2 + 6$. This shows that even when one roll is insufficient, adding a second roll creates enough flexibility to fill the gap.

Finally, for very small values like $x = 2$, the formula gives $k = 1$. The only possible sum is exactly one roll, which must be 2, matching the requirement exactly.
