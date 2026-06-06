---
title: "CF 404B - Marathon"
description: "Valera runs around the perimeter of a square stadium. The square has side length a, and the route follows the boundary in counterclockwise order. The starting point is the bottom-left corner (0, 0)."
date: "2026-06-07T01:27:58+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 404
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 237 (Div. 2)"
rating: 1500
weight: 404
solve_time_s: 260
verified: true
draft: false
---

[CF 404B - Marathon](https://codeforces.com/problemset/problem/404/B)

**Rating:** 1500  
**Tags:** implementation, math  
**Solve time:** 4m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

Valera runs around the perimeter of a square stadium. The square has side length `a`, and the route follows the boundary in counterclockwise order.

The starting point is the bottom-left corner `(0, 0)`. After running `a` meters he reaches `(a, 0)`, after another `a` meters he reaches `(a, a)`, and so on. The total perimeter is `4a`, so after every full lap he returns to `(0, 0)` and continues repeating the same path.

The coach gives Valera a drink every `d` meters. We must output Valera's coordinates after he has run `d`, `2d`, `3d`, ..., `nd` meters.

The key observation is that only the position along the current lap matters. If Valera has run a total distance `s`, then his location is determined by `s mod (4a)`, because every complete perimeter returns him to exactly the same place.

The constraints are large enough that we must generate up to `10^5` answers. Any solution that simulates movement meter by meter is impossible. Even if distances are represented as real numbers, a tiny-step simulation would require billions of operations in the worst case. We need a direct formula that computes each answer in constant time.

Several edge cases can easily cause wrong answers.

Consider:

```
a = 2
d = 2
n = 1
```

After running exactly `2` meters, Valera is at `(2, 0)`, the first corner. A careless implementation using strict inequalities may place him on the next edge instead.

Another example:

```
a = 3
d = 12
n = 1
```

Since `12 = 4a`, he completes exactly one lap and returns to `(0, 0)`. If we forget to take modulo `4a`, we may incorrectly try to locate him beyond the perimeter.

A more subtle case is:

```
a = 2
d = 5
n = 1
```

The perimeter is `8`, so `5 mod 8 = 5`. Distance `5` lies on the top edge. The correct position is `(1, 2)`. A solution that assumes only one lap or computes edge transitions incorrectly will fail here.

## Approaches

The most direct idea is to simulate the run. For every drink event we could start at `(0,0)` and repeatedly move along edges until covering the required distance. This is correct because it follows the path exactly.

The problem is scale. Distances can be as large as `10^5`, and there are up to `10^5` queries. Simulating movement incrementally would require far too many operations. Even processing each query by repeatedly subtracting side lengths is unnecessary work.

The structure of the path gives a much simpler solution. The stadium boundary is a cycle of length `4a`. After every full lap the runner returns to the same position. For the `i`-th drink, the total distance traveled is

$$s=i\cdot d$$

Only

$$r=s\bmod (4a)$$

matters.

Now the perimeter is divided into four segments of length `a`.

If `r` belongs to the first segment, Valera is on the bottom edge.

If `r` belongs to the second segment, he is on the right edge.

If `r` belongs to the third segment, he is on the top edge.

If `r` belongs to the fourth segment, he is on the left edge.

Each case gives coordinates through a simple formula. Since every query is handled independently in constant time, the whole solution runs in `O(n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · distance) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the perimeter length `p = 4 * a`.
2. Maintain the total traveled distance after each drink. Instead of recomputing `i * d`, we can keep a running value:

`cur = (cur + d) mod p`.

After the `i`-th iteration, `cur` equals `(i*d) mod p`.
3. Determine on which side of the square `cur` lies.

If `0 <= cur <= a`, the runner is on the bottom edge.

If `a < cur <= 2a`, the runner is on the right edge.

If `2a < cur <= 3a`, the runner is on the top edge.

Otherwise he is on the left edge.
4. Convert the distance along that edge into coordinates.

For the bottom edge:

$$(x,y)=(cur,0)$$

For the right edge:

$$(x,y)=(a,cur-a)$$

For the top edge:

$$(x,y)=(a-(cur-2a),a)$$

For the left edge:

$$(x,y)=(0,a-(cur-3a))$$
5. Output the coordinates.

### Why it works

At any moment, the runner's location depends only on how far he has progressed through the current lap. Taking modulo `4a` removes all completed laps while preserving the exact position on the perimeter.

The interval decomposition of `[0,4a)` matches the four sides of the square. Within each interval, movement occurs along a single straight edge at unit speed, so the coordinate formulas describe the unique point whose distance from the start along the perimeter equals `cur`. Since every possible value of `cur` belongs to exactly one edge, the algorithm always produces the correct position.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, d = map(float, input().split())
n = int(input())

perimeter = 4.0 * a
cur = 0.0

out = []

for _ in range(n):
    cur = (cur + d) % perimeter

    if cur <= a:
        x = cur
        y = 0.0
    elif cur <= 2.0 * a:
        x = a
        y = cur - a
    elif cur <= 3.0 * a:
        x = 3.0 * a - cur
        y = a
    else:
        x = 0.0
        y = 4.0 * a - cur

    out.append(f"{x:.10f} {y:.10f}")

sys.stdout.write("\n".join(out))
```

The first part reads the square side length and drink interval. The perimeter is computed once because it is reused for every query.

The variable `cur` stores the current distance along the perimeter after removing completed laps. Updating it with

```
cur = (cur + d) % perimeter
```

avoids repeatedly computing `i * d` and keeps values numerically small.

The four conditional branches correspond directly to the four sides of the square. The formulas are derived from how far the runner has progressed along the current edge.

One subtle point is handling corner positions. Using `<=` keeps distances exactly equal to `a`, `2a`, or `3a` on a single well-defined side. The coordinates are identical regardless of which adjacent side is chosen, so this avoids ambiguity.

The output volume is large, up to `10^5` lines. Collecting answers in a list and printing once is much faster than writing line by line.

## Worked Examples

### Example 1

Input:

```
2 5
2
```

Perimeter = 8.

| Drink # | cur = distance mod 8 | Side | Coordinates |
| --- | --- | --- | --- |
| 1 | 5 | Top | (1, 2) |
| 2 | 2 | Bottom | (2, 0) |

Output:

```
1.0000000000 2.0000000000
2.0000000000 0.0000000000
```

The first drink occurs after crossing two corners and reaching the top edge. The second drink happens after one complete lap plus two additional meters, placing Valera at `(2,0)`.

### Example 2

Input:

```
3 4
4
```

Perimeter = 12.

| Drink # | cur | Side | Coordinates |
| --- | --- | --- | --- |
| 1 | 4 | Right | (3, 1) |
| 2 | 8 | Top | (1, 3) |
| 3 | 0 | Bottom corner | (0, 0) |
| 4 | 4 | Right | (3, 1) |

This trace demonstrates the cyclic nature of the route. After exactly one perimeter length, `cur` becomes zero and the runner returns to the start.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Constant work for each of the `n` drink positions |
| Space | O(1) auxiliary, O(n) output storage | Only a few variables are used besides the output buffer |

With at most `10^5` queries, an `O(n)` solution performs comfortably within the limits. The memory usage is also small, even when storing all output lines before printing.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    a, d = map(float, input().split())
    n = int(input())

    perimeter = 4.0 * a
    cur = 0.0

    out = []

    for _ in range(n):
        cur = (cur + d) % perimeter

        if cur <= a:
            x, y = cur, 0.0
        elif cur <= 2.0 * a:
            x, y = a, cur - a
        elif cur <= 3.0 * a:
            x, y = 3.0 * a - cur, a
        else:
            x, y = 0.0, 4.0 * a - cur

        out.append(f"{x:.10f} {y:.10f}")

    return "\n".join(out)

# provided sample
assert run("2 5\n2\n") == (
    "1.0000000000 2.0000000000\n"
    "2.0000000000 0.0000000000"
)

# minimum-size input
assert run("1 1\n1\n") == "1.0000000000 0.0000000000"

# exactly one full lap
assert run("3 12\n1\n") == "0.0000000000 0.0000000000"

# corner transitions
assert run("2 2\n4\n") == (
    "2.0000000000 0.0000000000\n"
    "2.0000000000 2.0000000000\n"
    "0.0000000000 2.0000000000\n"
    "0.0000000000 0.0000000000"
)

# repeated cycling
assert run("3 4\n4\n") == (
    "3.0000000000 1.0000000000\n"
    "1.0000000000 3.0000000000\n"
    "0.0000000000 0.0000000000\n"
    "3.0000000000 1.0000000000"
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `(1,0)` | Minimum valid instance |
| `3 12 / 1` | `(0,0)` | Exact perimeter multiple |
| `2 2 / 4` | Four corners in order | Boundary handling |
| `3 4 / 4` | Position repeats after one lap | Correct modulo logic |

## Edge Cases

### Landing exactly on a corner

Input:

```
2 2
1
```

The perimeter position is `2`, which equals the side length. The algorithm enters the first branch (`cur <= a`) and outputs:

```
2.0000000000 0.0000000000
```

This is the correct corner. Any neighboring-edge interpretation would produce the same coordinates, so the result is unambiguous.

### Distance equal to a full perimeter

Input:

```
3 12
1
```

The perimeter is `12`.

The algorithm computes:

```
cur = 12 mod 12 = 0
```

Since `cur = 0`, the coordinates become:

```
0.0000000000 0.0000000000
```

The runner has completed one entire lap and returned to the start.

### Large distances spanning many laps

Input:

```
2 21
1
```

The perimeter is `8`.

The algorithm computes:

```
cur = 21 mod 8 = 5
```

Since `5` lies between `4` and `6`, the runner is on the top edge.

Coordinates:

```
x = 6 - 5 = 1
y = 2
```

Output:

```
1.0000000000 2.0000000000
```

Only the remainder matters. The twenty meters from completed laps have no effect on the final location.

### Repeated wrap-around

Input:

```
2 7
3
```

Perimeter = 8.

The sequence of remainders is:

```
7, 6, 5
```

producing:

```
0 1
0 2
1 2
```

The algorithm never tracks complete laps explicitly. The modulo operation keeps every query mapped into the current perimeter cycle, which is exactly the information needed to determine the position.
