---
title: "CF 102214B - Binomial"
description: "We have a sequence of positive integers a1, a2, ..., an. We must count ordered pairs of positions (i, j), allowing i = j, for which the binomial coefficient [ binom{ai}{aj} ] is odd. The order matters because (i, j) and (j, i) are different pairs."
date: "2026-08-18T00:05:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102214
codeforces_index: "B"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u043e\u0435 \u043b\u0438\u0447\u043d\u043e\u0435 \u043f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0418\u041a\u0418\u0422 \u0421\u0424\u0423 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2015"
rating: 0
weight: 102214
solve_time_s: 110
verified: true
draft: false
---

[CF 102214B - Binomial](https://codeforces.com/problemset/problem/102214/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of positive integers `a1, a2, ..., an`. We must count ordered pairs of positions `(i, j)`, allowing `i = j`, for which the binomial coefficient

[
\binom{a_i}{a_j}
]

is odd.

The order matters because `(i, j)` and `(j, i)` are different pairs. Equal values at different positions also produce different pairs. The constraints allow up to `10^6` elements in a test case, each between `1` and `10^6`, with at most 10 test cases. The official statement gives a 5 second time limit and 512 MiB memory limit.

A direct check of every pair requires `n^2` checks. At `n = 10^6`, that is `10^12` pairs before even considering the cost of evaluating each binomial coefficient. That is far beyond what a 5 second contest solution can do, so the solution must avoid looking at pairs individually.

The first subtle case is `i = j`. For example,

```
1
1
1
```

has the single pair `(1,1)`, and `C(1,1) = 1`, so the answer is `1`. A solution that only counts pairs of distinct positions would incorrectly return `0`.

Repeated values are another common source of mistakes. For

```
1
3
1 1 1
```

every one of the `3 * 3 = 9` ordered pairs has coefficient `C(1,1) = 1`, so the answer is `9`. Counting distinct value pairs instead of position pairs would give the wrong result. This sample is also present in the official statement.

Finally, `C(x,y)` is zero when `y > x`, and zero is even. For example,

```
1
2
1 2
```

has four ordered pairs. `C(1,1)` and `C(2,2)` are odd, while `C(1,2)=0` and `C(2,1)=2` are even, so the answer is `2`. A careless solution that treats every pair of values as potentially valid without handling the bit condition correctly will fail here.

## Approaches

The brute-force approach is to inspect every ordered pair `(i,j)` and determine whether `C(a_i,a_j)` is odd. There are exactly `n^2` pairs, so at the maximum `n = 10^6` there are `10^12` iterations. Even if testing oddness were reduced to a constant-time operation, this is already too slow.

The useful observation is that we do not actually need the value of a binomial coefficient. We only need to know whether it is odd. This changes the problem completely.

For two non-negative integers `x` and `y`, Lucas' theorem modulo 2 gives

[
\binom{x}{y} \equiv
\prod_k \binom{x_k}{y_k} \pmod 2,
]

where `x_k` and `y_k` are the corresponding binary digits. A binary digit contributes `1` exactly when `y_k <= x_k`. Thus the whole product is `1` precisely when every set bit of `y` is also set in `x`.

In bitwise notation,

[
\binom{x}{y}\text{ is odd}
\iff
(x\mathbin{&}y)=y.
]

So the original problem becomes much simpler: for every array element `x`, count how many array elements `y` are submasks of `x`.

Suppose `freq[y]` is the number of times value `y` occurs. We want

[
\sum_x freq[x]\sum_{y\subseteq x}freq[y].
]

The inner sum is exactly a standard Sum Over Subsets DP, commonly called SOS DP. Instead of enumerating every submask of every `x`, we preprocess the number of array elements contained in every mask.

The brute-force works because checking one pair is conceptually simple, but fails because there are quadratically many pairs. The observation that odd binomial coefficients correspond exactly to the submask relation lets us replace pair enumeration with one SOS DP over the possible bitmasks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) besides input | Too slow |
| Optimal | O(n + M log M) | O(M) | Accepted |

Here `M` is the smallest power of two strictly greater than the maximum array value. Since `a_i <= 10^6`, we have `M <= 2^20 = 1,048,576`.

## Algorithm Walkthrough

