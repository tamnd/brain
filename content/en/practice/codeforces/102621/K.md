---
title: "CF 102621K - Seal Sharing"
description: "We have a rectangular sheet of paper with dimensions a × b and n rectangular seals. Each seal creates a rectangle when placed, and it may be rotated by 90 degrees. We need to choose two different seals and place both of them on the paper without overlapping."
date: "2026-08-01T08:50:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102621
codeforces_index: "K"
codeforces_contest_name: "mBIT Advanced June 2020"
rating: 0
weight: 102621
solve_time_s: 64
verified: true
draft: false
---

[CF 102621K - Seal Sharing](https://codeforces.com/problemset/problem/102621/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular sheet of paper with dimensions `a × b` and `n` rectangular seals. Each seal creates a rectangle when placed, and it may be rotated by 90 degrees. We need to choose two different seals and place both of them on the paper without overlapping. The two rectangles must stay aligned with the paper edges, and the goal is to maximize the total covered area.

The input describes the paper size followed by the dimensions of every available seal. The output is the largest possible sum of areas of two seals that can both be placed. If no pair of seals can fit together, the answer is `0`.

The constraints are small: `n`, `a`, and `b` are at most `100`. This changes the strategy completely. An `O(n²)` enumeration performs at most around ten thousand pair checks, which is tiny for any normal time limit. More complicated approaches using dynamic programming or geometry structures would add unnecessary complexity.

The main traps are caused by rotation and by the fact that two rectangles do not need to be placed in a corner arrangement only. They can be placed side by side horizontally or vertically.

For example:

```
Input:
2 2 2
1 2
2 1

Output:
4
```

A careless solution that ignores rotation would reject the second seal, even though rotating it makes the two seals exactly fill the paper.

Another edge case is when one seal fits individually but no second seal can share space with it.

```
Input:
3 10 10
6 6
7 7
20 5

Output:
0
```

The third seal cannot be used, and the first two seals cannot fit together because their combined dimensions exceed the paper in every arrangement.

A final common mistake is checking only one orientation of the paper. A rectangle of size `x × y` can be placed as `y × x`, so every candidate pair must consider both rotations.

## Approaches

The straightforward solution is to try every pair of seals. For each pair, we decide how each seal is rotated and test whether the two rectangles can be placed together. If the first rectangle has dimensions `w1 × h1` and the second has dimensions `w2 × h2`, they can share the paper in two basic layouts. They can be stacked vertically, requiring `w1` and `w2` to fit within the paper width and `h1 + h2` to fit within the paper height. They can also be placed side by side, requiring `w1 + w2` to fit within the width and both heights to fit within the height.

This brute-force idea is already enough for the constraints. There are at most `100 × 100` pairs, and each pair only checks a constant number of rotations and layouts. The total work is only a few tens of thousands of operations.

The useful observation is that there are no hidden placement choices. Since both seals are rectangles aligned with the paper, every valid arrangement can be transformed into one where one rectangle is directly above, below, left, or right of the other. The position inside the paper does not matter, only whether the combined widths and heights satisfy the limits.

The brute-force works because the number of seals is small. It would fail if there were hundreds of thousands of seals because checking all pairs would become quadratic. Here, the same idea is the intended solution because the constraints allow it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n²) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all seal dimensions and store them.
2. Consider every pair of different seals. Only pairs matter because the final answer must contain exactly two seals.
3. For each pair, try both orientations of the first seal and both orientations of the second seal. Rotation changes the dimensions but not the area.
4. For every orientation combination, check two possible layouts. The first layout places the seals vertically, so their widths must fit and their heights must add up within the paper height. The second layout places them horizontally, so their heights must fit and their widths must add up within the paper width.
5. If an arrangement is valid, update the answer with the sum of the two rectangle areas.

The reason this covers every possible placement is that two axis-aligned rectangles that do not overlap can always be separated along either the horizontal axis or the vertical axis. That separation corresponds exactly to the two layouts checked by the algorithm.

### Why it works

