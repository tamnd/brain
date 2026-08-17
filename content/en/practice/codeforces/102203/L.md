---
title: "CF 102203L - \u0412 \u043f\u043e\u0438\u0441\u043a\u0430\u0445 \u0438\u0441\u0442\u0438\u043d\u044b"
description: "We have an unknown array (s1,s2,ldots,sn). The array is strictly increasing up to some position and strictly decreasing afterwards, so it has a single peak. All values are distinct."
date: "2026-08-18T00:54:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "L"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 70
verified: true
draft: false
---

[CF 102203L - \u0412 \u043f\u043e\u0438\u0441\u043a\u0430\u0445 \u0438\u0441\u0442\u0438\u043d\u044b](https://codeforces.com/problemset/problem/102203/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an unknown array (s_1,s_2,\ldots,s_n). The array is strictly increasing up to some position and strictly decreasing afterwards, so it has a single peak. All values are distinct. We know (n) and a target value (k), and the interactive judge lets us ask for the value at any index (i). The task is to find an index whose value is exactly (k).

The array itself is not available to the program. Every array access is an interactive query, written as `? i`, and the judge answers with (s_i). Once the required index has been identified, the program prints `! i` and terminates.

The bound (n\le 2\cdot10^5) immediately rules out scanning the array. Even though an ordinary (O(n)) algorithm would be small enough in many non-interactive problems, here every array access is an expensive query and there are only 80 queries available. We need logarithmic behavior. Since (\log_2(2\cdot10^5)<18), even several binary searches fit comfortably inside the query limit.

The values themselves are between 0 and (10^9), so ordinary Python integers are more than sufficient. The target is guaranteed to occur, so after correctly identifying the increasing and decreasing portions, one of the two binary searches must find it.

There are several boundary cases that can break a careless implementation. Consider `n = 2`, with values `[5, 3]` and `k = 3`. The peak is at the first position, so the decreasing part contains the answer at index 2. An implementation that assumes the peak is always an interior element can lose this case and never search the second position correctly.

Another case is `[1, 5, 3]` with `k = 1`. The answer is the first element, which lies exactly at the left boundary of the increasing part. A binary search that initializes its lower bound incorrectly can discard it.

Similarly, `[1, 5, 3]` with `k = 3` tests the right boundary of the decreasing part. The answer is index 3, so the decreasing binary search must allow its final endpoint.

The request to test an "all-equal" array cannot be satisfied literally because the original problem guarantees that all (s_i) are distinct. An array such as `[5, 5, 5]` is not a legal input. The closest meaningful test is a strictly monotone array, where the peak is at one of the endpoints, such as `[1, 2, 3, 4]` or `[4, 3, 2, 1]`.

## Approaches

The direct approach is to query positions from 1 through (n) until the value (k) is found. It is correct because every position is eventually inspected, and the answer is guaranteed to exist. Its problem is the query budget. In the worst case it needs (n) queries, which can be as many as (200,000), while the judge allows only 80. The issue is not merely running time, but exceeding the interactive protocol limit.

The structure of the array gives us much more information than an arbitrary array would. On the increasing part, if (s_i<k), the target can only be to the right. If (s_i>k), it can only be to the left. On the decreasing part, the directions are reversed. Thus, once we know where the peak is, the problem becomes two ordinary binary searches.

We can also find the peak with binary search. Suppose we query the middle position (m) and compare (s_m) with (s_{m+1}). If (s_m<s_{m+1}), we are still on the increasing side, so the peak is strictly to the right of (m). If (s_m>s_{m+1}), we are already on the decreasing side, so the peak is at (m) or somewhere to its left.

This gives a logarithmic search for the peak. After that, we binary-search the increasing segment and the decreasing segment. The total number of queries is at most roughly (3\log_2 n), well below 80 for (n\le2\cdot10^5).

The brute-force approach works because every position is explicitly checked, but fails because every check consumes one of only 80 queries. The mountain-shaped ordering lets us replace those individual checks with binary decisions, reducing the search from (O(n)) queries to (O(\log n)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n)) queries | (O(1)) | Too slow |
| Find peak + two binary searches | (O(\log n)) queries | (O(\log n)) cached values, or (O(1)) auxiliary space | Accepted |

