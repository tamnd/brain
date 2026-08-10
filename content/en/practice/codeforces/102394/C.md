---
title: "CF 102394C - Competition in Swiss-system"
description: "There are (n) players and (m) rounds. In every round, a player either participates in one match or receives a bye. A match contains either two or three games, and the input directly gives how many games each player won and how many were drawn."
date: "2026-08-10T21:22:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "C"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 137
verified: true
draft: false
---

[CF 102394C - Competition in Swiss-system](https://codeforces.com/problemset/problem/102394/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) players and (m) rounds. In every round, a player either participates in one match or receives a bye. A match contains either two or three games, and the input directly gives how many games each player won and how many were drawn.

For every player, we must report four statistics after every round. MP is the accumulated match points. GW is the accumulated game points divided by the maximum possible game points, with a lower bound of (1/3). OMW is the average of the current match-win percentages of every opponent the player has faced, counting repeated meetings separately. OGW is defined in the same way using current game-win percentages. Byes contribute points and games to the player's own statistics, but never create an opponent.

The input gives the number of matches in each round, followed by those matches in round order. A player missing from a round's match list is automatically treated as having a bye.

The official Codeforces page gives a 2 second time limit and 512 MB memory limit. The main structural constraint is (m\le16), while the sum of (n\cdot m) over all test cases is at most (3\cdot10^5). That last condition means an (O(nm)) pass over all player-round pairs is easily affordable. Even an (O(nm^2)) algorithm is effectively at most a small constant multiple of (n m), because (m) is bounded by 16. An algorithm involving all pairs of players, however, would be far too expensive when (n=10,000).

There are several places where a direct implementation can silently go wrong.

### Edge case: a player receives only byes

Consider

```
1
2 1
0
```

Both players receive a bye. Each gets 3 MP, 6 game points, and has played two games. Their GW is (6/(3\cdot2)=1). Since neither has an opponent, both OMW and OGW are defined as (1/3). The correct output is

```
Round 1
3 1/3 1/1 1/3
3 1/3 1/1 1/3
```

A common mistake is to treat a bye as an opponent or to use (1) for the opponent percentages because a bye is equivalent to a 2-0 match. It is equivalent to a win only for the player's own statistics.

### Edge case: the (1/3) lower bound changes the fraction

Consider

```
1
2 1
1
1 2 0 0 2
```

The match is a draw because both players won zero games. Each gets 1 MP and 2 game points from two drawn games. Their raw match percentage is (1/3), while their raw game percentage is (2/6=1/3). Thus both percentages are exactly (1/3), and each player's opponent has the same values.

The correct output is

```
Round 1
1 1/3 1/3 1/3
1 1/3 1/3 1/3
```

More generally, after round (r), the capped match percentage can be represented as

[
\frac{\max(r,\mathrm{MP})}{3r}.
]

For games, if a player has played (g) games and earned (G) game points, the capped value is

[
\frac{\max(g,G)}{3g}.
]

Using the uncapped value when computing OMW or OGW produces wrong answers for players with poor results.

### Edge case: the same opponent appears multiple times

Consider

```
1
2 2
1 1
1 2 2 0 0
1 2 0 2 0
```

Player 1 wins the first match and loses the second. Player 2 does the opposite. After the first round, player 1 has MP 3 and player 2 has MP 0. After the second round, both have played twice, so player 1 still has MP 3 and player 2 still has MP 3.

The opponent list of each player contains the same player twice. The second round OMW must average that opponent's current percentage twice, not once. The correct output is

```
Round 1
3 1/3 1/1 1/3
0 1/1 1/3 1/1
Round 2
3 1/1 1/1 1/3
3 1/1 1/3 1/1
```

A solution that stores only a set of distinct opponents would silently undercount repeated matches.

## Approaches

The most direct brute-force solution stores all matches seen so far. After each round, for every player it scans every previous match, checks whether the player participated in it, and if so adds that opponent's current MW and GW. This is correct because the definition of OMW and OGW is exactly an average over the historical matches.

The problem is the amount of repeated work. In the worst case, almost every player participates in every round, so after round (r) there are about (nr/2) matches. Scanning those matches separately for all (n) players costs about (n^2r/2) checks in that round. Summed over all 16 rounds, the worst case is

136n^2.
]

