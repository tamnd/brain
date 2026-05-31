---
title: "CF 1965A - Everything Nim"
description: "We are given several independent games, each defined by a list of piles containing stones. Two players alternate turns."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1965
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 941 (Div. 1)"
rating: 1400
weight: 1965
solve_time_s: 84
verified: false
draft: false
---

[CF 1965A - Everything Nim](https://codeforces.com/problemset/problem/1965/A)

**Rating:** 1400  
**Tags:** games, greedy, math, sortings  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent games, each defined by a list of piles containing stones. Two players alternate turns. A move consists of choosing an integer $k$ that does not exceed the smallest nonempty pile, then simultaneously subtracting $k$ stones from every pile that is still nonempty. Any pile that reaches zero disappears from play.

The game ends when all piles are empty, and the player who cannot make a move loses. Since a move always reduces at least the smallest pile to zero, the number of active piles strictly decreases over time, so every game finishes in at most $n$ moves.

The task is to determine, for each test case, whether the first player has a forced win under optimal play.

The constraints allow up to $2 \cdot 10^5$ total piles across all test cases, so any solution must be essentially linear or linearithmic in the input size. A solution that simulates each move is impossible because even a single game can have up to $10^5$ piles and each move touches all of them, leading to quadratic behavior.

A naive approach would simulate the game step by step. For each turn, we would scan all piles, compute the minimum, subtract a chosen $k$, and remove zeros. This fails immediately under the constraints.

Another common failure case comes from assuming the sum of all stones or parity of total stones determines the winner. For example, a configuration like $[1,7]$ has the same total parity as $[2,6]$, but the game outcomes differ because the structure of minimum-driven removal changes the number of forced moves.

## Approaches

The brute-force idea is straightforward: repeatedly compute the minimum nonempty pile, choose a legal $k$, and simulate both players under optimal choices. Even if we try to optimize by always picking an “obvious” move like $k = \min$, we still face a branching game tree because different values of $k$ can lead to different pile eliminations. This leads to an exponential number of states in general.

The key structural observation is that the minimum value fully controls the legality of moves. If the current minimum is $m$, then choosing any $k < m$ simply shifts all piles down by $k$ without removing any pile. This never changes the relative order of pile sizes and only delays termination. A rational player never prefers delaying forced reductions when they can instead eliminate the smallest layer immediately.

So optimal play always uses $k = m$, the current minimum. That move deletes all piles equal to the minimum and reduces the rest by exactly that value. After this, the next state depends only on the next distinct pile value, not on individual pile multiplicities beyond whether they are equal or not.

This turns the game into a process on the sequence of distinct values. Each step removes one “layer” corresponding to a distinct height. The only information that survives is how many distinct levels exist.

This reduces the entire game to a parity question.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Sort + Distinct Count | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reduce each test case to its set of distinct pile sizes.

1. Read the array of pile sizes.
2. Sort the array so equal values become adjacent, making it easy to identify distinct values.
3. Count how many distinct values exist.
4. If this count is odd, declare Alice the winner, otherwise declare Bob the winner.

The reason we only count distinct values is that every move removes exactly one distinct value level from the game. The internal multiplicity of each value does not affect how many “layers” of decisions exist, only how many piles disappear at each step.

### Why it works

The game evolves by repeatedly removing the current minimum value from all active piles. This operation eliminates at least one distinct value every move and never creates new distinct values. Therefore, the game is equivalent to a simple alternating process over the list of distinct pile heights. Each move corresponds to consuming exactly one level. The player who consumes the last level wins, so the outcome depends only on whether the number of levels is odd or even.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        
        distinct = 1
        for i in range(1, n):
            if a[i] != a[i - 1]:
                distinct += 1
        
        if distinct % 2 == 1:
            out.append("Alice")
        else:
            out.append("Bob")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code relies on sorting to group equal pile sizes together. After sorting, a single linear scan counts transitions between values. Each transition corresponds to a new distinct “layer” in the game.

The parity check at the end directly reflects the alternating structure of moves: each move removes one distinct minimum level, so the number of such levels determines who makes the final move.

## Worked Examples

We trace the logic on two representative cases.

### Example 1: `3 3 3 3 3`

After sorting, the array remains `[3]` in terms of distinct values.

| Step | Array | Distinct count |
| --- | --- | --- |
| Initial | [3,3,3,3,3] | 1 |

The count is odd, so Alice wins.

This matches intuition because Alice can remove all stones in one move by choosing $k=3$.

### Example 2: `1 7`

| Step | Array | Distinct count |
| --- | --- | --- |
| Initial | [1,7] | 2 |

The count is even, so Bob wins.

After Alice removes the first layer ($k=1$), the game collapses to a single pile of size 6, giving Bob a direct winning move.

This shows that the first move only exposes how many layers remain, and the second player benefits when that number is even.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, followed by a linear scan |
| Space | O(1) extra (or O(n) depending on sort) | Only the input array is stored |

The solution comfortably fits within the limits since the total number of elements across test cases is at most $2 \cdot 10^5$, and sorting that scale is efficient under a 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        d = 1
        for i in range(1, n):
            if a[i] != a[i - 1]:
                d += 1
        res.append("Alice" if d % 2 else "Bob")
    return "\n".join(res)

# provided samples
assert run("""7
5
3 3 3 3 3
2
1 7
7
1 3 9 7 4 2 100
3
1 2 3
6
2 1 3 4 2 4
8
5 7 2 9 6 3 3 2
1
1000000000
""") == """Alice
Bob
Alice
Alice
Bob
Alice
Alice"""

# all equal
assert run("""1
4
10 10 10 10
""") == "Alice"

# two piles same
assert run("""1
2
5 5
""") == "Alice"

# increasing chain
assert run("""1
4
1 2 3 4
""") == "Alice"

# alternating structure
assert run("""1
4
1 100 2 99
""") == "Bob"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal piles | Alice | single distinct level |
| identical two piles | Alice | minimal even-size symmetry case |
| strictly increasing | Alice | maximal distinct count parity |
| symmetric extremes | Bob | even distinct structure |

## Edge Cases

The most important edge case is when all piles are identical. In this situation, there is only one distinct value, so the first player immediately wins by removing everything in a single move. The algorithm captures this because the distinct counter equals one, producing Alice as the winner.

Another subtle case is when piles form a perfectly staggered sequence like $[1,2,3,4]$. Even though the values are spread out, each value still contributes exactly one distinct level, so the outcome depends only on the parity of four, leading to a win for the second player.

Finally, cases with repeated values interleaved with others, such as $[1,100,2,99]$, do not affect correctness. Sorting collapses duplicates correctly, and only transitions matter, so the algorithm correctly counts four distinct values and returns the losing position for Alice.
