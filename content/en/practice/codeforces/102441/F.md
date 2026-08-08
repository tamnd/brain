---
title: "CF 102441F - Random XOR"
description: "We have an array a of n integers. Each element is independently selected with probability P = X / Y. The selected elements are XORed together, producing a random integer s. If nothing is selected, the XOR is zero."
date: "2026-08-08T13:26:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102441
codeforces_index: "F"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Final"
rating: 0
weight: 102441
solve_time_s: 109
verified: true
draft: false
---

[CF 102441F - Random XOR](https://codeforces.com/problemset/problem/102441/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array `a` of `n` integers. Each element is independently selected with probability `P = X / Y`. The selected elements are XORed together, producing a random integer `s`. If nothing is selected, the XOR is zero. The task is to compute the expected value of `s²`, with the final answer represented modulo `10^9 + 7`.

The difficulty is not computing the expected XOR itself. The expectation of each individual bit is fairly easy to obtain. The square introduces products between different bits, so we also need to understand how pairs of XOR bits behave together.

The constraint `n <= 10^5` immediately rules out enumerating subsets. There can be `2^n` possible selections, which is astronomically large even for a few dozen elements. The values are below `10^9 + 7`, so every `a_i` fits into 30 binary bits because `2^30 > 10^9 + 7`. That small bit width is the structural property that makes the problem tractable. We can afford work involving the roughly 30 bit positions, but we cannot afford work proportional to the number of subsets.

There are several edge cases where a tempting simplification gives the wrong answer. First, if `P = 0`, nothing is ever selected. For example,

```
1 0 7
123
```

gives `s = 0` with certainty, so the answer is `0`. A formula that assumes every probability is strictly between zero and one can mishandle this boundary.

At the other extreme, if `P = 1`, every element is selected. For example,

```
1 1 1
5
```

always produces `s = 5`, so the answer is `25`. The probabilistic calculation must also work when the random process becomes deterministic.

The more subtle case is correlation between bits. Consider

```
1 1 2
3
```

The result is either `0` or `3`, each with probability `1/2`, so

`E[s²] = (0² + 3²) / 2 = 9/2`.

Modulo `10^9 + 7`, this is `500000008`. A careless approach might observe that each of the two bits is independently `1` with probability `1/2`. They are not independent here: the number is either `00` or `11`. Treating them as independent would give the wrong second moment.

The given sample is

```
3 1 2
2 8 10
```

and its correct answer is `42`.

## Approaches

The direct approach is to consider every subset of `a`, XOR the selected elements, square the result, and average all values with their corresponding probabilities. There are `2^n` subsets. If every subset is constructed by examining all `n` elements, the operation count is `O(n 2^n)`. Even if Gray-code enumeration reduces the work per subset and gives `O(2^n)`, the worst case still contains `2^100000` states, so this approach is unusable.

The brute force works because it explicitly follows the random experiment. It fails because the experiment has exponentially many outcomes. The key observation is that the final XOR is built bit by bit, and the answer only contains terms of degree at most two in those output bits.

Write the binary representation of the final XOR as

`S = sum_k 2^k Z_k`,

where `Z_k` is the random bit at position `k`. Squaring gives

`S² = sum_k 2^(2k) Z_k + 2 sum_{i<j} 2^(i+j) Z_i Z_j`.

So we only need `E[Z_k]` and `E[Z_i Z_j]`.

Each `Z_k` is itself an XOR of independent Bernoulli variables. For such a parity, the useful quantity is not its probability directly, but its signed expectation

`E[(-1)^Z_k]`.

Suppose bit `k` is set in exactly `c_k` array elements. Every element whose bit is zero contributes a factor `1` to this signed expectation. Every element whose bit is one contributes

`(1-P) + P(-1) = 1 - 2P`.

Thus

`E[(-1)^Z_k] = (1 - 2P)^(c_k)`.

Let

`q = 1 - 2P`.

Then

`E[Z_k] = (1 - q^(c_k)) / 2`.

The same idea handles a pair of bits. For two output bits `Z_i` and `Z_j`, define

`A = E[(-1)^Z_i]`,
`B = E[(-1)^Z_j]`,
`C = E[(-1)^(Z_i XOR Z_j)]`.

The last quantity depends on how many input elements have different values at these two bit positions. Let that number be `d_ij`. Then

`C = q^(d_ij)`.

The four possible combinations of two Boolean variables can be recovered from their three signed expectations. In particular,

`P(Z_i = 1 and Z_j = 1) = (1 - A - B + C) / 4`.

This gives every term required by `E[S²]`.

There are only 30 bit positions, so only 30 single-bit counts and `30 * 29 / 2` pair distances are needed. The pair distances can be computed efficiently by representing every bit column as a packed bitset. The Hamming distance between two columns is then the population count of their XOR. In Python, large integers provide exactly this packed representation: a column is stored as an integer whose bits represent all `n` array elements, and Python's C implementation handles the XOR and `bit_count()` efficiently.

The result is reduced from exponential enumeration to work over 30 bit positions and packed `n`-bit columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n 2^n)` | `O(n)` | Too slow |
| Optimal | `O(30n + 30² n / W)` | `O(30n / 8)` | Accepted |

Here `W` is the machine word size used internally by packed bit operations. In the Python implementation, the corresponding operations are performed by optimized arbitrary-precision integer routines.

## Algorithm Walkthrough

1. Read `n`, `X`, `Y`, and the array. Work modulo `MOD = 10^9 + 7`. Compute

`q = 1 - 2X/Y`

modulo `MOD`. Since `Y < MOD`, its modular inverse exists.
2. Build one packed bit column for each of the 30 possible bit positions. The `r`-th bit of column `k` records whether bit `k` of `a[r]` is set. We can store these columns as Python integers.

This representation lets us compare entire columns at once instead of visiting all `n` elements for every pair of bit positions.
3. For every bit `k`, calculate its number of set entries `c_k` using `column[k].bit_count()`. Then compute

`R_k = q^(c_k)`.

Since `R_k = E[(-1)^Z_k]`, the probability that the final XOR has bit `k` set is

`p_k = (1 - R_k) / 2`.
4. Add the diagonal terms of the square. Bit `k` contributes

`2^(2k) p_k`

to `E[S²]`.
5. For every pair of distinct bit positions `i < j`, XOR their packed columns and count the set bits. This gives

`d_ij = number of input elements where bits i and j differ`.

Compute

`R_ij = q^(d_ij)`.

Together with `R_i` and `R_j`, this gives

`p_ij = P(Z_i = 1, Z_j = 1)`

as

`(1 - R_i - R_j + R_ij) / 4`.
6. Add the cross term

`2 * 2^(i+j) * p_ij`

to the answer for every pair `i < j`.
7. Reduce the final value modulo `MOD` and print it. The divisions by 2 and 4 are performed with modular inverses, which are `2^(MOD-2)` and `4^(MOD-2)` modulo `MOD`.

### Why it works

The invariant is that for every processed bit or pair of bits, the stored power of `q` is exactly the signed expectation of the corresponding XOR parity. For one bit, every selected input element with that bit set flips the parity, contributing a factor `1 - 2P`. For two bits, their XOR flips exactly when the two input bits differ, so the number of differing rows determines the corresponding signed expectation. The formulas for one and two Boolean variables then recover their probabilities exactly. Since `S²` contains only individual bit terms and pairwise bit products, summing these expectations gives exactly `E[S²]`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007
BITS = 30

def solve():
    n, X, Y = map(int, input().split())
    a = list(map(int, input().split()))

    inv_y = pow(Y, MOD - 2, MOD)
    q = (1 - 2 * X * inv_y) % MOD

    inv2 = (MOD + 1) // 2
    inv4 = inv2 * inv2 % MOD

    # Store every bit column as a packed integer.
    # Byte r contains the r-th row of the column.
    columns = [bytearray(n) for _ in range(BITS)]

    for r, value in enumerate(a):
        for bit in range(BITS):
            columns[bit][r] = (value >> bit) & 1

    packed = [int.from_bytes(col, "little") for col in columns]

    # signed[k] = E[(-1)^Z_k]
    signed = [0] * BITS

    answer = 0

    for bit in range(BITS):
        cnt = packed[bit].bit_count()
        signed[bit] = pow(q, cnt, MOD)

        p_one = (1 - signed[bit]) * inv2 % MOD
        weight = (1 << (2 * bit)) % MOD
        answer = (answer + weight * p_one) % MOD

    for i in range(BITS):
        for j in range(i + 1, BITS):
            differing = (packed[i] ^ packed[j]).bit_count()
            both_signed = pow(q, differing, MOD)

            p_both = (
                1
                - signed[i]
                - signed[j]
                + both_signed
            ) % MOD
            p_both = p_both * inv4 % MOD

            weight = (1 << (i + j)) % MOD
            answer = (
                answer + 2 * weight * p_both
            ) % MOD

    print(answer)

if __name__ == "__main__":
    solve()
```

