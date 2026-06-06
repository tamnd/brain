---
title: "CF 294C - Shaass and Lights"
description: "We have a row of n lights. Some positions are already on, and all other positions are off. A move consists of choosing an off light that has at least one adjacent light already on, then switching it on. We continue until every light becomes on."
date: "2026-06-05T17:41:10+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 294
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 178 (Div. 2)"
rating: 1900
weight: 294
solve_time_s: 140
verified: true
draft: false
---

[CF 294C - Shaass and Lights](https://codeforces.com/problemset/problem/294/C)

**Rating:** 1900  
**Tags:** combinatorics, number theory  
**Solve time:** 2m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of `n` lights. Some positions are already on, and all other positions are off.

A move consists of choosing an off light that has at least one adjacent light already on, then switching it on. We continue until every light becomes on.

The task is to count how many different valid sequences of moves exist. Two sequences are considered different if at some step they switch on different positions. The answer must be computed modulo `1000000007`.

The input gives the positions that are initially on. Since `n ≤ 1000`, we are dealing with a relatively small size. An algorithm with exponential behavior is impossible because the number of off lights can be close to 1000. Even an `O(n³)` solution is unnecessary. The constraint strongly suggests a combinatorial counting solution with precomputed factorials and modular arithmetic.

The subtle part of the problem is that the legality of a move depends only on adjacency to already activated lights. This creates dependencies between positions inside each block of initially-off lights.

Several edge cases are easy to mishandle.

Consider:

```
5 2
2 4
```

The off positions form three gaps:

```
1 | 3 | 5
```

Each gap has size 1. Every gap can contribute positions independently, and the answer is not simply `3! = 6`. We must account for the internal constraints of each gap.

Another important case is an internal gap:

```
7 2
2 6
```

The gap between positions 2 and 6 contains:

```
3 4 5
```

This block can be filled from either end. Position 4 cannot be activated first. A naive solution that treats every ordering of these three positions as valid would overcount.

A final corner case occurs when all lights are already on:

```
4 4
1 2 3 4
```

There are no moves to perform. The correct answer is:

```
1
```

There is exactly one empty sequence.

## Approaches

A brute-force solution would simulate all possible valid move sequences. At each state we would find every currently switchable light, recursively try each choice, and continue until all lights are on.

This is correct because it explicitly enumerates every legal sequence. The problem is the number of states. If only one light starts on and the remaining 999 lights are off, the number of valid sequences is enormous. Exhaustive search becomes completely infeasible.

The key observation is that the row naturally splits into independent gaps between initially-on lights.

Suppose the initially-on positions are sorted. Between every consecutive pair of on lights there is a gap of off lights. There may also be a gap before the first on light and after the last on light.

The boundary gaps behave differently from the internal gaps.

For a boundary gap, activation can only expand from one side. If a gap contains `k` positions, the order inside that gap is completely forced.

For example:

```
111000
```

The three rightmost positions must be activated from left to right.

An internal gap is more interesting. Suppose the gap length is `k`.

```
1 0 0 0 1
```

Both ends are adjacent to active lights. At every step we may take the leftmost remaining position or the rightmost remaining position. The process continues until the gap disappears.

For a gap of length `k`, the number of valid internal orders is:

```
2^(k-1)
```

Why? The first `k-1` activations each have two choices, left end or right end. The final position is forced.

After counting valid orders inside each gap, we must merge moves from different gaps. If gap sizes are:

```
g1, g2, ..., gt
```

then the relative ordering of moves from different gaps can be chosen in

$$\frac{(g_1+g_2+\cdots+g_t)!}{g_1!g_2!\cdots g_t!}$$

ways, which is a multinomial coefficient.

The entire answer becomes:

$$\text{multinomial} \times \prod_{\text{internal gaps}} 2^{k-1}$$

This converts the problem into pure combinatorics.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) after factorial precomputation | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the initially-on positions and sort them.
2. Compute every gap length.

The gap before the first on light has length `a[0]-1`.

The gap after the last on light has length `n-a[m-1]`.

Between consecutive on lights `a[i]` and `a[i+1]`, the internal gap length is:

$$a[i+1]-a[i]-1$$
3. Let `off = n - m`, the total number of lights that still need to be activated.
4. Start with:

$$ans = off!$$

This counts all ways to arrange the future activations before considering gap constraints.
5. For every gap of length `k`, divide by `k!`.

This converts `off!` into the multinomial coefficient that counts how activations from different gaps can be interleaved.
6. For every internal gap of positive length `k`, multiply by:

$$2^{k-1}$$

because the gap can shrink from either side until only one position remains.
7. Perform all divisions modulo `10^9+7` using modular inverses.
8. Output the final result.

### Why it works

Every off position belongs to exactly one gap.

Inside a boundary gap, the activation order is uniquely determined because growth can only proceed from the side adjacent to an already-on light.

Inside an internal gap, the only available choices are always the two boundary positions of the remaining interval. Choosing left or right repeatedly completely determines the activation sequence. A gap of length `k` therefore contributes exactly `2^(k-1)` valid internal orders.

