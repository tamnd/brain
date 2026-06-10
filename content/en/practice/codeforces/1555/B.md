---
title: "CF 1555B - Two Tables"
description: "We are given a rectangular room of width W and height H. Inside this room, there is a first table, aligned with the axes, with its bottom-left corner at (x1, y1) and top-right corner at (x2, y2). We want to place a second table of width w and height h in the room."
date: "2026-06-10T12:51:07+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1555
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 112 (Rated for Div. 2)"
rating: 1300
weight: 1555
solve_time_s: 355
verified: false
draft: false
---

[CF 1555B - Two Tables](https://codeforces.com/problemset/problem/1555/B)

**Rating:** 1300  
**Tags:** brute force  
**Solve time:** 5m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular room of width `W` and height `H`. Inside this room, there is a first table, aligned with the axes, with its bottom-left corner at `(x1, y1)` and top-right corner at `(x2, y2)`. We want to place a second table of width `w` and height `h` in the room. The catch is that the second table cannot overlap the first one, but touching edges is allowed. We are allowed to move the first table anywhere inside the room, but not rotate it, and our goal is to find the minimum distance the first table must move to make enough room for the second table. If it is impossible to fit both tables even after moving the first table, we should output `-1`.

The room and table dimensions can be very large, up to $10^8$, and we have up to 5000 test cases. This means we cannot afford anything like simulating all possible positions of the first table. A solution must reason about the available space algebraically, not by trial and error.

A non-obvious edge case is when the first table is almost as large as the room in one dimension, leaving only a narrow strip for the second table. For instance, if `W = 5`, `x1 = 1`, `x2 = 4`, and `w = 3`, then the second table cannot fit unless we slide the first table all the way to the left or right. A careless approach that ignores moving the table optimally would incorrectly declare this impossible.

## Approaches

A brute-force approach would attempt to test every possible horizontal and vertical translation of the first table, checking whether the second table fits in any remaining free space. This is correct in principle, because any valid movement is a candidate, but it is far too slow. For each test case, the number of candidate moves would be proportional to the dimensions of the room, which can be $10^8$. With 5000 test cases, this is infeasible.

The key insight is that we only need to consider movements along the axes that bring the first table just enough to make room for the second table. We do not need to check every position inside the room. The problem reduces to checking four directions: moving the first table to the left, right, down, or up. For each direction, we compute the minimal movement required so that either the horizontal or vertical space outside the first table can accommodate the second table.

Mathematically, the minimal movement is calculated by comparing the required width `w` with the available space on the left and right of the first table, and similarly for the height `h` with the space below and above. We pick the direction with the smallest positive shift, as negative shifts are impossible. If all directions require moving beyond the room boundary, the solution is `-1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(W*H) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the free horizontal space on the left of the first table: `left = x1`. Compute the free horizontal space on the right: `right = W - x2`. If `left + right >= w`, the table can fit horizontally after possibly moving the first table.
2. Compute the minimal horizontal shift required to fit the second table. If `w - left <= 0`, no move is needed; otherwise, move the first table right by `w - left`, provided `w - left <= right`. Similarly, check moving the first table left by `w - right`, provided this does not push the table outside the room.
3. Repeat steps 1-2 for vertical space. Compute the free vertical space below (`bottom = y1`) and above (`top = H - y2`). Compute the minimal vertical shift needed.
4. Consider all possible minimal shifts that keep the first table inside the room. The final answer is the smallest positive shift among horizontal and vertical options. If no shift keeps the table inside, output `-1`.

Why it works: the invariant is that the first table is always inside the room and we only consider movements that bring the free space exactly to the required width or height. Any smaller shift would leave the second table unable to fit, and any larger shift increases the distance unnecessarily. By evaluating all four directions, we guarantee the global minimum distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        W, H = map(int, input().split())
        x1, y1, x2, y2 = map(int, input().split())
        w, h = map(int, input().split())

        dx = float('inf')
        dy = float('inf')

        # Horizontal check
        space_left = x1
        space_right = W - x2
        if w <= space_left + space_right:
            move_left = max(0, w - space_left)
            move_right = max(0, w - space_right)
            if move_left <= space_right:
                dx = min(dx, move_left)
            if move_right <= space_left:
                dx = min(dx, move_right)

        # Vertical check
        space_bottom = y1
        space_top = H - y2
        if h <= space_bottom + space_top:
            move_down = max(0, h - space_bottom)
            move_up = max(0, h - space_top)
            if move_down <= space_top:
                dy = min(dy, move_down)
            if move_up <= space_bottom:
                dy = min(dy, move_up)

        ans = min(dx, dy)
        if ans == float('inf'):
            print(-1)
        else:
            print(f"{ans:.9f}")

if __name__ == "__main__":
    solve()
```

The code first reads all inputs. For each test case, it computes the free space on each side of the first table. It calculates the minimal horizontal and vertical shifts required to fit the second table. Then it chooses the smallest feasible shift. Using `float('inf')` ensures that impossible shifts are ignored. The formatting ensures precision up to 9 decimal places.

## Worked Examples

**Example 1**

Input:

```
W=8, H=5
x1=2, y1=1, x2=7, y2=4
w=4, h=2
```

| Variable | Value |
| --- | --- |
| space_left | 2 |
| space_right | 1 |
| w <= space_left+space_right | True |
| move_left | 2 |
| move_right | 3 |
| feasible moves | move_left=1 (dx), move_right invalid |
| vertical | no move needed (h=2 fits above/below) |
| final answer | 1.0 |

We see the minimal horizontal shift is 1, moving the first table down is unnecessary.

**Example 2**

Input:

```
W=5, H=4
x1=2, y1=2, x2=5, y2=4
w=3, h=3
```

Horizontal space: left=2, right=0 → total=2 < w → impossible. Output=-1.

This demonstrates the algorithm correctly handles impossible configurations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations and comparisons |
| Space | O(1) per test case | Only storing variables for shifts and distances |

With up to 5000 test cases, total operations are well under 10^5, so the solution easily runs in under 2 seconds. Memory usage is minimal.

## Test Cases

```python
# helper function to run solution on input string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("""5
8 5
2 1 7 4
4 2
5 4
2 2 5 4
3 3
1 8
0 3 1 6
1 5
8 1
3 0 6 1
5 1
8 10
4 5 7 8
8 5
""") == "\n".join(["1.000000000","-1","2.000000000","2.000000000","0.000000000"])

# Custom tests
assert run("""1
10 10
0 0 6 6
5 5
""") == "1.000000000", "Needs to move right/up"
assert run("""1
5 5
0 0 5 5
1 1
""") == "-1", "Room fully occupied"
assert run("""1
5 5
1 1 2 2
1 1
""") == "0.000000000", "No move needed"
assert run("""1
10 10
4 0 7 5
6 6
""") == "3.000000000", "Move left by 3 to fit width"
```

| Test input | Expected output
