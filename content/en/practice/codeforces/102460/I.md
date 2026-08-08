---
title: "CF 102460I - The Spectrum"
description: "We need to reconstruct an increasing integer array (X) from all pairwise distances between its elements. The first element is fixed at zero, and every element is between zero and 999."
date: "2026-08-08T10:13:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102460
codeforces_index: "I"
codeforces_contest_name: "2019-2020 ICPC Asia Taipei-Hsinchu Regional Contest"
rating: 0
weight: 102460
solve_time_s: 164
verified: true
draft: false
---

[CF 102460I - The Spectrum](https://codeforces.com/problemset/problem/102460/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to reconstruct an increasing integer array (X) from all pairwise distances between its elements. The first element is fixed at zero, and every element is between zero and 999. For every pair of positions (i<j), the spectrum contains the value (x_j-x_i), including repeated values. The input gives these (\frac{n(n-1)}2) distances in sorted order, and the task is to find every array that could have produced exactly that multiset.

For example, the spectrum (1,2,3) for (n=3) can come from either (0,1,3) or (0,2,3). These arrays are different, but their pairwise distances are the same. We must output both, in lexicographic order.

The upper bound (n\le62) means the spectrum contains at most (\frac{62\cdot61}{2}=1891) values. That is small enough for us to maintain a frequency table indexed by distance. The coordinate bound of 999 is even more useful: every distance belongs to the tiny range from 1 through 999, so checking and locating remaining distances can be done with a fixed-size array rather than a balanced tree or hash table. The search itself cannot be polynomial in the general turnpike problem, so the solution has to exploit the structure of the largest remaining distance to make the branching extremely small.

The first non-obvious case is (n=2). There is only one distance. For input `2` followed by `7`, the only answer is `0 7`. A recursive implementation that assumes there is an interior point to reconstruct would fail here.

The second case is an invalid spectrum whose largest value exceeds the coordinate limit. For example,

```
2
1000
```

has no valid answer because the only possible array would be `0 1000`, which violates the bound (x_i\le999). A careless implementation might reconstruct the endpoints without checking the coordinate constraint.

Repeated distances also need to be treated as a multiset. For example,

```
4
2 2 2 4 4 6
```

has the answer `0 2 4 6`. The value 2 occurs three times because three different pairs are separated by two. Treating the spectrum as a set would lose this information and could accept invalid arrays.

A particularly important case is when the largest currently unexplained distance occurs twice and is exactly half of the total width. For

```
5
1 1 1 1 2 2 2 3 3 4
```

the answer is `0 1 2 3 4`. The distance 2 occurs twice between the endpoints and the middle point, but there is only one middle coordinate, namely 2. A rule that blindly inserts both (d) and (W-d) would insert the same coordinate twice.

## Approaches

A direct brute-force solution would fix the endpoints at 0 and some maximum value (W), then choose the remaining (n-2) coordinates from the integers between them. Since (W\le999), the worst case considers

[
\binom{998}{n-2}
]

different sets of interior coordinates. For every candidate array we then generate all (\frac{n(n-1)}2) distances and compare their multiplicities with the input spectrum. The worst-case work is therefore

[
O\left(\binom{998}{n-2}n^2\right).
]

For (n=62), this is far beyond feasible.

The brute force works because explicitly checking every candidate is certainly correct, but it completely ignores the strongest information contained in the spectrum: its largest distance.

Let the largest distance be (W). Any valid array must contain both 0 and (W), because the largest distance can only be the distance between the minimum and maximum coordinates. Once those endpoints are fixed, consider the largest distance (d) that has not yet been explained by already chosen points.

There are only two possible coordinates that can explain this distance through an endpoint. One is (d), because its distance from 0 is (d). The other is (W-d), because its distance from (W) is (d). Thus every valid completion must contain at least one of these two coordinates.

This gives the standard turnpike reconstruction strategy. We repeatedly take the largest unexplained distance and try the only coordinates that can account for it. Whenever a coordinate is proposed, all of its distances to already chosen coordinates must exist in the remaining multiset. If even one required distance is missing, the branch is impossible and can be discarded immediately.

That basic backtracking is still not enough for this problem. Arithmetic progressions can create many symmetric-looking branches. The additional observation is about multiplicity.

Suppose the largest unexplained distance is (d), and its remaining multiplicity is greater than two. That state is impossible. At this stage, an unexplained occurrence of (d) can only be accounted for by placing (d) or (W-d). There are only those two endpoint-generated occurrences available. Any pair of future unplaced points whose difference is (d) would also have a larger distance to an endpoint, and that larger distance would have been processed first. Consequently, at most two copies of the current largest distance can remain.

If (d) occurs exactly twice and (d\ne W-d), both (d) and (W-d) are forced. There is no reason to branch. If only one of them were inserted, only one copy of (d) would be explained by an endpoint, while the other copy would have to come from a future pair whose larger endpoint distance should already have been processed.

If (d=W-d), the two candidates are the same point. This is the midpoint case, so a single coordinate explains both endpoint distances.

These multiplicity rules collapse the problematic branches that make a naive turnpike DFS exponential in practice. The resulting search is still exponential in the theoretical worst case, but the coordinate bound and the strong forced-placement rule make it practical for the given limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O\left(\binom{998}{n-2}n^2\right)) | (O(n^2)) | Too slow |
| Backtracking with largest-distance pruning | (O(2^n n^2 + Rn\log n)) worst case | (O(1000+n+Rn)) | Accepted |

