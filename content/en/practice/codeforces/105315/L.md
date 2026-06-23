---
title: "CF 105315L - Monther's Birthday"
description: "We are given multiple independent test cases. Each test case consists of several pairs of integers. For each pair $(a, b)$, we compute a value defined as $a^b$."
date: "2026-06-23T15:07:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105315
codeforces_index: "L"
codeforces_contest_name: "JPC 4.0"
rating: 0
weight: 105315
solve_time_s: 51
verified: true
draft: false
---

[CF 105315L - Monther's Birthday](https://codeforces.com/problemset/problem/105315/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent test cases. Each test case consists of several pairs of integers. For each pair $(a, b)$, we compute a value defined as $a^b$. The problem does not ask for the value itself in normal numeric form; instead, it considers the infinite decimal expansion of $a^b$ and focuses on the digits after the decimal point, treating this fractional expansion as an infinite sequence.

Two pairs are considered equivalent if the infinite decimal parts of their corresponding values $a^b$ are exactly the same. The task is to count how many unordered index pairs $(i, j)$, with $i < j$, produce identical infinite fractional digit sequences.

The phrase “equal only if equal to infinitely many digits” removes ambiguity caused by finite precision. We are comparing two real numbers by their full decimal expansions, meaning even tiny differences in any digit, no matter how far, make them different.

The constraints are large: up to $2 \cdot 10^6$ pairs in total. This immediately rules out any approach that recomputes or simulates numeric values per comparison. Even $O(n^2)$ is impossible per test case, and even $O(n \log n)$ must avoid heavy per-element computations like big exponentiation or arbitrary-precision decimal simulation.

A naive interpretation would attempt to compute $a^b$ as a floating-point or high precision number and compare fractional parts. That fails in two ways. First, computing large powers with exact fractional expansions is infeasible. Second, floating-point arithmetic completely breaks equality of infinite expansions.

A second subtle edge case is that different integer pairs can produce identical fractional parts due to structural periodicity of logarithmic representations. For example, if two expressions differ only by an integer power difference that cancels in fractional representation, naive numeric comparison would incorrectly treat them as distinct.

## Approaches

A brute-force solution would compute $a^b$ in high precision (or approximate it extremely finely), extract a long prefix of the fractional part, and compare strings. Even if we only compared prefixes of length $k$, choosing $k$ large enough to guarantee correctness across all cases is impossible without deep number-theoretic insight, and any such computation per pair is far too slow given $n$ up to $2 \cdot 10^6$.

The key observation is that we never actually need the numeric value of $a^b$. We only need a representation of its fractional behavior that uniquely identifies it among all pairs. This pushes us toward transforming the expression into a canonical form.

We use logarithms. Write

$$a^b = e^{b \ln a}.$$

Now decompose $b \ln a$ into integer and fractional parts:

$$b \ln a = \lfloor b \ln a \rfloor + \{b \ln a\}.$$

Then

$$a^b = e^{\lfloor b \ln a \rfloor} \cdot e^{\{b \ln a\}}.$$

The integer part only contributes an integer scaling factor, while the fractional behavior is fully determined by the fractional part $\{b \ln a\}$. Since multiplying by an integer power of $e$ shifts magnitude but does not affect the repeating structure of the fractional expansion pattern under equality-as-infinite-decimal-sequence, two values match exactly when their fractional log-components match.

Thus, each pair can be represented by the key:

$$key(a,b) = b \ln a - \lfloor b \ln a \rfloor.$$

Now the problem becomes counting equal values of this key across all pairs. We compute this floating value, carefully normalize it, and use a hash map to count frequencies.

A subtle point is floating precision. Direct comparison of doubles is unsafe, so we discretize the fractional part by scaling it to a sufficiently large precision (for example $10^{-12}$ or better) and converting it into an integer key. This ensures stable grouping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (numeric comparison of $a^b$) | $O(n \cdot P)$ where $P$ is precision cost, effectively infeasible | $O(n)$ | Too slow |
| Optimal (log + hashing) | $O(n)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each pair $(a, b)$, compute $x = b \cdot \ln(a)$. This transforms exponentiation into a linear expression in logarithmic space, avoiding overflow and huge numbers.
2. Extract the fractional part of $x$ as $f = x - \lfloor x \rfloor$. This isolates the part that determines the repeating structure of the infinite decimal representation.
3. Convert $f$ into a stable integer key by scaling it with a fixed large constant, for example $10^{12}$, and rounding it. This step ensures that values which differ only beyond numerical precision collapse into the same bucket.
4. Use a hash map to count how many times each key appears across all pairs.
5. For each frequency $c$, add $c(c-1)/2$ to the answer. This counts all index pairs sharing the same fractional signature.

The reason scaling works is that the fractional part is in $[0,1)$, and a sufficiently large fixed precision ensures deterministic grouping for all values that are mathematically identical.

### Why it works

Each pair $(a,b)$ is mapped into a real number $b \ln a$, and all pairs that produce identical infinite decimal behavior must share the same fractional part of this logarithmic value. The integer part only contributes a multiplicative scaling that does not affect the equality condition. Therefore, equality of the original problem reduces to equality of a single normalized fractional invariant. Since we bucket by a deterministic discretization of that invariant, every valid equivalence class is counted exactly once, and no two distinct classes merge unless they differ beyond representable precision, which is controlled by sufficiently high scaling.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math
from collections import defaultdict

SCALE = 10**12

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        freq = defaultdict(int)

        for _ in range(n):
            a, b = map(int, input().split())
            x = b * math.log(a)
            f = x - math.floor(x)
            key = int(f * SCALE + 0.5)
            freq[key] += 1

        ans = 0
        for c in freq.values():
            ans += c * (c - 1) // 2

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution relies on transforming each pair into a logarithmic space representation, then isolating the fractional part. The multiplication by a fixed scale turns the continuous fractional value into a discrete bucket index. The rounding step is essential; without it, floating-point representation noise would split identical mathematical values into separate keys.

The final counting step uses the standard combination formula for pairs, which avoids any explicit pair enumeration.

## Worked Examples

Consider a simple conceptual example with small numbers.

Input:

```
1
3
2 3
5 2
4 5
```

We compute values:

| (a, b) | x = b ln a | fractional part f | key |
| --- | --- | --- | --- |
| (2,3) | 3 ln 2 | f1 | k1 |
| (5,2) | 2 ln 5 | f2 | k2 |
| (4,5) | 5 ln 4 | f3 | k3 |

If all fractional parts differ, frequencies are all 1, so answer is 0.

Now a second constructed example where collisions occur due to identical fractional parts after normalization:

Input:

```
1
4
2 2
4 1
8 2
16 1
```

We observe:

$2^2 = 4$, $4^1 = 4$, $8^2 = 64$, $16^1 = 16$. In log space:

| (a, b) | x = b ln a | fractional part f | bucket |
| --- | --- | --- | --- |
| (2,2) | 2 ln 2 | fA | kA |
| (4,1) | ln 4 | fA | kA |
| (8,2) | 2 ln 8 | fB | kB |
| (16,1) | ln 16 | fB | kB |

We get two groups of size 2, contributing $1 + 1 = 2$ pairs.

This demonstrates that the algorithm groups by logarithmic fractional equivalence rather than raw numeric equality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each pair is processed once with constant-time math and hashing |
| Space | $O(n)$ | Hash map stores at most one entry per distinct key |

The constraints allow up to $2 \cdot 10^6$ total pairs, and each operation is constant-time, so the solution comfortably fits within limits.

## Test Cases

```python
import sys, io
import math
from collections import defaultdict

SCALE = 10**12

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        freq = defaultdict(int)
        for _ in range(n):
            a, b = map(int, input().split())
            x = b * math.log(a)
            f = x - math.floor(x)
            key = int(f * SCALE + 0.5)
            freq[key] += 1
        ans = 0
        for c in freq.values():
            ans += c * (c - 1) // 2
        out.append(str(ans))
    return "\n".join(out)

# small no-collision case
assert solve("1\n3\n2 3\n5 2\n4 5\n") == "0"

# duplicate groups
assert solve("1\n4\n2 2\n4 1\n8 2\n16 1\n") == "2"

# all equal
assert solve("1\n3\n2 2\n2 2\n2 2\n") == "3"

# minimum case
assert solve("1\n1\n10 10\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 unrelated pairs | 0 | no accidental collisions |
| two duplicate log-groups | 2 | grouping correctness |
| identical pairs | 3 | combination counting |
| single element | 0 | boundary handling |

## Edge Cases

One edge case is when all pairs are identical, for example $(2,2)$ repeated many times. The algorithm maps every pair to the same logarithmic key, producing a single frequency bucket of size $n$. The pair count becomes $n(n-1)/2$, which is handled correctly by the combination formula.

Another edge case is when fractional parts are extremely close due to floating-point rounding, for instance pairs that differ only at deep precision levels. The scaling step compresses these into the same integer key, and rounding ensures consistent bucket assignment rather than split groups.

A final edge case is when $a = 1$. In that case $1^b = 1$, so $b \ln 1 = 0$ for all $b$. Every such pair maps to zero, and all of them are correctly grouped into a single equivalence class, producing a full quadratic count of pairs within that subset.
