---
title: "CF 105321D - Duo"
description: "Three players participate in a simple alliance game where exactly two of them form a team and the remaining player competes alone. Each player has a fixed integer score."
date: "2026-06-22T17:22:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105321
codeforces_index: "D"
codeforces_contest_name: "2024 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 105321
solve_time_s: 53
verified: true
draft: false
---

[CF 105321D - Duo](https://codeforces.com/problemset/problem/105321/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

Three players participate in a simple alliance game where exactly two of them form a team and the remaining player competes alone. Each player has a fixed integer score. For any chosen pair, the duo’s score is the sum of their individual scores, and this sum is compared against the score of the lone player.

The outcome rule is asymmetric: if the duo’s sum is strictly greater than the solo player’s score, the duo wins. Otherwise, meaning the sum is less than or equal to the solo player’s score, the solo player wins alone.

The question asks whether there exists at least one player who can guarantee a solo win under this rule, which effectively means that there exists a choice of the other two players such that their combined score does not exceed the chosen player’s score.

The input consists of three integers representing the scores of the three participants. The output is a single character indicating whether some player can win alone.

Even though the constraints are extremely small, this problem is fundamentally about checking all possible partitions of three elements into a single element versus a pair.

There are no meaningful algorithmic performance constraints here since the input size is constant. Any correct solution runs in constant time, so complexity classes beyond O(1) are irrelevant.

Edge cases are mostly about equality and symmetry.

A first subtle case is when all values are equal. For example, input `50 50 50` leads to every pair summing to 100, which is strictly greater than the remaining 50, so no solo player can win.

Another case is when one value dominates but barely. For example, `100 10 10` allows the 100-score player to win alone because 10 + 10 = 20 is not greater than 100.

A misleading case for a naive interpretation is to think “largest value always wins alone.” This is not always true; it only works when the largest value is at least the sum of the other two.

## Approaches

With only three players, the most direct method is to try every possible choice of the solo player and compute the sum of the remaining two. For each candidate, we check whether the sum of the other two players is less than or equal to that candidate’s score. If any such configuration holds, that player can win alone.

This brute-force view is already optimal because the number of configurations is fixed at three. For each player, we perform a constant amount of arithmetic, so the total work is constant.

The key observation is that the problem reduces to checking whether the maximum element is at least as large as the sum of the other two. If the strongest player cannot overpower the combined strength of the other two, then no rearrangement of alliances can produce a solo win. Conversely, if any player satisfies this inequality, they can be chosen as the solo winner and the remaining two form the opposing duo.

Thus the solution collapses to evaluating three simple inequalities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all solo choices) | O(1) | O(1) | Accepted |
| Optimal (check inequalities directly) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Read the three integer scores A, B, and C. These represent fixed strengths of the players and will be compared in different pairings.
2. Compute whether A can win alone by checking if A is greater than or equal to B + C. This directly encodes the rule that A defeats the duo of the other two players.
3. Compute whether B can win alone by checking if B is greater than or equal to A + C. This tests the same condition for the second player under a different pairing.
4. Compute whether C can win alone by checking if C is greater than or equal to A + B. This covers the final possible solo scenario.
5. If any of these three conditions holds, output "S". Otherwise output "N".

The reasoning behind checking all three cases is that each player must be independently evaluated as the potential solo competitor, since the pairing changes the opposing sum.

### Why it works

The game outcome depends only on comparisons between one value and the sum of the other two. Every valid configuration corresponds exactly to one of the three inequalities checked. If none of them hold, then for every possible solo choice, the duo’s sum strictly exceeds the solo score, which forces the duo to win in every case. If at least one holds, that player is guaranteed to win when chosen as the solo participant because no alternate pairing can change the fact that the opposing sum is fixed for that partition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, c = map(int, input().split())

    if a >= b + c or b >= a + c or c >= a + b:
        print("S")
    else:
        print("N")

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the mathematical conditions derived in the algorithm. Each inequality corresponds to one possible solo configuration. The final decision aggregates these checks with a logical OR.

There are no boundary issues beyond standard integer addition, which is safe under the given constraints. The comparison uses `>=` rather than `>` because equality means the duo does not exceed the solo player, which still results in a solo win.

## Worked Examples

### Example 1: `1 2 3`

| Step | A | B | C | A vs B+C | B vs A+C | C vs A+B | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Check | 1 | 2 | 3 | 1 >= 5 false | 2 >= 4 false | 3 >= 3 true | S |

The third player exactly matches the sum of the other two. Since the duo must strictly exceed the solo player to win, equality means the solo player wins.

### Example 2: `4 5 6`

| Step | A | B | C | A vs B+C | B vs A+C | C vs A+B | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Check | 4 | 5 | 6 | 4 >= 11 false | 5 >= 10 false | 6 >= 9 false | N |

No player can match or exceed the sum of the other two, so every possible duo wins against the remaining player.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three fixed comparisons are performed regardless of input |
| Space | O(1) | No additional data structures are used |

The constant-time nature guarantees the solution trivially satisfies the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    a, b, c = map(int, sys.stdin.readline().split())
    print("S" if (a >= b + c or b >= a + c or c >= a + b) else "N")

# provided samples
assert run("1 2 3") == "S", "sample 1"
assert run("4 5 6") == "N", "sample 2"

# custom cases
assert run("100 10 10") == "S", "dominant player"
assert run("50 50 50") == "N", "perfect symmetry"
assert run("1 1 2") == "S", "equality edge case"
assert run("2 3 4") == "N", "no dominant player"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 100 10 10 | S | dominant single player wins alone |
| 50 50 50 | N | full symmetry prevents solo win |
| 1 1 2 | S | equality boundary case |
| 2 3 4 | N | no inequality satisfied |

## Edge Cases

The most important edge case is equality, where the duo’s sum exactly matches the solo player. For input `1 2 3`, the condition `3 >= 1 + 2` holds, so the solo player wins. A common mistake is using strict inequality in the wrong direction, which would incorrectly reject this case.

Another case is complete symmetry such as `50 50 50`. Here every pair sums to 100, which strictly exceeds the remaining 50, so no solo win is possible. The algorithm correctly evaluates all three inequalities to false.

A third case is a heavily skewed distribution like `100 10 10`. The check `100 >= 20` succeeds immediately, confirming a solo win. This demonstrates that only one inequality needs to hold for a positive answer.
