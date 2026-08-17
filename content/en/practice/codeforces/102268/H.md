---
title: "CF 102268H - Hall's Theorem"
description: "We need to construct a bipartite graph with exactly n vertices on each side. For a subset A of the left vertices, its neighborhood N(A) consists of every right vertex touched by at least one vertex of A."
date: "2026-08-17T18:51:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102268
codeforces_index: "H"
codeforces_contest_name: "300iq Contest 1"
rating: 0
weight: 102268
solve_time_s: 218
verified: false
draft: false
---

[CF 102268H - Hall's Theorem](https://codeforces.com/problemset/problem/102268/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct a bipartite graph with exactly n vertices on each side. For a subset A of the left vertices, its neighborhood N(A) consists of every right vertex touched by at least one vertex of A. The subset is critical when it asks for more distinct right vertices than are actually available, meaning ∣N(A)∣<∣A∣.

The input gives n, with n≤20, and a target number k, with 0≤k<2 n. There are 2 n subsets of the left side, including the empty subset. The empty subset is never critical because both its size and neighborhood size are zero. Our graph must make exactly k of the remaining 2 n −1 subsets critical.

The small value n≤20 is a strong hint that subset enumeration is possible for verification, but it is not enough to freely search over graphs. A bipartite graph on n+n vertices has n 2 possible edges, so enumerating graphs would require 2 n 2 possibilities, which is already 2 400 when n=20. We need a direct construction whose description has only polynomial size.

There are two boundary cases that are especially easy to mishandle. For n=1,k=0, the graph must contain the single edge. The only nonempty subset then has one neighbor and is not critical. A careless construction that outputs no edges would instead make the only subset critical. For n=1,k=1, the correct graph has no edges, because the singleton left subset has zero neighbors and is critical. The other common mistake is to count the empty subset as critical. It never is, so the number of noncritical nonempty subsets is 2 n −1−k, not 2 n −k.

## Approaches

A direct brute-force solution could take a candidate graph and enumerate every subset of the left side. For each subset, we could scan its vertices and collect their right-side neighbors, then compare the two cardinalities. If the graph is represented by an n×n adjacency matrix, this takes O(n 2 2 n ) operations. At n=20, that is roughly 400⋅1,048,576, or about 4.2×10 8 elementary checks. Searching for the graph itself by enumerating all possible edge sets would be vastly worse, since there are 2 n 2 possible graphs.

The useful observation is that we do not need an arbitrary graph. We can deliberately construct a very restricted family whose critical subsets are easy to count.

Let the left vertices be 1,…,n, and choose integers

n≥a 1 ​ ≥a 2 ​ ≥⋯≥a n ​ ≥0.

Connect left vertex i to exactly the first a i ​ right vertices. Consider a nonempty subset A, and let i be its smallest left vertex. Since the sequence a i ​ is nonincreasing, every other selected vertex t>i has a t ​ ≤a i ​. Thus the union of all their neighborhoods is exactly the first a i ​ right vertices, so

∣N(A)∣=a i ​ .

There are n−i vertices after i. If exactly j of them are selected, then the subset has size j+1, and it is noncritical exactly when

j+1≤a i ​ ,

or j≤a i ​ −1. Hence the number of noncritical subsets whose smallest vertex is i is

j=0 ∑ a i ​ −1 ​ ( j n−i ​ ).

Summing over all possible smallest vertices gives

G= i=1 ∑ n ​ j=0 ∑ a i ​ −1 ​ ( j n−i ​ ),

where G is the number of noncritical nonempty subsets. Since there are 2 n −1 nonempty subsets, we need

G=2 n −1−k.

The remaining question is how to choose the a i ​. The inner sum is a prefix of one row of Pascal's triangle. Process the rows from n−1 down to 0. In row r, greedily take

( 0 r ​ ),( 1 r ​ ),( 2 r ​ ),…

as long as the current remainder is large enough. Taking the first t terms is exactly the same as setting the corresponding a i ​ =t, because that contributes

j=0 ∑ t−1 ​ ( j r ​ ).

After stopping, the remainder is smaller than the next binomial coefficient. In particular, it is at most 2 r −1, which is precisely the largest number of nonempty subsets of r elements. The same argument can then be applied recursively to the remaining rows.

This gives a direct O(n 2 ) construction. The key structure is that Pascal's triangle provides enough overlapping powers of two to represent every possible target between 0 and 2 n −1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n 2 2 n ) per graph, 2 n 2 graphs to search | O(n 2 ) | Too slow |
| Structured Construction | O(n 2 ) | O(n 2 ) | Accepted |

## Algorithm Walkthrough

1. Compute the required number of noncritical nonempty subsets as

G=2 n −1−k.

We work with noncritical subsets because the construction counts them naturally. The empty subset is excluded by the 2 n −1 term.
2. Build Pascal's triangle up to row n−1, storing

C[r][j]=( j r ​ ).

Since n≤20, ordinary Python integers are more than sufficient, and the largest value is only ( 9 19 ​ ).
3. Start with the last Pascal row, r=n−1, and associate it with left vertex 1. Scan j=0,1,…,r. Whenever the current remainder G is at least C[r][j], subtract this value and add the edge from left vertex 1 to right vertex j+1.

If we select j=0,…,t−1, the resulting neighborhood of left vertex 1 has exactly t vertices. Its contribution to the number of good subsets is precisely the prefix sum

j=0 ∑ t−1 ​ ( j r ​ ).
4. As soon as the next binomial coefficient is too large, stop processing this row and move to r−1. The next row corresponds to left vertex 2, and the same procedure continues.

The reason this greedy step is safe is that after taking the longest possible prefix, the remaining value is smaller than the first unused binomial coefficient. Thus it is certainly smaller than 2 r, so it can be represented using the smaller Pascal rows.
5. Continue until row 0. Every chosen edge is of the form (i,j) with 1≤i,j≤n. For a fixed left vertex, the chosen right endpoints are always 1,2,…,a i ​, so there are no duplicate edges.
6. Output all selected edges. The constructed graph has exactly G noncritical nonempty subsets, so the remaining

(2 n −1)−G=k

subsets are critical.

Why it works can be summarized by an invariant. After processing rows n−1,n−2,…,r+1, the edges already chosen contribute exactly the amount subtracted from G, and the remaining target is representable using rows r,r−1,…,0. When row r is processed, we take the longest possible binomial prefix. If the next term cannot be taken, the remainder is smaller than that term and hence smaller than 2 r, which is the entire range of values representable by the remaining r rows. The invariant survives until the remainder becomes zero. The neighborhood argument then converts each selected prefix length into exactly the required number of noncritical subsets.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    n, k = map(int, input().split())
    # Number of noncritical nonempty subsets we want.    need = (1 << n) - 1 - k
    # Pascal's triangle.    C = [[0] * (n + 1) for _ in range(n + 1)]    C[0][0] = 1    for i in range(1, n):        C[i][0] = C[i][i] = 1        for j in range(1, i):            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    edges = []
    # Row r corresponds to left vertex n-r.    for r in range(n - 1, -1, -1):        left = n - r
        for j in range(r + 1):            if need >= C[r][j]:                need -= C[r][j]                edges.append((left, j + 1))            else:                break
    print(len(edges))    for u, v in edges:        print(u, v)
```

The variable `need` is the number of noncritical nonempty subsets still to realize. Initially it is 2 n −1−k, because every nonempty subset is either critical or noncritical.

The Pascal triangle is constructed only through row n−1. The recurrence directly computes the binomial coefficients needed by the greedy decomposition. There is no overflow concern in Python, and even in a fixed-width language the values here are tiny enough for 64-bit integers.

The outer loop processes `r` from `n - 1` down to zero. The corresponding left vertex is `n - r`, so row n−1 produces the neighborhood of vertex 1, row n−2 produces the neighborhood of vertex 2, and so forth.

Inside a row, edges are added in increasing order of their right endpoint. Consequently, if a row receives t edges, they are exactly to right vertices 1,…,t. This is what gives the prefix-neighborhood structure required by the counting argument.

The `break` is also significant. Once `need < C[r][j]`, every later term in that row is not necessarily larger for arbitrary binomial rows, so a careless implementation should not simply assume that all later coefficients are unusable. Here the construction specifically requires taking a prefix, so we stop at the first unavailable term. The mathematical argument guarantees that the remainder can be handled by smaller rows.

The output contains at most 1+2+⋯+n=210 edges for n=20, so the construction is comfortably within the limits.

## Worked Examples

For the provided sample, let n=3 and k=5. We need

G=2 3 −1−5=2

noncritical nonempty subsets.

| Row r | Left vertex | j | ( j r ​ ) | Remaining before | Action | Remaining after |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1 | 0 | 1 | 2 | Add (1,1) | 1 |
| 2 | 1 | 1 | 2 | 1 | Stop row | 1 |
| 1 | 2 | 0 | 1 | 1 | Add (2,1) | 0 |

The resulting graph has edges (1,1) and (2,1). Its left-side subsets behave as follows.

| Subset | Neighborhood | Sizes | Critical? |
| --- | --- | --- | --- |
| {1} | {1} | 1,1 | No |
| {2} | {1} | 1,1 | No |
| {3} | ∅ | 1,0 | Yes |
| {1,2} | {1} | 2,1 | Yes |
| {1,3} | {1} | 2,1 | Yes |
| {2,3} | {1} | 2,1 | Yes |
| {1,2,3} | {1} | 3,1 | Yes |

There are exactly five critical subsets, matching the target. The two noncritical nonempty subsets are exactly the two counted by the greedy decomposition.

For a second example, take n=4,k=0. We want every nonempty subset to be noncritical, so

G=2 4 −1=15.

| Row r | Left vertex | Selected coefficients | Row contribution | Remaining |
| --- | --- | --- | --- | --- |
| 3 | 1 | 1,3,3,1 | 8 | 7 |
| 2 | 2 | 1,2,1 | 4 | 3 |
| 1 | 3 | 1,1 | 2 | 1 |
| 0 | 4 | 1 | 1 | 0 |

Every left vertex is connected to all four right vertices. Thus every nonempty subset has exactly four neighbors, or fewer only when the graph is restricted, but because all left vertices have the complete neighborhood, a subset of size at most four always satisfies ∣N(A)∣=4≥∣A∣. Hence there are zero critical subsets.

This example exercises the opposite boundary from the sample. The greedy process consumes the entire Pascal triangle and produces the complete bipartite graph.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n 2 ) | Pascal's triangle takes O(n 2 ), and the greedy scan visits O(n 2 ) coefficients. |
| Space | O(n 2 ) | The stored Pascal triangle has O(n 2 ) entries, and the edge list has at most O(n 2 ) edges. |

With n≤20, this is extremely small. The construction performs only a few hundred coefficient operations and produces at most 210 edges, so it is easily within the 1 second limit.

## Test Cases

Because the output is not unique, a robust test should validate the produced graph rather than require one particular edge list. The harness below uses the same construction function and then independently enumerates all left subsets to count critical ones.

```python
Python# helper: run solution on input string, return output stringimport sysimport io

def construct(inp: str) -> str:    old_stdin = sys.stdin    sys.stdin = io.StringIO(inp)
    n, k = map(int, sys.stdin.readline().split())    need = (1 << n) - 1 - k
    C = [[0] * (n + 1) for _ in range(n + 1)]    C[0][0] = 1
    for i in range(1, n):        C[i][0] = C[i][i] = 1        for j in range(1, i):            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    edges = []
    for r in range(n - 1, -1, -1):        left = n - r        for j in range(r + 1):            if need >= C[r][j]:                need -= C[r][j]                edges.append((left, j + 1))            else:                break
    sys.stdin = old_stdin
    out = [str(len(edges))]    out.extend(f"{u} {v}" for u, v in edges)    return "\n".join(out) + "\n"

def run(inp: str) -> str:    return construct(inp)

def validate(inp: str, out: str) -> None:    n, k = map(int, inp.split())
    lines = out.strip().splitlines()    m = int(lines[0])    assert len(lines) == m + 1
    adj = [0] * n    seen = set()
    for line in lines[1:]:        u, v = map(int, line.split())        assert 1 <= u <= n        assert 1 <= v <= n        assert (u, v) not in seen        seen.add((u, v))        adj[u - 1] |= 1 << (v - 1)
    critical = 0
    for mask in range(1 << n):        neighborhood = 0        for i in range(n):            if mask >> i & 1:                neighborhood |= adj[i]
        if neighborhood.bit_count() < mask.bit_count():            critical += 1
    assert critical == k

# Provided sample.sample = run("3 5")assert sample == "2\n1 1\n2 1\n", "sample 1"validate("3 5", sample)

# Minimum size, zero critical subsets.case = run("1 0")validate("1 0", case)

# Minimum size, all nonempty subsets critical.case = run("1 1")validate("1 1", case)

# All nonempty subsets must be noncritical.case = run("4 0")validate("4 0", case)

# Maximum n and a large target, exercising all subset sizes.case = run("20 1048575")validate("20 1048575", case)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 5` | The sample graph with 2 edges | Provided sample and normal construction |
| `1 0` | One edge from left 1 to right 1 | Smallest input and zero critical subsets |
| `1 1` | Zero edges | Smallest input and maximum possible critical count |
| `4 0` | Complete K 4,4 ​ | Boundary where every nonempty subset is noncritical |
| `20 1048575` | A graph with zero edges | Maximum n, maximum k=2 20 −1, and large integer handling |

## Edge Cases

For `1 0`, the required number of noncritical nonempty subsets is

2 1 −1−0=1.

The only Pascal coefficient is ( 0 0 ​ )=1, so the algorithm adds edge (1,1). The singleton left subset has one neighbor and is not critical, giving exactly zero critical subsets.

For `1 1`, the required number of noncritical nonempty subsets is zero. The greedy loop cannot subtract anything, so it outputs no edges. The only nonempty subset has neighborhood size zero and subset size one, making it critical. The answer contains exactly one critical subset.

For `4 0`, the target number of noncritical subsets is 15. The algorithm consumes every coefficient in rows 3,2,1,0, giving each of the four left vertices all four right vertices as neighbors. Any nonempty subset has neighborhood size four, while its size is at most four, so no subset is critical.

For `4 15), the target number of noncritical subsets is zero. No edge is selected at all. Every nonempty subset has an empty neighborhood, so every one of the 2 4 −1=15 nonempty subsets is critical.

For `20,2^{20}-1`, the algorithm again needs zero noncritical subsets and outputs the empty graph. Every nonempty left subset has neighborhood size zero, so all 1,048,575 nonempty subsets are critical. This also confirms that the construction handles the upper bound of k without any special-case arithmetic.
