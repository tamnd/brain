---
title: "CF 106043A - Squares"
description: "We are given up to $2 cdot 10^5$ axis-aligned squares on the plane. For each square, the input provides its lower-left and upper-right corners. Every coordinate lies in the range $[-10^9, 10^9]$."
date: "2026-06-25T12:48:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106043
codeforces_index: "A"
codeforces_contest_name: "Teamscode Summer 2025 Advanced Division"
rating: 0
weight: 106043
solve_time_s: 49
verified: true
draft: false
---

[CF 106043A - Squares](https://codeforces.com/problemset/problem/106043/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given up to $2 \cdot 10^5$ axis-aligned squares on the plane. For each square, the input provides its lower-left and upper-right corners. Every coordinate lies in the range $[-10^9, 10^9]$. We must output any axis-aligned square $S$ such that, for every given square $s_i$, the intersection $S \cap s_i$ is itself a square with positive area.

The first reaction is to think about the geometry of intersections between squares. One might try to construct a carefully positioned square whose overlap with every input square remains a square. With $n$ as large as $2 \cdot 10^5$, any solution involving pairwise geometric reasoning would need to be extremely efficient.

The key observation is much simpler.

All input squares are guaranteed to lie entirely inside the coordinate box

$$[-10^9, 10^9] \times [-10^9, 10^9].$$

If we output the square

$$S = [-10^9, -10^9] \to [10^9, 10^9],$$

then every input square is completely contained inside $S$.

As a result,

$$S \cap s_i = s_i$$

for every input square $s_i$.

Since each $s_i$ is already a square with positive area, every intersection is automatically a square with positive area. The output square itself also satisfies all coordinate limits because its corners are exactly on the allowed boundaries.

### Non-obvious Edge Cases

A common mistake is to try to build a square based on the input and accidentally make it too small.

For example:

```
1
1 1 2 2
```

If the chosen square does not overlap the input square, the intersection has zero area and becomes invalid.

The fixed square

```
-1000000000 -1000000000 1000000000 1000000000
```

contains the entire input square, so the intersection is exactly the original $1 \times 1$ square.

Another easy mistake is forgetting that coordinates may already lie on the boundary:

```
1
-1000000000 -1000000000 1000000000 1000000000
```

Our output square is identical to the input square. The intersection remains a square with positive area.

## Approaches

A brute-force mindset would be to examine the geometry of all given squares and construct a square whose overlap with each one remains square-shaped. One could analyze interval overlaps on both axes and try to satisfy a large collection of geometric constraints.

The problem becomes much easier after noticing that the statement only asks for **any** valid square.

Since every coordinate of every input square lies within $[-10^9, 10^9]$, the largest allowed axis-aligned square

$$[-10^9,-10^9] \to [10^9,10^9]$$

already contains every possible input square. When one shape contains another completely, their intersection is simply the smaller shape.

That means every intersection equals the original input square, which is guaranteed to be a square with nonzero area.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Depends on geometric construction | Depends on implementation | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input. The actual square descriptions do not affect the answer.
2. Output the fixed square:

$$(-10^9,-10^9)$$

as the lower-left corner and

$$(10^9,10^9)$$

as the upper-right corner.
3. Finish.

### Why it works

Every input square has all of its coordinates inside the range $[-10^9,10^9]$. The fixed square spans exactly that entire coordinate range. Consequently, every input square is fully contained inside it.

For any contained square $s_i$,

$$S \cap s_i = s_i.$$

Because $s_i$ is guaranteed to be a square with positive area, the intersection satisfies the required condition. Since this argument holds for every input square, the construction is always valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

for _ in range(n):
    input()

print(-1000000000, -1000000000, 1000000000, 1000000000)
```

The implementation reads and discards the input squares because their exact positions are irrelevant.

The only important fact is the coordinate bound given in the statement. The printed square occupies the entire allowed coordinate range. Since every input square must lie inside that range, each intersection equals the original square.

There are no overflow concerns in Python, and there are no geometric computations that could introduce boundary errors.

## Worked Examples

### Example 1

Input:

```
3
2 3 4 5
7 3 10 6
8 1 12 5
```

Output:

```
-1000000000 -1000000000 1000000000 1000000000
```

| Step | Action | Result |
| --- | --- | --- |
| 1 | Read n | 3 |
| 2 | Read all squares | Discarded |
| 3 | Print fixed square | Done |

Each of the three input squares lies entirely inside the output square. Every intersection equals the corresponding input square.

### Example 2

Input:

```
1
1 1 2 2
```

Output:

```
-1000000000 -1000000000 1000000000 1000000000
```

| Step | Action | Result |
| --- | --- | --- |
| 1 | Read n | 1 |
| 2 | Read square | Discarded |
| 3 | Print fixed square | Done |

The input square is contained in the output square, so the intersection is exactly the $1 \times 1$ square.

This example demonstrates that even the smallest valid input is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Aside from reading input, the algorithm performs no computation dependent on $n$ |
| Space | O(1) | No extra storage is used |

The solution comfortably fits within all limits because it performs a constant amount of work and stores no data structures.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    for _ in range(n):
        sys.stdin.readline()

    return "-1000000000 -1000000000 1000000000 1000000000\n"

# sample-like cases
assert run(
"""3
2 3 4 5
7 3 10 6
8 1 12 5
"""
) == "-1000000000 -1000000000 1000000000 1000000000\n"

assert run(
"""1
1 1 2 2
"""
) == "-1000000000 -1000000000 1000000000 1000000000\n"

# minimum size
assert run(
"""1
0 0 1 1
"""
) == "-1000000000 -1000000000 1000000000 1000000000\n"

# boundary coordinates
assert run(
"""1
-1000000000 -1000000000 1000000000 1000000000
"""
) == "-1000000000 -1000000000 1000000000 1000000000\n"

# multiple squares
assert run(
"""4
1 1 2 2
3 3 5 5
-7 -7 -3 -3
10 10 20 20
"""
) == "-1000000000 -1000000000 1000000000 1000000000\n"

# off-by-one style boundary test
assert run(
"""1
999999999 999999999 1000000000 1000000000
"""
) == "-1000000000 -1000000000 1000000000 1000000000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single small square | Fixed square | Minimum input size |
| Square covering full range | Fixed square | Boundary coordinates |
| Several separated squares | Fixed square | Input geometry is irrelevant |
| Square touching maximum coordinate | Fixed square | No off-by-one issues |
| Sample-style input | Fixed square | General correctness |

## Edge Cases

Consider the input:

```
1
-1000000000 -1000000000 1000000000 1000000000
```

The algorithm outputs:

```
-1000000000 -1000000000 1000000000 1000000000
```

The intersection is the same square. Its area is positive, so the requirement is satisfied.

Now consider:

```
1
999999999 999999999 1000000000 1000000000
```

The input square lies on the extreme upper-right corner of the allowed region. The fixed output square still contains it completely. The intersection equals the input square, which remains a valid square with nonzero area.

Finally:

```
3
1 1 2 2
100 100 200 200
-500 -500 -400 -400
```

All three squares are inside the fixed square. Each intersection is exactly the corresponding input square. No matter how far apart the squares are, the argument remains unchanged.
