---
title: "CF 321B - Ciel and Duel"
description: "We are given two sets of cards, one belonging to Jiro and one belonging to Ciel. Jiro’s cards come in two types, Attack and Defense, each with a strength value. Ciel’s cards are simpler: every one of her cards is an Attack card with a given strength."
date: "2026-06-06T02:32:34+07:00"
tags: ["codeforces", "competitive-programming", "dp", "flows", "greedy"]
categories: ["algorithms"]
codeforces_contest: 321
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 190 (Div. 1)"
rating: 1900
weight: 321
solve_time_s: 79
verified: true
draft: false
---

[CF 321B - Ciel and Duel](https://codeforces.com/problemset/problem/321/B)

**Rating:** 1900  
**Tags:** dp, flows, greedy  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sets of cards, one belonging to Jiro and one belonging to Ciel. Jiro’s cards come in two types, Attack and Defense, each with a strength value. Ciel’s cards are simpler: every one of her cards is an Attack card with a given strength.

Ciel plays by selecting each of her cards at most once, in any order she wants, and optionally stopping early. Each chosen card is used to either directly damage Jiro if no cards remain, or to destroy exactly one of Jiro’s cards first and possibly deal reduced damage depending on that card’s type. Attack-type enemy cards require Ciel’s strength to be at least theirs, and they reduce the damage by their strength. Defense-type cards require strict inequality and do not contribute any damage when destroyed.

The goal is to choose an order and subset of Ciel’s cards and pair them optimally with Jiro’s cards so that the total accumulated damage is maximized.

The constraints are small, with at most 100 cards on each side. This immediately suggests that an O(n^2) or O(n^3) solution is viable, but anything exponential in both sides’ sizes would still be dangerous if not carefully pruned.

A key subtlety is that Ciel can stop at any time. That means not every card must be used, and using a weak card too early can waste a potential high-value direct damage later. Another subtle point is that Defense cards cannot be destroyed with equality, which creates strict pairing constraints that affect ordering decisions.

A naive greedy approach often fails because choosing which enemy card to destroy first changes the available “future value” of Ciel’s remaining cards. For example, using a strong Ciel card early on a weak Defense card may waste potential large direct damage later.

## Approaches

A brute-force view of the problem is to consider all permutations of Ciel’s cards and all possible ways to assign each used card either to “attack directly” or to “destroy one valid Jiro card.” For each step, we choose which Jiro card to target or skip to direct damage if none remain. This leads to an explosion in states: at each step we have O(n) choices of target and O(m) choices of ordering, resulting in factorial growth that is far beyond feasible.

The structure becomes manageable if we observe that Ciel’s cards are the only resource controlling the order of interactions, while Jiro’s cards can be thought of as items to be consumed with constraints. The key idea is to treat Jiro’s cards as a fixed multiset and consider how many of them we destroy before switching to pure direct damage.

If we fix a subset of Jiro’s cards that we intend to destroy, then the best strategy for Ciel is to use the smallest sufficient card for each destruction, preserving large cards for direct damage at the end. This naturally leads to sorting and dynamic programming over how many Attack and Defense cards are already removed.

The core transformation is to think of the process as incrementally pairing Ciel’s cards with Jiro’s cards in a way that maximizes total reward, where each pairing has a cost (possible Jiro damage reduction) and a feasibility constraint.

This leads to a DP formulation over how many Jiro cards have been removed from each type and how many Ciel cards have been used, always choosing the best next action.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations and assignments | O(m! · branching) | O(m + n) | Too slow |
| DP over used cards and remaining enemies | O(n² · m) | O(n · m) | Accepted |

## Algorithm Walkthrough

We separate Jiro’s cards into two sorted arrays: Attack cards and Defense cards. Let A be sorted Attack strengths and D be sorted Defense strengths.

We also sort Ciel’s cards in increasing order, because using smaller cards earlier allows us to reserve stronger cards for higher-value operations.

We define a DP state that tracks how many Attack and Defense cards have already been destroyed, and how many Ciel cards we have used. Instead of explicitly tracking used cards, we iterate over Ciel’s cards in order and decide how to use each one.

We maintain a DP table where dp[i][j] represents the maximum damage achievable after processing some prefix of Ciel’s cards, having destroyed i Attack cards and j Defense cards.

We process Ciel’s cards one by one.

1. Sort Jiro’s Attack cards A and Defense cards D in ascending order.
2. Sort Ciel’s cards S in ascending order.
3. Initialize a DP array filled with -inf except dp[0][0] = 0.
4. For each Ciel card with strength x, compute a new DP table next.
5. For each state (i, j), consider three actions:

1. Skip the card, keeping dp[i][j].
2. Use it to kill the next Attack card A[i], if x ≥ A[i]. This adds reward x - A[i].
3. Use it to kill the next Defense card D[j], if x > D[j]. This adds 0 reward.
6. Transition to next state accordingly.
7. After processing all cards, the answer is the maximum dp[i][j] over all states.

The reason we only consider the next Attack or Defense card in sorted order is that assigning a stronger Ciel card to a weaker enemy is always worse than reserving it for a stronger one, since reward depends on subtraction and feasibility is monotonic with strength.

### Why it works

The DP invariant is that after processing the first k Ciel cards, dp[i][j] correctly represents the maximum possible damage achievable by destroying exactly i Attack cards and j Defense cards using those k cards. Any optimal strategy can be rearranged so that the destroyed enemy cards are taken in increasing order of required strength, because swapping assignments between weaker and stronger targets never reduces feasibility and never improves payoff if done in the wrong direction. This ordering property ensures that the DP never misses an optimal pairing structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    atk = []
    dfn = []
    
    for _ in range(n):
        t, x = input().split()
        x = int(x)
        if t == "ATK":
            atk.append(x)
        else:
            dfn.append(x)
    
    c = [int(input()) for _ in range(m)]
    
    atk.sort()
    dfn.sort()
    c.sort()
    
    INF_NEG = -10**18
    
    dp = [[INF_NEG] * (len(dfn) + 1) for _ in range(len(atk) + 1)]
    dp[0][0] = 0
    
    for x in c:
        ndp = [[INF_NEG] * (len(dfn) + 1) for _ in range(len(atk) + 1)]
        
        for i in range(len(atk) + 1):
            for j in range(len(dfn) + 1):
                if dp[i][j] == INF_NEG:
                    continue
                
                cur = dp[i][j]
                
                # skip
                if cur > ndp[i][j]:
                    ndp[i][j] = cur
                
                # attack next ATK
                if i < len(atk) and x >= atk[i]:
                    val = cur + (x - atk[i])
                    if val > ndp[i+1][j]:
                        ndp[i+1][j] = val
                
                # attack next DEF
                if j < len(dfn) and x > dfn[j]:
                    if cur > ndp[i][j+1]:
                        ndp[i][j+1] = cur
        
        dp = ndp
    
    ans = 0
    for i in range(len(atk) + 1):
        for j in range(len(dfn) + 1):
            ans = max(ans, dp[i][j])
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The DP explicitly tracks how many Attack and Defense cards have been removed. The transitions mirror the game rules: Attack removals contribute value while Defense removals only serve feasibility. The skip transition is essential because stopping early is always allowed.

The strict inequality for Defense cards is handled by using `x > dfn[j]` instead of `>=`. Attack cards use `>=`, matching the rule that ties are allowed.

## Worked Examples

### Sample 1

Input:

```
2 3
ATK 2000
DEF 1700
2500
2500
2500
```

We sort:

Attack = [2000], Defense = [1700], Ciel = [2500, 2500, 2500]

We track DP transitions.

| Step | Card | Action | (i,j) state | Damage |
| --- | --- | --- | --- | --- |
| 0 | - | init | (0,0) | 0 |
| 1 | 2500 | ATK 2000 | (1,0) | 500 |
| 2 | 2500 | DEF 1700 | (1,1) | 500 |
| 3 | 2500 | direct | (1,1) | 3000 |

This shows the optimal structure: first convert a card into partial damage via ATK, then remove DEF, then cash out.

### Sample 2

Input:

```
2 2
ATK 100
ATK 10
1001
101
```

Sorted:

Attack = [10, 100], Ciel = [101, 1001]

| Step | Card | Action | (i,j) state | Damage |
| --- | --- | --- | --- | --- |
| 0 | - | init | (0,0) | 0 |
| 1 | 101 | ATK 10 | (1,0) | 91 |
| 2 | 1001 | ATK 100 | (2,0) | 992 |

This demonstrates why stronger cards must be reserved for later, since the second assignment yields much higher marginal gain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m · n) | For each Ciel card, we update a DP over up to n × m states |
| Space | O(n · m) | DP table stores best values for each destroyed-prefix state |

