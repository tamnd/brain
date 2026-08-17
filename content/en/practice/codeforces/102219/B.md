---
title: "CF 102219B - SpongeBob SquarePants"
description: "Each test case describes a four-sided shape with right angles using its width w and height h. Since every such shape is already a rectangle, the only question is whether it is the special kind of rectangle whose two side lengths are equal."
date: "2026-08-17T22:46:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102219
codeforces_index: "B"
codeforces_contest_name: "2019 ICPC Malaysia National"
rating: 0
weight: 102219
solve_time_s: 156
verified: false
draft: false
---

[CF 102219B - SpongeBob SquarePants](https://codeforces.com/problemset/problem/102219/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Problem Understanding

Each test case describes a four-sided shape with right angles using its width `w` and height `h`. Since every such shape is already a rectangle, the only question is whether it is the special kind of rectangle whose two side lengths are equal.

If `w == h`, the shape is a square, so the required answer is `YES`. If the two dimensions differ, the shape is an ordinary rectangle, so the answer is `NO`.

The dimensions are positive integers between `1` and `1,000,000`. The values themselves are small enough to fit comfortably in Python integers, so there is no overflow concern. More importantly, the actual magnitude of the dimensions does not need to influence the algorithm at all. The decision depends only on one equality comparison, giving constant work per test case. Even if the number of test cases is large, a linear scan over the test cases is the natural limit because every pair of dimensions must be read and classified.

The edge cases are simple but still worth handling explicitly. The smallest possible square is `1 1`, which must produce `YES`. A careless implementation that checks whether the dimensions are greater than one could incorrectly reject it.

A shape can have a very large dimension while still being a square. For example, `1000000 1000000` produces `YES`. An implementation that accidentally uses a small fixed bound or treats the maximum value specially would fail even though equality is all that matters.

The order of the dimensions does not matter. For example, `3 7` and `7 3` are both rectangles and both produce `NO`. A comparison such as `w < h` or `w > h` alone does not determine whether the shape is a square, because either ordering is possible.

Finally, dimensions that differ by only one must still be rejected. For `5 6`, the correct output is `NO`. An implementation using an off-by-one condition such as `abs(w - h) <= 1` would incorrectly classify it as a square.

## Approaches

A brute-force solution could imagine the rectangle as a collection of unit cells and inspect the whole shape before deciding whether it is square. For a `w × h` rectangle, that means examining `w * h` cells. The approach is correct because the dimensions completely determine the rectangular grid, so after processing every cell we could compare the resulting width and height. However, with both dimensions equal to `1,000,000`, this requires exactly `1,000,000,000,000` cell inspections for one test case. That is far beyond what a one-second contest program can perform.

The brute-force works because it eventually processes all the information describing the shape, but it fails because almost all of that work is irrelevant. The square condition does not depend on any individual cell. It depends directly on the two side lengths. The observation that a rectangle is a square exactly when its width equals its height reduces the entire problem to one integer comparison.

For every test case, read `w` and `h`, compare them, and print `YES` when they are equal and `NO` otherwise. There is no iteration over the dimensions and no geometric construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(w × h) per test case | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `T`, because the same decision must be made independently for every shape.
2. For each test case, read the width `w` and height `h`.
3. Compare `w` and `h`. Equality is exactly the mathematical condition for a rectangle to be a square, so no other geometric calculation is necessary.
4. Print `YES` if `w == h`; otherwise print `NO`. Each test case produces exactly one output line, preserving the required correspondence between input shapes and answers.

### Why it works

The algorithm relies on the defining property of a square: its width and height are equal. For every test case, if the algorithm prints `YES`, then `w == h`, so the shape has equal side lengths and is a square. If it prints `NO`, then `w != h`, so the side lengths differ and the shape cannot be a square. These two cases cover every possible pair of positive dimensions, so the algorithm cannot classify a valid input incorrectly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        w, h = map(int, input().split())
        print("YES" if w == h else "NO")

if __name__ == "__main__":
    solve()
```

The first line is read as `t`, which controls exactly how many pairs of dimensions are processed. This avoids relying on end-of-file behavior and matches the input format.

Inside the loop, `map(int, input().split())` converts the two dimensions directly into integers. Python integers safely handle the given maximum value of `1,000,000`, so no special numeric type or overflow handling is needed.

The conditional expression performs the same comparison described in the algorithm. There are no boundary cases involving loops over the dimensions, so there are no off-by-one conditions to manage. The equality comparison also treats `1 1` and `1000000 1000000` correctly without any special cases.

Using `sys.stdin.readline` follows the requested fast-input pattern. For this particular problem, input parsing is already tiny compared with most competitive programming tasks, but the approach is appropriate when there can be many test cases.

## Worked Examples

### Sample 1

The four test cases are processed independently.

| Test case | `w` | `h` | `w == h` | Output |
| --- | --- | --- | --- | --- |
| 1 | 9 | 9 | True | `YES` |
| 2 | 16 | 30 | False | `NO` |
| 3 | 200 | 33 | False | `NO` |
| 4 | 547 | 547 | True | `YES` |

The first and fourth shapes have equal dimensions, so they are squares. The middle two have different dimensions, so they are rectangles that do not qualify. The trace demonstrates the central invariant: the output is determined entirely by the equality of the current pair.

### Constructed Sample 2

Consider the input:

```
4
1 1
1 2
999999 1000000
1000000 1000000
```

| Test case | `w` | `h` | `w == h` | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | True | `YES` |
| 2 | 1 | 2 | False | `NO` |
| 3 | 999999 | 1000000 | False | `NO` |
| 4 | 1000000 | 1000000 | True | `YES` |

This trace exercises both ends of the allowed range and also checks the case where the dimensions differ by exactly one. No special handling is required for any of them because the same equality test applies uniformly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires one comparison after reading two integers. |
| Space | O(1) | Only the current dimensions and loop state are stored. |

The dimensions can be as large as `1,000,000`, but their values do not increase the amount of computation. Even for a large number of test cases, the algorithm performs only constant work per case, so its total running time grows linearly with the input size. The memory usage remains constant and is far below the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        w, h = map(int, input().split())
        print("YES" if w == h else "NO")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run(
    """4
9 9
16 30
200 33
547 547
"""
) == """YES
NO
NO
YES
""", "sample 1"

assert run(
    """4
1 1
1 2
999999 1000000
1000000 1000000
"""
) == """YES
NO
NO
YES
""", "minimum and maximum boundaries"

assert run(
    """5
1 1
2 2
5 5
100 100
1000000 1000000
"""
) == """YES
YES
YES
YES
YES
""", "all equal values"

assert run(
    """5
1 2
2 1
999999 1000000
1000000 999999
5 6
"""
) == """NO
NO
NO
NO
NO
""", "off-by-one and reversed dimensions"

assert run(
    """3
1000000 1
1 1000000
999998 1000000
"""
) == """NO
NO
NO
""", "large unequal dimensions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, `1000000 1000000` | `YES`, `YES` | Minimum and maximum valid square sizes |
| Several equal pairs | All `YES` | Equality is sufficient regardless of magnitude |
| `1 2`, `2 1`, `5 6` | All `NO` | Reversed dimensions and off-by-one differences |
| `1000000 1`, `1 1000000` | Both `NO` | Large unequal dimensions at opposite orientations |

## Edge Cases

For the minimum-size shape, the input `1 1` makes the algorithm compare `1 == 1`, which is true, so it prints `YES`. There is no geometric reason to exclude a square of side length one, and the algorithm correctly accepts it without a special condition.

For the maximum-size square, the input `1000000 1000000` also produces `YES`. The comparison remains a constant-time integer operation regardless of the numerical size of the values, so the upper bound creates no performance or correctness issue.

For dimensions that differ by one, the input `5 6` gives `5 == 6`, which is false, so the output is `NO`. The algorithm does not confuse "almost equal" dimensions with equal dimensions, avoiding the common off-by-one mistake.

For reversed dimensions, `7 3` produces `NO` because `7 != 3`, and `3 7` also produces `NO` because `3 != 7`. A square has equal dimensions in either orientation, so there is no reason to normalize the pair using `min` and `max` before comparing it.

The algorithm handles every edge case through the same invariant, namely that `YES` is printed exactly when the two side lengths are identical. No additional geometric calculations or special-case branches are necessary.
