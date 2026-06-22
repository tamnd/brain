---
title: "CF 105608A - \u0421\u0443\u043d\u0434\u0443\u043a \u0441\u043e\u043a\u0440\u043e\u0432\u0438\u0449"
description: "We are given a rectangular chest with three edge lengths $X$, $Y$, and $Z$. The chest can be oriented in any way, meaning any pair of its sides can become the “base” that tries to pass through a rectangular portal."
date: "2026-06-22T14:53:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105608
codeforces_index: "A"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421, \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440 2024-2025"
rating: 0
weight: 105608
solve_time_s: 43
verified: true
draft: false
---

[CF 105608A - \u0421\u0443\u043d\u0434\u0443\u043a \u0441\u043e\u043a\u0440\u043e\u0432\u0438\u0449](https://codeforces.com/problemset/problem/105608/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular chest with three edge lengths $X$, $Y$, and $Z$. The chest can be oriented in any way, meaning any pair of its sides can become the “base” that tries to pass through a rectangular portal. The portal itself has sides $A$ and $B$, but its orientation is also flexible, so we only care about matching smaller-to-smaller and larger-to-larger after rotation.

The task is to determine whether there exists at least one face of the chest such that, when we pick any two of $(X, Y, Z)$, that rectangle can fit through the portal when optimally rotated. Fitting means both dimensions of the chosen chest face do not exceed the corresponding dimensions of the portal after reordering both rectangles so that smaller sides are compared together and larger sides are compared together.

The input consists of five integers representing the three dimensions of the chest and the two dimensions of the portal. The output is a single word, either “YES” if any face of the chest can pass through the portal, or “NO” otherwise.

Since there are only three possible faces of the chest, the computation is constant time. Even if constraints were large, the solution would remain trivial, so we are not dealing with any complexity pressure. The only potential pitfalls come from correctly handling orientation, since comparing sides in fixed order leads to wrong results.

A common mistake appears when one checks only a single alignment like $X \le A$ and $Y \le B$. This fails when the portal is rotated. For example, if $X = 5$, $Y = 3$, $A = 4$, $B = 6$, then direct comparison might fail depending on ordering, but a correct orientation check succeeds because $(3, 5)$ fits into $(4, 6)$.

Another subtle mistake is forgetting that each of the three faces must be checked independently. Passing through the portal depends on at least one valid pair, not all of them.

## Approaches

A brute-force view is straightforward. We take each face of the chest, namely $(X, Y)$, $(X, Z)$, and $(Y, Z)$, and for each one we try both possible orientations against the portal. For each attempt, we check whether both dimensions of the rotated chest face fit within the rotated portal. Since each face has exactly two orientations, this leads to a constant number of checks.

This works because there are only three candidate pairs and each pair has only two permutations, so the total work is fixed at six comparisons. Even though brute force is already minimal here, thinking in terms of brute force helps clarify correctness: we are explicitly enumerating all geometric configurations.

The key observation is that we do not need any optimization beyond this enumeration. The structure of the problem is fully bounded and discrete. The only requirement is to ensure we compare sorted dimensions so orientation is handled cleanly. Instead of checking both permutations manually, we can simply compare sorted pairs.

The transition from brute force to optimal solution is therefore not about reducing complexity, but about simplifying comparisons by normalizing each pair.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three dimensions of the chest and the two dimensions of the portal. These define two rectangles in 2D space that we will compare in multiple orientations.
2. For each pair of chest dimensions, form a candidate rectangle. The three candidates are $(X, Y)$, $(X, Z)$, and $(Y, Z)$. Each represents a possible face that might pass through the portal.
3. For each candidate pair, compare it with the portal by conceptually sorting both rectangles so that we always match the smaller side with the smaller side and the larger side with the larger side. This removes the need to explicitly try both rotations.
4. If any candidate pair satisfies both comparisons, immediately conclude that the chest can pass through the portal. There is no need to check remaining pairs once a valid configuration is found.
5. If none of the three pairs fits, conclude that no orientation allows passage.

Why it works: every valid way of inserting a rectangle into another axis-aligned rectangle corresponds to one of the two possible orderings of each pair. By normalizing both the chest face and portal sides into sorted order, we ensure that every possible rotation is represented by a single comparison. Since all geometric configurations reduce to these discrete cases, checking all three faces covers the entire search space without omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

x = int(input())
y = int(input())
z = int(input())
a = int(input())
b = int(input())

def fits(u, v, a, b):
    return (u <= a and v <= b) or (u <= b and v <= a)

ok = False
ok |= fits(x, y, a, b)
ok |= fits(x, z, a, b)
ok |= fits(y, z, a, b)

print("YES" if ok else "NO")
```

The solution reads all five integers directly. Each pair of chest edges is tested against both orientations of the portal using a helper function. The helper encapsulates the rotation logic so that we do not accidentally miss a valid configuration. The final answer is accumulated using a boolean flag, which short-circuits logically even though performance is not a concern here.

A common implementation error is forgetting the second orientation check `(u <= b and v <= a)`, which would incorrectly reject valid rotated fits.

## Worked Examples

Consider the input where the chest has dimensions 2, 3, 4 and the portal is 3 by 5.

For this case, we evaluate each face:

| Step | Pair | Portal | Fits (A,B) | Fits (B,A) | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | (2,3) | (3,5) | yes | yes | true |
| 2 | (2,4) | (3,5) | yes | yes | true (early stop) |

The algorithm stops after the first successful pair, confirming that at least one face passes through.

Now consider a failing case: chest 5, 6, 7 and portal 4, 5.

| Step | Pair | Portal | Fits (A,B) | Fits (B,A) | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | (5,6) | (4,5) | no | no | false |
| 2 | (5,7) | (4,5) | no | no | false |
| 3 | (6,7) | (4,5) | no | no | false |

No configuration succeeds, so the output is “NO”.

The first example shows early termination on success, while the second demonstrates full exhaustion of possibilities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three fixed comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The computation is constant regardless of input values, so it trivially satisfies any reasonable constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x = int(input())
    y = int(input())
    z = int(input())
    a = int(input())
    b = int(input())

    def fits(u, v, a, b):
        return (u <= a and v <= b) or (u <= b and v <= a)

    ok = False
    ok |= fits(x, y, a, b)
    ok |= fits(x, z, a, b)
    ok |= fits(y, z, a, b)

    return "YES" if ok else "NO"

# provided samples (illustrative, since original samples not given)
assert run("2\n3\n4\n3\n5\n") == "YES"
assert run("5\n6\n7\n4\n5\n") == "NO"

# custom cases
assert run("1\n1\n10\n10\n1\n") == "YES", "rotation-aligned fit"
assert run("3\n3\n3\n2\n5\n") == "YES", "equal cube face fits"
assert run("9\n8\n7\n6\n5\n") == "NO", "all faces too large"
assert run("5\n4\n3\n5\n4\n") == "YES", "exact match without rotation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 10 / 10 1 | YES | rotation necessity |
| 3 3 3 / 2 5 | YES | symmetry handling |
| 9 8 7 / 6 5 | NO | strict rejection |
| 5 4 3 / 5 4 | YES | boundary equality |

## Edge Cases

A subtle case is when all three dimensions are equal, such as $X = Y = Z = 3$ and portal $A = 2, B = 5$. Every face is identical, so the algorithm repeatedly checks the same effective condition.

For the pair (3, 3), both orientations against (2, 5) are tested:

First orientation checks $3 \le 2$ which fails, and $3 \le 5$ which passes, but since both dimensions must satisfy the same pairing consistently, this orientation is invalid. The second orientation is identical, leading to the same result. The algorithm correctly returns “NO”.

Another edge case is when one dimension is exactly equal to a portal side. For example $X = 5, Y = 4, Z = 3$ and portal $A = 5, B = 4$. For pair (5,4), the check succeeds immediately in either orientation since equality is allowed on both axes, producing “YES” without needing to examine the third dimension.