## Algorithm Walkthrough

1. Read (n) and (k). We do not know any array values yet, so every value that the algorithm needs must be obtained through an interactive query.
2. Define a query function that prints `? i`, flushes the output immediately, reads the judge's answer, and returns it. Flushing is mandatory because otherwise the judge may wait for a query that is still sitting in Python's output buffer.
3. Find the peak with binary search. Maintain a range `[lo, hi]` that is guaranteed to contain a peak. While `lo < hi`, take `mid = (lo + hi) // 2` and query `s[mid]` and `s[mid + 1]`.
4. If `s[mid] < s[mid + 1]`, the sequence is still increasing at `mid`, so the peak must lie strictly to the right. Set `lo = mid + 1`.
5. Otherwise, `s[mid] > s[mid + 1]`, because all values are distinct. The sequence has already started decreasing, so a peak is at `mid` or to the left. Set `hi = mid`.
6. When `lo == hi`, that index is the peak. The array is now split into an increasing segment `[1, peak]` and a decreasing segment `[peak + 1, n]`.
7. Binary-search `[1, peak]` as an increasing array. At position `mid`, if its value is smaller than `k`, move right. If it is larger than `k`, move left. If it equals `k`, output that index immediately.
8. If the first search fails, binary-search `[peak + 1, n]` as a decreasing array. Here the comparison directions are reversed. If `s[mid] > k`, move right because values get smaller toward the right. If `s[mid] < k`, move left.
9. When the target is found, print `! index` and terminate. The guarantee that (k) occurs means the second search will eventually find it if the first one did not.

### Why it works

The peak-search invariant is that the current interval always contains a maximum element. If `s[mid] < s[mid+1]`, the maximum cannot be at or before `mid`, because the sequence is still rising there, so moving to `[mid+1, hi]` preserves the invariant. If `s[mid] > s[mid+1]`, the sequence has begun falling by `mid+1`, so a maximum occurs at `mid` or earlier, preserving the invariant with `[lo, mid]`.

After the peak is known, every index on its left belongs to a strictly increasing sequence and every index on its right belongs to a strictly decreasing sequence. The corresponding binary search keeps exactly those indices where (k) can still occur. Since the target is guaranteed to exist, one of these searches reaches its index.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    cache = {}

    def ask(i):
        if i not in cache:
            print("?", i, flush=True)
            value = int(input())
            if value == -1:
                sys.exit(0)
            cache[i] = value
        return cache[i]

    # Find the peak.
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        left = ask(mid)
        right = ask(mid + 1)

        if left < right:
            lo = mid + 1
        else:
            hi = mid

    peak = lo

    # Binary search on the increasing part [1, peak].
    lo, hi = 1, peak
    while lo <= hi:
        mid = (lo + hi) // 2
        value = ask(mid)

        if value == k:
            print("!", mid, flush=True)
            return
        if value < k:
            lo = mid + 1
        else:
            hi = mid - 1

    # Binary search on the decreasing part [peak + 1, n].
    lo, hi = peak + 1, n
    while lo <= hi:
        mid = (lo + hi) // 2
        value = ask(mid)

        if value == k:
            print("!", mid, flush=True)
            return
        if value > k:
            lo = mid + 1
        else:
            hi = mid - 1

if __name__ == "__main__":
    solve()
```

The `ask` function is the only place that communicates with the judge. The cache is useful because peak detection may query a position that a later binary search needs again. Reusing the answer avoids spending another interactive query on the same index.

The peak search uses `lo = mid + 1` when `s[mid] < s[mid + 1]`, because `mid` itself cannot be the peak in that situation. In the other branch, `mid` remains a possible peak, so the correct update is `hi = mid`, not `mid - 1`.

The increasing binary search uses the usual comparison rules. The decreasing search reverses the direction because moving right makes the values smaller.

Python does not have an integer overflow issue here, and `(lo + hi) // 2` is safe for the given bounds. The crucial implementation detail is `flush=True` on every query and on the final answer. Without flushing, an otherwise correct interactive algorithm can fail because the judge never receives the request.

