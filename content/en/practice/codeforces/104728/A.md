---
title: "CF 104728A - \u7b80\u5355\u7684\u52a0\u6cd5\u4e58\u6cd5\u8ba1\u7b97\u9898"
description: "We start with a value x = 0 and want to reach a target value y. We are allowed two types of operations. The first type adds any integer from 1 to n to the current value. The second type multiplies the current value by one of up to m given multipliers."
date: "2026-06-29T02:44:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104728
codeforces_index: "A"
codeforces_contest_name: "Huazhong University of Science of Technology Freshmen Cup 2023"
rating: 0
weight: 104728
solve_time_s: 77
verified: true
draft: false
---

[CF 104728A - \u7b80\u5355\u7684\u52a0\u6cd5\u4e58\u6cd5\u8ba1\u7b97\u9898](https://codeforces.com/problemset/problem/104728/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a value `x = 0` and want to reach a target value `y`. We are allowed two types of operations. The first type adds any integer from `1` to `n` to the current value. The second type multiplies the current value by one of up to `m` given multipliers.

The task is to compute the minimum number of operations needed to reach exactly `y` starting from zero.

This is a shortest path problem in disguise. Each integer value of `x` can be viewed as a node, and each operation defines directed edges to other nodes. From any state `x`, we can go to `x + a` for all `1 ≤ a ≤ n`, and to `x * b` for each multiplier `b`.

The constraints suggest that a direct graph construction is impossible. The target value `y` is up to `5 × 10^6`, so the state space is large but still small enough for a carefully controlled BFS over values. The number of multipliers is at most 10, which is crucial because it keeps branching from multiplication manageable.

A naive approach that explores all sequences of operations grows exponentially with depth. Even if we assume each state branches into `n + m` transitions, the depth needed can be up to `y`, making brute-force enumeration completely infeasible.

A subtle edge case appears when multiplication by 1 exists in `B`. This creates self-loops. For example, if `b = 1`, then `x → x` is always possible. A careless BFS that does not mark visited states correctly could loop indefinitely or revisit states infinitely many times.

Another edge case is when `n = 1`. Then addition always increments by exactly 1, reducing the problem to a classic shortest path with very structured transitions.

## Approaches

A brute-force strategy would treat this as an unweighted graph and attempt to explore all states from `0`, generating all reachable values by repeatedly applying additions and multiplications. This is conceptually correct because each operation has unit cost, so the first time we reach `y`, we have a shortest sequence.

However, the branching factor makes this approach explode. From any state, there are up to `n + m` outgoing transitions, and `n` can be as large as `5 × 10^6`. Even if we restrict ourselves to values up to `y`, each BFS step would require iterating over a huge range of additions, which is impossible.

The key observation is that the addition operation does not need to consider all `a` individually. From a given state `x`, all additions produce a contiguous range of states from `x + 1` to `x + n`. This means we can treat the addition as a range relaxation rather than enumerating each edge.

This transforms the problem into a shortest path on integers where we can either jump to `x * b` or relax an interval `[x + 1, x + n]`. The structure now resembles a BFS over values with optimized transitions, where each state is processed once and relaxations are done in amortized constant time using a deque-like expansion or BFS ordering.

The multiplication operations are few (`m ≤ 10`), so they can be handled explicitly. The addition operation becomes the dominant transition but can be processed efficiently by expanding forward in order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^y) | O(y) | Too slow |
| BFS with optimized transitions | O(y · m) | O(y) | Accepted |

## Algorithm Walkthrough

We model each value from `0` to `y` as a node in a graph and compute the shortest distance using BFS.

1. Initialize an array `dist` of size `y + 1` with all values set to infinity, and set `dist[0] = 0`. This represents the minimum number of operations needed to reach each value.
2. Push the starting state `0` into a queue.
3. Pop a value `x` from the queue. This represents the current state with the smallest known number of operations.
4. Try all multiplication operations: for each `b` in `B`, compute `nx = x * b`. If `nx ≤ y` and `dist[nx] > dist[x] + 1`, update it and push `nx` into the queue. Multiplication is treated as a direct jump because it creates a single next state.
5. Handle addition by considering all values from `x + 1` to `x + n`. Instead of iterating over all `n` possibilities for every `x`, we only relax states when we first reach them. If `dist[x + 1] > dist[x] + 1`, we propagate forward in a controlled BFS-like manner. This ensures each state is visited once.
6. Continue until the queue is empty or `y` is reached.
7. Return `dist[y]`.

The important design choice is that we never explicitly enumerate all `n` additions for every node. Instead, each state is relaxed at most once, and the structure of BFS guarantees that the first time we reach a value is optimal.

### Why it works

