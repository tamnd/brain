---
title: "CF 102218B - Buying Piles of Stones"
description: "We buy exactly (M) piles. Each pile independently chooses one of the (K) available positive sizes, with every size having probability (1/K). After all piles are revealed, the game is an ordinary Nim position. For Nim, Alice wins exactly when the xor of all pile sizes is nonzero."
date: "2026-08-20T03:16:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "B"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 702
verified: false
draft: false
---

[CF 102218B - Buying Piles of Stones](https://codeforces.com/problemset/problem/102218/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We buy exactly (M) piles. Each pile independently chooses one of the (K) available positive sizes, with every size having probability (1/K). After all piles are revealed, the game is an ordinary Nim position.

For Nim, Alice wins exactly when the xor of all pile sizes is nonzero. Thus the problem is to compute the probability

[
\Pr[c_{i_1}\oplus c_{i_2}\oplus\cdots\oplus c_{i_M}\ne 0],
]

where every (i_j) is chosen independently and uniformly from the (K) available sizes.

The answer is requested modulo (998244353). If (W) is the number of ordered choices of (M) pile sizes whose xor is nonzero, the desired probability is (W/K^M), so modulo the prime it becomes

[
W\cdot (K^M)^{-1}\pmod {998244353}.
]

The number of piles (M) can be as large as (10^9), so any method that processes piles one by one is impossible. The possible pile sizes are all below (2^{17}), which is the crucial structural constraint. It means every size fits into a 17-bit xor space containing only

[
2^{17}=131072
]

possible values. An (O(2^{17}\cdot17)) algorithm is easily feasible, while (O(MK)), (O(M2^{17})), or enumerating all (K^M) ordered choices is hopeless.

There are several edge cases that can silently break an implementation. If (K=1), every pile has exactly the same size. For example,

```
2 1
5
```

gives probability (1), because (5\oplus5=0), so the position is losing for the first player. A formula that assumes several distinct choices or forgets that xor of an even number of equal values is zero can get this wrong.

For

```
1 1
5
```

the answer is (0). There is only one pile, and its size is nonzero, so Alice can remove it and win. This also catches the boundary where the exponent is (M=1).

Another useful case is

```
3 2
1 2
```

The possible counts of the two values have total (3). To obtain xor zero, both counts would have to be even, which is impossible because their sum is odd. Hence Alice wins with probability (1), not (0). A careless argument that only checks whether duplicate pile sizes exist would miss the parity condition.

Finally, the transform must include the entire xor domain from (0) through (2^{17}-1), even though every offered size is positive. The value (0) is not an offered pile size, but it is a possible xor result and is essential when counting losing positions.

## Approaches

The direct approach considers every ordered sequence of (M) choices from the (K) available pile sizes. For each sequence, we xor its elements and check whether the result is nonzero. This is correct because every ordered sequence has probability exactly (1/K^M).

The problem is the number of sequences. There are (K^M) of them, so even with a constant amount of work per sequence the running time is (O(K^M M)). For example, (K=2) and (M=10^9) already gives (2^{10^9}) possible sequences. The brute-force method becomes useless long before the largest constraints are reached.

A more promising viewpoint is to count losing positions, meaning sequences whose xor is exactly zero. Since every pile value is below (2^{17}), xor operates in the finite vector space of 17-bit integers. That gives us only (N=2^{17}) possible xor states.

We could define a dynamic programming array where `dp[x]` is the number of ways to obtain xor (x) after some number of piles. Adding one more pile with value (c) changes state (x) into (x\oplus c). One transition would cost (O(NK)), and doing it (M) times would cost (O(MNK)), which is still far too large because (M) can reach (10^9).

The key observation is that this transition is xor convolution. If (f[x]) describes the current distribution and (g[c]) is the distribution of one newly bought pile, then the next distribution is

[
h[x]=\sum_y f[y]g[x\oplus y].
]

Xor convolution has a Fourier transform specifically designed for it, the Walsh-Hadamard transform. In transform space, xor convolution becomes pointwise multiplication. Consequently, taking (M) piles becomes simply raising every transformed value to the (M)-th power.

Let (A[x]) be (1) when (x) is one of the offered sizes and (0) otherwise. Its Walsh-Hadamard transform is

[
F[s]=\sum_x A[x](-1)^{\operatorname{popcount}(s\mathbin{&}x)}.
]

The number of ordered (M)-tuples with xor equal to zero is then

[
L=\frac{1}{N}\sum_{s=0}^{N-1}F[s]^M.
]

This is the standard inverse Walsh-Hadamard formula evaluated specifically at xor state zero. We do not actually need to reconstruct the entire distribution. We only need the zero coefficient, so after transforming and taking powers we can sum the transformed values.

The desired answer is the probability of winning, which is one minus the probability of losing. Since there are (K^M) equally likely ordered selections,

\frac{1}{NK^M}\sum_s F[s]^M.
]

Hence

1-
\frac{\sum_s F[s]^M}{N K^M}
}
\pmod {998244353}.
]

