---
title: "CF 105043A - \u041f\u0435\u0442\u044f \u0438 \u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0435 \u0437\u0430\u043f\u0440\u043e\u0441\u044b"
description: "We are given a number $n$. Imagine writing all integers from $1$ to $n$ on a sheet. Two independent operations are performed on this set: every number divisible by 2 is marked in one color, and every number divisible by 3 is marked in another color."
date: "2026-06-28T01:31:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105043
codeforces_index: "A"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u041d\u0422\u041e: \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u043e\u043d\u043d\u0430\u044f \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u044c. \u0421\u0435\u043a\u0446\u0438\u044f - \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0430"
rating: 0
weight: 105043
solve_time_s: 74
verified: false
draft: false
---

[CF 105043A - \u041f\u0435\u0442\u044f \u0438 \u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0435 \u0437\u0430\u043f\u0440\u043e\u0441\u044b](https://codeforces.com/problemset/problem/105043/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a number $n$. Imagine writing all integers from $1$ to $n$ on a sheet. Two independent operations are performed on this set: every number divisible by 2 is marked in one color, and every number divisible by 3 is marked in another color. A number may receive one mark, two marks, or none.

The task is to count how many numbers receive exactly one mark. In other words, we want integers in $[1, n]$ that are divisible by 2 or 3, but not divisible by both.

The constraint $n \le 10^9$ immediately rules out any approach that iterates over all numbers. A linear scan would require up to a billion operations, which is too slow in Python under typical Codeforces limits. Any viable solution must compute the answer using arithmetic properties of divisibility.

A subtle edge case arises when a number is divisible by both 2 and 3. For example, at $n = 6$, the number 6 should not be counted even though it is divisible by both 2 and 3. A naive approach that simply counts multiples of 2 and multiples of 3 independently will overcount such numbers unless corrected.

## Approaches

The brute-force approach is straightforward. We iterate over all integers from 1 to $n$, check whether each is divisible by 2 or 3, and ensure it is not divisible by both. This is correct because it directly encodes the condition. However, it performs $n$ checks, which becomes infeasible when $n$ reaches $10^9$.

The key observation is that divisibility by 2 and 3 creates a periodic structure. Multiples of 2 appear every 2 numbers, multiples of 3 every 3 numbers, and numbers divisible by both appear every $\mathrm{lcm}(2,3) = 6$. This allows us to replace iteration with counting arithmetic progressions.

We compute three quantities: how many numbers are divisible by 2, how many are divisible by 3, and how many are divisible by both. Then we apply inclusion-exclusion to count those divisible by exactly one of the two conditions.

The final expression becomes:

$$\#(2 \text{ only}) + \#(3 \text{ only}) = (A + B - 2C)$$

where $A = \lfloor n/2 \rfloor$, $B = \lfloor n/3 \rfloor$, and $C = \lfloor n/6 \rfloor$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute $A = \lfloor n/2 \rfloor$, the number of integers divisible by 2 in $[1, n]$. This counts all numbers that would receive the first color.
2. Compute $B = \lfloor n/3 \rfloor$, the number of integers divisible by 3 in $[1, n]$. This counts all numbers that would receive the second color.
3. Compute $C = \lfloor n/6 \rfloor$, the number of integers divisible by both 2 and 3. These are exactly the numbers that get both marks, since $\mathrm{lcm}(2,3) = 6$.
4. Compute the final answer as $A + B - 2C$. Each number divisible by both was counted twice in $A + B$, but we want to exclude them entirely from the “exactly one mark” set, so we subtract them twice.

### Why it works

Every integer in $[1, n]$ falls into exactly one of four disjoint categories: divisible by neither 2 nor 3, divisible only by 2, divisible only by 3, or divisible by both. The expression $A + B - 2C$ assigns value 1 to elements in the “only 2” and “only 3” categories, and value 0 to all others. This alignment guarantees the computed sum matches exactly the count of numbers with exactly one mark.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

A = n // 2
B = n // 3
C = n // 6

print(A + B - 2 * C)
```

The code directly implements the inclusion-exclusion formula derived above. Integer division is safe because we are counting full multiples. The computation is constant time and uses only a few integer variables.

A common mistake is forgetting to subtract twice the overlap. Subtracting only once would count numbers divisible by both 2 and 3 as if they contributed one valid mark, but they should contribute zero.

## Worked Examples

### Example 1: $n = 5$

| Step | A = ⌊n/2⌋ | B = ⌊n/3⌋ | C = ⌊n/6⌋ | Expression |
| --- | --- | --- | --- | --- |
| Values | 2 | 1 | 0 | A + B - 2C = 3 |

The numbers are 1, 2, 3, 4, 5. Valid ones are 2 (only divisible by 2), 3 (only divisible by 3), and 4 (only divisible by 2). That yields 3, matching the computation.

This confirms that the formula correctly counts numbers with exactly one divisor condition active.

### Example 2: $n = 8$

| Step | A = ⌊n/2⌋ | B = ⌊n/3⌋ | C = ⌊n/6⌋ | Expression |
| --- | --- | --- | --- | --- |
| Values | 4 | 2 | 1 | A + B - 2C = 4 |

Numbers are 1 through 8. The valid ones are 2, 3, 4, 8. The number 6 is excluded because it is counted twice in A and B but corrected away by subtracting 2C.

The trace shows how overlap removal is essential to avoid counting numbers divisible by both.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a fixed number of arithmetic operations on integers |
| Space | $O(1)$ | Constant number of variables regardless of input size |

The solution easily fits within constraints because it avoids iteration over the range up to $n$. Even for $n = 10^9$, only a few integer divisions and additions are performed.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    A = n // 2
    B = n // 3
    C = n // 6
    return str(A + B - 2 * C)

def run(inp: str) -> str:
    return solve(inp)

# provided samples
assert run("5\n") == "3"
assert run("8\n") == "4"

# custom cases
assert run("1\n") == "0", "minimum size"
assert run("2\n") == "1", "only one multiple of 2"
assert run("3\n") == "1", "only one multiple of 3"
assert run("6\n") == "2", "boundary overlap case"
assert run("12\n") == "6", "regular periodic structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | minimum boundary |
| 2 | 1 | smallest multiple of 2 |
| 3 | 1 | smallest multiple of 3 |
| 6 | 2 | overlap handling |
| 12 | 6 | periodic correctness |

## Edge Cases

### Case $n = 1$

Input:

```
1
```

Here $A = 0$, $B = 0$, $C = 0$. The algorithm outputs 0. The only number present is 1, which is divisible by neither 2 nor 3, so it should not be counted. The formula correctly returns 0.

### Case $n = 6$

Input:

```
6
```

We compute $A = 3$, $B = 2$, $C = 1$. The result is $3 + 2 - 2 = 3$. The numbers contributing are 2, 3, and 4. The number 6 is excluded because it belongs to the overlap class and is fully removed by subtracting twice its contribution. This confirms correct handling of shared multiples.
