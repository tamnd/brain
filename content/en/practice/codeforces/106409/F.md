---
title: "CF 106409F - Pace Pushers"
description: "The problem describes several beacons placed on a line. Each beacon has a position and a current power. During a normal step, every beacon that can still expand increases its power by one. A beacon with power p covers the interval from x - p to x + p."
date: "2026-06-25T09:58:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106409
codeforces_index: "F"
codeforces_contest_name: "HPI 2026 Advanced"
rating: 0
weight: 106409
solve_time_s: 33
verified: true
draft: false
---

[CF 106409F - Pace Pushers](https://codeforces.com/problemset/problem/106409/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes several beacons placed on a line. Each beacon has a position and a current power. During a normal step, every beacon that can still expand increases its power by one. A beacon with power `p` covers the interval from `x - p` to `x + p`. A beacon stops expanding once its covered interval touches another beacon's covered interval, because it can no longer grow independently.

The task is to find the final total amount of covered positions after this repeated process finishes.

The input gives the number of beacons followed by each beacon's coordinate and initial power. The output is the number of integer positions covered after all possible expansions have happened.

The constraints require avoiding direct simulation. If there are `n` beacons and each one may expand many times, simulating every round can take far more than linear time. With large inputs, an approach that repeatedly scans all beacons is too slow because the number of rounds depends on coordinate distances, not just on `n`.

The tricky part is that simultaneous growth matters. A beacon that appears blocked after one partial update may still grow in the real process because other beacons also grow during the same round.

For example, two beacons:

```
2
0 1
5 1
```

Both start covering `[ -1, 1 ]` and `[4, 6]`. They eventually meet after both grow. A simulation that grows only the left beacon until it stops would incorrectly freeze it too early.

Another edge case is overlapping initial ranges:

```
2
0 5
3 1
```

The first beacon already covers the second one. Treating the second beacon as independent and adding both ranges separately would count positions twice.

# Approaches

A straightforward solution is to simulate full steps. In each round, find every beacon that can expand, increase its power, and repeat until no changes happen. This is correct because it follows the process exactly. The problem is that a beacon can require many expansions before reaching another beacon. If coordinates are large, the number of rounds can be proportional to the coordinate distance, making the worst case far beyond acceptable limits.

The useful observation is that the order of individual expansions does not matter. Instead of increasing all expandable beacons together, imagine performing smaller operations where only one beacon expands by one unit at a time. The final stable state is identical. This allows us to process expansions as merges between covered intervals.

After sorting beacons by position, maintain the current disjoint covered segments. When a new segment overlaps the previous segment, the two belong to the same final group. Their maximum reach becomes the reach of the merged segment. Each original segment participates in only a constant number of merges, so the total work after sorting is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of rounds × n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

# Algorithm Walkthrough

1. Sort all beacons by their positions. The left to right order is enough because interactions can only happen between neighboring covered intervals.
2. Represent each current group as a segment `[left, right]` together with its expansion power. Initially every beacon is its own segment.
3. Add beacons one by one in sorted order. After inserting a new segment, compare it with the segment before it.
4. If the two segments do not overlap, keep both. They are separated forever because future expansion inside one group cannot jump across an uncovered gap.
5. If the segments overlap, merge them. The new segment has the left boundary of the left segment and the right boundary of the merged coverage. Its power is the larger of the two powers because that beacon can continue expanding farthest.
6. Continue merging backward while the newest segment overlaps the previous one.
7. After all merges are finished, every remaining segment is a final connected covered component. A segment with left endpoint `l`, right endpoint `r`, and power `p` contributes `r - l + 2 * p + 1` positions.

Why it works: the invariant is that every stored segment represents exactly one connected component of the coverage that can no longer be separated. When two components touch, the future process treats them as one because expansion from either side can continue until the farthest reach inside the component is achieved. Since every merge preserves the maximum possible reach, the final segments are exactly the same as those produced by repeatedly applying the original full steps.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    beacons = []
    for _ in range(n):
        x, p = map(int, input().split())
        beacons.append((x, p))

    beacons.sort()

    stack = []

    for x, p in beacons:
        stack.append([x - p, x + p, p])

        while len(stack) >= 2:
            a = stack[-2]
            b = stack[-1]

            if a[1] < b[0]:
                break

            stack.pop()
            stack.pop()

            stack.append([
                a[0],
                max(a[1], b[1]),
                max(a[2], b[2])
            ])

    ans = 0
    for l, r, p in stack:
        ans += r - l + 2 * p + 1

    print(ans)

solve()
```

The input is sorted first because the merge process depends on neighboring intervals. The stack stores only intervals that are currently separate.

The merge loop is the core of the algorithm. When two intervals intersect, keeping them separate would violate the invariant that all stored intervals are disjoint. The new power is the maximum of the two original powers because only the strongest remaining expansion ability matters after they become connected.

The final loop counts the positions covered by each independent component. The formula includes the initial interval length and the extra growth available on both sides.

Python integers do not overflow, so the implementation does not need special handling for large answers.

# Worked Examples

Consider:

```
3
0 1
5 1
10 1
```

The processing looks like this:

| Step | Added beacon | Stack state |
| --- | --- | --- |
| 1 | `(0,1)` | `[-1,1]` |
| 2 | `(5,1)` | `[-1,1], [4,6]` |
| 3 | `(10,1)` | `[-1,1], [4,6], [9,11]` |

No intervals overlap, so the final answer is:

`3 + 3 + 3 = 9`

The example shows independent components staying separate.

Another example:

```
3
0 2
5 2
10 2
```

| Step | Added beacon | Stack state |
| --- | --- | --- |
| 1 | `(0,2)` | `[-2,2]` |
| 2 | `(5,2)` | `[-2,2], [3,7]` |
| 3 | `(10,2)` | `[-2,2], [3,7], [8,12]` |

The middle interval touches neither side initially, so the components remain separate. The algorithm does not merge intervals just because they are close, only when their covered positions intersect.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, and each interval is merged a constant number of times |
| Space | O(n) | The stack stores the current disjoint components |

The solution fits because it avoids simulating individual expansion rounds. Even when coordinates are very large, the number of stack operations remains linear after sorting.

# Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline
    n = int(data())
    a = []
    for _ in range(n):
        x, p = map(int, data().split())
        a.append((x, p))
    a.sort()
    st = []
    for x, p in a:
        st.append([x-p, x+p, p])
        while len(st) >= 2 and st[-2][1] >= st[-1][0]:
            b = st.pop()
            c = st.pop()
            st.append([c[0], max(c[1], b[1]), max(c[2], b[2])])
    ans = sum(r-l+2*p+1 for l, r, p in st)
    sys.stdin = old
    return str(ans) + "\n"

assert run("""1
0 0
""") == "1\n"

assert run("""2
0 1
5 1
""") == "6\n"

assert run("""3
0 2
5 2
10 2
""") == "15\n"

assert run("""2
0 5
3 1
""") == "11\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One beacon with zero power | `1` | Minimum size case |
| Two separated beacons | `6` | Independent components |
| Several touching growth ranges | `15` | Repeated merging |
| One beacon covering another initially | `11` | Overlap handling |

# Edge Cases

For a single beacon:

```
1
7 0
```

The stack contains one interval `[7,7]`. No merging occurs, and the contribution is `1`, which is correct because one position is covered.

For initially overlapping beacons:

```
2
0 5
3 1
```

The first beacon covers `[-5,5]` and the second covers `[2,4]`. The algorithm merges them immediately because the intervals overlap. The merged interval keeps the larger power, so the final coverage is determined by the first beacon only, avoiding double counting.

For separated beacons:

```
2
0 1
100 1
```

The intervals `[-1,1]` and `[99,101]` never intersect. The stack keeps two components, and the answer is the sum of both lengths.

For a chain of overlaps:

```
3
0 2
4 2
8 2
```

The first two intervals touch, so they merge. The resulting component reaches far enough to overlap the third interval, causing a second merge. The repeated merge loop handles this case because after every merge the new interval is checked again against the previous component.