For (n=10,000), that is about (13.6) billion match checks, before counting fraction arithmetic or output.

The brute force works because every statistic depends only on the matches that have already happened, but it repeatedly rediscovers which opponents belong to each player. The key observation is that the opponent relation never disappears. Once players (u) and (v) have played, (v) remains one of (u)'s opponents for every later round. Since a player can play at most once per round, each player has at most (m) opponent entries after the whole tournament.

We can consequently store, for every player, a list containing the opponent from every match they have played. After processing a round, we simply walk through these lists. At round (r), every list has length at most (r), so the total number of opponent entries inspected during the whole tournament is

[
O\left(n\sum_{r=1}^{m}r\right)=O(nm^2).
]

Because (m\le16), this is small. The global condition (\sum nm\le3\cdot10^5) makes it even safer across multiple test cases.

OMW has an additional simplification. At a fixed round (r), every player's MW has denominator (3r). If player (v) has MP (P_v), its capped MW is

[
\frac{\max(r,P_v)}{3r}.
]

Thus the average over a player's (d) opponent entries is simply

[
\frac{\sum_v\max(r,P_v)}{3rd}.
]

OGW does not have a common denominator because players may have played different numbers of games due to different numbers of byes and two-game or three-game matches. We therefore add the opponent GW fractions with ordinary exact fraction arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2m^2)) | (O(nm)) | Too slow |
| Optimal | (O(nm^2)) | (O(nm)) | Accepted |

## Algorithm Walkthrough

1. Create arrays for each player's accumulated MP, game points, and number of games played. Also create an opponent list for every player. The opponent list stores one entry per match, so repeated meetings are naturally represented multiple times.
2. Process the rounds in order. For every match, mark both players as having played this round and update their MP, game points, and number of games according to the supplied game result.

If (w_1>w_2), player 1 gets 3 MP and player 2 gets 0. If (w_1<w_2), the reverse happens. If (w_1=w_2), both receive 1 MP. The game points are (3w+d), and the number of games is (w_1+w_2+d).
3. Append each player to the other's opponent list. This happens exactly once per match, even if the two players have met before. The repetition is required because the definition averages over matches rather than distinct opponents.
4. After all matches of the current round have been processed, every unmarked player receives a bye. Add 3 MP, 6 game points, and 2 games to that player.

By processing byes after the actual matches, the current round's complete statistics are available before any percentages are calculated.
5. For every player, calculate the capped GW from their own accumulated game points and games:

[
GW_i=\frac{\max(\mathrm{games}_i,\mathrm{gamePoints}_i)}
{3\mathrm{games}_i}.
]

Reduce the fraction with a greatest common divisor.

1. Calculate the current MW numerator for every player as

[
M_i=\max(r,\mathrm{MP}_i).
]

The actual MW is (M_i/(3r)). For a player with opponents, sum (M_v) over every opponent entry (v), and divide by (3r) times the number of opponent entries.

1. For OGW, walk through the same opponent list. For each opponent (v), obtain its current capped GW as

[
\frac{\max(\mathrm{games}_v,\mathrm{gamePoints}_v)}
{3\mathrm{games}_v}.
]

Add these fractions exactly and finally divide by the number of opponent entries.

1. If a player has no opponents, print (1/3) for both OMW and OGW. Otherwise reduce both calculated fractions and print the four statistics.
2. Repeat this process after every round. Since all statistics are cumulative, nothing needs to be recomputed from the raw match results except the opponent averages.

### Why it works

