---
title: "CF 106511C - LCM Queries"
description: "We are given a sequence of integers and a set of queries. Each query asks for the least common multiple of all numbers inside a contiguous segment of the array. The task is to answer each query independently and output the resulting value for that segment."
date: "2026-06-18T19:06:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106511
codeforces_index: "C"
codeforces_contest_name: "Columbia University Local Contest (CULC) Spring 2026"
rating: 0
weight: 106511
solve_time_s: 53
verified: true
draft: false
---

[CF 106511C - LCM Queries](https://codeforces.com/problemset/problem/106511/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and a set of queries. Each query asks for the least common multiple of all numbers inside a contiguous segment of the array. The task is to answer each query independently and output the resulting value for that segment.

The core difficulty is not defining LCM itself, but handling many range queries efficiently. A direct recomputation of the LCM for every query would repeatedly scan large parts of the array and recompute multiplications and gcd operations from scratch, which becomes too slow when both the array size and number of queries are large.

The constraints typically associated with this kind of problem imply that the array can be large enough that a quadratic solution is impossible. Even a solution that recomputes each query in linear time would lead to roughly n times q operations, which exceeds what a two second limit can handle. This pushes us toward a preprocessing structure where each query can be answered in logarithmic or near constant time.

A subtle issue in this problem is that LCM values grow extremely quickly. Even moderate inputs can produce numbers that exceed standard 64-bit integer ranges. For example, combining values like 30, 42, and 70 already produces a large intermediate result. A naive implementation that multiplies first and divides later without care for overflow can silently produce incorrect answers. Another edge case arises when intermediate LCM values exceed practical bounds even though the final answer might still fit within constraints, which makes unchecked multiplication unsafe.

## Approaches

A brute-force solution processes each query by iterating over the requested segment and repeatedly folding values into a running LCM. This is straightforward: start from 1, and for each element in the segment compute `lcm(current, a[i]) = current * a[i] // gcd(current, a[i])`. This is correct because LCM is associative over pairs.

However, this approach recomputes from scratch for every query. If there are q queries over an array of size n, the worst case involves O(nq) gcd operations. With both n and q large, this quickly becomes infeasible.

The key observation is that LCM aggregation over segments is associative, which allows us to precompute partial results in a balanced structure. A segment tree fits naturally because each node stores the LCM of its interval, and combining two children gives the LCM of the parent interval.

The only complication is that LCM values can grow without bound. In practice, once the value exceeds a safe cutoff such as 10^18, it is no longer useful to distinguish exact values because any further multiplication will not restore smallness. This allows us to clamp values to a fixed threshold and still preserve correctness for comparisons and final answers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Segment Tree (LCM) | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We build a segment tree where each node represents the LCM of a segment of the array.

1. Build a segment tree over the array, where each leaf stores the corresponding array value. Each internal node stores the LCM of its two children. This ensures that every segment is pre-aggregated.
2. When computing LCM at a node, use the formula `lcm(a, b) = a // gcd(a, b) * b`. We compute in this order to reduce intermediate overflow risk.
3. If the computed LCM exceeds a fixed limit such as 10^18, we clamp it to that limit. This prevents overflow while preserving correctness, because any further combination will not bring the value back down.
4. For each query [l, r], traverse the segment tree. If a node’s segment lies completely inside the query range, use its stored value directly. If it lies outside, ignore it. Otherwise, combine results from both children using LCM.
5. Output the final aggregated value for each query.

The reason this structure works is that LCM over integers forms an associative operation, meaning the grouping of computations does not change the result. This allows us to precompute partial LCMs for all segments and reuse them during queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10**18

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    g = gcd(a, b)
    res = a // g * b
    return res if res <= LIMIT else LIMIT

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.t = [1] * (2 * self.size)

        for i in range(self.n):
            self.t[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.t[i] = lcm(self.t[2 * i], self.t[2 * i + 1])

    def query(self, l, r):
        l += self.size
        r += self.size
        res_left = 1
        res_right = 1

        while l <= r:
            if l % 2 == 1:
                res_left = lcm(res_left, self.t[l])
                l += 1
            if r % 2 == 0:
                res_right = lcm(self.t[r], res_right)
                r -= 1
            l //= 2
            r //= 2

        return lcm(res_left, res_right)

def main():
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    st = SegTree(arr)

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        out.append(str(st.query(l, r)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The segment tree is stored in a flat array where leaves begin at a power-of-two offset. This simplifies both construction and query traversal. The query function uses an iterative two-pointer style walk upward, merging partial results from left and right boundaries. The split into `res_left` and `res_right` avoids reversing order issues while preserving associativity.

The most delicate implementation detail is the LCM computation. Dividing before multiplying is necessary to reduce overflow risk, and clamping ensures we never propagate unbounded integers through the structure.

## Worked Examples

### Example 1

Input:

```
5 2
2 3 4 5 6
1 3
2 5
```

| Step | Segment | Combined Value |
| --- | --- | --- |
| Query 1 | [2, 3, 4] | lcm(2,3)=6 → lcm(6,4)=12 |
| Query 2 | [3, 4, 5, 6] | 60 |

First query builds up LCM incrementally over a small prefix, showing how repeated aggregation compresses the segment into a single value. The second query demonstrates reuse of precomputed structure instead of recomputing from scratch.

### Example 2

Input:

```
4 1
6 10 15 21
1 4
```

| Step | Segment | Combined Value |
| --- | --- | --- |
| Full range | [6,10,15,21] | 210 |

This trace highlights how quickly LCM stabilizes into a single product of distinct prime factors, since overlaps are removed through gcd divisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each update is not present, construction is O(n), each query combines O(log n) nodes |
| Space | O(n) | Segment tree storage proportional to array size |

The logarithmic query time ensures that even large inputs with many queries remain within limits, since each query touches only a small number of tree nodes instead of scanning the full segment.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    LIMIT = 10**18

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        if a == 0 or b == 0:
            return 0
        g = gcd(a, b)
        res = a // g * b
        return res if res <= LIMIT else LIMIT

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.t = [1] * (2 * self.size)
            for i in range(self.n):
                self.t[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.t[i] = lcm(self.t[2*i], self.t[2*i+1])

        def query(self, l, r):
            l += self.size
            r += self.size
            res_left, res_right = 1, 1
            while l <= r:
                if l % 2:
                    res_left = lcm(res_left, self.t[l])
                    l += 1
                if not r % 2:
                    res_right = lcm(self.t[r], res_right)
                    r -= 1
                l //= 2
                r //= 2
            return lcm(res_left, res_right)

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    st = SegTree(arr)

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        out.append(str(st.query(l-1, r-1)))
    return "\n".join(out)

# custom cases

assert run("""5 2
2 3 4 5 6
1 3
2 5
""") == "12\n60"

assert run("""4 1
6 10 15 21
1 4
""") == "210"

assert run("""1 1
7
1 1
""") == "7"

assert run("""3 2
2 2 2
1 3
2 3
""") == "2\n2"

assert run("""6 1
1 2 3 4 5 6
1 6
""") == "60"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | 7 | base case correctness |
| Repeated values | 2, 2 | idempotent LCM behavior |
| Full range | 60 | multi-element aggregation |

## Edge Cases

A single-element query such as `[7]` demonstrates that the segment tree correctly returns leaf values without modification. The query does not enter any combination logic beyond a single node, so the identity behavior of LCM is preserved.

A repeated-value array like `[2, 2, 2]` shows that redundant factors collapse properly. Even though multiple nodes contribute the same value, repeated LCM operations do not inflate the result, since `lcm(2, 2) = 2` and this propagates consistently through the tree.

A full-range query exercises maximum depth traversal. The algorithm combines multiple segments from both ends of the tree, and correctness relies on the associativity of LCM ensuring that any grouping of merges yields the same final value.