Here (R) is the number of valid solutions. The (2^n) term describes the theoretical search-tree bound. In practice, the multiplicity rule removes the large symmetric subtrees that make the naive version time out.

## Algorithm Walkthrough

1. Read the (\frac{n(n-1)}2) distances and find their maximum (W). If (W>999), there is no valid array. Otherwise, initialize a frequency array `cnt`, where `cnt[d]` stores how many copies of distance (d) are still unused.
2. Put 0 and (W) into the current coordinate set. The distance (W) has already been explained by this pair, so decrease `cnt[W]` by one. These endpoints are forced because no other pair can have distance larger than the distance between the minimum and maximum coordinates.
3. At every recursive state, find the largest distance (d) whose remaining frequency is positive. This is the next distance that must be explained.
4. If all (n) coordinates have been placed, record the current set as a solution. Every successful insertion removes exactly the distances introduced by the new point, so reaching (n) points means the complete spectrum has been consumed.
5. If the remaining multiplicity of (d) is greater than two, stop this branch. There are only two possible endpoint positions, (d) and (W-d), that can account for the current largest distance.
6. If `cnt[d] == 2` and (d\ne W-d), try placing both (d) and (W-d) together. This is forced, so there is no branching at this state.
7. Otherwise, try (d) as a candidate coordinate. For that candidate, compute its distance to every already placed coordinate. The candidate is legal only if every required distance has enough remaining multiplicity. If it is legal, remove those distances, add the coordinate, recurse, and then restore everything while backtracking.
8. If (d\ne W-d), also try (W-d) in the same way. These are the only two possible coordinates capable of explaining the current largest distance.
9. When the search finishes, sort all reconstructed arrays lexicographically. The coordinates inside a solution are also sorted before storing them, because the required output representation is increasing.

### Why it works

The key invariant is that `cnt` always represents exactly the distances not yet generated by the coordinates currently in `points`. Initially, only the endpoint distance (W) has been removed. Whenever a new coordinate is added, precisely its distances to all existing coordinates are removed, so the invariant remains true.

For the largest remaining distance (d), a valid completion must contain (d) or (W-d). If neither were present, any pair of future points producing distance (d) would have an endpoint distance larger than (d), contradicting the fact that (d) is currently the largest unexplained distance. Thus the search never discards a valid solution.

The multiplicity pruning follows the same argument. More than two unexplained copies of (d) cannot be accounted for by the two endpoint positions, so that state cannot lead to a solution. When exactly two copies remain and (d\ne W-d), both endpoint positions are forced. The midpoint case is different because one point at (W/2) has distance (d) to both endpoints.

