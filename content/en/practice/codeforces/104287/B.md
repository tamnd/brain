---
title: "CF 104287B - Mountain Climbing Easy"
description: "We are given a sequence of altitudes along a path, and we walk through it from left to right. The task is to count how many “mountain climbs” appear in this sequence."
date: "2026-07-01T20:44:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104287
codeforces_index: "B"
codeforces_contest_name: "Teamscode Spring 2023 Contest"
rating: 0
weight: 104287
solve_time_s: 68
verified: true
draft: false
---

[CF 104287B - Mountain Climbing Easy](https://codeforces.com/problemset/problem/104287/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of altitudes along a path, and we walk through it from left to right. The task is to count how many “mountain climbs” appear in this sequence.

A mountain climb is any contiguous segment of at least three consecutive points where the heights strictly increase at every step. Once a strictly increasing segment starts, it continues as long as each next value is larger than the previous one. If the increase continues for more than three points, it is still counted as a single mountain, not multiple overlapping ones. The key idea is that we are counting maximal strictly increasing runs whose length is at least three.

The input size is at most 1000, which is small enough that an O(N²) solution would still pass comfortably. However, since the structure is linear and local, we should expect an O(N) scan to be sufficient.

A few edge cases matter here. A single increasing step is not enough to form a mountain. For example, in `[1, 2]`, nothing is counted because the run length is only 2, even though it is increasing.

If a sequence increases and then stops increasing, we must only count it once if it is long enough. For example, `[1, 2, 3, 4, 2]` contains exactly one mountain, not multiple overlapping ones like `[1,2,3]` and `[2,3,4]`.

Flat values break a mountain. For example, `[1, 2, 2, 3, 4]` resets the increasing run at the plateau, so we cannot treat it as a single continuous climb.

## Approaches

A straightforward way to think about the problem is to examine every possible starting index and extend it forward while the sequence is strictly increasing. Each time we reach a point where the increase stops, we check whether the segment length is at least 3 and count it if so.

This brute-force method works because every mountain is a maximal strictly increasing subarray, so scanning from each position and expanding ensures we do not miss any candidate. However, it is wasteful: for each starting position, we may scan forward up to O(N) elements, leading to O(N²) operations in the worst case, such as a fully increasing array.

The key observation is that we do not need to restart scanning at every index. Instead, we only need to track contiguous strictly increasing runs. Each run can be processed once: when we detect that the sequence stops increasing, we finalize the run length and decide whether it forms a mountain.

This turns the problem into a single pass where we maintain the length of the current increasing streak and reset it whenever the streak breaks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Single Pass Tracking | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We scan the array from left to right while maintaining the length of the current strictly increasing segment.

1. Start with a counter `cnt = 1` representing the current increasing run length.

This works because a single element is trivially a run of length one.
2. For each index `i` from 1 to N−1, compare `a[i]` with `a[i−1]`.

If `a[i] > a[i−1]`, extend the current run by increasing `cnt` by one.

This preserves the property that `cnt` always represents the length of the current strictly increasing suffix.
3. If `a[i] <= a[i−1]`, the increasing property breaks. Before resetting, check if the run we just ended had length at least 3. If so, increment the answer.

Then reset `cnt = 1` because the new run starts at position `i`.
4. After finishing the loop, we must perform a final check on the last run, since the array may end while still increasing. If `cnt >= 3`, count it as a mountain.

Why it works comes from the fact that every strictly increasing segment is processed exactly once at its boundary. The algorithm never splits a valid mountain because it only finalizes a segment when the increasing property is broken. Each maximal increasing run is uniquely identified, and its length fully determines whether it is counted. No overlapping or partial segment is ever double-counted because we never restart inside a valid increasing streak.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

ans = 0
cnt = 1

for i in range(1, n):
    if a[i] > a[i - 1]:
        cnt += 1
    else:
        if cnt >= 3:
            ans += 1
        cnt = 1

if cnt >= 3:
    ans += 1

print(ans)
```

The solution keeps a single running counter for the current increasing streak. Each time the order breaks, we decide whether the streak qualifies as a mountain. The final check after the loop ensures the last segment is not missed.

The only subtlety is correctly handling resets: `cnt` must always reset to 1, not 0, because the current element starts a new potential segment. Forgetting the final check is another common mistake, since the last run never triggers a break condition.

## Worked Examples

### Example 1

Input:

```
11
1 2 3 2 4 4 1 4 5 7 3
```

We track runs:

| i | a[i] | prev | increasing? | cnt | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | - | start | 1 | 0 |
| 1 | 2 | 1 | yes | 2 | 0 |
| 2 | 3 | 2 | yes | 3 | 0 |
| 3 | 2 | 3 | no | 1 | 1 |
| 4 | 4 | 2 | yes | 2 | 1 |
| 5 | 4 | 4 | no | 1 | 1 |
| 6 | 1 | 4 | no | 1 | 1 |
| 7 | 4 | 1 | yes | 2 | 1 |
| 8 | 5 | 4 | yes | 3 | 1 |
| 9 | 7 | 5 | yes | 4 | 1 |
| 10 | 3 | 7 | no | 1 | 2 |

At the end, the last run `[1,4,5,7]` is length 4 and is counted. The final answer is 2, corresponding to `[1,2,3]` and `[1,4,5,7]`.

### Example 2

Input:

```
6
5 4 3 2 1 2
```

| i | a[i] | prev | increasing? | cnt | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | - | start | 1 | 0 |
| 1 | 4 | 5 | no | 1 | 0 |
| 2 | 3 | 4 | no | 1 | 0 |
| 3 | 2 | 3 | no | 1 | 0 |
| 4 | 1 | 2 | no | 1 | 0 |
| 5 | 2 | 1 | yes | 2 | 0 |

No segment ever reaches length 3, so the answer is 0.

This confirms that only maximal strictly increasing runs of sufficient length are counted, and short fluctuations do not contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is processed once in a single pass |
| Space | O(1) | Only a few counters are maintained |

The constraints allow up to 1000 elements, but the linear scan is already optimal and leaves ample margin. Even under much larger constraints, the same approach remains valid due to its single-pass structure.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    ans = 0
    cnt = 1

    for i in range(1, n):
        if a[i] > a[i - 1]:
            cnt += 1
        else:
            if cnt >= 3:
                ans += 1
            cnt = 1

    if cnt >= 3:
        ans += 1

    return str(ans)

# provided sample
assert run("11\n1 2 3 2 4 4 1 4 5 7 3\n") == "2"

# minimum increasing mountain
assert run("3\n1 2 3\n") == "1"

# no mountain due to plateau
assert run("5\n1 2 2 3 4\n") == "1"

# all decreasing
assert run("4\n4 3 2 1\n") == "0"

# multiple separate mountains
assert run("7\n1 2 3 1 2 3 4\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 | 1 | minimum valid mountain |
| 1 2 2 3 4 | 1 | plateau breaks continuity |
| 4 3 2 1 | 0 | no increasing segment |
| 1 2 3 1 2 3 4 | 2 | multiple independent runs |

## Edge Cases

One important edge case is when the array ends during an increasing streak. For example, in `[1, 2, 3]`, there is no “break” to trigger counting inside the loop. The algorithm handles this by performing a final check after iteration. The run length is 3, so it is correctly counted as one mountain.

Another case is alternating increases and decreases such as `[1, 3, 2, 4, 3, 5]`. The algorithm resets at every decrease and counts only segments that reach length 3. Each segment is isolated cleanly, and no partial overlap occurs because `cnt` is reset immediately when monotonicity fails.

A plateau like `[1, 2, 2, 3]` is handled correctly because the `<=` condition breaks the run at equality. The segment `[1, 2]` is discarded since its length is below 3, and a new run starts at `2 -> 3`, which is also too short.