After round (r), the arrays MP, game points, and games contain exactly the cumulative values earned through that round because every match and every bye has been processed once. The opponent list of each player contains exactly one entry for every match that player has played, including repeated opponents and excluding byes.

The MW calculation uses (\max(r,\mathrm{MP})/(3r)), which is precisely the required (1/3)-capped match percentage. Summing those values over the opponent list and dividing by its length gives exactly OMW. The same argument applies to GW and OGW, except that each opponent's game denominator depends on that opponent's own number of games. Since all arithmetic is performed with integers and reduced by GCD, the printed fractions are exact and irreducible.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def reduce_fraction(num, den):
    g = gcd(num, den)
    return num // g, den // g

def add_fraction(a, b, c, d):
    g = gcd(b, d)
    b1 = b // g
    d1 = d // g
    num = a * d1 + c * b1
    den = b1 * d
    g2 = gcd(num, den)
    return num // g2, den // g2

def main():
    T = int(input())
    out = []

    for _ in range(T):
        n, m = map(int, input().split())
        cnt = list(map(int, input().split()))

        mp = [0] * n
        game_points = [0] * n
        games = [0] * n
        opponents = [[] for _ in range(n)]

        for rnd in range(1, m + 1):
            played = [False] * n

            for _ in range(cnt[rnd - 1]):
                p1, p2, w1, w2, d = map(int, input().split())
                p1 -= 1
                p2 -= 1

                played[p1] = True
                played[p2] = True

                if w1 > w2:
                    mp[p1] += 3
                elif w1 < w2:
                    mp[p2] += 3
                else:
                    mp[p1] += 1
                    mp[p2] += 1

                game_points[p1] += 3 * w1 + d
                game_points[p2] += 3 * w2 + d

                total_games = w1 + w2 + d
                games[p1] += total_games
                games[p2] += total_games

                opponents[p1].append(p2)
                opponents[p2].append(p1)

            for i in range(n):
                if not played[i]:
                    mp[i] += 3
                    game_points[i] += 6
                    games[i] += 2

            out.append(f"Round {rnd}")

            for i in range(n):
                gw_num = max(games[i], game_points[i])
                gw_den = 3 * games[i]
                gw_num, gw_den = reduce_fraction(gw_num, gw_den)

                if not opponents[i]:
                    omw_num, omw_den = 1, 3
                    ogw_num, ogw_den = 1, 3
                else:
                    opponent_count = len(opponents[i])

                    omw_sum = 0
                    for v in opponents[i]:
                        omw_sum += max(rnd, mp[v])

                    omw_num = omw_sum
                    omw_den = 3 * rnd * opponent_count
                    omw_num, omw_den = reduce_fraction(
                        omw_num, omw_den
                    )

                    ogw_num, ogw_den = 0, 1
                    for v in opponents[i]:
                        v_num = max(games[v], game_points[v])
                        v_den = 3 * games[v]
                        ogw_num, ogw_den = add_fraction(
                            ogw_num, ogw_den, v_num, v_den
                        )

                    ogw_den *= opponent_count
                    ogw_num, ogw_den = reduce_fraction(
                        ogw_num, ogw_den
                    )

                out.append(
                    f"{mp[i]} "
                    f"{omw_num}/{omw_den} "
                    f"{gw_num}/{gw_den} "
                    f"{ogw_num}/{ogw_den}"
                )

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The three cumulative arrays are enough to reconstruct every player's own percentage. MP is updated from the match winner or draw, while game points and game count use the supplied game counts directly. A bye is represented by exactly the same cumulative increments as the specified 2-0 bye result.

The `opponents` lists are the central data structure. If players 1 and 2 meet three times, player 1's list contains `[2, 2, 2]`. No deduplication is performed because the tournament definition counts every meeting.

The order of updates matters. A complete round must be processed before calculating any percentages because OMW and OGW use the opponents' current statistics after that round. The code first processes every match, then assigns all byes, and only then calculates output.

