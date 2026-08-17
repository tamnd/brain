---
title: "CF 102215M - Shlakoblock is live!"
description: "There are (n) games. Before we vote, game (i) already has (vi) votes, and watching that game gives us pleasure (pi). We may add at most one vote to each game, so our choice is simply a subset of game indices. After we vote, one vote is chosen uniformly at random from all votes."
date: "2026-08-17T23:56:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "M"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 172
verified: false
draft: false
---

[CF 102215M - Shlakoblock is live!](https://codeforces.com/problemset/problem/102215/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 52s  
**Verified:** no  

## Solution
## Problem Understanding

There are (n) games. Before we vote, game (i) already has (v_i) votes, and watching that game gives us pleasure (p_i). We may add at most one vote to each game, so our choice is simply a subset of game indices.

After we vote, one vote is chosen uniformly at random from all votes. If game (i) ends with (v_i+1) votes, when we voted for it, its contribution to the expected pleasure is (p_i(v_i+1)). If we did not vote for it, its contribution is (p_i v_i).

Let

[
V=\sum_i v_i
]

be the number of existing votes and

[
P=\sum_i p_i v_i
]

be the total pleasure weighted by those votes. If we choose a subset (S) containing (k) games, the final number of votes is (V+k), while the total weighted pleasure becomes

[
P+\sum_{i\in S}p_i.
]

Thus the expected pleasure is

[
\frac{P+\sum_{i\in S}p_i}{V+|S|}.
]

The task is to choose (S) maximizing this fraction, then output the fraction in irreducible form and the selected game indices.

The constraints give (n\le 1000), so an (O(n^2)) solution is easily reasonable, and an (O(n\log n)) solution is comfortably within the two second limit. On the other hand, enumerating all subsets already gives (2^{1000}) possibilities, which is completely infeasible. The fact that there can be up to 500 test cases makes exponential approaches even less viable.

There are several cases where a careless implementation can fail. First, choosing no games must be allowed. For example,

```
1
1
0 5
```

already has expected pleasure (0), and voting for the game does not improve it. An optimal answer is

```
0/1
0
```

An implementation that always chooses at least one game would still obtain the same numerical value here, but it could violate its own assumptions about the selected set or produce unnecessary votes.

A more significant edge case is a game with no existing votes. Consider

```
1
2
100 0
0 1
```

Without our vote, the expected pleasure is (0). Voting for game 1 gives two total votes and expected pleasure (100/2=50), so game 1 must be selected. The existing value (p_i v_i) is zero for game 1, but our additional vote contributes (p_i). Forgetting that extra contribution is a common source of incorrect formulas.

Ties in pleasure are another boundary case. For

```
1
3
5 10
5 20
5 30
```

every possible expected pleasure is (5), including selecting no games. Any subset is valid, so the algorithm must not depend on a unique optimal subset. A deterministic tie-breaking rule is useful for testing, but is not required by the problem.

Finally, the answer is a fraction, not necessarily an integer. In the second sample, the optimum is (5110/1114), which reduces to (2555/557). Printing the unreduced fraction would violate the output requirement even though its numerical value is correct.

## Approaches

The direct approach is to enumerate every subset of the (n) games. For each subset, we can calculate its size, add the pleasures of its selected games to (P), divide by (V+|S|), and retain the best fraction. This is correct because every legal voting strategy is exactly one subset, so enumeration considers every possible strategy.

However, there are (2^n) subsets. If we calculate the numerator by scanning all (n) games for every subset, the worst-case work is (O(n2^n)). Even with a more careful subset dynamic program that evaluates each subset in (O(1)) additional time, there are still (2^n) states. At (n=1000), this is far beyond what any implementation can handle.

The useful observation is that the denominator depends only on how many games we choose, not on which games we choose. Suppose we decide in advance to vote for exactly (k) games. Then the denominator is fixed at (V+k), and (P) is also fixed. The only part we can optimize is

[
\sum_{i\in S}p_i.
]

For exactly (k) selected games, this sum is maximized by taking the (k) largest values of (p_i). The existing vote counts (v_i) no longer influence which games should be selected once (k) is fixed. They influence the fixed baseline (P) and (V), but every candidate with the same (k) has the same denominator and the same baseline.

This reduces the entire problem to sorting the games by (p_i), then considering every prefix of that sorted order. For prefix length (k), we know the best possible numerator among all subsets of size (k). We simply compare those (n+1) candidates using exact integer arithmetic.

The brute-force method works because each subset represents one possible voting strategy, but fails because there are exponentially many subsets. The observation that all strategies with the same number of added votes share the same denominator lets us replace all subsets of size (k) by a single best representative, the (k) largest pleasures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Compute (V=\sum v_i) and (P=\sum p_i v_i). These are the total number of existing votes and the total pleasure contributed by those votes. Since every strategy starts from the same existing poll, these quantities form a common baseline for every candidate.
2. Sort all games in decreasing order of (p_i). Keep their original indices along with their pleasure values. The order lets us represent the best subset of every possible size by a prefix.
3. Start with (k=0). Its candidate value is (P/V), because we do not add any votes. This case must be considered because adding a vote can decrease the expected pleasure.
4. Traverse the sorted games from largest pleasure to smallest. When the next game is added, increase the additional pleasure by its (p_i), and increase the number of votes by one. For a prefix of length (k), the candidate fraction is

[
\frac{P+\text{prefixPleasure}}{V+k}.
]

The prefix is optimal among all subsets containing exactly (k) games because it contains the (k) largest pleasure values.

1. Compare the current candidate with the best fraction found so far by cross multiplication. For fractions (a/b) and (c/d), compare (ad) and (cb). This avoids floating-point precision errors and gives an exact ordering.
2. Store the prefix length and indices whenever the new candidate is strictly better. Keeping the first optimum when values are equal is valid because the problem accepts any optimal subset.
3. After finding the best prefix, reduce its numerator and denominator by their greatest common divisor. Output the reduced fraction, the number of selected games, and their original indices.

Why it works: for every possible number (k) of votes we could add, the denominator (V+k) is fixed. The existing contribution (P) is also fixed. Consequently, among all subsets of size (k), maximizing expected pleasure is exactly the same as maximizing the sum of their (p_i) values. The (k) largest (p_i) values achieve that maximum, so the sorted prefix gives the best strategy for every possible (k). Since the algorithm checks every (k) from (0) through (n), it checks the best strategy in every possible size class and consequently finds a globally optimal strategy.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        games = []
        total_votes = 0
        base_pleasure = 0

        for i in range(n):
            p, v = map(int, input().split())
            games.append((p, i + 1))
            total_votes += v
            base_pleasure += p * v

        games.sort(key=lambda x: (-x[0], x[1]))

        best_num = base_pleasure
        best_den = total_votes
        best_k = 0
        best_indices = []

        prefix = 0

        for k, (p, idx) in enumerate(games, 1):
            prefix += p

            cur_num = base_pleasure + prefix
            cur_den = total_votes + k

            if cur_num * best_den > best_num * cur_den:
                best_num = cur_num
                best_den = cur_den
                best_k = k
                best_indices = [games[j][1] for j in range(k)]

        g = gcd(best_num, best_den)
        best_num //= g
        best_den //= g

        out.append(f"{best_num}/{best_den}")
        out.append(str(best_k))
        out.append(" ".join(map(str, best_indices)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop stores each game as its pleasure together with its original one-based index. At the same time it computes the two common baseline quantities, `total_votes` and `base_pleasure`, so they do not need to be recomputed for every candidate.

The sort uses decreasing pleasure. The secondary sort by original index is not mathematically necessary, but it makes the program deterministic when several games have the same pleasure. Since equal pleasures are interchangeable for the objective, any ordering among them is valid.

The initial candidate is the empty prefix. Its denominator is `total_votes`, which is guaranteed to be positive by the input condition, so there is no division-by-zero case.

During the scan, `prefix` contains the sum of the pleasures of the first `k` games. The current numerator is `base_pleasure + prefix`, while the denominator is `total_votes + k`. The comparison uses multiplication rather than `/`, so all decisions are exact. Python integers also grow automatically, so the cross products do not overflow.

The list of selected indices is reconstructed from the first `k` sorted games whenever a strictly better candidate is found. This is (O(n)) per improvement in the literal implementation, which could make the scan (O(n^2)) in the worst case. That is still easily acceptable for (n\le1000). If desired, the implementation can store only `best_k` during the scan and reconstruct the prefix once at the end, giving a strict (O(n\log n)) implementation.

Here is that slightly cleaner version, which avoids repeated list construction:

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        games = []
        total_votes = 0
        base_pleasure = 0

        for i in range(1, n + 1):
            p, v = map(int, input().split())
            games.append((p, i))
            total_votes += v
            base_pleasure += p * v

        games.sort(key=lambda x: (-x[0], x[1]))

        best_num = base_pleasure
        best_den = total_votes
        best_k = 0

        prefix = 0

        for k, (p, _) in enumerate(games, 1):
            prefix += p
            cur_num = base_pleasure + prefix
            cur_den = total_votes + k

            if cur_num * best_den > best_num * cur_den:
                best_num = cur_num
                best_den = cur_den
                best_k = k

        g = gcd(best_num, best_den)
        best_num //= g
        best_den //= g

        answer_indices = [idx for _, idx in games[:best_k]]

        out.append(f"{best_num}/{best_den}")
        out.append(str(best_k))
        out.append(" ".join(map(str, answer_indices)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The second version is the one to submit. Its only meaningful difference is that it remembers the optimal prefix length instead of copying the selected indices during every improvement. The final slicing operation constructs the required answer exactly once.

## Worked Examples

For the first test case, the existing weighted pleasure is

[
10\cdot5+4\cdot7+6\cdot3+8\cdot2+2\cdot4=120,
]

and there are (21) existing votes. Sorting by pleasure gives games (1,4,3,2,5).

| (k) | Selected prefix | Added pleasure | Numerator | Denominator | Expected pleasure |
| --- | --- | --- | --- | --- | --- |
| 0 | none | 0 | 120 | 21 | (120/21) |
| 1 | 1 | 10 | 130 | 22 | (130/22) |
| 2 | 1, 4 | 18 | 138 | 23 | (138/23=6) |
| 3 | 1, 4, 3 | 24 | 144 | 24 | (6) |
| 4 | 1, 4, 3, 2 | 28 | 148 | 25 | (148/25) |
| 5 | 1, 4, 3, 2, 5 | 30 | 150 | 26 | (150/26) |

The best value is (6), achieved with (k=2) by games 1 and 4. Selecting game 3 as well keeps the expected pleasure at (6), so the algorithm is allowed to retain the first strictly better candidate, namely games 1 and 4.

For the second test case, every existing game contributes (1000) to the weighted pleasure, so the baseline is (4000/1111). The games are already ordered by pleasure after sorting as (4,3,2,1).

| (k) | Selected prefix | Added pleasure | Numerator | Denominator | Comparison |
| --- | --- | --- | --- | --- | --- |
| 0 | none | 0 | 4000 | 1111 | baseline |
| 1 | 4 | 1000 | 5000 | 1112 | improves |
| 2 | 4, 3 | 1100 | 5100 | 1113 | improves |
| 3 | 4, 3, 2 | 1110 | 5110 | 1114 | improves |
| 4 | 4, 3, 2, 1 | 1111 | 5111 | 1115 | decreases |

The optimum is (5110/1114), which has greatest common divisor (2), giving the required output fraction (2555/557). The selected games are 4, 3, and 2, exactly the three games with the largest pleasure values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Sorting dominates the linear scan through the games. |
| Space | (O(n)) | The game array and output indices require linear memory. |

With (n\le1000), sorting at most 1000 pairs per test case is small, and the linear scan performs only a few thousand integer operations per case. Even with up to 500 test cases, the total input size is the relevant limiting factor, and the algorithm stays comfortably inside the 2 second and 256 MB limits.

## Test Cases

Because the problem allows multiple optimal subsets, a robust test harness should verify the mathematical validity of the produced answer rather than require one particular valid subset. The following test code calls the same solution logic and checks that the reported fraction is optimal, the selected indices are distinct and valid, and the reported fraction matches the selected set.

```python
import sys
import io
from math import gcd

def solve_data(inp: str) -> str:
    data = io.StringIO(inp)
    t = int(data.readline())
    out = []

    for _ in range(t):
        n = int(data.readline())

        games = []
        total_votes = 0
        base_pleasure = 0

        for i in range(1, n + 1):
            p, v = map(int, data.readline().split())
            games.append((p, i))
            total_votes += v
            base_pleasure += p * v

        games.sort(key=lambda x: (-x[0], x[1]))

        best_num = base_pleasure
        best_den = total_votes
        best_k = 0
        prefix = 0

        for k, (p, _) in enumerate(games, 1):
            prefix += p
            cur_num = base_pleasure + prefix
            cur_den = total_votes + k

            if cur_num * best_den > best_num * cur_den:
                best_num = cur_num
                best_den = cur_den
                best_k = k

        g = gcd(best_num, best_den)
        best_num //= g
        best_den //= g

        indices = [idx for _, idx in games[:best_k]]

        out.append(f"{best_num}/{best_den}")
        out.append(str(best_k))
        out.append(" ".join(map(str, indices)))

    return "\n".join(out)

def run(inp: str) -> str:
    return solve_data(inp)

def check(inp: str, out: str):
    in_lines = inp.strip().splitlines()
    pos = 0
    t = int(in_lines[pos])
    pos += 1

    out_lines = out.splitlines()
    out_pos = 0

    for _ in range(t):
        n = int(in_lines[pos])
        pos += 1

        games = []
        total_votes = 0
        base = 0

        for i in range(1, n + 1):
            p, v = map(int, in_lines[pos].split())
            pos += 1
            games.append((p, v))
            total_votes += v
            base += p * v

        num, den = map(int, out_lines[out_pos].split("/"))
        out_pos += 1

        k = int(out_lines[out_pos])
        out_pos += 1

        indices = []
        if k > 0:
            indices = list(map(int, out_lines[out_pos].split()))
        out_pos += 1

        assert len(indices) == k
        assert len(set(indices)) == k
        assert all(1 <= x <= n for x in indices)

        actual_num = base + sum(games[i - 1][0] for i in indices)
        actual_den = total_votes + k

        assert num * actual_den == actual_num * den
        assert gcd(num, den) == 1

        best_num = base
        best_den = total_votes

        for mask_k in range(n + 1):
            if mask_k == 0:
                cur_num = base
            else:
                values = sorted((p for p, _ in games), reverse=True)
                cur_num = base + sum(values[:mask_k])

            cur_den = total_votes + mask_k

            if cur_num * best_den > best_num * cur_den:
                best_num = cur_num
                best_den = cur_den

        assert num * best_den == best_num * den

# Provided sample.
sample = """2
5
10 5
4 7
6 3
8 2
2 4
4
1 1000
10 100
100 10
1000 1
"""

check(sample, run(sample))

# Minimum-size input.
case_min = """1
1
0 1
"""
assert run(case_min) == "0/1\n0\n"

# All pleasures equal. The deterministic implementation keeps k = 0.
case_equal = """1
3
5 10
5 20
5 30
"""
assert run(case_equal) == "5/1\n0\n"

# A zero-vote high-value game must be considered.
case_zero_votes = """1
2
100 0
0 1
"""
assert run(case_zero_votes) == "50/1\n1\n1"

# Boundary case where adding a lower-pleasure game makes the result worse.
case_off_by_one = """1
3
10 1
9 1
0 100
"""
assert run(case_off_by_one) == "19/102\n2\n1 2"

# Maximum-size input. All games have equal pleasure, so k = 0 is optimal.
max_case_lines = ["1", "1000"]
max_case_lines.extend(["1000 1000"] * 1000)
case_max = "\n".join(max_case_lines) + "\n"

max_out = run(case_max)
max_lines = max_out.splitlines()
assert max_lines[1] == "0"
assert max_lines[2] == ""
assert max_lines[0] == "1000/1"
```

The sample checker deliberately does not compare the output text against one fixed answer, because the problem explicitly allows any optimal subset. The small deterministic tests do use exact output, since the submitted implementation has a deterministic tie-breaking order.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 0 1` | `0/1`, `0`, empty index line | Minimum size and the possibility of selecting nothing |
| `3 / (5,10), (5,20), (5,30)` | `5/1`, `0`, empty index line | All equal pleasures and ties |
| `2 / (100,0), (0,1)` | `50/1`, `1`, game `1` | A game with zero existing votes can still be the best choice |
| `3 / (10,1), (9,1), (0,100)` | `19/102`, `2`, games `1 2` | Correct prefix boundary and recognizing that adding another game can hurt |
| 1000 copies of `(1000,1000)` | `1000/1`, `0`, empty index line | Maximum (n), large totals, and equal-value ties |

## Edge Cases

When (n=1), there are only two possible strategies. For the input

```
1
1
0 1
```

the baseline is (0/1). Selecting the only game adds another vote with pleasure zero, so the value remains zero. The scan starts with (k=0), sees that the (k=1) candidate is not strictly better, and keeps the empty set. The output is

```
0/1
0
```

A game with zero existing votes is handled naturally because its contribution to `base_pleasure` is zero, while selecting it adds its full pleasure to the numerator. For

```
1
2
100 0
0 1
```

the baseline is (0/1). After sorting, game 1 comes first. Selecting it produces (100/2=50), while selecting both gives (100/3). The best prefix is thus the first one, producing

```
50/1
1
1
```

When several games have identical pleasure, their order does not affect the objective. For

```
1
3
5 10
5 20
5 30
```

the baseline expectation is already (5), and every added vote also has pleasure (5). Every prefix has expectation (5). Since the implementation only updates on a strict improvement, it keeps (k=0), giving

```
5/1
0
```

This is also why comparing fractions with strict `>` rather than `>=` is useful. Either choice can produce a valid answer here, but strict comparison gives a stable smallest-prefix answer.

The last subtle case is when adding more games eventually becomes harmful. For

```
1
3
10 1
9 1
0 100
```

the baseline is (19/102). After sorting, the pleasures are (10,9,0). Selecting one game gives (29/103), selecting two gives (38/104=19/52), and selecting all three gives (38/105). The third vote contributes nothing to the numerator while increasing the denominator, so the optimum is the prefix of length two:

```
19/52
2
1 2
```

The algorithm checks every prefix rather than assuming that taking more high-pleasure games must always help. That exhaustive scan over the only relevant parameter, the number of selected games, is what preserves optimality while avoiding the exponential number of arbitrary subsets.
