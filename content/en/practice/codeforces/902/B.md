---
title: "CF 902B - Coloring a Tree"
description: "We are given a rooted tree with n vertices. The root is vertex 1, and every other vertex i has a parent pi, forming the tree structure. Each vertex has a target color c[i], and we begin with all vertices uncolored (color 0)."
date: "2026-06-12T10:51:56+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "greedy"]
categories: ["algorithms"]
codeforces_contest: 902
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 453 (Div. 2)"
rating: 1200
weight: 902
solve_time_s: 355
verified: false
draft: false
---

[CF 902B - Coloring a Tree](https://codeforces.com/problemset/problem/902/B)

**Rating:** 1200  
**Tags:** dfs and similar, dsu, greedy  
**Solve time:** 5m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with `n` vertices. The root is vertex 1, and every other vertex `i` has a parent `p_i`, forming the tree structure. Each vertex has a target color `c[i]`, and we begin with all vertices uncolored (color 0). We can perform a coloring operation where we choose a vertex `v` and a color `x`, and paint the entire subtree of `v` (including `v` itself) with color `x`. Our goal is to reach the target coloring using as few such operations as possible.

The input specifies the tree structure with a parent array of size `n-1` and the target color array of size `n`. The output is a single integer: the minimum number of coloring operations required.

The constraints are modest: `n` ≤ 10⁴. This allows algorithms with linear or near-linear time complexity. Any approach that is quadratic in `n` will be too slow, as it could require up to 10⁸ operations.

Non-obvious edge cases include situations where multiple children of the same parent have the same target color as the parent, which can sometimes be colored in a single operation if approached correctly, and cases where the root has the same target color as its child, requiring careful handling to avoid unnecessary operations.

For example, if `n = 2` and the root and its child both need color 1, we only need one operation coloring the root. A naive algorithm might color the root first and then unnecessarily color the child again.

## Approaches

The brute-force approach would try every possible subtree coloring at every vertex until the tree matches the target. This is correct but impractical because each coloring can affect many vertices, leading to potentially O(n²) operations in the worst case.

The key observation is that a subtree operation only changes colors along the path from the vertex to its descendants. Therefore, if a vertex already has the same color as its parent, we do not need a separate coloring operation. Conversely, whenever a vertex's target color differs from its parent, we must perform a coloring operation at that vertex. This is because any subtree coloring operation performed at the parent would have already given the vertex the parent's color.

This reduces the problem to a simple traversal: count 1 operation for the root (since its initial color is 0 and always differs from any target) and count 1 operation for each vertex whose target color differs from its parent. This gives the minimum number of operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse input to read `n`, the parent array `p`, and the target color array `c`.
2. Construct the tree as an adjacency list. For each `i` from 2 to `n`, append `i` to `p[i]`'s children.
3. Initialize a counter `steps` to 0. This will store the number of coloring operations.
4. Start a DFS traversal at the root (vertex 1). Pass along the parent's color in the traversal.
5. For the current vertex `v`, compare its target color `c[v]` with the parent's color.

- If `c[v] != parent_color`, increment `steps` by 1. This represents performing a coloring operation at `v`.
6. Recursively traverse all children of `v`, passing `c[v]` as the new parent color.
7. After the traversal, print `steps`.

Why it works: the invariant is that any vertex with the same color as its parent does not require a separate operation, because any subtree coloring at the parent already covers it. Counting only vertices whose color differs from the parent's guarantees the minimum number of operations, including the root, which is always counted because it initially differs from color 0.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(20000)

def main():
    n = int(input())
    p_list = list(map(int, input().split()))
    c_list = list(map(int, input().split()))
    
    # Build tree adjacency list
    tree = [[] for _ in range(n)]
    for i, parent in enumerate(p_list):
        tree[parent - 1].append(i + 1)
    
    steps = 0

    def dfs(node, parent_color):
        nonlocal steps
        if c_list[node] != parent_color:
            steps += 1
        for child in tree[node]:
            dfs(child, c_list[node])
    
    dfs(0, 0)  # root has parent color 0
    print(steps)

if __name__ == "__main__":
    main()
```

The solution reads the tree and target colors. The adjacency list construction offsets indices because the input uses 1-based indexing while Python lists are 0-based. The DFS passes down the parent's color so that we can decide if the current node requires a coloring operation. The recursion limit is increased to handle deep trees up to 10⁴ nodes.

## Worked Examples

**Sample 1:**

Input:

```
6
1 2 2 1 5
2 1 1 1 1 1
```

Trace table:

| Node | Parent color | Target color | Step increment |
| --- | --- | --- | --- |
| 1 | 0 | 2 | +1 |
| 2 | 2 | 1 | +1 |
| 3 | 1 | 1 | 0 |
| 4 | 1 | 1 | 0 |
| 5 | 2 | 1 | +1 |
| 6 | 1 | 1 | 0 |

Total steps: 3. Matches expected output.

**Sample 2:**

Input:

```
7
1 1 2 3 6 6
3 1 1 1 2 1 3
```

Steps calculated similarly, giving total steps = 5.

This demonstrates the invariant: operations are only performed where the color differs from the parent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited exactly once in DFS |
| Space | O(n) | Adjacency list + recursion stack |

With `n ≤ 10⁴`, a linear traversal easily fits within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided samples
assert run("6\n1 2 2 1 5\n2 1 1 1 1 1\n") == "3"
assert run("7\n1 1 2 3 6 6\n3 1 1 1 2 1 3\n") == "5"

# custom cases
assert run("2\n1\n1 1\n") == "1", "two nodes same color"
assert run("3\n1 1\n1 2 3\n") == "3", "each node different"
assert run("5\n1 1 2 2\n1 1 1 1 1\n") == "1", "all same color"
assert run("4\n1 1 1\n2 2 2 2\n") == "1", "root different color, others same"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes, same color | 1 | Root operation suffices, no extra operation |
| 3 nodes, all different | 3 | Each node must be colored separately |
| 5 nodes, all same color | 1 | One operation at root colors all |
| 4 nodes, root differs | 1 | Coloring root covers all children automatically |

## Edge Cases

When the root and its child have the same target color, the algorithm correctly counts only one operation at the root. For a deep linear tree where colors alternate between parent and child, each vertex will increment the step count, which is necessary. For a balanced tree with large uniform subtrees, only nodes whose color differs from the parent trigger operations, avoiding redundant recoloring. The algorithm handles all these cases due to the invariant: color only when the parent color differs.
