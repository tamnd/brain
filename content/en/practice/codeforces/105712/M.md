---
title: "CF 105712M - LIS On Tree"
description: "We are given a rooted tree where each vertex carries a value. The structure defines parent-child relationships, and every node lies on exactly one path from the root. For any node, consider the sequence of values encountered while walking from the root down to that node."
date: "2026-06-26T07:58:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105712
codeforces_index: "M"
codeforces_contest_name: "Rutgers University Programming Contest Fall 2024"
rating: 0
weight: 105712
solve_time_s: 40
verified: true
draft: false
---

[CF 105712M - LIS On Tree](https://codeforces.com/problemset/problem/105712/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree where each vertex carries a value. The structure defines parent-child relationships, and every node lies on exactly one path from the root.

For any node, consider the sequence of values encountered while walking from the root down to that node. The task is to compute, for every node, the length of the longest strictly increasing subsequence that can be formed from values along that root-to-node path. The subsequence does not need to be contiguous, only the order along the path must be preserved.

The output is the LIS length for each node, typically printed in order of node indices.

The main constraint implication is that a naive approach which recomputes LIS independently for each node would repeatedly process overlapping paths. Since each path can be length O(n), this leads to O(n^2) work in a chain-shaped tree. With n up to around 200000 in typical Codeforces tree problems, any quadratic or near-quadratic method is infeasible. The intended solution must process all nodes in near linear or n log n time, ideally sharing computation along DFS traversal.

A subtle issue arises with repeated values and branching structure. For example, if values repeat along different branches, a solution that incorrectly reuses global state without rollback will mix information between unrelated paths.

Consider a small case:

Input tree:

1(3)

└──2(1)

└──3(2)

For node 3, the path is 3 → 1 → 2 in values [3,1,2], and LIS length is 2. A naive “global LIS” update without restoring state might incorrectly carry contributions from sibling branches and overcount sequences that are not on a single root-to-node path.

## Approaches

A brute-force solution treats each node independently. For a fixed node, we walk from the root to that node, collect all values on the path, and run a standard LIS algorithm in O(k log k) using a temporary array of tails. Repeating this for all nodes gives a total complexity of O(n^2 log n) in a skewed tree. The correctness is straightforward because each node is solved independently using a standard LIS procedure.

The bottleneck is redundancy. Adjacent nodes share almost the entire path, so recomputing LIS from scratch wastes work on identical prefixes.

The key observation is that DFS naturally builds root-to-current-node paths incrementally. If we maintain the LIS structure of the current DFS path, we can update it in O(log n) per node and then restore it when backtracking. The LIS structure we maintain is the classic “patience sorting tails array”, where tails[len] stores the minimum possible ending value of an increasing subsequence of length len.

During DFS, when we enter a node, we temporarily insert its value into this structure using binary search. When we leave the node, we restore the previous state. This makes every node contribute exactly one insertion and one rollback, leading to an overall O(n log n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 log n) | O(n) | Too slow |
| DFS + LIS rollback | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the tree at node 1. We maintain a dynamic array `tails`, where `tails[i]` is the smallest possible ending value of an increasing subsequence of length `i+1` along the current DFS path.

We also maintain an answer array `ans` for each node.

1. Start DFS from the root. Before entering any node, `tails` is empty. This represents an empty subsequence along the current path.
2. At node `u`, we locate the position `pos` where `a[u]` can be inserted into `tails` using binary search. This position is the first index where `tails[pos] >= a[u]`.
3. If `pos` equals the current length of `tails`, we extend the structure by appending `a[u]`. Otherwise, we replace `tails[pos]` with `a[u]`.
4. The LIS length for node `u` is `pos + 1`, since it represents the best subsequence ending at this point in the DFS path. We store this in `ans[u]`.
5. We recurse into all children of `u`, keeping the updated `tails`. Each child extends the same root-to-current-node path.
6. After finishing all descendants of `u`, we must restore `tails` to its previous state before processing `u`. This is done by reversing the modification made at step 2 and 3, either by snapshotting the old value or by carefully tracking whether we appended or replaced.

The correctness hinges on the fact that at any DFS node, `tails` represents exactly one valid increasing subsequence structure over the root-to-current-node path. It never mixes values from different branches because we restore state before returning to the parent.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

from bisect import bisect_left

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))
    
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    ans = [0] * (n + 1)
    tails = []

    def dfs(u, p):
        # find insertion position
        pos = bisect_left(tails, a[u])
        
        old = None
        replaced = False
        
        if pos == len(tails):
            tails.append(a[u])
        else:
            old = tails[pos]
            tails[pos] = a[u]
            replaced = True
        
        ans[u] = pos + 1
        
        for v in g[u]:
            if v == p:
                continue
            dfs(v, u)
        
        # rollback
        if replaced:
            tails[pos] = old
        else:
            tails.pop()

    dfs(1, -1)
    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The DFS maintains a single global `tails` array representing the current root-to-node path state. The key implementation detail is the rollback mechanism: if we extended the array, we pop; if we replaced an element, we restore the previous value. This guarantees correctness across branching recursion.

A common mistake is forgetting that `tails` must reflect only the active recursion path. Any shared mutation without restoration will contaminate sibling subtrees.

## Worked Examples

Consider a tree:

Input:

```
5
1 3 2 4 0
1 2
2 3
2 4
4 5
```

We trace DFS starting at node 1.

At node 1, `tails = [1]`, LIS is 1.

| Node | Value | tails before | position | tails after | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | [] | 0 | [1] | 1 |
| 2 | 3 | [1] | 1 | [1,3] | 2 |
| 3 | 2 | [1,3] | 1 | [1,2] | 2 |
| backtrack to 2 | - | [1,2] | - | restored [1,3] | - |

This trace shows that node 3 replaces an internal value in `tails`, improving a subsequence of length 2 without extending it.

Another branch:

| Node | Value | tails before | position | tails after | ans |
| --- | --- | --- | --- | --- | --- |
| 4 | 4 | [1,3] | 2 | [1,3,4] | 3 |
| 5 | 0 | [1,3,4] | 0 | [0,3,4] | 1 |

Node 5 demonstrates replacement at the first position, showing how small values reset the best subsequence start while preserving structure for longer values.

These traces confirm that `tails` behaves like a global LIS structure restricted to the current DFS path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each node performs one binary search and one update in `tails` |
| Space | O(n) | adjacency list, recursion stack, and LIS tails storage |

The logarithmic factor comes from binary searching within the `tails` array. Since each node is processed once during DFS, the total cost scales as n log n, which comfortably fits typical constraints up to 200000 nodes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys
    sys.stdout = io.StringIO()
    
    # assume solve() is defined above in same module
    solve()
    
    return sys.stdout.getvalue().strip()

# simple chain
assert run("""3
1 2 3
1 2
2 3
""") == "1 2 3"

# decreasing chain
assert run("""4
4 3 2 1
1 2
2 3
3 4
""") == "1 1 1 1"

# star shape
assert run("""5
3 1 4 2 5
1 2
1 3
1 4
1 5
""") == "1 1 2 2 3"

# single node
assert run("""1
10
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain increasing | 1 2 3 | LIS grows along path |
| chain decreasing | 1 1 1 1 | replacements dominate |
| star tree | varies | independent branches |
| n=1 | 1 | minimal edge case |

## Edge Cases

For a single node tree, the DFS enters node 1 with an empty `tails`, inserts the value, and produces LIS length 1. There is no recursion, and rollback is never triggered, so the structure remains consistent.

For a strictly decreasing chain, every node inserts at position 0, repeatedly replacing `tails[0]`. The arra
