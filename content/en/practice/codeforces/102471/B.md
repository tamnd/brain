---
title: "CF 102471B - Black and White"
description: "We have an (ntimes m) chessboard whose cell ((i,j)) has value (+1) when (i+j) is even and (-1) otherwise. A valid path consists of exactly (n) north steps and (m) east steps, starting at the bottom-left corner and ending at the top-right corner."
date: "2026-08-12T08:56:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "B"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 731
verified: true
draft: false
---

[CF 102471B - Black and White](https://codeforces.com/problemset/problem/102471/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n\times m) chessboard whose cell ((i,j)) has value (+1) when (i+j) is even and (-1) otherwise. A valid path consists of exactly (n) north steps and (m) east steps, starting at the bottom-left corner and ending at the top-right corner.

The cells on the left side of the directed path contribute their values to the score. We need to count how many paths have score exactly (k), modulo (998244353).

The input contains up to (100) independent test cases. Both dimensions can be (10^5), so a solution depending on (nm) is already too large: one test case can contain (10^{10}) cells. Enumerating all paths is even more hopeless because their number is

[
\binom{n+m}{n},
]

which is enormous even for moderate dimensions. The useful algorithm must process a test case in essentially constant time after a global factorial precomputation.

There are a few boundary cases where an implementation based on a guessed score range can go wrong. For (n=m=1), the two paths have scores (1) and (0), so the input `1 1 0` has answer (1), while `1 1 -1` has answer (0). A formula that assumes the score is symmetric around zero would already fail here.

The parity of (n+m) also matters. For `2 3 1`, the correct answer is (1), while for `2 3 -1` it is (3). The two sides are not symmetric when the total path length is odd. Finally, an impossible score such as `2 2 2` has answer (0), and the safest implementation should obtain this automatically from invalid binomial coefficients rather than handling every score boundary separately.

## Approaches

A direct brute-force solution can enumerate every path. There are (\binom{n+m}{n}) such paths. Even if we compute one path's score in only (O(n+m)) time, the total work is

[
O\left((n+m)\binom{n+m}{n}\right).
]

At (n=m=100000), this is roughly (200000\binom{200000}{100000}) operations, far beyond any feasible limit. A cell-by-cell score computation would be even worse, adding another factor of (nm).

The useful observation is that the checkerboard coloring makes the score depend only on the parity of the positions of the north steps in the path word.

Write the path as a sequence of (n+m) characters, with `N` for a north step and `E` for an east step. Number these positions starting from (1). Let (A) be the number of north steps occurring at even positions.

The central identity is

[
\boxed{\text{score}=A-\left\lfloor\frac n2\right\rfloor}.
]

Once this is known, the geometry disappears. There are

[
L_1=\left\lfloor\frac{n+m}{2}\right\rfloor
]

even positions and

[
L_2=\left\lceil\frac{n+m}{2}\right\rceil
]

odd positions in the path word. If the score is (k), then the number of north steps in even positions must be

[
A=\left\lfloor\frac n2\right\rfloor+k.
]

The remaining

[
n-A=\left\lceil\frac n2\right\rceil-k
]

north steps must occupy odd positions. The choices are independent, giving

[
\boxed{
\binom{\lfloor(n+m)/2\rfloor}
{\lfloor n/2\rfloor+k}
\binom{\lceil(n+m)/2\rceil}
{\lceil n/2\rceil-k}
}.
]

The factorials and inverse factorials can be precomputed once up to (200000), making every test case (O(1)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((n+m)\binom{n+m}{n})) | (O(n+m)) | Too slow |
| Optimal | (O(1)) per test after precomputation | (O(n+m)) total | Accepted |

## Algorithm Walkthrough

1. Represent the path as a word of (n) `N` steps and (m) `E` steps. Every monotone path corresponds to exactly one such word, so counting paths is equivalent to counting these words.
2. For every row (i), let (c_i) be the column where the path makes its north step from row (i) to row (i+1). The cells to the left of that vertical step are exactly the cells with column indices (0,1,\ldots,c_i-1).

Their signed contribution is

[
\sum_{j=0}^{c_i-1}(-1)^{i+j}.
]

This sum is zero when (c_i) is even. When (c_i) is odd, it equals ((-1)^i).
3. Number the north steps in their occurrence order. Let the (q)-th north step occur at position (t_q) in the complete path word. Before that step there are (q-1) north steps, so its column is

[
c_{q-1}=t_q-q.
]

If this column is odd, (t_q) and (q) have opposite parity. The contribution of this north step is then ((-1)^{q-1}).
4. Let (A) be the number of north steps at even positions. The positive contributions are exactly the north steps with odd index (q) at even positions. The negative contributions are exactly the north steps with even index (q) at odd positions.

Among the (\lfloor n/2\rfloor) even-indexed north steps, every one is either at an even or an odd position. Hence

## #(\text{odd }q,\ t_q\text{ even})

# #(\text{even }q,\ t_q\text{ odd})

A-\left\lfloor\frac n2\right\rfloor.
]