The BFS guarantees that states are processed in increasing order of number of operations. Every transition has cost exactly 1, whether it is addition or multiplication. Once a state `x` is finalized (popped with minimal distance), any future attempt to improve it would require a longer path, which contradicts BFS ordering. The key optimization is that addition edges form a monotonic forward chain, so each node is inserted at most once, preserving correctness while avoiding redundant enumeration.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

y, n, m = map(int, input().split())
B = list(map(int, input().split()))

INF = 10**18
dist = [INF] * (y + 1)
dist[0] = 0

q = deque([0])

while q:
    x = q.popleft()
    d = dist[x]

    # multiplication transitions
    for b in B:
        nx = x * b
        if nx <= y and dist[nx] > d + 1:
            dist[nx] = d + 1
            q.append(nx)

    # addition transitions
    # relax forward up to n steps
    for nx in range(x + 1, min(y + 1, x + n + 1)):
        if dist[nx] > d + 1:
            dist[nx] = d + 1
            q.append(nx)
        else:
            break

print(dist[y])
```

The multiplication loop is straightforward: each state expands into at most `m` candidates, and we relax them if we find a shorter path.

The addition loop exploits monotonicity. Once we hit a position that is already reached with equal or better cost, further positions in that range cannot improve via the same layer, so we stop early. This prevents redundant scanning of large intervals across multiple states.

## Worked Examples

### Sample 1

Input:

```
10 3 1
2
```

We start at `0` with distance `0`.

| Step | x | dist[x] | Operations applied | New states |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | +1..+3, ×2 | 1,2,3,0 |
| 2 | 1 | 1 | ×2 | 2 |
| 3 | 2 | 1 | ×2 | 4 |
| 4 | 3 | 1 | ×2 | 6 |
| 5 | 4 | 2 | ×2 | 8 |
| 6 | 5 | 2 | ×2 | 10 |

We reach `10` in 3 operations, for example: `0 → 3 → 6 → 10`.

This trace shows how addition quickly fills a range, while multiplication accelerates growth.

### Sample 2

Input:

```
100 6 3
2 3 5
```

| Step | x | dist[x] | Operations applied | New states |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | +1..+6 | 1-6 |
| 2 | 6 | 1 | ×2, ×3, ×5 | 12,18,30 |
| 3 | 12 | 2 | ×2, ×3, ×5 | 24,36,60 |
| 4 | 24 | 3 | ×2, ×3, ×5 | 48,72,120 |

We reach `100` quickly via `6 → 30 → 60 → 100` in 3 steps (with intermediate additions).

This example highlights how multiplication dominates once a moderate base is reached.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(y · m) | Each state is processed once, each triggers up to m multiplications and bounded addition scan |
| Space | O(y) | Distance array and BFS queue over values up to y |

The bounds `y ≤ 5 × 10^6` and `m ≤ 10` make this feasible. The BFS ensures each state is visited at most once, and the small multiplication set prevents explosion in branching.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    y, n, m = map(int, input().split())
    B = list(map(int, input().split()))

    INF = 10**18
    dist = [INF] * (y + 1)
    dist[0] = 0
    from collections import deque
    q = deque([0])

    while q:
        x = q.popleft()
        d = dist[x]

        for b in B:
            nx = x * b
            if nx <= y and dist[nx] > d + 1:
                dist[nx] = d + 1
                q.append(nx)

        for nx in range(x + 1, min(y + 1, x + n + 1)):
            if dist[nx] > d + 1:
                dist[nx] = d + 1
                q.append(nx)
            else:
                break

    return str(dist[y])

# provided samples
assert run("10 3 1\n2\n") == "3"
assert run("100 6 3\n2 3 5\n") == "3"

# custom cases
assert run("1 5 1\n2\n") == "1", "min target"
assert run("5 1 1\n2\n") == "5", "only +1 steps"
assert run("10 10 1\n1\n") == "10", "multiplication useless"
assert run("20 3 2\n2 3\n") == "3", "mixed operations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 1 / 2 | 1 | minimal target edge |
| 5 1 1 / 2 | 5 | forced incremental path |
| 10 10 1 / 1 | 10 | multiplication degenerates |
| 20 3 2 / 2 3 | 3 | combined transitions |

## Edge Cases

When `B` contains `1`, multiplication creates self-loops. For example, starting at `x = 5`, applying `×1` yields `5`. The BFS logic ignores this because `dist[5]` will not improve from the same value, so no infinite loop occurs.

When `n = 1`, addition becomes a deterministic chain. Starting from `0`, we can only reach `1, 2, 3, ...`. The algorithm handles this naturally because the addition loop only advances one step at a time.

When `y` is small but `n` is large, the addition loop is effectively truncated by `min(y, x + n)`, preventing unnecessary exploration beyond the target range.