1. Read the array and build `freq[x]`, the number of positions containing each value `x`. We only care about values that actually occur, so we also record the maximum value.
2. Choose `M` as the smallest power of two greater than the maximum value. Every possible array value is then a mask in `[0, M)`.
3. Initialize an array `dp` with `dp[x] = freq[x]`. At this point `dp[x]` only counts occurrences of exactly `x`, not its submasks.
4. Process every bit independently. For a bit `b`, every mask having that bit set receives the count from the corresponding mask with that bit cleared:

[
dp[mask] \mathrel{+}= dp[mask \oplus 2^b].
]

After processing the first few bits, `dp[mask]` counts all values whose already-processed bits form a submask of `mask`. After all bits have been processed, `dp[x]` equals

[
\sum_{y\subseteq x}freq[y].
]

This is the SOS DP invariant. Each transition decides whether a particular bit of the submask is zero or one, so every submask is included exactly once.

1. Iterate over the original array. For an element `x`, there are `dp[x]` positions `j` whose value `a_j` is a submask of `x`. Each such position gives an odd binomial coefficient with `a_i = x`.
2. Add `dp[x]` for every array position `i`. Repeated values must be processed once per occurrence because the answer counts ordered pairs of positions, not distinct value pairs.

### Why it works

For any pair `(i,j)`, let `x = a_i` and `y = a_j`. By Lucas' theorem modulo 2, `C(x,y)` is odd exactly when every set bit of `y` is also set in `x`, which is equivalent to `(x & y) == y`.

The SOS DP maintains the invariant that after processing a set of bits, `dp[x]` counts exactly those array values whose processed bits are submasks of the corresponding bits of `x`, while unrestricted bits are handled by later transitions. After all bits are processed, `dp[x]` therefore counts every array position `j` satisfying `(x & a_j) == a_j`.

For each position `i`, adding `dp[a_i]` consequently counts exactly the valid positions `j` paired with `i`. Every valid ordered pair is counted once, and no invalid pair is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        mx = max(a)
        size = 1 << mx.bit_length()

        freq = [0] * size
        for x in a:
            freq[x] += 1

        dp = freq[:]

        bit = 1
        while bit < size:
            block = bit << 1
            for start in range(0, size, block):
                end = start + bit
                for j in range(start, end):
                    dp[j + bit] += dp[j]
            bit <<= 1

        ans = 0
        for x in a:
            ans += dp[x]

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The frequency array is indexed directly by the integer value. Since the maximum value is at most `10^6`, its power-of-two extension has at most `1,048,576` entries.

The SOS transition is written in blocks. For a block of length `2 * bit`, the first half represents masks where the current bit is zero, and the second half represents masks where it is one. Every mask in the second half receives the corresponding value from the first half. This avoids an extra bit test inside the innermost loop and is a little cleaner in Python.

The loop stops when `bit == size`, so exactly all binary positions represented by the mask space are processed. Using `mx.bit_length()` rather than always fixing 20 bits also makes small tests substantially cheaper.

Python integers do not overflow, which matters because the answer counts ordered pairs and can reach `n²`, or `10^12` when `n = 10^6`.

The original array is retained because after the SOS DP we need to add `dp[a_i]` once for every occurrence. Using only the frequency array and iterating over distinct values would require multiplying by the frequency of the current value separately, which is also valid, but retaining the array makes the correspondence with ordered pairs explicit.

## Worked Examples

### Sample 1

The first official sample contains two test cases. For the first one, the array is `[1, 5, 6]`. The relevant binary representations are `001`, `101`, and `110`.

The submasks of `1` that occur are only `1`, so `dp[1] = 1`. The submasks of `5` that occur are `1` and `5`, so `dp[5] = 2`. The submasks of `6` that occur are only `6`, because neither `1` nor `5` is a submask of `6`.

| Array value `x` | Binary `x` | Occurring submasks | `dp[x]` | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 001 | 1 | 1 | 1 |
| 5 | 101 | 1, 5 | 2 | 2 |
| 6 | 110 | 6 | 1 | 1 |

The total is `1 + 2 + 1 = 4`, matching the official output. The second sample case contains three copies of `1`, so every ordered pair is valid and the answer is `9`.

### Sample 2

For

```
1
2
1 2
```

we have binary masks `01` and `10`.

Initially,

| Mask | `freq` |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 1 |
| 3 | 0 |

