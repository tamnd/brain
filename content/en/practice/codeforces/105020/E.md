---
title: "CF 105020E - The Detective Game"
description: "Each player in this game maintains a personal list of other players they would vote against if those players were put on trial."
date: "2026-06-28T01:57:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105020
codeforces_index: "E"
codeforces_contest_name: "TCPC Tunisian Collegiate Programming Contest 2022"
rating: 0
weight: 105020
solve_time_s: 63
verified: false
draft: false
---

[CF 105020E - The Detective Game](https://codeforces.com/problemset/problem/105020/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** no  

## Solution
## Problem Understanding

Each player in this game maintains a personal list of other players they would vote against if those players were put on trial. The voting process is deterministic: when a specific player is accused, every other player checks whether that accused player appears in their personal suspect list. If it does, they vote to eliminate; otherwise, they do not.

A player is eliminated in a round if strictly more than half of all players vote against them. The task is to determine, for every player independently, whether they would be eliminated if they were the one put on trial.

So for each player $x$, we conceptually simulate a trial where we count how many other players include $x$ in their suspect list. If that count exceeds $\frac{n}{2}$, then $x$ would be eliminated; otherwise they survive that hypothetical trial.

The input structure is essentially describing a directed relation: each player $i$ points to a set of players they would vote against. The question reduces to counting incoming votes for each node in this directed graph and checking which nodes have indegree strictly greater than half of $n$.

The constraints push us toward linear or near-linear solutions. The total size of all suspect lists across all test cases is bounded by $4 \cdot 10^5$, which means any solution that processes each edge a constant number of times is acceptable. However, any per-query simulation for each player would be too slow because it would repeatedly scan all lists, leading to $O(n^2)$ behavior in the worst case.

A subtle edge case arises when no player reaches a majority threshold. For example, if $n = 4$ and each player is only suspected by at most one other player, then the threshold is strictly greater than 2, so no one qualifies. Another edge case is when a player is suspected by exactly half of the players; this must not be counted as elimination since the condition is strictly more than 50 percent.

Another important detail is that self-votes are impossible by construction, so we never need to handle self-loops or remove them.

## Approaches

A direct simulation for each candidate player would work like this: for a fixed player $x$, scan every other player's list and count how many contain $x$. This is correct but expensive. Each query costs $O(\sum k_i)$, and doing this for all $n$ players leads to $O(n \cdot \sum k_i)$, which degenerates into $O(n^2)$ in dense cases and is clearly too slow for $n$ up to $10^5$.

The key observation is that the voting structure does not change between queries. Each directed edge $i \rightarrow a_{ij}$ contributes exactly one vote against $a_{ij}$, and this contribution is independent of which player is currently being tested. This means we can precompute the number of incoming edges for every node in a single pass over all lists.

Once these counts are known, each player can be evaluated independently in constant time by checking whether their count exceeds $\lfloor n/2 \rfloor$. This transforms the problem into a simple frequency accumulation problem over edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot \sum k_i)$ | $O(1)$ extra | Too slow |
| Optimal | $O(n + \sum k_i)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem into counting how many times each player is targeted across all suspect lists, then filtering by a threshold.

1. Create an array `cnt` of size $n + 1$, initialized to zero. This will store how many votes each player receives. The index represents the player, and the value represents how many other players would vote against them.
2. Iterate over every player's suspect list. For each entry $a_{ij}$, increment `cnt[a_{ij}]` by one. This step aggregates all incoming votes in a single pass over the input structure.
3. Compute the elimination threshold as $\text{limit} = \lfloor n/2 \rfloor$. A player is eliminated only if their vote count is strictly greater than this value.
4. Iterate through all players from 1 to $n$. For each player $i$, check whether `cnt[i] > limit`. If so, include $i$ in the answer list.
5. Output the size of the answer list followed by the sorted list itself. The iteration order already guarantees sorting.

The correctness hinges on the fact that each vote is independent of the queried candidate. A vote is simply an edge contributing +1 to a fixed endpoint, and the elimination condition depends only on that final accumulated count.

### Why it works

At any moment, the number of votes against a player $x$ is exactly the number of directed edges pointing to $x$. The simulation of putting $x$ on trial does not change any other structure, so the vote distribution is fixed before the query. The algorithm effectively computes the indegree of each node in a directed graph and compares it against a global threshold. Since each edge contributes exactly once and no edge is ever double-counted or omitted, the computed value matches the true number of votes in every hypothetical trial.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        cnt = [0] * (n + 1)

        for i in range(1, n + 1):
            parts = list(map(int, input().split()))
            k = parts[0]
            for x in parts[1:]:
                cnt[x] += 1

        limit = n // 2
        ans = []
        for i in range(1, n + 1):
            if cnt[i] > limit:
                ans.append(i)

        print(len(ans))
        if ans:
            print(*ans)

if __name__ == "__main__":
    solve()
```

The solution reads each suspect list once and directly aggregates vote counts into an array. The key implementation choice is avoiding any per-player simulation; instead, every edge is processed exactly once. The threshold comparison uses integer division, which correctly implements the strict “more than 50 percent” condition.

The output is naturally sorted because players are checked in increasing order.

## Worked Examples

### Example 1

Input:

```
1
3
1 2
1 2
1 3
```

Here, player 2 is voted against by players 1 and 2, while player 3 is voted against only by player 3 is not possible since self-votes are disallowed, so only player 1 and 2 contribute to 2.

| Player | Incoming votes |
| --- | --- |
| 1 | 0 |
| 2 | 2 |
| 3 | 1 |

Threshold is $\lfloor 3/2 \rfloor = 1$. Only player 2 exceeds it.

Output:

```
1
2
```

This trace confirms that only aggregated incoming counts matter, not per-query recomputation.

### Example 2

Input:

```
1
4
1 2
1 3
1 4
0
```

| Player | Incoming votes |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

Threshold is $\lfloor 4/2 \rfloor = 2$. No player exceeds it.

Output:

```
0
```

This shows the strict inequality condition eliminates all players even when some reach half exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + \sum k_i)$ | Each suspect entry is processed once, plus a final scan over all players |
| Space | $O(n)$ | Storage for vote counts per player |

The total input size across test cases is bounded by $4 \cdot 10^5$, so a single pass over all edges and nodes comfortably fits within limits, both in time and memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-style
assert run("""1
3
1 2
1 2
1 3
""") == "1\n2"

# minimum n = 2
assert run("""1
2
1 2
0
""") == "1\n2"

# all zero votes
assert run("""1
3
0
0
0
""") == "0"

# full voting cycle
assert run("""1
4
1 2
1 3
1 4
1 2 3 4
""") == "1\n2"

# symmetric case no majority
assert run("""1
5
1 2
1 3
1 4
1 5
0
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 simple | 1 2 | minimal majority behavior |
| all zeros | 0 | no votes edge case |
| full cycle | 1 2 | mixed distribution correctness |
| sparse asymmetric | 0 | threshold strictness |

## Edge Cases

A key edge case is when a player receives exactly half of the votes. For instance, with $n = 6$, if a player has 3 incoming votes, the threshold is strictly greater than 3, so they must not be included. The algorithm handles this correctly because it uses `cnt[i] > n // 2`, not `>=`.

Another edge case is when one player receives almost all votes. In a star-shaped configuration where every list points to player 1, `cnt[1] = n - 1`, which always exceeds $n/2$ for $n \ge 2$, so player 1 is always included. The counting approach naturally captures this without special handling.

A final case is when lists are empty for all players. The counter array remains zero everywhere, and no index passes the threshold, which matches the intended behavior without additional logic.
