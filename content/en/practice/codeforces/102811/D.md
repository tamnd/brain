---
title: "CF 102811D - \u0422\u0430\u0431\u043b\u0438\u0446\u0430"
description: "We have an infinite grid whose rows and columns start from 1. The cells are filled with consecutive integers by walking around the borders of larger and larger squares. The task is to find the coordinates of the cell containing a given number n."
date: "2026-07-26T16:12:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102811
codeforces_index: "D"
codeforces_contest_name: "\u0428\u043a\u043e\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0432\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, 9-11 \u043a\u043b\u0430\u0441\u0441\u044b, \u041c\u043e\u0441\u043a\u0432\u0430  (\u0432\u0435\u0440\u0441\u0438\u044f CF)"
rating: 0
weight: 102811
solve_time_s: 67
verified: true
draft: false
---

[CF 102811D - \u0422\u0430\u0431\u043b\u0438\u0446\u0430](https://codeforces.com/problemset/problem/102811/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an infinite grid whose rows and columns start from 1. The cells are filled with consecutive integers by walking around the borders of larger and larger squares. The task is to find the coordinates of the cell containing a given number n.

The important observation is that the filling is not arbitrary. After finishing a square with side length k, exactly k² cells have been filled. This means every number belongs to one square layer, and the main challenge is finding that layer quickly and then locating the position inside its border.

The value of n can be as large as 10¹⁸, so simulating the filling process is impossible. Even an O(√n) simulation is unnecessary because the answer depends only on the square layer and a few arithmetic operations. The solution must work in constant time or close to it, using 64 bit integer arithmetic.

A common mistake is to use floating point square roots. For values near 10¹⁸, a floating point calculation can round incorrectly and place n into the wrong layer. For example, a number that is exactly a square, such as 16, must belong to the 4 by 4 border. A careless implementation may compute a slightly smaller square root and treat it as belonging to the previous layer, producing wrong coordinates.

Another edge case is the smallest possible value. For input `1`, the answer is `1 1`. Code that assumes the layer has a previous square will fail because the first layer has no earlier cells.

The other important boundary is the end of a layer. For example, the number `9` is the last value of the 3 by 3 square. Its coordinates are `1 3`. If the implementation uses strict comparisons instead of inclusive ones, it can move this value into the next layer.

## Approaches

The direct approach is to build the spiral cell by cell. Starting from the first cell, we keep moving along square borders and count until we reach n. This is correct because it follows exactly the order in which numbers are written. However, the largest input contains values up to 10¹⁸, so the number of visited cells can also be around 10¹⁸. Such a simulation cannot finish in any practical amount of time.

The structure of the spiral gives the faster approach. The square with side length k contains exactly k² cells, so the layer containing n is the smallest k for which k² is at least n. Once this layer is known, the first (k-1)² numbers are already behind us. The remaining offset tells us where n lies on the current square border.

The border direction depends only on whether k is odd or even. In odd layers, the new square starts at the bottom left corner and moves to the right, then upward along the right side. In even layers, it starts at the top right corner and moves downward, then left along the bottom side. This lets us compute the answer without visiting any other cells.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Find the smallest integer k such that k² is at least n. This is the side length of the square border containing n. The number of cells before this border is `(k - 1)²`, so every number in the layer can be identified by its offset from that value.
2. Compute `offset = n - (k - 1)²`. The offset is between 1 and `2k - 1`, because a square border adds exactly that many new cells.
3. If k is odd, process the border starting from the bottom left corner. When the offset is at most k, the number lies on the bottom row, so the row is k and the column is the offset. Otherwise, the number is on the right column, moving upward from the bottom, so the row decreases while the column stays k.
4. If k is even, process the border starting from the top right corner. When the offset is at most k, the number lies on the right column, so the row is the offset and the column is k. Otherwise, the number is on the bottom row, moving left, so the row stays k while the column decreases.

Why it works:

Every layer k contains exactly the cells that extend the previous square from side length k-1 to side length k. The algorithm first identifies this unique layer because all smaller layers contain exactly `(k-1)²` cells and the current layer ends at k². Inside the layer, the offset uniquely determines the position because the border traversal order is fixed. Since every possible position on the border is covered exactly once, the computed coordinates must match the location of n.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    k = int(n ** 0.5)
    while k * k < n:
        k += 1
    while (k - 1) * (k - 1) >= n:
        k -= 1

    offset = n - (k - 1) * (k - 1)

    if k % 2 == 1:
        if offset <= k:
            row = k
            col = offset
        else:
            row = 2 * k - offset
            col = k
    else:
        if offset <= k:
            row = offset
            col = k
        else:
            row = k
            col = 2 * k - offset

    print(row, col)

if __name__ == "__main__":
    solve()
```

The layer computation finds the first square large enough to contain n. The correction loops are used because the initial square root comes from floating point arithmetic, and the input range is large enough that rounding errors are possible.

The offset calculation converts the global number into a position inside only one square border. This avoids any dependency on the size of earlier layers.

The parity check controls the traversal direction. Odd and even square sizes have opposite starting corners, so using the wrong branch would mirror the answer across the square and fail on about half of the inputs.

Python integers have arbitrary precision, so there is no overflow issue even though intermediate values such as k² can approach 10¹⁸.

## Worked Examples

For the sample output, the missing input corresponds to `n = 15`.

| n | k | offset | case | row | col |
| --- | --- | --- | --- | --- | --- |
| 15 | 4 | 6 | even, bottom side | 4 | 2 |

The 4 by 4 layer starts after 9. The sixth new value on this border is reached after moving down the right side and then left along the bottom row, giving coordinates `(4,2)`.

Another example:

Input `1`

| n | k | offset | case | row | col |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | odd, bottom side | 1 | 1 |

The first layer contains only the first cell, so the algorithm immediately returns the starting position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and constant size corrections are performed. |
| Space | O(1) | The algorithm stores only several integer variables. |

The input limit of 10¹⁸ rules out any approach that walks through the table. The constant time solution easily fits within the given limits.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())

    k = int(n ** 0.5)
    while k * k < n:
        k += 1
    while (k - 1) * (k - 1) >= n:
        k -= 1

    offset = n - (k - 1) * (k - 1)

    if k % 2 == 1:
        if offset <= k:
            row, col = k, offset
        else:
            row, col = 2 * k - offset, k
    else:
        if offset <= k:
            row, col = offset, k
        else:
            row, col = k, 2 * k - offset

    sys.stdin = old_stdin
    return f"{row} {col}"

assert solve_case("15\n") == "4 2", "sample"
assert solve_case("1\n") == "1 1", "minimum value"
assert solve_case("9\n") == "1 3", "perfect square boundary"
assert solve_case("16\n") == "4 1", "even layer end"
assert solve_case("25\n") == "1 5", "maximum corner of odd layer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 15 | 4 2 | Provided example and even layer traversal |
| 1 | 1 1 | Smallest possible input |
| 9 | 1 3 | End of an odd layer |
| 16 | 4 1 | Boundary between two traversal directions |
| 25 | 1 5 | Largest corner of an odd layer |

## Edge Cases

For input `1`, the algorithm finds k = 1 and offset = 1. Since k is odd and the offset is within the first k cells, it places the value at row 1, column 1. This avoids trying to access a nonexistent previous square.

For input `9`, the algorithm finds k = 3 because 9 is exactly a square. The offset is 5 because eight cells belong to previous layers. Since k is odd and the offset is larger than k, the number is on the right column with row `2 * 3 - 5 = 1`, giving `(1,3)`. This confirms that exact square values are assigned to the correct layer.

For input `16`, the algorithm moves to the next layer with k = 4. The offset is 7, which is past the first four cells of the right side. The remaining movement is along the bottom row, giving column `2 * 4 - 7 = 1` and row 4. The answer is `(4,1)`, the first cell of the new border.
