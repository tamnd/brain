---
title: "CF 1203B - Equal Rectangles"
description: "We are given 4n sticks. Every rectangle requires four sticks: two sticks for one side length and two sticks for the other side length. Every stick must be used exactly once. The goal is to split all sticks into exactly n rectangles such that every rectangle has the same area."
date: "2026-06-11T23:42:19+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1203
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 579 (Div. 3)"
rating: 1200
weight: 1203
solve_time_s: 115
verified: true
draft: false
---

[CF 1203B - Equal Rectangles](https://codeforces.com/problemset/problem/1203/B)

**Rating:** 1200  
**Tags:** greedy, math  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given `4n` sticks. Every rectangle requires four sticks: two sticks for one side length and two sticks for the other side length. Every stick must be used exactly once.

The goal is to split all sticks into exactly `n` rectangles such that every rectangle has the same area. For each test case, we must determine whether such a construction exists.

A rectangle with side lengths `a` and `b` needs two sticks of length `a` and two sticks of length `b`. That immediately tells us that the sticks must naturally form pairs of equal lengths. If some stick length appears an odd number of times inside a required pair structure, forming rectangles becomes impossible.

The constraints are small. Each query contains at most `4 · 100 = 400` sticks, and there are at most 500 queries. Sorting 400 numbers is extremely cheap, so an `O(n log n)` solution per query is easily fast enough.

The tricky part is not building rectangles, but proving that all rectangles can have the same area.

Consider the sticks:

```
1 1 2 2 3 3 6 6
```

A careless approach might only verify that every length appears an even number of times. That condition is satisfied, yet the only possible rectangles are `(1,6)` and `(2,3)`, both having area `6`, so the answer is `YES`.

Now consider:

```
1 1 2 2 3 3 4 4
```

Again, every length appears an even number of times. The rectangles become `(1,4)` and `(2,3)`, whose areas are both `4` and `6` respectively. The answer is `NO`. Pair counts alone are not enough.

Another easy mistake is greedily matching equal pairs without checking the global area. For example:

```
1 1 1 1 2 2 2 2
```

We can build rectangles `(1,1)` and `(2,2)`, giving areas `1` and `4`. The correct answer is `NO`, despite every stick length appearing exactly four times.

## Approaches

A brute-force solution would try all ways to group the sticks into rectangles and then check whether every rectangle has the same area. This is correct because it examines every possible arrangement. Unfortunately, the number of possible groupings grows explosively. Even for a few dozen sticks, the number of combinations becomes astronomical, making such a method completely infeasible.

The key observation comes from sorting the sticks.

Suppose a valid solution exists. Every side of every rectangle must be formed by two equal sticks. After sorting, equal sticks must appear next to each other. If at any position `a[2i] != a[2i+1]`, some required side cannot be formed and the answer is immediately `NO`.

After verifying all pairs, think about the rectangle areas. Let the sorted array be:

```
a0 ≤ a1 ≤ ... ≤ a(4n-1)
```

In a valid arrangement, the smallest available side length must be paired with the largest available side length. Otherwise, some rectangle would have a smaller area and another would have a larger area.

This leads to a very strong structure. After sorting, the rectangle side lengths are formed from pair blocks:

```
(a0,a1), (a2,a3), ... , (a(4n-2),a(4n-1))
```

The first side pair and the last side pair must form one rectangle. The second side pair and the second-last side pair must form another rectangle, and so on.

If all rectangles have the same area, then

```
a0 * a(4n-1)
=
a2 * a(4n-3)
=
a4 * a(4n-5)
= ...
```

Checking this condition after sorting completely solves the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the `4n` stick lengths and sort them.
2. Verify that every consecutive pair is equal.

Check positions `(0,1)`, `(2,3)`, `(4,5)`, and so on. If any pair contains different values, a rectangle side cannot be formed, so output `"NO"`.
3. Compute the target area using the smallest and largest sticks.

Since valid rectangles must pair the smallest side with the largest side, the required area is:

```
area = a[0] * a[4n-1]
```
4. Move inward from both ends of the sorted array.

For each rectangle candidate, compare:

```
a[l] * a[r]
```

where `l` starts at `0` and increases by `2`, while `r` starts at `4n-1` and decreases by `2`.
5. If any product differs from the target area, output `"NO"`.
6. If all pair checks and all area checks succeed, output `"YES"`.

### Why it works

After sorting, every rectangle side must come from two equal adjacent sticks. Otherwise two equal sticks would have to be separated while some unmatched length remains between them, which is impossible in a valid pairing.

Once those side pairs are fixed, the only way for all rectangle areas to remain equal is to combine the smallest available side with the largest available side, the second-smallest with the second-largest, and so on. Any other arrangement would create a smaller product somewhere and a larger product elsewhere.

The algorithm checks exactly these necessary conditions. They are also sufficient. If every adjacent pair is equal and every extreme-pair product equals the same value, we can explicitly build rectangles from those pairs, and every rectangle has the required common area. Hence the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())

    for _ in range(q):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        ok = True

        for i in range(0, 4 * n, 2):
            if a[i] != a[i + 1]:
                ok = False
                break

        if not ok:
            print("NO")
            continue

        target = a[0] * a[-1]

        l = 0
        r = 4 * n - 1

        while l < r:
            if a[l] * a[r] != target:
                ok = False
                break

            l += 2
            r -= 2

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The first section sorts the sticks. Sorting exposes the equal-stick pairs that must become rectangle sides.

