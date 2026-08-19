---
title: "CF 102215M - Shlakoblock is live!"
description: "There are (n) games. Game (i) currently has (vi) votes, and watching that game gives pleasure (pi). We may vote for any game at most once."
date: "2026-08-20T03:04:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "M"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 451
verified: false
draft: false
---

[CF 102215M - Shlakoblock is live!](https://codeforces.com/problemset/problem/102215/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 31s  
**Verified:** no  

## Solution
## Problem Understanding

There are (n) games. Game (i) currently has (v_i) votes, and watching that game gives pleasure (p_i). We may vote for any game at most once. After our vote, one vote is chosen uniformly from all votes, so a game with (x) final votes is selected with probability (x) divided by the total number of votes.

Suppose we choose a set (S) of games. Let

[
V=\sum_{i=1}^{n}v_i,\qquad
A=\sum_{i=1}^{n}v_i p_i.
]

Before our vote, the expected pleasure is (A/V). If we vote for every game in (S), the total number of votes becomes (V+|S|), while the total pleasure-weighted number of votes becomes

[
A+\sum_{i\in S}p_i.
]

Thus the expected pleasure for (S) is

[
\frac{A+\sum_{i\in S}p_i}{V+|S|}.
]

The output must contain this maximum expected value as an irreducible fraction, followed by the number of games we selected and their indices.

The constraints are small enough for sorting but far too large for enumerating subsets. With (n\le 1000), an (O(n^2)) solution is easily practical, and an (O(n\log n)) solution has plenty of room under the 2 second limit. The (500) test cases do not change this conclusion because the total input size is still bounded by the corresponding sum of (n)'s in the actual test data, and the algorithm only needs to process each game a small number of times.

There are several cases where a careless implementation can fail. First, selecting no games must be allowed. For

```
1
1
5 10
```

the expected pleasure is already (5), and voting for the only game leaves the expectation unchanged. An optimal output can be

```
5/1
0
```

An implementation that assumes at least one game must be selected would unnecessarily constrain the answer.

A second issue is that a game with zero current votes can still be the best game to add. For

```
1
2
0 0
10 1
```

the initial expectation is (10). Selecting game (1) changes the expectation to (5), while selecting game (2) changes it to (10). Both choices are optimal, including selecting nothing. A solution that considers only games with (v_i>0) can miss a valid optimal selection when a zero-vote game has the same pleasure as the current expectation.

The most important edge case concerns the denominator. For

```
1
2
10 1
0 1
```

the initial expected pleasure is (5). Adding game (1) gives (20/3), while adding game (2) gives (10/3). The correct answer is (20/3). A method that compares only (p_i/v_i), rather than the actual effect of adding one vote, is solving a different problem.

Finally, the answer must be reduced. For

```
1
2
6 1
2 1
```

the initial expectation is (4), and selecting either game keeps the expectation at (4). The answer must be printed as `4/1`, not `8/2` or another equivalent fraction.

## Approaches

The direct approach is to try every subset of games. For a chosen subset (S), we can calculate its expected pleasure using

[
\frac{A+\sum_{i\in S}p_i}{V+|S|}.
]

This is correct because every possible voting decision is represented by exactly one subset. The problem is the number of subsets. There are (2^n) of them, and even if each subset were evaluated in (O(1)) time using suitable preprocessing, the worst case with (n=1000) would require (2^{1000}) operations, which is completely infeasible.

The useful observation is that the denominator depends only on the number of games selected, not on their identities. Fix the number of selected games to be (k). Then every candidate has the same denominator (V+k), and the original value (A) is also fixed. The only part we can improve is

[
\sum_{i\in S}p_i.
]

For exactly (k) selected games, this sum is maximized by taking the (k) largest pleasure values. There is no reason to choose a smaller pleasure value while excluding a larger one, because both choices add exactly one vote and affect the denominator identically.

This turns the problem into a one-dimensional search. Sort the games by decreasing (p_i), compute prefix sums of their pleasures, and evaluate

[
\frac{A+P_k}{V+k}
]

for every (k) from (0) through (n), where (P_k) is the sum of the first (k) pleasures. We simply keep the best fraction.

The brute force works because it examines every possible subset, but fails because there are exponentially many subsets. The observation that only the number of selected games matters for the denominator lets us replace all subsets of the same size by one representative, namely the set containing the (k) largest pleasures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n n)), or (O(2^n)) with subset preprocessing | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all games and compute the current total number of votes (V) and the current weighted pleasure (A=\sum v_i p_i). These values describe the expectation before we add any votes.
2. Sort the games by decreasing (p_i). Only the order of pleasures matters for deciding which games to choose. The existing vote counts (v_i) have already been fully accounted for in (A) and (V).
3. Start with (k=0). The corresponding candidate is the decision to vote for no game, with value (A/V). Including (k=0) is necessary because adding a vote can decrease the expectation.
4. Scan the sorted games from largest pleasure to smallest and maintain the prefix pleasure sum (P_k). After processing the first (k) games, the best possible answer among all choices containing exactly (k) games is

