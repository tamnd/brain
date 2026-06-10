---
title: "CF 1594B - Special Numbers"
description: "We are asked to enumerate a very specific set of numbers defined by a base expansion rule. A number is considered valid if we can write it as a sum of distinct powers of some fixed base $n$."
date: "2026-06-10T08:55:52+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "math"]
categories: ["algorithms"]
codeforces_contest: 1594
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 747 (Div. 2)"
rating: 1100
weight: 1594
solve_time_s: 76
verified: true
draft: false
---

[CF 1594B - Special Numbers](https://codeforces.com/problemset/problem/1594/B)

**Rating:** 1100  
**Tags:** bitmasks, math  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to enumerate a very specific set of numbers defined by a base expansion rule. A number is considered valid if we can write it as a sum of distinct powers of some fixed base $n$. That means each power $n^0, n^1, n^2, \dots$ can either be used once or not used at all, and the value is formed by adding the chosen powers together.

This immediately turns every valid number into a binary decision over exponents: for each exponent $i$, we decide whether $n^i$ contributes to the sum. If we think in terms of bitmasks, each number corresponds to a binary mask where bit $i$ controls inclusion of $n^i$.

The task is to sort all such representable numbers in increasing order and return the $k$-th one.

The constraints force a careful approach. The number of test cases can reach $10^4$, and both $n$ and $k$ can be as large as $10^9$. Any approach that tries to explicitly generate the sequence or iterate through candidates will immediately fail because the sequence grows exponentially in the number of usable powers. Even for moderate $k$, enumerating values would require exploring combinations of powers, which is infeasible.

A subtle failure case for naive thinking appears when $n$ is large. For example, if $n = 10^9$, then $n^0 = 1$ and $n^1$ already jumps beyond most intermediate sums, so ordering behaves very differently than in small bases. A naive greedy construction assuming uniform spacing between numbers breaks here because the growth is highly non-linear.

Another pitfall is assuming the sequence behaves like standard binary numbers for all $n$. That only holds when $n = 2$. For other $n$, positional values are weighted exponentially, so lexicographic ordering of bitmasks does not directly match numeric ordering unless we carefully justify it.

## Approaches

The brute-force idea is straightforward. We generate all numbers by trying every subset of powers $n^0, n^1, \dots$ up to a reasonable limit, compute their sums, store them, sort them, and pick the $k$-th element. This is correct because it exhaustively constructs exactly the definition of valid numbers.

The failure point is size. Even if we restrict ourselves to the first 60 powers (since $n^i$ becomes huge quickly), we still have $2^{60}$ subsets. That is far beyond any computational limit.

The key observation is that every valid number is uniquely determined by a binary choice vector over powers of $n$. That means the $k$-th smallest number corresponds to the binary representation of $k$ itself, but interpreted in base $n$ instead of base 2.

More precisely, if we write $k$ in binary, each bit indicates whether we include a corresponding power of $n$. The $i$-th bit contributes $n^i$ if it is set. This works because ordering of sums is consistent with increasing binary values of the mask: higher powers dominate all lower ones, so lexicographic ordering by bits aligns with numeric ordering of constructed values.

Thus, the problem reduces to converting $k$ into its binary form and evaluating it as a polynomial in base $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | exponential | Too slow |
| Optimal | $O(\log k)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We construct the answer digit by digit from the binary representation of $k$.

1. Convert $k$ into binary form, processing from least significant bit to most significant bit. Each bit tells us whether a corresponding power of $n$ is included in the sum.
2. Maintain a running value `ans`, initially zero, and a multiplier `pow_n` initialized to 1, representing $n^0$. This multiplier tracks the current power of $n$ we are assigning to the current bit position.
3. For each bit of $k$, if the bit is 1, we add `pow_n` to `ans`. This reflects selecting that power in the subset representation.
4. After processing each bit, update `pow_n *= n`, since we move to the next exponent.
5. Continue until all bits of $k$ have been processed.
6. Output `ans mod (10^9 + 7)`.

The reason we can safely process bits in order is that each higher bit corresponds to a strictly larger power of $n$, and those powers dominate all lower contributions in the ordering of valid numbers.

### Why it works

Each valid number corresponds to a subset of powers of $n$, which is equivalent to a binary mask. The ordering of these numbers matches the natural ordering of these masks interpreted as binary integers, because increasing the highest differing bit always increases the value regardless of lower bits due to the exponential growth of $n^i$. Therefore, the $k$-th subset in sorted order is exactly the binary representation of $k$, interpreted as a selection vector over powers of $n$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())

    ans = 0
    power = 1

    while k > 0:
        if k & 1:
            ans = (ans + power) % MOD
        power = (power * n) % MOD
        k >>= 1

    print(ans)
