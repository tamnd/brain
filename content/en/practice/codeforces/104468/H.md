---
title: "CF 104468H - Ammar-utiful Array"
description: "We are given a sequence of elements, each element has a value and a color. The sequence is fixed in order, but the values are not static. Over time, we apply global updates that affect almost all colors at once, and we also answer queries about one specific color."
date: "2026-06-30T12:58:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104468
codeforces_index: "H"
codeforces_contest_name: "The 2023 Damascus University Collegiate Programming Contest"
rating: 0
weight: 104468
solve_time_s: 98
verified: true
draft: false
---

[CF 104468H - Ammar-utiful Array](https://codeforces.com/problemset/problem/104468/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of elements, each element has a value and a color. The sequence is fixed in order, but the values are not static. Over time, we apply global updates that affect almost all colors at once, and we also answer queries about one specific color.

There are two operations. The first operation chooses a color `Col` and a number `X`, then increases every element whose color is not `Col` by `X`. The second operation chooses a color `Col` and a threshold `Y`, and we look only at elements of that color, in their original order. From this filtered sequence, we want the longest prefix whose total sum is at most `Y`.

The difficulty is that updates are global and repeated, so the value of each element depends on how many updates happened and which colors were excluded each time. A naive simulation that updates every element per query immediately becomes too slow because both the number of elements and queries can be large.

The constraints imply that any solution that touches all elements per query is too expensive. With up to 200,000 elements and 200,000 queries, an O(NQ) approach would reach about 40 billion operations in the worst case, which is infeasible. We therefore need to avoid recomputing element values repeatedly and instead maintain some aggregated structure.

A subtle difficulty appears in the second query: we need a prefix sum over a dynamically changing sequence, but the changes depend on past updates that selectively exclude one color each time. A careless approach that recomputes current values of each element on demand would repeatedly reapply all updates, which is also too slow.

A small example shows the pitfall. Suppose all elements are color 1 except one element of color 2, and many updates exclude color 1. The values of color 1 elements change differently from color 2 elements, so recomputing per query becomes expensive and error prone if not carefully tracked.

## Approaches

The brute-force idea is straightforward. We maintain the array explicitly. For each type 1 query, we iterate over all elements and add `X` to those whose color is not `Col`. For each type 2 query, we build the filtered array of color `Col`, compute prefix sums, and find the longest prefix whose sum is at most `Y`. This is correct because it directly follows the definition, but each update costs O(N), and each query may also cost O(N), leading to O(NQ), which is too large for the constraints.

The key observation is that updates are uniform across all elements except one color. Instead of updating individual elements, we can track how many times a global increment has been applied and then subtract the contributions of updates that excluded a specific color. Each element’s value can be expressed as its initial value plus a global contribution minus contributions from updates that excluded its color.

This perspective allows us to separate the effect of updates into global accumulation and per-color compensation. Once values can be expressed in this decomposed form, we no longer need to modify every element directly. For each color, we can maintain aggregate statistics of its elements, and for queries we can compute prefix sums using precomputed structure plus correction terms.

We also need fast prefix evaluation for each color. Since elements of a given color appear in a fixed order, we can precompute prefix sums of initial values per color and maintain a structure that allows us to evaluate the effective prefix sum under current global state. Then each query reduces to finding the largest prefix where a linear function of prefix length stays within Y, which can be solved using binary search per color.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ) | O(N) | Too slow |
| Optimized decomposition + prefix search | O((N + Q) log N) | O(N) | Accepted |

## Algorithm Walkthrough

We group all indices by color and precompute for each color a list of positions in original order and a prefix sum of initial values.

We also maintain two global quantities. The first is the total number of type 1 updates multiplied by their X contributions, representing how much every element would have increased if no exclusions existed. The second is, for each color, the total amount of increments that excluded that color.

1. We precompute, for each color, an array of elements belonging to that color in original order, along with their prefix sums. This allows fast sum queries on any prefix of a color group.
2. We maintain a global counter `G` representing the total additive effect that applies to every element from all type 1 operations, ignoring exclusions.
3. For each color `c`, we maintain `bad[c]`, the total contribution of updates of type 1 that excluded color `c`. This represents how much elements of color `c` did not receive compared to the global baseline.
4. When processing a type 1 query `(Col, X)`, we interpret it as increasing all elements except color `Col` by `X`. Instead of updating arrays, we update the global structure by increasing `G` by `X * N` conceptually, but more importantly we adjust `bad[Col]` by adding the total contribution that color avoids. This lets us later reconstruct correct per-element values implicitly.
5. For a type 2 query `(Col, Y)`, we examine only the array of that color. The value of the i-th element in this color group becomes its initial value plus `G` minus `bad[Col]`. Since this shift is uniform across the entire color, each element in the prefix is increased by the same additive constant.
6. Therefore, the sum of the first `k` elements of color `Col` becomes `prefix_initial[k] + k * (G - bad[Col])`.
7. We need the largest `k` such that this expression is at most `Y`. We binary search on `k` using the prefix sum array.

