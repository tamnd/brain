---
title: "CF 102222L - Continuous Intervals"
description: "For a subarray (al,ldots,ar), sort its values and look at consecutive values in that sorted order. The subarray is valid exactly when no gap between two neighboring distinct values exceeds (1). Equal values are allowed, so a subarray such as ([1,1,2,2]) is valid."
date: "2026-08-17T22:18:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "L"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 143
verified: true
draft: false
---

[CF 102222L - Continuous Intervals](https://codeforces.com/problemset/problem/102222/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

For a subarray (a_l,\ldots,a_r), sort its values and look at consecutive values in that sorted order. The subarray is valid exactly when no gap between two neighboring distinct values exceeds (1). Equal values are allowed, so a subarray such as ([1,1,2,2]) is valid.

A useful way to express the condition is to ignore repeated copies of the same value. Let (mx) be the maximum, (mn) the minimum, and (cnt) the number of distinct values in the subarray. Because every value is an integer between (mn) and (mx), there are (mx-mn+1) possible integer values in that range. The subarray is continuous exactly when every one of those values occurs, which gives

[
mx-mn+1=cnt.
]

Equivalently,

[
mx-mn-cnt=-1.
]

So the problem becomes counting subarrays for which the quantity (mx-mn-cnt) equals (-1). This is the central transformation used by the standard solution.

There are up to (10^5) elements in one test case and (10^6) elements in total. An (O(n^2)) solution performs roughly (n(n+1)/2) interval extensions, which is about (5\cdot10^9) operations when (n=10^5). Even with constant-time updates, that is far beyond what a 10-second contest limit can tolerate. We need an (O(n\log n)) approach, with only linear or logarithmic work per element.

The first edge case is repetition. For input

```
1
2
1 1
```

the correct answer is (3), because all three subarrays are continuous. A careless solution might compare the subarray length with (mx-mn+1), treating ([1,1]) as having two elements in a range containing only one integer. Repetitions do not create gaps, so the correct quantity is the number of distinct values, not the length.

The second edge case is a missing integer. For

```
1
2
1 3
```

the answer is (2). The singleton intervals are valid, but ([1,3]) is not, because the sorted values have a gap of (2). Merely checking that the minimum and maximum are close to the endpoints of some range is insufficient. The distinct-count equality detects the missing value correctly.

The third edge case is an interval containing duplicates and all required values. For

```
1
4
1 2 2 3
```

every one of the ten subarrays is continuous, so the answer is (10). The full interval has (mx=3), (mn=1), and (cnt=3), giving (3-1+1=3). The duplicate (2) does not change (cnt).

A final implementation edge case comes from the fact that the answer can be large. When all (10^5) elements are equal, every subarray is valid and the answer is

[
\frac{10^5\cdot100001}{2}=5,000,050,000.
]

A 32-bit signed integer is not enough. Python integers handle this automatically, but the same algorithm in C++ needs a 64-bit answer.

## Approaches

The direct approach fixes a left endpoint and extends the right endpoint. While extending, we can maintain the current minimum, maximum, and a set of distinct values. Each extension then takes expected (O(1)) work for the set and constant work for the extrema. This gives (O(n^2)) total time, and it is correct because every subarray is examined exactly once.

The problem is the number of subarrays. There are (n(n+1)/2) of them, which is about (5\cdot10^9) for (n=10^5). Even though each individual extension is cheap, the total work is not.

The faster approach fixes the right endpoint (r) and considers every possible left endpoint simultaneously. Define

[
F_r(l)=\max(a_l,\ldots,a_r)-\min(a_l,\ldots,a_r)-\operatorname{distinct}(a_l,\ldots,a_r).
]

We need the number of left endpoints with (F_r(l)=-1).

When (a_r) is appended, the maximum changes only for a contiguous collection of left endpoints. A monotonic decreasing stack tells us exactly which left endpoints have their maximum replaced by (a_r). Similarly, a monotonic increasing stack tells us which left endpoints have their minimum replaced by (a_r).

The distinct-count part has an especially clean update. Suppose the previous occurrence of (a_r) was at position (p). For a subarray ending at (r), the new value (a_r) is a new distinct value exactly when its left endpoint is in ([p+1,r]). Thus we subtract (1) from (F_r(l)) on precisely that range.

All three operations are range additions to an array indexed by the left endpoint. We need to maintain the minimum value of that array and how many positions attain that minimum. A lazy segment tree supports exactly this operation.

There is also a useful inequality:

[
\operatorname{distinct}\leq \max-\min+1.
]

Hence

[
F_r(l)=\max-\min-\operatorname{distinct}\geq -1.
]

The singleton interval ([r,r]) always has (F_r(r)=-1). Consequently, after processing position (r), the global minimum of the segment tree is always exactly (-1), and the number of positions attaining that minimum is precisely the number of valid subarrays ending at (r). We do not even need a separate query over ([1,r]).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Create a segment tree whose leaf (l) represents the value (F(l)) for the current right endpoint. Initially every value is (0), because no right endpoint has been processed yet. Each tree node stores the minimum value in its range, the number of leaves attaining that minimum, and a lazy addition.
2. Maintain a monotonic decreasing stack for maximum values. Each stack entry stores a value and its most recent position. Before inserting (a_r), the left endpoints after the previous stack top all obtain (a_r) as their new maximum, so add (a_r) to that range.
3. Remove stack entries whose value is less than or equal to (a_r). When an entry ((v,p)) is removed, the maximum contribution on the left-endpoint range between the previous surviving stack position and (p) changes from (v) to (a_r). Add (a_r-v) to that range. Equal values are popped as well because the newest occurrence gives the correct boundary for future updates.
4. Push ((a_r,r)) onto the maximum stack. Each array position enters and leaves this stack at most once, so all maximum updates together require only (O(n)) range-update operations.
5. Repeat the same construction with a monotonic increasing stack for minimum values. The minimum contributes with a negative sign in (F), so when (a_r) becomes the new minimum, the direct contribution is (-a_r). When an old minimum (v) is replaced by (a_r), add (v-a_r).
6. Look up the previous occurrence (p) of (a_r), using a dictionary. Add (-1) to the range ([p+1,r]). Those are exactly the left endpoints for which (a_r) was not already present in the preceding subarray. Then store (r) as the new previous occurrence.
7. Read the root of the segment tree. Its minimum is (-1), and its count is the number of valid intervals ending at (r). Add that count to the answer.
8. After all right endpoints have been processed, print the accumulated answer in the required `Case #x: y` format.

### Why it works

For every fixed right endpoint (r), the segment tree leaf (l) represents exactly

[
F_r(l)=\max(a_l,\ldots,a_r)-\min(a_l,\ldots,a_r)-\operatorname{distinct}(a_l,\ldots,a_r).
]

The maximum stack updates preserve the maximum term for every left endpoint, because the stack partitions left endpoints according to which occurrence is currently the maximum. The minimum stack does the same for the minimum term. The previous-occurrence update subtracts exactly once for every distinct value in every subarray, because a value contributes to the distinct count for left endpoints after its previous occurrence.

Thus every leaf has the correct (F_r(l)) after position (r) is processed. A subarray is continuous precisely when (F_r(l)=-1). Since every (F_r(l)\geq-1) and the singleton interval gives equality, the segment tree minimum is (-1), and its minimum count is exactly the number of continuous intervals ending at (r). Summing this count over all (r) counts every valid subarray exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

class SegmentTree:
    def __init__(self, n):
        self.n = n
        size = 4 * n + 5
        self.mn = [0] * size
        self.cnt = [0] * size
        self.lazy = [0] * size
        self._build(1, 1, n)

    def _build(self, p, l, r):
        self.cnt[p] = r - l + 1
        if l == r:
            return
        m = (l + r) >> 1
        self._build(p << 1, l, m)
        self._build(p << 1 | 1, m + 1, r)

    def _push(self, p):
        z = self.lazy[p]
        if z:
            lc = p << 1
            rc = lc | 1

            self.mn[lc] += z
            self.mn[rc] += z
            self.lazy[lc] += z
            self.lazy[rc] += z

            self.lazy[p] = 0

    def _pull(self, p):
        lc = p << 1
        rc = lc | 1

        if self.mn[lc] < self.mn[rc]:
            self.mn[p] = self.mn[lc]
            self.cnt[p] = self.cnt[lc]
        elif self.mn[lc] > self.mn[rc]:
            self.mn[p] = self.mn[rc]
            self.cnt[p] = self.cnt[rc]
        else:
            self.mn[p] = self.mn[lc]
            self.cnt[p] = self.cnt[lc] + self.cnt[rc]

    def _add(self, p, l, r, ql, qr, value):
        if ql <= l and r <= qr:
            self.mn[p] += value
            self.lazy[p] += value
            return

        self._push(p)

        m = (l + r) >> 1
        if ql <= m:
            self._add(p << 1, l, m, ql, qr, value)
        if qr > m:
            self._add(p << 1 | 1, m + 1, r, ql, qr, value)

        self._pull(p)

    def add(self, l, r, value):
        if l <= r:
            self._add(1, 1, self.n, l, r, value)

    @property
    def minimum(self):
        return self.mn[1]

    @property
    def minimum_count(self):
        return self.cnt[1]

def count_intervals(a):
    n = len(a)
    seg = SegmentTree(n)

    big = []
    small = []
    last = {}

    answer = 0

    for r, x in enumerate(a, 1):
        # Add the contribution of the new maximum.
        left = big[-1][1] + 1 if big else 1
        seg.add(left, r, x)

        # Replace old maxima by x.
        while big and big[-1][0] <= x:
            value, pos = big.pop()
            left = big[-1][1] + 1 if big else 1
            seg.add(left, pos, x - value)

        big.append((x, r))

        # Add the contribution of the new minimum.
        left = small[-1][1] + 1 if small else 1
        seg.add(left, r, -x)

        # Replace old minima by x.
        while small and small[-1][0] >= x:
            value, pos = small.pop()
            left = small[-1][1] + 1 if small else 1
            seg.add(left, pos, value - x)

        small.append((x, r))

        # Count x as a distinct value exactly for left endpoints
        # after its previous occurrence.
        previous = last.get(x, 0)
        seg.add(previous + 1, r, -1)
        last[x] = r

        # The minimum is always -1 because [r, r] is valid.
        answer += seg.minimum_count

    return answer

def solve():
    t = int(input())
    out = []

    for case_id in range(1, t + 1):
        n = int(input())
        a = list(map(int, input().split()))

        out.append(
            f"Case #{case_id}: {count_intervals(a)}"
        )

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The segment tree is initialized with all values equal to zero. The `cnt` array records how many leaves belong to each node, so the initial minimum is zero and every position contributes to its count.

The `_add` method performs a standard lazy range addition. A fully covered node receives the value directly, while partially covered nodes push their pending lazy value to their children, recurse, and then recompute their minimum and minimum count.

The maximum stack stores pairs `(value, position)` in decreasing value order. The first range addition assigns the new value to left endpoints after the current stack top. Every popped entry represents a range whose old maximum is replaced by the new value, so its contribution changes by `x - value`.

The minimum stack is symmetric, but its contribution has the opposite sign. Its replacement amount is `value - x`.

The dictionary `last` is keyed by the actual array value, so values up to (10^9) require no coordinate compression. If `previous` is the last occurrence of `x`, then exactly the left endpoints from `previous + 1` through `r` see `x` for the first time.

The answer is updated using `seg.minimum_count` after all three types of changes for the current right endpoint. The singleton ([r,r]) always makes the minimum equal to (-1), so no query range or special handling of inactive leaves is necessary.

Python integers also remove any overflow concern for the final answer. The recursive segment-tree depth is only (O(\log n)), while `sys.setrecursionlimit` provides enough room for the recursive implementation.

## Worked Examples

For the first sample, the array is ([1,2,1,2]). Every subarray is continuous because the only values that can appear are (1) and (2), which are consecutive.

| Right endpoint (r) | (a_r) | Valid left endpoints | Minimum | Minimum count | Running answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | -1 | 1 | 1 |
| 2 | 2 | 1, 2 | -1 | 2 | 3 |
| 3 | 1 | 1, 2, 3 | -1 | 3 | 6 |
| 4 | 2 | 1, 2, 3, 4 | -1 | 4 | 10 |

The important point here is that duplicates do not increase the distinct count. At (r=3), for example, the interval ([1,2,1]) has maximum (2), minimum (1), and two distinct values, so (2-1-2=-1). The three intervals ending at position (3) are all counted.

For the second sample, the array is ([1,3,2,4]).

| Right endpoint (r) | (a_r) | Valid left endpoints | Minimum | Minimum count | Running answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | -1 | 1 | 1 |
| 2 | 3 | 2 | -1 | 1 | 2 |
| 3 | 2 | 1, 2, 3 | -1 | 3 | 5 |
| 4 | 4 | 2, 3, 4 | -1 | 3 | 8 |

At (r=2), the interval ([1,3]) is rejected because its maximum is (3), its minimum is (1), and it contains two distinct values. Its value is (3-1-2=0), not (-1). At (r=3), adding (2) fills the missing integer in ([1,3]), so ([1,3,2]) becomes valid. At (r=4), ([3,2,4]) is valid because its sorted values are (2,3,4), while ([2,4]) remains invalid because (3) is missing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Every element enters and leaves each monotonic stack once, producing (O(n)) range additions, and each range addition costs (O(\log n)). |
| Space | (O(n)) | The segment tree, two monotonic stacks, and the last-occurrence dictionary all use (O(n)) memory. |

Across all test cases, the total (n) is at most (10^6). The algorithm performs a linear number of stack operations and range updates per element, with logarithmic segment-tree cost, giving (O(10^6\log 10^5)) asymptotic work. The memory consumption is linear in the largest test case, which fits the stated 256 MB limit for the intended implementation.

## Test Cases

The following tests are intended to be appended after the solution code above. The helper redirects standard input and output and resets the `input` function so each invocation behaves like a separate contest run.

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        global input
        input = sys.stdin.readline

        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

# Provided samples
sample = """\
2
4
1 2 1 2
4
1 3 2 4
"""
assert run(sample) == "Case #1: 10\nCase #2: 8", "provided samples"

# Minimum-size input
assert run("""\
1
1
7
""") == "Case #1: 1", "single element"

# All values equal: every subarray is continuous.
assert run("""\
1
5
9 9 9 9 9
""") == "Case #1: 15", "all equal values"

# Missing integer in the pair, then restored by the third value.
assert run("""\
1
3
1 3 2
""") == "Case #1: 5", "missing integer"

# Large value gap. Only the singleton intervals are valid.
assert run("""\
1
2
1 1000000000
""") == "Case #1: 2", "boundary values"

# Duplicates must not be counted as additional distinct values.
assert run("""\
1
4
1 2 2 3
""") == "Case #1: 10", "duplicates"

# Maximum-size case, also checks that the answer exceeds 32-bit range.
n = 100000
maximum_case = "1\n" + str(n) + "\n" + ("7 " * (n - 1)) + "7\n"
assert run(maximum_case) == "Case #1: 5000050000", "maximum-size all-equal case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 7` | `Case #1: 1` | Minimum input and singleton handling |
| `1 / 5 / 9 9 9 9 9` | `Case #1: 15` | Every subarray remains valid when all values are equal |
| `1 / 3 / 1 3 2` | `Case #1: 5` | A missing integer can make an interval invalid, then valid after extension |
| `1 / 2 / 1 1000000000` | `Case #1: 2` | Very large value gaps |
| `1 / 4 / 1 2 2 3` | `Case #1: 10` | Correct treatment of duplicates |
| (n=100000), all values `7` | `Case #1: 5000050000` | Maximum input size and large answer |

## Edge Cases

For the duplicate-value case

```
1
2
1 1
```

the first position produces (F(1,1)=1-1-1=-1). At the second position, the maximum and minimum do not change. The previous occurrence of (1) is position (1), so the distinct-count update affects only left endpoint (2). Both leaves consequently have value (-1), and the segment tree reports two valid intervals ending at position (2). Together with the first singleton, the answer is (3).

For the missing-value case

```
1
2
1 3
```

the interval ending at position (2) with left endpoint (1) has (mx=3), (mn=1), and (cnt=2), giving (F=0). The singleton ([3]) has (F=-1). Thus the segment tree minimum is still (-1), but only one leaf attains it. The total answer is (1+1=2).

For the duplicate-filled range

```
1
4
1 2 2 3
```

the full interval has (mx=3), (mn=1), and (cnt=3), so its value is (-1). The repeated (2) changes neither the minimum nor the distinct count. The same reasoning applies to every shorter interval, giving ten valid subarrays.

For the maximum-size equal-value case, every subarray has (mx=mn) and (cnt=1), so (F=-1) for every left endpoint. At each right endpoint (r), the segment tree minimum count is exactly (r). Summing (1+2+\cdots+100000) gives (5,000,050,000), which confirms both the counting logic and the need for an integer type capable of holding the full result.
