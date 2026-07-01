---
title: "CF 104344I - Fila da cantina"
description: "We are given a row of children, where each position already contains a child, but each child has a target position they are supposed to occupy."
date: "2026-07-01T18:29:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104344
codeforces_index: "I"
codeforces_contest_name: "Maratona dos Bixes 2023 - UNICAMP"
rating: 0
weight: 104344
solve_time_s: 61
verified: true
draft: false
---

[CF 104344I - Fila da cantina](https://codeforces.com/problemset/problem/104344/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of children, where each position already contains a child, but each child has a target position they are supposed to occupy. The input array describes this mapping: the child currently sitting at index `i` wants to end up at position `p[i]` after everything is sorted correctly.

The goal is to transform the current arrangement into a perfectly ordered one, where the child that should be in position `1` is there, the child that should be in position `2` is there, and so on until position `N`. The only allowed operation is swapping any two children in the row. We want the minimum number of swaps needed to reach the correct configuration.

This is a classic “rearrange a permutation using swaps” problem. The key observation is that the array is effectively a permutation of `1..N`, because every correct position is uniquely assigned.

The constraints are small enough that a solution with quadratic behavior in `N` would still pass in practice. With `N ≤ 1000`, even an algorithm doing on the order of `N^2` or `N^2 log N` operations is acceptable. This immediately rules out anything exponential or involving repeated deep recomputation per operation.

A naive but common mistake is to try simulating swaps greedily without a consistent structure. For example, repeatedly scanning for the next incorrect position and swapping it into place can work but becomes error-prone if one forgets that swaps can create new misplacements elsewhere. Another incorrect idea is to always swap a wrong element with the element currently in its target position without tracking where that element actually is, which breaks if positions are not indexed carefully.

Edge cases that tend to break naive solutions include already sorted arrays such as `[1,2,3,4]`, where the answer is zero, and pure cycles like `[2,3,1]`, where every element is misplaced but structured in a single cycle. A careless greedy swap may overcount or undercount swaps depending on how cycles are broken.

The deeper structure here is that the array defines a permutation, and permutations decompose into disjoint cycles. The minimum swaps needed is determined entirely by the cycle structure.

## Approaches

A brute-force approach would repeatedly fix the first incorrect position by finding the element that belongs there and swapping it into place. Each swap reduces the number of misplaced elements locally, but requires repeated searching. In the worst case, each placement requires scanning the array to locate the correct element, leading to an $O(N)$ scan repeated $O(N)$ times, giving $O(N^2)$ time. This is acceptable for $N ≤ 1000$, but the method is conceptually messy and easy to implement incorrectly when swaps affect future searches.

The key insight is to stop thinking in terms of individual swaps and instead view the array as a permutation graph. Each index points to the position where its current value should go. This creates directed edges from `i → p[i]`. Every node belongs to exactly one cycle. A cycle of length `k` requires exactly `k - 1` swaps to fix, because each swap can place one element correctly while preserving structure within the cycle.

Summing this over all cycles gives the minimum number of swaps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (repeated fixing) | O(N²) | O(N) | Accepted but clumsy |
| Cycle Decomposition | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Interpret the array as a permutation where position `i` must eventually contain value `i`.

This reframing allows us to reason about correctness in terms of indices rather than arbitrary swaps.
2. Build a visited array to track which indices have already been assigned to a cycle.

Without this, we would repeatedly reprocess the same structure and overcount swaps.
3. Iterate over each index from `1` to `N`.

If the index is already visited, it belongs to a previously processed cycle, so we skip it.
4. When we find an unvisited index, start following the chain `i → p[i] → p[p[i]] → ...` until we return to a visited node.

This traversal discovers a full cycle of the permutation.
5. Count the size `k` of this cycle.

Each cycle represents a closed dependency loop of misplaced elements.
6. Add `k - 1` to the answer.

This is the minimum number of swaps required to break a cycle into correctly placed fixed points.
7. Continue until all indices are visited and sum all contributions.

### Why it works

Every permutation can be uniquely decomposed into disjoint cycles. Inside a cycle of length `k`, no element can reach its correct position without interacting with the others in the same cycle. A single swap can correctly place at most one element from the cycle while preserving a smaller cycle structure among the remaining elements. Repeating this optimally yields exactly `k - 1` swaps, and summing over independent cycles ensures no interference between them.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    
    # convert to 0-based target interpretation
    p = [x - 1 for x in p]
    
    visited = [False] * n
    ans = 0
    
    for i in range(n):
        if visited[i]:
            continue
        
        # explore cycle starting at i
        cur = i
        cycle_size = 0
        
        while not visited[cur]:
            visited[cur] = True
            cycle_size += 1
            cur = p[cur]
        
        if cycle_size > 0:
            ans += cycle_size - 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first converts the permutation into zero-based indexing so that positions align naturally with array indices. The visited array ensures each index is processed exactly once, preventing double counting cycles. Each cycle traversal follows the permutation mapping until it loops back, and the cycle size directly determines the number of swaps added.

The subtraction `cycle_size - 1` is the critical transformation from structure to cost.

## Worked Examples

### Sample 1

Input:

```
4
2 1 4 3
```

| Step | Start | Cycle traversal | Cycle size | Added swaps | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 → 1 → 0 | 2 | 1 | 1 |
| 2 | 2 | 2 → 3 → 2 | 2 | 1 | 2 |

The permutation splits into two independent cycles of size 2. Each contributes exactly one swap, matching the intuition that each pair just needs a single swap to fix.

### Sample 2

Input:

```
4
1 2 3 4
```

| Step | Start | Cycle traversal | Cycle size | Added swaps | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 0 | 0 |
| 2 | 1 | 1 | 1 | 0 | 0 |
| 3 | 2 | 2 | 1 | 0 | 0 |
| 4 | 3 | 3 | 1 | 0 | 0 |

Every element is already in a fixed point cycle of size 1, so no swaps are needed.

These examples confirm that the algorithm correctly distinguishes between fixed points and non-trivial cycles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each index is visited exactly once while forming cycles |
| Space | O(N) | Visited array and input storage |

With `N ≤ 1000`, the algorithm runs well within limits. Even in the worst case of a single cycle of size `N`, the traversal is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    import builtins
    backup = builtins.input
    builtins.input = lambda: sys.stdin.readline().rstrip("\n")
    
    try:
        solve()
    finally:
        builtins.input = backup
    
    return output.getvalue().strip()

# provided samples
assert run("4\n2 1 4 3\n") == "2", "sample 1"
assert run("4\n1 2 3 4\n") == "0", "sample 2"
assert run("3\n2 3 1\n") == "2", "sample 3"

# custom cases
assert run("1\n1\n") == "0", "single element"
assert run("5\n2 3 4 5 1\n") == "4", "single large cycle"
assert run("6\n1 3 2 5 6 4\n") == "3", "multiple cycles"
assert run("4\n4 3 2 1\n") == "2", "reverse order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | smallest case |
| `5-cycle shift` | `4` | full cycle handling |
| `6 mixed cycles` | `3` | multiple disjoint cycles |
| `reverse` | `2` | symmetric cycle decomposition |

## Edge Cases

For already sorted input like `1 2 3 4`, the traversal immediately marks each index as a cycle of size 1. No swaps are accumulated, and the output remains zero.

For a full cycle like `2 3 4 1`, the algorithm follows `0 → 1 → 2 → 3 → 0`, producing cycle size 4 and contributing `3` swaps. This matches the minimal sequence where each swap progressively fixes one element while shrinking the remaining cycle.

For multiple independent cycles such as `2 1 4 3 5`, the visited mechanism ensures each cycle is isolated. The algorithm processes `(0,1)` and `(2,3)` separately, each contributing one swap, while the fixed point `4` contributes none.