The `-1` handling is a conventional defensive measure for interactive judges that use a negative response to signal an invalid query or protocol failure. The original statement does not require using such a response for valid execution, but terminating when it appears prevents the program from continuing with meaningless input.

The code is intended for the original interactive judge. A normal batch runner cannot execute it directly because the judge is responsible for answering `? i`.

## Worked Examples

The statement contains one interactive sample. The hidden array in that sample is `[1, 3, 10, 8, 2]`, with `n = 5` and `k = 3`. The following trace describes the decisions made by the algorithm. Because the original sample lists a particular sequence of queries rather than forcing one unique strategy, the exact queries produced by this implementation can differ while the final answer remains the same.

| Stage | Range | Query | Values | Decision |
| --- | --- | --- | --- | --- |
| Peak search | `[1, 5]` | `3, 4` | `10, 8` | Peak is in `[1, 3]` |
| Peak search | `[1, 3]` | `2, 3` | `3, 10` | Peak is in `[3, 3]` |
| Increasing search | `[1, 3]` | `2` | `3` | Found target |
| Answer |  |  |  | `! 2` |

The peak is position 3 because the sequence rises from 1 to 3 to 10 and then falls to 8 and 2. Once the increasing side is searched, position 2 immediately contains the requested value.

For a second example, consider the hidden array `[2, 6, 11, 9, 4, 1]` with `k = 4`. The target is on the decreasing side, which exercises the part of the algorithm that is easiest to reverse accidentally.

| Stage | Range | Query | Values | Decision |
| --- | --- | --- | --- | --- |
| Peak search | `[1, 6]` | `3, 4` | `11, 9` | Peak is in `[1, 3]` |
| Peak search | `[1, 3]` | `2, 3` | `6, 11` | Peak is in `[3, 3]` |
| Increasing search | `[1, 3]` | `2` | `6` | Target is left of 2 |
| Increasing search | `[1, 1]` | `1` | `2` | Increasing side fails |
| Decreasing search | `[4, 6]` | `5` | `4` | Found target |
| Answer |  |  |  | `! 5` |

At the decreasing search's first query, the value is already equal to the target. If the array were searched using the increasing-array comparison rules instead, the search direction could be reversed and the answer lost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log n)) queries | Peak detection and the two binary searches each require logarithmically many queries |
| Space | (O(\log n)) | The cache stores queried indices, and at most a logarithmic number of distinct positions is needed |

For (n\le2\cdot10^5), (\log_2 n) is below 18. The peak search takes fewer than 18 iterations, and each iteration asks for at most two positions. Each of the two target searches takes fewer than 18 iterations. Thus the total is comfortably below the limit of 80 queries. The memory usage is tiny compared with the 256 MB limit.

## Test Cases

Since the original task is interactive, the usual `run(input) -> output` unit-test pattern cannot be applied directly. A test harness must simulate the judge by supplying values for requested indices. The following tests use a batch version of the same algorithm, where the hidden array is explicitly available to the test code. This also makes the assertions deterministic.