The algorithm examines every possible choice of two seals and every possible rotation of those seals. For any valid placement, the two rectangles must either have one rectangle completely to the left or right of the other, or one rectangle completely above or below the other. The corresponding dimension checks are performed directly, so every valid pair is considered. Since every considered valid arrangement contributes its area to the maximum, and invalid arrangements are rejected, the final answer is exactly the best possible covered area.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    seals = [tuple(map(int, input().split())) for _ in range(n)]

    ans = 0

    def check(w1, h1, w2, h2):
        if w1 <= a and w2 <= a and h1 + h2 <= b:
            return True
        if h1 <= b and h2 <= b and w1 + w2 <= a:
            return True
        return False

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = seals[i]
            x2, y2 = seals[j]

            for w1, h1 in ((x1, y1), (y1, x1)):
                for w2, h2 in ((x2, y2), (y2, x2)):
                    if check(w1, h1, w2, h2):
                        ans = max(ans, x1 * y1 + x2 * y2)

    print(ans)

if __name__ == "__main__":
    solve()
```

The nested loops enumerate each unordered pair exactly once. Using `i + 1` avoids comparing a seal with itself and avoids repeating the same pair in reverse order.

The rotation loops generate the two possible orientations for every seal. The area calculation uses the original dimensions because rotating a rectangle does not change its area.

The `check` function contains the complete geometry condition. The first condition represents vertical stacking, while the second represents horizontal placement. Keeping these checks separate avoids mistakes with width and height being swapped.

Python integers do not overflow for these constraints because the maximum possible area is only `100 × 100 + 100 × 100`.

## Worked Examples

### Sample 1

Input:

```
2 2 2
1 2
2 1
```

| Step | First seal | Second seal | Orientation | Valid? | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1×2 | 2×1 | original | yes | 4 |

The second seal must be rotated for the placement to work. The algorithm finds that the two seals can be stacked to fill the entire paper.

### Sample 2

Input:

```
4 10 9
2 3
1 1
5 10
9 11
```

| Step | Pair | Orientation | Placement | Result |
| --- | --- | --- | --- | --- |
| 1 | 2×3 and 1×1 | checked | valid | area 7 |
| 2 | 2×3 and 5×10 | checked | valid | area 56 |
| 3 | 2×3 and 9×11 | checked | invalid | ignored |
| 4 | 1×1 and 5×10 | checked | valid | area 51 |

The largest valid pair is the first and third seals, giving area `6 + 50 = 56`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every pair of seals is tested with a constant number of rotations and layouts. |
| Space | O(n) | The list of seal dimensions is stored. |

With `n ≤ 100`, the quadratic number of comparisons is very small, so the solution easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""2 2 2
1 2
2 1
""") == "4\n", "sample 1"

assert run("""4 10 9
2 3
1 1
5 10
9 11
""") == "56\n", "sample 2"

assert run("""3 10 10
6 6
7 7
20 5
""") == "0\n", "sample 3"

assert run("""1 5 5
3 3
""") == "0\n", "only one seal"

assert run("""2 5 5
5 2
2 5
""") == "20\n", "rotation boundary"

assert run("""3 10 10
4 4
4 4
4 4
""") == "32\n", "equal rectangles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One seal only | 0 | A single seal cannot form a pair. |
| Two rotated seals | 20 | Rotation handling and exact boundary fitting. |
| Equal rectangles | 32 | Repeated dimensions and pair enumeration. |

## Edge Cases

When rotation is required, the algorithm explicitly tries both orientations. For the input:

```
2 2 2
1 2
2 1
```

the second seal becomes `1 × 2` after rotation, allowing the pair to occupy the entire paper. A solution checking only the given orientation would incorrectly output `0`.

When no pair fits, every orientation combination fails. For:

```
3 10 10
6 6
7 7
20 5
```

the first two seals cannot be arranged because their combined width or height is too large, and the third seal cannot be used. The answer remains `0`.

When dimensions exactly touch the border, the inequalities must allow equality. For:

```
2 5 5
5 2
2 5
```

the seals can be placed side by side or stacked with no unused space. The algorithm uses `<=`, so it correctly returns `20` instead of rejecting the arrangement.
