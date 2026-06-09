---
title: "CF 1997D - Maximize the Root"
description: "We are given a rooted tree. Every vertex contains a non-negative number. An operation can be applied to any non-leaf vertex. When we choose a vertex $v$, we increase the value at $v$ by one and simultaneously decrease every other vertex in the subtree of $v$ by one."
date: "2026-06-08T14:37:34+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dfs-and-similar", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1997
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 168 (Rated for Div. 2)"
rating: 1500
weight: 1997
solve_time_s: 156
verified: true
draft: false
---

[CF 1997D - Maximize the Root](https://codeforces.com/problemset/problem/1997/D)

**Rating:** 1500  
**Tags:** binary search, dfs and similar, dp, greedy, trees  
**Solve time:** 2m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree. Every vertex contains a non-negative number.

An operation can be applied to any non-leaf vertex. When we choose a vertex $v$, we increase the value at $v$ by one and simultaneously decrease every other vertex in the subtree of $v$ by one. All values must remain non-negative after the operation.

The goal is to maximize the value at the root after performing any number of valid operations.

The tree contains up to $2 \cdot 10^5$ vertices across all test cases. Values can be as large as $10^9$. A solution that simulates operations directly is impossible because the number of operations may also be extremely large. Even a single vertex may be increased billions of times.

The constraint on total $n$ immediately suggests that we need something close to $O(n)$ or $O(n \log n)$ per test file. Any approach that repeatedly modifies subtrees or searches for operations would be far too slow.

The most dangerous part of the problem is that operations interact across different levels of the tree.

Consider:

```
1(0)
|
2(10)
|
3(0)
```

A naive idea is that vertex 2 can donate all ten units upward. That is false. Every operation on vertex 2 decreases vertex 3 as well. Since vertex 3 starts at zero, vertex 2 cannot perform even one operation.

The correct answer is 0, not 10.

Another subtle case is:

```
1(0)
|
2(5)
|
3(3)
```

Vertex 2 can perform at most three operations because vertex 3 is the bottleneck. After that, vertex 2 becomes 8 and vertex 3 becomes 0. Now vertex 2 can no longer operate.

A careless solution that only looks at sums inside subtrees would incorrectly conclude that all eight units can eventually reach the root.

A third important case is a leaf.

```
1(0)
|
2(7)
```

Since vertex 2 has no children, it cannot perform operations. The root can receive at most 7 units from vertex 2, and no transformations inside the subtree are possible. Leaves behave differently from internal vertices and must be treated separately.

## Approaches

The brute-force interpretation is straightforward. Repeatedly search for a valid operation, apply it, update all affected vertices, and continue until no operation can improve the root.

This is correct because it follows the definition exactly. Unfortunately it is hopelessly slow. A single operation may touch an entire subtree, costing $O(n)$. Worse, the number of operations may be as large as $10^9$. Even for tiny trees this becomes infeasible.

To obtain something faster, we need to stop thinking about individual operations and instead ask a feasibility question.

Suppose we want the root to end with value at least $X$.

Can we determine whether this is possible?

If we can answer that question efficiently, then the final answer can be found with binary search.

The key observation is that operations only move resources upward. Every subtree must be capable of supplying enough value to its parent. This suggests a bottom-up DFS.

Consider a node $v$ and suppose its parent requires some amount from it.

If $v$ is a leaf, the maximum amount it can provide is simply $a_v$.

For an internal node, things become more interesting.

Assume $v$ must end with at least $need$ units available for its parent.

If $a_v \ge need$, then $v$ already satisfies the requirement. Any extra value is harmless.

If $a_v < need$, then $v$ must somehow create $need-a_v$ additional units. The only way is to perform operations at $v$.

Each operation increases $v$ by 1 but consumes 1 unit from every child subtree. Thus creating $d$ extra units at $v$ requires every child subtree to provide at least $d$ units.

This leads to a very clean recurrence.

Let $req(v)$ denote the minimum value that every child must be able to supply.

If $a_v \ge req(v)$, children only need to satisfy $req(v)$.

If $a_v < req(v)$, the deficit is $req(v)-a_v$. Generating that deficit requires the children to cover both the final requirement and the consumed resources:

$$req(child)=req(v)+(req(v)-a_v)$$

$$=2 \cdot req(v)-a_v$$

The whole problem becomes a feasibility check propagated from the root down to the leaves.

The brute-force works because operations transfer resources upward. The recurrence works because it captures exactly how much resource a subtree must guarantee to support a target value at its parent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded, potentially billions of operations | O(n) | Too slow |
| Optimal | O(n log A) | O(n) | Accepted |

Here $A$ is the answer range, roughly up to $10^9$.

## Algorithm Walkthrough

### Feasibility Check

Suppose we want to know whether the root can reach value $X$.

The root initially contains $a_1$. The rest of the tree must provide

$$need = X-a_1$$

additional units.

If $need \le 0$, the target is already achieved.

Otherwise we recursively verify whether every subtree can support the required amount.

### Recursive Meaning

For a node $v$, define a DFS parameter $need$.

The meaning is:

> Subtree $v$ must be capable of delivering at least $need$ units to its parent.

### Internal Node Transition

1. If $v$ is a leaf, return whether $a_v \ge need$.
2. If $a_v \ge need$, then $v$ already contains enough value.

Every child only needs to satisfy the same requirement $need$.
3. If $a_v < need$, let

$$d = need-a_v$$

be the deficit.

Node $v$ must generate $d$ additional units through operations at $v$.
4. Each such unit costs one unit from every child subtree.

Consequently each child must provide

$$need+d =2\cdot need-a_v$$

units.
5. Recursively verify every child with that new requirement.

### Binary Search

1. Let the search range be $[a_1, 10^{18}]$.
2. For a midpoint $mid$, run the feasibility DFS.
3. If feasible, move the lower bound upward.
4. Otherwise move the upper bound downward.
5. The largest feasible value is the answer.

### Why it works

The DFS invariant is:

> When a node is checked with parameter $need$, the recursion determines whether that subtree can guarantee at least $need$ units at the node itself after any necessary internal operations.

For a leaf this is immediate because no operations are available.

For an internal node, if its own value already meets the requirement, children do not need to compensate. If it falls short by $d$, exactly $d$ operations at that node are necessary. Every such operation consumes one unit from every child subtree, so each child must support an additional $d$ units. The recurrence is both necessary and sufficient.

Since the feasibility predicate is monotone, if a value $X$ is achievable then every smaller value is also achievable. Binary search is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        children = [[] for _ in range(n)]

        parents = list(map(int, input().split()))
        for v in range(1, n):
            p = parents[v - 1] - 1
            children[p].append(v)

        def feasible(target):
            need_root = target - a[0]
            if need_root <= 0:
                return True

            INF = 10**18

            def dfs(v, need):
                if need > INF:
                    return False

                if not children[v]:
                    return a[v] >= need

                if a[v] >= need:
                    child_need = need
                else:
                    child_need = 2 * need - a[v]
                    if child_need > INF:
                        return False

                for to in children[v]:
                    if not dfs(to, child_need):
                        return False

                return True

            for to in children[0]:
                if not dfs(to, need_root):
                    return False

            return True

        lo = a[0]
        hi = 10**18

        while lo < hi:
            mid = (lo + hi + 1) // 2

            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        print(lo)

solve()
```

The tree is stored as a children adjacency list because every DFS traversal proceeds from parent to child.

The function `feasible(target)` checks whether the root can be raised to `target`. The quantity `need_root` is exactly the amount that must arrive from the root's children.

The DFS implements the recurrence derived above. Leaves are the base case. Internal nodes either already satisfy the requirement or must compensate for a deficit by consuming resources from all child subtrees.

The overflow guard using `INF` is important. Along a long chain the recurrence may repeatedly double the required value. The real answer never exceeds the chosen binary-search range, so any requirement above `10^18` can safely be treated as impossible.

The binary search uses the standard upper-midpoint formula `(lo + hi + 1) // 2` to avoid infinite loops.

## Worked Examples

### Sample 1

Input:

```
4
0 1 0 2
1 1 3
```

Tree:

```
    1(0)
   /   \
 2(1)  3(0)
          \
           4(2)
```

Check whether root can become 1.

| Node | Required | Value | Child Requirement |
| --- | --- | --- | --- |
| 2 | 1 | 1 | leaf |
| 3 | 1 | 0 | 2 |
| 4 | 2 | 2 | leaf |

All checks succeed.

Check whether root can become 2.

| Node | Required | Value | Child Requirement |
| --- | --- | --- | --- |
| 2 | 2 | 1 | fail |

The target fails immediately.

Answer = 1.

This trace shows how deficits propagate downward. Node 3 lacks one unit, so its child must satisfy a larger requirement.

### Sample 3

Input:

```
5
2 5 3 9 6
3 1 5 2
```

Tree:

```
      1(2)
     /
   3(3)
   /
 5(6)
 /
2(5)
/
4(9)
```

Check target 6.

Root needs 4 additional units.

| Node | Required | Value | Child Requirement |
| --- | --- | --- | --- |
| 3 | 4 | 3 | 5 |
| 5 | 5 | 6 | 5 |
| 2 | 5 | 5 | 5 |
| 4 | 5 | 9 | leaf |

Success.

Check target 7.

Root needs 5 additional units.

| Node | Required | Value | Child Requirement |
| --- | --- | --- | --- |
| 3 | 5 | 3 | 7 |
| 5 | 7 | 6 | 8 |
| 2 | 8 | 5 | 11 |
| 4 | 11 | 9 | fail |

Answer = 6.

This example demonstrates repeated deficit amplification along a chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each feasibility check visits every node once, binary search performs O(log A) checks |
| Space | O(n) | Tree storage plus recursion stack |

The total number of vertices across all test cases is at most $2 \cdot 10^5$. With roughly 60 binary-search iterations for a $10^{18}$ range, the solution performs about $1.2 \times 10^7$ node visits in the worst case, which fits comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 20)

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        children = [[] for _ in range(n)]

        p = list(map(int, input().split()))
        for v in range(1, n):
            children[p[v - 1] - 1].append(v)

        def feasible(target):
            need = target - a[0]
            if need <= 0:
                return True

            def dfs(v, req):
                if not children[v]:
                    return a[v] >= req

                child_req = req if a[v] >= req else 2 * req - a[v]

                for to in children[v]:
                    if not dfs(to, child_req):
                        return False
                return True

            return all(dfs(to, need) for to in children[0])

        lo, hi = a[0], 10**18

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        out.append(str(lo))

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""3
4
0 1 0 2
1 1 3
2
3 0
1
5
2 5 3 9 6
3 1 5 2
"""
) == "1\n3\n6\n"

# minimum tree
assert run(
"""1
2
0 5
1
"""
) == "5\n"

# root already large
assert run(
"""1
2
10 0
1
"""
) == "10\n"

# chain blocked by zero leaf
assert run(
"""1
3
0 10 0
1 2
"""
) == "0\n"

# all equal values
assert run(
"""1
3
5 5 5
1 1
"""
) == "10\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two-node tree with values 0 and 5 | 5 | Smallest nontrivial tree |
| Root already largest | 10 | Binary search lower bound |
| Chain 0,10,0 | 0 | Deep bottleneck effect |
| Three nodes all equal to 5 | 10 | Symmetric subtree behavior |

## Edge Cases

### Deep bottleneck leaf

Input:

```
1
3
0 10 0
1 2
```

Tree:

```
1(0)
|
2(10)
|
3(0)
```

To make the root equal to 1, node 2 must provide one unit. Since node 2 already has enough value, the DFS asks node 3 for one unit as well. Node 3 is a leaf with value 0, so the check fails.

The algorithm outputs 0. This matches the real process because every operation at node 2 would decrease node 3 below zero.

### Internal node deficit amplification

Input:

```
1
3
0 1 10
1 2
```

Tree:

```
1(0)
|
2(1)
|
3(10)
```

Trying to make the root equal to 6 requires node 2 to provide 6 units.

Node 2 only contains 1 unit, so the deficit is 5.

The child requirement becomes:

$$2 \cdot 6 - 1 = 11$$

Leaf 3 only has 10 units, so the target fails.

The recurrence correctly captures the fact that generating extra value at node 2 consumes resources from node 3.

### Leaf child of the root

Input:

```
1
2
0 7
1
```

The root can only receive resources already present at vertex 2. Since vertex 2 is a leaf, it cannot create additional value through operations.

The DFS simply checks whether the leaf has enough value. The maximum root value becomes $0 + 7 = 7$, which is exactly the correct answer.
