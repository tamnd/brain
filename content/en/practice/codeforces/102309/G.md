---
title: "CF 102309G - Game of Orz Pandas"
description: "We have n rooms arranged from left to right. Each room contains piles of stones, and a grouped input record (p, q, c) means that room q contains c distinct piles whose size is p. A query gives an interval [l, r]."
date: "2026-08-13T06:59:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102309
codeforces_index: "G"
codeforces_contest_name: "The 2019 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102309
solve_time_s: 789
verified: true
draft: false
---

[CF 102309G - Game of Orz Pandas](https://codeforces.com/problemset/problem/102309/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` rooms arranged from left to right. Each room contains piles of stones, and a grouped input record `(p, q, c)` means that room `q` contains `c` distinct piles whose size is `p`. A query gives an interval `[l, r]`. From every room inside this interval, qkoqhh may either choose no pile or choose exactly one of the piles in that room.

There is also one extra pile of size `x`, created before the game starts. After all choices are made, the selected piles together with this extra pile form a Nim position. The first player wins exactly when the xor of all pile sizes is nonzero, so qkoqhh wins exactly when the xor of the selected room piles is `x`. The answer to a query is the number of different ways to make these choices, counted modulo `10007`.

The multiplicities matter. If a room contains three different piles of size `5`, choosing one pile of size `5` gives three different choices. A room containing `c` piles of size zero contributes `c` different ways to keep the xor unchanged, in addition to the choice of selecting nothing.

The constraints make the structure quite specific. There are only `n <= 500` rooms, and every pile size and `x` is at most `500`, so every pile size fits inside a 9-bit xor state. Thus there are only `2^9 = 512` possible xor values. On the other hand, `m` can be `10000`, and a single record can describe `10000` physical piles, so explicitly expanding all piles can create up to `10^8` objects. The algorithm must aggregate equal pile sizes rather than iterate over individual piles.

There can be as many as `n(n+1)/2 = 125250` queries. A method that spends `O(n)` or more work per query is already around tens of millions of operations, so the small fixed xor dimension of `512` has to be exploited. The useful target is roughly `O((n+Q) * 512)` after preprocessing.

A direct brute force over choices is completely hopeless. Even with only one nonzero pile in each of the `500` rooms, there are `2^500` possible selections, approximately `3.27 * 10^150`. If every selection scans all rooms, that is about `500 * 2^500` room decisions.

Several edge cases can silently break a simpler implementation. First, a zero-sized pile changes no xor value, but selecting different zero-sized piles still gives different choices. For example, with `n=1`, `x=0`, and one zero-sized pile in room `1`, the query `[1,1]` has answer `2`: choose nothing or choose the zero pile. An implementation that ignores zero-sized piles would return `1`.

Second, duplicate sizes must preserve their multiplicity. For `n=1`, `x=1`, and two distinct piles of size `1` in room `1`, the query `[1,1]` has answer `2`, because either physical pile produces xor `1`. Treating the two piles as one value would return `1`.

Third, modular division cannot be applied blindly to prefix products. A transformed room value can be `0` modulo `10007`. If such a room lies inside a query interval, the corresponding transformed interval product is zero. Dividing two zero prefix products loses this information and can produce an incorrect nonzero value. The optimal solution explicitly records the last zero factor for every transformed coordinate.

## Approaches

The brute-force solution would enumerate every legal selection of piles, compute the xor of the selected piles, xor it with `x`, and count the selections whose final xor is zero. This is correct because Nim is losing exactly when its pile xor is zero. The problem is the number of selections. Even the much smaller case of one pile per room already creates `2^500` choices, and the actual input can contain up to `10^8` physical piles through multiplicities.

A natural dynamic programming improvement is to keep `dp[s]`, the number of ways to obtain xor `s` after processing some rooms. For a room whose piles have sizes `p` with multiplicities `c[p]`, the transition is

`new[s] = dp[s] + sum(c[p] * dp[s xor p])`.

This is correct and already removes dependence on the number of physical piles. However, doing this transition directly costs `O(512 * number_of_distinct_sizes)` per room. More importantly, answering every interval independently would still require processing all rooms in that interval.

The key observation is that the transition is an XOR convolution. Define a room vector `f` by setting `f[0]` to `1` for choosing nothing and then adding the multiplicity of every pile size to its corresponding position. The interval DP is exactly the XOR convolution of all room vectors in the interval.

The Walsh-Hadamard transform diagonalizes XOR convolution. After transforming a vector, XOR convolution becomes ordinary pointwise multiplication. This is the same reason the Fast Walsh-Hadamard Transform is commonly used for XOR convolution.

For a transformed coordinate `k`, let `a_q[k]` be the transformed value of room `q`. The transformed value for an interval `[l,r]` is simply

`a_l[k] * a_{l+1}[k] * ... * a_r[k]`.

Now the interval problem has become a range product problem for `512` independent scalar sequences.

A prefix product would normally let us obtain a range product by division. There is one complication: a factor can be zero modulo `10007`. We solve it by maintaining two pieces of information for every transformed coordinate. The first is the product of all nonzero factors seen so far. The second is the position of the latest zero factor. If the latest zero lies inside `[l,r]`, the interval product is zero. Otherwise the interval product is the quotient of two nonzero prefix products.

Finally, the inverse Walsh-Hadamard transform gives the number of selections for every xor value. We only need the coefficient corresponding to `x`, so we can compute that coefficient directly using the inverse transform formula instead of transforming the entire interval back.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n * 2^n)` even with one pile per room | `O(n)` | Too slow |
| Direct xor DP per interval | `O(Q * n * 512)` | `O(512)` | Too slow |
| Optimal, WHT + range products | `O(n * 512 * log 512 + (n + Q) * 512)` | `O(n * 512)` | Accepted |

## Algorithm Walkthrough

1. For every room `q`, build an array `f_q` of length `512`. Position `0` starts with value `1`, representing the choice of selecting nothing. For every input record `(p,q,c)`, add `c` to `f_q[p]`. If `p=0`, this means `f_q[0]` becomes `1+c`, because selecting any one of the zero piles leaves the xor unchanged but gives a distinct choice.
2. Apply the Walsh-Hadamard transform to every room vector. The transformed vector `A_q` has `512` coordinates. At coordinate `k` it represents

`A_q[k] = sum_v f_q[v] * (-1)^{popcount(k & v)}`.

The reason for choosing this transform is that XOR convolution between room choice distributions becomes ordinary multiplication coordinate by coordinate.
3. For every transformed coordinate `k`, scan the rooms from left to right and build a prefix product containing only nonzero factors. Let `pref[k][i]` be the product of `A_1[k] ... A_i[k]` after skipping every factor equal to zero. Also store `last_zero[k][i]`, the greatest room index at most `i` where `A_q[k]` was zero.
4. For a query `[l,r]` and a fixed coordinate `k`, first check `last_zero[k][r]`. If it is at least `l`, then one factor inside the interval is zero, so the transformed interval product is zero. Otherwise every factor in the interval is nonzero, and its product is

`pref[k][r] / pref[k][l-1]`.

Since the modulus `10007` is prime, every nonzero residue has a modular inverse. The implementation precomputes the inverse of every nonzero residue once, so each range product is obtained in constant time.
5. The inverse Walsh-Hadamard transform has a particularly convenient formula. If `P[k]` is the transformed interval product, then the number of selections whose xor is `x` is

`answer = inv(512) * sum_k P[k] * (-1)^{popcount(k & x)}`.

Precompute this sign for every `k`, then evaluate the formula for every query.
6. Process all queries using the same transformed prefix data. There is no need to reconstruct an xor DP for each interval. Each query performs `512` independent scalar range-product lookups and one final modular reduction.

Why it works

For every room, `f_q[v]` is exactly the number of ways to make the room contribute xor `v`. Combining two rooms means choosing one contribution from each, so their resulting distribution is the XOR convolution of their vectors. The Walsh-Hadamard transform converts this convolution into coordinate-wise multiplication, so the transformed vector of an interval is exactly the product of its room transforms.

The prefix structure returns that product correctly for every coordinate. If a zero factor occurs inside the interval, the stored last-zero position detects it and returns zero. If no zero occurs, both prefix products are nonzero, so their quotient is exactly the desired interval product modulo `10007`.

The inverse Walsh-Hadamard formula then extracts the coefficient for xor `x`. That coefficient counts precisely the selections whose selected piles xor to `x`, which means their xor together with the initial pile `x` is zero. Such a Nim position is losing for the first player, so every counted selection is exactly a winning choice for qkoqhh.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10007
S = 512
INV_S = pow(S, MOD - 2, MOD)

# Modular inverses of every nonzero residue modulo MOD.
INV = [0] * MOD
INV[1] = 1
for i in range(2, MOD):
    INV[i] = MOD - (MOD // i) * INV[MOD % i] % MOD

def fwht(a):
    """Walsh-Hadamard transform for XOR convolution."""
    h = 1
    while h < S:
        step = h << 1
        for base in range(0, S, step):
            end = base + h
            j = base
            while j < end:
                u = a[j]
                v = a[j + h]

                x = u + v
                if x >= MOD:
                    x -= MOD

                y = u - v
                if y < 0:
                    y += MOD

                a[j] = x
                a[j + h] = y
                j += 1
        h <<= 1

def solve():
    out = []

    while True:
        line = input()
        if not line:
            break
        if not line.strip():
            continue

        n, x = map(int, line.split())

        m = int(input())

        rooms = [[0] * S for _ in range(n)]

        for _ in range(m):
            p, q, c = map(int, input().split())
            rooms[q - 1][p] = (rooms[q - 1][p] + c) % MOD

        # Choosing nothing is always one possibility.
        for q in range(n):
            rooms[q][0] = (rooms[q][0] + 1) % MOD

        # Transform every room.
        for q in range(n):
            fwht(rooms[q])

        # pref[k][i] = product of all nonzero transformed factors
        # among rooms 1..i at coordinate k.
        pref = [[1] * (n + 1) for _ in range(S)]

        # last_zero[k][i] = latest room <= i whose transformed
        # value at coordinate k is zero.
        last_zero = [[0] * (n + 1) for _ in range(S)]

        for k in range(S):
            p = 1
            z = 0

            prow = pref[k]
            zrow = last_zero[k]

            for i in range(1, n + 1):
                value = rooms[i - 1][k]

                if value == 0:
                    z = i
                else:
                    p = (p * value) % MOD

                prow[i] = p
                zrow[i] = z

        qn = int(input())
        queries = []

        for _ in range(qn):
            l, r = map(int, input().split())
            queries.append((l, r))

        # The inverse transform coefficient for xor x uses
        # the character (-1)^(popcount(k & x)).
        signs = [1] * S
        for k in range(S):
            if (k & x).bit_count() & 1:
                signs[k] = -1

        answers = [0] * qn

        # Process one transformed coordinate at a time.
        # This keeps the prefix rows local and avoids repeated
        # two-dimensional indexing in the hottest loop.
        for k in range(S):
            prow = pref[k]
            zrow = last_zero[k]
            sign = signs[k]

            for qi, (l, r) in enumerate(queries):
                if zrow[r] >= l:
                    continue

                # Both prefix values are nonzero, so division is valid.
                value = prow[r] * INV[prow[l - 1]]

                if sign == 1:
                    answers[qi] += value
                else:
                    answers[qi] -= value

        for value in answers:
            value %= MOD
            value = value * INV_S % MOD
            out.append(str(value))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input is first aggregated directly into `rooms[q][p]`, so the implementation never expands the potentially enormous number of physical piles. The extra `1` added at position zero represents choosing nothing from that room.

The Walsh-Hadamard transform uses the standard butterfly operation `u+v` and `u-v`. Values are reduced modulo `10007` after each butterfly, which keeps every stored coefficient small. The transform length is exactly `512` because all pile sizes are below `512`.

The prefix construction deliberately ignores zero transformed factors instead of multiplying them into the prefix. This is what makes division possible later. `last_zero` carries the missing information needed to distinguish an interval containing a zero factor from an interval whose nonzero product happens to have the same prefix values.

The inverse table `INV` avoids calling modular exponentiation for every query and frequency. Since the prefix products are never zero, `INV[prow[l - 1]]` is always valid. The expression `prow[r] * INV[prow[l - 1]]` is left as an ordinary Python integer until the final query reduction. This removes a costly modulo operation from the hottest loop.

The query loop runs over transformed coordinates rather than rebuilding an array for every query. The sign is determined by the parity of the bits shared by `k` and `x`, exactly matching the inverse Walsh-Hadamard character for xor value `x`.

There is no integer-overflow concern in Python. In a fixed-width language, the intermediate product is also small here because both operands are below `10007`, but Python naturally handles the larger temporary sums accumulated over `512` coordinates.

## Worked Examples

### Sample 1

The input describes three rooms with `x=1`. Room 1 contains two distinct piles of size `1`. Rooms 2 and 3 each contain one pile of size `2`.

For room 1, the choice distribution is `f=[1,2]` on xor values `0` and `1`. For room 2 it is `f=[1,0,1]`, and room 3 has the same distribution.

The following table shows the equivalent xor DP state for the relevant low xor values. This is the same state represented by the inverse Walsh-Hadamard transform, but it is easier to inspect directly.

| Processed rooms | `dp[0]` | `dp[1]` | `dp[2]` | `dp[3]` |
| --- | --- | --- | --- | --- |
| None | 1 | 0 | 0 | 0 |
| Room 1 | 1 | 2 | 0 | 0 |
| Rooms 1..2 | 1 | 2 | 1 | 2 |
| Rooms 1..3 | 2 | 4 | 2 | 4 |

For query `[1,1]`, the desired xor is `x=1`, so the answer is `dp[1]=2`. For `[1,2]`, it remains `2`. For `[1,3]`, it becomes `4`. Thus the output is `2, 2, 4`.

The third query demonstrates why different choices in different rooms combine through xor. To obtain xor `1`, qkoqhh chooses one of the two size-1 piles in room 1, and rooms 2 and 3 must either both be skipped or both contribute their size-2 pile. That gives `2 * 2 = 4` choices.

### Sample 2

Here `x=0`. Room 1 contains two distinct piles of size `1`, while room 2 contains two distinct piles of size `2`. The query covers both rooms.

| Processed rooms | `dp[0]` | `dp[1]` | `dp[2]` | `dp[3]` |
| --- | --- | --- | --- | --- |
| None | 1 | 0 | 0 | 0 |
| Room 1 | 1 | 2 | 0 | 0 |
| Rooms 1..2 | 1 | 2 | 2 | 4 |

The answer is the coefficient for xor `x=0`, namely `dp[0]=1`. The only winning choice is to select nothing. Selecting one size-1 pile gives xor `1`, selecting one size-2 pile gives xor `2`, and selecting one from both rooms gives xor `3`.

This example also confirms that multiplicities are counted correctly. The values `2` in `dp[1]` and `dp[2]` come from the two distinct physical piles in the corresponding rooms.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n * 512 * log 512 + (n + Q) * 512 + m)` | Each room is transformed once, prefixes are built for all 512 coordinates, and every query checks 512 coordinates |
| Space | `O(n * 512 + Q)` | Room transforms, prefix products, zero positions, and stored queries |