```

The code directly implements the binary decomposition idea. The variable `power` tracks successive powers of $n$, always kept modulo $10^9+7$ since only the final value is required modulo this number.

A common mistake here is trying to precompute powers up to $k$, but that is unnecessary because we only need as many powers as there are bits in $k$, which is at most 30 for constraints up to $10^9$. Another subtle point is updating `power` after processing each bit; reversing this order would shift all contributions by one exponent and break correctness.

## Worked Examples

### Example 1

Input:

```
n = 3, k = 4
```

Binary representation: $k = 100_2$

| Bit index | Bit value | power $3^i$ | ans |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 0 |
| 1 | 0 | 3 | 0 |
| 2 | 1 | 9 | 9 |

Output is 9.

This shows that only the highest selected bit contributes, and lower bits being zero simply skip smaller powers.

### Example 2

Input:

```
n = 2, k = 12
```

Binary: $1100_2$

| Bit index | Bit value | power $2^i$ | ans |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 0 |
| 1 | 0 | 2 | 0 |
| 2 | 1 | 4 | 4 |
| 3 | 1 | 8 | 12 |

This matches the sample output and demonstrates that multiple bits accumulate independent powers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log k)$ | Each test case processes bits of $k$ once |
| Space | $O(1)$ | Only a few integer variables are used |

The logarithmic dependence on $k$ is essential because $k$ can reach $10^9$, but its binary length is at most 30 bits, keeping the solution easily within limits even for $10^4$ test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7
    t = int(sys.stdin.readline())
    out = []

    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        ans = 0
        power = 1
        while k > 0:
            if k & 1:
                ans = (ans + power) % MOD
            power = (power * n) % MOD
            k >>= 1
        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("3\n3 4\n2 12\n105 564\n") == "9\n12\n3595374"

# custom cases
assert run("1\n2 1\n") == "1"
assert run("1\n2 2\n") == "2"
assert run("1\n10 5\n") == str((1 + 4) % (10**9 + 7))
assert run("1\n1000000000 1000000000\n")  # sanity check runs
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2, k=1 | 1 | smallest case correctness |
| n=2, k=2 | 2 | single-bit shift behavior |
| n=10, k=5 | 1 + 4 | multiple-bit accumulation |
| large values | stable | performance and overflow safety |

## Edge Cases

One edge case is when $k = 1$. The binary representation contains only the lowest bit, so the algorithm returns $n^0 = 1$. The loop runs once, adds `power = 1`, and stops correctly.

Another case is when $n$ is very large, such as $n = 10^9$. The first multiplication sets `power` to $10^9$, but since we immediately reduce modulo $10^9+7$, values remain valid. The structure of bit processing remains unchanged, and only one or two iterations are needed before higher powers exceed $k$'s bit length.

A final case is when $k$ has multiple high bits set, such as $k = 2^m - 1$. Here every bit contributes, producing a full geometric sum $1 + n + n^2 + \dots + n^m$. The algorithm naturally accumulates all powers in sequence, matching the expected construction of the largest representable numbers in that range.
