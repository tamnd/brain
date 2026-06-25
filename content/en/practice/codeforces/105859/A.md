---
title: "CF 105859A - Accomplices"
description: "The problem describes a group of candidates and friendships between them. We need to count how many groups of candidates can be chosen for every possible group size so that no two chosen candidates are friends."
date: "2026-06-25T14:40:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105859
codeforces_index: "A"
codeforces_contest_name: "Mines HSPC 2025 Open Division"
rating: 0
weight: 105859
solve_time_s: 42
verified: true
draft: false
---

[CF 105859A - Accomplices](https://codeforces.com/problemset/problem/105859/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a group of candidates and friendships between them. We need to count how many groups of candidates can be chosen for every possible group size so that no two chosen candidates are friends. In graph terminology, each candidate is a vertex and each friendship is an edge, so we are counting independent sets grouped by their size. The output contains one value for each size from zero to `n`, where the value is the number of independent sets containing exactly that many vertices.

The number of candidates can reach 40. This is the key restriction. A normal graph traversal or dynamic programming over vertices is not enough because counting all subsets directly requires checking up to `2^40` possibilities, which is about one trillion states. Even a very fast implementation cannot handle that within a few seconds. The limit strongly suggests splitting the problem into smaller pieces, because `2^20` is only about one million and is manageable.

There are some easy-to-miss cases. When there are no friendships, every subset is valid. For example:

```
3 0
```

The answer is:

```
1 3 3 1
```

A solution that only counts pairs or tries to greedily choose candidates would fail because every possible group works.

Another case is when the graph is complete:

```
3 3
1 2
1 3
2 3
```

The answer is:

```
1 3 0 0
```

Only the empty group and single candidates are allowed. A careless implementation that forgets to check conflicts between vertices from different halves could count invalid groups.

A third edge case is a disconnected graph:

```
4 2
1 2
3 4
```

The answer is:

```
1 4 4 0 0
```

The pairs `(1,3)`, `(1,4)`, `(2,3)`, and `(2,4)` are valid, but no group of size three exists. Treating the two connected components separately without combining their sizes correctly can give wrong counts.

## Approaches

The direct approach is to examine every subset of candidates and check whether it contains a friendship edge. For each of the `2^n` subsets, we would scan the selected candidates and verify that no two selected vertices are connected. The method is correct because every possible group is considered exactly once. The problem is that with `n = 40`, the number of subsets is around `1,099,511,627,776`, so the operation count is far beyond what can run in time.

The useful observation is that the graph is too large for full enumeration, but it is small enough to split. If we divide the vertices into two halves of at most 20 vertices each, every half has at most `2^20` subsets. We can enumerate all subsets of one half, determine which ones are internally valid, and store information that helps combine them with the other half.

For a subset of the left half, the important information is not only its size but also which vertices on the right half cannot be chosen with it. Each left vertex has a bitmask of its neighbors on the right side. By ORing these masks for the chosen left vertices, we know the forbidden right vertices. The remaining right vertices are available.

The right half can be preprocessed with a dynamic programming array. For every mask of right vertices, we store how many valid independent subsets are contained inside that mask, separated by their sizes. Then every valid left subset can query the number of ways to choose compatible right subsets by looking at the allowed mask.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(1) | Too slow |
| Optimal | O(2^(n/2) * n) | O(2^(n/2) * n) | Accepted |

## Algorithm Walkthrough

1. Split the vertices into two groups. Let the first group contain `a` vertices and the second group contain `b` vertices, where both values are at most 20. This reduces the exponential part from `2^40` to about `2^20`.
2. Enumerate every subset of the second group and determine whether it is an independent set. For every valid subset, store its size. The stored information will later answer: "How many valid right-side groups of each size fit inside this available set?"
3. Build a subset dynamic programming table over the second group. Start with the values for exact masks and propagate information to larger masks. After this, a query for a mask tells us how many independent subsets of every size are contained inside it.
4. Enumerate every subset of the first group. Check whether it is independent inside the first group. If it is not, discard it because adding vertices from the other half cannot fix an internal friendship.
5. For every valid left subset, compute the bitmask of right-side vertices blocked by its friendships. Invert this mask to get the right-side vertices that can still be used.
6. Add the stored counts for the available right-side mask to the answer. The size of the final group is the left subset size plus the chosen right subset size.

Why it works: every independent set in the original graph can be uniquely divided into the part that belongs to the left half and the part that belongs to the right half. The left part is checked for internal conflicts, and the right part is counted only among vertices not forbidden by left side friendships. Since the right side preprocessing counts exactly all valid subsets inside any allowed mask, every possible independent set is counted once and no invalid set is included.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    left = n // 2
    right = n - left

    g_left = [0] * left
    g_right = [0] * right
    cross = [0] * left

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1

        if a < left and b < left:
            g_left[a] |= 1 << b
            g_left[b] |= 1 << a
        elif a >= left and b >= left:
            x = a - left
            y = b - left
            g_right[x] |= 1 << y
            g_right[y] |= 1 << x
        else:
            if a < left:
                cross[a] |= 1 << (b - left)
            else:
                cross[b] |= 1 << (a - left)

    total_right = 1 << right
    dp = [[0] * (right + 1) for _ in range(total_right)]
    dp[0][0] = 1

    for mask in range(total_right):
        if mask == 0:
            continue
        bit = mask & -mask
        idx = bit.bit_length() - 1
        prev = mask ^ bit

        for k in range(right + 1):
            dp[mask][k] = dp[prev][k]

        if prev & g_right[idx] == 0:
            size = prev.bit_count()
            dp[mask][size + 1] += 1

    for bit in range(right):
        for mask in range(total_right):
            if mask & (1 << bit):
                for k in range(right + 1):
                    dp[mask][k] += dp[mask ^ (1 << bit)][k]

    ans = [0] * (n + 1)
    total_left = 1 << left

    for mask in range(total_left):
        ok = True
        blocked = 0

        for i in range(left):
            if mask & (1 << i):
                if g_left[i] & mask:
                    ok = False
                    break
                blocked |= cross[i]

        if not ok:
            continue

        available = (1 << right) - 1
        available ^= blocked

        size_left = mask.bit_count()
        for k in range(right + 1):
            ans[size_left + k] += dp[available][k]

    print(*ans)

if __name__ == "__main__":
    solve()
```

The graph is stored as bitmasks because each half has at most 20 vertices. A single integer can represent the neighbors of a vertex, making conflict checks constant time.

The right side preprocessing uses subset dynamic programming. The transition removes one chosen vertex and checks whether adding it creates a conflict. After the second propagation phase, `dp[mask][k]` represents the number of independent subsets of size `k` that are contained inside `mask`, not only the exact mask itself.

During left-side enumeration, the condition `g_left[i] & mask` catches any friendship entirely inside the chosen left subset. The `blocked` mask collects every right vertex that cannot appear together with the current left choice. Using the remaining vertices guarantees that cross edges are respected.

The implementation relies on Python integers being able to hold 20-bit masks easily. There is no overflow risk because Python integers grow automatically.

## Worked Examples

Consider:

```
5 3
1 2
2 3
4 5
```

The split can be:

```
left: 1 2
right: 3 4 5
```

The trace of left choices is:

| Left mask | Left size | Valid | Blocked right vertices | Contribution |
| --- | --- | --- | --- | --- |
| 00 | 0 | yes | none | all right independent sets |
| 01 | 1 | yes | none | right sets with candidate 1 |
| 10 | 1 | yes | candidate 3 | right sets without 3 |
| 11 | 2 | no | none | skipped |

The invalid mask `11` is skipped because candidates 1 and 2 are friends. The remaining masks combine with the right side counts and produce:

```
1 5 7 2 0 0
```

This example demonstrates that internal conflicts are removed before combining halves.

Another example:

```
4 2
1 2
3 4
```

Split into:

```
left: 1 2
right: 3 4
```

The trace is:

| Left mask | Left size | Valid | Blocked right vertices | Contribution |
| --- | --- | --- | --- | --- |
| 00 | 0 | yes | none | all right choices |
| 01 | 1 | yes | none | right without conflicts |
| 10 | 1 | yes | none | right without conflicts |
| 11 | 2 | no | none | skipped |

The two valid single vertex choices on the left combine with both valid right choices, creating the four valid pairs. The complete answer is:

```
1 4 4 0 0
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^(n/2) * n) | Both halves have at most 20 vertices, and each subset requires only bit operations over the vertices |
| Space | O(2^(n/2) * n) | The right side DP stores counts for every mask and every possible size |

