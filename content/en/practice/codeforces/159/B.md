---
title: "CF 159B - Matchmaker"
description: "We have two collections of objects. Markers are described by (color, diameter) and caps are also described by (color, diameter). A cap can be attached to a marker only if the diameters are equal."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 159
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Qualification Round 2"
rating: 1100
weight: 159
solve_time_s: 121
verified: true
draft: false
---

[CF 159B - Matchmaker](https://codeforces.com/problemset/problem/159/B)

**Rating:** 1100  
**Tags:** *special, greedy, sortings  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two collections of objects. Markers are described by `(color, diameter)` and caps are also described by `(color, diameter)`.

A cap can be attached to a marker only if the diameters are equal. Among all valid pairings, some are considered “beautiful” when the colors also match.

The optimization goal has two layers. First, maximize the total number of matched marker-cap pairs. Among all ways that achieve this maximum, maximize the number of beautiful matches.

A marker and a cap can each be used at most once.

The constraints are large enough that we cannot try every pairing directly. Both `n` and `m` can reach `10^5`, so an `O(n * m)` solution would perform up to `10^10` comparisons, which is far beyond the time limit. We need something close to linear or `O(n log n)`.

The most important observation is that diameter completely determines compatibility. A cap with diameter `5` can never interact with a marker of diameter `7`. This means every diameter group can be processed independently.

There are several edge cases that easily break careless solutions.

Consider this input:

```
2 2
1 5
2 5
3 5
4 5
```

The correct answer is:

```
2 0
```

Every marker can still be closed because all diameters match, even though no colors match. A wrong greedy strategy that only searches for beautiful matches would return `0 0`.

Now consider:

```
2 1
1 3
1 3
1 3
```

The correct answer is:

```
1 1
```

Only one cap exists, so only one marker can be closed. Forgetting that each cap is single-use would incorrectly produce `2 2`.

Another subtle case is when maximizing beautiful matches too early reduces the total number of matches.

```
2 2
1 1
2 1
1 1
3 1
```

The correct answer is:

```
2 1
```

If we first greedily consume the only `(1,1)` cap on the first marker, the second marker can still use `(3,1)`, so everything works. But in more complicated variants, consuming caps without respecting the primary objective can reduce the total number of closed markers. The problem explicitly says total matches matter more than beautiful matches, so the algorithm must preserve that priority.

## Approaches

The brute-force idea is straightforward. For every marker, scan through all caps and pick any unused cap with the same diameter. If possible, prefer a cap whose color also matches.

This approach is logically correct because it tries to build valid pairings directly. The problem appears small conceptually, but the constraints destroy this solution. With `10^5` markers and `10^5` caps, we may perform `10^10` compatibility checks. Even in optimized languages this is too slow.

The key observation is that compatibility depends only on diameter. Once we group everything by diameter, different groups become completely independent.

Suppose we focus on one fixed diameter `d`. Inside this group:

```
marker colors: frequencies
cap colors: frequencies
```

The maximum number of markers we can close is simply:

```
min(total markers with diameter d,
    total caps with diameter d)
```

No color information matters for this first objective.

Then, among those maximum possible pairings, we want as many beautiful matches as possible. For a specific color `c`, the number of beautiful pairs we can create is:

```
min(markers[d][c], caps[d][c])
```

because each beautiful match consumes one marker and one cap of that exact color.

Crucially, maximizing beautiful matches never reduces the total number of matches. Beautiful pairs are already valid pairs, and any remaining unmatched items inside the same diameter group can still be arbitrarily paired until we reach the maximum possible count.

This reduces the problem to frequency counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(m) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read all markers and group them by diameter and color.

For each marker `(x, y)`, increment:

```
markers_by_diameter[y]
markers_by_color[(y, x)]
```

The first structure tracks how many markers exist for a diameter. The second tracks exact `(diameter, color)` frequencies.
2. Read all caps and group them the same way.

For each cap `(a, b)`, increment:

```
caps_by_diameter[b]
caps_by_color[(b, a)]
```
3. Compute the maximum number of closed markers.

For every diameter that appears, add:

```
min(markers_by_diameter[d],
    caps_by_diameter[d])
```

This is the largest number of pairs possible for that diameter because only equal diameters can interact.
4. Compute the maximum number of beautiful matches.

For every `(diameter, color)` pair that appears among markers, add:

```
min(markers_by_color[(d, c)],
    caps_by_color[(d, c)])
```

Each such pair corresponds to a beautiful match opportunity.
5. Print the two totals.

### Why it works

The algorithm relies on the fact that diameter groups are independent. A cap from one diameter can never help a marker from another diameter.

Inside a fixed diameter group, the maximum number of valid pairs is completely determined by the smaller side. If there are 8 markers and 5 caps of diameter `d`, no strategy can create more than 5 pairs, and any arbitrary pairing achieves 5.

Beautiful matches are a refinement inside those already-valid pairings. For each color, we greedily create as many equal-color pairs as possible. This cannot reduce the total number of pairs because every beautiful pair already consumes one marker and one cap that were compatible anyway. The remaining unmatched items can still be paired arbitrarily by diameter.

Because both objectives are optimized independently and consistently inside every diameter group, the final answer is globally optimal.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

n, m = map(int, input().split())

markers_by_diameter = defaultdict(int)
caps_by_diameter = defaultdict(int)

markers_by_color = defaultdict(int)
caps_by_color = defaultdict(int)

for _ in range(n):
    x, y = map(int, input().split())
    markers_by_diameter[y] += 1
    markers_by_color[(y, x)] += 1

for _ in range(m):
    a, b = map(int, input().split())
    caps_by_diameter[b] += 1
    caps_by_color[(b, a)] += 1

closed = 0
beautiful = 0

all_diameters = set(markers_by_diameter.keys()) | set(caps_by_diameter.keys())

for d in all_diameters:
    closed += min(markers_by_diameter[d], caps_by_diameter[d])

for key, cnt in markers_by_color.items():
    beautiful += min(cnt, caps_by_color[key])

print(closed, beautiful)
```

The first part of the implementation builds frequency tables. Using `defaultdict(int)` avoids repeated existence checks and keeps updates constant time.

The code separates counting by diameter from counting by exact `(diameter, color)` pairs. This mirrors the two optimization goals in the problem. Diameter counts determine the maximum number of total matches, while exact pair counts determine the maximum number of beautiful matches.

The union of diameter sets is used when computing total closed markers. This avoids missing a diameter that appears only on one side.

For beautiful matches, iterating through marker keys is sufficient. If a `(diameter, color)` pair does not exist among caps, the defaultdict automatically returns zero.

No sorting is needed because the problem only depends on frequencies, not order.

## Worked Examples

### Example 1

Input:

```
3 4
1 2
3 4
2 4
5 4
2 4
1 1
1 2
```

### Diameter Counts

| Diameter | Markers | Caps | Contribution |
| --- | --- | --- | --- |
| 2 | 1 | 1 | 1 |
| 4 | 2 | 2 | 2 |

Total closed markers = `1 + 2 = 3`

### Beautiful Match Counts

| Diameter | Color | Marker Count | Cap Count | Beautiful Pairs |
| --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 1 | 1 |
| 4 | 3 | 1 | 0 | 0 |
| 4 | 2 | 1 | 1 | 1 |

Total beautiful matches = `2`

Output:

```
3 2
```

This trace shows that maximizing beautiful matches is done independently inside each diameter group. The unmatched color at diameter `4` still participates in a normal match.

### Example 2

Input:

```
4 3
1 1
2 1
3 2
4 2
2 1
5 2
3 2
```

### Diameter Counts

| Diameter | Markers | Caps | Contribution |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 2 | 2 | 2 |

Total closed markers = `3`

### Beautiful Match Counts

| Diameter | Color | Marker Count | Cap Count | Beautiful Pairs |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 |
| 1 | 2 | 1 | 1 | 1 |
| 2 | 3 | 1 | 1 | 1 |
| 2 | 4 | 1 | 0 | 0 |

Total beautiful matches = `2`

Output:

```
3 2
```

This example demonstrates that some markers inevitably remain unmatched because there are not enough caps of the same diameter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each marker and cap is processed once |
| Space | O(n + m) | Frequency tables store all distinct groups |

The solution easily fits within the limits. With at most `2 * 10^5` total objects, linear processing is fast enough in Python, and the hash maps remain comfortably within memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    markers_by_diameter = defaultdict(int)
    caps_by_diameter = defaultdict(int)

    markers_by_color = defaultdict(int)
    caps_by_color = defaultdict(int)

    for _ in range(n):
        x, y = map(int, input().split())
        markers_by_diameter[y] += 1
        markers_by_color[(y, x)] += 1

    for _ in range(m):
        a, b = map(int, input().split())
        caps_by_diameter[b] += 1
        caps_by_color[(b, a)] += 1

    closed = 0
    beautiful = 0

    all_diameters = set(markers_by_diameter) | set(caps_by_diameter)

    for d in all_diameters:
        closed += min(markers_by_diameter[d], caps_by_diameter[d])

    for key, cnt in markers_by_color.items():
        beautiful += min(cnt, caps_by_color[key])

    print(closed, beautiful)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run(
"""3 4
1 2
3 4
2 4
5 4
2 4
1 1
1 2
"""
) == "3 2", "sample 1"

# minimum size
assert run(
"""1 1
1 1
1 1
"""
) == "1 1", "minimum case"

# same diameter, different colors
assert run(
"""2 2
1 5
2 5
3 5
4 5
"""
) == "2 0", "all matches but no beautiful pairs"

# insufficient caps
assert run(
"""3 1
1 2
1 2
1 2
1 2
"""
) == "1 1", "single cap only"

# mixed groups
assert run(
"""4 3
1 1
2 1
3 2
4 2
2 1
5 2
3 2
"""
) == "3 2", "multiple diameter groups"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single marker and cap with same properties | `1 1` | Minimum valid input |
| All diameters equal but colors different | `2 0` | Total matches and beautiful matches are separate objectives |
| Many markers but one cap | `1 1` | Caps are single-use |
| Multiple diameter groups | `3 2` | Independent processing by diameter |

## Edge Cases

Consider the case where colors never match but diameters do.

Input:

```
2 2
1 5
2 5
3 5
4 5
```

The algorithm computes:

```
diameter 5:
markers = 2
caps = 2
```

So total closed markers becomes `2`.

For beautiful matches:

```
(5,1): min(1,0) = 0
(5,2): min(1,0) = 0
```

The final answer is:

```
2 0
```

This confirms the algorithm does not mistakenly require color equality for ordinary matches.

Now consider repeated identical markers with too few caps.

Input:

```
3 1
1 2
1 2
1 2
1 2
```

The algorithm computes:

```
diameter 2:
markers = 3
caps = 1
```

So only one total match is possible.

For beautiful matches:

```
(2,1): min(3,1) = 1
```

The answer becomes:

```
1 1
```

This verifies that every cap is consumed at most once.

Finally, consider isolated diameter groups.

Input:

```
2 2
1 1
2 2
1 2
2 3
```

Diameter contributions:

```
diameter 1: min(1,0) = 0
diameter 2: min(1,1) = 1
diameter 3: min(0,1) = 0
```

Beautiful matches:

```
(2,2): min(1,0) = 0
```

Output:

```
1 0
```

This demonstrates that different diameter groups are completely independent and cannot help each other.