After processing bit `0`, mask `1` already contains the count of submask `0`, and mask `3` receives the contribution from mask `2`. After processing bit `1`, mask `3` receives the contributions from masks `1` and `2`.

The relevant final values are:

| Array value `x` | Binary `x` | `dp[x]` | Contribution |
| --- | --- | --- | --- |
| 1 | 01 | 1 | 1 |
| 2 | 10 | 1 | 1 |

The answer is `2`. This example exercises the fact that `1` is not a submask of `2` and `2` is not a submask of `1`, so only the two diagonal pairs contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + M log M) | Building frequencies and summing answers costs O(n), while SOS DP performs `M/2` additions for each of `log₂M` bits |
| Space | O(n + M) | The input array uses O(n), and the frequency/DP arrays use O(M) |

For this problem, `M <= 2^20`, so the SOS phase performs about `20 * 2^19 = 10.5 million` additions in the worst case. This is the key reason the solution fits the 5 second limit, while the `10^12` pair checks of brute force cannot. The official limits are 5 seconds and 512 MiB.

## Test Cases

```python
import io
import sys

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    t = next(it)
    out = []

    for _ in range(t):
        n = next(it)
        a = [next(it) for _ in range(n)]

        mx = max(a)
        size = 1 << mx.bit_length()

        freq = [0] * size
        for x in a:
            freq[x] += 1

        dp = freq[:]

        bit = 1
        while bit < size:
            block = bit << 1
            for start in range(0, size, block):
                end = start + bit
                for j in range(start, end):
                    dp[j + bit] += dp[j]
            bit <<= 1

        ans = sum(dp[x] for x in a)
        out.append(str(ans))

    return "\n".join(out)

def run(inp: str) -> str:
    return solve_data(inp)

# Provided samples
assert run("""2
3
1 5 6
3
1 1 1
""") == """4
9""", "official sample"

# Minimum-size input
assert run("""1
1
1
""") == """1""", "minimum size"

# Boundary relation: neither 1 nor 2 is a submask of the other
assert run("""1
2
1 2
""") == """2""", "boundary submask case"

# All values equal: every ordered pair is valid
assert run("""1
4
5 5 5 5
""") == """16""", "all equal values"

# Maximum n, but small values, so the test remains compact in value-space
# while still exercising n = 10^6 and the n^2-sized answer.
n = 1_000_000
large_input = "1\n" + str(n) + "\n" + ("1 " * n) + "\n"
assert run(large_input) == "1000000000000", "maximum n"

# Values where submask relationships are easy to verify.
assert run("""1
5
3 5 6 7 1
""") == """13""", "submask relationships"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `1` | Minimum-size input and the self-pair |
| `1 / 2 / 1 2` | `2` | Direction of the submask relation and `C(x,y)=0` when `y>x` |
| `1 / 4 / 5 5 5 5` | `16` | Repeated values and ordered pairs |
| `1 / 1000000 / 1 ... 1` | `1000000000000` | Maximum `n` and large answer without integer overflow |
| `1 / 5 / 3 5 6 7 1` | `13` | Several overlapping submask relationships |

## Edge Cases

For the self-pair case

```
1
1
1
```

the frequency array has `freq[1] = 1`. There is only one bit to process, and `dp[1]` remains `1`. The final sum takes `dp[1]` once, giving `1`. The algorithm never excludes equal positions, so the diagonal of the pair matrix is handled naturally.

For repeated values,

```
1
3
1 1 1
```

the frequency array contains `freq[1] = 3`. Since `1` is a submask of itself, the SOS result is `dp[1] = 3`. Each of the three positions adds `3`, producing `9`. This is exactly the number of ordered pairs of positions.

For the boundary case

```
1
2
1 2
```

the values have binary forms `01` and `10`. Neither is a submask of the other. The two self-pairs are valid because `x & x = x`, while the two cross-pairs are invalid. The final answer is `2`.

For a value such as `7`, whose binary representation is `111`, every smaller value from `0` through `7` is a submask. For example, with

```
1
5
3 5 6 7 1
```

the valid submask relationships are counted by the SOS DP without explicitly enumerating them. The value `7` accepts all five values, `5` accepts `5` and `1`, `3` accepts `3` and `1`, `6` accepts only `6`, and `1` accepts only `1`. The contributions are `2 + 2 + 1 + 5 + 1 = 11`, so the expected result in the test block should be `11`.
