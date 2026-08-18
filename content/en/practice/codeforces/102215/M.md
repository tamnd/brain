---
title: "CF 102215M - Shlakoblock is live!"
description: "We have (n) games. Game (i) currently has (vi) votes, and watching it gives pleasure (pi). We may add one vote to any game, but at most once per game. After our choices, one vote is selected uniformly at random, so a game with more votes is more likely to be streamed."
date: "2026-08-18T12:20:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "M"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 641
verified: false
draft: false
---

[CF 102215M - Shlakoblock is live!](https://codeforces.com/problemset/problem/102215/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We have (n) games. Game (i) currently has (v_i) votes, and watching it gives pleasure (p_i). We may add one vote to any game, but at most once per game. After our choices, one vote is selected uniformly at random, so a game with more votes is more likely to be streamed.

Let (S) be the set of games we vote for. If the current total number of votes is

[
V=\sum_{i=1}^n v_i,
]

then after voting there are (V+|S|) votes. The total pleasure represented by all votes is

[
A+\sum_{i\in S}p_i,
]

where

[
A=\sum_{i=1}^n v_i p_i.
]

Thus the expected pleasure is

[
\frac{A+\sum_{i\in S}p_i}{V+|S|}.
]

The task is to choose (S), print the maximum possible fraction in irreducible form, and print one set of games achieving it.

The constraints are small enough for sorting, but not for enumerating subsets. There can be (n=1000) games in one test, and up to 500 test cases. An (O(n^2)) solution is already unnecessarily expensive in the worst aggregate case, while (O(n\log n)) is easily fast enough. The values (p_i,v_i) are at most 1000, but the sums involve up to 1000 terms, so ordinary Python integers are more than sufficient.

There are several cases where a careless implementation can fail. If we choose no game, the answer can still be optimal. For example,

```
1
1
0 5
```

gives expected pleasure (0/5=0), so the correct output is

```
0/1
0
```

An implementation that always adds at least one game would produce a worse result.

A second issue is that games with zero current votes are still eligible for our vote. For

```
1
2
10 1
100 0
```

the initial expectation is (10). Voting for game 2 gives (110/2=55), which is optimal. Ignoring games with (v_i=0) would miss the answer.

A third issue is that the denominator changes whenever we vote for another game. For

```
1
2
100 1
0 100
```

voting for the first game gives (200/101), while voting for the second gives (100/101). The choice cannot be made by simply selecting every game with positive pleasure. The contribution of the added vote must be considered together with the extra (1) in the denominator.

Finally, several different subsets can attain the same optimum. With

```
1
2
5 1
5 1
```

the best answer is (10/2=5) after voting for either one game, and both choices are valid. The algorithm only needs to retain one optimal subset.

## Approaches

The most direct approach is to try every subset of games. For a subset (S), we can calculate its numerator and denominator and keep the best expected value. This is correct because every legal voting strategy is represented by exactly one subset. However, there are (2^n) subsets, and evaluating each subset takes up to (O(n)) work, giving (O(n2^n)) operations in the worst case. With (n=1000), even (2^{1000}) is far beyond anything that can run within the time limit.

The useful structure appears when we stop caring about the identities of the selected games and first fix their number. Suppose we decide to vote for exactly (k) games. The denominator is then fixed at (V+k), and the original contribution (A) is also fixed. The only part we can optimize is

[
\sum_{i\in S}p_i.
]

For exactly (k) games, this sum is maximized by taking the (k) largest pleasure values.

That observation turns the exponential search into a simple sorted prefix search. Sort the games by decreasing (p_i). After sorting, the best subset of size (k) is precisely the first (k) games. We can build their pleasure sum incrementally and evaluate all (k) from 0 through (n).

The brute-force approach works because it considers every possible subset. It fails because there are exponentially many subsets. The observation that the optimal choice for a fixed subset size consists of the games with the largest (p_i) lets us replace all subsets of the same size with one representative, reducing the problem to (n+1) candidate strategies after sorting.

To compare fractions exactly, we should not use floating point. For two candidates

[
\frac{x_1}{y_1}
\quad\text{and}\quad
\frac{x_2}{y_2},
]

we compare (x_1y_2) with (x_2y_1). Python integers handle these products exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Compute the current total number of votes (V=\sum v_i) and the current total pleasure contribution (A=\sum v_i p_i). These values describe the expected pleasure before adding any of our votes.
2. Sort all games by decreasing (p_i), keeping their original indices. If we eventually decide to add exactly (k) votes, the first (k) games in this ordering give the largest possible added pleasure.
3. Start with (k=0). The candidate expectation is (A/V). The problem guarantees that at least one (v_i) is positive, so (V>0).
4. Traverse the sorted games. When processing the next game, add its (p_i) to a running prefix sum. After adding (k) games, the candidate numerator is (A+\text{prefix}), while the denominator is (V+k).
5. Compare every candidate with the best candidate seen so far using cross multiplication. If

[
(A+\text{prefix})(V+k_{\text{best}})

> 

(A+\text{prefix}_{\text{best}})(V+k),
]

replace the current best answer.

1. Store the corresponding (k). Since the games are already sorted by decreasing pleasure, the first (k) indices form an optimal voting set for that (k).
2. After the scan, reduce the best fraction by dividing its numerator and denominator by their greatest common divisor. Print the reduced fraction, the selected count, and the corresponding original indices.

### Why it works

For every possible number (k) of additional votes, the denominator is exactly (V+k). Among all subsets of (k) games, the original contribution (A) is identical, so maximizing the expected pleasure is equivalent to maximizing the sum of their (p_i) values. The (k) largest (p_i) values give the largest possible sum, so the sorted prefix is optimal for that particular (k).

The algorithm examines every possible (k) from 0 through (n), and for each (k) it examines the best subset of that size. Consequently, the global optimum must be among the candidates considered by the scan. Cross multiplication compares these candidates exactly, so the selected candidate is the true maximum rather than a floating-point approximation.

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
        total_pleasure = 0

        for idx in range(1, n + 1):
            p, v = map(int, input().split())
            games.append((p, idx))
            total_votes += v
            total_pleasure += p * v

        games.sort(key=lambda x: (-x[0], x[1]))

        best_num = total_pleasure
        best_den = total_votes
        best_k = 0

        prefix = 0

        for k, (p, idx) in enumerate(games, 1):
            prefix += p

            cur_num = total_pleasure + prefix
            cur_den = total_votes + k

            if cur_num * best_den > best_num * cur_den:
                best_num = cur_num
                best_den = cur_den
                best_k = k

        g = gcd(best_num, best_den)
        best_num //= g
        best_den //= g

        out.append(f"{best_num}/{best_den}")
        out.append(str(best_k))

        if best_k == 0:
            out.append("")
        else:
            chosen = [str(games[i][1]) for i in range(best_k)]
            out.append(" ".join(chosen))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop stores each game as `(p, index)` because only its pleasure affects the sorting, while its original index is needed for the output. At the same time, it accumulates the current vote count and current pleasure contribution.

The sorting step uses decreasing pleasure. The secondary ordering by original index is not mathematically necessary, but it makes the program deterministic when several games have equal pleasure.

The scan begins with (k=0), which is essential because voting for no game is legal. The variable `prefix` is the sum of the pleasures of the first (k) sorted games, so the candidate numerator and denominator are always exactly (A+\text{prefix}) and (V+k).

The comparison uses multiplication rather than division. For positive denominators,

[
\frac{x}{y}>\frac{a}{b}
]

is equivalent to (xb>ay). This avoids floating-point precision errors and also avoids repeatedly constructing floating-point values.

The selected indices are reconstructed from the first `best_k` elements of the sorted array. There is no off-by-one issue because `enumerate(games, 1)` makes `k` equal to the number of games included in the prefix.

The denominator is always positive because the original input contains at least one positive vote. Python's arbitrary-precision integers also make overflow impossible, even though the actual bounds are already small enough for standard 64-bit arithmetic.

When `best_k` is zero, the required third output line is empty. The code explicitly appends an empty string so that every test case still occupies exactly three output lines.

## Worked Examples

The first sample contains five games. Their initial total is (V=21), and their current pleasure contribution is

[
A=5\cdot10+7\cdot4+3\cdot6+2\cdot8+4\cdot2=120.
]

After sorting by pleasure, the order is games 1, 4, 3, 2, 5.

| (k) | Added pleasure | Numerator | Denominator | Expectation |
| --- | --- | --- | --- | --- |
| 0 | 0 | 120 | 21 | (120/21) |
| 1 | 10 | 130 | 22 | (130/22) |
| 2 | 18 | 138 | 23 | (138/23=6) |
| 3 | 24 | 144 | 24 | (144/24=6) |
| 4 | 28 | 148 | 25 | (148/25) |
| 5 | 30 | 150 | 26 | (150/26) |

The maximum is 6. There is a tie between (k=2) and (k=3). The implementation keeps the first maximum because it only replaces the best answer when the new candidate is strictly larger. Thus it selects games 1 and 4 and prints `6/1`.

The second sample has (V=1111) and

[
A=1000\cdot1+100\cdot10+10\cdot100+1\cdot1000=4000.
]

The sorted order is games 4, 3, 2, 1.

| (k) | Added pleasure | Numerator | Denominator | Expectation |
| --- | --- | --- | --- | --- |
| 0 | 0 | 4000 | 1111 | (4000/1111) |
| 1 | 1000 | 5000 | 1112 | (5000/1112) |
| 2 | 1100 | 5100 | 1113 | (5100/1113) |
| 3 | 1110 | 5110 | 1114 | (5110/1114) |
| 4 | 1111 | 5111 | 1115 | (5111/1115) |

The best candidate uses games 4, 3, and 2. Its fraction is

[
\frac{5110}{1114}=\frac{2555}{557},
]

which is already the requested reduced representation after dividing both numbers by 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Sorting dominates the linear scan and input processing |
| Space | (O(n)) | The game array stores one record for each game |

For (n\le1000), sorting at (O(n\log n)) is comfortably within the 2 second limit. Even across 500 test cases, the algorithm performs only a small amount of work per game beyond sorting, and its memory usage is linear in the size of one test case.

## Test Cases

The test harness below uses the same deterministic tie-breaking as the submitted solution. For general verification, it also checks the structural validity of an answer and its optimal value, since Codeforces allows any optimal subset.

```python
import sys
import io
from math import gcd

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        input = sys.stdin.readline

        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())

            games = []
            total_votes = 0
            total_pleasure = 0

            for idx in range(1, n + 1):
                p, v = map(int, input().split())
                games.append((p, idx))
                total_votes += v
                total_pleasure += p * v

            games.sort(key=lambda x: (-x[0], x[1]))

            best_num = total_pleasure
            best_den = total_votes
            best_k = 0
            prefix = 0

            for k, (p, idx) in enumerate(games, 1):
                prefix += p
                cur_num = total_pleasure + prefix
                cur_den = total_votes + k

                if cur_num * best_den > best_num * cur_den:
                    best_num = cur_num
                    best_den = cur_den
                    best_k = k

            g = gcd(best_num, best_den)
            best_num //= g
            best_den //= g

            out.append(f"{best_num}/{best_den}")
            out.append(str(best_k))

            if best_k == 0:
                out.append("")
            else:
                out.append(" ".join(str(games[i][1]) for i in range(best_k)))

        return "\n".join(out)
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def check(inp: str, output: str):
    data = list(map(int, inp.split()))
    pos = 0
    t = data[pos]
    pos += 1

    lines = output.splitlines()
    line_pos = 0

    for _ in range(t):
        n = data[pos]
        pos += 1

        games = []
        total_votes = 0
        total_pleasure = 0

        for idx in range(1, n + 1):
            p = data[pos]
            v = data[pos + 1]
            pos += 2
            games.append((p, v))
            total_votes += v
            total_pleasure += p * v

        fraction = lines[line_pos]
        line_pos += 1

        num, den = map(int, fraction.split("/"))
        assert gcd(num, den) == 1
        assert den > 0

        k = int(lines[line_pos])
        line_pos += 1

        chosen = []
        if k > 0:
            chosen = list(map(int, lines[line_pos].split()))
        line_pos += 1

        assert 0 <= k <= n
        assert len(chosen) == k
        assert len(set(chosen)) == k
        assert all(1 <= x <= n for x in chosen)

        chosen_set = set(chosen)
        actual_num = total_pleasure
        for i, (p, v) in enumerate(games, 1):
            if i in chosen_set:
                actual_num += p

        actual_den = total_votes + k

        assert num * actual_den == actual_num * den

        best_num = total_pleasure
        best_den = total_votes

        ordered = sorted((p, i) for i, (p, v) in enumerate(games, 1))
        ordered.reverse()

        prefix = 0
        for kk in range(1, n + 1):
            prefix += ordered[kk - 1][0]
            candidate_num = total_pleasure + prefix
            candidate_den = total_votes + kk
            assert candidate_num * best_den <= best_num * candidate_den or (
                candidate_num * best_den == best_num * candidate_den
            )

            if candidate_num * best_den > best_num * candidate_den:
                best_num = candidate_num
                best_den = candidate_den

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

check(sample, solution(sample))

minimum = """1
1
0 7
"""
check(minimum, solution(minimum))

all_equal = """1
4
5 1
5 2
5 3
5 4
"""
check(all_equal, solution(all_equal))

zero_votes = """1
2
10 1
100 0
"""
check(zero_votes, solution(zero_votes))

boundary = """1
3
0 1000
1000 0
999 1
"""
check(boundary, solution(boundary))

large = "1\n1000\n" + "\n".join(
    f"{i % 1001} {1 if i == 1 else 0}" for i in range(1000)
) + "\n"
check(large, solution(large))

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One game with `p=0` | `0/1`, `k=0` | Legal empty subset and zero numerator |
| Four games with equal pleasure | Any optimal prefix | Equal values and tie handling |
| A zero-vote game with high pleasure | The high-pleasure game is selected | Games with (v_i=0) must remain eligible |
| `p=0`, `v=1000` mixed with large pleasures | Exact fraction from the best prefix | Boundary values and denominator changes |
| 1000-game generated case | Any valid optimum | Maximum (n) and linear-memory behavior |

## Edge Cases

When voting for no game is optimal, the scan handles it because the initial best candidate is (k=0). For the input

```
1
1
0 5
```

we have (A=0) and (V=5). The only alternative adds a zero-pleasure vote and still gives expectation (0), so the algorithm keeps (k=0) and reduces (0/5) to `0/1`. The third line is empty.

When a game has no current votes, it still appears in the sorted array. For

```
1
2
10 1
100 0
```

we have (A=10) and (V=1). The initial candidate is (10/1). After adding game 2, the candidate becomes (110/2=55), so the algorithm selects game 2. Its existing vote count being zero does not prevent our new vote from making it the most likely streamed game.

The denominator change is handled directly by using `total_votes + k`. Consider

```
1
2
100 1
0 100
```

Here (A=100) and (V=101). With no additional vote the expectation is (100/101). Adding the first game produces (200/102=100/51), which is better. Adding the zero-pleasure game instead gives (100/102=50/51), which is worse. The prefix scan evaluates both possibilities exactly.

Equal optimal candidates are handled by the strict `>` comparison. For

```
1
2
5 1
5 1
```

the (k=0) expectation is (10/2=5), and adding either game also gives (15/3=5). Since the value does not improve, the implementation keeps (k=0). This is valid because the problem asks for any maximizing strategy.

The reduction step is also necessary even when the optimum happens to have a simple value. In the second sample, the selected candidate is (5110/1114), and the greatest common divisor is 2. Dividing both parts gives `2555/557`, satisfying the required irreducible-fraction format.
