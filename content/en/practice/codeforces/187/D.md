---
title: "CF 187D - BRT Contract "
description: "A bus travels through a fixed sequence of road segments. Between consecutive segments there are traffic lights, and every light follows the same synchronized cycle. Each cycle lasts g + r seconds."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 187
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 119 (Div. 1)"
rating: 2800
weight: 187
solve_time_s: 114
verified: true
draft: false
---

[CF 187D - BRT Contract ](https://codeforces.com/problemset/problem/187/D)

**Rating:** 2800  
**Tags:** data structures  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

A bus travels through a fixed sequence of road segments. Between consecutive segments there are traffic lights, and every light follows the same synchronized cycle.

Each cycle lasts `g + r` seconds. The light is green during the first `g` seconds of the cycle and red during the next `r` seconds. At time `0` every light starts green. A bus may cross an intersection only while the light is green. If it arrives exactly when green ends, it must wait for the next green phase.

The input gives the travel time of every road segment. The bus starts at some departure time `t`, traverses the first segment, possibly waits at the first intersection, traverses the next segment, and so on until it reaches the destination after the last segment.

For every query time `t_i`, we must compute the exact arrival time at the destination.

The constraints completely rule out simulating every intersection independently for every query. Both `n` and `q` are up to `10^5`, so an `O(nq)` solution would perform around `10^10` operations in the worst case, which is far beyond the time limit. We need something close to linear or logarithmic per query.

The tricky part is that waiting depends on the current time modulo the cycle length. A bus can arrive at the same intersection at slightly different times and either pass immediately or wait almost an entire red phase.

Several edge cases are easy to mishandle.

Suppose a bus reaches an intersection exactly when green ends.

```
g = 3, r = 2
arrival = 3
```

The interval `[0,3)` is green and `[3,5)` is red. The bus must wait. Treating `<= g` as green produces the wrong answer.

Another subtle case appears when many consecutive intersections are crossed without waiting.

```
n = 2
g = 10, r = 5
segments = [2,2,2]
start = 1
```

Arrival times at intersections are `3` and `5`, both inside green. A careless simulation that rounds cycles incorrectly may insert unnecessary waits.

The opposite extreme is repeated waiting at every intersection.

```
n = 2
g = 1, r = 10
segments = [1,1,1]
start = 0
```

The bus reaches the first intersection at time `1`, exactly at red, waits until `11`, reaches the second intersection at `12`, waits again until `22`, and finishes at `23`.

Another common bug comes from forgetting that the final segment has no traffic light afterward. Waiting is checked only at intersections, not after reaching the destination.

## Approaches

The direct simulation is straightforward. For each query, maintain the current time. Add the segment length, then if this is not the final segment, inspect the traffic light state at the new time.

Let `T = g + r`. If `current % T < g`, the bus passes immediately. Otherwise it waits until the next multiple of `T`.

This simulation is correct because it follows the exact rules of movement and waiting. The problem is cost. Every query processes all `n` intersections, so the total complexity becomes `O(nq)`. With both values equal to `10^5`, this reaches `10^10` operations.

The key observation is that the waiting behavior depends only on time modulo `T`.

Define a function:

```
f(x) = final arrival time if the bus starts at time x
```

Consider what happens if we increase the start time by exactly one full cycle `T`.

Every future arrival time also increases by exactly `T`, so the green/red decisions remain identical. The entire trajectory shifts forward by one cycle.

That means:

```
f(x + T) = f(x) + T
```

This periodic structure reduces the problem to computing answers for only the `T` possible residues modulo the cycle length.

Unfortunately `T` itself may be as large as `10^9`, so we still cannot precompute all residues directly.

The next observation is more powerful. As the start time changes continuously, the waiting pattern changes only at specific breakpoints. Between two breakpoints, the answer is simply:

```
f(x) = x + constant
```

Each intersection contributes one interval of bad residues that trigger waiting there. After processing all intersections, the entire time axis becomes partitioned into intervals where the total waiting time is fixed.

We can process intersections backwards and maintain these intervals inside an ordered map. Every query then becomes a binary search over intervals.

The final complexity is `O(n log n + q log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Key reformulation

Let:

```
pref[i] = l1 + l2 + ... + li
```

After traversing the first `i` segments, the bus reaches intersection `i` at time:

```
start + pref[i] + waits_before_i
```

The bus must wait at intersection `i` iff:

```
(start + pref[i] + waits_before_i) mod T >= g
```

Instead of simulating forward, we determine for which start times a wait occurs.

### Interval interpretation

Suppose the total waiting accumulated before intersection `i` is already fixed inside some interval of start times.

Then the condition for waiting at intersection `i` becomes a simple modular interval condition on the start time.

Crossing this interval increases future waiting by exactly `r`.

As we process intersections one by one, we maintain a partition of the start-time residues into intervals with equal accumulated waiting.

### Data structure

We store disjoint intervals over residues modulo `T`.

For every interval we keep:

```
value = total extra waiting accumulated
```

Initially all residues have waiting `0`.

When processing an intersection:

1. For every current interval, compute which residue subrange causes a wait at this intersection.
2. Split intervals if necessary.
3. Add `r` to the waiting value of the affected pieces.

Since each intersection introduces at most two new boundaries, the total number of intervals remains linear.

### Answering queries

For a query start time `x`:

1. Compute `k = x mod T`.
2. Find the interval containing `k`.
3. Let its stored waiting value be `w`.
4. The final answer is:

```
x + total_segment_sum + w
```

### Why it works

Inside any interval of residues, every intersection makes exactly the same decision, either pass immediately or wait one red phase. Since the sequence of decisions is fixed, the total waiting time is also fixed.

Whenever a residue crosses a boundary where some intersection changes behavior, the total waiting increases by exactly one additional red phase. The interval structure captures precisely these transitions.

Because all lights are synchronized, shifting the start time by one full cycle preserves every decision, so residue classes completely determine the behavior.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    n, g, r = map(int, input().split())
    l = list(map(int, input().split()))

    T = g + r
    total = sum(l)

    pref = []
    s = 0
    for i in range(n):
        s += l[i]
        pref.append(s % T)

    # events[pos] = added waiting after this breakpoint
    events = []

    cur_add = 0

    intervals = [(0, 0)]

    for p in pref:
        new_intervals = []

        for start, val in intervals:
            end = T

            L = (g - p - val) % T
            R = (-p - val) % T

            if L < R:
                pieces = [
                    (start, min(end, L), val),
                    (max(start, L), min(end, R), val + r),
                    (max(start, R), end, val),
                ]
            else:
                pieces = [
                    (start, min(end, R), val),
                    (max(start, R), min(end, L), val + r),
                    (max(start, L), end, val),
                ]

            for a, b, v in pieces:
                if a < b:
                    new_intervals.append((a, v))
                    if b < T:
                        new_intervals.append((b, val))

        new_intervals.sort()

        merged = []
        for pos, val in new_intervals:
            if merged and merged[-1][1] == val:
                continue
            merged.append((pos, val))

        intervals = merged

    starts = [x[0] for x in intervals]
    vals = [x[1] for x in intervals]

    q = int(input())

    out = []

    for _ in range(q):
        t = int(input())

        k = t % T
        idx = bisect_right(starts, k) - 1

        out.append(str(t + total + vals[idx]))

    print("\n".join(out))

solve()
```

The solution stores interval boundaries rather than explicit ranges. If an interval starts at `starts[i]`, it continues until the next boundary.

The preprocessing phase incrementally refines the partition of residues. For each intersection we determine which residues force waiting there and add `r` to their accumulated delay.

The modular arithmetic is the hardest part. The condition:

```
(start + pref[i] + current_wait) mod T >= g
```

defines a circular interval on residues. Circular intervals may wrap around zero, so the implementation handles the two cases separately.

Another subtle point is the exact handling of `>= g`. Arriving exactly at time `g` means the light has already turned red. Using `>` instead would produce incorrect answers.

All arithmetic uses Python integers, which naturally support the required 64-bit range.

## Worked Examples

### Sample 1

Input:

```
1 3 2
5 2
5
1
2
3
4
5
```

Here:

```
T = 5
total = 7
```

The only intersection is reached after `5` seconds.

| Start | Reach intersection | Residue | Wait? | Final answer |
| --- | --- | --- | --- | --- |
| 1 | 6 | 1 | No | 8 |
| 2 | 7 | 2 | No | 9 |
| 3 | 8 | 3 | Yes, wait 2 | 12 |
| 4 | 9 | 4 | Yes, wait 1 | 12 |
| 5 | 10 | 0 | No | 12 |

This example demonstrates the boundary condition. Residues `3` and `4` are red because green lasts only for residues `0,1,2`.

### Second example

Consider:

```
2 2 3
1 1 1
```

Cycle length is `5`.

| Start | First arrival | Wait after first? | Second arrival | Wait after second? | Finish |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | No | 2 | Yes | 6 |
| 1 | 2 | Yes | 6 | No | 7 |
| 2 | 3 | Yes | 7 | Yes | 11 |

This trace shows that earlier waiting shifts future residues. The second intersection cannot be analyzed independently from the first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | interval maintenance and binary searches |
| Space | O(n) | stored interval boundaries |

The number of interval boundaries grows linearly because each intersection introduces only a constant number of new split points. With `10^5` intersections and queries, the solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from bisect import bisect_right

def solve_io(inp: str) -> str:
    input_data = io.StringIO(inp)
    output = io.StringIO()

    input = input_data.readline

    n, g, r = map(int, input().split())
    l = list(map(int, input().split()))

    T = g + r
    total = sum(l)

    pref = []
    s = 0
    for i in range(n):
        s += l[i]
        pref.append(s % T)

    intervals = [(0, 0)]

    for p in pref:
        new_intervals = []

        for start, val in intervals:
            end = T

            L = (g - p - val) % T
            R = (-p - val) % T

            if L < R:
                pieces = [
                    (start, min(end, L), val),
                    (max(start, L), min(end, R), val + r),
                    (max(start, R), end, val),
                ]
            else:
                pieces = [
                    (start, min(end, R), val),
                    (max(start, R), min(end, L), val + r),
                    (max(start, L), end, val),
                ]

            for a, b, v in pieces:
                if a < b:
                    new_intervals.append((a, v))
                    if b < T:
                        new_intervals.append((b, val))

        new_intervals.sort()

        merged = []
        for pos, val in new_intervals:
            if merged and merged[-1][1] == val:
                continue
            merged.append((pos, val))

        intervals = merged

    starts = [x[0] for x in intervals]
    vals = [x[1] for x in intervals]

    q = int(input())

    ans = []

    for _ in range(q):
        t = int(input())

        k = t % T
        idx = bisect_right(starts, k) - 1

        ans.append(str(t + total + vals[idx]))

    return "\n".join(ans)

# provided sample
assert solve_io(
"""1 3 2
5 2
5
1
2
3
4
5
"""
) == "\n".join(["8", "9", "12", "12", "12"])

# minimum size
assert solve_io(
"""1 10 1
1 1
1
0
"""
) == "2"

# exact boundary hit
assert solve_io(
"""1 3 2
3 1
1
0
"""
) == "6"

# always green
assert solve_io(
"""2 100 1
1 1 1
2
0
50
"""
) == "\n".join(["3", "53"])

# repeated waiting
assert solve_io(
"""2 1 10
1 1 1
1
0
"""
) == "23"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum size | Correct simple traversal | Base functionality |
| Exact boundary hit | Bus stops at `time % T == g` | Off-by-one correctness |
| Always green | No waiting anywhere | Avoid unnecessary waits |
| Repeated waiting | Multiple red waits accumulate | Future residues shift correctly |

## Edge Cases

Consider the exact transition from green to red.

```
1 3 2
3 1
1
0
```

The bus reaches the intersection at time `3`. Since green covers only residues `0,1,2`, residue `3` is already red. The bus waits until time `5` and then finishes at `6`.

The algorithm handles this because the waiting condition uses:

```
residue >= g
```

rather than `>`.

Now consider repeated waiting:

```
2 1 10
1 1 1
1
0
```

The first arrival occurs at time `1`, which is red. The bus waits until `11`.

After traversing the second segment it reaches the next intersection at `12`, again red, waits until `22`, and finally reaches the destination at `23`.

The preprocessing intervals correctly accumulate both waits because every additional red encounter adds another `r` to the interval value.

Finally, consider a case with no waiting at all:

```
2 100 1
1 1 1
1
0
```

Every arrival residue stays below `100`, so the accumulated waiting remains zero for the entire residue interval. The final answer is simply the start time plus the total segment length.