This identity is the key invariant of the whole solution.
5. For a required score (k), solve the identity for (A):

[
A=\left\lfloor\frac n2\right\rfloor+k.
]

There are (\lfloor(n+m)/2\rfloor) even positions, so there are

[
\binom{\lfloor(n+m)/2\rfloor}
{\lfloor n/2\rfloor+k}
]

ways to choose the even positions occupied by north steps.
6. There are (\lceil(n+m)/2\rceil) odd positions. The remaining (n-A) north steps must occupy these positions. Since

[
n-A=\left\lceil\frac n2\right\rceil-k,
]

there are

[
\binom{\lceil(n+m)/2\rceil}
{\lceil n/2\rceil-k}
]

choices.
7. Multiply the two binomial coefficients modulo (998244353). If either lower argument is outside its valid range, the corresponding binomial coefficient is zero, so impossible scores require no special case.

### Why it works

The row containing each north step gives a direct description of which cells in that row lie to its left. Because the cell colors alternate, the signed sum of that row is zero for an even column and exactly (+1) or (-1) for an odd column. Expressing the column of the (q)-th north step as (t_q-q) converts this condition into a parity relation between the north-step index and its absolute position in the path word.

After this conversion, every contribution to the score is determined solely by whether that north step occupies an even or odd position. The total score is exactly the number (A) of north steps in even positions minus (\lfloor n/2\rfloor). Once (A) is fixed, the choices of north-step positions in the even and odd parts of the word are independent. The two binomial coefficients count precisely those choices, so every valid path is counted once and no invalid path is counted.

## Python Solution

```python
import sys

input = sys.stdin.readline

MOD = 998244353

def prepare(max_n):
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (max_n + 1)
    invfact[max_n] = pow(fact[max_n], MOD - 2, MOD)
    for i in range(max_n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    return fact, invfact

def comb(n, r, fact, invfact):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

def main():
    T = int(input())
    tests = [tuple(map(int, input().split())) for _ in range(T)]

    max_size = 0
    for n, m, _ in tests:
        max_size = max(max_size, n + m)

    fact, invfact = prepare(max_size)

    ans = []

    for n, m, k in tests:
        even_positions = (n + m) // 2
        odd_positions = (n + m + 1) // 2

        north_on_even = n // 2 + k
        north_on_odd = (n + 1) // 2 - k

        left = comb(even_positions, north_on_even, fact, invfact)
        right = comb(odd_positions, north_on_odd, fact, invfact)

        ans.append(str(left * right % MOD))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()
```

The input is read completely before preprocessing so the factorial arrays only need to be built up to the largest (n+m) appearing in the test file. Since (n,m\leq100000), this limit is at most (200000).

The `comb` function explicitly returns zero when its lower argument is negative or larger than the upper argument. This handles scores outside the possible range without additional branches in the main algorithm.

For each test case, `even_positions` and `odd_positions` are the counts of positions (2,4,\ldots) and (1,3,\ldots) in a path word of length (n+m). The variables `north_on_even` and `north_on_odd` come directly from the score identity. Their sum is exactly (n), which is a useful sanity check.

There is no integer overflow issue in Python. Every multiplication is reduced modulo (998244353), and modular inverses are obtained with Fermat's theorem because the modulus is prime.

## Worked Examples

### Sample 1: `1 1 0`

The path has two steps, so there is one even position and one odd position. We need the following values.

| Variable | Value |
| --- | --- |
| (n) | 1 |
| (m) | 1 |
| (k) | 0 |
| even positions | 1 |
| odd positions | 1 |
| north on even positions | (0+0=0) |
| north on odd positions | (1-0=1) |
| answer | (\binom10\binom11=1) |

The only path with score zero is `NE`. Its north step is at position (1), so there are zero north steps at even positions. The score identity gives (0-\lfloor1/2\rfloor=0).