Every candidate is accepted only after all newly created distances have been found in the remaining multiset. Hence every recorded array has exactly the requested spectrum. Since every valid completion follows one of the candidate choices considered by the recursion, every valid array is eventually found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, spec):
    m = n * (n - 1) // 2

    if len(spec) != m:
        return []

    width = spec[-1]

    if width > 999:
        return []

    cnt = [0] * (width + 1)

    for d in spec:
        if d <= 0 or d > width:
            return []
        cnt[d] += 1

    # The maximum distance must be between 0 and width.
    cnt[width] -= 1

    points = [0, width]
    answers = []

    def largest_remaining():
        for d in range(width, 0, -1):
            if cnt[d]:
                return d
        return 0

    def place(candidates):
        """Try placing all candidates as one forced/branched operation."""
        k = len(candidates)

        if len(points) + k > n:
            return

        if len(set(candidates)) != k:
            return

        for x in candidates:
            if x <= 0 or x >= width or x in points:
                return

        need = {}

        # Distances from every new point to every old point.
        for x in candidates:
            for y in points:
                d = abs(x - y)
                need[d] = need.get(d, 0) + 1

        # Distances between new points when two are inserted together.
        for i in range(k):
            for j in range(i + 1, k):
                d = abs(candidates[i] - candidates[j])
                need[d] = need.get(d, 0) + 1

        # Check whether the remaining spectrum contains all
        # distances introduced by the new points.
        for d, amount in need.items():
            if d == 0 or d > width or cnt[d] < amount:
                return

        # Apply the changes.
        for d, amount in need.items():
            cnt[d] -= amount

        points.extend(candidates)

        dfs()

        for _ in candidates:
            points.pop()

        for d, amount in need.items():
            cnt[d] += amount

    def dfs():
        if len(points) == n:
            answers.append(tuple(sorted(points)))
            return

        d = largest_remaining()

        if d == 0:
            return

        # At the current largest unexplained distance, at most
        # two copies can still be possible.
        if cnt[d] > 2:
            return

        reflected = width - d

        # Two copies force both symmetric positions, except when
        # they coincide at the midpoint.
        if cnt[d] == 2 and d != reflected:
            place((d, reflected))
            return

        # One copy means either endpoint-side candidate may be used.
        # When d == reflected there is only one distinct candidate.
        place((d,))

        if reflected != d:
            place((reflected,))

    dfs()

    answers.sort()
    return answers

def main():
    n_line = input().strip()
    if not n_line:
        return

    n = int(n_line)
    m = n * (n - 1) // 2

    spec = []
    while len(spec) < m:
        spec.extend(map(int, input().split()))

    answers = solve_case(n, spec)

    out = [str(len(answers))]
    for ans in answers:
        out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The frequency array is indexed directly by distance. This is preferable to a dictionary here because the largest possible distance is only 999, so every lookup and update is constant time with very small constants.

The initialization fixes the two endpoints and removes their distance from `cnt`. This handles the (n=2) case naturally, because after removing the only distance, the recursion immediately sees that both required points are already present.

The `place` function performs the central multiset operation. It first rejects coordinates outside the open interval ((0,W)), because the endpoints already occupy 0 and (W). It also rejects duplicate coordinates, since the original array must contain distinct values.

The `need` dictionary is necessary because several newly generated pairs can have the same distance. For example, inserting the midpoint into an interval of even width generates the same distance to both endpoints. Aggregating the multiplicities before modifying `cnt` prevents a sequence of individual checks from accidentally accepting a multiset with insufficient copies.

The two-candidate case is handled by passing both coordinates to `place` at once. Their mutual distance is included in `need`, which is another subtle detail. Omitting that distance would leave the spectrum with an unexplained copy and could incorrectly accept the reconstruction.

The recursion depth is at most 62, so Python's recursion limit is not a concern. Python integers also have arbitrary precision, although every relevant value in this problem is at most 999 and no large arithmetic is needed.

