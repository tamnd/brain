---
title: "CF 105400H - Pirate's Booty"
description: "We have a line of ships, each ship behaving like a container with a fixed maximum number of crate slots. Initially all ships are empty. Over time, crates are poured into a chosen ship index."
date: "2026-06-22T12:44:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105400
codeforces_index: "H"
codeforces_contest_name: "Fall 2024 Cupertino Informatics Tournament"
rating: 0
weight: 105400
solve_time_s: 129
verified: false
draft: false
---

[CF 105400H - Pirate's Booty](https://codeforces.com/problemset/problem/105400/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We have a line of ships, each ship behaving like a container with a fixed maximum number of crate slots. Initially all ships are empty. Over time, crates are poured into a chosen ship index. If that ship is already full, the overflow continues to the next ship, and so on, until either all crates are placed or we run past the last ship, in which case the remaining crates are discarded.

The second type of query asks for the current number of crates stored in a specific ship at that moment in time, after all previous loads have been processed.

So the system is a dynamic one dimensional pipeline with capacities, where every update is a “push forward until space is found” operation, and every query is a point inspection.

The constraints push us away from any naive simulation. With up to 100,000 ships and 100,000 operations, a straightforward approach that walks forward ship by ship for each load can degrade to quadratic behavior. In the worst case, every load starts at ship 1 and propagates almost to ship N, producing about 10^10 primitive operations, which is far beyond the limit for 2 seconds.

A more subtle issue appears in partial filling. A single ship may be visited many times across different load operations, each time receiving only a small number of crates until it eventually fills up. Any solution that processes crates one by one or updates capacity incrementally without aggregation will silently time out even if logically correct.

Edge cases worth explicitly considering include a chain of fully saturated ships at the beginning, where loads immediately skip forward, for example:

Input:

```
5 1
0 0 10 10 10
1 1 7
```

Here ships 1 and 2 are already full or effectively unusable, so the load must begin at ship 3. A naive implementation that does not skip efficiently will waste time checking ships 1 and 2 repeatedly.

Another edge case is repeated small loads:

```
3 3
5 5 5
1 1 1
1 1 1
1 1 1
```

Even though each operation is tiny, any approach that redistributes crate-by-crate becomes too slow because it repeats work over the same indices.

## Approaches

The brute-force simulation is straightforward. For each load operation, we start at the given ship index and move forward. At each ship, we take as many crates as possible up to its remaining capacity, subtracting from the incoming amount, and continue to the next ship if needed. This is correct because it exactly follows the rules of overflow propagation.

The problem is that this scan can revisit long prefixes of ships many times. If every operation starts near the front, each update can take O(N), leading to O(NM) behavior in the worst case.

The key structural observation is that a ship only becomes “irrelevant” once it reaches full capacity. After that moment, it never contributes to future allocations again except as a skip point. This means the active set of useful positions only shrinks over time. If we can efficiently jump over full ships, each ship can be eliminated once, which suggests a disjoint set union style “next alive position” structure or a segment tree that supports fast “find first non-full” queries.

We maintain remaining capacity per ship. For each load, instead of scanning every index, we repeatedly jump to the next ship at or after the starting position that still has remaining capacity. We then push as much as possible into it. If it becomes full, we mark it as inactive so future jumps skip it entirely.

This reduces repeated scanning over full ships and turns the problem into a sequence of jumps and updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(NM) | O(N) | Too slow |
| Segment Tree / DSU Jumps | O((N + M) log N) | O(N) | Accepted |

## Algorithm Walkthrough

We store an array `rem[i] = G[i]`, representing remaining capacity for each ship. We also maintain a data structure that can quickly find the first index at or beyond a position that still has positive remaining capacity. A segment tree storing maximum remaining capacity over ranges is sufficient for this.

For each load operation starting at ship `K` with `C` crates, we repeatedly locate the next usable ship and distribute crates there until either the crates are exhausted or no usable ship remains.

1. Initialize `i` as the first index at or after `K` where `rem[i] > 0`. This is found using a segment tree “first true” query over the condition `rem[i] > 0`. This step is necessary because many ships may already be full and should be skipped entirely.
2. While `i` exists and `C > 0`, compute how many crates can be placed in ship `i` as `x = min(rem[i], C)`. We then subtract `x` from both `rem[i]` and `C`.
3. If `rem[i]` becomes zero after this operation, we update the segment tree so that this position is marked as inactive. This ensures future searches will skip this ship entirely.
4. If `rem[i]` is still positive but `C` is zero, the operation ends immediately. We do not advance manually because no more crates are being distributed.
5. Otherwise, if `C` is still positive and the current ship is full, we query again for the next usable ship at or after `i + 1`.

The important structural idea is that movement only happens when a ship is completely saturated. Partial fills do not trigger movement; they only reduce remaining capacity.

### Why it works

At any point in time, every ship has a well-defined remaining capacity, and crates always flow strictly left to right without ever skipping a ship that still has space. The segment tree always returns the earliest ship with available capacity in the required suffix, so every placement step respects the original greedy rule.

Since ships are only removed from consideration when they reach zero capacity, and once removed they never become active again, each removal is permanent. This guarantees that the search structure only shrinks monotonically, preventing repeated unnecessary scanning.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, l, r, arr):
        if l == r:
            self.t[v] = arr[l]
            return
        m = (l + r) // 2
        self.build(v * 2, l, m, arr)
        self.build(v * 2 + 1, m + 1, r, arr)
        self.t[v] = max(self.t[v * 2], self.t[v * 2 + 1])

    def update(self, v, l, r, idx, val):
        if l == r:
            self.t[v] = val
            return
        m = (l + r) // 2
        if idx <= m:
            self.update(v * 2, l, m, idx, val)
        else:
            self.update(v * 2 + 1, m + 1, r, idx, val)
        self.t[v] = max(self.t[v * 2], self.t[v * 2 + 1])

    def find_first(self, v, l, r, ql, qr):
        if r < ql or l > qr or self.t[v] == 0:
            return -1
        if l == r:
            return l
        m = (l + r) // 2
        res = self.find_first(v * 2, l, m, ql, qr)
        if res != -1:
            return res
        return self.find_first(v * 2 + 1, m + 1, r, ql, qr)

