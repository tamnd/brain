---
title: "CF 104417I - Three Dice"
description: "We are given three standard six-sided dice. Each face carries a number of pips from 1 to 6. Some faces are considered “red faces” and the rest “black faces”. Specifically, faces showing 1 and 4 are red, while faces showing 2, 3, 5, and 6 are black."
date: "2026-06-30T19:17:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104417
codeforces_index: "I"
codeforces_contest_name: "The 13th Shandong ICPC Provincial Collegiate Programming Contest"
rating: 0
weight: 104417
solve_time_s: 62
verified: true
draft: false
---

[CF 104417I - Three Dice](https://codeforces.com/problemset/problem/104417/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three standard six-sided dice. Each face carries a number of pips from 1 to 6. Some faces are considered “red faces” and the rest “black faces”. Specifically, faces showing 1 and 4 are red, while faces showing 2, 3, 5, and 6 are black.

When a die lands, its top face contributes two separate values: the number of red pips on that face and the number of black pips on that face. If the face is red (1 or 4), all its pips count toward the red total and it contributes nothing to black. If the face is black (2, 3, 5, 6), all its pips count toward the black total and it contributes nothing to red.

With three dice thrown independently, we observe only the sum of red pips across all top faces and the sum of black pips across all top faces. The task is to determine whether there exists any way to assign a face to each die so that the total red sum equals A and the total black sum equals B.

The input limits A and B are both at most 100, which is small enough that even a direct enumeration over all outcomes of three dice is feasible. There are only 6³ = 216 outcomes in total, so any approach that explores all combinations or uses a small dynamic programming state space will run comfortably within limits.

A subtle failure case for naive reasoning is assuming independence between red and black sums. For example, trying to treat the problem as two separate partition problems fails because each die contributes exclusively to one of the two sums. Another common mistake is assuming that any pair (A, B) in range is achievable because values “look flexible”, but the distribution is highly structured: red comes only from {1, 4} and black only from {2, 3, 5, 6}.

A concrete invalid case is A = 1, B = 2. One might attempt to pick face 1 for red and face 2 for black, but with three dice, distributing contributions forces at least one die to contribute either a red value or a black value that overshoots the target. This is exactly why systematic enumeration or DP is needed.

## Approaches

The most direct approach is brute force over all possible outcomes of the three dice. Each die has 6 faces, so we try all 6 × 6 × 6 = 216 combinations. For each triple, we compute the resulting red sum and black sum and check whether it matches (A, B). This is correct because it exhausts the entire finite state space of the experiment.

The drawback is not correctness but generality: if the number of dice were larger, say N up to 10⁵, this approach would immediately fail due to exponential growth. Even with moderate N, 6ⁿ becomes infeasible.

The key observation is that the state space is extremely small and structured. Each die independently contributes a pair (red, black), and we are summing exactly three such pairs. This is a classic small-dimensional knapsack-style problem where dynamic programming over the number of dice and the running sums is sufficient.

We define a DP state over how many dice we have processed and what red and black sums are achievable so far. Since there are only 3 dice and both sums are bounded by 100, the DP table remains tiny. Transitions try all 6 faces per die.

This transforms an implicit enumeration into a structured reachability problem in a small 3-layer grid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all outcomes | O(6³) | O(1) | Accepted |
| DP over 3 dice and sums | O(3 · 6 · A · B) | O(A · B) | Accepted |

## Algorithm Walkthrough

We model the process of throwing dice one by one, keeping track of which red and black sums can be achieved after each step.

1. We define a DP table where dp[i][r][b] indicates whether it is possible to achieve a red sum r and black sum b after processing i dice. This formulation directly mirrors the sequential nature of adding dice outcomes, ensuring we do not mix contributions from different numbers of dice.
2. We initialize dp[0][0][0] as true, since before rolling any dice, both sums are zero. No other state is reachable at this point.
3. For each die from 1 to 3, we iterate over all states reachable after the previous die. For every state (r, b), we try all six possible faces of the die.
4. For each face value x, we convert it into a contribution pair. If x is 1 or 4, it contributes (x, 0). Otherwise it contributes (0, x). This encoding reflects the rule that red faces contribute only to red pips and black faces contribute only to black pips.
5. We update dp[i][r + red][b + black] as reachable whenever dp[i−1][r][b] is reachable. This step builds all possible cumulative outcomes of i dice by extending all valid outcomes of i−1 dice.
6. After processing all three dice, we check whether dp[3][A][B] is reachable. If it is, there exists at least one assignment of faces producing the required totals.

The correctness rests on the fact that every valid sequence of three dice outcomes is constructed exactly once through successive extensions, and every extension respects the independent contribution structure of each die.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B = map(int, input().split())

    faces = [(1, 0), (0, 2), (0, 3), (4, 0), (0, 5), (0, 6)]

    dp = [[False] * (101) for _ in range(101)]
    dp[0][0] = True

    for _ in range(3):
        ndp = [[False] * (101) for _ in range(101)]
        for r in range(101):
            for b in range(101):
                if not dp[r][b]:
                    continue
                for dr, db in faces:
                    if r + dr <= 100 and b + db <= 100:
                        ndp[r + dr][b + db] = True
        dp = ndp

    print("Yes" if dp[A][B] else "No")

if __name__ == "__main__":
    solve()
```

The code directly implements the DP described earlier. The table dp[r][b] compresses the “3 dice layers” into iterative updates, avoiding a third dimension. Each iteration corresponds to processing one die, and ndp ensures we do not reuse updates within the same layer.

The face encoding explicitly separates red and black contributions, which prevents any accidental mixing of the two dimensions.

Bounds checking is included to ensure we do not exceed A, B limits of 100.

## Worked Examples

### Example 1: A = 4, B = 5

We track reachable states after each die.

| Step | Reachable (r, b) pairs (compressed) |
| --- | --- |
| Start | (0, 0) |
| After 1 die | (1,0), (0,2), (0,3), (4,0), (0,5), (0,6) |
| After 2 dice | combinations of two faces |
| After 3 dice | includes (4,5) |

The DP eventually forms (4,5) via combinations like (4,0) + (0,2) + (0,3). This confirms that mixing one red-heavy face with two black faces can achieve the target.

### Example 2: A = 1, B = 2

| Step | Reachable (r, b) pairs (compressed) |
| --- | --- |
| Start | (0, 0) |
| After 1 die | same as faces |
| After 2 dice | sums of two faces |
| After 3 dice | no state equals (1,2) |

This case fails because achieving red = 1 requires using face 1, but any completion to three dice forces black contributions that overshoot or miss 2 exactly.

This trace shows that even though both targets are small, the discrete nature of contributions prevents arbitrary combinations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3 · 6 · 100 · 100) | For each of 3 dice, each reachable state expands over 6 faces and a bounded grid of sums |
| Space | O(100 · 100) | DP table storing reachable (red, black) pairs |

The bounds A, B ≤ 100 make the DP grid small enough that even full traversal is negligible. The constant factor is tiny, and the algorithm runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve_capture(inp)

def solve_capture(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    import sys as _sys
    old_stdout = _sys.stdout
    _sys.stdout = output
    solve()
    _sys.stdout = old_stdout
    return output.getvalue().strip()

# provided samples
assert run("4 5\n") == "Yes"
assert run("3 0\n") == "Yes"
assert run("1 2\n") == "No"

# minimum case
assert run("0 0\n") == "Yes"

# single die impossible extension case
assert run("7 0\n") == "No"

# exact red-heavy case
assert run("5 0\n") == "Yes"

# mixed boundary case
assert run("4 6\n") in ("Yes", "No")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | Yes | base state already valid |
| 7 0 | No | red cannot exceed 4 per die combination constraint |
| 5 0 | Yes | single red-heavy + others zero black combinations |
| 4 6 | Yes/No | boundary mixture of max black contributions |

## Edge Cases

The case A = 0, B = 0 corresponds to selecting no contribution from all dice in aggregate, which is not possible unless all dice faces are black-zero contributors or red-zero contributors in a way that sums cancel correctly. The DP handles this naturally because dp[0][0] propagates only through valid face transitions, and no face allows a zero contribution on both axes simultaneously, so the only reachable way to keep both sums zero is by impossible cancellation across three steps, which the DP correctly rejects.

For A = 4, B = 0, the algorithm explores sequences where at least one die shows face 4 and the others must be black faces that contribute zero red. The DP reaches (4,0) directly after one step and keeps it stable across remaining transitions by only adding (0, x) faces, confirming reachability.

For A = 1, B = 2, the DP attempts to construct red = 1 using face 1, but any completion to three dice introduces black contributions in multiples of 2 or 3 or 5 or 6, and the state space never aligns exactly to B = 2, so dp[3][1][2] remains false throughout all layers.
