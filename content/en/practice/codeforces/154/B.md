---
title: "CF 154B - Colliders"
description: "We maintain a set of currently active colliders. Each collider is identified by an integer from 1 to n. The system is safe only if every pair of active colliders is coprime. In other words, no prime factor may appear in two different active numbers at the same time."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 154
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 109 (Div. 1)"
rating: 1600
weight: 154
solve_time_s: 124
verified: true
draft: false
---

[CF 154B - Colliders](https://codeforces.com/problemset/problem/154/B)

**Rating:** 1600  
**Tags:** math, number theory  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a set of currently active colliders. Each collider is identified by an integer from `1` to `n`. The system is safe only if every pair of active colliders is coprime. In other words, no prime factor may appear in two different active numbers at the same time.

Each query either tries to activate a collider or deactivate one. Activating a collider can fail in two different ways. If the collider is already active, we print `"Already on"`. Otherwise we must check whether its number shares a common divisor greater than `1` with any currently active collider. If such a collider exists, activation fails and we print `"Conflict with x"` for any conflicting active collider `x`. If no conflict exists, activation succeeds.

Deactivation is simpler. If the collider is inactive, we print `"Already off"`. Otherwise we remove it from the active set.

The constraints are large enough that pairwise checking cannot work directly. Both `n` and the number of queries are up to `10^5`. A naive solution that scans all active colliders for every activation would perform around `10^10` gcd computations in the worst case, which is far beyond the limit. We need something close to linear or `O(n log n)` overall.

The hidden structure is that conflicts depend entirely on prime factors. Two numbers conflict if and only if they share at least one prime divisor. This turns the problem from pairwise gcd checking into ownership tracking for prime factors.

Several edge cases are easy to mishandle.

Consider activating the same collider twice:

```
5 2
+ 2
+ 2
```

The correct output is:

```
Success
Already on
```

A careless implementation might attempt conflict checking before checking whether the collider is already active. Since `2` obviously shares a factor with itself, it could incorrectly report `"Conflict with 2"`.

Another subtle case happens when a collider has multiple prime factors and conflicts with more than one active collider:

```
10 3
+ 2
+ 3
+ 6
```

The correct output can be either:

```
Success
Success
Conflict with 2
```

or

```
Success
Success
Conflict with 3
```

The problem allows any valid conflicting collider. The implementation should stop at the first detected conflict instead of trying to gather all of them.

A third trap appears during deactivation:

```
10 4
+ 6
- 6
+ 2
+ 3
```

The correct output is:

```
Success
Success
Success
Success
```

If we forget to release the prime factors of `6` after turning it off, both `2` and `3` would incorrectly appear blocked.

## Approaches

The most direct solution stores the set of active colliders and, for every activation request `+ x`, checks `gcd(x, y)` against every active collider `y`.

This works logically because the definition of safety is exactly pairwise coprimality. If all gcd values equal `1`, activation is safe. Otherwise any collider with gcd greater than `1` is a valid conflict.

The problem is performance. In the worst case, almost all colliders stay active, so each activation scans `O(n)` colliders. With `10^5` queries, this becomes roughly `10^10` gcd operations. Even fast gcd implementations cannot handle that volume.

The key observation is that conflicts happen because of shared prime divisors, not because of the numbers themselves. If collider `30` is active, then primes `2`, `3`, and `5` become unavailable. Any future number containing one of those primes must conflict.

This suggests a much faster representation. Instead of tracking pairwise relationships, we track ownership of each prime factor.

Suppose we maintain an array `owner[p]` storing which active collider currently uses prime `p`. To activate `x`, we factorize `x` into distinct primes. If any prime already has an owner, we immediately know a conflict exists. Otherwise we assign all those primes to `x`.

Each number up to `10^5` has only a small number of distinct prime factors, at most about `6`. With precomputed smallest prime factors from a sieve, factorization becomes very fast. Each query now processes only the prime factors of one number instead of scanning all active colliders.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(mn) | O(n) | Too slow |
| Optimal | O(n log log n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the smallest prime factor for every integer from `1` to `n` using a sieve.

This allows fast factorization later. Instead of trial division, we repeatedly divide by the smallest known prime factor.
2. Maintain a boolean array `on[x]` indicating whether collider `x` is currently active.

This handles `"Already on"` and `"Already off"` immediately.
3. Maintain an array `owner[p]` where `owner[p]` stores the active collider currently using prime `p`.

If `owner[p] = 0`, the prime is free.
4. For each query `+ x`, first check whether `x` is already active.

If `on[x]` is true, print `"Already on"`.
5. Otherwise factorize `x` into its distinct prime divisors.

We only need distinct primes because sharing even one prime causes a conflict.
6. For each prime factor `p` of `x`, check `owner[p]`.

If some `owner[p]` is nonzero, activation fails. Print `"Conflict with owner[p]"` and stop processing this query.
7. If no conflicts were found, activate `x`.

Set `on[x] = True` and assign `owner[p] = x` for every prime factor `p` of `x`. Then print `"Success"`.
8. For each query `- x`, first check whether `x` is inactive.

If `on[x]` is false, print `"Already off"`.
9. Otherwise factorize `x` again and release all its prime factors.

For every prime `p` dividing `x`, set `owner[p] = 0`. Then set `on[x] = False` and print `"Success"`.

### Why it works

The algorithm maintains a strong invariant:

For every prime `p`, `owner[p]` is either `0` or the unique active collider divisible by `p`.

When activating `x`, we check all its prime factors. If any factor already has an owner, then `x` shares that prime with an active collider, so the gcd is greater than `1` and activation must fail. If all prime factors are free, then no active collider shares any prime with `x`, which means `x` is coprime with every active collider.

Deactivation restores the invariant by releasing exactly the primes belonging to that collider.

Because every conflict is detected through shared prime factors, and every shared prime factor corresponds to a gcd greater than `1`, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    spf = list(range(n + 1))

    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def get_primes(x):
        primes = []

        while x > 1:
            p = spf[x]
            primes.append(p)

            while x % p == 0:
                x //= p

        return primes

    on = [False] * (n + 1)
    owner = [0] * (n + 1)

    ans = []

    for _ in range(m):
        op, val = input().split()
        x = int(val)

        if op == '+':
            if on[x]:
                ans.append("Already on")
                continue

            primes = get_primes(x)

            conflict = 0

            for p in primes:
                if owner[p] != 0:
                    conflict = owner[p]
                    break

            if conflict:
                ans.append(f"Conflict with {conflict}")
            else:
                on[x] = True

                for p in primes:
                    owner[p] = x

                ans.append("Success")

        else:
            if not on[x]:
                ans.append("Already off")
                continue

            primes = get_primes(x)

            for p in primes:
                owner[p] = 0

            on[x] = False
            ans.append("Success")

    print('\n'.join(ans))

solve()
```

The sieve computes the smallest prime factor for every number. When `spf[x] == x`, the number is prime. During the inner loop, we only update numbers whose smallest prime factor has not already been assigned.

The `get_primes` function extracts distinct prime divisors. The inner `while` loop removes all copies of the same prime so that each factor appears exactly once. This matters because a number like `12 = 2^2 * 3` should only claim prime `2` once.

The `on` array handles state checks in constant time. Without it, duplicate activation and duplicate deactivation become awkward to detect correctly.

The `owner` array is the core optimization. Each prime can belong to at most one active collider at a time. During activation we first check for conflicts before assigning ownership. The order matters. If we assigned ownership immediately while iterating, then a partially processed activation could corrupt the structure after discovering a later conflict.

Deactivation recomputes the prime factors and releases ownership. This is safe because the invariant guarantees that all those primes currently belong to the collider being turned off.

## Worked Examples

### Example 1

Input:

```
10 10
+ 6
+ 10
+ 5
- 10
- 5
- 6
+ 10
+ 3
+ 6
+ 3
```

| Query | Prime Factors | Active Colliders | Owner State | Output |
| --- | --- | --- | --- | --- |
| + 6 | 2, 3 | {6} | 2→6, 3→6 | Success |
| + 10 | 2, 5 | {6} | 2 already owned by 6 | Conflict with 6 |
| + 5 | 5 | {5, 6} | 5→5 | Success |
| - 10 | 2, 5 | {5, 6} | 10 inactive | Already off |
| - 5 | 5 | {6} | 5 released | Success |
| - 6 | 2, 3 | {} | 2 and 3 released | Success |
| + 10 | 2, 5 | {10} | 2→10, 5→10 | Success |
| + 3 | 3 | {3, 10} | 3→3 | Success |
| + 6 | 2, 3 | {3, 10} | 2 owned by 10 | Conflict with 10 |
| + 3 | 3 | {3, 10} | already active | Already on |

This trace shows the invariant clearly. Prime ownership fully determines whether activation is legal. Once `10` owns prime `2`, collider `6` cannot activate even though collider `3` is also active.

### Example 2

Input:

```
6 5
+ 2
+ 3
+ 6
- 2
+ 6
```

| Query | Prime Factors | Active Colliders | Owner State | Output |
| --- | --- | --- | --- | --- |
| + 2 | 2 | {2} | 2→2 | Success |
| + 3 | 3 | {2, 3} | 3→3 | Success |
| + 6 | 2, 3 | {2, 3} | 2 owned by 2 | Conflict with 2 |
| - 2 | 2 | {3} | 2 released | Success |
| + 6 | 2, 3 | {3} | 3 owned by 3 | Conflict with 3 |

This example demonstrates that removing one conflict source may still leave another. Collider `6` conflicts independently with both `2` and `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log log n + m log n) | Sieve preprocessing plus fast factorizations |
| Space | O(n) | Arrays for smallest prime factors, ownership, and activity |

Each query only touches the distinct prime factors of one number. Numbers up to `10^5` have very few distinct prime divisors, so the practical runtime is extremely fast. The solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())

        spf = list(range(n + 1))

        for i in range(2, int(n ** 0.5) + 1):
            if spf[i] == i:
                for j in range(i * i, n + 1, i):
                    if spf[j] == j:
                        spf[j] = i

        def get_primes(x):
            res = []

            while x > 1:
                p = spf[x]
                res.append(p)

                while x % p == 0:
                    x //= p

            return res

        on = [False] * (n + 1)
        owner = [0] * (n + 1)

        out = []

        for _ in range(m):
            op, val = input().split()
            x = int(val)

            if op == '+':
                if on[x]:
                    out.append("Already on")
                    continue

                primes = get_primes(x)

                bad = 0

                for p in primes:
                    if owner[p]:
                        bad = owner[p]
                        break

                if bad:
                    out.append(f"Conflict with {bad}")
                else:
                    on[x] = True

                    for p in primes:
                        owner[p] = x

                    out.append("Success")

            else:
                if not on[x]:
                    out.append("Already off")
                    continue

                for p in get_primes(x):
                    owner[p] = 0

                on[x] = False
                out.append("Success")

        return '\n'.join(out)

    return solve()

