---
title: "CF 22D - Segments"
description: "We are given several closed intervals on the number line. A nail placed at an integer coordinate covers every segment that contains that coordinate, including endpoints."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 22
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 22 (Div. 2 Only)"
rating: 1900
weight: 22
solve_time_s: 85
verified: true
draft: false
---
[CF 22D - Segments](https://codeforces.com/problemset/problem/22/D)

**Rating:** 1900  
**Tags:** greedy, sortings  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several closed intervals on the number line. A nail placed at an integer coordinate covers every segment that contains that coordinate, including endpoints. The task is to choose as few nail positions as possible so that every segment contains at least one chosen point.

Another way to think about the problem is this: we want the minimum set of integer points such that every interval intersects the set.

The constraints are small enough that many approaches could pass. There are at most 1000 segments, and coordinates are bounded by 10000 in absolute value. A quadratic solution would already be acceptable, since $10^6$ operations is tiny for a 1 second limit. Even $O(n^3)$ would likely survive in practice. Still, the structure of the problem admits a classic greedy solution with $O(n \log n)$ complexity.

One subtle point is that intervals are closed. If one segment ends at position 2 and another begins at position 2, then a single nail at 2 covers both.

Consider this example:

```
2
0 2
2 5
```

The correct answer is one nail at position 2. A careless implementation that treats intervals as open or forgets to include endpoints would incorrectly use two nails.

Another edge case is degenerate intervals, where both endpoints are equal.

```
3
1 1
1 3
5 5
```

The optimal answer uses nails at 1 and 5. A solution that assumes intervals always have positive length may accidentally skip point segments.

There is also the possibility that the input endpoints are not ordered.

```
2
5 1
2 4
```

The first segment really means $[1,5]$. Forgetting to normalize endpoints can completely break sorting and coverage checks.

Overlapping chains are another source of mistakes.

```
4
1 4
2 5
3 6
7 8
```

All first three intervals can be covered with one nail, but not necessarily at the left endpoint of the first interval. Choosing greedily from the wrong side may produce too many nails.

## Approaches

A brute-force mindset starts with the observation that coordinates are small. Since every useful nail position must lie somewhere on the integer line between $-10000$ and $10000$, we could try every coordinate and repeatedly choose positions that cover many uncovered intervals.

The problem is that this becomes a set cover style search if we want the true minimum. Exhaustively testing subsets of coordinates is exponential and quickly impossible. Even restricting ourselves to interval endpoints still leaves up to 2000 candidate positions, and $2^{2000}$ is hopeless.

A more practical brute-force approach is dynamic programming on coordinates. For each integer point, we could track which intervals are already covered. But representing interval subsets requires $2^n$ states, which again explodes even for $n=1000$.

The reason the problem becomes much easier is the structure of intervals on a line. Intervals have a natural ordering, and once we commit to a nail position, every interval ending before that point is permanently handled. This allows a greedy strategy.

The key insight is this: when we decide to place a nail, placing it as far right as possible is always optimal. Suppose we look at the segment with the smallest right endpoint. Any valid solution must place some nail inside this segment. If we place the nail exactly at the segment's right endpoint, we maximize the chance that this same nail also covers future intervals.

That observation leads directly to the classic interval stabbing greedy algorithm:

1. Sort segments by right endpoint.
2. Take the first uncovered segment.
3. Place a nail at its right endpoint.
4. Remove every segment containing that point.
5. Repeat.

The greedy choice is safe because any solution needs a nail inside the current earliest-ending segment. Moving that nail to the segment's right endpoint cannot reduce coverage of future intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all segments and normalize each one so that $l \le r$.

This prevents incorrect comparisons when endpoints are given in reverse order.
2. Sort the segments by increasing right endpoint.

The segment that finishes earliest is the most restrictive one. If we delay handling it, we risk missing the chance to cover it together with later segments.
3. Initialize an empty list of nail positions.
4. Iterate through the sorted segments from left to right.
5. For the current segment $[l,r]$, check whether the most recently placed nail already lies inside it.

Since segments are processed by increasing right endpoint, only the latest nail matters. Earlier nails are even farther left.
6. If the current segment is already covered, continue to the next segment.
7. Otherwise, place a new nail at position $r$, the segment's right endpoint.

This is the greedy step. Choosing the farthest possible valid point gives maximum overlap with future segments.
8. Add this nail to the answer list.
9. After processing all segments, output the number of nails and their coordinates.

### Why it works

The invariant is that after processing the first $k$ sorted intervals, the algorithm has used the minimum possible number of nails to cover them.

Take the first uncovered interval in sorted order, call it $[l,r]$. Any valid solution must place some nail inside this interval. Suppose an optimal solution uses a nail at position $x$, where $l \le x \le r$. Replacing that nail with a nail at $r$ cannot hurt future coverage, because every future interval ends no earlier than $r$. Any interval containing $x$ and appearing later must also extend to at least $r$, so it still contains $r$.

That means there always exists an optimal solution matching the greedy choice. After fixing that nail, the remaining subproblem is identical in structure, so repeating the argument proves optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    segments = []
    
    for _ in range(n):
        l, r = map(int, input().split())
        
        if l > r:
            l, r = r, l
        
        segments.append((l, r))
    
    segments.sort(key=lambda x: x[1])
    
    nails = []
    
    for l, r in segments:
        if nails and l <= nails[-1] <= r:
            continue
        
        nails.append(r)
    
    print(len(nails))
    print(*nails)

solve()
```

The first section reads and normalizes the intervals. Swapping endpoints when $l > r$ avoids subtle bugs later during sorting and containment checks.

The sort order is the heart of the greedy strategy. By processing intervals with smaller right endpoints first, we guarantee that every decision is forced as early as possible.

The `nails` list stores all chosen positions. The algorithm only checks the most recent nail because of the sorted order. Earlier nails are always less than or equal to the latest one, so if the latest nail does not cover the current interval, none of the older ones can either.

The condition:

```
if nails and l <= nails[-1] <= r:
```

tests whether the current interval is already covered. Since intervals are closed, the comparison includes equality on both sides.

When coverage fails, we append `r`, the current interval's right endpoint. This is the greedy placement that preserves optimality.

## Worked Examples

### Example 1

Input:

```
2
0 2
2 5
```

After sorting by right endpoint:

$$[0,2], [2,5]$$

| Current Segment | Existing Nails | Covered? | Action | Nails After Step |
| --- | --- | --- | --- | --- |
| [0,2] | [] | No | Place nail at 2 | [2] |
| [2,5] | [2] | Yes | Skip | [2] |

Final answer:

```
1
2
```

This example demonstrates why endpoints must count as covered. The nail at position 2 lies on both intervals.

### Example 2

Input:

```
4
1 4
2 5
3 6
7 8
```

Sorted intervals:

$$[1,4], [2,5], [3,6], [7,8]$$

| Current Segment | Existing Nails | Covered? | Action | Nails After Step |
| --- | --- | --- | --- | --- |
| [1,4] | [] | No | Place nail at 4 | [4] |
| [2,5] | [4] | Yes | Skip | [4] |
| [3,6] | [4] | Yes | Skip | [4] |
| [7,8] | [4] | No | Place nail at 8 | [4,8] |

Final answer:

```
2
4 8
```

This trace shows the benefit of placing nails at right endpoints. A nail at 4 covers all three overlapping intervals, while choosing the left endpoint greedily could fail.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the runtime |
| Space | $O(n)$ | Storage for segments and answer list |

With only 1000 intervals, this solution easily fits within the limits. Sorting 1000 elements is trivial, and memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    
    out = io.StringIO()
    sys.stdout = out
    
    n = int(input())
    
    segments = []
    
    for _ in range(n):
        l, r = map(int, input().split())
        
        if l > r:
            l, r = r, l
        
        segments.append((l, r))
    
    segments.sort(key=lambda x: x[1])
    
    nails = []
    
    for l, r in segments:
        if nails and l <= nails[-1] <= r:
            continue
        
        nails.append(r)
    
    print(len(nails))
    print(*nails)
    
    return out.getvalue()

# provided sample
assert run(
"""2
0 2
2 5
"""
) == "1\n2\n", "sample 1"

# minimum-size input
assert run(
"""1
3 3
"""
) == "1\n3\n", "single point segment"

# reversed endpoints
assert run(
"""2
5 1
2 4
"""
) == "1\n4\n", "endpoint normalization"

# disjoint intervals
assert run(
"""3
1 2
4 5
7 8
"""
) == "3\n2 5 8\n", "all intervals separate"

# overlapping chain
assert run(
"""4
1 4
2 5
3 6
7 8
"""
) == "2\n4 8\n", "greedy right endpoint"

# touching endpoints
assert run(
"""3
1 2
2 3
3 4
"""
) == "2\n2 4\n", "closed interval boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single point interval | One nail at that point | Degenerate segments |
| Reversed endpoints | Correct normalization | Input robustness |
| Fully disjoint intervals | One nail per interval | Worst-case answer size |
| Overlapping chain | Shared coverage | Greedy correctness |
| Touching endpoints | Endpoint inclusion | Closed interval handling |

## Edge Cases

Consider reversed endpoints:

```
2
5 1
2 4
```

After normalization, the intervals become $[1,5]$ and $[2,4]$. Sorting gives:

$$[2,4], [1,5]$$

The algorithm places a nail at 4 for the first interval. The second interval also contains 4, so no additional nail is needed.

Output:

```
1
4
```

Without normalization, the interval $(5,1)$ would behave incorrectly during sorting and containment checks.

Now consider degenerate intervals:

```
3
1 1
1 3
5 5
```

Sorted order:

$$[1,1], [1,3], [5,5]$$

The algorithm first places a nail at 1. That covers both the point interval and the larger interval. Later it places another nail at 5.

Output:

```
2
1 5
```

This confirms that intervals of length zero work naturally with the same greedy logic.

Finally, consider touching intervals:

```
3
1 2
2 3
3 4
```

Sorted order is unchanged.

The algorithm places a nail at 2 for the first interval. The second interval is already covered because it includes 2. The third interval does not contain 2, so another nail is placed at 4.

Output:

```
2
2 4
```

This demonstrates why endpoint inclusion matters. Treating intervals as open would incorrectly require three nails.
