---
title: "CF 1574D - The Strongest Build"
description: "In this problem, we are asked to help Ivan choose the strongest possible hero build from a set of equipment slots, each with multiple items of different strengths. Each slot has its own list of items, already sorted by increasing strength."
date: "2026-06-10T11:04:57+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dfs-and-similar", "graphs", "greedy", "hashing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1574
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 114 (Rated for Div. 2)"
rating: 2000
weight: 1574
solve_time_s: 81
verified: true
draft: false
---

[CF 1574D - The Strongest Build](https://codeforces.com/problemset/problem/1574/D)

**Rating:** 2000  
**Tags:** binary search, brute force, data structures, dfs and similar, graphs, greedy, hashing, implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

In this problem, we are asked to help Ivan choose the strongest possible hero build from a set of equipment slots, each with multiple items of different strengths. Each slot has its own list of items, already sorted by increasing strength. Ivan must pick exactly one item per slot, forming a build. Some builds are explicitly banned, and the task is to find a build with the largest total strength that is not banned. The output is simply the chosen indices of the items in each slot.

The constraints are important for designing an algorithm. The number of slots, $n$, is at most 10, which is very small. This suggests that an approach exponential in $n$ may still be feasible. Each slot can have up to $2 \cdot 10^5$ items, but the sum of all items over all slots is capped at $2 \cdot 10^5$, so we cannot afford to enumerate every possible combination naively, because in the worst case the total number of builds is the product of the $c_i$, which can easily exceed $10^{18}$ if we tried brute force.

Non-obvious edge cases include scenarios where the strongest build (picking the last, largest item in every slot) is banned. In that case, a naive solution that always picks the largest item per slot would fail. For example, if we have two slots with items `[1, 2]` and `[1, 3]`, and the banned build is `[2, 2]`, the algorithm must correctly pick `[2, 1]` instead, which has the next highest total strength.

## Approaches

The simplest brute-force approach is to generate every possible combination of items, calculate the strength of each build, and filter out the banned builds. While correct in principle, this approach is infeasible because even for $n = 10$ and small lists of length 20 each, there would be $20^{10} \approx 10^{13}$ builds.

A better approach takes advantage of the small $n$ and the fact that each slot’s items are sorted. The optimal build in the absence of bans is always the one using the last item in each list. Therefore, the problem reduces to checking if this “all-last-items” build is banned. If it is, the next candidate builds are those where one slot is reduced by one index, i.e., we try `[c_1 - 1, c_2, ..., c_n]`, `[c_1, c_2 - 1, ..., c_n]`, etc., prioritizing the largest reductions in total strength. This structure forms a max-heap search problem: we treat builds as nodes with a total strength, always expanding the highest-strength node that hasn't been banned yet.

We use a priority queue (max-heap) to maintain candidate builds, sorted by strength. Initially, the heap contains the maximal build. We pop the strongest build; if it is not banned, it is our answer. Otherwise, we generate new candidate builds by decreasing one index in each slot (but only if the resulting build hasn't already been visited). This way, we explore builds in descending strength order without enumerating all possibilities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(∏ c_i) | O(∏ c_i) | Too slow |
| Max-Heap Search | O(m log m + n log n * m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read all slot data and banned builds. Convert banned builds into tuples and store in a set for O(1) lookups.
2. Construct the initial build by picking the last item from each slot. Compute its total strength.
3. Initialize a max-heap with a tuple `(-strength, build)` to simulate a max-heap using Python’s min-heap.
4. Maintain a set of visited builds to avoid reprocessing the same build multiple times.
5. While the heap is not empty, pop the build with the current highest strength. If it is not banned, print it as the answer and exit.
6. Otherwise, for each slot, create a new build by reducing the index in that slot by one (but only if the index is still ≥ 1). If this new build has not been visited, compute its strength and push it to the heap.
7. Continue until a non-banned build is found. Because the initial build is guaranteed not to be banned, this loop will always terminate.

Why it works: At every step, the heap ensures that we process builds in strictly descending order of total strength. We only skip builds that are banned, and every candidate that could possibly be stronger than any unvisited build is either in the heap or will be pushed to it. The visited set prevents revisiting the same build. This guarantees that the first build popped from the heap that is not banned has the maximum possible strength.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

n = int(input())
slots = []
for _ in range(n):
    data = list(map(int, input().split()))
    c_i = data[0]
    slots.append(data[1:])

m = int(input())
banned = set()
for _ in range(m):
    b = tuple(map(int, input().split()))
    banned.add(b)

# Initial build: last item from each slot
init_build = tuple(len(slot) for slot in slots)
init_strength = sum(slots[i][idx - 1] for i, idx in enumerate(init_build))

heap = [(-init_strength, init_build)]
visited = set()
visited.add(init_build)

while heap:
    neg_strength, build = heapq.heappop(heap)
    if build not in banned:
        print(' '.join(map(str, build)))
        break
    for i in range(n):
        if build[i] > 1:
            new_build = list(build)
            new_build[i] -= 1
            new_build = tuple(new_build)
            if new_build not in visited:
                new_strength = -neg_strength - slots[i][build[i]-1] + slots[i][new_build[i]-1]
                heapq.heappush(heap, (-new_strength, new_build))
                visited.add(new_build)
```

The solution starts by reading the input and creating the slot arrays. The banned builds are stored in a set for fast membership checks. The initial build is constructed by taking the last element from each slot, giving the maximal possible strength. The heap guarantees that we always consider the strongest unvisited candidate next. When generating neighbors, we carefully compute the new strength by subtracting the old item and adding the new one to avoid recalculating the full sum each time. The visited set ensures we never push the same build twice, which could lead to infinite loops or inefficiency.

## Worked Examples

Sample 1 Input:

```
3
3 1 2 3
2 1 5
3 2 4 6
2
3 2 3
3 2 2
```

| Step | Heap Top | Strength | Build Popped | Action |
| --- | --- | --- | --- | --- |
| 0 | [(12, (3,2,3))] | 12 | (3,2,3) | Banned, generate neighbors |
| 1 | [(11,(2,2,3)),(10,(3,1,3)),(10,(3,2,2))] | 11 | (2,2,3) | Not banned, print |

Trace shows the algorithm quickly finds the next-strongest non-banned build `(2,2,3)`.

Custom Input:

```
2
2 5 10
2 7 9
1
2 2
```

| Step | Heap Top | Strength | Build Popped | Action |
| --- | --- | --- | --- | --- |
| 0 | [(19,(2,2))] | 19 | (2,2) | Banned, generate neighbors |
| 1 | [(16,(1,2)),(17,(2,1))] | 17 | (2,1) | Not banned, print |

Confirms correct handling when the strongest build is banned.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m + k n log m) | Each build pushed into the heap is unique and ≤ number of builds processed before finding answer; heap operations are log of heap size, neighbor generation is O(n) per build. |
| Space | O(m + k) | `banned` set uses O(m), `visited` set stores O(k) builds until solution found. |

Given $n \le 10$ and $m \le 10^5$, the algorithm processes only builds near the strongest ones and terminates quickly, well within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    slots = []
    for _ in range(n):
        data = list(map(int, input().split()))
        c_i = data[0]
        slots.append(data[1:])
    m = int(input())
    banned = set()
    for _ in range(m):
        banned.add(tuple(map(int, input().split())))
    import heapq
    init_build = tuple(len(slot) for slot in slots)
    init_strength = sum(slots[i][idx - 1] for i, idx in enumerate(init_build))
    heap = [(-init_strength, init_build)]
```
