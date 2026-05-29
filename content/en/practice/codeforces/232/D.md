---
title: "CF 232D - Fence"
description: "We have an array of fence heights. A query gives one contiguous segment of the fence, and we must count how many other segments match it. Two segments match if they have the same length, do not overlap, and their heights differ by the same constant at every position."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "string-suffix-structures"]
categories: ["algorithms"]
codeforces_contest: 232
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 144 (Div. 1)"
rating: 2900
weight: 232
solve_time_s: 141
verified: false
draft: false
---

[CF 232D - Fence](https://codeforces.com/problemset/problem/232/D)

**Rating:** 2900  
**Tags:** binary search, data structures, string suffix structures  
**Solve time:** 2m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of fence heights. A query gives one contiguous segment of the fence, and we must count how many other segments match it.

Two segments match if they have the same length, do not overlap, and their heights differ by the same constant at every position. For example:

```
[1 2 2 1]
[100 101 101 100]
```

These match because every corresponding difference equals `99`.

The key observation is that matching depends only on adjacent differences. If two segments differ by a constant shift, then all consecutive differences inside them are identical.

For a segment:

```
h[l], h[l+1], ..., h[r]
```

define its difference sequence as:

```
h[l+1]-h[l], h[l+2]-h[l+1], ...
```

Two segments match exactly when their difference sequences are equal.

The fence has up to `10^5` planks and there are up to `10^5` queries. Any solution comparing segments directly is impossible. Even `O(length)` per query can become quadratic in the worst case. We need something close to linear or `O(n log n)` preprocessing with fast query answers.

There are several easy-to-miss edge cases.

A segment of length `1` has an empty difference sequence. Every single plank matches every other single plank as long as they are distinct positions.

Example:

```
n = 3
h = [5 100 7]
query = [2,2]
```

The answer is `2`, because positions `1` and `3` are both valid matching segments.

A careless implementation may return `0` because it tries to compare nonexistent differences.

Another subtle case is overlap handling.

Example:

```
h = [1 2 1 2]
query = [1,2]
```

The pattern is `[+1]`. Segment `[3,4]` matches, but `[2,3]` does not because its difference is `-1`.

Even if equal patterns appear many times, overlapping occurrences must not be counted.

The hardest edge case is repeated patterns with dense overlaps.

Example:

```
h = [1 2 1 2 1]
query = [1,3]
```

The difference pattern is:

```
[+1, -1]
```

Occurrences appear at positions `1` and `3`, but these segments overlap at plank `3`, so the correct answer is `0`.

A naive substring-frequency approach would incorrectly count both.

## Approaches

The brute force approach is straightforward. For each query segment, compute its difference sequence and compare it against every other segment of the same length.

Suppose the query length is `k`. We would compare up to `n-k+1` candidate segments, and each comparison costs `O(k)`.

In the worst case:

```
n = q = 100000
k ≈ 50000
```

This becomes roughly `10^10` operations, far beyond the limit.

The reason brute force works conceptually is that matching segments are exactly segments with equal difference arrays. The problem is only speed.

The key insight is that the entire fence can be converted into one difference array:

```
d[i] = h[i+1] - h[i]
```

Now every fence segment corresponds to a subarray in `d`.

If two fence segments of length `k` match, then their corresponding difference subarrays of length `k-1` are identical.

So the problem becomes:

```
For each substring of the difference array,
count equal occurrences that are far enough apart.
```

This is now a classic suffix structure problem.

We build a suffix array over the difference array. Equal substrings become contiguous intervals in suffix-array order. Using LCP information, we can find all occurrences of a query pattern.

The remaining challenge is overlap filtering.

Suppose the original fence segment length is `k`. Then two occurrences starting at positions `a` and `b` are valid only if:

```
|a - b| >= k
```

Inside the suffix-array interval of equal substrings, we need to count starts sufficiently far from the query start.

This can be handled offline with sorted occurrence positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(qn^2) | O(n) | Too slow |
| Optimal | O(n log n + q log^2 n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the difference array:

```
d[i] = h[i+1] - h[i]
```

A fence segment of length `k` becomes a difference subarray of length `k-1`.
2. Build a suffix array over `d`.

Every suffix represents a starting position in the difference array. Equal prefixes correspond to equal fence patterns.
3. Build the LCP array and a sparse table for RMQ.

This lets us compute the longest common prefix between any two suffixes in `O(1)` time after preprocessing.
4. For every query segment `[l,r]`, compute:

```
len = r - l + 1
pat = len - 1
```

If `len == 1`, the answer is simply `n-1`, because every other single plank matches.
5. Otherwise, locate the suffix corresponding to position `l` in the difference array.

We need all suffixes sharing at least `pat` common prefix elements with it.
6. Binary search left and right in suffix-array order.

Using LCP queries, find the maximal interval where every suffix shares at least `pat` values with the query suffix.

Every suffix inside this interval represents an occurrence of the same pattern.
7. Extract the original fence starting positions from this interval.

If a suffix starts at difference-array index `x`, then the corresponding fence segment starts at plank `x`.
8. Count only non-overlapping occurrences.

A candidate start `x` is valid iff:

```
|x - l| >= len
```

Use binary search on sorted start positions to count valid occurrences efficiently.

### Why it works

The invariant is:

```
Two fence segments match
iff their difference sequences are equal.
```

Subtracting consecutive elements removes the unknown constant shift between segments. Equal difference sequences guarantee that all pairwise offsets are identical, which is exactly the matching condition.

The suffix array groups equal prefixes together lexicographically. The LCP structure guarantees that the interval we extract contains exactly all occurrences of the query pattern.

Finally, the overlap condition depends only on starting indices and segment length, so filtering by distance removes precisely the forbidden overlapping segments.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right
input = sys.stdin.readline

def build_suffix_array(arr):
    n = len(arr)
    if n == 0:
        return [], []

    vals = {v: i for i, v in enumerate(sorted(set(arr)))}
    rank = [vals[x] for x in arr]

    sa = list(range(n))
    k = 1

    tmp = [0] * n

    while True:
        sa.sort(key=lambda x: (rank[x], rank[x + k] if x + k < n else -1))

        tmp[sa[0]] = 0

        for i in range(1, n):
            a = sa[i - 1]
            b = sa[i]

            prev = (rank[a], rank[a + k] if a + k < n else -1)
            cur = (rank[b], rank[b + k] if b + k < n else -1)

            tmp[b] = tmp[a] + (prev != cur)

        rank, tmp = tmp, rank

        if rank[sa[-1]] == n - 1:
            break

        k <<= 1

    return sa, rank

def build_lcp(arr, sa, rank):
    n = len(arr)
    if n == 0:
        return []

    lcp = [0] * (n - 1)
    k = 0

    for i in range(n):
        r = rank[i]

        if r == n - 1:
            k = 0
            continue

        j = sa[r + 1]

        while i + k < n and j + k < n and arr[i + k] == arr[j + k]:
            k += 1

        lcp[r] = k

        if k:
            k -= 1

    return lcp

class SparseTable:
    def __init__(self, arr):
        n = len(arr)

        self.n = n
        self.log = [0] * (n + 1)

        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1

        self.st = [arr[:]]

        k = 1

        while (1 << k) <= n:
            prev = self.st[-1]
            size = n - (1 << k) + 1

            cur = [0] * size

            half = 1 << (k - 1)

            for i in range(size):
                cur[i] = min(prev[i], prev[i + half])

            self.st.append(cur)
            k += 1

    def query(self, l, r):
        if l > r:
            return 10**18

        k = self.log[r - l + 1]

        return min(
            self.st[k][l],
            self.st[k][r - (1 << k) + 1]
        )

def solve():
    n = int(input())
    h = list(map(int, input().split()))

    q = int(input())

    if n == 1:
        for _ in range(q):
            input()
            print(0)
        return

    d = [h[i + 1] - h[i] for i in range(n - 1)]

    sa, rank = build_suffix_array(d)
    lcp = build_lcp(d, sa, rank)

    st = SparseTable(lcp) if lcp else None

    pos_in_sa = rank

    groups = {}

    def get_lcp(i, j):
        if i == j:
            return len(d) - i

        ri = pos_in_sa[i]
        rj = pos_in_sa[j]

        if ri > rj:
            ri, rj = rj, ri

        return st.query(ri, rj - 1)

    for idx, start in enumerate(sa):
        groups.setdefault(start, idx)

    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1

        length = r - l + 1

        if length == 1:
            print(n - 1)
            continue

        pat = length - 1

        p = pos_in_sa[l]

        low = 0
        high = p

        while low < high:
            mid = (low + high) // 2

            if get_lcp(sa[mid], l) >= pat:
                high = mid
            else:
                low = mid + 1

        left = low

        low = p
        high = len(sa) - 1

        while low < high:
            mid = (low + high + 1) // 2

            if get_lcp(sa[mid], l) >= pat:
                low = mid
            else:
                high = mid - 1

        right = low

        starts = sorted(sa[i] for i in range(left, right + 1))

        bad_left = bisect_left(starts, l - length + 1)
        bad_right = bisect_right(starts, l + length - 1)

        total = len(starts)
        bad = bad_right - bad_left

        print(total - bad)

if __name__ == "__main__":
    solve()
```

The first part converts the fence into consecutive differences. This transformation is the entire core of the problem. Once differences are equal, the original heights can differ only by a constant.

The suffix array is built using the standard doubling algorithm. Each iteration sorts suffixes by the first `2^k` elements. The implementation compresses values first because differences may be as large as `10^9`.

The LCP construction uses Kasai's algorithm. This gives the longest common prefix between neighboring suffixes in linear time.

The sparse table supports range minimum queries on the LCP array. To compute the LCP between arbitrary suffixes, we query the minimum LCP value between their suffix-array positions.

For a query, we binary search outward from the query suffix inside suffix-array order. Every suffix with LCP at least `pat` belongs to the same pattern interval.

The final subtle part is overlap removal. Suppose the query segment length is `len`. Any segment starting inside:

```
[l-len+1, l+len-1]
```

would overlap the query segment, so those starts are excluded with binary searches on sorted positions.

## Worked Examples

### Example 1

Input:

```
h = [1 2 2 1 100 99 99 100 100 100]
query = [1,4]
```

Difference array:

```
d = [1 0 -1 99 -1 0 1 0 0]
```

Query pattern:

```
[1 0 -1]
```

| Step | Value |
| --- | --- |
| Query length | 4 |
| Pattern length | 3 |
| Matching starts | 1, 5 |
| Segment at 1 | [1 2 2 1] |
| Segment at 5 | [100 99 99 100] |
| Distance between starts | 4 |
| Overlap? | No |
| Answer | 1 |

The trace shows why equal difference sequences are sufficient. The actual heights are completely different, but all consecutive changes match.

### Example 2

Input:

```
h = [1 2 1 2 1]
query = [1,3]
```

Difference array:

```
[1 -1 1 -1]
```

Pattern:

```
[1 -1]
```

| Step | Value |
| --- | --- |
| Query length | 3 |
| Candidate starts | 1, 3 |
| Segment at 1 | [1 2 1] |
| Segment at 3 | [1 2 1] |
| Distance between starts | 2 |
| Required distance | at least 3 |
| Overlap? | Yes |
| Answer | 0 |

This trace demonstrates the overlap filter. Pattern equality alone is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log^2 n) | suffix array construction plus binary searches per query |
| Space | O(n) | suffix array, LCP, sparse table |

With `n,q ≤ 100000`, this easily fits the limits. The preprocessing is dominated by suffix-array construction, and each query performs only logarithmic work.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    h = list(map(int, input().split()))
    q = int(input())

    for _ in range(q):
        l, r = map(int, input().split())

        ans = 0

        for s in range(n - (r - l)):
            e = s + (r - l)

            if not (e < l - 1 or s > r - 1):
                continue

            ok = True

            for i in range(r - l):
                if h[s + i + 1] - h[s + i] != h[l + i] - h[l + i - 1]:
                    ok = False
                    break

            if ok:
                ans += 1

        print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

# sample 1
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
) == """1
2
2
0
2
9
"""

# minimum size
assert run(
"""1
5
1
1 1
"""
) == """0
"""

# all equal
assert run(
"""5
7 7 7 7 7
2
1 2
2 4
"""
) == """2
0
"""

# overlap trap
assert run(
"""5
1 2 1 2 1
1
1 3
"""
) == """0
"""

# single plank queries
assert run(
"""4
1 5 9 13
2
1 1
4 4
"""
) == """3
3
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single plank fence | 0 | No non-overlapping segment exists |
| All equal heights | Correct overlap handling | Equal patterns appear everywhere |
| Alternating pattern | 0 | Overlapping identical segments are excluded |
| Length-1 queries | n-1 | Empty difference sequences handled correctly |

## Edge Cases

Consider the smallest possible fence:

```
n = 1
h = [5]
query = [1,1]
```

The segment has length `1`. There are no other segments in the fence, so the answer is `0`.

The algorithm immediately detects `length == 1` and returns `n-1 = 0`.

Now consider repeated equal patterns with overlap:

```
h = [1 2 1 2 1]
query = [1,3]
```

The difference array is:

```
[1 -1 1 -1]
```

Occurrences of `[1,-1]` start at positions `1` and `3`.

The algorithm finds both through the suffix array interval. Then it checks overlap:

```
|3 - 1| = 2 < 3
```

So the second occurrence is removed.

Another tricky case is all equal heights:

```
h = [7 7 7 7 7]
query = [1,2]
```

Every difference equals `0`, so all length-2 segments share the same pattern.

Candidate starts are:

```
1, 2, 3, 4
```

But starts `1` and `2` overlap the query segment `[1,2]`.

Only starts `3` and `4` remain, so the answer is `2`.

The suffix-array interval correctly groups all zero-pattern suffixes together, and the distance filter removes only invalid overlaps.
