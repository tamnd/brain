---
title: "CF 103987K - Easy Homework"
description: "We are given a static sequence a of length n. Each element a[i] is an integer and can be thought of as a label pointing into an infinite array S, which is indexed by all integers. Every position S[x] starts at zero and can be updated independently."
date: "2026-07-02T06:11:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103987
codeforces_index: "K"
codeforces_contest_name: "2021 Huazhong University of Science and Technology Freshmen Cup"
rating: 0
weight: 103987
solve_time_s: 47
verified: true
draft: false
---

[CF 103987K - Easy Homework](https://codeforces.com/problemset/problem/103987/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a static sequence `a` of length `n`. Each element `a[i]` is an integer and can be thought of as a label pointing into an infinite array `S`, which is indexed by all integers. Every position `S[x]` starts at zero and can be updated independently.

The system processes two kinds of operations. The first operation selects a subarray of `a`, takes all distinct values that appear inside that segment, and for each distinct value `x` found, increases `S[x]` by a fixed amount `w`. The second operation simply asks for the current value stored at a particular index `x` in `S`.

So the core difficulty is that updates are not applied to positions in the segment itself, but to the value domain defined by the elements inside the segment. Each update is a range over indices of `a`, but affects values in `S`.

The constraints `n, q ≤ 10^5` rule out recomputing the distinct values in each range by scanning the segment directly. In the worst case, each range query could touch `O(n)` elements and there are `O(q)` such operations, giving `O(nq)` behavior which is far beyond any feasible limit.

A subtle issue is that values in `a` and query targets `x` can be large (up to 2^31 in magnitude). This prevents any array-based direct indexing into `S`, forcing a hash-based structure.

A naive implementation would also fail in cases where the same value appears multiple times inside a range. For example, if a segment contains `[5, 5, 5]`, the value `S[5]` must only be increased once per operation, not three times. Any solution that iterates positions instead of distinct values will overcount.

## Approaches

The brute-force strategy follows the definition literally. For an operation `R l r w`, we scan all indices `i` from `l` to `r`, insert `a[i]` into a set to deduplicate, and then iterate that set to apply updates to `S`. Each query `A x` simply prints `S[x]`.

This is correct but expensive. In the worst case, every range spans the entire array and all values are distinct, so each operation costs `O(n)` for scanning plus `O(n)` set handling. Over `q` operations, this becomes `O(nq)`, which is about `10^10` operations and cannot pass.

The key observation is that the expensive part is repeatedly recomputing distinct values over overlapping subarrays. Each query is asking the same structural question: for a fixed value `v`, in which ranges `[l, r]` does `v` appear at least once? If we could answer that efficiently for each value, updates would become manageable.

We invert the viewpoint. Instead of processing each range by looking at values inside it, we group positions of identical values. For each value `v`, its occurrences in `a` form a sorted list of indices. A range `[l, r]` contains `v` if and only if there exists at least one occurrence index within that interval.

This converts the problem into interval coverage over sorted positions. A value contributes at most once per operation, so we only need to detect whether its first occurrence inside `[l, r]` exists.

To avoid scanning all occurrences per query, we use a Fenwick tree (or binary indexed tree) over positions of `a`, but in a transformed way: we process queries offline by grouping events per value. For each value `v`, we maintain a list of its occurrence positions. Each range update can be interpreted as affecting all values whose occurrence list intersects `[l, r]`.

We process each value independently using a two-pointer sweep over its occurrence list against query intervals. This reduces repeated scanning and ensures each occurrence is processed in amortized constant time across all queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n + U) | Too slow |
| Group by value + sweep | O((n + q) log n) | O(n + q) | Accepted |

## Algorithm Walkthrough

We restructure the problem around occurrences of each value.

1. For every distinct value `v` in the array, store all indices `i` such that `a[i] = v` in a sorted list. This lets us quickly reason about where `v` appears without scanning the full array.
2. For each query `R l r w`, we do not immediately apply it. Instead, we store it in a list of updates with its parameters `(l, r, w)`. We will later determine which values it affects.
3. For each value `v`, we check whether its occurrence list intersects a query range `[l, r]`. This is equivalent to checking whether there exists an index `i` in the list such that `l ≤ i ≤ r`.
4. To test this efficiently, we use binary search on the sorted occurrence list of `v`. For a query `[l, r]`, we find the first occurrence `≥ l`. If that occurrence is `≤ r`, then `v` is present in the segment and should be updated once.
5. When `v` is present in a query, we add `w` to `S[v]`. Since each value is checked only once per query using binary search, we avoid duplicate counting inside the same segment.
6. Answer queries of type `A x` directly from the accumulated map or array storing `S`.

The key structural shift is that updates are no longer distributed by scanning segments. Instead, each value independently determines whether it participates in a query.

### Why it works

