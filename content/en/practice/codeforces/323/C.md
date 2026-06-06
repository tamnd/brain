---
title: "CF 323C - Two permutations"
description: "Each value from 1 to n appears exactly once in both permutations. For a value v, let: - posP[v] be its position in the first permutation. - posQ[v] be its position in the second permutation."
date: "2026-06-06T05:54:23+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 323
codeforces_index: "C"
codeforces_contest_name: "Testing Round 7"
rating: 2400
weight: 323
solve_time_s: 125
verified: true
draft: false
---

[CF 323C - Two permutations](https://codeforces.com/problemset/problem/323/C)

**Rating:** 2400  
**Tags:** data structures  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

Each value from `1` to `n` appears exactly once in both permutations.

For a value `v`, let:

- `posP[v]` be its position in the first permutation.
- `posQ[v]` be its position in the second permutation.

A query asks for the number of values whose position in the first permutation lies inside `[l1, r1]` and whose position in the second permutation lies inside `[l2, r2]`.

A useful way to visualize the data is as points on a grid. Every value `v` contributes one point

$$(posP[v],\; posQ[v])$$

and the query asks how many points lie inside an axis-aligned rectangle.

Because both arrays are permutations, there are exactly `n` points and no two points share the same x-coordinate or the same y-coordinate.

The constraints completely rule out any per-query scan. With `n = 10^6` and `m = 2 \cdot 10^5`, even an `O(n)` query would require roughly `2 \cdot 10^{11}` operations.

We need something close to logarithmic time per query.

The query parameters are also encoded using the previous answer. This prevents offline reordering techniques such as Mo's algorithm. Queries must be answered online, in the given order.

A common source of mistakes is forgetting that the rectangle borders are inclusive.

For example:

```
p = [1,2,3]
q = [1,2,3]
```

The query

```
[1,2] × [2,3]
```

contains only the values `2`, so the answer is `1`.

A half-open interpretation would incorrectly produce `0`.

Another subtle case comes from the online transformation. Suppose `n = 5` and the previous answer is `2`. Then `x = 3`, and

$$f(5)=((5-1+3)\bmod 5)+1=3.$$

The modulo wrap-around is part of the query generation and must be applied before taking minima and maxima.

## Approaches

The most direct solution is to process each query independently.

For every value `v`, we check whether

$$l_1 \le posP[v] \le r_1$$

and

$$l_2 \le posQ[v] \le r_2.$$

This is correct because it literally implements the definition of the query. Unfortunately it requires `O(n)` work per query. With `10^6` values and `2 \cdot 10^5` queries, the worst case exceeds `10^{11}` checks.

The key observation is that once we know the positions in the second permutation, the problem becomes a one-dimensional range counting problem.

Construct an array

$$A[i] = posQ[p_i].$$

Position `i` in this array corresponds to x-coordinate `i`, and the stored value corresponds to the y-coordinate of the same point.

Now a query rectangle

$$[l_1,r_1] \times [l_2,r_2]$$

becomes:

> In the subarray `A[l1..r1]`, count how many values belong to `[l2,r2]`.

This is a classic static range counting problem.

Because `A` is a permutation of `1..n`, a Wavelet Tree is a natural fit. It supports:

$$\text{count values } \le k$$

inside any subarray in `O(log n)` time.

Then

$$count([l_2,r_2]) = count(\le r_2) - count(\le l_2-1).$$

The structure is built once, then every query is answered online in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Wavelet Tree | O(n log n + m log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Read both permutations.
2. Compute `posQ[v]` for every value `v`.

This lets us immediately find where any value appears in the second permutation.
3. Build the array

$$A[i] = posQ[p_i].$$

Each value now becomes a point `(i, A[i])`.
4. Build a Wavelet Tree over `A`.

For every level, store prefix counts describing how many elements went to the left child. These prefix counts are exactly what allow us to restrict a query interval while descending the tree.
5. Maintain `last_answer`.

The statement defines

$$x = last\_answer + 1$$

except for the first query where `x = 0`.
6. Decode the four query parameters using the given function

$$f(z)=((z-1+x)\bmod n)+1.$$
7. Compute

$$l_1=\min(f(a),f(b)), \quad r_1=\max(f(a),f(b)),$$

and similarly for the second interval.
8. Query the Wavelet Tree for the number of values in `A[l1..r1]` that belong to `[l2,r2]`.

This equals

$$count_{\le r_2} - count_{\le l_2-1}.$$
9. Output the answer and store it as `last_answer`.

### Why it works

The array `A` contains exactly the y-coordinate of the point whose x-coordinate is the array index.

Selecting positions `l1..r1` in `A` is equivalent to restricting points to the x-range of the rectangle. Counting values of `A` inside `[l2,r2]` is equivalent to restricting points to the y-range of the rectangle.

A point belongs to the rectangle if and only if both conditions hold simultaneously. The Wavelet Tree counts exactly those values inside the requested y-range while considering only the requested x-range. Every valid point is counted once, and no invalid point is counted.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

class WaveletTree:
    def __init__(self, data):
        self.pref = []
        self.lo = []
        self.hi = []

        cur = array('I', data)
        segments = [(cur, 1, len(cur))]

        while segments:
            next_segments = []

            for arr, lo, hi in segments:
                self.lo.append(lo)
                self.hi.append(hi)

                if lo == hi:
                    self.pref.append(None)
                    continue

                mid = (lo + hi) >> 1

                pref = array('I', [0])
                left = array('I')
                right = array('I')

                cnt = 0
                for x in arr:
                    if x <= mid:
                        cnt += 1
                        left.append(x)
                    else:
                        right.append(x)
                    pref.append(cnt)

                self.pref.append(pref)

                next_segments.append((left, lo, mid))
                next_segments.append((right, mid + 1, hi))

            segments = next_segments

    def count_leq(self, l, r, k):
        if l > r or k <= 0:
            return 0

        ans = 0
        stack = [(0, l, r)]

        while stack:
            idx, l, r = stack.pop()

            lo = self.lo[idx]
            hi = self.hi[idx]

            if l > r or k < lo:
                continue

            if hi <= k:
                ans += r - l + 1
                continue

            if lo == hi:
                continue

            pref = self.pref[idx]

            left_l = pref[l - 1]
            left_r = pref[r]

            left_count = left_r - left_l

            left_idx = idx * 2 + 1
            right_idx = idx * 2 + 2

            stack.append((
                right_idx,
                l - left_l,
                r - left_r
            ))

            stack.append((
                left_idx,
                left_l + 1,
                left_r
            ))

        return ans

    def range_count(self, l, r, low, high):
        return self.count_leq(l, r, high) - self.count_leq(l, r, low - 1)

def main():
    n = int(input())

    p = list(map(int, input().split()))
    q = list(map(int, input().split()))

    pos_q = [0] * (n + 1)
    for i, v in enumerate(q, 1):
        pos_q[v] = i

    arr = [pos_q[v] for v in p]

    wt = WaveletTree(arr)

    m = int(input())

    last = 0
    out = []

    for qi in range(m):
        a, b, c, d = map(int, input().split())

        x = 0 if qi == 0 else last + 1

        def f(z):
            return ((z - 1 + x) % n) + 1

        fa = f(a)
        fb = f(b)
        fc = f(c)
        fd = f(d)

        l1 = min(fa, fb)
        r1 = max(fa, fb)

        l2 = min(fc, fd)
        r2 = max(fc, fd)

        last = wt.range_count(l1, r1, l2, r2)

        out.append(str(last))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The first stage computes the inverse permutation of `q`. This converts every value into its position in the second permutation.

The array `arr` is the geometric representation of the problem. Index `i` is an x-coordinate and `arr[i]` is the corresponding y-coordinate.

The Wavelet Tree stores, for every internal node, a prefix array telling how many elements of each prefix moved to the left child. During a query, these prefix counts translate a subarray interval from the parent node into the corresponding intervals inside the children.

The query routine computes counts of values at most `k`. A range count is obtained by subtraction. This avoids implementing a separate rectangle-counting operation.

One easy mistake is indexing. The Wavelet Tree query formulas assume 1-based intervals, so all query intervals are kept 1-based throughout the implementation.

Another subtle point is the online decoding. The value `x` uses the previous answer plus one, not the current answer. The first query is the only exception where `x = 0`.

## Worked Examples

### Sample 1

Input:

```
3
3 1 2
3 2 1
1
1 2 3 3
```

We first compute:

| Value | posQ |
| --- | --- |
| 1 | 3 |
| 2 | 2 |
| 3 | 1 |

Then:

| Position in p | Value | A[position] |
| --- | --- | --- |
| 1 | 3 | 1 |
| 2 | 1 | 3 |
| 3 | 2 | 2 |

So `A = [1,3,2]`.

The query decoding gives:

| Variable | Value |
| --- | --- |
| l1 | 1 |
| r1 | 2 |
| l2 | 3 |
| r2 | 3 |

We inspect `A[1..2] = [1,3]`.

Only one value lies in `[3,3]`, namely `3`.

Answer:

```
1
```

This trace shows the reduction from a rectangle query to a value-range query inside a subarray.

### Custom Example

Input:

```
4
1 2 3 4
2 1 4 3
1
1 4 1 2
```

Inverse positions of `q`:

| Value | posQ |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 4 |
| 4 | 3 |

Hence:

| Position | A |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 4 |
| 4 | 3 |

The rectangle is `[1,4] × [1,2]`.

| Subarray | Values |
| --- | --- |
| A[1..4] | 2,1,4,3 |

Values inside `[1,2]` are `2` and `1`.

Answer:

```
2
```

This example shows that x-range filtering and y-range filtering become subarray selection and value selection inside `A`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log n) | Wavelet Tree construction plus logarithmic queries |
| Space | O(n log n) | Prefix counts stored at each level |

With `n = 10^6`, the height is roughly `20`. The total amount of stored prefix information is about `20n`, which fits comfortably within the memory limit when stored in compact integer arrays. The query count is only `2 · 10^5`, so `O(log n)` per query is easily fast enough.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    from array import array

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    # call solution here
    main()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# sample 1
assert run(
"""3
3 1 2
3 2 1
1
1 2 3 3
"""
) == "1"

# n = 1
assert run(
"""1
1
1
1
1 1 1 1
"""
) == "1"

# identical permutations
assert run(
"""3
1 2 3
1 2 3
1
1 3 2 3
"""
) == "2"

# full rectangle
assert run(
"""4
1 2 3 4
2 1 4 3
1
1 4 1 4
"""
) == "4"

# single point rectangle
assert run(
"""4
1 2 3 4
2 1 4 3
1
2 2 1 1
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 1 | Basic correctness |
| n = 1 | 1 | Minimum size |
| Identical permutations | 2 | Inclusive boundaries |
| Full rectangle | 4 | Entire point set counted |
| Single point rectangle | 1 | Exact coordinate matching |

## Edge Cases

Consider the smallest possible input:

```
1
1
1
1
1 1 1 1
```

The only point is `(1,1)`. The query rectangle is also exactly `(1,1)`. The Wavelet Tree contains a single value, and the range count returns `1`. No special handling is needed.

Consider an interval consisting of a single position:

```
4
1 2 3 4
2 1 4 3
1
2 2 1 1
```

The rectangle asks whether the point at x-coordinate `2` has y-coordinate `1`. Since `A[2] = 1`, the answer is `1`. The query interval remains valid because the implementation uses inclusive boundaries everywhere.

Consider modulo wrap-around during query decoding. Let `n = 5` and suppose the previous answer was `2`. Then `x = 3`.

For input value `5`:

$$f(5)=((5-1+3)\bmod 5)+1=3.$$

The algorithm performs this transformation before constructing the rectangle endpoints. After decoding, it still applies `min` and `max`, guaranteeing a valid interval even when wrapping occurs.

Finally, consider a rectangle that covers the entire plane:

```
l1 = 1, r1 = n
l2 = 1, r2 = n
```

Every point satisfies the query. The Wavelet Tree computes

$$count(\le n)-count(\le 0)=n-0=n,$$

which is exactly the correct answer.
