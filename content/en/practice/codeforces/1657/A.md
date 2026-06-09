---
title: "CF 1657A - Integer Moves"
description: "We start with a chip at the origin (0, 0) and want to reach a target point (x, y). A move is allowed whenever the Euclidean distance between the current position and the next position is an integer. The task is to find the minimum number of moves needed to reach the target."
date: "2026-06-10T03:27:33+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1657
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 125 (Rated for Div. 2)"
rating: 800
weight: 1657
solve_time_s: 99
verified: true
draft: false
---

[CF 1657A - Integer Moves](https://codeforces.com/problemset/problem/1657/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a chip at the origin `(0, 0)` and want to reach a target point `(x, y)`.

A move is allowed whenever the Euclidean distance between the current position and the next position is an integer. The task is to find the minimum number of moves needed to reach the target.

The coordinates are very small, at most `50`, and there are at most `3000` test cases. Even a somewhat inefficient solution would fit comfortably within the limits. Still, the problem has a simple mathematical observation that reduces everything to constant time per test case.

The key quantity is the distance from the origin to the destination:

$$d = \sqrt{x^2 + y^2}$$

If this distance is already an integer, we can move directly from `(0,0)` to `(x,y)` in one operation.

A special case appears when the destination itself is the origin. If `(x,y) = (0,0)`, no movement is required, so the answer is `0`.

The main subtlety is understanding what happens when the distance is not an integer. A careless solution might think that more than two moves could sometimes be necessary. For example:

Input:

```
1
9 15
```

The distance is

$$\sqrt{9^2+15^2}=\sqrt{306}$$

which is not an integer. Direct movement is impossible, but the correct answer is still `2`, not some larger number.

Another easy mistake is forgetting the origin case:

Input:

```
1
0 0
```

Output:

```
0
```

The distance is an integer (`0`), but the minimum number of moves is not `1`, because we are already at the destination.

## Approaches

A brute-force way to think about the problem is to search for intermediate points. If the destination cannot be reached directly, we could try every lattice point `(a,b)` and check whether both distances

$$\sqrt{a^2+b^2}$$

and

$$\sqrt{(x-a)^2+(y-b)^2}$$

are integers.

Because coordinates are at most `50`, such a search would actually be fast enough here. We would examine a few thousand candidate points per test case and stop when a valid intermediate point is found.

The brute-force idea works because the coordinates are tiny, but it completely misses the underlying structure.

The crucial observation is that every non-origin point can always be reached in at most two moves.

Suppose the target is `(x,y)` and its distance from the origin is not an integer. We cannot reach it in one move.

However, we can first move from `(0,0)` to `(0,0)` plus some point at integer distance from the origin, for example `(x,0)` if `x > 0`, or any other suitable lattice point. More generally, a stronger geometric fact holds: every point in the plane can be expressed as the sum of two vectors whose lengths are integers. For lattice points, two moves are always sufficient.

Since one move is possible exactly when the distance from the origin is an integer, and otherwise two moves always suffice, only three answers can ever occur:

`0`, `1`, or `2`.

That turns the problem into a simple classification based on `x² + y²`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C²) per test case | O(1) | Accepted but unnecessary |
| Optimal | O(1) per test case | O(1) | Accepted |

Here `C` denotes the coordinate bound.

## Algorithm Walkthrough

1. Read the target coordinates `(x, y)`.
2. If `x == 0` and `y == 0`, output `0`.

We are already at the destination, so no move is needed.
3. Compute

$$s = x^2 + y^2$$

The distance from the origin is `√s`.
4. Check whether `s` is a perfect square.

If it is, then `√s` is an integer, so a direct move from `(0,0)` to `(x,y)` is legal.
5. If `s` is a perfect square, output `1`.
6. Otherwise, output `2`.

One move is impossible because the distance is not an integer, and two moves are always sufficient.

### Why it works

The answer can never exceed `2`.

If the destination is the origin, the minimum is clearly `0`.

For any other point, if `x² + y²` is a perfect square, then the distance from `(0,0)` to `(x,y)` is an integer. A direct move exists, so the answer is `1`.

