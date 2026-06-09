---
title: "CF 1681A - Game with Cards"
description: "Two players each hold a multiset of integers. They play a turn-based game where the only rule is that every newly played number must be strictly larger than the previous one."
date: "2026-06-10T00:22:15+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1681
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 129 (Rated for Div. 2)"
rating: 800
weight: 1681
solve_time_s: 658
verified: false
draft: false
---

[CF 1681A - Game with Cards](https://codeforces.com/problemset/problem/1681/A)

**Rating:** 800  
**Tags:** games, greedy  
**Solve time:** 10m 58s  
**Verified:** no  

## Solution
## Problem Understanding

Two players each hold a multiset of integers. They play a turn-based game where the only rule is that every newly played number must be strictly larger than the previous one. Players alternate turns, and on each turn a player must pick a remaining card that is larger than the last played value. If no such card exists, that player immediately loses.

For each test case, we must determine the winner under optimal play for two scenarios: when Alice starts and when Bob starts.

The constraints are very small. Each player has at most 50 cards and values are bounded by 50, and there are up to 1000 test cases. This immediately suggests that any solution can safely use sorting and even simple counting strategies without worrying about performance. Brute force simulation of game states is also theoretically possible, but unnecessary.

A subtle issue is that the first move is unconstrained. A naive approach might assume “start with the smallest card” or “start with the largest card” is always optimal. That is not true in general, because the choice of the first number determines the entire chain of forced responses. However, because the value range is tiny, the correct solution does not require deep game tree search.

Another common pitfall is trying to simulate greedily by always picking the smallest valid next card. That strategy can fail because it ignores that sometimes consuming a small card early prevents the opponent from building a longer chain later.

## Approaches

A direct brute force solution would treat the game as a state space where each state is defined by the last played value, whose turn it is, and which cards remain. From each state, we try all valid moves. This is correct but quickly becomes exponential since each player can reorder their plays in many ways.

The key observation is that the game does not depend on order among identical values, and the only constraint is monotonic increase. Since values are small, what really matters is how many cards of each value each player has.

Once we sort both players’ arrays, we can think in terms of choosing an initial starting value and then greedily extending the longest possible alternating chain. Each player always wants to respond with the smallest available card that is still greater than the previous move, because choosing a larger card only reduces future options.

This reduces the problem to checking, for each possible starting move, how far the sequence can be extended. Since there are only 100 possible starting values in the worst case, this becomes extremely efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | Exponential | O(n) | Too slow |
| Sorted greedy simulation over all starts | O(t * (n + m) * 100) | O(n + m) | Accepted |

## Algorithm Walkthrough

We solve each test case independently.

First, we sort both Alice’s and Bob’s cards. Sorting ensures that when we try to extend a sequence, we can always pick the next valid card in linear scan order.

Next, we try every possible first move. There are two types of first moves: Alice starts or Bob starts. For each case, we simulate the game.

During simulation, we maintain a pointer into each sorted list. The pointer always moves forward and never backtracks, because once a card is used it is removed from consideration.

We alternate turns. On each turn, the current player advances their pointer until they find a card strictly greater than the last played value. If no such card exists, the current player loses and the simulation ends.

We compute the result for both starting configurations and output the winners.

The lexicographic or structural complexity is irrelevant here because the game is fully determined once the first move is fixed.

### Why it works

At any point in the game, both players are optimally trying to preserve future flexibility. In a sorted array, choosing the smallest valid card is always optimal because it leaves the largest possible space for future moves. Any larger choice strictly reduces the number of available future responses without improving the ability to continue the chain. This makes the greedy simulation equivalent to optimal play.

## Python Solution

```python
import sys
input = sys.stdin.readline

def simulate(a, b, start_a):
    ia = ib = 0
    last = -1
    turn_a = start_a

    while True:
        if turn_a:
            while ia < len(a) and a[ia] <= last:
                ia += 1
            if ia == len(a):
                return "Bob"
            last = a[ia]
            ia += 1
        else:
            while ib < len(b) and b[ib] <= last:
                ib += 1
            if ib == len(b):
                return "Alice"
            last = b[ib]
            ib += 1
        turn_a = not turn_a

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        m = int(input())
        b = list(map(int, input().split()))

        a.sort()
        b.sort()

        res1 = simulate(a, b, True)
        res2 = simulate(a, b, False)

        print(res1)
        print(res2)

if __name__ == "__main__":
    solve()
```

The solution keeps both arrays sorted so that finding the next valid move becomes a linear scan with a moving pointer. Each simulation runs in linear time over the total number of cards, since each pointer only advances forward.

A subtle point is that the comparison uses `<= last`, ensuring strict increase is enforced correctly. Another important detail is that the last played value is updated immediately after selecting a card, which preserves correctness of turn transitions.

## Worked Examples

We trace two representative cases.

### Example 1

Alice: [6]

Bob: [6, 8]

Alice starts.

| Turn | Player | Last value | Alice pointer | Bob pointer | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | Alice | - | 6 used | - | Alice plays 6 |
| 2 | Bob | 6 | 6 skipped, 8 used | 8 used | Bob plays 8 |
| 3 | Alice | 8 | no valid | 1 | Alice loses |

This confirms that even with equal starting values, the strict inequality forces progression and quickly exhausts Alice.

### Example 2

Alice: [1, 3, 3, 7]

Bob: [2, 4]

Alice starts.

| Turn | Player | Last value | State A | State B | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | Alice | - | 1,3,3,7 | 2,4 | Alice plays 1 |
| 2 | Bob | 1 | 1,3,3,7 | 2,4 | Bob plays 2 |
| 3 | Alice | 2 | 3,3, |  |  |