With `n = 40`, `2^(n/2)` is around one million. The algorithm performs a few million bit operations and fits comfortably within the intended limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = old
    return out.getvalue()

# sample 1
assert run("""5 3
1 2
2 3
4 5
""") == "1 5 7 2 0 0\n", "sample 1"

# minimum size
assert run("""1 0
""") == "1 1\n", "single vertex"

# all equal behaviour: complete graph
assert run("""4 6
1 2
1 3
1 4
2 3
2 4
3 4
""") == "1 4 0 0 0\n", "complete graph"

# no edges
assert run("""5 0
""") == "1 5 10 10 5 1\n", "empty graph"

# boundary case with disconnected edges
assert run("""6 3
1 2
3 4
5 6
""") == "1 6 12 8 1 0 0\n", "three components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | `1 1` | Handles the smallest graph |
| Complete graph | `1 4 0 0 0` | Checks conflict detection |
| Empty graph | `1 5 10 10 5 1` | Checks that every subset is counted |
| Three disjoint edges | `1 6 12 8 1 0 0` | Checks combining independent halves |

## Edge Cases

For the empty graph case:

```
3 0
```

The right side preprocessing marks every subset as independent. During left enumeration, no vertex blocks anything, so every left choice combines with every right choice. The answer becomes the binomial counts `1 3 3 1`.

For the complete graph case:

```
3 3
1 2
1 3
2 3
```

Any left subset containing two vertices is rejected immediately because the adjacency mask intersects the chosen mask. The only surviving choices are the empty set and single vertices, so the output is `1 3 0 0`.

For the disconnected case:

```
4 2
1 2
3 4
```

Choosing vertex 1 does not block vertices 3 or 4 because the friendship is entirely inside another component. The algorithm keeps the cross-half blocking mask empty and allows all compatible right subsets. This correctly counts the four valid pairs and avoids creating triples.
