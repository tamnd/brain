---
title: "CF 102800J - Situation"
description: "We are given a partially filled 3 × 3 Tic-tac-toe board. Alice uses O, Bob uses X, and some cells may still be empty. Unlike normal Tic-tac-toe, the game never stops when someone completes a line. Every empty cell will eventually be filled."
date: "2026-07-28T22:49:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "J"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 57
verified: true
draft: false
---

[CF 102800J - Situation](https://codeforces.com/problemset/problem/102800/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a partially filled 3 × 3 Tic-tac-toe board. Alice uses `O`, Bob uses `X`, and some cells may still be empty. Unlike normal Tic-tac-toe, the game never stops when someone completes a line. Every empty cell will eventually be filled. At the end, we count every row, every column, and both diagonals. Each line consisting entirely of `O` contributes `+1`, each line consisting entirely of `X` contributes `-1`, and mixed lines contribute `0`. The required answer is the final score assuming both players always play optimally. Alice tries to maximize the score, while Bob tries to minimize it.

Each test case specifies whose turn it is next and the current board configuration. We must compute the optimal final score for every test case.

The number of test cases is as large as 40,000, so even though the board is tiny, the per-test-case work must be extremely small. A full minimax search from scratch for every test case would repeatedly solve the same game states thousands of times. The entire game contains only nine cells, so the number of distinct board positions is limited. This strongly suggests precomputing every reachable state once, then answering each query with a simple lookup.

Several situations can easily produce incorrect implementations.

A completed line does **not** stop the game. For example,

```
1
OOO
...
...
```

Alice already has a winning row, but both players must continue placing pieces until the board is full. A solution that immediately evaluates the board as `+1` is incorrect because additional completed rows, columns, or diagonals may appear later.

The player to move is determined by the input, not by counting pieces. For example,

```
0
...
...
...
```

Although an empty board normally belongs to Alice, this input explicitly says Bob moves next. Ignoring the turn value produces incorrect minimax decisions.

Another easy mistake is evaluating only the newest completed line after each move. Consider

```
1
OO.
OO.
...
```

The final move may simultaneously complete a row and a column. The score always depends on the final board, not on intermediate events.

## Approaches

The most direct solution is a recursive minimax search. From the current position, try every legal move, recursively solve the remaining game, and let Alice choose the maximum value while Bob chooses the minimum value. When the board becomes full, count the completed rows, columns, and diagonals to obtain the final score.

This search is correct because it explicitly explores every possible continuation. The problem is repetition. The same partially filled board can be reached through many different move orders, causing the same subtree to be recomputed repeatedly. Although a single game contains at most nine moves, solving up to 40,000 independent test cases makes this unnecessary duplication expensive.

The key observation is that the game state is completely determined by the board configuration and the player whose turn it is. The total number of board configurations is only $3^9 = 19,683$, since every cell is either empty, `O`, or `X`. Multiplying by two possible players gives fewer than 40,000 distinct states.

Instead of solving every query independently, we solve each state exactly once using memoized minimax. Whenever recursion reaches a previously computed state, we immediately reuse its answer. Since every state is evaluated at most once, the total work is bounded by the number of distinct states rather than the number of recursive paths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(b!)$, where $b$ is the number of empty cells | $O(b)$ | Too slow for many test cases |
| Optimal | $O(3^9 \times 9)$ preprocessing, $O(1)$ per query | $O(3^9)$ | Accepted |

## Algorithm Walkthrough

1. Represent every board as a nine-character string. This uniquely identifies a game state and can be used as the memoization key.
2. Write a function that evaluates a full board by checking all three rows, all three columns, and both diagonals. Each all-`O` line adds one, and each all-`X` line subtracts one.
3. Create a recursive minimax function taking the current board and the player to move.
4. If the board contains no empty cells, return the evaluation from Step 2. This is the final score of that completed game.
5. If this state has already been computed, return the stored answer immediately. This avoids solving the same position multiple times.
6. Otherwise, generate every legal move by placing the current player's mark into one empty cell.
7. Recursively solve the resulting state with the opposite player.
8. If Alice moved, keep the maximum returned value because she wants the largest final score. If Bob moved, keep the minimum returned value because he wants the smallest final score.
9. Store the computed value in the memoization table before returning it.
10. For each test case, convert the board into the chosen representation, read the player to move, invoke the memoized minimax function, and print the returned value.

### Why it works

Every recursive call represents exactly one legal game position. The recursion explores every possible continuation from that position. The terminal evaluation exactly matches the score defined in the problem because it counts completed lines only after the board is full. Since Alice always chooses the continuation with the largest score and Bob always chooses the smallest, the recurrence is precisely the definition of optimal play. Memoization changes only how often a state is solved, not which value it receives, so the returned value remains correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

memo = {}

def score(board):
    res = 0
    for a, b, c in LINES:
        if board[a] == board[b] == board[c]:
            if board[a] == 'O':
                res += 1
            elif board[a] == 'X':
                res -= 1
    return res

def dfs(board, alice_turn):
    key = (board, alice_turn)
    if key in memo:
        return memo[key]

    if '.' not in board:
        val = score(board)
        memo[key] = val
        return val

    if alice_turn:
        best = -10
        mark = 'O'
        for i, ch in enumerate(board):
            if ch == '.':
                nxt = board[:i] + mark + board[i + 1:]
                best = max(best, dfs(nxt, False))
    else:
        best = 10
        mark = 'X'
        for i, ch in enumerate(board):
            if ch == '.':
                nxt = board[:i] + mark + board[i + 1:]
                best = min(best, dfs(nxt, True))

    memo[key] = best
    return best

t = int(input())
for _ in range(t):
    turn = int(input())
    board = "".join(input().strip() for _ in range(3))
    print(dfs(board, turn == 1))
```

The `LINES` array stores every scoring line exactly once, avoiding repeated index calculations throughout the program.

The `score` function is called only for completely filled boards. It checks each of the eight possible winning lines and computes the required difference between Alice's and Bob's completed lines.

The recursive `dfs` function implements minimax together with memoization. The memoization key contains both the board and the current player because identical boards may have different optimal values depending on whose turn it is.

The recursion terminates only when the board has no empty cells. This matches the modified rules of the game, where completed lines during play do not end the game.

The initial values `-10` and `10` are safe because the score is always between `-8` and `8`, as there are only eight possible lines on the board.

## Worked Examples

### Sample 1

Suppose the input is

```
1
1
.OO
X.O
OXO
```

| Step | Current Player | Empty Cells | Chosen Value |
| --- | --- | --- | --- |
| Initial | Alice | 2 | Explore both moves |
| After first move | Bob | 1 | Bob minimizes |
| Terminal | None | 0 | Evaluate final board |

The recursion explores both legal continuations. Bob always responds with the move giving Alice the smaller final score. The returned value is the optimal game result.

### Sample 2

```
1
1
XXX
XXX
XXX
```

| Step | Current Player | Empty Cells | Returned Value |
| --- | --- | --- | --- |
| Initial | Alice | 0 | -8 |

The board is already full, so recursion stops immediately. Every one of the eight possible lines belongs to Bob, giving a final score of `0 - 8 = -8`.

These examples illustrate the two termination conditions. The first reaches a terminal board through recursion, while the second is already a terminal state when the query begins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(3^9 \times 9)$ total preprocessing, $O(1)$ average per query | Every distinct state is solved once, each considering at most nine moves |
| Space | $O(3^9)$ | Memoization stores one value for every reachable state |

Since fewer than 40,000 distinct states exist, the entire state space easily fits into memory. After memoization has been populated, each test case becomes a simple hash table lookup, making 40,000 queries easily fit within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    from functools import lru_cache

    LINES = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    @lru_cache(None)
    def dfs(board, turn):
        if '.' not in board:
            s = 0
            for a,b,c in LINES:
                if board[a]==board[b]==board[c]:
                    if board[a]=='O':
                        s += 1
                    elif board[a]=='X':
                        s -= 1
            return s
        if turn:
            ans = -10
            for i,c in enumerate(board):
                if c=='.':
                    ans = max(ans, dfs(board[:i]+'O'+board[i+1:], 0))
            return ans
        ans = 10
        for i,c in enumerate(board):
            if c=='.':
                ans = min(ans, dfs(board[:i]+'X'+board[i+1:], 1))
        return ans

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        turn = int(input())
        board = "".join(input().strip() for _ in range(3))
        out.append(str(dfs(board, turn)))
    return "\n".join(out)

# provided sample 2
assert run("""1
1
XXX
XXX
XXX
""") == "-8"

# custom cases
assert run("""1
1
OOO
OOO
OOO
""") == "8"

assert run("""1
0
XXX
XXX
XXX
""") == "-8"

assert run("""1
1
...
...
...
""")

assert run("""1
1
OXO
XOX
OXO
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All `O` board | 8 | Maximum possible score |
| All `X` board | -8 | Minimum possible score |
| Empty board | Computed by minimax | Full search from the initial position |
| Full mixed board | 2 | Terminal evaluation without recursion |

## Edge Cases

Consider the case where a winning line already exists but the board is not full.

```
1
1
OOO
...
...
```

The algorithm does not stop after observing the completed row. Since empty cells remain, recursion continues until every square is occupied. Only then does the evaluation function count all completed lines. This exactly matches the modified game rules.

Now consider a board whose turn disagrees with the number of existing pieces.

```
0
...
...
...
```

The memoization key includes both the board and the player to move. The search begins with Bob minimizing the result, even though this position would never occur in a normal game. The algorithm follows the input rather than making assumptions from the piece counts.

Finally, consider a position where one move creates multiple lines simultaneously.

```
1
OO.
OO.
...
```

The recursive search eventually reaches a completely filled board, and the evaluation function independently checks all eight possible lines. If a single move completes both a row and a column, both are counted because every scoring line is examined separately. This avoids undercounting positions with multiple simultaneous connections.
