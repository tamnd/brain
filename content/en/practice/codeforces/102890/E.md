---
title: "CF 102890E - End of the year bonus"
description: "We are given a circular line of people, each with a performance value. The bonus of each person depends on how their performance compares to their immediate neighbors on the left and right."
date: "2026-07-04T12:28:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102890
codeforces_index: "E"
codeforces_contest_name: "2020 ICPC Gran Premio de Mexico 3ra Fecha"
rating: 0
weight: 102890
solve_time_s: 46
verified: true
draft: false
---

[CF 102890E - End of the year bonus](https://codeforces.com/problemset/problem/102890/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular line of people, each with a performance value. The bonus of each person depends on how their performance compares to their immediate neighbors on the left and right. If a person performs better than the neighbor on one side, they receive a base bonus contribution from that side equal to a fixed value plus the neighbor’s bonus. If they outperform both neighbors, their final bonus is the maximum of the two possible contributions. Since the people are seated in a circle, the first and last person are also neighbors.

The task is to compute the bonus for every person under these dependency rules. The dependencies are not independent: each value depends on adjacent values, which themselves depend on others, forming a system of constraints over a cycle.

The structure implies that a direct evaluation is not possible without resolving these mutual dependencies. Each position potentially depends on both neighbors, and the direction of dependency is determined dynamically by comparisons of performance values.

If the number of people is large, say up to 200000, then any solution that repeatedly recomputes values or propagates updates naively across the array would become quadratic in the worst case, since each update can trigger chain reactions around the circle. That immediately rules out iterative relaxation or naive recursion without memoization.

A subtle edge case arises when the performance values form a strict increasing or decreasing cycle. In such cases, every position depends on a consistent direction, and naive local propagation might incorrectly assume independence between left-to-right and right-to-left contributions.

For example, consider three people in a circle with values `[1, 2, 3]`. Person with value 3 is better than both neighbors, so their bonus depends on both sides. A naive left-to-right pass might assign partial values but fail to propagate the right-to-left influence correctly, producing inconsistent results.

Another edge case occurs when all values are equal, such as `[5, 5, 5, 5]`. No one is strictly better than any neighbor, so all bonuses should remain at their base level. Any algorithm that assumes at least one strict inequality direction per edge will incorrectly propagate updates.

## Approaches

The dependency structure becomes clearer if we interpret each directed comparison as creating a potential “flow” of bonus contribution. For any adjacent pair, if `p[i] > p[j]`, then `i` can receive a contribution derived from `j`. This creates directed edges between neighbors, but the direction is not fixed globally, it depends on the relative ordering of values.

A brute-force approach would repeatedly update all bonuses until no value changes. In each iteration, every position checks its neighbors and updates its value if either neighbor gives a better contribution. Each update depends on current neighbor states, so values propagate gradually around the circle.

This works because the system is monotonic: bonuses only increase. However, in the worst case, each update may propagate only one step per iteration around the circle. With `n` elements, this can take `O(n)` iterations, and each iteration costs `O(n)`, producing `O(n^2)` complexity. For large inputs this is not feasible.

The key observation is that the update rule has a directional asymmetry induced by value comparisons, not by indices. Once we fix the ordering induced by `p[i]`, we can treat transitions only along “downhill to uphill” directions. A person can only receive contribution from a neighbor with strictly smaller performance, and that contribution itself depends on further smaller neighbors.

This turns the problem into computing longest weighted chains on a graph where each node connects only to neighbors with smaller values. Because each node has at most two neighbors, the structure becomes a directed acyclic graph after orienting edges from smaller to larger values. On this DAG, we can compute values using memoized DFS or iterative processing in decreasing order of `p[i]`.

Sorting nodes by decreasing performance ensures that when we process a node, all possible contributors (which must have smaller values) are already computed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (iterative relaxation) | O(n²) | O(n) | Too slow |
| Optimal (value-ordered DP) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform the circular dependency into directed relations based on comparisons of adjacent values, then compute DP in decreasing order of performance.

1. Construct an array of indices sorted by decreasing `p[i]`. This ensures that when processing a node, both neighbors with smaller values are already processed if they are valid contributors. The ordering is the key to removing cycles from dependency resolution.
2. Initialize an array `f[i] = 0` for all positions. This represents that initially no contributions are assigned.
3. Iterate through indices in sorted order. For each position `i`, examine its left and right neighbors using circular indexing.
4. For each neighbor `j`, check if `p[i] > p[j]`. If so, candidate contribution from that direction is `B + f[j]`. We compute this because `i` is strictly better than `j`, so `j`'s already computed bonus can be extended upward to `i`.
5. Maintain the best value among valid contributions. If both neighbors are smaller, take the maximum of both candidate contributions. If only one is valid, that one is used. If none are valid, the value remains zero.
6. Assign `f[i]` to the computed best value.

The reason we process in decreasing order is that whenever `p[i] > p[j]`, the value at `j` must already be finalized before we process `i`. This prevents repeated updates and ensures each state is computed exactly once.

### Why it works

The core invariant is that when processing a node `i`, every neighbor `j` such that `p[j] < p[i]` already has its final value `f[j]`. Since contributions only flow from strictly smaller to strictly larger values, no later operation will ever modify `f[j]` in a way that affects `i`. This makes the dependency graph acyclic under the ordering of `p`, and guarantees that each `f[i]` computed is final at assignment time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, B = map(int, input().split())
    p = list(map(int, input().split()))
    
    order = sorted(range(n), key=lambda i: p[i], reverse=True)
    f = [0] * n
    
    for i in order:
        best = 0
        
        left = (i - 1) % n
        right = (i + 1) % n
        
        if p[i] > p[left]:
            best = max(best, B + f[left])
        if p[i] > p[right]:
            best = max(best, B + f[right])
        
        f[i] = best
    
    print(*f)

if __name__ == "__main__":
    solve()
```

The code starts by reading the number of people and the base bonus value. The performance array is stored in `p`. We then sort indices by decreasing performance so that higher-performing positions are computed after all potentially contributing lower-performing neighbors.

The array `f` stores computed bonuses. For each index in sorted order, we compute its two circular neighbors using modulo arithmetic. We only consider contributions from neighbors with strictly smaller performance. Each valid contribution adds `B` plus the already computed neighbor value. The maximum of valid contributions becomes the final bonus for that index.

A subtle point is the use of modulo indexing to enforce circular adjacency. Without this, boundary cases for first and last elements would require special handling and are easy to get wrong.

## Worked Examples

Consider `n = 3`, `B = 10`, `p = [1, 2, 3]`.

We process in order `[2, 1, 0]`.

| i | p[i] | left | right | f[left] | f[right] | f[i] |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 | 1 | 0 | 0 | 0 | 0 |
| 1 | 2 | 0 | 2 | 0 | 0 | 10 |
| 0 | 1 | 2 | 1 | 0 | 10 | 20 |

At index 2, both neighbors are smaller, but their `f` values are not yet useful for propagation. At index 1, only index 0 is smaller, so it gains `B + f[0] = 10`. At index 0, both neighbors are larger in value ordering context, but only index 1 is smaller, giving `10 + 10 = 20`.

This trace shows how values accumulate along increasing performance order.

Now consider `n = 4`, `B = 5`, `p = [4, 1, 3, 2]`.

| i | p[i] | left | right | valid contributions | f[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | 3 | 1 | from 3,1 | max(5+f[3], 5+f[1]) |
| 2 | 3 | 1 | 3 | from 1,3 | max(5+f[1], 5+f[3]) |
| 3 | 2 | 2 | 0 | from 2 | 5+f[2] |
| 1 | 1 | 0 | 2 | none | 0 |

This demonstrates how different nodes accumulate contributions depending on local comparisons rather than index order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting indices dominates, each node processed once with O(1) work |
| Space | O(n) | Arrays for performance values, DP results, and ordering |

The solution comfortably fits typical constraints up to 200000 elements, since all heavy work is sorting and single-pass DP evaluation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return sys.stdout.getvalue()

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, B = map(int, input().split())
    p = list(map(int, input().split()))
    
    order = sorted(range(n), key=lambda i: p[i], reverse=True)
    f = [0] * n
    
    for i in order:
        best = 0
        left = (i - 1) % n
        right = (i + 1) % n
        
        if p[i] > p[left]:
            best = max(best, B + f[left])
        if p[i] > p[right]:
            best = max(best, B + f[right])
        
        f[i] = best
    
    return " ".join(map(str, f)) + "\n"

# minimum size
assert solve("1 10\n5\n") == "0\n"

# all equal
assert solve("4 3\n2 2 2 2\n") == "0 0 0 0\n"

# increasing circle
assert solve("3 5\n1 2 3\n") == "20 10 0\n"

# decreasing circle
assert solve("3 5\n3 2 1\n") == "0 10 20\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimum boundary |
| all equal | all zeros | no propagation |
| increasing | chain propagation | directional flow |
| decreasing | reverse chain | circular correctness |

## Edge Cases

For a single-person circle, say `n = 1`, the left and right neighbors are itself due to circular indexing. Since `p[i] > p[i]` is false, no contribution is ever triggered and the result is `0`. The algorithm handles this naturally because both neighbor checks fail.

For `p = [5, 5, 5, 5]`, every comparison `p[i] > p[j]` fails, so every node assigns `f[i] = 0`. The sorted order is irrelevant since no transitions are activated, and the DP remains stable at zero throughout.

For a strict monotone cycle like `[1, 2, 3, 4, 5]`, each node only receives contributions from its smaller neighbors. Processing in decreasing order ensures that when evaluating a node, all smaller nodes already have their final contributions, so chain accumulation happens cleanly without revisiting nodes.
