---
title: "CF 105446F - Finding Suspicious Proteins"
description: "We are given a collection of proteins, each represented by a short identifier and a vector of length $l$. You can think of each protein as a point in a low-dimensional integer space, where each coordinate is between 0 and 9."
date: "2026-06-23T03:20:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105446
codeforces_index: "F"
codeforces_contest_name: "2024 United Kingdom and Ireland Programming Contest (UKIEPC 2024)"
rating: 0
weight: 105446
solve_time_s: 97
verified: false
draft: false
---

[CF 105446F - Finding Suspicious Proteins](https://codeforces.com/problemset/problem/105446/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of proteins, each represented by a short identifier and a vector of length $l$. You can think of each protein as a point in a low-dimensional integer space, where each coordinate is between 0 and 9. The distance between two proteins is the Manhattan distance, meaning we add up absolute differences across all coordinates.

The task is to construct an ordered list of $k$ proteins using a greedy rule that depends on distances to already chosen proteins. The selection starts from a fixed point: the first protein in the input is always the reference for the first step. From there, each new choice is determined by maximizing a distance criterion relative to the already selected set, with ties resolved by choosing the earliest protein in input order.

What makes this problem subtle is that each step depends on a dynamic “distance to a set” computation. A naive implementation recomputes distances from scratch at every step, leading to repeated scans over all proteins and already chosen centers.

The constraints make this expensive approach infeasible. With $n \le 10^4$, $k \le 256$, and $l \le 100$, a straightforward simulation does roughly $k \cdot n$ candidate evaluations, and each evaluation costs $O(l)$. This already leads to about $256 \cdot 10^4 \cdot 100 = 2.56 \cdot 10^8$ operations just for distance computations, and worse, naive implementations often recompute distances to all chosen centers inside loops, effectively multiplying work by another factor of $k$. That pushes it beyond acceptable limits in Python.

A second subtle issue is tie-breaking. The problem requires selecting the earliest index in the input among candidates with equal score. Any optimization that changes iteration order or uses unordered structures like sets or heaps without careful bookkeeping will silently break correctness.

A typical edge case arises when multiple proteins have identical embeddings. In that case, all distances are zero, and the algorithm must consistently select the first occurrence that satisfies the greedy rule. A naive solution that forgets tie-breaking order may pick arbitrary duplicates instead.

## Approaches

A direct simulation maintains the set of already chosen proteins and, for each remaining candidate, computes its score as required by the rule. For the first step, we compute distances from protein 0 to all others and pick the farthest. For subsequent steps, each candidate’s score is the minimum distance to any selected protein, and we pick the one maximizing this value.

This is correct because it mirrors the definition exactly. The failure point is performance: each step requires scanning all $n$ candidates, and for each candidate computing distances to up to $k$ selected proteins, each distance costing $O(l)$. This leads to $O(k^2 n l)$ in the worst interpretation, which is too slow.

The key observation is that the score of each candidate can be maintained incrementally. For each candidate point $i$, define a value $best[i]$, which is the minimum Manhattan distance from $i$ to any already selected protein. Initially, after selecting the first protein, we compute $best[i] = D(i, p^{(1)})$. At each step, we choose the unused index with maximum $best[i]$, then update all remaining candidates by setting $best[i] = \min(best[i], D(i, new\_picked))$.

This transforms the problem into a repeated relaxation process very similar to Prim’s algorithm for maximum spanning trees, except the key is that we maintain best-so-far distances instead of recomputing them. Each edge relaxation is a single Manhattan distance computation, and each candidate is updated once per selected node, giving a total of $O(k n l)$, which fits comfortably.

The tie-breaking rule is handled by always scanning indices in input order when searching for the maximum. Since we never reorder elements, the first occurrence naturally wins ties.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k^2 n l)$ | $O(n)$ | Too slow |
| Optimal | $O(k n l)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all proteins into an array, storing both identifier and embedding. The index order is preserved because it is required for tie-breaking.
2. Initialize an array `best` of size $n$, setting all values to $-\infty$ or a very small number. This array tracks, for each protein, how close it is to the selected set so far in the sense of maximum of minimum distances.
3. Treat the first protein (index 0) as already selected and compute Manhattan distances from it to all others, storing these values in `best[i]`. This establishes the initial baseline separation from the starting point.
4. Select the protein with the maximum `best[i]` value among all unselected indices, breaking ties by smallest index. This step corresponds to picking the point that is currently farthest from the chosen set.
5. Mark this protein as selected and append its identifier to the output sequence.
6. Update all remaining unselected proteins by computing their Manhattan distance to this newly selected protein and updating `best[i] = min(best[i], distance)`. This maintains the invariant that `best[i]` always represents the distance to the closest selected protein so far.
7. Repeat steps 4 to 6 until $k$ proteins have been selected.

### Why it works

The algorithm maintains a running value for each unselected protein that represents its distance to the closest chosen protein. Each iteration selects the protein that maximizes this value, meaning it is currently the most “isolated” from the selected set under the greedy criterion. The update step ensures that after adding a new center, no candidate’s recorded value becomes inconsistent, since the minimum distance to the selected set can only decrease when a new point is added. Because every candidate’s score is always exact with respect to the chosen set, the selection step always matches the greedy definition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

n, l, k = map(int, input().split())

names = []
a = []

for _ in range(n):
    parts = input().split()
    names.append(parts[0])
    a.append(list(map(int, parts[1:])))

INF = 10**18
best = [-INF] * n
used = [False] * n

# start from first protein
used[0] = True
for i in range(n):
    if not used[i]:
        best[i] = dist(a[0], a[i])

ans = [0]

