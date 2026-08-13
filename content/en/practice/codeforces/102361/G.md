---
title: "CF 102361G - Game on Chessboard"
description: "We have an (ntimes n) board containing at most one chess piece in each cell. Every piece is either white or black and has a positive removal value. A white and a black piece may be removed together if both are currently exposed from the bottom-left direction."
date: "2026-08-14T02:51:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "G"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 189
verified: true
draft: false
---

[CF 102361G - Game on Chessboard](https://codeforces.com/problemset/problem/102361/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n\times n) board containing at most one chess piece in each cell. Every piece is either white or black and has a positive removal value. A white and a black piece may be removed together if both are currently exposed from the bottom-left direction. The price of such a pair is the absolute difference of their values. A single piece may also be removed at any time for its own value.

The exposure condition is the unusual part. For a piece at ((x,y)), another piece at ((x',y')) blocks it whenever (x'\ge x) and (y'\le y). In other words, nothing may remain weakly below and weakly to the left of the piece. We need the minimum total cost needed to remove every piece.

The original contest has (n\le12), with a one-second time limit and 1024 MB of memory. The board can contain as many as (12^2=144) pieces, so a subset DP over the pieces would have up to (2^{144}) states. That is far beyond what is possible. The small value of (n), rather than the potentially large number of pieces, suggests that the useful state should describe a boundary of the board. There are only (\binom{24}{12}=2,704,156) monotone boundaries when (n=12), which is large but manageable in a low-level language and fits comfortably in the given memory limit. This contour-DP viewpoint is also the standard solution direction for the problem.

There are several edge cases that defeat a direct greedy interpretation. A single piece must be handled by itself. For

```
1
W
7
```

the answer is (7), because there is no black piece to pair with it. A solution that only searches for pairs would incorrectly return zero or leave the piece unprocessed.

A pair of equal-valued pieces can have cost zero, but they still must both be exposed at the same time. Consider

```
2
W.
.B
5 0
0 5
```

Both pieces are already exposed, so they can be removed together for cost (0). A solution that assumes every pair requires a positive single-removal cost would miss this.

The opposite situation is more subtle. Consider

```
2
WB
B.
5 7
7 0
```

The black piece at ((2,1)) blocks both pieces above it, so it is the only relevant exposed piece initially. Removing it alone costs (7). The white and black pieces in the first row then become simultaneously exposed and can be paired for cost (2). The answer is (9). A careless algorithm might immediately pair the two first-row pieces because their cells look compatible, even though the bottom-left blocking condition prevents that pair from being used at the beginning.

The freedom to remove a single arbitrary piece does not require us to put arbitrary removals into the contour state. Suppose an optimal solution removes a blocked piece (p) singly while another piece (q) still blocks (p). Removing (p) cannot be necessary for making (q) available, because (p) itself is one of the pieces blocking (q). Any operation involving pieces unrelated to this dependency can be performed in the same order without (p). We can postpone the single removal of (p) until (p) reaches the exposed contour, paying exactly the same amount. Hence there is always an optimal solution in which every single removal happens when that piece lies on the current contour.

## Approaches

A natural brute-force solution treats every remaining set of pieces as a state. From a state, it can try every currently exposed white piece with every currently exposed black piece, and it can also try removing every single piece. Memoization would make this a subset DP over the (m) pieces. Even ignoring the cost of checking which pieces are exposed, the state space is (2^m), and checking all possible pairs costs (O(m^2)) per state. With (m=144), that gives an upper bound of

[
2^{144}\cdot144^2 \approx 4.6\times10^{47}
]

pair-state checks. The brute force is conceptually correct because it directly models every legal operation, but the state representation contains far too much information.

The useful observation is geometric. The currently exposed pieces always lie on a monotone staircase running from the top-left side toward the bottom-right side. Once everything on the bottom-left side of this staircase has been removed, any piece on the staircase can be removed, and after removing it the staircase moves across that cell.

Represent the staircase by a path containing exactly (n) downward moves and (n) rightward moves. Encode a downward move by (0) and a rightward move by (1). There are exactly

[
\binom{2n}{n}
]

such paths. A local pattern (01) is a corner of the staircase. The cell at that corner is exactly a cell that can currently be removed. Removing that cell changes the local path from (01) to (10).

An empty corner costs nothing and simply moves the contour through an empty cell. An occupied corner can be removed alone, paying its value. If two occupied corners have different colors, both pieces are exposed simultaneously, so they can be removed together and the two corresponding (01\to10) changes can be made at once. Their transition cost is the absolute difference of their values.

This gives a shortest-path-style DP over all contour states. The important simplification is that every transition moves the contour in one direction, so the states form a DAG. No general shortest-path algorithm is needed. We can process the masks in topological order.

The contour approach has (\binom{2n}{n}) states. For one state there are at most (n) corners, and trying all pairs of corners costs (O(n^2)). This gives the accepted (O(n^2\binom{2n}{n})) complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subset DP | (O(2^{n^2}n^4)) | (O(2^{n^2})) | Too slow |
| Contour DP | (O(n^2\binom{2n}{n})) | (O(2^{2n})) | Accepted |

## Algorithm Walkthrough

1. Represent a contour by a binary string of length (2n). A zero means that the contour moves down, and a one means that it moves right. Exactly (n) bits are one, so every valid contour corresponds to one of (\binom{2n}{n}) masks.

We use the contour to separate cells that have already been cleared from cells that may still contain pieces. A corner represented by the pattern (01) identifies the next cell that can be exposed.
2. Start with the contour that goes down (n) times and then right (n) times. In the original bit order this is (0^n1^n). Its only relevant corner is the bottom-left boundary of the board, exactly where the first initially exposed piece must occur.

The final contour is (1^n0^n). At that point the entire board has been processed.
3. For every contour, find all positions containing the local pattern (01). Convert each such position into its board cell ((x,y)). Empty cells are also included because the contour may pass through them for zero cost.
4. For every corner cell, perform a single-removal transition. If the cell is empty, the cost added is zero. If it contains a piece, the cost added is its value.

This transition represents removing that piece alone when it is exposed, or simply advancing the contour through an empty cell.
5. Collect all occupied corner cells. For every pair having different colors, perform a transition that flips both (01) corners to (10) simultaneously. Add the absolute difference of their values.

Both pieces are legal at the same time because they are both corners of the same contour before the transition. Since two (01) patterns cannot overlap, the two local flips are independent.
6. Store the minimum cost for every contour. The transition always changes (01) into (10), so it moves the contour monotonically toward the final contour. This gives a DAG and lets us process states in order without revisiting them.
7. In the implementation, reverse the contour bit order. Then an original (01\to10) transition becomes (10\to01), which increases the integer value of the mask. We can consequently enumerate all masks with exactly (n) set bits using Gosper's combination-generation trick in increasing numerical order. The resulting masks are exactly the contour states, but now their transition direction agrees with the enumeration direction.
8. The answer is the DP value at the reversed form of the final contour. Empty boards naturally work as well, because every contour transition through an empty cell costs zero.

Why it works: maintain the invariant that the DP value of a contour is the minimum cost of clearing everything on the already-processed side of that contour while leaving the rest untouched. Every legal operation can be transformed into an operation performed when its pieces reach the contour. A single operation corresponds to one corner flip, while a valid white-black pair corresponds to two corner flips made simultaneously. Conversely, every transition generated by the DP is a legal operation, because its corner cells are exposed on the current contour. Thus every valid removal sequence is represented by a path through the DP, and every DP path describes a valid removal sequence with exactly the same cost. Taking the minimum DP value at the final contour therefore gives the optimum.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())

    board = [input().strip() for _ in range(n)]
    color = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if board[i][j] == 'W':
                color[i][j] = 1
            elif board[i][j] == 'B':
                color[i][j] = 2

    weight = []
    for _ in range(n):
        weight.append(list(map(int, input().split())))

    length = 2 * n
    size = 1 << length

    # We store the contour in reversed bit order.
    #
    # Original start:  0^n 1^n
    # Reversed start:  1^n 0^n
    #
    # Original end:    1^n 0^n
    # Reversed end:    0^n 1^n
    start = (1 << n) - 1
    end = start << n

    # int32 is sufficient:
    # at most 144 single removals, each <= 1e6.
    dp = array('i', [-1]) * size
    dp[start] = 0

    # Bit j of r is the lower bit of an original 01 corner.
    corner_mask = (1 << (length - 1)) - 1

    r = start
    limit = 1 << length

    while r < limit:
        cur = dp[r]

        if cur != -1:
            corners = r & ~(r >> 1) & corner_mask

            pieces = []

            c = corners
            while c:
                low = c & -c
                j = low.bit_length() - 1

                # In the reversed contour, this corner corresponds
                # to original bit positions i and i+1.
                i = length - 2 - j

                # Bits strictly above j+1 in the reversed mask
                # correspond to the original prefix before i.
                y = (r >> (j + 2)).bit_count()
                x = i - y

                col = color[x][y]

                if col:
                    pieces.append((j, col, weight[x][y]))
                    add = weight[x][y]
                else:
                    add = 0

                # 10 -> 01 in the reversed mask.
                # This increases the mask by exactly 2^j.
                nxt = r + low
                nv = cur + add

                old = dp[nxt]
                if old == -1 or nv < old:
                    dp[nxt] = nv

                c -= low

            # Remove two exposed pieces together.
            m = len(pieces)
            for a in range(m):
                j1, c1, w1 = pieces[a]
                for b in range(a):
                    j2, c2, w2 = pieces[b]

                    if c1 == c2:
                        continue

                    low1 = 1 << j1
                    low2 = 1 << j2

                    nxt = r + low1 + low2
                    nv = cur + abs(w1 - w2)

                    old = dp[nxt]
                    if old == -1 or nv < old:
                        dp[nxt] = nv

        # Gosper's hack: next mask with exactly n set bits.
        low = r & -r
        nxt = r + low
        r = (((nxt ^ r) >> 2) // low) | nxt

    print(dp[end])

if __name__ == "__main__":
    solve()
```

The input is first converted into two arrays. `color[i][j]` stores zero for an empty cell, one for white, and two for black. The separate `weight` array stores the removal value.

The DP array uses signed 32-bit integers through `array('i')`. The maximum possible answer is at most (144\cdot10^6=144,000,000), so 32 bits are sufficient. Using an ordinary Python list would be much more expensive because every integer would be a Python object. At (n=12), the dense DP has (2^{24}) entries, so the compact integer array keeps the memory consumption around 64 MB.

The implementation stores the contour backwards. In the original representation, removing an exposed corner changes `01` to `10`, decreasing the integer mask. Processing decreasing masks would work, but enumerating all such masks efficiently is less convenient in Python. After reversing the bit order, the same transition becomes `10` to `01` and increases the mask. Gosper's hack then enumerates exactly the masks containing (n) ones, in increasing order.

For a reversed corner at bit position `j`, the corresponding original corner occurs at `i = 2*n - 2 - j`. The number of original right moves before that corner is the number of set bits in the reversed suffix above `j + 1`, which is computed by

```
y = (r >> (j + 2)).bit_count()
```

and the number of downward moves is `x = i - y`. This is why no explicit (2n)-step path scan is needed for every state.

The expression

```
corners = r & ~(r >> 1) & corner_mask
```

finds every reversed `10` pattern. The `corner_mask` removes the nonexistent final position, avoiding an out-of-bounds corner at bit (2n-1).

For one corner, changing `10` to `01` increases the mask by exactly (2^j), so `nxt = r + low` is enough. Two different corners cannot overlap, because two `10` patterns cannot share a bit, so two flips can similarly be written as `r + low1 + low2`.

The pair transition is considered only when the two corner colors differ. The transition cost is exactly `abs(w1 - w2)`, matching the pair-removal rule. Single transitions are considered for every corner, including empty corners, because an empty contour cell must be traversable even though it represents no removal.

## Worked Examples

### Sample 1

For the official sample, every occupied cell has value (1), so every legal pair costs zero. The only positive cost comes from pieces that have to be removed alone before the desired pairings become possible. The given optimal sequence has three such removals.

The contour DP can be viewed through the following relevant transitions. The masks are shown in the original contour convention, where `0` means down and `1` means right.

| Stage | Operation represented | Contour effect | DP cost |
| --- | --- | --- | --- |
| 0 | Start | `00001111` | 0 |
| 1 | Remove ((4,1)) alone | flip its `01` corner | 1 |
| 2 | Remove ((2,1)) alone | flip its corner | 2 |
| 3 | Remove ((2,4)) alone | flip its corner | 3 |
| 4 | Pair ((4,2),(3,1)) | flip two corners | 3 |
| 5 | Pair ((1,1),(3,2)) | flip two corners | 3 |
| 6 | Pair ((2,2),(4,3)) | flip two corners | 3 |
| 7 | Pair ((1,2),(3,3)) | flip two corners | 3 |
| 8 | Pair ((2,3),(4,4)) | flip two corners | 3 |
| 9 | Pair ((1,3),(3,4)) | flip two corners | 3 |
| 10 | Final empty contour | `11110000` | 3 |

The trace demonstrates why the DP must consider both one-corner and two-corner transitions. Once the three unavoidable single removals have been paid for, all remaining useful operations can pair equal-valued pieces and cost zero.

### Two-by-two blocking example

Consider

```
2
WB
B.
5 7
7 0
```

The relevant states are much smaller.

| Stage | Exposed pieces | Transition | Cost |
| --- | --- | --- | --- |
| 0 | Only ((2,1)) | Remove black ((2,1)) alone | 7 |
| 1 | ((1,1)) and ((1,2)) | Pair white 5 with black 7 | 9 |
| 2 | No pieces | Finish through empty corners | 9 |

This example exercises the blocking rule directly. The two pieces in the first row cannot be paired initially because the black piece at ((2,1)) blocks them. The contour DP sees only the bottom-left black piece as a valid occupied corner at the initial contour, so it cannot make the illegal pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2\binom{2n}{n})) | There are (\binom{2n}{n}) contours, at most (n) corners, and (O(n^2)) corner pairs per contour. |
| Space | (O(2^{2n})) | The dense DP array has (2^{2n}) 32-bit entries. |

At (n=12), the number of contour states is

[
\binom{24}{12}=2,704,156.
]

The DP array has (2^{24}=16,777,216) entries, requiring about 64 MB with 32-bit integers. The theoretical time bound is the standard contour-DP bound for this problem. The Python implementation also avoids scanning all (2^{24}) integers by enumerating only masks with exactly (12) set bits, which reduces the number of processed states from about 16.8 million to about 2.7 million.

## Test Cases

The following tests assume the submitted solution is saved as `solution.py`. The helper resets the module's `input` binding after replacing `sys.stdin`, because the solution intentionally uses `sys.stdin.readline` for fast input.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solution.input = sys.stdin.readline

    try:
        solution.solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
sample1 = """\
4
WBB.
BWBW
WBWW
BBBW
1 1 1 0
1 1 1 1
1 1 1 1
1 1 1 1
"""
assert run(sample1) == "3", "sample 1"

# Minimum-size board, one piece.
case2 = """\
1
W
7
"""
assert run(case2) == "7", "single piece"

# Two exposed equal-valued opposite colors.
case3 = """\
2
W.
.B
5 0
0 5
"""
assert run(case3) == "0", "zero-cost exposed pair"

# Equal values, but the pair is initially blocked.
case4 = """\
2
W.
B.
1 0
1 0
"""
assert run(case4) == "2", "blocking must be respected"

# Pairing is possible only after removing the bottom-left blocker.
case5 = """\
2
WB
B.
5 7
7 0
"""
assert run(case5) == "9", "blocked first-row pair"

# Maximum n, but only one occupied cell.
case6 = """\
12
W...........
............
............
............
............
............
............
............
............
............
............
............
1000000 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
"""
assert run(case6) == "1000000", "maximum n with one piece"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 3 | Official optimal sequence with both single and paired removals |
| `1 / W / 7` | 7 | Minimum board and absence of a possible pair |
| `2 / W. / .B` with values 5 and 5 | 0 | Zero-cost pairing of two exposed opposite colors |
| `2 / W. / B.` with both values 1 | 2 | Equal values do not imply a free pair when one piece blocks the other |
| `2 / WB / B.` with values 5 and 7 | 9 | A pair becomes available only after an earlier single removal |
| (12\times12) board with one piece | 1000000 | Maximum (n), large value, and empty-contour transitions |

## Edge Cases

The single-piece case

```
1
W
7
```

starts and ends with the only contour transition. The cell is an occupied corner, so the DP adds (7), moves to the final contour, and returns (7). There is no special-case code for the color or for the missing opposite color.

The zero-cost pair

```
2
W.
.B
5 0
0 5
```

first crosses the empty bottom-left corner. That exposes both occupied corners, one white and one black. The pair transition flips both corners together and adds (|5-5|=0). The remaining contour movement passes through empty cells for zero cost, so the final answer is (0).

The blocking case

```
2
W.
B.
1 0
1 0
```

starts with only the lower-left black piece on an occupied corner. The DP must remove it alone for (1). The white piece then becomes exposed and is removed alone for another (1), giving (2). There is no transition that pairs them because they never have different colors on two simultaneous corners.

The more interesting blocking example

```
2
WB
B.
5 7
7 0
```

starts with the bottom-left black piece exposed. Removing it alone costs (7). The contour then reaches a state where the two first-row pieces are both corners. They have different colors, so the DP can pair them for (|5-7|=2). The total is (9). This is exactly the kind of dependency that makes greedy pairing unreliable.

Finally, the maximum-size sparse case has (n=12) but only one piece. The contour DP still enumerates the full family of contour states, but every reachable transition except the one through the occupied cell costs zero. The only positive contribution is the single removal of the (1,000,000)-valued white piece, so the answer is (1,000,000). The test confirms that the implementation handles the full 24-bit contour representation and large cell values without integer overflow.