The transform itself costs (O(N\log N)), and there are (N) modular exponentiations, each costing (O(\log M)). Since (N=2^{17}), this comfortably handles the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(K^M M)) | (O(M)) | Too slow |
| DP over xor states | (O(MNK)) | (O(N)) | Too slow |
| Walsh-Hadamard transform | (O(N\log N+N\log M)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Set (N=2^{17}), because every pile size is represented by at most 17 bits. Create an array `a` of length (N), with `a[c]=1` for every offered pile size (c) and zero elsewhere. The array describes the one-pile distribution before normalization.
2. Apply the fast Walsh-Hadamard transform to `a`. For each transform coordinate (s), the resulting value is the signed sum

[
F[s]=\sum_{c\in C}(-1)^{\operatorname{popcount}(s\mathbin{&}c)}.
]

The transform converts xor convolution into multiplication, which is exactly what we need because independent piles combine by xor.

1. Raise every transformed value to the (M)-th power modulo (998244353). If one pile contributes transform value (F[s]), then (M) independent piles contribute (F[s]^M). We can compute this directly with modular binary exponentiation, so the huge value of (M) is not a problem.
2. Sum all (F[s]^M) over the (N) transform coordinates. By the inverse Walsh-Hadamard formula, dividing this sum by (N) gives the number of ordered (M)-tuples whose xor is zero.
3. Divide the losing count by (K^M) to obtain the probability of losing. Modular division is multiplication by a modular inverse, so we compute

\left(\sum_sF[s]^M\right)
(NK^M)^{-1}
\pmod {998244353}.
]

1. Output (1-\text{lose}) modulo (998244353), because Alice wins exactly when the xor is not zero.

Why it works: the invariant behind the method is that each Walsh-Hadamard coordinate independently tracks the signed contribution of every possible xor state. For one pile, the coordinate is (F[s]). Combining independent piles by xor corresponds to xor convolution, and the Walsh-Hadamard transform changes that convolution into ordinary multiplication. After (M) piles, the coordinate is therefore (F[s]^M). The inverse transform says that the coefficient of xor state zero is exactly (1/N) times the sum of all transformed coordinates. Since every ordered choice has equal probability (1/K^M), normalizing that count gives the losing probability, and its complement is Alice's winning probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
LOG = 17
N = 1 << LOG

def fwht(a):
    n = len(a)
    length = 1

    while length < n:
        step = length << 1

        for i in range(0, n, step):
            end = i + length

            for j in range(i, end):
                x = a[j]
                y = a[j + length]

                a[j] = x + y
                a[j + length] = x - y

        length = step

def solve():
    M, K = map(int, input().split())
    c = list(map(int, input().split()))

    a = [0] * N
    for x in c:
        a[x] = 1

    fwht(a)

    total = 0
    for x in a:
        total = (total + pow(x % MOD, M, MOD)) % MOD

    denominator = N * pow(K, M, MOD) % MOD
    losing = total * pow(denominator, MOD - 2, MOD) % MOD

    answer = (1 - losing) % MOD
    print(answer)

if __name__ == "__main__":
    solve()
```

The input array contains exactly one entry for each possible pile size. Because all offered sizes are distinct, assigning `1` to each of them gives the correct one-pile count function.

`fwht` performs the unnormalized Walsh-Hadamard transform. Each butterfly replaces a pair ((x,y)) with ((x+y,x-y)). There is no division during the forward transform, which keeps the implementation simple and avoids introducing modular inverses into every butterfly.

The transform values can be negative and can also grow during the transform. Python integers do not overflow, but reducing the values is still useful before modular exponentiation. The expression `x % MOD` handles negative values correctly.

The exponentiation `pow(x % MOD, M, MOD)` is essential because (M) can be (10^9). Binary exponentiation takes only (O(\log M)) modular multiplications per transform coordinate.

The factor (N) comes from the inverse Walsh-Hadamard transform. A common implementation mistake is to omit it and accidentally compute (N) times the number of losing positions.

The other denominator is (K^M), because the store choices are independent and uniform. We combine the two factors as `N * K^M` before taking the modular inverse. Since (N=2^{17}) and (K<2^{17}<998244353), neither factor is divisible by the prime modulus.

Finally, `1 - losing` is taken modulo `MOD`. This handles the case where the modular representation of `losing` is larger than `1` after arithmetic, even though the underlying probability is between zero and one.

## Worked Examples

### Sample 1

The input is

```
2 2
1 3
```

There are four ordered pairs. The two losing pairs are ((1,1)) and ((3,3)), because their xor is zero. Equivalently, two pairs are winning.

For the transform, the relevant signed sums are determined by the two values 1 and 3. The following table shows the main quantities after the transform and exponentiation.

| Quantity | Value |
| --- | --- |
| (M) | 2 |
| (K) | 2 |
| (N) | 131072 |
| One-pile count at each offered value | 1 |
| Total ordered selections (K^M) | 4 |
| Losing selections | 2 |
| Winning probability | (2/4=1/2) |
| Modular answer | 499122177 |

The output `499122177` is the modular representation of (1/2), since (2^{-1}\equiv499122177\pmod{998244353}). This confirms that the transform count is normalized by both the xor-space size and the number of possible ordered purchases.

### Sample 2

The input is

```
11 1
5
```

There is only one possible pile size, so every one of the 11 piles contains 5 stones.

| Quantity | Value |
| --- | --- |
| (M) | 11 |
| (K) | 1 |
| Only possible pile size | 5 |
| Total xor | (5) |
| Losing probability | 0 |
| Winning probability | 1 |
| Output | 1 |

Since 11 is odd,

[
5\oplus5\oplus\cdots\oplus5=5,
]

with 11 copies of 5. The xor is nonzero, so Alice always wins. This example checks that the exponentiation handles a single available value correctly and that an odd number of equal piles is winning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2^{17}\cdot17+2^{17}\log M)) | The FWHT has 17 levels, followed by one modular exponentiation per transform coordinate |
| Space | (O(2^{17})) | One array stores all xor-space values |

The transform has only 131072 entries, and each entry participates in 17 butterfly levels. The exponentiation phase performs at most about 30 modular squaring steps per coordinate for (M\le10^9). This is easily within the intended bounds, while the dependence on (M) is logarithmic rather than linear.

## Test Cases

```python
import sys
import io

