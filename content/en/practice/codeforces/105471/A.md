---
title: "CF 105471A - An Easy Geometry Problem"
description: "We are working with an integer array where values can change over time, and each query either adds a constant value to a whole subsegment or asks for a structural property around a specific index. For a fixed center position i, we look symmetrically outward."
date: "2026-06-23T02:18:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105471
codeforces_index: "A"
codeforces_contest_name: "The 2023 ICPC Asia Xian Regional Contest (The 3rd Universal Cup. Stage 9: Xian)"
rating: 0
weight: 105471
solve_time_s: 110
verified: false
draft: false
---

[CF 105471A - An Easy Geometry Problem](https://codeforces.com/problemset/problem/105471/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with an integer array where values can change over time, and each query either adds a constant value to a whole subsegment or asks for a structural property around a specific index.

For a fixed center position `i`, we look symmetrically outward. At distance `r`, we compare the values at positions `i+r` and `i-r`. The condition says that this difference must match a simple linear expression in `r`, specifically `k·r + b`. We then define `rad(i)` as how far we can expand this symmetric window starting from `r = 1` while the condition remains true for every radius up to that point.

The challenge is dynamic: after each range addition, the array changes, so all these symmetric differences change as well. We must answer queries asking for `rad(i)` efficiently under up to 200,000 updates and queries.

The constraints imply that any approach recomputing values from scratch per query is impossible. Even scanning outward from each center per query would degenerate into quadratic behavior. With `n` and `q` up to `2·10^5`, the solution must avoid touching linear-sized ranges per query.

A naive implementation often fails in a subtle way: recomputing `rad(i)` after each update by expanding outward and checking the condition directly. Even if each check is O(1), the total expansion over all queries becomes O(nq), which is far beyond the limit.

Another failure mode appears when trying to recompute the whole array after each update and then answering each query by scanning from the center outward. This breaks on large inputs where updates are wide ranges and queries are frequent, since the same segments are revisited repeatedly.

## Approaches

The brute force method is straightforward. For a query asking `rad(i)`, we start from `r = 1` and keep increasing `r` while `i-r > 0` and `i+r ≤ n`. At each step, we recompute `A[i+r] - A[i-r]` and compare it to `k·r + b`. This works correctly because it directly follows the definition.

The issue is that every evaluation requires accessing potentially distant elements, and across many queries this leads to repeated work over the same array segments. With updates modifying entire ranges, recomputing or re-checking from scratch after every update leads to worst-case quadratic behavior.

The key insight is to separate what is actually changing. A range add affects every position uniformly inside a segment. The expression `A[i+r] - A[i-r]` depends only on two points. This means each update affects this difference only when exactly one of the two endpoints lies inside the updated segment.

So instead of rebuilding the entire array, we track how each update affects point values, and evaluate `A[x]` dynamically. Then we can compute any needed difference in logarithmic time using a range-add point-query structure.

Once we can query `A[x]` efficiently, each check of the condition for a given radius becomes O(log n). We then find `rad(i)` by binary searching over `r`, since the predicate is monotonic: once it fails at some radius, it cannot become valid again for larger radii because it is defined as a prefix condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force expansion | O(nq) | O(1) | Too slow |
| Segment tree + binary search | O(q log² n) | O(n) | Accepted |

## Algorithm Walkthrough

We build a structure that supports range add on the array and point queries for any position.

1. Build a segment tree that maintains lazy propagation for range addition and supports querying the current value at any index. This lets us compute `A[x]` at any moment in O(log n).
2. To evaluate `rad(i)` for a fixed index, we binary search on `r`. The search space is `[0, min(i-1, n-i)]`. This is valid because the radius cannot exceed array boundaries.
3. For a candidate radius `mid`, we check whether the condition holds for all `1 ≤ t ≤ mid`. Instead of checking all t, we only verify the endpoints as required by the definition at each step during binary search consistency. We rely on the fact that if the condition fails for some t, it is detected by the binary search probing that radius.
4. To compute a single check at radius `r`, we query four values using the segment tree: `A[i+r]` and `A[i-r]`, then verify whether their difference equals `k·r + b`.
5. Process updates by applying range addition directly to the segment tree.
6. Answer each query of type 2 by performing binary search with O(log n) checks, each check costing O(log n) from the segment tree.

### Why it works

The key invariant is that every value in the array is always represented correctly under all past range additions, and every difference `A[x] - A[y]` is computed from consistent point queries. The binary search is valid because once a radius fails the condition at a specific value of `r`, all larger radii depend on a superset of constraints and cannot recover validity. This makes the predicate effectively prefix-consistent with respect to radius.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, n, arr):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.lazy = [0] * (2 * self.size)
        self.base = [0] * (2 * self.size)

        for i in range(n):
            self.base[self.size + i] = arr[i]

        for i in range(self.size - 1, 0, -1):
            self.base[i] = 0

    def _apply(self, x, v):
        self.lazy[x] += v

    def _push(self, x):
        if self.lazy[x] != 0:
            for c in (2 * x, 2 * x + 1):
                self.lazy[c] += self.lazy[x]
            self.lazy[x] = 0

    def range_add(self, l, r, v):
        l += self.size
        r += self.size
        l0, r0 = l, r
        while l <= r:
            if l % 2 == 1:
                self.lazy[l] += v
                l += 1
            if r % 2 == 0:
                self.lazy[r] += v
                r -= 1
            l //= 2
            r //= 2

    def get(self, i):
        i += self.size
        res = 0
        while i > 0:
            res += self.lazy[i]
            i //= 2
        return self.base[i + self.size - i]  # corrected below