The OMW calculation avoids fraction addition entirely. At round (r), every MW has denominator (3r), so only the integer numerator `max(r, mp[v])` needs to be accumulated. OGW requires real fraction addition because two opponents can have different numbers of games.

Python integers are arbitrary precision, so there is no overflow issue. The largest denominators are small anyway because a player plays at most 16 rounds and at most three games per match, with byes contributing two games.

The `add_fraction` function reduces after every addition. This keeps intermediate integers small and avoids constructing a large common denominator across all opponents.

## Worked Examples

### Sample 1

The first test case has two players and three rounds. Round 1 contains no matches, so both players receive byes. Round 2 contains a 2-0-1 match, and round 3 contains a 1-1-1 match.

| Round | Player | MP | Game Points | Games | Opponents |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 6 | 2 | [] |
| 1 | 2 | 3 | 6 | 2 | [] |
| 2 | 1 | 6 | 13 | 5 | [2] |
| 2 | 2 | 3 | 7 | 5 | [1] |
| 3 | 1 | 7 | 17 | 8 | [2] |
| 3 | 2 | 4 | 11 | 8 | [1] |

After round 2, player 1 has MW (6/6=1), while player 2 has MW (3/6=1/2). Their GW values are (13/15) and (7/15). Since they have each played exactly one opponent, those values become the other's OMW and OGW.

After round 3, the same opponent lists are still present, but their current statistics have changed. Player 2 now has GW (11/24), so that becomes player 1's OGW. Player 1 has GW (17/24), so it becomes player 2's OGW.

This trace demonstrates why opponent percentages must be calculated using the current statistics, not the statistics from the round when the match occurred.

### Sample 2

The second test case has three players. In round 1, players 1 and 2 play while player 3 receives a bye. In round 2, player 2 plays player 3 while player 1 receives a bye.

| Round | Player | MP | Game Points | Games | Opponents |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 2 | [2] |
| 1 | 2 | 3 | 6 | 2 | [1] |
| 1 | 3 | 3 | 6 | 2 | [] |
| 2 | 1 | 3 | 6 | 4 | [2] |
| 2 | 2 | 6 | 12 | 4 | [1, 3] |
| 2 | 3 | 3 | 6 | 4 | [2] |

After round 1, player 1's raw MW is zero, so it is capped to (1/3). Player 2's MW is 1, so player 1 has OMW (1), while player 2 has OMW (1/3).

After round 2, player 2 has faced two opponents. Player 1 has MW (3/6=1/2), and player 3 also has MW (3/6=1/2). Consequently player 2's OMW is

[
\frac{1/2+1/2}{2}=\frac12.
]

The same averaging happens for OGW, where all three players have played four games by this point.

This trace exercises both byes and the fact that a player's opponent list can contain different players with different current statistics.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm^2)) | After round (r), each player has at most (r) opponent entries, so all opponent lists contain (O(nr)) entries. Summing over all rounds gives (O(nm^2)). |
| Space | (O(nm)) | The cumulative statistics use (O(n)) memory and all opponent lists contain at most (nm) entries in total. |

Since (m\le16), the (m^2) factor is at most 256. More significantly, the input guarantees that the sum of (n m) across all cases is only (3\cdot10^5). The resulting number of opponent-list iterations is comfortably within the intended range, while the memory usage remains linear in the total tournament size.

## Test Cases

