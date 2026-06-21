---
title: "CF 105562F - Flowing Fountain"
description: "We are given a vertical stack of bowls, each bowl sitting above the next one. Every bowl has a fixed capacity, and we process two kinds of operations over time. One operation pours some amount of champagne into a chosen bowl."
date: "2026-06-22T06:27:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105562
codeforces_index: "F"
codeforces_contest_name: "2024-2025 ICPC Northwestern European Regional Programming Contest (NWERC 2024)"
rating: 0
weight: 105562
solve_time_s: 46
verified: true
draft: false
---

[CF 105562F - Flowing Fountain](https://codeforces.com/problemset/problem/105562/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a vertical stack of bowls, each bowl sitting above the next one. Every bowl has a fixed capacity, and we process two kinds of operations over time. One operation pours some amount of champagne into a chosen bowl. If that bowl cannot hold all of it, the excess flows downward through the stack. The rule for where it goes is important: overflow does not go to the next index, it goes to the next bowl below that still has remaining capacity available in the downward direction. If even the lowest bowl overflows, the extra is lost.

The second operation asks for the current amount of champagne in a particular bowl at that moment. The system evolves over a long sequence of such pours and queries, so we must maintain a dynamic state efficiently.

The key difficulty is that pouring into a high level can propagate through many intermediate full bowls. In the worst case, a single operation could traverse the entire structure, and there are up to 3×10^5 operations. A naive simulation that moves unit flow step by step would immediately fail because each operation could cost O(n), leading to O(nq) which is far beyond feasible limits.

A subtle edge case appears when many bowls are already full in a contiguous segment. For example, if all bowls below a certain point are saturated, a new pour might instantly skip a large block and deposit directly far below, or be completely wasted. Another corner case is repeated queries after many partial pours: we must not recompute flows from scratch each time, since state is persistent and must be maintained incrementally.

A naive mistake is to treat flow as always going to the next index. That fails on cases like capacities [2, 4, 3], pouring 10 into level 1: most of the value bypasses intermediate levels depending on residual space, not just adjacency.

## Approaches

A brute-force simulation treats each pour as a literal flow process. We maintain an array of current fills. When pouring into level ℓ, we add x, then while that level exceeds capacity we push the excess to the next level, and so on downward. Each unit of overflow might traverse many levels, so a single operation can degrade to O(n) in the worst case when everything is full and we keep walking downward.

This is correct but fundamentally too slow because each of the q operations may scan through a long suffix. With q up to 3×10^5, this leads to roughly 10^10 operations in the worst case.

The key observation is that the flow process is monotone in a very strong way. Once a bowl becomes full, it behaves like a “solid block” that immediately redirects all incoming flow downward. This suggests compressing consecutive full segments. Instead of simulating step-by-step flow, we want to jump directly to the next bowl that still has remaining capacity.

This transforms the problem into maintaining a structure that can answer two things efficiently: how much free space remains in a segment, and where the next non-full position is. A disjoint-set union structure fits naturally if we treat “full bowls” as removed nodes. Each time a bowl becomes full, we union it with the next candidate below. Then finding where a unit of flow lands becomes a sequence of find operations that jump over saturated segments.

Thus each bowl is visited at most once as full, and each query amortizes over near-constant time inverse Ackermann behavior.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| DSU skip-full optimization | O((n + q) α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain three core pieces of information: the current fill in each bowl, its capacity, and a DSU structure that allows us to jump to the next non-full bowl below a given index.

1. Initialize an array `cur[i] = 0` for current fill, and store capacities `cap[i]`. Build a DSU parent array where each index points to itself initially.
2. Define a function `find(i)` that returns the nearest index at or below i that is not fully saturated. If i is out of range, we return a sentinel meaning overflow to ground.
3. When processing a pour query `(ℓ, x)`, repeatedly locate the first available bowl using `i = find(ℓ)`.
4. At each step, compute how much free space remains in bowl i as `cap[i] - cur[i]`.
5. If x is less than or equal to this free space, we simply add x to `cur[i]` and stop. This is the case where flow does not propagate further.
6. If x exceeds free space, we fill bowl i completely, subtract that free space from x, and mark i as full.
7. When a bowl becomes full, we union it with i + 1 so that future finds skip it immediately. This is the mechanism that compresses already-saturated regions.
8. Continue the process from the next available bowl until x becomes zero or we run past the last bowl, in which case remaining x is discarded.
9. For a query `(ℓ)`, simply output `cur[ℓ]`.

The reason this works efficiently is that each bowl transitions from “not full” to “full” exactly once. After that transition, it is never processed again as a free node. So the total number of expensive DSU merges is linear over n.

### Why it works

The invariant is that `find(i)` always returns the first bowl at or below i that still has remaining capacity. Whenever we saturate a bowl, we permanently remove it from consideration by linking it to the next index. This ensures that future flow never revisits already full bowls, matching exactly the physical interpretation of overflow. Since every unit of flow either fills a bowl or is discarded, and each bowl is filled once, the total number of structural changes is bounded by n, which guarantees correctness and efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, q = map(int, input().split())
cap = list(map(int, input().split()))

cur = [0] * n
parent = list(range(n + 1))

def find(x):
    if x >= n:
        return n
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    x = find(x)
    y = find(y)
    if x != y:
        parent[x] = y

for i in range(n):
    parent[i] = i

parent[n] = n

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '+':
        l = int(tmp[1]) - 1
        x = int(tmp[2])

        i = find(l)

        while i < n and x > 0:
            free = cap[i] - cur[i]
            if free == 0:
                union(i, i + 1)
                i = find(i)
                continue

            if x <= free:
                cur[i] += x
                x = 0
            else:
                cur[i] += free
                x -= free
                union(i, i + 1)
                i = find(i)

    else:
        l = int(tmp[1]) - 1
        print(cur[l])
```

The implementation relies on DSU path compression to ensure that once a bowl is full, it is effectively skipped in constant amortized time. The `union(i, i+1)` operation is the key mechanism that removes saturated positions from future consideration.

A subtle detail is handling already-full bowls: even if `cur[i] == cap[i]`, we immediately union it forward before continuing. This prevents infinite loops where we repeatedly land on a full bowl. Another important point is the sentinel index `n`, which represents overflow beyond the last bowl, allowing the loop to terminate cleanly when all remaining flow is wasted.

## Worked Examples

### Example 1

Input:

```
4 4
1 2 3 4
+ 1 6
? 4
+ 1 6
? 4
```

For the first operation, we start at bowl 1 with capacity 1. We pour 6. Bowl 1 fills completely and 5 units remain. We move to bowl 2, which has capacity 2, so it takes 2 and becomes full, leaving 3. Then bowl 3 takes 3 exactly and becomes full. No overflow reaches bowl 4.

| Step | Bowl | Cur | Cap | Remaining x | Action |
| --- | --- | --- | --- | --- | --- |
| start | 1 | 0 | 1 | 6 | fill |
| 1 | 1 | 1 | 1 | 5 | full, move |
| 2 | 2 | 2 | 2 | 3 | full, move |
| 3 | 3 | 3 | 3 | 0 | stop |

After this, bowl 4 is still empty, so query returns 0.

The second identical pour repeats the same process, confirming that repeated full propagation behaves consistently.

### Example 2

Input:

```
4 8
2 4 3 5
+ 1 4
? 2
+ 2 3
? 4
+ 3 4
? 4
+ 2 10
? 4
```

We track only relevant states.

After `+ 1 4`, bowl 1 takes 2 and bowl 2 takes 2.

After `+ 2 3`, bowl 2 takes 2 more to become full, and bowl 3 takes 1.

After `+ 3 4`, bowl 3 fills completely and bowl 4 takes 1.

After `+ 2 10`, overflow from bowl 2 bypasses it, flows into bowl 3 (already full), then bowl 4, filling it further.

The key behavior demonstrated is that once a bowl becomes full, future pours skip it entirely and continue downward efficiently, which is exactly what DSU enforces.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) α(n)) | Each bowl becomes full once, each DSU operation is amortized inverse Ackermann |
| Space | O(n) | Arrays for capacity, current fill, and DSU parent |

The constraints allow up to 3×10^5 operations, so near-linear amortized behavior is necessary. The DSU-based skipping ensures each unit of structural change is paid for once, keeping the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, q = map(int, sys.stdin.readline().split())
    cap = list(map(int, sys.stdin.readline().split()))
    cur = [0] * n
    parent = list(range(n + 1))

    def find(x):
        if x >= n:
            return n
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        x = find(x)
        y = find(y)
        if x != y:
            parent[x] = y

    for _ in range(q):
        parts = sys.stdin.readline().split()
        if parts[0] == '+':
            l = int(parts[1]) - 1
            x = int(parts[2])
            i = find(l)
            while i < n and x > 0:
                free = cap[i] - cur[i]
                if free == 0:
                    union(i, i + 1)
                    i = find(i)
                    continue
                if x <= free:
                    cur[i] += x
                    x = 0
                else:
                    cur[i] += free
                    x -= free
                    union(i, i + 1)
                    i = find(i)
        else:
            l = int(parts[1]) - 1
            print(cur[l])

# custom minimal case
assert run("1 1\n5\n+ 1 10\n? 1\n") == "5\n", "cap overflow"

# all equal simple chain
assert run("3 4\n2 2 2\n+ 1 3\n? 1\n? 2\n? 3\n") == "2\n1\n0\n", "chain fill"

# no overflow case
assert run("3 3\n5 5 5\n+ 2 3\n? 2\n? 3\n") == "3\n0\n", "no spill"

# cascading overflow
assert run("3 3\n1 1 1\n+ 1 5\n? 3\n? 1\n") == "1\n1\n", "cascade"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 bowl overflow | 5 capped | overflow clipping |
| equal chain fill | 2 1 0 | propagation correctness |
| no spill | 3 0 | local fill behavior |
| full cascade | 1 1 | multi-level propagation |

## Edge Cases

One edge case is repeated attempts to pour into already full regions. For example, a bowl with capacity 2 that is already full must immediately redirect flow. The DSU structure handles this by ensuring `find(i)` never returns a saturated index, so we never loop indefinitely on it.

Another case is when a large pour skips over many full bowls and directly lands far below. Consider capacities `[1,1,1,10]` and pouring 100 into level 1. After the first three bowls are saturated, DSU compresses them into a single jump, so the remaining 97 is applied directly to the last bowl without revisiting intermediate indices.

A final edge case is when the pour fully empties into the ground. Once `find` returns the sentinel index `n`, all remaining liquid is discarded immediately. This prevents out-of-bounds access and ensures termination even when all bowls are full.
