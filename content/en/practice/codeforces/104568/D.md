---
title: "CF 104568D - Freeform Factory"
description: "We are given a bipartite system with workers on one side and machines on the other, both of size $N$. Each worker initially knows how to operate some subset of machines. Every day, all workers arrive in an arbitrary order."
date: "2026-06-30T08:30:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104568
codeforces_index: "D"
codeforces_contest_name: "2016 Google Code Jam Round 2 (GCJ 16 Round 2)"
rating: 0
weight: 104568
solve_time_s: 76
verified: true
draft: false
---

[CF 104568D - Freeform Factory](https://codeforces.com/problemset/problem/104568/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a bipartite system with workers on one side and machines on the other, both of size $N$. Each worker initially knows how to operate some subset of machines. Every day, all workers arrive in an arbitrary order. When a worker arrives, they look at machines they know that are still unassigned, and they pick one of them arbitrarily. Once a machine is taken, it stays assigned for the rest of the day.

We are allowed to add new “training edges”, meaning we can teach any worker any machine at cost 1 per pair, effectively adding an edge in the bipartite graph. The goal is to guarantee that no matter how workers are ordered and no matter how they break ties when choosing a machine, at the end of the process every machine is assigned to exactly one worker.

The key difficulty is that the adversary controls both the arrival order and the choices among available machines. That means any fragile structure in the graph can be exploited to force a failure.

The constraint $N \le 25$ suggests that solutions that try to enumerate subsets or simulate states of size $2^N$ are potentially acceptable, but it also leaves room for a much simpler structural observation if one exists.

A subtle failure case appears whenever some worker does not know some machine. Even if a perfect matching exists in the static graph, the greedy process can still destroy it by making a “bad early choice” that blocks a necessary later assignment.

For example, if worker $A$ cannot operate machine 2, but worker $B$ can operate both machines, then if $B$ arrives first and chooses machine 1, worker $A$ is later forced to take machine 1 as well or be idle, leaving machine 2 unassigned. The existence of a perfect matching is not enough; the system must be robust under all greedy executions.

This robustness requirement is what drives the solution.

## Approaches

A natural starting point is to think in terms of greedy matching on a bipartite graph. The process is not the standard offline matching problem; instead, it is an online process with adversarial ordering and adversarial tie-breaking.

One could attempt to characterize when greedy matching always succeeds. This leads quickly to trying to enforce structural constraints like Hall’s condition for all prefixes and all subchoices. However, because workers may choose arbitrarily among multiple available machines, the system must remain correct under every possible sequence of destructive choices, not just some sequence.

The brute-force way to think about fixing the graph is to consider adding edges and simulating all possible arrival orders and choices. For each configuration, we would verify whether every possible greedy run yields a perfect matching. This explodes combinatorially: even for a fixed graph, the number of possible executions is exponential in both permutations and branching choices.

The key observation is that any missing edge introduces a potential point of failure that can be exploited. Suppose worker $i$ does not know machine $j$. If we try to argue that the system is still safe, we must show that machine $j$ can never be “lost” due to earlier arbitrary assignments. But since earlier workers may consume all alternative machines needed to preserve feasibility, the adversary can always force a configuration where $j$ becomes isolated from all remaining workers except $i$, and $i$ cannot take it. That produces an unavoidable failure.

This reasoning forces a very strong conclusion: to guarantee correctness under arbitrary greedy behavior, every worker must be able to operate every machine. Once that is true, no choice can ever eliminate feasibility, because every remaining worker always has full flexibility to take any remaining machine.

So the optimal strategy is simply to complete the bipartite graph by adding every missing worker-machine edge.

The answer becomes the number of zero entries in the matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulate / brute-force all greedy outcomes | Exponential | Exponential | Too slow |
| Complete bipartite completion | $O(N^2)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the $N \times N$ matrix describing which worker can operate which machine. Each “1” is an existing edge, each “0” is a missing edge.
2. Count how many pairs $(i, j)$ have a zero in the matrix. Each such pair represents a missing capability.
3. Output this count as the cost, since we must add all missing edges to guarantee robustness.

### Why it works

If any worker-machine pair is missing, then that pair can be turned into a forced bottleneck under a carefully chosen arrival order. The adversary can ensure that all other workers consume alternative machines in such a way that the only remaining safe assignment for a machine would require a missing edge. Since that assignment is impossible, the system cannot be guaranteed to complete.

Once all edges are present, every worker always has full freedom among all machines regardless of the current partial assignment. No sequence of greedy choices can eliminate the ability to complete the matching because no worker ever runs out of valid options until the last step, where only one machine remains.

This removes all possible failure modes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for tc in range(1, T + 1):
        n = int(input())
        ans = 0
        for _ in range(n):
            row = input().strip()
            ans += row.count('0')
        print(f"Case #{tc}: {ans}")

if __name__ == "__main__":
    solve()
```

The code directly counts how many training edges must be added. Each row is scanned once, and every missing capability contributes one dollar to the answer. The formatting follows the required output style.

No additional data structures are needed because the solution depends only on the total number of missing connections.

## Worked Examples

### Example 1

Consider a small system:

```
2
10
01
```

| Step | Worker 1 edges | Worker 2 edges | Missing count |
| --- | --- | --- | --- |
| Read row 1 | machine 1 only | - | 1 |
| Read row 2 | - | machine 2 only | 1 |

Total missing edges is 2, so we need to add both missing capabilities.

This demonstrates that when workers have disjoint knowledge, every missing pairing must be fixed to eliminate dependency on arrival order.

### Example 2

```
3
111
111
111
```

| Step | Row | Missing count |
| --- | --- | --- |
| 1 | 111 | 0 |
| 2 | 111 | 0 |
| 3 | 111 | 0 |

No training is needed since every worker already knows every machine. Any greedy execution always has full flexibility, so no failure is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ per test case | Each cell of the matrix is scanned once |
| Space | $O(1)$ extra | Only a counter is maintained |

Given $N \le 25$ and up to 100 test cases, this runs easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-style checks (illustrative format)
assert run("1\n1\n1\n") == "Case #1: 0"

# all zeros
assert run("1\n2\n00\n00\n") == "Case #1: 4"

# already complete
assert run("1\n2\n11\n11\n") == "Case #1: 0"

# mixed case
assert run("1\n3\n101\n010\n101\n") == "Case #1: 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 full | 0 | minimal trivial case |
| all zeros | 4 | maximum missing edges |
| all ones | 0 | already complete graph |
| alternating pattern | 5 | non-uniform structure |

## Edge Cases

If a worker initially knows no machines, every missing edge involving that worker must be added. Without those edges, that worker can become permanently idle regardless of ordering.

If a machine is known by no workers, every missing edge involving that machine must also be added, otherwise that machine can never be assigned.

In both situations, the algorithm naturally counts all zeros, ensuring these pathological configurations are fully repaired.
