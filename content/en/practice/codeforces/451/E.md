---
title: "CF 451E - Devu and Flowers"
description: "We have n flower boxes. From box i, we may take any number of flowers between 0 and f[i], inclusive. The colors are distinct, so a selection is completely described by how many flowers we take from each box."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 451
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 258 (Div. 2)"
rating: 2300
weight: 451
solve_time_s: 97
verified: true
draft: false
---

[CF 451E - Devu and Flowers](https://codeforces.com/problemset/problem/451/E)

**Rating:** 2300  
**Tags:** bitmasks, combinatorics, number theory  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` flower boxes. From box `i`, we may take any number of flowers between `0` and `f[i]`, inclusive. The colors are distinct, so a selection is completely described by how many flowers we take from each box.

The task is to count the number of integer vectors

$$x_1+x_2+\cdots+x_n=s$$

such that

$$0 \le x_i \le f_i$$

for every box. The answer must be reported modulo $10^9+7$.

The first thing that stands out is the size of the numbers. The number of boxes is at most $20$, which is very small. On the other hand, both $s$ and the box capacities can be enormous, reaching $10^{14}$ and $10^{12}$ respectively.

These constraints immediately rule out dynamic programming over the sum. Any solution whose complexity depends on $s$ is hopeless. Even $O(ns)$ would require processing up to $10^{14}$ states.

The small value of $n$ is the real clue. Whenever $n \le 20$, techniques involving subsets often become viable because $2^{20}\approx 10^6$, which is manageable.

There are several easy-to-miss edge cases.

Consider

```
1 0
0
```

The only valid choice is taking zero flowers. The answer is `1`. A formula that accidentally treats zero as a special invalid case would fail here.

Consider

```
1 5
3
```

No valid selection exists because the box contains only three flowers. The answer is `0`. Any unrestricted counting formula would incorrectly count one solution.

Consider

```
2 1
0 0
```

Again the answer is `0`. The upper bounds completely eliminate every candidate solution.

Another subtle case appears during inclusion-exclusion. Some subset contributions correspond to counting solutions of

$$x_1+\cdots+x_n = T$$

with $T<0$. Such terms must contribute zero. Forgetting this check causes invalid binomial coefficients to enter the calculation.

## Approaches

A brute force solution would try every possible choice of flowers from every box.

For each box $i$, there are $f_i+1$ possibilities. The total search space is

$$\prod_{i=1}^{n}(f_i+1).$$

Since $f_i$ may reach $10^{12}$, this is astronomically large. Even with tiny values such as $f_i=100$, the search space becomes $101^{20}$, which is already impossible.

The natural unrestricted version of the problem is much easier. If we ignore the upper bounds and only require

$$x_1+\cdots+x_n=s,\qquad x_i\ge 0,$$

then the classic stars-and-bars formula gives

$$\binom{s+n-1}{n-1}.$$

The only obstacle is the upper bounds $x_i\le f_i$.

Whenever we have simple lower bounds together with upper bounds, inclusion-exclusion becomes a strong candidate. The unrestricted count is easy. The solutions violating one or more upper bounds can be counted systematically.

Suppose a particular box $i$ violates its limit. Then

$$x_i\ge f_i+1.$$

Let

$$y_i=x_i-(f_i+1).$$

After this shift, $y_i\ge 0$, and the total sum decreases by $f_i+1$.

If a subset $S$ of boxes is forced to violate its limit, then after shifting every variable in $S$,

$$\sum x_i=s$$

becomes

$$\sum y_i=s-\sum_{i\in S}(f_i+1).$$

The number of nonnegative solutions is again a stars-and-bars count.

Since $n\le 20$, we can enumerate all subsets $S$. There are only $2^n$ of them.

The remaining challenge is computing binomial coefficients where the top value may be as large as $10^{14}$. Fortunately, the bottom value is always at most

$$n-1\le 19.$$

This tiny value allows direct multiplicative computation modulo $10^9+7$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O\!\left(\prod (f_i+1)\right)$ | $O(n)$ | Too slow |
| Optimal Inclusion-Exclusion | $O(n2^n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read `n`, `s`, and the capacities `f[i]`.
2. Enumerate every subset of boxes using a bitmask from `0` to `(1<<n)-1`.
3. For the current subset `mask`, compute

$$T=s-\sum_{i\in S}(f_i+1),$$

where $S$ is the set of selected bits.

This corresponds to forcing every box in $S$ to exceed its limit.

1. If $T<0$, there are no nonnegative solutions after the shift, so this subset contributes zero.
2. Otherwise count the unrestricted solutions of

$$y_1+\cdots+y_n=T.$$

Stars-and-bars gives

$$\binom{T+n-1}{n-1}.$$

1. If the subset size is even, add this quantity to the answer.
2. If the subset size is odd, subtract this quantity from the answer.

This is exactly the inclusion-exclusion principle.
3. After processing all subsets, normalize the answer modulo $10^9+7$.

### Why it works

For every subset $S$, inclusion-exclusion counts solutions where all variables in $S$ violate their upper bounds. Replacing each violating variable by

$$y_i=x_i-(f_i+1)$$

creates a bijection between such solutions and nonnegative solutions of a reduced-sum equation. Stars-and-bars counts these solutions exactly.

Inclusion-exclusion guarantees that every valid solution is counted once, while every invalid solution is canceled out. Since every subset is processed, the final sum equals the number of solutions satisfying all upper bounds simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def modinv(x):
    return pow(x, MOD - 2, MOD)

def comb_large_n_small_k(n, k):
    if n < 0 or k < 0 or k > n:
        return 0

    res = 1
    for i in range(1, k + 1):
        res = res * ((n - k + i) % MOD) % MOD
        res = res * modinv(i) % MOD
    return res

def solve():
    n, s = map(int, input().split())
    f = list(map(int, input().split()))

    ans = 0

    for mask in range(1 << n):
        t = s
        bits = 0

        for i in range(n):
            if mask & (1 << i):
                t -= f[i] + 1
                bits += 1

        if t < 0:
            continue

        ways = comb_large_n_small_k(t + n - 1, n - 1)

        if bits & 1:
            ans -= ways
        else:
            ans += ways

    print(ans % MOD)

solve()
```

The central routine is `comb_large_n_small_k`. The upper argument may be as large as $10^{14}$, but the lower argument is at most $19$. We compute

$$\binom{N}{K} = \prod_{i=1}^{K} \frac{N-K+i}{i} \pmod{MOD}$$

directly.

Because $K<MOD$, every denominator has a modular inverse.

The subset loop implements inclusion-exclusion exactly. For each selected box we subtract `f[i] + 1`, which corresponds to forcing that box to exceed its limit. If the resulting sum becomes negative, there are no solutions and the subset contributes nothing.

The parity of the subset size determines whether the contribution is added or subtracted.

## Worked Examples

### Sample 1

Input:

```
2 3
1 3
```

We need

$$x_1+x_2=3, \quad 0\le x_1\le1, \quad 0\le x_2\le3.$$

| Mask | Subset | $T$ | Contribution | Sign |
| --- | --- | --- | --- | --- |
| 00 | {} | 3 | $\binom{4}{1}=4$ | + |
| 01 | {1} | 1 | $\binom{2}{1}=2$ | - |
| 10 | {2} | -1 | 0 | - |
| 11 | {1,2} | -3 | 0 | + |

Final value:

$$4-2=2.$$

Output:

```
2
```

This trace shows inclusion-exclusion removing the two unrestricted solutions where the first box exceeds its capacity.

### Sample 2

Input:

```
2 4
2 2
```

| Mask | Subset | $T$ | Contribution | Sign |
| --- | --- | --- | --- | --- |
| 00 | {} | 4 | $\binom{5}{1}=5$ | + |
| 01 | {1} | 1 | $\binom{2}{1}=2$ | - |
| 10 | {2} | 1 | $\binom{2}{1}=2$ | - |
| 11 | {1,2} | -2 | 0 | + |

Final value:

$$5-2-2=1.$$

Output:

```
1
```

The only surviving solution is $(2,2)$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n2^n)$ | Each subset examines up to $n$ boxes |
| Space | $O(1)$ | Only a few variables besides the input array |

