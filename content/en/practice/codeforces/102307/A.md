---
title: "CF 102307A - Amazon"
description: "We are given several pairs of points. Each pair determines an infinite straight subway line through those two points. The actual segment between the points is irrelevant because the subway line extends indefinitely."
date: "2026-08-13T23:33:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "A"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 66
verified: true
draft: false
---

[CF 102307A - Amazon](https://codeforces.com/problemset/problem/102307/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several pairs of points. Each pair determines an infinite straight subway line through those two points. The actual segment between the points is irrelevant because the subway line extends indefinitely.

Two different subway lines produce a strong intersection exactly when they are perpendicular. The same geometric line may be described by several input pairs, and those descriptions must count as one subway line. The task is to count pairs of distinct geometric lines whose directions form a right angle.

The input contains up to (10^5) pairs in one test case, with up to 100 test cases. The coordinates are bounded by (2\cdot10^4), but the answer can be much larger than the coordinate range. With (10^5) lines, checking every pair would require about (10^{10}/2) comparisons, which is far beyond a one-second time limit. We need a solution close to linear or (O(n\log n)) in the number of input pairs.

There are several ways a careless implementation can silently count the wrong thing. First, duplicate descriptions of the same line must not create extra intersections. For example,

```
1
3
0 0 2 0
5 0 -3 0
0 1 0 3
```

contains two descriptions of the horizontal line (y=0), plus the vertical line (x=0). The correct output is `1`, because there is only one geometric horizontal line and it is perpendicular to the vertical line. Counting input pairs directly would incorrectly produce two intersections.

Reversing the endpoints must also leave the line unchanged. For example,

```
1
2
0 0 4 0
4 0 0 0
```

describes the same line twice, so the answer is `0`. A representation based on the raw direction vector would see `(4, 0)` and `(-4, 0)` as different unless the direction is normalized.

Vertical and horizontal lines need special handling if slopes are represented with division. For example,

```
1
2
-20000 20000 20000 20000
20000 -20000 20000 20000
```

describes (y=20000) and (x=20000), which are perpendicular, so the answer is `1`. Using floating-point slopes is unnecessary and can introduce precision problems. We can represent every line entirely with integers.

Finally, several parallel lines are different subway lines and must be counted separately when a perpendicular family exists. For example,

```
1
3
-2 0 2 0
-2 1 2 1
0 -2 0 2
```

contains two distinct horizontal lines and one vertical line. The correct answer is `2`, because the vertical line intersects both horizontal lines at right angles.

## Approaches

The direct approach is to construct all subway lines and then examine every pair of them. For each pair, we would check whether they are distinct and whether their direction vectors have dot product zero. This is correct because every strong intersection corresponds exactly to one perpendicular pair of distinct lines.

The problem is the number of comparisons. For (n=10^5), there are

[
\frac{n(n-1)}2 \approx 5\cdot10^9
]

pairs. Even if one comparison took only a few integer operations, billions of comparisons cannot fit into the time limit.

The key observation is that perpendicularity depends only on the direction of a line, while duplicate input pairs can be removed by identifying the complete geometric line. We can first canonicalize each line and put it into a set. After duplicates are removed, we only need to know how many distinct lines have each direction.

A line through ((x_1,y_1)) and ((x_2,y_2)) has a direction vector

[
(dx,dy)=(x_2-x_1,y_2-y_1).
]

To identify the same direction regardless of scale or orientation, divide by (\gcd(|dx|,|dy|)) and choose one sign convention. For example, require the first nonzero component to be positive. Thus `(4, 2)`, `(2, 1)`, `(-2, -1)`, and `(-4, -2)` all represent the same direction.

However, direction alone is not enough to identify a line, because parallel lines can be different. We therefore represent the complete line as

[
Ax+By+C=0,
]

where

[
A=dy,\qquad B=-dx,\qquad C=dx,y_1-dy,x_1.
]

We divide all three coefficients by their common gcd and normalize their sign. The resulting triple `(A, B, C)` is a unique representation of the geometric line.

Once every distinct line is known, suppose its canonical direction is `(dx, dy)`. A perpendicular direction is

[
(-dy,dx).
]

We normalize that direction using the same sign convention. If `cnt[d]` is the number of distinct lines having direction `d`, then all intersections involving this direction and its perpendicular contribute

[
cnt[d]\cdot cnt[perp].
]

We process each unordered pair of direction classes only once, using a simple ordering comparison between the two direction tuples.

The brute-force method works because it directly checks the definition of a strong intersection, but it fails because it repeats essentially the same geometric reasoning for billions of pairs. The observation that the answer depends only on unique lines grouped by direction reduces the problem to building a set and counting compatible groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n\log C+n)) expected | (O(n)) | Accepted |

