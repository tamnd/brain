---
title: "CF 1503B - 3-Coloring"
description: "Alice and Bob are filling an $n times n$ grid. On every turn Alice first announces a color from ${1,2,3}$. Bob must then choose an empty cell and place a token of a different color. Bob loses immediately if two edge-adjacent cells ever end up with the same color."
date: "2026-06-10T20:54:11+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "games", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1503
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 712 (Div. 1)"
rating: 1700
weight: 1503
solve_time_s: 389
verified: false
draft: false
---

[CF 1503B - 3-Coloring](https://codeforces.com/problemset/problem/1503/B)

**Rating:** 1700  
**Tags:** constructive algorithms, games, interactive  
**Solve time:** 6m 29s  
**Verified:** no  

## Solution
## Problem Understanding

Alice and Bob are filling an $n \times n$ grid. On every turn Alice first announces a color from $\{1,2,3\}$. Bob must then choose an empty cell and place a token of a different color.

Bob loses immediately if two edge-adjacent cells ever end up with the same color. His goal is to fill the entire board while avoiding such conflicts.

In the original interactive version, Alice chooses colors adaptively. In the hacked version used on Codeforces, we are given all of Alice's future color choices in advance. We only need to output any valid sequence of Bob's moves.

The board size is at most $100 \times 100$, so there are at most $10^4$ turns. Any solution that performs a constant amount of work per move is easily fast enough. The challenge is not computational complexity, it is constructing moves that are always legal regardless of Alice's choices.

The first subtle point is that Bob cannot simply color cells greedily with one fixed color. Consider $n=2$ and Alice repeatedly choosing color $1$. If Bob always responds with color $2$, adjacent cells eventually receive the same color and a conflict appears.

Another easy mistake is to partition the board correctly but forget that Bob's chosen color must differ from Alice's current color. Suppose a cell belongs to the group that is supposed to receive color $1$. If Alice also announces $1$, Bob cannot use that color and must temporarily use color $3$ instead.

A third pitfall appears near the end of the game. One partition may become empty before the other. A solution that always tries to play from a preferred partition will fail once that partition runs out of cells. The strategy must explicitly handle the situation where only one partition remains.

## Approaches

A brute force mindset is to treat every move independently. Given Alice's color, search all empty cells and all allowed colors, looking for a move that keeps the board conflict-free. Such a move always exists, but proving it and implementing it cleanly is difficult. Even if we scan the entire board every turn, the complexity is roughly $O(n^4)$: there are $n^2$ turns, and each turn may inspect $O(n^2)$ cells. With $n=100$, that reaches around $10^8$ operations.

The key observation comes from the structure of the grid graph. A chessboard coloring splits the cells into two independent sets. Every edge connects one black cell and one white cell.

Suppose we reserve color $1$ for all black cells and color $2$ for all white cells. If we could always follow that plan, adjacent cells would automatically have different colors because neighboring cells belong to opposite partitions.

Alice only prevents one color at a time. If she says $1$, we can still place color $2$. If she says $2$, we can still place color $1$. The only difficult situation occurs when the partition whose reserved color is available has already been exhausted.

The solution is to maintain two lists:

- Cells of one chessboard parity, associated with color $1$.
- Cells of the other parity, associated with color $2$.

As long as both lists are non-empty, Alice's choice determines which partition we use. If Alice says $1$, we take a cell from the color-$2$ partition and paint it $2$. If Alice says $2$, we take a cell from the color-$1$ partition and paint it $1$. If Alice says $3$, either partition works.

Eventually one partition becomes empty. At that point all remaining cells belong to the other partition. Their reserved color may sometimes be forbidden by Alice. When that happens, we use color $3$ instead. Since all remaining cells lie in the same chessboard partition, none of them are adjacent to each other, so introducing color $3$ cannot create a conflict.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^4)$ | $O(n^2)$ | Too slow / unnecessary |
| Optimal | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Split all board cells into two groups according to chessboard parity.

Cells with $(i+j)\bmod 2=0$ go into the first group. Cells with $(i+j)\bmod 2=1$ go into the second group.
2. Reserve color $1$ for the first group and color $2$ for the second group.

This assignment guarantees that neighboring cells would receive different colors if the reservation were followed exactly.
3. For each color announced by Alice, first check whether both groups still contain unused cells.
4. If both groups are non-empty and Alice chose color $1$, take any unused cell from the second group and paint it color $2$.

Color $2$ is legal because it differs from Alice's color.
5. If both groups are non-empty and Alice chose color $2$, take any unused cell from the first group and paint it color $1$.
6. If both groups are non-empty and Alice chose color $3$, choose either group. Conventionally, use the first group and paint it color $1$.
7. If the first group is empty, all remaining cells belong to the second group.

Their reserved color is $2$.

If Alice did not choose $2$, paint a remaining cell with $2$.

Otherwise paint it with $3$.
8. If the second group is empty, all remaining cells belong to the first group.

Their reserved color is $1$.

If Alice did not choose $1$, paint a remaining cell with $1$.

Otherwise paint it with $3$.

### Why it works

The invariant is that every cell from the first chessboard partition receives either color $1$ or, when forced, color $3$. Every cell from the second partition receives either color $2$ or, when forced, color $3$.

While both partitions are available, we never use color $3$. Each partition receives only its reserved color, so adjacent cells always have different colors.

Once one partition becomes empty, all remaining cells belong to a single chessboard partition. No two cells inside the same partition are adjacent. Replacing the reserved color with color $3$ when necessary cannot create a conflict because there is no neighboring cell in that partition.

Every move uses a color different from Alice's choice, and every cell is used exactly once. Hence the board is completely filled without ever creating equal-colored adjacent cells.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    alice = list(map(int, input().split()))

    p1 = []
    p2 = []

    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                p1.append((i + 1, j + 1))
            else:
                p2.append((i + 1, j + 1))

    ans = []

    for a in alice:
        if p1 and p2:
            if a == 1:
                x, y = p2.pop()
                ans.append((2, x, y))
            elif a == 2:
                x, y = p1.pop()
                ans.append((1, x, y))
            else:
                x, y = p1.pop()
                ans.append((1, x, y))

        elif p1:
            x, y = p1.pop()

            if a == 1:
                ans.append((3, x, y))
            else:
                ans.append((1, x, y))

        else:
            x, y = p2.pop()

            if a == 2:
                ans.append((3, x, y))
            else:
                ans.append((2, x, y))

    sys.stdout.write(
        "\n".join(f"{c} {i} {j}" for c, i, j in ans)
    )

solve()
```

The two arrays `p1` and `p2` store the unused cells of the two chessboard partitions. Removing a cell with `pop()` is $O(1)$, so each move requires constant work.

The first branch handles the main phase where both partitions still contain cells. Alice's choice determines which reserved color remains available. We immediately use a cell from the corresponding partition.

The second and third branches handle the endgame. Only one partition remains, so we use its reserved color whenever possible. If Alice blocks that color, we switch to color `3`.

The implementation stores coordinates using one-based indexing because the problem output expects rows and columns numbered from `1`.

## Worked Examples

### Example 1

Input:

```
n = 2
Alice = [1, 2, 1, 3]
```

Initial partitions:

| Partition | Cells |
| --- | --- |
| p1 | (1,1), (2,2) |
| p2 | (1,2), (2,1) |

| Turn | Alice | Action | Output |
| --- | --- | --- | --- |
| 1 | 1 | take from p2, use |  |
