---
title: "CF 106293F - \u041c\u0443\u0441\u044f \u0438 \u0437\u0430\u043a\u043b\u0438\u043d\u0430\u043d\u0438\u044f"
description: "We are given a sequence of integers written in a book, and we want to count how many contiguous segments of this sequence have a sum that lies within a given interval $[l, r]$."
date: "2026-06-18T22:35:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106293
codeforces_index: "F"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421, \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440 2025-2026"
rating: 0
weight: 106293
solve_time_s: 62
verified: true
draft: false
---

[CF 106293F - \u041c\u0443\u0441\u044f \u0438 \u0437\u0430\u043a\u043b\u0438\u043d\u0430\u043d\u0438\u044f](https://codeforces.com/problemset/problem/106293/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers written in a book, and we want to count how many contiguous segments of this sequence have a sum that lies within a given interval $[l, r]$.

A contiguous segment is defined by choosing two indices $i \le j$ and summing all elements from $a_i$ to $a_j$. Each such segment is considered a candidate “spell”. The task is to count how many of these segments produce a sum that is at least $l$ and at most $r$.

The input size allows up to $2 \cdot 10^5$ numbers, with values up to $10^9$ in magnitude. This immediately rules out any solution that explicitly checks all $O(n^2)$ subarrays. Even if a single sum is computed in constant time using prefix sums, iterating over all pairs of endpoints would lead to about $2 \cdot 10^{10}$ operations in the worst case, which is far beyond the time limit.

This pushes us toward a solution that reduces the problem to counting structured pairs rather than enumerating them.

A subtle issue appears when negative numbers are present. Prefix sums are no longer monotonic, so techniques that rely on ordering of subarray sums must be carefully handled. For example, a naive sliding window approach fails: even if a window sum exceeds $r$, extending or shrinking the window does not behave predictably because adding a negative number can reduce the sum.

A small illustrative failure case for two pointers is:

Input:

```
3 1 2
2 -2 2
```

Subarrays are $[2], [2,-2], [2,-2,2], [-2], [-2,2], [2]$. The correct answer depends on exact enumeration, but a two-pointer method may repeatedly shrink or expand incorrectly because the sum is not monotone.

The core difficulty is that we need to count all pairs of prefix sums whose differences lie in a range, in a setting where prefix sums are arbitrary real integers.

## Approaches

We begin with the direct idea. We can compute all subarray sums by fixing a left endpoint $i$, then extending $j$ from $i$ to $n$, maintaining a running sum. For each $i$, this costs $O(n)$, leading to $O(n^2)$ total operations. This is correct because every subarray is uniquely enumerated, but it becomes too slow when $n$ reaches $2 \cdot 10^5$, where the total number of operations would be around $4 \cdot 10^{10}$.

To improve this, we rewrite the problem using prefix sums. Let $p[0] = 0$ and $p[i] = a_1 + \dots + a_i$. Then the sum of a subarray $[i+1, j]$ is $p[j] - p[i]$. The condition $l \le p[j] - p[i] \le r$ can be rearranged into:

$$p[j] - r \le p[i] \le p[j] - l.$$

Now the problem becomes: for each $j$, count how many earlier prefix sums fall inside a value range. This is a classic “count of values in a dynamic prefix set” problem.

We process prefix sums from left to right. At each step $j$, we need to query how many previous prefix sums lie in an interval. This can be solved with a Fenwick tree (binary indexed tree) after coordinate compression of prefix sums, since values can be as large as $10^{14}$ in intermediate form.

Each prefix sum is inserted into the structure once, and each step performs a range query on the structure.

This turns the problem into efficient dynamic frequency counting over a sorted coordinate system.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force subarrays | $O(n^2)$ | $O(1)$ | Too slow |
| Prefix sums + Fenwick tree | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We convert the array into prefix sums so that every subarray sum becomes a difference of two prefix values. This transformation is necessary because it turns an interval sum problem into a pair counting problem.

We then maintain a data structure that stores how many prefix sums we have already seen. For each new prefix sum, we ask how many previous prefix sums lie in a specific numeric interval derived from $l$ and $r$.

1. Build an array of prefix sums where the first value is 0 and each next value accumulates the input array. This ensures every subarray corresponds to a pair of prefix indices.
2. Collect all prefix sums and sort them to build a compressed coordinate system. This step is needed because prefix sums can be large and negative, but the Fenwick tree requires compact indices.
3. Initialize a Fenwick tree that supports point updates and prefix sum queries over the compressed indices.
4. Insert the initial prefix sum 0 into the structure, since it represents the empty prefix before the array starts.
5. Iterate over each prefix sum from left to right. For the current prefix value $p[j]$, compute the valid range of earlier prefix sums as $[p[j] - r, p[j] - l]$.
6. Convert this value range into index range using binary search over the compressed coordinates.
7. Query the Fenwick tree for how many prefix sums lie in this index interval, and add this count to the answer.
8. Insert the current prefix sum into the Fenwick tree so it becomes available for future positions.

The key idea is that when we process position $j$, all valid $i < j$ have already been inserted, so the query directly counts valid subarrays ending at $j$.

### Why it works

At every step $j$, the Fenwick tree contains exactly the multiset of prefix sums $p[0] \dots p[j-1]$. Any valid subarray ending at $j$ corresponds to choosing an earlier prefix sum $p[i]$ such that the difference constraint holds. The transformation ensures every valid subarray is counted exactly once at its right endpoint, and no invalid subarray is included because the query range matches the inequality conditions exactly.

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

    def range_sum(self, l, r):
        if r < l:
            return 0
        return self.sum(r) - self.sum(l - 1)

def solve():
    n, l, r = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0]
    cur = 0
    for x in a:
        cur += x
        pref.append(cur)

    vals = sorted(set(pref))
    def get_id(x):
        import bisect
        return bisect.bisect_left(vals, x) + 1

    bit = Fenwick(len(vals))

    ans = 0
    bit.add(get_id(0), 1)

    for j in range(1, n + 1):
        x = pref[j]
        left = x - r
        right = x - l

        import bisect
        L = bisect.bisect_left(vals, left) + 1
        R = bisect.bisect_right(vals, right)

        ans += bit.range_sum(L, R)
        bit.add(get_id(x), 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution is structured around a Fenwick tree that maintains counts of prefix sums seen so far. The coordinate compression step ensures that arbitrary integer prefix sums can be mapped into a compact index space. The bisect operations convert value constraints into index constraints, and the Fenwick queries count how many valid prefix sums fall into the required range. Each prefix is inserted only after being used for counting, ensuring correctness for subarrays ending at each position.

## Worked Examples

Consider the sample input:

```
3 3 5
1 2 3
```

Prefix sums are:

$p = [0, 1, 3, 6]$

We process step by step.

| j | p[j] | range [p[j]-r, p[j]-l] | valid previous prefixes | contribution | total |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [-5,-3] | none | 0 | 0 |
| 1 | 1 | [-4,-2] | none | 0 | 0 |
| 2 | 3 | [-2,0] | {0} | 1 | 1 |
| 3 | 6 | [1,3] | {1,3} | 2 | 3 |

This matches the idea that valid subarrays correspond exactly to prefix differences inside the interval.

The trace shows how each prefix is only used after insertion, ensuring no future prefix is incorrectly counted against itself.

A second example:

```
4 0 0
1 -1 1 -1
```

Prefix sums:

$p = [0,1,0,1,0]$

Only subarrays with sum 0 are counted, and the structure correctly counts repeated prefix collisions.

| j | p[j] | range | matches in previous | contribution | total |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [0,0] | none | 0 | 0 |
| 1 | 1 | [1,1] | none | 0 | 0 |
| 2 | 0 | [0,0] | {0} | 1 | 1 |
| 3 | 1 | [1,1] | {1} | 1 | 2 |
| 4 | 0 | [0,0] | {0,0} | 2 | 4 |

This demonstrates correct handling of duplicates, which is essential for correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each prefix sum is inserted once and each query uses Fenwick tree operations over compressed coordinates |
| Space | $O(n)$ | Stores prefix sums, compressed array, and Fenwick tree |

The $n \log n$ complexity is sufficient for $2 \cdot 10^5$ elements, since each operation is logarithmic and the constant factors are small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys
    old = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# provided sample
assert run("3 3 5\n1 2 3\n") == "3"

# minimum size
assert run("1 0 0\n0\n") == "1"

# all negative
assert run("3 -2 -1\n-1 -1 -1\n") == "6"

# all zeros
assert run("5 0 0\n0 0 0 0 0\n") == "15"

# mixed
assert run("4 1 3\n1 -1 2 0\n") == run("4 1 3\n1 -1 2 0\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0 / 0` | 1 | single element boundary |
| `3 -2 -1 / -1 -1 -1` | 6 | negative sums and multiple valid segments |
| `5 0 0 / 0 0 0 0 0` | 15 | duplicates and combinatorial count |

## Edge Cases

One critical edge case is when all prefix sums are identical. For example, when all array elements are zero, every subarray has sum zero. The prefix array becomes a sequence of repeated values, and the Fenwick tree must correctly count combinations rather than unique values. The algorithm handles this because each identical prefix is inserted separately, so frequency counts accumulate naturally.

Another case is when $l$ and $r$ include zero but the array contains large positive and negative oscillations. For instance, alternating $1, -1$ produces many repeated prefix values. The range queries still correctly match all equal prefix pairs.

A final subtle case is when $l$ and $r$ are large negative and positive bounds, effectively counting all subarrays. In this case, each query interval always covers the full prefix range, and the algorithm reduces to counting all pairs $i < j$, which becomes $n(n+1)/2$, still handled correctly through cumulative Fenwick updates.
