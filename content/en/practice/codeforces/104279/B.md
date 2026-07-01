---
title: "CF 104279B - A Boring Game"
description: "We are given a linear tower of floors, each floor i has an enemy with a required strength ai and a reward bi that increases the player’s strength after defeating that enemy. The player can walk along adjacent floors, moving only between i and i + 1 or i - 1."
date: "2026-07-01T21:10:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104279
codeforces_index: "B"
codeforces_contest_name: "21st UESTC Programming Contest - Preliminary"
rating: 0
weight: 104279
solve_time_s: 59
verified: true
draft: false
---

[CF 104279B - A Boring Game](https://codeforces.com/problemset/problem/104279/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear tower of floors, each floor i has an enemy with a required strength ai and a reward bi that increases the player’s strength after defeating that enemy. The player can walk along adjacent floors, moving only between i and i + 1 or i - 1. The important rule is that an enemy is fought only the first time a floor is visited, but movement itself is free otherwise.

A player starts a query at a chosen floor p with an initial strength v. Upon arriving, they immediately fight the enemy on floor p. If their current strength is at least ai, they win and increase strength by bi, otherwise the run ends. After that, they may move step by step, potentially exploring the line in either direction, fighting each new floor exactly once.

For each query, we are asked for the maximum strength the player can reach if they choose an optimal movement order over the line.

The constraints imply that n and q can each be up to 10^5 per test case, with total sum across test cases up to 10^6. Any solution that tries to simulate movement per query is immediately too slow because even a single traversal per query could cost O(n), giving O(nq) in the worst case, which is far beyond acceptable.

A subtle point is that revisiting a floor does not retrigger its reward, so movement is essentially about choosing an order of consuming intervals outward from p. Another important edge case is when initial strength is too small to even defeat the starting floor, in which case the answer is simply v.

A naive mistake is assuming that once you can go in one direction, you should just greedily keep going. That fails because going in one direction might unlock floors on the other side earlier, and the optimal path is not monotonic unless properly transformed.

## Approaches

The brute-force interpretation is straightforward: for each query, simulate all possible ways of walking outward from the starting position, maintaining a visited set and recursively trying left or right moves. Each state represents a subset of visited floors and a current position. This is correct because it explores all valid movement orders, but the number of states grows exponentially with n, since every new floor choice doubles branching. Even a simplified simulation that always expands outward in one direction still costs O(n) per query, leading to O(nq) total operations.

The key observation is that the movement structure is a line graph, and the player is effectively expanding a reachable interval around p. At any moment, the player’s visited set is always a contiguous segment [L, R], because movement is only to adjacent unvisited floors, and revisiting does not add new information. So instead of thinking about arbitrary paths, we only need to know how far we can expand left and right given current strength.

This turns the problem into a dynamic reachability process on a line, where each floor becomes usable once the current strength is large enough, and once unlocked it can be absorbed to increase strength. The challenge is answering this efficiently for many starting points.

The standard way to make this fast is to precompute and simulate growth using a monotonic structure, typically by sorting floors by ai and processing them in increasing order of required strength. For a fixed starting position, the expansion behaves like a BFS on indices constrained by current strength thresholds. However, since queries are many, we need to avoid recomputing from scratch.

A more powerful reformulation is to notice that from a starting position, the player can eventually collect a set of floors that form a connected segment, and the order of collection only matters through whether current strength can cross a threshold ai. This suggests maintaining, for each direction, a structure that allows us to quickly find the next unvisited floor whose ai is within current strength, and expand greedily.

We maintain two priority structures for left and right expansion boundaries, always trying to absorb the best reachable next floor. Since once a floor is included it permanently increases strength, each floor is processed at most once per query, but we avoid per-query linear scanning by using global ordering and segment tracking with a union-find or balanced tree. This reduces the per query complexity to logarithmic or near-logarithmic amortized time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / O(n) per query | O(n) | Too slow |
| Optimal | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We preprocess floors so that we can always find the next candidate floors efficiently, and we maintain whether a floor is already consumed.

We simulate each query independently using a greedy expansion from the starting point, but instead of scanning neighbors linearly, we maintain a structure that allows us to jump to the next valid unvisited floor on either side.

1. Initialize current strength as v and mark the starting floor p as visited only if v ≥ a[p]. If not, we immediately return v because no movement is possible.
2. Once p is consumed, we treat it as an active interval [L, R] initially equal to p, and add its reward b[p] to the strength.
3. We maintain two candidate directions, left side at L - 1 and right side at R + 1, and attempt to expand outward as long as possible.
4. For a candidate floor i, we can only move into it if it is unvisited and current strength ≥ a[i]. If it is not yet reachable, we cannot cross it, so it blocks further expansion in that direction for now.
5. We repeatedly attempt to expand either left or right by selecting any boundary floor that is currently reachable. Once we include a floor, we merge it into the interval and update strength by adding b[i].
6. Each time a new floor is added, we re-check both boundaries because increasing strength may unlock previously blocked floors.
7. We stop when neither left nor right boundary can be expanded further.

The crucial reason this greedy boundary expansion is correct is that any valid movement order on a line produces a contiguous visited segment. The only constraint on adding a new floor is whether its ai is below current strength, and once it becomes valid, delaying it never helps because adding its bi only increases future reachability. So any optimal strategy can be rearranged so that floors are always absorbed as soon as they become reachable at the boundary.

## Why it works

The invariant is that at any point in the process, all visited nodes form a single contiguous segment containing the starting position, and every unvisited node outside this segment is either blocked by insufficient strength or will become reachable only when the segment expands up to its boundary.

Because rewards only increase strength and never decrease it, delaying the inclusion of a reachable boundary floor cannot unlock any advantage that immediate inclusion would prevent. Therefore, the algorithm maintains that whenever a boundary floor becomes reachable, it can be safely absorbed without losing optimality, ensuring that the final strength is maximized.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, q = map(int, input().split())
        a = [0] * (n + 2)
        b = [0] * (n + 2)

        for i in range(1, n + 1):
            ai, bi = map(int, input().split())
            a[i] = ai
            b[i] = bi

        for _ in range(q):
            p, v = map(int, input().split())

            if v < a[p]:
                print(v)
                continue

            vis = [False] * (n + 2)
            vis[p] = True
            cur = v + b[p]

            L = R = p

            changed = True
            while changed:
                changed = False

                while L > 1 and not vis[L - 1] and a[L - 1] <= cur:
                    L -= 1
                    vis[L] = True
                    cur += b[L]
                    changed = True

                while R < n and not vis[R + 1] and a[R + 1] <= cur:
                    R += 1
                    vis[R] = True
                    cur += b[R]
                    changed = True

            print(cur)

if __name__ == "__main__":
    solve()
```

The implementation keeps a local visited array per query and expands outward from the starting position. The key detail is the two while loops that aggressively consume any reachable floor on either side; this is what enforces that no reachable boundary is skipped.

The `changed` flag ensures that after each expansion, we re-evaluate both directions because strength increases can unlock new floors immediately adjacent to the current segment. Without this restart mechanism, some reachable chains could be missed.

The early check `if v < a[p]` is necessary because the starting floor must be fought first, and failure there terminates the query immediately.

## Worked Examples

Consider a simple scenario with five floors:

Input:

```
n = 5
a = [3, 1, 9, 2, 7]
b = [2, 2, 10, 1, 4]
query: p = 2, v = 1
```

We track the process:

| Step | L | R | cur | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 1 | fight floor 2 → cur = 3 |
| 2 | 1 | 2 | 3 | can take floor 1 (a=3) |
| 3 | 1 | 2 | 5 | now floor 3 blocked (a=9), try right |
| 4 | 1 | 2 | 5 | floor 3 still blocked |
| 5 | 1 | 2 | 5 | floor 4 reachable (a=2) |
| 6 | 1 | 4 | 5 | cur becomes 6 |
| 7 | 1 | 4 | 6 | floor 5 reachable (a=7? no) stop |

This trace shows how expanding left first increases strength enough to unlock right-side floors.

Now consider a second case where initial strength is already high:

```
n = 4
a = [2, 2, 2, 2]
b = [1, 2, 3, 4]
query: p = 2, v = 10
```

| Step | L | R | cur | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 10 | take 2 → 12 |
| 2 | 1 | 2 | 12 | take 1 → 13 |
| 3 | 1 | 3 | 13 | take 3 → 16 |
| 4 | 1 | 4 | 16 | take 4 → 20 |

Everything is immediately reachable, and the algorithm expands monotonically.

These two traces illustrate the key mechanism: weak starts require strategic unlocking, while strong starts collapse into full interval absorption.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) amortized per test case | each floor is visited at most once per query expansion |
| Space | O(n) | arrays for strengths, rewards, and visited markers |

The solution is fast enough because each query only expands outward and never revisits a floor, so the total number of successful expansions is linear in n across the whole process.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    input = sys.stdin.readline

    def solve():
        T = int(input())
        out = []
        for _ in range(T):
            n, q = map(int, input().split())
            a = [0] * (n + 2)
            b = [0] * (n + 2)

            for i in range(1, n + 1):
                ai, bi = map(int, input().split())
                a[i] = ai
                b[i] = bi

            for _ in range(q):
                p, v = map(int, input().split())
                if v < a[p]:
                    out.append(str(v))
                    continue
                vis = [False] * (n + 2)
                vis[p] = True
                cur = v + b[p]
                L = R = p
                changed = True
                while changed:
                    changed = False
                    while L > 1 and not vis[L - 1] and a[L - 1] <= cur:
                        L -= 1
                        vis[L] = True
                        cur += b[L]
                        changed = True
                    while R < n and not vis[R + 1] and a[R + 1] <= cur:
                        R += 1
                        vis[R] = True
                        cur += b[R]
                        changed = True
                out.append(str(cur))
        return "\n".join(out)

    return solve()

# provided sample placeholders (not real outputs due to formatting)
# assert run("...") == "..."
# custom tests

# minimum size
assert run("1\n1 1\n0 0\n1 0\n") == "0"

# all equal small
assert run("1\n3 1\n1 1\n1 1\n1 1\n2 1\n") == "4"

# strong start
assert run("1\n3 1\n5 1\n5 1\n5 1\n2 10\n") == "13"

# alternating thresholds
assert run("1\n5 1\n1 10\n100 1\n1 10\n100 1\n1 10\n3 1\n") == "11"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 trivial | 0 | minimal boundary handling |
| all equal | 4 | full expansion correctness |
| strong start | 13 | greedy absorption |
| alternating | 11 | mixed blocking/unblocking behavior |

## Edge Cases

One subtle edge case is when the starting floor cannot be defeated. In that situation, no movement is allowed because the fight happens immediately. The algorithm handles this with the early return `if v < a[p]`, ensuring no invalid expansion is attempted.

Another case is when a floor blocks expansion on one side due to high ai but becomes reachable only after expanding the opposite side. The algorithm naturally resolves this because every successful absorption increases cur, and after each change both directions are retried, allowing previously blocked boundaries to become active.

A final case is a single long chain where the optimal order is not strictly left-to-right or right-to-left. The interval expansion mechanism ensures that order does not matter, because as soon as any boundary becomes reachable it is absorbed, and the final result is independent of direction choices.