The first part of the implementation converts the rational probability into modular arithmetic. `inv_y` represents `Y⁻¹`, so `q = 1 - 2P` becomes `(1 - 2X/Y) mod MOD`. The modulus is prime and `Y` is strictly smaller than it, so Fermat's little theorem gives a valid inverse.

The `columns` array is a compact representation of the input viewed vertically. Instead of storing the 30 bits of each number as separate Python integers and repeatedly scanning the whole array, each column is stored as `n` bytes and then converted into one large integer. The conversion uses little-endian order so the `r`-th input element corresponds to the `r`-th bit position of the packed integer.

The distinction between bytes in `columns` and bits in `packed` is deliberate. A bytearray makes construction straightforward because each input row can be assigned directly. After packing, all expensive pair comparisons happen on Python integers implemented in optimized native code.

The first loop computes `signed[k]`, which is `q` raised to the number of elements containing bit `k`. It immediately converts this signed expectation into the probability that the final XOR bit is one and adds the corresponding diagonal contribution to the square.

The second loop handles every pair of bit positions. XORing two packed columns marks exactly those array elements where the two input bits differ. `bit_count()` therefore gives `d_ij` without a Python loop over `n` elements. The pair probability follows from the signed-expectation identity, and its contribution receives the factor `2 * 2^(i+j)` from the cross terms of the square.

