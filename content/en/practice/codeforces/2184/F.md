---
title: "CF 2184F - Cherry Tree"
description: "We have a rooted tree whose leaves each contain exactly one cherry. A shake performed at vertex v makes the cherries fall from every leaf inside the subtree of v. Once a cherry has fallen, it must never be affected by another shake."
date: "2026-06-07T21:40:27+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 2184
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1072 (Div. 3)"
rating: 1900
weight: 2184
solve_time_s: 224
verified: true
draft: false
---

[CF 2184F - Cherry Tree](https://codeforces.com/problemset/problem/2184/F)

**Rating:** 1900  
**Tags:** dfs and similar, dp, graphs, trees  
**Solve time:** 3m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree whose leaves each contain exactly one cherry.

A shake performed at vertex `v` makes the cherries fall from every leaf inside the subtree of `v`. Once a cherry has fallen, it must never be affected by another shake. If any leaf belongs to two different shakes, the process is invalid.

The goal is to collect every cherry and use a number of shakes that is divisible by three.

The tree contains up to `2·10^5` vertices across all test cases. Any algorithm that repeatedly scans subtrees or tries many combinations of vertices is immediately ruled out. With this input size, we need something close to linear time per test case.

The tricky part is understanding which sets of vertices can be shaken simultaneously.

Suppose we shake a vertex and also shake one of its descendants. Then every leaf in the descendant's subtree is affected twice, once by the ancestor and once by the descendant. That is forbidden.

As a result, the chosen vertices must form an antichain with respect to the ancestor relation. Every leaf must belong to exactly one chosen subtree.

A few edge cases are easy to misinterpret.

Consider a tree with only two leaves:

```
1
├─2
└─3
```

The only valid ways to cover all leaves are:

```
{1}      -> 1 shake
{2,3}    -> 2 shakes
```

Neither count is divisible by three, so the answer is `NO`.

Another important case is a single leaf subtree.

```
1
└─2
```

The leaf must be covered somehow. Either we shake vertex `1` or vertex `2`. We cannot leave the subtree uncovered and hope that some sibling contributes, because coverage is required for every leaf individually.

A third subtle case is when several child subtrees each have multiple valid shake counts. We are not interested in the exact count. Since only divisibility by three matters, keeping counts modulo three is enough. Missing this observation leads to an explosion in the number of states.

## Approaches

A brute-force approach would try every subset of vertices, check whether the chosen vertices form a valid cover of all leaves, and then test whether the number of chosen vertices is divisible by three.

This is correct but completely impractical. A tree with `n = 2·10^5` vertices has `2^n` subsets, which is far beyond anything that can be processed.

The structure of valid solutions gives a much better direction.

Focus on a single rooted subtree.

For a vertex `v`, there are only two possibilities.

Either we shake `v` itself. Then every leaf in its subtree is covered immediately, and no descendant may be shaken.

Or we do not shake `v`. Then every child subtree must independently cover all of its own leaves.

This naturally creates a tree DP.

Let `D[v]` be the set of possible shake counts modulo three that can cover all leaves inside the subtree of `v`.

For a leaf, the only possibility is shaking the leaf itself, giving count `1`.

For an internal vertex:

1. We may shake `v`, contributing count `1`.
2. We may skip `v`, in which case every child chooses one valid residue and the residues are added modulo three.

Since there are only three residues, each state contains at most three values. Combining children becomes a tiny modulo-three convolution.

The brute-force approach tracks exact subsets of vertices. The key observation is that only the count modulo three matters, and every subtree interacts with the rest of the tree only through that residue. This collapses an exponential search into a linear tree DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal DP on Tree | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex `1`.
2. Process vertices in postorder so that every child is computed before its parent.
3. For a leaf vertex, set

```
D[v] = {1}
```

The leaf must be shaken if no ancestor in the same DP state is chosen.
4. For an internal vertex, first compute the case where `v` is not shaken.

Start with residue `{0}`.
5. For every child, combine the current residue set with the child's residue set.

If residue `a` is already achievable and residue `b` is achievable in the child, then residue `(a + b) mod 3` becomes achievable after processing that child.
6. After all children are processed, the resulting set represents every residue achievable when `v` itself is not shaken.
7. Add the alternative where `v` is shaken.

Shaking `v` contributes exactly one shake, so residue `1` is always achievable.
8. Store

```
D[v] = D_not_choose ∪ {1}
```
9. After computing the root, check whether residue `0` belongs to `D[1]`.

If it does, some valid covering uses a number of shakes divisible by three, so print `"YES"`. Otherwise print `"NO"`.

### Why it works

For every subtree, `D[v]` contains exactly the residues of all valid ways to cover every leaf inside that subtree without using any ancestor of `v`.

The definition is complete because every valid solution for a subtree falls into exactly one of two categories: either `v` is chosen or it is not.

If `v` is chosen, the entire subtree is covered by a single shake. If `v` is not chosen, each child subtree must solve the same problem independently, and the total shake count is the sum of the child counts.

No valid solution is omitted, and no invalid solution is introduced. By induction on subtree size, every computed residue is achievable and every achievable residue is computed. Thus residue `0` at the root is equivalent to the existence of a valid global solution whose shake count is a multiple of three.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())

        g = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        parent = [-1] * n
        order = [0]
        parent[0] = 0

        for v in order:
            for to in g[v]:
                if parent[to] == -1:
                    parent[to] = v
                    order.append(to)

        dp = [0] * n

        for v in reversed(order):
            children = [to for to in g[v] if to != parent[v]]

            if not children:
                dp[v] = 1 << 1
                continue

            cur = 1 << 0

            for ch in children:
                nxt = 0
                child_mask = dp[ch]

                for r1 in range(3):
                    if not (cur & (1 << r1)):
                        continue

                    for r2 in range(3):
                        if child_mask & (1 << r2):
                            nxt |= 1 << ((r1 + r2) % 3)

                cur = nxt

            dp[v] = cur | (1 << 1)

        ans.append("YES" if (dp[0] & 1) else "NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The DFS is implemented iteratively to avoid Python recursion limits on deep trees.

Each DP state is stored as a three-bit mask. Bit `r` is set if residue `r` modulo three is achievable.

For example:

```
mask = 0b101
```

means residues `0` and `2` are possible.

The child combination step is a modulo-three convolution. Since there are only three residues, the work per child is constant.

The leaf case deserves attention. A leaf has no children, but its subtree still contains one cherry. The only valid local action is shaking the leaf, so its state is exactly `{1}`.

The root answer checks whether residue `0` is present. That corresponds to a total shake count divisible by three.

## Worked Examples

### Sample 1

Input:

```
4
1 2
1 3
1 4
```

The root has three leaf children.

| Vertex | Children residues | Not chosen residue | Final residues |
| --- | --- | --- | --- |
| 2 | - | - | {1} |
| 3 | - | - | {1} |
| 4 | - | - | {1} |
| 1 | {1},{1},{1} | {0} | {0,1} |

Residue `0` is achievable at the root, so the answer is `YES`.

This corresponds to shaking vertices `2`, `3`, and `4`, using exactly three shakes.

### Sample 2

Input:

```
3
1 2
1 3
```

| Vertex | Children residues | Not chosen residue | Final residues |
| --- | --- | --- | --- |
| 2 | - | - | {1} |
| 3 | - | - | {1} |
| 1 | {1},{1} | {2} | {1,2} |

Residue `0` does not appear.

The possible shake counts are `1` and `2`, neither divisible by three, so the answer is `NO`.

This example shows why merely counting leaves is insufficient. The root itself may be shaken, changing the count from `2` to `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each edge is processed a constant number of times, and each DP merge uses only 3×3 residue transitions |
| Space | O(n) | Adjacency list, parent array, traversal order, and DP masks |

The total number of vertices across all test cases is at most `2·10^5`, so a linear solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())
            g = [[] for _ in range(n)]

            for _ in range(n - 1):
                u, v = map(int, input().split())
                u -= 1
                v -= 1
                g[u].append(v)
                g[v].append(u)

            parent = [-1] * n
            order = [0]
            parent[0] = 0

            for v in order:
                for to in g[v]:
                    if parent[to] == -1:
                        parent[to] = v
                        order.append(to)

            dp = [0] * n

            for v in reversed(order):
                children = [to for to in g[v] if to != parent[v]]

                if not children:
                    dp[v] = 1 << 1
                    continue

                cur = 1

                for ch in children:
                    nxt = 0
                    for a in range(3):
                        if cur & (1 << a):
                            for b in range(3):
                                if dp[ch] & (1 << b):
                                    nxt |= 1 << ((a + b) % 3)
                    cur = nxt

                dp[v] = cur | (1 << 1)

            out.append("YES" if dp[0] & 1 else "NO")

        return "\n".join(out)

    return solve()

# provided sample
assert run("""3
4
1 2
1 3
1 4
3
1 2
1 3
9
1 2
3 1
2 4
5 2
5 6
3 7
8 3
8 9
""") == """YES
NO
YES"""

# minimum tree
assert run("""1
2
1 2
""") == "NO"

# star with 3 leaves
assert run("""1
4
1 2
1 3
1 4
""") == "YES"

# chain of length 4, shaking root only
assert run("""1
4
1 2
2 3
3 4
""") == "NO"

# root with 6 leaf children
assert run("""1
7
1 2
1 3
1 4
1 5
1 6
1 7
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge tree | NO | Minimum size case |
| Root with 3 leaves | YES | Exactly three shakes possible |
| Long chain | NO | Only one leaf exists, counts are a |
