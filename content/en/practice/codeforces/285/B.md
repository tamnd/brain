---
title: "CF 285B - Find Marble"
description: "We are given a row of positions from 1 to n, and each position currently holds a glass. A marble is initially hidden under the glass at position s. The only way the configuration changes is by applying a fixed rearrangement rule multiple times."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 285
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 175 (Div. 2)"
rating: 1200
weight: 285
solve_time_s: 58
verified: true
draft: false
---

[CF 285B - Find Marble](https://codeforces.com/problemset/problem/285/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of positions from 1 to n, and each position currently holds a glass. A marble is initially hidden under the glass at position s. The only way the configuration changes is by applying a fixed rearrangement rule multiple times. One application of this rule simultaneously moves every glass: the glass currently at position i moves to position p[i].

Because the marble is always glued to its glass, it effectively follows the movement of positions through repeated application of the same permutation. After applying the operation some number of times, the marble ends up at position t, and we need to determine the smallest number of applications needed to make this happen, or decide that it is impossible.

The key point is that the transformation is deterministic. From any position, the next position is uniquely defined, so repeated operations generate a fixed path starting from s.

The constraint n ≤ 100000 immediately rules out any simulation that recomputes full states for each step or explores all possible sequences. Since each operation is O(n), even 10^5 operations would be too large. The structure of the mapping is the important part, not repeated simulation of the whole array.

A few edge cases are easy to miss. If s equals t, the answer is zero, because no operation is needed. Another subtle case is when t is not reachable from s. For example, if n = 4, p = [2, 1, 4, 3], then positions split into cycles (1 ↔ 2) and (3 ↔ 4). If s = 1 and t = 3, the marble can never reach 3 because it stays inside its cycle, so the answer must be -1. A naive simulation that just runs for n steps without checking structure might incorrectly assume all nodes are reachable or fail to detect cycle separation.

## Approaches

A direct simulation approach applies the permutation repeatedly, updating the marble position each time. After each application, we compute the new position of the marble in O(1), but the full operation conceptually corresponds to iterating the permutation. We continue until we either reach t or repeat a state. Since there are at most n distinct positions, this would take O(n) steps in the worst case. However, a careless version that recomputes the full permutation effect each time would cost O(n^2), which is too slow for n = 10^5.

The key structural observation is that each position has exactly one outgoing transition, forming a directed graph where every node points to exactly one node. This guarantees that the graph decomposes into disjoint cycles. Starting from s, repeated applications never leave the cycle containing s. The task reduces to walking along this cycle until we either encounter t or return to s.

Once we realize this, the problem becomes: find the cycle starting at s, record the order of visited nodes, and measure the distance along this cycle from s to t.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) worst case | O(1) | Too slow |
| Cycle Traversal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start from position s and repeatedly apply the permutation rule, moving from i to p[i]. We do this because each operation is identical, so tracking the path of a single token fully describes the process.
2. Keep a list of visited positions in the order they are encountered. This reconstructs the cycle structure reachable from s.
3. Continue traversal until we return to s again. The moment we revisit s, we have completed exactly one full cycle, because every node has a unique next state.
4. Once the cycle is recorded, search for position t inside this cycle list. If t never appears, it is unreachable from s.
5. If t appears at index j in the cycle list and s is at index 0, the answer is j, because each step corresponds to exactly one application of the shuffling operation.

### Why it works

From any starting node in a permutation graph, repeated application of the transition function generates a sequence that must eventually repeat. Since every node has exactly one outgoing edge and exactly one incoming edge, the first repeated node must be the starting node of a cycle. This guarantees that the traversal from s produces exactly one simple cycle containing all reachable states. Any position not in this cycle is provably unreachable from s, so checking membership inside this cycle fully characterizes feasibility and shortest distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, s, t = map(int, input().split())
p = [0] + list(map(int, input().split()))

if s == t:
    print(0)
    sys.exit()

