---
title: "CF 102219B - SpongeBob SquarePants"
description: "Each test case describes one four-sided shape using its width w and height h. Since all angles are already right angles, the only question that separates a square from an ordinary rectangle is whether the two side lengths are equal."
date: "2026-08-25T19:06:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102219
codeforces_index: "B"
codeforces_contest_name: "2019 ICPC Malaysia National"
rating: 0
weight: 102219
solve_time_s: 3729
verified: true
draft: false
---

[CF 102219B - SpongeBob SquarePants](https://codeforces.com/problemset/problem/102219/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1h 2m  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes one four-sided shape using its width `w` and height `h`. Since all angles are already right angles, the only question that separates a square from an ordinary rectangle is whether the two side lengths are equal.

For a particular shape, the required output is `YES` when `w == h`, because equal width and height make the rectangle a square. When the two values differ, the output is `NO`.

The dimensions are positive integers between `1` and `1,000,000`. The upper bound is small enough that a single integer comparison is trivial, but it also tells us that there is no reason to perform geometric simulation or enumerate possible side lengths. The number of test cases is processed independently, so the useful target is constant work per case, giving linear time in the number of cases. Even if there are many test cases, an `O(T)` solution only performs one comparison per shape, while an approach that performs up to one million operations for every shape can quickly become too expensive under the one-second limit.

The first edge case is the smallest possible square. For input `1 1`, the correct output is `YES`. A careless implementation that checks whether both dimensions are greater than one would incorrectly reject it, even though a square can have side length one.

Another edge case is a rectangle whose dimensions differ by only one. For input `7 8`, the output is `NO`. Code that accidentally uses a condition such as `abs(w - h) <= 1` would incorrectly accept this shape. Equality must be exact.

The orientation of the dimensions does not change whether the shape is a square. For input `3 10`, the answer is `NO`, and the same is true for `10 3`. A solution that treats width and height differently beyond comparing them can introduce an unnecessary directional dependency.

Finally, the maximum values must work normally. For input `1000000 1000000`, the answer is `YES`. The values fit comfortably in Python integers, so no special numeric handling is required.

## Approaches

A brute-force way to solve the problem would be to try every possible side length from `1` through `max(w, h)` and ask whether that candidate can be the common side length of the shape. If the candidate equals both dimensions, the shape is a square. If all candidates are exhausted, it is not.

This method is correct because a square with dimensions `w` and `h` has exactly one possible common side length, namely `w = h`. However, it can perform up to `1,000,000` candidate checks for a single test case. Across `T` cases, the worst-case work is `1,000,000T` checks. The problem does not provide a useful reason to spend that much time when the answer is already encoded directly in the two input values.

The key observation is that there is no hidden geometry to reconstruct. A four-sided shape with four right angles is a square precisely when its width and height are identical. The brute-force approach works because it eventually tests equality indirectly, but the observation that equality itself is the complete condition lets us replace up to one million checks with one comparison.

The resulting algorithm reads each pair `(w, h)`, compares the two integers, and prints `YES` if they are equal and `NO` otherwise.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(T * max(w, h))`, up to `1,000,000T` checks | `O(1)` | Too slow |
| Optimal | `O(T)` | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `T`. Each test case represents one independent shape, so no information needs to be shared between cases.
2. For every test case, read `w` and `h`. These are the two side lengths that determine whether the rectangle is a square.
3. Compare `w` and `h`. If `w == h`, both dimensions have the same length, which is exactly the defining condition needed here for the rectangle to be a square.
4. Print `YES` when the comparison is true and `NO` otherwise. No other geometric calculation is necessary because the input already guarantees that the shape has four right angles.

### Why it works

For every processed shape, the algorithm checks the necessary and sufficient condition for being a square. If `w == h`, the rectangle has equal width and height, so it is a square and the algorithm prints `YES`. If `w != h`, its two side lengths are different, so it cannot be a square and the algorithm prints `NO`. Since every test case is decided directly from this exact condition, the algorithm cannot produce an incorrect classification.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        w, h = map(int, input().split())

        if w == h:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The first line is read as `t`, which controls exactly how many pairs of dimensions are processed. This matches the input format and prevents the program from accidentally reading beyond the test cases.

Inside the loop, `w` and `h` are parsed as integers. The only decision is the equality test `w == h`, directly implementing the defining property of a square from the algorithm walkthrough.

The code does not need a special boundary condition for `1` or `1,000,000`. Both are ordinary integer values, and Python handles them without overflow. There are also no off-by-one issues because the algorithm does not iterate over the dimensions or use ranges. Each test case requires exactly one comparison and one output.

## Worked Examples

### Sample 1

The sample contains four independent shapes. The state of the key variables and the resulting comparison is:

| Test case | `w` | `h` | `w == h` | Output |
| --- | --- | --- | --- | --- |
| 1 | 9 | 9 | `True` | `YES` |
| 2 | 16 | 30 | `False` | `NO` |
| 3 | 200 | 33 | `False` | `NO` |
| 4 | 547 | 547 | `True` | `YES` |

The first and fourth shapes have equal dimensions, so both are accepted as square pants. The middle two have different dimensions and are rejected. Each decision depends only on the current pair, which confirms that test cases do not require any shared state.

### Additional Example

Consider the input:

```
5
1 1
1 2
7 8
1000000 999999
1000000 1000000
```

The execution is:

| Test case | `w` | `h` | `w == h` | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | `True` | `YES` |
| 2 | 1 | 2 | `False` | `NO` |
| 3 | 7 | 8 | `False` | `NO` |
| 4 | 1000000 | 999999 | `False` | `NO` |
| 5 | 1000000 | 1000000 | `True` | `YES` |

This trace covers both boundaries of the allowed range and also tests a pair whose dimensions differ by only one. The algorithm never treats near-equality as equality, so `7 8` correctly produces `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(T)` | Each of the `T` test cases requires one equality comparison and one output operation. |
| Space | `O(1)` | Apart from the input values for the current test case, the algorithm stores no data proportional to `T`. |

The dimensions can be as large as one million, but their magnitude has no effect on the running time because the solution does not iterate over them. Even with a large number of test cases, the work grows linearly with `T`, which is the appropriate complexity for an input where every case must be read and classified.

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

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

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

# Minimum-size values
assert run("""3
1 1
1 2
2 1
""") == """YES
NO
NO
""", "minimum-size and orientation cases"

# Maximum-size values
assert run("""3
1000000 1000000
1000000 999999
999999 1000000
""") == """YES
NO
NO
""", "maximum-size cases"

# Equality and near-equality
assert run("""4
7 7
7 8
8 7
8 8
""") == """YES
NO
NO
YES
""", "exact equality versus one-unit difference"

# Multiple independent cases
assert run("""5
3 10
50 50
123456 654321
999999 999999
42 43
""") == """NO
YES
NO
YES
NO
""", "mixed cases")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, `1 2`, `2 1` | `YES`, `NO`, `NO` | Minimum dimensions and reversed width and height |
| `1000000 1000000`, `1000000 999999`, `999999 1000000` | `YES`, `NO`, `NO` | Maximum dimensions and boundary differences |
| `7 7`, `7 8`, `8 7`, `8 8` | `YES`, `NO`, `NO`, `YES` | Exact equality and one-unit differences |
| Mixed five-case input | `NO`, `YES`, `NO`, `YES`, `NO` | Independent processing of multiple cases |
| Sample input | `YES`, `NO`, `NO`, `YES` | Official sample behavior |

## Edge Cases

The minimum-size square is `1 1`. The algorithm reads `w = 1` and `h = 1`, evaluates `1 == 1` as true, and prints `YES`. There is no requirement for a side length greater than one, so this correctly accepts the smallest possible square.

For the near-equal rectangle `7 8`, the algorithm evaluates `7 == 8` as false and prints `NO`. A careless solution based on the difference being small could incorrectly classify this as a square, but a square requires exact equality, not approximate equality.

For reversed dimensions such as `10 3`, the algorithm evaluates `10 == 3` as false and prints `NO`. The same result would occur for `3 10`. Since the square condition is symmetric in width and height, their order has no effect on the classification.

For the maximum square `1000000 1000000`, the comparison evaluates to true and produces `YES`. For `1000000 999999`, it evaluates to false and produces `NO`. These cases confirm that the upper boundary is handled directly without overflow, iteration limits, or special cases.
