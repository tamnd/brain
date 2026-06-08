---
title: "CF 1996D - Fun"
description: "We need to count ordered triples of positive integers $(a,b,c)$ that satisfy two independent restrictions. The first restriction limits the pairwise products: $$ab + ac + bc le n$$ The second restriction limits the sum: $$a + b + c le x$$ The word \"ordered\" matters."
date: "2026-06-08T14:43:23+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1996
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 962 (Div. 3)"
rating: 1500
weight: 1996
solve_time_s: 137
verified: true
draft: false
---

[CF 1996D - Fun](https://codeforces.com/problemset/problem/1996/D)

**Rating:** 1500  
**Tags:** binary search, brute force, combinatorics, math, number theory  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count ordered triples of positive integers $(a,b,c)$ that satisfy two independent restrictions.

The first restriction limits the pairwise products:

$$ab + ac + bc \le n$$

The second restriction limits the sum:

$$a + b + c \le x$$

The word "ordered" matters. If $(1,1,2)$ is valid, then $(1,2,1)$ and $(2,1,1)$ are counted separately.

The input contains multiple test cases. For each test case we receive $n$ and $x$, and must output the number of valid triples.

The constraints are the real clue. A single test can have $n,x$ as large as $10^6$, but the sum of all $n$ values over the entire input is at most $10^6$, and the sum of all $x$ values is also at most $10^6$.

A cubic search over all possible values of $a,b,c$ is completely impossible. Even a quadratic search over all values up to $10^6$ would be too large. We need to exploit the structure of

$$ab + ac + bc$$

to restrict the search space dramatically.

One easy mistake is forgetting that the variables must be strictly positive. For example:

```
n = 1, x = 10
```

There is no valid triple, because the smallest possible value of

$$ab+ac+bc$$

with positive integers is $1+1+1=3$.

Another subtle case appears when the sum bound is huge and effectively irrelevant:

```
n = 7, x = 1000
```

The answer is not determined by $x$. Every valid triple comes from the product inequality alone. A solution that iterates values up to $x$ would waste enormous time.

A third common bug is treating permutations as identical. For

```
n = 7, x = 4
```

the valid triples are

$$(1,1,1), (1,1,2), (1,2,1), (2,1,1)$$

which gives answer $4$, not $2$.

## Approaches

The most direct idea is brute force. Enumerate every positive $a$, every positive $b$, every positive $c$, check both inequalities, and count the valid triples.

This is obviously correct because every candidate is examined exactly once.

Unfortunately, even if we only considered values up to $10^6$, the search space would be on the order of

$$10^{18}$$

triples. That is nowhere near feasible.

The key observation is that once $a$ and $b$ are fixed, both constraints become simple upper bounds on $c$.

From

$$ab + ac + bc \le n$$

we obtain

$$c(a+b) \le n-ab$$

and therefore

$$c \le \frac{n-ab}{a+b}.$$

Since $c$ must be an integer,

$$c \le \left\lfloor \frac{n-ab}{a+b} \right\rfloor.$$

The sum restriction gives

$$c \le x-a-b.$$

So for a fixed pair $(a,b)$, the number of valid values of $c$ is simply

$$\min\!\left( \left\lfloor \frac{n-ab}{a+b} \right\rfloor, x-a-b \right)$$

provided this quantity is positive.

Now the problem becomes counting over pairs $(a,b)$.

We still need to avoid iterating all $10^{12}$ possible pairs. The product inequality itself gives a strong bound. Since $c\ge1$,

$$ab+a+b \le n.$$

Rearranging,

$$b(a+1) \le n-a.$$

Thus

$$b \le \frac{n-a}{a+1}.$$

For large $a$, this upper bound quickly becomes small. The total number of examined pairs is approximately

$$\sum_{a=1}^{n} \frac{n}{a} = O(n\log n).$$

Because the sum of all $n$ values across the input is only $10^6$, this harmonic-series complexity is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ or worse | $O(1)$ | Too slow |
| Optimal | $O(n \log n)$ per aggregate input | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Initialize the answer to zero.
2. Iterate all positive values of $a$.
3. For the current $a$, compute the largest possible $b$ that could still allow some positive $c$.

From $ab+a+b\le n$,

$$b \le \left\lfloor \frac{n-a}{a+1} \right\rfloor.$$

From $a+b+c\le x$ with $c\ge1$,

$$b \le x-a-1.$$

Take the minimum of these two bounds.
4. Iterate $b$ from $1$ to that maximum value.
5. Compute the product-based limit on $c$:

$$c_1= \left\lfloor \frac{n-ab}{a+b} \right\rfloor.$$
6. Compute the sum-based limit on $c$:

$$c_2=x-a-b.$$
7. Every integer $c$ in the range

$$1 \le c \le \min(c_1,c_2)$$

is valid, so add

$$\min(c_1,c_2)$$

to the answer.
8. After all pairs $(a,b)$ have been processed, output the accumulated answer.

### Why it works

For a fixed pair $(a,b)$, both original inequalities independently produce upper bounds on $c$. A value of $c$ is valid exactly when it satisfies both bounds simultaneously. The largest permissible $c$ is therefore the minimum of the two limits.

Every valid triple corresponds to exactly one pair $(a,b)$ and one counted value of $c$. Every counted value of $c$ satisfies both original inequalities by construction. This establishes a one-to-one correspondence between counted objects and valid triples, so the algorithm counts neither too many nor too few.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, x = map(int, input().split())

        total = 0

        a = 1
        while True:
            b1 = (n - a) // (a + 1)
            b2 = x - a - 1
            bmax = min(b1, b2)

            if bmax < 1:
                if b1 < 1:
                    break
                a += 1
                continue

            for b in range(1, bmax + 1):
                c1 = (n - a * b) // (a + b)
                c2 = x - a - b
                total += min(c1, c2)

            a += 1

        ans.append(str(total))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The outer loop iterates over possible values of $a$. The expression

```
(n - a) // (a + 1)
```

comes directly from the necessary condition $ab+a+b\le n$, which guarantees that at least one positive value of $c$ can exist.

The second bound

```
x - a - 1
```

comes from requiring room for a positive $c$ in the sum constraint.

For each valid pair $(a,b)$, the code computes the two independent upper bounds on $c$. The number of admissible values is exactly the smaller of the two bounds.

A common off-by-one mistake is forgetting that $c$ must be positive. The bounds for $b$ are derived assuming $c\ge1$, which is why the formulas contain the extra $+a+b$ terms rather than only $ab$.

Python integers automatically handle the large answers, which can exceed $2^{31}$.

## Worked Examples

### Example 1

Input:

```
n = 7, x = 4
```

| a | b | c from product | c from sum | added |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | 2 |
| 1 | 2 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 1 |

Total answer = 4.

The counted triples are:

$$(1,1,1), (1,1,2), (1,2,1), (2,1,1).$$

This example shows how a single pair $(a,b)$ can contribute multiple values of $c$.

### Example 2

Input:

```
n = 10, x = 5
```

| a | b | c from product | c from sum | added |
| --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 3 | 3 |
| 1 | 2 | 2 | 2 | 2 |
| 1 | 3 | 1 | 1 | 1 |
| 2 | 1 | 2 | 2 | 2 |
| 2 | 2 | 1 | 1 | 1 |
| 3 | 1 | 1 | 1 | 1 |

Total answer = 10.

This trace demonstrates that either inequality can become the active restriction. Sometimes the sum bound is smaller, sometimes the product bound is smaller.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O\!\left(\sum \frac{n}{a}\right)=O(n\log n)$ | Harmonic-series count of examined pairs |
| Space | $O(1)$ | Only a few integer variables are stored |

The crucial fact is that the total $n$ across all test cases is at most $10^6$. The harmonic-series iteration count is roughly $n\log n$, which is comfortably within the time limit for this aggregate input size.

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
        n, x = map(int, input().split())

        total = 0
        a = 1

        while True:
            b1 = (n - a) // (a + 1)
            b2 = x - a - 1
            bmax = min(b1, b2)

            if bmax < 1:
                if b1 < 1:
                    break
                a += 1
                continue

            for b in range(1, bmax + 1):
                c1 = (n - a * b) // (a + b)
                c2 = x - a - b
                total += min(c1, c2)

            a += 1

        out.append(str(total))

    return "\n".join(out)

# provided sample
assert run(
"""4
7 4
10 5
7 1000
900000 400000
"""
) == """4
10
7
1768016938"""

# minimum values
assert run(
"""1
1 1
"""
) == "0"

# exactly one valid triple
assert run(
"""1
3 3
"""
) == "1"

# sum bound dominates
assert run(
"""1
100 3
"""
) == "1"

# small manual case
assert run(
"""1
4 10
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | No positive triple exists |
| `3 3` | `1` | Smallest feasible valid triple |
| `100 3` | `1` | Very tight sum constraint |
| `4 10` | `1` | Large sum bound, product constraint dominates |

## Edge Cases

Consider:

```
1
1 1
```

The smallest possible value of $ab+ac+bc$ with positive integers is $3$. The loop computes

$$b_{\max}=\left\lfloor\frac{1-1}{2}\right\rfloor=0,$$

so no pair $(a,b)$ is processed and the answer remains $0$.

Now consider:

```
1
7 1000
```

The sum constraint is effectively irrelevant. For $(a,b)=(1,1)$, the product bound gives $c\le2$, while the sum bound gives $c\le998$. The algorithm correctly takes the smaller value and counts only the feasible $c$'s.

Finally consider:

```
1
7 4
```

The triples $(1,1,2)$, $(1,2,1)$, and $(2,1,1)$ are all distinct because the loops iterate ordered pairs $(a,b)$. No symmetry reduction is performed, so ordered triples are counted exactly as required.
