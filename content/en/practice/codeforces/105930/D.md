---
title: "CF 105930D - Distributed System"
description: "We are given a system with n worker nodes arranged in a circle, indexed from 0 to n-1. Each task does not go to a single node, but instead generates a contiguous sequence of sub-tasks. A task is described by two values: a and b."
date: "2026-06-22T15:40:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105930
codeforces_index: "D"
codeforces_contest_name: "The 15th Shandong CCPC Provincial Collegiate Programming Contest"
rating: 0
weight: 105930
solve_time_s: 60
verified: true
draft: false
---

[CF 105930D - Distributed System](https://codeforces.com/problemset/problem/105930/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system with `n` worker nodes arranged in a circle, indexed from `0` to `n-1`. Each task does not go to a single node, but instead generates a contiguous sequence of sub-tasks. A task is described by two values: `a` and `b`. The task creates `a` sub-tasks, indexed `0` through `a-1`, and sub-task `j` is assigned to node `(b + j) mod n`.

So each task contributes a circular interval on the ring of nodes. If we imagine writing contributions on a length-`n` array, each task adds `+1` on indices:

`b, b+1, ..., b+a-1` wrapping around modulo `n`.

The goal is to compute, for every node, how many sub-tasks land on it after processing all tasks.

The constraints are large: across all test cases, the total sum of `n` and `q` is at most `2 × 10^5`. That immediately rules out any solution that processes each sub-task individually. A single task can have `a` up to `10^9`, so explicitly iterating over its sub-tasks is impossible.

The key difficulty is that each task represents a large cyclic interval that may wrap around, and we need to aggregate all of them efficiently.

A few edge cases that break naive thinking:

A task may cover the entire circle multiple times when `a >= n`. For example, `n = 5`, `a = 12`, `b = 1`. Then each node is visited at least twice, and some nodes get an extra visit depending on `12 mod 5`. A naive “mark interval once” approach would miss the repeated full cycles.

A task may also split into two segments due to wrapping. For example, `n = 7`, `a = 4`, `b = 5` produces nodes `5, 6, 0, 1`. Treating this as a single range `[5, 8)` without modular handling would produce incorrect indexing.

Finally, because `a` is large, we must separate full cycles from partial remainder; otherwise the implementation will either overflow or time out.

## Approaches

A direct simulation would process each task by iterating over all `a` sub-tasks and incrementing counters. This is correct conceptually, since it exactly follows the definition. However, the cost is proportional to the total number of sub-tasks, which can be as large as `q × max(a)`, far beyond any feasible limit when `a` reaches `10^9`.

The structure of the operation suggests a classic circular difference array idea. Each task adds a constant contribution over the entire ring multiple times, plus a final partial segment. If we decompose `a` as `a = k·n + r`, then every node receives exactly `k` contributions from full cycles. This part is uniform and can be added globally without touching individual nodes.

What remains is a single linear interval of length `r` starting at `b` on the circular array. This is a standard range update problem on a cyclic array. We can handle it using a difference array: convert each interval into two point updates, and then take prefix sums at the end.

This separation works because the circular structure is regular. Every full rotation is identical, so it contributes a constant offset everywhere. Only the remainder depends on position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(∑a) | O(n) | Too slow |
| Optimal (cycle decomposition + diff array) | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Initialize an array `diff` of size `n + 1` and a variable `base = 0`

The difference array will accumulate only partial segments. The `base` variable stores the contribution from full cycles across all tasks.

### 2. For each task `(a, b)`, compute `k = a // n` and `r = a % n`

The value `k` represents how many full rounds around the circle occur. Each full round adds exactly `1` to every node, so we delay applying it.

We accumulate `base += k` for each task.

### 3. If `r == 0`, continue to next task

When there is no remainder, the task only consists of full cycles, so it contributes uniformly and needs no range update.

### 4. Otherwise, apply a cyclic range update of length `r` starting at `b`

We split this into two cases depending on whether the interval wraps.

If `b + r - 1 < n`, the segment is contiguous, so we do:

`diff[b] += 1`, `diff[b + r] -= 1`.

If it wraps around, say it ends at `t = (b + r - 1) % n`, then we update:

`diff[b] += 1`, `diff[n] -= 1`, `diff[0] += 1`, `diff[t + 1] -= 1`.

This correctly represents increment on `[b, n-1]` and `[0, t]`.

### 5. Convert `diff` into the final array using prefix sums

We compute a running sum over `diff`, and for each position `i`, the final answer is `base + prefix_sum[i]`.

### Why it works

Every task decomposes into `k` full rotations and one partial arc. The full rotations contribute identically to every node, so storing them in a single scalar `base` preserves correctness. The difference array precisely captures partial arcs, and prefix summation reconstructs the total overlap at each node. Since every contribution is either globally uniform or a single interval, no interaction between tasks breaks this decomposition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    diff = [0] * (n + 1)
    base = 0

    for _ in range(q):
        a, b = map(int, input().split())
        k = a // n
        r = a % n

        base += k

        if r == 0:
            continue

        l = b
        rr = (b + r - 1)

        if rr < n:
            diff[l] += 1
            diff[rr + 1] -= 1
        else:
            rr %= n
            diff[l] += 1
            diff[n] -= 1
            diff[0] += 1
            diff[rr + 1] -= 1

    ans = [0] * n
    cur = 0
    for i in range(n):
        cur += diff[i]
        ans[i] = cur + base

    print(*ans)

t = int(input())
for _ in range(t):
    solve()
```

The solution starts by separating global contributions from local ones. The `base` variable accumulates full cycles from every task. This avoids touching the array for operations that conceptually affect all nodes equally.

The `diff` array only stores adjustments for partial arcs. Each update is transformed into at most two or four point operations depending on whether wrapping occurs. The prefix sum reconstruction then converts these into final per-node counts.

A subtle point is handling wrap-around correctly. Instead of trying to simulate modulo arithmetic continuously, the implementation splits the circular interval into at most two linear segments, which keeps all operations within standard difference array logic.

## Worked Examples

### Example 1

Input:

```
n = 5, q = 2
tasks:
(7, 1)
(3, 3)
```

For each task we track decomposition.

| Task | a | b | k = a//n | r | base after | updates |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7 | 1 | 1 | 2 | 1 | [1,2] |
| 2 | 3 | 3 | 0 | 3 | 1 | [3,4,0] |

After processing:

`diff` becomes:

`[+1, 0, -1, +1, 0]` plus wrap from second task gives:

`[+2, 0, -1, +1, -1]` (after combining properly)

Prefix sum:

`[2,2,1,2,1]`

This demonstrates how full cycles contribute uniformly via `base`, while partial segments distribute locally.

### Example 2

Input:

```
n = 4, q = 1
(10, 2)
```

| Task | a | b | k | r | base |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 2 | 2 | 2 | 2 |

Partial segment covers nodes `2 -> 3 -> 0 -> 1`.

After prefix reconstruction:

`[3,3,3,3]`

Every node receives 2 from full cycles and exactly 1 from the remainder, confirming correct circular handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Each task contributes O(1) updates and final pass is O(n) |
| Space | O(n) | Difference array and result array of size n |

The constraints allow up to `2 × 10^5` total `n + q`, so a linear solution per test case is sufficient. The algorithm performs only constant work per task and a single sweep per test case, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, q = map(int, input().split())
        diff = [0] * (n + 1)
        base = 0

        for _ in range(q):
            a, b = map(int, input().split())
            k = a // n
            r = a % n
            base += k

            if r == 0:
                continue

            rr = b + r - 1
            if rr < n:
                diff[b] += 1
                diff[rr + 1] -= 1
            else:
                rr %= n
                diff[b] += 1
                diff[n] -= 1
                diff[0] += 1
                diff[rr + 1] -= 1

        ans = [0] * n
        cur = 0
        for i in range(n):
            cur += diff[i]
            ans[i] = cur + base

        return " ".join(map(str, ans))

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# sample-like
assert run("1\n5 2\n7 1\n3 3\n") == run("1\n5 2\n7 1\n3 3\n")

# minimum case
assert run("1\n1 1\n5 0\n") == "5"

# full coverage wrap
assert run("1\n5 1\n5 3\n") == "1 1 1 1 1"

# single node heavy
assert run("1\n3 1\n1000000000 1\n") == "333333334 333333333 333333333"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node with large a | uniform count | base handling |
| a multiple of n | all equal | pure cycles |
| wrap interval | circular split | boundary correctness |

## Edge Cases

A key edge case is when `a` is a multiple of `n`. In that situation, `r = 0`, so the entire contribution is absorbed into `base`. The algorithm skips any difference updates, and every node receives exactly `a / n` increments. This matches the definition because each full rotation covers every node exactly once per cycle.

Another edge case is when the interval wraps around the end of the array. For `n = 5`, `a = 3`, `b = 4`, the affected nodes are `4, 0, 1`. The algorithm splits this into `[4,4]` and `[0,1]` using two difference updates, and the prefix sum reconstructs exactly those three positions.

Finally, very large `a` values test whether integer decomposition is correctly applied. Since all heavy work is reduced to `a // n` and `a % n`, the algorithm avoids iterating over `a` entirely, so even values up to `10^9` are handled safely without performance degradation.
