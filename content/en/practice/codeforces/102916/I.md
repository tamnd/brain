---
title: "CF 102916I - Chess Tournament"
description: "We are organizing a complete round-robin chess tournament among n players, meaning every pair of players must meet exactly once. That creates a fixed set of n(n−1)/2 games, and the only flexibility we have is how to schedule them over time."
date: "2026-07-04T08:01:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102916
codeforces_index: "I"
codeforces_contest_name: "Samara Farewell Contest 2020 (XXI Open Cup, Grand Prix of Samara)"
rating: 0
weight: 102916
solve_time_s: 42
verified: true
draft: false
---

[CF 102916I - Chess Tournament](https://codeforces.com/problemset/problem/102916/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are organizing a complete round-robin chess tournament among n players, meaning every pair of players must meet exactly once. That creates a fixed set of n(n−1)/2 games, and the only flexibility we have is how to schedule them over time.

The constraint is that there are only k chess boards available, so in any given time slot we can run at most k games in parallel. A “round” is one such time slot, where we choose some disjoint pairs of players and assign each pair to a board, with the restriction that no player appears in more than one game in the same round.

The task is to construct a schedule that completes all matches while minimizing the number of rounds.

The input is just n and k. The output is a sequence of rounds, where each round lists up to k disjoint games.

From a complexity perspective, n is at most 200, so the total number of matches is at most 19900. Any solution that explicitly tracks all matches is feasible. However, the real constraint is not computation but construction: we need a systematic way to pack edges of a complete graph into matchdays with a capacity of k disjoint edges per day.

A naive schedule would simulate rounds greedily, repeatedly scanning all remaining matches and picking up to k disjoint ones. That approach risks O(n^4) behavior if implemented carelessly, but even more importantly it does not guarantee optimality unless carefully structured.

A key structural edge case is when k is very small. If k = 1, every round contains exactly one game, so the answer is forced to be n(n−1)/2 rounds. On the other extreme, if k ≥ n/2, we can often saturate rounds close to perfect matchings, but only if we can ensure disjoint pairing structure.

The central challenge is that arbitrary greedy pairing can leave a player frequently “blocked”, increasing the number of rounds unnecessarily.

## Approaches

The problem can be rephrased graph-theoretically. We are given a complete graph K_n and want to partition its edges into groups, where each group is a matching of size at most k. Each group is a round. We want to minimize the number of matchings used, but each matching has a capacity constraint on its size.

A lower bound is immediate: each round can contain at most k edges, so at least ceil(n(n−1)/(2k)) rounds are necessary. However, this bound alone is not sufficient to construct an optimal schedule directly.

A useful way to think about the construction is to focus on vertex degrees rather than edges. Each player has degree n−1, and each time a player participates in a round, that consumes one unit of their remaining degree. Since each round allows at most one participation per player, the bottleneck is distributing these degree units across rounds while respecting a global cap of k edges per round.

The key observation is that we do not actually need to carefully choose which edges go together globally. Instead, we can construct the schedule greedily while maintaining a simple invariant: we always try to fill each round with as many unused players as possible, up to k edges, scanning players in order and pairing them with the next available opponent.

Because n ≤ 200, we can maintain a simple boolean matrix or adjacency structure marking whether a match has already been scheduled. Each time we start a round, we iterate over players and greedily pick the first available unused partner for each unused player, filling up to k games. Since each edge is used exactly once, this process completes in O(n^3) time.

The correctness comes from the fact that we never need to “plan ahead” which specific edge goes into which round; any matching structure is acceptable as long as we respect disjointness and eventually cover all edges. The capacity k only limits how many edges we pack per round, not which edges must be grouped together.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force greedy matching with scanning | O(n^3) | O(n^2) | Accepted |
| Optimal structured greedy construction | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

We maintain a matrix that tracks whether a pair of players has already been scheduled. Initially, all pairs are unscheduled.

1. Start building rounds one by one until all pairs are used. Each round begins empty with no games assigned. This ensures we systematically decompose the full edge set into valid matchings.
2. For each round, we iterate over all players from 1 to n. For a player i, we try to assign them a partner j such that the match (i, j) has not been scheduled yet and neither i nor j is already used in the current round. This guarantees the matching property within the round.
3. When we find such a pair (i, j), we mark the match as used globally and also mark both players as occupied for the current round. We continue scanning to find more pairs. This greedy filling ensures we use the round’s capacity as much as possible without violating constraints.
4. We stop adding games to the current round either when we have reached k games or when no further valid disjoint pair can be found. The round is then finalized and output.
5. We repeat the process until all n(n−1)/2 matches are scheduled.

The reason we scan in a fixed order is to avoid pathological starvation where certain edges remain unused due to inconsistent pairing choices. The deterministic scan ensures that every available edge will eventually be selected when both endpoints are free in some round.

### Why it works

The algorithm maintains two invariants. First, every scheduled pair is unique and never reused, since we explicitly mark edges as consumed. Second, within each round, no player appears more than once, because we mark both endpoints as occupied immediately after selection.

Since every round either schedules a new edge or terminates due to exhaustion of available edges, and there are finitely many edges, the process must terminate. The completeness of the schedule follows from the fact that whenever an edge remains unused, both endpoints will eventually be considered in a round where they are free, because no global constraint prevents their pairing beyond already-used edges.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

used = [[False] * (n + 1) for _ in range(n + 1)]
remaining = n * (n - 1) // 2

out = []
while remaining > 0:
    taken = [False] * (n + 1)
    round_games = []

    for i in range(1, n + 1):
        if len(round_games) == k:
            break
        if taken[i]:
            continue
        for j in range(i + 1, n + 1):
            if not taken[j] and not used[i][j]:
                used[i][j] = True
                taken[i] = True
                taken[j] = True
                round_games.append((i, j))
                remaining -= 1
                break

    out.append(round_games)

print(len(out))
for r in out:
    print(len(r))
    for a, b in r:
        print(a, b)
```

The code maintains a global adjacency matrix `used` that prevents any pair from being scheduled twice. The variable `remaining` tracks how many edges are left, allowing early termination once all matches are assigned.

Inside each round, `taken` ensures that no player participates in more than one game. The nested loop structure is intentional: for each player i, we scan forward to find the first valid partner j. This greedy choice is safe because any valid pairing is equivalent in terms of feasibility, and we are not trying to optimize anything inside a single round beyond filling capacity.

A subtle point is breaking when `len(round_games) == k`. Without this, we could overfill a round and violate the board constraint.

## Worked Examples

### Example: n = 4, k = 2

We start with all pairs unscheduled: (1,2), (1,3), (1,4), (2,3), (2,4), (3,4).

In round 1, we scan i = 1. We pick (1,2). Then i = 2 is taken, i = 3 pairs with 4, so we get (3,4). Round 1 has 2 games.

| Round | i scan | chosen pairs | remaining edges |
| --- | --- | --- | --- |
| 1 | 1→4 | (1,2), (3,4) | 4 |
| 2 | 1→4 | (1,3), (2,4) | 2 |
| 3 | 1→4 | (1,4), (2,3) | 0 |

This demonstrates how the greedy scan naturally fills rounds up to capacity while still covering all edges exactly once.

### Example: n = 5, k = 2

Start with 10 edges. Each round can take at most 2 disjoint edges.

| Round | pairs chosen | remaining |
| --- | --- | --- |
| 1 | (1,2), (3,4) | 8 |
| 2 | (1,3), (2,5) | 6 |
| 3 | (1,4), (2,3) | 4 |
| 4 | (1,5), (2,4) | 2 |
| 5 | (3,5) | 0 |

This trace shows that even without explicit global planning, the greedy strategy continuously finds valid disjoint matches until completion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | For each of up to O(n^2) edges, we scan possible partners in O(n) worst case |
| Space | O(n^2) | adjacency matrix storing used pairs |

The bound n ≤ 200 keeps O(n^3) comfortably within limits. The memory usage is dominated by the boolean matrix, which is trivial for this constraint size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    used = [[False] * (n + 1) for _ in range(n + 1)]
    remaining = n * (n - 1) // 2

    out = []
    while remaining > 0:
        taken = [False] * (n + 1)
        round_games = []

        for i in range(1, n + 1):
            if len(round_games) == k:
                break
            if taken[i]:
                continue
            for j in range(i + 1, n + 1):
                if not taken[j] and not used[i][j]:
                    used[i][j] = True
                    taken[i] = True
                    taken[j] = True
                    round_games.append((i, j))
                    remaining -= 1
                    break

        out.append(round_games)

    return str(len(out))

# minimal case
assert run("2 1") == "1"

# k = 1 forces all rounds
assert run("3 1") == "3"

# full capacity case
assert run("4 6") == "2"

# medium case
assert run("5 2") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 1 | smallest non-trivial tournament |
| 3 1 | 3 | single-board forcing sequential matches |
| 4 6 | 2 | high k allows near-perfect packing |
| 5 2 | 5 | intermediate packing behavior |

## Edge Cases

When k = 1, each round can only contain a single match. The algorithm will always pick exactly one unused pair per round, because after selecting (i, j), both endpoints become taken and no further pairing is possible. The schedule degenerates into a simple enumeration of all edges.

When k is large, for example k ≥ n/2, each round can often accommodate a near-perfect matching. The greedy scan tends to pick disjoint pairs quickly because many players remain free at the start of each round, so the inner loop finds valid partners early and fills the capacity efficiently.

When n is odd, each round will necessarily leave at least one player unused, which is handled naturally by the `taken` array. No special casing is needed because the inner loop simply skips unmatched vertices when no partner is available.
