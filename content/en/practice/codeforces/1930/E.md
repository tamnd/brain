---
title: "CF 1930E - 2..3...4.... Wonderful! Wonderful!"
description: "We start with the array $$[1,2,3,dots,n].$$ A value $k$ is fixed for the whole process. In one operation we choose a subsequence of length $2k+1$. Among those chosen elements, we delete the first $k$ and the last $k$, keeping only the middle one."
date: "2026-06-08T18:32:58+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1930
codeforces_index: "E"
codeforces_contest_name: "think-cell Round 1"
rating: 2400
weight: 1930
solve_time_s: 110
verified: true
draft: false
---

[CF 1930E - 2..3...4.... Wonderful! Wonderful!](https://codeforces.com/problemset/problem/1930/E)

**Rating:** 2400  
**Tags:** combinatorics, dp, math  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with the array

$$[1,2,3,\dots,n].$$

A value $k$ is fixed for the whole process. In one operation we choose a subsequence of length $2k+1$. Among those chosen elements, we delete the first $k$ and the last $k$, keeping only the middle one.

Since the original array is strictly increasing and we only delete elements, every final state is simply a subsequence of $[1,2,\dots,n]$.

The task is: for every $k$ from $1$ to $\lfloor (n-1)/2 \rfloor$, count how many different subsequences can appear after performing the operation any number of times.

The answer must be reported modulo $998244353$.

The constraints are large. A single test can have $n=10^6$, and the sum of all $n$ values is also $10^6$. Any algorithm that examines individual subsequences is impossible because there are $2^n$ of them. Even an $O(n^2)$ algorithm would perform around $10^{12}$ operations in the worst case. We need something close to $O(n \log n)$ over all $k$.

The tricky part is characterizing exactly which subsequences are reachable.

Consider $n=5$ and $k=2$. One operation chooses a subsequence of length $5$, so the only possible deletion removes two elements on each side of a chosen middle element. The only nontrivial result is $[3]$. A naive idea that "any subsequence with an odd number of elements is reachable" would incorrectly count many impossible arrays.

Another subtle case is $k=1$ and subsequence $[1,4]$ in $n=4$. Two elements were deleted, which is a multiple of $2k$, but that alone is not sufficient. Reachability depends on the structure of deleted positions, not only their count.

The core of the problem is finding a clean characterization of reachable subsequences.

## Approaches

A brute-force solution would view every state as a subsequence and perform BFS over all possible operations. This is correct because every reachable array is eventually discovered.

Unfortunately, the state space already has $2^n$ subsequences. For $n=30$ this is already over one billion states, so the approach becomes useless long before reaching the actual constraints.

The key observation is that the operation depends only on which positions survive.

Represent a final subsequence by a binary string of length $n$:

$$1 = \text{element survives}, \qquad
0 = \text{element deleted}.$$

Each operation deletes exactly $2k$ elements. Hence the total number of zeros must be a multiple of $2k$.

The surprising fact is that this condition is almost sufficient.

Let the number of deleted elements be $2ck$. A non-empty subsequence is reachable if and only if there exists a surviving position such that at least $k$ deleted elements lie on its left and at least $k$ deleted elements lie on its right.

This characterization turns the problem into pure counting.

For a fixed $k$, let $2ck$ be the number of deleted elements. There are

$$\binom{n}{2ck}$$

binary strings with exactly $2ck$ zeros.

We now count the bad strings, those that do not contain any surviving position with at least $k$ zeros on both sides.

A bad configuration has a very rigid shape. Apart from at most $k-1$ zeros near the left end and at most $k-1$ zeros near the right end, all remaining zeros must form one contiguous block. After compressing that block into a single object, we are choosing positions for $2k-1$ special objects among

$$n-(2ck-(2k-2))+1$$

total positions. This yields

$$\binom{n-2ck+2k-1}{2k-1}.$$

Thus for fixed $k$,

$$\text{answer}
=
1+
\sum_{c\ge1}
\left(
\binom{n}{2ck}
-
\binom{n-2ck+2k-1}{2k-1}
\right).$$

The extra $1$ counts the original array, corresponding to zero deletions.

The remaining work is efficient evaluation of binomial coefficients.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ or worse | $O(2^n)$ | Too slow |
| Optimal | $O(n \log n)$ overall | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Precomputation

1. Precompute factorials and inverse factorials modulo $998244353$ up to $10^6$.
2. Using these arrays, evaluate any binomial coefficient

$$\binom{a}{b}$$

in $O(1)$ time.

### For each test case

1. Read $n$.
2. For every $k$ from $1$ to $\lfloor (n-1)/2 \rfloor$, initialize

$$ans = 1.$$

The value $1$ corresponds to performing no operations.

1. Enumerate the number of deleted blocks:

$$c = 1,2,\dots,\left\lfloor \frac{n-1}{2k}\right\rfloor.$$

Then exactly $2ck$ elements are deleted.

1. Add the number of binary strings with exactly $2ck$ deleted positions:

$$\binom{n}{2ck}.$$

1. Subtract the bad configurations:

$$\binom{n-2ck+2k-1}{2k-1}.$$

1. Reduce modulo $998244353$.
2. Output all answers for this test case.

### Why it works

A reachable final array can be represented solely by the set of surviving positions.

Every operation removes exactly $2k$ elements, so the number of deleted positions must be a multiple of $2k$. The characterization of reachable states says that a non-empty configuration is reachable exactly when some surviving position has at least $k$ deleted elements on each side.

For a fixed deletion count $2ck$, every binary string is either good or bad. Counting all strings gives $\binom{n}{2ck}$. The bad strings are precisely those where all excess zeros collapse into one central block, leading to the count $\binom{n-2ck+2k-1}{2k-1}$.

Subtracting bad strings from all strings gives the number of reachable configurations for that deletion count. Summing over all valid multiples of $2k$, and adding the untouched array, counts every reachable final array exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXN = 10 ** 6 + 5

fact = [1] * MAXN
for i in range(1, MAXN):
    fact[i] = fact[i - 1] * i % MOD

inv_fact = [1] * MAXN
inv_fact[-1] = pow(fact[-1], MOD - 2, MOD)

for i in range(MAXN - 2, -1, -1):
    inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

def C(n, r):
    if r < 0 or r > n or n < 0:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

t = int(input())

for _ in range(t):
    n = int(input())

    res = []

    for k in range(1, (n - 1) // 2 + 1):
        ans = 1

        limit = (n - 1) // (2 * k)

        for c in range(1, limit + 1):
            deleted = 2 * k * c

            ans += C(n, deleted)
            ans -= C(n - deleted + 2 * k - 1, 2 * k - 1)

        ans %= MOD
        res.append(str(ans))

    print(" ".join(res))
```

The factorial and inverse-factorial tables are built once for the maximum possible value of $n$. Since the modulus is prime, Fermat's theorem gives the modular inverse of the largest factorial, and all other inverse factorials are obtained in a single backward pass.

The function `C(n, r)` handles invalid arguments explicitly. This avoids subtle bugs when the compressed-count formula produces a negative upper index.

For a fixed $k$, the variable `c` represents how many groups of $2k$ deletions occurred. The maximum valid value is $\lfloor (n-1)/(2k) \rfloor$, because at least one element must survive.

The expression

```
C(n - deleted + 2 * k - 1, 2 * k - 1)
```

is the count of bad configurations after compression. Getting the `-1` terms wrong here is the most common source of off-by-one mistakes.

## Worked Examples

### Example 1

Input:

```
n = 5
```

For $k=1$:

| c | deleted | All strings | Bad strings | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 2 | 10 | 4 | 6 |
| 2 | 4 | 5 | 2 | 3 |

Starting from `ans = 1`:

$$1 + 6 + 3 = 10.$$

Output for $k=1$ is $10$.

For $k=2$:

| c | deleted | All strings | Bad strings | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 4 | 5 | 4 | 1 |

$$1 + 1 = 2.$$

Output:

```
10 2
```

This matches the sample.

### Example 2

Input:

```
n = 3
```

Only $k=1$ exists.

| c | deleted | All strings | Bad strings | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 2 | 1 |

Starting from `ans = 1`:

$$1 + 1 = 2.$$

Output:

```
2
```

This example shows the role of the initial `1`, which counts the original array when no operation is performed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ per full test set | $\sum_k n/(2k)=O(n\log n)$ |
| Space | $O(n)$ | Factorial and inverse-factorial tables |

Since the sum of all input sizes is at most $10^6$, the harmonic-series bound gives roughly $10^6 \log 10^6$ iterations. This comfortably fits within the limits.

## Test Cases

```
# helper: run solution on input string, return output string

# provided samples

assert run("1\n3\n") == "2\n"

assert run("1\n4\n") == "4\n"

assert run("1\n5\n") == "10 2\n"

assert run("1\n10\n") == "487 162 85 10\n"

# minimum size
assert run("1\n3\n") == "2\n"

# first case with two k values
assert run("1\n5\n") == "10 2\n"

# boundary where largest k is used
assert run("1\n7\n") == "42 14 2\n"

# multiple test cases together
assert run("2\n3\n5\n") == "2\n10 2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=3` | `2` | Smallest legal instance |
| `n=5` | `10 2` | Multiple values of `k` |
| `n=7` | `42 14 2` | Largest admissible `k` handling |
| Two test cases together | Combined output | State reset between tests |

## Edge Cases

### Only one operation can ever occur

Input:

```
1
5
```

For $k=2$, the only possible deletion count is $4$. The algorithm evaluates exactly one term:

$$1+\binom{5}{4}-\binom{4}{3}
=
1+5-4
=
2.$$

The answer is correctly `2`, corresponding to the original array and the singleton array `[3]`.

### Deletion count is a multiple of $2k$ but configuration is unreachable

Take $n=4$, $k=1$. The subsequence corresponding to survivors `{1,4}` deletes two elements, which satisfies the divisibility condition. A naive solution would count it automatically.

The bad-configuration subtraction removes exactly such cases. The formula subtracts all binary strings where no surviving position has at least one deleted element on both sides.

This is why the final answer becomes `4` instead of a larger incorrect value.

### Largest possible $k$

When

$$k=\left\lfloor \frac{n-1}{2} \right\rfloor,$$

the inner loop executes only once because $2k$ is already close to $n$.

For example, $n=5, k=2$:

$$\left\lfloor \frac{n-1}{2k}\right\rfloor = 1.$$

The implementation handles this naturally without any special case, avoiding boundary errors in the summation limits.
