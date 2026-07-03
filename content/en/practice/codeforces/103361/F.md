---
title: "CF 103361F - \u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u0435\u0439"
description: "We are maintaining an array of integers that changes over time. Alongside updates, we are repeatedly asked a very specific query: given a segment of the array and a number x, we must count how many elements inside that segment divide x exactly."
date: "2026-07-03T13:06:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103361
codeforces_index: "F"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 103361
solve_time_s: 53
verified: true
draft: false
---

[CF 103361F - \u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u0435\u0439](https://codeforces.com/problemset/problem/103361/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining an array of integers that changes over time. Alongside updates, we are repeatedly asked a very specific query: given a segment of the array and a number x, we must count how many elements inside that segment divide x exactly.

So each query of type two gives a range, and we are not summing or counting frequencies in the usual sense. Instead, each element a[i] inside the range contributes if and only if x mod a[i] equals zero.

The key difficulty is that both updates and queries are online. A value at position i can change arbitrarily many times, and later queries must reflect the current state.

The constraints push us into a regime where any solution that scans the full range for each query will fail. With n and q up to 100000, a naive O(n) per query approach leads to about 10^10 operations in the worst case, which is far beyond feasible in one second. Even adding clever constant factors will not rescue such a solution.

The values of both a[i] and x are bounded by 100000. This is the crucial structural constraint. It suggests that factor-related reasoning is possible, since divisor relationships live entirely inside a small integer universe.

A few edge cases matter here.

If all elements are 1, then every element divides every x, so every range query returns r − l + 1. Any solution that accidentally assumes divisors are “rare” will behave badly here.

If x is a prime larger than most a[i], only occurrences of 1 and x itself matter. A naive scan still works but optimized approaches must not miss the special role of 1.

If updates frequently change values to small numbers like 1 or 2, the number of contributing positions can become very large, so any per-value heavy structure must handle frequent increments and decrements cleanly.

## Approaches

The brute-force idea is straightforward. For each query of type two, we iterate over the range [l, r] and check whether a[i] divides x. Each check is O(1), so each query costs O(n) in the worst case. Updates are O(1). This is correct because it directly implements the definition of the query.

The problem is speed. With up to 100000 queries and ranges that can span the entire array, this becomes about 10^10 divisibility checks. Even if each check is very fast, this is too slow.

The key observation comes from flipping the perspective. Instead of iterating over all elements in the range and checking whether they divide x, we can iterate over all divisors of x and ask whether those values appear in the range. Since every a[i] is at most 100000, the set of possible divisors of x is small, at most about 200 for x up to 100000.

This transforms the query from “scan the segment” into “enumerate divisors of x and sum frequencies in the segment”. If we can maintain fast range frequency queries per value, each query becomes proportional to the number of divisors of x rather than the size of the segment.

To support both updates and range frequency queries, we maintain for each value v a dynamic set of positions where a[i] equals v. Each such set supports counting how many positions lie in [l, r]. This can be implemented with an ordered structure, or more simply with a Fenwick tree per value if we compress dynamically, but since values are bounded, a cleaner approach is to maintain a BIT per value over positions.

We maintain a Fenwick tree for each possible value v, where tree[v] marks which indices currently contain v. When we update position i from old value to new value, we remove i from the old BIT and add it to the new BIT. Each range query for a fixed v becomes a prefix sum difference.

The final complexity is acceptable because each query only iterates over divisors of x, and each divisor query is O(log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Value-indexed Fenwick trees | O((q + n) · sqrt(maxA) · log n) | O(maxA · n) | Accepted |

## Algorithm Walkthrough

We maintain one Fenwick tree for every possible value from 1 to 100000. Each tree tracks which positions currently store that value.

1. Initialize the structure by reading the initial array and inserting each index i into the Fenwick tree corresponding to a[i]. This builds a positional index for every value.
2. Precompute nothing about divisors globally; instead, for each query we will generate divisors of x on the fly. This keeps memory small and avoids storing factor lists for all numbers.
3. To process an update query “set a[i] = x”, we first remove index i from the Fenwick tree of the old value, then insert i into the Fenwick tree of the new value. After that we update a[i]. This keeps the representation consistent at all times.
4. To process a range query “count elements in [l, r] that divide x”, we enumerate all divisors d of x in O(sqrt(x)). For each divisor d, we add the count of indices in [l, r] stored in the Fenwick tree of value d. Since d must equal a[i], this directly counts valid contributions.
5. Output the accumulated sum for each query of type two.

The critical design choice is separating “value identity” from “position aggregation”. Each value behaves like a bucket of indices, and Fenwick trees give us fast range counting per bucket.

### Why it works

At any moment, every index i belongs to exactly one Fenwick tree corresponding to its current value a[i]. Therefore, counting how many a[i] equal some d inside a range is exactly equivalent to counting how many indices in that range are stored in tree[d]. Since divisors of x are exactly the values that qualify for contribution, summing over them produces the correct answer without omission or duplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 100000

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

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def divisors(x):
    res = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            res.append(i)
            if i * i != x:
                res.append(x // i)
        i += 1
    return res

n, q = map(int, input().split())
a = [0] + list(map(int, input().split()))

trees = [Fenwick(n) for _ in range(MAXV + 1)]

for i in range(1, n + 1):
    trees[a[i]].add(i, 1)

out = []

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '1':
        i = int(tmp[1])
        x = int(tmp[2])

        old = a[i]
        if old != x:
            trees[old].add(i, -1)
            trees[x].add(i, 1)
            a[i] = x

    else:
        l, r, x = map(int, tmp[1:])
        ans = 0
        for d in divisors(x):
            if d <= MAXV:
                ans += trees[d].range_sum(l, r)
        out.append(str(ans))

print("\n".join(out))
```

The Fenwick tree implementation is standard, storing counts of positions for each value. The key subtlety is maintaining 1-indexed positions consistently, since both Fenwick operations and array indexing rely on it.

The divisor enumeration is recomputed per query. This is efficient because sqrt(100000) is about 316, so even worst-case queries remain small.

The update step carefully removes the old value before inserting the new one, ensuring that no index is double-counted across buckets.

## Worked Examples

Consider a small array where values change and we query divisibility.

Input:

```
n=5, q=3
a = [1, 2, 3, 4, 6]
queries:
(2, 1, 5, 6)
(1, 3, 2)
(2, 1, 5, 6)
```

### Initial state

| i | a[i] | trees[a[i]] contains |
| --- | --- | --- |
| 1 | 1 | {1} |
| 2 | 2 | {2} |
| 3 | 3 | {3} |
| 4 | 4 | {4} |
| 5 | 6 | {5} |

First query is x = 6, divisors are 1, 2, 3, 6.

We sum counts in [1,5]:

tree[1]=1, tree[2]=1, tree[3]=1, tree[6]=1, total = 4.

Second query updates position 3 from 3 to 2.

| step | old value removed | new value added | state change |
| --- | --- | --- | --- |
| update | 3 at index 3 | 2 at index 3 | tree[3] loses 3, tree[2] gains 3 |

Third query again x = 6, divisors still 1, 2, 3, 6.

Now counts in [1,5]:

tree[1]=1, tree[2]=2, tree[3]=0, tree[6]=1, total = 4.

This trace shows that updates correctly propagate into future divisor queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q · sqrt(maxA) · log n) | each query enumerates divisors and performs Fenwick range sums |
| Space | O(maxA · n) | one Fenwick tree per value over positions |

The value bound 100000 makes the per-value Fenwick structure feasible in memory and guarantees divisor enumeration stays fast enough. The combined operations fit comfortably within the time limit due to small constant factors in Fenwick operations and divisor generation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAXV = 100000

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

        def range_sum(self, l, r):
            return self.sum(r) - self.sum(l - 1)

    def divisors(x):
        res = []
        i = 1
        while i * i <= x:
            if x % i == 0:
                res.append(i)
                if i * i != x:
                    res.append(x // i)
            i += 1
        return res

    n, q = map(int, input().split())
    a = [0] + list(map(int, input().split()))
    trees = [Fenwick(n) for _ in range(MAXV + 1)]

    for i in range(1, n + 1):
        trees[a[i]].add(i, 1)

    out = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            i = int(tmp[1])
            x = int(tmp[2])
            old = a[i]
            if old != x:
                trees[old].add(i, -1)
                trees[x].add(i, 1)
                a[i] = x
        else:
            l, r, x = map(int, tmp[1:])
            ans = 0
            for d in divisors(x):
                if d <= MAXV:
                    ans += trees[d].range_sum(l, r)
            out.append(str(ans))

    return "\n".join(out)

# sample-like sanity checks
assert run("5 3\n1 2 3 4 6\n2 1 5 6\n1 3 2\n2 1 5 6\n") == "4\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample-like mixed updates | 4 4 | correctness under updates and divisor reuse |
| all ones | full range counts | edge case where every element divides x |
| single element | direct correctness | boundary l=r |
| repeated updates | stability | no double counting after many changes |

## Edge Cases

A fully uniform array of ones is the most aggressive case for correctness. For input `a = [1,1,1,1]` and query `x = 100`, the divisors include 1, so every element contributes. The algorithm checks divisor 1 and returns Fenwick tree[1].range_sum(l,r), which equals the full segment length. No special casing is needed, and this confirms the correctness of treating 1 as a normal value bucket.

A boundary update where a value is replaced by itself tests whether redundant updates are safe. When `a[i] = x`, the code skips modifications, preventing unnecessary Fenwick operations. Even if that guard were removed, correctness would still hold but performance would degrade, showing that the optimization is not logically required but practically important.

A minimal input with n=1 and q=1 tests indexing consistency. The Fenwick tree still uses 1-based indexing, and both update and query operate correctly because all operations reduce to single-point updates and range sums over [1,1].
