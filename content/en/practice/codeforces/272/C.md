---
title: "CF 272C - Dima and Staircase"
description: "We have a staircase where the height of stair i is a[i], and the heights are already sorted in non-decreasing order. Boxes are dropped one after another. A box with width w covers exactly the first w stairs, meaning its horizontal span is above stairs 1..w."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 272
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 167 (Div. 2)"
rating: 1500
weight: 272
solve_time_s: 88
verified: true
draft: false
---

[CF 272C - Dima and Staircase](https://codeforces.com/problemset/problem/272/C)

**Rating:** 1500  
**Tags:** data structures, implementation  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a staircase where the height of stair `i` is `a[i]`, and the heights are already sorted in non-decreasing order. Boxes are dropped one after another. A box with width `w` covers exactly the first `w` stairs, meaning its horizontal span is above stairs `1..w`.

The box falls straight down until its bottom touches something solid underneath. That support can be either the staircase itself or a previously placed box. After landing, the box stays there permanently and future boxes may land on top of it.

For every box, we must output the height of its bottom after it lands.

The key geometric detail is that the box only interacts with the first `w` stairs. A box of width `3` does not care about stair `4`, even if stair `4` is much taller. The staircase heights being non-decreasing simplifies things a lot: among the first `w` stairs, the tallest stair is always stair `w`.

The constraints are large enough that simulation by explicitly storing every occupied height for every stair would be dangerous. Both `n` and `m` are up to `10^5`, so anything quadratic is impossible. An `O(nm)` algorithm could require around `10^10` operations, which is far beyond the limit. We need something close to linear time.

One easy mistake is misunderstanding what the landing height represents. The answer is the height of the box's bottom, not its top.

Consider:

```
stairs = [2]
box = (1, 5)
```

The box lands with its bottom at height `2`, not `7`.

Another subtle case is stacking caused by earlier boxes.

```
3
1 2 3
3
3 1
2 2
3 4
```

The first box of width `3` lands at height `3`, so its top becomes `4`.

The second box only covers stairs `1..2`, whose tallest stair is `2`. Since the earlier box spans width `3`, it also overlaps this region and blocks the fall at height `4`. So the second box lands at `4`.

The third box now lands on top of the second one, even though the staircase itself is only height `3`.

A naive implementation that only checks staircase heights would miss this stacking effect.

Another common bug comes from updating the current height incorrectly.

```
2
5 5
2
1 1
1 1
```

The first box lands at `5` and raises the occupied height for width `1` to `6`.

The second box must land at `6`, not `5`. If we forget to include previous boxes in the state, we get the wrong answer.

## Approaches

The brute-force idea is straightforward. For every box of width `w`, look at all stairs `1..w` and determine the highest occupied position there. The box lands on that height, and then raises the occupied level across those same stairs by its own height.

This works because the physical interpretation is accurate: the box cannot pass through the tallest obstacle under any part of its base.

The problem is performance. If every query scans up to `n` stairs, the complexity becomes `O(nm)`. With both values up to `10^5`, that means roughly `10^10` operations in the worst case.

The crucial observation is that the staircase heights are already sorted.

For a box of width `w`, the tallest stair among `1..w` is simply `a[w]`. We never need to scan the prefix.

Now think about previously placed boxes. Suppose we maintain:

```
current = highest occupied level so far
```

More precisely, after processing some boxes, `current` stores the highest top surface that can affect future boxes.

For a new box with width `w`, its bottom lands at:

```
max(current, a[w])
```

Then the new top becomes:

```
landing_height + h
```

and this updates `current`.

Why is a single variable enough? Because every new box always starts from stair `1`. All boxes overlap horizontally near the left side, so later boxes can always potentially rest on the tallest previously placed stack.

This turns the entire process into a simple running maximum simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the staircase heights into array `a`.
2. Store a variable `top`, initially `0`.

This variable represents the highest currently occupied vertical level created by previous boxes.
3. For each box `(w, h)`:

Compute the landing height:

```
landing = max(top, a[w - 1])
```

We use `w - 1` because Python arrays are zero-indexed.

The box must stop either on the staircase or on earlier boxes, whichever is higher.
4. Output `landing`.
5. Update the occupied height:

```
top = landing + h
```

Future boxes may stack on top of this one.

### Why it works

At every moment, `top` equals the highest top surface among all previously placed boxes.

Every new box overlaps the left side of the staircase, because all boxes cover stairs starting from `1`. That means any earlier box can potentially block the current box from falling further.

The staircase contribution for width `w` is exactly `a[w - 1]`, since the heights are non-decreasing.

So the current box must land at the larger of:

```
highest staircase under it
highest previous box stack
```

After placing the box, its top becomes the new highest occupied level.

Because this invariant stays true after every operation, the simulation is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    m = int(input())

    top = 0
    ans = []

    for _ in range(m):
        w, h = map(int, input().split())

        landing = max(top, a[w - 1])
        ans.append(str(landing))

        top = landing + h

    sys.stdout.write("\n".join(ans))

solve()
```

The array `a` stores staircase heights. Since the staircase is non-decreasing, the tallest stair among the first `w` stairs is always `a[w - 1]`.

The variable `top` is the entire state of the simulation. It tracks the highest occupied height produced by earlier boxes. This works because every box begins at stair `1`, so all boxes overlap horizontally and can affect future boxes.

The order of operations matters. We first compute and output the landing height, then update `top` using the box height. Reversing these steps would incorrectly shift every answer upward by the current box's own height.

The implementation uses `w - 1` carefully because the problem statement uses one-based indexing while Python uses zero-based indexing.

All values fit comfortably inside Python integers, since heights can grow to around `10^14` in the worst case.

## Worked Examples

### Sample 1

Input:

```
5
1 2 3 6 6
4
1 1
3 1
1 1
4 3
```

| Box | w | h | Stair height `a[w-1]` | Previous `top` | Landing | New `top` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 0 | 1 | 2 |
| 2 | 3 | 1 | 3 | 2 | 3 | 4 |
| 3 | 1 | 1 | 1 | 4 | 4 | 5 |
| 4 | 4 | 3 | 6 | 5 | 6 | 9 |

Output:

```
1
3
4
6
```

This trace shows both types of support. The second and fourth boxes land directly on the staircase because it is taller than previous stacks. The third box lands on top of earlier boxes instead.

### Custom Example

Input:

```
3
5 5 5
4
1 2
2 1
3 3
1 1
```

| Box | w | h | Stair height `a[w-1]` | Previous `top` | Landing | New `top` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 5 | 0 | 5 | 7 |
| 2 | 2 | 1 | 5 | 7 | 7 | 8 |
| 3 | 3 | 3 | 5 | 8 | 8 | 11 |
| 4 | 1 | 1 | 5 | 11 | 11 | 12 |

Output:

```
5
7
8
11
```

This example demonstrates continuous stacking. Even though the staircase height never exceeds `5`, the occupied height keeps increasing because every new box lands on earlier boxes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Reading the staircase takes `O(n)`, each box is processed in constant time |
| Space | O(1) | Aside from the input array and output list, only a few variables are used |

The solution easily fits the constraints. Processing `10^5` queries with constant work per query is well within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))

        m = int(input())

        top = 0
        ans = []

        for _ in range(m):
            w, h = map(int, input().split())

            landing = max(top, a[w - 1])
            ans.append(str(landing))

            top = landing + h

        return "\n".join(ans)

    return solve()

# provided sample
assert run(
"""5
1 2 3 6 6
4
1 1
3 1
1 1
4 3
"""
) == """1
3
4
6"""

# minimum size
assert run(
"""1
1
1
1 1
"""
) == "1"

# all staircase heights equal
assert run(
"""4
5 5 5 5
3
1 2
2 2
4 1
"""
) == """5
7
9"""

# increasing staircase dominates early
assert run(
"""5
1 3 5 7 9
3
1 1
3 1
5 1
"""
) == """1
5
9"""

# stacking dominates later
assert run(
"""3
2 2 2
4
1 5
1 1
2 1
3 1
"""
) == """2
7
8
9"""

# off-by-one width check
assert run(
"""4
1 2 100 100
2
2 1
2 1
"""
) == """2
3"""

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single stair and single box | `1` | Minimum constraints |
| Equal staircase heights | `5 7 9` | Pure stacking behavior |
| Strictly increasing staircase | `1 5 9` | Staircase dominating landing heights |
| Repeated narrow boxes | `2 7 8 9` | Persistent accumulation of occupied height |
| Width boundary case | `2 3` | Correct use of `a[w-1]` instead of neighboring stairs |

## Edge Cases

Consider a case where earlier boxes are taller than the staircase.

Input:

```
3
1 2 3
3
3 5
1 1
2 1
```

Processing:

The first box lands at height `3`, so the occupied top becomes `8`.

The second box only covers stair `1`, whose height is `1`, but it still overlaps the earlier box horizontally. It lands at `8`.

The third box lands at `9`.

Outputs:

```
3
8
9
```

The algorithm handles this because `top` always stores the highest previous stack.

Now consider a case where the staircase itself is taller than previous boxes.

Input:

```
4
2 4 6 10
2
1 1
4 1
```

The first box lands at `2`, making `top = 3`.

The second box compares `top = 3` with staircase height `10`, so it lands at `10`.

Outputs:

```
2
10
```

This confirms that the staircase still dominates when it is higher than previous stacks.

Finally, consider the indexing boundary.

Input:

```
4
1 2 100 100
1
2 1
```

The box only covers stairs `1` and `2`, so the correct landing height is `2`.

If we accidentally used `a[w]` instead of `a[w - 1]`, we would incorrectly use stair `3` and produce `100`.

The algorithm avoids this by consistently converting the one-based width into zero-based indexing.
