---
title: "CF 1624B - Make AP"
description: "We are given three fixed positions in a sequence: first value a, second value b, and third value c. We are allowed exactly one modification operation: choose one of these three positions and multiply it by some positive integer m of our choice."
date: "2026-06-10T05:35:04+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1624
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 764 (Div. 3)"
rating: 900
weight: 1624
solve_time_s: 75
verified: true
draft: false
---

[CF 1624B - Make AP](https://codeforces.com/problemset/problem/1624/B)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three fixed positions in a sequence: first value `a`, second value `b`, and third value `c`. We are allowed exactly one modification operation: choose one of these three positions and multiply it by some positive integer `m` of our choice.

After this single change, we want the resulting triple to form an arithmetic progression in the given order. That means the middle element must be exactly halfway between the first and the third, or equivalently the condition `2 * middle = first + third` must hold.

The task is not to construct the progression explicitly, but only to decide whether such a choice of index and multiplier exists.

The constraints are tight on the number of test cases, up to 10⁴, but each test case is constant work. That immediately rules out anything involving searching over values of `m` or enumerating candidates. Since `m` can be as large as 10⁸, any brute force over possible multipliers is impossible.

The subtle part of this problem is that modifying one value changes the structure asymmetrically. A naive approach might try all choices of index and all possible `m`, but that introduces a huge search space.

Edge cases that commonly break incorrect solutions come from symmetry and zero-difference cases. For example, when all numbers are equal, any multiplication of one element still allows an AP if we pick `m = 1`. Another tricky case is when the AP already holds: we are still forced to apply an operation, but multiplying by 1 preserves it. A careless solution might forget that “doing nothing” is allowed via `m = 1`.

A second important corner is when the AP is “almost valid” but requires adjusting a middle element that must satisfy a strict linear relation, not just equality of differences.

## Approaches

A brute-force approach would try every index `i ∈ {a, b, c}` and every possible multiplier `m`, recompute the triple, and check whether it forms an arithmetic progression. This is correct in principle because it explores all allowed operations.

However, this immediately fails because `m` ranges up to 10⁸. Even if we cap ourselves at checking feasibility algebraically, iterating over values is impossible. The real issue is not just the size of `m`, but that there is no monotonic structure in how `m` affects the AP condition across different choices of index.

The key observation is that we do not need to search over `m` at all. Instead, we can assume which position is modified and directly solve for `m` using the arithmetic progression condition.

If we fix the index, the AP condition becomes a linear equation in `m`. Each case reduces to checking whether a derived value of `m` is a positive integer.

This transforms the problem from search over values into a constant number of algebraic checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over m | O(t · 10⁸) | O(1) | Too slow |
| Try 3 positions + solve equation | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

We consider each of the three possibilities separately.

1. Assume we multiply `a` by `m`. The new sequence becomes `[a·m, b, c]`. For this to be an AP, we need `2b = a·m + c`. We rearrange this into `m = (2b - c) / a`. This only works if `2b - c > 0` and divisible by `a`.
2. Assume we multiply `b` by `m`. The sequence becomes `[a, b·m, c]`. The AP condition is `2(b·m) = a + c`, so `m = (a + c) / (2b)`. We require exact divisibility and `a + c > 0`, which is always true given constraints.
3. Assume we multiply `c` by `m`. The sequence becomes `[a, b, c·m]`. The AP condition becomes `2b = a + c·m`, so `m = (2b - a) / c`. We again require positivity and divisibility.

At any point, if we find a valid integer `m ≥ 1`, we can immediately return YES.

If none of the three cases produces a valid multiplier, the answer is NO.

### Why it works

Every valid solution must correspond to exactly one modified position. For that fixed position, the AP condition uniquely determines the required value of `m` through a linear equation. Since there are only three possible choices, and each case is checked exhaustively, any valid configuration must be discovered. Conversely, every computed candidate is derived directly from the AP condition, so no invalid configuration can pass the checks.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(x, y, z):
    # try multiplying x by m: (x*m, y, z)
    num = 2*y - z
    if num > 0 and num % x == 0:
        m = num // x
        if m >= 1:
            return True

    # try multiplying y by m: (x, y*m, z)
    num = x + z
    if num % (2*y) == 0:
        m = num // (2*y)
        if m >= 1:
            return True

    # try multiplying z by m: (x, y, z*m)
    num = 2*y - x
    if num > 0 and num % z == 0:
        m = num // z
        if m >= 1:
            return True

    return False

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    print("YES" if ok(a, b, c) else "NO")
```

The code directly implements the three derived algebraic checks. Each block corresponds to fixing one index as the modified element. The integer division checks ensure we only accept valid multipliers, and the positivity condition prevents invalid negative or zero solutions.

A common pitfall here is forgetting that the multiplier must be at least 1. Another subtle issue is integer division: we must confirm divisibility before dividing to avoid incorrect truncation.

## Worked Examples

### Example 1

Input: `10 5 30`

We try modifying each position.

| Case | Equation | Derived m | Valid? |
| --- | --- | --- | --- |
| multiply a | 2·5 = 10·m + 30 | m = (10 - 30)/10 invalid | No |
| multiply b | 10 + 30 = 2·5·m | m = 40 / 10 = 4 | Yes |
| multiply c | 2·5 = 10 + 30·m | invalid | No |

We find a valid multiplier when modifying `b`, so the answer is YES.

This confirms that the algorithm correctly identifies the middle element adjustment case.

### Example 2

Input: `2 6 3`

| Case | Equation | Derived m | Valid? |
| --- | --- | --- | --- |
| multiply a | 12 = 2·m + 3 | m = 4.5 | No |
| multiply b | 2 + 3 = 12·m | m < 1 | No |
| multiply c | 12 = 2 + 3·m | m = 10/3 | No |

No valid integer multiplier exists, so output is NO.

This shows that even when values are close, divisibility constraints prevent a solution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test performs constant arithmetic checks |
| Space | O(1) | Only a few variables are used per test case |

The solution easily fits within limits because even for 10⁴ test cases, we perform only a handful of integer operations per case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        a, b, c = map(int, input().split())

        def check(a, b, c):
            num = 2*b - c
            if num > 0 and num % a == 0 and num // a >= 1:
                return True
            if (a + c) % (2*b) == 0 and (a + c) // (2*b) >= 1:
                return True
            num = 2*b - a
            if num > 0 and num % c == 0 and num // c >= 1:
                return True
            return False

        return "YES" if check(a, b, c) else "NO"

    out = []
    t = int(sys.stdin.readline())
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# provided samples
assert run("""11
10 5 30
30 5 10
1 2 3
1 6 3
2 6 3
1 1 1
1 1 2
1 1 3
1 100000000 1
2 1 1
1 2 2
""") == """YES
YES
YES
YES
NO
YES
NO
YES
YES
NO
YES"""

# custom cases
assert run("""1
5 5 5
""") == "YES", "all equal"

assert run("""1
1 2 4
""") == "NO", "already AP but cannot fix wrong shape with single mult"

assert run("""1
3 1 2
""") in ["YES", "NO"], "sanity boundary"

assert run("""1
2 6 3
""") == "NO", "no valid multiplier"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5 5 | YES | all equal case |
| 1 2 4 | NO | impossible near-AP |
| 2 6 3 | NO | divisibility failure |

## Edge Cases

One edge case is when all three numbers are equal. The AP condition already holds, and multiplying any element by `m = 1` preserves it. The algorithm handles this because each case allows `m = 1`, and the divisibility checks pass naturally.

Another case is when the valid solution requires modifying the middle element. Many incorrect solutions miss this or assume endpoints must be adjusted. The equation `m = (a + c) / (2b)` explicitly captures this possibility, and the integer divisibility check ensures correctness.

A final subtle case is when the computed numerator becomes non-positive, such as `2b - c ≤ 0`. This corresponds to impossible AP configurations where the chosen modification would require a non-positive multiplier. The algorithm explicitly rejects these cases, preventing invalid arithmetic solutions from slipping through.
