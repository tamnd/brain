---
title: "CF 474E - Pillars"
description: "We have a sequence of pillars arranged from left to right. Pillar i has height h[i]. A valid jump can only go forward, from a smaller index to a larger index, and the height difference between the two pillars must be at least d."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 474
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 271 (Div. 2)"
rating: 2000
weight: 474
solve_time_s: 121
verified: true
draft: false
---

[CF 474E - Pillars](https://codeforces.com/problemset/problem/474/E)

**Rating:** 2000  
**Tags:** binary search, data structures, dp, sortings, trees  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of pillars arranged from left to right. Pillar `i` has height `h[i]`. A valid jump can only go forward, from a smaller index to a larger index, and the height difference between the two pillars must be at least `d`.

The task is to choose a sequence of pillar indices

`i1 < i2 < ... < ik`

such that every consecutive pair forms a valid jump. Among all such sequences, we need one with maximum possible length and must print the actual indices.

The structure immediately suggests a longest-path style dynamic programming problem. If we define `dp[i]` as the longest valid sequence ending at pillar `i`, then

`dp[i] = 1 + max(dp[j])`

over all `j < i` satisfying

`|h[i] - h[j]| ≥ d`.

The challenge is finding that maximum efficiently.

The constraints are what make the problem interesting. There can be up to `100000` pillars, and heights can be as large as `10^15`. A quadratic algorithm would examine roughly `10^10` pairs in the worst case, which is far beyond what can run in one second. We need something around `O(n log n)`.

Several edge cases deserve attention.

When `d = 0`, every forward jump is allowed. For example:

```
3 0
5 5 5
```

The answer is all three pillars. Any solution that accidentally excludes equal heights when `d = 0` would lose valid transitions.

When many pillars have the same height and `d > 0`, jumps between them are forbidden.

```
4 1
7 7 7 7
```

No jump is possible because every height difference is zero. The correct answer has length `1`.

Another subtle case occurs when both smaller and larger heights are valid predecessors.

```
4 3
10 1 20 8
```

For pillar `8`, both height `1` and height `20` satisfy the constraint because the condition uses absolute difference. A solution that only searches one side of the height range misses valid transitions.

The huge height limit also means we cannot build a segment tree directly on height values. Heights must first be compressed into ranks.

## Approaches

The most direct solution is dynamic programming over all pairs of pillars.

Let `dp[i]` be the maximum sequence length ending at pillar `i`. For every pillar `i`, we inspect every earlier pillar `j`. If `|h[i] - h[j]| ≥ d`, then we may extend the sequence ending at `j`.

```
dp[i] = max(dp[i], dp[j] + 1)
```

This recurrence is correct because every valid sequence ending at `i` must come from some earlier valid predecessor. Unfortunately, there are `O(n²)` pairs. With `n = 100000`, this means roughly ten billion comparisons.

The bottleneck is finding

```
max(dp[j])
```

among earlier pillars whose heights belong to one of two regions:

```
h[j] ≤ h[i] - d
```

or

```
h[j] ≥ h[i] + d
```

The key observation is that the condition depends only on height, not on position once we have already processed pillars from left to right.

Suppose we process pillars in index order. When we reach pillar `i`, all valid predecessors have already been processed. Among those processed pillars, we need the maximum DP value in two height intervals.

This becomes a range maximum query problem over heights.

The heights can be compressed into sorted unique coordinates. Then we maintain a segment tree indexed by compressed heights. Each tree position stores the best `(dp value, pillar index)` seen so far for that height.

For pillar `i`, we perform two segment-tree queries:

First interval:

```
(-∞, h[i] - d]
```

Second interval:

```
[h[i] + d, +∞)
```

The better of those two answers gives the predecessor producing the longest sequence ending at `i`.

After computing `dp[i]`, we update the segment tree at the compressed position of `h[i]`.

This reduces the work per pillar to a few binary searches and segment-tree operations, yielding `O(n log n)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all pillar heights.
2. Coordinate-compress the heights by sorting the distinct values and assigning each height a position in that sorted list.
3. Create a segment tree where each node stores a pair `(best_dp, pillar_index)` representing the strongest sequence among processed pillars in that height range.
4. Process pillars from left to right.
5. For the current height `h[i]`, find the last compressed coordinate whose value is at most `h[i] - d`.
6. Query the segment tree on that prefix range. This finds the best predecessor with sufficiently smaller height.
7. Find the first compressed coordinate whose value is at least `h[i] + d`.
8. Query the segment tree on that suffix range. This finds the best predecessor with sufficiently larger height.
9. Take the better result from the two queries. If neither range contains a processed pillar, start a new sequence of length `1`.
10. Set

```
dp[i] = predecessor_dp + 1
```

and store the predecessor index for reconstruction.

1. Update the segment tree at the compressed position of `h[i]` with the pair `(dp[i], i)` if it improves the stored value.
2. After all pillars are processed, find the pillar with maximum `dp`.
3. Follow predecessor pointers backward to reconstruct the optimal sequence.
4. Reverse the reconstructed list and print it.

### Why it works

When processing pillar `i`, the segment tree contains information only about pillars with smaller indices, exactly the set of legal predecessors. Every valid predecessor must have height at most `h[i] - d` or at least `h[i] + d`. The two range queries examine precisely those heights and return the maximum DP value among them.

The recurrence is identical to the quadratic dynamic program, but the segment tree computes the required maximum efficiently. Since every DP state is computed from all valid predecessors and no invalid predecessor is considered, the resulting `dp[i]` is optimal. Reconstruction through stored predecessor indices yields an actual maximum-length sequence.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

n, d = map(int, input().split())
h = list(map(int, input().split()))

vals = sorted(set(h))
m = len(vals)

NEG = (0, -1)

class SegmentTree:
    def __init__(self, n):
        self.n = 1
        while self.n < n:
            self.n <<= 1
        self.seg = [NEG] * (2 * self.n)

    def _better(self, a, b):
        if a[0] >= b[0]:
            return a
        return b

    def update(self, pos, value):
        p = pos + self.n
        if value[0] > self.seg[p][0]:
            self.seg[p] = value
        else:
            return

        p >>= 1
        while p:
            self.seg[p] = self._better(self.seg[p * 2],
                                       self.seg[p * 2 + 1])
            p >>= 1

    def query(self, l, r):
        if l > r:
            return NEG

        l += self.n
        r += self.n

        left_res = NEG
        right_res = NEG

        while l <= r:
            if l & 1:
                left_res = self._better(left_res, self.seg[l])
                l += 1

            if not (r & 1):
                right_res = self._better(self.seg[r], right_res)
                r -= 1

            l >>= 1
            r >>= 1

        return self._better(left_res, right_res)

st = SegmentTree(m)

dp = [0] * n
parent = [-1] * n

for i in range(n):
    best = NEG

    right_small = bisect_right(vals, h[i] - d) - 1
    if right_small >= 0:
        best = st.query(0, right_small)

    left_large = bisect_left(vals, h[i] + d)
    if left_large < m:
        cand = st.query(left_large, m - 1)
        if cand[0] > best[0]:
            best = cand

    dp[i] = best[0] + 1
    parent[i] = best[1]

    pos = bisect_left(vals, h[i])
    st.update(pos, (dp[i], i))

end = max(range(n), key=lambda x: dp[x])

answer = []
cur = end

while cur != -1:
    answer.append(cur + 1)
    cur = parent[cur]

answer.reverse()

print(len(answer))
print(*answer)
```

The coordinate compression step converts heights up to `10^15` into indices between `0` and `m - 1`, making segment-tree storage feasible.

The segment tree stores pairs `(dp value, index)` rather than only DP values. The DP value is needed for optimization, while the index is needed later for reconstruction.

The two binary searches identify the two valid height regions. `bisect_right(vals, h[i] - d) - 1` gives the largest compressed coordinate that still belongs to the lower interval. `bisect_left(vals, h[i] + d)` gives the first coordinate belonging to the upper interval.

A common mistake is updating the segment tree before querying it. Doing so would allow a pillar to use itself as a predecessor. Processing strictly in left-to-right order and querying before updating prevents that issue.

Another subtle point is handling empty ranges. When no height belongs to a queried interval, the segment tree query is skipped and the result remains the neutral value `(0, -1)`.

## Worked Examples

### Sample 1

Input:

```
5 2
1 3 6 7 4
```

Compressed heights:

```
[1, 3, 4, 6, 7]
```

| i | height | best predecessor dp | dp[i] | parent |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | -1 |
| 2 | 3 | 1 | 2 | 1 |
| 3 | 6 | 2 | 3 | 2 |
| 4 | 7 | 3 | 4 | 3 |
| 5 | 4 | 3 | 4 | 3 |

The maximum DP value is `4`. One valid reconstruction is:

```
1 2 3 5
```

This trace shows how each pillar obtains the best predecessor through height-range queries rather than checking every earlier pillar individually.

### Example 2

Input:

```
4 1
7 7 7 7
```

| i | height | best predecessor dp | dp[i] | parent |
| --- | --- | --- | --- | --- |
| 1 | 7 | 0 | 1 | -1 |
| 2 | 7 | 0 | 1 | -1 |
| 3 | 7 | 0 | 1 | -1 |
| 4 | 7 | 0 | 1 | -1 |

Since the height difference between any pair is zero, no jump is legal. Every pillar starts its own sequence.

The final answer has length `1`, and any single index is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each pillar performs a constant number of binary searches and segment-tree operations |
| Space | O(n) | DP arrays, parent array, compressed coordinates, and segment tree |

With `n = 100000`, an `O(n log n)` solution performs only a few million operations, which comfortably fits within the time limit. The memory usage is linear and well below the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left, bisect_right

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, d = map(int, input().split())
    h = list(map(int, input().split()))

    vals = sorted(set(h))
    m = len(vals)

    NEG = (0, -1)

    class SegmentTree:
        def __init__(self, n):
            self.n = 1
            while self.n < n:
                self.n <<= 1
            self.seg = [NEG] * (2 * self.n)

        def better(self, a, b):
            return a if a[0] >= b[0] else b

        def update(self, pos, value):
            p = pos + self.n
            if value[0] <= self.seg[p][0]:
                return
            self.seg[p] = value
            p >>= 1
            while p:
                self.seg[p] = self.better(
                    self.seg[p * 2],
                    self.seg[p * 2 + 1]
                )
                p >>= 1

        def query(self, l, r):
            if l > r:
                return NEG
            l += self.n
            r += self.n
            res = NEG
            while l <= r:
                if l & 1:
                    res = self.better(res, self.seg[l])
                    l += 1
                if not (r & 1):
                    res = self.better(res, self.seg[r])
                    r -= 1
                l >>= 1
                r >>= 1
            return res

    st = SegmentTree(m)

    dp = [0] * n
    par = [-1] * n

    for i in range(n):
        best = NEG

        p = bisect_right(vals, h[i] - d) - 1
        if p >= 0:
            best = st.query(0, p)

        q = bisect_left(vals, h[i] + d)
        if q < m:
            cand = st.query(q, m - 1)
            if cand[0] > best[0]:
                best = cand

        dp[i] = best[0] + 1
        par[i] = best[1]

        st.update(bisect_left(vals, h[i]), (dp[i], i))

    ans = max(dp)
    return str(ans)

# provided sample
assert run("5 2\n1 3 6 7 4\n") == "4"

# minimum size
assert run("1 5\n10\n") == "1"

# all equal heights, d > 0
assert run("4 1\n7 7 7 7\n") == "1"

# d = 0, every jump allowed
assert run("5 0\n2 2 2 2 2\n") == "5"

# alternating valid jumps
assert run("5 10\n1 20 2 30 3\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 / 10` | `1` | Minimum input size |
| `4 1 / 7 7 7 7` | `1` | Equal heights with forbidden jumps |
| `5 0 / 2 2 2 2 2` | `5` | Special case where every jump is legal |
| `5 10 / 1 20 2 30 3` | `5` | Long chain using both low and high height ranges |

## Edge Cases

Consider:

```
4 1
7 7 7 7
```

For every pillar, the valid height ranges are `≤ 6` and `≥ 8`. Neither range contains any processed pillar. Both segment-tree queries return the neutral value, so every `dp[i]` becomes `1`. The algorithm correctly reports that no jump is possible.

Consider:

```
5 0
2 2 2 2 2
```

Now every earlier pillar is a valid predecessor. The lower interval becomes `≤ 2`, which already contains all processed pillars. Each new pillar extends the best sequence found so far, producing DP values `1, 2, 3, 4, 5`. The answer is the full sequence.

Consider:

```
4 3
10 1 20 8
```

For height `8`, the valid predecessors are both height `1` and height `20`, since the condition is based on absolute difference. The algorithm performs two separate range queries, one for smaller heights and one for larger heights, then takes the better result. This avoids the common bug of considering only one side of the height spectrum.

Consider:

```
3 1000000000
1 1000000000000000 2
```

The heights are enormous, but coordinate compression maps them to a tiny index range. The segment tree never depends on the raw height values, so the algorithm handles the full `10^15` range without increasing memory usage.