Here (C) represents the magnitude of the integer coefficients. With the given coordinate bounds, the gcd computation is effectively constant time, so the practical complexity is (O(n)) expected time because Python sets and dictionaries provide expected (O(1)) insertion and lookup.

## Algorithm Walkthrough

1. For every pair of input points, compute `dx = x2 - x1` and `dy = y2 - y1`. These values describe the direction of the subway line without using floating-point arithmetic.
2. Construct the line equation (Ax+By+C=0) using `A = dy`, `B = -dx`, and `C = dx*y1 - dy*x1`. Divide all three coefficients by their gcd and normalize their common sign. Store the resulting triple in a set. This removes repeated descriptions of exactly the same geometric line, including descriptions with reversed endpoints.
3. For every newly inserted line, normalize its direction vector `(dx, dy)` by dividing by `gcd(abs(dx), abs(dy))`. Flip both components if necessary so that the first nonzero component is positive. Increment the frequency of this direction. We count directions only for distinct lines, because two input pairs describing the same line must contribute only one subway line.
4. After all lines have been processed, iterate over every direction `d = (dx, dy)`. Construct its perpendicular direction as `(-dy, dx)` and normalize it with the same convention. The number of perpendicular pairs represented by these two direction classes is `cnt[d] * cnt[perp]`.
5. Add this product only when `d < perp` lexicographically. This makes every unordered pair of direction classes appear exactly once. A line direction can never equal its own perpendicular direction, so there is no special self-pair case.

### Why it works

After canonicalization, every geometric subway line has exactly one line key, so the set contains each actual line once. For every such line, its normalized direction identifies its orientation independently of its position and of the coordinates used to describe it. Two nonzero direction vectors are perpendicular exactly when their dot product is zero, and `(dx,dy)` is perpendicular to `(-dy,dx)`. Thus every pair of distinct perpendicular subway lines belongs to exactly one pair of direction classes `d` and `perp`. The frequency product counts every combination of one line from each class, while the lexicographic condition counts that unordered pair of classes only once. Hence the final sum is exactly the number of strong intersections.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def normalize_direction(dx, dy):
    g = gcd(abs(dx), abs(dy))
    dx //= g
    dy //= g

    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy

    return dx, dy

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        n = int(input())

        lines = set()
        direction_count = {}

        for _ in range(n):
            x1, y1, x2, y2 = map(int, input().split())

            dx = x2 - x1
            dy = y2 - y1

            # The problem describes a line using two locations,
            # so the two locations are assumed to be distinct.
            A = dy
            B = -dx
            C = dx * y1 - dy * x1

            g = gcd(gcd(abs(A), abs(B)), abs(C))
            A //= g
            B //= g
            C //= g

            if A < 0 or (A == 0 and B < 0) or (
                A == 0 and B == 0 and C < 0
            ):
                A = -A
                B = -B
                C = -C

            line = (A, B, C)

            if line in lines:
                continue

            lines.add(line)

            direction = normalize_direction(dx, dy)
            direction_count[direction] = direction_count.get(direction, 0) + 1

        answer = 0

        for dx, dy in direction_count:
            perp = normalize_direction(-dy, dx)

            if (dx, dy) < perp:
                answer += direction_count.get(perp, 0) * direction_count[(dx, dy)]

        answers.append(str(answer))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The `normalize_direction` function removes the common factor from a direction vector, then fixes its orientation. The condition `dx < 0 or (dx == 0 and dy < 0)` means that horizontal directions become `(positive, 0)` and vertical directions become `(0, positive)`. This gives one representation for each undirected orientation.

