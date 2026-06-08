---
title: "CF 1981A - Turtle and Piggy Are Playing a Game"
description: "We are given a range of integers $[l, r]$. Turtle chooses a number $x$ from this range. After that, Piggy repeatedly divides $x$ by one of its divisors greater than or equal to $2$, earning one point for each division, until the number becomes $1$."
date: "2026-06-08T16:47:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1981
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 949 (Div. 2)"
rating: 800
weight: 1981
solve_time_s: 133
verified: true
draft: false
---

[CF 1981A - Turtle and Piggy Are Playing a Game](https://codeforces.com/problemset/problem/1981/A)

**Rating:** 800  
**Tags:** brute force, greedy, math  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a range of integers $[l, r]$. Turtle chooses a number $x$ from this range. After that, Piggy repeatedly divides $x$ by one of its divisors greater than or equal to $2$, earning one point for each division, until the number becomes $1$.

Both players want the final score to be as large as possible. We need to determine that maximum possible score.

The key observation is that every operation replaces $x$ by $x / p$, where $p \ge 2$. Since $p$ is at least $2$, each operation reduces the current value by at least a factor of $2$. The score is simply the number of division steps before reaching $1$.

The constraints are extremely small from an algorithmic perspective. There are up to $10^4$ test cases and values are at most $10^9$. Any solution that iterates through the entire interval $[l,r]$ would be impossible because the interval length can approach $10^9$. We need a direct mathematical formula per test case.

A subtle mistake is to think that prime factorization itself determines the answer. For example, for $x=12$, the prime factorization is $2^2 \cdot 3$, giving three prime factors. The score is indeed $3$, but that is because Piggy can always choose prime divisors and remove only one prime factor at a time. The maximum score equals the total number of prime factors counted with multiplicity.

Another easy mistake is to search for the best number in the interval. Consider $l=114514$, $r=1919810$. Brute forcing millions of values is unnecessary. The optimal number is always the largest power of two that fits inside the interval.

## Approaches

A brute-force solution would examine every number $x$ in $[l,r]$, factorize it, count the total number of prime factors, and keep the maximum. This is correct because the maximum score for a fixed number equals the number of prime factors with multiplicity. Unfortunately, the interval length can be nearly $10^9$, making such a search completely infeasible.

The crucial observation is that every operation divides the current value by at least $2$. Starting from $x$, after $s$ operations we must have

$$x \ge 2^s.$$

This immediately gives

$$s \le \lfloor \log_2 x \rfloor.$$

This bound is achievable whenever $x$ itself is a power of two. For example, $2^{10}$ can be divided by $2$ exactly ten times.

Since Turtle may choose any number in $[l,r]$, the largest possible score is achieved by choosing the largest power of two that does not exceed $r$. Let

$$2^k \le r < 2^{k+1}.$$

Then $k=\lfloor \log_2 r \rfloor$.

Because the statement guarantees $2l \le r$, the interval always contains at least one power of two. If $2^k$ is the largest power of two not exceeding $r$, then $2^k > r/2 \ge l$. Thus $2^k$ lies inside the interval and can be chosen.

The answer is simply $\lfloor \log_2 r \rfloor$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l+1)\sqrt r)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $l$ and $r$.
2. Compute the largest integer $k$ such that $2^k \le r$.
3. Output $k$.

The easiest way in Python is to use the bit length of $r$. For any positive integer,

$$\lfloor \log_2 r \rfloor = r.\text{bit\_length()} - 1.$$

### Why it works

Every division removes a factor at least equal to $2$, so after $s$ operations the original number must be at least $2^s$. No number not exceeding $r$ can produce more than $\lfloor \log_2 r \rfloor$ operations.

The interval always contains the largest power of two not exceeding $r$. Choosing that value achieves exactly $\lfloor \log_2 r \rfloor$ operations by repeatedly dividing by $2$. Since both an upper bound and a matching construction exist, the answer is exactly $\lfloor \log_2 r \rfloor$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        l, r = map(int, input().split())
        ans.append(str(r.bit_length() - 1))

    sys.stdout.write("\n".join(ans))

solve()
```

The solution never uses $l$ after reading it. That may look surprising at first, but the guarantee $2l \le r$ is precisely what ensures the necessary power of two always lies inside the interval.

The expression `r.bit_length() - 1` computes $\lfloor \log_2 r \rfloor$ without floating-point arithmetic, avoiding precision issues. Since $r \le 10^9$, integer overflow is never a concern.

## Worked Examples

### Example 1

Input:

```
2 15
```

The largest power of two not exceeding $15$ is $8$.

| Value | Result |
| --- | --- |
| r | 15 |
| Largest power of two ≤ r | 8 |
| Score | 3 |

Output:

```
3
```

Choosing $x=8$:

$$8 \to 4 \to 2 \to 1$$

which gives three operations.

### Example 2

Input:

```
6 22
```

| Value | Result |
| --- | --- |
| r | 22 |
| Largest power of two ≤ r | 16 |
| Score | 4 |

Output:

```
4
```

Choosing $x=16$:

$$16 \to 8 \to 4 \to 2 \to 1$$

which gives four operations.

This example shows that the optimal choice is not necessarily $r$ itself. The best choice is the power of two inside the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test case | Only a bit-length computation |
| Space | $O(1)$ | Constant extra memory |

With at most $10^4$ test cases, the solution performs only a few integer operations per case and easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    lines = inp.strip().splitlines()
    t = int(lines[0])
    out = []

    idx = 1
    for _ in range(t):
        l, r = map(int, lines[idx].split())
        idx += 1
        out.append(str(r.bit_length() - 1))

    return "\n".join(out)

# provided sample
assert run(
"""5
2 4
3 6
2 15
6 22
114514 1919810
"""
) == "2\n2\n3\n4\n20"

# minimum valid range
assert run(
"""1
1 2
"""
) == "1"

# exact power of two
assert run(
"""1
8 16
"""
) == "4"

# interval containing many powers of two
assert run(
"""1
10 100
"""
) == "6"

# largest constraints style case
assert run(
"""1
500000000 1000000000
"""
) == "29"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `1` | Smallest valid interval |
| `8 16` | `4` | Upper endpoint is a power of two |
| `10 100` | `6` | Best choice is an interior power of two |
| `500000000 1000000000` | `29` | Large values near the limit |

## Edge Cases

Consider the smallest possible interval:

```
1
1 2
```

The only power of two available is $2$. We have

$$2 \to 1$$

so the score is $1$. The formula gives $\lfloor \log_2 2 \rfloor = 1$.

Consider an interval where the upper endpoint is itself a power of two:

```
1
8 16
```

The answer is $4$ because $16 = 2^4$. Repeatedly dividing by $2$ achieves four operations. The formula returns `16.bit_length() - 1 = 4`.

Consider a range where the optimal number is not the largest number:

```
1
6 22
```

The largest value is $22$, whose prime factorization is $2 \cdot 11$, giving only two operations. The interval also contains $16$, which gives four operations. The algorithm correctly finds the answer from the largest power of two not exceeding $22$, producing $4$.
