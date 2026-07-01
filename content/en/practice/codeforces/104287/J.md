---
title: "CF 104287J - Two and Three"
description: "We are given several independent test cases. In each test case there is an array of positive integers. Two players alternate turns, starting with Nino."
date: "2026-07-01T20:49:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104287
codeforces_index: "J"
codeforces_contest_name: "Teamscode Spring 2023 Contest"
rating: 0
weight: 104287
solve_time_s: 73
verified: true
draft: false
---

[CF 104287J - Two and Three](https://codeforces.com/problemset/problem/104287/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case there is an array of positive integers. Two players alternate turns, starting with Nino. On a turn, a player selects any single element and replaces it with either ⌊x/2⌋ or ⌊x/3⌋, but only if the result is still positive. If a player has no valid move on their turn, they lose. The question is who wins assuming both players play optimally.

The key aspect is that the game state is not just the array values but how many reduction steps are still possible from each value. Each number evolves independently except for turn order, since only one element is modified per move.

The constraints are large: up to 100000 test cases and total array size up to 100000. This rules out any per-move simulation of the game tree. Even computing the full game graph per number would be too slow, since a single value up to 10^9 can have many reduction paths if explored naively.

The natural danger is trying to simulate moves directly. For example, for a single value like 10^9, repeatedly dividing by 2 or 3 generates a large branching tree of states, and combining multiple such values makes the state space exponential. Any approach that treats each move explicitly will fail.

A second subtle issue is assuming that only parity of values matters. That is false because dividing by 3 creates a different reduction trajectory than dividing by 2, and they are not equivalent in game terms.

## Approaches

At first glance, this is a normal impartial combinatorial game. Each array element behaves like a pile where you can reduce its size in discrete steps. This suggests computing a Grundy number per element and XORing them.

If we brute-force a single value x, we can define all reachable states by repeatedly applying x → ⌊x/2⌋ or x → ⌊x/3⌋ while result remains positive. That builds a directed acyclic graph of states. From that graph we compute the Grundy number. This is correct, because each move reduces the value strictly, so no cycles exist.

However, brute-force generation of all states for each x is expensive. In the worst case, each number can generate O(log x) depth, and branching by 2 operations leads to many repeated states across different test cases. Over 10^5 values, this becomes too slow.

The key observation is that the state graph of a number is extremely structured. Every value eventually maps down to a small set of terminal states, and most paths quickly converge. More importantly, the Grundy value depends only on how many times we can divide by 2 and 3 in different sequences, which reduces to counting states in a small reachable set rather than exploring full paths.

A more efficient view is to compute the Grundy value for all numbers up to the maximum reachable via division chains, but since each step reduces the value by at least a factor of 2 or 3, the total distinct reachable values across all nodes is small enough to precompute dynamically per test case without duplication. This leads to memoization over states with direct transitions to ⌊x/2⌋ and ⌊x/3⌋.

Once we compute Grundy values for each element, the overall game is a sum of independent impartial games, so XOR determines the winner: non-zero XOR means first player wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force state exploration per test case | Exponential in worst case | O(n) | Too slow |
| Memoized DP over transitions x→x/2, x/3 | O(n log A) amortized | O(n log A) | Accepted |

## Algorithm Walkthrough

We treat each value as a game state whose Grundy number depends on its two possible moves.

1. For each test case, we process every element independently, but reuse a global memoization map so repeated values are not recomputed. This is valid because the game rules depend only on the value, not its position.
2. Define a function grundy(x) that returns the Grundy number of a value x. If x equals 1, no move is possible, so its Grundy number is 0.
3. For x greater than 1, we consider all reachable states: x divided by 2 and x divided by 3, but only if the result stays positive. These are the only legal moves, so they fully define the transition structure.
4. Recursively compute grundy(x // 2) and grundy(x // 3). Collect their results into a set.
5. The Grundy value of x is the mex (minimum excluded value) of that set. In this problem, the set size is at most 2, so mex is computed by checking 0, 1, 2 in order.
6. XOR all grundy(a_i) over the array. If the result is non-zero, Nino wins; otherwise Miku wins.

### Why it works

Each move strictly decreases the value of a chosen element, so the game graph is acyclic and fits standard Sprague-Grundy theory. Each element is an independent subgame because a move only affects one position. Therefore the full game is the XOR of independent Grundy values.

The memoization ensures each integer value is solved once, and since every transition reduces magnitude by at least a factor of 2 or 3, the recursion depth is logarithmic in the value size. This guarantees that the DP converges quickly and no recomputation inflates the complexity.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

memo = {}

def grundy(x):
    if x == 1:
        return 0
    if x in memo:
        return memo[x]

    moves = set()

    nx = x // 2
    if nx > 0:
        moves.add(grundy(nx))

    ny = x // 3
    if ny > 0:
        moves.add(grundy(ny))

    g = 0
    while g in moves:
        g += 1

    memo[x] = g
    return g

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    xor_sum = 0
    for v in arr:
        xor_sum ^= grundy(v)

    print("Nino" if xor_sum != 0 else "Miku")
```

The solution is built around a memoized recursive Grundy computation. The memo dictionary ensures each value is evaluated once globally. The recursion handles the two allowed transitions directly.

The mex computation is simplified because each state has at most two outgoing edges, so we only test small integers sequentially.

The XOR aggregation implements Sprague-Grundy theorem for disjoint piles.

A subtle implementation detail is the global memo: without it, repeated values across test cases would recompute entire chains, blowing up time. Another subtlety is recursion depth; although values shrink quickly, Python recursion limits can still be hit for adversarial chains, so the recursion limit is increased.

## Worked Examples

We trace two of the sample test cases.

### Sample: `[1, 2, 5]`

We compute Grundy values:

| Value | x//2 | x//3 | Move Grundy set | Grundy |
| --- | --- | --- | --- | --- |
| 1 | - | - | ∅ | 0 |
| 2 | 1 | 0 invalid | {0} | 1 |
| 5 | 2 | 1 | {1, 0} | 2 |

Now XOR: 0 ⊕ 1 ⊕ 2 = 3 ≠ 0, so Nino wins.

This demonstrates that even small branching from 5 produces two distinct reachable Grundy states, giving a non-trivial mex.

### Sample: `[1, 2, 3, 4]`

We compute:

| Value | x//2 | x//3 | Move Grundy set | Grundy |
| --- | --- | --- | --- | --- |
| 1 | - | - | ∅ | 0 |
| 2 | 1 | 0 invalid | {0} | 1 |
| 3 | 1 | 1 | {0} | 1 |
| 4 | 2 | 1 | {1, 0} | 2 |

XOR: 0 ⊕ 1 ⊕ 1 ⊕ 2 = 2 ≠ 0, so Nino wins.

This trace shows cancellation effects in XOR when multiple identical Grundy values appear, while still leaving a non-zero result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑ log a_i) amortized | Each integer state is computed once, and each computation only recurses to x/2 and x/3 |
| Space | O(#distinct reachable values) | Memoization stores one entry per encountered value |

The total number of states is bounded by the number of unique values reachable via repeated division by 2 and 3 from all inputs. Since each step reduces magnitude quickly, this remains within limits for total input size 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    sys.setrecursionlimit(10**7)
    memo = {}

    def grundy(x):
        if x == 1:
            return 0
        if x in memo:
            return memo[x]

        moves = set()

        nx = x // 2
        if nx > 0:
            moves.add(grundy(nx))

        ny = x // 3
        if ny > 0:
            moves.add(grundy(ny))

        g = 0
        while g in moves:
            g += 1

        memo[x] = g
        return g

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        xor_sum = 0
        for v in arr:
            xor_sum ^= grundy(v)
        res.append("Nino" if xor_sum else "Miku")

    return "\n".join(res) + "\n"

# provided samples
assert run("""5
3
1 2 5
3
2 3 4
2
3366 3366
1
1000000000
7
1 2 3 4 5 6 7
""") == """Nino
Nino
Miku
Nino
Miku
"""

# custom cases
assert run("""1
1
1
""") == "Miku\n", "single losing state"

assert run("""1
1
2
""") == "Nino\n", "single winning state"

assert run("""1
3
1 1 1
""") == "Miku\n", "all neutral"

assert run("""1
4
2 2 2 2
""") == "Miku\n", "even XOR cancellation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1 | Miku | terminal losing position |
| single 2 | Nino | simplest winning move |
| all ones | Miku | all zero Grundy |
| four twos | Miku | XOR cancellation |

## Edge Cases

For `a = [1]`, the only element already has no valid moves, so the starting player immediately loses. The algorithm returns Grundy(1) = 0, XOR = 0, so Miku wins.

For large values like `10^9`, recursion repeatedly applies division by 2 and 3 until reaching 1. The memoization ensures that overlapping subproblems like 10^9 → 5×10^8 → 2.5×10^8 are computed once, and reused across the entire test suite. This prevents exponential blowup.

For repeated identical elements, such as `[2, 2, 2, 2]`, each contributes Grundy(2) = 1, and XOR cancels pairwise. The algorithm correctly produces 0, meaning the second player wins, matching the symmetry of identical independent piles.
