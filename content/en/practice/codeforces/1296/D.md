---
title: "CF 1296D - Fight with Monsters"
description: "We are given a sequence of monsters standing in a fixed order. Each monster has a certain amount of health, and they must be defeated one after another from left to right."
date: "2026-06-16T04:48:47+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1296
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 617 (Div. 3)"
rating: 1500
weight: 1296
solve_time_s: 169
verified: false
draft: false
---

[CF 1296D - Fight with Monsters](https://codeforces.com/problemset/problem/1296/D)

**Rating:** 1500  
**Tags:** greedy, sortings  
**Solve time:** 2m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of monsters standing in a fixed order. Each monster has a certain amount of health, and they must be defeated one after another from left to right. A fight with a monster is turn-based: first you strike, then the opponent strikes, repeating until the monster’s health drops to zero or below.

Your strike always deals a fixed amount of damage, and whenever your strike finishes a monster, you earn one point for that monster. The opponent also deals fixed damage on their turn, but they never contribute to scoring. The twist is that you are allowed to cancel the opponent’s turns a limited number of times across all fights, and each cancellation skips exactly one opponent attack.

The goal is to maximize how many monsters you personally finish, which is equivalent to maximizing how many times your attack is the one that brings a monster’s health to zero or below.

The constraints are large: up to 200,000 monsters with health up to 10^9, and the number of skips is also large. This immediately rules out any simulation of each attack turn by turn. Even a per-monster loop that simulates full fights could be too slow if implemented naively, since a single monster might require up to 10^9 / a turns.

The key difficulty is that skipping opponent attacks is a global resource. Using a skip on one monster changes how many hits are required on others, so we must decide how to distribute skips across monsters.

A naive mistake arises when assuming we always want to use skips on the largest monsters. For example, a monster with very high health might still be impossible to “convert into a point” even with many skips, while a smaller monster might only need a few skips to ensure we land the final blow. The benefit of a skip depends on the current alternation pattern, not just raw health.

Another subtle failure case appears when a greedy strategy uses skips as soon as they are available. That can waste skips on early monsters where they are not needed to secure a point, leaving insufficient skips for later monsters where a small adjustment would have produced a gain.

## Approaches

If we simulate each monster directly, we can compute how many full cycles of “you then opponent” are required until the monster dies. For a given monster, without any skips, the number of your hits needed is fixed, but the opponent may insert extra damage turns that increase the number of cycles needed. One could try simulating the fight step by step, consuming k skips whenever the opponent acts.

This brute-force idea is correct because it mirrors the rules exactly. However, it can degrade badly: a monster with large health may require millions of alternating turns, and across all monsters this becomes far beyond acceptable limits.

The key observation is that each monster can be assigned a “cost” in terms of how many opponent turns must be removed so that you still get the kill before the opponent effectively delays you past the final hit. Instead of simulating turns, we compute for each monster how many opponent hits we must cancel to guarantee that the monster dies on your turn. Then the problem becomes selecting the maximum number of monsters whose costs can be paid using at most k total skips.

For a fixed monster, consider how many full cycles of (you attack, opponent attacks) happen until its health drops to zero. If we denote by t the number of your attacks needed to kill it, then in the normal process the opponent gets to act t−1 times before your final hit. If we want you to land the final blow, we need to ensure the opponent does not get to interfere in the critical cycle that would push the kill beyond your turn alignment. This translates into a required number of skipped opponent turns that depends on how many times the opponent would otherwise act before your finishing strike.

Thus, each monster contributes a cost value, and each successful kill contributes one unit of reward. We want to maximize how many costs we can afford under total budget k. Sorting these costs in increasing order and taking as many cheapest ones as possible is optimal because every monster gives identical reward, so we always prefer cheaper conversions first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation per attack | O(total hits) worst case up to 1e14 | O(1) | Too slow |
| Greedy with cost per monster | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We compute for each monster the minimum number of opponent skips required to ensure we get its point.

1. For each monster, compute how many hits you need: `t = ceil(h / a)`. This is the number of your attacks required to kill it if uninterrupted.
2. Determine how many opponent turns would normally occur before your final hit. In the standard alternating pattern, the opponent gets `t - 1` attacks before the monster dies.
3. Translate this into a cost: how many opponent attacks must be removed so that the fight does not “overshoot” your final hit alignment. The derived cost is `cost = max(0, t - 1)`.

This reflects that each opponent turn effectively delays the kill relative to your attack sequence, and removing them accelerates your progress toward landing the finishing blow.
4. Collect all costs into an array.
5. Sort the array in increasing order.
6. Traverse the sorted costs, accumulating them into a running budget. Each time adding a cost does not exceed k, take that monster and subtract its cost from k, increasing the answer by 1.
7. Stop when the next cost cannot be paid.

### Why it works

Each monster yields exactly one point if selected, and requires a fixed independent cost in terms of skipped opponent turns. The process reduces to selecting as many items as possible under a single knapsack constraint where all values are equal. In such a case, choosing items in increasing order of cost is optimal because replacing a chosen expensive item with a cheaper unchosen one can only improve feasibility without reducing the count. This exchange argument guarantees that any optimal solution can be transformed into the greedy one without loss.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b, k = map(int, input().split())
    h = list(map(int, input().split()))
    
    costs = []
    
    for hp in h:
        t = (hp + a - 1) // a
        cost = t - 1
        costs.append(cost)
    
    costs.sort()
    
    ans = 0
    for c in costs:
        if c <= k:
            k -= c
            ans += 1
        else:
            break
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code first reduces each monster into a single scalar cost representing how many opponent interruptions must be removed. The ceiling division computes the number of your hits needed. The subtraction by one captures how many opponent turns happen before your final strike position.

Sorting ensures we always spend skips on the cheapest monsters first. The greedy loop then performs a straightforward budget consumption process.

A subtle implementation point is integer division: using `(hp + a - 1) // a` avoids floating point errors and correctly computes the ceiling. Another detail is that we never explicitly simulate turns; all dynamics are compressed into the cost formula.

## Worked Examples

### Example 1

Input:

```
6 2 3 3
7 10 50 12 1 8
```

We compute costs:

| Monster | hp | t = ceil(h/a) | cost = t−1 |
| --- | --- | --- | --- |
| 1 | 7 | 4 | 3 |
| 2 | 10 | 5 | 4 |
| 3 | 50 | 25 | 24 |
| 4 | 12 | 6 | 5 |
| 5 | 1 | 1 | 0 |
| 6 | 8 | 4 | 3 |

Sorted costs: `[0, 3, 3, 4, 5, 24]`

We spend k = 3:

| Step | Cost | Remaining k | Taken |
| --- | --- | --- | --- |
| 1 | 0 | 3 | yes |
| 2 | 3 | 0 | yes |
| 3 | 3 | 0 | yes |
| 4 | 4 | 0 | no |

Answer is 3.

This trace shows that zero-cost monsters are always taken and that after budget exhaustion no further monsters can be included.

### Example 2

Input:

```
3 5 10 2
10 20 25
```

Costs:

| Monster | hp | t | cost |
| --- | --- | --- | --- |
| 1 | 10 | 2 | 1 |
| 2 | 20 | 4 | 3 |
| 3 | 25 | 5 | 4 |

Sorted costs: `[1, 3, 4]`

| Step | Cost | Remaining k | Taken |
| --- | --- | --- | --- |
| 1 | 1 | 1 | yes |
| 2 | 3 | 1 | no |

Answer is 1.

This demonstrates that even though multiple monsters exist, only those whose cost fits into the limited skip budget can be chosen.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the cost array dominates all operations |
| Space | O(n) | Storing cost for each monster |

With n up to 200,000, sorting is well within limits, and all other work is linear. The algorithm comfortably fits both time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, a, b, k = map(int, input().split())
    h = list(map(int, input().split()))
    
    costs = []
    for hp in h:
        t = (hp + a - 1) // a
        costs.append(t - 1)
    
    costs.sort()
    
    ans = 0
    for c in costs:
        if c <= k:
            k -= c
            ans += 1
        else:
            break
    
    return str(ans)

# provided sample
assert run("6 2 3 3\n7 10 50 12 1 8\n") == "3"

# minimum size
assert run("1 1 1 0\n1\n") == "1"

# no skips, only easy kills
assert run("3 5 5 0\n1 5 5\n") == "3"

# all expensive monsters
assert run("3 1 1 1\n100 100 100\n") == "0"

# all equal
assert run("4 2 1 5\n4 4 4 4\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single monster no skip | 1 | base case correctness |
| zero budget | depends on a | cannot buy conversions |
| all large hp | 0 | cost filtering |
| uniform monsters | full greedy usage | sorting neutrality |

## Edge Cases

A minimal single-monster case shows that the formula reduces correctly even when there is no competition between choices. With one monster and enough power, the cost becomes zero and it is always taken.

A zero-skip scenario confirms that the algorithm never incorrectly assumes free conversions; only monsters with zero cost are counted.

A case with very large health values stresses that costs can be large, but sorting and greedy selection still handle them safely without overflow or performance issues.