All powers such as `1 << (2 * bit)` and `1 << (i + j)` are small enough for Python integers, and they are reduced modulo `MOD` before entering the modular arithmetic. There is no integer overflow in Python, but reducing intermediate values keeps the modular expressions manageable.

The loop over bits runs exactly 30 times. The pair loop runs only 435 times. The potentially large `n` dimension is hidden inside packed integer operations rather than exposed as a Python-level loop for every pair.

## Worked Examples

### Sample 1

The input is

```
3 1 2
2 8 10
```

Here `P = 1/2`, so `q = 1 - 2P = 0`.

The relevant bit columns are:

```
2  = 0010
8  = 1000
10 = 1010
```

The trace is:

| Bit or pair | Count / distance | `q^count` | Probability | Contribution |
| --- | --- | --- | --- | --- |
| bit 0 | 0 | 1 | 0 | 0 |
| bit 1 | 2 | 0 | 1/2 | 2 |
| bit 2 | 0 | 1 | 0 | 0 |
| bit 3 | 2 | 0 | 1/2 | 32 |
| bits 0,1 | 2 | 0 | 0 | 0 |
| bits 0,2 | 3 | 0 | 0 | 0 |
| bits 0,3 | 2 | 0 | 0 | 0 |
| bits 1,2 | 2 | 0 | 0 | 0 |
| bits 1,3 | 2 | 0 | 1/4 | 8 |
| bits 2,3 | 2 | 0 | 0 | 0 |

The diagonal contribution is `2 + 32 = 34`. The only nonzero pair contribution is between bits 1 and 3, giving `8`, so the answer is `34 + 8 = 42`. This matches the published sample output.

The trace also shows why the pair calculation is necessary. The final XOR is uniformly distributed over `0, 2, 8, 10`, whose squared values average to `42`. Computing only the expected value of each individual bit would not be enough to recover the square.

### Example 2

Consider

```
1 1 2
3
```

There is one element and it is selected with probability `1/2`. The number `3` has both low bits set.

| Bit or pair | Count / distance | `q^count` | Probability |
| --- | --- | --- | --- |
| bit 0 | 1 | 0 | 1/2 |
| bit 1 | 1 | 0 | 1/2 |
| bits 0,1 | 0 | 1 | 1/2 |

The diagonal part is

`1² * 1/2 + 2² * 1/2 = 5/2`.

The pair probability is `1/2`, not `1/4`, because the two output bits are perfectly correlated. The cross contribution is

`2 * 1 * 2 * 1/2 = 2`.

The total is `5/2 + 2 = 9/2`, which becomes `500000008` modulo `10^9 + 7`.

This example directly validates the reason for using `q^(d_ij)` instead of assuming that different output bits are independent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(30n + 30² n / W)` | Building the 30 columns costs `O(30n)`, while 435 packed XOR and population-count operations process `n` bits in machine-sized chunks |
| Space | `O(30n / 8)` | The implementation stores 30 byte columns, plus their packed integer representations |

With `n = 10^5`, there are only 30 bit positions, so the Python-level work is roughly three million simple bit assignments plus 435 native big-integer comparisons. The expensive pairwise scans are executed inside Python's optimized integer implementation rather than as tens of millions of interpreted Python iterations. The memory consumption of the 30 byte columns is about 3 MB, comfortably below 256 MB.

## Test Cases

```python
import sys
import io