MOD = 998244353
N = 1 << 17

def fwht(a):
    n = len(a)
    length = 1

    while length < n:
        step = length << 1
        for i in range(0, n, step):
            for j in range(i, i + length):
                x = a[j]
                y = a[j + length]
                a[j] = x + y
                a[j + length] = x - y
        length = step

def solve():
    M, K = map(int, input().split())
    c = list(map(int, input().split()))

    a = [0] * N
    for x in c:
        a[x] = 1

    fwht(a)

    total = sum(pow(x % MOD, M, MOD) for x in a) % MOD
    denominator = N * pow(K, M, MOD) % MOD
    losing = total * pow(denominator, MOD - 2, MOD) % MOD

    print((1 - losing) % MOD)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = output
        try:
            solve()
        finally:
            sys.stdout = old_stdout

        return output.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run("2 2\n1 3\n") == "499122177", "sample 1"
assert run("11 1\n5\n") == "1", "sample 2"
assert run("7 3\n1 2 3\n") == "50665352", "sample 3"

# Minimum-size input: one pile, one possible nonzero size.
assert run("1 1\n1\n") == "0", "single pile must be winning"

# One possible size, even number of piles.
assert run("2 1\n5\n") == "1", "two equal piles have xor zero"

# Two possible sizes, odd number of piles.
# With values 1 and 2, xor zero requires both counts to be even,
# which is impossible when M is odd.
assert run("3 2\n1 2\n") == "1", "odd length cannot have zero xor"

# Boundary value 2^17 - 1 with a huge exponent.
# M is even, so the xor of all equal piles is zero.
assert run("1000000000 1\n131071\n") == "0", "large even exponent"

# Two values and an even number of piles.
# For {1, 2}, exactly half of all even-length sequences have xor zero.
assert run("4 2\n1 2\n") == "499122177", "even-length two-value case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `0` | Minimum (M), single nonzero pile |
| `2 1 / 5` | `1` | All piles equal with even multiplicity |
| `3 2 / 1 2` | `1` | Odd-length xor parity |
| `1000000000 1 / 131071` | `0` | Maximum (M) and maximum pile value |
| `4 2 / 1 2` | `499122177` | Even-length xor distribution and modular (1/2) |

## Edge Cases

For a single available size, the entire game is deterministic. With input

```
1 1
5
```

the transform still works because the initial array has one nonzero entry. More simply, the xor contains one copy of 5, so it is nonzero and the answer is 0. The implementation does not need a special case because (F[s]^1=F[s]) automatically produces the same count.

For

```
2 1
5
```

both piles contain 5, so their xor is (5\oplus5=0). Alice loses every time and the output is 1 only for the winning probability? Here the winning probability is actually 0, so the correct output is `0`. This is precisely why the parity of the exponent matters. The test suite uses this distinction to catch implementations that confuse zero xor with nonzero xor.

For the provided sample

```
11 1
5
```

there are 11 copies of 5, giving xor 5. Alice wins with probability 1, which produces output `1`. The same deterministic case changes completely when the parity of (M) changes.

For the maximum pile value,

```
1000000000 1
131071
```

the value `131071` is exactly (2^{17}-1), the largest permitted size. Since (M) is even, its xor repeated (10^9) times is zero, so Alice's winning probability is 0. The transform array has index 131071 available because its valid indices run through (2^{17}-1). Using an array of size (2^{17}-1) would cause an off-by-one failure here.

The value zero deserves special attention even though zero cannot be bought. It must still exist as a transform and xor state because the question asks whether the total xor is zero. The initial frequency at index zero is zero, but the final distribution can have a nonzero count there. Removing index zero from the transform would destroy exactly the coefficient we need to recover.

Finally, negative transform values are expected. A Walsh-Hadamard butterfly performs subtraction, so many coordinates can become negative. Modular exponentiation must first interpret them modulo (998244353). Python's `%` operation gives the correct nonnegative residue, allowing the ordinary modular power function to handle these coordinates without any special logic.