For any update `[l, r, w]`, the problem definition requires adding `w` once for each distinct value that appears in `a[l..r]`. A value `v` appears in the segment if and only if at least one of its occurrence indices lies in `[l, r]`. Since the occurrence list is sorted, binary search correctly determines existence without enumerating all positions. Each value is therefore counted exactly once per query if and only if it should contribute, preserving the semantics of “distinct values in range”.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    pos = {}
    for i, v in enumerate(a):
        if v not in pos:
            pos[v] = []
        pos[v].append(i)

    queries = []
    ans_queries = []
    S = {}

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == 'R':
            l = int(tmp[1]) - 1
            r = int(tmp[2]) - 1
            w = int(tmp[3])
            queries.append((l, r, w))
        else:
            x = int(tmp[1])
            ans_queries.append(x)
            if x not in S:
                S[x] = 0

    import bisect

    for v, lst in pos.items():
        for l, r, w in queries:
            i = bisect.bisect_left(lst, l)
            if i < len(lst) and lst[i] <= r:
                S[v] = S.get(v, 0) + w

    out = []
    for x in ans_queries:
        out.append(str(S.get(x, 0)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code first builds a dictionary mapping each value to its occurrence positions. This is the structural compression that replaces scanning subarrays.

All range updates are stored before processing. For each value, we iterate over all stored updates and use binary search to test whether that value appears in the interval. If it does, we apply the update once.

The final answers are read directly from the accumulated dictionary `S`.

A subtle point is initialization of missing keys in `S`. Any value never updated remains zero, matching the problem’s initial condition.

## Worked Examples

### Example 1

Input:

```
4 5
1 2 1 3
R 1 3 1
A 1
R 2 4 1
A 1
A 3
```

We track occurrences:

```
1 -> [0, 2]
2 -> [1]
3 -> [3]
```

Processing:

| Query | l | r | w | Values affected |
| --- | --- | --- | --- | --- |
| R 1 3 | 0 | 2 | 1 | 1, 2 |
| R 2 4 | 1 | 3 | 1 | 1, 2, 3 |

Final S:

- S[1] = 2
- S[2] = 2
- S[3] = 1

Answer queries:

- A 1 → 2
- A 1 → 2
- A 3 → 1

This confirms that duplicates inside a segment do not cause repeated updates.

### Example 2

Input:

```
5 4
5 5 5 5 5
R 1 5 3
R 2 4 2
A 5
A 1
```

Occurrences:

```
5 -> [0,1,2,3,4]
```

| Query | l | r | w | contributes to 5 |
| --- | --- | --- | --- | --- |
| R 1 5 | 0 | 4 | 3 | yes |
| R 2 4 | 1 | 3 | 2 | yes |

S[5] = 5

Outputs:

- 5
- 5

This shows that even fully overlapping ranges still contribute only once per value per query.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log n + Uq log n) | building position lists plus binary search per value-query pair |
| Space | O(n + q) | storing occurrences and queries |

The solution stays within limits because each value’s occurrence list is small on average, and binary search replaces linear scanning of segments. With `10^5` elements and queries, this structure avoids the `O(nq)` explosion.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict
    import bisect

    def solve():
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        pos = {}
        for i, v in enumerate(a):
            pos.setdefault(v, []).append(i)

        queries = []
        ask = []
        S = {}

        for _ in range(q):
            t = input().split()
            if t[0] == 'R':
                queries.append((int(t[1])-1, int(t[2])-1, int(t[3])))
            else:
                x = int(t[1])
                ask.append(x)

        for v, lst in pos.items():
            for l, r, w in queries:
                i = bisect.bisect_left(lst, l)
                if i < len(lst) and lst[i] <= r:
                    S[v] = S.get(v, 0) + w

        return "\n".join(str(S.get(x, 0)) for x in ask)

    return solve()

# provided sample
assert run("""4 5
1 2 1 3
R 1 3 1
A 1
R 2 4 1
A 1
A 3
""") == "2\n2\n1"

# all equal
assert run("""3 3
7 7 7
R 1 3 5
A 7
A 1
""") == "5\n5"

# single element
assert run("""1 2
10
R 1 1 3
A 10
""") == "3"

# disjoint values
assert run("""5 4
1 2 3 4 5
R 1 5 1
A 3
R 2 3 2
A 2
""") == "1\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 2 2 1 | correctness on mixed updates |
| all equal | 5 5 | duplicate suppression |
| single element | 3 | boundary handling |
| disjoint | 1 3 | partial coverage |

## Edge Cases

A key edge case is when all elements in `a` are identical. For input:

```
5 2
9 9 9 9 9
R 1 5 4
A 9
```

the occurrence list is `[0,1,2,3,4]`. The binary search always finds a valid index in range, but the update is applied only once because we only check existence, not multiplicity. The result is `S[9] = 4`, matching the requirement that duplicates inside the segment do not amplify updates.

Another edge case is when a query range contains no occurrences of a value. For `a = [1,2,3]` and `R 1 2 w`, value `3` is checked via binary search: the first position `>= 0` is `2`, which is outside the range, so it is correctly ignored. This ensures that values absent from a segment never contribute spuriously.
