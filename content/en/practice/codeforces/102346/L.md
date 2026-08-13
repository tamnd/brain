---
title: "CF 102346L - Less Coin Tosses"
description: "We have all binary strings of length (N), representing the possible results of (N) tosses of the same possibly biased coin. Carla and Daniel must assign every chosen string to at most one of them, while some strings may remain unused."
date: "2026-08-14T02:08:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "L"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 90
verified: true
draft: false
---

[CF 102346L - Less Coin Tosses](https://codeforces.com/problemset/problem/102346/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have all binary strings of length (N), representing the possible results of (N) tosses of the same possibly biased coin. Carla and Daniel must assign every chosen string to at most one of them, while some strings may remain unused. The assignment is fair if, for every possible bias of the coin, the total probability of obtaining a Carla string equals the total probability of obtaining a Daniel string.

The task is to minimize the number of unused strings. The official problem has (2 \le N \le 10^{18}), with a one-second time limit, so an algorithm that depends on the (2^N) possible strings is impossible. Even an (O(N)) algorithm is too slow in the worst case because (N) can be (10^{18}). We need a solution whose running time depends only on the number of binary digits of (N).

The key difficulty is that the coin is not necessarily fair. A string with (k) ones does not have the same probability as a string with a different number of ones. However, every string with exactly (k) ones has the same probability. There are exactly (\binom Nk) such strings.

Suppose the coin produces a tail with probability (p). A string containing (k) ones and (N-k) zeroes has probability

[
p^k(1-p)^{N-k}.
]

Let (c_k) be the number of strings with (k) ones assigned to Carla, and (d_k) the corresponding number assigned to Daniel. Fairness means

[
\sum_{k=0}^{N}(c_k-d_k)p^k(1-p)^{N-k}=0
]

for every possible (p).

The functions (p^k(1-p)^{N-k}) form the Bernstein basis of degree (N), so they are linearly independent. Consequently,

[
c_k=d_k
]

for every (k). This is the central reduction: strings with the same number of ones can only be balanced against other strings with the same number of ones.

For a fixed (k), there are (\binom Nk) available strings. If this number is even, we can give half to Carla and half to Daniel. If it is odd, equal integer counts are impossible, so at least one string must remain unused. This gives

[
\text{answer}=\sum_{k=0}^{N}\binom Nk\bmod 2.
]

The remaining problem is purely combinatorial: count the odd entries in row (N) of Pascal's triangle.

A careless implementation might try to generate all strings. For (N=3), there are only eight strings, so this appears harmless and gives the correct answer (4). But for (N=60), there are already (2^{60}) strings, and for (N=10^{18}) the number is beyond any practical computation.

Another edge case is (N=2). The binomial coefficients are (1,2,1). The two outer classes each contain one string and must leave that string unused, while the middle class can be split equally. The correct output is therefore (2). A solution that simply divides every binomial coefficient by two would incorrectly obtain zero.

A useful boundary case is (N=8). Pascal's row begins

[
1,8,28,56,70,56,28,8,1.
]

Only the two outer coefficients are odd, so exactly two strings must remain unused. The correct output is (2). This case also exposes solutions that count odd coefficients incorrectly when (N) is a power of two.

## Approaches

The brute-force approach follows directly from the reduction. We could enumerate all (2^N) binary strings, count their number of ones, and inspect the parity of the resulting frequency for every (k). If the number of ones in each string is computed by inspecting its (N) positions, this takes (\Theta(N2^N)) elementary bit inspections. Even with a smarter enumeration that maintains the number of ones incrementally, the (2^N) states alone make the approach infeasible.

The brute force works because the problem has been reduced to counting how many strings exist in every Hamming-weight class. It fails because the number of strings grows exponentially with (N).

The observation that unlocks the faster solution is that we do not actually need the binomial coefficients themselves. We only need to know whether each coefficient is odd.

Consider Pascal's triangle modulo (2). The number of odd coefficients in row (N) has a remarkably simple form:

[
2^{\operatorname{popcount}(N)},
]

where (\operatorname{popcount}(N)) is the number of set bits in the binary representation of (N).

One way to derive this is to work modulo (2). Write

[
N=2^{b_1}+2^{b_2}+\cdots+2^{b_r},
]

where (r=\operatorname{popcount}(N)). Over modulo (2),

[
(1+x)^{2^b}=1+x^{2^b}.
]

Thus

\prod_{i=1}^{r}(1+x^{2^{b_i}}).
]

When the product is expanded, every factor contributes either (1) or its power of (x). Since the powers (2^{b_i}) are distinct, every subset produces a distinct exponent. There are exactly (2^r) subsets, so exactly (2^r) coefficients are odd.

Since every odd binomial coefficient forces one unused string and every even coefficient can be split perfectly, the minimum number of unused strings is exactly

[
\boxed{2^{\operatorname{popcount}(N)}}.
]

