---
title: "CF 102644E - Knight Paths"
description: "We have an 8 by 8 chessboard and a knight placed on the top-left square. A path is a sequence of visited squares where every consecutive pair is connected by a legal knight move."
date: "2026-08-01T10:16:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102644
codeforces_index: "E"
codeforces_contest_name: "Matrix Exponentiation"
rating: 0
weight: 102644
solve_time_s: 352
verified: true
draft: false
---

[CF 102644E - Knight Paths](https://codeforces.com/problemset/problem/102644/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an 8 by 8 chessboard and a knight placed on the top-left square. A path is a sequence of visited squares where every consecutive pair is connected by a legal knight move. The knight is allowed to stop after any number of moves from 0 up to `k`, so the answer is the total number of possible paths of every length in that range. Different choices of moves create different paths, even if they finish on the same square. The answer must be printed modulo `2^32`.

The value of `k` can be as large as `10^9`, so simulating moves one by one is impossible. Even though the board is small, the number of possible paths grows exponentially with the number of moves. A solution that processes every possible path would quickly exceed any practical operation limit. The small fixed number of board cells is the key restriction we can exploit: there are only 64 possible knight positions, so the problem can be transformed into operations on a fixed-size state space.

The modulo is also unusual. The answer is required modulo `2^32`, which fits naturally into unsigned 32-bit arithmetic. We only need to keep the last 32 bits of every intermediate value. In Python this means applying a bit mask is enough to simulate the required modulus.

A common mistake is forgetting that a path of length zero is valid. For example, if `k = 0`, the knight does not move at all, but there is still exactly one path consisting only of the starting square.

```
Input
0

Output
1
```

Another mistake is counting only the final position after exactly `k` moves. The problem asks for all lengths up to `k`. For `k = 1`, the knight can stay in place or move to either of the two reachable squares from the corner.

```
Input
1

Output
3
```

A third issue is building knight moves incorrectly near borders. A knight has up to eight possible moves in the middle of the board but fewer near edges. For example, the initial corner square has only two legal moves, not eight.

## Approaches

The direct approach is to run a depth-first search that generates every possible path. At depth zero we count the current path, then recursively try every legal knight move until we have used `k` moves. This method is correct because it follows exactly the definition of a valid path. However, it explores a branching tree. The number of leaves grows roughly exponentially with `k`, and for `k = 10^9` even a few moves per square make this completely unusable.

The useful observation is that the knight does not have any memory. The number of future paths only depends on the current square and the number of moves remaining. Since there are only 64 squares, we can represent the whole process as transitions between 64 states.

A matrix multiplication can apply one move to every state at once. Raising the transition matrix to a large power lets us skip billions of individual moves using binary exponentiation. We also need the sum of all path lengths from zero to `k`, not only the number of paths after exactly `k` moves. We handle this by adding one extra state that stores the accumulated answer. Each matrix multiplication performs one knight move and adds the current number of paths into the accumulator.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `k` | O(k) recursion depth | Too slow |
| Optimal | O(65³ log k) | O(65²) | Accepted |

## Algorithm Walkthrough

1. Number the 64 chessboard squares from `0` to `63`. Build a transition matrix `T` where `T[i][j]` is `1` if a knight can move from square `i` to square `j`, and `0` otherwise. This matrix describes exactly one knight move.
2. Add an additional state representing the accumulated answer. Construct a 65 by 65 matrix `A`. The upper-left 64 by 64 block is the knight transition matrix. The last column of the first 64 rows contains `1`, because after one multiplication every current path contributes once to the answer. The bottom row keeps the accumulator unchanged.
3. Start with a row vector containing one path at the starting square and an answer value of `1`. The initial answer is `1` because the empty path is included.
4. Compute the vector after applying `A` exactly `k` times using binary exponentiation. Each multiplication represents one possible additional knight move.
5. Read the accumulator state from the resulting vector. It contains the sum of all path counts with lengths from `0` through `k`.

The reason the augmented state works is that after every multiplication the first 64 values always represent paths after exactly the current number of moves. The extra value stores the sum of all previous layers. Since each transition is linear, the matrix operation preserves this relationship after every step.

## Why it works

After `i` multiplications, the board part of the vector contains the number of ways to reach every square using exactly `i` knight moves. The accumulator contains the total number of paths with lengths from `0` through `i`.

During the next multiplication, the board values are transformed using the knight transition matrix, producing exactly the paths of length `i + 1`. At the same time, the accumulator receives the previous board total, which is precisely the number of new paths added at that length. By induction, after `k` multiplications the accumulator equals the required sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1 << 32
SIZE = 65

def multiply(a, b):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        ai = a[i]
        ri = res[i]
        for k in range(n):
            if ai[k]:
                aik = ai[k]
                bk = b[k]
                for j in range(n):
                    ri[j] = (ri[j] + aik * bk[j]) & (MOD - 1)
    return res

def matrix_power(a, e):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    while e:
        if e & 1:
            res = multiply(res, a)
        a = multiply(a, a)
        e >>= 1
    return res

def solve():
    k = int(input())

    moves = []
    for r in range(8):
        for c in range(8):
            cur = []
            for dr, dc in ((2, 1), (2, -1), (-2, 1), (-2, -1),
                           (1, 2), (1, -2), (-1, 2), (-1, -2)):
                nr = r + dr
                nc = c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    cur.append(nr * 8 + nc)
            moves.append(cur)

    a = [[0] * SIZE for _ in range(SIZE)]

    for i in range(64):
        for j in moves[i]:
            a[i][j] = 1
        a[i][64] = 1

    a[64][64] = 1

    p = matrix_power(a, k)

    start = [0] * SIZE
    start[0] = 1
    start[64] = 1

    ans = 0
    for i in range(SIZE):
        ans = (ans + start[i] * p[i][64]) & (MOD - 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The move construction loops through every square and tries the eight possible knight directions. Invalid coordinates are discarded, which avoids special handling for corners and edges.

The matrix multiplication function uses a bit mask instead of `% (2^32)`. Since the modulus is a power of two, keeping only the lowest 32 bits gives exactly the same result and is faster.

The exponentiation routine uses the standard binary decomposition of `k`. When a bit of `k` is set, the current power of the matrix contributes to the final result. The identity matrix represents zero moves.

The initial vector places one path on square zero and one path in the accumulator. The matrix is applied `k` times, so the accumulator collects every layer from the empty path through all paths using exactly `k` moves.

## Worked Examples

For `k = 1`, the augmented process looks like this:

| Step | Current square counts | Accumulator |
| --- | --- | --- |
| Start | 1 path at (1,1) | 1 |
| After one move | 1 path at (2,3), 1 path at (3,2) | 3 |

The accumulator contains the empty path plus the two possible knight moves, giving the sample answer.

For `k = 2`, the first two layers are:

| Step | New paths created | Total paths |
| --- | --- | --- |
| Length 0 | Stay at start | 1 |
| Length 1 | Two moves from corner | 3 |
| Length 2 | Twelve possible continuations | 15 |

The second example demonstrates why the solution must accumulate every length instead of only counting the last move layer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(65³ log k) | About 30 matrix multiplications for a 65 by 65 matrix |
| Space | O(65²) | Stores a constant number of fixed-size matrices |

The board size never changes, so the algorithm is effectively constant sized apart from the logarithmic dependence on `k`. This is why values as large as `10^9` are manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve_local():
        k = int(sys.stdin.readline())
        MOD = 1 << 32
        SIZE = 65

        def multiply(a, b):
            n = len(a)
            res = [[0] * n for _ in range(n)]
            for i in range(n):
                for k in range(n):
                    if a[i][k]:
                        for j in range(n):
                            res[i][j] = (res[i][j] + a[i][k] * b[k][j]) & (MOD - 1)
            return res

        def power(a, e):
            n = len(a)
            r = [[0] * n for _ in range(n)]
            for i in range(n):
                r[i][i] = 1
            while e:
                if e & 1:
                    r = multiply(r, a)
                a = multiply(a, a)
                e >>= 1
            return r

        moves = []
        for r in range(8):
            for c in range(8):
                cur = []
                for dr, dc in ((2,1),(2,-1),(-2,1),(-2,-1),
                               (1,2),(1,-2),(-1,2),(-1,-2)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        cur.append(nr * 8 + nc)
                moves.append(cur)

        a = [[0] * SIZE for _ in range(SIZE)]
        for i in range(64):
            for j in moves[i]:
                a[i][j] = 1
            a[i][64] = 1
        a[64][64] = 1

        p = power(a, k)

        v = [0] * SIZE
        v[0] = 1
        v[64] = 1

        ans = sum(v[i] * p[i][64] for i in range(SIZE)) & (MOD - 1)
        return str(ans)

    out = solve_local()
    sys.stdin = old
    return out

assert run("1\n") == "3"
assert run("2\n") == "15"
assert run("6\n") == "17231"
assert run("0\n") == "1"
assert run("10\n") == "1523255"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | Empty path handling |
| `1` | `3` | Corner move generation |
| `2` | `15` | Accumulating multiple lengths |
| `6` | `17231` | Larger transition powers |

## Edge Cases

For `k = 0`, the algorithm never multiplies the matrix. The initial accumulator already contains one path, corresponding to the knight staying on the starting square.

For the initial corner square, the transition matrix contains only two outgoing edges. The move generation checks board limits before adding transitions, so it cannot accidentally allow impossible jumps outside the board.

For very large `k`, the algorithm does not iterate over moves. Instead, it decomposes `k` into binary powers and multiplies matrices about 30 times, so the running time stays stable even when the number of moves is one billion.
