---
title: "CF 1020B - Badge"
description: "We are given a directed structure over students where each student points to exactly one other student. This forms a functional graph: every node has outdegree one, so starting from any node and repeatedly following pointers eventually forces us into a cycle."
date: "2026-06-16T22:00:01+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1020
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 503 (by SIS, Div. 2)"
rating: 1000
weight: 1020
solve_time_s: 90
verified: true
draft: false
---

[CF 1020B - Badge](https://codeforces.com/problemset/problem/1020/B)

**Rating:** 1000  
**Tags:** brute force, dfs and similar, graphs  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed structure over students where each student points to exactly one other student. This forms a functional graph: every node has outdegree one, so starting from any node and repeatedly following pointers eventually forces us into a cycle.

A teacher starts at some student `a`. That student is immediately marked once. Then the teacher keeps moving from the current student `i` to `p[i]`, marking each visited student. The process stops the moment the teacher arrives at a student who has already been marked, and that student receives the second mark.

The task is to determine, for every possible starting node `a`, which student would be the first one to be visited twice.

The constraint `n ≤ 1000` is small enough that an O(n²) or even O(n³) simulation is safe. Any solution that runs a fresh traversal from each starting node is already within limits, since each traversal can visit at most `n` nodes before repeating.

A subtle point is that the process is not simply “find a cycle entry” in a static sense, because the set of visited nodes depends on the starting point. The first repeated node is the first node that appears twice in the traversal order, not necessarily the start of a cycle in the usual decomposition sense.

Edge cases that matter include:

A self-loop such as `p[i] = i`. Starting from such a node immediately revisits it on the first move, so the answer is trivially itself.

Another case is when all nodes eventually flow into a single cycle. Even then, different starting points within a tail can lead to different first-repeated nodes because the entry point into the cycle depends on how the path is traversed.

## Approaches

The brute-force idea is straightforward: simulate the teacher’s movement for each starting student. We maintain a visited array, walk along `p[current]`, and stop as soon as we reach a node already seen in that simulation. That node is recorded as the answer for the start.

This works because each simulation independently reconstructs the exact process described in the statement. The correctness is immediate since we are literally following the rules step by step.

The inefficiency comes from repeating the same walks from scratch. Each simulation may traverse a long chain of length O(n), and we do this for all n starting points, giving O(n²) steps overall. With n up to 1000, this is still fine, but it hints at a deeper structure: every traversal is deterministic and only depends on following pointers in a functional graph.

The key observation is that the answer for a starting node depends only on where its path first intersects a cycle or revisits a node already on its path. Since the graph is functional, every node belongs either to a tail leading into a cycle or to the cycle itself. The first repeated node for any start is exactly the first node on the path whose next visit would violate the “first time seen” property in that traversal.

Because n is small, we do not need heavy preprocessing or cycle decomposition; direct simulation with a fresh visited array is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each starting student `a`, create a fresh boolean array `visited` of size `n + 1`. This ensures each simulation is independent and does not leak state across starts.
2. Initialize `current = a`.
3. Repeatedly check whether `current` has been visited. If it has, this means we have returned to a node already seen in this simulation, so `current` is the answer for this starting point.
4. If it has not been visited, mark `current` as visited.
5. Move `current = p[current]` and repeat.
6. Store the first node that triggered the “already visited” condition as the answer for `a`.

The reason this step order matters is that the check must happen before advancing, because the repeated node is defined as the node we just entered, not the node we are about to leave.

### Why it works

During the simulation from a fixed start `a`, the algorithm maintains the invariant that `visited[x]` is true if and only if node `x` has been visited earlier in this exact traversal. Since the graph has outdegree one, the sequence of visited nodes forms a single walk. The first time we encounter a node that is already marked, that node must be the earliest repetition in the sequence by definition of how we maintain `visited`. No earlier node can be a repeat, otherwise the loop would have terminated earlier. This guarantees the returned node is exactly the first node visited twice in the process.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = [0] + list(map(int, input().split()))
    
    ans = [0] * (n + 1)
    
    for start in range(1, n + 1):
        visited = [False] * (n + 1)
        cur = start
        
        while True:
            if visited[cur]:
                ans[start] = cur
                break
            visited[cur] = True
            cur = p[cur]
    
    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The implementation follows the traversal exactly as described. The crucial detail is that we check `visited[cur]` before marking or moving, since the repetition is detected at the moment we land on an already-seen node. Each start recomputes its own visited array to avoid interference between simulations.

The 1-indexed array simplifies mapping directly from student labels to indices, avoiding off-by-one errors when reading `p`.

## Worked Examples

### Example 1

Input:

```
3
2 3 2
```

We compute each start separately.

For `start = 1`, we track the traversal:

| Step | Current | Visited before | Action |
| --- | --- | --- | --- |
| 1 | 1 | {} | mark 1 |
| 2 | 2 | {1} | mark 2 |
| 3 | 3 | {1,2} | mark 3 |
| 4 | 2 | {1,2,3} | repeat found |

Answer is 2.

For `start = 2`:

| Step | Current | Visited before | Action |
| --- | --- | --- | --- |
| 1 | 2 | {} | mark 2 |
| 2 | 3 | {2} | mark 3 |
| 3 | 2 | {2,3} | repeat found |

Answer is 2.

For `start = 3`:

| Step | Current | Visited before | Action |
| --- | --- | --- | --- |
| 1 | 3 | {} | mark 3 |
| 2 | 2 | {3} | mark 2 |
| 3 | 3 | {2,3} | repeat found |

Answer is 3.

This confirms that the first repetition depends on where the traversal enters the cycle and not just the cycle itself.

### Example 2

Consider:

```
4
1 2 3 4
```

Each node points to the next, forming a cycle.

For `start = 1`, we visit `1 → 1`, so answer is 1.

For `start = 2`, we visit `2 → 2`, so answer is 2.

Similarly for others. Each node is a self-return in this traversal sense because we immediately revisit after cycling through all nodes already seen in that run.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each of n starts performs a traversal of up to n steps |
| Space | O(n) | Visited array per traversal |

With `n ≤ 1000`, at most about 1e6 operations occur, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("""3
2 3 2
""") == "2 2 3"

# self-loop case
assert run("""1
1
""") == "1"

# simple chain
assert run("""4
2 3 4 4
""") == "4 4 4 4"

# all point to 1
assert run("""4
1 1 1 1
""") == "1 1 1 1"

# cycle
assert run("""3
2 3 1
""") == "1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | single-node self-loop |
| chain to cycle | 4 4 4 4 | tail leading into cycle |
| all to 1 | 1 1 1 1 | star-shaped convergence |
| 2 3 1 | 1 2 3 | pure cycle behavior |

## Edge Cases

A self-loop like `p[i] = i` is the most direct case. Starting at `i`, we mark it and immediately see it again after one transition, so the algorithm returns `i` correctly because `visited[i]` is already true when we revisit it.

A chain that leads into a cycle behaves similarly but with delayed repetition. For example `1 → 2 → 3 → 3`. Starting at 1, we visit 1, 2, 3, then attempt to move to 3 again. Since 3 is already marked, it is correctly identified as the first repeated node. The simulation ensures the cycle entry is detected exactly at first revisit, not earlier or later.
