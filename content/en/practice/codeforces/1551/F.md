---
title: "CF 1551F - Equidistant Vertices"
description: "We are given a tree with up to 100 vertices and must count how many subsets of exactly k vertices have the property that every pair of chosen vertices is at the same distance. The object being selected is a set of vertices. If we choose vertices v1, v2, ..."
date: "2026-06-10T13:23:58+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dfs-and-similar", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1551
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 734 (Div. 3)"
rating: 2200
weight: 1551
solve_time_s: 404
verified: false
draft: false
---

[CF 1551F - Equidistant Vertices](https://codeforces.com/problemset/problem/1551/F)

**Rating:** 2200  
**Tags:** brute force, combinatorics, dfs and similar, dp, trees  
**Solve time:** 6m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with up to 100 vertices and must count how many subsets of exactly `k` vertices have the property that every pair of chosen vertices is at the same distance.

The object being selected is a set of vertices. If we choose vertices `v1, v2, ..., vk`, then there must exist a single value `c` such that the distance between every distinct pair is exactly `c`.

The output is the number of such subsets modulo `10^9 + 7`.

The constraints are surprisingly small. The tree contains at most 100 vertices, and there are at most 10 test cases. A brute force over all subsets is impossible because the number of `k`-subsets can be as large as `C(100,50)`, which is astronomically large. On the other hand, `n = 100` is small enough that algorithms around `O(n^3)` or even `O(n^4)` are realistic.

The main challenge is characterizing what a set of pairwise equidistant vertices looks like inside a tree. Trees impose strong structural restrictions, and exploiting them is the key to the solution.

Several edge cases are easy to mishandle.

Consider a path of three vertices:

```
1 - 2 - 3
```

with `k = 3`.

The pairwise distances are:

```
d(1,2)=1
d(2,3)=1
d(1,3)=2
```

No valid subset exists, so the answer is `0`.

A naive idea such as "all chosen vertices must be at the same depth from some center" is not sufficient. Vertices `1` and `3` are at equal depth from vertex `2`, yet the full set of three vertices is not pairwise equidistant.

Another subtle case is `k = 2`.

For any pair of vertices, there is only one pairwise distance to check. Every pair automatically satisfies the condition.

Example:

```
1 - 2 - 3 - 4
```

with `k = 2`.

The answer is simply:

```
C(4,2)=6
```

Trying to apply the general DP used for larger `k` would be unnecessary and easy to get wrong.

A third tricky situation occurs when the common distance is odd. For example:

```
1 - 2 - 3 - 4
```

Vertices `1` and `4` are distance `3` apart. The midpoint lies on the edge `(2,3)` rather than at a vertex. For `k ≥ 3`, this cannot happen. Any valid set of at least three pairwise equidistant vertices must have a vertex center, not an edge center. Missing this observation leads to overcounting impossible configurations.

## Approaches

The most direct solution is brute force. Enumerate every subset of size `k`, compute all pairwise distances inside it, and check whether they are identical.

This is correct because it directly matches the definition. Unfortunately, the number of subsets is exponential. For `n = 100`, even enumerating all subsets is impossible. The search space is vastly larger than anything that can fit into the time limit.

To improve upon this, we need to understand the geometry of pairwise equidistant vertices in a tree.

Suppose we have at least three selected vertices and every pair is distance `2r`. Pick any two selected vertices. Their path has a unique midpoint because the distance is even. In fact, all selected vertices must share the same midpoint vertex.

Why? If three vertices are pairwise equidistant, the intersection structure of their paths forces a unique central vertex. Every selected vertex is exactly distance `r` from that center.

This immediately transforms the problem.

For a fixed center `c` and radius `r`, every chosen vertex must lie at distance `r` from `c`.

That condition alone is not enough. If two chosen vertices belong to the same child subtree of `c`, their path meets before reaching `c`, making their distance smaller than `2r`.

So each chosen vertex must come from a different branch of the center.

Now the problem becomes combinatorial.

Fix a center `c` and radius `r`.

For every child subtree of `c`, count how many vertices are exactly distance `r` from `c` inside that subtree. Let these counts be:

```
cnt1, cnt2, ..., cntm
```

To form a valid subset, we must choose exactly `k` different subtrees and pick one vertex from each chosen subtree.

The number of ways is exactly the coefficient of:

```
(1 + cnt1*x)(1 + cnt2*x)...(1 + cntm*x)
```

at degree `k`.

This can be computed with a simple DP over the child subtrees.

We repeat this process for every center and every radius.

Since `n ≤ 100`, we can afford DFS traversals from every neighboring subtree and a small combinatorial DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `n` | Exponential | Too slow |
| Optimal | O(n³) | O(n²) | Accepted |

## Algorithm Walkthrough

### Special case: k = 2

Any pair of vertices is automatically pairwise equidistant because there is only one distance to check.

The answer is simply:

```
C(n,2)
```

### General case: k ≥ 3

1. Treat every vertex `c` as a potential center.
2. For every neighbor of `c`, run a DFS into that neighbor's subtree while preventing traversal back through `c`.
3. During the DFS, count how many vertices appear at each distance from `c`.

If a vertex is reached at depth `d`, it contributes to the bucket corresponding to radius `d`.
4. For every radius `r`, collect the counts from all child subtrees.

Suppose the child subtrees contribute:

```
cnt1, cnt2, ..., cntm
```

where `cnti` is the number of vertices in subtree `i` at distance `r` from `c`.
5. Compute the number of ways to choose exactly `k` distinct subtrees and pick one vertex from each chosen subtree.

Use DP:

```
dp[j] = number of ways to choose j vertices so far
```

Initially:

```
dp[0] = 1
```

For each subtree count `cnt`:

```
ndp[j+1] += dp[j] * cnt
ndp[j] += dp[j]
```

This corresponds to either ignoring the subtree or choosing exactly one vertex from it.
6. Add `dp[k]` to the answer.
7. Repeat for all radii and all centers.

### Why it works

Take any valid subset with `k ≥ 3`.

All pairwise distances are equal. In a tree, the paths between the chosen vertices have a unique common midpoint vertex `c`. Every chosen vertex lies at the same distance `r` from `c`.

If two chosen vertices were located inside the same child subtree of `c`, their path would avoid `c`, giving a distance strictly smaller than `2r`. Since all pairwise distances must equal `2r`, this is impossible.

Thus every chosen vertex comes from a different child subtree of `c`, and each chosen vertex is exactly distance `r` from `c`.

Conversely, if we choose one distance-`r` vertex from each of `k` different child subtrees of `c`, the path between any two chosen vertices must pass through `c`. Each endpoint is distance `r` from `c`, so every pairwise distance equals `2r`.

The DP counts exactly these choices, and every valid subset has a unique center and radius, so no subset is counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    t = int(input())

    for _ in range(t):
        line = input().strip()
        while line == "":
            line = input().strip()

        n, k = map(int, line.split())

        g = [[] for _ in range(n)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        if k == 2:
            print(n * (n - 1) // 2)
            continue

        ans = 0

        for center in range(n):
            depth_cnt = []

            def dfs(v, p, depth, idx):
                if depth >= len(depth_cnt[idx]):
                    depth_cnt[idx].extend(
                        [0] * (depth - len(depth_cnt[idx]) + 1)
                    )

                depth_cnt[idx][depth] += 1

                for to in g[v]:
                    if to == p:
                        continue
                    dfs(to, v, depth + 1, idx)

            for nxt in g[center]:
                idx = len(depth_cnt)
                depth_cnt.append([])
                dfs(nxt, center, 1, idx)

            max_depth = 0
            for arr in depth_cnt:
                max_depth = max(max_depth, len(arr) - 1)

            for dist in range(1, max_depth + 1):
                dp = [0] * (k + 1)
                dp[0] = 1

                for arr in depth_cnt:
                    cnt = arr[dist] if dist < len(arr) else 0

                    ndp = dp[:]

                    for used in range(k):
                        ndp[used + 1] = (
                            ndp[used + 1]
                            + dp[used] * cnt
                        ) % MOD

                    dp = ndp

                ans = (ans + dp[k]) % MOD

        print(ans)

solve()
```

The implementation follows the structural characterization directly.

For each candidate center, every neighboring subtree is explored independently. The DFS records how many vertices occur at each distance from the center inside that specific branch.

The array `depth_cnt[i][d]` stores the number of vertices in branch `i` whose distance from the center equals `d`.

For a fixed radius, the DP processes branches one by one. Each branch contributes either nothing or exactly one chosen vertex. Multiplying by `cnt` represents choosing one of the available vertices at that distance.

The update must use a copied array `ndp`. Updating in place would allow the same subtree to be selected multiple times, which violates the requirement that chosen vertices come from distinct branches.

The loop over distances starts from `1` because selected vertices must be different from the center itself. For `k ≥ 3`, the center can never belong to the selected set.

All arithmetic is performed modulo `10^9 + 7`.

## Worked Examples

### Example 1

Input:

```
5 3
1 2
2 3
2 4
4 5
```

The only valid subset is `{1,3,5}`.

Using center `2`:

| Branch | Vertices at distance 1 | Vertices at distance 2 |
| --- | --- | --- |
| through 1 | 1 | 0 |
| through 3 | 1 | 0 |
| through 4 | 1 | 1 |

For radius `1`, the counts are:

```
[1, 1, 1]
```

DP evolution:

| Processed branches | dp[0] | dp[1] | dp[2] | dp[3] |
| --- | --- | --- | --- | --- |
| Start | 1 | 0 | 0 | 0 |
| First | 1 | 1 | 0 | 0 |
| Second | 1 | 2 | 1 | 0 |
| Third | 1 | 3 | 3 | 1 |

So one valid subset is counted.

For radius `2`, only one branch contributes, making it impossible to choose three vertices.

The final answer is `1`.

This example shows why vertices must come from different branches of the center.

### Example 2

Input:

```
4 2
1 2
2 3
2 4
```

Since `k = 2`, every pair of vertices is valid.

| Quantity | Value |
| --- | --- |
| n | 4 |
| C(n,2) | 6 |

Output:

```
6
```

This trace demonstrates the special-case shortcut. No tree structure analysis is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) | Every center is processed, DFS work across its branches is O(n), and the radius/DP processing contributes another O(n²) factor |
| Space | O(n²) | Distance counts for all branches of a center may store O(n²) values in total |

With `n ≤ 100`, an `O(n³)` solution performs roughly one million basic operations per test case, which comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    MOD = 1000000007

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        line = input().strip()
        while line == "":
            line = input().strip()

        n, k = map(int, line.split())

        g = [[] for _ in range(n)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        if k == 2:
            out.append(str(n * (n - 1) // 2))
            continue

        ans = 0

        for center in range(n):
            depth_cnt = []

            def dfs(v, p, d, idx):
                if d >= len(depth_cnt[idx]):
                    depth_cnt[idx].extend(
                        [0] * (d - len(depth_cnt[idx]) + 1)
                    )

                depth_cnt[idx][d] += 1

                for to in g[v]:
                    if to != p:
                        dfs(to, v, d + 1, idx)

            for nxt in g[center]:
                idx = len(depth_cnt)
                depth_cnt.append([])
                dfs(nxt, center, 1, idx)

            maxd = 0
            for arr in depth_cnt:
                maxd = max(maxd, len(arr) - 1)

            for dist in range(1, maxd + 1):
                dp = [0] * (k + 1)
                dp[0] = 1

                for arr in depth_cnt:
                    cnt = arr[dist] if dist < len(arr) else 0
                    ndp = dp[:]

                    for j in range(k):
                        ndp[j + 1] += dp[j] * cnt

                    dp = ndp

                ans += dp[k]

        out.append(str(ans % MOD))

    return "\n".join(out)

# provided samples
assert run("""3

4 2
1 2
2 3
2 4

3 3
1 2
2 3

5 3
1 2
2 3
2 4
4 5
""") == """6
0
1"""

# minimum tree
assert run("""1

2 2
1 2
""") == "1"

# path of length 2, k=3
assert run("""1

3 3
1 2
2 3
""") == "0"

# star with 4 leaves, choose 3 leaves
assert run("""1

5 3
1 2
1 3
1 4
1 5
""") == "4"

# star with 5 leaves, choose all leaves
assert run("""1

6 5
1 2
1 3
1 4
1 5
1 6
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-vertex tree, k=2 | 1 | Minimum valid input |
| 3-vertex path, k=3 | 0 | Pairwise distances not all equal |
| Star with 4 leaves, k=3 | 4 | Choosing vertices from distinct branches |
| Star with 5 leaves, k=5 | 1 | Exact full-leaf selection |

## Edge Cases

### Case 1: k = 2

Input:

```
1

4 2
1 2
2 3
2 4
```

The algorithm immediately enters the special case and returns:

```
C(4,2)=6
```

No center enumeration occurs. This avoids unnecessary work and guarantees every pair is counted exactly once.

### Case 2: Odd-distance midpoint

Input:

```
1

4 3
1 2
2 3
3 4
```

Any candidate triple must contain all vertices except one.

The pairwise distances can never all be equal:

```
1, 1, 2
```

or

```
1, 2, 3
```

and so on.

When the algorithm tests every center and radius, no radius obtains contributions from three distinct branches. Every DP result remains zero, producing answer `0`.

### Case 3: Multiple vertices in one branch

Input:

```
1

5 3
1 2
2 3
2 4
4 5
```

Relative to center `2`, vertices `4` and `5` belong to the same branch.

A careless solution that only checked equal depth from the center could incorrectly count `{1,3,4}` and `{1,3,5}` together without distinguishing branch structure.

The DP processes branches independently and allows at most one chosen vertex from each branch. Only `{1,3,5}` survives, yielding answer `1`.

### Case 4: Large star

Input:

```
1

6 5
1 2
1 3
1 4
1 5
1 6
```

The center is vertex `1`.

At radius `1`, each branch contributes exactly one vertex:

```
[1,1,1,1,1]
```

The DP computes:

```
C(5,5)=1
```

Every chosen pair has distance `2`, so the answer is correctly `1`. This confirms that the combinatorial counting matches the geometric interpretation of the tree.