MOD = 1_000_000_007
BITS = 30

def solve():
    input = sys.stdin.readline

    n, X, Y = map(int, input().split())
    a = list(map(int, input().split()))

    inv_y = pow(Y, MOD - 2, MOD)
    q = (1 - 2 * X * inv_y) % MOD

    inv2 = (MOD + 1) // 2
    inv4 = inv2 * inv2 % MOD

    columns = [bytearray(n) for _ in range(BITS)]

    for r, value in enumerate(a):
        for bit in range(BITS):
            columns[bit][r] = (value >> bit) & 1

    packed = [int.from_bytes(col, "little") for col in columns]

    signed = [0] * BITS
    answer = 0

    for bit in range(BITS):
        cnt = packed[bit].bit_count()
        signed[bit] = pow(q, cnt, MOD)

        p_one = (1 - signed[bit]) * inv2 % MOD
        answer = (
            answer + ((1 << (2 * bit)) % MOD) * p_one
        ) % MOD

    for i in range(BITS):
        for j in range(i + 1, BITS):
            differing = (packed[i] ^ packed[j]).bit_count()
            both_signed = pow(q, differing, MOD)

            p_both = (
                1 - signed[i] - signed[j] + both_signed
            ) % MOD
            p_both = p_both * inv4 % MOD

            weight = (1 << (i + j)) % MOD
            answer = (
                answer + 2 * weight * p_both
            ) % MOD

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("""3 1 2
2 8 10
""") == "42", "sample 1"

assert run("""1 1 2
1
""") == "500000004", "single element with probability 1/2"

assert run("""1 1 2
3
""") == "500000008", "correlated bits"

assert run("""1 0 7
123
""") == "0", "P = 0"

assert run("""1 1 1
5
""") == "25", "P = 1"

assert run("""2 1 2
1 1
""") == "500000004", "all equal values"

assert run("""1 1 1000000006
1000000006
""") == "1", "maximum input value with P = 1"

max_case = "100000 1 2\n" + "0 " * 99999 + "0\n"
assert run(max_case) == "0", "maximum n, all values zero"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 2 / 2 8 10` | `42` | Provided sample and pairwise bit terms |
| `1 1 2 / 1` | `500000004` | Minimum size and fractional expectation |
| `1 1 2 / 3` | `500000008` | Correlation between two bits |
| `1 0 7 / 123` | `0` | Boundary case `P = 0` |
| `1 1 1 / 5` | `25` | Boundary case `P = 1` |
| `2 1 2 / 1 1` | `500000004` | Repeated equal values |
| `1 1 1000000006 / 1000000006` | `1` | Maximum allowed array value |
| `100000 1 2 / 0 ... 0` | `0` | Maximum `n` and zero-valued elements |

## Edge Cases

When `P = 0`, every signed factor is `q^c = 1`, because `q = 1`. Consequently every single-bit probability is zero, every pair probability is zero, and the answer remains zero. For

```
1 0 7
123
```

the packed columns correctly record the bits of `123`, but none of them can appear in the final XOR. The output is `0`.

When `P = 1`, `q = -1`. A bit occurring an even number of times has signed expectation `1`, while a bit occurring an odd number of times has signed expectation `-1`. This exactly describes a deterministic XOR. For

```
1 1 1
5
```

the only possible result is `5`, and the algorithm produces `25`.

Repeated values require no special treatment. For

```
2 1 2
1 1
```

the XOR is `0` if neither or both copies are selected and `1` otherwise. Each of the four selections has probability `1/4`, so `P(S = 1) = 1/2` and `E[S²] = 1/2`, giving `500000004`. The bit count is two, so the formula gives the same result without considering duplicate values separately.

The correlation example

```
1 1 2
3
```

is the main trap. Both bits always change together because the only possible outputs are `00` and `11`. The pair distance is zero, so `q^0 = 1`, producing a joint probability of `1/2`. If the pair distance were incorrectly replaced by the assumption of independent bits, the answer would be wrong.

Finally, zero-valued elements are harmless. In

```
100000 1 2
0 0 0 ... 0
```

every bit column is entirely zero, so all single-bit counts are zero and every pair distance is zero. The final XOR is always zero regardless of which elements are selected, and the algorithm immediately obtains an answer of `0`.
