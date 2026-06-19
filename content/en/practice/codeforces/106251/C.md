---
title: "CF 106251C - Marbles"
description: "We are given a permutation on the integers from 1 to n, meaning every position points to exactly one other position, and every position is pointed to exactly once."
date: "2026-06-19T14:15:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106251
codeforces_index: "C"
codeforces_contest_name: "MITIT Winter 2025-26 Beginner Round"
rating: 0
weight: 106251
solve_time_s: 52
verified: true
draft: false
---

[CF 106251C - Marbles](https://codeforces.com/problemset/problem/106251/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation on the integers from 1 to n, meaning every position points to exactly one other position, and every position is pointed to exactly once. This structure can be viewed as a directed graph where each node has exactly one outgoing edge and exactly one incoming edge, so the graph decomposes into disjoint directed cycles.

The task is to assign one of three colors to each node so that each cycle is colored under a specific pattern. For a cycle of even length, we must alternate two colors along the cycle. For a cycle of odd length, we still alternate two colors along the cycle but one node cannot fit into the alternation cleanly, so it receives a third distinct color.

The output is simply the color assigned to each index from 1 to n.

The constraints implied by a permutation of size up to typical Codeforces limits, usually around 2 times 10^5 or 10^6, immediately rule out any quadratic simulation over pairs of elements. Any approach that revisits nodes repeatedly or scans arrays per cycle would be too slow. A linear traversal is required, which suggests that each node must be visited a constant number of times, most likely by marking visited nodes and walking through cycles directly.

A subtle edge case occurs when all cycles are of length one. For example, if the permutation is [1], then the cycle has odd length and consists of a single node. A naive alternating coloring approach would try to assign two colors and fail to assign the third consistently, but the correct output is simply that this node must be colored with the special color.

Another edge case is a large single cycle such as [2, 3, 4, ..., n, 1]. If its length is odd, exactly one node must become the special color, and careless implementations may accidentally assign two special nodes if they restart coloring mid cycle or fail to preserve state across traversal.

## Approaches

A brute force approach would repeatedly pick an unvisited node, follow the permutation pointers until returning to the start, and then attempt to assign colors while storing the full cycle. This is already close to optimal, but if implemented inefficiently, it may rescan or re-walk cycles multiple times, leading to quadratic behavior in the worst case where there is a single cycle of length n and repeated scanning is used to detect structure.

The key observation is that the permutation structure guarantees a partition into disjoint cycles, and each cycle can be processed independently. Once we enter a cycle, we can walk through it exactly once, record or directly assign colors, and never revisit its nodes again. This removes any need for global reasoning beyond local cycle structure.

The optimal solution is therefore a single pass over all nodes, launching a cycle traversal whenever an unvisited node is encountered, and coloring nodes on the fly according to parity position within the cycle. If the cycle length is odd, we deliberately assign the last node a special color after completing the alternating pattern.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Cycle Rescans | O(n^2) | O(n) | Too slow |
| Cycle Decomposition Once | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Maintain a visited array initialized to false for all nodes. This ensures each node belongs to exactly one processed cycle and is never revisited in later traversals.
2. Iterate through all nodes from 1 to n. Whenever an unvisited node is found, it becomes the starting point of a new cycle.
3. Traverse the cycle by repeatedly following the permutation pointer until returning to the starting node. While traversing, collect nodes in a list in the order they appear in the cycle. This ordering matters because coloring depends on adjacency along the cycle.
4. After the cycle is collected, determine its length k. If k is even, assign colors alternately along the list using two colors, ensuring adjacent nodes in the cycle receive different colors.
5. If k is odd, assign alternating colors for the first k minus one nodes, then assign the final node the special third color. This resolves the parity mismatch that makes a pure two-color alternation impossible on an odd cycle.
6. Store the assigned colors in an output array indexed by node.

The reason this traversal is safe is that once we leave a node, following its outgoing edge always stays inside the same cycle, so we never accidentally merge or split structures.

### Why it works

The permutation guarantees that every node lies in exactly one simple directed cycle, meaning the graph decomposes into disjoint closed loops. Within a cycle, each node has exactly two neighbors in the undirected sense of the cycle order. Alternating two colors works perfectly on even-length cycles because parity is consistent when wrapping around. On odd-length cycles, parity flips after every edge, so returning to the start forces a contradiction, which is resolved by breaking the alternation at exactly one node. Since cycles are disjoint, coloring one cycle never constrains another, so independent processing is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = [0] + list(map(int, input().split()))

    vis = [False] * (n + 1)
    color = [''] * (n + 1)

    for i in range(1, n + 1):
        if vis[i]:
            continue

        cycle = []
        cur = i

        while not vis[cur]:
            vis[cur] = True
            cycle.append(cur)
            cur = p[cur]

        k = len(cycle)

        if k % 2 == 0:
            for j in range(k):
                color[cycle[j]] = 'R' if j % 2 == 0 else 'B'
        else:
            for j in range(k - 1):
                color[cycle[j]] = 'R' if j % 2 == 0 else 'B'
            color[cycle[-1]] = 'G'

    print("".join(color[1:]))

if __name__ == "__main__":
    solve()
```

The core implementation directly follows cycle extraction. The visited array prevents revisiting nodes across cycles, ensuring linear complexity. The cycle list preserves order so that alternating coloring is consistent along edges. The only subtle decision is handling odd cycles by assigning the last collected node the special color, which works because the traversal order matches the cycle order.

## Worked Examples

Consider a permutation of size 4 given by p = [2, 1, 4, 3]. This forms two cycles: (1, 2) and (3, 4).

| Step | Current Node | Cycle Built So Far | Action |
| --- | --- | --- | --- |
| 1 | 1 | [1] | visit 1 |
| 2 | 2 | [1, 2] | follow edge back to 1 and stop |
| 3 | 3 | [3] | start new cycle |
| 4 | 4 | [3, 4] | close cycle |

Both cycles have even length, so we alternate colors. Cycle (1, 2) becomes R, B and cycle (3, 4) becomes R, B.

Now consider p = [2, 3, 1], a single cycle of length 3.

| Step | Current Node | Cycle Built So Far | Action |
| --- | --- | --- | --- |
| 1 | 1 | [1] | start |
| 2 | 2 | [1, 2] | continue |
| 3 | 3 | [1, 2, 3] | return to start |

Since the cycle length is odd, nodes 1 and 2 get alternating colors R and B, while node 3 receives G.

These examples confirm that traversal order matches cycle structure and that coloring is consistent within each cycle independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each node is visited exactly once during cycle traversal |
| Space | O(n) | storage for visited array, color array, and cycle buffer |

The solution fits comfortably within typical constraints for permutation-based problems, since every operation is constant work per node and no nested traversal occurs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve_capture()

def solve_capture():
    import sys
    input = sys.stdin.readline

    n = int(input())
    p = [0] + list(map(int, input().split()))

    vis = [False] * (n + 1)
    color = [''] * (n + 1)

    for i in range(1, n + 1):
        if vis[i]:
            continue
        cycle = []
        cur = i
        while not vis[cur]:
            vis[cur] = True
            cycle.append(cur)
            cur = p[cur]
        k = len(cycle)
        if k % 2 == 0:
            for j in range(k):
                color[cycle[j]] = 'R' if j % 2 == 0 else 'B'
        else:
            for j in range(k - 1):
                color[cycle[j]] = 'R' if j % 2 == 0 else 'B'
            color[cycle[-1]] = 'G'

    return "".join(color[1:])

# sample-like test 1: two cycles
assert run("4\n2 1 4 3\n") == "RBRB", "two even cycles"

# single odd cycle
assert run("3\n2 3 1\n") == "RBG", "odd cycle length 3"

# single fixed points
assert run("1\n1\n") == "G", "single node cycle"

# mixed
assert run("5\n2 1 4 5 3\n") in ["RBRBG", "BRBRG"], "mixed cycles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 / 2 1 4 3 | RBRB | two independent even cycles |
| 3 / 2 3 1 | RBG | odd cycle handling |
| 1 / 1 | G | minimum cycle edge case |
| 5 / 2 1 4 5 3 | variant | multiple cycles and consistency |

## Edge Cases

A single-node cycle such as n = 1 with p1 = 1 produces a cycle of length one. The traversal collects only that node, and since the length is odd, the algorithm assigns it the special color directly. The cycle logic still works because the loop terminates immediately after returning to the start.

A fully connected cycle such as n = 5 with p = [2, 3, 4, 5, 1] is handled by collecting all nodes in order. The coloring assigns alternating colors for the first four nodes and then places the fifth into the special color slot. The traversal ensures exactly one node receives the special color because the cycle list contains each node exactly once and the last position is uniquely defined by the traversal order.