visited = []
cur = s

while True:
    visited.append(cur)
    cur = p[cur]
    if cur == s:
        break

pos = {v: i for i, v in enumerate(visited)}

if t not in pos:
    print(-1)
else:
    print(pos[t])
```

The implementation directly follows the cycle construction described earlier. The array p is kept 1-indexed for clarity, matching the problem statement.

The traversal loop collects all nodes in the cycle starting from s. We stop exactly when we return to s, ensuring we do not duplicate the cycle. The dictionary pos maps each node to its first occurrence index, allowing constant-time lookup for t.

A subtle point is handling the case s == t early. Without this, the cycle construction would still work, but we would unnecessarily traverse the entire cycle.

## Worked Examples

### Example 1

Input:

n = 4, s = 2, t = 1, p = [2, 3, 4, 1]

| Step | Current | Next | Visited |
| --- | --- | --- | --- |
| 1 | 2 | 3 | [2] |
| 2 | 3 | 4 | [2, 3] |
| 3 | 4 | 1 | [2, 3, 4] |
| 4 | 1 | 2 | stop |

Position t = 1 appears at index 3, so answer is 3.

This trace shows that the traversal forms a full cycle containing all nodes, and distance is measured along this cycle.

### Example 2

Input:

n = 4, s = 1, t = 3, p = [2, 1, 4, 3]

| Step | Current | Next | Visited |
| --- | --- | --- | --- |
| 1 | 1 | 2 | [1] |
| 2 | 2 | 1 | stop |

Cycle from 1 is [1, 2]. Position 3 is not present, so the answer is -1.

This confirms that even though 3 is part of the permutation, it is in a different cycle and cannot be reached from 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node in the cycle is visited exactly once until we return to the start |
| Space | O(n) | We store the cycle and a position map |

The constraints allow linear time traversal comfortably. Even in the worst case where all nodes form a single cycle, we visit each node once, which is well within limits for n up to 100000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys
    input = sys.stdin.readline

    n, s, t = map(int, input().split())
    p = [0] + list(map(int, input().split()))

    if s == t:
        return "0"

    visited = []
    cur = s

    while True:
        visited.append(cur)
        cur = p[cur]
        if cur == s:
            break

    pos = {v: i for i, v in enumerate(visited)}

    if t not in pos:
        return "-1"
    return str(pos[t])

# provided sample
assert run("4 2 1\n2 3 4 1\n") == "3"

# minimum size, no move needed
assert run("1 1 1\n1\n") == "0"

# simple unreachable (two cycles)
assert run("4 1 3\n2 1 4 3\n") == "-1"

# full cycle
assert run("3 1 2\n2 3 1\n") == "1"

# t is start
assert run("5 4 4\n2 3 4 5 1\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 2 1 / 2 3 4 1 | 3 | standard full cycle distance |
| 1 1 1 / 1 | 0 | minimum edge case |
| 4 1 3 / 2 1 4 3 | -1 | unreachable across cycles |
| 3 1 2 / 2 3 1 | 1 | basic shift inside cycle |
| 5 4 4 / 2 3 4 5 1 | 0 | start equals target |

## Edge Cases

### s equals t

Input:

n = 5, s = 3, t = 3, p = [2, 3, 4, 5, 1]

The algorithm immediately returns 0 before traversal. Even though a full cycle exists, no movement is needed, so skipping traversal avoids unnecessary work.

### Different cycles

Input:

n = 4, s = 1, t = 3, p = [2, 1, 4, 3]

Traversal from 1 yields [1, 2] and stops when returning to 1. The map does not contain 3, so we correctly output -1. This demonstrates that cycle decomposition fully determines reachability.

### Full cycle

Input:

n = 3, s = 1, t = 2, p = [2, 3, 1]

Traversal yields [1, 2, 3]. The position of 2 is 1, so we return 1. This shows how distance is directly encoded in the cycle order without any additional computation.
