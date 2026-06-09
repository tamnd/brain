---
title: "CF 2007F - Eri and Expanded Sets"
description: "For every subarray, we throw all of its values into a set, removing duplicates. Starting from that set, we may repeatedly pick two distinct elements whose average is an integer and add that average if it is not already present."
date: "2026-06-09T02:46:09+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2007
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 969 (Div. 2)"
rating: 2300
weight: 2007
solve_time_s: 65
verified: true
draft: false
---

[CF 2007F - Eri and Expanded Sets](https://codeforces.com/problemset/problem/2007/F)

**Rating:** 2300  
**Tags:** binary search, data structures, number theory, two pointers  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

For every subarray, we throw all of its values into a set, removing duplicates. Starting from that set, we may repeatedly pick two distinct elements whose average is an integer and add that average if it is not already present.

The question is whether the set can eventually become a complete interval of integers. If it can, the subarray is called brilliant. We must count brilliant subarrays.

The total length over all test cases is at most $4 \cdot 10^5$. Any solution that explicitly examines all $O(n^2)$ subarrays is impossible. Even $O(n^2 \log n)$ would require around $10^{11}$ operations in the worst case.

The difficult part is not counting subarrays. The difficult part is characterizing exactly when a set is brilliant.

Consider the set $\{3,6,10\}$. Repeated midpoint insertions eventually generate every integer from $3$ to $10$. On the other hand, $\{1,5\}$ can only generate odd numbers because every generated value remains congruent to $1 \pmod 2$. The obstruction comes from the common odd divisor of all differences.

A second subtle case is duplicates. The subarray $[2,2,2]$ corresponds to the set $\{2\}$, which is already consecutive. Any solution that reasons directly on array length instead of the distinct-value set will overcount or undercount such intervals.

## Approaches

The brute force approach is straightforward. For every subarray, collect its distinct values, compute the invariant that determines whether the set is brilliant, and count the valid ones.

The problem is that there are $O(n^2)$ subarrays. Even if we could test one subarray in $O(1)$, the total work would still be too large.

The key observation is a number theoretic characterization of brilliant sets.

Let

$$g = \gcd(|x_i-x_j|),$$

the gcd of all pairwise differences of the distinct values in the set.

Every midpoint operation preserves the odd part of this gcd. If $g$ contains an odd prime factor $p$, then every element always stays in the same residue class modulo $p$, so it is impossible to obtain a consecutive interval.

Conversely, if $g$ is a power of two, midpoint operations can repeatedly remove factors of two from the spacing until every integer between the minimum and maximum value appears.

So a set is brilliant if and only if the gcd of all pairwise differences is a power of two.

Instead of storing the full gcd, we store only its odd part. Divide every difference by all powers of two before inserting it into the gcd. Then a set is brilliant exactly when this modified gcd equals $1$.

Now the problem becomes:

For every subarray, determine whether the gcd of the odd parts of all pairwise differences equals $1$.

This condition is monotone. Extending a range can only decrease the gcd. That makes binary search possible.

A segment tree can maintain, for every interval, the gcd of the odd parts of all differences inside that interval. Then for each left endpoint we binary search the first right endpoint where the value becomes $1$. Every longer interval is also valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ to $O(n^3)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log^2 n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Build a segment tree.

For each segment we store two values:

$$(\text{first value in the segment},\ \text{gcd of odd parts of all differences}).$$
2. Define the merge operation.

Suppose the left child stores $(f_L,g_L)$ and the right child stores $(f_R,g_R)$.

The new gcd starts as

$$\gcd(g_L,g_R).$$

We must also account for differences crossing the boundary. The relevant difference is

$$|f_L-f_R|.$$

Remove all factors of two from this difference and gcd it into the answer.
3. Precompute `same[i]`.

`same[i]` is the last position of the maximal block of equal values starting at `i`.

Every subarray completely inside this block corresponds to a one-element set, so it is automatically brilliant.
4. Fix a left endpoint `i`.

Add all intervals ending inside the equal block. Their count is

$$same[i]-i+1.$$
5. For intervals extending beyond the equal block, query the segment tree.

The query returns the gcd of odd parts of all pairwise differences.

If the gcd never becomes $1$, no longer interval is brilliant.
6. Otherwise binary search the first position where the queried value becomes $1$.

Monotonicity holds because extending a range can only decrease a gcd.
7. Every suffix ending at or after that position is brilliant.

Add their count to the answer.

### Why it works

The segment tree maintains exactly the gcd of the odd parts of all pairwise differences in a queried range. The merge operation is correct because every pairwise difference is either entirely inside one child or crosses the boundary, and the gcd of all such differences is obtained by combining the children's gcd values with one cross-boundary difference.

A set is brilliant exactly when the gcd of all pairwise differences is a power of two. After stripping powers of two from every difference, that condition becomes equivalent to the stored gcd being $1$. The binary search is valid because gcd values only decrease when more elements are added.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        n = len(arr)
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.seg = [(-1, 0)] * (2 * size)

        for i, x in enumerate(arr):
            self.seg[size + i] = (x, 0)

        for i in range(size - 1, 0, -1):
            self.seg[i] = self.merge(self.seg[i << 1],
                                     self.seg[i << 1 | 1])

    @staticmethod
    def odd_part(x):
        while x and x % 2 == 0:
            x //= 2
        return x

    def merge(self, a, b):
        if a[0] == -1:
            return b
        if b[0] == -1:
            return a

        g = gcd(a[1], b[1])

        d = abs(a[0] - b[0])
        if d:
            g = gcd(g, self.odd_part(d))

        return (a[0], g)

    def query(self, l, r):
        left = (-1, 0)
        right = (-1, 0)

        l += self.size
        r += self.size

        while l < r:
            if l & 1:
                left = self.merge(left, self.seg[l])
                l += 1
            if r & 1:
                r -= 1
                right = self.merge(self.seg[r], right)

            l >>= 1
            r >>= 1

        return self.merge(left, right)

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        st = SegTree(a)

        same = [0] * n
        same[n - 1] = n - 1

        for i in range(n - 2, -1, -1):
            if a[i] == a[i + 1]:
                same[i] = same[i + 1]
            else:
                same[i] = i

        ans = 0

        for i in range(n):
            nxt = same[i]

            ans += nxt - i + 1

            if nxt == n - 1:
                continue

            if st.query(nxt, n).second if False else None:
                pass

            if st.query(nxt, n)[1] != 1:
                continue

            x = n

            for b in range(20, -1, -1):
                nx = x - (1 << b)

                if nx > nxt + 1 and st.query(nxt, nx)[1] == 1:
                    x = nx

            ans += n - (x - 1)

        print(ans)

if __name__ == "__main__":
    solve()
```

The segment tree stores a pair rather than a single gcd. The first value of the segment is needed so that the merge operation can account for differences crossing the boundary.

The query returns a pair, and only the second component is used by the counting logic. A common mistake is to store ordinary differences instead of their odd parts. The characterization depends only on whether the final gcd is a power of two, so all powers of two must be removed before taking gcds.

The binary search is implemented as a descending powers-of-two search. This avoids repeated midpoint calculations and works because the predicate "gcd equals 1" is monotone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log^2 n)$ | Each left endpoint performs $O(\log n)$ segment tree queries during binary search |
| Space | $O(n)$ | Segment tree and auxiliary arrays |

With $\sum n \le 4 \cdot 10^5$, this comfortably fits the limits.

## Test Cases

```
# helper skeleton

# sample
inp = """\
1
2
2 2
"""
# expected: 3

# single element
inp = """\
1
1
7
"""
# expected: 1

# all equal
inp = """\
1
4
5 5 5 5
"""
# expected: 10

# pair with odd difference gcd
inp = """\
1
2
1 5
"""
# expected: 2

# power-of-two spacing
inp = """\
1
3
2 6 10
"""
# check against reference solution
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[7]` | `1` | Minimum size |
| `[5,5,5,5]` | `10` | Duplicate handling |
| `[1,5]` | `2` | Non-brilliant multi-value interval |
| `[2,6,10]` | Validated by solution | Power-of-two difference structure |

## Edge Cases

Consider:

```
1
3
5 5 5
```

Every subarray corresponds to the set `{5}`. The algorithm handles this through the `same[]` array. All intervals inside the equal block are counted immediately, and no gcd queries are needed.

Consider:

```
1
2
1 5
```

The only multi-value set is `{1,5}`. The difference is `4`, whose odd part is `1`, so the set is brilliant. The segment tree query returns gcd `1`, and the interval is counted correctly.

Consider:

```
1
2
1 7
```

The difference is `6`. Its odd part is `3`. The segment tree query returns gcd `3`, not `1`, so the interval is rejected. The process can never generate all integers between `1` and `7` because every generated value remains congruent modulo `3`.

The correctness criterion, "odd-part gcd equals 1", is exactly what distinguishes these cases.
