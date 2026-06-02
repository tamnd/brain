---
title: "CF 171H - A polyline"
description: "The input contains two numbers. The first number, a, determines the order of a recursively constructed polyline. The second number, b, is an index along that polyline. The picture in the statement is the key."
date: "2026-06-02T08:52:57+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 171
codeforces_index: "H"
codeforces_contest_name: "April Fools Day Contest"
rating: 1700
weight: 171
solve_time_s: 99
verified: true
draft: false
---

[CF 171H - A polyline](https://codeforces.com/problemset/problem/171/H)

**Rating:** 1700  
**Tags:** *special, implementation  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The input contains two numbers. The first number, `a`, determines the order of a recursively constructed polyline. The second number, `b`, is an index along that polyline.

The picture in the statement is the key. It is the classical Hilbert curve, a space-filling curve that visits every cell of a `2^a × 2^a` grid exactly once. The cells are numbered in the order in which the curve passes through them. Given the order `a` and a position `b` on the curve, we must recover the coordinates of the corresponding grid cell.

The constraint `a ≤ 10` is extremely small. The grid side length is at most `2^10 = 1024`, so the total number of cells is at most `2^20 = 1,048,576`. Even a recursive or bit-by-bit construction is trivial within the limits.

The main difficulty is not efficiency. The challenge is recognizing the structure encoded by the picture and correctly handling the rotations and reflections that occur inside each recursive quadrant of the Hilbert curve.

A common mistake is to treat the numbering as simple row-major order or Morton order. For example:

Input

```
2 15
```

The answer is

```
3 0
```

A row-major interpretation would produce `(3,3)`, which is incorrect because the Hilbert curve changes orientation between quadrants.

Another easy place to make a mistake is the recursive orientation handling. For example:

Input

```
4 160
```

The answer is

```
12 12
```

A solution that enters the correct quadrant but forgets the required rotation will reach the wrong cell even though all higher-level decisions are correct.

## Approaches

A brute-force approach would explicitly generate the entire Hilbert curve of order `a`, store every visited coordinate, and then output the `b`-th one.

This works because the largest curve contains only about one million cells. Generating all of them is feasible. The method is also easy to justify: if we literally construct the curve in visit order, the answer is simply the `b`-th generated point.

The weakness is that we are solving a direct indexing problem by constructing the entire object. We only need one cell, yet we generate every cell.

The recursive structure of the Hilbert curve gives a much cleaner solution. A Hilbert curve of order `a` consists of four Hilbert curves of order `a-1`, each occupying one quadrant. The index `b` immediately tells us which quadrant contains the answer. After identifying the quadrant, we remove the contribution of all previous quadrants and continue recursively inside the selected one.

The only complication is that each quadrant may be rotated or reflected relative to the parent. Once those transformations are handled correctly, every recursion level processes exactly one pair of bits from the index.

This leads to the standard Hilbert index-to-coordinate conversion algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force generation | O(4^a) | O(4^a) | Accepted but unnecessary |
| Optimal Hilbert decoding | O(a) | O(1) | Accepted |

## Algorithm Walkthrough

1. Let `n = 2^a`. We want the coordinates of cell number `b` inside an `n × n` grid.
2. Process the Hilbert index from the lowest recursion level upward.
3. At a level whose square size is `s × s`, determine two bits:

`rx` and `ry`.

These bits identify which subquadrant contains the target cell.
4. Before moving into the chosen quadrant, apply the Hilbert orientation rule.

If `ry = 0`, the current square must be rotated. If additionally `rx = 1`, the coordinates are reflected before the rotation.
5. After the transformation, add the quadrant offset:

`x += s * rx`

and

`y += s * ry`.
6. Remove the two processed bits from the index by dividing by four.
7. Double `s` and continue until all recursion levels have been processed.
8. Output the final `(x, y)`.

### Why it works

The Hilbert curve is defined recursively. At every order, the square is split into four equal quadrants. The traversal order of those quadrants is fixed, but each quadrant contains a rotated version of a smaller Hilbert curve.

The algorithm maintains the invariant that after processing a level, `(x, y)` is the correct position inside the already reconstructed portion of the curve. The rotation and reflection rules exactly match the way the Hilbert curve connects its four child curves. Since each iteration decodes one recursion level and preserves this invariant, after all `a` levels have been processed the resulting coordinates are precisely the cell visited at index `b`.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = map(int, input().split())

n = 1 << a

x = 0
y = 0
t = b
s = 1

while s < n:
    rx = (t // 2) & 1
    ry = (t ^ rx) & 1

    if ry == 0:
        if rx == 1:
            x = s - 1 - x
            y = s - 1 - y
        x, y = y, x

    x += s * rx
    y += s * ry

    t //= 4
    s <<= 1

print(x, y)
```

The variable `t` stores the remaining portion of the Hilbert index that has not yet been decoded. Each iteration consumes two bits because every recursion level chooses one of four quadrants.

The values `rx` and `ry` identify the selected quadrant. The orientation correction must happen before adding the quadrant offset. Reversing this order produces incorrect coordinates because the rotation is defined inside the local coordinate system of the current square.

The reflection step uses `s - 1 - x` and `s - 1 - y`. The `-1` is essential. Forgetting it shifts every coordinate by one cell and breaks the recursion.

No overflow concerns exist because coordinates never exceed `1023`.

## Worked Examples

### Example 1

Input

```
1 0
```

| s | t | rx | ry | x | y |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 0 |

Output:

```
0 0
```

This is the first cell visited by the order-1 Hilbert curve.

### Example 2

Input

```
2 15
```

| s | t | rx | ry | x | y |
| --- | --- | --- | --- | --- | --- |
| 1 | 15 | 1 | 0 | 1 | 0 |
| 2 | 3 | 1 | 0 | 3 | 0 |

Output:

```
3 0
```

This example demonstrates why orientation matters. The last Hilbert index in a `4 × 4` grid is not `(3,3)`. The recursive rotations place it at `(3,0)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(a) | One iteration per recursion level |
| Space | O(1) | Only a few integer variables are stored |

Since `a ≤ 10`, the loop runs at most ten times. The solution is effectively instantaneous and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    a, b = map(int, input().split())

    n = 1 << a
    x = y = 0
    t = b
    s = 1

    while s < n:
        rx = (t // 2) & 1
        ry = (t ^ rx) & 1

        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            x, y = y, x

        x += s * rx
        y += s * ry

        t //= 4
        s <<= 1

    print(x, y)

def run(inp: str) -> str:
    global input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old
    return out.getvalue().strip()

# provided samples
assert run("1 0\n") == "0 0", "sample 1"
assert run("2 15\n") == "3 0", "sample 2"
assert run("4 160\n") == "12 12", "sample 3"

# custom cases
assert run("1 1\n") == "0 1", "second cell of order 1"
assert run("1 3\n") == "1 0", "last cell of order 1"
assert run("10 0\n") == "0 0", "minimum index at maximum order"
assert run("10 1048575\n") == "1023 0", "last index of largest grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0 1` | Correct first rotation |
| `1 3` | `1 0` | End of smallest nontrivial curve |
| `10 0` | `0 0` | Maximum order, minimum index |
| `10 1048575` | `1023 0` | Maximum order, maximum index |

## Edge Cases

Consider:

```
1 0
```

The loop executes exactly one level. Both quadrant bits are zero, no offset is added, and the result remains `(0,0)`. This confirms correct handling of the smallest possible index.

Consider:

```
2 15
```

At both recursion levels we enter the fourth Hilbert quadrant. The algorithm performs the required reflection and rotation before adding offsets. Skipping that transformation would incorrectly end at `(3,3)`. The correct output is `(3,0)`.

Consider:

```
10 1048575
```

This is the largest valid index. Every recursion level chooses the final quadrant. The algorithm still performs only ten iterations and returns `(1023,0)`, showing that the implementation handles the upper bound without any special cases.
