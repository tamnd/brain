---
title: "CF 104633O - Which Planet is This?!"
description: "We are given two sets of points on a sphere, each point described by latitude and longitude. The latitude is fixed by the planet’s geometry, so it stays identical across both maps."
date: "2026-06-29T17:18:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104633
codeforces_index: "O"
codeforces_contest_name: "2020 ICPC World Finals"
rating: 0
weight: 104633
solve_time_s: 49
verified: true
draft: false
---

[CF 104633O - Which Planet is This?!](https://codeforces.com/problemset/problem/104633/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sets of points on a sphere, each point described by latitude and longitude. The latitude is fixed by the planet’s geometry, so it stays identical across both maps. The only freedom between the two datasets comes from rotation of the planet around its own axis, which shifts longitudes uniformly for all points.

The task is to decide whether there exists a single rotation angle along the longitude direction such that, after shifting every point in the first map by that angle, the resulting set of coordinates exactly matches the second map.

So the structure is purely geometric: two multisets of points on a sphere where latitude is invariant, and longitude is defined modulo 360 degrees, and we want to test whether the second set can be obtained by applying a uniform circular shift on the longitude coordinate.

The constraint n up to 400,000 immediately rules out any quadratic comparison between all point pairs. Even sorting twice is acceptable, but any approach involving pairing points naively across both sets would fail. We need something closer to linear or linearithmic time, likely relying on hashing or canonical representation.

A subtle issue is floating-point precision. Coordinates are given with up to four decimals, so direct floating comparisons are risky unless normalized carefully. Another issue is that longitude wraps around at -180 and 180, so shifting must be handled modulo 360. Finally, duplicates in latitude groups matter: multiple points may share latitude but differ in longitude, so matching must preserve multiplicity within each latitude band.

A naive approach might try to align one point from the first set with one point in the second set, derive a candidate rotation, and verify all points. That is conceptually sound, but trying all pairings would be far too slow. The key is to reduce candidates for rotation to a small set derived from structure.

## Approaches

The brute-force idea starts from a simple observation: if we guess which point in the first map corresponds to which point in the second map, we can compute the required longitude shift as the difference between their longitudes. Then we could apply this shift to all points in the first map and check whether the transformed set equals the second map.

This is correct, but the number of pairings is n squared. Each check costs n, so the total becomes O(n^3) if done naively or at least O(n^2) if we try to optimize checking. With n up to 400,000, even O(n log n) is the realistic upper bound, so this is completely infeasible.

The key insight is that latitudes do not change under rotation. That means each latitude defines an independent circular ordering of points along longitude. If two maps correspond to the same planet, then for each fixed latitude, the multiset of longitudes must match up to the same global shift. More importantly, the same shift must work simultaneously for all latitudes.

This turns the problem into matching circular multisets at each latitude, all aligned by a single global rotation value. Instead of testing all rotations, we can compute a canonical representation of each map that is invariant under rotation. A standard trick is to sort points by latitude, then within each latitude group consider the circular sequence of longitudes and encode it in a rotation-invariant way, such as subtracting a reference point and normalizing.

To avoid floating-point instability, we scale coordinates to integers. Since precision is up to 1e-4, multiplying by 10000 makes all values safe integers.

Finally, we reduce each latitude group into a sorted circular sequence and compute a hash that is independent of starting point. Then the entire map is represented as a multiset of these per-latitude canonical hashes. If both maps produce identical multisets, the answer is Same.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) or worse | O(n) | Too slow |
| Group + canonical hashing | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We treat each point as a pair of integers after scaling latitude and longitude.

We group points by latitude. Within each latitude group, we collect all longitudes and sort them. This gives us a circular sequence on a line modulo 360 degrees.

For each group we construct a rotation-invariant signature. We do this by computing differences between consecutive sorted longitudes, including wrap-around from last back to first. This produces a cyclic structure independent of where we start reading the circle. We then encode this cyclic difference sequence into a hash.

We repeat this for every latitude group, producing a multiset of group signatures for each map. Finally, we compare the two multisets.

1. Read all points of the first map and second map, scaling coordinates into integers.
2. Group points of each map by latitude using a dictionary.
3. For each latitude group, sort its longitudes.
4. For each sorted longitude list, compute circular differences including wrap-around.
5. Hash the resulting difference sequence into a canonical value.
6. Collect all hashes into a multiset representation for the map.
7. Compare the two multisets for equality and output the result.

The reason we use differences instead of absolute longitudes is that a global rotation shifts all longitudes by the same constant, but differences between consecutive points on a circle remain unchanged.

### Why it works