The line equation uses the direction vector to construct a normal vector. Since `A = dy` and `B = -dx`, the vector `(A, B)` is perpendicular to the line. The constant `C` is chosen so that the first input point satisfies the equation. Dividing all three coefficients by their common gcd removes arbitrary scaling.

The sign normalization of `(A, B, C)` is necessary because both

[
Ax+By+C=0
]

and

[
-Ax-By-C=0
]

describe the same line. Without the sign rule, identical lines could occupy two different set entries.

The line is inserted into `lines` before its direction is counted. This ordering is essential. If the line has already appeared, its second description must not increase the direction frequency.

The answer uses Python integers, so there is no overflow issue even though the maximum number of intersections can reach

[
\frac{10^5(10^5-1)}2=4,999,950,000.
]

The final lexicographic comparison prevents double counting. For example, if `(1, 0)` is perpendicular to `(0, 1)`, processing `(1, 0)` counts the product, while processing `(0, 1)` does nothing because `(0, 1) < (1, 0)` is false.

## Worked Examples

### Sample 1

The first test case contains the lines (y=2), (x=3), and (y=-3).

| Input line | Canonical direction | Line | Direction counts after insertion | Answer |
| --- | --- | --- | --- | --- |
| `-3 2 2 2` | `(1, 0)` | (y=2) | `(1,0): 1` | 0 |
| `3 1 3 -3` | `(0, 1)` | (x=3) | `(1,0): 1`, `(0,1): 1` | 0 |
| `-3 -3 -1 -3` | `(1, 0)` | (y=-3) | `(1,0): 2`, `(0,1): 1` | 0 |

The horizontal direction `(1,0)` is perpendicular to the vertical direction `(0,1)`. Their frequencies are 2 and 1, giving (2\cdot1=2). The output is therefore `2`. This example also demonstrates why parallel lines must remain separate after duplicate removal.

### Sample 2

The three lines have direction vectors proportional to `(-6, 9)`, `(6, 4)`, and `(-4, 2)`.

| Input line | Normalized direction | Perpendicular direction | Direction count | Added |
| --- | --- | --- | --- | --- |
| `2 -2 -4 7` | `(2, -3)` | `(3, 2)` | 1 | 0 initially |
| `0 -2 6 2` | `(3, 2)` | `(-2, 3)` → `(2, -3)` | 1 | 1 |
| `4 -2 0 0` | `(2, -1)` | `(1, 2)` | 1 | 0 |

The first and second lines are perpendicular because their original direction vectors have dot product

[
(-6)\cdot6+9\cdot4=0.
]

The third direction has no perpendicular partner among the three lines. The result is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) expected | Each line uses a constant number of gcd operations and expected (O(1)) set or dictionary operations, followed by one pass over the distinct direction classes. |
| Space | (O(n)) | The set of canonical lines and the direction-frequency dictionary each contain at most (n) entries. |

For (n=10^5), the algorithm performs roughly a few hash-table operations per input line instead of several billion pairwise checks. The coordinate bounds also keep the integer coefficients small enough that Python's arbitrary-precision arithmetic is inexpensive here.

## Test Cases

