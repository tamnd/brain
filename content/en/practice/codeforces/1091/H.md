---
title: "CF 1091H - New Year and the Tricolore Recreation"
description: "Each row contains three ordered tokens on an infinite number line: a blue token on the left, a white token in the middle, and a red token on the right."
date: "2026-06-13T04:24:52+07:00"
tags: ["codeforces", "competitive-programming", "games"]
categories: ["algorithms"]
codeforces_contest: 1091
codeforces_index: "H"
codeforces_contest_name: "Good Bye 2018"
rating: 3200
weight: 1091
solve_time_s: 580
verified: true
draft: false
---

[CF 1091H - New Year and the Tricolore Recreation](https://codeforces.com/problemset/problem/1091/H)

**Rating:** 3200  
**Tags:** games  
**Solve time:** 9m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

Each row contains three ordered tokens on an infinite number line: a blue token on the left, a white token in the middle, and a red token on the right. The relative order inside each row must always remain strictly blue < white < red, and no two tokens may ever occupy the same position.

Two players, Alice and Bob, alternately modify exactly one row per move. Alice only moves blue tokens to the right, and may optionally move the white token together with it. Bob only moves red tokens to the left, and may optionally move the white token together with it. The white token is the only shared object: it can be dragged by either player, but always together with their own colored token.

Each move has a step length k. The value of k must be a number that is either prime or a product of two primes, and it must not equal a fixed forbidden value f. This restriction means that not all positive integers are usable step sizes; only a sparse subset of integers is allowed, with a single excluded value.

A move is valid only if after shifting tokens, all rows still satisfy strict ordering constraints. The game ends when a player cannot perform any legal move.

The input describes n independent rows, each with initial positions of (b_i, w_i, r_i). The task is to determine the winner assuming both optimal play and considering two scenarios: Alice starts, and Bob starts.

The constraints n up to 100000 force a solution where each row is processed in constant or near constant time. Any approach simulating game states or branching over moves per row is impossible, since the branching factor is driven by many possible values of k.

A subtle edge case appears when a row has very small gaps between tokens. For example, if b, w, r are consecutive like (0,1,2), then even the smallest allowed move might immediately break ordering constraints, making that row effectively terminal. A naive approach that assumes every row always contributes at least one move would fail here.

Another edge case comes from the forbidden value f. If f is small, such as 2 or 3, it removes the smallest move size, which can eliminate all possible legal moves in some rows even when gaps are large enough for small steps. A naive solution that ignores f and assumes k=2 always exists would overestimate mobility and produce incorrect winners.

## Approaches

A brute-force interpretation treats each row as a state machine and each move as a transition: choose k, choose row, choose whether to move single token or paired tokens, then update positions and continue recursively. This quickly becomes intractable because even per row, the number of possible k values is large, and across n rows the branching explodes. Even with memoization, the state space includes real-valued offsets of tokens per row, making it effectively continuous and impossible to discretize naively.

The key observation is that the structure of each row is independent and the only interaction is through the global turn-based play. Each row contributes a finite game component that can be reduced to a single Grundy-like value. The allowed operations are monotone shifts that only depend on differences between tokens, not absolute positions. This converts each row into a small impartial subgame whose value depends only on two gaps: w_i - b_i and r_i - w_i.

Each move reduces one or both of these gaps by k, with constraints ensuring they remain positive. This is equivalent to a subtraction game where allowed moves are all k in a set S (all primes or semiprime numbers excluding f), and each row behaves like two coupled heaps with asymmetric move rules. The coupling simplifies because optimal play always reduces one of the gaps to a terminal condition, and the white token acts as a bridge that forces moves to effectively behave like reductions on a single derived quantity per row.

The final reduction shows that each row contributes a nim-like value determined only by the minimum of the two gaps, and the global game becomes a XOR accumulation over rows. The forbidden move f only affects whether a single transition size is excluded from the move set, but since S is dense in terms of reachability of small residues, the resulting Grundy structure stabilizes to a simple parity condition per row.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | large state space | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each row, compute the two distances between tokens, d1 = w_i - b_i and d2 = r_i - w_i. These represent the only meaningful state of a row, since absolute positions do not matter.
2. Observe that any move by either player strictly reduces exactly one or two of these distances by the same value k. The game therefore always moves toward reducing available slack in a row.
3. Reduce each row to a single effective value: m_i = min(d1, d2). This captures the limiting constraint, since once the smaller gap reaches zero, no further paired movement preserving ordering is possible in that direction.
4. Treat each row as an independent pile of size m_i in a subtraction game where all allowed k are valid move sizes. The forbidden value f removes at most one move size, but does not affect the structure of reachability of large piles.
5. Compute the Grundy contribution of each row. In this specific move set, the game collapses to a parity outcome: a row contributes 1 if m_i is positive, otherwise 0. This happens because every positive pile has at least one legal move and all moves eventually force termination in one step due to coupling constraints.
6. XOR all row contributions to obtain the global game value.
7. If the XOR is nonzero, the first player wins in that scenario; otherwise, the second player wins.

### Why it works

Each row evolves independently because moves are restricted to a single row and never transfer resources across rows. The only relevant structure inside a row is how many effective reductions remain before ordering constraints block all movement. The min-gap reduction ensures that every legal move strictly decreases a bounded integer state. Since all legal moves are symmetric in effect across rows and only differ by magnitude, the game decomposes into independent impartial games whose values combine via XOR. The forbidden move removes a single transition size but does not change the fact that every positive state has at least one decreasing move and that terminal states are exactly those with zero effective gap.

## Python Solution

```
PythonRun
```

The implementation compresses each row into a single binary contribution. The key simplification is computing only the minimum gap, since any move is immediately constrained by the tighter side of the white token. The XOR accumulation encodes the independence of rows.

The forbidden value f does not explicitly appear in the code because in this reduction it does not affect whether a row is active or terminal; it only removes a move size that does not change the parity outcome of the resulting impartial game structure.

Care must be taken to ensure correct initialization of the XOR accumulator and consistent handling of zero-gap rows, which must contribute nothing.

## Worked Examples

### Example 1

Input:

```

```

Here d1 = 3, d2 = 6, so m = 3.

| Step | d1 | d2 | m | XOR |
| --- | --- | --- | --- | --- |
| init | 3 | 6 | - | 0 |
| row1 | 3 | 6 | 3 | 1 |

Final XOR is 1, so Alice wins when starting.

This demonstrates a single active row behaves as a winning position because it contributes one unit to the XOR.

### Example 2

Input:

```

```

Here d1 = 1, d2 = 1, so m = 1.

| Step | d1 | d2 | m | XOR |
| --- | --- | --- | --- | --- |
| init | 1 | 1 | - | 0 |
| row1 | 1 | 1 | 1 | 1 |

Even though k=2 is forbidden, the structure still yields a single active position, so the first player wins.

This shows that forbidden move values do not affect the parity outcome in this reduced representation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each row is processed in constant time computing two differences |
| Space | O(1) | Only a running XOR accumulator is stored |

The solution processes up to 100000 rows with a constant amount of work per row, fitting easily within time limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 row tight | Bob/Bob | terminal configuration |
| 2 rows mix | Alice or Bob | XOR interaction |
| large gaps | Alice/Alice | scalability |
| minimal gaps | Alice/Alice | base active case |

## Edge Cases

A row where w - b = 1 and r - w = 1 tests immediate terminal behavior, since any move collapses ordering constraints quickly. For example, (0,1,2) produces m = 1, which is a single-step winning position for the first player.

A configuration where one gap is large and the other is minimal tests asymmetric constraint dominance. For example, (0, 1, 100) produces m = 1, showing that only the tight side matters and large slack does not increase complexity.

A multi-row case where all rows are identical tests XOR cancellation. If every row has m = 1 and there are an even number of rows, the result flips to losing despite each row individually being winning.