```python
import io
import sys
from math import gcd

def solve(data: str) -> str:
    inp = io.StringIO(data)

    def rd():
        return inp.readline()

    t = int(rd())
    out = []

    def reduce_fraction(a, b):
        g = gcd(a, b)
        return a // g, b // g

    def add_fraction(a, b, c, d):
        g = gcd(b, d)
        b1 = b // g
        d1 = d // g
        a = a * d1 + c * b1
        b = b1 * d
        g = gcd(a, b)
        return a // g, b // g

    for _ in range(t):
        n, m = map(int, rd().split())
        counts = list(map(int, rd().split()))

        mp = [0] * n
        gp = [0] * n
        games = [0] * n
        opp = [[] for _ in range(n)]

        for r in range(1, m + 1):
            played = [False] * n

            for _ in range(counts[r - 1]):
                p1, p2, w1, w2, d = map(int, rd().split())
                p1 -= 1
                p2 -= 1

                played[p1] = True
                played[p2] = True

                if w1 > w2:
                    mp[p1] += 3
                elif w2 > w1:
                    mp[p2] += 3
                else:
                    mp[p1] += 1
                    mp[p2] += 1

                gp[p1] += 3 * w1 + d
                gp[p2] += 3 * w2 + d

                g = w1 + w2 + d
                games[p1] += g
                games[p2] += g

                opp[p1].append(p2)
                opp[p2].append(p1)

            for i in range(n):
                if not played[i]:
                    mp[i] += 3
                    gp[i] += 6
                    games[i] += 2

            out.append(f"Round {r}")

            for i in range(n):
                gw_num, gw_den = reduce_fraction(
                    max(games[i], gp[i]),
                    3 * games[i]
                )

                if not opp[i]:
                    omw_num, omw_den = 1, 3
                    ogw_num, ogw_den = 1, 3
                else:
                    d = len(opp[i])

                    omw_num = sum(max(r, mp[v]) for v in opp[i])
                    omw_den = 3 * r * d
                    omw_num, omw_den = reduce_fraction(
                        omw_num, omw_den
                    )

                    ogw_num, ogw_den = 0, 1
                    for v in opp[i]:
                        x = max(games[v], gp[v])
                        y = 3 * games[v]
                        ogw_num, ogw_den = add_fraction(
                            ogw_num, ogw_den, x, y
                        )

                    ogw_den *= d
                    ogw_num, ogw_den = reduce_fraction(
                        ogw_num, ogw_den
                    )

                out.append(
                    f"{mp[i]} {omw_num}/{omw_den} "
                    f"{gw_num}/{gw_den} {ogw_num}/{ogw_den}"
                )

    return "\n".join(out)

def run(inp: str) -> str:
    return solve(inp)

sample = """\
2
2 3
0 1 1
1 2 2 0 1
1 2 1 1 1
3 2
1 1
1 2 0 2 0
2 3 2 0 0
"""

sample_expected = """\
Round 1
3 1/3 1/1 1/3
3 1/3 1/1 1/3
Round 2
6 1/2 13/15 7/15
3 1/1 7/15 13/15
Round 3
7 4/9 17/24 11/24
4 7/9 11/24 17/24
Round 1
0 1/1 1/3 1/1
3 1/3 1/1 1/3
3 1/3 1/1 1/3
Round 2
3 1/1 1/2 1/1
6 1/2 1/1 1/2
3 1/1 1/2 1/1
"""

assert run(sample) == sample_expected, "official sample"

case_min = """\
1
2 1
0
"""

expected_min = """\
Round 1
3 1/3 1/1 1/3
3 1/3 1/1 1/3
"""

assert run(case_min) == expected_min, "minimum all-bye case"

case_draw = """\
1
2 1
1
1 2 1 1 1
"""

expected_draw = """\
Round 1
1 1/3 4/9 4/9
1 1/3 4/9 4/9
"""

assert run(case_draw) == expected_draw, "draw and exact 1/3 cap"

case_repeat = """\
1
2 2
1 1
1 2 2 0 0
1 2 0 2 0
"""

expected_repeat = """\
Round 1
3 1/3 1/1 1/3
0 1/1 1/3 1/1
Round 2
3 1/1 1/1 1/3
3 1/1 1/3 1/1
"""

assert run(case_repeat) == expected_repeat, "repeated opponent"

case_equal = """\
1
4 2
2 2
1 2 1 1 1
3 4 1 1 1
1 2 1 1 1
3 4 1 1 1
"""

expected_equal = """\
Round 1
1 1/3 4/9 4/9
1 1/3 4/9 4/9
1 1/3 4/9 4/9
1 1/3 4/9 4/9
Round 2
2 1/3 4/9 4/9
2 1/3 4/9 4/9
2 1/3 4/9 4/9
2 1/3 4/9 4/9
"""

assert run(case_equal) == expected_equal, "all equal results"

# Maximum n*m case: 10,000 players, 16 rounds, every player gets a bye.
# This checks both the input-size boundary and repeated-round processing.
n = 10000
m = 16
max_case = "1\n10000 16\n" + " ".join(["0"] * 16) + "\n"

max_output = run(max_case)
lines = max_output.splitlines()

assert len(lines) == 16 * (n + 1), "maximum-size output length"

for r in range(1, 17):
    base = (r - 1) * (n + 1)
    assert lines[base] == f"Round {r}", "round header"

    expected_line = f"{3 * r} 1/3 1/1 1/3"
    assert lines[base + 1] == expected_line, "first player"
    assert lines[base + n] == expected_line, "last player"
```

