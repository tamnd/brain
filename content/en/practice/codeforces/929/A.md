---
title: "CF 929A - \u041f\u0440\u043e\u043a\u0430\u0442 \u0432\u0435\u043b\u043e\u0441\u0438\u043f\u0435\u0434\u043e\u0432"
description: "We are given a sequence of positions along a straight line where bike stations are located. The first station coincides with Arkady’s starting point (school), and the last station coincides with his destination (home)."
date: "2026-06-17T03:05:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 929
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2018 - \u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f 2"
rating: 1400
weight: 929
solve_time_s: 70
verified: true
draft: false
---

[CF 929A - \u041f\u0440\u043e\u043a\u0430\u0442 \u0432\u0435\u043b\u043e\u0441\u0438\u043f\u0435\u0434\u043e\u0432](https://codeforces.com/problemset/problem/929/A)

**Rating:** 1400  
**Tags:** *special, greedy, implementation  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of positions along a straight line where bike stations are located. The first station coincides with Arkady’s starting point (school), and the last station coincides with his destination (home). Between them are intermediate stations that he may use as mandatory stopping points.

Arkady travels only by bike, but each time he rents a bike, he can ride it for at most a fixed distance `k`. When he reaches a station, he must return the current bike, optionally take a new one, and continue. He is allowed to switch bikes only at these stations. The goal is to determine whether he can reach the final station, and if so, the minimum number of bikes he must rent, counting the first one.

The key observation is that movement is constrained to jumps between stations, and each ride must cover a segment whose length does not exceed `k`.

The constraints `n ≤ 1000` and coordinates up to `100000` mean that an O(n²) solution is already acceptable. However, the structure is even simpler, so a linear greedy scan is sufficient. We are effectively selecting a minimal number of segments covering the path from left to right.

A naive failure case appears when someone tries to always take the farthest reachable station without carefully updating from the correct current position. For example, if stations are `0, 3, 6` and `k = 4`, greedy must go 0 → 3 → 6. A buggy approach that incorrectly recomputes reachability from the wrong origin might skip valid transitions.

Another subtle case is when the distance between consecutive stations exceeds `k`. For example, `0, 5, 6` with `k = 4` makes travel impossible even though a later segment is small enough. Any correct solution must detect this immediately.

## Approaches

A brute-force interpretation is to treat each station as a node and try all possible sequences of valid moves. From station `i`, we can move to any station `j > i` such that `x[j] - x[i] ≤ k`. We then recursively try to minimize the number of rentals needed to reach the last station.

This works because the problem is a shortest path in a directed acyclic graph, but exploring all paths leads to exponential branching in the worst case. With `n = 1000`, this becomes completely infeasible.

The key structural insight is that the graph is ordered and edges only go forward. This means that once we decide to take a bike from station `i`, the best possible next station is the farthest reachable one, because any earlier choice only reduces future reach. This turns the problem into a greedy walk: repeatedly jump as far right as possible within distance `k`.

We only need to maintain a pointer to the farthest reachable station from the current position and move there, counting how many segments we use.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the stations in order from left to right.

1. Start at station 0 (index 0) with a current position pointer.
2. From the current station, scan forward to find the furthest station whose distance from the current station is at most `k`.
3. If no such station exists, the trip is impossible and we stop immediately.
4. Move to that furthest reachable station and increment the bike count by 1.
5. Repeat until we reach the final station.

The reason we always choose the furthest reachable station is that any closer choice strictly reduces or keeps the same remaining reachable set from the next position, never expanding it. Since all future decisions depend only on the current position, maximizing immediate progress is optimal.

### Why it works

At any station `i`, define the set of reachable stations as all `j > i` such that `x[j] - x[i] ≤ k`. Any valid solution must choose its next station from this set. If we pick the furthest `j`, then every station reachable from any smaller choice is also reachable from `j`, because `x[j]` is maximal. This preserves reachability and minimizes the number of transitions, which directly corresponds to minimizing bike rentals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    x = list(map(int, input().split()))
    
    i = 0
    ans = 0
    
    while i < n - 1:
        j = i
        while j + 1 < n and x[j + 1] - x[i] <= k:
            j += 1
        
        if j == i:
            print(-1)
            return
        
        ans += 1
        i = j
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps a pointer `i` for the current station. The inner loop advances `j` as far as possible while staying within distance `k` from `x[i]`. If `j` does not move, it means even the next station is unreachable, so the answer is `-1`.

Each successful move increments the number of bike rentals and jumps directly to the farthest reachable station, ensuring minimal transitions.

## Worked Examples

### Example 1

Input:

```
4 4
3 6 8 10
```

We start at index 0 (position 3).

| Current i | Current position | Furthest reachable j | Action | Rentals |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1 (6) | jump to 1 | 1 |
| 1 | 6 | 3 (10) | jump to 3 | 2 |

We reach the last station in 2 rentals, which matches the output.

This demonstrates that intermediate station 2 (8) is skipped because jumping directly from 6 to 10 is still within `k`.

### Example 2

Input:

```
2 9
0 10
```

| Current i | Current position | Furthest reachable j | Action | Rentals |
| --- | --- | --- | --- | --- |
| 0 | 0 | none | impossible | - |

From 0, the next station is 10, but the distance exceeds `k = 9`, so no move is possible. The algorithm correctly outputs `-1`.

This shows that failure occurs immediately when even the first segment is invalid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each station is visited at most once as the current pointer and once in scanning |
| Space | O(1) | Only a few pointers are used |

The linear scan fits easily within limits since `n ≤ 1000`, and even larger constraints would remain efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, k = map(int, input().split())
    x = list(map(int, input().split()))
    
    i = 0
    ans = 0
    
    while i < n - 1:
        j = i
        while j + 1 < n and x[j + 1] - x[i] <= k:
            j += 1
        if j == i:
            return "-1"
        ans += 1
        i = j
    
    return str(ans)

# provided sample
assert run("4 4\n3 6 8 10\n") == "2"

# minimum size impossible
assert run("2 1\n0 5\n") == "-1"

# minimum size possible
assert run("2 10\n0 5\n") == "1"

# all stations reachable in one go
assert run("5 100\n0 10 20 30 40\n") == "1"

# chain requiring many jumps
assert run("5 5\n0 3 6 9 12\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 / 0 5 | -1 | immediate impossibility |
| 2 10 / 0 5 | 1 | single jump suffices |
| wide spaced chain | 1 | full reachability in one ride |
| uniform gaps | 4 | worst-case linear progression |

## Edge Cases

When two consecutive stations are farther apart than `k`, the inner loop fails immediately because `j` cannot move beyond `i`. For input `2 3` with positions `0 10`, the algorithm starts at `i = 0`, sees no valid `j`, and returns `-1` directly. This matches the requirement that Arkady never walks.

When all stations are within one segment of length `k`, such as `0 2 4 6` with `k = 10`, the inner loop always reaches the last station in one step. The algorithm increments `ans` once and finishes, correctly minimizing rentals.

When greedy choices appear ambiguous, such as `0 3 5 7 10` with `k = 5`, the algorithm always pushes to the furthest reachable station, producing `0 → 5 → 10`, which avoids unnecessary intermediate rentals and confirms that local maximal jumps preserve global optimality.
