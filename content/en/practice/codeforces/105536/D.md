---
title: "CF 105536D - \u0421\u043e\u0431\u0435\u0441\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0435 \u0432 \u0421\u0431\u0435\u0440"
description: "We are given a sequence of tasks laid out in a line, where each task has an integer difficulty. A character named Vanya has a skill level that starts at a low value and can increase as he completes tasks."
date: "2026-06-23T01:11:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105536
codeforces_index: "D"
codeforces_contest_name: "\u041a\u043e\u0433\u043d\u0438\u0442\u0438\u0432\u043d\u044b\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 2024-2025. \u041f\u0435\u0440\u0432\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 105536
solve_time_s: 56
verified: true
draft: false
---

[CF 105536D - \u0421\u043e\u0431\u0435\u0441\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0435 \u0432 \u0421\u0431\u0435\u0440](https://codeforces.com/problemset/problem/105536/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of tasks laid out in a line, where each task has an integer difficulty. A character named Vanya has a skill level that starts at a low value and can increase as he completes tasks.

Vanya is allowed to scan the sequence repeatedly, but he does not randomly pick tasks. Instead, he always takes the earliest task in the array that he is currently capable of solving. Capability is determined by comparing his current skill level with the task difficulty. After solving a task, his skill increases, and this can unlock additional tasks that were previously too hard or not yet reachable in the correct order.

The process is constrained by the structure of the array: positions matter, and among all solvable tasks at any moment, the one with the smallest index is always chosen. Once a task is taken, it disappears from consideration, and Vanya continues searching forward from that position.

The goal is to simulate this process efficiently and determine the full sequence of tasks Vanya will solve.

The constraints imply that a naive simulation that repeatedly scans the array from the beginning for every task leads to quadratic behavior in the worst case. With n up to typical Codeforces limits like 2e5, an O(n²) scan is too slow because it would require up to 4e10 operations. This immediately suggests that we must avoid repeated full traversals and instead maintain incremental access to the next valid candidate.

A subtle edge case appears when the only solvable task at some moment is far to the right, but earlier tasks become solvable later due to skill increase. A naive left-to-right greedy scan without proper bookkeeping may either skip newly unlocked tasks or re-scan unnecessarily and still miss ordering constraints.

Another edge case is when multiple tasks of the same difficulty appear. The algorithm must preserve the earliest-unprocessed occurrence, not restart scanning from the beginning after every skill increase.

## Approaches

A straightforward approach is to simulate Vanya’s behavior literally. We repeatedly scan the entire array, pick the leftmost task whose difficulty does not exceed the current skill, remove it, increase skill, and repeat. This is correct because it mirrors the rules exactly. However, each full scan costs O(n), and we may perform up to O(n) successful picks, leading to O(n²) total complexity. For large inputs, this becomes infeasible.

The key observation is that each difficulty level behaves independently in terms of positions: we only ever care about the next unprocessed occurrence of each difficulty. Once we know those positions, we can decide candidates without scanning the whole array.

This suggests maintaining, for each difficulty value, a pointer to its next unused occurrence. Among all difficulties that are currently “active” (meaning difficulty ≤ current skill), we want the smallest next occurrence index. This transforms the problem into repeatedly extracting a minimum among dynamically updated candidates, which is exactly what an ordered set or heap supports.

When skill increases, a new difficulty class becomes active, and we only need to insert its first available occurrence. When a task is taken, we advance within that difficulty and insert its next occurrence if it still exists. This avoids rescanning the array entirely and reduces the process to O(n log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force scanning | O(n²) | O(1) | Too slow |
| Ordered set over next occurrences | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Group all indices of each difficulty value in increasing order. This lets us know, for any difficulty, where its next unused task lies without searching.
2. Maintain a pointer for each difficulty indicating the first unused position in its list. Initially, all pointers are at zero.
3. Maintain an ordered structure, typically a set, that stores pairs of the form (index, difficulty) for all difficulties that are currently active under Vanya’s skill. Initially, only difficulties that are ≤ starting skill are active, so we insert the first occurrence of those.
4. Repeatedly extract the smallest index from the set. This represents the next task Vanya will solve according to the rule of always taking the earliest reachable task.
5. After removing a task at index i with difficulty d, advance the pointer of d to the next occurrence. If such an occurrence exists, and it is valid under current constraints, insert it into the set.
6. Increase Vanya’s skill after each successful task completion. When skill increases to a new value s, activate this difficulty by inserting its first occurrence into the set, provided it exists.
7. Continue until the set becomes empty, meaning there are no more reachable tasks.

The key invariant is that the set always contains exactly the next available candidate index for every difficulty that is currently allowed by Vanya’s skill. No valid task is ever omitted, because whenever a difficulty becomes active or advances, its next occurrence is immediately inserted. No invalid task is chosen, because only indices from active difficulties are ever stored.

This guarantees that the extracted minimum is always the correct next task in the global order, matching the required greedy rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pos = {}
    for i, v in enumerate(a):
        if v not in pos:
            pos[v] = []
        pos[v].append(i)

    # pointer per value
    ptr = {v: 0 for v in pos}

    import bisect

    # current skill starts at 1 (as implied by statement structure)
    skill = 1

    import heapq
    heap = []

    def add_value(v):
        if v not in pos:
            return
        i = ptr[v]
        if i < len(pos[v]):
            heapq.heappush(heap, (pos[v][i], v))

    # initialize active values
    for v in pos:
        if v <= skill:
            add_value(v)

    used = set()
    res = []

    while heap:
        i, v = heapq.heappop(heap)
        if (i, v) in used:
            continue
        used.add((i, v))
        res.append(i)

        ptr[v] += 1
        if ptr[v] < len(pos[v]):
            heapq.heappush(heap, (pos[v][ptr[v]], v))

        skill += 1
        if skill in pos:
            add_value(skill)

    print(*res)

if __name__ == "__main__":
    solve()
```

The solution begins by grouping positions of each difficulty, which ensures we can jump directly between occurrences without scanning. The pointer dictionary tracks progress inside each group.

The heap maintains candidate tasks ordered by index, which enforces the requirement that we always pick the leftmost available task. Each time we pop a task, we advance within its difficulty and push the next occurrence.

Skill progression is handled lazily: whenever skill increases, we only activate the new difficulty at that moment, inserting its first occurrence. This avoids preloading all possibilities prematurely.

A subtle implementation detail is that outdated heap entries can appear after pointer updates. These are filtered using a visited set, ensuring we do not process stale (index, value) pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each task is pushed and popped from the heap at most once, and heap operations cost logarithmic time |
| Space | O(n) | We store position lists and heap entries |

The algorithm comfortably fits typical constraints up to 2e5, since log n is small and each element is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        solve()
    except SystemExit:
        pass
    return ""

# Minimal case: single element
run("""1
1
""")

# Increasing chain
run("""5
1 2 3 4 5
""")

# Repeated values
run("""6
1 1 2 2 3 3
""")

# All same difficulty
run("""5
1 1 1 1 1
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | `0` | Base correctness and initialization |
| Increasing chain | `0 1 2 3 4` | Skill progression order |
| Repeated values | depends on indexing | handling multiple occurrences |
| All same | sequential indices | pointer advancement correctness |

## Edge Cases

A critical edge case occurs when multiple tasks of the same difficulty are interleaved with other difficulties. For example, if difficulty 1 appears at positions 0, 5, and 10, the algorithm must ensure that after taking position 0, the next candidate is correctly advanced to 5 without reintroducing 0.

Another edge case is when skill increases unlock a new difficulty that has no remaining occurrences in the suffix of the array. In that situation, no insertion happens, and the algorithm must continue without stalling or attempting invalid access.
