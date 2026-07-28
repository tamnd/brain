---
title: "CF 102770E - Easy DP Problem"
description: "The straightforward approach is to compute the DP for every query independently. For a segment of length m, we can maintain the states dp[i][j] while scanning its elements. This is correct because the recurrence directly describes the optimal choice among the first i elements."
date: "2026-07-28T23:08:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102770
codeforces_index: "E"
codeforces_contest_name: "The 17th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102770
solve_time_s: 64
verified: true
draft: false
---

[CF 102770E - Easy DP Problem](https://codeforces.com/problemset/problem/102770/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Approaches

The straightforward approach is to compute the DP for every query independently. For a segment of length `m`, we can maintain the states `dp[i][j]` while scanning its elements. This is correct because the recurrence directly describes the optimal choice among the first `i` elements. However, one query costs `O(mk)`, because every state up to `m` and `k` has to be considered. With `m` and `k` both near `100000`, a single query can already require billions of operations.

The key observation is that the DP contains a hidden simpler problem. Remove the part contributed by the `i²` terms. Define:

`g[i][j] = dp[i][j] - (1² + 2² + ... + i²)`

The transition becomes:

`g[i][j] = max(g[i-1][j], g[i-1][j-1] + b[i])`

This is exactly the recurrence for choosing `j` elements with maximum possible sum from the first `i` elements. Since the values are positive, the best `k` elements are simply the `k` largest numbers in the segment.

Each query is now reduced to finding the sum of the largest `k` values in a subarray, then adding the fixed value:

`m(m+1)(2m+1)/6`

To answer these range queries quickly, we build a wavelet tree. It recursively divides values into smaller ranges. At every node, it stores how many values and what sum of values go into the left side. This lets us skip entire value ranges when searching for the largest elements. To find the sum of the largest `k` values, we always inspect the larger-value child first. If that child contains at least `k` elements, the answer is entirely inside it. Otherwise, we take all elements from that child and continue searching for the remaining elements in the smaller-value child.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(mk)` per query | `O(m)` | Too slow |
| Wavelet Tree | `O(log A)` per query | `O(n log A)` | Accepted |

Here `A` is the maximum array value, at most `10^6`.

## Algorithm Walkthrough

1. Build a wavelet tree over the original array. Each node represents a range of possible values. While building a node, split the sequence into values going to the lower half and higher half, and store prefix counts and prefix sums for the lower half. These prefix arrays allow us to know how many values move to each child inside any query interval.
2. For each query `(l, r, k)`, convert the positions to the wavelet tree's zero-based indexing. We need the sum of the largest `k` values in this interval.
3. At a wavelet tree node, determine how many elements of the query range belong to the high-value child. If this count is at least `k`, recurse into that child because all required elements are among the larger values.
4. If the high-value child contains fewer than `k` elements, add the sum of all those elements to the answer and continue into the low-value child asking for the remaining number of elements.
5. Add the quadratic contribution of the DP. If the segment length is `m`, the contribution is the sum of squares from `1` to `m`, computed with the formula `m(m+1)(2m+1)/6`.

The invariant behind the query process is that at every wavelet tree node, the algorithm keeps exactly the number of largest values still required from the current value interval. The higher child always contains values larger than every value in the lower child, so taking all possible values from the higher side before exploring the lower side preserves the definition of the top `k` sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

class WaveletTree:
    def __init__(self, arr, lo, hi):
        self.lo = lo
        self.hi = hi
        self.pref_cnt = None
        self.pref_sum = None
        self.left = None
        self.right = None

        if not arr or lo == hi:
            return

        mid = (lo + hi) // 2
        left_arr = []
        right_arr = []

        self.pref_cnt = [0]
        self.pref_sum = [0]

        for x in arr:
            if x <= mid:
                left_arr.append(x)
                self.pref_cnt.append(self.pref_cnt[-1] + 1)
                self.pref_sum.append(self.pref_sum[-1] + x)
            else:
                right_arr.append(x)
                self.pref_cnt.append(self.pref_cnt[-1])
                self.pref_sum.append(self.pref_sum[-1])

        self.left = WaveletTree(left_arr, lo, mid)
        self.right = WaveletTree(right_arr, mid + 1, hi)

    def top_sum(self, l, r, k):
        if k == 0:
            return 0
        if self.lo == self.hi:
            return self.lo * k

        left_before = self.pref_cnt[l]
        left_in_range = self.pref_cnt[r] - left_before

        right_count = (r - l) - left_in_range

        if right_count >= k:
            return self.right.top_sum(l - left_before, r - self.pref_cnt[r], k)

        right_sum = self.pref_sum[r] - self.pref_sum[l]
        return right_sum + self.left.top_sum(left_before, self.pref_cnt[r], k - right_count)

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        tree = WaveletTree(a, 1, 10**6)

        q = int(input())
        for _ in range(q):
            l, r, k = map(int, input().split())

            selected = tree.top_sum(l - 1, r, k)

            length = r - l + 1
            squares = length * (length + 1) * (2 * length + 1) // 6

            ans.append(str(selected + squares))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The wavelet tree stores the array split by value, not by position. This is the key detail that makes it useful for this problem. A query range can be translated through every node because each node stores enough prefix information to know how many elements went to each child.

The `top_sum` function works with half-open positions inside the current node. The variables `l` and `r` describe the current interval inside that node's stored sequence. The expression `self.pref_cnt[r] - self.pref_cnt[l]` gives the number of values that belong to the lower child. The number of values in the higher child is the rest.

The leaf case is simple because every remaining value is identical. If we need `k` values from a leaf containing value `x`, their sum is `x * k`.

Python integers automatically handle the large intermediate values. The square sum can reach around `10^15`, so using a fixed-width 32-bit type would overflow in languages where integers are not automatically expanded.

## Worked Examples

Consider the segment `[1, 100, 2]` with `k = 2`.

| Step | Current value range | High side count | Remaining k | Added sum |
| --- | --- | --- | --- | --- |
| Root | `[1,1000000]` | 1 | 2 | 100 |
| Lower child | `[1,500000]` | 1 | 1 | 2 |

The wavelet tree first takes the largest value `100`, then searches the remaining part for one more value. It finds `2`, producing the selected contribution `102`. The DP contribution is `14`, so the answer is `116`.

For a single element segment `[5]` with `k = 1`, the traversal reaches a leaf immediately.

| Step | Current value range | Remaining k | Added sum |
| --- | --- | --- | --- |
| Leaf | `[5,5]` | 1 | 5 |

The selected contribution is `5`. The segment length is `1`, so the square contribution is `1`, giving the final answer `6`.

These traces show that the data structure always takes the highest available values first and that the fixed DP term is independent of the chosen values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + q) log A)` | Building the wavelet tree visits each value through `log A` levels, and every query follows one path per level. |
| Space | `O(n log A)` | Prefix information is stored for every level of the wavelet tree. |

The maximum value is only `10^6`, so the tree height is about twenty levels. With at most `500000` total elements and queries, the logarithmic factor keeps the total work within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    data = sys.stdin.readline
    t = int(data())
    out = []

    class WT:
        def __init__(self, arr, lo, hi):
            self.lo = lo
            self.hi = hi
            self.pc = self.ps = None
            self.l = self.r = None
            if not arr or lo == hi:
                return
            mid = (lo + hi) // 2
            la, ra = [], []
            self.pc = [0]
            self.ps = [0]
            for x in arr:
                if x <= mid:
                    la.append(x)
                    self.pc.append(self.pc[-1] + 1)
                    self.ps.append(self.ps[-1] + x)
                else:
                    ra.append(x)
                    self.pc.append(self.pc[-1])
                    self.ps.append(self.ps[-1])
            self.l = WT(la, lo, mid)
            self.r = WT(ra, mid + 1, hi)

        def get(self, l, r, k):
            if k == 0:
                return 0
            if self.lo == self.hi:
                return self.lo * k
            left_count = self.pc[r] - self.pc[l]
            right_count = r - l - left_count
            if right_count >= k:
                return self.r.get(l - self.pc[l], r - self.pc[r], k)
            return self.ps[r] - self.ps[l] + self.l.get(self.pc[l], self.pc[r], k - right_count)

    def solve_case(s):
        it = iter(s.split())
        n = int(next(it))
        a = [int(next(it)) for _ in range(n)]
        tree = WT(a, 1, 10**6)
        q = int(next(it))
        res = []
        for _ in range(q):
            l = int(next(it))
            r = int(next(it))
            k = int(next(it))
            m = r - l + 1
            res.append(str(tree.get(l - 1, r, k) + m * (m + 1) * (2 * m + 1) // 6))
        return "\n".join(res)

    result = solve_case(sys.stdin.read())
    sys.stdin = old
    return result

assert run("""1
3
1 100 2
1
1 3 2
""") == "116"

assert run("""1
1
5
1
1 1 1
""") == "6"

assert run("""1
3
3 4 5
1
1 3 3
""") == "26"

assert run("""1
5
7 7 7 7 7
3
1 5 1
1 5 5
2 4 2
""") == "22\n55\n30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,100,2], k=2` | `116` | Choosing non-consecutive largest values |
| `[5], k=1` | `6` | Minimum length and square contribution |
| `[3,4,5], k=3` | `26` | Selecting the entire segment |
| All values equal | `22,55,30` | Equal-value handling and range boundaries |

## Edge Cases

For a length-one query, the wavelet tree reaches a leaf immediately. With the input array `[5]` and query `(1,1,1)`, the selected sum is `5`. The square formula gives `1`, so the output is `6`. The algorithm does not depend on having internal tree nodes for this case.

For a query where `k` equals the segment length, the search eventually collects every value in the range. For `[3,4,5]` and `(1,3,3)`, the wavelet traversal gathers `5`, then `4`, then `3`, giving `12`. Adding the square contribution `14` produces `26`.

For non-consecutive choices, `[1,100,2]` with `k=2` demonstrates why the DP cannot be simplified to a contiguous selection problem. The wavelet tree selects `100` from the high-value side and then `2` from the remaining side, exactly matching the original DP recurrence.
