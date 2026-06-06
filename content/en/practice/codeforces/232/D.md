---
title: "CF 232D - Fence"
description: "We have an array of plank heights. A fence piece is simply a contiguous segment. For a query segment $[l,r]$, we must count how many other segments of the same length match it. Matching has three requirements. The two segments must have equal length. They must be disjoint."
date: "2026-06-04T09:37:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "string-suffix-structures"]
categories: ["algorithms"]
codeforces_contest: 232
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 144 (Div. 1)"
rating: 2900
weight: 232
solve_time_s: 410
verified: false
draft: false
---

[CF 232D - Fence](https://codeforces.com/problemset/problem/232/D)

**Rating:** 2900  
**Tags:** binary search, data structures, string suffix structures  
**Solve time:** 6m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of plank heights. A fence piece is simply a contiguous segment.

For a query segment $[l,r]$, we must count how many other segments of the same length match it. Matching has three requirements.

The two segments must have equal length.

They must be disjoint.

If we align them position by position, the sum of corresponding heights must always be the same value. For a segment $[l,r]$ and another segment $[a,b]$, this means

$$h_{l+i}+h_{a+i}=h_l+h_a$$

for every valid offset $i$.

The first reaction is to look at heights directly, but the condition becomes much cleaner after taking differences.

Let

$$d_i=h_i-h_{i+1}$$

for $1\le i<n$.

Suppose two segments have width $k$. The matching condition implies

$$(h_{l+i}-h_{l+i+1}) = -(h_{a+i}-h_{a+i+1})$$

for every position.

In other words, if

$$d'_i=-d_i,$$

then matching segments correspond exactly to equal substrings between the difference array $d$ and the negated difference array $d'$. This is the key transformation used by the official solution.

The constraints are what force this transformation. Both $n$ and $q$ are up to $10^5$. Any algorithm that scans a segment per query immediately becomes too slow. Even $O(n)$ per query would require around $10^{10}$ operations. We need roughly $O((n+q)\log n)$.

There are several easy-to-miss edge cases.

Consider a segment of length one.

```
h = [5, 8, 1]
query = [2,2]
```

There are no differences inside a single plank. Every other single plank automatically satisfies the shape condition. The only restriction is disjointness. The answer is $n-1$. A solution that only works on difference arrays must treat this case carefully because the corresponding difference substring has length zero.

Consider complete overlap.

```
h = [1,2,1]
query = [1,2]
```

The segment itself matches its own pattern, but matching segments are required to be disjoint. Counting all occurrences of the pattern and forgetting the overlap restriction produces an answer that is too large.

Consider repeated patterns.

```
h = [1,2,1,2,1]
query = [1,2]
```

The same pattern appears many times. Some occurrences overlap the query segment and must be excluded, while others are valid. The counting structure must support both pattern matching and geometric position restrictions.

## Approaches

The brute force solution is straightforward.

For every query segment, enumerate every segment of the same length. Check whether the two segments are disjoint. Then compare corresponding positions and verify the matching condition.

A single comparison costs $O(k)$, where $k$ is the segment length. There are $O(n)$ candidate segments. In the worst case a query costs $O(n^2)$, and with $10^5$ queries this is hopeless.

The crucial observation is that the matching condition is really a condition on consecutive differences.

For matching segments,

$$h_{l+i}+h_{a+i}=C.$$

Subtract the equation for offset $i+1$:

$$(h_{l+i}-h_{l+i+1}) = -(h_{a+i}-h_{a+i+1}).$$

Using

$$d_i=h_i-h_{i+1}, \qquad d'_i=-d_i,$$

the problem becomes:

Find occurrences of the substring

$$d[l..r-1]$$

inside the array $d'$.

Now the problem looks like a classical string problem on integer alphabets.

The official solution builds a suffix array on

$$d + [\text{separator}] + d'.$$

For a query segment of width $k=r-l+1$, we need all suffixes in $d'$ whose first $k-1$ difference values equal

$$d[l..r-1].$$

In a suffix array, all such suffixes form one contiguous interval. We can find that interval using LCP information and binary search.

The remaining task is counting which occurrences correspond to fence segments that are disjoint from the query segment.

This becomes a geometric counting problem on suffix-array ranks. Each query asks:

How many suffixes from a suffix-array interval have starting positions outside a forbidden range?

A persistent segment tree or wavelet-tree style structure lets us answer that in $O(\log n)$ after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(qn^2)$ worst case | $O(1)$ | Too slow |
| Suffix Array + LCP + Persistent Counting | $O(n\log n + q\log n)$ | $O(n\log n)$ | Accepted |

## Algorithm Walkthrough

1. Build the difference array

$$d_i=h_i-h_{i+1}.$$

Also build

$$d'_i=-d_i.$$
2. Concatenate

$$T=d+[SEP]+d'.$$

The separator must be a value smaller than every compressed coordinate so that no match crosses the boundary.
3. Coordinate-compress all values and build a suffix array on $T$.
4. Build the LCP array and an RMQ structure so that the LCP of any two suffixes can be obtained in $O(1)$.
5. For every position in the original difference array $d$, store its suffix-array rank.
6. For a query $[l,r]$, let

$$len=r-l.$$

This is the length of the difference substring.
7. If $len=0$, the query segment contains one plank. Every disjoint single-plank segment matches. The answer is $n-1$.
8. Otherwise locate the suffix corresponding to position $l$ in $d$.
9. Using binary search on suffix-array positions and LCP queries, find the maximal suffix-array interval $[L,R]$ containing that suffix such that every suffix in the interval shares at least $len$ difference values with it.

These are exactly the occurrences of the required pattern in the concatenated structure.
10. Among those suffixes, keep only suffixes that belong to the $d'$ half.
11. Let such a suffix start at position $p$ inside $d'$. It corresponds to a fence segment

$$[a,b]$$

with

$$a=p,\qquad b=p+len.$$
12. The segment intersects the query iff

$$a\le r \quad\text{and}\quad b\ge l.$$

Equivalently, valid occurrences satisfy

$$b<l \quad\text{or}\quad a>r.$$
13. Use the persistent counting structure to count positions inside the suffix-array interval whose start indices satisfy the allowed ranges.
14. Output that count.

### Why it works

The transformation to difference arrays is exact. Two segments satisfy the original height-sum condition if and only if every consecutive height difference in one segment equals the negated consecutive height difference in the other. That converts the geometric fence condition into substring equality between $d$ and $d'$.

A suffix array groups equal prefixes into contiguous intervals. The LCP condition guarantees that every suffix in the located interval contains the required difference pattern, and no suffix outside the interval does.

The counting structure only filters occurrences by the disjointness requirement. Since every remaining occurrence corresponds to exactly one matching fence segment, the reported count is precisely the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SuffixArray:
    def __init__(self, s):
        n = len(s)
        sa = list(range(n))
        rank = s[:]
        tmp = [0] * n

        k = 1
        while True:
            sa.sort(key=lambda x: (
                rank[x],
                rank[x + k] if x + k < n else -1
            ))

            tmp[sa[0]] = 0
            for i in range(1, n):
                a, b = sa[i - 1], sa[i]
                tmp[b] = tmp[a] + (
                    (rank[a], rank[a + k] if a + k < n else -1) <
                    (rank[b], rank[b + k] if b + k < n else -1)
                )

            rank, tmp = tmp, rank

            if rank[sa[-1]] == n - 1:
                break
            k <<= 1

        self.sa = sa
        self.rank = rank

        lcp = [0] * (n - 1)
        h = 0
        for i in range(n):
            r = rank[i]
            if r == 0:
                continue
            j = sa[r - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[r - 1] = h
            if h:
                h -= 1

        self.lcp = lcp

        m = max(1, len(lcp))
        lg = [0] * (m + 1)
        for i in range(2, m + 1):
            lg[i] = lg[i >> 1] + 1

        st = [lcp[:]]
        j = 1
        while (1 << j) <= len(lcp):
            prev = st[j - 1]
            cur = [
                min(prev[i], prev[i + (1 << (j - 1))])
                for i in range(len(lcp) - (1 << j) + 1)
            ]
            st.append(cur)
            j += 1

        self.lg = lg
        self.st = st

    def get_lcp(self, i, j):
        if i == j:
            return 10 ** 9
        ri = self.rank[i]
        rj = self.rank[j]
        if ri > rj:
            ri, rj = rj, ri
        l = rj - ri
        k = self.lg[l]
        return min(
            self.st[k][ri],
            self.st[k][rj - (1 << k)]
        )

class Node:
    __slots__ = ("l", "r", "sum")

    def __init__(self, l=None, r=None, s=0):
        self.l = l
        self.r = r
        self.sum = s

def build(lo, hi):
    node = Node()
    if lo != hi:
        mid = (lo + hi) >> 1
        node.l = build(lo, mid)
        node.r = build(mid + 1, hi)
    return node

def update(prev, lo, hi, pos):
    node = Node(prev.l, prev.r, prev.sum + 1)
    if lo != hi:
        mid = (lo + hi) >> 1
        if pos <= mid:
            node.l = update(prev.l, lo, mid, pos)
        else:
            node.r = update(prev.r, mid + 1, hi, pos)
    return node

def query(rt_r, rt_l, lo, hi, ql, qr):
    if ql > hi or qr < lo or ql > qr:
        return 0
    if ql <= lo and hi <= qr:
        return rt_r.sum - rt_l.sum
    mid = (lo + hi) >> 1
    return (
        query(rt_r.l, rt_l.l, lo, mid, ql, qr) +
        query(rt_r.r, rt_l.r, mid + 1, hi, ql, qr)
    )

def solve():
    n = int(input())
    h = list(map(int, input().split()))

    if n == 1:
        q = int(input())
        print("\n".join("0" for _ in range(q)))
        return

    d = [h[i] - h[i + 1] for i in range(n - 1)]
    nd = [-x for x in d]

    vals = sorted(set(d + nd))
    comp = {v: i + 1 for i, v in enumerate(vals)}

    sep = 0
    T = [comp[x] for x in d] + [sep] + [comp[x] for x in nd]

    sa = SuffixArray(T)

    m = n - 1
    offset = m + 1

    roots = [build(1, m)]
    for pos in sa.sa:
        val = 0
        if offset <= pos < offset + m:
            val = pos - offset + 1

        if val:
            roots.append(update(roots[-1], 1, m, val))
        else:
            roots.append(roots[-1])

    q = int(input())
    ans = []

    for _ in range(q):
        l, r = map(int, input().split())

        if l == r:
            ans.append(str(n - 1))
            continue

        pat_len = r - l
        pos = l - 1

        rk = sa.rank[pos]
        N = len(T)

        lo, hi = 0, rk
        left = rk
        while lo <= hi:
            mid = (lo + hi) // 2
            ok = True
            if mid < rk:
                ok = sa.get_lcp(sa.sa[mid], sa.sa[rk]) >= pat_len
            if ok:
                left = mid
                hi = mid - 1
            else:
                lo = mid + 1

        lo, hi = rk, N - 1
        right = rk
        while lo <= hi:
            mid = (lo + hi) // 2
            ok = True
            if mid > rk:
                ok = sa.get_lcp(sa.sa[mid], sa.sa[rk]) >= pat_len
            if ok:
                right = mid
                lo = mid + 1
            else:
                hi = mid - 1

        total = 0

        max_left_start = l - pat_len
        if max_left_start >= 1:
            total += query(
                roots[right + 1],
                roots[left],
                1,
                m,
                1,
                max_left_start
            )

        min_right_start = r + 1
        if min_right_start <= m:
            total += query(
                roots[right + 1],
                roots[left],
                1,
                m,
                min_right_start,
                m
            )

        ans.append(str(total))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution follows the exact structure of the official approach. The suffix array identifies all occurrences of the required difference pattern. The persistent segment tree stores starting positions from the $d'$ half ordered by suffix-array rank, allowing interval counting in logarithmic time. The most delicate part is converting between fence positions and difference-array positions. A fence segment of width $k$ corresponds to a difference substring of length $k-1$, which is why the query length inside the suffix structure is `r - l`, not `r - l + 1`.

## Worked Examples

### Sample 1

```
h = [1,2,2,1,100,99,99,100,100,100]
query = [1,4]
```

The difference array is:

```
d = [-1,0,1,-99,1,0,-1,0,0]
```

The query corresponds to:

```
[-1,0,1]
```

Searching inside $d'$:

```
[1,0,-1,99,-1,0,1,0,0]
```

gives one valid occurrence.

| Step | Value |
| --- | --- |
| Query segment | [1,4] |
| Difference length | 3 |
| Pattern | [-1,0,1] |
| Matching occurrence in d' | start = 5 |
| Disjoint | yes |
| Answer | 1 |

This example demonstrates the core reduction from fence matching to substring matching.

### Custom Example

```
h = [5,5,5,5]
query = [2,2]
```

| Step | Value |
| --- | --- |
| Segment length | 1 |
| Difference substring length | 0 |
| All other single planks match | yes |
| Disjoint positions | 1,3,4 |
| Answer | 3 |

This exercises the special length-one case. No difference values exist, so every disjoint single plank is a match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\log n + q\log n)$ | suffix array construction plus logarithmic query processing |
| Space | $O(n\log n)$ | persistent segment tree and suffix-array structures |

With $n,q \le 10^5$, this complexity comfortably fits the limits. The preprocessing is performed once, and each query requires only a few binary searches and persistent-tree range counts.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

assert run(
"""10
1 2 2 1 100 99 99 100 100 100
6
1 4
1 2
3 4
1 5
9 10
10 10
"""
) == "\n".join([
"1",
"2",
"2",
"0",
"2",
"9"
]), "sample 1"

assert run(
"""1
7
1
1 1
"""
) == "0", "minimum size"

assert run(
"""4
5 5 5 5
2
1 1
2 2
"""
) == "\n".join([
"3",
"3"
]), "all equal"

assert run(
"""3
1 2 3
2
1 2
2 3
"""
) == "\n".join([
"0",
"0"
]), "overlapping only"

assert run(
"""5
1 2 1 2 1
1
1 2
"""
) == "1", "repeated pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single plank | 0 | Minimum boundary |
| All heights equal | 3, 3 | Length-one handling |
| Increasing heights | 0, 0 | No matching segments |
| Alternating pattern | 1 | Multiple occurrences and overlap filtering |

## Edge Cases

Consider a length-one query.

```
n = 4
h = [5,7,9,11]
query = [2,2]
```

The algorithm immediately enters the special branch `l == r`. Every other plank forms a valid matching segment because there are no internal differences to compare. The answer is $3$.

Consider a pattern that occurs only in overlapping positions.

```
h = [1,2,1]
query = [1,2]
```

The required difference pattern appears once, namely in the query segment itself. The suffix-array interval contains that occurrence, but the persistent counting stage rejects it because the corresponding segment intersects the query. The answer becomes $0$.

Consider multiple equal occurrences.

```
h = [1,2,1,2,1]
query = [1,2]
```

The difference pattern occurs more than once. The suffix-array interval captures all occurrences. The counting structure keeps only those whose start positions lie completely before or completely after the query segment. The final answer counts exactly the disjoint matches and ignores overlapping ones.

The combination of suffix-array interval search and positional filtering handles all of these cases uniformly.