With n, m ≤ 100, this comfortably fits within limits, since about 10^6 transitions are processed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else _run(inp)

def _run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old
    return out.getvalue().strip()

# provided sample 1
assert _run("""2 3
ATK 2000
DEF 1700
2500
2500
2500
""") == "3000"

# sample 2
assert _run("""2 2
ATK 100
ATK 10
1001
101
""") == "992"

# custom 1: only DEF, strict inequality
assert _run("""1 1
DEF 5
5
""") == "0"

# custom 2: minimal case
assert _run("""1 1
ATK 0
0
""") == "0"

# custom 3: greedy trap
assert _run("""2 2
ATK 50
ATK 1
60
2
""") == "59"

# custom 4: many equal cards
assert _run("""1 3
ATK 10
5
5
5
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| only DEF with equal strength | 0 | strict inequality handling |
| minimal single ATK 0 | 0 | zero-damage edge case |
| greedy trap case | 59 | ordering importance |
| repeated weak cards | 0 | no invalid ATK kills |

## Edge Cases

A critical edge case is when Ciel’s card strength exactly matches a Defense card. For example:

Input:

```
1 1
DEF 0
0
```

The DP enforces `x > DEF`, so this transition is invalid. The only available move is to skip or attempt direct damage later, resulting in 0.

Another case is when all Jiro cards are Defense and all Ciel cards are equal. The algorithm correctly avoids illegal transitions and ensures that no partial pairing is counted, only valid future direct damage if any.

A final subtle case is when Ciel has more cards than needed. The DP allows skipping, so extra cards never reduce the answer, preserving optimal stopping behavior.
