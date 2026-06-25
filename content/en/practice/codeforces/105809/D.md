---
title: "CF 105809D - Distinct Token Arrangements"
description: "We have two kinds of tokens. The first kind consists of the labels 1, 2, ..., m. Each of these tokens is unique, so a label can appear at most once inside a single arrangement. The second kind consists of n copies of the label 0."
date: "2026-06-25T15:27:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105809
codeforces_index: "D"
codeforces_contest_name: "Code Rush 2025"
rating: 0
weight: 105809
solve_time_s: 47
verified: true
draft: false
---

[CF 105809D - Distinct Token Arrangements](https://codeforces.com/problemset/problem/105809/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two kinds of tokens.

The first kind consists of the labels `1, 2, ..., m`. Each of these tokens is unique, so a label can appear at most once inside a single arrangement.

The second kind consists of `n` copies of the label `0`. These copies are indistinguishable, so an arrangement only cares about where the value `0` appears, not which physical zero-token was used.

An arrangement is an ordered sequence whose length `L` can be any value from `1` to `n`.

For every valid length, we must count how many different sequences can be formed under the rule that each non-zero label is used at most once. The answer is required modulo `10^9 + 7`.

The constraints are small enough to suggest a combinatorial counting solution. Both `m` and `n` are at most `1000`, so an `O(nm)` algorithm performs about one million iterations, which is easily fast enough. Any brute-force generation of arrangements is impossible because the number of valid sequences grows exponentially.

A few edge cases are easy to mishandle.

Suppose `m = 1` and `n = 1`.

```
Input
1 1
```

The valid arrangements are `[0]` and `[1]`, so the answer is `2`.

A solution that only counts arrangements containing non-zero tokens would incorrectly return `1`.

Consider:

```
Input
2 2
```

Length `2` contains arrangements such as `[0,0]`, `[0,1]`, `[1,0]`, `[1,2]`, and `[2,1]`. The arrangement `[1,1]` is illegal because token `1` is unique and cannot be reused. A counting formula that treats non-zero labels as reusable would overcount.

Another important case is when the desired length exceeds the number of unique labels.

```
m = 2, L = 5
```

At most two non-zero labels can appear. Any formula that allows `k > m` distinct non-zero tokens would count impossible arrangements.

## Approaches

The most direct idea is to generate every arrangement of every allowed length and insert it into a set. This is correct because every valid sequence is explicitly constructed and counted once.

The problem is that even for moderate values, the number of arrangements becomes enormous. The search space grows exponentially with the length, making brute force completely infeasible.

Instead of generating sequences, we can count them.

Fix a length `L`. Let `k` be the number of non-zero tokens used in the arrangement.

Since the labels `1..m` are unique, exactly `k` different labels must be chosen and each chosen label appears once.

First choose which `k` positions among the `L` positions will contain non-zero labels. This contributes

$$\binom{L}{k}$$

ways.

Now fill those `k` positions with distinct labels from `1..m`.

We need an ordered selection of `k` distinct labels, which is

$$P(m,k)=m(m-1)\cdots(m-k+1)$$

ways.

Multiplying the independent choices gives

$$\binom{L}{k} P(m,k).$$

Summing over every valid value of `k` counts all arrangements of length `L`.

$$\text{count}(L)
=
\sum_{k=0}^{\min(L,m)}
\binom{L}{k} P(m,k).$$

Finally, sum over all allowed lengths:

$$\text{answer}
=
\sum_{L=1}^{n}
\sum_{k=0}^{\min(L,m)}
\binom{L}{k} P(m,k).$$

Since `m,n ≤ 1000`, we can evaluate this double sum in `O(nm)` time using precomputed factorials and inverse factorials.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(nm) | O(m+n) | Accepted |

## Algorithm Walkthrough

1. Read `m` and `n`.
2. Precompute factorials up to `max(m,n)` modulo `10^9 + 7`.
3. Precompute inverse factorials using Fermat's theorem.
4. For every length `L` from `1` to `n`, iterate `k` from `0` to `min(L,m)`.
5. Compute

$$\binom{L}{k}
=
\frac{L!}{k!(L-k)!}$$

using factorials and inverse factorials.
6. Compute

$$P(m,k)
=
\frac{m!}{(m-k)!}.$$
7. Add

$$\binom{L}{k}P(m,k)$$

to the answer modulo `10^9 + 7`.
8. Print the final sum.

### Why it works

Every arrangement of length `L` contains some number `k` of non-zero labels.

Once `k` is fixed, the arrangement is uniquely determined by two decisions: which positions contain non-zero labels, and which ordered set of distinct labels occupies those positions.

The factor `C(L,k)` counts the position choice. The factor `P(m,k)` counts the ordered assignment of distinct labels. Every valid arrangement corresponds to exactly one pair of such choices, and every such pair produces a valid arrangement.

Summing over all valid `k` values counts every arrangement exactly once. Summing over all lengths counts every valid arrangement in the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

m, n = map(int, input().split())

mx = max(m, n)

fact = [1] * (mx + 1)
for i in range(1, mx + 1):
    fact[i] = fact[i - 1] * i % MOD

inv_fact = [1] * (mx + 1)
inv_fact[mx] = pow(fact[mx], MOD - 2, MOD)

for i in range(mx, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD

def comb(a, b):
    if b < 0 or b > a:
        return 0
    return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

ans = 0
fact_m = fact[m]

for L in range(1, n + 1):
    limit = min(L, m)
    for k in range(limit + 1):
        perm = fact_m * inv_fact[m - k] % MOD
        ans = (ans + comb(L, k) * perm) % MOD

print(ans)
```

The factorial and inverse-factorial arrays allow every combination value to be computed in constant time.

The permutation count

$$P(m,k)=\frac{m!}{(m-k)!}$$

is also obtained in constant time from the same tables.

The nested loops iterate through every valid pair `(L,k)`. Since `L` never exceeds `1000`, the total number of iterations is about one million, which is comfortably within the limit.

A common mistake is forgetting the case `k = 0`. That term represents arrangements consisting entirely of zeros, such as `[0]` or `[0,0,0]`. Those arrangements are valid and must be counted.

Another common mistake is allowing `k > m`. There are only `m` distinct non-zero labels available, so such states are impossible.

## Worked Examples

### Example 1

Input:

```
2 2
```

For each length:

| L | k | C(L,k) | P(2,k) | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 2 | 2 |
| 2 | 0 | 1 | 1 | 1 |
| 2 | 1 | 2 | 2 | 4 |
| 2 | 2 | 1 | 2 | 2 |

Total:

$$1+2+1+4+2=10$$

Output:

```
10
```

This example shows how arrangements with only zeros are naturally included through the `k=0` term.

### Example 2

Input:

```
1 3
```

| L | k | C(L,k) | P(1,k) | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 0 | 1 | 1 | 1 |
| 2 | 1 | 2 | 1 | 2 |
| 3 | 0 | 1 | 1 | 1 |
| 3 | 1 | 3 | 1 | 3 |

Total:

$$1+1+1+2+1+3=9$$

Output:

```
9
```

This trace demonstrates the situation where `m` is smaller than the sequence length. We never allow `k > 1` because only one unique non-zero token exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Double sum over lengths and possible numbers of non-zero tokens |
| Space | O(max(n,m)) | Factorial and inverse-factorial tables |

With `m,n ≤ 1000`, the algorithm performs roughly one million iterations and stores only a few arrays of length about one thousand, which easily fits within typical contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    m, n = map(int, input().split())

    mx = max(m, n)

    fact = [1] * (mx + 1)
    for i in range(1, mx + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (mx + 1)
    inv_fact[mx] = pow(fact[mx], MOD - 2, MOD)

    for i in range(mx, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    ans = 0

    for L in range(1, n + 1):
        for k in range(min(L, m) + 1):
            c = fact[L] * inv_fact[k] % MOD * inv_fact[L - k] % MOD
            p = fact[m] * inv_fact[m - k] % MOD
            ans = (ans + c * p) % MOD

    return str(ans) + "\n"

# provided sample
assert run("2 2\n") == "10\n", "sample 1"

# custom cases
assert run("1 1\n") == "2\n", "minimum size"
assert run("1 2\n") == "5\n", "single unique token"
assert run("2 1\n") == "3\n", "length one"
assert run("3 2\n") == "17\n", "all transition cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `2` | Smallest valid instance |
| `1 2` | `5` | Correct handling of repeated zeros |
| `2 1` | `3` | Only length 1 exists |
| `3 2` | `17` | Multiple values of `k` contribute |

## Edge Cases

Consider:

```
1 1
```

For `L = 1`, the algorithm evaluates `k = 0` and `k = 1`.

`k = 0` contributes the arrangement `[0]`.

`k = 1` contributes the arrangement `[1]`.

The answer becomes `2`, which is correct. Any implementation that starts `k` from `1` would miss `[0]`.

Consider:

```
2 2
```

For `L = 2`, the algorithm allows only `k = 0, 1, 2`.

When `k = 2`, the contribution is

$$C(2,2)\cdot P(2,2)=1\cdot2.$$

These are exactly `[1,2]` and `[2,1]`.

The invalid sequences `[1,1]` and `[2,2]` never appear because `P(2,2)` counts ordered selections of distinct labels.

Consider:

```
2 5
```

Even though the length is five, the loop restricts

$$k \le \min(L,m)=2.$$

The algorithm never attempts to use three distinct non-zero labels, because only two exist. This correctly enforces the uniqueness constraint.
