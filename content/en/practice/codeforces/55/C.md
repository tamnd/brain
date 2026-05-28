---
title: "CF 55C - Pie or die"
description: "We have an grid. Some cells contain pies, and several pies may share the same cell."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "games"]
categories: ["algorithms"]
codeforces_contest: 55
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 51"
rating: 1900
weight: 55
solve_time_s: 103
verified: true
draft: false
---
[CF 55C - Pie or die](https://codeforces.com/problemset/problem/55/C)

**Rating:** 1900  
**Tags:** games  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an $n \times m$ grid. Some cells contain pies, and several pies may share the same cell.

Each turn has two phases. First, Volodya chooses one pie and moves it by one cell in one of the four directions. If the pie is already on the boundary, he may move it outside the board through one border edge and instantly win the entire game. After that, if the game has not ended yet, Vlad blocks exactly one unit border edge of the board. Once blocked, that edge can never be used again to move a pie outside.

The game is about whether Volodya can eventually force a win assuming both players play perfectly.

The board dimensions are at most 100, and there are at most 100 pies. These limits are tiny, which is a signal that the real difficulty is not implementation complexity but finding the correct game-theoretic observation. A brute-force search over game states is still impossible because the state includes positions of all pies together with the set of already blocked border edges. Even a $100 \times 100$ board has 400 border edges, so the number of possible blocked-edge subsets alone is astronomical.

The dangerous part of this problem is that it looks like pathfinding, but the actual game depends only on border access. A naive idea such as "if some pie can reach the boundary then Volodya wins" is completely wrong because every border exit can eventually be blocked.

Several edge cases are easy to mishandle.

Consider a board with no pies:

```
2 2 0
```

The correct answer is `NO` because Volodya has nothing to move. Any implementation that only checks board dimensions or border size without handling $k=0$ separately will fail.

Another subtle case is when a pie already starts on the border:

```
2 2 1
1 2
```

The answer is `YES`. Volodya wins immediately on the first move before Vlad blocks anything. Forgetting move order leads to the wrong result.

The most important tricky case is when there are many pies but all are deep inside the board:

```
5 5 20
3 3
3 3
...
```

Even with many pies, the answer can still be `NO`. Vlad blocks only one border edge per turn, but Volodya also needs time to bring pies to the boundary. The decisive quantity is not the number of pies alone, but whether enough pies can threaten exits faster than Vlad can seal them.

A final subtlety is that different boundary cells contribute different numbers of exits. Corner cells have two border edges leading outside, while non-corner boundary cells have one. Treating every boundary cell equally loses crucial information.

## Approaches

A brute-force approach would model the entire game state. We would track all pie positions and all blocked border edges, then run minimax or retrograde analysis. This is theoretically correct because the game is finite and deterministic.

The problem is the state count explodes immediately. The board has $2n + 2m$ border edges. Each edge may be blocked or not, giving roughly $2^{2n+2m}$ possibilities even before considering pie positions. With $n=m=100$, this is completely hopeless.

The key observation is that the game only cares about one thing: how many turns Vlad needs to completely seal the board.

Every move by Vlad blocks exactly one border edge. The total number of border edges is:

$$2n + 2m$$

If Volodya can force some pie to reach an unblocked exit before all these edges are sealed, he wins.

Now think from the perspective of a single pie. Suppose its minimum distance to any boundary cell is $d$. Then Volodya needs exactly $d$ moves to place it on the boundary, and one more move to leave the board. So that pie can escape after $d+1$ Volodya moves.

Meanwhile, after each of those moves, Vlad blocks one edge. After $t$ turns, Vlad has blocked exactly $t$ border edges.

The critical insight is that a pie does not need all exits to stay open. It only needs one usable edge at the moment it reaches the boundary. Since the entire board has only $2n+2m$ exits total, Vlad eventually runs out of blocking capacity.

The official solution simplifies this even further. If there exists at least one pie whose distance to the nearest boundary is at most 4, then Volodya wins. Otherwise Vlad wins.

Why 4? Because the total number of distinct exits around any local region is too large for Vlad to seal quickly enough. A pie close enough to the boundary can always force access to some still-open edge before Vlad can close every possibility. If all pies are farther away than 4, Vlad has enough time to prepare a complete defense.

So the game reduces to checking whether some pie lies within distance 4 from the border.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(k)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the board dimensions and the number of pies.
2. For each pie at position $(x,y)$, compute its minimum distance to any board boundary.

The four distances are:

$$x-1,\ n-x,\ y-1,\ m-y$$

Their minimum tells us how many moves are needed to first reach a boundary cell.
3. If this minimum distance is at most 4 for any pie, immediately print `YES`.

A pie this close to the boundary can always force an escape before Vlad seals every relevant border edge.
4. If all pies have distance greater than 4, print `NO`.

Vlad has enough time to organize a complete blockade before any pie becomes dangerous.

### Why it works

The game is controlled entirely by timing.

A pie at distance $d$ from the boundary needs $d+1$ moves to escape. Vlad gains exactly one blocked edge after each move. If $d \le 4$, the pie reaches the boundary region quickly enough that there are still unavoidable open exits available. Vlad cannot simultaneously seal all possible escape routes in so few turns.

If every pie has distance at least 5, then Volodya needs many turns before any escape attempt becomes immediate. Vlad can use this time to block exits strategically and eventually prevent every possible escape. Since only border edges matter, interior movement no longer helps once the perimeter is controlled.

That dichotomy exactly matches the condition checked by the algorithm.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())

