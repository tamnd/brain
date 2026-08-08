---
title: "CF 102431G - Game on the Tree"
description: "We have a tree rooted at vertex 1, with a token initially at vertex 1. Panda moves first. On every turn after the first, the player must move the token farther than the opponent moved on the preceding turn. A player who has no legal move loses."
date: "2026-08-08T23:51:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102431
codeforces_index: "G"
codeforces_contest_name: "2019 China Collegiate Programming Contest Final (CCPC-Final 2019)"
rating: 0
weight: 102431
solve_time_s: 247
verified: true
draft: false
---

[CF 102431G - Game on the Tree](https://codeforces.com/problemset/problem/102431/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree rooted at vertex 1, with a token initially at vertex 1. Panda moves first. On every turn after the first, the player must move the token farther than the opponent moved on the preceding turn. A player who has no legal move loses.

Sheep is allowed to delete edges and vertices indirectly by choosing any connected subgraph that contains vertex 1. Since the original graph is a tree, every such subgraph is itself a tree containing the root. We need to count how many of these rooted connected subgraphs are winning positions for Sheep, modulo (10^9+7). The official solution reduces the game to the position of the tree's diameter center, and then counts rooted subgraphs for which vertex 1 is that center.

The input contains up to (2\cdot10^5) vertices per test case and up to ten test cases. There is no useful dependence on edge weights or other small numeric parameters, so an algorithm that is quadratic in (n) is already too expensive. In particular, a DP that scans a depth array of length (O(n)) at every vertex can perform (O(n^2)) work on a long tree. We need to make the total amount of depth-DP work close to linear, or at worst (O(n\log n)).

There are three boundary cases that deserve attention.

For a single vertex, the only possible subgraph is vertex 1 itself. Its diameter has length zero and its center is vertex 1, so the answer is 1.

For two vertices, the only winning subgraph is the singleton ({1}). The subgraph containing both vertices has a diameter consisting of one edge, whose center is the middle of that edge rather than vertex 1. Thus

```
1
2
1 2
```

produces

```
Case #1: 1
```

A path can also be misleading if we only look at its maximum depth from the root. For

```
1
3
1 2
2 3
```

the three possible rooted subgraphs are ({1}), ({1,2}), and ({1,2,3}). Only the singleton has vertex 1 as its diameter center, so the answer is 1. A careless implementation that treats the root as a center whenever it is one of the deepest vertices would incorrectly count more.

A star gives the opposite boundary. For

```
1
4
1 2
1 3
1 4
```

any subgraph containing vertex 1 and at least two leaves has diameter 2 and center 1. There are four such non-singleton subgraphs, corresponding to the three pairs of leaves and the set of all three leaves. Together with the singleton, the answer is 5. This case catches the distinction between "the maximum depth occurs" and "the maximum depth occurs in at least two different root branches."

## Approaches

A direct solution can enumerate every connected subgraph containing vertex 1, determine its diameter, and check whether vertex 1 is the center. There are exponentially many candidates. Even using the looser upper bound of (2^{n-1}) edge subsets, testing each candidate in (O(n)) gives (O(n2^{n-1})) work. For (n=2\cdot10^5), this is completely impossible.

The first useful observation is that the complicated move rule has a surprisingly simple game-theoretic characterization. Consider any fixed tree and its diameter. If the initial token is at the diameter's center, the second player has a mirror strategy. Whenever the first player moves to some vertex at distance (d) from the center, the second player can move to a vertex at the same distance on the opposite side of the center. The required move distances match, and the strict inequality forces the eventual game toward a diameter endpoint. The official analysis gives precisely this diameter-center characterization.

If the starting vertex is not the diameter center, the first player can move toward the center and obtain the corresponding advantage. Thus Sheep wins exactly when vertex 1 is the center of the chosen subgraph's diameter.

Now the game has disappeared. The problem is purely combinatorial: count connected rooted subtrees whose diameter is centered at vertex 1.

Root the original tree at vertex 1. Consider a selected connected subtree containing the root. Let its maximum depth from vertex 1 be (D). Vertex 1 is the diameter center exactly when the depth (D) is achieved in at least two different child subtrees of vertex 1.

Why? If two different branches both contain vertices at depth (D), those two vertices are distance (2D) apart through the root. Any path completely inside one branch has length at most (2D-2), so the diameter goes through vertex 1 and its center is exactly vertex 1. Conversely, if only one root branch reaches depth (D), a diameter of length (2D) cannot be formed through the root, so the root is not the center.

We therefore need a tree DP that counts connected subtrees containing each vertex, classified by their maximum depth.

Define (f_u[i]) as the number of connected subtrees inside the subtree of (u), containing (u), whose maximum depth measured from (u) is exactly (i). For a leaf, (f_u[0]=1).

Suppose we already processed some children of (u), represented by an array (A_i), and now add a child (v), whose corresponding array is (B_i). A new subtree whose maximum depth is (i) can arise in two ways. The new child reaches depth (i), while the previous part has depth at most (i), or the previous part reaches depth (i), while the new child has depth strictly less than (i). This gives the pointwise recurrence

B_i\left(1+\sum_{j=0}^{i}A_j\right)
+
A_i\left(1+\sum_{j=0}^{i-1}B_j\right).
]

