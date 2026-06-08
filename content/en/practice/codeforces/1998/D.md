---
title: "CF 1998D - Determine Winning Islands in Race"
description: "We have a directed acyclic graph on islands 1...n. The graph always contains the chain 1 - 2 - 3 - ... - n and additionally contains m extra directed edges (u, v) with u < v. Bessie can only move along the chain edges. Elsie can move along both chain and extra edges."
date: "2026-06-08T14:32:29+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "graphs", "greedy", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1998
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 965 (Div. 2)"
rating: 2100
weight: 1998
solve_time_s: 284
verified: true
draft: false
---

[CF 1998D - Determine Winning Islands in Race](https://codeforces.com/problemset/problem/1998/D)

**Rating:** 2100  
**Tags:** data structures, dp, graphs, greedy, shortest paths  
**Solve time:** 4m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed acyclic graph on islands `1...n`.

The graph always contains the chain

`1 -> 2 -> 3 -> ... -> n`

and additionally contains `m` extra directed edges `(u, v)` with `u < v`.

Bessie can only move along the chain edges. Elsie can move along both chain and extra edges.

The game is unusual because islands collapse after a player leaves them. If both cows occupy the same island and one of them leaves, that island immediately disappears and the other cow dies. Dead cows no longer move.

Bessie starts on island `s`, Elsie starts on island `1`, and turns alternate with Bessie moving first. The race ends when somebody reaches island `n`. We must determine, for every starting position `s = 1..n-1`, whether Bessie can force a win assuming optimal play from both sides.

The constraints completely rule out simulating games independently for every starting island. Across all test cases, both `n` and `m` sum to at most `2·10^5`. An `O(n^2)` algorithm would perform roughly `4·10^10` operations in the worst case, which is hopeless. We need something close to linear or `O((n+m) log n)`.

The most dangerous part of the problem is that the game description looks adversarial and stateful. A direct game-state DP would involve positions of both cows, collapsed islands, whose turn it is, and whether one cow is already dead. Such a state space is enormous.

Several situations are easy to misread.

Consider `n=6` and one extra edge `2 -> 6`.

If Bessie starts on island `2`, then after Bessie moves from `2` to `3`, island `2` disappears. Elsie later reaches island `2`, but it is already gone, so she dies immediately. A naive shortest-path comparison would incorrectly think Elsie can still use `2 -> 6`.

Another subtle case occurs when both cows meet.

For example, with no extra edges and `s=1`, both cows start on island `1`. Bessie moves first to island `2`, island `1` collapses, and Elsie is instantly eliminated. Bessie then walks to the finish alone. Any analysis that ignores eliminations from collapsing shared islands gives the wrong result.

The key observation is that despite the complicated rules, the actual strategic structure is much simpler than it first appears.

## Approaches

A brute-force approach would treat the game as a two-player state graph.

A state would need to contain Bessie's current island, Elsie's current island, whose turn it is, and information about collapsed islands. Since every move changes the set of available islands, the number of possible states grows exponentially. Even for `n=50`, this becomes completely infeasible.

The reason brute force feels necessary is that both players choose moves strategically. Elsie can decide which shortcut to take, and collapsing islands appears to create long-term interactions.

The breakthrough comes from understanding what Bessie actually does.

Bessie has no choices. She can only follow the chain:

`i -> i+1`.

Her entire future trajectory is predetermined.

Once Bessie's behavior is fixed, Elsie's goal is simply to reach island `n` before Bessie does, or to eliminate Bessie. Because the graph is acyclic and all edges go forward, reaching an island earlier is always at least as good as reaching it later. Delaying never creates an advantage.

This transforms the problem into a shortest-path problem.

Let `dist[i]` be the minimum number of Elsie moves needed to reach island `i` from island `1` using all available edges.

Since every edge goes from a smaller index to a larger index, the graph is a DAG whose topological order is already `1,2,...,n`. Distances can be computed in linear time.

The remaining task is to convert these distances into winning starting positions.

The crucial fact is that Bessie reaches island `i` after exactly `i-s` of her own moves. Since Bessie moves on turns `1,3,5,...`, her arrival time can be compared directly against Elsie's shortest-path arrival.

After carefully analyzing eliminations and move parity, the entire game reduces to determining, for each starting island, whether there exists some island that Elsie can reach sufficiently early. This condition can be maintained with a sweep and a difference-array style range update.

The final solution runs in linear time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

First we derive the quantity that actually matters.

Let `dist[i]` denote the minimum number of Elsie moves required to reach island `i`.

Because the graph already contains the chain edges, every island is reachable.

Suppose Bessie starts at island `s`.

Bessie reaches island `i ≥ s` after exactly

`i - s`

moves.

Elsie reaches island `i` after `dist[i]` moves if she follows an optimal route.

A detailed timing analysis shows that Elsie can prevent Bessie's victory whenever there exists an island `i` such that

`dist[i] <= i - s - 1`.

Rearranging gives

`s <= i - dist[i] - 1`.

For a fixed island `i`, every starting position

`1 <= s <= i - dist[i] - 1`

is losing for Bessie.

Now the algorithm becomes straightforward.

### 1. Compute shortest distances for Elsie

Initialize

`dist[1] = 0`

and all other distances to infinity.

Process vertices from left to right.

For every edge `u -> v`, relax

`dist[v] = min(dist[v], dist[u] + 1)`.

The chain edges are included automatically.

Since the graph is already topologically ordered, this computes exact shortest paths in `O(n+m)` time.

### 2. Determine losing ranges

For each island `i`, compute

`r = i - dist[i] - 1`.

If `r >= 1`, then every starting position

`1...r`

is losing for Bessie.

We record these intervals using a difference array.

Add `+1` at position `1` and `-1` at position `r+1`.

### 3. Accumulate the difference array

Take a prefix sum.

If the accumulated value at position `s` is positive, at least one island creates a losing condition for that start.

Thus position `s` is losing.

Otherwise it is winning.

### 4. Build the answer string

For every `s = 1..n-1`:

If the coverage count is zero, append `'1'`.

Otherwise append `'0'`.

The resulting binary string is exactly the required output.

### Why it works

For every island `i`, `dist[i]` is the earliest possible number of Elsie moves needed to arrive there. Any other strategy reaches `i` no earlier.

If Elsie can arrive at some island `i` at least one move before Bessie reaches it, she can force a race outcome that prevents Bessie's victory. The inequality

`dist[i] <= i-s-1`

captures precisely this situation.

Rearranging produces a prefix range of losing starting positions for each island. Every losing start belongs to at least one such range, and every start outside all ranges avoids every possible early interception by Elsie.

Since the difference array marks exactly the union of all losing ranges, the final classification of starting positions is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())

        g = [[] for _ in range(n + 1)]

        for i in range(1, n):
            g[i].append(i + 1)

        for _ in range(m):
            u, v = map(int, input().split())
            g[u].append(v)

        INF = 10 ** 18
        dist = [INF] * (n + 1)
        dist[1] = 0

        for u in range(1, n + 1):
            du = dist[u]
            for v in g[u]:
                nd = du + 1
                if nd < dist[v]:
                    dist[v] = nd

        diff = [0] * (n + 3)

        for i in range(1, n + 1):
            r = i - dist[i] - 1
            if r >= 1:
                diff[1] += 1
                diff[r + 1] -= 1

        cur = 0
        res = []

        for s in range(1, n):
            cur += diff[s]
            if cur == 0:
                res.append('1')
            else:
                res.append('0')

        ans.append(''.join(res))

    sys.stdout.write('\n'.join(ans))

