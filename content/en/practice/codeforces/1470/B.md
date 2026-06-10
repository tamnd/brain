---
title: "CF 1470B - Strange Definition"
description: "We are given an array of integers. Define two values as adjacent when $$frac{operatorname{lcm}(x,y)}{gcd(x,y)}$$ is a perfect square. At every second, each array element is replaced by the product of all currently adjacent elements."
date: "2026-06-11T01:00:24+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "graphs", "hashing", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1470
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 694 (Div. 1)"
rating: 1900
weight: 1470
solve_time_s: 187
verified: true
draft: false
---

[CF 1470B - Strange Definition](https://codeforces.com/problemset/problem/1470/B)

**Rating:** 1900  
**Tags:** bitmasks, graphs, hashing, math, number theory  
**Solve time:** 3m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. Define two values as adjacent when

$$\frac{\operatorname{lcm}(x,y)}{\gcd(x,y)}$$

is a perfect square.

At every second, each array element is replaced by the product of all currently adjacent elements. The quantity we care about is the beauty of the array, which is the largest adjacency count among all positions.

For each query value $w$, we must report the beauty after exactly $w$ seconds.

The first challenge is understanding adjacency. The second challenge is understanding how the repeated transformations affect the array. The queries ask for arbitrarily large times, up to $10^{18}$, so direct simulation is impossible.

The total number of array elements across all test cases is at most $3 \cdot 10^5$, and the same bound holds for the total number of queries. This immediately rules out anything quadratic in $n$. An $O(n^2)$ adjacency graph would require roughly $9 \cdot 10^{10}$ comparisons in the worst case. We need something close to linear or $O(n \log n)$ per test case.

The values themselves are at most $10^6$. That is small enough to preprocess prime factors for every number using a sieve.

A common mistake is to work with the original numbers instead of their square-free kernels.

Consider:

```
1
3
12 3 48
1
0
```

Both $12$ and $48$ reduce to $3$ after removing all squared prime factors:

$$12 = 2^2 \cdot 3 \rightarrow 3$$

$$48 = 2^4 \cdot 3 \rightarrow 3$$

All three values belong to the same adjacency class, so the answer is 3. Treating the original numbers as distinct would incorrectly produce smaller groups.

Another subtle case is the value 1.

```
1
4
1 4 9 16
2
0
1
```

Every number reduces to square-free kernel 1. Initially the largest group size is 4. After stabilization it remains 4. Forgetting that perfect squares collapse to kernel 1 produces wrong answers.

The most important edge case concerns large $w$.

```
1
3
2 2 3
2
0
100
```

The answer for $w=0$ differs from the answer for $w>0$. The process stabilizes after one transformation, so all positive times share the same answer. Simulating time would miss this structural simplification.

## Approaches

A brute-force solution would first build the adjacency graph. For every pair $(i,j)$, compute whether

$$\frac{\operatorname{lcm}(a_i,a_j)}{\gcd(a_i,a_j)}$$

is a perfect square.

This requires $O(n^2)$ pair checks. Even if each check were constant time, $n=3\cdot10^5$ makes this completely infeasible.

The key observation comes from prime factorization.

Let

$$x=\prod p_i^{\alpha_i},
\qquad
y=\prod p_i^{\beta_i}.$$

Since

$$\frac{\operatorname{lcm}(x,y)}{\gcd(x,y)}
=
\prod p_i^{|\alpha_i-\beta_i|},$$

the result is a perfect square exactly when every exponent difference is even.

That means

$$\alpha_i \equiv \beta_i \pmod 2$$

for every prime.

Only exponent parity matters.

For each number, keep precisely the primes whose exponents are odd. Their product is called the square-free kernel.

Examples:

$$12 = 2^2\cdot3 \rightarrow 3$$

$$18 = 2\cdot3^2 \rightarrow 2$$

$$72 = 2^3\cdot3^2 \rightarrow 2$$

Two numbers are adjacent if and only if they have the same square-free kernel.

This transforms the problem into counting frequencies of kernels.

The remaining question is the repeated evolution of the array.

Suppose a kernel class contains $k$ elements. Every element in that class multiplies exactly the same set of values, namely all members of the class. Thus after one second every element of the class becomes identical.

A deeper analysis shows that after one step, every class whose kernel is 1 or whose size is even collapses into kernel 1. Classes with odd size and non-one kernel remain distinct.

This is the central observation used in the official solution.

Let:

- `mx0` be the largest frequency among all kernels.
- `mx1` be the total frequency of:

- kernel 1,
- every non-one kernel whose frequency is even.

Then all remaining odd-frequency non-one kernels stay separate.

For any positive time, the answer becomes

$$\max(mx1,\text{largest odd-frequency non-one class}).$$

This value is traditionally called `mx_inf`.

The process stabilizes immediately, so:

- $w=0$ uses `mx0`.
- $w>0$ uses `mx_inf`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n^2)$ | Too slow |
| Optimal | $O(n \log \log M + n)$ after sieve preprocessing | $O(n)$ | Accepted |

