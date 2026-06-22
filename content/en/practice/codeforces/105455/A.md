---
title: "CF 105455A - Juan's Femur"
description: "We are given multiple independent scenarios. Each scenario provides three positive integers representing the lengths of three bone fragments left after a fracture."
date: "2026-06-23T02:51:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105455
codeforces_index: "A"
codeforces_contest_name: "XXIII Spain Olympiad in Informatics, Day 1"
rating: 0
weight: 105455
solve_time_s: 90
verified: true
draft: false
---

[CF 105455A - Juan's Femur](https://codeforces.com/problemset/problem/105455/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent scenarios. Each scenario provides three positive integers representing the lengths of three bone fragments left after a fracture. For each triple, we must decide whether these three lengths can serve as the side lengths of a non-degenerate triangle.

A valid triangle requires that the sum of any two sides is strictly greater than the third side. This condition must hold for all three pairwise combinations of the given lengths.

The output is simply a yes-or-no decision per test case, depending on whether the triangle inequality holds.

The constraints allow each length to be as large as 10^8, which immediately rules out any need for special numeric handling beyond standard integer arithmetic. The number of test cases is not explicitly bounded, but typical Codeforces formatting implies potentially large input streams, so each case must be processed in constant time.

A naive approach that tries to construct or simulate geometry is unnecessary. The only meaningful operation is comparing sums of pairs of numbers.

Edge cases are mostly about equality and ordering. A common mistake is to forget that the triangle must be non-degenerate, so equality is invalid. For example, inputs like 1 2 3 fail because 1 + 2 equals 3, which does not form a valid triangle. Another subtle case is when all sides are equal, such as 5 5 5, which is always valid because 5 + 5 is strictly greater than 5.

## Approaches

A brute-force way to think about the problem is to directly apply the definition of a triangle: check all three inequalities for each test case. Since there are only three numbers, this is already constant work per case, so there is no meaningful “slow” version beyond doing redundant or repeated computations.

One could imagine a misguided approach where we try to permute sides or simulate triangle construction, but that would be unnecessary overhead. The structure of the problem is purely relational: only comparisons matter.

The key simplification comes from realizing that among the three inequalities, only one needs careful checking after sorting. If we reorder the sides so that a ≤ b ≤ c, then the only potentially nontrivial condition is whether a + b > c. The other two inequalities automatically hold because c is the largest value.

This reduces the problem to a single comparison per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct inequality checks | O(1) per case | O(1) | Accepted |
| Sort + single check | O(1) per case | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal method

1. Read triples of integers until input ends. Each triple represents three candidate side lengths.
2. For each triple, reorder the values so that they are in non-decreasing order. This step isolates the largest value, which is the only one that can violate the triangle condition.
3. Compare the sum of the two smaller values with the largest value. If the sum is strictly greater, the three segments can form a triangle.
4. Output "si" if the condition holds, otherwise output "no".

The sorting step is not about efficiency but about reducing the number of conditions that need to be checked. Without ordering, we would need to check all three inequalities explicitly, but ordering guarantees two of them are redundant.

### Why it works

The triangle inequality requires all pairwise sums to exceed the remaining side. Once the values are ordered so that a ≤ b ≤ c, the inequalities a + c > b and b + c > a are automatically true because c is the largest and both b and c are positive. The only remaining constraint that can fail is whether the two smallest values together are large enough to exceed the largest one. If that fails, no permutation of the same values can satisfy the triangle condition, since any other pairing would only reduce the sum being compared to c.

This reduction relies on the monotonic structure of ordered values: the largest element dominates all comparisons involving it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    out = []
    for line in sys.stdin:
        if not line.strip():
            continue
        a, b, c = map(int, line.split())
        if a > b:
            a, b = b, a
        if b > c:
            b, c = c, b
        if a > b:
            a, b = b, a

        if a + b > c:
            out.append("si")
        else:
            out.append("no")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation processes input line by line, which is sufficient given the problem format. Each triple is sorted using a minimal sequence of swaps rather than a full sort, since only three elements are involved.

The core decision is the single inequality `a + b > c`. Strict inequality is essential because equality corresponds to a degenerate triangle, which is explicitly disallowed.

The output is accumulated in a list and printed once to avoid repeated I/O overhead.

## Worked Examples

### Example 1

Input:

```
3 4 5
```

After ordering, values remain (3, 4, 5).

| Step | a | b | c | Check |
| --- | --- | --- | --- | --- |
| Input | 3 | 4 | 5 | raw |
| Ordered | 3 | 4 | 5 | a ≤ b ≤ c |
| Compare | 3 | 4 | 5 | 3 + 4 > 5 |

Result is true, so output is "si".

This demonstrates a standard valid triangle where all inequalities are strictly satisfied.

### Example 2

Input:

```
9 2 4
```

After ordering, values become (2, 4, 9).

| Step | a | b | c | Check |
| --- | --- | --- | --- | --- |
| Input | 9 | 2 | 4 | raw |
| Ordered | 2 | 4 | 9 | a ≤ b ≤ c |
| Compare | 2 | 4 | 9 | 2 + 4 > 9 |

Since 6 is not greater than 9, the triangle condition fails.

This case highlights why ordering matters: the largest side dominates the feasibility check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires a constant number of comparisons and swaps |
| Space | O(1) | Only a few integer variables are used regardless of input size |

The solution is linear in the number of input lines, which is optimal since every case must be read at least once. Memory usage remains constant and well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("3 4 5\n9 2 4\n") == "si\nno"

# all equal sides
assert run("5 5 5\n") == "si"

# degenerate case
assert run("1 2 3\n") == "no"

# large valid triangle
assert run("100000000 99999999 99999998\n") == "si"

# two small, one large
assert run("1 1 100\n") == "no"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5 5 | si | equal sides valid triangle |
| 1 2 3 | no | degenerate boundary case |
| 100000000 99999999 99999998 | si | large values within constraints |
| 1 1 100 | no | extreme imbalance failure |

## Edge Cases

A subtle edge case is when the triangle is nearly degenerate. For example, `1 2 3` after sorting becomes `(1, 2, 3)`. The algorithm computes `1 + 2 = 3`, and since strict inequality is required, it correctly outputs "no". A weak implementation that uses `>=` instead of `>` would incorrectly accept this case.

Another case is when inputs are already sorted in reverse order, such as `9 2 4`. The swap-based ordering ensures correct normalization to `(2, 4, 9)`, after which the same single comparison applies. Without ordering, a naive check might mistakenly compare mismatched pairs and still arrive at the correct result, but in more complex extensions of this problem that approach would fail, making the ordering step the stable general pattern.