The recurrence is simple, but evaluating it independently for every child would still be too slow. The key structural observation is that we only need to process the shorter child arrays explicitly. We choose, for every vertex, a child of maximum height as its heavy child. The DP array is stored along this heavy chain and is shared between its vertices. A light child's array is then merged into the current array in time proportional to the light child's height. This is the long-chain decomposition used by accepted solutions for this problem.

The suffix of the current DP array that is beyond the light child's maximum depth only needs multiplication by one scalar. We store this multiplication lazily. When an array position is eventually accessed, its pending multiplication is pushed to the next position. Because DP positions are consumed from small depth to large depth, each lazy tag moves only forward along the chain.

After computing all (f_u), the root is handled separately. For every child (c) of the root, define

[
a_c(D)=f_c[D-1],
]

which counts nonempty choices in branch (c) whose maximum root depth is exactly (D). Also define

[
b_c(D)=1+\sum_{j=0}^{D-2}f_c[j],
]

where the additional 1 represents choosing nothing from that branch. Thus (b_c(D)) counts branch choices whose maximum depth is strictly smaller than (D).

For a fixed depth (D), the product

[
P_D=\prod_c (a_c(D)+b_c(D))
]

counts all rooted subtrees whose maximum depth is at most (D). Hence (P_D-P_{D-1}) counts those whose maximum depth is exactly (D).

Among these, we must remove the configurations where exactly one root branch reaches depth (D). Define

[
Q_D=\sum_c a_c(D)\prod_{j\ne c}b_j(D).
]

Then

[
P_D-P_{D-1}-Q_D
]

is exactly the number of configurations whose maximum depth (D) is achieved in at least two root branches.

We maintain (P_D), (\prod b_c(D)), and (Q_D) with a segment tree over the root's children. Each branch changes its (a_c,b_c) only once per depth, and the total number of such changes is at most the sum of the branch heights, which is (O(n)). The segment tree makes every change (O(\log n)).

