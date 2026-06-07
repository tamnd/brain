---
title: "CF 2158A - Suspension"
description: "We are given a football match with a fixed number of players, and a sequence of disciplinary actions in the form of yellow and red cards. Each yellow card contributes toward a potential suspension, and each red card immediately suspends a player."
date: "2026-06-08T00:11:48+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2158
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1067 (Div. 2)"
rating: 800
weight: 2158
solve_time_s: 71
verified: true
draft: false
---

[CF 2158A - Suspension](https://codeforces.com/problemset/problem/2158/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a football match with a fixed number of players, and a sequence of disciplinary actions in the form of yellow and red cards. Each yellow card contributes toward a potential suspension, and each red card immediately suspends a player. A player can be suspended in two different ways: either they directly receive a red card, or they accumulate two yellow cards.

The key restriction is that once a player is suspended, any further cards that would have gone to them are irrelevant, since they are no longer in the game. We are not asked to simulate a real distribution of cards over time, but instead to determine the maximum number of distinct players that can end up suspended given the total counts of yellow and red cards.

The output for each test case is therefore the maximum possible number of players who can be made to leave the game, assuming we distribute cards in the most favorable way.

The constraints are small, with at most 100 players per test and up to 500 test cases. This immediately suggests that even a direct reasoning or constant-time formula per test case is sufficient. Anything even quadratic in n would still pass comfortably, but the structure of the problem strongly hints that we are looking for a closed-form greedy allocation rather than a simulation.

A subtle edge case arises when yellow cards are abundant but red cards are scarce. For example, if we have many yellows but few reds, we must decide whether to "waste" yellows by grouping them into pairs or distribute them across players. Another corner case is when reds alone already exceed the number of players, since each red corresponds to at most one suspension.

A naive mistake would be to treat yellow cards independently, counting each yellow as a potential suspension. That fails because two yellows are required for a single suspension, and leftover single yellows may not be usable if there are not enough players left to receive them in pairs.

## Approaches

A brute-force interpretation would attempt to simulate assigning each yellow and red card to individual players, branching over all possible assignments. Each card can be given to any still-active player, and each assignment might change whether a player becomes suspended. This quickly leads to an explosion: for each of up to 2n cards, there are up to n choices, making the search space on the order of n^(2n), which is completely infeasible even for n = 100.

The key observation is that we do not actually care about the identity of players, only how many suspensions can be created. Each red card can independently create at most one suspended player, and each pair of yellow cards can also create one suspended player. Since players are indistinguishable in terms of capacity (each can only be suspended once), the problem reduces to counting how many disjoint “suspension units” we can form from the available resources.

Each red card is already a full unit. For yellow cards, every two yellows form one unit. Thus, the number of yellow-based suspensions is bounded by floor(y / 2). The only coupling between reds and yellows is that we cannot exceed n total suspended players.

So the answer is the minimum of three quantities: the number of players n, the number of red cards r, and the total number of possible suspension units r + floor(y / 2).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Assignment | O(n^(2n)) | O(n) | Too slow |
| Greedy Counting | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We compute the answer for each test case using a direct counting strategy.

1. Compute how many players could be suspended purely by red cards. Each red card suspends a distinct player, so this contributes r potential suspensions.
2. Compute how many suspensions can be formed from yellow cards. Since two yellows are required per suspension, we take floor(y / 2). This gives the number of full yellow-based suspensions.
3. Add these two sources together to get the total number of “available suspension slots” without considering the player limit.
4. Cap the result by n, since there are only n players available to be suspended in total.
5. Output the final value.

The key reasoning step is that red-card suspensions and yellow-pair suspensions are independent sources of “consumption” of players. Each uses exactly one player, and no player can be counted twice.

### Why it works

At any optimal arrangement, every suspension corresponds to exactly one player being assigned either a red card or at least two yellow cards. Since red cards cannot be split and yellow cards only matter in pairs, the best we can do is maximize how many disjoint groups of size 1 (red) or 2 (yellow pairs) we can form, subject only to the availability of n players. There is no interaction that can increase total suspensions beyond r + floor(y/2), and no rearrangement can exceed n.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    y, r = map(int, input().split())

    yellow_susp = y // 2
    ans = r + yellow_susp
    print(min(n, ans))
```

The implementation follows the derived formula directly. We compute how many full yellow pairs exist using integer division, then add the number of red cards. Finally, we clamp by n to respect the number of available players.

The only subtle point is ensuring integer division is used for yellow cards, since any leftover single yellow cannot contribute to a suspension without pairing.

## Worked Examples

We trace two representative cases to see how the formula behaves.

### Example 1

Input:

n = 3, y = 1, r = 2

| Step | r | y // 2 | r + y//2 | min(n, result) |
| --- | --- | --- | --- | --- |
| Compute red effect | 2 | - | 2 | - |
| Compute yellow pairs | - | 0 | 2 | - |
| Combine | - | - | 2 | 2 |
| Apply limit | - | - | - | 2 |

This shows that even though there are only 3 players, only 2 can be suspended because there is insufficient yellow structure to generate more suspensions.

### Example 2

Input:

n = 10, y = 11, r = 5

| Step | r | y // 2 | r + y//2 | min(n, result) |
| --- | --- | --- | --- | --- |
| Compute red effect | 5 | - | 5 | - |
| Compute yellow pairs | - | 5 | 10 | - |
| Combine | - | - | 10 | 10 |
| Apply limit | - | - | - | 10 |

This case shows a situation where yellow cards contribute significantly, and the total exactly saturates the number of players.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses constant-time arithmetic operations |
| Space | O(1) | No auxiliary structures are used |

The solution comfortably fits within the constraints since even the maximum number of test cases requires only a few hundred operations total.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        y, r = map(int, input().split())
        out.append(str(min(n, r + y // 2)))
    return "\n".join(out) + "\n"

# provided samples
assert run("""5
3
1 2
2
0 0
4
6 0
3
3 3
10
11 5
""") == """2
0
3
3
10
"""

# custom cases
assert run("""1
1
0 0
""") == "0\n", "no cards"

assert run("""1
5
10 0
""") == "5\n", "only yellows"

assert run("""1
5
0 10
""") == "5\n", "only reds capped by n"

assert run("""1
4
1 10
""") == "4\n", "mix capped by n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1, 0 0 | 0 | no suspensions |
| 5, 10 0 | 5 | yellow pairing saturation |
| 5, 0 10 | 5 | red overflow capped by n |
| 4, 1 10 | 4 | combined overflow case |

## Edge Cases

A key edge case is when yellows are abundant but cannot all be paired into suspensions due to player limit. For example, n = 4, y = 10, r = 0. The algorithm computes y // 2 = 5, but r + y // 2 = 5 exceeds n. The final answer correctly becomes 4, since only 4 players exist. Any attempt to assign yellows greedily per player without recognizing the global cap would incorrectly overcount.

Another edge case is when reds already exceed n. For n = 3, r = 5, y = 0, we compute 5 suspensions from reds, but only 3 players exist, so the answer is 3. The formula correctly handles this via the min(n, ...), preventing invalid over-assignment.

A final subtle case is when there is an odd number of yellows. For n = 6, y = 5, r = 0, we get y // 2 = 2. The leftover single yellow is unusable, and the answer is 2, which matches the fact that one yellow must remain unpaired and cannot form a suspension on its own.