The first loop validates the pair structure. Checking every second position is enough because a valid side requires exactly two equal sticks. If even one pair fails, no arrangement can use all sticks correctly.

The variable `target` stores the area that every rectangle must achieve. Using the smallest and largest remaining side lengths is not arbitrary. In any valid construction, those two sides must belong together.

The two-pointer loop walks inward through the sorted array. The pointers always sit on the first element of a side pair and the last element of a side pair. Comparing their product against the target verifies that every rectangle would have the same area.

Python integers comfortably handle the largest possible product, `10000 × 10000 = 10^8`, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
n = 2
1 1 2 2 3 3 6 6
```

Sorted array:

```
1 1 2 2 3 3 6 6
```

Pair validation:

| Pair Indices | Values | Valid |
| --- | --- | --- |
| (0,1) | 1,1 | Yes |
| (2,3) | 2,2 | Yes |
| (4,5) | 3,3 | Yes |
| (6,7) | 6,6 | Yes |

Target area:

```
1 × 6 = 6
```

Area checks:

| l | r | Product | Expected |
| --- | --- | --- | --- |
| 0 | 7 | 1×6=6 | 6 |
| 2 | 5 | 2×3=6 | 6 |

All products match, so the answer is:

```
YES
```

This example demonstrates the central invariant: every extreme-pair product is identical.

### Example 2

Input:

```
n = 2
1 1 2 2 3 3 4 4
```

Sorted array:

```
1 1 2 2 3 3 4 4
```

Pair validation:

| Pair Indices | Values | Valid |
| --- | --- | --- |
| (0,1) | 1,1 | Yes |
| (2,3) | 2,2 | Yes |
| (4,5) | 3,3 | Yes |
| (6,7) | 4,4 | Yes |

Target area:

```
1 × 4 = 4
```

Area checks:

| l | r | Product | Expected |
| --- | --- | --- | --- |
| 0 | 7 | 1×4=4 | 4 |
| 2 | 5 | 2×3=6 | 4 |

The second product differs from the target, so the answer is:

```
NO
```

This shows why checking only frequency parity is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting `4n` sticks dominates the running time |
| Space | O(1) extra | Only a few variables besides the input array |

With at most 400 sticks per query, sorting is extremely fast. Even across all 500 queries, the total work remains comfortably within the time limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    q = int(input())
    ans = []

    for _ in range(q):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        ok = True

        for i in range(0, 4 * n, 2):
            if a[i] != a[i + 1]:
                ok = False
                break

        if ok:
            target = a[0] * a[-1]

            l = 0
            r = 4 * n - 1

            while l < r:
                if a[l] * a[r] != target:
                    ok = False
                    break
                l += 2
                r -= 2

        ans.append("YES" if ok else "NO")

    return "\n".join(ans)

# provided sample
assert run(
"""5
1
1 1 10 10
2
10 5 2 10 1 1 2 5
2
10 5 1 10 5 1 1 1
2
1 1 1 1 1 1 1 1
1
10000 10000 10000 10000
"""
) == """YES
YES
NO
YES
YES"""

# minimum size
assert run(
"""1
1
5 5 7 7
"""
) == "YES"

# pair mismatch
assert run(
"""1
1
1 1 1 2
"""
) == "NO"

# equal pairs but unequal areas
assert run(
"""1
2
1 1 2 2 3 3 4 4
"""
) == "NO"

# all equal lengths
assert run(
"""1
3
5 5 5 5 5 5 5 5 5 5 5 5
"""
) == "YES"

# larger valid construction
assert run(
"""1
3
1 1 2 2 2 2 4 4 4 4 8 8
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 5 7 7` | YES | Smallest possible valid case |
| `1 1 1 2` | NO | Missing equal pair |
| `1 1 2 2 3 3 4 4` | NO | Pairing exists but areas differ |
| Twelve sticks all equal to 5 | YES | Every rectangle becomes a square |
| `1 1 2 2 2 2 4 4 4 4 8 8` | YES | Multiple rectangles with matching areas |

## Edge Cases

Consider:

```
1
1
1 1 1 2
```

After sorting we obtain:

```
1 1 1 2
```

The pair `(1,2)` fails the equality check. The algorithm immediately outputs `NO`. A solution that only counted frequencies loosely could incorrectly attempt to form a rectangle.

Consider:

```
1
2
1 1 2 2 3 3 4 4
```

All adjacent pairs are valid, so rectangle sides can be formed. The target area becomes `1 × 4 = 4`. During the inward scan, the second product is `2 × 3 = 6`, which breaks the invariant that every rectangle area must match. The algorithm correctly outputs `NO`.

Consider:

```
1
2
1 1 1 1 1 1 1 1
```

Every adjacent pair is equal. The target area is `1 × 1 = 1`, and every inward product is also `1`. The algorithm outputs `YES`, correctly handling the case where every rectangle is the same square.

Consider:

```
1
2
1 1 2 2 3 3 6 6
```

All pairs are valid. The target area is `1 × 6 = 6`. The inward products are `1 × 6 = 6` and `2 × 3 = 6`. Every rectangle receives area `6`, so the algorithm outputs `YES`. This confirms that the extreme-pair product invariant is both necessary and sufficient.