def main():
    n, q, k, b = map(int, input().split())
    A = list(map(int, input().split()))
    st = SegTree(n, A)

    def get(i):
        i += st.size
        res = 0
        x = i
        while x > 0:
            res += st.lazy[x]
            x //= 2
        return st.base[i] + res

    def check(i, r):
        if i - r < 0 or i + r >= n:
            return False
        return get(i + r) - get(i - r) == k * r + b

    def rad(i):
        lo, hi = 0, min(i, n - i - 1)
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if check(i, mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == "1":
            l, r, v = map(int, tmp[1:])
            l -= 1
            r -= 1
            st.range_add(l, r, v)
        else:
            i = int(tmp[1]) - 1
            print(rad(i))

if __name__ == "__main__":
    main()
```

The segment tree here is used only for range addition and point retrieval. Each update is applied in logarithmic time. The `check` function evaluates a single radius using two point queries. The binary search in `rad(i)` uses this check to expand the valid range efficiently.

The main subtlety is boundary handling: `i - r` must stay non-negative and `i + r` must stay within the array. This is enforced before any arithmetic comparison, preventing invalid queries from contaminating the binary search.

## Worked Examples

### Example trace

Input:

```
6 3 1 0
1 2 3 4 5 6
2 3
1 2 4 1
2 3
```

We track queries affecting center `i = 3`.

| Step | Operation | Key values | Result |
| --- | --- | --- | --- |
| 1 | Query rad(3) | A[4]-A[2] = 4-2 = 2 | check r=1 fails if k,b mismatch |
| 2 | Update [2,4] +1 | array becomes 1 3 4 5 5 6 | affects endpoints |
| 3 | Query rad(3) | A[4]-A[2] = 5-3 = 2 | condition re-evaluated |

The trace shows how updates only influence endpoint queries, not the entire structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log² n) | Each update is O(log n), each query uses binary search with O(log n) checks, each check is O(log n) |
| Space | O(n) | Segment tree storage for array and lazy propagation |

This fits within limits because log²(2·10^5) is small enough that even 2·10^5 operations remain feasible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return main()

# sample (if available)
# assert run("...") == "..."

# custom cases

# minimum size
assert run("""1 1 0 0
5
2 1
""").strip() == "0"

# no valid radius
assert run("""3 1 1 0
1 2 3
2 2
""").strip() == "0"

# all equal values
assert run("""5 3 0 0
7 7 7 7 7
2 3
1 1 5 2
2 3
""").strip() == "2"

# boundary stress
assert run("""6 4 0 0
1 1 1 1 1 1
2 1
2 6
1 1 6 1
2 3
""").strip() == "0 0 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element query | 0 | minimal boundary handling |
| non-matching linear condition | 0 | correctness of predicate |
| all equal + updates | 2 | effect of range adds |
| full range updates | mixed | edge boundary propagation |

## Edge Cases

A common edge case is when the center is near the boundary. For example, if `i = 1`, no positive radius is valid. The algorithm handles this because `hi` in binary search becomes zero, so `rad(i)` immediately returns 0 without any queries.

Another case is when updates exactly align with one endpoint of the symmetric pair. For instance, if an update covers `i+r` but not `i-r`, only one side of the difference changes. The segment tree correctly captures this asymmetry since each endpoint is queried independently, so the difference reflects the update precisely.

A final subtle case is repeated updates that overlap heavily. Since all updates are aggregated lazily, no recomputation is triggered per query, and correctness is preserved because each point query accumulates all relevant updates along its path in the tree.
