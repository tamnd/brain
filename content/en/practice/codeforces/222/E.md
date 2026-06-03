---
title: "CF 222E - Decoding Genome"
description: "We have an alphabet of size m, consisting of the first m symbols from the sequence a..zA..Z. Some ordered pairs of symbols are forbidden. If pair (x, y) is forbidden, then symbol y cannot appear immediately after symbol x in the DNA string."
date: "2026-06-04T02:06:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "matrices"]
categories: ["algorithms"]
codeforces_contest: 222
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 137 (Div. 2)"
rating: 1900
weight: 222
solve_time_s: 115
verified: true
draft: false
---

[CF 222E - Decoding Genome](https://codeforces.com/problemset/problem/222/E)

**Rating:** 1900  
**Tags:** dp, matrices  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an alphabet of size `m`, consisting of the first `m` symbols from the sequence `a..zA..Z`. Some ordered pairs of symbols are forbidden. If pair `(x, y)` is forbidden, then symbol `y` cannot appear immediately after symbol `x` in the DNA string.

The task is to count how many DNA strings of length `n` satisfy all adjacency restrictions. The answer must be reported modulo `10^9 + 7`.

A useful way to view the problem is as a directed graph. Each nucleotide is a vertex. There is a directed edge from vertex `u` to vertex `v` if the pair `(u, v)` is allowed. A valid DNA sequence corresponds to a walk in this graph. Every adjacent pair of characters in the sequence must follow an allowed edge.

The constraints completely determine the intended solution. The alphabet size is at most `52`, which is tiny. On the other hand, `n` can be as large as `10^15`, which rules out any dynamic programming that iterates over positions one by one. Even an `O(n)` algorithm is impossible. Whenever a problem combines a very small state space with an enormous length, matrix exponentiation is usually the right direction.

There are several edge cases that are easy to mishandle.

Consider a length-one DNA:

```
1 3 2
ab
ba
```

The answer is `3`, not affected by any forbidden pairs. A string of length one contains no adjacent pair at all.

Another important case is when every transition is forbidden:

```
2 1 1
aa
```

The answer is `0`. There is one symbol, but it cannot follow itself, so no length-two sequence exists.

A third case is when `n` is extremely large but `m = 1`:

```
1000000000000000 1 0
```

There is exactly one valid sequence, namely `"aaaa..."`. Any solution that iterates over positions will never finish.

## Approaches

The most direct approach is dynamic programming over positions.

Let `dp[i][j]` be the number of valid strings of length `i` ending with symbol `j`. To compute the next layer, we try every allowed transition:

$$dp[i+1][v] += dp[i][u]$$

This is correct because every valid string ending at `u` can be extended to `v` whenever `(u,v)` is allowed.

The problem is the value of `n`. Even if we optimize the transition using the small alphabet size, the running time remains proportional to the length of the DNA. With `n` up to `10^{15}`, this is hopeless.

The key observation is that the DP transition is linear. If we store the counts for all ending symbols in a vector, one DP step is simply a matrix multiplication.

Let `A` be the `m × m` transition matrix:

$$A[u][v] =
\begin{cases}
1 & \text{if transition } u \to v \text{ is allowed}\\
0 & \text{otherwise}
\end{cases}$$

If `f_i` is the row vector of counts for length `i`, then

$$f_{i+1} = f_i A$$

Applying the transition repeatedly gives

$$f_n = f_1 A^{n-1}$$

Now the huge value of `n` becomes manageable. Since `m ≤ 52`, we can exponentiate the matrix using binary exponentiation in `O(m^3 log n)` time.

The initial vector for length one contains all ones, because any symbol may be chosen as the first character.

After computing `A^(n-1)`, we multiply it by the initial vector and sum all final counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over positions | O(nm²) | O(m) | Too slow |
| Matrix Exponentiation | O(m³ log n) | O(m²) | Accepted |

## Algorithm Walkthrough

1. Create an index mapping for characters. Symbols `'a'..'z'` map to `0..25`, and `'A'..'Z'` map to `26..51`.
2. Build an `m × m` transition matrix `A`.

Initially every entry is `1`, meaning every transition is allowed.
3. Read each forbidden pair `(x, y)` and set the corresponding matrix entry to `0`.

The matrix now exactly represents the graph of allowed transitions.
4. Handle the special case `n = 1`.

Every symbol alone forms a valid DNA string, so the answer is simply `m`.
5. Compute `A^(n-1)` using binary exponentiation.

Each matrix multiplication is performed modulo `10^9 + 7`.
6. Create the initial row vector

$$f_1 = [1,1,\ldots,1]$$

because any symbol can be chosen as the first character.
7. Multiply `f_1` by `A^(n-1)`.

The resulting vector contains the number of valid length-`n` strings ending with each symbol.
8. Sum all entries of the resulting vector modulo `10^9 + 7`.

This gives the total number of valid DNA strings.

### Why it works

The transition matrix encodes exactly the same recurrence as the ordinary dynamic program. Entry `(u,v)` equals one precisely when a string ending at `u` may be extended by symbol `v`.

Multiplying a count vector by `A` performs one DP transition. Multiplying by `A²` performs two transitions. By induction, multiplying by `A^k` performs `k` consecutive DP transitions. Since a length-`n` string consists of one initial symbol followed by `n-1` transitions, the count vector for length `n` is exactly

$$f_1 A^{n-1}.$$

Summing the final vector counts all valid strings regardless of their ending symbol.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def char_id(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    return ord(c) - ord('A') + 26

def mat_mul(a, b):
    n = len(a)
    res = [[0] * n for _ in range(n)]

    for i in range(n):
        ai = a[i]
        ri = res[i]

        for k in range(n):
            if ai[k] == 0:
                continue

            val = ai[k]
            bk = b[k]

            for j in range(n):
                ri[j] = (ri[j] + val * bk[j]) % MOD

    return res

def mat_pow(mat, exp):
    n = len(mat)

    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1

    while exp:
        if exp & 1:
            res = mat_mul(res, mat)

        mat = mat_mul(mat, mat)
        exp >>= 1

    return res

def solve():
    n, m, k = map(int, input().split())

    trans = [[1] * m for _ in range(m)]

    for _ in range(k):
        s = input().strip()
        u = char_id(s[0])
        v = char_id(s[1])
        trans[u][v] = 0

    if n == 1:
        print(m)
        return

    power = mat_pow(trans, n - 1)

    ans = 0

    for col in range(m):
        total = 0
        for row in range(m):
            total += power[row][col]
        ans = (ans + total) % MOD

    print(ans)

solve()
```

The transition matrix is built directly from the forbidden-pair information. Every allowed adjacency contributes a `1`, every forbidden adjacency contributes a `0`.

The exponentiation routine uses the standard binary exponentiation pattern. Since `n` can be as large as `10^15`, only about fifty matrix squarings are required.

The final computation deserves attention. The initial vector consists entirely of ones. Multiplying a row vector of all ones by the powered matrix is equivalent to summing each column of that matrix. The implementation exploits this fact and avoids an extra vector-matrix multiplication.

All arithmetic is performed modulo `10^9 + 7`. Python integers do not overflow, but reducing modulo at each accumulation keeps the computation efficient.

## Worked Examples

### Example 1

Input:

```
3 3 2
ab
ba
```

Allowed transition matrix:

| From \ To | a | b | c |
| --- | --- | --- | --- |
| a | 1 | 0 | 1 |
| b | 0 | 1 | 1 |
| c | 1 | 1 | 1 |

After exponentiation we need `A²`.

| Step | Matrix |
| --- | --- |
| A | transitions above |
| A² | counts of length-2 walks |

Computing column sums of `A²` gives:

| Column | Sum |
| --- | --- |
| a | 5 |
| b | 5 |
| c | 7 |

Total:

| Value |
| --- |
| 5 + 5 + 7 = 17 |

Output:

```
17
```

This trace shows that matrix powers count walks of multiple steps. The final answer is the total number of length-three strings.

### Example 2

Input:

```
2 3 0
```

Every transition is allowed.

Transition matrix:

| From \ To | a | b | c |
| --- | --- | --- | --- |
| a | 1 | 1 | 1 |
| b | 1 | 1 | 1 |
| c | 1 | 1 | 1 |

Since `n = 2`, we need `A¹`.

| Column | Sum |
| --- | --- |
| a | 3 |
| b | 3 |
| c | 3 |

Total:

| Value |
| --- |
| 9 |

Output:

```
9
```

This matches the obvious count `3²`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m³ log n) | Matrix exponentiation with cubic matrix multiplication |
| Space | O(m²) | Storage of several `m × m` matrices |

Since `m ≤ 52`, a matrix multiplication costs roughly `52³ ≈ 140,000` arithmetic operations. Binary exponentiation performs about `log₂(10¹⁵) ≈ 50` iterations. This comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def char_id(c):
        if 'a' <= c <= 'z':
            return ord(c) - ord('a')
        return ord(c) - ord('A') + 26

    def mat_mul(a, b):
        n = len(a)
        res = [[0] * n for _ in range(n)]

        for i in range(n):
            for k in range(n):
                if a[i][k] == 0:
                    continue
                for j in range(n):
                    res[i][j] = (res[i][j] + a[i][k] * b[k][j]) % MOD

        return res

    def mat_pow(mat, exp):
        n = len(mat)
        res = [[0] * n for _ in range(n)]

        for i in range(n):
            res[i][i] = 1

        while exp:
            if exp & 1:
                res = mat_mul(res, mat)
            mat = mat_mul(mat, mat)
            exp >>= 1

        return res

    n, m, k = map(int, input().split())

    trans = [[1] * m for _ in range(m)]

    for _ in range(k):
        s = input().strip()
        trans[char_id(s[0])][char_id(s[1])] = 0

    if n == 1:
        return str(m)

    power = mat_pow(trans, n - 1)

    ans = 0
    for col in range(m):
        for row in range(m):
            ans = (ans + power[row][col]) % MOD

    return str(ans)

# sample
assert run("3 3 2\nab\nba\n") == "17"

# minimum size
assert run("1 1 0\n") == "1"

# single symbol, self-transition forbidden
assert run("2 1 1\naa\n") == "0"

# all transitions allowed
assert run("2 3 0\n") == "9"

# n=1 ignores restrictions
assert run("1 2 4\naa\nab\nba\nbb\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0` | `1` | Smallest possible instance |
| `2 1 1 / aa` | `0` | Forbidden self-loop |
| `2 3 0` | `9` | Fully connected graph |
| `1 2 4 ...` | `2` | Length one ignores adjacency restrictions |

## Edge Cases

Consider:

```
1 2 4
aa
ab
ba
bb
```

Every transition is forbidden, yet the answer is `2`. The algorithm returns immediately when `n = 1`, because no adjacency exists in a one-character string. A solution that blindly exponentiates or applies transitions could incorrectly produce zero.

Consider:

```
2 1 1
aa
```

The transition matrix is:

$$[0]$$

Since `n-1 = 1`, the powered matrix is still `[0]`. The column sum is zero, so the answer is zero. This correctly captures the fact that the only possible adjacent pair is forbidden.

Consider:

```
1000000000000000 1 0
```

The matrix is:

$$[1]$$

Any power of this matrix remains `[1]`. Binary exponentiation handles the huge exponent in logarithmic time, producing answer `1`. This is exactly the scenario that eliminates any position-by-position dynamic programming approach.
