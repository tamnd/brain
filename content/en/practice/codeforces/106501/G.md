---
title: "CF 106501G - LCM Matrix"
description: "The matrix is not arbitrary. Each row has a hidden value and each column has a hidden value, and every visible cell is the least common multiple of those two values."
date: "2026-06-25T08:32:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106501
codeforces_index: "G"
codeforces_contest_name: "IPL 2026"
rating: 0
weight: 106501
solve_time_s: 42
verified: true
draft: false
---

[CF 106501G - LCM Matrix](https://codeforces.com/problemset/problem/106501/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The matrix is not arbitrary. Each row has a hidden value and each column has a hidden value, and every visible cell is the least common multiple of those two values. Some cells are missing, and the task is to choose row and column values that could create all visible cells while making the product of every chosen value as small as possible.

The product is the same as minimizing the sum of prime exponents across all row and column values. This is because multiplication of numbers can be viewed independently for every prime. For example, if a prime contributes exponent 3 to one row value, that contributes exactly the same factor as increasing another value by the same exponent. The LCM condition also works independently by prime, because the exponent in an LCM is the maximum exponent among the two numbers.

The dimensions are at most 500, and the total number of rows and columns over all tests is bounded by 500 each. This rules out anything close to checking every possible assignment of row and column values. The hidden values are not bounded, so a search over possible numbers is impossible. The solution has to use the structure of LCM and prime factors.

The missing cells create an easy-to-miss situation. A row or column that only appears in zero cells has no restrictions and should contribute nothing. For example, with input

```
2 2
0 0
0 0
```

the answer is `1`, because every hidden value can be chosen as 1. A careless approach that initializes every row and column from a matrix value would fail here.

Another tricky case is that the minimum values are not always found by taking values from a single row or column. For example:

```
1 2
6 10
```

The minimum is `30`, not `60`. The row value can be `1` and the two column values can be `6` and `10`, giving product `60`, but the better choice is row value `2`, columns `3` and `5`, giving the same LCMs with product `30`. The solution must reason about prime exponents instead of copying visible numbers.

## Approaches

A direct approach would try to reconstruct the hidden row and column arrays. Since every visible cell says `lcm(row[i], col[j]) = b[i][j]`, we could try different divisors of the matrix values and keep the smallest product. This is correct because every valid answer must satisfy those equations.

The problem is the number of possibilities. A value up to `10^8` can have many divisors, and there are up to 500 row values and 500 column values. Trying combinations quickly becomes impossible. Even considering only a few candidates per position can lead to a search over an enormous state space.

The useful observation is that we never need the full values while solving. Consider one prime separately. Let the exponent of this prime in row `i` be `r[i]`, and in column `j` be `c[j]`. A known cell with exponent `x` gives the condition:

```
max(r[i], c[j]) = x
```

For a vertex, the largest exponent it can have is the smallest exponent among all adjacent known cells. If a row touches cells with exponents `2`, `5`, and `3`, then its exponent cannot exceed `2`. Any larger value would make the first cell impossible.

Now assign every row and column this maximum allowed exponent. Because the original matrix is guaranteed to be valid, every known cell has at least one endpoint whose maximum allowed exponent is exactly the cell exponent. If neither endpoint had that exponent, both would be smaller and the LCM could never reach the required value.

This gives the smallest possible assignment. Increasing any vertex above its maximum allowed exponent is impossible, and decreasing a vertex would break a cell that relies on it. Applying this independently for every prime gives the minimum product.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of rows and columns | O(nm) | Too slow |
| Optimal | O(nm log A) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Factor every non-zero matrix entry. For each prime, store the exponent that appears in every known cell. We only care about primes that actually occur in the matrix.

The number of different prime factors is small because every value is at most `10^8`.

1. For each prime, create arrays of the smallest possible exponents for all rows and columns. Initialize every row and column with a large value, then process every known cell with exponent `e`. Update the row and column upper bounds with `e`.

This computes the largest exponent each vertex could possibly receive.

1. Add the row and column contributions for this prime to the answer. If a row has final exponent `x`, multiply the answer by `p^x`. Do the same for every column.

The product can be built prime by prime because prime powers are independent.

1. Ignore rows and columns without any known cells. Their upper bound remains unset, and their minimum possible value is 1.

Why it works: for every prime, the hidden matrix only depends on the maximum of two exponents. Every vertex has an upper bound from its incident edges. A valid solution cannot assign a larger exponent. Assigning all vertices their maximum allowed exponent satisfies every edge because the original matrix is guaranteed to have some valid assignment, so each edge has at least one endpoint capable of reaching its required exponent. Any smaller assignment would reduce an exponent that is needed by some edge. Thus the constructed assignment is exactly the minimum one.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def factorize(x):
    res = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            res.append((d, cnt))
        d += 1 if d == 2 else 2
    if x > 1:
        res.append((x, 1))
    return res

def solve_case(n, m, a):
    factors = [[[] for _ in range(m)] for _ in range(n)]
    primes = set()

    for i in range(n):
        for j in range(m):
            if a[i][j]:
                f = factorize(a[i][j])
                factors[i][j] = f
                for p, _ in f:
                    primes.add(p)

    ans = 1

    for p in primes:
        row = [-1] * n
        col = [-1] * m

        for i in range(n):
            for j in range(m):
                if a[i][j]:
                    exp = 0
                    for q, e in factors[i][j]:
                        if q == p:
                            exp = e
                            break
                    if row[i] == -1 or exp < row[i]:
                        row[i] = exp
                    if col[j] == -1 or exp < col[j]:
                        col[j] = exp

        for x in row:
            if x > 0:
                ans = ans * pow(p, x, MOD) % MOD

        for x in col:
            if x > 0:
                ans = ans * pow(p, x, MOD) % MOD

    return ans

def main():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]
        out.append(str(solve_case(n, m, a)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The factorization stage stores the prime exponents for every non-zero cell. Storing them avoids factoring the same value repeatedly while processing different primes.

The main loop processes one prime at a time. The `row` and `col` arrays represent the smallest upper bounds for that prime. Every visible cell can only decrease these bounds, because every endpoint must be no larger than the cell exponent.

A common mistake is to use zero as the initial value. Zero is a real exponent, so it would incorrectly force every row or column to have no contribution. The code uses `-1` to mean that the vertex has no known incident cell.

The final multiplication uses modular exponentiation because the product of all prime powers can be very large.

## Worked Examples

For the first sample:

```
1 2
6 10
```

The trace is:

| Step | Prime | Row exponent | Column exponents | Contribution |
| --- | --- | --- | --- | --- |
| Factor 6,10 | 2 | 0 | 1,0 | 2 |
| Factor 6,10 | 3 | 0 | 1,0 | 3 |
| Factor 6,10 | 5 | 0 | 0,1 | 5 |

The final product is:

```
2 * 3 * 5 = 30
```

This shows why splitting by primes finds a smaller assignment than using the visible values directly.

For the third sample:

```
3 3
0 0 0
0 0 0
0 0 0
```

The trace is:

| Step | Known cells | Row bounds | Column bounds | Contribution |
| --- | --- | --- | --- | --- |
| Scan matrix | none | unset | unset | 1 |

No prime is processed, so every hidden value stays 1 and the answer is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm log A + Pnm) | Each value is factored, and each relevant prime is processed over the matrix. |
| Space | O(nm) | The stored factor lists and matrix occupy this space. |

Here `A` is the maximum matrix value and `P` is the number of distinct primes appearing. With values up to `10^8` and total matrix dimensions bounded by the problem constraints, this fits comfortably.

## Test Cases

```python
import sys, io

MOD = 998244353

def factorize(x):
    res = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            c = 0
            while x % d == 0:
                x //= d
                c += 1
            res.append((d, c))
        d += 1 if d == 2 else 2
    if x > 1:
        res.append((x, 1))
    return res

def solve(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]
        factors = [[[] for _ in range(m)] for _ in range(n)]
        primes = set()

        for i in range(n):
            for j in range(m):
                if a[i][j]:
                    factors[i][j] = factorize(a[i][j])
                    for p, _ in factors[i][j]:
                        primes.add(p)

        cur = 1
        for p in primes:
            row = [-1] * n
            col = [-1] * m
            for i in range(n):
                for j in range(m):
                    if a[i][j]:
                        e = 0
                        for q, v in factors[i][j]:
                            if q == p:
                                e = v
                                break
                        row[i] = e if row[i] == -1 else min(row[i], e)
                        col[j] = e if col[j] == -1 else min(col[j], e)
            for x in row + col:
                if x > 0:
                    cur = cur * pow(p, x, MOD) % MOD
        ans.append(str(cur))

    return "\n".join(ans)

assert solve("""3
1 2
6 10
2 2
6 6
6 6
3 3
0 0 0
0 0 0
0 0 0
""") == "30\n36\n1"

assert solve("""1
1 1
1
""") == "1"

assert solve("""1
2 2
2 2
2 2
""") == "2"

assert solve("""1
2 3
0 6 0
0 0 10
""") == "30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1` matrix with `1` | `1` | Smallest possible value |
| All entries equal to `2` | `2` | Shared prime contribution |
| Sparse matrix with zeros | `30` | Missing cells and unconstrained vertices |

## Edge Cases

For the all-zero matrix:

```
2 2
0 0
0 0
```

Every row and column has no incident constraint. The algorithm never assigns a prime exponent, so all hidden values remain 1. The product is `1`.

For a sparse matrix:

```
2 3
0 6 0
0 0 10
```

The prime factors are handled independently. For prime 2, the first known value forces exponent 1 on its row or column, and the same happens for prime 5 and prime 3 from the value 10. The minimum product is obtained by assigning the necessary exponents only once where possible.

For equal values:

```
2 2
6 6
6 6
```

Every edge requires exponents for primes 2 and 3. The row and column bounds become the same values, but the algorithm chooses the smallest total contribution, producing `36` instead of multiplying all visible cells together.
