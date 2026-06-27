---
title: "CF 105020N - How many rectangles?"
description: "Each rectangle in the input is fully determined by its bottom-left corner and its top-right corner. Because all rectangles start in the non-negative quadrant, the origin (0, 0) acts as a natural reference point. A query gives a point (x, y)."
date: "2026-06-28T02:02:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105020
codeforces_index: "N"
codeforces_contest_name: "TCPC Tunisian Collegiate Programming Contest 2022"
rating: 0
weight: 105020
solve_time_s: 77
verified: false
draft: false
---

[CF 105020N - How many rectangles?](https://codeforces.com/problemset/problem/105020/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

Each rectangle in the input is fully determined by its bottom-left corner and its top-right corner. Because all rectangles start in the non-negative quadrant, the origin (0, 0) acts as a natural reference point.

A query gives a point (x, y). This defines an axis-aligned rectangle from the origin up to that point. The task is to count how many of the given rectangles lie completely inside this query rectangle.

A rectangle is fully contained if every point of it is inside the query boundary. Since all rectangles already start from non-negative coordinates, containment reduces to a simple condition on their top-right corners: a rectangle is valid for a query if its top-right corner (x2, y2) satisfies x2 ≤ x and y2 ≤ y.

So the problem is not geometric in a complex sense anymore. It becomes a 2D dominance counting problem over the set of points formed by the rectangles’ upper-right corners.

The constraints n, Q ≤ 100000 imply that any solution close to O(nQ) is impossible. A direct check per query would require up to 10^10 comparisons, which is far beyond time limits. Even O(n log n + Q log n) is necessary, and usually we aim for O((n + Q) log n).

A subtle issue arises from equality handling. Rectangles with x2 exactly equal to query x must be included, and the same applies for y. Any strict inequality mistake would silently undercount.

Another edge case is when many rectangles share the same x2 or y2 values. A naive sorting approach that does not group equal values carefully can lead to incorrect incremental updates if queries are processed in the wrong order.

## Approaches

The brute-force idea is straightforward. For each query, iterate over all rectangles and check whether x2 ≤ x and y2 ≤ y. This is correct because it directly encodes the definition of containment. However, each query costs O(n), and with Q queries this becomes O(nQ), which in the worst case is about 10^10 operations. That is too slow.

The key observation is that rectangles can be reduced to points (x2, y2), and each query asks for how many points lie in the lower-left quadrant bounded by (x, y). This is a classic prefix counting problem in two dimensions.

If we sort rectangles by x2, we can process queries in increasing order of x. As we move through queries, we maintain a data structure that stores all y2 values of rectangles whose x2 is already small enough. Then each query reduces to a 1D prefix count over y.

A Fenwick Tree (Binary Indexed Tree) over compressed y-coordinates allows us to maintain counts and answer prefix sums in logarithmic time. Each rectangle is inserted once, and each query performs one prefix sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nQ) | O(1) | Too slow |
| Sorting + Fenwick Tree | O((n + Q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Replace each rectangle by a point (x2, y2). This works because only the top-right corner determines containment, and the bottom-left corner is irrelevant for this problem since all rectangles start from non-negative coordinates.
2. Store all queries as triples (x, y, index), because we need to return answers in the original order.
3. Sort rectangles by x2 in increasing order. Also sort queries by x in increasing order. This ensures that when we process a query, all rectangles with x2 ≤ x are already considered.
4. Compress all y2 values and all query y values into a smaller coordinate range. This allows the Fenwick Tree to operate efficiently even though original coordinates go up to 10^9.
5. Sweep through queries in increasing order of x. Maintain a pointer over rectangles. For each query, insert all rectangles with x2 ≤ current query x into the Fenwick Tree, updating their y2 frequency.
6. For each query, compute how many inserted rectangles have y2 ≤ query y using a prefix sum query on the Fenwick Tree. Store the result.
7. Output results in the original query order.

### Why it works

At every query point x, the data structure contains exactly the set of rectangles whose x2 is small enough to fit inside the query boundary. The Fenwick Tree maintains counts over y2 values, so querying a prefix over y directly counts exactly those rectangles that also satisfy y2 ≤ y. Since both conditions are enforced incrementally and independently, no rectangle is ever double counted or missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    n = int(input())
    rects = []
    ys = []

    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        rects.append((x2, y2))
        ys.append(y2)

    q = int(input())
    queries = []
    for i in range(q):
        x, y = map(int, input().split())
        queries.append((x, y, i))
        ys.append(y)

    ys = sorted(set(ys))
    def get(v):
        l, r = 0, len(ys) - 1
        while l <= r:
            m = (l + r) // 2
            if ys[m] <= v:
                l = m + 1
            else:
                r = m - 1
        return l

    rects.sort()
    queries.sort()

    fw = Fenwick(len(ys))
    ans = [0] * q

    i = 0
    for x, y, idx in queries:
        while i < n and rects[i][0] <= x:
            fw.add(get(rects[i][1]), 1)
            i += 1
        ans[idx] = fw.sum(get(y))

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The implementation first reduces the geometry to a sorted sweep problem. The Fenwick tree is responsible only for y-prefix counting, while the sorting step ensures x constraints are enforced by construction. Coordinate compression is necessary because direct indexing with values up to 10^9 would be infeasible.

The binary search inside `get` converts a y-coordinate into its compressed index. Using `<= v` ensures that equality is handled correctly so that rectangles exactly on the boundary are included.

## Worked Examples

Consider rectangles (1, 2)-(7, 6), (7, 0)-(10, 3), and query (8, 10).

We transform rectangles into points (7, 6) and (10, 3). After sorting, we process in x order.

| Step | Processed Rectangles | Fenwick Content (y2 counts) | Query | Result |
| --- | --- | --- | --- | --- |
| 1 | (7,6) | {6:1} | (8,10) | 1 |
| 2 | (10,3) not included yet | {6:1} | - | - |

The query includes only (7,6) because 7 ≤ 8 and 6 ≤ 10, while (10,3) is excluded due to x2 > 8.

Now consider a second example with rectangles (2,2)-(5,5), (1,1)-(3,3), (4,4)-(6,6) and queries (3,3) and (6,6).

| Query | Active rectangles | Count condition result |
| --- | --- | --- |
| (3,3) | (3,3), (5,5 not yet in x order), (6,6 not yet) | 1 |
| (6,6) | all rectangles | 3 |

This confirms that the sweep correctly accumulates valid rectangles as x increases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Sorting plus Fenwick updates and queries |
| Space | O(n + q) | Storage for rectangles, queries, and compressed coordinates |

The operations scale comfortably within limits because each rectangle and query is processed a constant number of logarithmic Fenwick operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return capture_output(solve)

def capture_output(func):
    import sys, io
    old = sys.stdout
    sys.stdout = io.StringIO()
    func()
    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# minimal
assert run("""1
1 0 2 3
1
2 3
""") == "1"

# boundary equality
assert run("""2
1 1 3 3
3 3 5 5
1
3 3
""") == "1"

# all rectangles inside
assert run("""3
1 1 2 2
2 2 3 3
3 3 4 4
1
5 5
""") == "3"

# none inside
assert run("""2
5 5 10 10
6 6 9 9
1
4 4
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | 1 | base correctness |
| equality case | 1 | boundary inclusion |
| all inside | 3 | accumulation correctness |
| none inside | 0 | exclusion logic |

## Edge Cases

One important edge case is when rectangles share identical x2 or y2 values. The algorithm handles this safely because sorting and Fenwick updates do not depend on uniqueness; each rectangle is inserted independently and counted through frequency increments.

Another case is when a query lies exactly on a rectangle boundary. Since both x2 ≤ x and y2 ≤ y are used with non-strict comparisons through coordinate compression and prefix sums, boundary rectangles are correctly included.

Finally, when all rectangles lie outside the maximum query range, the Fenwick tree remains empty during all queries, producing zero counts consistently without special handling.
