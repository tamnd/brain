---
title: "CF 105007B - Corgi Hike"
description: "We are given a one-dimensional terrain described by an array of elevations. Each index represents a location along a path, and each location has a height value."
date: "2026-06-28T03:10:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105007
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 03-01-24 Div. 2 (Beginner)"
rating: 0
weight: 105007
solve_time_s: 175
verified: false
draft: false
---

[CF 105007B - Corgi Hike](https://codeforces.com/problemset/problem/105007/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a one-dimensional terrain described by an array of elevations. Each index represents a location along a path, and each location has a height value. For any two queried positions $i$ and $j$, we must decide whether a straight line of sight exists between them under a specific obstruction rule.

The rule says that the segment between $i$ and $j$ blocks visibility if there exists any intermediate position whose elevation is at least as high as the taller of the two endpoints. In other words, if we define $H = \max(e_i, e_j)$, then every index strictly between $i$ and $j$ must have elevation strictly less than $H$ for the two endpoints to be visible.

Each query is independent. We are not updating the terrain, only checking visibility conditions repeatedly.

The constraints allow up to $N = 100{,}000$ positions but only up to $q = 100$ queries. This imbalance is the key structural hint. Any solution that preprocesses aggressively or spends logarithmic work per query is acceptable, while anything linear per query still passes comfortably, since $100 \times 100{,}000 = 10^7$ operations is safe in Python.

A quadratic scan over all pairs of positions is ruled out for preprocessing, but scanning along a single segment per query is still feasible.

One subtle case arises when $i = j$. In that situation, there are no intermediate points, so visibility should always be true.

Another corner case is when the maximum elevation between endpoints is not unique. For example, if both endpoints are equal and some interior point matches that same height, visibility must fail because the condition allows “greater than or equal to,” not strictly greater. A naive solution that checks only for strictly greater interior values will incorrectly accept such cases.

## Approaches

The brute-force approach evaluates each query independently by scanning every index strictly between $i$ and $j$. For a fixed query, we compute $H = \max(e_i, e_j)$ and then check whether any intermediate position has elevation at least $H$. If such a position exists, the answer is “no,” otherwise “yes.”

This approach is correct because it directly implements the definition of visibility. The issue is cost. In the worst case, a single query spans nearly the entire array, so each query costs $O(N)$. With up to 100 queries, the total cost becomes $O(Nq) = 10^7$, which is borderline but still acceptable in Python for tight loops, yet leaves little margin for overhead.

We can avoid unnecessary overhead by recognizing that the structure of the problem does not require preprocessing or advanced data structures. The array is static, and queries are independent, so the simplest linear scan per query is already optimal given constraints.

There is no need for segment trees or RMQ structures because queries are few. The main optimization is conceptual: avoid overengineering and directly implement the condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scan per query | $O(Nq)$ | $O(1)$ | Accepted |
| Segment tree / RMQ | $O((N+q)\log N)$ | $O(N)$ | Accepted but unnecessary |

## Algorithm Walkthrough

1. For each query $(i, j)$, normalize the interval so that we always iterate from left to right. This avoids conditional branching inside the scan and simplifies reasoning about intermediate indices.
2. Compute $H = \max(e_i, e_j)$. This value represents the visibility threshold that any blocking point must reach or exceed.
3. Iterate over all indices strictly between $i$ and $j$. For each position $k$, check whether $e_k \ge H$. If this condition is met, the line of sight is blocked and the answer is immediately “no.”
4. If the scan completes without finding any blocking position, the interval satisfies the visibility rule, so the answer is “yes.”

The key decision point is the early exit during scanning. Once a blocking height is found, continuing the scan has no effect on correctness and only wastes time.

### Why it works

For any pair of endpoints, visibility depends entirely on whether an interior maximum reaches the threshold $H = \max(e_i, e_j)$. The algorithm checks exactly this condition over the full set of interior points. Since every possible obstruction must appear in that set, and every detected obstruction correctly invalidates visibility, the decision is equivalent to the formal definition. No intermediate configuration or global property matters beyond this maximum check.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    e = list(map(int, input().split()))

    for _ in range(q):
        i, j = map(int, input().split())
        i -= 1
        j -= 1

        if i == j:
            print("yes")
            continue

        if i > j:
            i, j = j, i

        H = e[i] if e[i] > e[j] else e[j]

        ok = True
        for k in range(i + 1, j):
            if e[k] >= H:
                ok = False
                break

        print("yes" if ok else "no")

if __name__ == "__main__":
    solve()
```

The solution reads the array once and answers each query independently. Each query normalizes endpoints so the scan direction is consistent. The threshold $H$ is computed directly from endpoint values, and the loop checks only interior indices. The early break is essential to avoid unnecessary scanning when a blocking peak appears early.

Care must be taken with indexing since the input is 1-based but Python arrays are 0-based. The equality case $i = j$ is handled explicitly to avoid an empty-loop ambiguity.

## Worked Examples

### Example 1

Input:

```
5 2
1 3 2 4 1
1 4
2 5
```

For query (1, 4), endpoints are 1 and 4, so $H = 4$. We inspect positions 2 and 3. Their values are 3 and 2, both below 4, so visibility holds.

For query (2, 5), endpoints are 3 and 1, so $H = 3$. We inspect positions 3 and 4, which are 2 and 4. Since 4 is at least 3, visibility fails.

| Query | i | j | H | Interior values | Blocking? | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 4 | 3, 2 | No | yes |
| 2 | 2 | 5 | 3 | 2, 4 | Yes | no |

This confirms that the algorithm correctly distinguishes between a clean descent and an intermediate peak that blocks sight.

### Example 2

Input:

```
4 1
5 5 5 5
1 4
```

Here $H = 5$, and every interior value is 5, which satisfies the blocking condition immediately. The algorithm finds the first interior index and rejects the query.

| k | e[k] | Compare with H=5 | Status |
| --- | --- | --- | --- |
| 2 | 5 | ≥ | block |
| 3 | - | stop early | - |

This shows that equality is correctly treated as blocking, which is essential for correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Nq)$ | Each query may scan a full segment of the array in the worst case |
| Space | $O(1)$ | Only a fixed number of variables are used beyond input storage |

With $N \le 10^5$ and $q \le 100$, the worst-case work is around $10^7$ comparisons, which is comfortably within limits for Python given simple integer comparisons and early exits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-style tests
assert run("""5 2
1 3 2 4 1
1 4
2 5
""") == "yes\nno"

# minimum size
assert run("""1 1
10
1 1
""") == "yes"

# all equal
assert run("""4 2
7 7 7 7
1 4
2 3
""") == "no\nno"

# no blockers
assert run("""5 1
1 2 3 4 5
1 5
""") == "yes"

# endpoint reversed order
assert run("""5 1
5 1 4 2 3
5 1
""") == "no"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | yes | i = j case |
| all equal | no/no | equality blocking rule |
| increasing array | yes | no interior blockers |
| reversed endpoints | no | normalization of i, j |

## Edge Cases

A critical edge case is when all interior points equal the endpoint maximum. Consider:

```
4 1
5 5 5 5
1 4
```

Here $H = 5$. The loop checks index 2 first, finds $e_2 = 5 \ge 5$, and immediately returns “no.” This confirms that equality must block visibility, not just strictly greater values.

Another case is a single-point query:

```
3 1
10 1 2
2 2
```

Since $i = j$, the algorithm skips scanning entirely and returns “yes,” matching the definition that a point is always visible to itself.

Finally, reversed endpoints:

```
3 1
1 100 1
3 1
```

The algorithm swaps indices, computes $H = 1$, and checks only index 2. Since $100 \ge 1$, it correctly outputs “no.”