Different gaps do not interact except through the global timeline. Once the valid internal order for each gap is fixed, the only remaining freedom is how moves from different gaps are interleaved. The multinomial coefficient counts precisely these interleavings.

Since the answer multiplies the number of valid internal orders by the number of valid interleavings, every legal global sequence is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def main():
    n, m = map(int, input().split())
    a = sorted(map(int, input().split()))

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    gaps = []

    left_gap = a[0] - 1
    gaps.append(left_gap)

    ans = 1

    for i in range(m - 1):
        k = a[i + 1] - a[i] - 1
        gaps.append(k)
        if k > 0:
            ans = ans * pow(2, k - 1, MOD) % MOD

    right_gap = n - a[-1]
    gaps.append(right_gap)

    off = n - m
    ans = ans * fact[off] % MOD

    for k in gaps:
        ans = ans * inv_fact[k] % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The factorial and inverse-factorial arrays allow multinomial coefficients to be computed in constant time per gap.

The variable `ans` first accumulates the contribution from internal gaps. After that we multiply by `off!`, which represents all possible placements of future activations in the global timeline.

Dividing by `k!` for every gap is implemented as multiplication by `inv_fact[k]`. Since the modulus is prime, Fermat's little theorem gives the modular inverse:

$$x^{-1} \equiv x^{MOD-2} \pmod{MOD}$$

A common mistake is multiplying by `2^k` instead of `2^(k-1)` for internal gaps. The last remaining position has no choice, so only the first `k-1` activations contribute binary decisions.

Another frequent bug is applying the power-of-two factor to boundary gaps. Boundary gaps expand from only one side and contribute exactly one internal ordering.

## Worked Examples

### Sample 1

Input:

```
3 1
1
```

The lights are:

```
1 0 0
```

| Quantity | Value |
| --- | --- |
| Left gap | 0 |
| Right gap | 2 |
| Internal gaps | none |
| Off lights | 2 |

Computation:

| Step | Value |
| --- | --- |
| Internal contribution | 1 |
| Multiply by 2! | 2 |
| Divide by 0! | 2 |
| Divide by 2! | 1 |

Final answer:

```
1
```

This demonstrates a pure boundary gap. The activation order is forced.

### Example 2

Input:

```
7 2
2 6
```

Gaps:

```
[1] [3] [1]
```

where the middle gap is internal.

| Quantity | Value |
| --- | --- |
| Left gap | 1 |
| Internal gap | 3 |
| Right gap | 1 |
| Off lights | 5 |

Computation:

| Step | Value |
| --- | --- |
| Internal contribution | 2^(3-1)=4 |
| Multiply by 5! | 480 |
| Divide by 1! | 480 |
| Divide by 3! | 80 |
| Divide by 1! | 80 |

Final answer:

```
80
```

The example shows how an internal gap contributes additional flexibility beyond simple interleavings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Factorial precomputation and gap processing |
| Space | O(n) | Factorial and inverse-factorial arrays |

With `n ≤ 1000`, this solution is easily within the limits. The algorithm performs only a few thousand modular arithmetic operations and uses a few arrays of length at most 1001.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = sorted(map(int, input().split()))

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    gaps = [a[0] - 1]
    ans = 1

    for i in range(m - 1):
        k = a[i + 1] - a[i] - 1
        gaps.append(k)
        if k > 0:
            ans = ans * pow(2, k - 1, MOD) % MOD

    gaps.append(n - a[-1])

    ans = ans * fact[n - m] % MOD

    for k in gaps:
        ans = ans * inv_fact[k] % MOD

    return str(ans)

# provided sample
assert run("3 1\n1\n") == "1"

# all lights already on
assert run("4 4\n1 2 3 4\n") == "1"

# single light
assert run("1 1\n1\n") == "1"

# one internal gap of length 1
assert run("3 2\n1 3\n") == "1"

# internal gap length 2
assert run("4 2\n1 4\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 4 / 1 2 3 4` | `1` | Empty sequence case |
| `1 1 / 1` | `1` | Minimum input size |
| `3 2 / 1 3` | `1` | Internal gap of length one |
| `4 2 / 1 4` | `2` | Verifies `2^(k-1)` contribution |

## Edge Cases

Consider:

```
4 4
1 2 3 4
```

There are no gaps and `off = 0`.

The algorithm computes:

```
0! = 1
```

No power-of-two factors appear. The answer remains `1`, which corresponds to the unique empty sequence.

Consider:

```
4 2
1 4
```

The middle gap has length `2`.

The algorithm computes:

```
2! / 2! × 2^(2-1)
= 2
```

The two valid activation orders are:

```
2,3
3,2
```

This confirms that internal gaps contribute binary choices.

Consider:

```
5 1
3
```

The gaps are:

```
2 and 2
```

Both are boundary gaps.

The answer becomes:

```
4! / (2!2!) = 6
```

No power-of-two factor is added because neither gap is internal. A solution that treated every gap identically would incorrectly multiply by extra powers of two and overcount.