```python
import io
import sys

def find_target(a, k):
    n = len(a)
    queries = 0

    def ask(i):
        nonlocal queries
        queries += 1
        return a[i - 1]

    lo, hi = 1, n

    while lo < hi:
        mid = (lo + hi) // 2
        left = ask(mid)
        right = ask(mid + 1)

        if left < right:
            lo = mid + 1
        else:
            hi = mid

    peak = lo

    lo, hi = 1, peak
    while lo <= hi:
        mid = (lo + hi) // 2
        value = ask(mid)

        if value == k:
            return mid, queries
        if value < k:
            lo = mid + 1
        else:
            hi = mid - 1

    lo, hi = peak + 1, n
    while lo <= hi:
        mid = (lo + hi) // 2
        value = ask(mid)

        if value == k:
            return mid, queries
        if value > k:
            lo = mid + 1
        else:
            hi = mid - 1

    raise AssertionError("Target is guaranteed to exist")

# Provided sample.
assert find_target([1, 3, 10, 8, 2], 3)[0] == 2

# Minimum-size input, peak at the first position.
assert find_target([5, 3], 3)[0] == 2

# Minimum-size input, peak at the second position.
assert find_target([3, 5], 3)[0] == 1

# Target is exactly the peak.
assert find_target([1, 4, 9, 7, 2], 9)[0] == 3

# Target is at the right boundary.
assert find_target([1, 5, 8, 6, 3], 3)[0] == 5

# Strictly increasing array, peak at the right boundary.
assert find_target([1, 2, 3, 4, 5], 1)[0] == 1

# Strictly decreasing array, peak at the left boundary.
assert find_target([5, 4, 3, 2, 1], 1)[0] == 5

# Large legal instance.
a = list(range(100000))
a += list(range(100000, 0, -1))
expected = 150000
assert find_target(a, a[expected - 1])[0] == expected
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1, 3, 10, 8, 2], k=3` | `2` | Provided sample |
| `[5, 3], k=3` | `2` | Minimum size, peak at left boundary |
| `[3, 5], k=3` | `1` | Minimum size, peak at right boundary |
| `[1, 4, 9, 7, 2], k=9` | `3` | Target equals the peak |
| `[1, 5, 8, 6, 3], k=3` | `5` | Target at the final position |
| `[1,2,3,4,5], k=1` | `1` | Entire array is increasing |
| `[5,4,3,2,1], k=1` | `5` | Entire array is decreasing |
| Large mountain array | `150000` | Large input and logarithmic behavior |

The "all-equal values" case requested in the test specification is deliberately absent. Such an array violates the original condition that every (s_i) is distinct. Replacing it with strictly monotone arrays tests the corresponding boundary behavior without testing an impossible state.

## Edge Cases

For a peak at the first position, consider `n = 2`, `k = 3`, and the hidden array `[5, 3]`. During peak detection, comparing positions 1 and 2 gives `5 > 3`, so the peak range becomes `[1, 1]`. The increasing search checks position 1 and fails because its value is 5. The decreasing search then checks position 2 and finds 3, producing `! 2`. The case works because the peak interval is allowed to collapse directly to the left endpoint.

For a peak at the last position, consider `[3, 5]` with `k = 3`. The comparison `3 < 5` moves the peak search to position 2. The increasing search covers both positions and finds the target at position 1. No decreasing segment needs to contain any elements. This validates the use of `[peak + 1, n]` for the second search rather than forcing an invalid range.

For a target equal to the peak, consider `[1, 4, 9, 7, 2]` with `k = 9`. Peak detection identifies position 3. The increasing binary search includes the peak itself, queries position 3, and immediately returns it. Excluding the peak from the first binary search would be an unnecessary and potentially incorrect boundary change.

For a target at the rightmost position, consider `[1, 5, 8, 6, 3]` with `k = 3`. The peak is position 3, so the decreasing search covers `[4, 5]`. Querying position 5 returns 3. The search must use `hi = n` inclusively, otherwise a target at the final index would be silently discarded.

For a completely increasing array such as `[1, 2, 3, 4, 5]`, the peak is position 5. Every comparison during peak detection finds `s[mid] < s[mid+1]`, so the lower bound moves right until it reaches 5. The first binary search then covers the entire array. This is legal because the definition allows the turning point to be (n).

For a completely decreasing array such as `[5, 4, 3, 2, 1]`, the peak is position 1. Every peak comparison finds `s[mid] > s[mid+1]`, so the upper bound moves left until it reaches 1. The increasing part contains only position 1, and the decreasing search handles positions 2 through 5. This is the symmetric boundary case.

Finally, duplicate values must not be handled as though they were possible. For example, `[1, 4, 4, 2]` would make the comparison between positions 2 and 3 equal, but such an array is forbidden by the problem. The peak search relies on the fact that every comparison is strictly either increasing or decreasing. Adding an equality branch to the implementation would solve a different problem and is unnecessary here.
