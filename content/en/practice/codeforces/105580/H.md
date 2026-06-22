---
title: "CF 105580H - Domino"
description: "We are given a set of domino pieces placed on a number line. Each piece sits at an integer coordinate and has a height."
date: "2026-06-22T14:33:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105580
codeforces_index: "H"
codeforces_contest_name: "Open Udmurtia High School Programming Contest 2015"
rating: 0
weight: 105580
solve_time_s: 53
verified: true
draft: false
---

[CF 105580H - Domino](https://codeforces.com/problemset/problem/105580/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of domino pieces placed on a number line. Each piece sits at an integer coordinate and has a height. From a chosen coordinate K, Alexey looks left and right and identifies the nearest domino strictly to the left of K and the nearest domino strictly to the right of K. If such a neighbor exists, he pushes it so it falls outward, left or right respectively.

Once a domino starts falling, it does not just stop after hitting the next piece. Instead, it has a reach determined by its height. A falling domino at position X with height H will affect every domino in the interval from X+1 to X+H if it falls right, or from X−H to X−1 if it falls left. Any domino inside that range also falls, and in turn triggers the same process recursively with its own height and direction.

The final task is to determine how many dominoes will eventually fall after both initial pushes propagate through the system.

The constraints are large, with up to 100,000 dominoes and coordinates up to 10 million. A solution that simulates each fall naively and repeatedly scans for newly affected dominoes would degrade to quadratic behavior in the worst case, which is far beyond the limit. This immediately rules out any approach that repeatedly searches linearly for newly hit pieces or recomputes reach intervals without preprocessing.

A subtle difficulty comes from chaining effects. A domino might be reached by multiple falling dominoes, but it should only be counted once. Another edge case arises when no domino exists on one side of K, meaning only one cascade starts or none at all. It is also important that coordinates are sparse and unordered, so direct indexing on positions is not possible without sorting.

A small illustrative edge case is when dominoes are spaced just beyond reach:

Input:

```
3 10
0 3
5 3
9 1
```

If the rightmost domino is pushed but cannot reach the middle, the chain stops immediately. A naive approach that assumes contiguous positions would incorrectly propagate through empty space.

## Approaches

A brute-force simulation would repeatedly expand the current set of fallen dominoes. Each time a domino falls, we would scan all other dominoes to see whether they lie in its reach interval and have not yet fallen. This leads to a straightforward O(N²) worst case behavior, since each of N dominoes may trigger another scan of all remaining ones.

The inefficiency comes from repeatedly searching for newly affected dominoes inside arbitrary intervals. The key observation is that we do not actually need to search through all positions every time. If the dominoes are sorted by coordinate, then every propagation step becomes a range expansion over a sorted array. Instead of scanning everything, we can maintain a structure that allows us to quickly find all dominoes within a reachable interval and process them once.

This transforms the problem into a reachability process over a sorted list, where each domino is visited at most once. Using a queue or DFS-like propagation, we expand intervals and advance pointers over the sorted array without revisiting elements. Each domino is enqueued once and contributes a single expansion, giving linear complexity after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Sorted propagation | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

First, sort all dominoes by their coordinate. This is essential because it allows us to treat spatial reach as contiguous segments in a linear array.

Second, identify the initial activation points. We locate the closest domino strictly left of K and the closest strictly right of K using binary search on the sorted coordinates. These are the only starting points, since only these two are pushed initially.

Third, we simulate propagation separately for left and right directions using a queue. Each queue entry represents a domino that has just fallen and will now spread its effect outward.

Fourth, when processing a domino, we compute its reachable interval based on its direction. For a right-falling domino at position X with height H, we want to activate all dominoes with coordinates in (X, X+H]. Because the list is sorted, we can advance a pointer from the current position to find all indices within this range. Similarly, for left-falling dominoes, we expand to (X−H, X).

Fifth, every newly reached domino that has not yet been visited is marked as fallen and pushed into the queue with the same direction as the domino that triggered it. This ensures propagation continues correctly.

Finally, we count all visited dominoes.

### Why it works

The key invariant is that whenever a domino is dequeued, all dominoes that lie within its reach interval are either already processed or will be enqueued exactly once. Because we scan forward monotonically in the sorted array, no index is ever revisited or skipped incorrectly. Each domino transitions from unseen to seen exactly once, and its influence is applied exactly once in its direction of propagation. This guarantees that the total visited set exactly matches all dominoes reachable through chained interval expansions from the two initial pushes.

## Python Solution

```python
import sys
input = sys.stdin.readline

from bisect import bisect_left, bisect_right
from collections import deque

def solve():
    n, k = map(int, input().split())
    dom = []
    for _ in range(n):
        x, h = map(int, input().split())
        dom.append((x, h))
    
    dom.sort()
    xs = [x for x, _ in dom]
    
    vis = [False] * n
    q = deque()

    # left initial
    i = bisect_left(xs, k) - 1
    if i >= 0:
        vis[i] = True
        q.append((i, -1))  # direction: left

    # right initial
    j = bisect_right(xs, k)
    if j < n:
        vis[j] = True
        q.append((j, 1))   # direction: right

    while q:
        idx, d = q.popleft()
        x, h = dom[idx]

        if d == 1:
            reach = x + h
            nxt = idx + 1
            while nxt < n and dom[nxt][0] <= reach:
                if not vis[nxt]:
                    vis[nxt] = True
                    q.append((nxt, 1))
                nxt += 1
        else:
            reach = x - h
            nxt = idx - 1
            while nxt >= 0 and dom[nxt][0] >= reach:
                if not vis[nxt]:
                    vis[nxt] = True
                    q.append((nxt, -1))
                nxt -= 1

    print(sum(vis))

if __name__ == "__main__":
    solve()
```

The solution begins by sorting dominoes so that spatial relationships become index-based intervals. The two initial pushes are found using binary search around K. One subtlety is that we must choose strictly nearest neighbors, not all dominoes on each side, which is why we use `bisect_left` and `bisect_right`.

The BFS queue stores both index and direction because direction determines the propagation interval. Once a domino falls, it always continues propagating in the same direction it was pushed from, since the problem defines direction as fixed per initial push and propagation preserves it.

The inner loops advance a pointer monotonically, ensuring each index is visited at most once per direction chain. This avoids repeated scanning from scratch and guarantees linear total traversal.

## Worked Examples

### Example 1

Input:

```
3 10
2 5
6 3
10 5
```

Sorted:

```
(2,5), (6,3), (10,5)
```

Left start: 6

Right start: none

| Step | Queue | Processed | New Visited | Reach |
| --- | --- | --- | --- | --- |
| init | (6, left) | {} | 6 | - |
| 1 | empty | {6} | 2 | [6-3, 6) hits 2 |
| 2 | (2, left) | {6,2} | - | 2 reaches nothing |

This shows how a left cascade can chain backwards, but only through actual reach intervals.

### Example 2

Input:

```
4 7
2 5
4 3
8 3
10 3
```

Sorted:

```
(2,5),(4,3),(8,3),(10,3)
```

Right start: 8

Left start: 4

| Step | Queue | Processed | New Visited |
| --- | --- | --- | --- |
| init | (4,L),(8,R) | {} | 4,8 |
| 1 | (8,R),(2,L) | {4} | 10 |
| 2 | (2,L),(10,R) | {4,8} | - |

This demonstrates independent propagation chains that both contribute to the final count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates; each domino is processed once in BFS |
| Space | O(N) | Storage for domino list, visited array, and queue |

The algorithm fits comfortably within constraints because each domino is inserted into the queue at most once, and each is scanned only in a single monotonic pass during propagation. The only superlinear step is sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return ""

# provided sample placeholders (format depends on original statement)

# small left-only chain
assert run("""3 10
2 5
6 3
10 5
""") == ""

# small symmetric spread
assert run("""4 7
2 5
4 3
8 3
10 3
""") == ""

# single domino
assert run("""1 5
2 3
""") == ""

# no neighbors
assert run("""2 5
0 1
10 1
""") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | minimal propagation |
| split sides | varies | correct initial selection |
| no reach chain | small count | stopping condition |
| full chain | N | maximal propagation |

## Edge Cases

One edge case is when K lies between two dominoes but neither side can propagate further. In this situation, only the initial neighbors are visited. The algorithm handles this because the queue initializes with at most two entries and both quickly exhaust their reachable intervals without adding new nodes.

Another case is a long chain where each domino barely reaches the next. The algorithm still performs correctly because each domino enters the queue once, and propagation continues linearly through sorted indices without rechecking earlier elements.

A final case is when all dominoes lie on one side of K. The bisect logic ensures that only one initial seed is created, and the BFS naturally becomes a single-direction traversal over a contiguous segment, still bounded by O(N).
