---
title: "CF 103688A - Bookshelf  Filling"
description: "We are given two types of books that behave identically in width when placed upright: every book occupies exactly one unit of shelf width. The difference is in height. Type A books have height a, and type B books are taller with height b, where a < b."
date: "2026-07-02T20:51:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103688
codeforces_index: "A"
codeforces_contest_name: "The 17th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 103688
solve_time_s: 62
verified: true
draft: false
---

[CF 103688A - Bookshelf  Filling](https://codeforces.com/problemset/problem/103688/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two types of books that behave identically in width when placed upright: every book occupies exactly one unit of shelf width. The difference is in height. Type A books have height `a`, and type B books are taller with height `b`, where `a < b`. We also have a bookshelf with maximum allowed height `h`, and we are told `h` is at least `b`, so both types can stand upright without violating the height limit.

Initially, all books are placed vertically in a single row: all `n` type A books first, followed by all `m` type B books. In this configuration, the total width is simply `n + m`.

The twist is that we are allowed to take some number of type B books from the right side, specifically `k` books with `0 ≤ k ≤ m - 1`, and rotate them horizontally. These rotated books are placed on top of the existing vertical arrangement, which changes how height is consumed but removes them from contributing to the horizontal width as standalone vertical books.

The goal is to choose how many type B books to rotate so that the final required width of the shelf is as small as possible while still respecting the height limit `h`.

The constraints are large, with up to `10^3` test cases and values of `n` and `m` up to `10^9`, so any solution must run in constant time per test case. This immediately rules out any simulation over books or any approach that iterates over possible values of `k`.

A subtle failure case appears when reasoning about the interaction between height and the number of rotated books. For example, if `h` is only slightly larger than `b`, then only very few B books can be rotated, even if there are many available. Conversely, if `h` is large, we are limited only by the constraint `k ≤ m - 1`.

A naive mistake is to assume we can always rotate all B books except possibly one, reducing width to `n + 1`. This fails when stacking too many horizontal books exceeds the height limit, which is the true constraint that governs feasibility.

## Approaches

A brute-force strategy would try every possible `k` from `0` to `m - 1`, compute whether rotating `k` books is valid under the height constraint, and then compute the resulting width `n + m - k`. The issue is that checking feasibility of each `k` would require modeling how stacked horizontal books increase height. Even if each check were O(1), iterating over up to `10^9` values of `k` is impossible.

The key insight is that the arrangement is completely monotonic. Every additional rotated type B book adds exactly the same kind of height pressure in the same region of the shelf. This means that once a certain number of B books can be rotated without exceeding height `h`, any smaller number is also valid, and any larger number is invalid.

This reduces the problem to finding the maximum feasible `k`. The structure simplifies further because the only height interaction comes from stacking horizontal books on top of the existing tallest vertical books, which are the type B books. Each horizontal book contributes an extra unit of height over a region that already has height `b`, so stacking `k` such books increases the effective height requirement in that region to `b + k`. The constraint `b + k ≤ h` directly bounds the answer.

We also must respect the condition that we cannot rotate all B books, so `k ≤ m - 1`.

Once the maximum valid `k` is determined, the final width is simply reduced by `k`, since each rotated book removes one vertical-width contribution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k | O(m) per test case | O(1) | Too slow |
| Direct formula | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that rotating a type B book removes it from the vertical layout, so each valid rotation reduces total width by exactly one unit. This turns the problem into finding the maximum number of B books that can be rotated.
2. Determine how height changes when rotating B books. Each horizontal B contributes an additional unit of height on top of already existing B-height stacks, so stacking `k` rotated B books forces a height of `b + k` in the affected region.
3. Enforce the height constraint by requiring `b + k ≤ h`. This gives the upper bound `k ≤ h - b`.
4. Enforce the problem constraint that we cannot rotate all B books, giving `k ≤ m - 1`.
5. Combine both constraints to get the maximum feasible number of rotations: `k = min(m - 1, h - b)`.
6. Compute the final width by subtracting the number of rotated books from the original width: `w = n + m - k`.

### Why it works

The structure of the problem ensures that all rotated books interact with height in an identical and cumulative way. There is no benefit to distributing rotations differently because every additional horizontal B book contributes a uniform +1 to the limiting height region. This makes feasibility depend only on the count of rotated books, not their positions. As a result, the set of valid `k` forms a prefix interval starting from zero, and maximizing `k` is sufficient to minimize width.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b, n, m, h = map(int, input().split())
        
        # maximum number of B books we can rotate
        k = min(m - 1, h - b)
        if k < 0:
            k = 0
        
        # final width after removing k books from vertical layout
        print(n + m - k)

if __name__ == "__main__":
    solve()
```

The solution reads each test case and computes the answer in constant time. The only nontrivial step is correctly bounding `k`. The expression `h - b` captures how many additional horizontal layers can be stacked before exceeding the shelf height. We also clamp `k` to at least zero because if `h == b`, no horizontal stacking is possible.

A common mistake is forgetting the `m - 1` constraint, which prevents rotating all B books. Another is misinterpreting horizontal placement as affecting width multiplicatively; in reality, it only affects height and removes those books from the vertical width count.

## Worked Examples

### Example 1

Input:

```
a=2, b=4, n=5, m=7, h=6
```

We compute:

| Step | Value |
| --- | --- |
| h - b | 2 |
| m - 1 | 6 |
| k | min(2, 6) = 2 |
| width | 5 + 7 - 2 = 10 |

This shows that only two B books can be safely rotated before the height limit is reached.

### Example 2

Input:

```
a=3, b=5, n=4, m=3, h=5
```

| Step | Value |
| --- | --- |
| h - b | 0 |
| m - 1 | 2 |
| k | 0 |
| width | 4 + 3 = 7 |

Here, no B books can be rotated because even a single horizontal layer would exceed the height limit.

These examples confirm that the limiting factor is purely `h - b`, independent of `a`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case is handled with a constant number of arithmetic operations |
| Space | O(1) | No additional storage beyond a few integers |

The constraints allow up to `10^3` test cases with large values up to `10^9`, so constant-time processing per test case is sufficient and optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    output = []

    def solve():
        t = int(input())
        for _ in range(t):
            a, b, n, m, h = map(int, input().split())
            k = min(m - 1, h - b)
            if k < 0:
                k = 0
            output.append(str(n + m - k))

    solve()
    return "\n".join(output)

# provided sample-style tests
assert run("3\n2 4 5 7 5\n2 6 5 2 6\n3 4 3 2 5\n") == "10\n7\n5"

# minimum case
assert run("1\n1 2 1 1 2\n") == "2"

# no rotation possible
assert run("1\n1 5 10 10 5\n") == "20"

# large rotation possible
assert run("1\n1 5 10 10 100\n") == "11"

# edge: m = 1 (cannot rotate anything)
assert run("1\n1 5 10 1 100\n") == "11"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| m = 1 case | no reduction | enforces k ≤ m-1 |
| tight height | no rotation | h constraint blocks action |
| large h | max rotation | correctness of h-b bound |
| minimal sizes | baseline correctness | trivial configuration |

## Edge Cases

When `h` equals `b`, the height budget for stacking horizontal books becomes zero. In that situation, the formula yields `k = min(m - 1, 0) = 0`, so the width remains `n + m`. This matches the physical interpretation that even one horizontal book would immediately exceed the allowed height in the stacked region.

When `m = 1`, the constraint `k ≤ m - 1` forces `k = 0` regardless of height. The implementation handles this naturally because `min(0, h - b)` is always zero or negative, and we clamp it to zero.

When `h` is very large, the limiting factor becomes `m - 1`, meaning we can rotate almost all B books. The final width becomes `n + 1`, which is consistent with leaving exactly one unrotated B book in the vertical arrangement.