Here $M=10^6$.

## Algorithm Walkthrough

### Preprocessing

Compute the smallest prime factor for every integer up to $10^6$. This lets us factor each array value quickly.

### Per Test Case

1. For every array value, compute its square-free kernel.

Factor the number and keep only primes whose exponent is odd.
2. Count the frequency of every kernel.

Let `cnt[k]` be the number of occurrences of kernel `k`.
3. Compute `mx0`.

This is simply the maximum frequency among all kernels.
4. Compute the stabilized large group.

Initialize

$$\text{good}=0.$$

For every kernel-frequency pair:

- If the kernel equals 1, add its frequency to `good`.
- Else if the frequency is even, add its frequency to `good`.

These groups merge into the kernel-1 component after one step.
5. Compute the largest remaining odd-frequency non-one class.

Let

$$\text{oddmax}$$

be the maximum frequency among kernels different from 1 whose frequency is odd.
6. Define

$$mx\_inf=\max(\text{good},\text{oddmax}).$$

This is the answer for every positive time.
7. For each query:

- If $w=0$, print `mx0`.
- Otherwise, print `mx_inf`.

### Why it works

Adjacency depends only on exponent parity in prime factorizations. Replacing each number by its square-free kernel preserves all adjacency relationships.

All numbers with the same kernel form a complete component, and numbers with different kernels are never adjacent. After one transformation, every element inside a component becomes identical because each multiplies exactly the same set of values.

A component with even size produces a perfect square factor contribution and collapses into kernel 1. Components already having kernel 1 also belong there. Odd-sized non-one components retain their kernel. After this first transformation the partition no longer changes, so the process is stable forever.

Consequently the beauty at time 0 is the largest original component size, while the beauty at every positive time is the largest component size after this stabilization.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXA = 10 ** 6