If `x² + y²` is not a perfect square, a direct move is impossible. The known geometric property used in the official solution is that every lattice point can be reached in two integer-length moves. Since one move cannot work and two moves always can, the minimum is exactly `2`.

These three cases are mutually exclusive and cover all inputs, so the algorithm is correct.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

t = int(input())

for _ in range(t):
    x, y = map(int, input().split())

    if x == 0 and y == 0:
        print(0)
        continue

    s = x * x + y * y
    r = isqrt(s)

    if r * r == s:
        print(1)
    else:
        print(2)
```

The first branch handles the origin. Without it, `(0,0)` would incorrectly be classified as requiring one move because `0` is a perfect square.

The variable `s` stores the squared distance. Working with squared distances avoids floating-point arithmetic entirely.

`isqrt(s)` returns the integer floor of `√s`. A number is a perfect square exactly when `isqrt(s)^2 == s`.

Once we know whether the distance is an integer, the answer follows directly from the three-case classification described earlier.

## Worked Examples

### Example 1

Input:

```
8 6
```

| Step | x | y | s = x²+y² | isqrt(s) | Perfect Square? | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Read input | 8 | 6 | 100 | 10 | Yes | 1 |

The squared distance is `100`, which is `10²`. The distance is an integer, so one direct move reaches the target.

### Example 2

Input:

```
9 15
```

| Step | x | y | s = x²+y² | isqrt(s) | Perfect Square? | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Read input | 9 | 15 | 306 | 17 | No | 2 |

The squared distance is `306`. Since `17² = 289` and `18² = 324`, it is not a perfect square.

A direct move is impossible, so the answer becomes `2`.

This example demonstrates the key distinction between "distance exists" and "distance is an integer". Only the latter allows a single move.

### Example 3

Input:

```
0 0
```

| Step | x | y | Special Case? | Answer |
| --- | --- | --- | --- | --- |
| Read input | 0 | 0 | Yes | 0 |

This confirms the special handling of the origin.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Constant amount of arithmetic per test case |
| Space | O(1) | Only a few integer variables are stored |

Even with `3000` test cases, the program performs only a few thousand arithmetic operations. The running time and memory usage are far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isqrt

def solve():
    input = sys.stdin.readline
    t = int(input())

    ans = []
    for _ in range(t):
        x, y = map(int, input().split())

        if x == 0 and y == 0:
            ans.append("0")
            continue

        s = x * x + y * y
        r = isqrt(s)

        ans.append("1" if r * r == s else "2")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run(
"""3
8 6
0 0
9 15
"""
) == "1\n0\n2"

# origin
assert run(
"""1
0 0
"""
) == "0"

# classic Pythagorean triple
assert run(
"""1
3 4
"""
) == "1"

# non-perfect-square distance
assert run(
"""1
1 1
"""
) == "2"

# maximum coordinates
assert run(
"""1
50 50
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0` | Destination already reached |
| `3 4` | `1` | Integer distance via Pythagorean triple |
| `1 1` | `2` | Non-square distance requires two moves |
| `50 50` | `2` | Largest coordinates in the constraints |

## Edge Cases

Consider the destination already being the origin.

Input:

```
1
0 0
```

The algorithm enters the special-case branch immediately and outputs `0`. This avoids the common mistake of treating distance `0` as an ordinary integer distance and returning `1`.

Consider a point whose distance is an integer.

Input:

```
1
24 7
```

The squared distance is

$$24^2+7^2=576+49=625$$

Since `625 = 25²`, the algorithm outputs `1`. A direct move of length `25` is legal.

Consider a point whose distance is not an integer.

Input:

```
1
1 1
```

The squared distance is `2`, which is not a perfect square. The perfect-square test fails, and the algorithm outputs `2`.

This is exactly correct because one move is impossible while two moves are always sufficient.

Consider a boundary-value input.

Input:

```
1
50 50
```

The squared distance is

$$50^2+50^2=5000$$

`5000` is not a perfect square, so the algorithm outputs `2`. The size of the coordinates does not change the reasoning, showing that the solution handles the entire allowed range uniformly.
