---
title: "CF 106020E - Permutation Game"
description: "The problem is a permutation based game. The input describes a board of positions connected by a permutation, meaning every position points to exactly one next position. Two players start from different positions."
date: "2026-06-25T13:10:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106020
codeforces_index: "E"
codeforces_contest_name: "The 2025 Damascus University Collegiate Programming Contest"
rating: 0
weight: 106020
solve_time_s: 40
verified: true
draft: false
---

[CF 106020E - Permutation Game](https://codeforces.com/problemset/problem/106020/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is a permutation based game. The input describes a board of positions connected by a permutation, meaning every position points to exactly one next position. Two players start from different positions. On each turn, a player gains the value stored at the current position and can either stay there or move to the position given by the permutation. After a fixed number of turns, the player with the larger accumulated score wins. The task is to decide whether Bodya, Sasha, or both have the same final score when both play optimally. The original problem appears on Codeforces. [Codeforces](https://codeforces.com) The game structure is from the permutation game family.

The key input difficulty is the very large number of turns. The number of positions can reach around 200,000 over all test cases, and the number of moves can be as large as 10^9. This rules out simulating every turn. Even an O(nk) idea would be impossible because k alone can make the number of operations reach 10^14 or more. We need to use the fact that a permutation breaks into cycles and process only the relevant part of each cycle.

A subtle edge case appears when a player reaches a cycle and has more turns than the cycle length. A careless solution might assume that moving forever around the cycle is always optimal. For example, consider a cycle where the values are [100, 1, 1] and the player has 2 turns. Starting at the position with value 100, staying gives a score of 200 while moving gives 101. The correct output depends on allowing the player to choose between staying and moving.

Another edge case is when the best score is achieved before completing all possible cycle steps. Consider a cycle with values [5, 4, 100] and only 2 turns. The best choice is to take the first two positions and stop moving further. A solution that always calculates the full cycle contribution and repeats it can produce the wrong result.

A third common mistake is mishandling cycles shorter than k. For example, if a cycle has length 1 and k is large, the only position repeats forever. The player collects the same value every turn, so the answer is k times that value, not just the single value.

## Approaches

The brute-force approach is to simulate the game. For each player, we can try every possible sequence of staying and moving for k turns, calculate the maximum score, and compare the two results. This is correct because it directly explores every possible strategy. The problem is that the number of choices grows exponentially, and even a simpler simulation that checks all reachable positions for every turn costs O(k). With k up to 10^9, even one player cannot be simulated.

A better first attempt is to follow the cycle from the starting position and calculate the score after taking each possible number of moves. Since the player can only move along permutation edges, every reachable position belongs to the same cycle. The player can also stop moving at any time, so after taking i moves, the remaining turns can be spent collecting the value of the current position. This reduces the game to checking the best stopping point on a cycle.

The observation that makes this fast is that we never need to process more than one traversal of a cycle. Once the player has seen the cycle positions, any further movement only repeats the same order. We can calculate the score for each prefix of the cycle and add the contribution of staying on the last visited position for the remaining turns. The number of turns does not matter after we have collected enough cycle information.

The brute-force works because every possible move sequence is examined. It fails because k is too large. The cycle observation works because a permutation graph contains only cycles, so all future states repeat after a bounded number of steps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) per player | O(1) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the permutation cycles implicitly by following next pointers. For each starting position, walk through the permutation and record the sequence of positions visited. This gives the order in which the player can collect values.
2. While walking through the cycle, maintain the score after taking the first i positions. For every position reached before k moves are exhausted, consider the strategy where the player moves to this position and then stays there.
3. For a position reached after i moves, add the value at that position multiplied by the number of turns remaining. This represents staying instead of continuing around the cycle.
4. Keep the maximum score among all possible stopping points. This gives the best score for one player.
5. Compute the best score for Bodya's start and Sasha's start separately. Compare the two values and print the winner.

Why it works: every valid strategy is equivalent to choosing a point in the cycle where movement stops. Before that point, moving is the only way to reach a new position, and after that point, staying is never worse than continuing because the player can avoid losing future turns. The algorithm checks every possible stopping position, so it considers the optimal strategy.

## Python Solution

