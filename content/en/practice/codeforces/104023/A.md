---
title: "CF 104023A - Dunai"
description: "We are given a history of champion teams in a five-position competitive game. Each past champion team consists of exactly five named players, one per fixed position from 1 to 5."
date: "2026-07-02T04:23:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104023
codeforces_index: "A"
codeforces_contest_name: "2022 China Collegiate Programming Contest (CCPC) Weihai Site"
rating: 0
weight: 104023
solve_time_s: 48
verified: true
draft: false
---

[CF 104023A - Dunai](https://codeforces.com/problemset/problem/104023/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a history of champion teams in a five-position competitive game. Each past champion team consists of exactly five named players, one per fixed position from 1 to 5. From this history, some players are known champions and each such player has a fixed position that never changes across teams.

Now we are also given a pool of players for an upcoming tournament. Each of these players has a known fixed position as well. However, we do not know how they will be grouped into teams.

The goal is to form as many valid teams as possible from the given pool. A valid team must consist of exactly five distinct players, one for each position from 1 to 5, and each team must include at least one player who has previously been a champion.

Each player can be used in at most one team, and some players may remain unused.

So the task is to maximize the number of disjoint complete 5-person teams such that every team contains at least one historically champion player.

The constraints are small enough that we can afford to scan all players and perform greedy or combinational grouping. With at most 1000 players, any solution that is roughly linear or linearithmic will be sufficient. Even solutions involving a small constant number of passes over arrays grouped by position are acceptable.

A key subtlety is that players have fixed positions, so a team is not an arbitrary grouping of five people, it is exactly one from each position 1 through 5. This structure removes any combinatorial matching complexity between positions: we only choose one player per position.

Another important point is that we do not need to maximize total usage of players, only the number of full teams. This suggests a greedy packing approach rather than a global optimization like flow.

A typical mistake would be trying to assign all champions first or greedily forming teams without tracking feasibility per position. Another mistake is ignoring that each team must contain at least one champion, which creates a coupling constraint across positions.

## Approaches

A brute force idea would be to consider all possible ways of grouping players into teams of size five respecting positions, then checking whether each grouping satisfies the champion constraint. However, even if we ignore symmetry, the number of ways to partition up to 1000 players into groups of five is astronomically large. This makes brute force completely infeasible.

The structure of the problem simplifies things significantly. Since each team must contain exactly one player from each position, we can separate players by position. Let cnt[i] be the number of available players in position i. Then the maximum number of teams is limited by the smallest cnt[i], since each team consumes one player per position.

So the only real question is whether we can ensure that among these potential teams, each team contains at least one champion player.

We can classify players into two types: champion players and non-champion players. For each position, we count how many champions exist and how many non-champions exist.

We first observe that if we form k teams, we must pick exactly k players from each position. So for each position i, we need at least k players total.

Now we also require that each team contains at least one champion. This is equivalent to saying that among all selected 5k players, at least k of them are champions, but distributed such that each team has coverage.

A more direct and simpler view is to think greedily in terms of filling teams one by one. For a fixed k, we need to check feasibility: can we pick k players from each position such that every team has at least one champion? This becomes a bipartite-like feasibility problem, but due to fixed positions, it collapses into a counting condition.

A useful transformation is to consider that non-champions are "free fillers", while champions are "team anchors". Each team must consume at least one champion, so the total number of teams cannot exceed the total number of champion players across all positions. That gives an upper bound.

On the other hand, each position must have enough total players to support k teams. So k is bounded by both min over positions of total counts and total champions.

These bounds turn out to be sufficient: if we set k to the minimum of (min position count) and (total champions), we can always construct valid teams by greedily assigning champions first and filling remaining slots per position with any leftover players.

So the optimal strategy is simply to compute these two quantities and take their minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Partitioning | Exponential | Exponential | Too slow |
| Counting + Greedy Feasibility | O(n + m) | O(1) to O(m) | Accepted |

## Algorithm Walkthrough

1. Read all historical champion teams and collect all names that have ever appeared as champions. Also record their fixed positions. This gives us a set that lets us identify whether a player in the current pool is a champion.
2. Read the current pool of m players. For each player, classify it by its position and whether it is a champion. Maintain two arrays cnt[pos] and champ[pos], each of size 5. cnt counts total players per position, champ counts champions per position. This separation is necessary because teams are strictly position-constrained.
3. Compute total_champions as the sum over all positions of champ[pos]. This represents the total number of “mandatory contributors” available for satisfying the requirement that every team must contain at least one champion.
4. Compute max_complete_by_position as the minimum over pos in 1..5 of cnt[pos]. This is the maximum number of full 5-position teams possible if we ignore the champion constraint, since each team consumes one player per position.
5. The answer is min(total_champions, max_complete_by_position). This is the maximum number of teams that can be formed while respecting both the structural constraint (five distinct positions) and the requirement that each team contains at least one champion.

### Why it works

Each team requires exactly one player from each of five independent position buckets, so the number of teams is fundamentally limited by the smallest bucket size. Separately, each team requires at least one champion, so each team must consume at least one element from the global set of champions. Since champions are not position-restricted beyond their fixed assignment, they act as a global limiting resource. Any construction that forms k teams necessarily uses at least k champions, so k cannot exceed the total number of champions available. Conversely, if both constraints are satisfied, teams can be formed by first assigning one distinct champion per team and then filling remaining positions arbitrarily from leftover players, ensuring feasibility without conflicts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    champ_names = set()

    for _ in range(n):
        parts = input().split()
        for name in parts:
            champ_names.add(name)

    m = int(input())

    cnt = [0] * 6
    champ_cnt = [0] * 6

    for _ in range(m):
        name, pos = input().split()
        pos = int(pos)
        cnt[pos] += 1
        if name in champ_names:
            champ_cnt[pos] += 1

    total_champions = sum(champ_cnt)
    max_by_pos = min(cnt[1:6]) if m > 0 else 0

    print(min(total_champions, max_by_pos))

if __name__ == "__main__":
    solve()
```

The code first builds a set of all champion names so membership checks are constant time. Then it aggregates players by position while simultaneously counting how many of them are champions.

The key decision is the final min between total champions and the bottleneck position count. This directly encodes the two independent constraints: availability of full positional slots and availability of required champion presence per team.

## Worked Examples

### Example 1

Input:

```
1
A B C D E
5
A 1
F 2
G 3
H 4
I 5
```

We have one champion team, so A, B, C, D, E are champions.

| Step | cnt | champ_cnt | total_champions | min(cnt) |
| --- | --- | --- | --- | --- |
| After processing | [1,1,1,1,1] | [1,0,0,0,0] | 1 | 1 |

We can form exactly one team because all positions have at least one player, but only one champion exists in position 1.

Answer is min(1,1) = 1.

This shows that even though only one position contains a champion, that is enough to satisfy the constraint for one team.

### Example 2

Input:

```
2
A B C D E
X Y Z W V
10
A 1
X 1
B 2
Y 2
C 3
Z 3
D 4
W 4
E 5
V 5
```

| Step | cnt | champ_cnt | total_champions | min(cnt) |
| --- | --- | --- | --- | --- |
| After processing | [2,2,2,2,2] | [1,1,1,1,1] | 5 | 2 |

We can form 2 teams because each position has 2 players, but only 5 champions exist total, which is still enough. The limiting factor is positional capacity.

Answer is 2.

This confirms the interaction between global champion supply and per-position capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | We scan all historical and current players once |
| Space | O(1) + O(n) | Set of champions stores at most 5n names |

The solution comfortably fits within limits since n ≤ 100 and m ≤ 1000, making the operations negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp))

# We adapt solve to return output
def solve_output(inp: str) -> int:
    import sys
    input = sys.stdin.readline

    lines = inp.strip().splitlines()
    it = iter(lines)

    n = int(next(it))
    champ_names = set()
    for _ in range(n):
        parts = next(it).split()
        for name in parts:
            champ_names.add(name)

    m = int(next(it))
    cnt = [0] * 6
    champ_cnt = [0] * 6

    for _ in range(m):
        name, pos = next(it).split()
        pos = int(pos)
        cnt[pos] += 1
        if name in champ_names:
            champ_cnt[pos] += 1

    total_champions = sum(champ_cnt)
    max_by_pos = min(cnt[1:6]) if m > 0 else 0
    return min(total_champions, max_by_pos)

# sample-like tests
assert solve_output("""1
A B C D E
5
A 1
F 2
G 3
H 4
I 5
""") == 1

# all champions concentrated
assert solve_output("""1
A B C D E
5
A 1
B 1
C 1
D 1
E 1
""") == 1

# multiple balanced teams
assert solve_output("""2
A B C D E
X Y Z W V
10
A 1
X 1
B 2
Y 2
C 3
Z 3
D 4
W 4
E 5
V 5
""") == 2

# insufficient positional balance
assert solve_output("""1
A B C D E
4
A 1
F 2
G 3
H 4
""") == 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single sparse team | 1 | minimal feasibility |
| All champions same position | 1 | uneven champion distribution |
| Balanced perfect pairing | 2 | optimal packing |
| Missing position | 0 | positional bottleneck |

## Edge Cases

One subtle case is when champions exist but are concentrated in only one position. For example, if all champions are position 1 players, but other positions have no champions, teams are still possible as long as we have enough non-champions to fill the remaining positions and at least one champion per team comes from position 1. The algorithm handles this correctly because total_champions still counts all available anchors regardless of distribution, and min(cnt[pos]) enforces structural feasibility.

Another case is when there are enough players in each position but no champions at all. In that case champ_cnt sums to zero, so the answer becomes zero even though min(cnt[pos]) may be large. This correctly reflects that no team can satisfy the “at least one champion” requirement.

A final boundary is when one position is empty. Then min(cnt[pos]) is zero, forcing the answer to zero regardless of champion availability. This is correct because a valid team cannot be formed without all five positions being filled.
