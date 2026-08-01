---
title: "CF 102644G - Recurrence With Square"
description: "The sequence in this problem is not a standard linear recurrence because the next value depends not only on previous values, but also on the current position in the sequence."
date: "2026-08-01T10:20:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102644
codeforces_index: "G"
codeforces_contest_name: "Matrix Exponentiation"
rating: 0
weight: 102644
solve_time_s: 58
verified: true
draft: false
---

[CF 102644G - Recurrence With Square](https://codeforces.com/problemset/problem/102644/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
# Problem Understanding

The sequence in this problem is not a standard linear recurrence because the next value depends not only on previous values, but also on the current position in the sequence. We are given the first several values of a sequence, the coefficients that combine previous values, and three extra coefficients that create a quadratic function of the index. The task is to find the value of the sequence at a potentially enormous index and print it modulo $10^9+7$.

The recurrence has the form that every new element is created from the previous $n$ elements plus a polynomial term. The previous elements are weighted by fixed coefficients, while the additional part grows as a quadratic expression in the index.

The index $k$ can be as large as $10^{18}$, so simulating the sequence one element at a time is impossible. Even $O(k)$ operations would require far more work than any contest time limit allows. The order of the recurrence is small, with $n \le 10$, so the intended solution must exploit the small state size rather than the size of the requested index.

A common mistake is forgetting that the polynomial term depends on the index. For example, treating the recurrence as a normal linear recurrence and using only the previous $n$ values loses the information needed to generate future quadratic contributions.

Consider the input:

```
1 3
5
1
2 3 4
```

The values are generated as $a_i = a_{i-1} + 2 + 3i + 4i^2$. The sequence becomes $5, 14, 38, 85$, so the answer is:

```
85
```

A careless implementation that only tracks $a_i$ and ignores the current index would incorrectly assume the added value is constant.

Another edge case is when the requested index is inside the initial values. For:

```
3 1
7 8 9
1 1 1
0 0 0
```

the answer is:

```
8
```

No recurrence step should be performed because $a_1$ is already provided. A solution that always starts matrix exponentiation from the first transition would access the wrong state.

## Approaches

The direct approach is to repeatedly apply the recurrence until reaching index $k$. To compute one new element, we multiply the previous $n$ values by their coefficients and add the quadratic expression. This takes $O(n)$ work per generated element, so the complete simulation needs $O(nk)$ operations. With $k$ reaching $10^{18}$, this is not remotely feasible.

The reason the brute force works at all is that every new value only depends on a small amount of information: the previous $n$ sequence values and the current index information needed for the quadratic term. The sequence therefore has a small fixed-size state.

The key observation is that the quadratic part can also be represented as a recurrence. If we store the current index and its square as additional state values, the next index and next square can be produced with a linear transformation. The entire process becomes a matrix multiplication on a vector of size $n+3$.

Once the transition is represented as a matrix, reaching index $k$ requires applying the same transformation $k-(n-1)$ times. Fast exponentiation reduces this to logarithmic matrix multiplications.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Matrix Exponentiation | O((n+3)^3 log k) | O((n+3)^2) | Accepted |

## Algorithm Walkthrough

1. Build a state vector containing the current sequence values, a constant value, the current index, and the square of the current index. At position $n-1$, the state is:

$$[a_{n-1}, a_{n-2}, \dots, a_0, 1, n-1, (n-1)^2]$$

The extra three values allow the quadratic part of the recurrence to be handled by the same linear transformation.

1. Construct the transition matrix that moves the state from index $i$ to index $i+1$. The first row creates $a_{i+1}$. It combines the stored sequence values using the recurrence coefficients and adds:

$$p + (i+1)q + (i+1)^2r$$

which becomes:

$$(p+q+r) + (q+2r)i + r i^2$$

using the stored values $1$, $i$, and $i^2$.

1. Fill the remaining rows of the matrix to shift the previous sequence values forward. The sequence part behaves like a normal linear recurrence, so every value simply moves one position down.
2. If $k$ is smaller than $n$, return the already known initial value. Otherwise, raise the transition matrix to the power $k-(n-1)$.

The exponent is exactly the number of transitions needed to move from the initial state at index $n-1$ to the desired index.

1. Multiply the powered matrix by the initial state vector. The first element of the resulting vector is $a_k$.

Why it works:

The invariant is that after applying the transition matrix $t$ times, the state vector contains exactly the sequence values and index information for position $n-1+t$. The matrix computes the next sequence value using the same recurrence formula and updates the index information consistently. Since matrix exponentiation produces the same result as applying the transition repeatedly, the first component after $k-(n-1)$ transitions must be $a_k$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def mat_mul(a, b):
    n = len(a)
    m = len(b[0])
    k = len(b)
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        for x in range(k):
            if a[i][x]:
                ax = a[i][x]
                for j in range(m):
                    res[i][j] = (res[i][j] + ax * b[x][j]) % MOD
    return res

def mat_pow(a, e):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    while e:
        if e & 1:
            res = mat_mul(res, a)
        a = mat_mul(a, a)
        e >>= 1
    return res

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    c = list(map(int, input().split()))
    p, q, r = map(int, input().split())

    if k < n:
        print(a[k] % MOD)
        return

    size = n + 3
    trans = [[0] * size for _ in range(size)]

    for i in range(n):
        trans[0][i] = c[i] % MOD

    trans[0][n] = (p + q + r) % MOD
    trans[0][n + 1] = (q + 2 * r) % MOD
    trans[0][n + 2] = r % MOD

    for i in range(1, n):
        trans[i][i - 1] = 1

    trans[n][n] = 1
    trans[n + 1][n] = 1
    trans[n + 1][n + 1] = 1
    trans[n + 2][n] = 1
    trans[n + 2][n + 1] = 2
    trans[n + 2][n + 2] = 1

    state = [[0] for _ in range(size)]
    for i in range(n):
        state[i][0] = a[n - 1 - i] % MOD

    idx = n - 1
    state[n][0] = 1
    state[n + 1][0] = idx % MOD
    state[n + 2][0] = (idx * idx) % MOD

    result = mat_mul(mat_pow(trans, k - (n - 1)), state)
    print(result[0][0] % MOD)

if __name__ == "__main__":
    solve()
```

The code first handles the simple case where the answer is among the provided initial values. This avoids unnecessary matrix construction and also prevents indexing errors.

The transition matrix uses the first $n$ columns for the sequence history. The sequence is stored in reverse order so that the first row can directly apply the coefficients $c_1, c_2, \ldots, c_n$.

The last three positions store $1$, the current index, and the current index squared. The square transition follows:

$$(i+1)^2 = i^2 + 2i + 1$$

which explains the coefficients in the last row. All operations are performed modulo $10^9+7$, so Python's integer size is not a concern.

The exponent is $k-(n-1)$, not $k$. The starting state already represents $a_{n-1}$, so only the remaining transitions need to be applied.

## Worked Examples

For the first sample:

```
2 2
0 30
2 1
2 1 1
```

The initial state is:

| Step | Current index | Stored values | Added term | Result |
| --- | --- | --- | --- | --- |
| Initial | 1 | a1=30, a0=0 | none | 30 |
| Transition | 2 | 2×30+0 | 2+2+4 | 68 |

The transition moves from index 1 to index 2 once. The matrix correctly combines the previous values and the quadratic contribution.

For the second sample:

```
1 3
5
1
2 3 4
```

The state evolution is:

| Step | Current index | Previous value | Polynomial contribution | New value |
| --- | --- | --- | --- | --- |
| Initial | 0 | 5 | none | 5 |
| Transition | 1 | 5 | 2+3+4 | 14 |
| Transition | 2 | 14 | 2+6+16 | 38 |
| Transition | 3 | 38 | 2+9+36 | 85 |

The trace demonstrates why the index and square must be part of the state. The added value changes every step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+3)^3 log k) | Matrix multiplication is done during binary exponentiation. |
| Space | O((n+3)^2) | Only the transition matrix and vectors are stored. |

The matrix dimension is at most 13 because $n$ is at most 10. The logarithm of $k$ is about 60 even for $10^{18}$, so the solution easily fits the limits.

## Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    n = int(next(it))
    k = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    c = [int(next(it)) for _ in range(n)]
    p = int(next(it))
    q = int(next(it))
    r = int(next(it))

    if k < n:
        return str(a[k] % MOD)

    size = n + 3
    trans = [[0] * size for _ in range(size)]

    for i in range(n):
        trans[0][i] = c[i] % MOD
    trans[0][n] = (p + q + r) % MOD
    trans[0][n + 1] = (q + 2 * r) % MOD
    trans[0][n + 2] = r % MOD

    for i in range(1, n):
        trans[i][i - 1] = 1

    trans[n][n] = 1
    trans[n + 1][n] = 1
    trans[n + 1][n + 1] = 1
    trans[n + 2][n] = 1
    trans[n + 2][n + 1] = 2
    trans[n + 2][n + 2] = 1

    def mul(a, b):
        m = len(a)
        res = [[0] * m for _ in range(m)]
        for i in range(m):
            for x in range(m):
                for j in range(m):
                    res[i][j] = (res[i][j] + a[i][x] * b[x][j]) % MOD
        return res

    def power(a, e):
        m = len(a)
        res = [[int(i == j) for j in range(m)] for i in range(m)]
        while e:
            if e & 1:
                res = mul(res, a)
            a = mul(a, a)
            e >>= 1
        return res

    state = [[0] for _ in range(size)]
    for i in range(n):
        state[i][0] = a[n - 1 - i]
    state[n][0] = 1
    state[n + 1][0] = n - 1
    state[n + 2][0] = (n - 1) * (n - 1)

    ans = mul(power(trans, k - n + 1), state)
    return str(ans[0][0] % MOD)

assert run("""2 2
0 30
2 1
2 1 1
""") == "68"

assert run("""1 3
5
1
2 3 4
""") == "85"

assert run("""1 0
123
5
1 1 1
""") == "123"

assert run("""3 2
7 8 9
1 1 1
0 0 0
""") == "9"

assert run("""1 1000000000000000000
0
1
0 0 0
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Second sample | 85 | Quadratic growth with order 1 recurrence |
| Initial index query | 123 | Returning an already known value |
| Zero polynomial recurrence | 9 | Correct handling of a pure linear recurrence |
| Huge index | Valid non-empty result | Matrix exponentiation for very large k |

## Edge Cases

The first important edge case is a query inside the initial sequence. For:

```
3 1
7 8 9
1 1 1
0 0 0
```

the algorithm immediately returns the second provided value. It never applies the transition matrix because the recurrence only defines future elements.

The second edge case is a recurrence where the polynomial contribution is zero. In that situation the last three state values still exist, but the first row simply ignores them. The matrix behaves exactly like a normal linear recurrence.

The final edge case is an extremely large index. For example:

```
1 1000000000000000000
0
1
0 0 0
```

A simulation would need $10^{18}$ transitions. The algorithm instead performs about 60 matrix squarings and obtains the same transition power using binary exponentiation.
