---
title: "CF 2093B - Expensive Number"
description: "We are given a decimal number as a string. We may delete any subset of its digits while preserving the relative order of the remaining digits. The resulting sequence of digits must represent a positive number, although leading zeros are allowed."
date: "2026-06-08T05:37:58+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2093
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1016 (Div. 3)"
rating: 900
weight: 2093
solve_time_s: 108
verified: true
draft: false
---

[CF 2093B - Expensive Number](https://codeforces.com/problemset/problem/2093/B)

**Rating:** 900  
**Tags:** greedy, math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a decimal number as a string. We may delete any subset of its digits while preserving the relative order of the remaining digits. The resulting sequence of digits must represent a positive number, although leading zeros are allowed.

For every resulting number, its cost is defined as:

$$\text{cost}=\frac{\text{number value}}{\text{sum of its digits}}$$

Among all valid subsequences, we want the smallest possible cost. Once that minimum cost is achieved, we want to keep as many digits as possible, because the output asks for the minimum number of deletions.

The input number can contain up to 100 digits, so it is far larger than standard integer types. This immediately suggests that any solution based on converting subsequences into actual integers is risky. The number of test cases is at most 1000, which means we need something close to linear time per test case. Since each string has length at most 100, even an $O(n^2)$ solution is easily fast enough.

The tricky part is understanding what the minimum possible cost actually is.

One easy mistake is to assume that keeping more non-zero digits helps. Consider:

```
n = 12
```

Possible valid subsequences are `1`, `2`, and `12`.

The costs are:

$$1/1=1,\quad 2/2=1,\quad 12/(1+2)=4$$

The minimum cost is 1, achieved by a single non-zero digit. The correct answer is 1 deletion.

Another subtle case is when leading zeros become useful:

```
n = 1005
```

Keeping `0005` is impossible because order must be preserved, but keeping `005` is valid. Its cost is

$$5/(0+0+5)=1$$

The result has three digits, not one. A solution that only searches for a single digit would miss the optimal deletion count.

A third common pitfall is forgetting that the final number must be positive:

```
n = 1000
```

Keeping only zeros is invalid because the resulting number equals zero. The best valid subsequence is `0001`? That order does not exist. The best choice is `1000`, `100`, `10`, or `1`. The minimum cost is achieved by `1`, and we can keep only one digit. The answer is 3 deletions.

## Approaches

A brute-force solution would enumerate every subsequence of the given string. For a length-100 number, there are

$$2^{100}$$

possible subsequences, which is completely infeasible. Even for length 60, this is already far beyond what can be processed.

The brute-force works conceptually because we can compute the cost of every valid subsequence and choose the best one. The problem is that the search space grows exponentially.

To find a better approach, we need to understand the structure of the cost function.

Suppose a subsequence has digit sum $S$ and numerical value $V$. Since the number is positive, $V \ge S$.

Why is this always true? A decimal number

$$d_k10^k+d_{k-1}10^{k-1}+\cdots+d_0$$

is at least

$$d_k+d_{k-1}+\cdots+d_0$$

because every power of ten is at least 1.

This gives

$$\frac{V}{S}\ge 1$$

for every valid subsequence.

So the minimum possible cost can never be below 1.

When does equality hold?

We need $V=S$. The only way a decimal number equals its digit sum is when exactly one non-zero digit exists and every other kept digit is a leading zero. Examples:

```
5
05
005
0007
```

All of these have cost 1.

Once we know the minimum achievable cost is always 1, the task changes completely. We are no longer optimizing a fraction. We only need the longest subsequence whose cost equals 1.

Such a subsequence must contain exactly one non-zero digit, and all other kept digits must be zeros before it. Any zero after that non-zero digit would contribute a decimal place and increase the numerical value without increasing the digit sum, making the cost greater than 1.

So for every non-zero digit position, we can form a cost-1 subsequence consisting of:

1. Any zeros before that position.
2. That non-zero digit itself.

Its length equals:

$$(\text{number of zeros before it}) + 1$$

We want the maximum such length.

If the original string length is $n$ and the maximum keepable length is $L$, then the answer is:

$$n-L$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Let the length of the string be $n$.
2. Scan the string from left to right while maintaining the number of zeros seen so far.
3. Whenever the current digit is `'0'`, increment the zero counter.
4. Whenever the current digit is non-zero, compute the length of the longest cost-1 subsequence ending at this digit.

That length is:

$$\text{zeros\_before}+1$$

because we can keep every earlier zero and this non-zero digit.
5. Track the maximum such length over all non-zero positions.
6. After the scan, let this maximum length be $L$.
7. Output:

$$n-L$$

since we keep $L$ digits and delete the rest.

### Why it works

Every positive number satisfies $V \ge S$, so every valid cost is at least 1. A subsequence achieves cost 1 exactly when its numerical value equals its digit sum.

For a decimal representation, that happens only when there is one non-zero digit and every other kept digit lies before it and is zero. Any additional non-zero digit increases the value more than the digit sum. Any zero after the non-zero digit creates an extra decimal place and also increases the value.

For a fixed non-zero digit, keeping all earlier zeros maximizes the subsequence length while preserving cost 1. Checking every non-zero position finds the longest possible cost-1 subsequence. Since cost 1 is the global minimum cost, maximizing the length among such subsequences minimizes the number of deletions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    s = input().strip()

    zeros = 0
    best = 0

    for ch in s:
        if ch == '0':
            zeros += 1
        else:
            best = max(best, zeros + 1)

    print(len(s) - best)
```

The variable `zeros` stores how many zeros have appeared before the current position.

Whenever we encounter a non-zero digit, we know that every previous zero can be kept together with this digit to form a cost-1 subsequence. The resulting length is `zeros + 1`.

The variable `best` stores the largest such length over the entire string.

Finally, if `best` digits can be kept while achieving the minimum possible cost, then all remaining digits must be removed. The answer is `len(s) - best`.

A subtle detail is that zeros appearing after the chosen non-zero digit are never counted. They cannot belong to a cost-1 subsequence because they would increase the numerical value while leaving the digit sum unchanged.

## Worked Examples

### Example 1

Input:

```
13700
```

| Position | Digit | Zeros Before | Candidate Length | Best |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 3 | 0 | 1 | 1 |
| 2 | 7 | 0 | 1 | 1 |
| 3 | 0 | 1 | - | 1 |
| 4 | 0 | 2 | - | 1 |

The longest cost-1 subsequence has length 1. We keep any one non-zero digit and delete the other four digits.

Answer:

$$5-1=4$$

### Example 2

Input:

```
102030
```

| Position | Digit | Zeros Before | Candidate Length | Best |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 1 | - | 1 |
| 2 | 2 | 1 | 2 | 2 |
| 3 | 0 | 2 | - | 2 |
| 4 | 3 | 2 | 3 | 3 |
| 5 | 0 | 3 | - | 3 |

The best choice is the subsequence `003`, formed by the two earlier zeros and the digit `3`.

Its length is 3, so:

$$6-3=3$$

deletions are needed.

This example demonstrates why leading zeros matter. They increase the number of kept digits without affecting the cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One left-to-right scan of the string |
| Space | $O(1)$ | Only a few counters are stored |

With at most 100 digits per test case and at most 1000 test cases, the total amount of work is tiny. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        s = input().strip()

        zeros = 0
        best = 0

        for ch in s:
            if ch == '0':
                zeros += 1
            else:
                best = max(best, zeros + 1)

        out.append(str(len(s) - best))

    return "\n".join(out)

# provided samples
assert run("4\n666\n13700\n102030\n7\n") == "2\n4\n3\n0"

# minimum size
assert run("1\n1\n") == "0"

# many leading zeros before final non-zero after deletions
assert run("1\n1005\n") == "1"

# all digits non-zero
assert run("1\n99999\n") == "4"

# off-by-one around final position
assert run("1\n0001\n") == "0"

# length 100 boundary
assert run("1\n" + "1" + "0" * 99 + "\n") == "99"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Smallest valid input |
| `1005` | `1` | Leading zeros can be kept before a non-zero digit |
| `99999` | `4` | No zeros available, only one digit can remain |
| `0001` | `0` | Entire string already has cost 1 |
| `1` followed by 99 zeros | `99` | Maximum length boundary and trailing-zero behavior |

## Edge Cases

### A number containing only one non-zero digit

Input:

```
1000
```

Scan:

| Digit | Zeros Before | Candidate |
| --- | --- | --- |
| 1 | 0 | 1 |
| 0 | 1 | - |
| 0 | 2 | - |
| 0 | 3 | - |

`best = 1`, so the answer is `4 - 1 = 3`.

Keeping any trailing zero after the digit `1` would produce `10`, `100`, or `1000`, all of which have cost greater than 1.

### Leading zeros are beneficial

Input:

```
1005
```

Scan:

| Digit | Zeros Before | Candidate |
| --- | --- | --- |
| 1 | 0 | 1 |
| 0 | 1 | - |
| 0 | 2 | - |
| 5 | 2 | 3 |

`best = 3`, corresponding to subsequence `005`.

The answer is `4 - 3 = 1`.

This shows why maximizing subsequence length among cost-1 subsequences matters.

### Multiple non-zero digits

Input:

```
12
```

Scan:

| Digit | Zeros Before | Candidate |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 0 | 1 |

`best = 1`, so the answer is `2 - 1 = 1`.

Keeping both digits yields cost $12/3 = 4$, which is worse than the minimum achievable cost of 1.

### Entire number already has minimum cost

Input:

```
0007
```

Scan:

| Digit | Zeros Before | Candidate |
| --- | --- | --- |
| 0 | 1 | - |
| 0 | 2 | - |
| 0 | 3 | - |
| 7 | 3 | 4 |

`best = 4`, so the answer is `4 - 4 = 0`.

The whole number already consists of leading zeros followed by a single non-zero digit, which gives cost 1 and requires no deletions.
