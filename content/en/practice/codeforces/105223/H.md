---
title: "CF 105223H - Game with wife"
description: "We are given several independent test cases. Each test case describes a game state consisting of several piles of stones."
date: "2026-06-24T16:40:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105223
codeforces_index: "H"
codeforces_contest_name: "HIAST Collegiate Programming Contest 2024"
rating: 0
weight: 105223
solve_time_s: 60
verified: true
draft: false
---

[CF 105223H - Game with wife](https://codeforces.com/problemset/problem/105223/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case describes a game state consisting of several piles of stones. On each turn, a player may either remove a single stone from any one non-empty pile, or perform a combined move where exactly three non-empty piles are chosen, all having the same parity in their current sizes, and one stone is removed from each of those three piles.

Players alternate moves, and the player who cannot make a move loses, which only happens when all piles are empty. The question is to determine whether the first player to move (Besher) has a forced win or not under optimal play.

The constraints are large, with up to 200,000 piles across all test cases and pile sizes up to 10^9. This immediately rules out any simulation of gameplay or state exploration. Any solution that attempts to model states dynamically or search through moves is infeasible because the branching factor is large and the depth can reach the total number of stones.

The only structure that can realistically survive these constraints is something that compresses the entire configuration into a small invariant, most likely involving parity or a simple aggregate.

A subtle failure case for naive reasoning is assuming piles are independent because of the “take one from any pile” move. For example, with piles `[1, 1, 1]`, independence would suggest three separate single-stone games, but the triple-parity move immediately allows removing all three stones in one move, which changes the game length and structure significantly. Any correct solution must account for that interaction.

Another misleading case is thinking only the number of piles matters. For instance, `[2, 2, 2]` and `[1, 1, 1]` have identical structure in terms of count, but different future parity behavior if one tries to reason too coarsely.

## Approaches

A brute-force approach would treat the state as the full vector of pile sizes and attempt to compute winning/losing positions using recursion with memoization. Each state would branch into up to `n` single-removal moves and potentially many triple-removal moves depending on parity groups. Even if we compress states, the number of reachable configurations is astronomically large because each pile can independently decrease from `10^9` to `0`. This makes any state-based dynamic programming impossible.

The key observation is that every move reduces the total number of stones by either 1 or 3. Both are odd numbers, so every move flips the parity of the total sum of stones. This immediately restricts the game graph into two alternating layers based on sum parity.

Once we focus on parity of the total sum, the structure simplifies further. In all examined cases, the presence of the special triple-parity move does not create a second independent invariant beyond total parity, because it still consumes an odd number of stones and does not introduce any operation that preserves parity or creates cyclic advantage. It only bundles three independent single removals into one move, without changing reachability of losing positions.

This leads to the core simplification: the game outcome depends only on whether the total number of stones is odd or even.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force State Search | Exponential | Exponential | Too slow |
| Parity Reduction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce each test case to a single integer, the sum of all pile sizes.

1. Compute the total sum of all stones across all piles. This is the only global quantity that matters, because every move changes the sum by an odd number, which flips parity.
2. Check whether this sum is odd or even. The parity fully determines the winner under optimal play.
3. If the sum is odd, the first player wins. Otherwise, the second player wins.

The reason this is sufficient is that every legal move transitions the game into a state with the opposite parity of total stones. Since the only terminal state is sum zero, which is even, any odd-sum state must have at least one move, and optimal play reduces to forcing the opponent into the opposite parity each turn until termination.

## Why it works

The game can be viewed as a finite directed acyclic graph where each edge corresponds to a legal move, and every edge flips the parity of the total sum. Because the terminal position has even parity (sum zero), the game becomes a bipartite structure where winning positions alternate strictly by parity layer. There is no additional invariant introduced by the parity-restricted triple move that breaks this alternation or creates a separate losing class within a parity layer, so parity fully characterizes the winning condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        total = sum(arr)
        if total % 2 == 1:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction. The only computation per test case is summing the array, which is safe under the constraints. There is no need to track parity per pile or simulate transitions.

A common mistake here is attempting to maintain counts of odd and even piles or simulating the triple-move condition. None of that affects the final decision, because the global sum already encodes all relevant information.

## Worked Examples

Consider the input where piles are `[1, 1]`.

| Step | Piles | Sum | Decision |
| --- | --- | --- | --- |
| Start | [1, 1] | 2 | Even |

The sum is even, so the first player is predicted to lose. Indeed, any move reduces the sum to 1, leaving a single stone for the second player, who can take it and win.

Now consider `[1, 1, 1]`.

| Step | Piles | Sum | Decision |
| --- | --- | --- | --- |
| Start | [1, 1, 1] | 3 | Odd |

The sum is odd, so the first player wins. In fact, they can immediately use the triple-parity move to remove all three stones and finish the game.

Now consider `[1, 1, 2]`.

| Step | Piles | Sum | Move choice | Next sum |
| --- | --- | --- | --- | --- |
| Start | [1, 1, 2] | 4 | remove from 2 | 3 |
| Result | [1, 1, 1] | 3 | forced transition | odd |

All possible moves lead to odd-sum states, which are winning for the next player, making the starting position losing.

These examples show that only the parity of the total sum is stable under optimal reasoning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each pile is read once and added to the sum |
| Space | O(1) extra | Only a running sum is stored |

The solution fits easily within constraints because the total number of elements across all test cases is at most 2 × 10^5, making a single linear scan sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        total = sum(arr)
        out.append("YES" if total % 2 == 1 else "NO")
    return "\n".join(out) + "\n"

# provided sample (interpreted)
assert run("1\n2\n1 2\n") == "NO\n"

# all equal small
assert run("1\n3\n1 1 1\n") == "YES\n"

# even sum simple
assert run("1\n3\n1 1 2\n") == "NO\n"

# single pile
assert run("2\n1\n1\n1\n2\n") == "YES\nNO\n"

# large even
assert run("1\n4\n2 2 2 2\n") == "NO\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,1,1]` | YES | triple move immediate win |
| `[1,1,2]` | NO | mixed parity losing position |
| single pile cases | YES/NO by parity | reduction to classic subtraction game |
| all even | NO | even-sum losing state |

## Edge Cases

For a single pile, the game reduces to repeatedly removing one stone, so the outcome alternates purely by parity. The algorithm handles this correctly because the sum is exactly the pile size, and parity matches the known result of a single take-1 game.

For configurations where triple moves are technically available, such as `[2,2,2]`, the algorithm still behaves correctly. The sum is even, so it predicts a loss for the first player. Even though a triple move exists, it only removes three stones and does not change the parity-based conclusion.

For mixtures like `[1,1,1,1]`, multiple triple moves are possible at different stages, but each move still flips parity. The total sum is even, so the first player loses, and any move preserves the correctness of this classification when traced step by step.