With `n <= 500` and `Q <= 125250`, the query phase performs at most about `64` million simple coordinate operations. The xor dimension is fixed at `512`, and the room transforms require only `9` butterfly layers. The algorithm also avoids storing the physical piles, which is necessary because the multiplicities can represent far more objects than `m` suggests.

The official problem page gives the same `n <= 500`, `m <= 10000`, and `Q <= n(n+1)/2` bounds.

## Test Cases

The following harness assumes the `solve()` function from the solution above is available from a file named `solution.py`.

```python
import sys
import io

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
sample = """\
3 1
3
1 1 2
2 2 1
2 3 1
3
1 1
1 2
1 3
3 0
3
1 1 1
1 1 1
2 2 2
1
1 3
"""

assert run(sample) == "2\n2\n4\n1", "provided samples"

# Minimum-size input, nonzero pile.
assert run("""\
1 1
1
1 1 1
1
1 1
""") == "1", "minimum-size nonzero case"

# Zero-sized pile must count as a separate choice.
assert run("""\
1 0
1
0 1 1
1
1 1
""") == "2", "zero pile multiplicity"

# Duplicate piles in one room are distinct choices.
assert run("""\
1 1
1
1 1 2
1
1 1
""") == "2", "duplicate physical piles"

# Boundary intervals and xor values.
assert run("""\
3 3
3
1 1 1
2 2 1
4 3 1
3
1 2
2 3
1 3
""") == "1\n0\n1", "interval boundaries"

# Maximum n, with a large multiplicity.
assert run("""\
500 0
1
0 500 10000
1
1 500
""") == "10001", "maximum room count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, one size-1 pile | `1` | Minimum input and the basic Nim xor condition |
| `1 0`, one size-0 pile | `2` | Selecting a zero pile is different from selecting nothing |
| `1 1`, two size-1 piles | `2` | Equal pile sizes remain distinct choices |
| Three rooms with sizes `1,2,4` | `1, 0, 1` | Left and right interval boundaries |
| `n=500`, ten thousand zero piles | `10001` | Large `n`, large multiplicity, and modulo-safe aggregation |

## Edge Cases

A room containing zero-sized piles is handled when its vector is initialized. Suppose the input is

```
1 0
1
0 1 1
1
1 1
```

Room 1 initially has the empty choice, contributing one way to xor zero. The single zero-sized pile adds another way to xor zero, so `f[0]=2`. Every transformed coordinate is consequently multiplied by `2`. The final xor-zero coefficient is `2`, which is exactly the number of choices. A careless implementation that starts with `f[0]=1` but discards records with `p=0` would incorrectly produce `1`.

Duplicate piles are handled through addition into the same `f[p]` entry. For

```
1 1
1
1 1 2
1
1 1
```

the room vector has `f[0]=1` and `f[1]=2`. There are three legal room choices: select nothing, select the first size-1 pile, or select the second size-1 pile. Only the last two give xor `1`, so the answer is `2`. The algorithm never needs to distinguish the two piles inside the transformed vector because their multiplicity is already represented by the coefficient `2`.

The interval boundary case is

```
3 3
3
1 1 1
2 2 1
4 3 1
3
1 2
2 3
1 3
```

For `[1,2]`, the available nonzero values are `1` and `2`, and their possible xors are `0,1,2,3`, so xor `3` occurs once by selecting both piles. The answer is `1`. For `[2,3]`, the possible xors are `0,2,4,6`, so xor `3` never occurs and the answer is `0`. For `[1,3]`, selecting the size-1 and size-2 piles gives xor `3`, while the size-4 pile cannot be part of another combination producing `3`, so the answer is again `1`. The prefix indexing uses `pref[l-1]`, which is exactly what prevents the left endpoint from being accidentally excluded or included twice.

The zero transformed factor case is handled independently of pile sizes. For some frequency `k`, suppose the transformed room values over an interval are `5,0,7`. The correct transformed product is zero. The prefix structure stores the product of nonzero factors as `35` and records the zero's position. A query covering the zero sees `last_zero[k][r] >= l` and immediately contributes zero. A query beginning after that zero sees no zero inside its interval and safely divides the nonzero prefix products. This is the reason the implementation does not simply use ordinary prefix division.

Finally, the extra initial pile is not treated as another room. Its only role is to change the target xor from `0` to `x`. A selected set of room piles is winning for qkoqhh exactly when its xor equals `x`, because then the total xor including the initial pile is `x xor x = 0`. This is why the final inverse-transform extraction uses coordinate `x` rather than coordinate `0`.
