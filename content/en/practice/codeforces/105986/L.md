---
title: "CF 105986L - \u7b49\u4ef7\u4ea4\u6362"
description: "We are given a system of items, where each item can eventually become “energized” if it is either directly chosen at the start or can be produced through recipes."
date: "2026-06-22T16:35:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105986
codeforces_index: "L"
codeforces_contest_name: "2025 Wuhan University of Technology Programming Contest"
rating: 0
weight: 105986
solve_time_s: 62
verified: true
draft: false
---

[CF 105986L - \u7b49\u4ef7\u4ea4\u6362](https://codeforces.com/problemset/problem/105986/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system of items, where each item can eventually become “energized” if it is either directly chosen at the start or can be produced through recipes. Each recipe takes several input items and produces one output item, with the rule that the output becomes energized only when all its inputs are already energized.

Initially, no item is energized. We are allowed to manually energize some items. Once that is done, we repeatedly apply all recipes whose inputs are fully energized, and those outputs also become energized. The process continues until no more items can be activated.

The twist is that we do not actually know the structure of the recipes. We only know that there are n items and m recipes, and we must assume the best possible arrangement of recipes to minimize how many items we initially energize. The goal is to compute this minimum possible number.

The constraint n up to 2×10^5 and m up to n implies we need a linear or near-linear solution. Anything quadratic in n would immediately fail because even 10^10 operations is far beyond the time limit.

A subtle edge case appears when m is zero. With no recipes, nothing can ever be produced, so every item must be manually energized, giving answer n. Another edge case is when recipes are abundant enough to potentially connect everything into a single derivation chain, in which case the answer should drop to 1.

The key difficulty is understanding how much “merging power” m recipes can provide under optimal design.

## Approaches

We start from the most pessimistic viewpoint: if there were no recipes, every item is isolated. The only way to energize everything is to manually choose all n items, so the answer is n.

Now consider what a recipe actually does in the best possible scenario. If we design recipes freely, we would always prefer them to be as simple as possible in terms of prerequisites. A recipe with multiple inputs is actually harder to satisfy because it requires all of them to already be active. In contrast, a recipe with a single input behaves like a directed edge from one item to another: once the first is active, the second becomes active immediately.

This observation is the key simplification. In an optimal construction, every recipe can be treated as a directed edge from one item to another. The problem reduces to choosing m directed edges over n nodes to minimize how many starting nodes are needed so that all nodes become reachable under reachability along directed edges.

Now the structure becomes familiar. We are trying to minimize the number of sources needed to cover all nodes in a directed forest-like structure. Each directed edge can reduce the number of independent starting components by at most one, because it can connect a previously independent node into an existing reachable chain.

So if we start from n isolated nodes, every recipe can reduce the number of required starting points by one in the best case. After using m such reductions, the number of required starting points becomes n - m. If m is large enough to go below 1, we still need at least one starting node, because some node must be initially energized.

This leads directly to the formula max(1, n - m).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force construction simulation | O(2^n) | O(n) | Too slow |
| Optimal edge-reduction reasoning | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read n and m from input. These describe how many items exist and how many recipes we are allowed to optimally design.
2. If there are no recipes, return n. With no transformations available, each item must be initially energized.
3. Otherwise, interpret each recipe in its most effective form as a single directed dependency between two items. This is the configuration that maximizes propagation efficiency.
4. Start with the idea that each item initially forms its own independent requirement, so there are n required starting points.
5. Each recipe can merge exactly one previously independent item into a reachable structure, reducing the number of required starting points by one. After using all m recipes optimally, the count becomes n - m.
6. If this value drops below 1, clamp it to 1 because at least one initial energized item is necessary to trigger any propagation.

### Why it works

The process can be viewed as gradually reducing the number of independent “activation sources” needed to cover the graph. Every recipe, when optimally designed as a single prerequisite rule, can attach one previously unreachable component into an existing reachable structure. Since recipes cannot create activation from nothing, they can only propagate existing energy, not eliminate the need for a starting point entirely. This means the total number of independent starting components decreases by at most one per recipe, and this bound is achievable by constructing a chain-like dependency structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    ans = n - m
    if ans < 1:
        ans = 1
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution relies on the fact that we never need to explicitly construct the recipe graph. The answer depends only on how many independent reductions m can achieve relative to the initial n isolated items. The subtraction captures how many items can be absorbed into dependency chains, and the final clamp ensures we do not remove the need for a starting seed entirely.

A common mistake would be trying to simulate recipes or build an actual graph, which is unnecessary and would introduce overhead without changing the final combinatorial structure.

## Worked Examples

### Example 1

Input:

```
3 2
```

We start with 3 isolated items.

| Step | Independent components | Remaining recipes used | Current answer |
| --- | --- | --- | --- |
| Initial | 3 | 2 | 3 |
| After 1 recipe | 2 | 1 | 2 |
| After 2 recipes | 1 | 0 | 1 |

Final answer is 1.

This shows that two optimal dependencies are enough to collapse three isolated items into a single activation chain.

### Example 2

Input:

```
5 1
```

| Step | Independent components | Remaining recipes used | Current answer |
| --- | --- | --- | --- |
| Initial | 5 | 1 | 5 |
| After 1 recipe | 4 | 0 | 4 |

Final answer is 4.

This demonstrates that a single recipe can only reduce the need for one initial energized item.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic on n and m |
| Space | O(1) | No auxiliary structures needed |

The constraints allow this direct computation easily, since even the maximum input size only requires constant-time processing per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    ans = n - m
    if ans < 1:
        ans = 1
    return str(ans)

# provided sample
assert run("3 2\n") == "1"

# minimum case
assert run("1 0\n") == "1"

# no recipes, many items
assert run("5 0\n") == "5"

# enough recipes to fully connect
assert run("6 10\n") == "1"

# exact boundary
assert run("5 4\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 | minimum size boundary |
| 5 0 | 5 | no recipe case |
| 6 10 | 1 | clamp behavior when m ≥ n |
| 5 4 | 1 | exact saturation case |

## Edge Cases

When n is 1, there is only one item and it must be energized regardless of m. The formula gives max(1, 1 - m), which always evaluates to 1, matching the requirement.

When m is zero, no propagation is possible and every item must be initially chosen. The formula gives max(1, n), which correctly returns n for any n ≥ 1.

When m is very large relative to n, the subtraction n - m becomes negative, but the clamp ensures the answer never drops below one, reflecting the fact that at least one starting item is always necessary to initiate any chain of derivations.