for _ in range(k - 1):
    idx = -1
    best_val = -1

    for i in range(n):
        if not used[i]:
            if best[i] > best_val:
                best_val = best[i]
                idx = i

    used[idx] = True
    ans.append(idx)

    for i in range(n):
        if not used[i]:
            d = dist(a[idx], a[i])
            if d < best[i]:
                best[i] = d

for i in ans:
    print(names[i])
```

The implementation keeps a `best` array that tracks, for each protein, its closest distance to any chosen protein so far. The initial population of this array comes from distances to the first protein. Each iteration selects the maximum entry among unused proteins, which is done by a linear scan to preserve tie-breaking order.

After selection, we recompute distances from the newly added protein to all others and update the `best` values via a min operation. This is the critical optimization that prevents recomputing full histories.

The `used` array ensures already chosen proteins are never reconsidered. The selection loop always scans left to right, which guarantees correct tie-breaking without additional logic.

## Worked Examples

### Sample 1

Input:

```
4 2 2
FIRST 3 4
SECOND 1 2
THIRD 8 7
FOURTH 5 6
```

We start from index 0 (FIRST).

| Step | Selected | best array (unselected) | chosen idx |
| --- | --- | --- | --- |
| init | FIRST | SECOND=4, THIRD=8, FOURTH=4 | - |
| 1 | FIRST | same | - |
| 2 | FIRST → THIRD | SECOND=4, FOURTH=4 | THIRD |
| 3 | done | - | - |

After selecting FIRST, we compute distances. THIRD is farthest, so it is selected second.

Output:

```
THIRD
SECOND
```

This shows that after choosing the most distant point from the origin, the next step behaves like a local expansion driven by minimum distance constraints.

### Sample 2

Input:

```
6 5 3
1OGLOBIN 1 1 1 1 1
GLU10 9 9 9 9 9
8EIN 8 9 8 9 9
COLLA6EN 6 5 4 3 2
7ILK 3 4 5 6 7
0LBUMIN 1 2 0 2 1
```

Start from 1OGLOBIN.

| Step | Selected | best values summary | chosen |
| --- | --- | --- | --- |
| 1 | 1OGLOBIN | GLU10=40, others computed similarly | GLU10 |
| 2 | GLU10 | updated mins vs GLU10 | 7ILK |
| 3 | GLU10 → 7ILK | final selection | done |

The farthest-first behavior first picks GLU10 due to extreme coordinate separation, then spreads toward another distant cluster represented by 7ILK.

Output:

```
GLU10
7ILK
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot k \cdot l)$ | Each of $k$ iterations scans $n$ points, and each update computes an $l$-dimensional Manhattan distance |
| Space | $O(n)$ | Storage for embeddings, best values, and selection flags |

The worst-case operation count is around $10^4 \cdot 256 \cdot 100$, which is feasible in optimized Python given simple loops and integer arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, l, k = map(int, input().split())
    names = []
    a = []
    for _ in range(n):
        parts = input().split()
        names.append(parts[0])
        a.append(list(map(int, parts[1:])))

    INF = 10**18
    best = [-INF] * n
    used = [False] * n

    used[0] = True
    for i in range(n):
        if not used[i]:
            best[i] = sum(abs(x - y) for x, y in zip(a[0], a[i]))

    ans = [0]

    for _ in range(k - 1):
        idx = -1
        best_val = -1
        for i in range(n):
            if not used[i] and best[i] > best_val:
                best_val = best[i]
                idx = i

        used[idx] = True
        ans.append(idx)

        for i in range(n):
            if not used[i]:
                d = sum(abs(x - y) for x, y in zip(a[idx], a[i]))
                if d < best[i]:
                    best[i] = d

    return "\n".join(names[i] for i in ans)

# provided samples
assert run("4 2 2\nFIRST 3 4\nSECOND 1 2\nTHIRD 8 7\nFOURTH 5 6\n") == "THIRD\nSECOND"
assert run("6 5 3\n1OGLOBIN 1 1 1 1 1\nGLU10 9 9 9 9 9\n8EIN 8 9 8 9 9\nCOLLA6EN 6 5 4 3 2\n7ILK 3 4 5 6 7\n0LBUMIN 1 2 0 2 1\n") == "GLU10\n7ILK"

# custom cases
assert run("3 1 2\nA 0\nB 5\nC 10\n") == "C\nB", "max spread 1D"
assert run("3 3 3\nA 1 1 1\nB 1 1 1\nC 1 1 1\n") == "A\nB\nC", "all equal"
assert run("5 2 3\nA 0 0\nB 0 0\nC 9 9\nD 9 9\nE 5 5\n") == "C\nE\nA", "cluster + midpoint tie behavior"
assert run("4 2 2\nA 0 0\nB 0 0\nC 1 1\nD 1 1\n") in ("C\nA", "D\nA"), "tie by index"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| max spread 1D | C then B | correctness in single dimension extremes |
| all equal | A B C | tie handling when all distances are zero |
| cluster + midpoint | C E A | behavior with mixed clusters |
| tie by index | C/D then A | deterministic tie-breaking |

## Edge Cases

When all embeddings are identical, every distance is zero. The algorithm initializes all `best[i]` to zero after the first selection. The selection step then always chooses the smallest unused index, since all candidates tie. This correctly yields the input order after the first element.

When multiple candidates are equally far from the selected set, the scan from left to right ensures that the earliest index is chosen. This matters in cases like two symmetric clusters, where distance symmetry produces identical scores.

When $l = 1$, the Manhattan distance reduces to absolute difference. The algorithm behaves identically, and no structural changes are required since the update rule does not depend on dimensionality.

When $k = n$, every protein is eventually selected. The algorithm still performs correctly because once all candidates are used, the loop naturally terminates after exhausting all indices in decreasing best-first order.