spf = list(range(MAXA + 1))
for i in range(2, int(MAXA ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXA + 1, i):
            if spf[j] == j:
                spf[j] = i

def kernel(x):
    res = 1
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt ^= 1
        if cnt:
            res *= p
    return res

t = int(input())

for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    freq = {}

    for x in arr:
        k = kernel(x)
        freq[k] = freq.get(k, 0) + 1

    mx0 = max(freq.values())

    good = 0
    oddmax = 0

    for k, c in freq.items():
        if k == 1 or c % 2 == 0:
            good += c
        else:
            oddmax = max(oddmax, c)

    mx_inf = max(good, oddmax)

    q = int(input())

    for _ in range(q):
        w = int(input())
        if w == 0:
            print(mx0)
        else:
            print(mx_inf)
```

The sieve computes the smallest prime factor for every number once. Since all values are at most $10^6$, this preprocessing cost is shared across every test case.

The `kernel` function removes squared prime contributions. Instead of storing full exponents, it tracks parity. Whenever a prime appears an odd number of times, that prime contributes to the kernel.

The frequency map represents connected components in the adjacency graph. Every number with the same kernel belongs to the same component.

`mx0` answers the original array. The variables `good` and `oddmax` encode the stabilized state. The distinction between kernel 1, even-sized groups, and odd-sized non-one groups is exactly the characterization proved above.

The query handling is extremely simple because the process stabilizes after one step. Every query with $w>0$ receives the same answer.

## Worked Examples

### Sample 1

Input array:

```
6 8 4 2
```

| Value | Factorization | Kernel |
| --- | --- | --- |
| 6 | $2\cdot3$ | 6 |
| 8 | $2^3$ | 2 |
| 4 | $2^2$ | 1 |
| 2 | $2$ | 2 |

Frequency table:

| Kernel | Frequency |
| --- | --- |
| 6 | 1 |
| 2 | 2 |
| 1 | 1 |

Then:

| Variable | Value |
| --- | --- |
| mx0 | 2 |
| good | 3 |
| oddmax | 1 |
| mx_inf | 3 |

The query is $w=0$, so the answer is `mx0 = 2`.

This example shows that time 0 uses the original component sizes, not the stabilized ones.

### Sample 2

Input array:

```
12 3 20 5 80 1
```

Kernel reductions:

| Value | Kernel |
| --- | --- |
| 12 | 3 |
| 3 | 3 |
| 20 | 5 |
| 5 | 5 |
| 80 | 5 |
| 1 | 1 |

Frequency table:

| Kernel | Frequency |
| --- | --- |
| 3 | 2 |
| 5 | 3 |
| 1 | 1 |

Computed values:

| Variable | Value |
| --- | --- |
| mx0 | 3 |
| good | 3 |
| oddmax | 3 |
| mx_inf | 3 |

The query is $w=1$, so the answer is `mx_inf = 3`.

This example demonstrates that an odd-sized non-one component can remain the largest group even after stabilization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log \log 10^6 + q)$ overall per test case after preprocessing | Kernel computation is near-linear using SPF factorization |
| Space | $O(n)$ | Frequency map stores at most one entry per distinct kernel |

The total number of array elements and queries across all test cases is only $3 \cdot 10^5$. The sieve is built once, and every value is factorized quickly using its smallest prime factors. The solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    from collections import defaultdict

    data = io.StringIO(inp)
    input = data.readline

    MAXA = 10**6

    spf = list(range(MAXA + 1))
    for i in range(2, int(MAXA ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def kernel(x):
        r = 1
        while x > 1:
            p = spf[x]
            parity = 0
            while x % p == 0:
                x //= p
                parity ^= 1
            if parity:
                r *= p
        return r

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        freq = defaultdict(int)
        for x in arr:
            freq[kernel(x)] += 1

        mx0 = max(freq.values())

        good = 0
        oddmax = 0

        for k, c in freq.items():
            if k == 1 or c % 2 == 0:
                good += c
            else:
                oddmax = max(oddmax, c)

        mx_inf = max(good, oddmax)

        q = int(input())
        for _ in range(q):
            w = int(input())
            out.append(str(mx0 if w == 0 else mx_inf))

    return "\n".join(out) + "\n"

# provided samples
assert run(
"""2
4
6 8 4 2
1
0
6
12 3 20 5 80 1
1
1
"""
) == """2
3
"""

# minimum size
assert run(
"""1
1
1
2
0
100
"""
) == """1
1
"""

# all equal values
assert run(
"""1
5
2 2 2 2 2
2
0
1
"""
) == """5
5
"""

# all perfect squares
assert run(
"""1
4
4 9 16 25
2
0
10
"""
) == """4
4
"""

# mixed parity frequencies
assert run(
"""1
5
2 8 18 50 3
2
0
1
"""
) == """4
4
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single value 1 | 1, 1 | Minimum size and kernel 1 handling |
| All values equal | 5, 5 | One large component |
| All perfect squares | 4, 4 | Everything collapses to kernel 1 |
| Mixed parity frequencies | 4, 4 | Correct treatment of even and odd class sizes |

## Edge Cases

### All values reduce to kernel 1

Input:

```
1
4
4 9 16 25
1
100
```

The kernels are:

```
1 1 1 1
```

Frequency table:

```
{1: 4}
```

We get:

```
mx0 = 4
good = 4
oddmax = 0
mx_inf = 4
```

Answer: 4.

An implementation that keeps original values separate would incorrectly produce four singleton groups.

### Large positive time

Input:

```
1
3
2 2 3
2
1
1000000000000000000
```

Kernel frequencies:

```
2 -> 2
3 -> 1
```

Then:

```
mx0 = 2
good = 2
oddmax = 1
mx_inf = 2
```

Both positive-time queries return 2.

The algorithm never simulates time. It uses the fact that the process stabilizes after one transformation.

### Odd-sized non-one component

Input:

```
1
3
20 5 80
2
0
1
```

All three numbers reduce to kernel 5.

Frequency table:

```
5 -> 3
```

Then:

```
mx0 = 3
good = 0
oddmax = 3
mx_inf = 3
```

Answers:

```
3
3
```

This verifies that odd-sized non-one groups remain separate after stabilization and must still be considered when computing `mx_inf`.