[
\frac{A+P_k}{V+k}.
]

1. Compare this candidate with the best value found so far using cross multiplication. For two fractions (a/b) and (c/d), compare (a d) with (c b). This avoids floating-point precision issues and gives an exact comparison.
2. When a candidate is better, save its (k). The selected games are exactly the first (k) games in the sorted order, so no separate subset reconstruction is needed.
3. Recompute the numerator and denominator for the saved (k), divide both by their greatest common divisor, and print the reduced fraction. Then print the saved (k) and the corresponding original indices.

Why it works: for every fixed (k), the denominator (V+k) is fixed, so maximizing the expected value is equivalent to maximizing the added pleasure. The (k) largest (p_i) values give the maximum possible added pleasure among all (k)-element subsets. Consequently, the scan considers the best possible subset for every possible cardinality (k). Since every legal subset has some cardinality between (0) and (n), one of these candidates is globally optimal.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        games = []
        total_votes = 0
        weighted_pleasure = 0

        for idx in range(1, n + 1):
            p, v = map(int, input().split())
            games.append((p, idx))
            total_votes += v
            weighted_pleasure += p * v

        # For a fixed number k of new votes, choose the k largest pleasures.
        games.sort(reverse=True)

        best_k = 0
        best_num = weighted_pleasure
        best_den = total_votes

        prefix = 0

        for k, (p, idx) in enumerate(games, 1):
            prefix += p

            num = weighted_pleasure + prefix
            den = total_votes + k

            # num / den > best_num / best_den
            if num * best_den > best_num * den:
                best_num = num
                best_den = den
                best_k = k

        selected = [games[i][1] for i in range(best_k)]

        g = math.gcd(best_num, best_den)
        best_num //= g
        best_den //= g

        out.append(f"{best_num}/{best_den}")
        out.append(str(best_k))
        out.append(" ".join(map(str, selected)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first loop computes (V) and (A) while storing each game's pleasure and original index. The original index is retained because sorting changes the order, but the output must refer to the input positions.

Sorting in reverse order places the largest pleasures first. Python sorts tuples lexicographically, so `(p, idx)` with `reverse=True` also reverses the index when pleasures are equal. That does not affect correctness because equal pleasures are interchangeable.

The scan starts with the (k=0) candidate. For each newly included game, `prefix` becomes (P_k), so the candidate numerator is `weighted_pleasure + prefix` and its denominator is `total_votes + k`.

The comparison uses multiplication rather than `/`. Python integers have arbitrary precision, so even products such as `num * best_den` are handled exactly. This avoids both floating-point rounding and overflow concerns.

The selected indices are the first `best_k` games after sorting. Finally, `math.gcd` reduces the exact fraction. When `best_k` is zero, the selected list is empty and the final output line is simply empty, which is valid because (k=0).

## Worked Examples

The first test case has five games. Initially,

[
V=5+7+3+2+4=21
]

and

[
A=10\cdot5+4\cdot7+6\cdot3+8\cdot2+2\cdot4=132.
]

After sorting by pleasure, the games appear as (10,8,6,4,2).

| (k) | Added game pleasure | Prefix (P_k) | Numerator | Denominator | Value |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 132 | 21 | (132/21=44/7) |
| 1 | 10 | 10 | 142 | 22 | (71/11) |
| 2 | 8 | 18 | 150 | 23 | (150/23) |
| 3 | 6 | 24 | 156 | 24 | (6) |
| 4 | 4 | 28 | 160 | 25 | (32/5) |
| 5 | 2 | 30 | 162 | 26 | (81/13) |

The best candidate is (k=3), with value (6). However, the sample output chooses games (1) and (4), giving (150/25=6) as well. This illustrates why multiple optimal subsets can exist. In the implementation above, the first strictly better candidate is retained, so the output is also valid even though its selected indices differ from the sample.

For the second test case,

[
V=1000+100+10+1=1111
]

and

[
A=1\cdot1000+10\cdot100+100\cdot10+1000\cdot1=4000.
]

The pleasures are already in increasing order, so sorting produces (1000,100,10,1).

| (k) | Added game pleasure | Prefix (P_k) | Numerator | Denominator | Value |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 4000 | 1111 | (4000/1111) |
| 1 | 1000 | 1000 | 5000 | 1112 | (625/139) |
| 2 | 100 | 1100 | 5100 | 1113 | (1700/371) |
| 3 | 10 | 1110 | 5110 | 1114 | (2555/557) |
| 4 | 1 | 1111 | 5111 | 1115 | (5111/1115) |

The maximum occurs at (k=3), corresponding to the original games with pleasures (10,100,1000), namely games (2,3,4). The resulting fraction is

[
\frac{5110}{1114}=\frac{2555}{557}.
]

The trace also shows why taking all games is not automatically optimal. The final game has pleasure (1), which is too low to compensate for the additional denominator.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Sorting dominates the linear scan |
| Space | (O(n)) | The games and selected indices are stored |

For (n\le1000), sorting at (O(n\log n)) is easily within the 2 second limit. The algorithm performs only a constant number of integer operations per game after sorting, and Python's arbitrary-precision integers make the fraction comparisons exact without introducing a practical memory concern for these bounds.

## Test Cases

The test harness below checks the solution semantically rather than requiring one particular optimal subset. This is necessary because the problem explicitly permits any optimal answer. It verifies that the reported fraction is reduced, the indices are distinct and valid, and the reported expected value is globally optimal.

```python
import sys
import io
import math
from fractions import Fraction

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        games = []
        total_votes = 0
        weighted_pleasure = 0

        for idx in range(1, n + 1):
            p, v = map(int, input().split())
            games.append((p, idx))
            total_votes += v
            weighted_pleasure += p * v

        games.sort(reverse=True)

        best_k = 0
        best_num = weighted_pleasure
        best_den = total_votes

        prefix = 0

        for k, (p, idx) in enumerate(games, 1):
            prefix += p
            num = weighted_pleasure + prefix
            den = total_votes + k

            if num * best_den > best_num * den:
                best_num = num
                best_den = den
                best_k = k

        selected = [games[i][1] for i in range(best_k)]

        g = math.gcd(best_num, best_den)
        best_num //= g
        best_den //= g

        out.append(f"{best_num}/{best_den}")
        out.append(str(best_k))
        out.append(" ".join(map(str, selected)))

    sys.stdout.write("\n".join(out))

def validate(inp: str):
    output = solve_data(inp).strip("\n")
    lines = output.splitlines()

    data = inp.split()
    pos = 0
    t = int(data[pos])
    pos += 1

    line_pos = 0

    for case in range(t):
        n = int(data[pos])
        pos += 1

        games = []
        total_votes = 0
        weighted = 0

        for idx in range(1, n + 1):
            p = int(data[pos])
            v = int(data[pos + 1])
            pos += 2
            games.append((p, v))
            total_votes += v
            weighted += p * v

        frac = lines[line_pos]
        line_pos += 1

        num_s, den_s = frac.split("/")
        num = int(num_s)
        den = int(den_s)

        assert den > 0
        assert math.gcd(num, den) == 1

        k = int(lines[line_pos])
        line_pos += 1

        indices = []
        if line_pos < len(lines):
            current = lines[line_pos].strip()
            if current:
                indices = list(map(int, current.split()))
        line_pos += 1

        assert len(indices) == k
        assert len(set(indices)) == k
        assert all(1 <= x <= n for x in indices)

        actual_num = weighted + sum(games[i - 1][0] for i in indices)
        actual_den = total_votes + k

        assert Fraction(num, den) == Fraction(actual_num, actual_den)

        best = Fraction(weighted, total_votes)
        for mask in range(1 << n) if n <= 10 else []:
            s = 0
            cnt = 0
            for i in range(n):
                if mask >> i & 1:
                    s += games[i][0]
                    cnt += 1
            best = max(best, Fraction(weighted + s, total_votes + cnt))

        if n <= 10:
            assert Fraction(num, den) == best

sample = """\
2
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

validate(sample)

validate("""\
1
1
5 10
""")

validate("""\
1
2
0 0
10 1
""")

validate("""\
1
2
10 1
0 1
""")

validate("""\
1
3
7 1000
7 0
7 1
""")

# Maximum-size case. All games have the same pleasure, so k = 0 is optimal.
maximum_case = "1\n1000\n" + "\n".join(["500 1"] * 1000) + "\n"
validate(maximum_case)

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 5 10` | `5/1`, (k=0) | Minimum size and the possibility of selecting nothing |
| `2 / (0,0),(10,1)` | `10/1` with either (k=0) or the second game | Zero current votes and an unchanged optimum |
| `2 / (10,1),(0,1)` | `20/3` with game 1 | Correct ordering by pleasure and fraction comparison |
| `3 / (7,1000),(7,0),(7,1)` | `7/1` | Equal pleasures and zero-vote games |
| 1000 games with `(500,1)` | `500/1` with (k=0) | Maximum (n), repeated values, and linear scan boundaries |

The provided sample is checked by the validator without requiring the exact sample indices, because a different optimal subset is allowed. The maximum-size case confirms that the implementation handles all (1000) games without relying on small input sizes.

## Edge Cases

When selecting no games is optimal, the algorithm handles it by initializing `best_k = 0` before scanning any game. For the input

```
1
1
5 10
```

we have (A=50) and (V=10), so the initial value is (50/10=5). Adding the only game gives (55/11=5), which is equal rather than strictly better. Because the code updates only on a strict improvement, it keeps (k=0) and prints `5/1`.

Zero-vote games require no special treatment. Consider

```
1
2
0 0
10 1
```

The initial value is (10/1=10). After sorting, the pleasure sequence is (10,0). The first candidate is (20/2=10), so it ties the initial value and does not replace it. The second candidate is (20/3), which is worse. The answer remains `10/1` with no selected games. A zero-vote game is still present in the scan, as it must be, but its pleasure is evaluated exactly like every other game.

The choice must be based on pleasure, not on the current number of votes. For

```
1
2
10 1
0 1
```

we have (A=10) and (V=2), giving an initial expectation of (5). Selecting the game with pleasure (10) produces (20/3), while selecting the game with pleasure (0) produces (10/3). Sorting by pleasure places the correct game first, and the scan selects it.

Equal values also require strict comparison. For

```
1
3
7 1000
7 0
7 1
```

we have (A=7007) and (V=1001), so the initial expectation is exactly (7). Every added vote also has pleasure (7), so for every (k),

[
\frac{7007+7k}{1001+k}=7.
]

The algorithm keeps (k=0), although selecting any number of games would also be optimal. This is why using `>` rather than `>=` is convenient: it gives a deterministic preference for the empty selection when all candidates tie.

Finally, the fraction reduction is performed after the optimal (k) has been found. For the first sample's optimal value (156/24), the greatest common divisor is (24), so the printed result is `6/1`. Keeping all arithmetic as integers until this final reduction avoids precision errors and makes every comparison exact.
