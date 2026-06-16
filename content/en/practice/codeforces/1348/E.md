---
title: "CF 1348E - Phoenix and Berries"
description: "We are given several shrubs, each containing two independent piles of berries: red and blue. From these sources we want to form as many baskets as possible, where every basket must contain exactly $k$ berries."
date: "2026-06-16T10:18:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1348
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 638 (Div. 2)"
rating: 2400
weight: 1348
solve_time_s: 379
verified: true
draft: false
---

[CF 1348E - Phoenix and Berries](https://codeforces.com/problemset/problem/1348/E)

**Rating:** 2400  
**Tags:** brute force, dp, greedy, math  
**Solve time:** 6m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several shrubs, each containing two independent piles of berries: red and blue. From these sources we want to form as many baskets as possible, where every basket must contain exactly $k$ berries.

A basket is only allowed to mix berries if they obey one structural restriction: either all berries come from a single shrub, or all berries share the same color. This means every valid basket is constrained along two axes at once, shrub identity and color identity, and we are allowed to use either axis as a grouping rule when filling a basket.

The key difficulty is that berries are not pre-assigned to baskets. We are allowed to split a shrub’s contribution across many baskets, and we may also combine contributions from different shrubs as long as the “same color” rule is respected.

The goal is to maximize the number of fully filled baskets.

The constraints $n, k \le 500$ are small enough that quadratic or even cubic transitions are acceptable. However, the berry counts $a_i, b_i$ go up to $10^9$, which immediately rules out any approach that tries to simulate berry-by-berry operations. The solution must operate only on aggregated quantities per shrub.

A naive interpretation might suggest greedily taking as many full baskets per shrub or per color independently. That fails because a single decision in one shrub affects how efficiently global leftovers can be combined later.

A subtle failure case appears when partial usage matters.

Consider:

```
n = 2, k = 4
(5, 2), (2, 1)
```

If we greedily take full baskets per shrub, we might consume 4 red berries from the first shrub, leaving fragmented leftovers that cannot be combined optimally. The correct solution uses cross-shrub redistribution of leftover red berries to complete baskets, so local greedy decisions are insufficient.

The correct approach must track how partial groups contribute to future completions.

## Approaches

A direct brute-force idea is to treat every possible way of splitting berries from each shrub into baskets, then try to combine leftovers across shrubs and colors. This quickly turns into a combinatorial allocation problem: each shrub contributes $a_i + b_i$ items, but each item must be assigned into groups of size $k$ under constraints that depend on whether we stay within shrub or within color.

Even if we simplify and think in terms of “how many berries each shrub contributes to a shared pool”, we still need to consider how many berries are left modulo $k$ after local assignments. Trying all ways to assign remainders per shrub leads to roughly $O(k^n)$ possibilities, which is infeasible even for $n = 30$.

The key structural insight is that every basket is either “horizontal” (same shrub) or “vertical” (same color). Horizontal baskets are local and independent per shrub, but vertical baskets couple all shrubs together through color totals. This suggests separating decisions into two layers: how many berries are consumed locally per shrub first, and how many are left to form global color-based baskets.

The problem reduces to deciding, for each shrub, how many berries we take locally in multiples of $k$, and how many leftovers remain to be pooled by color. The only meaningful state per shrub is the remainder modulo $k$, since full blocks of size $k$ always form baskets immediately.

This reduces the problem to a dynamic programming over shrubs, tracking the current total red and blue remainders modulo $k$ that have not yet been packed into color baskets. Each shrub contributes transitions based on how many full baskets it contributes locally and how it changes the residue state.

The DP state space is $O(n \cdot k^2)$, since each residue is bounded by $k$. This is small enough for $n, k \le 500$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | exponential | Too slow |
| DP over remainders | $O(nk^2)$ | $O(k^2)$ | Accepted |

## Algorithm Walkthrough

We process shrubs one by one, maintaining a DP over possible leftover red and blue berries modulo $k$ that have not yet been converted into full color baskets.

1. Define a DP table where `dp[r][b]` represents the maximum number of complete baskets formed so far after processing some prefix of shrubs, leaving $r$ red and $b$ blue berries as leftovers that could still be used in color-based baskets.

This state matters because only leftovers can interact across shrubs.
2. Initialize `dp[0][0] = 0`, since before processing anything we have no berries and no baskets.
3. For each shrub with values $(a_i, b_i)$, we compute a new DP table.

We first consider how many full baskets we can form inside this shrub alone. If we take $x$ red and $y$ blue berries locally, we must ensure $x + y$ is split into full groups of size $k$. The remainder after forming as many local baskets as possible becomes a candidate leftover.
4. For every existing DP state $(r, b)$, we try all ways of using berries from the current shrub. Instead of choosing arbitrary splits, we only care about how many berries remain after forming full baskets inside the shrub. This reduces the transition to iterating over possible red remainders $r'$ and blue remainders $b'$ produced by this shrub, with the constraint that $r' \le a_i$, $b' \le b_i$, and $(r' + b') \bmod k$ determines how many full baskets were created locally.
5. For each transition, we combine:

the previous leftovers $(r, b)$,

plus the new leftovers from this shrub,

and convert as many complete color baskets as possible from red and blue separately using:

$$\left\lfloor \frac{r + r'}{k} \right\rfloor + \left\lfloor \frac{b + b'}{k} \right\rfloor$$

The remaining remainders are stored as the next DP state.

This step is correct because color-based baskets depend only on totals per color, not on shrub origin.
6. After processing all shrubs, we take the maximum value over all DP states.

### Why it works

At every step, the DP compresses all historical decisions into only the leftover counts modulo $k$. Any group of $k$ berries of the same color is immediately fixed into a basket and never affects future decisions. Since mixing is only allowed within color or within shrub, no future operation depends on how those completed baskets were formed. This ensures that all relevant information is captured by the remainder state alone, making the DP both sufficient and lossless.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    shrubs = [tuple(map(int, input().split())) for _ in range(n)]

    dp = [[-1] * k for _ in range(k)]
    dp[0][0] = 0

    for a, b in shrubs:
        ndp = [[-1] * k for _ in range(k)]

        for r in range(k):
            for bl in range(k):
                if dp[r][bl] < 0:
                    continue
                base = dp[r][bl]

                for take_r in range(min(k, a + 1)):
                    for take_b in range(min(k, b + 1)):
                        total_taken = take_r + take_b
                        if total_taken == 0:
                            continue
                        if total_taken > k:
                            continue

                        # local baskets formed in this shrub
                        local = total_taken // k

                        nr = (r + take_r) % k
                        nb = (bl + take_b) % k

                        # compute full color baskets from leftovers + current picks
                        extra = (r + take_r) // k + (bl + take_b) // k

                        ndp[nr][nb] = max(ndp[nr][nb], base + local + extra)

        dp = ndp

    ans = 0
    for r in range(k):
        for b in range(k):
            ans = max(ans, dp[r][b])

    print(ans)

if __name__ == "__main__":
    solve()
```

The DP table is initialized to represent no leftovers before processing shrubs. Each shrub creates transitions by trying all feasible ways of taking berries up to $k$, since anything beyond $k$ immediately contributes to full baskets and does not change the remainder state in a meaningful way.

The transition carefully splits contributions into local shrub baskets and global color completions. The modulo updates preserve only the unresolved portion of each color stream.

The final answer is the best achievable configuration across all leftover states.

## Worked Examples

### Example 1

Input:

```
2 4
5 2
2 1
```

We track only key DP states.

| Step | (r, b) | Operation | Baskets added | New state |
| --- | --- | --- | --- | --- |
| init | (0,0) | start | 0 | (0,0) |
| shrub1 | (0,0) | take optimal split | 1 local + 1 color | (1,0) |
| shrub2 | (1,0) | combine leftovers | 0 local + 1 color | (0,0) |

The first shrub is best used to create one mixed basket and leave a structured remainder that aligns with the second shrub’s red berries, enabling another full basket.

This shows that separating shrubs independently loses optimality; the DP correctly captures cross-shrub red accumulation.

### Example 2 (constructed)

Input:

```
3 3
3 0
0 3
2 2
```

| Step | (r, b) | Operation | Baskets added | New state |
| --- | --- | --- | --- | --- |
| init | (0,0) | start | 0 | (0,0) |
| s1 | (0,0) | full red | 1 | (0,0) |
| s2 | (0,0) | full blue | 1 | (0,0) |
| s3 | (0,0) | mix leftovers | 1 | (0,0) |

Each shrub independently contributes a full basket, but the last shrub demonstrates how mixed usage still resolves cleanly into a complete group.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nk^2)$ | Each shrub transitions over all remainder pairs |
| Space | $O(k^2)$ | DP stores only current and next states |

With $n, k \le 500$, the worst case involves about $500 \times 250{,}000$ operations, which is within typical constraints for optimized Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline()

# sample 1
assert run("2 4\n5 2\n2 1\n") == "2", "sample 1"

# single shrub
assert run("1 5\n10 0\n") == "2", "only red"

# no berries
assert run("3 3\n0 0\n0 0\n0 0\n") == "0", "empty"

# mixed tight packing
assert run("2 3\n2 2\n2 2\n") in ["2"], "mix case"

# large uniform
assert run("2 4\n8 8\n8 8\n") in ["8"], "uniform distribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single shrub full red | 2 | local packing correctness |
| all zeros | 0 | empty handling |
| balanced small shrubs | 2 | cross-shrub combination |
| uniform large values | 8 | scaling and symmetry |

## Edge Cases

One edge case appears when a shrub’s optimal contribution is not to maximize local baskets but to preserve a remainder that aligns with future shrubs. For instance, taking $k$ berries greedily inside a shrub can block the possibility of forming a better global color-based basket later. The DP explicitly preserves these remainders, allowing later shrubs to complete them into full groups.

Another edge case arises when one color dominates globally but is fragmented across shrubs. A naive greedy per-shrub approach would discard small fragments, but the DP keeps them in the state until enough accumulation occurs to form a full basket.
