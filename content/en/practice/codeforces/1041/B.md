---
problem: 1041B
contest_id: 1041
problem_index: B
name: "Buying a TV Set"
contest_name: "Codeforces Round 509 (Div. 2)"
rating: 1000
tags: ["math"]
answer: passed_samples
verified: false
solve_time_s: 403
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a33bb22-b27c-83ec-943d-62a14de8036c
---

# CF 1041B - Buying a TV Set

**Rating:** 1000  
**Tags:** math  
**Model:** gpt-5-3-mini  
**Solve time:** 6m 43s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a33bb22-b27c-83ec-943d-62a14de8036c  

---

## Solution

## Problem Understanding

We are looking for how many screen sizes are possible under two simultaneous constraints. First, the width of the TV must not exceed a limit `a`, and the height must not exceed a limit `b`. Second, the screen must follow a fixed aspect ratio `x : y`, meaning every valid screen must be some integer scaling of this ratio.

Any valid screen therefore has the form `(w, h) = (kx, ky)` for some positive integer `k`. The task is to count how many values of `k` keep both `kx ≤ a` and `ky ≤ b`.

So the problem reduces to finding how many integer multiples of a base rectangle fit inside a bounding box.

The constraints go up to 10^18, which immediately rules out iterating over all possible widths or heights. Even a linear scan is impossible. Any valid solution must reduce the problem to a constant number of arithmetic operations.

A naive mistake is to try checking all `w` up to `a` and verifying whether `w * y % x == 0`, then computing `h = w * y / x`. This is far too slow and also risks overflow if multiplication is not carefully handled.

Another subtle issue is integer division truncation. If we compute `a // x` or `b // y` incorrectly in a derived form, we may miscount boundary cases where one constraint is tighter than the other.

The core difficulty is recognizing that we are counting valid scaling factors, not independent choices of width and height.

## Approaches

A brute-force interpretation would try every possible integer pair `(w, h)` such that `w ≤ a` and `h ≤ b`, and then check whether `w / h = x / y`. For each pair we would verify the ratio condition using cross multiplication `w * y == h * x`.

This approach is correct but extremely expensive. The number of pairs is `a × b`, which in the worst case is `10^36`. Even conceptual iteration is impossible.

The key observation is that the ratio condition forces all valid pairs to lie on a single arithmetic progression of scaled rectangles. Once we fix `(x, y)`, every valid screen is uniquely determined by a scaling factor `k`. So instead of searching over a 2D grid, we only need to find how many integers `k` satisfy both bounds.

From `(kx ≤ a)` we get `k ≤ a / x`, and from `(ky ≤ b)` we get `k ≤ b / y`. Both must hold simultaneously, so the limiting factor is the minimum of these two upper bounds.

Thus the answer is simply `min(a // x, b // y)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over (w, h) | O(a · b) | O(1) | Too slow |
| Optimal scaling factor | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Interpret the aspect ratio constraint as a scaling rule. Any valid screen must be `(w, h) = (k·x, k·y)` for some integer `k ≥ 1`. This eliminates independent choice of width and height.
2. Translate the width constraint into an inequality on `k`. Since `kx ≤ a`, we derive `k ≤ a // x`. Integer division is safe because we only count full valid scalings.
3. Translate the height constraint into another inequality on `k`. Since `ky ≤ b`, we derive `k ≤ b // y`.
4. Combine both constraints. The same `k` must satisfy both upper bounds, so the maximum valid `k` is `min(a // x, b // y)`.
5. Count valid solutions. Every integer `k` from `1` to this maximum produces exactly one valid pair, so the answer is that maximum value.

### Why it works

Every valid pair must satisfy the ratio exactly, which forces proportionality between width and height. This collapses the search space from a 2D grid into a single parameter `k`. The constraints on `w` and `h` become independent upper bounds on `k`, and the intersection of these constraints is exactly the minimum of the two derived limits. No valid pair is missed because every feasible screen corresponds to a unique integer `k`, and no invalid pair is included because any `k` beyond either bound violates at least one constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, x, y = map(int, input().split())
    print(min(a // x, b // y))

if __name__ == "__main__":
    solve()
```

The solution directly applies the derived transformation from geometry to arithmetic. The key implementation detail is using integer division, which automatically floors the maximum feasible scaling factor. There is no need for loops or further validation since the ratio constraint is already enforced structurally by representing all solutions as multiples of `(x, y)`.

## Worked Examples

### Example 1

Input:

```
17 15 5 3
```

We compute bounds for `k`.

| Step | a // x | b // y | Result |
| --- | --- | --- | --- |
| Compute width limit | 17 // 5 = 3 | - | - |
| Compute height limit | - | 15 // 3 = 5 | - |
| Take minimum | 3 | 5 | 3 |

This shows that `k = 1, 2, 3` are valid. Each produces `(5,3), (10,6), (15,9)`.

The trace confirms that width becomes the limiting factor, not height.

### Example 2

Input:

```
5 5 4 3
```

| Step | a // x | b // y | Result |
| --- | --- | --- | --- |
| Compute width limit | 5 // 4 = 1 | - | - |
| Compute height limit | - | 5 // 3 = 1 | - |
| Take minimum | 1 | 1 | 1 |

Only `k = 1` works, producing `(4, 3)`. Any larger scaling immediately exceeds both constraints.

This example shows the case where both constraints are tight simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within limits because it avoids iteration entirely. Even with maximum input values near 10^18, integer division and comparison are constant-time operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b, x, y = map(int, input().split())
    return str(min(a // x, b // y))

# provided sample
assert run("17 15 5 3\n") == "3"

# minimum values
assert run("1 1 1 1\n") == "1"

# impossible case
assert run("5 5 6 1\n") == "0"

# only width constrains
assert run("20 100 5 10\n") == "4"

# only height constrains
assert run("100 20 10 5\n") == "2"

# both tight equally
assert run("12 12 3 3\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 1 | smallest valid scaling |
| 5 5 6 1 | 0 | no valid k exists |
| 20 100 5 10 | 4 | width-limited case |
| 100 20 10 5 | 2 | height-limited case |
| 12 12 3 3 | 4 | symmetric boundary case |

## Edge Cases

When `a < x` or `b < y`, the formula immediately yields zero because at least one division becomes zero. For example, input `a = 4, b = 100, x = 5, y = 1` gives `4 // 5 = 0`, so no valid TV exists. The algorithm handles this naturally without special conditions.

When both constraints are large but uneven, such as `a = 10^18, b = 10^18, x = 1, y = 10^18`, the width allows many values of `k`, but height restricts it to exactly one. The computation `min(a // 1, b // 10^18)` correctly yields `1`, demonstrating that the tighter dimension always dominates through the minimum operation.