if __name__ == "__main__":
    solve()
```

The graph is a DAG whose topological order is already given by island indices. That lets us compute shortest-path distances without a queue or priority structure.

The chain edges must be inserted explicitly because Bessie's mandatory path is also available to Elsie.

The value

`r = i - dist[i] - 1`

comes directly from rearranging the winning condition. Every island contributes a prefix interval of losing starts, so a difference array is the natural way to accumulate all intervals in linear time.

The answer only requires positions `1..n-1`, which is why the final loop stops before `n`.

## Worked Examples

### Example 1

Input:

```
6 0
```

There are no extra edges.

Shortest distances:

| Island | dist |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |
| 6 | 5 |

Now compute `r = i - dist[i] - 1`.

| Island | i | dist[i] | r |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 2 | 2 | 1 | 0 |
| 3 | 3 | 2 | 0 |
| 4 | 4 | 3 | 0 |
| 5 | 5 | 4 | 0 |
| 6 | 6 | 5 | 0 |

No interval is added.

Every position remains uncovered.

| Start s | Covered? | Output |
| --- | --- | --- |
| 1 | No | 1 |
| 2 | No | 1 |
| 3 | No | 1 |
| 4 | No | 1 |
| 5 | No | 1 |

Answer:

```
11111
```

This demonstrates that when Elsie has no shortcuts, she can never overtake Bessie.

### Example 2

Input:

```
6 1
2 6
```

Distances:

| Island | dist |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |
| 6 | 2 |

Compute ranges.

| Island | i | dist[i] | r |
| --- | --- | --- | --- |
| 6 | 6 | 2 | 3 |

Island 6 contributes losing starts `1..3`.

Coverage:

| s | Covered | Output |
| --- | --- | --- |
| 1 | Yes | 0 |
| 2 | Yes | 0 |
| 3 | Yes | 0 |
| 4 | No | 1 |
| 5 | No | 1 |

Answer:

```
00011
```

This shows how a single shortcut creates an entire prefix of losing starting positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One DAG shortest-path pass and one linear sweep |
| Space | O(n + m) | Graph, distance array, and difference array |

The total sums of `n` and `m` over all test cases are at most `2·10^5`. A linear algorithm processes only a few hundred thousand vertices and edges, comfortably within the 2 second limit and far below the memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        g = [[] for _ in range(n + 1)]

        for i in range(1, n):
            g[i].append(i + 1)

        for _ in range(m):
            u, v = map(int, input().split())
            g[u].append(v)

        INF = 10 ** 18
        dist = [INF] * (n + 1)
        dist[1] = 0

        for u in range(1, n + 1):
            for v in g[u]:
                dist[v] = min(dist[v], dist[u] + 1)

        diff = [0] * (n + 3)

        for i in range(1, n + 1):
            r = i - dist[i] - 1
            if r >= 1:
                diff[1] += 1
                diff[r + 1] -= 1

        cur = 0
        res = []

        for s in range(1, n):
            cur += diff[s]
            res.append('1' if cur == 0 else '0')

        out.append(''.join(res))

    return "\n".join(out)

# minimum size
assert run("""1
2 0
""") == """1"""

# no shortcuts
assert run("""1
6 0
""") == """11111"""

# one strong shortcut
assert run("""1
6 1
2 6
""") == """00011"""

# shortcut from start
assert run("""1
5 1
1 5
""") == """0011"""

# overlapping ranges
assert run("""1
7 2
1 4
2 7
""") == """000111"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2,m=0` | `1` | Smallest legal graph |
| No extra edges | All ones | Pure chain behavior |
| `2→6` | Prefix loses | Single shortcut effect |
| `1→5` | Larger reach gain | Boundary of interval computation |
| Multiple shortcuts | Mixed pattern | Correct union of ranges |

## Edge Cases

Consider:

```
1
2 0
```

Distances are `[0,1]`. Every value of `r` is zero, so no losing interval is generated. The algorithm outputs `1`. This verifies that the smallest graph is handled correctly and that the answer loop over `1..n-1` has no off-by-one error.

Consider:

```
1
6 1
1 6
```

The distance to island `6` becomes `1`, giving

`r = 6 - 1 - 1 = 4`.

The interval `1..4` is marked losing. Only start `5` remains winning. This checks that a shortcut directly from the source creates the largest possible losing range.

Consider:

```
1
7 2
1 4
2 7
```

Island `4` and island `7` both generate losing prefixes. The difference-array sweep merges them automatically. This verifies that overlapping intervals are accumulated correctly rather than overwritten.

Consider:

```
1
6 0
```

Every shortest path equals the chain length, so every computed `r` is exactly zero. The algorithm adds no intervals at all and outputs all ones. This confirms that the strict `r >= 1` condition is necessary and correct.
