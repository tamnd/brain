---
title: "CF 1895F - Fancy Arrays"
description: "We are counting arrays of length n consisting of non-negative integers. Adjacent values may move by at most k in either direction. An array is considered fancy if at least one element belongs to the interval $$[x, x+k-1].$$ The task is to count all such arrays modulo $10^9+7$."
date: "2026-06-08T21:46:31+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "matrices"]
categories: ["algorithms"]
codeforces_contest: 1895
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 157 (Rated for Div. 2)"
rating: 2600
weight: 1895
solve_time_s: 139
verified: true
draft: false
---

[CF 1895F - Fancy Arrays](https://codeforces.com/problemset/problem/1895/F)

**Rating:** 2600  
**Tags:** combinatorics, dp, math, matrices  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are counting arrays of length `n` consisting of non-negative integers. Adjacent values may move by at most `k` in either direction.

An array is considered fancy if at least one element belongs to the interval

$$[x, x+k-1].$$

The task is to count all such arrays modulo $10^9+7$.

The first thing that looks unusual is that array values are unbounded above. A direct dynamic programming over values is impossible because values can be arbitrarily large.

The constraints explain where the real structure lies. Both `n` and `k` can reach $10^9$, so anything linear in either parameter is immediately impossible. The only small parameter is `x`, which is at most `40`. Any accepted solution must reduce the problem to a state space depending on `x` and then use matrix exponentiation to handle the huge length.

A subtle point is that the set of all arrays satisfying only the adjacency condition is infinite, because values can be shifted upward without bound. The requirement that some element lies in $[x,x+k-1]$ is what makes the answer finite.

Another easy mistake is to try counting arrays that contain a value from the target interval directly. The interval may be visited multiple times, so inclusion-exclusion over positions becomes messy.

Consider:

```
n = 2, x = 1, k = 1
```

The valid arrays are:

```
[0,1]
[1,0]
[1,1]
[1,2]
[2,1]
```

There are 5 of them. Counting "first visit" positions separately would double-count several arrays.

A second trap appears when `x = 0`.

```
n = 1, x = 0, k = 3
```

Every value in `{0,1,2}` already satisfies the requirement, so the answer is `3`.

Any formula that subtracts arrays entirely below `x` must correctly handle the fact that there are no values below `0`.

## Approaches

Let us first imagine a brute-force solution.

Suppose values were restricted to some finite range. We could enumerate every array and check whether adjacent differences stay within `k` and whether at least one element belongs to the target interval. This is obviously correct, but even for tiny ranges the number of arrays grows exponentially as $M^n$. With $n$ up to $10^9$, such an approach is hopeless.

The key observation comes from looking at the minimum value of the array.

Take any array satisfying the adjacency condition. Let its minimum value be `m`.

If we subtract `m` from every element, all differences remain unchanged. The shifted array has minimum `0`.

Now look at the sequence of increments between consecutive elements. Each step can be any integer in `[-k,k]`, giving exactly `2k+1` possibilities.

Once the minimum value `m` and the step sequence are fixed, the whole array is uniquely determined.

This suggests counting arrays by their minimum.

An array is fancy iff its minimum is at most $x+k-1$, and not all elements are strictly below `x`.

Indeed, if the minimum exceeds $x+k-1$, then every element exceeds $x+k-1$, so the target interval is never reached.

Conversely, if the minimum is at most $x+k-1$, then some element equals the minimum and therefore lies in $[0,x+k-1]$. The only way to miss the target interval is when every element is actually below `x`.

This transforms the answer into

$$(\text{arrays with minimum } \le x+k-1)
-
(\text{arrays entirely in } [0,x-1]).$$

The first quantity becomes extremely simple.

Choose the minimum value. It can be any integer from `0` to `x+k-1`, giving `x+k` choices.

After fixing the minimum, each of the `n-1` differences can be chosen independently from `[-k,k]`, giving

$$(2k+1)^{n-1}$$

possibilities.

Hence

$$A=(x+k)(2k+1)^{n-1}.$$

The second quantity only involves values in `[0,x-1]`. Since `x ≤ 40`, we can perform DP on these states.

Let

$$dp_i[j]$$

be the number of length-`i` arrays ending at value `j`, where all values stay inside `[0,x-1]`.

The transition is

$$dp_i[j]
=
\sum_{|j-t|\le k} dp_{i-1}[t].$$

This is a linear transformation on at most 40 states, so matrix exponentiation computes the result for huge `n`.

The answer is

$$(x+k)(2k+1)^{n-1}
-
\text{count\_below\_x}.$$

This yields an $O(x^3\log n)$ solution.

The underlying idea is exactly the one used in the official solutions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(x^3\log n)$ | $O(x^2)$ | Accepted |

## Algorithm Walkthrough

1. Compute

$$T=(x+k)(2k+1)^{n-1}.$$

This counts all arrays whose minimum value belongs to `[0, x+k-1]`.
2. Count arrays whose every value lies in `[0,x-1]`.

Let the states be the values `0,1,...,x-1`.
3. Build an `x × x` transition matrix `M`.

`M[i][j] = 1` if `|i-j| ≤ k`, otherwise `0`.

This exactly matches the adjacency constraint.
4. Create the initial row vector

$$V=[1,1,\dots,1].$$

Every value in `[0,x-1]` may appear as the first element.
5. Compute

$$V' = V \cdot M^{\,n-1}.$$

Matrix exponentiation reduces the huge exponent to $O(\log n)$.
6. Sum all entries of `V'`.

This is the number of arrays whose values never leave `[0,x-1]`.
7. Subtract that quantity from `T`.
8. Output the result modulo $10^9+7$.

### Why it works

Every array satisfying the adjacency condition has a unique minimum value.

Fixing the minimum and the sequence of consecutive differences uniquely determines the whole array. Since every difference has exactly `2k+1` possibilities, the number of arrays with a fixed minimum equals $(2k+1)^{n-1}$.

The minimum can take any value from `0` to `x+k-1`, yielding $(x+k)(2k+1)^{n-1}$ arrays whose minimum does not exceed $x+k-1$.

Among them, the only arrays that fail the fancy condition are those whose values are all strictly below `x`. Those arrays are counted by the matrix DP.

The two sets differ exactly by the set of fancy arrays, so the subtraction produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def mat_mul(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)

    C = [[0] * m for _ in range(n)]

    for i in range(n):
        for k in range(p):
            if A[i][k] == 0:
                continue
            aik = A[i][k]
            for j in range(m):
                C[i][j] = (C[i][j] + aik * B[k][j]) % MOD

    return C

def mat_pow(M, e):
    n = len(M)

    R = [[0] * n for _ in range(n)]
    for i in range(n):
        R[i][i] = 1

    while e:
        if e & 1:
            R = mat_mul(R, M)
        M = mat_mul(M, M)
        e >>= 1

    return R

def solve_case(n, x, k):
    total = (x + k) % MOD
    total = total * pow(2 * k + 1, n - 1, MOD) % MOD

    if x == 0:
        below = 0
    else:
        M = [[0] * x for _ in range(x)]

        for i in range(x):
            for j in range(x):
                if abs(i - j) <= k:
                    M[i][j] = 1

        P = mat_pow(M, n - 1)

        vec = [[1] * x]
        res = mat_mul(vec, P)

        below = sum(res[0]) % MOD

    return (total - below) % MOD

def main():
    t = int(input())
    ans = []

    for _ in range(t):
        n, x, k = map(int, input().split())
        ans.append(str(solve_case(n, x, k)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()
```

The computation splits naturally into two independent pieces.

The first piece counts arrays whose minimum is at most `x+k-1`. That is just a modular exponentiation.

The second piece counts arrays entirely below `x`. Since `x ≤ 40`, the state space is tiny. The transition matrix contains exactly the valid moves between values.

The initial vector is all ones because any value below `x` can be chosen as the first element. Multiplying by $M^{n-1}$ applies the transition `n-1` times.

One subtle boundary case is `x = 0`. Then there are no states at all in the "below x" DP. The count of arrays entirely below `x` is simply zero.

Another detail is that `n` can equal `1`. Matrix exponentiation with exponent `0` correctly returns the identity matrix, so the code naturally handles this case.

## Worked Examples

### Example 1

Input:

```
n = 1, x = 4, k = 25
```

First compute the large count.

| Quantity | Value |
| --- | --- |
| x+k | 29 |
| (2k+1)^(n-1) | 1 |
| total | 29 |

Now count arrays entirely below `4`.

| Value | Possible first element? |
| --- | --- |
| 0 | Yes |
| 1 | Yes |
| 2 | Yes |
| 3 | Yes |

So:

| Quantity | Value |
| --- | --- |
| below | 4 |
| answer | 29 - 4 = 25 |

Output:

```
25
```

This example shows why the subtraction is necessary. The first formula counts all minima from `0` to `28`, but minima `0..3` correspond to arrays that never touch the target interval.

### Example 2

Input:

```
n = 3, x = 0, k = 1
```

| Quantity | Value |
| --- | --- |
| x+k | 1 |
| (2k+1)^(n-1) | 3^2 = 9 |
| total | 9 |

Since `x=0`, there are no values below `x`.

| Quantity | Value |
| --- | --- |
| below | 0 |
| answer | 9 |

Output:

```
9
```

This demonstrates the special case where every valid minimum already lies inside the target interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(x^3 \log n)$ | Matrix exponentiation on an `x × x` matrix |
| Space | $O(x^2)$ | Storing matrices |

Since `x ≤ 40`, the matrix dimension never exceeds 40. Even $40^3$ matrix multiplications are small, and only $O(\log n)$ of them are needed. The solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    MOD = 1000000007

    def mat_mul(A, B):
        n = len(A)
        m = len(B[0])
        p = len(B)

        C = [[0] * m for _ in range(n)]

        for i in range(n):
            for k in range(p):
                if A[i][k] == 0:
                    continue
                for j in range(m):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
        return C

    def mat_pow(M, e):
        n = len(M)
        R = [[0] * n for _ in range(n)]
        for i in range(n):
            R[i][i] = 1

        while e:
            if e & 1:
                R = mat_mul(R, M)
            M = mat_mul(M, M)
            e >>= 1
        return R

    data = io.StringIO(inp)
    t = int(data.readline())
    out = []

    for _ in range(t):
        n, x, k = map(int, data.readline().split())

        total = (x + k) % MOD
        total = total * pow(2 * k + 1, n - 1, MOD) % MOD

        if x == 0:
            below = 0
        else:
            M = [[0] * x for _ in range(x)]
            for i in range(x):
                for j in range(x):
                    if abs(i - j) <= k:
                        M[i][j] = 1

            P = mat_pow(M, n - 1)
            res = mat_mul([[1] * x], P)
            below = sum(res[0]) % MOD

        out.append(str((total - below) % MOD))

    return "\n".join(out)

# provided sample
assert run(
"""4
3 0 1
1 4 25
4 7 2
1000000000 40 1000000000
"""
) == """9
25
582
514035484"""

# minimum size
assert run("1\n1 0 1\n") == "1"

# x = 0 boundary
assert run("1\n1 0 3\n") == "3"

# single-element interval starting above zero
assert run("1\n1 1 1\n") == "1"

# all values below x excluded
assert run("1\n1 2 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 1` | `1` | Smallest possible instance |
| `1 0 3` | `3` | `x=0` special handling |
| `1 1 1` | `1` | Single target value |
| `1 2 1` | `1` | Correct subtraction of values below `x` |

## Edge Cases

Consider:

```
1
1 0 3
```

The target interval is `[0,2]`. Every valid array has one element, and that element must be one of `0,1,2`. The formula gives

$$(0+3)\cdot 1 = 3.$$

There are no arrays entirely below `0`, so the subtraction term is zero. The algorithm returns `3`.

Now consider:

```
1
1 4 25
```

The first formula counts all minima from `0` through `28`, giving `29`. Among these, values `0,1,2,3` never reach the target interval `[4,28]`. The matrix DP counts exactly those four arrays, and the answer becomes `25`.

Finally, consider:

```
1
2 1 1
```

The interval is `[1,1]`. The formula gives

$$2 \cdot 3 = 6.$$

The DP below `x` has only state `0`, and there is exactly one length-2 array staying there, namely `[0,0]`. Subtracting it yields `5`, which matches direct enumeration. This confirms that the matrix DP removes precisely the non-fancy arrays and nothing else.