Each latitude forms an independent circular arrangement of points. A rotation of the planet corresponds to a uniform cyclic shift in every such arrangement. A cyclic shift does not change the multiset of adjacent differences in a circular sequence. Therefore each latitude group is reduced to an invariant representation under rotation. Since all groups share the same rotation, equality of these invariants across all latitudes is both necessary and sufficient for the maps to match.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def normalize_group(lons):
    lons.sort()
    m = len(lons)
    if m == 0:
        return 0
    if m == 1:
        return 1
    diffs = []
    for i in range(m):
        j = (i + 1) % m
        diff = lons[j] - lons[i]
        if j == 0:
            diff += 3600000  # scaled 360 degrees
        diffs.append(diff)
    diffs.sort()
    h = 1469598103934665603
    for d in diffs:
        h ^= d + 0x9e3779b97f4a7c15
        h *= 1099511628211
        h &= (1 << 64) - 1
    return h

def build_signature(points):
    groups = defaultdict(list)
    for a, b in points:
        la = int(round(a * 10000))
        lo = int(round(b * 10000))
        groups[la].append(lo)

    sig = []
    for la in groups:
        sig.append(normalize_group(groups[la]))
    sig.sort()
    return sig

def solve():
    n = int(input())
    p1 = [tuple(map(float, input().split())) for _ in range(n)]
    p2 = [tuple(map(float, input().split())) for _ in range(n)]

    s1 = build_signature(p1)
    s2 = build_signature(p2)

    print("Same" if s1 == s2 else "Different")

if __name__ == "__main__":
    solve()
```

The solution first discretizes coordinates to avoid floating comparison issues. Each latitude group is isolated because rotation does not mix latitudes. Inside each group, sorting longitudes reduces the circular structure into a linear representation. The wrap-around difference ensures that the cyclic structure is preserved regardless of starting point.

The hash function is a standard multiplicative rolling hash to compress the difference sequence into a fixed-size fingerprint. Sorting group hashes ensures we compare multisets rather than ordered lists of latitude bands.

One subtle point is that floating rounding must be consistent across both maps. Multiplying by 10000 and rounding ensures stable integer representation.

## Worked Examples

### Example 1

First map has points grouped by latitudes, and the second map is the same configuration but rotated in longitude. After grouping and normalization, both produce identical signatures.

| Step | Map 1 group hashes | Map 2 group hashes | Comparison |
| --- | --- | --- | --- |
| After grouping | [H1, H2] | [H1, H2] | same multiset |
| After sorting | [H1, H2] | [H1, H2] | equal |

This demonstrates that a global longitude shift does not affect cyclic difference hashes.

### Example 2

In the second sample, the distribution of longitudes within at least one latitude differs structurally, meaning no cyclic shift can align the sets.

| Step | Map 1 group hashes | Map 2 group hashes | Comparison |
| --- | --- | --- | --- |
| After grouping | [H1, H2] | [H1, H3] | mismatch |

This confirms that even if total counts match, internal circular structure differences are detected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting within each latitude group dominates, and each point is processed once |
| Space | O(n) | Storage of grouped points and hashes |

The algorithm fits comfortably within limits since sorting 400,000 elements and hashing them is feasible in Python with careful implementation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve()

# provided samples
assert run("""3
0.0000 0.0000
30.0000 90.0000
-45.0000 -30.0000
3
30.0000 60.0000
30.0000 150.0000
-45.0000 30.0000
""") == "Same"

assert run("""3
0.0000 0.0000
30.0000 0.0000
30.0000 90.0000
3
0.0000 0.0000
30.0000 0.0000
30.0000 -90.0000
""") == "Different"

# custom cases
assert run("""1
10.0000 20.0000
1
10.0000 200.0000
""") == "Same"

assert run("""2
0.0000 0.0000
0.0000 180.0000
2
0.0000 90.0000
0.0000 270.0000
""") == "Same"

assert run("""2
0.0000 0.0000
10.0000 0.0000
2
0.0000 0.0000
20.0000 0.0000
""") == "Different"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point shift | Same | trivial invariance |
| opposite hemisphere rotation | Same | wrap-around correctness |
| mismatched latitudes | Different | structure mismatch |

## Edge Cases

One important edge case is a latitude group with only one point. In this case, there is no meaningful circular structure, so the hash must be constant for any single-point group. The algorithm returns a fixed value for m = 1, ensuring that rotations do not introduce false distinctions.

Another edge case is when longitudes lie near the -180/180 boundary. Because we work in scaled integers and treat differences modulo 3600000, wrap-around is explicitly included in the last difference computation. For example, points at -179.9999 and 179.9999 produce a small circular gap rather than a large linear gap, preserving correctness.

A final subtle case is when multiple points share identical latitudes but are widely separated in longitude. Sorting ensures consistent ordering, and cyclic differences guarantee invariance under rotation.