Finally, the answers are sorted after reconstruction. The DFS order is determined by spectrum multiplicities rather than lexicographic order, so relying on search order would not satisfy the output requirement.

## Worked Examples

### Sample 1

The input is

```
4
2 2 2 4 4 6
```

The important state transitions are:

| Step | Largest remaining distance | Count | Candidate action | Current points | Remaining spectrum |
| --- | --- | --- | --- | --- | --- |
| Initial | 6 | 1 | Fix endpoints 0 and 6 | 0, 6 | 2,2,2,4,4 |
| 1 | 4 | 2 | Force 2 and 4 | 0,2,4,6 | 2 |
| 2 | 2 | 1 | No new point needed, because 2 was consumed as the distance between 2 and 4 | 0,2,4,6 | empty |

The distance 4 occurs twice, so the coordinates 4 and (6-4=2) are forced. Inserting them together also creates their mutual distance 2, which consumes the final copy of 2. The reconstruction is complete.

The resulting output is

```
1
0 2 4 6
```

This example exercises the multiplicity-two rule and the need to count distances between two simultaneously inserted coordinates.

### Sample 2

The input spectrum is

```
3 3 6 9 9 12 12 15 18 21
```

The reconstruction starts with endpoints 0 and 21.

| Step | Largest remaining | Count | Candidate tried | New distances required | Current points |
| --- | --- | --- | --- | --- | --- |
| Initial | 21 | 1 | 0, 21 fixed | 21 | 0,21 |
| 1A | 18 | 1 | 18 | 18,3 | 0,18,21 |
| 2A | 15 | 1 | 15 | 15,3,6 | rejected because 3 is unavailable |
| 2B | 15 | 1 | 6 | 6,15,12 | 0,6,18,21 |
| 3A | 12 | 1 | 12 | 12,9,6 | rejected because 6 is unavailable |
| 3B | 12 | 1 | 9 | 9,12,3 | 0,6,9,18,21 |
| Final | 0 | 0 | complete | none | 0,6,9,18,21 |
| 1C | 18 | 1 | 3 | 3,18 | 0,3,21 |
| 2C | 15 | 1 | 15 | 15,6,12 | 0,3,15,21 |
| 3C | 12 | 1 | 12 | 12,9,9,3 | 0,3,12,15,21 |
| Final | 0 | 0 | complete | none | 0,3,12,15,21 |

Both branches are valid, producing

```
2
0 3 12 15 21
0 6 9 18 21
```

The trace demonstrates why a candidate is not accepted merely because its coordinate is plausible. Every distance from the new coordinate to every existing coordinate must be available with the correct multiplicity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2^n n^2 + Rn\log n)) worst case | At most two candidate branches exist at a normal state, each candidate checks distances to at most (n) existing points. Finding the largest remaining distance scans at most 999 entries. |
| Space | (O(1000+n+Rn)) | The frequency array uses (O(1000)), recursion and the current coordinate set use (O(n)), and storing all answers requires (O(Rn)). |

The theoretical search remains exponential because the general turnpike reconstruction problem is not known to admit a polynomial-time solution. The relevant practical improvement is that the largest-distance multiplicity rule frequently turns two-way branching into a forced insertion of two coordinates. The coordinate limit of 999 also makes the frequency operations extremely cheap. With at most 1891 input distances and recursion depth at most 62, this is well suited to the stated 5 second and 1024 MB limits.

## Test Cases

The following tests assume the editorial solution is saved as `solution.py`, with `solve_case` available from it.