for _ in range(k):
    x, y = map(int, input().split())

    dist = min(x - 1, n - x, y - 1, m - y)

    if dist <= 4:
        print("YES")
        sys.exit()

print("NO")
```

The implementation is intentionally tiny because the hard part is discovering the game property.

For each pie, we compute the minimum number of steps required to reach any boundary cell. Since coordinates are 1-indexed, the top distance is `x - 1`, the bottom distance is `n - x`, the left distance is `y - 1`, and the right distance is `m - y`.

The moment we find a pie with distance at most 4, we can stop immediately and print `YES`. No further pies matter because Volodya only needs one successful escape.

The early `sys.exit()` avoids unnecessary processing and keeps the code simple.

A common off-by-one mistake is confusing "distance to boundary cell" with "distance to leave the board". The theorem already accounts for this correctly. We only check whether the boundary distance is at most 4.

## Worked Examples

### Example 1

Input:

```
2 2 1
1 2
```

Trace:

| Pie Position | Distances | Minimum Distance | Decision |
| --- | --- | --- | --- |
| (1,2) | 0,1,1,0 | 0 | YES |

The pie already starts on the boundary. Volodya immediately moves it outside before Vlad can block anything.

### Example 2

Input:

```
15 15 2
8 8
10 10
```

Trace:

| Pie Position | Distances | Minimum Distance | Decision |
| --- | --- | --- | --- |
| (8,8) | 7,7,7,7 | 7 | continue |
| (10,10) | 9,5,9,5 | 5 | continue |

No pie has distance at most 4, so the answer is `NO`.

This example demonstrates that even relatively central pies remain too slow. Vlad has enough turns to prepare a complete perimeter defense.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k)$ | Each pie is processed once |
| Space | $O(1)$ | Only a few integer variables are stored |

With at most 100 pies, the program runs instantly. Memory usage is negligible because we never store the entire board or simulate the game.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    for _ in range(k):
        x, y = map(int, input().split())

        dist = min(x - 1, n - x, y - 1, m - y)

        if dist <= 4:
            print("YES")
            return

    print("NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run(
"""2 2 1
1 2
"""
) == "YES", "sample 1"

# no pies
assert run(
"""5 5 0
"""
) == "NO", "no pies"

# pie exactly distance 4
assert run(
"""10 10 1
5 5
"""
) == "YES", "distance exactly 4"

# pie too far
assert run(
"""20 20 1
10 10
"""
) == "NO", "deep interior"

# multiple pies, one winning
assert run(
"""30 30 3
15 15
20 20
5 10
"""
) == "YES", "one reachable pie"

# smallest board
assert run(
"""1 1 1
1 1
"""
) == "YES", "already on boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 5 0` | `NO` | Handles empty input correctly |
| `10 10` with pie `(5,5)` | `YES` | Distance exactly 4 is winning |
| `20 20` with pie `(10,10)` | `NO` | Interior pies lose |
| Multiple pies with one close | `YES` | Only one winning pie is needed |
| `1 1 1` | `YES` | Smallest possible board |

## Edge Cases

Consider the empty-board case:

```
2 2 0
```

The algorithm never enters the loop over pies, so it directly prints `NO`.

This matches the game because Volodya has no legal move.

Now consider a pie already on the boundary:

```
3 3 1
1 2
```

The computed distances are:

$$0,\ 2,\ 1,\ 1$$

The minimum is 0, which is at most 4, so the algorithm prints `YES`.

Volodya wins instantly by moving the pie outside before Vlad acts.

Next, consider a pie exactly at the critical threshold:

```
10 10 1
5 5
```

Distances are:

$$4,\ 5,\ 4,\ 5$$

Minimum distance is 4, so the answer is `YES`.

This checks the inclusive boundary condition. Using `< 4` instead of `<= 4` would fail here.

Finally, consider a pie just beyond the threshold:

```
12 12 1
6 6
```

Distances are:

$$5,\ 6,\ 5,\ 6$$

Minimum distance is 5, so the algorithm prints `NO`.

This is the smallest losing interior configuration and catches off-by-one errors around the cutoff.
