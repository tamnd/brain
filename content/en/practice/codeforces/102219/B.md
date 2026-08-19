---
title: "CF 102219B - SpongeBob SquarePants"
description: "Each test case describes a four-sided shape with right angles using its width w and height h. Since every such shape is already a rectangle, the only question is whether its two dimensions are equal."
date: "2026-08-20T03:44:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102219
codeforces_index: "B"
codeforces_contest_name: "2019 ICPC Malaysia National"
rating: 0
weight: 102219
solve_time_s: 274
verified: false
draft: false
---

[CF 102219B - SpongeBob SquarePants](https://codeforces.com/problemset/problem/102219/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 34s  
**Verified:** no  

## Solution
## Problem Understanding

Each test case describes a four-sided shape with right angles using its width `w` and height `h`. Since every such shape is already a rectangle, the only question is whether its two dimensions are equal. A square has the same width and height, while a non-square rectangle has different dimensions.

For every test case, we print `YES` when `w == h`, because the shape can be a square, and `NO` otherwise.

The dimensions are positive integers between `1` and `1,000,000`. Even at the largest possible values, comparing two integers is a constant-time operation, so the numerical size of `w` and `h` does not create any arithmetic difficulty. The only factor that can affect running time is the number of test cases, and the solution should process each test case once. A solution that performs work proportional to the area, such as iterating over all `w * h` unit positions, could require up to `10^12` iterations for one test case and is completely unsuitable for a 1 second limit.

There are a few small cases that can expose careless implementations. The minimum dimensions are `1 1`, which must produce `YES`; an implementation that treats small dimensions specially could accidentally reject it. A nearly equal pair such as `5 6` must produce `NO`, because equality is required exactly, not approximately. The order of the dimensions does not matter geometrically, so `6 5` also produces `NO`, while `1000000 1000000` produces `YES`. Finally, equal dimensions at the maximum boundary are still perfectly valid, so no special overflow or boundary handling is necessary.

## Approaches

A literal brute-force approach could imagine constructing the rectangle from its unit cells and checking whether its geometry forms a square. For a `w × h` rectangle, that requires examining up to `w * h` positions. At the maximum dimensions, this becomes `1,000,000 × 1,000,000 = 10^12` cell operations for a single test case. The approach is conceptually correct because the complete shape contains exactly `w * h` unit cells, but it solves a geometric question by reconstructing information that is already encoded directly in the two dimensions.

The key observation is that the definition of a square gives us exactly the condition we need: its width and height must be equal. There is no need to inspect the interior, calculate the area, measure diagonals, or enumerate possible sides. The two input integers contain all relevant information, so one equality comparison completely determines the answer.

The brute-force works because examining the entire shape would eventually reveal whether its two dimensions match, but it fails because it performs up to `10^12` unnecessary operations. The observation that squarehood is equivalent to `w == h` reduces the entire test case to one constant-time comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(w × h) per test case | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `T`, because the same independent decision must be made for every shape.
2. For each test case, read its width `w` and height `h`. These two values completely describe the distinction we care about.
3. Compare `w` and `h`. If they are equal, output `YES`, because equal width and height is exactly the defining condition for a square.
4. If they are different, output `NO`, because a rectangle with unequal width and height cannot be a square.
5. Continue until all `T` test cases have been processed, producing exactly one answer for each input shape.

### Why it works

The invariant for each processed test case is simple: the output is `YES` exactly when the two dimensions are equal. A square must have equal width and height, so equality is sufficient for the required classification. Conversely, if the dimensions differ, the shape cannot have four equal sides and is not a square. Since every test case is evaluated using this exact condition, the algorithm cannot classify a valid input incorrectly.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    w, h = map(int, input().split())
    print("YES" if w == h else "NO")
```

The first line reads `T`, which determines how many independent test cases follow. The loop runs exactly `T` times, so every shape receives one answer and no extra input is processed.

Inside the loop, `w` and `h` are parsed as integers. The conditional expression directly implements the algorithm: equality produces `YES`, and inequality produces `NO`.

There are no boundary calculations, loops over dimensions, or array indices, so there are no off-by-one issues. Python integers also have arbitrary precision, although that is not needed here because the dimensions are at most `1,000,000`. Using `sys.stdin.readline` provides efficient input handling even when there are many test cases.

## Worked Examples

### Sample 1

The sample contains four independent rectangles.

| Test case | `w` | `h` | `w == h` | Output |
| --- | --- | --- | --- | --- |
| 1 | 9 | 9 | True | `YES` |
| 2 | 16 | 30 | False | `NO` |
| 3 | 200 | 33 | False | `NO` |
| 4 | 547 | 547 | True | `YES` |

For the first and fourth shapes, the dimensions match exactly, so they are accepted as squares. The other two have different dimensions and are rejected. This demonstrates that the algorithm needs no geometric construction, because every decision follows directly from the input pair.

### Constructed Example

Consider the input:

```
3
1 1
5 6
1000000 1000000
```

The execution is:

| Test case | `w` | `h` | `w == h` | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | True | `YES` |
| 2 | 5 | 6 | False | `NO` |
| 3 | 1000000 | 1000000 | True | `YES` |

This trace covers both boundaries of the allowed dimensions and a pair that differs by exactly one. It confirms that the algorithm tests equality itself rather than relying on a size threshold or a difference greater than some value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each of the `T` test cases requires one comparison. |
| Space | O(1) | Only the current width and height are stored. |

The maximum dimension of `1,000,000` has no effect on the amount of work performed by the optimal solution. Even if `T` is large, the algorithm performs only a constant amount of work per test case, which easily fits the 1 second time limit and uses negligible memory.

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

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output

# Provided sample
assert run("""4
9 9
16 30
200 33
547 547
""") == """YES
NO
NO
YES
""", "sample 1"

# Minimum-size dimensions
assert run("""1
1 1
""") == """YES
""", "minimum dimensions"

# Maximum-size equal dimensions
assert run("""1
1000000 1000000
""") == """YES
""", "maximum equal dimensions"

# Maximum-size unequal dimensions
assert run("""2
1000000 999999
999999 1000000
""") == """NO
NO
""", "maximum boundary with unequal dimensions"

# Difference of exactly one and several equal cases
assert run("""5
2 3
3 2
7 7
42 42
100 99
""") == """NO
NO
YES
YES
NO
""", "boundary equality cases")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `YES` | Minimum allowed dimensions and equality at the lower boundary |
| `1000000 1000000` | `YES` | Maximum allowed dimensions with equal sides |
| `1000000 999999`, `999999 1000000` | `NO`, `NO` | Maximum boundary values and independence from dimension order |
| `2 3`, `3 2`, `7 7`, `42 42`, `100 99` | `NO`, `NO`, `YES`, `YES`, `NO` | Exact equality and off-by-one style mistakes |

## Edge Cases

The smallest possible shape is `1 × 1`. The input

```
1
1 1
```

gives `w = 1` and `h = 1`, so the comparison `w == h` is true and the output is `YES`. A careless implementation that assumes a square must have dimensions larger than one would fail here.

A rectangle whose dimensions differ by only one is still not a square. For

```
1
5 6
```

the algorithm compares `5` and `6`, finds them unequal, and prints `NO`. There is no tolerance involved, so the fact that the dimensions are close does not change the classification.

The two dimensions may appear in either order. For

```
1
6 5
```

the comparison is again false, producing `NO`. The algorithm does not need to normalize the dimensions with `min` and `max`, because equality is unaffected by their order.

Finally, the largest valid dimensions require no special treatment. With

```
1
1000000 1000000
```

both values are equal, so the algorithm immediately prints `YES`. With

```
1
1000000 999999
```

the values differ, so it prints `NO`. Since the solution never multiplies the dimensions or performs any operation proportional to their magnitude, these boundary cases cost exactly the same amount of work as `1 × 1`.