```python
import sys
import io
from math import gcd

def normalize_direction(dx, dy):
    g = gcd(abs(dx), abs(dy))
    dx //= g
    dy //= g

    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy

    return dx, dy

def solve(data):
    it = iter(data.strip().split())
    t = int(next(it))
    out = []

    for _ in range(t):
        n = int(next(it))

        lines = set()
        direction_count = {}

        for _ in range(n):
            x1 = int(next(it))
            y1 = int(next(it))
            x2 = int(next(it))
            y2 = int(next(it))

            dx = x2 - x1
            dy = y2 - y1

            A = dy
            B = -dx
            C = dx * y1 - dy * x1

            g = gcd(gcd(abs(A), abs(B)), abs(C))
            A //= g
            B //= g
            C //= g

            if A < 0 or (A == 0 and B < 0) or (
                A == 0 and B == 0 and C < 0
            ):
                A = -A
                B = -B
                C = -C

            line = (A, B, C)

            if line in lines:
                continue

            lines.add(line)

            d = normalize_direction(dx, dy)
            direction_count[d] = direction_count.get(d, 0) + 1

        ans = 0

        for d in direction_count:
            dx, dy = d
            p = normalize_direction(-dy, dx)

            if d < p:
                ans += direction_count[d] * direction_count.get(p, 0)

        out.append(str(ans))

    return "\n".join(out)

# Provided samples
sample_input = """\
3
3
-3 2 2 2
3 1 3 -3
-3 -3 -1 -3
3
2 -2 -4 7
0 -2 6 2
4 -2 0 0
2
0 -1 -6 1
2 5 -3 0
"""

assert solve(sample_input) == "2\n1\n0", "provided samples"

# Minimum-size input: one line cannot have an intersection.
assert solve("""\
1
1
0 0 1 1
""") == "0", "minimum size"

# Duplicate descriptions of the same line must count once.
assert solve("""\
1
3
0 0 4 0
4 0 0 0
-2 0 2 0
""") == "0", "duplicate line descriptions"

# Horizontal and vertical boundary-coordinate lines are perpendicular.
assert solve("""\
1
2
-20000 20000 20000 20000
20000 -20000 20000 20000
""") == "1", "boundary coordinates"

# Three lines: two horizontal and one vertical, giving two intersections.
assert solve("""\
1
3
-2 0 2 0
-2 1 2 1
0 -2 0 2
""") == "2", "multiple parallel lines"

# Maximum n, but every input pair describes the same geometric line.
max_case = ["1", "100000"]
max_case.extend(["0 0 20000 0"] * 100000)
assert solve("\n".join(max_case)) == "0", "maximum n"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 0 0 1 1` | `0` | Minimum-size input |
| Three copies of `y=0` | `0` | Duplicate line removal |
| `y=20000` and `x=20000` | `1` | Vertical, horizontal, and coordinate boundaries |
| Two horizontal lines and one vertical line | `2` | Multiple distinct parallel lines |
| 100000 copies of the same line | `0` | Maximum input size and efficient duplicate handling |

## Edge Cases

### Duplicate descriptions of one line

For

```
1
3
0 0 4 0
4 0 0 0
-2 0 2 0
```

all three pairs describe (y=0). Their normalized line equation is the same canonical triple, so only one entry reaches `direction_count`. There is no perpendicular direction present, and the output is `0`. A solution that counts directions before removing duplicate lines would incorrectly think there are three horizontal lines.

### Reversed endpoints

For

```
1
2
0 0 4 0
4 0 0 0
```

the first direction is `(4,0)` and the second is `(-4,0)`. Both normalize to `(1,0)`. More importantly, both produce the same canonical line equation, so the second input pair is discarded as a duplicate. The answer is `0`.

### Vertical and horizontal lines

For

```
1
2
-20000 20000 20000 20000
20000 -20000 20000 20000
```

the first line is horizontal with direction `(1,0)`, while the second is vertical with direction `(0,1)`. The perpendicular lookup of `(1,0)` produces `(0,1)`, and each direction has frequency one. The product is `1`, which is the correct answer.

### Multiple parallel lines

For

```
1
3
-2 0 2 0
-2 1 2 1
0 -2 0 2
```

the first two lines normalize to the same direction `(1,0)` but have different `C` values in their line equations, so both remain in the set. The vertical line has direction `(0,1)`. The direction frequencies are 2 and 1, producing (2\cdot1=2). The algorithm counts both physical intersections even though the horizontal lines are parallel to each other.

### Large answer

If many distinct horizontal lines and many distinct vertical lines are present, every horizontal line is perpendicular to every vertical line. The answer can approach (n^2/4), which is billions for (n=10^5). The implementation uses Python integers, so the result is represented exactly without overflow.

### Maximum input with identical geometry

With 100000 copies of the same pair, the line set remains of size one even though the input is large. Each subsequent pair is rejected by the set lookup, and the final answer is zero. This case is also a useful practical check that the solution does not accidentally perform work proportional to the number of pairs of input descriptions.
