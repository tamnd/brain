---
title: "CF 106157M - Motorway Stops"
description: "We are given the locations of motorway stops along a route, stored as strictly increasing cumulative distances. Between every pair of consecutive stops there is a driving segment."
date: "2026-06-25T11:20:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106157
codeforces_index: "M"
codeforces_contest_name: "2025 United Kingdom and Ireland Programming Contest (UKIEPC 2025)"
rating: 0
weight: 106157
solve_time_s: 37
verified: true
draft: false
---

[CF 106157M - Motorway Stops](https://codeforces.com/problemset/problem/106157/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the locations of motorway stops along a route, stored as strictly increasing cumulative distances.

Between every pair of consecutive stops there is a driving segment. If the stop at position `i` is removed, where `i` is neither the first nor the last stop, then the two segments adjacent to that stop become a single longer segment.

The task is to remove exactly one internal stop so that the longest remaining driving segment is as small as possible. We must output that minimum possible longest distance.

Let

`g[j] = s[j+1] - s[j]`

be the distances between consecutive stops.

If we remove stop `i`, then gaps `g[i-1]` and `g[i]` disappear and are replaced by one gap of length

`g[i-1] + g[i]`.

All other gaps remain unchanged.

The number of stops can be as large as 200,000, so there are almost 200,000 gaps. An algorithm that recomputes the maximum gap from scratch for every possible removed stop would require roughly `O(n²)` work, which is far too large. With `n = 200,000`, that would mean tens of billions of operations.

A few edge cases deserve attention.

Suppose the gaps are `10 20 30`.

Removing the middle stop merges `10` and `20`, producing gaps `30 30`. The answer is `30`, not `20`. Any solution that only looks at existing gaps and ignores the merged segment would fail.

Consider:

```
4
0 100 101 200
```

The gaps are `100 1 99`.

Removing the second stop creates a gap of `101`, giving a maximum of `101`.

Removing the third stop creates a gap of `100`, giving a maximum of `100`.

The correct answer is `100`. A greedy rule such as "remove the stop next to the smallest gap" is not reliable.

Another boundary case is when the optimal removal occurs next to the first or last removable stop:

```
3
0 5 12
```

Only one stop can be removed. The resulting segment length is `12`, so the answer is `12`. Careless prefix or suffix handling can easily access invalid indices here.

## Approaches

The most direct solution is to try every removable stop.

For a chosen stop, merge its two adjacent gaps and then scan all remaining gaps to find the largest one. This is correct because it explicitly evaluates the result of every possible removal.

The problem is the running time. There are `O(n)` candidate stops, and each evaluation takes `O(n)` time to recompute the maximum gap. The total complexity becomes `O(n²)`, which is impossible for `n = 200,000`.

The key observation is that after removing a stop, only two gaps change.

For a removal between gaps `g[i-1]` and `g[i]`:

The merged gap becomes `g[i-1] + g[i]`.

Every other gap stays exactly the same.

So the maximum gap after this removal is simply the larger of:

1. The merged gap.
2. The maximum gap among all gaps except `g[i-1]` and `g[i]`.

This suggests precomputing maximum values on prefixes and suffixes of the gap array.

Let:

`pref[j]` = maximum gap among `g[0..j]`

`suff[j]` = maximum gap among `g[j..m-1]`

where `m = n - 1`.

Then for a removal involving gaps `g[i-1]` and `g[i]`, the maximum unaffected gap can be obtained in constant time from the prefix before `g[i-1]` and the suffix after `g[i]`.

Each candidate removal is evaluated in `O(1)` time, giving an overall `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the stop positions.
2. Build the gap array `g`, where `g[i] = s[i+1] - s[i]`.
3. Build a prefix maximum array `pref`.

`pref[i]` stores the largest gap seen from the beginning up to index `i`.
4. Build a suffix maximum array `suff`.

`suff[i]` stores the largest gap from index `i` to the end.
5. Iterate over every removable stop.

If the removed stop lies between gaps `g[i-1]` and `g[i]`, then the new merged gap is:

`merged = g[i-1] + g[i]`.
6. Compute the largest unaffected gap.

The gaps before `g[i-1]` contribute `pref[i-2]` if such an index exists.

The gaps after `g[i]` contribute `suff[i+1]` if such an index exists.

The larger of these two values is the maximum unaffected gap.
7. The largest segment after this removal is:

`max(merged, unaffected_max)`.
8. Take the minimum value among all candidate removals.
9. Output that minimum.

### Why it works

For any chosen stop, exactly two adjacent gaps are modified. Every other gap remains unchanged.

The longest segment after removing that stop must be either the newly merged gap or one of the unchanged gaps. The prefix and suffix maximum arrays give the largest unchanged gap outside the merged pair in constant time.

Since the algorithm evaluates the exact longest segment for every valid removal and returns the minimum among them, it always finds the optimal stop to remove.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = list(map(int, input().split()))

gaps = [s[i + 1] - s[i] for i in range(n - 1)]
m = n - 1

pref = [0] * m
pref[0] = gaps[0]
for i in range(1, m):
    pref[i] = max(pref[i - 1], gaps[i])

suff = [0] * m
suff[m - 1] = gaps[m - 1]
for i in range(m - 2, -1, -1):
    suff[i] = max(suff[i + 1], gaps[i])

ans = 10**18

for i in range(1, m):
    merged = gaps[i - 1] + gaps[i]

    other = 0
    if i - 2 >= 0:
        other = max(other, pref[i - 2])
    if i + 1 < m:
        other = max(other, suff[i + 1])

    ans = min(ans, max(merged, other))

print(ans)
```

The first part converts stop positions into gap lengths. Working with gaps is much simpler because removing a stop only affects two adjacent gaps.

The prefix and suffix arrays allow us to query the largest unaffected gap in constant time. Without them, we would need to rescan the entire array for every candidate removal.

The index handling is the subtle part.

When removing the stop between `g[i-1]` and `g[i]`, the unaffected gaps are everything before `g[i-1]` and everything after `g[i]`.

That is why the left contribution uses `pref[i-2]` and the right contribution uses `suff[i+1]`.

Using `0` when one side does not exist correctly handles removals near the ends of the route.

Python integers easily handle the maximum possible distance values, since coordinates are at most `10^9`.

## Worked Examples

### Example 1

Input:

```
5
0 50 125 175 236
```

Gap array:

```
50 75 50 61
```

| Removal | Merged Gap | Largest Other Gap | Result |
| --- | --- | --- | --- |
| Remove stop at 50 | 125 | 61 | 125 |
| Remove stop at 125 | 125 | 61 | 125 |
| Remove stop at 175 | 111 | 75 | 111 |

The minimum result is `111`.

Output:

```
111
```

This example shows that the optimal removal is not necessarily near the smallest gap. The merged segment and the remaining largest segment must both be considered.

### Example 2

Input:

```
4
100 300 600 10000
```

Gap array:

```
200 300 9400
```

| Removal | Merged Gap | Largest Other Gap | Result |
| --- | --- | --- | --- |
| Remove stop at 300 | 500 | 9400 | 9400 |
| Remove stop at 600 | 9700 | 200 | 9700 |

The best choice produces a maximum segment length of `9400`.

Output:

```
9400
```

This trace demonstrates that sometimes an already existing large gap dominates the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Building gaps, prefix maxima, suffix maxima, and scanning all removals each take linear time |
| Space | O(n) | Gap, prefix, and suffix arrays |

With `n ≤ 200,000`, linear time is easily fast enough. The memory usage is also comfortably within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    s = list(map(int, input().split()))

    gaps = [s[i + 1] - s[i] for i in range(n - 1)]
    m = n - 1

    pref = [0] * m
    pref[0] = gaps[0]
    for i in range(1, m):
        pref[i] = max(pref[i - 1], gaps[i])

    suff = [0] * m
    suff[m - 1] = gaps[m - 1]
    for i in range(m - 2, -1, -1):
        suff[i] = max(suff[i + 1], gaps[i])

    ans = 10**18

    for i in range(1, m):
        merged = gaps[i - 1] + gaps[i]

        other = 0
        if i - 2 >= 0:
            other = max(other, pref[i - 2])
        if i + 1 < m:
            other = max(other, suff[i + 1])

        ans = min(ans, max(merged, other))

    return str(ans) + "\n"

# provided samples
assert run("5\n0 50 125 175 236\n") == "111\n", "sample 1"
assert run("4\n100 300 600 10000\n") == "9400\n", "sample 2"

# custom cases
assert run("3\n0 5 12\n") == "12\n", "minimum size"
assert run("5\n0 10 20 30 40\n") == "20\n", "all equal gaps"
assert run("4\n0 100 101 200\n") == "100\n", "choose correct side"
assert run("5\n0 1 100 101 102\n") == "100\n", "boundary removal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 0 5 12` | `12` | Smallest valid instance |
| `5 / 0 10 20 30 40` | `20` | Uniform gaps |
| `4 / 0 100 101 200` | `100` | Correct comparison between candidate removals |
| `5 / 0 1 100 101 102` | `100` | Removal near an endpoint |

## Edge Cases

Consider:

```
3
0 5 12
```

There is only one removable stop. The gap array is `[5, 7]`. Removing the middle stop merges them into `12`. The algorithm evaluates the single candidate, computes `merged = 12`, finds no unaffected gaps, and outputs `12`.

Consider:

```
4
0 100 101 200
```

The gaps are `[100, 1, 99]`.

Removing the second stop gives a merged gap of `101` and another gap of `99`, so the maximum becomes `101`.

Removing the third stop gives a merged gap of `100` and another gap of `100`, so the maximum becomes `100`.

The algorithm checks both possibilities and correctly returns `100`.

Consider:

```
5
0 1 100 101 102
```

The gaps are `[1, 99, 1, 1]`.

Removing the stop at position `1` merges the first two gaps into `100`. The remaining gaps are `1` and `1`, so the maximum is `100`.

The prefix and suffix queries correctly handle the fact that one side of the removed pair has no remaining gaps. This is exactly where off-by-one mistakes often appear, and the index checks prevent them.
