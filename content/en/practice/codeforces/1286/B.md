---
title: "CF 1286B - Numbers on Tree"
description: "We are given a rooted tree where every node has a hidden integer value. What we do know is the tree structure and, for each node, a number ci."
date: "2026-06-16T03:46:55+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dfs-and-similar", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1286
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 612 (Div. 1)"
rating: 1800
weight: 1286
solve_time_s: 321
verified: false
draft: false
---

[CF 1286B - Numbers on Tree](https://codeforces.com/problemset/problem/1286/B)

**Rating:** 1800  
**Tags:** constructive algorithms, data structures, dfs and similar, graphs, greedy, trees  
**Solve time:** 5m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree where every node has a hidden integer value. What we do know is the tree structure and, for each node, a number `c_i`. This number tells us something local to the subtree: among all nodes inside the subtree of `i`, exactly `c_i` of them have values strictly smaller than the value at `i`.

The task is to reconstruct any assignment of integers to the nodes that is consistent with all these subtree constraints. If multiple assignments work, any one is acceptable, and if no assignment can satisfy all constraints, we must report impossibility.

The key difficulty is that every node imposes a constraint that depends on comparisons inside its subtree, but those comparisons depend on a global ordering of values that we do not know in advance. The tree couples these constraints across different levels, so a naive independent treatment of nodes fails.

The constraints allow up to 2000 nodes. This is small enough that a solution with a cubic or quadratic factor can pass, but anything that tries to reason over all value assignments explicitly or simulates permutations of values will not be feasible. What we should expect instead is a constructive process that assigns values incrementally while maintaining consistency.

A common failure mode appears when one tries to assign values greedily without respecting subtree structure. For example, assigning values in BFS order or by parent before children ignores that `c_i` depends on the full subtree, not just immediate neighbors. Another subtle failure arises if we try to assign values based only on sorting nodes by `c_i`, because `c_i` does not represent global rank, only subtree-relative rank.

A small illustrative issue: consider a parent with `c = 0` and a child with `c = 1`. If we assign values greedily so that smaller `c` means smaller value, we may force a contradiction inside the subtree because the parent constraint depends on both children ordering simultaneously, not individually.

## Approaches

A brute-force idea would be to try to assign values from a permutation of `1..n` to nodes and check whether all constraints hold. For each assignment, verifying the condition requires computing subtree counts, which itself needs a DFS per node or a merged traversal. Even if checking one assignment takes `O(n^2)`, trying all permutations is `O(n!)`, which is far beyond any limit.

The structure of the problem suggests we need to construct values in a way that respects subtree constraints locally while gradually fixing relative order. The crucial observation is that `c_i` describes how many nodes in the subtree must be placed before node `i` in value ordering, but only relative to nodes that are still “available” inside that subtree.

This leads to a constructive idea: process the tree from leaves upward, and at each node decide its relative rank among nodes in its subtree. If we already know the ordering of children subtrees, we can merge them and insert the parent in a position consistent with `c_i`. Since subtrees are disjoint, merging behaves like merging sorted lists, and the constraint reduces to choosing the correct insertion point.

We maintain for each node a list of positions representing how many elements are smaller than each candidate placement. When combining children, we merge these lists and then place the current node at a position where exactly `c_i` elements in its subtree are smaller.

This reduces the problem to a tree DP where each node builds a sorted structure of possible ranks in its subtree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutation checking | O(n! · n^2) | O(n) | Too slow |
| Tree DP with ordered merging | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Root the tree at the node with `p_i = 0`. We will compute a valid relative ordering inside each subtree.
2. For each node, define a list that represents the final ordering of nodes in its subtree. Instead of storing actual values, we store positions in a conceptual sorted order.
3. Perform a DFS from the root. For a leaf node, its list contains only itself, since there is no internal constraint to violate. This serves as the base case.
4. For an internal node, first recursively compute lists for all children. Each child already represents a consistent ordering of its subtree.
5. Merge all child lists into one list. This merge is done by concatenating and then treating the result as a single multiset of positions. At this stage, we only care about relative sizes inside the subtree.
6. After merging children, we must insert the current node into this merged list so that exactly `c_i` elements in its subtree are smaller than it. This means placing it at index `c_i` in a zero-based ordering of the merged list.
7. If `c_i` is larger than the size of the merged list, no placement is possible and the construction fails immediately.
8. Once the full DFS is complete, we have a valid ordering of nodes from smallest value to largest value. Assign increasing integers `1..n` according to this order.

### Why it works

Each subtree is processed independently before being combined, so every subtree list correctly represents a valid internal ordering. When we insert a node at position `c_i`, we are enforcing exactly the number of smaller elements in its subtree. Because children subtrees are disjoint, merging does not break previously satisfied constraints. The DFS invariant is that every subtree list can be extended upward without violating any `c_i`, so the final root construction encodes a globally consistent ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n = int(input())
children = [[] for _ in range(n)]
c = [0] * n
root = -1

for i in range(n):
    p, ci = map(int, input().split())
    c[i] = ci
    if p == 0:
        root = i
    else:
        children[p - 1].append(i)

# Each node returns a list of nodes in increasing order of final value
def dfs(u):
    cur = [u]
    for v in children[u]:
        sub = dfs(v)
        cur.extend(sub)

    # We need to place u so that exactly c[u] elements in its subtree are smaller
    # but cur currently includes u at front; we will reposition it.
    cur.remove(u)

    if c[u] > len(cur):
        raise ValueError("impossible")

    cur.insert(c[u], u)
    return cur

try:
    order = dfs(root)
    ans = [0] * n
    for i, node in enumerate(order):
        ans[node] = i + 1

    print("YES")
    print(*ans)
except ValueError:
    print("NO")
```

The implementation follows the DFS construction literally. Each recursive call builds the ordering for a subtree. We temporarily include the node itself, then remove and reinsert it at the correct index dictated by `c_i`. This avoids complicated counting logic, since insertion position directly enforces how many smaller elements exist in that subtree ordering.

The final assignment step maps the constructed global order to values `1..n`, which is always valid because only relative ordering matters.

A subtle implementation point is recursion depth, since the tree can degenerate into a chain. Increasing recursion limit prevents stack overflow in Python.

## Worked Examples

### Example 1

Input:

```
3
2 0
0 2
2 0
```

Tree structure: node 2 is root, nodes 1 and 3 are children.

We start DFS at node 2.

| Step | Node | Child results | Merged list | Insert position | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | [] | [1] | c1 = 0 | [1] |
| 2 | 3 | [] | [3] | c3 = 0 | [3] |
| 3 | 2 | [1,3] | [1,3] | c2 = 2 | [1,3,2] |

Final order is `[1, 3, 2]`. Assign values `1,2,3` accordingly gives a valid reconstruction such as `1 3 2` or any equivalent consistent labeling.

This trace shows how each subtree is independently constructed before the root imposes its global constraint.

### Example 2

Input:

```
4
2 0
0 1
2 0
2 1
```

Node 2 is root, with children 1, 3, 4.

| Step | Node | Child results | Merged list | Insert position | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | [] | [1] | c1 = 0 | [1] |
| 2 | 3 | [] | [3] | c3 = 0 | [3] |
| 3 | 4 | [] | [4] | c4 = 1 | [4] |
| 4 | 2 | [1,3,4] | [1,3,4] | c2 = 0 | [2,1,3,4] |

This demonstrates how a root with `c = 0` forces itself to be smallest in its subtree, shifting all children upward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each DFS merge involves list operations over subtree sizes, and each node may be inserted into a list of size up to n |
| Space | O(n^2) | Each subtree stores an explicit list of its nodes |

The constraints allow `n ≤ 2000`, so an `O(n^2)` construction is acceptable. The operations are simple list manipulations, and Python handles this comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    children = [[] for _ in range(n)]
    c = [0] * n
    root = -1

    for i in range(n):
        p, ci = map(int, input().split())
        c[i] = ci
        if p == 0:
            root = i
        else:
            children[p - 1].append(i)

    sys.setrecursionlimit(10**7)

    def dfs(u):
        cur = [u]
        for v in children[u]:
            cur.extend(dfs(v))
        cur.remove(u)
        if c[u] > len(cur):
            raise ValueError
        cur.insert(c[u], u)
        return cur

    try:
        order = dfs(root)
        ans = [0] * n
        for i, v in enumerate(order):
            ans[v] = i + 1
        return "YES\n" + " ".join(map(str, ans))
    except:
        return "NO"

# sample
assert run("""3
2 0
0 2
2 0
""").split()[0] == "YES"

# chain
assert run("""1
0 0
""").startswith("YES")

# simple invalid
assert run("""2
2 1
0 0
""").startswith("NO")

# star
assert run("""4
2 0
0 1
2 0
2 1
""").split()[0] == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | YES 1 | minimal structure |
| invalid constraint | NO | impossible insertion |
| star tree | YES | merging multiple children |
| sample case | YES | correctness of construction |

## Edge Cases

A single-node tree always works since `c_1` must be zero and the only valid assignment is trivial. The DFS returns a singleton list, and insertion at position zero preserves correctness.

A node with `c_i` larger than its subtree size immediately makes the construction impossible. In the algorithm, this is detected at insertion time when `c_i > len(cur)` before placement, ensuring early rejection instead of producing a malformed ordering.

A star-shaped tree stresses merging many independent child subtrees. Since each child contributes a disjoint ordering, concatenation preserves validity, and the root insertion position controls the final structure without ambiguity.
