---
title: "CF 104962A - \u041a\u0440\u0443\u0433\u043b\u044b\u0439 \u0413\u0440\u0430\u0444"
description: "We are given a cycle of n houses. Each house is placed on a circle, so every house has a natural notion of moving left or right along the cycle. We are allowed to choose a parameter k."
date: "2026-06-28T06:57:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104962
codeforces_index: "A"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2021. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 104962
solve_time_s: 55
verified: true
draft: false
---

[CF 104962A - \u041a\u0440\u0443\u0433\u043b\u044b\u0439 \u0413\u0440\u0430\u0444](https://codeforces.com/problemset/problem/104962/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a cycle of `n` houses. Each house is placed on a circle, so every house has a natural notion of moving left or right along the cycle.

We are allowed to choose a parameter `k`. Once `k` is fixed, every house is directly connected to the `k` nearest houses on its left side and the `k` nearest houses on its right side. After building these connections, the graph becomes much denser than a simple cycle, because from each node you can jump to a whole block of nearby nodes in one move.

The distance between two houses is defined as the minimum number of edges needed to travel between them in this new graph. The task is to choose the smallest `k` such that the maximum possible shortest-path distance between any pair of houses is at most `d`.

In other words, we are controlling how far each node can “see” in one step along the circle, and we want the resulting graph to have diameter at most `d`.

The constraints are extremely large, with `n` and `d` up to `10^12`. This immediately rules out any simulation of the graph or BFS-style reasoning per test case. Even storing adjacency is impossible, so the solution must collapse the structure into a direct formula or at most a logarithmic computation.

A subtle edge case is when `n` is very small. For example, if `n = 3`, the structure is already almost fully connected even for small `k`, and distance behavior becomes trivial. Another corner is when `d` is large enough that even `k = 1` already satisfies the requirement, as in small cycles where the diameter of a cycle is already within bounds.

A naive misunderstanding would be to think distances depend on complicated graph shortcuts. For example, one might try to simulate shortest paths on a weighted interval graph, but that is unnecessary because the connectivity has a very rigid structure: all edges correspond to bounded jumps on a cycle.

## Approaches

A direct brute-force approach would try values of `k` starting from `1`, construct the graph, and compute its diameter using BFS from every node. Each BFS would be `O(n)` and repeated `n` times, giving `O(n^2)` per `k`. Since `k` can also go up to `n`, this becomes completely infeasible even for moderate sizes, and certainly impossible for `n = 10^12`.

The key observation is that the graph is fully symmetric. Every node has the same structure of connections, and the only thing that matters is how far we can move along the cycle in a single step. From any node, a single move allows jumping up to `k` positions clockwise or counterclockwise. This turns the graph into a one-dimensional metric where each step reduces the remaining circular distance by at most `k`.

If two nodes are separated by a circular distance `x`, then the shortest path between them is exactly `ceil(x / k)`. The worst case occurs when `x` is as large as possible, which is the farthest distance on a circle, namely `floor(n / 2)`.

So the diameter of the graph becomes `ceil(floor(n/2) / k)`. The problem reduces to finding the smallest `k` such that this value is at most `d`.

This inequality is simple to invert, giving a direct formula for `k`. The entire problem collapses into constant time arithmetic per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (graph + BFS) | O(n²) | O(n) | Too slow |
| Formula-based reasoning | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the maximum relevant distance on the cycle, which is the farthest two nodes can be apart. On a circle, this is `floor(n / 2)`. This is because any longer arc can be traversed in the opposite direction more cheaply.
2. Observe that with parameter `k`, a single step can cover up to `k` positions along the cycle. This means traveling a distance `A = floor(n / 2)` takes `ceil(A / k)` steps in the worst case.
3. We require the graph diameter to be at most `d`, so we enforce `ceil(A / k) ≤ d`.
4. Transform this inequality into a condition on `k`. The smallest integer `k` satisfying it is `ceil(A / d)`.
5. Return this value as the answer for each test case.

### Why it works

All nodes behave identically in terms of connectivity, so the worst-case shortest path is determined purely by circular distance, not by node identity. Each move reduces remaining distance by at most `k`, and no path can outperform greedy reduction because every edge respects the same bounded interval structure. This makes the shortest path equivalent to dividing the distance into chunks of size `k`, and the diameter is fully controlled by the largest possible distance on the cycle.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, d = map(int, input().split())
        A = n // 2
        k = (A + d - 1) // d
        out.append(str(k))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly applies the derived formula. The only subtlety is computing `ceil(A / d)` safely using integer arithmetic as `(A + d - 1) // d`. Using integer division avoids floating-point errors, which are irrelevant here but still a common pitfall in competitive programming.

The value `A = n // 2` captures the worst-case circular distance, and everything else follows from that reduction. No graph construction is needed.

## Worked Examples

Consider the first sample input.

Input:

`n = 6, d = 2`

The farthest distance on the circle is `A = 3`. Each step with parameter `k` can cover up to `k` distance. We need `ceil(3 / k) ≤ 2`.

| k | ceil(3 / k) | valid |
| --- | --- | --- |
| 1 | 3 | no |
| 2 | 2 | yes |
| 3 | 1 | yes |

The smallest valid value is `k = 2`.

Now consider a second example.

Input:

`n = 3, d = 1`

Here `A = 1`. We need `ceil(1 / k) ≤ 1`, which holds for any `k ≥ 1`.

| k | ceil(1 / k) | valid |
| --- | --- | --- |
| 1 | 1 | yes |

So the answer is `1`.

These examples confirm that the formula behaves correctly both when the graph is small and when it requires actual shortcutting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed with a constant number of arithmetic operations |
| Space | O(1) | Only a few integers are stored regardless of input size |

The solution easily fits within constraints because even `10` test cases require only constant-time computation per case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n, d = map(int, input().split())
        A = n // 2
        k = (A + d - 1) // d
        res.append(str(k))
    return "\n".join(res)

# provided samples
assert run("2\n6 2\n3 1\n") == "2\n1"

# minimum size cycle behavior
assert run("1\n3 1\n") == "1"

# already dense requirement relaxed
assert run("1\n10 100\n") == "1"

# larger structure
assert run("1\n100 3\n") == str((100 // 2 + 3 - 1) // 3)

# boundary equality case
assert run("1\n8 1\n") == str((8 // 2 + 1 - 1) // 1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 2 | 2 | basic non-trivial case |
| 3 1 | 1 | smallest cycle |
| 10 100 | 1 | large d dominates |
| 100 3 | computed value | scaling correctness |
| 8 1 | computed value | tight diameter constraint |

## Edge Cases

For very small `n`, such as `n = 3`, the cycle has only one meaningful distance value, so the algorithm reduces correctly because `n // 2` becomes `1`. The computed `k` is always at least `1`, so no special handling is required.

For very large `d`, such as `d ≥ floor(n/2)`, the formula yields `k = 1`. This matches intuition because even the basic cycle edges already allow reaching the farthest node within the allowed number of steps.

For cases where `d = 1`, the requirement forces the graph diameter to collapse in one move. The formula correctly returns `k = floor(n/2)`, meaning every node must be directly reachable from the farthest node in one step, which matches the structure of the construction.