The singleton root is handled separately, so the final answer is one plus the sum of the valid configurations for all positive depths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^{n-1})) | (O(n)) | Too slow |
| Ordinary tree DP | (O(n^2)) | (O(n^2)) in the worst case | Too slow |
| Long-chain DP + root aggregation | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex 1 and build a parent-before-child traversal order. Processing this order backwards gives every child's DP before its parent is processed.
2. Compute the height of every vertex and select a heavy child with maximum height. The DP array of a vertex is placed at one position on the heavy chain, so the child immediately below it corresponds to the next position in the same array.
3. Allocate one contiguous DP array for every heavy chain. A chain of height (h) needs (h+2) positions, because one extra position is needed for the lazy suffix multiplication.
4. Process vertices from leaves toward the root. Set (f_u[0]=1), representing the subtree consisting only of (u).
5. Skip the heavy child during the merge because its DP array is already physically shared with (u). Every other child is a light child and is merged explicitly.
6. While merging a light child (v), scan its DP array from depth zero upward. Maintain two prefix sums. The first is (1+\sum_{j\le i}f_u[j]), and the second is (1+\sum_{j<i}f_v[j]). These two quantities are exactly the coefficients required by the recurrence for the new maximum depth.
7. After the last depth represented by (v), every remaining position is multiplied by the same factor, namely (1+\sum_j f_v[j]). Store that operation as a lazy multiplication instead of touching the rest of the chain.
8. After the complete tree DP, consider each child of the root as one independent branch. At depth (D), maintain (a_c=f_c[D-1]) and (b_c=1+\sum_{j<D-1}f_c[j]). The pair ((a_c,b_c)) completely describes how branch (c) participates in a subtree whose maximum depth is (D).
9. Use a segment tree whose node stores three values. The first is the product of (a_c+b_c), the second is the product of (b_c), and the third counts configurations in which exactly one branch contributes (a_c). If the two children of a segment-tree node have states ((P_1,B_1,Q_1)) and ((P_2,B_2,Q_2)), combine them as
[
P=P_1P_2,
]
[
B=B_1B_2,
]
[
Q=Q_1B_2+B_1Q_2.
]
The last formula says that the unique branch reaching the current maximum is either in the left segment or in the right segment.
10. For every positive depth (D), let the segment-tree root give (P_D) and (Q_D). If (P_{D-1}) is the number of choices with maximum depth below (D), then
[
P_D-P_{D-1}-Q_D
]
counts exactly the subtrees whose maximum depth is (D) in at least two root branches. Add this to the answer and continue to the next depth.

### Why it works

The game is winning for the second player exactly when the starting vertex is the center of the tree's diameter. A rooted connected subtree has vertex 1 as its diameter center exactly when its greatest root depth occurs in at least two different root branches. The DP counts every possible connected choice inside every branch according to its exact maximum depth. The root aggregation then separates configurations by their global maximum depth and removes exactly those in which only one branch reaches that maximum. Consequently every counted subtree has root 1 as its diameter center, and every subtree with root 1 as its diameter center is counted exactly once.

