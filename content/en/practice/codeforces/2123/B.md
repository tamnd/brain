---
title: "CF 2123B - Tournament"
description: "We have a tournament with n players. Player i has strength a[i]. Repeatedly, two surviving players are selected, and the weaker one is eliminated. If both strengths are equal, either one may be eliminated. The process stops when exactly k players remain."
date: "2026-06-08T03:36:43+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2123
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1034 (Div. 3)"
rating: 800
weight: 2123
solve_time_s: 104
verified: true
draft: false
---

[CF 2123B - Tournament](https://codeforces.com/problemset/problem/2123/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tournament with `n` players. Player `i` has strength `a[i]`. Repeatedly, two surviving players are selected, and the weaker one is eliminated. If both strengths are equal, either one may be eliminated.

The process stops when exactly `k` players remain. We are interested in a specific player `j`. The question is whether there exists some sequence of pair selections and tie outcomes that allows player `j` to still be alive among the final `k` players.

The key phrase is "is there any way". We are not asked for probability, nor must the player survive under all possible tournament outcomes. We only need one favorable sequence.

The constraints are large enough that any simulation of tournament states is impossible. Across all test cases, the total number of players reaches `2 · 10^5`, so we should expect an `O(n)` or `O(n log n)` solution. Anything that explores tournament brackets, subsets of survivors, or state-space transitions would grow exponentially and fail immediately.

A subtle aspect of the problem is that pairings are completely under our control when checking existence. If a player can be protected by choosing other matches first, that is allowed.

Consider the case

```
n = 4, j = 1, k = 1
strengths = [1, 2, 3, 4]
```

Player 1 is the weakest. To become the sole survivor, player 1 would eventually have to defeat a stronger player, which is impossible. The correct answer is `NO`.

Now consider

```
n = 4, j = 1, k = 2
strengths = [1, 2, 3, 4]
```

We can eliminate two stronger players against each other:

```
2 vs 3 -> 2 eliminated
4 vs winner -> another player eliminated
```

When only two players remain, player 1 can still be alive. The correct answer is `YES`.

A common mistake is to think that the relative rank of player `j` among all strengths always matters. It only matters when we need player `j` to be the unique champion.

## Approaches

A brute-force approach would model the entire tournament process. At each stage we would choose a pair of surviving players, perform the elimination, and recursively continue. The number of possible tournament states grows explosively. Even for twenty players the number of possible elimination sequences is enormous, making this completely infeasible.

The reason brute force is correct is that it explicitly explores every valid tournament. The reason it fails is that the number of pair choices is roughly quadratic at every step, creating an exponential search tree.

To find a simpler characterization, focus on what eliminations actually do.

Whenever two players meet, one player disappears. If there are at least two players stronger than player `j`, we can simply keep matching those stronger players against each other. Every such match removes one strong player. Repeating this eventually leaves at most one player stronger than `j`.

If the tournament stops with `k > 1` survivors, having one stronger player remaining is perfectly fine. Player `j` only needs to be among the survivors, not necessarily the strongest survivor.

The only difficult case is `k = 1`. Then player `j` must be the champion. A champion cannot have any strictly stronger player in the tournament, because sooner or later that stronger player would defeat player `j` or defeat whoever reaches the final against them.

Thus:

If `k > 1`, every player can be kept alive until the final `k` survivors.

If `k = 1`, player `j` can win only when their strength is equal to the maximum strength in the entire array.

This reduces the whole problem to a single maximum check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the strength of player `j`, namely `a[j-1]`.
2. If `k > 1`, immediately answer `"YES"`.

When more than one survivor is allowed, we can always arrange matches among other players and avoid eliminating player `j` until only `k` players remain.
3. If `k = 1`, compute the maximum strength in the array.
4. Compare `a[j-1]` with that maximum.

If they are equal, answer `"YES"`.

Otherwise answer `"NO"`.
5. Repeat for all test cases.

### Why it works

When `k > 1`, we only need player `j` to survive, not to become champion. Any time there are more than `k` players remaining, we can choose two players different from `j` whenever possible. Eliminations among the other players reduce the field while preserving player `j`. Eventually only `k` players remain, and player `j` is still alive.

When `k = 1`, player `j` must be the final survivor. Any player with strictly greater strength can never lose to player `j`, so such a player prevents player `j` from becoming champion. Conversely, if player `j` has maximum strength, all remaining opponents are no stronger. By arranging matches appropriately and using favorable tie outcomes when strengths are equal, player `j` can become the champion.

These two observations completely characterize all possible cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        n, j, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        if k > 1:
            print("YES")
        else:
            print("YES" if a[j - 1] == max(a) else "NO")

solve()
```

The implementation follows the proof directly.

For each test case we first check whether `k` exceeds `1`. In that situation the answer is always `"YES"`, so no further work is required.

Only the `k = 1` case needs analysis. We retrieve the strength of player `j` using `j - 1` because Python arrays are zero-indexed while the problem uses one-indexed player numbering.

The comparison must be against the global maximum strength, not against the count of stronger players. Equal maximum values are sufficient because ties can be resolved in whichever way is favorable to player `j`.

The code performs a single pass to compute the maximum, giving linear time per test case.

## Worked Examples

### Example 1

Input:

```
n = 5
j = 2
k = 3
strengths = [3, 2, 4, 4, 1]
```

| Variable | Value |
| --- | --- |
| k | 3 |
| k > 1 ? | Yes |
| Answer | YES |

Since more than one survivor is allowed, player 2 can simply avoid elimination while other players are removed.

### Example 2

Input:

```
n = 6
j = 1
k = 1
strengths = [1, 2, 3, 4, 5, 6]
```

| Variable | Value |
| --- | --- |
| k | 1 |
| Player strength | 1 |
| Maximum strength | 6 |
| Equal? | No |
| Answer | NO |

Player 1 is not among the strongest players. A stronger player must survive every confrontation against player 1, so player 1 can never become champion.

These traces demonstrate the two branches of the solution. Once `k > 1`, survival is always achievable. When `k = 1`, only the maximum-strength players can possibly win.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Computing the maximum strength requires one scan |
| Space | O(1) extra | Only a few variables are used |

The sum of all `n` values is at most `2 · 10^5`, so the total running time is linear in the input size. This easily fits within the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    out = []

    t = int(input())

    for _ in range(t):
        n, j, k = map(int, input().split())
        a = list(map(int, input().split()))

        if k > 1:
            out.append("YES")
        else:
            out.append("YES" if a[j - 1] == max(a) else "NO")

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""3
5 2 3
3 2 4 4 1
5 4 1
5 3 4 5 2
6 1 1
1 2 3 4 5 6
"""
) == """YES
YES
NO
"""

# minimum size, strongest player
assert run(
"""1
2 1 1
2 1
"""
) == """YES
"""

# minimum size, weakest player
assert run(
"""1
2 2 1
2 1
"""
) == """NO
"""

# all equal strengths
assert run(
"""1
5 3 1
7 7 7 7 7
"""
) == """YES
"""

# k > 1 always succeeds
assert run(
"""1
5 1 2
1 2 3 4 5
"""
) == """YES
"""

# maximum strength appears multiple times
assert run(
"""1
4 2 1
5 5 1 1
"""
) == """YES
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1 / 2 1` | YES | Smallest valid winning case |
| `2 2 1 / 2 1` | NO | Smallest valid losing case |
| All strengths equal | YES | Tie handling for maximum values |
| `k = 2` with weakest player | YES | Any player can survive when `k > 1` |
| Multiple maximum values | YES | Maximum need not be unique |

## Edge Cases

Consider:

```
1
4 1 1
1 2 3 4
```

Player 1 has strength 1, while the maximum is 4. The algorithm enters the `k = 1` branch and compares `1` with `4`, producing `NO`. This is correct because player 1 must eventually face a stronger player and lose.

Consider:

```
1
5 1 2
1 2 3 4 5
```

The algorithm sees `k > 1` and immediately outputs `YES`. A careless solution might reject player 1 because they are the weakest. That would be wrong, since we only need player 1 to remain among the final two survivors, not to win the entire tournament.

Consider:

```
1
5 3 1
7 7 7 7 7
```

The maximum strength is 7, and player 3 also has strength 7. The algorithm outputs `YES`. This correctly handles ties. Since equal-strength matches may eliminate either participant, there exists a sequence where player 3 becomes the final champion.

Consider:

```
1
4 2 1
5 5 1 1
```

Player 2 shares the maximum strength. The algorithm outputs `YES` because `a[1] = max(a)`. Even though another player has the same strength, tie outcomes can be chosen favorably, so player 2 can still be the sole survivor.