```python
from solution import solve_case

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    n = data[0]
    spec = data[1:]

    ans = solve_case(n, spec)

    out = [str(len(ans))]
    for x in ans:
        out.append(" ".join(map(str, x)))

    return "\n".join(out) + "\n"

# Provided sample 1
assert run("""
4
2 2 2 4 4 6
""") == """1
0 2 4 6
""", "sample 1"

# Provided sample 2
assert run("""
5
3 3 6 9 9 12 12 15 18 21
""") == """2
0 3 12 15 21
0 6 9 18 21
""", "sample 2"

# Provided sample 3
assert run("""
5
6 7 8 9 10
""") == """0
""", "sample 3"

# Minimum-size input, n = 2.
assert run("""
2
7
""") == """1
0 7
""", "minimum n"

# All spectrum values are equal, possible only for n = 2.
assert run("""
2
999
""") == """1
0 999
""", "maximum coordinate"

# Two different solutions, catches reflection handling.
assert run("""
3
1 2 3
""") == """2
0 1 3
0 2 3
""", "two reflected solutions"

# Invalid repeated distances for n = 3.
assert run("""
3
1 1 1
""") == """0
""", "impossible spectrum"

# Largest distance outside the allowed coordinate range.
assert run("""
2
1000
""") == """0
""", "coordinate boundary"

# Maximum n. Construct X = 0, 1, ..., 61.
x = list(range(62))
spec = []
for i in range(62):
    for j in range(i + 1, 62):
        spec.append(j - i)
spec.sort()

max_input = "62\n" + " ".join(map(str, spec)) + "\n"
max_expected = "1\n" + " ".join(map(str, x)) + "\n"

assert run(max_input) == max_expected, "maximum n"
```

The custom cases can be summarized as follows.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 7` | `1 / 0 7` | Minimum (n), endpoint initialization |
| `2 / 999` | `1 / 0 999` | Maximum coordinate boundary |
| `3 / 1 2 3` | Two solutions | Reflection and lexicographic ordering |
| `3 / 1 1 1` | `0` | Invalid multiplicities |
| `2 / 1000` | `0` | Rejecting an impossible width |
| `62` with spectrum of `0..61` | One solution | Maximum (n), recursion depth, large spectrum |

## Edge Cases

For (n=2), the input

```
2
7
```

starts with the endpoints 0 and 7. The only spectrum value is immediately consumed by their pair, so the current set already has the required two elements. The algorithm records `0 7` without trying to insert an interior coordinate.

For the coordinate boundary,

```
2
999
```

the width is exactly 999, so it is accepted. The result is `0 999`. The implementation checks `width > 999`, rather than `width >= 999`, which avoids an off-by-one error at the legal upper boundary.

For an out-of-range width,

```
2
1000
```

the maximum distance itself would require an element at 1000 because the first element is fixed at zero. The algorithm rejects the case before starting the search.

For repeated distances,

```
4
2 2 2 4 4 6
```

the width 6 fixes the endpoints. The next largest distance is 4 with multiplicity two, so both 4 and (6-4=2) are forced. Their mutual distance is another 2, consuming all three copies of distance 2. The final array is `0 2 4 6`.

For the midpoint case,

```
5
1 1 1 1 2 2 2 3 3 4
```

the width is 4. When distance 2 becomes the largest remaining distance with multiplicity two, the two candidates are both coordinate 2 because (4-2=2). The algorithm recognizes that the candidates coincide and inserts only one point. That point creates two endpoint distances of 2, while its distances to the other chosen coordinates account for the remaining copies.

For an invalid spectrum,

```
3
1 1 1
```

the width is 1, so the endpoints would have to be 0 and 1. A third distinct coordinate cannot fit strictly between them. The recursive search finds no legal candidate and returns zero solutions.

For the two-solution case,

```
3
1 2 3
```

the endpoints are 0 and 3. The largest remaining distance is 2, whose candidates are 2 and 1. Placing 1 produces `0 1 3`, while placing 2 produces `0 2 3`. Both consume exactly the same spectrum, and sorting the final answers puts `0 1 3` before `0 2 3`.

The central invariant behind all of these cases is the remaining frequency table. A branch is never accepted merely because its coordinates look plausible. Every newly created pair must consume one matching copy from the input multiset, and every consumed copy is restored when the branch is abandoned. This is what prevents repeated distances, midpoint distances, and symmetric solutions from being handled incorrectly.
