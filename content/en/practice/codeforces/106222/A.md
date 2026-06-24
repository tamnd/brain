---
title: "CF 106222A - River"
description: "Each person lives at a position on the north bank and works at a position on the south bank. Walking is only possible along a bank, while crossing the river normally requires a boat that takes B time units."
date: "2026-06-25T06:57:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106222
codeforces_index: "A"
codeforces_contest_name: "ZCO 2025"
rating: 0
weight: 106222
solve_time_s: 62
verified: true
draft: false
---

[CF 106222A - River](https://codeforces.com/problemset/problem/106222/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

Each person lives at a position on the north bank and works at a position on the south bank. Walking is only possible along a bank, while crossing the river normally requires a boat that takes `B` time units. We may build a single bridge at some location `L`, and crossing that bridge takes exactly `1` time unit. A person will choose the bridge if the bridge route is at most `T` time units slower than their optimal boat route. We want to choose the bridge location and find the smallest tolerance value `T` such that at least `M` people use the bridge.

The constraints are the real challenge. There can be up to `10^5` people, while positions and boat time can be as large as `10^9`. Any solution that tries every bridge location is impossible because there are up to `10^9` candidate locations. We need something around `O(N log N)`.

A subtle point is that the optimal boat route is not necessarily to cross directly at the home position or workplace position. A person may walk first, then take the boat. Missing this observation leads to incorrect travel times.

Consider a person with `H = 2`, `W = 8`, `B = 5`.

The optimal boat route is:

```
walk from 2 to any position between 2 and 8
cross by boat
walk to 8
```

Its cost is `|2 - 8| + 5 = 11`, not `5`.

Another easy mistake is forgetting that the bridge location must be an integer. When inequalities involve division by two, rounding must be handled carefully.

For example:

```
H = 4, W = 4, B = 1
```

If `T = 0`, only a bridge built exactly at location `4` is acceptable. Treating locations as continuous would incorrectly allow nearby positions.

## Approaches

A brute force approach would try every bridge location `L` from `0` to `K - 1`. For each location we could compute how many people would use the bridge and then determine the required tolerance. Even if evaluating one location took only `O(N)`, the total complexity would be `O(NK)`, which is hopeless when `K` can reach `10^9`.

The key observation comes from expressing the extra cost of using the bridge.

Let

```
l = min(H, W)
r = max(H, W)
```

The optimal boat travel time is

```
|H - W| + B
```

because crossing anywhere between `H` and `W` minimizes the walking distance.

If the bridge is at location `L`, the bridge travel time is

```
|H - L| + 1 + |W - L|
```

The extra cost becomes

```
|H - L| + |W - L| - |H - W| + (1 - B)
```

The first three terms have a useful geometric meaning:

```
|H - L| + |W - L| - |H - W|
= 2 * distance(L, [l, r])
```

where `distance(L, [l, r])` is the distance from `L` to the interval `[l, r]`.

So a person uses the bridge iff

```
2 * distance(L, [l, r]) + (1 - B) <= T
```

Rearrange:

```
distance(L, [l, r]) <= (T + B - 1) / 2
```

Let

```
D = floor((T + B - 1) / 2)
```

Since distances are integers, the condition becomes

```
distance(L, [l, r]) <= D
```

That means this person accepts every bridge location inside

```
[l - D, r + D]
```

After clipping to `[0, K - 1]`.

For a fixed `D`, every person contributes one interval of acceptable bridge locations. We only need to know whether some location is covered by at least `M` intervals.

That is a standard maximum overlap problem. Using a sweep line with difference events gives an `O(N log N)` check.

The overlap count is monotonic in `D`, so we can binary search the smallest `D` that allows at least `M` people. After obtaining that `D`, we convert it back to the minimum tolerance `T`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NK) | O(1) | Too slow |
| Optimal | O(N log N log K) | O(N) | Accepted |

## Algorithm Walkthrough

1. For every person, compute the interval

```
[l, r] = [min(H, W), max(H, W)]
```
2. Binary search the smallest integer `D` such that there exists a bridge location covered by at least `M` expanded intervals.
3. During a check for a fixed `D`, expand every interval to

```
[max(0, l - D), min(K - 1, r + D)]
```

These are exactly the bridge locations acceptable to that person.
4. Convert the intervals into sweep events:

```
+1 at left endpoint
-1 at right endpoint + 1
```
5. Sort all event positions and scan from left to right, maintaining the current overlap count.
6. If the overlap ever reaches at least `M`, this `D` is feasible.
7. After binary search finds the minimum feasible `D`, recover the smallest tolerance value.

We need

```
floor((T + B - 1) / 2) >= D
```

The smallest nonnegative integer satisfying this is

```
T = max(0, 2 * D - (B - 1))
```

### Why it works

For a fixed person, the quantity

```
|H - L| + |W - L| - |H - W|
```

is exactly twice the distance from `L` to the interval between home and workplace. Expanding that interval by `D` on both sides produces precisely the set of bridge locations that satisfy the tolerance condition.

A bridge location is feasible if and only if it belongs to at least `M` of these expanded intervals. The sweep line computes the maximum number of intervals covering any location, so it correctly determines feasibility for a given `D`.

