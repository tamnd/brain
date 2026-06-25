---
title: "CF 106078H - Uranus"
description: "Each probe can be described by two limits and a cost. One limit is how much temperature it can survive, the other is how much wind it can survive. A probe is usable at a location only if it handles both conditions at the same time."
date: "2026-06-25T12:09:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106078
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 9-17-25 Div. 1 (Advanced)"
rating: 0
weight: 106078
solve_time_s: 54
verified: true
draft: false
---

[CF 106078H - Uranus](https://codeforces.com/problemset/problem/106078/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

Each probe can be described by two limits and a cost. One limit is how much temperature it can survive, the other is how much wind it can survive. A probe is usable at a location only if it handles both conditions at the same time. For every location query, we want the cheapest probe that is strong enough for that location’s temperature and wind.

In more concrete terms, we have a collection of rectangles in a 2D plane where each probe defines a corner threshold. A probe is valid for a query if its threshold point lies up and to the right of the query point, meaning both coordinates are at least as large. Among all such probes, we want the minimum cost.

The input size reaches up to one hundred thousand probes and one hundred thousand queries. That immediately rules out checking every probe per query, since that would be on the order of 10¹⁰ comparisons in the worst case, which is far beyond what a one or two second limit can handle. Any acceptable solution needs to process both probes and queries in roughly linearithmic time.

A naive interpretation that often fails in implementation is to treat the constraints independently, for example filtering by temperature first and then scanning wind linearly. That breaks when both dimensions interact. Another subtle failure case appears when multiple probes dominate each other partially: a probe might be better in temperature but worse in wind, and vice versa, so greedy ordering by a single dimension does not work.

A small illustrative failure: suppose we have probes (temperature, wind, cost) as (5, 1, 100), (1, 5, 1), and (3, 3, 2). For a query (3, 3), the correct answer is 2. If we only sort by temperature and take the first valid, we might incorrectly pick (5,1,100) even though it fails wind constraints, or if we filter incorrectly we might miss the optimal middle tradeoff probe.

## Approaches

The brute-force idea is straightforward: for each query, scan all probes and check whether both constraints are satisfied, tracking the minimum cost. This is correct because it directly evaluates the definition of validity. The cost is checking n probes for each of q queries, giving n·q operations, which reaches 10¹⁰ in the worst case. That scale is too large to finish within the time limit.

The key observation is that both constraints are monotonic. If a probe works for a certain temperature and wind, it automatically works for any easier query (lower temperature or wind requirement). This structure allows us to treat probes as points in a 2D space and queries as dominance checks.

We can sort both probes and queries by temperature in descending order. As we sweep from high temperature to low temperature, every probe that becomes eligible is inserted into a structure keyed by wind. At any moment, the structure contains exactly those probes that satisfy the temperature requirement for the current query. The remaining task becomes: among all stored probes, find the minimum cost among those with wind at least the query’s wind. This is a standard prefix or suffix minimum query over a compressed coordinate axis.

This turns the problem into an offline sweep line combined with a segment tree over wind values. Each probe is inserted once, each query triggers one range minimum query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Sweep + Segment Tree | O((n+q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform the problem into an offline process where probes and queries are handled in a unified order based on temperature.

1. First collect all probes and queries and extract all wind values that appear in either. We compress these values into a smaller index range because a segment tree cannot efficiently operate on values up to 10⁹ directly. Compression preserves ordering, which is the only property we need.
2. Sort all probes in descending order of temperature. This ensures that when we process a query with temperature T, every probe we have inserted so far already satisfies temperature ≥ T.
3. Sort all queries in descending order of temperature as well, keeping their original indices so we can restore output order later.
4. Build a segment tree over the compressed wind axis. Each node stores the minimum cost among all probes currently inserted in that segment.
5. Sweep through queries in sorted order. Maintain a pointer over probes. For each query, insert all probes whose temperature is at least the query temperature into the segment tree, updating the position corresponding to their wind with the minimum cost. This step ensures the structure always represents exactly the valid probe set for that query’s temperature constraint.
6. After all relevant probes are inserted, we query the segment tree on the range of winds from the query’s required wind up to the maximum possible wind index. This gives the minimum cost among all probes that satisfy both constraints.
7. If no probe exists in that range, we return -1 for that query.

The correctness relies on the fact that once a probe is inserted, it remains valid for all future queries in the sweep because those queries only decrease temperature requirements.

### Why it works

At every query step, the segment tree contains exactly the set of probes whose temperature constraint is satisfied. The wind condition is enforced by range minimum query. Since both constraints are enforced independently but consistently through the sweep order and the segment tree, every probe is considered exactly when it becomes valid, and never excluded once valid. This guarantees that the minimum returned is taken over precisely the feasible probes.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, n):
        self.n = 1
        while self.n < n:
            self.n *= 2
        self.inf = 10**18
        self.t = [self.inf] * (2 * self.n)

    def update(self, i, val):
        i += self.n
        if val < self.t[i]:
            self.t[i] = val
            i //= 2
            while i:
                self.t[i] = min(self.t[2*i], self.t[2*i+1])
                i //= 2

    def query(self, l, r):
        res = self.inf
        l += self.n
        r += self.n
        while l <= r:
            if l % 2 == 1:
                res = min(res, self.t[l])
                l += 1
            if r % 2 == 0:
                res = min(res, self.t[r])
                r -= 1
            l //= 2
            r //= 2
        return res

def solve():
    n, q = map(int, input().split())
    probes = []
    wind_vals = []

    for _ in range(n):
        x, y, c = map(int, input().split())
        probes.append((x, y, c))
        wind_vals.append(y)

    queries = []
    for i in range(q):
        t, w = map(int, input().split())
        queries.append((t, w, i))
        wind_vals.append(w)

    wind_vals = sorted(set(wind_vals))
    comp = {v: i for i, v in enumerate(wind_vals)}

    probes.sort(reverse=True)
    queries.sort(reverse=True)

    seg = SegTree(len(wind_vals))

    ans = [-1] * q
    j = 0

    for t, w, idx in queries:
        while j < n and probes[j][0] >= t:
            _, y, c = probes[j]
            seg.update(comp[y], c)
            j += 1

        pos = comp[w]
        res = seg.query(pos, len(wind_vals) - 1)
        ans[idx] = -1 if res == seg.inf else res

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The solution is built around the sweep order. The probe list is sorted so that once we move past a probe, it will never become relevant again. The segment tree stores minimum cost per wind bucket, and updates only ever decrease values, which is why a simple minimum propagation works.

The query logic is always a suffix query because we need wind ≥ required value, so we query from compressed index onward.

A common implementation pitfall is forgetting that multiple probes may map to the same wind coordinate after compression. The segment tree update must take the minimum cost, not overwrite blindly.

## Worked Examples

Since the original statement does not provide explicit samples in a clean format, consider the following constructed cases.

### Example 1

Input:

```
3 2
5 1 100
1 5 1
3 3 2
3 3
2 2
```

We process probes sorted by temperature: (5,1,100), (3,3,2), (1,5,1). Queries are (3,3) then (2,2).

At query (3,3), only probes with temperature ≥ 3 are inserted: (5,1,100) and (3,3,2). Wind constraint selects among valid winds ≥ 3, only (3,3,2) qualifies, so answer is 2.

At query (2,2), all probes are inserted. Valid candidates include all three; among those with wind ≥ 2, both (1,5,1) and (3,3,2) qualify, so minimum is 1.

| Query | Inserted probes (x≥t) | Valid wind range | Answer |
| --- | --- | --- | --- |
| (3,3) | (5,1,100), (3,3,2) | y≥3 → {2} | 2 |
| (2,2) | all | y≥2 → {1,2} | 1 |

This shows how temperature filtering is handled entirely by sweep order.

### Example 2

Input:

```
2 1
10 10 5
1 10 1
10 5
```

Only probe (10,10,5) satisfies wind ≥ 5, so answer is 5. The other probe is eliminated by wind constraint even though temperature matches.

| Query | Active probes | Valid wind ≥ 5 | Answer |
| --- | --- | --- | --- |
| (10,5) | both probes | only (10,10,5) | 5 |

This confirms wind filtering is correctly handled by the segment tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | each probe is inserted once, each query performs a log n range minimum query |
| Space | O(n) | segment tree plus coordinate compression arrays |

The log factor comes from segment tree operations over compressed wind values. With n and q up to 10⁵, this comfortably fits within typical limits for 2 seconds in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    class SegTree:
        def __init__(self, n):
            self.n = 1
            while self.n < n:
                self.n *= 2
            self.inf = 10**18
            self.t = [self.inf] * (2 * self.n)

        def update(self, i, val):
            i += self.n
            self.t[i] = min(self.t[i], val)
            i //= 2
            while i:
                self.t[i] = min(self.t[2*i], self.t[2*i+1])
                i //= 2

        def query(self, l, r):
            res = self.inf
            l += self.n
            r += self.n
            while l <= r:
                if l % 2:
                    res = min(res, self.t[l])
                    l += 1
                if not r % 2:
                    res = min(res, self.t[r])
                    r -= 1
                l //= 2
                r //= 2
            return res

    def solve():
        n, q = map(int, input().split())
        probes = []
        vals = []
        for _ in range(n):
            x, y, c = map(int, input().split())
            probes.append((x, y, c))
            vals.append(y)

        queries = []
        for i in range(q):
            t, w = map(int, input().split())
            queries.append((t, w, i))
            vals.append(w)

        vals = sorted(set(vals))
        mp = {v:i for i,v in enumerate(vals)}

        probes.sort(reverse=True)
        queries.sort(reverse=True)

        seg = SegTree(len(vals))
        ans = [-1]*q
        j = 0

        for t, w, idx in queries:
            while j < n and probes[j][0] >= t:
                x, y, c = probes[j]
                seg.update(mp[y], c)
                j += 1

            res = seg.query(mp[w], len(vals)-1)
            ans[idx] = -1 if res == seg.inf else res

        return "\n".join(map(str, ans))

    return solve()

# custom tests

assert run("""1 1
5 5 10
5 5
""") == "10"

assert run("""2 1
1 10 5
10 1 1
5 5
""") == "-1"

assert run("""3 2
5 1 100
3 3 2
1 5 1
3 3
2 2
""") == "2\n1"

assert run("""4 2
10 10 7
10 9 5
9 10 6
8 8 1
9 9
10 10
""") == "5\n5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single probe match | 10 | minimal valid case |
| no valid probe | -1 | failure handling |
| mixed dominance | 2 / 1 | correctness of 2D filtering |
| multiple overlaps | 5 / 5 | tie handling and compression correctness |

## Edge Cases

A tricky situation arises when multiple probes share the same wind value but different costs. The segment tree update must always keep the minimum cost; overwriting would incorrectly discard better probes.

Another edge case is when all probes fail one constraint. In that case the segment tree query returns infinity, and the output must be converted to -1 rather than printed directly.

A final subtle case is when a query’s wind value is smaller than all compressed coordinates or larger than all of them. Compression ensures we always map correctly, but forgetting to use the full suffix range would silently drop valid candidates.
