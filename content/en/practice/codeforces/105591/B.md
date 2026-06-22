---
title: "CF 105591B - \u041f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u0442\u0440\u0435\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a"
description: "We are asked whether it is possible to form a triangle whose side lengths are three consecutive natural numbers and whose perimeter equals a given value $p$. A valid triangle in this setting is fully determined by a starting integer $a$."
date: "2026-06-22T17:58:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105591
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, 7-8 \u043a\u043b\u0430\u0441\u0441\u044b, \u041d\u0438\u0436\u0435\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2024"
rating: 0
weight: 105591
solve_time_s: 43
verified: true
draft: false
---

[CF 105591B - \u041f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u0442\u0440\u0435\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a](https://codeforces.com/problemset/problem/105591/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked whether it is possible to form a triangle whose side lengths are three consecutive natural numbers and whose perimeter equals a given value $p$.

A valid triangle in this setting is fully determined by a starting integer $a$. The sides must then be $a$, $a+1$, and $a+2$. The perimeter constraint fixes their sum, so we are really checking whether there exists an integer $a \ge 1$ such that

$$a + (a+1) + (a+2) = p.$$

At the same time, these three values must satisfy the triangle inequality, meaning the largest side must be strictly smaller than the sum of the other two.

The input is a single integer $p$, and the output is binary: print 1 if at least one such triple exists, otherwise print 0.

Even though the problem looks geometric, it collapses entirely into arithmetic structure. The main constraint is not geometry but whether a simple linear system has an integer solution that also respects positivity and the triangle inequality.

The range $1 \le p \le 10^9$ immediately rules out any attempt to try all triples of consecutive integers. Even though $a$ is at most about $p/3$, iterating up to $10^9$ is impossible under a 1 second limit. The solution must reduce the search to constant time.

A subtle edge case appears when the perimeter is very small. For example, $p = 1$ or $p = 2$ cannot form any triangle at all, but even slightly larger values like $p = 4$ or $p = 5$ also fail because the smallest consecutive triple is $1,2,3$, whose perimeter is already 6. Another failure mode is forgetting the triangle inequality, although for consecutive integers it turns out to be automatically satisfied once positivity holds.

## Approaches

A direct approach would try every possible starting value $a$, compute the triple $(a, a+1, a+2)$, check whether the sum equals $p$, and verify the triangle inequality. This is correct but inefficient. The sum condition alone forces $3a + 3 = p$, so in practice there is only one candidate $a$ for each $p$, but a naive approach would still conceptually iterate over $O(p)$ possible values of $a$. With $p$ up to $10^9$, this is far beyond feasible limits.

The key observation is that the structure of the sides completely determines the perimeter. Once we assume consecutive integers, there is no combinatorial choice left. The perimeter equation fixes $a$ uniquely:

$$a = \frac{p - 3}{3}.$$

So the entire problem reduces to checking whether this value is an integer and whether it is at least 1. The triangle inequality then does not add a new constraint because for any positive $a$,

$$a + (a+1) > a+2$$

holds automatically.

Thus the problem becomes a divisibility and lower bound check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $a$ | O(p) | O(1) | Too slow |
| Direct formula check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute $p - 3$. This corresponds to removing the constant contribution of the fixed offsets in the consecutive structure.
2. Check whether $p - 3$ is divisible by 3. If not, no integer $a$ exists, so no valid triangle can be formed.
3. If divisible, compute $a = (p - 3) / 3$. This is the only possible candidate for the smallest side.
4. Verify that $a \ge 1$. This ensures the sides are valid natural numbers starting from 1 or greater.
5. If both conditions hold, output 1; otherwise output 0.

The logic relies on the fact that every valid triangle must correspond to exactly one arithmetic progression of length 3, so there is no need to search.

### Why it works

Any valid configuration must be of the form $(a, a+1, a+2)$. The perimeter equation forces a unique $a$. Since there is no freedom in choosing sides, the existence question reduces to whether this forced $a$ lies in the valid domain of natural numbers. The triangle inequality adds no additional restriction because consecutive integers always satisfy it once $a \ge 1$. This makes the arithmetic condition both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

p = int(input())

# Solve 3a + 3 = p
if (p - 3) % 3 != 0:
    print(0)
else:
    a = (p - 3) // 3
    if a >= 1:
        print(1)
    else:
        print(0)
```

The code directly encodes the derived equation. The expression $3a + 3 = p$ comes from summing three consecutive integers. The modulo check ensures integrality of $a$. The second check enforces that the sequence starts from a natural number at least 1, since the problem requires positive integer side lengths.

A common pitfall is forgetting to check $a \ge 1$, which would incorrectly accept cases like $p = 3$, producing $a = 0$, which is invalid.

## Worked Examples

### Example 1: $p = 18$

We compute $a = (18 - 3) / 3 = 5$.

| Step | p | p-3 | (p-3)%3 | a | Valid |
| --- | --- | --- | --- | --- | --- |
| Start | 18 | - | - | - | - |
| Compute remainder | 18 | 15 | 0 | - | yes |
| Compute a | 18 | 15 | 0 | 5 | candidate |
| Check bounds | 18 | 15 | 0 | 5 | valid |

The triple is $5, 6, 7$, which sums to 18 and satisfies triangle inequalities.

This confirms that when the arithmetic progression fits exactly, the solution exists.

### Example 2: $p = 10$

We compute $a = (10 - 3) / 3 = 7/3$, not an integer.

| Step | p | p-3 | (p-3)%3 | a | Valid |
| --- | --- | --- | --- | --- | --- |
| Start | 10 | - | - | - | - |
| Compute remainder | 10 | 7 | 1 | - | no |

Since divisibility fails, no valid consecutive triple can sum to 10.

This shows that most values of $p$ are immediately rejected by the modular condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic and one modulo check |
| Space | O(1) | No auxiliary data structures used |

The solution performs a constant number of integer operations regardless of $p$, so it trivially fits within the constraints even for $10^9$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    p = int(input())
    if (p - 3) % 3 != 0:
        return "0"
    a = (p - 3) // 3
    if a >= 1:
        return "1"
    return "0"

# provided-style sample
assert run("18\n") == "1"

# too small
assert run("5\n") == "0"

# smallest valid triangle 1,2,3
assert run("6\n") == "1"

# invalid divisibility
assert run("10\n") == "0"

# larger valid case 10,11,12 sum 33
assert run("33\n") == "1"

# boundary just below valid
assert run("5\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 | 1 | minimum valid triangle (1,2,3) |
| 5 | 0 | below minimum perimeter |
| 10 | 0 | non-divisible by 3 structure |
| 33 | 1 | larger valid progression |

## Edge Cases

A small perimeter such as $p = 6$ produces $a = 1$, giving the minimal triangle $1,2,3$. The algorithm computes $(6 - 3) = 3$, which is divisible by 3, yielding $a = 1$, so it accepts correctly.

For $p = 5$, the computation gives $p - 3 = 2$, which is not divisible by 3. The algorithm immediately rejects it, matching the fact that no three consecutive positive integers can sum to 5.

For $p = 3$, we get $p - 3 = 0$, which is divisible by 3, yielding $a = 0$. The final check $a \ge 1$ rejects it, preventing an invalid triangle with non-positive sides.
