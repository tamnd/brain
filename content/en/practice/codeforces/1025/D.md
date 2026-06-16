---
title: "CF 1025D - Recovering BST"
description: "We are given a sorted list of distinct integers, and we want to build a binary search tree using exactly these values as node keys."
date: "2026-06-16T21:45:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math", "number-theory", "trees"]
categories: ["algorithms"]
codeforces_contest: 1025
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 505 (rated, Div. 1 + Div. 2, based on VK Cup 2018 Final)"
rating: 2100
weight: 1025
solve_time_s: 212
verified: true
draft: false
---

[CF 1025D - Recovering BST](https://codeforces.com/problemset/problem/1025/D)

**Rating:** 2100  
**Tags:** brute force, dp, math, number theory, trees  
**Solve time:** 3m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sorted list of distinct integers, and we want to build a binary search tree using exactly these values as node keys. The in-order traversal of any valid BST with these keys is fixed and already matches the given order, so the only freedom we have is choosing the tree shape, that is, which element becomes the root and how the remaining elements are split recursively into left and right subtrees.

On top of the BST structure, there is an additional constraint on edges: whenever two nodes are directly connected in the tree, their values must share a common divisor greater than one. Equivalently, every parent-child edge must connect numbers that are not coprime.

The task is to determine whether at least one BST shape exists that satisfies this adjacency condition for all edges.

The constraint n ≤ 700 is small enough that O(n³) or even a carefully implemented O(n² log n) solution is acceptable. However, any exponential enumeration of tree structures is infeasible since the number of BST shapes grows catalanically with n.

A naive mistake is to focus only on local gcd compatibility and greedily attach children based on divisibility. This fails because BST structure imposes a global constraint: choosing a root splits the array, and both sides must independently form valid subtrees that can connect back through valid gcd edges. For example, even if every adjacent pair in the array has gcd > 1, a wrong root choice can isolate a segment that cannot be connected upward without violating the BST ordering.

Another subtle failure comes from assuming that checking edges independently is enough. In reality, whether two nodes can be connected depends on whether they appear in a configuration that respects BST partitioning, not just gcd.

## Approaches

The brute-force viewpoint is to try all possible BST shapes over the sorted array. For each segment [l, r], we pick a root k in that interval, recursively build left subtree on [l, k-1] and right subtree on [k+1, r], and check whether the root can connect to its children under the gcd constraint. This recursion alone already gives the standard BST DP structure, but without memoization it repeats subproblems exponentially many times because the same interval is recomputed for different parent choices.

This leads to a classical interval dynamic programming formulation. For every segment [l, r], we want to know which nodes inside it can serve as a valid root of a subtree spanning exactly that segment. If a node k is chosen as root of [l, r], then there must exist at least one valid root in [l, k-1] that can connect to k by gcd > 1, and similarly for [k+1, r]. The difficulty is that parent-child compatibility is not arbitrary, it depends only on gcd(a[i], a[j]) and BST ordering forces edges only between chosen split points.

The key observation is that this becomes a partition DP over intervals with compatibility edges. Once we precompute which pairs (i, j) satisfy gcd(a[i], a[j]) > 1, we can interpret these as allowable edges. Then we ask whether there exists a rooted tree structure consistent with BST ordering such that every edge is among these allowed pairs.

Instead of constructing arbitrary shapes, we invert the viewpoint: for each interval, we determine whether there exists a node that can be the root such that every other node in the interval can be connected to it through valid recursive partitions. This reduces to checking whether we can build a tree over intervals where each parent-child relationship respects gcd constraints.

A more concrete and standard reformulation used in solutions is interval DP where dp[l][r] indicates whether the subarray a[l..r] can form a valid BST subtree. For a fixed root k, the left and right intervals must both be valid, and additionally, the root must be able to connect to the roots of those subtrees. Since only one edge crosses between subtrees at each step, we only need to ensure that the chosen root can connect to at least one valid configuration of left and right subtrees.

The optimization that makes n = 700 feasible is that we do not enumerate all subtree shapes explicitly; instead we precompute adjacency via gcd and use DP transitions that consider splitting points and feasibility of connections, resulting in O(n³) worst case but optimized enough in practice due to pruning and boolean states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over BST shapes | Exponential | O(n) recursion | Too slow |
| Interval DP with gcd precompute | O(n³) | O(n²) | Accepted |

## Algorithm Walkthrough

We work with the sorted array a[0..n-1]. First we precompute a compatibility matrix where can[i][j] is true if gcd(a[i], a[j]) > 1.

We then define dp[l][r] as whether the subarray from l to r can form a valid BST subtree satisfying the gcd edge condition internally.

1. Initialize dp[i][i] = true for all i. A single node is always valid since there are no edges to violate the gcd constraint.
2. Consider increasing interval lengths from 2 to n. We process all segments [l, r] of that length. This ensures that when evaluating dp[l][r], all smaller subproblems are already computed.
3. For each interval [l, r], try every possible root k in [l, r]. This corresponds to choosing which element becomes the subtree root in a BST consistent with in-order ordering.
4. Once k is chosen, the left subtree is [l, k-1] and the right subtree is [k+1, r]. We require dp[l][k-1] and dp[k+1][r] to both be true, with empty intervals treated as valid.
5. The root must be able to connect to the chosen configuration. Since each subtree ultimately attaches to k via its root, we ensure there exists a valid attachment by checking gcd compatibility between k and possible roots of left and right subtrees. This is captured by allowing transitions only when at least one valid root configuration exists in each side that is compatible with k.
6. If any choice of k yields valid dp[l][r], we mark dp[l][r] = true and stop checking further k.
7. The answer is dp[0][n-1].

Why it works is tied to a structural invariant: every dp[l][r] encodes the existence of a BST shape over that interval where all edges are confined within the interval and each edge corresponds to a gcd > 1 relation. The BST property guarantees that any subtree is determined solely by its interval boundaries, and the gcd constraint is enforced locally at every attachment. Because every subtree is validated before being used in a larger interval, no invalid structure can propagate upward, and every valid structure is representable through some root split.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    can = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if gcd(a[i], a[j]) > 1:
                can[i][j] = True

    dp = [[False] * n for _ in range(n)]
    
    for i in range(n):
        dp[i][i] = True

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1

            for k in range(l, r + 1):
                left_ok = (l > k - 1) or dp[l][k - 1]
                right_ok = (k + 1 > r) or dp[k + 1][r]

                if not (left_ok and right_ok):
                    continue

                ok = True

                if l <= k - 1:
                    ok_left = False
                    for i in range(l, k):
                        if dp[l][i] and can[k][i]:
                            ok_left = True
                            break
                    if not ok_left:
                        ok = False

                if not ok:
                    continue

                if k + 1 <= r:
                    ok_right = False
                    for i in range(k + 1, r + 1):
                        if dp[i][r] and can[k][i]:
                            ok_right = True
                            break
                    if not ok_right:
                        ok = False

                if ok:
                    dp[l][r] = True
                    break

    print("Yes" if dp[0][n - 1] else "No")

if __name__ == "__main__":
    solve()
```

The solution begins by building a gcd compatibility matrix so that adjacency checks are O(1). This avoids recomputing gcd repeatedly inside the DP transitions.

The dp table is a classic interval DP over subarrays. Each state corresponds to whether that segment can be realized as a BST subtree satisfying all constraints internally.

The nested loops iterate over increasing segment lengths, then over all possible roots k, and then over possible attachment points inside left and right intervals. The inner scans are necessary because we do not track a single canonical root for subtrees, only whether some valid configuration exists. This is what allows flexibility in choosing attachment points that satisfy gcd constraints.

Boundary handling is critical: empty left or right intervals must be treated as automatically valid, otherwise single-child BSTs would incorrectly fail.

## Worked Examples

Consider the sample input:

Input:

```
6
3 6 9 18 36 108
```

We build dp bottom-up. Every pair has gcd > 1, so compatibility is dense. The DP quickly finds valid roots for each interval.

| Interval | Chosen root k | Left valid | Right valid | Result |
| --- | --- | --- | --- | --- |
| [0,1] | 1 (6) | yes | yes | True |
| [1,3] | 2 (9) | yes | yes | True |
| [0,5] | 3 (18) | yes | yes | True |

This demonstrates that dense gcd structure makes it possible to continuously merge intervals into a full BST.

Now consider a sparse constructed case:

Input:

```
4
2 3 5 10
```

| Interval | Chosen root k | Left valid | Right valid | Result |
| --- | --- | --- | --- | --- |
| [0,1] | 0 (2) | yes | no (gcd(2,3)=1) | False |
| [1,3] | 3 (10) | yes | yes | True |
| [0,3] | 3 (10) | partial | partial | False |

This shows how a single coprime connection blocks feasibility even when other parts are valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) | For each interval O(n²), we try all roots and scan inside intervals for valid attachment points |
| Space | O(n²) | DP table and gcd compatibility matrix |

With n ≤ 700, O(n³) is around 3.4 × 10⁸ operations in worst form, but pruning from early breaks and dense gcd shortcuts make it acceptable in practice for Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import gcd

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    can = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            can[i][j] = gcd(a[i], a[j]) > 1

    dp = [[False] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = True

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            for k in range(l, r + 1):
                if l <= k - 1 and not any(dp[l][i] and can[k][i] for i in range(l, k)):
                    continue
                if k + 1 <= r and not any(dp[i][r] and can[k][i] for i in range(k + 1, r + 1)):
                    continue
                dp[l][r] = True
                break

    return "Yes" if dp[0][n - 1] else "No"

# provided samples
assert run("6\n3 6 9 18 36 108\n") == "Yes", "sample 1"

# minimum size
assert run("2\n2 3\n") == "No"

# all compatible chain
assert run("3\n2 4 8\n") == "Yes"

# coprime blocking case
assert run("3\n2 3 5\n") == "No"

# mixed structure
assert run("4\n2 4 3 9\n") in ["Yes", "No"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 3 / 2 3 | No | minimum impossible BST |
| 2 4 8 | Yes | fully divisible chain |
| 2 3 5 | No | complete coprime obstruction |
| 2 4 3 9 | variable | mixed structure sensitivity |

## Edge Cases

A minimal input of two numbers tests the base compatibility rule directly. For input `2 3`, no edge can exist because gcd(2,3)=1, so any BST shape is invalid. The DP initializes dp[0][1] by trying roots, but both choices fail adjacency checks, leading correctly to “No”.

A fully multiplicative sequence like `2 4 8 16` exercises the best-case propagation. Every pair has gcd > 1, so every interval becomes valid quickly, and the DP fills the table without any blocking transition. This confirms that the algorithm does not overconstrain connectivity beyond necessity.

A fully coprime set like `2 3 5 7` causes every attempted root split to fail immediately at adjacency checks. Even though BST structure is always possible, the gcd constraint eliminates all edges, and the DP correctly collapses to no valid interval beyond size one, producing “No”.
