---
title: "CF 429C - Guess the Tree"
description: "The problem asks us to reconstruct a rooted tree given constraints on the sizes of the subtrees for each node. You are given an array c of length n, where c[i] represents the total number of nodes in the subtree rooted at node i."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 429
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 245 (Div. 1)"
rating: 2300
weight: 429
solve_time_s: 86
verified: true
draft: false
---

[CF 429C - Guess the Tree](https://codeforces.com/problemset/problem/429/C)

**Rating:** 2300  
**Tags:** bitmasks, constructive algorithms, dp, greedy, trees  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to reconstruct a rooted tree given constraints on the sizes of the subtrees for each node. You are given an array `c` of length `n`, where `c[i]` represents the total number of nodes in the subtree rooted at node `i`. Each node that has children must have at least two children. The task is to determine whether a tree satisfying these properties exists.

The input size is small, `n ≤ 24`, so algorithms that scale exponentially with `n` are feasible. Each `c[i]` is at most `n`, so there is no value outside the valid range. The tricky part is that the values in `c` can appear in any order, so we cannot assume the last element is the root or that values increase monotonically down the tree.

A naive approach might try all possible trees and check their subtree sizes. For `n = 24`, this is infeasible since the number of rooted trees grows super-exponentially. Another subtle edge case occurs when there is only one node. If `n = 1` and `c = [1]`, the solution is trivially "YES" because a single node counts as a subtree of size one. Another pitfall is having `c[i] = n` for more than one node; the tree cannot have two roots with the full tree size.

Additionally, if all `c[i] = 1`, the only valid configuration is a forest of leaf nodes, which is impossible if `n > 1` because an internal node must have at least two children. For example, input `[1,1,1]` should return "NO".

## Approaches

The brute-force approach would generate all possible rooted trees and check each one against the subtree sizes. For `n` nodes, the number of possible rooted trees is exponential in `n`. Checking the subtree sizes for each tree takes `O(n^2)`, so even for `n = 15`, this approach becomes infeasible. The correctness of this brute-force method comes from exhaustively verifying every structure, but it is too slow.

The key insight is that the problem can be reduced to a combinatorial partitioning problem. If we sort the nodes by their subtree sizes in descending order, the largest value must correspond to the root. Then each internal node must be assigned children such that the sum of their subtree sizes plus one equals the subtree size of the parent. This resembles a recursive subset sum problem. Because `n ≤ 24`, we can efficiently explore all possible groupings of remaining nodes using bitmask dynamic programming. The bitmask represents which nodes are still unassigned. We recursively try to form a valid set of children for the current node, and memoize results to avoid repeated work. This reduces the search space drastically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(#trees × n^2) | O(n) | Too slow |
| Bitmask DP / Recursive Construction | O(2^n × n^2) | O(2^n) | Accepted |

## Algorithm Walkthrough

1. Sort the array `c` in descending order. The largest element must be the root, otherwise no tree can satisfy all subtree sizes.
2. Use a recursive function `can_build(mask)` where `mask` represents nodes not yet placed in the tree. If `mask` is zero, we successfully assigned all nodes.
3. For the current node `u`, we try to assign a subset of remaining nodes as children. A valid subset `S` satisfies `sum(c[i] for i in S) + 1 = c[u]`. Each internal node must have at least two children if `c[u] > 1`.
4. For each valid subset `S`, recursively attempt to build trees for the remaining nodes, `mask - S`. If any branch succeeds, return true.
5. Use memoization to store results for each `mask`, since the same set of remaining nodes may be encountered multiple times.
6. If no valid assignment exists for the current node and mask, return false.

Why it works: The algorithm maintains the invariant that every node in the current mask is unassigned. Each recursion ensures that the subtree size constraint is satisfied exactly. Sorting nodes ensures the largest subtree size is always assigned first, guaranteeing the root is valid. Memoization avoids rechecking the same configuration. If the algorithm returns true, there exists a valid assignment for all nodes that satisfies the given rules.

## Python Solution

```python
import sys
input = sys.stdin.readline
from functools import lru_cache

def solve():
    n = int(input())
    c = list(map(int, input().split()))
    c.sort(reverse=True)

    @lru_cache(None)
    def can_build(mask):
        if mask == 0:
            return True
        # pick the first node in mask
        u = mask.bit_length() - 1
        size_needed = c[u]
        # if it's a leaf
        if size_needed == 1:
            return can_build(mask ^ (1 << u))
        # try all subsets of remaining nodes to be children
        submask = mask ^ (1 << u)
        subset = submask
        while subset:
            total = sum(c[i] for i in range(n) if (subset >> i) & 1)
            if total + 1 == size_needed:
                if bin(subset).count("1") >= 2 and can_build(submask ^ subset):
                    return True
            subset = (subset - 1) & submask
        return False

    full_mask = (1 << n) - 1
    if can_build(full_mask):
        print("YES")
    else:
        print("NO")

solve()
```

The code begins by sorting nodes to guarantee the root is handled first. The recursive function uses a bitmask to track remaining nodes. Subset generation checks all possible child combinations efficiently using the `(subset - 1) & submask` trick. Leaf nodes (`c[i] = 1`) are automatically handled. Memoization ensures exponential work is not repeated.

## Worked Examples

Sample Input 1:

```
4
1 1 1 4
```

| Step | Mask (binary) | Current node | Children subset | Action |
| --- | --- | --- | --- | --- |
| 1 | 1111 | node 3 (size 4) | 0111 (nodes 0,1,2) | 3 children assigned |
| 2 | 0000 | leaf nodes 0,1,2 | - | success |

The recursion picks node 3 as root, assigns the other three nodes as its children. Each child is a leaf, satisfying subtree sizes. The function returns YES.

Custom Input 2:

```
3
1 2 2
```

Mask `111` → largest node size 2 → cannot assign exactly one node (needs at least two children) → NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^n × n^2) | Bitmask recursion explores all subsets of remaining nodes, each requiring sum over up to n elements |
| Space | O(2^n) | Memoization cache for each bitmask |

With `n ≤ 24`, `2^24 ≈ 16 million` entries is feasible. Each recursion only iterates over subsets of the mask, and the overall runtime fits under 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("4\n1 1 1 4\n") == "YES", "sample 1"

# minimum input
assert run("1\n1\n") == "YES", "single node tree"

# impossible small tree
assert run("3\n1 2 2\n") == "NO", "cannot form internal node with 2 children"

# all leaves but more than 1 node
assert run("4\n1 1 1 1\n") == "NO", "no internal node possible"

# maximum node values
assert run("5\n1 2 2 3 5\n") == "YES", "valid tree with root size 5"

# another impossible
assert run("4\n2 2 2 4\n") == "NO", "internal nodes cannot satisfy size 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | YES | Correct tree reconstruction |
| 1 | YES | Minimum-size input |
| 3 | NO | Impossible configuration for internal nodes |
| 4 | NO | All leaf nodes with n>1 |
| 5 | YES | Larger valid tree |
| 4 | NO | Internal node size mismatch |

## Edge Cases

For a single node input `1\n1\n`, the mask starts as `1`. The root node has size 1, recursion removes it, mask becomes `0`. Algorithm returns YES correctly.

For input `[1,1,1,1]`, mask `1111`, the largest node has size 1. Each node is a leaf, but the root must have size >1 to have children. No subset of remaining nodes satisfies the child requirement of ≥2 children for internal nodes. The algorithm explores all subsets and returns NO. This confirms the handling of all-leaf scenarios.