# provided sample
assert run(
"""10 10
+ 6
+ 10
+ 5
- 10
- 5
- 6
+ 10
+ 3
+ 6
+ 3
"""
) == """Success
Conflict with 6
Success
Already off
Success
Success
Success
Success
Conflict with 10
Already on"""

# minimum-size case
assert run(
"""1 3
+ 1
+ 1
- 1
"""
) == """Success
Already on
Success"""

# repeated deactivate
assert run(
"""5 2
- 3
- 3
"""
) == """Already off
Already off"""

# multiple conflicts
assert run(
"""10 4
+ 2
+ 3
+ 6
+ 5
"""
) == """Success
Success
Conflict with 2
Success"""

# release ownership correctly
assert run(
"""10 5
+ 6
- 6
+ 2
+ 3
+ 6
"""
) == """Success
Success
Success
Success
Conflict with 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single collider with repeated activation | Already on handling | Correct state tracking |
| Repeated deactivation | Already off handling | Inactive checks |
| Simultaneous possible conflicts | Any valid conflict detection | Prime ownership logic |
| Activate after removal | Ownership release | Correct cleanup during deactivation |

## Edge Cases

Consider repeated activation:

```
5 2
+ 2
+ 2
```

The first query activates collider `2` and sets `owner[2] = 2`. During the second query, the algorithm checks `on[2]` before factorization or conflict detection. Since the collider is already active, it immediately prints:

```
Success
Already on
```

This ordering avoids falsely reporting a conflict with itself.

Now consider multiple possible conflicts:

```
10 3
+ 2
+ 3
+ 6
```

After activating `2` and `3`, the ownership table contains:

```
owner[2] = 2
owner[3] = 3
```

Collider `6` factorizes into `{2, 3}`. The algorithm scans its prime factors and stops at the first occupied one. Depending on iteration order, it may print either:

```
Conflict with 2
```

or

```
Conflict with 3
```

Both are correct because the statement allows any conflicting collider.

Finally, consider stale ownership after deactivation:

```
10 4
+ 6
- 6
+ 2
+ 3
```

Collider `6` owns primes `2` and `3`. During deactivation, the algorithm recomputes the same prime factors and clears:

```
owner[2] = 0
owner[3] = 0
```

After that, both `2` and `3` can activate successfully. If ownership were not cleared correctly, later activations would incorrectly report conflicts with an inactive collider.