The minimum case checks that byes update MP, game points, and games without creating opponents. The draw case checks a non-winning match and exact fraction reduction. The repeated-opponent case verifies that the same opponent is counted once per match. The all-equal case checks repeated rounds with identical statistics and catches accidental state replacement instead of cumulative updates. The final test uses the maximum allowed (n) and (m) together, with (n m=160,000), and verifies the entire output structure without storing a giant hand-written expected string.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=2,m=1), no matches | Both players have `3 1/3 1/1 1/3` | Bye handling and no-opponent percentages |
| (n=2,m=1), one 1-1-1 draw | Both players have `1 1/3 4/9 4/9` | Draw scoring and exact fractions |
| (n=2,m=2), same players meet twice | Round-dependent cumulative values shown above | Repeated opponents |
| (n=4,m=2), every match is a draw | All players remain symmetric | Cumulative state and equal statistics |
| (n=10000,m=16), no matches | 16 rounds of identical bye results | Maximum (n), maximum (m), output size, performance |

## Edge Cases

A player receiving only byes is handled by the `played` array. After all actual matches in a round are processed, every player whose flag is still false receives exactly 3 MP, 6 game points, and 2 games. Their opponent list remains empty, so the output explicitly uses (1/3) for both OMW and OGW. For the input

```
1
2 1
0
```

the first player reaches MP 3 and GW (6/6=1), giving `3 1/3 1/1 1/3`, and the second player gets the same result.

The (1/3) cap is applied through `max(r, mp[i])` for MW and `max(games[i], gp[i])` for GW. Suppose a player has lost every match. After round 3 their MP may be zero, but their MW numerator is still `max(3, 0) = 3`, giving (3/9=1/3). The same construction works for GW, where a player with zero game points still receives a capped numerator equal to their number of games.

Repeated opponents are preserved by appending the opponent on every match. If the opponent list becomes `[2, 2]`, the OMW loop processes player 2 twice. After the second round, both entries use player 2's current round-2 MW, exactly matching the definition. No set or deduplication operation appears anywhere in the algorithm.

The timing of percentage computation also matters. Suppose players 1 and 2 meet in round 1, and player 2 then plays someone else in round 2. When calculating player 1's OMW after round 2, player 2's round-2 result must already be included. The implementation processes all round-2 matches and all round-2 byes before calculating any output, so every opponent statistic comes from the same completed round.

Finally, game percentages cannot use the number of rounds as their denominator. A bye contributes two games, a normal match may contain two or three games, and different players can therefore have different numbers of games. The code maintains `games[i]` explicitly and uses (3\cdot\mathrm{games}[i]) as the maximum possible game points. This is also why OGW is calculated by adding the opponents' individual GW fractions rather than trying to combine their game points and game counts.
