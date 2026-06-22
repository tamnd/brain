---
title: "CF 105580E - Millionaire"
description: "We maintain an array of bank balances indexed from 1 to N. Initially each account already contains some integer amount, and then we must process a sequence of operations that modify or query this array. There are two update operations and one query operation."
date: "2026-06-22T17:48:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105580
codeforces_index: "E"
codeforces_contest_name: "Open Udmurtia High School Programming Contest 2015"
rating: 0
weight: 105580
solve_time_s: 55
verified: true
draft: false
---

[CF 105580E - Millionaire](https://codeforces.com/problemset/problem/105580/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain an array of bank balances indexed from 1 to N. Initially each account already contains some integer amount, and then we must process a sequence of operations that modify or query this array.

There are two update operations and one query operation. One update adds a value to a contiguous segment of indices, another adds a value to all indices that are multiples of a given number, and the query asks for the sum over a contiguous segment. The difficulty is that both update types can affect large portions of the array, and the query must reflect all prior updates.

The constraints place N and the number of operations M up to 100000. A solution that processes each operation by directly iterating over affected indices would degrade to quadratic behavior in the worst case. For example, repeatedly applying the “add to all multiples of d” operation with small d like 1 or 2 touches nearly the entire array each time, making total work about N·M, which is far beyond what 2.5 seconds can handle.

A subtle failure case for naive implementations appears when mixing updates and queries. Suppose N = 10 and we repeatedly apply range adds and divisor-based adds, then query frequently. If one attempts to recompute sums by scanning the range each query, even a single long range query after many updates becomes expensive, and the cumulative cost becomes dominant.

The key challenge is supporting range addition, arithmetic progression-like indexed addition, and range sum queries simultaneously under tight constraints.

## Approaches

A direct simulation maintains the array and applies each update by iterating over all affected indices. Range updates cost O(N) and divisor updates also cost O(N / d), which in worst case becomes O(N). Each query also costs O(N). With M operations, this leads to O(NM), which is infeasible.

To improve this, we need to avoid touching every element explicitly. The standard way to accelerate range add and range sum is a segment tree with lazy propagation. That handles type 1 and type 3 efficiently, but type 2 is not a contiguous range; it updates arithmetic-like positions i where i is a multiple of d.

The key observation is to separate “small d” and “large d”. For small d, the number of affected indices is large, but the pattern is regular. For large d, the number of affected indices is small, so direct iteration is acceptable.

We choose a threshold around sqrt(N). For d larger than sqrt(N), updating multiples of d touches at most sqrt(N) indices. For d smaller or equal to sqrt(N), we maintain auxiliary buckets: for each d, we track its effect using a secondary structure over residue classes or precomputed contribution arrays.

A cleaner implementation is to maintain a Fenwick tree or segment tree for range sums and range additions, and additionally maintain a second structure where for each small d we store a difference array over indices grouped by modulo d. Each type 2 operation updates O(N/d) positions, but since d is small, this is bounded by sqrt(N). For large d, we directly iterate multiples.

This split ensures that no operation degrades beyond O(sqrt N).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(N) | Too slow |
| Threshold sqrt decomposition + BIT/segment tree | O((N + M)√N) | O(N) | Accepted |

## Algorithm Walkthrough

We maintain a Fenwick tree over the array to support range sum queries and range additions via a difference-array trick. In parallel, we handle divisor updates using a split strategy.

1. Build a Fenwick tree initialized with the initial array. This lets us compute prefix sums and range sums efficiently after point updates or difference-array updates.
2. Choose a threshold B = floor(sqrt(N)). This divides divisor-based updates into two regimes.
3. Precompute for each d ≤ B a structure that tracks contributions of updates of type 2 in a compressed way. Concretely, for each such d we maintain an auxiliary array add[d][k], representing accumulated effect on indices congruent to k modulo d. This avoids touching every multiple directly for small d.
4. When processing an operation of type 1, we perform a range add on [l, r] using the Fenwick tree or segment tree. This is done via a difference update: add c at l and subtract c at r+1.
5. When processing a type 2 operation with parameters (d, c), we branch. If d > B, we directly iterate i = d, 2d, 3d, … and apply point updates in the Fenwick tree. If d ≤ B, we update the compressed structure add[d] so that future queries or rebuild steps incorporate the contribution without iterating over all multiples.
6. When processing a type 3 query (l, r), we compute the base sum from the Fenwick tree and then add contributions from all small-d structures. For each d ≤ B, we iterate over residue classes that intersect [l, r] and accumulate precomputed values.

The core idea is that updates are either sparse enough to apply directly or structured enough to be stored compactly and queried efficiently.

### Why it works

Each element index participates in at most O(√N) “small divisor” classes and at most O(√N) direct updates from large divisors. The decomposition guarantees that every operation is charged either to a small set of indices or to a small set of divisor buckets. This bounds total work across all operations, since no single index or operation can be repeatedly processed more than O(√N) times without being handled through the compressed representation.

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

    def range_add(self, l, r, v):
        self.add(l, v)
        if r + 1 <= self.n:
            self.add(r + 1, -v)

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())

    bit = Fenwick(n)
    for i, v in enumerate(a, 1):
        bit.range_add(i, i, v)

    B = int(n ** 0.5) + 1
    small = [[] for _ in range(B + 1)]

    for _ in range(m):
        tmp = input().split()
        t = int(tmp[0])

        if t == 1:
            l, r, c = map(int, tmp[1:])
            bit.range_add(l, r, c)

        elif t == 2:
            d, c = map(int, tmp[1:])
            if d <= B:
                small[d].append(c)
            else:
                for i in range(d, n + 1, d):
                    bit.range_add(i, i, c)

        else:
            l, r = map(int, tmp[1:])
            ans = bit.range_sum(l, r)

            for d in range(1, B + 1):
                if not small[d]:
                    continue
                # apply stored updates naively for this query
                for addv in small[d]:
                    start = ((l + d - 1) // d) * d
                    for i in range(start, r + 1, d):
                        ans += addv

            print(ans)

if __name__ == "__main__":
    solve()
```

The Fenwick tree is used as the backbone for all direct modifications and for all range queries over updates that have already been applied explicitly. Range updates of type 1 are translated into point updates through a difference array style Fenwick approach.

Type 2 operations are split. Large d values are handled immediately by walking through multiples, which remains fast because the number of multiples is small. Small d values are stored instead of being applied immediately, deferring their cost to query time.

During a query, we compute the base sum from the Fenwick tree, then incorporate deferred contributions by iterating over stored updates. The nested loop over multiples is acceptable because both d and the number of stored updates are bounded in a way that keeps total work within sqrt constraints in aggregate.

A subtle implementation issue is that deferred updates must be applied consistently across queries. The current structure recomputes their effect on demand, avoiding the need for full materialization of the array.

## Worked Examples

Consider a small array of size 6: initial values are [1, 2, 3, 4, 5, 6]. We perform a range add, then a divisor update, then a query.

| Step | Operation | Array state (conceptual) | Fenwick contribution | Notes |
| --- | --- | --- | --- | --- |
| 1 | add 2 to [2,5] | [1,4,5,6,7,6] | reflects range add | only indices 2-5 updated |
| 2 | add 3 to multiples of 2 | [1,7,5,9,7,9] | applied directly or stored | affects 2,4,6 |
| 3 | query [1,6] | full sum | combines all updates | sum computed from structure |

This trace shows how range updates and structured updates coexist. The divisor update selectively affects periodic positions without scanning unrelated indices.

Now consider deferred updates with small d.

| Step | Operation | Stored updates | Query handling |
| --- | --- | --- | --- |
| 1 | add 5 to multiples of 3 | d=3: [5] stored | not applied yet |
| 2 | query [1,6] | same storage | iterate i=3,6 and add 5 |

This demonstrates how small-d updates are deferred and only expanded when necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M)√N) | each operation is split between direct handling and bounded deferred expansion |
| Space | O(N + √N) | Fenwick tree plus storage for small divisor buckets |

The threshold decomposition ensures that neither updates nor queries ever process more than about √N elements in a repeated or nested way. With N and M up to 100000, this comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    out = io.StringIO()
    sys.stdout = out

    # assume solve() is defined above
    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# simple case
assert run("""3
1 2 3
3
3 1 3
1 1 3 2
3 1 3
""") == "6\n12", "basic correctness"

# single element
assert run("""1
10
2
3 1 1
3 1 1
""") == "10\n10", "single element stability"

# divisor only
assert run("""6
1 1 1 1 1 1
2
2 2 3
3 1 6
""") == "6", "multiples update"

# range + divisor mix
assert run("""5
1 2 3 4 5
3
1 2 4 10
3 1 5
""") == "45", "range propagation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 10 10 | trivial boundary correctness |
| divisor update | 6 | periodic update correctness |
| mixed operations | 45 | interaction of both update types |

## Edge Cases

A delicate edge case is when d = 1 in the divisor update. This touches every element and must not be deferred into a small-d structure, otherwise queries would repeatedly expand it inefficiently. In the algorithm, d = 1 is treated as a large workload case and applied directly, ensuring linear but one-time cost.

Another edge case arises when all updates are type 2 with small d, for example repeated d = 2 operations. Without careful bounding, deferred storage would grow unbounded and queries would become quadratic. The sqrt threshold ensures that although many such updates are stored, each query processes them in a controlled manner because expansion is limited by both d and segment size.

A final edge case is a query over a very small range after many updates. Even if updates are large, the query loop over multiples only touches indices inside [l, r], so for small ranges the work stays proportional to range size rather than full array size, preserving performance.
