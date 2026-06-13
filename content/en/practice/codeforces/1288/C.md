---
title: "CF 1288C - Two Arrays"
description: "We need to count pairs of arrays $(a,b)$, both of length $m$, whose values lie between $1$ and $n$. Array $a$ must be non-decreasing, array $b$ must be non-increasing, and at every position we require $ai le bi$. The answer can be very large, so we output it modulo $10^9+7$."
date: "2026-06-11T19:02:18+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 1288
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 80 (Rated for Div. 2)"
rating: 1600
weight: 1288
solve_time_s: 211
verified: true
draft: false
---

[CF 1288C - Two Arrays](https://codeforces.com/problemset/problem/1288/C)

**Rating:** 1600  
**Tags:** combinatorics, dp  
**Solve time:** 3m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count pairs of arrays $(a,b)$, both of length $m$, whose values lie between $1$ and $n$.

Array $a$ must be non-decreasing, array $b$ must be non-increasing, and at every position we require $a_i \le b_i$.

The answer can be very large, so we output it modulo $10^9+7$.

The first thing to notice is that $m$ is tiny, at most $10$, while $n$ can reach $1000$. Any solution whose complexity is polynomial in $n$ and $m$ is fine. A solution that tries to enumerate arrays is hopeless because the number of possible arrays is exponential. Even for $n=1000$ and $m=10$, there are $1000^{10}$ possible arrays.

The interesting part is the interaction between the monotonicity constraints and the condition $a_i \le b_i$. The arrays are not independent.

Consider a small example:

```
n = 2, m = 2
```

The valid pairs are exactly the five pairs listed in the statement.

A common mistake is to count non-decreasing arrays $a$ and non-increasing arrays $b$ separately and then try to combine them. That ignores the position-wise constraint $a_i \le b_i$. For example,

$$a=[1,2],\qquad b=[1,1]$$

satisfies the monotonicity requirements but violates $a_2 \le b_2$.

Another subtle case is when $n=1$.

```
1 10
```

Every element must be $1$, so there is exactly one valid pair:

$$a=[1,1,\ldots,1],\quad b=[1,1,\ldots,1].$$

Any formula that accidentally assumes multiple values are available will overcount.

A third edge case occurs when equality is frequent. For example:

```
2 1
```

Valid pairs are

$$(1,1),\ (1,2),\ (2,2).$$

The answer is $3$, not $2$. Solutions that treat $a_i<b_i$ instead of $a_i\le b_i$ lose all equal pairs.

## Approaches

The brute force approach is straightforward. Generate every non-decreasing array $a$, generate every non-increasing array $b$, and check whether $a_i\le b_i$ for all positions.

The number of non-decreasing arrays of length $m$ over values $1\ldots n$ is

$$\binom{n+m-1}{m}.$$

For $n=1000$ and $m=10$, this is already around $2.8\times10^{23}$. Enumerating them is completely impossible.

The key observation is that the two arrays can be merged into a single monotone sequence.

Write the values of $a$ from left to right:

$$a_1 \le a_2 \le \cdots \le a_m.$$

Now write the values of $b$ in reverse order:

$$b_m \le b_{m-1} \le \cdots \le b_1.$$

Because $a_i \le b_i$, the middle connection also respects the order:

$$a_m \le b_m.$$

Combining everything gives

$$a_1 \le a_2 \le \cdots \le a_m \le b_m \le b_{m-1} \le \cdots \le b_1.$$

This is simply a non-decreasing sequence of length $2m$ whose values lie in $1\ldots n$.

Conversely, every non-decreasing sequence of length $2m$ uniquely determines a valid pair $(a,b)$:

$$a_i = s_i, \qquad b_i = s_{2m-i+1}.$$

So the original problem is exactly equivalent to counting non-decreasing sequences of length $2m$ over $n$ values.

That is a classic stars-and-bars count:

$$\binom{n+2m-1}{2m}.$$

Since the modulus is prime and $n+2m-1 \le 1019$, we can compute this binomial coefficient efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Let

$$N = n + 2m - 1, \qquad K = 2m.$$
2. Observe that every valid pair $(a,b)$ corresponds to a non-decreasing sequence

$$a_1,\ldots,a_m,b_m,\ldots,b_1$$

of length $2m$.
3. Observe that every non-decreasing sequence of length $2m$ over values $1\ldots n$ reconstructs exactly one valid pair.

The correspondence is bijective, so counting pairs is the same as counting such sequences.
4. Count non-decreasing sequences of length $2m$ using stars and bars.

The number of multisets of size $2m$ chosen from $n$ values equals

$$\binom{n+2m-1}{2m}.$$
5. Compute the binomial coefficient modulo $10^9+7$.

Since the modulus is prime, use factorials and modular inverses:

$$\binom{N}{K} = \frac{N!}{K!(N-K)!}.$$
6. Output the result.

### Why it works

The entire solution rests on a bijection.

Given a valid pair $(a,b)$, the sequence

$$a_1,\ldots,a_m,b_m,\ldots,b_1$$

is non-decreasing because $a$ is non-decreasing, $b$ is non-increasing, and the condition $a_m\le b_m$ connects the two halves.

Given any non-decreasing sequence of length $2m$, assigning its first half to $a$ and its reversed second half to $b$ automatically produces a non-decreasing $a$, a non-increasing $b$, and $a_i\le b_i$ for every position. The two constructions are inverses of each other, so the mapping is one-to-one and onto.

Thus the answer is exactly the number of non-decreasing sequences of length $2m$ over $n$ possible values, which is $\binom{n+2m-1}{2m}$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n, m = map(int, input().split())

N = n + 2 * m - 1
K = 2 * m

fact = [1] * (N + 1)
for i in range(1, N + 1):
    fact[i] = fact[i - 1] * i % MOD

inv_fact = [1] * (N + 1)
inv_fact[N] = pow(fact[N], MOD - 2, MOD)

for i in range(N, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD

ans = fact[N]
ans = ans * inv_fact[K] % MOD
ans = ans * inv_fact[N - K] % MOD

print(ans)
```

The code directly implements the combinatorial formula.

The value $N=n+2m-1$ is the top of the binomial coefficient and $K=2m$ is the bottom.

Factorials are precomputed modulo $10^9+7$. Because the modulus is prime, Fermat's theorem gives

$$x^{-1} \equiv x^{MOD-2} \pmod{MOD}.$$

Computing the inverse factorial of $N$ first and then filling the remaining inverse factorials backwards is the standard linear-time technique.

The largest possible $N$ is

$$1000 + 20 - 1 = 1019,$$

so the arrays are tiny and fit comfortably within the limits.

## Worked Examples

### Example 1

Input:

```
2 2
```

We compute:

$$N = 2 + 4 - 1 = 5, \qquad K = 4.$$

| Variable | Value |
| --- | --- |
| n | 2 |
| m | 2 |
| N | 5 |
| K | 4 |
| Answer | $\binom{5}{4}=5$ |

Output:

```
5
```

This example demonstrates the bijection. The valid pairs correspond exactly to the five non-decreasing sequences of length four over values $\{1,2\}$.

### Example 2

Input:

```
1 3
```

We compute:

$$N = 1 + 6 - 1 = 6, \qquad K = 6.$$

| Variable | Value |
| --- | --- |
| n | 1 |
| m | 3 |
| N | 6 |
| K | 6 |
| Answer | $\binom{6}{6}=1$ |

Output:

```
1
```

Only the value $1$ exists, so every position in both arrays is forced. The formula correctly returns one valid pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Building factorial and inverse-factorial arrays up to $n+2m-1$ |
| Space | O(n + m) | Storage for factorial tables |

Since $n+2m-1\le1019$, the actual running time is tiny. The solution easily fits within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys

def solve():
    MOD = 10**9 + 7

    n, m = map(int, input().split())

    N = n + 2 * m - 1
    K = 2 * m

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)

    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    ans = fact[N]
    ans = ans * inv_fact[K] % MOD
    ans = ans * inv_fact[N - K] % MOD

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("2 2\n") == "5\n", "sample 1"

# minimum size
assert run("1 1\n") == "1\n", "minimum"

# single position
assert run("2 1\n") == "3\n", "all valid pairs"

# only one value available
assert run("1 10\n") == "1\n", "forced arrays"

# another small hand-checkable case
assert run("2 3\n") == "7\n", "C(7,6)=7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest possible instance |
| `2 1` | `3` | Correct handling of equality |
| `1 10` | `1` | Only one value available |
| `2 3` | `7` | Correct stars-and-bars formula |

## Edge Cases

Consider:

```
1 10
```

The algorithm computes

$$\binom{1+20-1}{20} = \binom{20}{20} = 1.$$

Only one non-decreasing sequence of length $20$ exists, namely all ones. This maps to the unique valid pair of arrays.

Consider:

```
2 1
```

The algorithm computes

$$\binom{2+2-1}{2} = \binom{3}{2} = 3.$$

The three pairs are $(1,1)$, $(1,2)$, and $(2,2)$. Equality cases are counted naturally because stars and bars counts multisets rather than strictly increasing sequences.

Consider:

```
2 2
```

The merged sequence has length $4$. The number of non-decreasing sequences over values $\{1,2\}$ is

$$\binom{5}{4}=5.$$

Reconstructing $a$ from the first two positions and $b$ from the reversed last two positions yields exactly the five valid pairs. The bijection guarantees that no valid pair is missed and none is counted twice.
