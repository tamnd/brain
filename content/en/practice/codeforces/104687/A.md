---
title: "CF 104687A - \u0422\u0440\u0435\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a"
description: "We are given three integers, each representing a potential side length of a triangle. The task is to determine whether these three lengths can form a valid triangle."
date: "2026-06-29T08:45:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "A"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 57
verified: true
draft: false
---

[CF 104687A - \u0422\u0440\u0435\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a](https://codeforces.com/problemset/problem/104687/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three integers, each representing a potential side length of a triangle. The task is to determine whether these three lengths can form a valid triangle.

Geometrically, three segments form a triangle only when no single segment is too long to be “closed” by the other two together. In algebraic terms, this translates into the condition that the sum of any two sides must be strictly greater than the third side. Since we are dealing with three values, we need to check this condition for all three permutations.

The input size is minimal: exactly three integers, each between 1 and 100. This immediately tells us that any approach that even scans a small constant number of conditions is sufficient. There is no need for data structures, loops over large ranges, or optimization concerns. A constant-time check is the only meaningful complexity class here.

The main edge case comes from borderline equality. A naive reader might mistakenly accept cases like `1 2 3` because the sum equals the third side, but equality does not form a triangle. Another subtle case is when values are not sorted; for example, `3 1 2` should still be rejected even though the largest value is not in the last position.

## Approaches

The brute-force way to think about this problem is to directly apply the definition. We check all three inequalities: whether `a + b > c`, `a + c > b`, and `b + c > a`. If all are true, the sides form a triangle.

There is no meaningful way to simplify this further because the problem is already constant-sized. A “naive” approach might still try to permute all orderings of the sides and test triangle validity per permutation, but that introduces unnecessary repetition. With three values, that would mean checking six permutations, each requiring up to three comparisons, which is still constant time but redundant.

The key observation is that triangle validity depends only on pairwise sums against the remaining side. Once we recognize symmetry, we can either check all three conditions directly or sort the sides and reduce the condition to a single inequality: after sorting so that `x ≤ y ≤ z`, we only need to verify `x + y > z`. Sorting gives a cleaner structure and avoids reasoning about permutations.

Both approaches are valid, but the sorted version is often preferred in competitive programming because it generalizes cleanly to higher dimensions or similar problems.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check all inequalities) | O(1) | O(1) | Accepted |
| Sort + single check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We use the sorted approach for clarity.

1. Read the three input integers.
2. Store them in a list.
3. Sort the list in non-decreasing order.
4. Let the sorted values be `x`, `y`, and `z`, where `z` is the largest side.
5. Check whether `x + y > z`.
6. If the condition holds, output `YES`, otherwise output `NO`.

The sorting step is not about performance but about reducing reasoning complexity. Once the largest element is isolated, the triangle condition collapses into a single inequality instead of three.

### Why it works

A triangle can only fail to exist when one side is at least as long as the sum of the other two. Sorting guarantees we always compare the largest side against the sum of the other two. If that inequality holds strictly, the remaining two inequalities are automatically satisfied because both involve sums that are at least as large as `x + y`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, c = map(int, input().split())
    sides = [a, b, c]
    sides.sort()

    if sides[0] + sides[1] > sides[2]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The code reads the three values in one line, stores them in a list, and sorts them so the largest value is at the end. The only decision point is the triangle inequality check between the two smaller values and the largest value. The comparison is strict, which correctly rejects degenerate cases where the sum equals the third side.

## Worked Examples

### Example 1: `1 1 1`

| Step | Sides | Sorted Sides | Check |
| --- | --- | --- | --- |
| Read input | [1, 1, 1] |  |  |
| Sort | [1, 1, 1] | [1, 1, 1] |  |
| Inequality |  | [1, 1, 1] | 1 + 1 > 1 |

The inequality holds, so the output is `YES`. This corresponds to an equilateral triangle where all sides are equal and strictly satisfy the triangle condition.

### Example 2: `1 2 3`

| Step | Sides | Sorted Sides | Check |
| --- | --- | --- | --- |
| Read input | [1, 2, 3] |  |  |
| Sort | [1, 2, 3] | [1, 2, 3] |  |
| Inequality |  | [1, 2, 3] | 1 + 2 > 3 |

Here the sum equals the largest side, not strictly greater, so the condition fails and the output is `NO`. This represents a degenerate triangle that collapses into a straight line.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Sorting three elements is constant work, and only one comparison is performed afterward |
| Space | O(1) | Only a fixed-size list of three integers is stored |

The constraints are extremely small, so even the most direct implementation runs instantly within limits. There is no concern about memory or performance overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b, c = map(int, input().split())
    sides = [a, b, c]
    sides.sort()
    return "YES\n" if sides[0] + sides[1] > sides[2] else "NO\n"

# provided samples
assert run("1 1 1") == "YES\n"
assert run("1 2 3") == "NO\n"

# custom cases
assert run("2 3 4") == "YES\n", "valid small triangle"
assert run("1 1 2") == "NO\n", "degenerate equality case"
assert run("100 1 1") == "NO\n", "large imbalance case"
assert run("5 5 9") == "YES\n", "near boundary valid case"
assert run("10 10 20") == "NO\n", "strict equality boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 3 4 | YES | basic valid triangle |
| 1 1 2 | NO | equality edge case |
| 100 1 1 | NO | extreme imbalance |
| 5 5 9 | YES | near boundary valid case |
| 10 10 20 | NO | strict inequality enforcement |

## Edge Cases

A common edge case is when the largest side is exactly equal to the sum of the other two. For example, input `10 10 20`.

After sorting, we get `[10, 10, 20]`. The algorithm checks `10 + 10 > 20`, which evaluates to `20 > 20`, false. The output is correctly `NO`. This confirms that equality is treated correctly and prevents degenerate “flat” triangles.

Another case is when inputs are not ordered, such as `3 1 2`. Sorting transforms this into `[1, 2, 3]`, and the same inequality check correctly rejects it. This shows that correctness does not depend on input order, only on relative magnitudes.