Because increasing `D` only enlarges intervals, feasibility is monotonic. Binary search therefore finds the minimum feasible `D`. The final formula converts that minimum `D` back into the minimum tolerance `T`, so the answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k, b = map(int, input().split())

    segs = []
    for _ in range(n):
        h, w = map(int, input().split())
        l = min(h, w)
        r = max(h, w)
        segs.append((l, r))

    def feasible(d):
        events = []

        for l, r in segs:
            left = max(0, l - d)
            right = min(k - 1, r + d)

            events.append((left, 1))
            events.append((right + 1, -1))

        events.sort()

        cur = 0
        i = 0
        while i < len(events):
            pos = events[i][0]

            delta = 0
            while i < len(events) and events[i][0] == pos:
                delta += events[i][1]
                i += 1

            cur += delta
            if cur >= m:
                return True

        return False

    lo = 0
    hi = k

    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    d = lo
    t = max(0, 2 * d - (b - 1))
    print(t)

solve()
```

The first part stores only the interval between each person's home and workplace. That interval is all we need later.

The feasibility check expands each interval by `D`, clips it to the valid bridge range, and performs a sweep line. Using `right + 1` for the removal event is the standard trick for inclusive intervals.

The binary search runs on `D`, not directly on `T`. The overlap structure depends only on `D`, which makes the check much cleaner.

All arithmetic uses Python integers, so values up to `10^9` and beyond are handled safely.

## Worked Examples

### Example 1

Input:

```
5 3 10 1
1 2
7 4
4 3
9 9
0 0
```

For `D = 1`:

| Person | Original Interval | Expanded Interval |
| --- | --- | --- |
| 1 | [1, 2] | [0, 3] |
| 2 | [4, 7] | [3, 8] |
| 3 | [3, 4] | [2, 5] |
| 4 | [9, 9] | [8, 9] |
| 5 | [0, 0] | [0, 1] |

At location `L = 3`, the first three intervals overlap.

| Location | Coverage |
| --- | --- |
| 3 | 3 |

So `D = 1` is feasible.

The answer is

```
T = max(0, 2 * 1 - (1 - 1))
  = 2
```

### Example 2

Input:

```
2 2 8 1
1 1
6 6
```

For `D = 2`:

| Person | Expanded Interval |
| --- | --- |
| 1 | [0, 3] |
| 2 | [4, 7] |

No overlap exists.

For `D = 3`:

| Person | Expanded Interval |
| --- | --- |
| 1 | [0, 4] |
| 2 | [3, 7] |

Locations `3` and `4` are covered by both intervals, so `D = 3` is feasible.

Then

```
T = 2 * 3 = 6
```

which matches the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N log K) | Binary search over `D`, each check performs a sweep on `2N` events |
| Space | O(N) | Event list and stored intervals |

With `N = 10^5` and `log K ≈ 30`, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    sys.stdin = input_data
    sys.stdout = output_data

    import sys
    input = sys.stdin.readline

    n, m, k, b = map(int, input().split())

    segs = []
    for _ in range(n):
        h, w = map(int, input().split())
        segs.append((min(h, w), max(h, w)))

    def feasible(d):
        events = []
        for l, r in segs:
            L = max(0, l - d)
            R = min(k - 1, r + d)
            events.append((L, 1))
            events.append((R + 1, -1))

        events.sort()

        cur = 0
        i = 0
        while i < len(events):
            pos = events[i][0]
            delta = 0
            while i < len(events) and events[i][0] == pos:
                delta += events[i][1]
                i += 1
            cur += delta
            if cur >= m:
                return True
        return False

    lo, hi = 0, k
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    ans = max(0, 2 * lo - (b - 1))
    print(ans)

    sys.stdout = sys.__stdout__
    return output_data.getvalue()

# provided samples
assert run("5 3 10 1\n1 2\n7 4\n4 3\n9 9\n0 0\n") == "2\n"
assert run("5 4 10 2\n1 2\n7 4\n4 3\n9 9\n0 0\n") == "3\n"
assert run("5 5 10 4\n1 2\n7 4\n4 3\n9 9\n0 0\n") == "7\n"
assert run("2 2 8 1\n1 1\n6 6\n") == "6\n"

# custom cases
assert run("1 1 5 10\n2 2\n") == "0\n"
assert run("3 2 10 1\n5 5\n5 5\n5 5\n") == "0\n"
assert run("2 2 10 1\n0 0\n9 9\n") == "10\n"
assert run("2 1 10 1\n0 9\n9 0\n") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single person, large boat time | 0 | Bridge already faster than boat |
| All intervals identical | 0 | Maximum overlap at one point |
| Opposite ends of the city | 10 | Large expansion requirement |
| Need only one user | 0 | Minimum `M` behavior |

## Edge Cases

Consider:

```
1 1 5 10
2 2
```

The bridge at location `2` takes time `1`, while the boat takes time `10`. The bridge is already better, so tolerance `0` is enough. The algorithm finds `D = 0`, then computes

```
T = max(0, -(B - 1)) = 0
```

which is correct.

Now consider:

```
2 2 8 1
1 1
6 6
```

The original intervals are disjoint. The algorithm expands both intervals during the binary search. The first feasible value is `D = 3`, where the expanded intervals become `[0,4]` and `[3,7]`. They overlap, so one bridge location can satisfy both people. The resulting tolerance is

```
T = 2 * 3 = 6
```

matching the expected answer.

Finally, consider the rounding-sensitive case:

```
1 1 10 1
4 4
```

For `T = 0`, we get

```
D = floor((0 + 1 - 1)/2) = 0
```

so the acceptable bridge interval remains `[4,4]`. Only location `4` works, exactly as required. The integer formulation avoids any mistakes caused by half-integer distances.
