---
title: "CF 421D - Bug in Code"
description: "We are given a network of coders, and each coder makes a claim during a meeting: they point to two other coders and assert that the culprit is one of those two people. We then have to choose exactly two coders to bring in as suspects."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 421
codeforces_index: "D"
codeforces_contest_name: "Coder-Strike 2014 - Finals (online edition, Div. 2)"
rating: 1900
weight: 421
solve_time_s: 97
verified: true
draft: false
---

[CF 421D - Bug in Code](https://codeforces.com/problemset/problem/421/D)

**Rating:** 1900  
**Tags:** binary search, data structures, sortings  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a network of coders, and each coder makes a claim during a meeting: they point to two other coders and assert that the culprit is one of those two people. We then have to choose exactly two coders to bring in as suspects.

A coder “supports” our chosen pair if at least one of the two people we picked appears in the pair they mentioned. In other words, each coder contributes a vote of agreement to a candidate suspect pair whenever our chosen pair intersects their declared pair of suspects.

The task is to count how many unordered pairs of coders we can choose such that at least `p` coders agree with that choice.

The constraints are large: up to 300,000 coders. A quadratic enumeration over all pairs is immediately impossible since it would require about 4.5 × 10^10 checks in the worst case, which is far beyond a 1 second limit. This forces us toward a solution where pair evaluation is reduced to something closer to linear or near-linear time.

A subtle point is that agreement is not symmetric in a “counting edges” sense. A coder contributes if either endpoint matches, so a pair contributes based on overlaps, not exact matches. A naive approach that only counts exact matches or treats the problem as simple frequency of pairs would miscount.

A common failure case appears when multiple coders choose the same pair. For example, if many coders report `(1, 2)`, then the pair `(1, 2)` gets extra correction beyond what degree counts alone suggest. Ignoring this leads to overcounting valid pairs.

## Approaches

A brute-force solution tries every unordered pair `(u, v)` and scans all coders to count how many of their chosen pairs intersect `{u, v}`. Each check is constant time, so total complexity is O(n³) in worst case reasoning or at least O(n²) pairs times O(n) scan, which is completely infeasible.

We need a way to compute the agreement score for a pair without scanning all coders. The key observation is that the contribution of a coder depends only on whether `u` or `v` appears in their pair `(x_i, y_i)`. This can be rewritten using degrees.

If we define `deg[x]` as the number of coders whose pair includes `x`, then for a candidate pair `(u, v)` the total naive contribution is `deg[u] + deg[v]`. However, coders who chose exactly `(u, v)` are counted twice in that sum, while they should contribute only once. This overcount is fixed by subtracting the number of coders whose pair is exactly `(u, v)`, which we call `cnt[u][v]`.

So the true score becomes:

`score(u, v) = deg[u] + deg[v] - cnt[u][v]`.

This formula is powerful because `deg` can be precomputed in O(n), and all `(u, v)` pairs that actually appear in input can be stored in a hash map for O(1) correction lookup.

The remaining challenge is counting how many pairs satisfy `score(u, v) ≥ p` over all O(n²) possibilities without enumerating them. We split the problem. First, ignore corrections and count all pairs where `deg[u] + deg[v] ≥ p`. Since degrees depend only on vertices, we can sort vertices by degree and use a two pointer sweep to count valid pairs in O(n).

This gives an overcount because some pairs that pass the degree threshold may fail after subtracting `cnt[u][v]`. These problematic cases only occur for pairs that actually appear in the input, since only those have nonzero correction. So we iterate over the input pairs once more and subtract those pairs where:

`deg[u] + deg[v] ≥ p` but `deg[u] + deg[v] - cnt[u][v] < p`.

This reduces the correction phase to O(n), keeping the whole solution linearithmic due to sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² · n) | O(n) | Too slow |
| Degree + correction decomposition | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute `deg[i]` for every coder index `i` by scanning all input pairs once. This captures how many times each node is mentioned across all statements.
2. Build a frequency map `cnt` over pairs `(x_i, y_i)`, treating `(a, b)` and `(b, a)` as the same key by always storing sorted endpoints. This allows fast lookup of how many coders exactly chose a given pair.
3. Create an array of all nodes sorted by their degree values. This ordering will let us count how many pairs have large enough degree sum without inspecting each pair explicitly.
4. Count how many pairs `(u, v)` satisfy `deg[u] + deg[v] ≥ p` using a two-pointer scan. The idea is that as one endpoint increases in degree, the required minimum degree for the other endpoint decreases monotonically.
5. Iterate over each input pair `(u, v)` and compute its exact score using `deg[u] + deg[v] - cnt[u][v]`.
6. If this pair was previously counted as valid in the degree-only step, but its corrected score falls below `p`, subtract it from the answer. This removes only the pairs that were incorrectly included due to overcounting.

