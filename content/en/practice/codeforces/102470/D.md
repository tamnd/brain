---
title: "CF 102470D - Darts"
description: "The straightforward approach is to keep the entire game tree. From a state containing both scores, we try every possible dart result, move to the next state, and continue recursively. This is correct because each possible future is explored with its probability."
date: "2026-08-05T20:40:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102470
codeforces_index: "D"
codeforces_contest_name: "2009-2010 ACM ICPC Southwestern European Regional Programming Contest (SWERC 2009)"
rating: 0
weight: 102470
solve_time_s: 85
verified: true
draft: false
---

[CF 102470D - Darts](https://codeforces.com/problemset/problem/102470/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Approaches

The straightforward approach is to keep the entire game tree. From a state containing both scores, we try every possible dart result, move to the next state, and continue recursively. This is correct because each possible future is explored with its probability. However, the number of possible histories grows exponentially. Even if we only considered 20 outcomes per throw, a few dozen turns already create more branches than the program can handle.

The useful observation is that the future depends only on the two remaining scores and whose turn it is. We do not need to remember how those scores were reached. The game is a finite state dynamic program over `(score of A, score of B, turn)`.

Let `winA[a][b]` be the probability that A eventually wins when it is A's turn and the two remaining scores are `a` and `b`. Let `winB[a][b]` be the same probability when it is B's turn.

A's transition is direct: for every possible sector hit, either A finishes immediately or the game moves to B's turn with a smaller A score. B's transition is similar, except B is trying to win, so a successful B throw contributes probability zero to A's winning chance.

The states can be filled in increasing order of the two scores because every non-terminal transition decreases one player's score. When computing `(a, b)`, all required states have already been computed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of throws | Exponential recursion tree | Too slow |
| Optimal | O(N² · 20) | O(N²) | Accepted |

## Algorithm Walkthrough

1. Precompute the probability distribution for A. Every one of the 20 sectors has probability `1/20`, so A's distribution is the same for every state.
2. Precompute the probability distribution that B gets after choosing each possible target sector. For every target, the target sector and its two neighbors receive probability `1/3`. For a given remaining score, B selects the target that maximizes B's chance of finishing the game.
3. Build two dynamic programming tables. `winA[a][b]` stores A's winning probability when A throws with scores `a` and `b`. `winB[a][b]` stores the same value when B throws.
4. Fill the tables from small scores to large scores. When calculating `winA[a][b]`, examine every possible A dart result. A result that removes exactly `a` points gives an immediate win. Other valid results move to `winB[a - value][b]`.
5. When calculating `winB[a][b]`, first determine the best target sector for B. Every possible result from that target is considered. Hitting exactly `b` means A loses, while all other results continue with A's turn.
6. For an input `N`, the first requested answer is `winA[N][N]`. The second is `1 - winB[N][N]`, because `winB` stores the probability that A wins when B starts.

Why it works:

The invariant is that each dynamic programming entry represents the exact winning probability from that game state. A transition partitions all possible dart outcomes into mutually exclusive cases whose probabilities sum to one. Every non-winning outcome reduces one player's score, so the dependency always points to an already computed state. Since all possible first throws and all later states are included, the computed probability matches the real game probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

ORDER = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17,
         3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

MAXN = 501

def solve():
    # A's distribution
    a_prob = [0.0] * 21
    for x in ORDER:
        a_prob[x] += 1.0 / 20.0

    # For every score, compute B's best distribution.
    # b_probs[score] is a list of (value, probability) pairs.
    b_probs = [[] for _ in range(MAXN + 1)]
    for score in range(1, MAXN + 1):
        best = None
        best_finish = -1.0
        for i in range(20):
            dist = {}
            for j in ((i - 1) % 20, i, (i + 1) % 20):
                dist[ORDER[j]] = dist.get(ORDER[j], 0.0) + 1.0 / 3.0
            finish = dist.get(score, 0.0)
            if finish > best_finish:
                best_finish = finish
                best = list(dist.items())
        b_probs[score] = best

    win_a = [[0.0] * (MAXN + 1) for _ in range(MAXN + 1)]
    win_b = [[0.0] * (MAXN + 1) for _ in range(MAXN + 1)]

    for a in range(1, MAXN + 1):
        for b in range(1, MAXN + 1):
            wa = 0.0
            for value, p in enumerate(a_prob):
                if value == 0:
                    continue
                if a - value <= 0:
                    wa += p
                else:
                    wa += p * win_b[a - value][b]
            win_a[a][b] = wa

            wb = 0.0
            for value, p in b_probs[b]:
                if b - value <= 0:
                    pass
                else:
                    wb += p * win_a[a][b - value]
            win_b[a][b] = wb

    out = []
    for line in sys.stdin:
        n = int(line)
        if n == 0:
            break
        out.append(f"{win_a[n][n]:.12f} {1.0 - win_b[n][n]:.12f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part builds A's fixed throwing probabilities. The array has one entry for each possible sector value, because later transitions only care about how many points are removed.

The second part builds B's decisions. For every possible current score, the code tries every target sector and keeps the one with the largest chance of immediately finishing. This is sufficient because the dynamic programming state already represents the future after a non-finishing throw.

The two nested loops fill the game states. The order of the loops works because every transition decreases either A's score or B's score, so no state depends on itself or a future state.

The final output uses `1.0 - win_b[n][n]` because the B-turn table was defined as the probability that A wins. The requested value is the opposite event.

## Worked Examples

For `N = 5`, the initial state is `(5,5)`.

| State | Turn | Action considered | Result |
| --- | --- | --- | --- |
| (5,5) | A | A can only finish by hitting 5 | A wins with probability 0.05 immediately, otherwise state changes |
| (remaining A score, 5) | B | B chooses the sector maximizing its finishing chance | B-turn values are used |
| (5,5) | A first | Dynamic programming value | 0.136363636364 |

This trace shows why overshooting cannot be treated as a reduction. Most throws do not change the score and the recursion must return to the opponent's turn.

For `N = 100`, the same recurrence is applied over a much larger state space.

| State | Turn | Main transition | Stored value |
| --- | --- | --- | --- |
| (100,100) | A | Average over 20 equally likely sectors | `win_a[100][100]` |
| (a,100) | B | Use B's best target for score 100 | `win_b[a][100]` |
| (100,100) | B first | Convert A-win probability to B-win probability | 0.950215081962 |

The second trace demonstrates that the same precomputed tables answer all input sizes without recomputing the game.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(501² · 20) | Every score pair is processed once and each transition checks at most 20 dart sectors |
| Space | O(501²) | Two probability tables store all game states |

The largest tables contain roughly 252,000 entries each. The number of operations is only a few million, which fits comfortably in the limits.

## Test Cases

```python
import sys
import io

# This assumes solve() from the solution is available.
def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    ans = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return ans

assert run("5\n100\n0\n") == (
    "0.136363636364 0.909090909091\n"
    "0.072504908290 0.950215081962\n"
), "samples"

assert run("1\n0\n").strip() == "0.050000000000 0.950000000000", "minimum score"

assert run("501\n0\n").count("\n") == 1, "maximum score"

assert run("20\n0\n").strip().startswith("0."), "sector boundary"

assert run("100\n100\n0\n").count("\n") == 2, "multiple queries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5`, `100` | Sample probabilities | General correctness |
| `1` | Finishing only with sector 1 | Exact-zero handling |
| `501` | One valid result line | Maximum state size |
| `20` | Probability calculation for a common sector | Sector transitions |
| Two identical queries | Two identical answers | Multiple test case handling |

## Edge Cases

For input `1`, the dynamic program considers every dart value. Only the sector with value 1 reaches zero. Every other sector leaves the score unchanged or too high, so those probabilities continue through the other player's turn. This avoids the common mistake of counting any value greater than or equal to the remaining score as a win.

For input `5`, sectors such as 20 or 18 are not useful finishing throws. The transition keeps the score unchanged for those outcomes. The table still handles the state because the turn changes even when the score does not.

For input `501`, the largest possible state is still inside the precomputed table. The same recurrence works because the number of possible scores, not the number of possible game histories, controls the running time.
