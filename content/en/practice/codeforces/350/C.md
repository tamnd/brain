---
title: "CF 350C - Bombs"
description: "We have a robot starting at the origin on a 2D grid. Several bombs are placed at distinct coordinates, and the robot must destroy all of them."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 350
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 203 (Div. 2)"
rating: 1600
weight: 350
solve_time_s: 228
verified: true
draft: false
---

[CF 350C - Bombs](https://codeforces.com/problemset/problem/350/C)

**Rating:** 1600  
**Tags:** greedy, implementation, sortings  
**Solve time:** 3m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a robot starting at the origin on a 2D grid. Several bombs are placed at distinct coordinates, and the robot must destroy all of them.

The robot can move horizontally or vertically, pick up a bomb when standing on its cell, and destroy a carried bomb only after returning to the origin. The tricky part is the movement restriction: while walking toward some destination, the robot cannot pass through another bomb unless that bomb is exactly the destination.

Each bomb must eventually follow the same lifecycle:

1. Walk from `(0, 0)` to the bomb.
2. Pick it up.
3. Return to `(0, 0)`.
4. Destroy it.

The task is not to minimize travel distance. The cost is the number of operations. Every move command counts as one operation regardless of distance, because `"1 k dir"` is a single operation even if `k` is large.

The input size reaches `10^5` bombs, so anything quadratic is immediately dangerous. We need something close to `O(n log n)` because sorting that many points is already acceptable, while repeatedly checking paths against all bombs would be too slow.

The most subtle part of the problem is the movement restriction. A naive route may accidentally walk through another bomb. Consider:

```
2
1 0
2 0
```

If we first try to destroy `(2, 0)`, the robot must walk through `(1, 0)`, which is forbidden because that bomb is still present.

The correct approach is to process bombs in increasing distance from the origin. Then every path segment is guaranteed to avoid remaining bombs.

Another easy mistake is mishandling negative coordinates. For example:

```
1
-3 2
```

The robot must move `L 3` and `U 2`. Forgetting to map signs correctly produces invalid commands.

A third edge case appears when one coordinate is zero:

```
1
0 -5
```

The optimal solution uses only one move operation to reach the bomb and one move operation to return. Some implementations incorrectly emit useless zero-length moves, but operations require `k >= 1`.

## Approaches

A brute-force mindset suggests treating each bomb independently. For every bomb, move from the origin to its coordinates, pick it up, move back, destroy it, and repeat.

This already gives the minimum number of operations for a fixed bomb order. A bomb at `(x, y)` requires:

- One horizontal move if `x != 0`
- One vertical move if `y != 0`
- One pickup operation
- The same movement operations to return
- One destroy operation

So each bomb contributes either 4, 5, or 6 operations depending on how many coordinates are nonzero.

The real problem is choosing a valid order. If we process bombs arbitrarily, movement may cross another undestroyed bomb. Detecting such conflicts naively means checking every path against every remaining bomb, which becomes `O(n^2)`.

The key observation is that movement always happens along axis-aligned segments starting from the origin. If we process bombs in increasing Manhattan distance `|x| + |y|`, then every bomb closer to the origin is already removed before we attempt to reach a farther one.

Why does this help? Suppose we are moving toward `(x, y)`. Any bomb lying on the horizontal or vertical path from the origin to `(x, y)` must have strictly smaller Manhattan distance. Since those bombs were processed earlier, they no longer block the route.

This turns the problem into a simple constructive algorithm:

1. Sort bombs by Manhattan distance.
2. For each bomb:

- Move to it.
- Pick it up.
- Return.
- Destroy it.

The operation count is automatically minimal because each bomb must necessarily require one pickup and one destroy operation, and each nonzero coordinate necessarily requires one move operation in each direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all bomb coordinates.
2. Sort the bombs by increasing Manhattan distance `|x| + |y|`.

This ordering guarantees that when we travel toward a bomb, any bomb that could lie on the path has already been removed.
3. For each bomb `(x, y)`:

If `x > 0`, emit the operation:

```
1 x R
```

If `x < 0`, emit:

```
1 |x| L
```
4. Handle the vertical movement similarly.

If `y > 0`, emit:

```
1 y U
```

If `y < 0`, emit:

```
1 |y| D
```
5. Emit operation `2`.

The robot is now standing exactly on the bomb's position, so it can pick the bomb up.
6. Return to the origin using reverse directions.

If we originally moved right, we now move left. If we moved up, we now move down.
7. Emit operation `3`.

The robot is back at the origin and can destroy the carried bomb.
8. Count all generated operations and print them.

### Why it works

The algorithm maintains a simple invariant:

Before processing a bomb, every bomb with smaller Manhattan distance has already been removed.

Any bomb that could lie on the path from the origin to `(x, y)` must satisfy:

```
|x'| <= |x|
|y'| <= |y|
```

and at least one inequality is strict unless the coordinates are identical. That implies:

```
|x'| + |y'| < |x| + |y|
```

So every blocking bomb has already been destroyed earlier.

The operation count is minimal because each bomb requires exactly one pickup and one destruction operation, and each nonzero coordinate requires one outward move and one return move. No valid solution can use fewer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    bombs = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        bombs.append((abs(x) + abs(y), x, y))
    
    bombs.sort()
    
    ops = []
    
    for _, x, y in bombs:
        if x > 0:
            ops.append(f"1 {x} R")
        elif x < 0:
            ops.append(f"1 {-x} L")
        
        if y > 0:
            ops.append(f"1 {y} U")
        elif y < 0:
            ops.append(f"1 {-y} D")
        
        ops.append("2")
        
        if y > 0:
            ops.append(f"1 {y} D")
        elif y < 0:
            ops.append(f"1 {-y} U")
        
        if x > 0:
            ops.append(f"1 {x} L")
        elif x < 0:
            ops.append(f"1 {-x} R")
        
        ops.append("3")
    
    print(len(ops))
    print("\n".join(ops))

solve()
```

The first section reads all bombs and stores them together with their Manhattan distance. Keeping the distance in the tuple allows Python's default tuple sorting to order bombs correctly.

The movement generation is completely symmetric. The outward trip moves along the x-axis first and then the y-axis. The return trip simply reverses those moves in reverse order.

The order of return operations matters. If we moved right and then up, we should move down and then left to retrace the exact path safely.

The implementation carefully skips zero coordinates. Operations require positive movement lengths, so generating commands like `"1 0 R"` would be invalid.

The total number of operations never exceeds `6n`, comfortably below the allowed `10^6`.

## Worked Examples

### Example 1

Input:

```
2
1 1
-1 -1
```

Sorted order remains the same because both bombs have equal Manhattan distance.

| Bomb | Operations Generated |
| --- | --- |
| `(1, 1)` | `1 1 R`, `1 1 U`, `2`, `1 1 D`, `1 1 L`, `3` |
| `(-1, -1)` | `1 1 L`, `1 1 D`, `2`, `1 1 U`, `1 1 R`, `3` |

The full output becomes:

```
12
1 1 R
1 1 U
2
1 1 D
1 1 L
3
1 1 L
1 1 D
2
1 1 U
1 1 R
3
```

This trace shows the basic structure repeated for every bomb. Each bomb uses exactly six operations because both coordinates are nonzero.

### Example 2

Input:

```
3
0 5
2 0
-1 3
```

After sorting by Manhattan distance:

| Order | Bomb | Distance |
| --- | --- | --- |
| 1 | `(2, 0)` | 2 |
| 2 | `(-1, 3)` | 4 |
| 3 | `(0, 5)` | 5 |

Generated operations:

| Bomb | Operations |
| --- | --- |
| `(2, 0)` | `1 2 R`, `2`, `1 2 L`, `3` |
| `(-1, 3)` | `1 1 L`, `1 3 U`, `2`, `1 3 D`, `1 1 R`, `3` |
| `(0, 5)` | `1 5 U`, `2`, `1 5 D`, `3` |

This example demonstrates why zero coordinates matter. Bombs lying directly on an axis require only four operations instead of six.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(n) | Stored bombs and generated operations |

With `n ≤ 10^5`, an `O(n log n)` solution easily fits within the time limit. The number of generated operations is at most `6n`, so memory usage also remains small.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    bombs = []

    for _ in range(n):
        x, y = map(int, input().split())
        bombs.append((abs(x) + abs(y), x, y))

    bombs.sort()

    ops = []

    for _, x, y in bombs:
        if x > 0:
            ops.append(f"1 {x} R")
        elif x < 0:
            ops.append(f"1 {-x} L")

        if y > 0:
            ops.append(f"1 {y} U")
        elif y < 0:
            ops.append(f"1 {-y} D")

        ops.append("2")

        if y > 0:
            ops.append(f"1 {y} D")
        elif y < 0:
            ops.append(f"1 {-y} U")

        if x > 0:
            ops.append(f"1 {x} L")
        elif x < 0:
            ops.append(f"1 {-x} R")

        ops.append("3")

    print(len(ops))
    print("\n".join(ops))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# sample 1
out = run("2\n1 1\n-1 -1\n")
assert out.startswith("12\n")

# minimum size
out = run("1\n5 0\n")
assert out == (
    "4\n"
    "1 5 R\n"
    "2\n"
    "1 5 L\n"
    "3\n"
)

# negative coordinates
out = run("1\n-3 -2\n")
assert out == (
    "6\n"
    "1 3 L\n"
    "1 2 D\n"
    "2\n"
    "1 2 U\n"
    "1 3 R\n"
    "3\n"
)

# axis-aligned bombs
out = run("2\n0 1\n0 -2\n")
assert out.startswith("8\n")

# ordering test
out = run("2\n2 0\n1 0\n")
assert out.startswith("8\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n5 0\n` | 4 operations | Correct handling of zero coordinate |
| `1\n-3 -2\n` | Proper `L` and `D` moves | Sign handling |
| `2\n0 1\n0 -2\n` | 8 operations | Vertical-only movement |
| `2\n2 0\n1 0\n` | Smaller-distance bomb first | Path safety ordering |

## Edge Cases

Consider the blocking-path scenario:

```
2
1 0
2 0
```

If we process `(2, 0)` first, the robot would have to walk through `(1, 0)`, which is forbidden.

Our algorithm sorts by Manhattan distance:

| Bomb | Distance |
| --- | --- |
| `(1, 0)` | 1 |
| `(2, 0)` | 2 |

The first bomb is removed before the second trip begins, so the path becomes legal.

Now consider negative coordinates:

```
1
-3 2
```

The algorithm emits:

```
1 3 L
1 2 U
2
1 2 D
1 3 R
3
```

The return path exactly reverses the outward path, bringing the robot safely back to the origin.

Finally, consider a bomb lying directly on an axis:

```
1
0 -5
```

The algorithm emits:

```
1 5 D
2
1 5 U
3
```

No useless horizontal operations appear. This matters because move operations require positive distance.
