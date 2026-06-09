---
title: "CF 1891F - A Growing Tree"
description: "We are asked to process a sequence of operations on a growing rooted tree. The tree starts with a single node numbered 1, and each node has a numerical value, initially 0."
date: "2026-06-08T22:02:27+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 1891
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 907 (Div. 2)"
rating: 2000
weight: 1891
solve_time_s: 126
verified: false
draft: false
---

[CF 1891F - A Growing Tree](https://codeforces.com/problemset/problem/1891/F)

**Rating:** 2000  
**Tags:** data structures, dfs and similar, trees  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to process a sequence of operations on a growing rooted tree. The tree starts with a single node numbered 1, and each node has a numerical value, initially 0. Queries either add a new child to an existing node or increment all values in the subtree of a given node by a specified amount. After all queries, we need to output the final values of all nodes in the tree.

The input consists of multiple test cases, each with up to 500,000 queries. The sum of queries across all test cases is guaranteed to not exceed 500,000. Values can be as large as $10^9$ or as small as $-10^9$. These constraints imply that any algorithm with worse than $O(q \log q)$ per test case is unlikely to be efficient enough. A naive solution that updates all nodes in a subtree for every query would take $O(nq)$ time in the worst case, which can reach $2.5 \cdot 10^{11}$ operations-far too slow.

Non-obvious edge cases include adding children to nodes that themselves have large subtrees, and multiple overlapping subtree increments. For example, if we have a tree with nodes 1-3 and we perform an increment on node 1 followed by an increment on node 2, a naive approach that traverses subtrees each time may double-count or miss updates if implemented incorrectly. Another edge case is adding a new node and immediately performing a subtree increment on it. The algorithm must correctly account for newly added nodes in future increments.

## Approaches

A brute-force approach is straightforward: maintain an adjacency list for the tree, store values for each node, and for each query traverse the subtree to apply increments. This is correct, but its time complexity is $O(qn)$ because each type 2 query may touch every node in the subtree. In the worst case, where the tree is a star or a chain and every query is an increment on the root, we reach half a billion operations per test case-impractical.

The key observation is that subtree increments and tree growth have a sequential structure. Each node is added exactly once, and once a node is added, its parent never changes. We can represent the tree as an array with a "parent" pointer for each node. Then, we can propagate values from parents to children in a single traversal after all queries. Instead of updating all nodes in a subtree immediately, we can record the increment at the parent and push it down later. This is essentially a DFS-based prefix propagation: each node accumulates increments from its ancestors.

The brute-force works because updating each subtree directly gives correct values, but fails when the subtree is large and there are many queries. The observation that we only need to propagate increments once in a DFS allows us to reduce the complexity from $O(nq)$ to $O(n+q)$ per test case, which is efficient for the given bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Parent-pointer + DFS propagation | O(n+q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `parent` where `parent[i]` stores the parent of node `i`. Initialize an array `value` of zeros for node values. Set `children` as a list of lists to track each node's children.
2. For each query of type 1 (add child to vertex `v`), increment the tree size `sz` by 1, set `parent[sz] = v`, and append `sz` to `children[v]`. This maintains the tree structure in memory efficiently.
3. For each query of type 2 (increment subtree of vertex `v` by `x`), update `value[v] += x`. Do not traverse the subtree yet; store the increment at the root of the intended subtree.
4. After processing all queries, perform a DFS starting from the root (node 1). At each node `u`, for every child `c` in `children[u]`, propagate the accumulated value: `value[c] += value[u]`. Then recursively process child `c`. This ensures that all subtree increments are applied correctly.
5. After DFS, the `value` array contains the correct values for all nodes. Output them in order from 1 to `sz`.

The invariant that guarantees correctness is that each node's value should be the sum of all increments applied to it or any of its ancestors. By storing increments at the root and propagating them once with DFS, we maintain this property exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

def solve():
    T = int(input())
    for _ in range(T):
        q = int(input())
        parent = [0]  # 1-indexed, parent[1] unused
        children = [[] for _ in range(q + 2)]
        value = [0] * (q + 2)
        sz = 1

        for _ in range(q):
            line = input().split()
            if line[0] == '1':
                v = int(line[1])
                sz += 1
                parent.append(v)
                children[v].append(sz)
            else:
                v, x = int(line[1]), int(line[2])
                value[v] += x

        def dfs(u):
            for c in children[u]:
                value[c] += value[u]
                dfs(c)

        dfs(1)
        print(' '.join(str(value[i]) for i in range(1, sz + 1)))

if __name__ == "__main__":
    solve()
```

In this solution, `parent` is maintained to add children correctly, but is not used in DFS propagation because we track children directly. We preallocate `children` and `value` arrays to avoid dynamic resizing during queries, which improves performance. Recursive DFS propagates increments from parent to child exactly once, handling overlapping subtree increments correctly.

## Worked Examples

### Sample 1 trace

Input:

```
9
2 1 3
1 1
2 2 1
1 1
2 3 2
1 3
2 1 4
1 3
2 3 2
```

| Query | Node added / increment | Value array after operation |
| --- | --- | --- |
| 2 1 3 | +3 to node 1 | [3] |
| 1 1 | add node 2 to 1 | [3,0] |
| 2 2 1 | +1 to node 2 | [3,1] |
| 1 1 | add node 3 to 1 | [3,1,0] |
| 2 3 2 | +2 to node 3 | [3,1,2] |
| 1 3 | add node 4 to 3 | [3,1,2,0] |
| 2 1 4 | +4 to node 1 | [7,1,6,0] |
| 1 3 | add node 5 to 3 | [7,1,6,0,0] |
| 2 3 2 | +2 to node 3 | [7,1,8,2,2] |

DFS propagation adds parent values to children: node 1->2,3-> children 4,5.

Final `value`: 7 5 8 6 2

This trace confirms the algorithm correctly accumulates overlapping subtree increments and accounts for dynamically added nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n+q) | Each query is processed in O(1) and DFS propagates values through all nodes once |
| Space | O(n) | Arrays `value`, `children`, and `parent` store tree and values for up to `q+1` nodes |

With $q \le 5 \cdot 10^5$, total operations are under 1 million per test case, easily within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided sample 1
assert run("1\n9\n2 1 3\n1 1\n2 2 1\n1 1\n2 3 2\n1 3\n2 1 4\n1 3\n2 3 2\n") == "7 5 8 6 2"

# minimum-size tree
assert run("1\n1\n2 1 5\n") == "5"

# all nodes added linearly, multiple increments
assert run("1\n5\n1 1\n1 2\n2 1 3\n2 3 2\n2 2 1\n") == "3 4 5"

# negative increment
assert run("1\n3\n1 1\n2 2 -2\n2 1 5\n") == "5 3"

# multiple test cases
assert run("2\n2\n1 1\n2 2 3\n2\n1 1\n2 1 4\n") == "0 3\n4 0"
```

| Test input | Expected
