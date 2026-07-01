---
title: "CF 104377A - \u8ba1\u7b97\u5f02\u6216\u548c"
description: "We are asked to look at all ordered arrays of length $m$ consisting of non-negative integers whose total sum is fixed to $n$. Every such array contributes a value equal to the bitwise XOR of all its elements, and we need the sum of these XOR values over all valid arrays."
date: "2026-07-01T17:21:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104377
codeforces_index: "A"
codeforces_contest_name: "The 21st Sichuan University Programming Contest"
rating: 0
weight: 104377
solve_time_s: 87
verified: true
draft: false
---

[CF 104377A - \u8ba1\u7b97\u5f02\u6216\u548c](https://codeforces.com/problemset/problem/104377/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to look at all ordered arrays of length $m$ consisting of non-negative integers whose total sum is fixed to $n$. Every such array contributes a value equal to the bitwise XOR of all its elements, and we need the sum of these XOR values over all valid arrays.

A useful way to picture the input is that we are distributing $n$ identical units into $m$ labeled boxes. Each distribution defines an array $a_1, a_2, \dots, a_m$. For each distribution we compute a second value: we take the binary representation of every $a_i$, XOR them together, and then add that result into a global total.

The constraints are what make this interesting. The sum $n$ can be as large as $10^{15}$, so we cannot enumerate compositions or even store anything proportional to $n$. The number of boxes $m$ is at most 500, which is small enough that per-position combinatorial dynamic programming is plausible. Any solution depending on iterating over all compositions or using DP over $n$ directly is immediately infeasible because even a linear dependence on $n$ would be far too slow.

A naive approach also breaks quickly in subtle ways. For example, if $m = 2$ and $n = 10$, the valid pairs already number 11, and each pair has to be XORed. Scaling this to $n = 10^{15}$ makes brute force completely impossible, but more importantly, even attempting to generate states incrementally by splitting $n$ leads to exponential blowup.

Another common failure case is trying to treat bits independently. If we incorrectly assume each bit of $a_i$ can be assigned independently subject only to a per-bit sum constraint, we ignore carry propagation between bits. For instance, $a_i = 1$ and $a_i = 2$ behave very differently at bit level even though both contribute to multiple bit positions through addition structure.

So the real difficulty is that the condition $\sum a_i = n$ couples all bits through binary carries, while the XOR depends only on per-bit parity of the column values.

## Approaches

A direct brute force strategy would generate all $m$-tuples of non-negative integers summing to $n$, then compute their XOR. This is essentially enumerating all weak compositions of $n$ into $m$ parts. The number of such tuples is $\binom{n+m-1}{m-1}$, which is already astronomically large when $n$ is up to $10^{15}$. Even for small $n$, iterating over all valid tuples is infeasible, and each tuple requires $O(m)$ work to compute XOR.

The key structural observation is that the constraint $\sum a_i = n$ is a binary addition constraint. Each bit position contributes independently to the sum, except for carries. This suggests processing numbers bit by bit, maintaining a carry from lower bits, exactly like digit DP on addition.

However, we are not only counting valid assignments, we are accumulating XOR values. The XOR at a bit position depends only on how many of the $a_i$ have a 1 in that bit, specifically its parity. This lets us separate the problem into per-bit contributions, while still carrying global validity through the addition constraint.

So the solution becomes a DP over binary positions, where each state tracks how many ways we can form partial assignments of bits with a given carry into the next position, and simultaneously accumulates the sum of XOR contributions contributed by already fixed lower bits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $n$ | $O(m)$ | Too slow |
| Bitwise DP with carry | $O(60 \cdot m^2 \cdot \text{carry})$ | $O(m \cdot \text{carry})$ | Accepted |

## Algorithm Walkthrough

We process the binary representation of $n$ from least significant bit to most significant bit. At each bit position, we decide how the $m$ numbers distribute their bits, while respecting that their total sum must match $n$ including carries.

We define a DP state where we track how many ways we can reach a given carry after processing a prefix of bits, and how much XOR contribution has already been accumulated from processed bits.

### Steps

1. We precompute binomial coefficients $C(m, k)$ for all $0 \le k \le m$. This is needed because at each bit we choose exactly how many of the $m$ numbers have a 1 in that position.
2. We initialize a DP table where the initial state has zero carry and zero XOR contribution, representing no processed bits.
3. For each bit position $pos$ from 0 up to about 60, we take the current DP states and try all possible choices of how many ones $k$ appear among the $m$ numbers at this bit.

Choosing $k$ contributes a combinatorial factor $C(m, k)$, since we are selecting which $k$ indices have bit 1.
4. Let the current carry into this bit be $c$, and let $n_{bit}$ be the $pos$-th bit of $n$. The sum of bits at this position across all numbers is $k + c$.

This sum must satisfy the binary addition constraint:

$$k + c \equiv n_{bit} \pmod{2}$$

and the next carry is:

$$c' = \frac{k + c - n_{bit}}{2}$$
5. For each valid transition, we update two quantities. First, the number of ways multiplies by $C(m, k)$. Second, the XOR contribution at this bit is determined by whether $k$ is odd, since XOR of $k$ ones is 1 iff $k$ is odd. If it is 1, we add $2^{pos}$ multiplied by the number of ways contributing to this transition.
6. We accumulate these transitions into the next DP state indexed by $c'$.
7. After processing all bits, the answer is the total XOR contribution over all DP states with zero final carry.

### Why it works

The DP enforces correctness of the sum constraint exactly as binary addition with carry. Every valid tuple corresponds to exactly one sequence of bit choices and carries. The combinatorial factor ensures we count all assignments of 1-bits across the $m$ positions correctly. The XOR accumulation is linear over bits, so contributions from different bit positions never interfere, and can safely be summed during transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, m = map(int, input().split())

    max_c = m

    # precompute binomial coefficients
    C = [[0] * (m + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j] + C[i - 1][j - 1]) % MOD

    # dp[carry] = (ways, xor_sum)
    dp = [[0, 0] for _ in range(m + 1)]
    dp[0][0] = 1

    for bit in range(61):
        ndp = [[0, 0] for _ in range(m + 1)]
        nb = (n >> bit) & 1

        for carry in range(m + 1):
            ways, xs = dp[carry]
            if ways == 0:
                continue

            for k in range(m + 1):
                comb = C[m][k]
                if comb == 0:
                    continue

                total = k + carry
                if (total & 1) != nb:
                    continue

                nc = (total - nb) // 2
                if nc < 0 or nc > m:
                    continue

                nways = ways * comb % MOD

                # xor contribution from this bit
                if k & 1:
                    add_xor = (nways * ((1 << bit) % MOD)) % MOD
                else:
                    add_xor = 0

                ndp[nc][0] = (ndp[nc][0] + nways) % MOD
                ndp[nc][1] = (ndp[nc][1] + xs * comb % MOD + add_xor) % MOD

        dp = ndp

    print(dp[0][1] % MOD)

if __name__ == "__main__":
    solve()
```

The code builds a digit-DP over binary positions of $n$. The binomial table is used to count how many ways we can assign $k$ ones among $m$ positions at each bit. The DP state tracks carry propagation so that the constructed numbers always sum exactly to $n$. The XOR accumulation is split into inherited contributions from previous bits and new contributions from the current bit weighted by $2^{bit}$.

A subtle point is the separation of `ways` and `xor_sum`. The XOR sum depends on how many ways reach a state, so every transition updates both multiplicatively and additively. Mixing these incorrectly is a common source of overcounting.

## Worked Examples

Consider a small case $n = 4, m = 2$. We enumerate valid pairs:

$(0,4), (1,3), (2,2), (3,1), (4,0)$.

We track contributions by bit.

| Pair | XOR |
| --- | --- |
| (0,4) | 4 |
| (1,3) | 2 |
| (2,2) | 0 |
| (3,1) | 2 |
| (4,0) | 4 |

Total is 12.

In DP terms, at each bit we choose how many of the two numbers carry a 1. The carry constraint ensures exactly those pairs whose binary sums match 4 survive through all bits, while XOR contributions are accumulated when exactly one of the two numbers has a 1 at a bit position.

A second example $n = 3, m = 2$ gives pairs $(0,3),(1,2),(2,1),(3,0)$. XOR values are $3,3,3,3$, total 12. Here every valid assignment has exactly one bit contributing at each XOR computation pattern, and the DP correctly counts symmetric contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(60 \cdot m^2 \cdot m)$ | For each bit, each carry state tries all $k$ values |
| Space | $O(m)$ | DP only stores carry states |

The bounds $m \le 500$ and about 60 bits make this feasible. The total transitions are on the order of a few tens of millions, which fits comfortably in time limits in optimized Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return sys.stdout.getvalue() if False else solve_wrapper(inp)

def solve_wrapper(inp: str) -> str:
    import sys
    from io import StringIO
    backup_stdin = sys.stdin
    sys.stdin = StringIO(inp)

    MOD = 10**9 + 7

    def solve():
        n, m = map(int, input().split())

        C = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            C[i][0] = 1
            for j in range(1, i + 1):
                C[i][j] = (C[i - 1][j] + C[i - 1][j - 1]) % MOD

        dp = [[0, 0] for _ in range(m + 1)]
        dp[0][0] = 1

        for bit in range(20):
            ndp = [[0, 0] for _ in range(m + 1)]
            nb = (n >> bit) & 1

            for c in range(m + 1):
                w, x = dp[c]
                if not w:
                    continue
                for k in range(m + 1):
                    comb = C[m][k]
                    if not comb:
                        continue
                    total = k + c
                    if (total & 1) != nb:
                        continue
                    nc = (total - nb) // 2
                    if nc < 0 or nc > m:
                        continue
                    nw = w * comb % MOD
                    add = (nw * ((1 << bit) % MOD)) % MOD if k & 1 else 0
                    ndp[nc][0] = (ndp[nc][0] + nw) % MOD
                    ndp[nc][1] = (ndp[nc][1] + x * comb % MOD + add) % MOD

            dp = ndp

        return str(dp[0][1] % MOD)

    return solve()

# provided sample
assert run("4 2") == "12"

# custom cases
assert run("1 1") == "1", "single configuration"
assert run("2 2") == "4", "symmetric splits"
assert run("0 2") == "0", "all zeros"
assert run("3 1") == "3", "single variable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 2 | 12 | sample correctness |
| 1 1 | 1 | minimal non-zero structure |
| 2 2 | 4 | symmetry in compositions |
| 0 2 | 0 | zero-sum edge case |
| 3 1 | 3 | single-variable degenerate case |

## Edge Cases

For $n = 0$, all arrays are forced to be all zeros. The DP starts with zero carry and immediately propagates only one valid configuration. At every bit, only $k = 0$ is valid, so XOR is always zero and the final output remains zero.

For $m = 1$, there is exactly one variable $a_1 = n$. The DP reduces to tracking a single path where carry is always consistent with $n$, and XOR equals $n$ itself since there is only one value in the XOR.

For large $n$ with sparse binary representation, most DP states are pruned early because carry constraints eliminate invalid transitions. This ensures the algorithm behaves closer to $O(60 \cdot m^2)$ rather than exploring all theoretical carry states.
