---
title: "CF 103466G - Poker Game"
description: "This is a simulated poker tournament where five fixed-strategy players repeatedly participate in a series of independent rounds."
date: "2026-07-03T06:49:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103466
codeforces_index: "G"
codeforces_contest_name: "The 2019 ICPC Asia Nanjing Regional Contest"
rating: 0
weight: 103466
solve_time_s: 31
verified: false
draft: false
---

[CF 103466G - Poker Game](https://codeforces.com/problemset/problem/103466/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** no  

## Solution
## Problem Understanding

This is a simulated poker tournament where five fixed-strategy players repeatedly participate in a series of independent rounds. In each round, a shuffled sequence of cards is already fixed in advance, and the dealer distributes them deterministically: each still-active player receives two private cards in order, followed by shared community cards dealt in stages, with betting rounds in between.

Each player starts each round with a fixed stack of chips, but can lose chips by calling bets of fixed sizes across up to three betting rounds. If a player ever reaches zero chips, they are removed from all future rounds. The only thing we must compute is the total number of chips each player has accumulated across all rounds after simulating all decisions and payouts.

A round has a sequence of decisions: pre-flop betting, flop betting, and river betting. At each stage, players may fold or call based on their private rules, and in some cases may go all-in if their stack is small. If at any point only one player remains, they immediately win all committed chips for that round. Otherwise, if multiple players survive to the end, a showdown occurs and the best poker hand among their seven cards decides the winner, with deterministic tie-breaking favoring the player later in turn order.

The constraints are essentially hidden inside simulation complexity. There are at most 1000 rounds, and only five players. Each round involves constant-time poker evaluation for a handful of 7-card hands and a fixed number of rule checks. This means the intended solution is a straightforward simulation, with careful attention to correctness of poker hand ranking and player decision logic. Any solution that attempts combinatorial search over decisions or hand outcomes would be unnecessary and risk implementation complexity without performance benefit.

The main subtle failure cases come from poker hand comparison details. The straight rules, especially A2345 and TJQKA edge cases, require careful handling. Another common pitfall is handling all-in players: once all-in, they no longer participate in betting logic but still contribute to showdown evaluation. Finally, tie-breaking depends on player order, which must be preserved exactly.

Example failure scenario: if A2345 is treated as having Ace as high card instead of 5 for sequence comparison, comparisons against other straights become inconsistent, producing wrong winners in low straight situations.

Another example: if flush and straight are not unified into a stronger category (straight flush implied by rules), the hand strength ordering becomes incorrect in suits like A2345 all same suit, which is explicitly treated as a special strongest structure in that segment.

## Approaches

The naive idea is to explicitly simulate every round step-by-step, maintaining player states, dealing cards, evaluating decisions sequentially, and computing final results. Since each round has a fixed number of players and fixed actions, this simulation is already efficient enough. The only complexity lies in correctly implementing poker evaluation and strategy conditions.

The brute-force bottleneck would only appear if we attempted to enumerate possible outcomes of folding decisions or card combinations. That is unnecessary because all randomness is eliminated: card order and strategies are deterministic. Therefore, the entire problem reduces to deterministic state simulation.

The key insight is that the problem is not combinatorial in nature despite its poker theme. It is a rule engine simulation problem with a strong requirement: correct evaluation of 7-card poker hands and strict adherence to player decision logic. Once we model a round correctly, everything else is linear in the number of rounds.

The optimal solution is simply:

simulate rounds → simulate betting phases → track stacks → evaluate hands → assign pot.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over outcomes | exponential | high | Too slow |
| Full deterministic simulation | O(n) rounds × O(1) work | O(1) | Accepted |

## Algorithm Walkthrough

We simulate each round independently, maintaining current chip stacks and active status.

### 1. Initialize players

Each player starts with 100 chips and is marked active. Once a player reaches zero, they are removed permanently from future rounds.

### 2. Deal cards in order

For each round, iterate through active players in fixed order and assign two cards each from the precomputed sequence. Then deal community cards in the given stages.

The ordering matters because later comparisons rely on deterministic seating order.

### 3. Pre-flop betting

Each player in order decides based on their private rule. If they fold, they leave the round immediately. If they call, subtract 5 chips. If they go all-in, their entire stack is committed and they become “locked” for remaining betting logic.

This step defines the initial survival set for the round.

### 4. Flop betting

Community cards increase to 3 visible cards. Remaining players again decide based on their rules. Chips are deducted similarly unless all-in.

This step often eliminates weak hands early and changes pot size.

### 5. River betting

Community cards become 5. Final betting decisions are applied. After this stage, surviving players proceed to showdown unless only one remains.

### 6. Early termination check

If at any stage only one player remains, they win all committed chips immediately. No hand evaluation is needed.

This is a key optimization and correctness condition: betting structure alone can end the round.

### 7. Showdown evaluation

If multiple players remain, compute the best 5-card poker hand from each player’s 7 cards. Compare hands using:

First, category rank (high card < pair < three of a kind < straight < flush).

Then tie-break using critical card rules, carefully handling A2345 where the effective highest card is 5, not Ace.

If tied, the player with later position in seating order wins.

### 8. Award pot

Winner gains all chips committed in that round. U