Since $n\le 20$, the algorithm processes at most

$$20\cdot 2^{20}\approx 2\times10^7$$

simple operations, which fits comfortably within the limits. The huge values of $s$ and $f_i$ never appear in loops.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    def comb_large_n_small_k(n, k):
        if n < 0 or k < 0 or k > n:
            return 0

        res = 1
        for i in range(1, k + 1):
            res = res * ((n - k + i) % MOD) % MOD
            res = res * modinv(i) % MOD
        return res

    n, s = map(int, input().split())
    f = list(map(int, input().split())

    ans = 0

    for mask in range(1 << n):
        t = s
        bits = 0

        for i in range(n):
            if mask & (1 << i):
                t -= f[i] + 1
                bits += 1

        if t >= 0:
            ways = comb_large_n_small_k(t + n - 1, n - 1)
            if bits & 1:
                ans -= ways
            else:
                ans += ways

    return str(ans % MOD)

# provided sample
assert run("2 3\n1 3\n") == "2", "sample 1"

# custom cases
assert run("1 0\n0\n") == "1", "minimum input"
assert run("1 5\n3\n") == "0", "sum exceeds capacity"
assert run("2 4\n2 2\n") == "1", "unique solution"
assert run("3 0\n0 0 0\n") == "1", "all zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 0` | `1` | Empty selection is counted |
| `1 5 / 3` | `0` | Impossible target sum |
| `2 4 / 2 2` | `1` | Exact boundary solution |
| `3 0 / 0 0 0` | `1` | Multiple zero-capacity boxes |

## Edge Cases

Consider

```
1 0
0
```

The empty subset gives

$$\binom{0}{0}=1.$$

The violating subset produces a negative reduced sum and contributes zero. The final answer is `1`, representing the unique choice of taking no flowers.

Consider

```
1 5
3
```

The empty subset contributes

$$\binom{5}{0}=1.$$

The violating subset contributes

$$\binom{1}{0}=1.$$

Inclusion-exclusion yields

$$1-1=0.$$

Every unrestricted solution violates the upper bound, so cancellation is complete.

Consider

```
2 1
0 0
```

The empty subset contributes

$$\binom{2}{1}=2.$$

Each single-box violating subset contributes $1$, and the double-box subset contributes $0$. The result is

$$2-1-1=0.$$

No valid selection exists because neither box contains any flowers.

The negative-sum case is handled automatically. Whenever

$$s-\sum_{i\in S}(f_i+1)<0,$$

there cannot be any nonnegative solution after the variable shift, so the contribution is zero. This prevents invalid binomial evaluations and keeps inclusion-exclusion mathematically correct.
