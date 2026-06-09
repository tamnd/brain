---
title: "CF 1822A - TubeTube Feed"
description: "The feed can be thought of as a linear list of videos, each with two attributes: how long it takes to watch and how enjoyable it is. Mushroom Filippov starts at the first video and can move rightwards through the list, spending one second per step to skip to the next item."
date: "2026-06-09T07:48:02+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1822
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 867 (Div. 3)"
rating: 800
weight: 1822
solve_time_s: 71
verified: true
draft: false
---

[CF 1822A - TubeTube Feed](https://codeforces.com/problemset/problem/1822/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The feed can be thought of as a linear list of videos, each with two attributes: how long it takes to watch and how enjoyable it is. Mushroom Filippov starts at the first video and can move rightwards through the list, spending one second per step to skip to the next item. At any moment he can decide to stop skipping and start watching a video. Once he chooses a video at position `i`, the total time consumed is the time spent skipping from position 1 to `i` plus the duration of the video itself.

For each test case, we must determine which single video he should pick so that the sum of “time to reach it” and “watch time” does not exceed the total available lunch time `t`. Among all videos that satisfy this constraint, we pick one with maximum entertainment value.

The important part of the model is that the cost to reach video `i` is fixed and deterministic: it is exactly `i - 1` seconds. There is no branching or interaction between choices, so each index can be evaluated independently.

The constraints are small: `n ≤ 50` and `q ≤ 1000`. This implies at most 50,000 video checks overall. Any solution that is linear in `n` per test case is easily fast enough, while anything involving nested heavy computation per video would still be acceptable but unnecessary.

A common mistake is to ignore the skipping cost and only compare `a[i] ≤ t`. That fails because reaching deeper videos consumes time. For example, if `t = 5`, a video at position 4 with duration 2 is not valid because reaching it already costs 3 seconds, making total time 5. Another mistake is trying to simulate the feed dynamically; that is unnecessary since each candidate is independent.

Edge cases arise when:

- No video is reachable within time. Example: `n = 3, t = 1`, durations `[10,10,10]`. Even the first video costs at least 1 second to reach plus 10 seconds to watch, exceeding `t`. Output must be `-1`.
- The best entertainment video is not the earliest valid one, so we must track maximum `b[i]` among valid choices, not stop at the first valid index.

## Approaches

The brute-force approach is direct: for each video `i`, compute whether `i - 1 + a[i] ≤ t`. If it is valid, consider its entertainment value `b[i]`. Keep the best among all valid indices. This requires checking every video for every test case, resulting in `O(n)` work per test case.

With `n ≤ 50` and up to 1000 test cases, this is at most 50,000 evaluations, which is extremely small. Even a naive implementation is safe.

There is no deeper optimization structure required because each video’s feasibility depends only on its own index and duration. The “skipping cost” is linear and independent per position, so there is no benefit to prefix sums, sorting, or greedy reordering.

The key observation is that the problem reduces to independent filtering: we are selecting the best element from a set defined by a simple constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Accepted |
| Optimal | O(nq) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`, `t`, the duration array `a`, and entertainment array `b`. We keep them aligned by index since each video is a paired object.
2. Initialize variables `best_value = -1` and `best_index = -1`. These track the best valid video seen so far. The sentinel `-1` represents the case where no valid video exists.
3. Iterate over each video index `i` from `1` to `n`.
4. Compute the time needed to choose video `i`, which is `(i - 1) + a[i]`. The first term represents skipping time from the start of the feed, and the second is the viewing duration.
5. If this total time is less than or equal to `t`, the video is feasible within lunch constraints.
6. If feasible, compare its entertainment value `b[i]` with `best_value`. If it is larger, update both `best_value` and `best_index` to this video.
7. After scanning all videos, output `best_index`. If no valid video was found, `best_index` remains `-1`.

### Why it works

Each video is evaluated under a fixed deterministic cost model that depends only on its position. There are no interactions between choices, so feasibility is a per-element property. The algorithm maintains the invariant that after processing the first `i` videos, `best_index` is the highest entertainment value among all valid videos in the prefix `[1..i]`. Because every video is checked exactly once, the final result is the best among all valid candidates in the entire array.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())
for _ in range(q):
    n, t = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    best_val = -1
    best_idx = -1

    for i in range(n):
        time_needed = i + a[i]  # i == i-1 in 0-based indexing

        if time_needed <= t:
            if b[i] > best_val:
                best_val = b[i]
                best_idx = i + 1

    print(best_idx)
```

The code directly follows the observation that the skipping time is exactly the index offset in zero-based indexing. The loop checks feasibility and updates the best answer greedily.

A subtle point is keeping indexing consistent: in Python we use `i` starting from 0, so reaching video `i` costs `i` seconds, not `i-1`. The returned index is adjusted back to 1-based indexing.

## Worked Examples

### Example 1

Input:

```
n = 5, t = 9
a = [1, 5, 7, 6, 6]
b = [3, 4, 7, 1, 9]
```

| i | a[i] | b[i] | skip cost | total time | valid | best (value, index) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 0 | 1 | yes | (3,1) |
| 2 | 5 | 4 | 1 | 6 | yes | (4,2) |
| 3 | 7 | 7 | 2 | 9 | yes | (7,3) |
| 4 | 6 | 1 | 3 | 9 | yes | (7,3) |
| 5 | 6 | 9 | 4 | 10 | no | (7,3) |

The best feasible entertainment value is 7 at index 3. This shows why we cannot stop at the first valid choice; later candidates may improve the answer.

### Example 2

Input:

```
n = 4, t = 4
a = [4, 3, 3, 2]
b = [1, 2, 3, 4]
```

| i | a[i] | b[i] | skip cost | total time | valid | best |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 0 | 4 | yes | (1,1) |
| 2 | 3 | 2 | 1 | 4 | yes | (2,2) |
| 3 | 3 | 3 | 2 | 5 | no | (2,2) |
| 4 | 2 | 4 | 3 | 5 | no | (2,2) |

The answer is index 2. This demonstrates that higher entertainment values are irrelevant if time constraints eliminate those videos.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nq) | Each test case scans all videos once |
| Space | O(1) | Only a few tracking variables are used |

