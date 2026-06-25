---
title: "CF 106035A - Pyramidal paths"
description: "We are given a sequence that represents a walk visiting each vertex exactly once, so it is already a permutation of the numbers from 1 to n. The task is to determine whether this ordering has a very specific shape. The allowed shape is “pyramidal” in the following sense."
date: "2026-06-25T12:55:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106035
codeforces_index: "A"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2024"
rating: 0
weight: 106035
solve_time_s: 49
verified: true
draft: false
---

[CF 106035A - Pyramidal paths](https://codeforces.com/problemset/problem/106035/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence that represents a walk visiting each vertex exactly once, so it is already a permutation of the numbers from 1 to n. The task is to determine whether this ordering has a very specific shape.

The allowed shape is “pyramidal” in the following sense. If you look at the permutation from left to right, it must first strictly move in one direction in terms of values (either strictly increasing or strictly decreasing), and after that it must switch direction exactly once and continue strictly in the opposite direction. Both parts must have length at least two, although the turning point itself belongs to both monotonic interpretations in the sense that it is shared by the two segments.

So the structure is essentially a single peak or a single valley: either values go up then down, or go down then up, with no second reversal allowed.

The input is just n followed by the permutation. The output is a simple yes or no depending on whether such a single-change monotonic structure exists.

The constraint n up to 100000 forces any solution to be linear, since anything quadratic would be around 10^10 operations in the worst case and immediately impossible under typical time limits. Even an O(n log n) approach is acceptable but unnecessary here; the structure is local enough that a single pass is enough.

The main edge cases are subtle failures of “almost monotone” sequences.

A first example is a fully monotone array like [1, 2, 3, 4, 5]. It might look acceptable at first glance because it has no violations, but it never forms two segments with a change of direction, so it must be rejected.

Another example is something like [4, 5, 6, 1, 2, 3]. This has one clean increase followed by a decrease in terms of actual values, but the transition is not consistent with a single peak or valley over the entire sequence because the direction changes more than once when interpreted over the full permutation ordering.

A more subtle case is a short oscillation like [1, 3, 2]. This is valid because it increases once and then decreases once, and both segments have sufficient length.

## Approaches

A brute-force interpretation would try every possible split point i, treating the prefix as one monotone direction and the suffix as the opposite direction. For each split we would verify monotonicity by scanning both halves. This leads to O(n^2) behavior because each split costs O(n) and there are O(n) splits. At n = 10^5 this is far beyond feasible limits.

The structure of the problem is that the sequence is already a permutation, so comparisons between neighbors fully describe all changes in trend. Instead of testing all split points, we only need to detect how many times the direction of adjacent differences changes.

If we compute the sign of each adjacent difference, the entire problem reduces to checking whether the sign sequence has at most one transition from positive to negative or negative to positive, and that the initial segment has at least one step in each direction if a change exists. This is equivalent to counting how many times the sequence switches between increasing and decreasing trends.

The key insight is that any pyramidal sequence can only have one extremum, so the direction changes at most once. If it changes zero times, the sequence is monotone and invalid. If it changes once, it is valid as long as both sides are non-empty.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Split Checking | O(n^2) | O(1) | Too slow |
| Direction Change Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process adjacent differences and track direction changes.

1. Compute whether each adjacent pair is increasing or decreasing by comparing a[i] and a[i+1]. This compresses the sequence into a binary trend representation.
2. Traverse this trend array and count how many times the trend flips from increasing to decreasing or vice versa. Each flip corresponds to a potential peak or valley.
3. If the number of flips is greater than 1, the structure cannot be pyramidal because it would imply multiple turning points.
4. If there are zero flips, the array is fully monotone and does not contain the required single peak or valley structure, so it is invalid.
5. If there is exactly one flip, check that both segments formed by this flip have length at least 2 in the original sequence. This ensures the “pyramid” has meaningful ascending and descending parts.

The core idea is that we are reducing a global shape condition into a local property of transitions.

### Why it works

The invariant is that the sequence is always being interpreted as a piecewise monotone path. Every time we see a change in sign of adjacent differences, we identify a boundary between monotone segments. A valid pyramidal path must have exactly two monotone segments: one increasing and one decreasing, in either order. If more than one boundary exists, there are at least three monotone segments, meaning the sequence changes direction more than once, which violates the definition. If no boundary exists, the sequence never switches direction, so it cannot form a pyramid. Maintaining this invariant over a single pass guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

# build trend array: +1 for up, -1 for down
trend = []
for i in range(n - 1):
    if a[i] < a[i + 1]:
        trend.append(1)
    else:
        trend.append(-1)

changes = 0
for i in range(1, len(trend)):
    if trend[i] != trend[i - 1]:
        changes += 1

# valid pyramidal path must have exactly one change
if changes != 1:
    print("NO")
else:
    print("YES")
```

The code first compresses the permutation into a sequence of directions between neighbors. This avoids reasoning about values directly and instead focuses on structural changes.

The second loop counts how many times this direction flips. That count directly corresponds to the number of monotone segments minus one.

Finally, the decision checks whether there is exactly one such flip, which is the signature of a single peak or valley structure.

A subtle point is that equality never occurs because the input is a permutation, so every adjacent comparison is strictly increasing or decreasing. That removes ambiguity in trend extraction.

## Worked Examples

### Example 1

Input:

```
5
4 3 1 2 5
```

Trend construction:

| i | a[i] vs a[i+1] | trend |
| --- | --- | --- |
| 0 | 4 > 3 | -1 |
| 1 | 3 > 1 | -1 |
| 2 | 1 < 2 | +1 |
| 3 | 2 < 5 | +1 |

Change detection:

| i | trend[i-1] | trend[i] | change |
| --- | --- | --- | --- |
| 1 | -1 | -1 | 0 |
| 2 | -1 | +1 | 1 |
| 3 | +1 | +1 | 1 |

Total changes = 1, so output is YES.

This confirms a single valley structure: decreasing then increasing.

### Example 2

Input:

```
6
4 5 6 1 2 3
```

Trend:

| i | trend |
| --- | --- |
| 0 | +1 |
| 1 | +1 |
| 2 | -1 |
| 3 | +1 |
| 4 | +1 |

Change detection:

| i | change |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

Total changes = 2, so output is NO.

This demonstrates a sequence with multiple direction shifts, meaning it has more than one extremum and cannot be pyramidal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the permutation once to build trends and once to count changes |
| Space | O(n) | We store the trend array, which has size n−1 |

The constraints allow up to 100000 elements, so a linear scan comfortably fits within limits, both in runtime and memory. A constant-space version is also possible by computing trends on the fly, but unnecessary here.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    trend = []
    for i in range(n - 1):
        trend.append(1 if a[i] < a[i + 1] else -1)

    changes = 0
    for i in range(1, len(trend)):
        if trend[i] != trend[i - 1]:
            changes += 1

    return "YES\n" if changes == 1 else "NO\n"

# provided samples
assert run("5\n4 3 1 2 5\n") == "YES\n"
assert run("3\n1 3 2\n") == "YES\n"

# custom cases
assert run("3\n1 2 3\n") == "NO\n", "fully increasing"
assert run("3\n3 2 1\n") == "NO\n", "fully decreasing"
assert run("4\n2 1 3 4\n") == "YES\n", "single valley"
assert run("6\n1 3 2 4 5 6\n") == "NO\n", "multiple changes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 | NO | monotone increasing should be rejected |
| 3 2 1 | NO | monotone decreasing should be rejected |
| 2 1 3 4 | YES | single valley structure is valid |
| 1 3 2 4 5 6 | NO | multiple direction changes break pyramidal form |

## Edge Cases

A strictly increasing sequence like `1 2 3 4` produces a trend array of all +1 with zero changes, so it is immediately rejected. The algorithm counts no flips and correctly outputs NO.

A strictly decreasing sequence like `4 3 2 1` behaves symmetrically, also producing zero flips and returning NO.

A minimal valid pyramid such as `2 1 3` produces a single change from -1 to +1. The algorithm detects exactly one flip and returns YES, matching the requirement that both segments exist and are non-empty.

A sequence with multiple oscillations like `1 3 2 4` produces two flips in the trend array, causing rejection because it contains more than one extremum, which violates the pyramidal constraint.
