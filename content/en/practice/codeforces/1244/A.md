---
title: "CF 1244A - Pens and Pencils"
description: "Polycarp has two kinds of work tomorrow: lectures and practical classes. Lectures can only be handled with pens, and each pen can support a fixed number of lectures before it runs out."
date: "2026-06-13T20:25:30+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1244
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 592 (Div. 2)"
rating: 800
weight: 1244
solve_time_s: 368
verified: false
draft: false
---

[CF 1244A - Pens and Pencils](https://codeforces.com/problemset/problem/1244/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 6m 8s  
**Verified:** no  

## Solution
## Problem Understanding

Polycarp has two kinds of work tomorrow: lectures and practical classes. Lectures can only be handled with pens, and each pen can support a fixed number of lectures before it runs out. Practical classes can only be handled with pencils, and each pencil lasts for a fixed number of practical classes.

The task is to decide how many pens and pencils to take so that all lectures and all practical classes are covered, while the total number of writing tools does not exceed the capacity of the pencil case. If it is impossible to both cover all work and fit everything into the case, we must report failure.

For each test case, we are given the number of lectures and practical classes, the capacity of each pen and pencil, and the maximum number of items the case can hold. The output is either a pair describing how many pens and pencils to take, or -1 if no valid combination exists.

The constraints are small enough that any solution operating in constant time per test case is sufficient. With at most 100 test cases and all values bounded by 100, even a direct arithmetic computation is trivially fast. There is no need for simulation or search.

The key subtlety is that it is easy to overthink this as a constrained optimization problem. A naive interpretation might suggest trying many distributions of pens and pencils, but the structure is actually fixed: the number of pens depends only on lectures, and the number of pencils depends only on practical classes. The only real question is whether the sum fits into the capacity.

A common mistake is attempting to “trade” pens for pencils or vice versa. That is impossible because their roles are independent. Another mistake is misinterpreting durability, for example thinking one pen corresponds to one lecture, when in fact each pen covers multiple lectures.

Edge cases arise when capacity is just barely sufficient or insufficient. For example, if a solution computes required pens and pencils but forgets to take ceilings, it will underestimate requirements and produce invalid answers. Similarly, if one assumes integer division without rounding up, cases like 7 lectures with 4 uses per pen will be mishandled.

## Approaches

A brute-force approach would try all possible numbers of pens and pencils up to the capacity limit and check whether they are sufficient. For each candidate pair, we would verify whether the pens cover all lectures and the pencils cover all practical classes. This leads to roughly k² combinations per test case, which in the worst case is 10⁴ operations per test and up to 10⁶ overall. This is already unnecessary given the structure, but more importantly it ignores that feasibility is not coupled between the two variables.

The key observation is that each resource requirement is independent. The minimum number of pens is fully determined by how many lectures must be covered and how many lectures a single pen supports. The same applies to pencils and practical classes. Once these two minimum values are computed, the only remaining constraint is whether their sum fits inside the pencil case.

This collapses the problem from a two-dimensional search into a direct computation problem. We compute the minimum required pens using a ceiling division, compute the minimum required pencils similarly, and then validate capacity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) per test | O(1) | Too slow / unnecessary |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum number of pens needed to cover all lectures. Each pen handles up to c lectures, so we divide the total lectures a by c, rounding up. This ensures no lecture is left uncovered even if the last pen is partially used.
2. Compute the minimum number of pencils needed to cover all practical classes. Each pencil handles up to d classes, so we again use ceiling division of b by d.
3. Check whether the total number of items required, pens plus pencils, is within the pencil case capacity k. If it exceeds k, there is no valid configuration because we are already using the minimum possible number of items for each type.
4. If the sum fits, output these computed values. Since the problem allows any valid answer, there is no need to adjust or redistribute counts.

Why it works: Each pen contributes only to lectures and each pencil contributes only to practical classes, so there is no interaction between the two constraints. Any valid solution must use at least the computed minimum of each type, because using fewer would fail coverage. Therefore the only feasibility condition is whether these two independent lower bounds fit into the total capacity.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, d, k = map(int, input().split())
    
    pens = (a + c - 1) // c
    pencils = (b + d - 1) // d
    
    if pens + pencils > k:
        print(-1)
    else:
        print(pens, pencils)
```

The computation uses integer ceiling division via (x + y - 1) // y, which avoids floating point operations and ensures correctness for exact multiples and non-multiples alike. The condition check is done after both values are computed because partial feasibility is irrelevant; both constraints must be satisfied simultaneously.

The output directly prints the derived counts since any feasible pair is acceptable. No further optimization or balancing is required.

## Worked Examples

Consider the input `7 5 4 5 8`. The required pens are ceil(7 / 4) = 2, and pencils are ceil(5 / 5) = 1. The total is 3, which is within capacity 8, so we output (2, 1). Any other pair with sufficient coverage and sum ≤ 8 would also be valid, but we stick to the minimal one for simplicity.

| Step | a | b | pens | pencils | pens + pencils | k | decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| init | 7 | 5 | 2 | 1 | 3 | 8 | valid |

This shows the independence of computations and how feasibility is checked only at the end.

Now consider `7 5 4 5 2`. We again compute pens = 2 and pencils = 1, but now total is 3, which exceeds k = 2. There is no way to reduce either value without breaking coverage requirements, so the answer is impossible.

| Step | pens | pencils | sum | k | decision |
| --- | --- | --- | --- | --- | --- |
| compute | 2 | 1 | 3 | 2 | reject |

This confirms that the failure comes not from a wrong choice but from insufficient capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires only a constant number of arithmetic operations |
| Space | O(1) | No auxiliary data structures are used |

The solution comfortably fits within limits since even for t = 100, the total work is negligible.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        a, b, c, d, k = map(int, input().split())
        pens = (a + c - 1) // c
        pencils = (b + d - 1) // d
        if pens + pencils > k:
            out.append("-1")
        else:
            out.append(f"{pens} {pencils}")
    return "\n".join(out)

# provided samples
assert solve("""3
7 5 4 5 8
7 5 4 5 2
20 53 45 26 4
""") == """2 1
-1
1 3"""

# minimum case
assert solve("""1
1 1 1 1 2
""") == "1 1"

# exact boundary
assert solve("""1
4 5 4 5 2
""") == "1 1"

# tight failure
assert solve("""1
4 5 4 5 1
""") == "-1"

# large balanced
assert solve("""1
100 100 1 1 200
""") == "100 100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 2 | 1 1 | minimal valid configuration |
| 4 5 4 5 2 | 1 1 | exact boundary fit |
| 4 5 4 5 1 | -1 | capacity too small |
| 100 100 1 1 200 | 100 100 | maximum requirement scaling |

## Edge Cases

One edge case is when both a and b are exact multiples of c and d. In this case, ceiling division equals simple division, and the solution should not overcount. For example, a = 8, c = 4 yields exactly 2 pens. The algorithm handles this correctly because (8 + 4 - 1) // 4 evaluates to 2.

Another edge case is when capacity is exactly equal to the required sum. For instance, pens = 3 and pencils = 2 with k = 5 must be accepted. The check pens + pencils > k ensures equality is allowed.

A failure case occurs when one resource dominates capacity. If pens alone already exceed k, even setting pencils to zero cannot fix the solution. The algorithm correctly rejects this because the computed minimum pens already violates the constraint, and no alternative configuration exists that reduces pens without breaking lecture coverage.
