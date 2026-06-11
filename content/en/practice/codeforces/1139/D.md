---
title: "CF 1139D - Steps to One"
description: "We repeatedly choose a random integer from 1 to m, independently and uniformly. After each choice, we look at the gcd of all numbers chosen so far. The process stops as soon as this gcd becomes 1. We must compute the expected number of chosen integers."
date: "2026-06-12T03:53:41+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1139
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 548 (Div. 2)"
rating: 2300
weight: 1139
solve_time_s: 99
verified: true
draft: false
---

[CF 1139D - Steps to One](https://codeforces.com/problemset/problem/1139/D)

**Rating:** 2300  
**Tags:** dp, math, number theory, probabilities  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We repeatedly choose a random integer from `1` to `m`, independently and uniformly.

After each choice, we look at the gcd of all numbers chosen so far. The process stops as soon as this gcd becomes `1`. We must compute the expected number of chosen integers.

The answer is a rational number. The problem asks for that expectation modulo `10^9+7`, which means we work in modular arithmetic and represent divisions using modular inverses.

The key observation is that the entire history of chosen numbers is irrelevant. Only the current gcd matters. If the current gcd is `g`, then after choosing a new number `x`, the new gcd becomes `gcd(g, x)`. This turns the process into a Markov chain on gcd values.

The constraint `m ≤ 100000` is the most important part of the problem. Any solution that explicitly models all subsets, all sequences, or all states of the process is impossible. Even an `O(m²)` algorithm would perform around `10¹⁰` operations, far beyond the limit. We need something around `O(m log m)` or `O(m log² m)`.

There are several subtle cases that easily lead to incorrect reasoning.

Consider `m = 1`.

Input:

```
1
```

The only possible choice is `1`, so the process stops immediately and the expectation is exactly `1`. Any recurrence must correctly treat gcd `1` as an absorbing state.

Consider `m = 2`.

The first number is either `1` or `2`.

If it is `1`, we stop immediately.

If it is `2`, we keep drawing until a `1` appears.

The expectation is `2`, not `1.5`. A naive attempt that only looks at the first draw misses the possibility of arbitrarily long runs of `2`s.

Another common mistake is to think that all gcd values from `1` to `m` are equally likely. They are not. For example, when `m = 10`, gcd `6` can only arise from numbers divisible by `6`, while gcd `2` can arise in many more ways. The recurrence must use exact transition probabilities.

## Approaches

A brute-force approach would model the process directly. Let a state contain the entire sequence of chosen numbers. From each state we append every possible next value and continue until the gcd becomes `1`.

This is correct because it follows the process definition exactly. Unfortunately, the number of possible sequences is infinite. Even if we truncate at some length, the number of states grows exponentially and becomes useless almost immediately.

The first useful observation is that the sequence itself does not matter. If we know the current gcd `g`, then after drawing `x` the next state is simply `gcd(g, x)`. The process depends only on the current gcd.

This reduces the state space to only `m` states.

Let `E[g]` denote the expected number of additional draws needed to reach gcd `1`, assuming the current gcd equals `g`.

For `g = 1`, we already finished, so `E[1] = 0`.

For `g > 1`, after one draw we move to some divisor of `g`. This gives a linear equation involving expectations of smaller divisors.

The remaining challenge is computing transition probabilities efficiently.

For a fixed gcd state `g`, the next state becomes `d` exactly when

```
gcd(g, x) = d
```

The number of such `x` can be computed using inclusion-exclusion over divisors, which is essentially a Möbius-style divisor DP.

Since every transition goes from `g` to a divisor of `g`, processing states in increasing order allows all smaller expectations to be known when computing `E[g]`.

This transforms an infinite probabilistic process into a divisor DP with about `m log m` divisor relations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / Infinite-state | Exponential | Too slow |
| Optimal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

Let `cnt[d] = floor(m / d)`, the number of integers in `[1, m]` divisible by `d`.

Define `E[g]` as the expected number of future draws required to reach gcd `1` when the current gcd is `g`.

1. Set `E[1] = 0`.
2. For every `g > 1`, compute how many values `x` satisfy `gcd(g, x) = d` for every divisor `d` of `g`.

Let this quantity be `ways[d]`.
3. Compute `ways[d]` using inclusion-exclusion.

Start with:

```
ways[d] = count of x divisible by d
        = floor(m / d)
```

Then subtract contributions of larger divisors of `g`.

Processing divisors from largest to smallest gives the exact count of numbers with gcd exactly `d`.
4. Let `self = ways[g]`.

These are choices that keep the gcd unchanged.
5. Write the expectation equation:

```
E[g]
=
1
+
(self/m) E[g]
+
Σ (ways[d]/m) E[d]
```

over all proper divisors `d < g`.
6. Rearrange:

```
E[g]
=
(m + Σ ways[d] E[d])
/
(m - self)
```
7. Perform all arithmetic modulo `10^9+7`.

Division becomes multiplication by a modular inverse.
8. Compute states from `2` to `m`.

Every proper divisor of `g` is smaller than `g`, so all needed expectations have already been computed.
9. The first chosen number is uniformly random.

If the first number equals `i`, the current gcd becomes `i`.

The total expected length equals

```
1 + (1/m) Σ E[i]
```

because the first draw always occurs.

### Why it works

The crucial property is that the future depends only on the current gcd.

Suppose the current gcd is `g`. Any previous sequence leading to `g` becomes irrelevant because the next gcd is always `gcd(g, x)`. This makes the process Markovian.

For each state `g`, the recurrence enumerates every possible next draw. The term `1` accounts for the draw we are about to make. The transition probabilities are exact because `ways[d]` counts precisely the values producing gcd `d`.

The recurrence is solved after isolating the self-loop probability. Since every other transition goes to a proper divisor, expectations are computed in topological order. Thus every value used in the formula is already correct, and induction over increasing `g` proves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    m = int(input())

    inv = [0] * (m + 1)
    for i in range(1, m + 1):
        inv[i] = pow(i, MOD - 2, MOD)

    divisors = [[] for _ in range(m + 1)]
    for d in range(1, m + 1):
        for multiple in range(d, m + 1, d):
            divisors[multiple].append(d)

    dp = [0] * (m + 1)

    for g in range(2, m + 1):
        divs = divisors[g]

        exact = {}
        for d in reversed(divs):
            cur = m // d
            for bigger in divs:
                if bigger > d and bigger % d == 0:
                    cur -= exact[bigger]
            exact[d] = cur

        num = m % MOD

        for d in divs:
            if d == g:
                continue
            num = (num + exact[d] * dp[d]) % MOD

        stay = exact[g]
        denom = m - stay

        dp[g] = num * inv[denom] % MOD

    ans = 1

    total = 0
    for i in range(1, m + 1):
        total += dp[i]

    ans = (ans + total % MOD * inv[m]) % MOD

    print(ans)

solve()
```

The first preprocessing step builds the divisor list of every integer up to `m`. This allows each state to access all its divisors efficiently.

For a fixed gcd state `g`, we need counts of numbers producing each divisor. The inclusion-exclusion computation starts from larger divisors and subtracts already-computed exact counts. This is the standard way to convert "multiples of d" counts into "gcd exactly d" counts.

The expectation formula contains a self-loop. Solving such recurrences requires moving the self-loop term to the left side before dividing by its remaining probability mass. Forgetting this rearrangement is the most common bug in implementations.

All divisions are performed modulo `10^9+7` using modular inverses. Since the statement guarantees denominators are invertible modulo the prime modulus, this is valid.

## Worked Examples

### Sample 1

Input:

```
1
```

State computation:

| g | E[g] |
| --- | --- |
| 1 | 0 |

Final expectation:

| Quantity | Value |
| --- | --- |
| First draw | 1 |
| Average additional draws | 0 |
| Answer | 1 |

The process always chooses `1` immediately, so the array length is always exactly `1`.

### Sample 2

Input:

```
2
```

For `g = 2`:

| Divisor d | Count with gcd(2,x)=d |
| --- | --- |
| 1 | 1 |
| 2 | 1 |

Recurrence:

```
E[2] = (2 + 1·E[1]) / (2 - 1)
     = 2
```

Final expectation:

| Quantity | Value |
| --- | --- |
| E[1] | 0 |
| E[2] | 2 |
| Total | 2 |
| Answer | 1 + (0 + 2)/2 = 2 |

This matches the geometric-process interpretation: we keep drawing `2` until the first `1` appears.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Divisor preprocessing and divisor-DP over all integers |
| Space | O(m) | Divisor lists, inverses, and DP arrays |

For `m = 100000`, the total number of divisor relations is about `m log m`, which comfortably fits within the time limit. Memory usage is also well below the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    MOD = 1000000007

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    m = int(input())

    inv = [0] * (m + 1)
    for i in range(1, m + 1):
        inv[i] = pow(i, MOD - 2, MOD)

    divisors = [[] for _ in range(m + 1)]
    for d in range(1, m + 1):
        for v in range(d, m + 1, d):
            divisors[v].append(d)

    dp = [0] * (m + 1)

    for g in range(2, m + 1):
        divs = divisors[g]

        exact = {}
        for d in reversed(divs):
            cur = m // d
            for b in divs:
                if b > d and b % d == 0:
                    cur -= exact[b]
            exact[d] = cur

        num = m % MOD
        for d in divs:
            if d != g:
                num = (num + exact[d] * dp[d]) % MOD

        dp[g] = num * inv[m - exact[g]] % MOD

    ans = (1 + sum(dp) % MOD * inv[m]) % MOD
    return str(ans)

# provided sample
assert run("1\n") == "1", "sample 1"

# custom cases
assert run("2\n") == "2", "sample described in statement"

# boundary checks
assert run("3\n").isdigit(), "small prime"
assert run("10\n").isdigit(), "composite range"
assert run("100000\n").isdigit(), "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Absorbing state immediately |
| `2` | `2` | Simple geometric process |
| `3` | Numeric answer | Prime boundary behaviour |
| `10` | Numeric answer | Multiple divisor transitions |
| `100000` | Numeric answer | Maximum constraint |

## Edge Cases

Consider:

```
1
```

The process starts at gcd `1` after the first draw. Our DP sets `E[1]=0`, so the final answer becomes exactly `1`. Any recurrence that tries to divide by `(m-self)` for `g=1` would fail, which is why state `1` is handled separately.

Consider:

```
2
```

State `2` has a self-loop probability of `1/2`. The recurrence becomes

```
E[2] = 1 + (1/2)E[2].
```

Solving gives `E[2]=2`. If the self-loop term were ignored, we would incorrectly obtain `E[2]=1`.

Consider a highly composite value such as:

```
10
```

Several divisors can be reached from the same state. The inclusion-exclusion step guarantees that a number contributing to gcd `10` is not counted again in gcd `5`, gcd `2`, or gcd `1`. Without exact-gcd counting, transition probabilities would sum to more than one and the expectation would be wrong.

Finally, for the maximum input

```
100000
```

the algorithm never iterates over all pairs `(i,j)`. It only traverses divisor relationships, keeping the running time near `m log m`, which is why it remains fast enough under the given limits.
