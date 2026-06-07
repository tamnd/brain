---
title: "CF 2199A - Game"
description: "Alice and Bob play a three-round card game where each round has independent scores between 0 and a maximum k. The first two rounds are already played, with Alice and Bob scoring a1, b1 in round one and a2, b2 in round two."
date: "2026-06-07T20:22:56+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 2199
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 14"
rating: 1000
weight: 2199
solve_time_s: 196
verified: true
draft: false
---

[CF 2199A - Game](https://codeforces.com/problemset/problem/2199/A)

**Rating:** 1000  
**Tags:** *special  
**Solve time:** 3m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

Alice and Bob play a three-round card game where each round has independent scores between `0` and a maximum `k`. The first two rounds are already played, with Alice and Bob scoring `a1, b1` in round one and `a2, b2` in round two. The third round has not yet occurred, but the scores must differ, and each is within `[0, k]`. The goal is to determine if Bob has any scenario in the third round that allows him to win the game, or if Alice wins regardless of the third round's outcome.

Winning is defined primarily by total points across all three rounds. If totals are tied, the player who won more rounds among the three wins. This means the third round can potentially overturn the winner if the point difference is small enough or if Alice and Bob have an equal number of round victories so far.

Constraints are small: `k` is at most 50, and there are up to `10^4` test cases. This makes exhaustive simulation feasible since the third round only has at most 51 possibilities per player, and each test case can be evaluated independently. Non-obvious edge cases include situations where Alice is ahead by exactly one point in total or has narrowly won both rounds, because small score manipulations in round three could change the winner or tie-breaker.

For example, if `k=5`, `a1=3, b1=4`, `a2=2, b2=1`, Bob can still win by scoring 5 in round three while Alice scores 0, even though Alice won the second round. A careless implementation might only compare total scores and ignore round wins, producing a wrong verdict when totals tie.

## Approaches

The naive approach is brute force: enumerate every possible score pair `(a3, b3)` for the third round where `0 ≤ a3, b3 ≤ k` and `a3 ≠ b3`, then compute total scores and count rounds won for each scenario. If Bob wins in any combination, output `YES`; otherwise, `NO`. This works because `k` is small, but in the worst case, this is O(k^2) per test case, which is fine for `k=50` and `t=10^4` but can be optimized.

The key observation is that only extreme scores matter. Bob's best chance to win is to maximize his points in the third round while minimizing Alice's. Conversely, Alice wins regardless if even in Bob’s optimal case she still has a higher total score or cannot lose the tie-breaker on rounds won. This reduces the problem to a simple check: compute the maximum score difference Bob can generate in the third round (`b3 - a3 = k - 0 = k`), add it to his current lead (or deficit), and compare totals and rounds won. If Bob cannot surpass Alice in total points or cannot win more rounds even with the maximum delta, Alice wins unconditionally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^2) per test case | O(1) | Accepted but could be simplified |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `k` and the scores `a1, b1` and `a2, b2`.
3. Compute the current total score for Alice (`totalA = a1 + a2`) and Bob (`totalB = b1 + b2`).
4. Count the number of rounds Alice won (`roundA`) and Bob won (`roundB`) in the first two rounds by comparing `a1 > b1` and `a2 > b2`.
5. Calculate the maximum score difference Bob can achieve in round three, which is `k - 0 = k`.
6. Check if Bob can surpass Alice’s total score by adding `k` to `totalB` and assuming Alice scores 0 in round three. If `totalB + k > totalA`, output `YES`.
7. If totals could tie after the third round, check the round wins. Bob must be able to have more round wins than Alice. If the round win difference is too large for Bob to overcome in one round, output `NO`.
8. If neither total nor rounds allow Bob to win, output `NO`.

Why it works: The invariant is that Alice’s unconditional win only occurs if even under Bob’s maximum possible effort in the third round, she either has a higher total score or wins the tie-breaker by rounds. This guarantees correctness because we only need to consider the extreme scoring scenario for Bob, avoiding unnecessary enumeration.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    k = int(input())
    a1, b1 = map(int, input().split())
    a2, b2 = map(int, input().split())
    
    totalA = a1 + a2
    totalB = b1 + b2
    
    roundsA = (a1 > b1) + (a2 > b2)
    roundsB = (b1 > a1) + (b2 > a2)
    
    # Maximum Bob can score and minimum Alice can score in round 3
    maxBob = totalB + k
    minAlice = totalA + 0
    
    if maxBob > minAlice:
        print("YES")
    elif maxBob == minAlice:
        # Check if Bob can win the tie-breaker (round wins)
        # Bob can only win one additional round in third round
        if roundsB + 1 > roundsA:
            print("YES")
        else:
            print("NO")
    else:
        print("NO")
```

The code calculates totals and round wins for the first two rounds. It then simulates the extreme possible third round to check if Bob can win either by total points or by round count. Using direct comparison avoids full enumeration, simplifying the logic while maintaining correctness. Boundary cases such as `a3=0, b3=k` are inherently handled because we assume the best for Bob.

## Worked Examples

**Example 1**

Input: `k=6`, `a1=2, b1=3`, `a2=1, b2=4`

| totalA | totalB | roundsA | roundsB | maxBob | minAlice | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 7 | 0 | 2 | 13 | 3 | YES |

Bob can score 6 in round 3 and Alice scores 0. TotalB = 7 + 6 = 13 > 3, so Bob has a winning scenario.

**Example 2**

Input: `k=3`, `a1=3, b1=1`, `a2=3, b2=1`

| totalA | totalB | roundsA | roundsB | maxBob | minAlice | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 2 | 2 | 0 | 5 | 6 | NO |

Even if Bob scores 3 in round 3 and Alice scores 0, totalB = 5 < 6. Alice wins unconditionally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is handled in constant time since we only compute totals and compare |
| Space | O(1) | Only a fixed number of variables are used per test case |

Given `t ≤ 10^4`, this algorithm easily runs within the 2-second limit, and the memory footprint is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        k = int(input())
        a1, b1 = map(int, input().split())
        a2, b2 = map(int, input().split())
        totalA = a1 + a2
        totalB = b1 + b2
        roundsA = (a1 > b1) + (a2 > b2)
        roundsB = (b1 > a1) + (b2 > a2)
        maxBob = totalB + k
        minAlice = totalA + 0
        if maxBob > minAlice:
            output.append("YES")
        elif maxBob == minAlice:
            output.append("YES" if roundsB + 1 > roundsA else "NO")
        else:
            output.append("NO")
    return "\n".join(output)

# Provided samples
assert run("5\n6\n2 3\n1 4\n5\n3 1\n3 1\n3\n3 1\n3 1\n10\n0 1\n10 0\n4\n3 1\n3 1\n") == "YES\nYES\nNO\nYES\nNO"

# Custom cases
assert run("1\n1\n0 1\n0 1\n") == "YES" # Bob can tie in totals but win last round
assert run("1\n50\n50 0\n50 0\n") == "NO" # Alice already guaranteed win
assert run("1\n10\n5 5\n5 5\n") == "YES" # Close totals, Bob can surpass
```