The connection between the brute-force and optimal approaches is therefore quite direct. Brute force asks which entries of Pascal's row are odd by constructing the row implicitly through all strings. The optimal solution skips the entire row and reads the answer directly from the binary representation of (N).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N2^N)) | (O(N)) | Too slow |
| Optimal | (O(\log N)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (N). We only need its binary representation, because the number of odd binomial coefficients depends on the number of set bits in (N).
2. Count the set bits of (N). This gives (\operatorname{popcount}(N)). In Python, `int.bit_count()` performs exactly this operation.
3. Compute (2^{\operatorname{popcount}(N)}). Each set bit of (N) contributes an independent binary choice in the modulo-(2) expansion of ((1+x)^N), so (r) set bits create (2^r) odd coefficients.
4. Print the result. Python integers have arbitrary precision, so there is no overflow even when (N=10^{18}).

### Why it works

For every possible number (k) of ones, fairness requires Carla and Daniel to receive exactly the same number of strings from the class containing (k) ones. If (\binom Nk) is even, that class can be divided perfectly. If it is odd, one string is necessarily left unused, and one unused string is sufficient.

Hence the optimum equals the number of odd coefficients in row (N) of Pascal's triangle. The modulo-(2) identity

[
(1+x)^N=\prod_{i:\text{bit}_i(N)=1}(1+x^{2^i})
]

contains exactly two choices for every set bit of (N), producing exactly (2^{\operatorname{popcount}(N)}) distinct terms. Thus exactly that many binomial coefficients are odd, and exactly that many strings must remain unassigned.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    print(1 << n.bit_count())

if __name__ == "__main__":
    solve()
```

The input is a single integer, so `solve()` reads it directly and computes the answer from its set-bit count.

The expression `n.bit_count()` gives (\operatorname{popcount}(N)). The expression `1 << k` is exactly (2^k), so it avoids a floating-point power operation and keeps the computation entirely integral.

There is no loop over (N), no construction of Pascal's triangle, and no enumeration of binary strings. Since (N\le10^{18}), its binary representation has at most 60 bits, so even explicitly counting bits would take only a few dozen iterations.

The upper bound also causes no overflow in Python. The answer is at most (2^{60}), because an integer up to (10^{18}) has at most 60 set bits. Python's arbitrary-precision integers handle this directly.

## Worked Examples

The official samples are (N=3), (N=5), and (N=8), with outputs (4), (4), and (2), respectively.

For the first sample, (N=3) has binary representation (11_2), so it contains two set bits.

| (N) | Binary (N) | Set-bit count | Answer |
| --- | --- | --- | --- |
| 3 | 11 | 2 | (2^2=4) |

The corresponding Pascal row is (1,3,3,1), and all four coefficients are odd. Each class therefore requires one unused string, giving four unused strings in total.

For the second sample, (N=5) is (101_2), again with two set bits.

| (N) | Binary (N) | Set-bit count | Answer |
| --- | --- | --- | --- |
| 5 | 101 | 2 | (2^2=4) |

Pascal's row is

[
1,5,10,10,5,1.
]

The odd coefficients are the first, second, fifth, and last entries, so there are four of them. The algorithm obtains the same value without constructing the row.

For the third sample, (N=8) is (1000_2), containing only one set bit.

| (N) | Binary (N) | Set-bit count | Answer |
| --- | --- | --- | --- |
| 8 | 1000 | 1 | (2^1=2) |

Only two binomial coefficients are odd in row eight, namely the two outer coefficients. Every other class contains an even number of strings and can be divided equally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log N)) | Counting the set bits examines at most the binary digits of (N). |
| Space | (O(1)) | Only the input integer and the resulting integer are stored. |

For (N\le10^{18}), there are at most 60 binary digits. The algorithm consequently performs only a constant-sized amount of work for the given constraint range, rather than touching any of the (2^N) possible strings.

## Test Cases

```python
import sys
import io

def solve_value(n: int) -> str:
    return str(1 << n.bit_count())

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n = int(sys.stdin.readline())
        return solve_value(n) + "\n"
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("3\n") == "4\n", "sample 1"
assert run("5\n") == "4\n", "sample 2"
assert run("8\n") == "2\n", "sample 3"

# Minimum-size input
assert run("2\n") == "2\n", "minimum N"

# Maximum-size input
assert run("1000000000000000000\n") == "16777216\n", "maximum N"

# Power of two, only one set bit
assert run("16\n") == "2\n", "power of two"

# Three set bits
assert run("7\n") == "8\n", "three set bits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `2` | Minimum allowed (N) and the smallest nontrivial Pascal row |
| `1000000000000000000` | `16777216` | Maximum-size input and large integer handling |
| `16` | `2` | Power of two, where exactly one binomial coefficient at each end is odd |
| `7` | `8` | Three set bits and the (2^{\operatorname{popcount}(N)}) rule |

## Edge Cases

For the minimum input (N=2), the binary representation is (10_2), so the algorithm counts one set bit and returns (2^1=2). Directly, Pascal's row is (1,2,1), giving two odd coefficients. The two corresponding singleton classes cannot be split between the players, so two strings must remain unused.

For (N=3), the binary representation is (11_2), giving two set bits and output (4). The binomial coefficients are (1,3,3,1), all odd. Every Hamming-weight class has an odd number of strings, so each class contributes exactly one unused string. This gives four unused strings, matching the sample.

For a power of two such as (N=8), the binary representation contains exactly one set bit. The answer is (2). This is the smallest possible answer for any valid (N), because the classes (k=0) and (k=N) each contain exactly one string, and those strings can never be assigned to both players simultaneously.

For the maximum input (N=10^{18}), the algorithm never attempts to construct (10^{18}) strings or iterate (10^{18}) times. It only examines the binary representation. The number (10^{18}) has 24 set bits, so the result is

[
2^{24}=16,777,216.
]

The result fits comfortably in Python's integer type, and the computation finishes after processing only the roughly 60 binary digits of (N).
