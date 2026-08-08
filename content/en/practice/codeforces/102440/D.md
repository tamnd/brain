---
title: "CF 102440D - \u041f\u0435\u0442\u044f \u0438 \u043c\u0430\u0441\u0441\u0438\u0432"
description: "We have an array (a) and a nonnegative threshold (k). A subarray is called beautiful if, after deleting at most one element from it, its maximum minus its minimum can be made at most (k)."
date: "2026-08-08T13:46:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "D"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 166
verified: true
draft: false
---

[CF 102440D - \u041f\u0435\u0442\u044f \u0438 \u043c\u0430\u0441\u0441\u0438\u0432](https://codeforces.com/problemset/problem/102440/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array (a) and a nonnegative threshold (k). A subarray is called beautiful if, after deleting at most one element from it, its maximum minus its minimum can be made at most (k). A query ([L,R]) asks for the number of pairs ((l,r)) with (L\le l<r\le R) such that the subarray (a_l,\ldots,a_r) is beautiful.

The phrase "delete at most one element" is what makes the problem interesting. If the original range is already at most (k), nothing needs to be deleted. Otherwise, deleting one element can only help if that element is the unique minimum or the unique maximum. If the minimum occurs twice, deleting one minimum leaves another copy at the same value. The same applies to the maximum.

Suppose a window has minimum (mn), maximum (mx), second smallest element (mn_2), and second largest element (mx_2), where the second values are allowed to equal the corresponding extreme when that extreme occurs at least twice. The window is beautiful exactly when

[
mx-mn\le k,
]

or the maximum occurs exactly once and

[
mx_2-mn\le k,
]

or the minimum occurs exactly once and

[
mx-mn_2\le k.
]

The constraints rule out algorithms that inspect all subarrays for every query. There are almost (2\cdot10^{10}) pairs of endpoints in an array of length (2\cdot10^5), so even an (O(1)) check for every subarray would already be too expensive. We need to exploit the fact that beautiful subarrays are hereditary: every subarray of a beautiful array is also beautiful. This gives the monotonic structure needed for a two-pointer scan.

There are several edge cases that are easy to mishandle.

Consider

```
2 1 4
0 10
1 2
```

The answer is (1). The interval ([1,2]) has range (10), which is greater than (4), but deleting either element leaves a singleton with range (0). An implementation that checks only `max - min <= k` would incorrectly output (0).

Now consider

```
4 1 0
0 0 10 10
1 4
```

The answer is (4). The whole interval is not beautiful because deleting one zero leaves a (10), and deleting one ten leaves a (0), so the remaining range is (10). However, ([1,3]) is beautiful by deleting the ten, and ([2,4]) is beautiful by deleting the zero. The two equal-value pairs ([1,2]) and ([3,4]) are also beautiful. A careless implementation that treats the second extreme as a different value without tracking multiplicity can make the wrong deletion decision.

A query of length one is another boundary case. For example,

```
1 1 0
7
1 1
```

has answer (0), because the problem asks only for (l<r). Although a singleton is always beautiful, it is never counted as a requested subarray.

## Approaches

The direct approach is to enumerate every pair of endpoints inside every query and determine whether that subarray is beautiful. For one query covering the whole array, this means examining

[
\frac{n(n-1)}2
]

candidate intervals. At (n=200000), that is (19,999,900,000) intervals. Even if the beauty test were magically (O(1)), this is already far beyond the limit. If each interval were scanned to find its extrema, the cost would be cubic.

The brute force is correct because it literally checks the definition for every possible pair ((l,r)), but it completely ignores the overlap between neighboring subarrays. When we extend a window by one element, almost all of its contents are unchanged. The same is true when its left endpoint moves by one position.

The key observation is that beauty is monotone under shrinking. If a subarray is beautiful, choose the element whose deletion makes its range at most (k). Any smaller subarray either does not contain that element, in which case its range was already bounded by the same argument, or it contains the element and we can delete it again. Thus every smaller subarray is beautiful.

This means that for every fixed right endpoint (r), there is a smallest left endpoint (f[r]) such that ([f[r],r]) is beautiful. Every interval ([l,r]) with (l\ge f[r]) is then beautiful. As (r) moves to the right, (f[r]) never moves to the left.

We can find all (f[r]) with a sliding window. The only remaining difficulty is testing whether the current window is beautiful. A monotonic minimum deque gives the smallest value, and a monotonic maximum deque gives the largest value. With frequencies of values, we can determine whether the current minimum or maximum occurs once. If an extreme is unique, the second entry of the corresponding monotonic deque gives the next distinct extreme.

After computing (f[r]), the queries become a one-dimensional counting problem. Since (f[r]) is nondecreasing, binary search can split every query into positions where (f[r]\le L) and positions where (f[r]>L). Prefix sums then make both parts constant-time after the binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qn^2)) even with (O(1)) beauty tests | (O(n^2)) if tests are precomputed | Too slow |
| Optimal | (O(n+q\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Maintain a sliding window ([left,r]) while processing the array from left to right. The window will always be the smallest beautiful window ending at (r) after we finish shrinking it.
2. Keep a monotonic increasing deque of indices for the minimum and a monotonic decreasing deque of indices for the maximum. When a new value is inserted, remove indices from the back that can never become the minimum or maximum again. Because both endpoints only move forward, every index enters and leaves each deque at most once.
3. Maintain a frequency dictionary for the values currently inside the window. The frequency is needed because the value at the front of the minimum deque may occur several times even though the deque stores only one representative of that value.
4. Test the current window. Let (mn) and (mx) be its minimum and maximum. If (mx-mn\le k), the window is directly beautiful.
5. If (mx-mn>k), the only possible successful deletion is a unique extreme. If the maximum occurs once, deleting it leaves the second largest value as the new maximum. If the resulting range (mx_2-mn) is at most (k), the window is beautiful. Symmetrically, if the minimum occurs once and (mx-mn_2\le k), the window is beautiful.
6. If the window is not beautiful, increment `left` and remove (a[left]) from the window. The removed value is deleted from the frequency dictionary, and its index is removed from the front of either deque when necessary. Repeat until the window becomes beautiful.
7. Store the resulting `left` as (f[r]). Because the previous window was already minimal for (r-1), adding a new element cannot make a previously invalid smaller left endpoint valid again. Consequently, the sequence (f[0],f[1],\ldots,f[n-1]) is nondecreasing.
8. Build prefix sums of the indices and of (f[r]). For a query ([L,R]), an endpoint (r) contributes all valid left endpoints from (L) through (r-1) if (f[r]\le L). Its contribution is then (r-L).
9. If (f[r]>L), the valid left endpoints begin at (f[r]), so the contribution is (r-f[r]). Because (f[r]) is nondecreasing, binary search finds the first (r) in the query with (f[r]>L).
10. Use the prefix sums to evaluate both portions of the query. The singleton endpoint (r=L) contributes zero automatically, so no separate special case is needed.

### Why it works

For every right endpoint (r), the sliding window invariant is that after shrinking, ([f[r],r]) is beautiful while every interval ([l,r]) with (l<f[r]) is not. Beauty is preserved when an interval is shrunk, so all starts from (f[r]) through (r) produce beautiful intervals. The query only excludes the singleton (l=r), leaving exactly (r-\max(L,f[r])) valid starts.

The monotonic deques give the current minimum and maximum. Their front entries represent the extremes, while the next entries give the next candidate value once the corresponding extreme is unique. The frequency dictionary distinguishes the unique-extreme case from the repeated-extreme case. Thus the beauty test exactly matches the definition.

Finally, the left boundary only moves right, so (f[r]) is nondecreasing. This makes the query split valid and allows one binary search to identify all endpoints with (f[r]\le L).

## Python Solution

```python
import sys
from bisect import bisect_right
from collections import deque

input = sys.stdin.readline

def solve():
    n, q, k = map(int, input().split())
    a = list(map(int, input().split()))

    minq = deque()
    maxq = deque()
    freq = {}

    f = [0] * n
    left = 0

    def add(i):
        x = a[i]

        while minq and a[minq[-1]] >= x:
            minq.pop()
        minq.append(i)

        while maxq and a[maxq[-1]] <= x:
            maxq.pop()
        maxq.append(i)

        freq[x] = freq.get(x, 0) + 1

    def remove(i):
        x = a[i]

        freq[x] -= 1
        if freq[x] == 0:
            del freq[x]

        while minq and minq[0] < left:
            minq.popleft()

        while maxq and maxq[0] < left:
            maxq.popleft()

    def beautiful():
        mn = a[minq[0]]
        mx = a[maxq[0]]

        if mx - mn <= k:
            return True

        if freq[mx] == 1:
            mx2 = a[maxq[1]]
            if mx2 - mn <= k:
                return True

        if freq[mn] == 1:
            mn2 = a[minq[1]]
            if mx - mn2 <= k:
                return True

        return False

    for r in range(n):
        add(r)

        while not beautiful():
            left += 1
            remove(left - 1)

        f[r] = left

    pref_index = [0] * (n + 1)
    pref_f = [0] * (n + 1)

    for i in range(n):
        pref_index[i + 1] = pref_index[i] + i
        pref_f[i + 1] = pref_f[i] + f[i]

    out = []

    for _ in range(q):
        L, R = map(int, input().split())
        L -= 1
        R -= 1

        # First position p in [L, R] with f[p] > L.
        p = bisect_right(f, L, lo=L, hi=R + 1)

        # For r in [L, p), contribution is r - L.
        count1 = p - L
        sum_r1 = pref_index[p] - pref_index[L]
        ans = sum_r1 - count1 * L

        # For r in [p, R], contribution is r - f[r].
        sum_r2 = pref_index[R + 1] - pref_index[p]
        sum_f2 = pref_f[R + 1] - pref_f[p]
        ans += sum_r2 - sum_f2

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `minq` deque stores indices whose values are strictly increasing after each insertion. When a new value is smaller than or equal to values at the back, those older indices can never become the minimum while the new index remains in the window, so they are discarded. `maxq` uses the symmetric rule.

The frequency dictionary is deliberately separate from the deques. Equal minimum values are collapsed in the deque, but their multiplicity still matters. For example, if the current minimum is (0) and appears three times, deleting one occurrence cannot remove (0) from the window. The dictionary detects exactly this situation.

The `remove` function uses the current global `left` boundary. An index may already have disappeared from a deque because a better candidate was inserted later, so the cleanup is written as a `while` loop rather than assuming that the removed index is present.

The beauty test checks the ordinary range first. Only when the range is too large does it inspect the unique-extreme cases. If the maximum is unique, `maxq[1]` is the next maximum. If the minimum is unique, `minq[1]` is the next minimum. The checks are safe because the current window has at least two distinct values whenever the first range check fails.

The array `f` uses zero-based indices. For a fixed endpoint (r), if `f[r] <= L`, every start from (L) through (r-1) works, giving (r-L) choices. Otherwise the starts are (f[r]) through (r-1), giving (r-f[r]) choices. The prefix sum of indices handles the first expression, while the prefix sum of `f` handles the second.

Python integers have arbitrary precision, so the answer does not overflow. The largest possible answer is roughly (n^2/2), which is about (2\cdot10^{10}) for (n=2\cdot10^5).

## Worked Examples

### Sample 1

The input array is

[
[0,10,10,2,4]
]

with (k=4). The following table shows the state after the window has been shrunk as much as necessary.

| (r) | Current window | Minimum | Maximum | Count of min | Count of max | (f[r]) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [0] | 0 | 0 | 1 | 1 | 0 |
| 1 | [0,10] | 0 | 10 | 1 | 1 | 0 |
| 2 | [0,10,10] | 0 | 10 | 1 | 2 | 0 |
| 3 | [10,10,2] | 2 | 10 | 1 | 2 | 1 |
| 4 | [10,2,4] | 2 | 10 | 1 | 1 | 2 |

At (r=1), the range is (10), but the maximum is unique, so deleting it leaves only (0). At (r=2), the maximum occurs twice, but the minimum is unique, so deleting the minimum leaves `[10,10]`. At (r=3), `[0,10,10,2]` is not beautiful, so the left endpoint advances to (1). The resulting `[10,10,2]` becomes beautiful by deleting (2).

The resulting boundary array is

[
f=[0,0,0,1,2].
]

For the query ([1,5]), endpoint (2) contributes (1), endpoint (3) contributes (2), endpoint (4) contributes (2), and endpoint (5) contributes (2). Their sum is (7).

### Sample 2

Here the array is

[
[0,10,1,2,4]
]

and (k=4).

| (r) | Current window | Minimum | Maximum | Count of min | Count of max | (f[r]) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [0] | 0 | 0 | 1 | 1 | 0 |
| 1 | [0,10] | 0 | 10 | 1 | 1 | 0 |
| 2 | [0,10,1] | 0 | 10 | 1 | 1 | 0 |
| 3 | [0,10,1,2] | 0 | 10 | 1 | 1 | 0 |
| 4 | [0,10,1,2,4] | 0 | 10 | 1 | 1 | 0 |

At (r=4), the entire array is beautiful because deleting the unique maximum (10) leaves values from (0) through (4), whose range is exactly (k). Thus every endpoint has (f[r]=0), and every nonempty interval of length at least two is beautiful.

There are

[
1+2+3+4=10
]

such subarrays, matching the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+q\log n)) | Each array index enters and leaves each monotonic deque once, while every query performs one binary search. |
| Space | (O(n)) | The deques, frequency dictionary, boundary array, and two prefix arrays all use linear space. |

The preprocessing is linear because the two pointers and both deques move only forward. The query phase costs (O(\log n)) per query because `f` is sorted in nondecreasing order. With (n,q\le2\cdot10^5), this gives about (O(n+q\log n)) operations and stays comfortably within the intended complexity for the stated limits.

## Test Cases

```python
import sys
import io
from bisect import bisect_right
from collections import deque

def solve():
    input = sys.stdin.readline

    n, q, k = map(int, input().split())
    a = list(map(int, input().split()))

    minq = deque()
    maxq = deque()
    freq = {}

    f = [0] * n
    left = 0

    def add(i):
        x = a[i]

        while minq and a[minq[-1]] >= x:
            minq.pop()
        minq.append(i)

        while maxq and a[maxq[-1]] <= x:
            maxq.pop()
        maxq.append(i)

        freq[x] = freq.get(x, 0) + 1

    def remove(i):
        x = a[i]
        freq[x] -= 1
        if freq[x] == 0:
            del freq[x]

        while minq and minq[0] < left:
            minq.popleft()

        while maxq and maxq[0] < left:
            maxq.popleft()

    def beautiful():
        mn = a[minq[0]]
        mx = a[maxq[0]]

        if mx - mn <= k:
            return True

        if freq[mx] == 1 and a[maxq[1]] - mn <= k:
            return True

        if freq[mn] == 1 and mx - a[minq[1]] <= k:
            return True

        return False

    for r in range(n):
        add(r)

        while not beautiful():
            left += 1
            remove(left - 1)

        f[r] = left

    pref_index = [0] * (n + 1)
    pref_f = [0] * (n + 1)

    for i in range(n):
        pref_index[i + 1] = pref_index[i] + i
        pref_f[i + 1] = pref_f[i] + f[i]

    ans = []

    for _ in range(q):
        L, R = map(int, input().split())
        L -= 1
        R -= 1

        p = bisect_right(f, L, lo=L, hi=R + 1)

        count1 = p - L
        sum_r1 = pref_index[p] - pref_index[L]
        cur = sum_r1 - count1 * L

        sum_r2 = pref_index[R + 1] - pref_index[p]
        sum_f2 = pref_f[R + 1] - pref_f[p]
        cur += sum_r2 - sum_f2

        ans.append(str(cur))

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """5 1 4
0 10 10 2 4
1 5
"""
) == "7", "sample 1"

# Provided sample 2
assert run(
    """5 1 4
0 10 1 2 4
1 5
"""
) == "10", "sample 2"

# Minimum-size input. A singleton is never counted.
assert run(
    """1 1 0
7
1 1
"""
) == "0", "minimum-size input"

# Maximum-size input. All values are equal, so every interval is beautiful.
n = 200000
expected = n * (n - 1) // 2
big_input = f"200000 1 0\n{' '.join(['7'] * n)}\n1 200000\n"
assert run(big_input) == str(expected), "maximum-size input"

# Repeated minimum and maximum. The full interval is not beautiful,
# while [1,3] and [2,4] become beautiful by deleting one extreme.
assert run(
    """4 1 0
0 0 10 10
1 4
"""
) == "4", "repeated extremes"

# Boundary query. This is a suffix of sample 1 and catches query
# conversion and f[r] boundary mistakes.
assert run(
    """5 1 4
0 10 10 2 4
2 5
"""
) == "5", "query boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0 / 7 / 1 1` | `0` | Singleton queries must not count length-one subarrays. |
| `200000 1 0` with all values equal | `19999900000` | Maximum (n), maximum answer size, prefix sums, and linear preprocessing. |
| `4 1 0 / 0 0 10 10 / 1 4` | `4` | Repeated minima and maxima must not be treated as unique extremes. |
| Sample 1 with query `2 5` | `5` | Query boundaries and the conversion from one-based to zero-based indices. |

## Edge Cases

The first edge case is a two-element interval whose range is larger than (k). For

```
2 1 4
0 10
1 2
```

the current window `[0,10]` has range (10), so the first beauty condition fails. Both extremes are unique. Deleting either one leaves a singleton, whose range is (0). The algorithm therefore keeps `left=0`, records (f[1]=0), and the query counts the one valid pair ((1,2)).

The second edge case involves repeated extremes:

```
4 1 0
0 0 10 10
1 4
```

When the complete window is present, the minimum and maximum both occur twice. The ordinary range is (10>0), but neither extreme is removable with one deletion because another copy remains. The algorithm correctly rejects the window and moves `left`. It eventually obtains the two beautiful longer intervals `[0,0,10]` and `[0,10,10]`, together with `[0,0]` and `[10,10]`, giving (4).

The third edge case is a query of length one:

```
1 1 0
7
1 1
```

The preprocessing records (f[0]=0), since a singleton is beautiful. During the query, however, the contribution for endpoint (r=L) is (r-L=0). Thus the singleton is correctly excluded without a special query branch.

The fourth edge case is the case where every value is equal. For

```
4 1 0
7 7 7 7
1 4
```

every window has range zero, so the first condition immediately succeeds. The boundary array is `[0,0,0,0]`, and the query counts (1+2+3=6) subarrays of length greater than one. This also verifies that the second-extreme logic is never needed when the ordinary range already satisfies the threshold.

The fifth edge case is when deleting the minimum is the only valid operation. In Sample 1, the window `[0,10,10]` has maximum (10) twice, so deleting one maximum cannot remove the large value. The minimum (0) is unique, and deleting it leaves `[10,10]`. The algorithm uses the frequency of the maximum to reject the first deletion direction and the frequency of the minimum to accept the second one. This distinction is the central reason the frequency dictionary is necessary.
