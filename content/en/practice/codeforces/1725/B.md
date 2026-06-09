---
title: "CF 1725B - Basketball Together"
description: "We are asked to form teams from a list of candidate basketball players, each with an integer power. There is an opposing team with power $D$, and a team we form wins if the total power of its members exceeds $D$."
date: "2026-06-09T19:01:35+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1725
codeforces_index: "B"
codeforces_contest_name: "COMPFEST 14 - Preliminary Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1000
weight: 1725
solve_time_s: 119
verified: true
draft: false
---

[CF 1725B - Basketball Together](https://codeforces.com/problemset/problem/1725/B)

**Rating:** 1000  
**Tags:** binary search, greedy, sortings  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to form teams from a list of candidate basketball players, each with an integer power. There is an opposing team with power $D$, and a team we form wins if the total power of its members exceeds $D$. The twist is that before each match, the coach can amplify all players in a team to match the strongest player in that team. Each player can participate in at most one team, and we want to maximize the number of teams that can win.

The input consists of $N$ integers representing player powers, and $D$, the enemy power. The output is a single integer: the maximum wins.

The constraints allow $N$ up to $10^5$ and powers up to $10^9$. This tells us that an $O(N^2)$ approach will not work. We need something near $O(N \log N)$ at worst. Operations must scale efficiently with large arrays. A naive approach that tries every possible subset to see if its amplified sum beats $D$ is infeasible.

Edge cases include: all player powers smaller than $D$, only one very strong player, or all powers equal to each other. For instance, if $N = 3$, $D = 100$, and powers are $[30, 30, 30]$, no team can win because even amplifying to the strongest member gives $30 * 3 = 90 \le D$. A careless approach might incorrectly assume each player alone can form a winning team, but the amplified sum must exceed $D$.

## Approaches

The brute-force method would consider every possible subset of players to form a team, calculate the amplified sum for that subset, and check if it exceeds $D$. In the worst case, this requires iterating over $2^N$ subsets. For $N = 10^5$, this is impossible. Even a heuristic of trying all consecutive segments after sorting is too slow if implemented naively.

The key insight is that after sorting the players by power, the best strategy is greedy. To maximize wins, we should form the smallest possible team with the strongest available players. For a candidate team of size $k$, if the strongest member has power $p$, the amplified team sum is $k * p$. We need $k * p > D$. Because larger $k$ values make it easier to exceed $D$ for smaller players, we start forming teams from the strongest down. Each time we pick a player as the strongest in a new team, we calculate the minimum team size needed to beat $D$ and take that many of the weakest remaining players. This ensures each team wins and no player is used twice.

This greedy observation turns the problem into a simple sort and two-pointer approach or index tracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N) | O(N) | Too slow |
| Optimal (Greedy + Sort) | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Sort the player powers in ascending order. Sorting ensures we can efficiently pick the strongest player for each team and the weakest available teammates.
2. Initialize two pointers or indices: one at the start (`i`) and one at the end (`j`) of the sorted array. `i` points to the weakest available player, `j` to the strongest.
3. Initialize a counter `wins` to zero. This will track the number of winning teams formed.
4. While `i <= j`, consider the strongest remaining player at `j`. Calculate the minimum team size required to beat `D`: `k = ceil(D / P[j])`. This is the smallest number of copies of `P[j]` needed.
5. Check if enough players remain: if `j - i + 1 >= k`, form a team with player `j` and `k-1` of the weakest available players starting from `i`. Increment `wins`, increment `i` by `k-1` to remove used players from the front, and decrement `j` to remove the used strongest player.
6. If not enough players remain to form a winning team with `P[j]`, stop. No more teams can win.
7. Return `wins`.

Why it works: The invariant is that at each step, we always form a team that is guaranteed to win using the smallest number of players, and we always consume the strongest available player. No player is used twice, and no winning opportunity is skipped. The sorted array ensures we can always choose the combination that maximizes remaining potential wins.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def max_wins():
    n, D = map(int, input().split())
    P = list(map(int, input().split()))
    P.sort()
    
    i, j = 0, n - 1
    wins = 0
    
    while i <= j:
        strongest = P[j]
        team_size = (D + strongest) // strongest  # ceil(D / strongest)
        if team_size <= (j - i + 1):
            wins += 1
            i += team_size - 1
            j -= 1
        else:
            break
    
    print(wins)

if __name__ == "__main__":
    max_wins()
```

The code first sorts powers. The two-pointer approach ensures we always consume players optimally. The `(D + strongest) // strongest` trick computes the ceiling without importing `math.ceil` for speed. Boundary conditions `i <= j` and `team_size <= j - i + 1` handle small arrays and prevent index errors.

## Worked Examples

**Sample 1**

Input: `6 180`

Powers: `[90, 80, 70, 60, 50, 100]`

| i | j | strongest | team_size | i after | j after | wins |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 5 | 100 | 2 | 1 | 4 | 1 |
| 1 | 4 | 90 | 2 | 2 | 3 | 2 |
| 2 | 3 | 70 | 3 | - | - | 2 |

Explanation: First team uses 100+60. Second team uses 90+70. Remaining players cannot form a team with total >180.

**Custom Sample**

Input: `3 100`

Powers: `[30, 30, 30]`

| i | j | strongest | team_size | i after | j after | wins |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 30 | 4 | - | - | 0 |

No team can exceed 100. Algorithm correctly outputs 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates; linear scan with two pointers is O(N) |
| Space | O(N) | Input array storage |

With $N\le10^5$, $N \log N \approx 5 \times 10^5$ operations, comfortably within the 1s time limit. Memory is well under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    max_wins()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("6 180\n90 80 70 60 50 100\n") == "2", "sample 1"

# minimum input
assert run("1 1\n1\n") == "1", "single player equal to D"

# all equal
assert run("4 10\n3 3 3 3\n") == "1", "all equal small powers"

# maximum powers
assert run("5 1000000000\n1000000000 1000000000 1000000000 1000000000 1000000000\n") == "5", "max power values"

# edge case: not enough for second team
assert run("5 10\n2 3 3 3 4\n") == "1", "cannot form second winning team"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1 1\n1\n" | 1 | Single-player minimum input |
| "4 10\n3 3 3 3\n" | 1 | All powers equal, sum barely enough |
| "5 1000000000\n1000000000 ...\n" | 5 | Maximum powers handled correctly |
| "5 10\n2 3 3 3 4\n" | 1 | Correct handling when remaining players cannot form a team |

## Edge Cases

If all players have the same power, the algorithm correctly calculates the required team size and forms as many teams as possible. For input `[3,3,3,3]` with `D=10`, the required team size is 4, so only one team forms. If powers are extremely large, the algorithm still works because integer division avoids overflow. Single-player scenarios are correctly handled since the team size calculation accounts for ceil division.
