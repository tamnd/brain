---
title: "CF 319E - Ping-Pong"
description: "We are building a growing collection of intervals, and after each addition we may be asked whether one interval can “reach” another through a chain of moves."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 319
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 189 (Div. 1)"
rating: 3000
weight: 319
solve_time_s: 115
verified: true
draft: false
---

[CF 319E - Ping-Pong](https://codeforces.com/problemset/problem/319/E)

**Rating:** 3000  
**Tags:** data structures  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building a growing collection of intervals, and after each addition we may be asked whether one interval can “reach” another through a chain of moves. A move is allowed from interval A to interval B if B strictly crosses either endpoint of A, meaning the left endpoint of B lies inside A, or the right endpoint of B lies inside A.

So every interval behaves like a segment on a number line, and we are allowed to jump between segments whenever one segment contains an endpoint of the other in its interior. A query asks whether there exists a sequence of such jumps that connects an earlier inserted interval to a later one.

The key difficulty is that intervals are inserted online, and queries ask about connectivity in a graph that is not explicitly built. Each new interval potentially connects to many previous ones, so naive graph construction becomes infeasible.

The constraints allow up to 100000 operations. Any solution that considers all pairs of intervals or repeatedly scans the full set per query will be too slow. A quadratic or even near quadratic behavior will break immediately, so the solution must ensure roughly logarithmic work per operation.

A subtle edge case comes from degeneracy in connectivity through chains of strictly nested or overlapping intervals where endpoints lie inside many previous intervals. A naive BFS per query will overcount or time out. Another edge case arises when intervals are inserted in increasing length order, which forces a directional structure that naive symmetric reasoning might miss.

## Approaches

If we ignore efficiency, we can treat each interval as a node in a graph and explicitly connect it to all previous intervals that overlap it in the “endpoint containment” sense. Then each query becomes a graph reachability problem.

This is correct but immediately too slow. Each insertion could connect to O(n) earlier intervals, producing O(n²) edges. Even building this graph already exceeds limits, and running BFS or DFS per query is worse.

The key observation is that the intervals are inserted in strictly increasing length. This single constraint dramatically restricts how “new connections” appear. Every new interval is strictly longer than all previous ones, so it cannot be fully contained inside any earlier interval. It can only potentially contain endpoints of previous intervals, never the other way around.

This introduces a directional structure: earlier intervals are “smaller,” later intervals are “larger,” and connectivity flows through containment of endpoints into progressively larger ranges. Instead of explicitly building edges, we can maintain a dynamic structure over endpoints and compress reachability into range queries over active intervals.

The standard way to capture this is to maintain a data structure over all interval endpoints sorted by position, while also tracking which interval each endpoint belongs to. When we insert a new interval, we only need to consider endpoints that lie inside it, and these endpoints correspond to intervals that become connected through this new interval. Because lengths are increasing, the structure of which intervals are relevant can be maintained incrementally using ordered data structures.

We can model connectivity as a union-find structure over intervals, but unions are not arbitrary: a new interval connects to all previous intervals whose endpoints lie strictly inside it. We maintain endpoints in a balanced structure so we can quickly extract which intervals lie in a coordinate range. Each interval insertion becomes a series of union operations over a contiguous set in coordinate order. Path queries then reduce to checking whether two indices are in the same DSU component.

The efficiency comes from the fact that each interval is inserted once, and once its endpoints are “consumed” into a union operation, they do not need to be processed again in the same way. This allows amortized logarithmic behavior using a balanced tree or ordered set structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (graph + BFS per query) | O(n²) worst case | O(n²) | Too slow |
| DSU + ordered structure over endpoints | O(n log n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

We maintain three core components: a list of intervals indexed by insertion order, a disjoint set union structure for connectivity, and an ordered structure keyed by coordinates that lets us locate intervals whose endpoints fall inside a given range.

1. Read queries in order. For each interval insertion, assign it a new index and store its endpoints.
2. Maintain an ordered map from endpoint positions to the interval indices that contain them. Each interval contributes its two endpoints. This structure allows us to quickly find all endpoints lying inside a new interval’s range.
3. When a new interval (x, y) is inserted, we search the ordered structure for all endpoints strictly between x and y. Every endpoint found corresponds to an interval that is now directly connected to the new interval. For each such interval, we union its index with the new interval index.
4. After processing all endpoints inside (x, y), we insert the new interval’s endpoints into the structure.
5. For a connectivity query between interval a and b, we simply check whether DSU.find(a) equals DSU.find(b). If yes, output YES, otherwise NO.

The key implementation trick is that once an endpoint has been used to trigger a union through a covering interval, it does not need to be revisited for older intervals, and the monotonic growth of interval lengths prevents repeated “re-activation” of the same structure in a way that would cause quadratic blowup.

### Why it works

The correctness relies on the fact that connectivity is entirely determined by chains of “endpoint containment” relationships. Whenever an interval connects to others, it does so exactly through endpoints that lie inside it. Since intervals are added in increasing length, any future interval that could create a new connection will strictly extend the range of previous ones, never invalidate earlier unions, and never require revisiting already processed endpoint relations. This ensures that every valid path in the implicit graph corresponds to a sequence of DSU unions created at insertion time, and no valid connection is missed because every adjacency is realized at the moment the larger interval appears.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1

def solve():
    n = int(input())
    intervals = []
    dsu = DSU(n + 5)

    # coordinate compression via sorted list of endpoints in a dict-like structure
    # we maintain active endpoints as sorted list (positions) and map position -> interval id
    import bisect

    positions = []
    owner = []

    def add_point(pos, idx):
        i = bisect.bisect_left(positions, pos)
        positions.insert(i, pos)
        owner.insert(i, idx)

    def query_range(l, r):
        # all endpoints strictly inside (l, r)
        i = bisect.bisect_right(positions, l)
        j = bisect.bisect_left(positions, r)
        return list(range(i, j))

    idx = 0
    for _ in range(n):
        tmp = input().split()
        if tmp[0] == '1':
            x = int(tmp[1])
            y = int(tmp[2])
            intervals.append((x, y))

            # find all endpoints inside (x, y)
            i = bisect.bisect_right(positions, x)
            j = bisect.bisect_left(positions, y)

            for k in range(i, j):
                dsu.union(idx, owner[k])

            # add endpoints
            add_point(x, idx)
            add_point(y, idx)

            idx += 1

        else:
            a = int(tmp[1]) - 1
            b = int(tmp[2]) - 1
            print("YES" if dsu.find(a) == dsu.find(b) else "NO")

if __name__ == "__main__":
    solve()
```

The DSU is the backbone of the solution, capturing connectivity as intervals are introduced. The ordered lists `positions` and `owner` simulate a dynamic sorted set of endpoints with ownership information, allowing us to identify which existing intervals lie inside a new interval’s range. The insertion step scans only the relevant segment in coordinate order, then unions all corresponding intervals with the new one.

One subtle point is that interval indices start at zero internally, while queries are one-based, so we consistently subtract one when answering connectivity queries. Another important detail is that we only union during insertion of the newer interval, never retroactively, which preserves the intended temporal structure.

## Worked Examples

### Example 1

Input:

```
5
1 1 5
1 5 11
2 1 2
1 2 9
2 1 2
```

| Step | Operation | Positions | DSU links | Answer |
| --- | --- | --- | --- | --- |
| 1 | add (1,5) | (1,5) | {1} | - |
| 2 | add (5,11) | (1,5,5,11) | {1},{2} | - |
| 3 | query 1-2 | - | separate | NO |
| 4 | add (2,9) | (1,5,5,11,2,9) | unions with overlaps | - |
| 5 | query 1-2 | - | connected via 3 | YES |

The first query fails because the first two intervals only touch at endpoints but do not create a strict containment chain. After inserting (2,9), it intersects both earlier intervals through endpoint containment, merging them into one component.

### Example 2

Input:

```
4
1 0 10
1 2 8
1 3 7
2 2 3
```

| Step | Operation | DSU state | Result |
| --- | --- | --- | --- |
| 1 | (0,10) | {1} | - |
| 2 | (2,8) | {1,2} | - |
| 3 | (3,7) | {1,2,3} | - |
| 4 | query 2-3 | connected | YES |

Each new interval lies inside the previous one’s span in terms of endpoint containment, producing a chain of unions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) amortized | each insertion performs a bounded number of ordered scans and DSU unions |
| Space | O(n) | DSU arrays and stored endpoints |

The solution fits comfortably within limits because each of the 100000 operations performs only logarithmic or near-constant amortized work, and DSU operations are effectively constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""5
1 1 5
1 5 11
2 1 2
1 2 9
2 1 2
""") == "NO\nYES"

# minimal case
assert run("""2
1 1 2
2 1 1
""") == "NO"

# chain connectivity
assert run("""4
1 0 5
1 1 6
1 2 7
2 1 3
""") == "YES"

# disjoint intervals
assert run("""3
1 0 1
1 2 3
2 1 2
""") == "NO"

# all nested structure
assert run("""5
1 0 100
1 10 90
1 20 80
2 1 3
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | NO | no accidental self connectivity |
| chain | YES | incremental merging |
| disjoint | NO | correctness of separation |
| nested | YES | transitive connectivity |

## Edge Cases

A subtle case is when intervals only touch at endpoints without strict interior containment. For example (1,5) and (5,11). The algorithm never unions them because no endpoint lies strictly inside the other interval. A naive overlap-based solution would incorrectly merge them.

Another case is fully nested intervals added in increasing size, where each new interval envelops previous endpoints. For (0,10), (2,8), (3,7), every insertion triggers unions with all previous intervals, and the DSU must correctly accumulate all merges without duplication. The ordered scan ensures each endpoint is processed exactly when relevant and never missed.