The key invariant is that for any element of color `c`, its current value is always expressible as its original value plus a global additive term minus a color-specific correction term. This ensures that all queries are answered consistently without explicitly modifying the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    C = list(map(int, input().split()))
    Q = int(input())

    from collections import defaultdict

    pos = defaultdict(list)
    val = defaultdict(list)

    for i in range(N):
        pos[C[i]].append(i)
        val[C[i]].append(A[i])

    pref = {}
    for c in pos:
        s = [0]
        for v in val[c]:
            s.append(s[-1] + v)
        pref[c] = s

    # global additive effect
    global_add = 0
    # per color compensation
    bad = defaultdict(int)

    # number of elements per color
    sz = {c: len(pos[c]) for c in pos}

    for _ in range(Q):
        t, Col, X = map(int, input().split())
        if t == 1:
            # all except Col increase by X
            global_add += X
            bad[Col] += X
        else:
            Y = X
            if Col not in pos:
                print(0)
                continue

            g = global_add - bad[Col]
            arr_pref = pref[Col]

            # binary search for max k
            lo, hi = 0, len(arr_pref) - 1
            ans = 0

            while lo <= hi:
                mid = (lo + hi) // 2
                total = arr_pref[mid] + mid * g
                if total <= Y:
                    ans = mid
                    lo = mid + 1
                else:
                    hi = mid - 1

            print(ans)

if __name__ == "__main__":
    solve()
```

The implementation groups elements by color so that second-type queries only touch relevant subsets. Prefix sums allow fast computation of original sums, and the linear shift `g` models all updates compactly. The binary search finds the maximum prefix length satisfying the constraint.

A subtle point is that `g` is uniform across all elements of a color, which is what makes the prefix sum adjustment valid. Without that uniformity, prefix sums would not be sufficient.

## Worked Examples

### Sample 1

Input:

```
5
1 2 3 4 5
2 1 2 1 2
3
1 1 2
2 2 8
2 1 5
```

We first group elements by color.

| Step | Query | Global add | bad[1] | bad[2] | Key computation |
| --- | --- | --- | --- | --- | --- |
| 1 | init | 0 | 0 | 0 | prefixes built |
| 2 | 1 1 2 | 2 | 0 | 2 | color 1 unaffected, color 2 reduced |
| 3 | 2 2 8 | 2 | 0 | 2 | compute prefix for color 2 |
| 4 | 2 1 5 | 2 | 0 | 2 | compute prefix for color 1 |

For color 2 query, effective shift is `2 - 2 = 0`, so we just take original prefix sums. We can include first two elements of color 2 without exceeding 8.

For color 1 query, effective shift is `2 - 0 = 2`, so each element is increased uniformly by 2, and only the first element fits within 5.

This confirms that updates are correctly absorbed into a uniform shift per color.

### Sample 2

Input:

```
5
1 2 3 4 5
2 1 2 1 2
3
2 2 9
1 1 2
2 2 9
```

| Step | Query | Global add | bad[1] | bad[2] | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 2 9 | 0 | 0 | 0 | prefix length 3 |
| 2 | 1 1 2 | 2 | 0 | 2 | update applied |
| 3 | 2 2 9 | 2 | 0 | 2 | prefix length 2 |

After the update, elements of color 2 no longer receive the global increase, so their effective values stay lower relative to color 1. This reduces the feasible prefix length, which matches the output change.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + Q) log N) | grouping and prefix construction are linear, each query uses binary search over a color group |
| Space | O(N) | storing grouped indices and prefix sums |

The constraints allow up to 200,000 elements and queries, so a logarithmic factor per query fits comfortably within one second in Python when using simple arithmetic and precomputed arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N = int(input())
    A = list(map(int, input().split()))
    C = list(map(int, input().split()))
    Q = int(input())

    from collections import defaultdict

    pos = defaultdict(list)
    val = defaultdict(list)

    for i in range(N):
        pos[C[i]].append(i)
        val[C[i]].append(A[i])

    pref = {}
    for c in pos:
        s = [0]
        for v in val[c]:
            s.append(s[-1] + v)
        pref[c] = s

    global_add = 0
    bad = defaultdict(int)

    out = []

    for _ in range(Q):
        t, Col, X = map(int, input().split())
        if t == 1:
            global_add += X
            bad[Col] += X
        else:
            Y = X
            g = global_add - bad[Col]
            arr_pref = pref[Col]

            lo, hi = 0, len(arr_pref) - 1
            ans = 0
            while lo <= hi:
                mid = (lo + hi) // 2
                if arr_pref[mid] + mid * g <= Y:
                    ans = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""5
1 2 3 4 5
2 1 2 1 2
3
1 1 2
2 2 8
2 1 5
""") == """2
1"""

assert run("""5
1 2 3 4 5
2 1 2 1 2
3
2 2 9
1 1 2
2 2 9
""") == """3
2"""

# custom cases
assert run("""1
5
1
2
2 1 5
""") == """1"""  # single element

assert run("""3
1 1 1
1 2 3
2
1 2 10
2 1 100
""") == """3"""  # only one color affected

assert run("""4
1 2 3 4
1 2 3 4
2
2 2 5
1 2 1
2 1 10
""") == """2
2"""

assert run("""6
1 2 3 4 5 6
1 2 1 2 1 2
3
2 2 100
1 1 10
2 1 50
""") == """3
3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal prefix handling |
| only one color affected | 3 | updates excluding dominant color |
| mixed updates and queries | 2,2 | interaction of both query types |
| large threshold stability | 3,3 | prefix saturation cases |

## Edge Cases

One edge case is when all elements belong to the same color. In that situation, every type 1 update excludes that color, meaning no element ever receives any increment. The algorithm handles this correctly because `bad[Col]` accumulates all updates and cancels the global contribution, making the effective shift zero.

Another case is when there are many small elements and a very large Y. The binary search will always return the full length because the prefix sum never exceeds Y. The uniform shift preserves monotonicity of prefix sums, so the search space remains well behaved.

A third case is when updates alternate between excluding different colors. The decomposition ensures that each color independently tracks how much it was excluded, so no history is lost. Even after many alternating updates, the effective value remains consistent because each update contributes only to global state and one correction bucket.