The heavy-chain representation does not change any DP value. It only changes where the values are stored. A vertex and its heavy child use adjacent positions in the same array, while a light child's array is merged into that shared array. The lazy suffix multiplier is algebraically identical to multiplying all unaffected larger-depth states by the same factor. Thus the optimization preserves the original DP recurrence.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve_case(n, adj):
    if n == 1:
        return 1

    # Root the tree at 0.
    parent = [-1] * n
    parent[0] = -2
    order = [0]

    for u in order:
        for v in adj[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    # Height and heavy child.
    height = [0] * n
    heavy = [-1] * n

    for u in reversed(order):
        best_h = -1
        best_v = -1
        for v in adj[u]:
            if parent[v] == u:
                hv = height[v]
                if hv > best_h:
                    best_h = hv
                    best_v = v
        if best_v != -1:
            height[u] = best_h + 1
            heavy[u] = best_v

    # Allocate one contiguous array per heavy chain.
    base = [0] * n
    pool_size = 0

    for u in order:
        p = parent[u]
        if p != -2 and heavy[p] == u:
            continue

        x = u
        cur = pool_size
        length = height[u] + 2
        pool_size += length

        while x != -1:
            base[x] = cur
            cur += 1
            x = heavy[x]

    val = [0] * pool_size
    tag = [1] * pool_size

    def modify(pos, mul):
        val[pos] = val[pos] * mul % MOD
        tag[pos] = tag[pos] * mul % MOD

    def pushdown(pos):
        t = tag[pos]
        if t != 1:
            nxt = pos + 1
            val[nxt] = val[nxt] * t % MOD
            tag[nxt] = tag[nxt] * t % MOD
            tag[pos] = 1

    # Tree DP.
    for u in reversed(order):
        bu = base[u]
        val[bu] = 1

        # Only light children are explicitly merged.
        for v in adj[u]:
            if parent[v] != u or v == heavy[u]:
                continue

            bv = base[v]
            length = height[v] + 1

            r = 1
            s = 1

            for i in range(1, length + 1):
                pu = bu + i
                pv = bv + i - 1

                pushdown(pu)
                pushdown(pv)

                a = val[pu]
                b = val[pv]

                # r = 1 + sum of current f-values through depth i.
                r += a
                if r >= MOD:
                    r -= MOD

                # s = 1 + sum of child f-values below depth i.
                val[pu] = (r * b + s * a) % MOD

                s += b
                if s >= MOD:
                    s -= MOD

            # For all larger depths the light child can only be chosen
            # completely or omitted, so the multiplier is the same.
            modify(bu + length + 1, s)

    # Root aggregation.
    root_children = [v for v in adj[0] if parent[v] == 0]
    k = len(root_children)

    if k == 0:
        return 1

    max_depth = max(height[v] + 1 for v in root_children)

    # events[d] contains branches whose height reaches depth d.
    events = [[] for _ in range(max_depth + 1)]

    for idx, v in enumerate(root_children):
        branch_height = height[v] + 1
        for d in range(1, branch_height + 1):
            events[d].append(idx)

    # For each root branch:
    # b[idx] = number of choices with maximum depth < current d
    # a[idx] = number of choices with maximum depth == current d
    b = [1] * k
    a = [1] * k

    size = 1
    while size < k:
        size <<= 1

    seg_p = [1] * (2 * size)
    seg_b = [1] * (2 * size)
    seg_q = [0] * (2 * size)

    # Initially d = 1, so b = 1 and a = f_child[0] = 1.
    for i in range(k):
        pos = size + i
        seg_p[pos] = 2
        seg_b[pos] = 1
        seg_q[pos] = 1

    for pos in range(size - 1, 0, -1):
        left = pos << 1
        right = left | 1

        seg_p[pos] = seg_p[left] * seg_p[right] % MOD
        seg_b[pos] = seg_b[left] * seg_b[right] % MOD
        seg_q[pos] = (
            seg_q[left] * seg_b[right]
            + seg_b[left] * seg_q[right]
        ) % MOD

    def update_branch(idx):
        pos = size + idx
        x = (b[idx] + a[idx]) % MOD

        seg_p[pos] = x
        seg_b[pos] = b[idx]
        seg_q[pos] = a[idx]

        pos >>= 1
        while pos:
            left = pos << 1
            right = left | 1

            seg_p[pos] = seg_p[left] * seg_p[right] % MOD
            seg_b[pos] = seg_b[left] * seg_b[right] % MOD
            seg_q[pos] = (
                seg_q[left] * seg_b[right]
                + seg_b[left] * seg_q[right]
            ) % MOD

            pos >>= 1

    answer = 1
    previous_p = 1

    for d in range(1, max_depth + 1):
        if d >= 2:
            for idx in events[d]:
                v = root_children[idx]

                old_a = a[idx]
                b[idx] += old_a
                if b[idx] >= MOD:
                    b[idx] -= MOD

                pos = base[v] + d - 1
                pushdown(pos)
                a[idx] = val[pos]

                update_branch(idx)

        current_p = seg_p[1]
        exactly_one = seg_q[1]

        good = current_p - previous_p - exactly_one
        good %= MOD

        answer += good
        if answer >= MOD:
            answer -= MOD

        previous_p = current_p

    return answer

def solve():
    t = int(input())
    out = []

    for case_id in range(1, t + 1):
        n = int(input())
        adj = [[] for _ in range(n)]

        for _ in range(n - 1):
            x, y = map(int, input().split())
            x -= 1
            y -= 1
            adj[x].append(y)
            adj[y].append(x)

        ans = solve_case(n, adj)
        out.append(f"Case #{case_id}: {ans}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first traversal establishes the rooted representation without recursion. Avoiding recursive DFS is deliberate because a path of (2\cdot10^5) vertices would otherwise exceed Python's recursion depth.

The height computation is performed in reverse order. A child with the greatest height becomes the heavy child. The heavy child is not merged explicitly because its DP storage is already adjacent to the parent's storage. This is the central memory optimization.

The `val` array stores the actual DP values, while `tag` stores pending multiplication. When a suffix beginning at position (p) is multiplied by some value, only position (p) needs to be changed immediately. The tag records the same multiplier for later positions. Calling `pushdown(p)` transfers it to (p+1). Since every merge reads depths in increasing order, each pending tag moves forward exactly when needed.

The variables `r` and `s` in the merge are prefix counts. The expression

```
val[pu] = (r * b + s * a) % MOD
```

is the two-case recurrence for the new exact maximum depth. The order of the update matters: `r` must include the current `a`, while `s` must still represent only child depths strictly smaller than the current depth.

The root aggregation deliberately does not use modular division. A product of branch counts can be zero modulo (10^9+7), so trying to remove one factor with a modular inverse would require special handling for zero factors. The segment tree avoids division entirely.

For a segment tree node, `seg_p` represents all choices, `seg_b` represents choices where no branch in that segment reaches the current maximum, and `seg_q` represents choices where exactly one branch does. These three values are enough to combine arbitrary groups of root branches.

All arithmetic is reduced modulo (10^9+7). Python integers do not overflow, but reducing products keeps the integers small and avoids unnecessary growth.

## Worked Examples

### Sample 1

The tree is simply (1-2). There is only one root branch, so no nonempty subtree can have the maximum depth in two different branches.

| Depth (D) | Branch (a) | Branch (b) | (P_D) | (Q_D) | New valid subtrees |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 1 | (2-1-1=0) |

The singleton root is added separately, giving the final answer 1.

### Sample 2

The tree is

```
      1
     / \
    2   4
    |  / \
    3 5   6
```

For the branch rooted at 2, the exact-depth DP is

[
f_2=[1,1].
]

For the branch rooted at 4, the exact-depth DP is

[
f_4=[1,3],
]

because the only depth-zero choice is vertex 4, while at depth one we may select vertex 5, vertex 6, or both.

At depth 1, both branches can reach the maximum:

| Depth (D) | Branch 2 (a,b) | Branch 4 (a,b) | (P_D) | (Q_D) | New valid |
| --- | --- | --- | --- | --- | --- |
| 1 | ((1,1)) | ((1,1)) | 4 | 2 | (4-1-2=1) |

At depth 2, the branch rooted at 2 has (a=1,b=2), while the branch rooted at 4 has (a=3,b=2).

| Depth (D) | Branch 2 (a,b) | Branch 4 (a,b) | (P_D) | (Q_D) | New valid |
| --- | --- | --- | --- | --- | --- |
| 2 | ((1,2)) | ((3,2)) | 15 | 8 | (15-4-8=3) |

There is one singleton, one valid subtree with maximum depth 1, and three valid subtrees with maximum depth 2. The total is

[
1+1+3=5,
]

matching the sample output.

The trace also shows why merely counting subtrees whose diameter passes through the root is not enough. The maximum depth must be attained on at least two distinct branches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Long-chain DP processes each light-chain depth explicitly, and root branch updates use a segment tree. |
| Space | (O(n)) | Heavy-chain DP storage, tree representation, and root aggregation structures are all linear. |

The tree DP is substantially smaller than the quadratic approach because a vertex's long heavy path is stored once and reused by all vertices on that path. Light-child merges are charged to shorter chains, giving the standard (O(n\log n)) bound for this implementation. The root aggregation performs only (O(n)) branch-depth updates, each taking (O(\log n)). With (n\le2\cdot10^5), this fits the intended complexity of the problem. The official contest material also gives (O(n)) or (O(n\log n)) tree-DP solutions and explicitly warns against an (O(n^2)) degeneration.

## Test Cases

The following test harness assumes the submitted solution has been saved as `solution.py`. It invokes the actual program, so the assertions test the complete input/output behavior rather than a separate reimplementation.

```python
# helper: run the submitted solution and return its output
import subprocess
import sys

def run(inp: str) -> str:
    result = subprocess.run(
        [sys.executable, "solution.py"],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()

# Provided sample
sample = """\
2
2
1 2
6
1 2
2 3
1 4
4 5
4 6
"""
assert run(sample) == """\
Case #1: 1
Case #2: 5
""".strip(), "provided samples"

# Minimum-size tree
assert run("""\
1
1
""") == "Case #1: 1", "single vertex"

# Path of length 3
assert run("""\
1
3
1 2
2 3
""") == "Case #1: 1", "path"

# Star with three leaves.
# Valid choices are the singleton plus every choice containing
# at least two leaves: 1 + C(3,2) + C(3,3) = 5.
assert run("""\
1
4
1 2
1 3
1 4
""") == "Case #1: 5", "star"

# Maximum-size path.
# Every connected subgraph containing vertex 1 is a prefix of the path,
# and only the singleton has vertex 1 as its diameter center.
n = 200000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
max_path = f"1\n{n}\n{edges}\n"

assert run(max_path) == "Case #1: 1", "maximum-size path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `Case #1: 1` | Minimum size and singleton handling |
| `1-2-3` | `Case #1: 1` | A path where the root is never the center of a nontrivial prefix |
| Star with three leaves | `Case #1: 5` | Multiple branches reaching the same maximum depth |
| Path with 200000 vertices | `Case #1: 1` | Maximum size and avoidance of recursive DFS or quadratic DP |
| Official samples | `1`, `5` | Full correctness against the given examples |

## Edge Cases

For the single-vertex tree

```
1
1
```

the rooted tree has no children. The DP contains only (f_1[0]=1), and the root aggregation has no positive depth to process. The answer starts at one for the singleton and remains one.

For the two-vertex tree

```
1
2
1 2
```

there is one root branch. At depth 1, that branch has (a=1) and (b=1), so (P_1=2). Exactly one branch reaches depth 1 in one configuration, giving (Q_1=1). Since (P_0=1), the number with at least two branches at maximum depth is (2-1-1=0). The singleton remains the only winning choice.

For the path

```
1
3
1 2
2 3
```

the root still has only one branch. The maximum depth can be 1 or 2, but it can never occur in two different branches. Both depths contribute zero winning configurations, leaving only the singleton.

For the star

```
1
4
1 2
1 3
1 4
```

there are three root branches. At depth 1, every branch has (a=1) and (b=1). Thus all (2^3=8) branch selections are represented by (P_1), while exactly one branch reaches the maximum in (Q_1=3) configurations. Removing the singleton case and the exactly-one-branch cases gives (8-1-3=4) valid non-singleton subtrees. Adding the singleton gives 5.

The maximum-size path is also a useful implementation edge case. Its depth can be (199999), so an implementation using recursive DFS would normally overflow Python's recursion limit. The solution uses iterative traversal throughout. Since a path has no light children, the expensive merge loop is almost entirely absent, so the large depth does not cause quadratic work.

Equal-height branches are another subtle case. The heavy child is chosen arbitrarily among children with maximum height. If two children have the same height, one becomes heavy and the other becomes light. The light branch is still fully merged into the shared DP array, so no subtree choices are lost. The choice of which equal-height child is heavy affects only storage, never the DP values.

Finally, modular zero must not be treated as ordinary integer zero when dividing products. A branch count can be congruent to zero modulo (10^9+7), even though the actual number of configurations is positive. The root aggregation consequently uses a segment tree and multiplication only, avoiding modular inverses and making the calculation valid even when some products vanish modulo the modulus.