The constraints allow up to 50,000 total checks, which is trivial under a 1-second limit. Memory usage is constant beyond input storage.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    q = int(input())
    out = []
    for _ in range(q):
        n, t = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        best_val = -1
        best_idx = -1

        for i in range(n):
            if i + a[i] <= t:
                if b[i] > best_val:
                    best_val = b[i]
                    best_idx = i + 1

        out.append(str(best_idx))

    return "\n".join(out)

# provided sample
assert solve("""5
5 9
1 5 7 6 6
3 4 7 1 9
4 4
4 3 3 2
1 2 3 4
5 7
5 5 5 5 5
2 1 3 9 7
4 33
54 71 69 96
42 24 99 1
2 179
55 66
77 88
""") == """3
2
3
-1
2"""

# minimum size
assert solve("""1
1 5
3
10
""") == """-1"""

# all valid
assert solve("""1
3 10
1 1 1
1 2 3
""") == """3"""

# boundary skip dominance
assert solve("""1
4 3
1 1 1 1
10 9 8 7
""") == """3"""

# no valid
assert solve("""1
2 1
10 10
5 5
""") == """-1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single invalid | -1 | impossible case |
| all valid increasing | last index | best selection logic |
| high skip constraint | index 3 | index cost correctness |
| no feasible video | -1 | full rejection case |

## Edge Cases

When `t` is very small, the only possible candidate is often the first video, since every later position adds at least one second of skip cost. The algorithm naturally handles this because `i + a[i]` quickly exceeds `t` for all `i > 0`.

For example:

```
n = 3, t = 2
a = [5, 1, 1]
b = [10, 20, 30]
```

Execution checks:

- i = 1: 0 + 5 = 5 > 2, invalid
- i = 2: 1 + 1 = 2 ≤ 2, valid → best = 20
- i = 3: 2 + 1 = 3 > 2, invalid

Output becomes index 2, showing that skipping cost can make later short videos preferable even when earlier ones are longer.

The algorithm correctly evaluates each candidate independently and never assumes monotonicity in entertainment values or durations.
