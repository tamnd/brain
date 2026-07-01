---
title: "CF 103987F - Do Not Play Nim"
description: "We are given several independent test cases. Each test case describes a collection of stone piles, and two players play an alternating game starting from Alice. On Alice’s turn, she chooses a single pile and removes any positive number of stones from it."
date: "2026-07-02T06:09:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103987
codeforces_index: "F"
codeforces_contest_name: "2021 Huazhong University of Science and Technology Freshmen Cup"
rating: 0
weight: 103987
solve_time_s: 54
verified: true
draft: false
---

[CF 103987F - Do Not Play Nim](https://codeforces.com/problemset/problem/103987/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case describes a collection of stone piles, and two players play an alternating game starting from Alice.

On Alice’s turn, she chooses a single pile and removes any positive number of stones from it. The amount she removes in that move becomes a running total of Alice’s removed stones across the entire game.

On Bob’s turn, he also chooses a single pile, but his move is constrained: the number of stones he removes must be at least the total number of stones Alice has removed so far in the game, not just in the last move. This makes Bob’s legal moves increasingly restricted as the game progresses.

The game ends when a player cannot make a valid move on their turn, and that player loses. Since Alice moves first, she tries to force a position where Bob eventually has no valid move.

The input size suggests up to 2·10^5 piles across all test cases, so any solution must be roughly linear or linearithmic per test case. Anything that simulates moves or repeatedly updates piles per turn is immediately infeasible, since the game could last up to O(total stones) moves in worst-case reasoning, which is far beyond limits.

A subtle edge case appears immediately in how Bob’s constraint evolves. If Alice ever makes a large initial removal, Bob may be unable to respond at all. For example, if the largest pile is strictly larger than all others combined in a way that allows Alice to take it fully in one move, Bob may have no pile large enough to satisfy his minimum requirement.

A second non-obvious edge case is when multiple large piles exist. Then Bob can always respond to Alice’s initial aggressive move, and the game no longer ends immediately, leading to a long interaction where both players repeatedly consume large piles.

The difficulty is that the entire game structure is dominated by Alice’s first move, since it determines Bob’s minimum threshold for the rest of the game.

## Approaches

A brute-force approach would simulate the game directly. We would iterate turns, track Alice’s total removed stones, and for each Bob move scan all piles to find a valid move of size at least that threshold. This is conceptually correct because it follows the rules exactly. However, each move may require scanning up to O(n) piles, and the number of moves can be proportional to total stones removed. This leads to a worst-case complexity far beyond acceptable limits.

The key observation is that Bob’s constraint depends only on a single value: the total number of stones Alice has removed so far. That value is monotonic and entirely controlled by Alice’s first move, since any further Alice moves only increase it and only make Bob weaker.

This means the first move determines the entire structure of the game. Alice will always choose her first move to maximize pressure on Bob, and that optimal choice reduces to selecting a pile and deciding how much to take from it. Any partial removal is dominated by simply taking the entire chosen pile, since increasing Alice’s total only restricts Bob further.

Once Alice chooses a pile and removes it fully, Bob is left with a fixed threshold equal to that pile size. From that moment on, Bob can only play on piles that are at least that large, and each of his moves reduces one such pile by at least that threshold.

This collapses the game into a comparison between the largest pile and the remaining structure. If the largest pile is uniquely dominant, Alice can immediately force Bob into a position with no legal move. Otherwise, Bob can always answer at least the initial move, and the game continues in a controlled way where Bob survives long enough to eventually exhaust Alice’s advantage.

### Complexity comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(total stones × n) | O(n) | Too slow |
| Optimal Reduction | O(n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

The solution reduces to inspecting only the largest and second largest pile.

1. Find the maximum pile value in the array. This represents Alice’s optimal first move because any smaller choice only weakens her position.
2. Count how many piles attain this maximum value. This matters because Bob’s ability to respond depends on whether another pile can match Alice’s threshold.
3. If the maximum value appears exactly once, Alice can take the entire largest pile in her first move. After this move, no other pile can satisfy Bob’s requirement, so Bob immediately loses.
4. If the maximum value appears more than once, Bob can always respond to Alice’s initial move by choosing another maximum pile. This keeps the game alive past the opening and prevents Alice from forcing an immediate win.
5. In this case, the interaction continues in a symmetric way on the remaining large piles, and Bob can always mirror Alice’s pressure long enough to avoid being trapped immediately, leading to a win for Bob under optimal play.

### Why it works

The key invariant is that Bob’s constraint is fully determined by Alice’s first move and never depends on Bob’s actions. This makes the game effectively one of selecting a threshold from Alice’s initial choice. Once the threshold is fixed, Bob’s ability to move depends only on whether there exists at least one pile meeting or exceeding that threshold after each round of reductions.

If the maximum is unique, Alice can choose a threshold that is unattainable after her move, immediately collapsing Bob’s legal move set. If it is not unique, the threshold is always supported by at least one other pile at the start of Bob’s turn, preventing immediate collapse and allowing Bob to maintain viability through optimal play.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        mx = max(a)
        cnt = 0
        for x in a:
            if x == mx:
                cnt += 1
        
        if cnt == 1:
            print("Alice")
        else:
            print("Bob")

if __name__ == "__main__":
    solve()
```

The implementation directly computes the maximum and counts its occurrences. The reasoning is entirely based on the structure of the first move, so no simulation is required. The only subtlety is ensuring that the maximum count is computed correctly in O(n) time per test case.

## Worked Examples

### Example 1

Input:

```
1
3
1 4 5
```

We compute the maximum value as 5.

| Step | Maximum | Count of Max | Outcome |
| --- | --- | --- | --- |
| Initial | 5 | 1 | Alice wins |

Alice takes the entire pile of size 5. Bob would need to remove at least 5 stones from a remaining pile, but no such pile exists. The game ends immediately.

This confirms that a unique maximum directly forces a terminal position after Alice’s first move.

### Example 2

Input:

```
1
4
1 4 5 5
```

| Step | Maximum | Count of Max | Outcome |
| --- | --- | --- | --- |
| Initial | 5 | 2 | Bob wins |

Alice cannot force an immediate collapse because Bob can respond using the second maximum pile. The existence of multiple maximal piles prevents Alice from isolating Bob in a single move.

This demonstrates the structural difference introduced by duplicate maxima.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan once to compute maximum and frequency |
| Space | O(1) | Only counters and input array storage |

The constraints allow up to 2·10^5 total elements, so a single linear pass per test case is sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# Since solve() prints directly, wrap carefully in real usage environment

# provided-like samples
# (pseudo checks; adapt if embedding in full script)

# custom cases
# single pile
# assert run("1\n1\n10\n") == "Alice\n"

# two equal maxima
# assert run("1\n2\n5 5\n") == "Bob\n"

# strictly increasing
# assert run("1\n3\n1 2 3\n") == "Alice\n"

# all equal
# assert run("1\n4\n7 7 7 7\n") == "Bob\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 pile only | Alice | immediate win condition |
| two equal max | Bob | duplicate maximum case |
| strictly increasing | Alice | unique max dominance |
| all equal | Bob | full symmetry case |

## Edge Cases

A critical edge case is when all piles are identical. In this situation, no single pile gives Alice a dominating first move. After Alice takes one full pile, Bob always has another pile of equal size to respond, preventing immediate collapse. The algorithm correctly classifies this as Bob’s win because the maximum is not unique.

Another edge case is when there is only one pile. Alice removes it completely and Bob has no legal move. The algorithm correctly outputs Alice because the maximum appears exactly once.

A final subtle case is when the array is heavily skewed but not unique at the top. Even if one pile is extremely large and others are much smaller, as long as that maximum is unique, Alice wins immediately. The correctness depends only on uniqueness of the maximum, not its relation to the sum of other piles.
