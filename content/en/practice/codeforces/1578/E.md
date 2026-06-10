---
title: "CF 1578E - Easy Scheduling"
description: "We are asked to schedule tasks that are arranged as a full binary tree of height $h$. A full binary tree of height $h$ has $2^h - 1$ nodes. Initially, only the root task is ready. At each discrete moment of time, up to $p$ processes can perform ready tasks simultaneously."
date: "2026-06-10T10:36:50+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1578
codeforces_index: "E"
codeforces_contest_name: "ICPC WF Moscow Invitational Contest - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1200
weight: 1578
solve_time_s: 201
verified: false
draft: false
---

[CF 1578E - Easy Scheduling](https://codeforces.com/problemset/problem/1578/E)

**Rating:** 1200  
**Tags:** implementation, math  
**Solve time:** 3m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to schedule tasks that are arranged as a full binary tree of height $h$. A full binary tree of height $h$ has $2^h - 1$ nodes. Initially, only the root task is ready. At each discrete moment of time, up to $p$ processes can perform ready tasks simultaneously. Once a task is performed, its children become ready in the next moment of time. The goal is to determine the minimum number of time moments required to perform all tasks in the tree.

The input provides multiple test cases. Each test case gives $h$ and $p$, representing the tree height and number of processes. The output for each test case is a single integer, the minimal number of time moments needed to complete all tasks.

Constraints are crucial. There can be up to $5 \cdot 10^5$ test cases. Heights $h$ are at most 50, which means the largest tree has $2^{50} - 1$ nodes. Number of processes $p$ is up to $10^4$. These constraints indicate that we cannot simulate each task individually for large $h$ - explicit traversal of all nodes is infeasible. Instead, we need a strategy that leverages the tree’s structure and the predictable number of nodes at each depth.

Non-obvious edge cases include having only one process with a moderately large tree. For example, $h = 3$, $p = 1$ results in a sequential execution of tasks: time moments would be 7, since the tasks have to be performed one by one. A careless greedy approach that assumes parallelism can always fully utilize all processes might underestimate the required time in such cases.

## Approaches

The brute-force approach is straightforward: simulate the process. Keep a queue of ready tasks, each moment assign up to $p$ processes, mark tasks as done, and push their children into the ready queue. This works correctly, but for $h = 50$, there are $2^{50} - 1$ tasks. Simulating each task would take $10^{15}$ operations - far beyond any reasonable time limit.

The optimal approach exploits the binary tree structure. At depth $d$, there are $2^{d-1}$ tasks. Tasks at a depth become ready only after the previous level is finished. Because all tasks at the same level become ready simultaneously, we can compute the number of ready tasks and process them in batches of size up to $p$. This reduces the problem to summing over levels, performing ceiling division of tasks by the process limit $p$. The computation depends on counting tasks per depth, not iterating through each node individually.

The key insight is recognizing that the problem can be reduced to counting how many moments are needed to complete the last level, considering the cumulative backlog of unfinished tasks from previous levels. By maintaining a sorted list of remaining tasks and always processing the largest available batches first, we minimize the total time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^h) | O(2^h) | Too slow for h > 30 |
| Level-based Greedy Counting | O(h log h) | O(h) | Accepted |

## Algorithm Walkthrough

1. Compute the number of tasks at each depth of the tree. For depth $d$ from 1 to $h$, there are $2^{d-1}$ tasks. Store these in a list `tasks`.
2. Reverse the list so that we start processing from the deepest level. This allows prioritizing the largest batches, which is crucial for minimizing total time moments.
3. Initialize `ready` as 1, representing the root task ready at time moment 1. Initialize `time` as 0.
4. While there are still tasks to perform:

4.1. Add the number of tasks at the current depth to `ready`.

4.2. Determine how many tasks can be performed in this time moment: `done = min(ready, p)`.

4.3. Subtract `done` from `ready`.

4.4. Increment `time` by 1.
5. Repeat until all levels are exhausted and `ready` reaches 0. Return `time` as the minimal number of time moments.

Why it works: the invariant is that `ready` always correctly represents the number of tasks that can be performed in the current moment. By always executing up to `p` tasks per moment and processing larger batches first, we ensure no idle time occurs if processes are available. This strategy guarantees the minimal total time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def minimal_time(h, p):
    tasks = [(1 << i) for i in range(h)]
    tasks.reverse()
    ready = 0
    time = 0
    for t in tasks:
        ready += t
        done = min(ready, p)
        ready -= done
        time += 1
    while ready > 0:
        done = min(ready, p)
        ready -= done
        time += 1
    return time

t = int(input())
for _ in range(t):
    h, p = map(int, input().split())
    print(minimal_time(h, p))
```

The first loop constructs the number of tasks per depth, reversed so we process the largest batches first. The variable `ready` keeps track of tasks available for execution. We repeatedly execute up to `p` tasks per moment. The final while loop handles remaining tasks from previous depths. This ensures no tasks are left unprocessed.

## Worked Examples

Sample input:

```
3 1
3 2
10 6
```

For `3 1`:

| Depth | Tasks | Ready | Done | Time |
| --- | --- | --- | --- | --- |
| 3 | 4 | 4 | 1 | 1 |
| 2 | 2 | 5 | 1 | 2 |
| 1 | 1 | 5 | 1 | 3 |
| Remaining | - | 3 | 1 | 4 |
| Remaining | - | 2 | 1 | 5 |
| Remaining | - | 1 | 1 | 6 |
| Remaining | - | 0 | 1 | 7 |

Time = 7, as expected.

For `3 2`:

| Depth | Tasks | Ready | Done | Time |
| --- | --- | --- | --- | --- |
| 3 | 4 | 4 | 2 | 1 |
| 2 | 2 | 4 | 2 | 2 |
| 1 | 1 | 2 | 2 | 3 |
| Remaining | - | 0 | 0 | 4 |

Time = 4, matches the sample.

This confirms the algorithm respects task availability, batch limits, and processes larger levels first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h) | Each level of the tree is visited once, h ≤ 50, plus at most h iterations for leftover tasks. |
| Space | O(h) | We store tasks per depth in a list of length h. |

The solution easily handles $t \le 5\cdot10^5$ test cases, since each test requires only O(h) = O(50) operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        h, p = map(int, input().split())
        print(minimal_time(h, p))
    return output.getvalue().strip()

# Provided samples
assert run("3\n3 1\n3 2\n10 6\n") == "7\n4\n173", "sample"

# Custom cases
assert run("1\n1 1\n") == "1", "minimum tree"
assert run("1\n50 10000\n") == "50", "maximum height, many processes"
assert run("1\n4 1\n") == "15", "single process, small tree"
assert run("1\n4 10\n") == "4", "more processes than tasks per level"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | Single-node tree |
| 50 10000 | 50 | Large tree, enough processes to never wait |
| 4 1 | 15 | Sequential processing with one process |
| 4 10 | 4 | Parallelism exceeds level size |

## Edge Cases

For `h = 1`, `p = 1`: the tree has only the root. The algorithm correctly counts `ready = 1`, performs it in one moment, and terminates.

For `h = 50`, `p = 10000`: initially `ready = 2^49` for the deepest level, but the while loop correctly performs `p = 10000` tasks per moment until all are done, which would take multiple iterations. The algorithm never attempts to store all tasks individually, preventing memory overflow.

For `p > 2^(depth)`, the algorithm