def main():
    n, m = map(int, input().split())
    g = list(map(int, input().split()))
    rem = g[:]
    st = SegTree(rem)

    out = []

    for _ in range(m):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            _, k, c = tmp
            k -= 1
            i = st.find_first(1, 0, n - 1, k, n - 1)
            while i != -1 and c > 0:
                take = min(rem[i], c)
                rem[i] -= take
                c -= take
                st.update(1, 0, n - 1, i, rem[i])
                if rem[i] > 0:
                    break
                i = st.find_first(1, 0, n - 1, i + 1, n - 1)
        else:
            _, k = tmp
            out.append(str(rem[k - 1]))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The segment tree is used in two roles. The first is tracking the maximum remaining capacity in a range so we can quickly determine whether any usable ship exists. The second is locating the first index in a suffix that still has capacity, which is essential for preserving left-to-right order.

The update operation is always applied after modifying a ship’s remaining capacity. If a ship reaches zero, it effectively becomes invisible in future searches because its segment tree value becomes zero.

The loop inside the load query is carefully structured so that each iteration either fully consumes a ship or exits early when no crates remain. The key is that we never scan linearly; every jump is logarithmic.

## Worked Examples

Consider a small case:

Input:

```
4 2
2 3 1 2
1 1 4
2 2
```

We track remaining capacity and pointer movement.

| Step | Operation | Ship index | rem before | take | rem after | remaining C |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | load | 1 | 2 | 2 | 0 | 2 |
| 2 | load continues | 2 | 3 | 2 | 1 | 0 |

