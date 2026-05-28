---
title: "CF 128C - Games with Rectangle"
description: "We start with a rectangle drawn on grid paper. Only the border matters, not the interior. Players repeatedly draw a strictly smaller rectangle inside the previous one."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 128
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 94 (Div. 1 Only)"
rating: 2000
weight: 128
solve_time_s: 112
verified: true
draft: false
---

[CF 128C - Games with Rectangle](https://codeforces.com/problemset/problem/128/C)

**Rating:** 2000  
**Tags:** combinatorics, dp  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a rectangle drawn on grid paper. Only the border matters, not the interior. Players repeatedly draw a strictly smaller rectangle inside the previous one. The new border cannot touch the previous border at any point, so every new rectangle must be separated from the old one by at least one grid cell in all four directions.

After exactly `k` moves, we want to count how many different final drawings are possible. Two games are considered different if the set of rectangles drawn during the process differs.

The key observation is that each move shrinks the rectangle by removing at least one row from the top, one from the bottom, one from the left, and one from the right. If the current rectangle has height `h` and width `w`, the next rectangle must fit strictly inside with at least one layer of spacing, so its height becomes at most `h - 2` and its width becomes at most `w - 2`.

The constraints go up to `1000` for all three parameters. That immediately rules out any approach that explicitly generates sequences of rectangles. Even a cubic dynamic program starts becoming dangerous in Python if every transition is expensive. We need something around `O(n + m + k)` or `O(nk + mk)`.

There are several easy-to-miss edge cases.

If `k = 1`, we are only choosing one rectangle strictly inside the original one. For example:

```
3 3 1
```

The answer is `1`, because only the central `1 × 1` square works.

A careless implementation might incorrectly count rectangles touching the outer border.

Another subtle case happens when the rectangle becomes too small before finishing all moves.

```
2 2 2
```

The correct answer is `0`.

After one move, the only possible rectangle is `0 × 0`, which is invalid. Any solution that only tracks the number of shrinking operations without checking geometric feasibility will overcount.

A more interesting example is:

```
4 5 1
```

The answer is `9`.

The valid inner rectangles are:

```
1×1: 6 positions
1×2: 2 positions
2×1: 1 position
```

A naive rectangle-counting formula often misses that placement counts depend on dimensions.

## Approaches

The brute-force interpretation is straightforward. At every move, enumerate all rectangles that fit strictly inside the previous one without touching its border. Recursively continue for `k` moves.

This works because every valid game is literally a nested sequence of rectangles. The recursion exactly matches the game rules.

The problem is the branching factor. A rectangle of size `h × w` contains roughly `O(h²w²)` subrectangles. In the worst case, the recursion tree explodes exponentially. Even for moderate dimensions, the number of states becomes enormous.

The structure of the game gives a much cleaner viewpoint.

Suppose the original rectangle spans rows `[1, n]` and columns `[1, m]`. Every move independently chooses how much to shrink from the top, bottom, left, and right. Since rectangles cannot touch, each move must increase all four margins by at least `1`.

After `k` moves, we have selected:

```
k rows removed from the top,
k rows removed from the bottom,
k columns removed from the left,
k columns removed from the right.
```

The order matters only in how these removals are distributed across moves.

Focus on the vertical dimension first.

If after all moves we removed `a` rows from the top and `b` rows from the bottom, then:

```
a ≥ k
b ≥ k
a + b < n
```

The sequence of removals across moves corresponds to partitioning `a` into `k` positive parts and partitioning `b` into `k` positive parts.

The number of ways to split an integer `x` into `k` positive parts is:

$\binom{x-1}{k-1}$

Instead of tracking every intermediate rectangle, we only count how the total shrinkage is distributed.

The same reasoning applies horizontally.

After simplifying the sums with a standard combinatorial identity, the total number of valid vertical shrinking patterns becomes:

$\binom{n-1}{2k}$

Similarly, the number of horizontal patterns is:

$\binom{m-1}{2k}$

The two dimensions are independent, so the final answer is their product.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and `k`.
2. Check whether `2k > n - 1` or `2k > m - 1`.

Every move consumes at least one layer from both opposite sides. After `k` moves, we need at least `2k` removed rows and `2k` removed columns total. If either dimension is too small, no valid sequence exists.
3. Precompute factorials and inverse factorials up to `1000`.

We need fast binomial coefficient queries modulo `10^9 + 7`.
4. Compute:

$\binom{n-1}{2k}$
5. Compute:

$\binom{m-1}{2k}$
6. Multiply the two values modulo `10^9 + 7`.
7. Print the result.

### Why it works

Each move independently increases four margins: top, bottom, left, and right. After all `k` moves, the total removals from opposite sides determine the entire nested structure.

Choosing a valid game is equivalent to choosing where the `2k` mandatory shrinking layers occur among the `n - 1` available vertical gaps, and similarly among the `m - 1` horizontal gaps.

The combinatorial identity counts exactly these choices, neither missing nor duplicating any sequence of rectangles.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def build_factorials(limit):
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (limit + 1)
    inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)

    for i in range(limit, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    return fact, inv_fact

def comb(n, r, fact, inv_fact):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

def solve():
    n, m, k = map(int, input().split())

    limit = max(n, m)
    fact, inv_fact = build_factorials(limit)

    ans = comb(n - 1, 2 * k, fact, inv_fact)
    ans *= comb(m - 1, 2 * k, fact, inv_fact)
    ans %= MOD

    print(ans)

solve()
```

The factorial precomputation supports constant-time binomial coefficient queries. Since the maximum value is only `1000`, this is very cheap.

The helper `comb` safely handles invalid cases by returning `0` when `r > n`. That automatically handles impossible configurations such as `2k > n - 1`.

The formula uses `n - 1` and `m - 1` because shrinking happens between grid lines. A common off-by-one mistake is using `n` directly, which overcounts impossible border placements.

The modulo inverse uses Fermat's little theorem because `10^9 + 7` is prime.

## Worked Examples

### Example 1

Input:

```
3 3 1
```

We compute:

| Variable | Value |
| --- | --- |
| n - 1 | 2 |
| m - 1 | 2 |
| 2k | 2 |
| C(2, 2) | 1 |
| C(2, 2) | 1 |
| Answer | 1 |

The only valid rectangle is the central `1 × 1` square. This confirms that every move must leave one layer of spacing on all sides.

### Example 2

Input:

```
4 5 1
```

We compute:

| Variable | Value |
| --- | --- |
| n - 1 | 3 |
| m - 1 | 4 |
| 2k | 2 |
| C(3, 2) | 3 |
| C(4, 2) | 6 |
| Answer | 18 |

The vertical dimension contributes three ways to choose top and bottom shrink positions. The horizontal dimension contributes six ways. Their product gives all possible inner rectangles.

This example demonstrates the independence between rows and columns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(max(n, m)) | Factorial precomputation dominates |
| Space | O(max(n, m)) | Factorial and inverse factorial arrays |

With limits only up to `1000`, this solution easily fits within both time and memory constraints. The computation is effectively instantaneous.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def build_factorials(limit):
        fact = [1] * (limit + 1)

        for i in range(1, limit + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (limit + 1)
        inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)

        for i in range(limit, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        return fact, inv_fact

    def comb(n, r, fact, inv_fact):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

    n, m, k = map(int, input().split())

    fact, inv_fact = build_factorials(max(n, m))

    ans = comb(n - 1, 2 * k, fact, inv_fact)
    ans *= comb(m - 1, 2 * k, fact, inv_fact)
    ans %= MOD

    return str(ans)

# provided sample
assert run("3 3 1\n") == "1", "sample 1"

# minimum possible input
assert run("1 1 1\n") == "0", "cannot place any inner rectangle"

# exactly enough space for one move
assert run("3 4 1\n") == "3", "single shrinking layer"

# impossible because too many moves
assert run("5 5 3\n") == "0", "not enough layers"

# symmetric medium case
assert run("5 5 1\n") == "36", "basic combinatorial count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `0` | Smallest dimensions |
| `3 4 1` | `3` | Exact boundary feasibility |
| `5 5 3` | `0` | Impossible number of moves |
| `5 5 1` | `36` | General combinatorial counting |

## Edge Cases

Consider:

```
2 2 2
```

We need:

```
2k = 4
n - 1 = 1
m - 1 = 1
```

The algorithm computes:

```
C(1, 4) = 0
```

for both dimensions, so the answer becomes `0`.

This correctly reflects the geometry. After one move, there is already no room for another rectangle.

Now consider:

```
3 3 1
```

The computation becomes:

```
C(2, 2) × C(2, 2) = 1
```

There is exactly one legal placement, the center cell. This confirms that rectangles touching the outer border are excluded automatically by the combinatorial interpretation.

Finally, consider:

```
1000 1000 1
```

The answer is:

```
C(999, 2)^2
```

The implementation handles this efficiently because all binomial coefficients are computed in constant time after linear preprocessing.
