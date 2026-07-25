---
title: "CF 102878G - Nim plus"
description: "The game is played with a single pile containing n paper balls. Long Long and Mao Mao do not share the same legal moves. Long Long has a set of numbers he is allowed to remove, and Mao Mao has another set."
date: "2026-07-25T12:44:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "G"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 41
verified: true
draft: false
---

[CF 102878G - Nim plus](https://codeforces.com/problemset/problem/102878/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played with a single pile containing `n` paper balls. Long Long and Mao Mao do not share the same legal moves. Long Long has a set of numbers he is allowed to remove, and Mao Mao has another set. On a turn, a player chooses one number from their own set and removes exactly that many balls, but only if the pile contains enough balls. A player who cannot make a move loses. The task is to determine whether the first player, Long Long, can force a win with optimal play.

The input gives the initial number of balls, the size of both move sets, and the two sets themselves. The output is the winner's name in the required format. The important part of the problem is that the players have different move options, so ordinary impartial Nim theory does not directly apply. The state depends on whose turn it is.

The constraints are small enough for dynamic programming. The pile size can reach 5000, and each move set has at most 100 values. This means a solution around `n * m`, which is about 500,000 transitions, is easily fast enough. A simulation of every possible game sequence would be impossible because the number of possible move orders grows exponentially.

Several edge cases can break a careless implementation. If a player has a move larger than the current pile, that move cannot be used. For example:

```
5 1
6
7
```

The correct output is:

```
Mao Mao nb!
```

Long Long cannot remove 6 balls from a pile of size 5, so he loses immediately. An implementation that only checks whether a move exists in the set, without checking the current pile size, would give the wrong answer.

Another tricky case is when a player can move now but every resulting state gives the opponent a winning position. For example:

```
1 1
1
1
```

The correct output is:

```
Long Long nb!
```

Long Long removes the only ball, leaving Mao Mao unable to move. The algorithm must evaluate future positions, not only whether the current player has at least one legal move.

A third important situation appears when the two players have identical move sets. The winner is not determined by comparing the sets, because the first player advantage still depends on the current pile size. For example:

```
2 1
1
1
```

The correct output is:

```
Mao Mao nb!
```

Long Long removes one ball, leaving one ball for Mao Mao, who removes it and wins.

## Approaches

A direct approach is to recursively explore the game tree. For every state, we try every legal move for the current player. If any move sends the opponent to a losing state, the current player wins. This is correct because every possible game continuation is considered.

The problem is the number of repeated states. The same pile size can appear through many different sequences of moves. Without memoization, the recursion can revisit the same positions exponentially many times. Even with memoization, the natural state has two possibilities for the player turn and up to 5000 pile sizes, so dynamic programming is the right way to organize the computation.

The key observation is that the entire history is irrelevant. The only information needed is the number of balls remaining and whose turn it is. We can compute these states in increasing order of the pile size. Since every move decreases the pile size, every transition points to a state that has already been solved.

Let `winL[x]` mean Long Long can win when there are `x` balls and it is his turn. Let `winM[x]` mean Mao Mao can win when there are `x` balls and it is his turn.

For Long Long, a state is winning if there exists a legal removal that leaves Mao Mao in a losing state:

`winL[x] = true` if some `a` satisfies `a <= x` and `winM[x-a] = false`.

The same idea applies to Mao Mao:

`winM[x] = true` if some `b` satisfies `b <= x` and `winL[x-b] = false`.

The base state is `0` balls. A player with zero balls cannot move, so that player loses immediately. This means both `winL[0]` and `winM[0]` are false.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(number of states) with memoization | Too slow without DP structure |
| Optimal | O(nm) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create two dynamic programming arrays. `winL[i]` stores whether Long Long wins with `i` balls before his move, and `winM[i]` stores whether Mao Mao wins with `i` balls before his move. Both values start as false because a player with no balls cannot move.
2. Process pile sizes from `1` to `n`. For each size, try every move available to Long Long. If a move is not larger than the current pile and the resulting Mao Mao state is losing, mark `winL[i]` as true. This follows the normal game rule that one winning move is enough.
3. For the same pile size, try every move available to Mao Mao. If one move leaves Long Long in a losing state, mark `winM[i]` as true.
4. After all states are calculated, check `winL[n]`. If it is true, Long Long can force a victory. Otherwise Mao Mao can force the win.

Why it works:

The invariant of the dynamic programming is that when we calculate state `i`, every possible next state has already been calculated because every move reduces the pile size. For a player to win, there must exist at least one move leading to an opponent state where the opponent cannot force a victory. The transitions check exactly these possibilities, so every state is classified correctly. Since the initial game is simply Long Long's turn with `n` balls, `winL[n]` gives the answer.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    win_l = [False] * (n + 1)
    win_m = [False] * (n + 1)

    for i in range(1, n + 1):
        for x in a:
            if x <= i and not win_m[i - x]:
                win_l[i] = True
                break

        for x in b:
            if x <= i and not win_l[i - x]:
                win_m[i] = True
                break

    if win_l[n]:
        print("Long Long nb!")
    else:
        print("Mao Mao nb!")

if __name__ == "__main__":
    solve()
```

The two arrays represent the two different players' turns. Keeping separate arrays is necessary because the same pile size can be winning for one player and losing for the other due to their different move sets.

The loops go upward from smaller piles to larger piles. When calculating `win_l[i]`, every state `win_m[i - x]` is already known because `i - x < i`. The same property holds for Mao Mao's states.

The condition `x <= i` is the boundary check that prevents illegal removals. The early `break` is only an optimization. Once a winning move is found, checking other moves cannot change the result.

## Worked Examples

Sample 1:

```
5 1
6
7
```

| Balls | Long Long state | Mao Mao state | Reason |
| --- | --- | --- | --- |
| 0 | Lose | Lose | No legal moves |
| 1 | Lose | Lose | Both moves are too large |
| 2 | Lose | Lose | Both moves are too large |
| 3 | Lose | Lose | Both moves are too large |
| 4 | Lose | Lose | Both moves are too large |
| 5 | Lose | Lose | Long Long cannot remove 6 |

The first player has no legal move at the initial state, so Mao Mao wins.

Sample 2:

```
20 3
3 7 10
2 6 7
```

| Balls | Long Long state | Mao Mao state | Reason |
| --- | --- | --- | --- |
| 0 | Lose | Lose | No moves |
| 1 | Lose | Lose | No legal removals |
| 3 | Win | Lose | Long Long can remove 3 |
| 10 | Win | Win | Both players have winning replies |
| 20 | Win | Unknown after checking | Long Long removes 10 and leaves 10 |

The important part of this trace is that a winning move does not need to empty the pile. Long Long only needs to move to a state where Mao Mao cannot force a win.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every pile size checks every move from both sets |
| Space | O(n) | Two boolean arrays store all solved states |

With `n <= 5000` and `m <= 100`, the algorithm performs about one million simple checks in the worst case, which fits comfortably within the limits.

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

# provided samples
assert run("""5 1
6
7
""") == "Mao Mao nb!\n", "sample 1"

assert run("""20 3
3 7 10
2 6 7
""") == "Long Long nb!\n", "sample 2"

# minimum size
assert run("""1 1
1
1
""") == "Long Long nb!\n", "single ball"

# all equal moves
assert run("""2 1
1
1
""") == "Mao Mao nb!\n", "same move set"

# large pile with repeated possible cycles
assert run("""10 2
1 10
1 10
""") == "Mao Mao nb!\n", "large equal moves"

# unavailable moves at start
assert run("""3 2
5 6
1 2
""") == "Mao Mao nb!\n", "illegal first moves"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 / 1` | Long Long nb! | Immediate winning move |
| `2 1 / 1 / 1` | Mao Mao nb! | Alternating turns with equal moves |
| `10 2 / 1 10 / 1 10` | Mao Mao nb! | Longer dependency chain |
| `3 2 / 5 6 / 1 2` | Mao Mao nb! | Moves larger than the pile |

## Edge Cases

For the case where Long Long has no usable move, the transition correctly leaves `winL[n]` false. In the input:

```
5 1
6
7
```

the only Long Long move is 6, which is greater than 5. The algorithm skips it because `x <= i` is false, so the state remains losing.

For the case where both players have the same moves, the algorithm does not make assumptions based on symmetry. In:

```
2 1
1
1
```

the state with one ball is winning for the player whose turn it is, but the state with two balls is losing because the first player must give the opponent the one-ball winning state.

For a state where a move removes all remaining balls, the algorithm handles it through the base case. If a player removes the entire pile, the opponent reaches state `0`, which is losing. This makes the move correctly appear as a winning transition.