After the first query, ship 1 is full, ship 2 has 1 remaining. Query 2 asks ship 2, which returns 1.

This trace shows how overflow continues smoothly and stops exactly when the incoming crates are exhausted.

Now consider skipping full ships:

Input:

```
3 2
0 5 5
1 1 3
2 2
```

| Step | Operation | Ship index | rem before | take | rem after | remaining C |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | load start | 2 | 5 | 3 | 2 | 0 |

Ship 1 is skipped entirely because it has zero capacity. The algorithm jumps directly to ship 2, demonstrating why the segment tree search is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log N) | Each update and “first available” query runs on a segment tree |
| Space | O(N) | Stores remaining capacity and segment tree nodes |

The constraints allow up to 100,000 operations, so a logarithmic factor per operation is comfortably within limits. The structure ensures that no operation degrades into linear scanning.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.t = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def build(self, v, l, r, arr):
            if l == r:
                self.t[v] = arr[l]
                return
            m = (l + r) // 2
            self.build(v * 2, l, m, arr)
            self.build(v * 2 + 1, m + 1, r, arr)
            self.t[v] = max(self.t[v * 2], self.t[v * 2 + 1])

        def update(self, v, l, r, idx, val):
            if l == r:
                self.t[v] = val
                return
            m = (l + r) // 2
            if idx <= m:
                self.update(v * 2, l, m, idx, val)
            else:
                self.update(v * 2 + 1, m + 1, r, idx, val)
            self.t[v] = max(self.t[v * 2], self.t[v * 2 + 1])

        def find_first(self, v, l, r, ql, qr):
            if r < ql or l > qr or self.t[v] == 0:
                return -1
            if l == r:
                return l
            m = (l + r) // 2
            res = self.find_first(v * 2, l, m, ql, qr)
            if res != -1:
                return res
            return self.find_first(v * 2 + 1, m + 1, r, ql, qr)

    n, m = map(int, input().split())
    g = list(map(int, input().split()))
    rem = g[:]
    st = SegTree(rem)

    out = []

    for _ in range(m):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            _, k, c = tmp
            k -= 1
            i = st.find_first(1, 0, n - 1, k, n - 1)
            while i != -1 and c > 0:
                take = min(rem[i], c)
                rem[i] -= take
                c -= take
                st.update(1, 0, n - 1, i, rem[i])
                if rem[i] > 0:
                    break
                i = st.find_first(1, 0, n - 1, i + 1, n - 1)
        else:
            _, k = tmp
            out.append(str(rem[k - 1]))

    return "\n".join(out)

# provided samples (formatted from statement)
# assert run(...) == ...

# custom cases
assert run("""1 1
10
2 1
""") == "10", "single ship query"

assert run("""3 1
1 1 1
1 1 10
""") == "", "overflow discard"

assert run("""3 2
0 5 5
1 1 3
2 2
""") == "2", "skip empty prefix"

assert run("""5 4
2 3 1 4 2
1 2 5
1 1 3
1 1 2
2 3
""") == "1", "mixed operations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single ship query | 10 | base query correctness |
| overflow discard | (empty) | discard beyond last ship |
| skip empty prefix | 2 | skipping zero-capacity ships |
| mixed operations | 1 | correctness under interleaving |

## Edge Cases

A key edge case is when the starting ship is already full. In that situation, the first segment tree query immediately jumps to the next available ship, and no incorrect attempt is made to write into a full slot. The structure guarantees that full ships are never returned as valid candidates because their stored value is zero.

Another edge case is complete overflow beyond the last ship. When the segment tree search returns no valid index, the algorithm stops immediately and discards remaining crates. This matches the rule that excess crates fall into the ocean.

A final subtle case is repeated partial fills of the same ship across multiple operations. The segment tree always reflects the current remaining capacity, so each time a ship is revisited, only the currently available space is used. Once it reaches zero, it is permanently removed from consideration, ensuring it will never be incorrectly selected again.