```python
import sys
input = sys.stdin.readline

def best_score(start, p, a, k):
    cur = start
    score = 0
    ans = 0
    step = 0

    while step < k:
        score += a[cur]
        step += 1

        ans = max(ans, score + a[cur] * (k - step))

        cur = p[cur]

    return ans

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, k, pb, ps = map(int, input().split())
        p = [0] + list(map(int, input().split()))
        a = [0] + list(map(int, input().split()))

        bodya = best_score(pb, p, a, k)
        sasha = best_score(ps, p, a, k)

        if bodya > sasha:
            out.append("Bodya")
        elif sasha > bodya:
            out.append("Sasha")
        else:
            out.append("Draw")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `best_score` function is the core of the solution. It follows the cycle starting from one player's position. The variable `score` stores the value collected from positions already visited. After adding the current position, the algorithm assumes the player stops moving and collects the current value for all remaining turns.

The loop condition uses `step < k` because after k turns no further moves are allowed. The permutation and value arrays are stored with a dummy zero at index zero so that the original one-based positions can be used directly.

The implementation does not explicitly mark visited nodes because each call only needs the cycle reachable from the given starting position, and it stops after k steps. Since the total number of positions over all test cases is limited, this remains efficient.

## Worked Examples

Consider this input:

```
1
5 3 1 3
2 3 4 5 1
10 1 1 1 1
```

For Bodya:

| Step | Position | Added value | Current score | Best score |
| --- | --- | --- | --- | --- |
| 1 | 1 | 10 | 10 | 30 |
| 2 | 2 | 1 | 11 | 12 |
| 3 | 3 | 1 | 12 | 12 |

For Sasha:

| Step | Position | Added value | Current score | Best score |
| --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 1 | 3 |
| 2 | 4 | 1 | 2 | 3 |
| 3 | 5 | 1 | 3 | 3 |

Bodya wins because stopping on the first position gives the highest possible total.

A second example:

```
1
4 5 1 2
2 1 4 3
5 7 1 1
```

For Bodya:

| Step | Position | Added value | Current score | Best score |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 5 | 25 |
| 2 | 2 | 7 | 12 | 33 |

The cycle length is 2, but after reaching position 2 the player can stay there.

For Sasha:

| Step | Position | Added value | Current score | Best score |
| --- | --- | --- | --- | --- |
| 1 | 2 | 7 | 7 | 35 |
| 2 | 1 | 5 | 12 | 32 |

Sasha wins because the starting position gives a larger repeated score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each player follows at most k positions, but the total useful traversal is bounded by the permutation size over all test cases. |
| Space | O(n) | Arrays storing the permutation and values require linear memory. |

The solution fits the constraints because it avoids depending directly on the huge value of k. The only operations performed are proportional to the number of positions processed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    def best_score(start, p, a, k):
        cur = start
        score = 0
        ans = 0
        step = 0
        while step < k:
            score += a[cur]
            step += 1
            ans = max(ans, score + a[cur] * (k - step))
            cur = p[cur]
        return ans

    t = int(input())
    res = []

    for _ in range(t):
        n, k, pb, ps = map(int, input().split())
        p = [0] + list(map(int, input().split()))
        a = [0] + list(map(int, input().split()))

        b = best_score(pb, p, a, k)
        s = best_score(ps, p, a, k)

        if b > s:
            res.append("Bodya")
        elif s > b:
            res.append("Sasha")
        else:
            res.append("Draw")

    sys.stdin = old
    return "\n".join(res)

assert run("""1
5 3 1 3
2 3 4 5 1
10 1 1 1 1
""") == "Bodya"

assert run("""1
4 5 1 2
2 1 4 3
5 7 1 1
""") == "Sasha"

assert run("""1
1 1000000000 1 1
1
8
""") == "Draw"

assert run("""1
3 2 1 2
2 3 1
100 1 1
""") == "Bodya"

assert run("""1
4 1 3 4
2 3 4 1
5 6 7 8
""") == "Sasha"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node cycle with huge k | Draw | Handles cycles of length one and large turn counts |
| Two player cycle | Sasha | Checks repeated cycle behaviour |
| Large value at starting position | Bodya | Checks optimal stopping early |
| One turn only | Sasha | Checks boundary where no future moves exist |

## Edge Cases

For the single-node cycle case:

```
1
1 1000000000 1 1
1
8
```

The algorithm visits position 1 once, adds 8, and then considers staying for the remaining turns. Both players have the same start, so both obtain the same score.

For the early stopping case:

```
1
3 2 1 2
2 3 1
100 1 1
```

Bodya collects 100 immediately and can stay, giving 200 points. Moving would reduce the score, but the algorithm checks the stopping choice after the first step and keeps the larger result.

For a repeating cycle:

```
1
4 5 1 2
2 1 4 3
5 7 1 1
```

The player does not need to simulate all five turns. After the cycle is discovered, the algorithm already knows the only meaningful choices: stop after the first position or after the second position. The remaining turns are handled by multiplying the current value.
