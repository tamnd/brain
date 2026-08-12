---
title: "CF 102348K - Moonbound"
description: "We need to construct an (n times n) checkerboard, where cell ((i,j)) must contain stone if (i+j) is even and sand otherwise. The value (n) is even and at most (50). The difficulty is not choosing the final colors. The difficulty is the order in which cells can be reached."
date: "2026-08-13T01:15:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "K"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 158
verified: true
draft: false
---

[CF 102348K - Moonbound](https://codeforces.com/problemset/problem/102348/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct an (n \times n) checkerboard, where cell ((i,j)) must contain stone if (i+j) is even and sand otherwise. The value (n) is even and at most (50).

The difficulty is not choosing the final colors. The difficulty is the order in which cells can be reached. An empty cell can be filled individually only when it is on the border or touches an already filled cell. A (2 \times 2) operation is more powerful, but every currently empty cell inside that square receives the same color. Since every (2 \times 2) checkerboard contains two stone cells and two sand cells, a square operation can only be used after the cells of one color inside that square have already been filled.

The output is a sequence of valid operations. Every operation must place only the correct color, every chosen position must satisfy the required accessibility condition, and the total number of operations must not exceed (3n^2/4).

The constraint (n \le 50) means even a direct (O(n^2)) construction is tiny computationally, since there are at most (2500) cells. The real restriction is the number of manipulator uses. Filling every cell individually would require (n^2) operations, which is always larger than the allowed (3n^2/4). We therefore need to exploit the (2 \times 2) operation rather than merely finding a valid traversal of all cells.

The fact that (n) is even is exactly what lets us partition the entire wall into disjoint (2 \times 2) squares. There are (n^2/4) such squares, and if each square can be completed in three operations, the total is exactly (3n^2/4), matching the limit.

There are two small cases that commonly break careless constructions. For (n=2), the entire wall is one (2 \times 2) square. A direct (2 \times 2) operation cannot be the first operation, because all four cells are empty and it would paint them with one color, creating incorrect cells. For example, with input `2`, a valid construction is three operations: fill two cells of one diagonal individually, then use one square operation for the other diagonal.

For an interior (2 \times 2) square, simply filling one cell and then trying to fill its same-colored diagonal partner also fails. Those two cells are diagonally adjacent, so the second cell is not made free by the first operation. A construction must choose the two seed cells so that each is already on the boundary of the built region.

## Approaches

The most direct construction is to fill every cell independently. A cell can be selected once it is reachable, and processing the wall from its border toward the interior gives a valid order. The final coloring is obviously correct because every operation chooses the required color. However, this uses exactly (n^2) operations in the worst case, while the problem permits only (3n^2/4). For (n=50), that is (2500) operations instead of the maximum allowed (1875). The issue is the operation budget rather than computational running time.

The key observation is that the wall can be partitioned into (n^2/4) disjoint (2 \times 2) squares. Consider one such square with top-left corner ((x,y)), where both (x) and (y) are odd. Its cells are

[
(x,y),\quad (x,y+1),\quad (x+1,y),\quad (x+1,y+1).
]

The cells ((x,y+1)) and ((x+1,y)) have the same color. More importantly, when the (2 \times 2) squares are processed from top to bottom and left to right, both of these cells are reachable before we process their square. The first is either on the top border or touches the completely constructed square above. The second is either on the left border or touches the completely constructed square to the left.

We can fill those two same-colored cells with two singleton operations. At that point the remaining two cells in the square have the opposite color, so a single (2 \times 2) operation with that opposite color fills exactly those two empty cells. No incorrect cell is ever painted.

Thus every (2 \times 2) square costs exactly three operations. Since there are (n^2/4) squares, the total is

[
3 \cdot \frac{n^2}{4}=\frac{3n^2}{4},
]

which is exactly the allowed maximum.

The brute-force construction works because individual operations give complete control over every cell, but it spends one operation per cell. The observation that every checkerboard (2 \times 2) square consists of two equal-color diagonals lets us replace four singleton operations by two singleton seeds and one square operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Fill every cell individually | (O(n^2)) | (O(n^2)) | Valid but exceeds operation limit |
| Partition into (2 \times 2) squares | (O(n^2)) | (O(n^2)) for stored operations | Accepted |

## Algorithm Walkthrough

1. Partition the wall into disjoint (2 \times 2) squares whose top-left corners are ((x,y)), where (x) and (y) take the odd values (1,3,5,\ldots,n-1). Every wall cell belongs to exactly one such square.
2. Process these squares in increasing row order and, inside each row, increasing column order. This order guarantees that every square except those touching the outer border has an already completed square directly above it or directly to its left.
3. For the current square, first fill ((x,y+1)) individually. Its required color is sand, because (x+y+1) is odd. The cell is free because (x=1) puts it on the top border, while (x>1) gives it a filled neighbor above.
4. Fill ((x+1,y)) individually with sand as well. If (y=1), it is on the left border. Otherwise, the square immediately to its left has already been completed, so ((x+1,y)) has a filled neighbor.
5. Use a (2 \times 2) operation at ((x,y)) with stone. The two sand cells placed in the previous operations are already occupied, while the other two cells, ((x,y)) and ((x+1,y+1)), are exactly the two stone cells of this checkerboard square. Hence the operation fills only correct cells.
6. Continue until every (2 \times 2) square has been processed. There are (n/2) choices of (x) and (n/2) choices of (y), so there are (n^2/4) squares and exactly three operations per square.

### Why it works

The invariant is that before processing a square, every previously processed square is completely correct, and the current square is still empty. The first seed ((x,y+1)) is always free because it is either on the top border or touches the completed square above. The second seed ((x+1,y)) is always free because it is either on the left border or touches the completed square to the left. Both seeds are sand cells. After they are placed, the only empty cells in the square are the two stone cells, so the final (2 \times 2) operation can safely use stone. Thus every operation is valid and every occupied cell has its required color. Since the squares are disjoint and cover the entire wall, the final wall is exactly the required checkerboard.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ans = []

    for x in range(1, n, 2):
        for y in range(1, n, 2):
            # (x, y + 1) and (x + 1, y) are both sand cells.
            ans.append((1, x, y + 1, 2))
            ans.append((1, x + 1, y, 2))

            # The remaining two cells of this 2x2 square are stone.
            ans.append((2, x, y, 1))

    print(len(ans))
    for t, x, y, b in ans:
        print(t, x, y, b)

if __name__ == "__main__":
    solve()
```

The outer loop chooses the top row of each (2 \times 2) block. Because it increments by two, it visits exactly the rows (1,3,\ldots,n-1). The inner loop does the same for columns.

The first singleton operation targets ((x,y+1)). Its parity is odd, so it must be sand. The second targets ((x+1,y)), which has the same parity and therefore also requires sand.

The square operation starts at ((x,y)). Its four cells are inside the wall because (x,y \le n-1). The two sand cells are already occupied, so the operation fills only the two empty stone cells. Choosing stone as the square color is what makes the operation safe.

No simulation of the wall is necessary. The construction order itself proves that the required cells are free. Python integers also need no special handling because all coordinates and operation counts are at most a few thousand.

## Worked Examples

### Example 1

For the provided input (n=2), there is only one (2 \times 2) square.

| Square ((x,y)) | First seed | Second seed | Square operation | Operations used |
| --- | --- | --- | --- | --- |
| ((1,1)) | ((1,2)), sand | ((2,1)), sand | ((1,1)), stone | 3 |

The resulting wall is

| Position | ((1,1)) | ((1,2)) |
| --- | --- | --- |
| Row 1 | stone | sand |
| Row 2 | sand | stone |

The sample uses a different but equally valid ordering, namely two stone singleton operations followed by one sand square operation. The problem accepts any valid construction within the operation limit. Our construction also uses exactly (3=3\cdot2^2/4) operations.

### Example 2

For (n=4), there are four disjoint (2 \times 2) squares.

| Square ((x,y)) | First seed | Second seed | Final square operation | Total operations |
| --- | --- | --- | --- | --- |
| ((1,1)) | ((1,2)), sand | ((2,1)), sand | stone | 3 |
| ((1,3)) | ((1,4)), sand | ((2,3)), sand | stone | 3 |
| ((3,1)) | ((3,2)), sand | ((4,1)), sand | stone | 3 |
| ((3,3)) | ((3,4)), sand | ((4,3)), sand | stone | 3 |

After the first square is complete, the cell ((2,3)) in the second square is adjacent to the completed square on its left. The cell ((3,2)) in the third square is similarly adjacent to the completed square above. This is exactly why row-major processing works for interior squares.

The final count is (4\cdot3=12), while

[
\frac{3n^2}{4}=\frac{3\cdot16}{4}=12.
]

The example therefore reaches the operation limit exactly without exceeding it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2)) | There are (n^2/4) squares, and each produces three operations. |
| Space | (O(n^2)) | The output operations are stored before printing, with (3n^2/4) operations at most. |

With (n\le50), there are at most (2500) cells and (1875) generated operations. The construction performs only a constant amount of work per cell, so it is easily within the one-second time limit and far below the memory limit.

## Test Cases

Since the output is not unique, the tests should validate the generated operation sequence rather than compare it character-for-character with one particular valid output.

```python
# This test harness validates the construction itself.
# It can be used with the solve() implementation above.

import sys
import io

def build(n):
    ans = []

    for x in range(1, n, 2):
        for y in range(1, n, 2):
            ans.append((1, x, y + 1, 2))
            ans.append((1, x + 1, y, 2))
            ans.append((2, x, y, 1))

    out = [str(len(ans))]
    out.extend(f"{t} {x} {y} {b}" for t, x, y, b in ans)
    return "\n".join(out) + "\n"

def validate(inp: str) -> str:
    n = int(inp.strip())
    output = build(n)

    data = list(map(int, output.split()))
    k = data[0]
    assert 1 <= k <= 3 * n * n // 4

    board = [[0] * n for _ in range(n)]
    p = 1

    def wanted(i, j):
        # i and j are zero-based here.
        return 1 if (i + j) % 2 == 0 else 2

    def free(i, j):
        if board[i][j] != 0:
            return False

        if i == 0 or i == n - 1 or j == 0 or j == n - 1:
            return True

        return (
            board[i - 1][j] != 0
            or board[i + 1][j] != 0
            or board[i][j - 1] != 0
            or board[i][j + 1] != 0
        )

    for _ in range(k):
        t, x, y, b = data[p:p + 4]
        p += 4

        x -= 1
        y -= 1

        if t == 1:
            assert 0 <= x < n
            assert 0 <= y < n
            assert free(x, y)
            assert wanted(x, y) == b
            board[x][y] = b

        else:
            assert t == 2
            assert 0 <= x < n - 1
            assert 0 <= y < n - 1

            cells = [
                (x, y),
                (x, y + 1),
                (x + 1, y),
                (x + 1, y + 1),
            ]

            assert any(free(i, j) for i, j in cells)

            for i, j in cells:
                if board[i][j] == 0:
                    assert wanted(i, j) == b

            for i, j in cells:
                if board[i][j] == 0:
                    board[i][j] = b

    for i in range(n):
        for j in range(n):
            assert board[i][j] == wanted(i, j)

    return output

# Provided sample.
sample1 = validate("2")
assert sample1.startswith("3\n"), "sample 1"

# Minimum size, exercising the single 2x2 square.
case2 = validate("2")
assert case2.splitlines()[0] == "3"

# A small interior case, where reachability depends on previously
# completed squares.
case3 = validate("4")
assert case3.splitlines()[0] == "12"

# Another even size, catching row and column progression errors.
case4 = validate("6")
assert case4.splitlines()[0] == "27"

# Maximum allowed n.
case5 = validate("50")
assert case5.splitlines()[0] == str(3 * 50 * 50 // 4)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | 3 operations | Minimum size and the fact that the first square needs two seeds before the square operation |
| `4` | 12 operations | Interior squares and propagation from the top and left |
| `6` | 27 operations | Repeated row and column transitions |
| `50` | 1875 operations | Maximum size and the exact operation bound |

## Edge Cases

For (n=2), the input is

```
2
```

The only square is ((1,1)). The algorithm first fills ((1,2)) with sand and then ((2,1)) with sand. Both are border cells, so both singleton operations are valid. The final (2 \times 2) operation fills ((1,1)) and ((2,2)) with stone. The output uses exactly three operations.

For an interior square, consider (n=4) and the square starting at ((3,3)). Before reaching it, the squares starting at ((1,1)), ((1,3)), and ((3,1)) have already been completed. The cell ((3,4)) is free because it is adjacent to the completed square above, while ((4,3)) is free because it is adjacent to the completed square on the left. Both are sand cells, so they can be placed individually. The remaining cells ((3,3)) and ((4,4)) are both stone, and the final square operation fills exactly those cells.

The boundary cases where (x=1) or (y=1) are handled without special code. If (x=1), the first seed lies on the top border. If (y=1), the second seed lies on the left border. Once the construction moves farther inward, the corresponding previously completed square provides the required neighboring block.

The maximum case (n=50) contains (25) block rows and (25) block columns, giving (625) disjoint (2 \times 2) squares. Each square costs three operations, so the construction produces (625\cdot3=1875) operations, exactly equal to (3n^2/4). No operation count or coordinate exceeds the stated limits.