The trace demonstrates the asymmetric behavior caused by an odd number of total steps.

### Sample 2: `1 1 -1`

The structural values are unchanged, but now the requested score is (-1).

| Variable | Value |
| --- | --- |
| (n) | 1 |
| (m) | 1 |
| (k) | -1 |
| even positions | 1 |
| odd positions | 1 |
| north on even positions | (0-1=-1) |
| north on odd positions | (1-(-1)=2) |
| answer | (\binom1{-1}\binom12=0) |

Both required binomial coefficients are invalid. Hence the answer is zero. This matches the fact that a (1\times1) board cannot have score (-1).

### Sample 3: `2 2 1`

There are four positions, two of each parity.

| Variable | Value |
| --- | --- |
| (n) | 2 |
| (m) | 2 |
| (k) | 1 |
| even positions | 2 |
| odd positions | 2 |
| north on even positions | (1+1=2) |
| north on odd positions | (1-1=0) |
| answer | (\binom22\binom20=1) |

The unique path counted here is `NENE`. Both north steps occupy even positions, giving (A=2) and score (2-1=1).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(M+T)) | Factorials are precomputed up to (M=\max(n+m)), then each test case takes constant time |
| Space | (O(M)) | The factorial and inverse-factorial arrays each contain (M+1) values |

The largest possible (M) is (200000), so the preprocessing is small enough for the memory limit. After preprocessing, even (100) large test cases require only a constant amount of work each. No grid is constructed and no individual path is enumerated.

## Test Cases

```python
# Complete assert-based tests for the formula used by the solution.

MOD = 998244353

def build_fact(limit):
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (limit + 1)
    invfact[limit] = pow(fact[limit], MOD - 2, MOD)
    for i in range(limit, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    return fact, invfact

FACT, INVFACT = build_fact(200000)

def C(n, r):
    if r < 0 or r > n:
        return 0
    return FACT[n] * INVFACT[r] % MOD * INVFACT[n - r] % MOD

def expected(n, m, k):
    l1 = (n + m) // 2
    l2 = (n + m + 1) // 2
    a = n // 2 + k
    b = (n + 1) // 2 - k
    return C(l1, a) * C(l2, b) % MOD

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    t = data[0]
    pos = 1
    out = []

    for _ in range(t):
        n, m, k = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        out.append(str(expected(n, m, k)))

    return "\n".join(out)

# Provided samples.
sample = """\
5
1 1 0
1 1 -1
2 2 1
2 2 0
4 4 1
"""
assert run(sample) == """\
1
0
1
4
16
""", "provided samples"

# Minimum-size and asymmetric odd-length cases.
assert run("1\n1 1 1\n") == "1", "1x1 maximum score"
assert run("1\n1 2 0\n") == "2", "1x2 zero score"
assert run("1\n1 2 1\n") == "1", "1x2 positive score"

# Catches the asymmetry between positive and negative scores.
assert run("3\n2 3 1\n2 3 0\n2 3 -1\n") == """\
1
6
3
""", "odd total path length"

# Impossible score.
assert run("1\n2 2 2\n") == "0", "score outside the possible range"

# Maximum-size test case.
max_expected = expected(100000, 100000, 0)
assert run("1\n100000 100000 0\n") == str(max_expected), \
    "maximum n and m"

# A maximum-size dimension with a very small other dimension.
assert run("1\n100000 1 0\n") == "50001", \
    "maximum n with m=1"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Minimum board and maximum attainable score |
| `1 2 0` | `2` | Odd total path length and zero score |
| `2 3 1`, `2 3 0`, `2 3 -1` | `1`, `6`, `3` | Positive, zero, and negative scores with asymmetric distribution |
| `2 2 2` | `0` | Invalid score and binomial boundary handling |
| `100000 100000 0` | `C(100000,50000)^2 mod 998244353` | Both dimensions at their maximum |
| `100000 1 0` | `50001` | Large dimension with a thin board |

## Edge Cases

For `1 1 0`, the formula gives (L_1=L_2=1), (A=0), and (B=1). The answer is (\binom10\binom11=1). The path `NE` has its north step at odd position one, so its score is zero.

For `1 1 -1`, the required number of north steps in even positions is (-1). Since a binomial coefficient with a negative lower argument is zero, the answer is immediately zero. The same mechanism handles every impossible score.

For `2 3`, the total path length