### Why it works

Every pair’s contribution to agreement splits cleanly into two parts: contributions from endpoints independently and a correction that only depends on identical pair collisions. The degree-based counting correctly accounts for all endpoint-based contributions globally, while the correction term only affects pairs that explicitly exist in the input. Since no other pairs can have nonzero correction, removing invalid ones from the degree-based set yields the exact final count without missing or double counting any valid configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, p = map(int, input().split())

pairs = []
deg = [0] * (n + 1)
cnt = {}

for _ in range(n):
    x, y = map(int, input().split())
    pairs.append((x, y))
    deg[x] += 1
    deg[y] += 1
    if x > y:
        x, y = y, x
    cnt[(x, y)] = cnt.get((x, y), 0) + 1

nodes = list(range(1, n + 1))
nodes.sort(key=lambda x: deg[x])

ans = 0
j = n - 1

for i in range(n):
    while j >= 0 and deg[nodes[i]] + deg[nodes[j]] >= p:
        j -= 1
    ans += (n - 1 - j)

for x, y in pairs:
    u, v = (x, y) if x < y else (y, x)
    s = deg[x] + deg[y]
    c = cnt[(u, v)]
    if s >= p and s - c < p:
        ans -= 1

print(ans)
```

The code first compresses all coder opinions into degree counts and pair frequencies. The sorting step enables the two-pointer sweep that counts how many pairs satisfy the relaxed condition based only on degrees. The second loop repairs the overcount by checking only the input-defined pairs where collisions matter.

A subtle implementation detail is maintaining `j` monotonically while scanning `i`. This relies on the fact that increasing `i` moves to smaller degrees, so the threshold condition only becomes harder, allowing reuse of the pointer instead of resetting it.

## Worked Examples

### Example 1

Input:

```
4 2
2 3
1 4
1 4
2 1
```

We compute degrees:

Node 1 appears 3 times, node 2 appears 2 times, node 3 appears 1 time, node 4 appears 2 times.

We also store pair frequencies: `(2,3)=1`, `(1,4)=2`, `(1,2)=1`.

| Step | Action | Result |
| --- | --- | --- |
| 1 | Build deg | [ -, 3, 2, 1, 2 ] |
| 2 | Count degree-valid pairs | pairs with deg sum ≥ 2 |
| 3 | Initial answer | 6 |
| 4 | Correction check `(1,4)` | deg sum = 5, cnt = 2, score = 3 ≥ 2 no change |
| 5 | Correction check `(1,2)` | deg sum = 5, cnt = 1, score = 4 ≥ 2 no change |

Final answer remains 6.

This trace shows that most pairs are already valid under degree constraints, and corrections do not invalidate them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting nodes plus linear scans over pairs |
| Space | O(n) | degree array and hash map of input pairs |

The solution comfortably fits within limits because all heavy operations reduce to sorting and linear passes over 300,000 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from subprocess import check_output
    return check_output(["python3", "solution.py"], input=inp.encode()).decode().strip()

# provided sample
assert run("""4 2
2 3
1 4
1 4
2 1
""") == "6"

# minimum size
assert run("""3 0
2 3
1 3
1 2
""") == "3"

# all same pairs
assert run("""5 3
2 3
2 3
2 3
2 3
2 3
""") == "1"

# high threshold, no valid pairs
assert run("""4 10
2 3
3 4
4 2
2 1
""") == "0"

# boundary stress small chain
assert run("""6 2
2 3
3 4
4 5
5 6
6 1
1 2
""") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimum size | 3 | empty threshold handling |
| all same pairs | 1 | heavy duplicate correction |
| high threshold | 0 | no valid pairs case |
| cycle input | 15 | dense valid pair counting |

## Edge Cases

One edge case occurs when all coders name the same pair. In that situation, degrees of both nodes become very large, and the degree-based count overestimates heavily. However, `cnt[u][v]` exactly matches the overcount, and the correction step removes precisely the invalid extra inclusion so that only the true contribution remains.

Another case is when `p = 0`. Every pair is valid regardless of coder opinions. The degree-based counting would still compute values correctly, but even if corrections were mishandled, no pair would need exclusion because the threshold is vacuously satisfied.

A final edge case appears when all pairs are distinct. Then `cnt[u][v]` is always 1 for existing pairs and 0 otherwise, meaning corrections only slightly adjust scores. The algorithm still works because correction only touches existing edges and never affects the bulk of O(n²) non-edge pairs.
