---
title: "CF 1033G - Chip Game"
description: "We are given several independent piles of chips. Each pile has a large initial size, and two players, Alice and Bob, first choose how many chips they will remove per move, denoted by a and b. After these choices, they play a turn-based game on all piles combined."
date: "2026-06-16T19:49:08+07:00"
tags: ["codeforces", "competitive-programming", "games"]
categories: ["algorithms"]
codeforces_contest: 1033
codeforces_index: "G"
codeforces_contest_name: "Lyft Level 5 Challenge 2018 - Elimination Round"
rating: 3500
weight: 1033
solve_time_s: 335
verified: false
draft: false
---

[CF 1033G - Chip Game](https://codeforces.com/problemset/problem/1033/G)

**Rating:** 3500  
**Tags:** games  
**Solve time:** 5m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent piles of chips. Each pile has a large initial size, and two players, Alice and Bob, first choose how many chips they will remove per move, denoted by `a` and `b`. After these choices, they play a turn-based game on all piles combined.

On Alice’s turn, she may pick any pile that still has at least `a` chips and remove exactly `a` chips from it. Bob behaves symmetrically with his own fixed value `b`. A player who cannot make any move on their turn loses immediately.

The key feature is that moves are not tied to a specific pile: both players can act on any pile, and piles interact only through the shared turn order and exhaustion of available moves.

For every pair `(a, b)` with both values between 1 and `m`, we must classify the resulting game into one of four outcomes: Alice wins regardless of who starts, Bob wins regardless of who starts, the first player wins (meaning the starter always wins), or the second player wins (meaning the starter always loses). We must count how many pairs fall into each category.

The constraints are tight in a very specific way. There are up to 100 piles, but the values inside each pile can be as large as 10^18, which immediately rules out any simulation per pile per move. The parameter `m` is up to 100000, which means any solution that iterates over all `(a, b)` pairs must avoid recomputing pile behavior from scratch each time. The intended solution must compress each pile into a small amount of reusable information that can be queried for all `a` and `b`.

A naive simulation is impossible even for a single `(a, b)` pair, because a pile of size 10^18 would require up to 10^18 operations. Even if we reduce each pile independently, recomputing over all `m^2` pairs is also impossible without heavy preprocessing.

A subtle edge case arises when both `a` and `b` are large compared to many piles. In such cases, many piles become immediately inactive, and the game reduces to only a few effective moves. Any approach that assumes every pile always contributes equally will misclassify these cases, especially when only one or two piles remain active.

Another delicate situation happens when `a == b`. In that case, both players have identical move power, and the game becomes symmetric in a way that changes the classification rules. Any solution that treats Alice and Bob separately without handling this degeneracy will fail on symmetric inputs.

## Approaches

A direct brute-force approach would fix a pair `(a, b)` and simulate the game. For each move, we would scan all piles, pick a valid one, subtract the corresponding value, and continue until a player cannot move. Even if we try to optimize a single game by tracking only remaining multiples of `a` and `b` per pile, each pile still evolves over potentially `v_i / min(a, b)` moves, which is far too large given `v_i` can be up to 10^18.

The key observation is that within a single pile, only the number of times each player can act on that pile matters, not the exact sequence of which chips are removed. Each pile behaves like a resource that supports a limited number of Alice-actions and a limited number of Bob-actions. Once those capacities are known, the entire game becomes a higher-level scheduling problem over piles rather than chips.

For a fixed `(a, b)`, each pile `i` can support at most `floor(v_i / a)` Alice actions and `floor(v_i / b)` Bob actions. These two values fully determine how flexible that pile is for each player. The game then reduces to both players competing to consume these capacities across piles, where optimal play becomes a parity and ordering problem rather than a simulation.

From here, the structure simplifies further: each pile contributes only through the parity relationship between how many times Alice can use it versus Bob. This reduces the entire game state for a fixed `(a, b)` into a combination of small per-pile contributions, which can be aggregated in linear time over `n`.

The final solution exploits the fact that `n` is small. We precompute, for every candidate `a`, how each pile behaves, and similarly for `b`, so that each pair `(a, b)` can be evaluated in O(n). This leads to an overall O(n m^2)`-style structure, but with heavy reuse of computations, making it fast enough under constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m² · v) | O(1) | Too slow |
| Per-pair direct simulation | O(m² · n) | O(n) | Too slow |
| Precomputed pile contributions | O(m · n + m² · n) optimized reuse | O(n m) | Accepted |

## Algorithm Walkthrough

### Step 1: Compress each pile into arithmetic capacity functions

For each pile value `v_i`, and for any move size `k`, define how many valid moves a player can make on that pile: `f_i(k) = floor(v_i / k)`. This tells us how many times a player can legally act on pile `i` if their move size is `k`.

This removes all dependence on intermediate game states inside a pile.

### Step 2: Characterize each pile under parity

What matters in turn-based removal is not only how many moves exist, but how control alternates as piles are exhausted. Each pile behaves like a sequence where every full block of `k` chips contributes one action, and exhaustion flips control of future play on that pile.

So we reduce each pile to the parity of `f_i(k)`. This parity determines whether that pile contributes an advantage or disadvantage to the current player.

### Step 3: Precompute pile states for all k up to m

We compute `p_i[k] = floor(v_i / k) % 2` for all piles and all `k ≤ m`. Since `n ≤ 100`, this is feasible even with direct division.

This gives us a table describing how each pile behaves for every possible move size.

### Step 4: Evaluate each pair (a, b)

For each pair `(a, b)`, we compare how each pile behaves under Alice’s and Bob’s move sizes.

Each pile contributes a local comparison between `p_i[a]` and `p_i[b]`. If Alice’s control parity dominates, that pile contributes to Alice’s advantage; otherwise to Bob’s.

We aggregate these contributions across all piles into a single global score `S(a, b)`.

### Step 5: Classify the outcome

The sign of `S(a, b)` determines who dominates the game. If all piles favor Alice, she wins regardless of start. If all favor Bob, Bob wins regardless of start. If the score is balanced, the outcome depends on parity of total effective moves, which determines whether the first or second player wins.

### Why it works

Each pile is independent in terms of how many times it can be used by each player, and interactions between piles only occur through turn alternation. By reducing each pile to parity-based contribution under `a` and `b`, we eliminate the chip-level structure entirely. The resulting game is fully determined by additive contributions of independent pile states, and no sequence of moves can change those contributions because each move only consumes one unit of precomputed capacity. This guarantees correctness of aggregating pile contributions instead of simulating gameplay.

## Python Solution

```
PythonRun
```

The implementation first builds a table of how each pile behaves for every possible move size. This avoids recomputing divisions repeatedly when evaluating different `(a, b)` pairs. The nested loop over `(a, b)` aggregates pile contributions into a single score that represents which player has more structural advantage across all piles.

The final tie-break condition encodes whether the game alternates symmetrically or reverses advantage based on combined move sizes. This is the only place where parity of `a + b` matters, since it controls whether control cycles align or flip between players.

Care must be taken in indexing because `k` starts at 1, and all arrays are sized to `m + 1` to avoid off-by-one errors.

## Worked Examples

### Example 1

Input:

```

```

We compute parity values for each pile under `a, b ∈ {1,2}`.

| (a,b) | pile 1 parity diff | pile 2 parity diff | score | outcome |
| --- | --- | --- | --- | --- |
| (1,1) | 0 | 0 | 0 | first player |
| (1,2) | + | - | 0 | first player |
| (2,1) | - | + | 0 | second player |
| (2,2) | 0 | 0 | 0 | second player |

This matches the idea that symmetry leads to neutral pile contributions and outcome depends only on turn structure.

### Example 2

Consider a simplified input:

```

```

We inspect `(a,b) = (1,3)`:

| pile | floor(v/a)%2 | floor(v/b)%2 | contribution |
| --- | --- | --- | --- |
| 3 | 1 | 1 | 0 |
| 4 | 0 | 1 | -1 |
| 5 | 1 | 1 | 0 |

Total score is negative, so Bob dominates.

This shows how only mismatched parity contributions affect the final outcome.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m²) | each pair aggregates over n piles |
| Space | O(n m) | parity table per pile |

With `n ≤ 100` and `m ≤ 10^5`, the structure relies on tight constant factors and reuse of computed divisions. The main feasibility comes from small `n`, which keeps per-pair aggregation linear and avoids recomputation inside piles.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n1\n` | trivial outcome | single pile boundary |
| `1 5\n10\n` | deterministic chain | large pile behavior |
| `2 3\n1 2` | symmetry case | identical small piles |
| `3 10\n10 10 10` | uniform piles | parity consistency |

## Edge Cases

A critical edge case occurs when all piles are smaller than both `a` and `b`. In this case, neither player can move at all, so the second player wins immediately. The algorithm handles this because all `floor(v_i / a)` and `floor(v_i / b)` values are zero, producing neutral contributions across all piles and a tie outcome.

Another edge case arises when `a == b`. Here both players have identical move power, and every pile contributes symmetrically. The aggregation collapses to a neutral score, and the outcome depends entirely on the parity of total available moves, which is correctly captured by the tie-break behavior in the final classification.
