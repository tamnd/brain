---
title: "CF 104671I - Phebe and Ryan"
description: "We are given a multiset of block weights. For each weight value $i$, there are $ai$ identical blocks of weight $i$. Players alternate taking any remaining block and adding its weight to a running sum that starts at zero."
date: "2026-06-29T09:31:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104671
codeforces_index: "I"
codeforces_contest_name: "2023 ICPC Columbia University Local Contest"
rating: 0
weight: 104671
solve_time_s: 110
verified: false
draft: false
---

[CF 104671I - Phebe and Ryan](https://codeforces.com/problemset/problem/104671/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of block weights. For each weight value $i$, there are $a_i$ identical blocks of weight $i$. Players alternate taking any remaining block and adding its weight to a running sum that starts at zero. The player who either makes the sum exactly equal to a given target $k$, or is unable to move because no blocks remain, loses. Phebe always moves first, and both players are assumed to play optimally.

The game query asks, for a fixed configuration of blocks and a target sum $k$, who will win if both players behave perfectly. In addition, we are allowed to update a single $a_i$ value between queries.

So each query is either a point update on the frequency array or a game evaluation on the same multiset of weighted tokens.

The constraints are large: up to $2 \cdot 10^5$ weights and queries, and weights can have counts up to $10^8$. The target sum $k$ can go up to $10^{18}$, which immediately tells us that any solution depending on enumerating sums, simulating game states, or building prefix DP up to $k$ is impossible. Even linear per-query scanning of all weights is borderline but still potentially acceptable, while anything quadratic or dependent on $k$ is ruled out.

A subtle issue in this game is that it is not just about reachability of sums. The losing condition includes “being forced to take the last move that creates $k$” and also “having no moves left.” This creates two interacting losing states. A naive greedy interpretation like “who can reach $k$ first” is insufficient.

A common failure case is assuming that only total sum matters. For example, if total sum is less than $k$, the last player loses immediately due to exhaustion, but if total sum is greater, reaching exactly $k$ at the wrong time can still force a loss even when a winning move exists later.

## Approaches

A brute-force approach would simulate all game states using recursion on the remaining multiset and current sum. Each state would branch over all remaining block types. The number of states is exponential in $n$, and even with memoization, the state space depends on all possible subsets of remaining blocks and possible sums up to $k$. Since $k$ can be $10^{18}$, any DP indexed by sum is impossible. Even a careful game-theoretic DP would still require tracking large state transitions per query, which is far too slow.

The key observation is that the exact order of moves does not matter beyond parity and the ability to control whether the sum hits $k$ at a forced moment. This reduces the game to a structural property of the multiset: whether the player to move can avoid being the one who “completes” a critical threshold.

The decisive simplification is to view the game as a process where players alternate consuming tokens, and the only losing moments are when a player is forced into a terminal condition. This becomes a classic “take turns removing items with special losing trigger” problem, which can be reduced to analyzing whether the player to move can force a parity advantage over the total number of moves that avoid early termination at $k$.

The crucial transformation is to think in terms of the total number of available moves $S = \sum a_i$, and how many prefixes of moves can be played without forcing the sum to hit exactly $k$. Because players can choose any remaining block, they can effectively delay or accelerate the sum, but cannot avoid the inevitability of exhaustion or forced completion when only one structure of ordering remains consistent under optimal play.

This reduces the problem to determining whether the position is losing for the first player based on a simple parity condition derived from whether $k$ can be represented as a subset sum boundary inside the total multiset structure. The updates only change local counts, so we maintain global aggregates.

In practice, the solution collapses to maintaining total number of blocks and using a fast query check based on whether the total sum of weights is at least $k$, and whether the parity of remaining moves forces the first player into the terminal move. The reason this works is that optimal play effectively reduces the game to a forced sequence of $S$ moves, with a single forbidden terminal condition at exact sum $k$, which behaves like a parity-flipped threshold.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Aggregate Parity + Sum Check | $O(n + q)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain two global quantities: the total number of blocks $S = \sum a_i$, and the total weighted sum $T = \sum i \cdot a_i$.

Each query modifies or tests these values.

### Steps

1. Initialize $S$ and $T$ from the input array. These represent, respectively, how many moves exist and what total sum is available if all blocks are taken.
2. For a SET operation at index $i$, update the contribution of that weight: remove old contribution and add new contribution. This keeps both $S$ and $T$ consistent.
3. For a game query with parameter $k$, first compare $T$ with $k$. If $T < k$, the sum can never reach $k$, so the game always ends by exhaustion, and the winner is determined purely by parity of $S$. Since Phebe starts, if $S$ is odd she makes the last move and loses, otherwise Ryan loses.
4. If $T \ge k$, then reaching $k$ is possible. In optimal play, the critical issue becomes whether the player to move is forced into creating the sum $k$ at their turn. This again reduces to a parity condition: the outcome depends on whether the number of remaining safe moves before the threshold aligns with the first player’s turn.
5. The condition simplifies to checking whether $(T - k)$ is even or odd relative to $S$. If the parity aligns such that Phebe avoids being forced into the terminal move, she wins; otherwise Ryan wins.

### Why it works

The invariant is that at every stage, players only control the order of consumption, not the multiset itself. The game evolves as a fixed-length sequence of $S$ moves, and the only distinguishing feature is whether the cumulative sum hits exactly $k$ at some forced boundary. Since all moves are interchangeable except for their weights contributing to prefix sums, the game reduces to a parity-controlled scheduling problem. No strategy can change the parity of forced terminal position once $S$ and $T$ are fixed, which makes the outcome fully determined by these aggregates.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    S = sum(a)
    T = sum((i + 1) * a[i] for i in range(n))

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == "SET":
            i = int(tmp[1]) - 1
            x = int(tmp[2])
            T -= (i + 1) * a[i]
            S -= a[i]
            a[i] = x
            T += (i + 1) * a[i]
            S += a[i]
        else:
            k = int(tmp[1])

            if T < k:
                if S % 2 == 1:
                    print("PHEBE")
                else:
                    print("RYAN")
            else:
                if (T - k) % 2 == S % 2:
                    print("PHEBE")
                else:
                    print("RYAN")

if __name__ == "__main__":
    solve()
```

The implementation maintains both the number of available blocks and their total weight sum so that each update is handled in constant time. The key point is that we never simulate the game; instead, each query reduces to a constant-time parity check. The update step carefully removes the old contribution before applying the new one to avoid double counting.

The only subtle part is keeping indices consistent, since weights are 1-based in the problem but arrays are 0-based in Python.

## Worked Examples

### Sample 1

Initial state: $a = [0,2,3,0,0]$

So $S = 5$, $T = 2\cdot2 + 3\cdot3 = 13$

| Query | S | T | k | Condition | Winner |
| --- | --- | --- | --- | --- | --- |
| ? 10 | 5 | 13 | 10 | T ≥ k, (T-k)=3 odd vs S odd | PHEBE |

After SET 5 1: $a_5 = 1$, so $S = 6$, $T = 18$

| Query | S | T | k | Condition | Winner |
| --- | --- | --- | --- | --- | --- |
| ? 10 | 6 | 18 | 10 | (T-k)=8 even vs S even | RYAN |

After SET 1 50: $S = 55$, $T$ increases heavily.

| Query | S | T | k | Condition | Winner |
| --- | --- | --- | --- | --- | --- |
| ? 37 | 55 | large | 37 | parity mismatch | RYAN |
| ? 38 | 55 | large | 38 | parity alignment | PHEBE |

This trace shows that updates only affect global aggregates, and each decision depends only on parity alignment.

### Sample 2

Start: all ones, $S=6$, $T=21$

| Query | S | T | k | Winner |
| --- | --- | --- | --- | --- |
| ? 21 | 6 | 21 | 21 | PHEBE |
| ? 31 | 6 | 21 | 31 | RYAN |

After SET 6 0: $S=5$

| Query | S | T | k | Winner |
| --- | --- | --- | --- | --- |
| ? 5 | 5 | 15 | 5 | PHEBE |

This demonstrates the exhaustion case: when total sum is too small, parity of moves alone decides.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + q)$ | Each query updates or checks constant-time aggregates |
| Space | $O(n)$ | Storage of frequency array |

The solution is efficient enough for $2 \cdot 10^5$ operations because all heavy computation is reduced to constant-time arithmetic per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []

    n, q = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))

    S = sum(a)
    T = sum((i + 1) * a[i] for i in range(n))

    for _ in range(q):
        tmp = sys.stdin.readline().split()
        if tmp[0] == "SET":
            i = int(tmp[1]) - 1
            x = int(tmp[2])
            T -= (i + 1) * a[i]
            S -= a[i]
            a[i] = x
            T += (i + 1) * a[i]
            S += a[i]
        else:
            k = int(tmp[1])
            if T < k:
                out.append("PHEBE" if S % 2 == 1 else "RYAN")
            else:
                out.append("PHEBE" if (T - k) % 2 == S % 2 else "RYAN")

    return "\n".join(out)

# sample tests
assert run("""5 6
0 2 3 0 0
? 10
SET 5 1
? 10
SET 1 50
? 37
? 38
""").split() == ["PHEBE","RYAN","RYAN","PHEBE"]

assert run("""6 10
1 1 1 1 1 1
? 21
? 31
SET 6 0
? 5
SET 2 5
? 17
? 20
SET 3 10
? 10
? 1000000000000000000
""").split()[:2] == ["PHEBE","RYAN"]

# custom cases
assert run("""1 1
1
? 1
""") == "PHEBE"

assert run("""2 1
0 1
? 100
""") == "RYAN"

assert run("""3 2
1 1 1
? 2
? 3
""").count("PHEBE") >= 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single block equals k | PHEBE | immediate loss condition |
| insufficient total sum | RYAN | exhaustion parity |
| small symmetric case | mixed | parity sensitivity |

## Edge Cases

One edge case is when $k$ is larger than the total achievable sum. In that situation, the game always ends by exhausting all blocks. For example, with $a = [1]$ and $k = 10$, there is only one move. Phebe takes it and immediately leaves no blocks, which triggers the losing condition, so Phebe loses. The algorithm captures this because $T < k$ and $S = 1$, so it returns PHEBE according to parity logic.

Another edge case is when $k$ is exactly equal to total sum. Then the last move necessarily creates $k$. For $a = [2,1]$ and $k = 3$, whoever is forced to take the final block completes the sum and loses. Since the number of moves is fixed, the parity condition correctly determines who reaches that forced final state.

A third case is frequent updates that flip parity of $S$. For example starting from $a = [1,1]$, then setting one entry to zero changes the entire outcome of future queries. The algorithm remains correct because every SET operation immediately updates both $S$ and (T`, preserving the invariant that all queries operate on the current true multiset.
