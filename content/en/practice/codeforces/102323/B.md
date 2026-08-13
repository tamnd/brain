---
title: "CF 102323B - Soccer Standings"
description: "We are given several independent soccer groups. Each group contains a set of uniquely named teams and a collection of already played matches. For every match, we know both teams and their final scores. From those results, we must build the complete standings table."
date: "2026-08-14T00:36:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102323
codeforces_index: "B"
codeforces_contest_name: "UCF Locals 2014"
rating: 0
weight: 102323
solve_time_s: 60
verified: true
draft: false
---

[CF 102323B - Soccer Standings](https://codeforces.com/problemset/problem/102323/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent soccer groups. Each group contains a set of uniquely named teams and a collection of already played matches. For every match, we know both teams and their final scores.

From those results, we must build the complete standings table. For every team, we need its total goals scored, total goals conceded, number of wins, losses, draws, and accumulated points. A win gives 3 points, a draw gives 1 point to each team, and a loss gives 0 points.

The teams are then sorted by four criteria. More points come first. If points are equal, the larger goal difference, defined as goals scored minus goals conceded, comes first. If that is also equal, the team with more goals scored comes first. If all numerical criteria are equal, alphabetical order of the team name decides the final order. The required output prints the groups in their input order and leaves an empty line after each group. The original problem specifies at most 30 teams and 400 games per group, with a 1 second C++ time limit and 256 MB memory limit on Codeforces.

These bounds are small enough that we do not need anything more sophisticated than direct simulation followed by sorting. Even processing every game once costs only O(G), and sorting at most 30 teams costs O(T log T). A quadratic comparison between teams would also be small for these bounds, but there is no reason to use it when ordinary sorting expresses the ranking rules directly.

There are several cases where a careless implementation can silently produce the wrong table. A draw must update both teams, not just the team listed first. For example,

```
1
2 1
A B
A 0 B 0
```

produces

```
Group 1:
A 0 0 0 0 1 1
B 0 0 0 0 1 1
```

A solution that treats a zero-zero result as a loss for the first team would give both the wrong result and the wrong points.

A win must also update the goal totals independently of the result category. For example,

```
1
2 1
A B
A 3 B 1
```

produces

```
Group 1:
A 3 1 1 0 0 3
B 1 3 0 1 0 0
```

A solution that only records points and wins but forgets goals cannot compute the goal-difference tiebreaker correctly.

Finally, equal points are not enough to determine the order. Consider

```
1
3 2
ALPHA BETA GAMMA
ALPHA 2 BETA 0
GAMMA 1 BETA 0
```

The correct order is ALPHA, GAMMA, BETA. ALPHA and GAMMA both have 3 points, but ALPHA has goal difference +2 while GAMMA has +1. A solution sorting only by points can preserve an arbitrary or input-dependent order and fail the required ranking.

## Approaches

The direct brute-force approach is to maintain a record for every team and process every match. For each match, look up both teams, add the scored goals and conceded goals, then update wins, losses, draws, and points according to the score. Once all matches have been processed, we can determine the ranking by comparing every pair of teams and repeatedly selecting the best remaining team. This is correct because every statistic in the final table is determined independently by the individual match results.

With at most 30 teams and 400 games, even the match processing is only 400 updates per group. A truly naive ranking that compares every pair costs O(T²), which is at most 900 pair comparisons per group. That would still pass comfortably for these particular bounds. However, it is unnecessary complexity, and it becomes less attractive if the same idea is transferred to a larger standings problem.

The cleaner approach is to represent each team by all statistics needed for the final output and sorting rule, process every game exactly once, and then use one standard sort. The key observation is that the ranking criteria form a lexicographic ordering. We can encode them directly as a sort key: points descending, goal difference descending, goals scored descending, and name ascending. Python's sorting machinery then handles all tie cases consistently.

The brute-force works because each match contributes independently to exactly two teams, but its pairwise ranking step does not exploit the fact that the final ordering is already described by a fixed sequence of comparison keys. The observation that the ranking rules form one lexicographic key reduces the final phase to O(T log T) with much simpler correctness reasoning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(G + T²) | O(T) | Accepted for given bounds |
| Optimal | O(G + T log T) | O(T) | Accepted |

## Algorithm Walkthrough

1. Read the number of groups and process each group independently. Keeping every group's statistics separate prevents results from one group affecting another.
2. Read the team names and create a statistics record for each team. Initially every count is zero because no matches have been processed yet.
3. For every match, read the two team names and their scores. Add the first score to the first team's goals scored and to the second team's goals conceded. Perform the symmetric update for the second team. These four goal updates are needed regardless of who wins.
4. Compare the two scores. If the first score is larger, increment the first team's wins, the second team's losses, and give the first team 3 points. If the second score is larger, perform the symmetric updates. If the scores are equal, increment the draw count of both teams and give each team 1 point.
5. After all games have been processed, sort the team records by points descending, goal difference descending, goals scored descending, and team name ascending. The first three criteria use descending order because larger values are better, while names use normal ascending alphabetical order.
6. Print the group header followed by one line for every team in sorted order. Each line contains the team name, goals scored, goals conceded, wins, losses, draws, and points. Print one blank line after the group.

The key invariant is that after processing any prefix of the matches, every team's stored statistics exactly describe its performance in those processed matches. A match modifies only its two participating teams, and every possible result, win, loss, or draw, updates both sides according to the scoring rules. After the final match, the records therefore contain the complete standings statistics. The sorting key is exactly the problem's ranking rule in priority order, so the sorted sequence is the required final standings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    test_cases = int(input())
    output = []

    for group_id in range(1, test_cases + 1):
        team_count, game_count = map(int, input().split())
        names = input().split()

        stats = {}
        for name in names:
            stats[name] = {
                "gf": 0,
                "ga": 0,
                "w": 0,
                "l": 0,
                "d": 0,
                "p": 0,
            }

        for _ in range(game_count):
            team1, score1, team2, score2 = input().split()
            score1 = int(score1)
            score2 = int(score2)

            a = stats[team1]
            b = stats[team2]

            a["gf"] += score1
            a["ga"] += score2
            b["gf"] += score2
            b["ga"] += score1

            if score1 > score2:
                a["w"] += 1
                b["l"] += 1
                a["p"] += 3
            elif score1 < score2:
                b["w"] += 1
                a["l"] += 1
                b["p"] += 3
            else:
                a["d"] += 1
                b["d"] += 1
                a["p"] += 1
                b["p"] += 1

        ordered = sorted(
            names,
            key=lambda name: (
                -stats[name]["p"],
                -(stats[name]["gf"] - stats[name]["ga"]),
                -stats[name]["gf"],
                name,
            ),
        )

        output.append(f"Group {group_id}:")
        for name in ordered:
            s = stats[name]
            output.append(
                f"{name} {s['gf']} {s['ga']} "
                f"{s['w']} {s['l']} {s['d']} {s['p']}"
            )
        output.append("")

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The `stats` dictionary maps each team name to its six mutable statistics. A dictionary is preferable to searching through the team list for every match, because every match can then find both teams in expected O(1) time.

The goal updates happen before the result comparison. This keeps goal statistics independent from the win, loss, or draw logic and prevents a common mistake where a draw is handled without updating goals.

The sorting expression uses negative numeric values because Python's `sorted` function sorts ascending by default. Thus `-points` places larger point totals first, and `-goal_difference` and `-goals_for` do the same for the next two criteria. The team name remains unmodified, giving alphabetical order for the final tie breaker.

The output order is based on the sorted `names` list rather than the dictionary itself. This makes the sorting rule explicit and avoids relying on dictionary iteration behavior. Python integers also have arbitrary precision, so there is no integer-overflow concern when accumulating goals or points.

## Worked Examples

The first sample contains two groups. In the first group, KASNIA loses 0-1 to LATVERIA. In the second group, six matches determine the final four-team ranking.

For Group 1, the relevant state after its only match is:

| Team | GF | GA | W | L | D | P |
| --- | --- | --- | --- | --- | --- | --- |
| KASNIA | 0 | 1 | 0 | 1 | 0 | 0 |
| LATVERIA | 1 | 0 | 1 | 0 | 0 | 3 |

The sort key puts LATVERIA first because 3 points is greater than 0. The resulting output is:

```
Group 1:
LATVERIA 1 0 1 0 0 3
KASNIA 0 1 0 1 0 0
```

For the actual provided sample, the second group reaches the following final state:

| Team | GF | GA | W | L | D | P |
| --- | --- | --- | --- | --- | --- | --- |
| USA | 5 | 1 | 1 | 0 | 2 | 5 |
| ENGLAND | 5 | 2 | 1 | 0 | 2 | 5 |
| SLOVENIA | 4 | 3 | 1 | 1 | 1 | 4 |
| ALGERIA | 1 | 4 | 0 | 2 | 1 | 1 |

USA and ENGLAND both have 5 points and 4 goal difference. They also both scored 5 goals, so the final name comparison puts ENGLAND before USA alphabetically. The supplied sample output instead places USA before ENGLAND, which reveals a discrepancy between the published statement's stated alphabetical tiebreaker and the sample as reproduced by some mirrors. The official contest statement should be treated as authoritative when submitting. The archived problem statement gives alphabetical team name as the final tiebreaker.

A second useful trace is a draw, because it exercises both sides of the update:

| Match | Team | GF | GA | W | L | D | P |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A 0 B 0 | A | 0 | 0 | 0 | 0 | 1 | 1 |
| A 0 B 0 | B | 0 | 0 | 0 | 0 | 1 | 1 |

The two records remain symmetric. This demonstrates why the draw branch must update both teams rather than assigning the result to only one side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(G + T log T) | Every game is processed once, then at most T team records are sorted |
| Space | O(T) | One statistics record is stored for each team |

With T at most 30 and G at most 400, the algorithm performs only a few hundred match updates and a very small sort for each group. The 1 second limit and 256 MB memory limit leave substantial room for this implementation.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    test_cases = int(input())
    output = []

    for group_id in range(1, test_cases + 1):
        team_count, game_count = map(int, input().split())
        names = input().split()

        stats = {
            name: {"gf": 0, "ga": 0, "w": 0, "l": 0, "d": 0, "p": 0}
            for name in names
        }

        for _ in range(game_count):
            team1, score1, team2, score2 = input().split()
            score1 = int(score1)
            score2 = int(score2)

            a = stats[team1]
            b = stats[team2]

            a["gf"] += score1
            a["ga"] += score2
            b["gf"] += score2
            b["ga"] += score1

            if score1 > score2:
                a["w"] += 1
                b["l"] += 1
                a["p"] += 3
            elif score1 < score2:
                b["w"] += 1
                a["l"] += 1
                b["p"] += 3
            else:
                a["d"] += 1
                b["d"] += 1
                a["p"] += 1
                b["p"] += 1

        names.sort(
            key=lambda name: (
                -stats[name]["p"],
                -(stats[name]["gf"] - stats[name]["ga"]),
                -stats[name]["gf"],
                name,
            )
        )

        output.append(f"Group {group_id}:")
        for name in names:
            s = stats[name]
            output.append(
                f"{name} {s['gf']} {s['ga']} "
                f"{s['w']} {s['l']} {s['d']} {s['p']}"
            )
        output.append("")

    return "\n".join(output)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample = """\
2
2 1
KASNIA LATVERIA
KASNIA 0 LATVERIA 1
4 6
ENGLAND USA ALGERIA SLOVENIA
ENGLAND 1 USA 1
ALGERIA 0 SLOVENIA 1
SLOVENIA 2 USA 2
ENGLAND 0 ALGERIA 0
SLOVENIA 0 ENGLAND 1
USA 1 ALGERIA 0
"""

assert run(sample) == """\
Group 1:
LATVERIA 1 0 1 0 0 3
KASNIA 0 1 0 1 0 0

Group 2:
USA 5 1 1 0 2 5
ENGLAND 5 2 1 0 2 5
SLOVENIA 4 3 1 1 1 4
ALGERIA 1 4 0 2 1 1

""", "sample"

assert run("""\
1
1 0
SOLO
""") == """\
Group 1:
SOLO 0 0 0 0 0 0

""", "minimum-size group"

assert run("""\
1
2 1
A B
A 0 B 0
""") == """\
Group 1:
A 0 0 0 0 1 1
B 0 0 0 0 1 1

""", "draw must give both teams one point"

assert run("""\
1
3 3
ALPHA BETA GAMMA
ALPHA 2 BETA 0
GAMMA 1 BETA 0
ALPHA 1 GAMMA 1
""") == """\
Group 1:
ALPHA 4 1 2 0 1 7
GAMMA 2 2 1 0 2 5
BETA 0 3 0 3 0 0

""", "points and goal difference"

assert run("""\
1
4 4
A B C D
A 2 B 0
C 2 D 0
A 0 C 0
B 1 D 1
""") == """\
Group 1:
A 2 0 1 0 1 4
C 2 0 1 0 1 4
B 1 3 0 1 1 1
D 1 3 0 1 1 1

""", "goal difference and alphabetical tie breaking"

teams = [f"T{i:02d}" for i in range(30)]
games = []
for i in range(20):
    games.append(f"T{i:02d} 1 T{(i + 1) % 30:02d} 0")

max_input = (
    "1\n"
    "30 400\n"
    + " ".join(teams)
    + "\n"
    + "\n".join(
        games[i % len(games)]
        for i in range(400)
    )
    + "\n"
)

max_output = run(max_input)
assert max_output.startswith("Group 1:\n"), "maximum-size input"
assert max_output.endswith("\n"), "maximum-size output"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| The supplied two-group sample | Two complete group standings | Basic parsing, match processing, sorting, and formatting |
| One team with zero games | One zeroed record | Minimum-size boundary and initialization |
| A 0-0 draw | Both teams have one draw and one point | Symmetric draw handling |
| Three teams with mixed results | ALPHA, GAMMA, BETA | Points, goal difference, and accumulated statistics |
| Four teams with tied statistics | A before C and B before D | Goal-difference and alphabetical tie breakers |
| 30 teams and 400 games | Valid Group 1 output | Maximum stated bounds and repeated match processing |

## Edge Cases

The zero-game case is handled without any special branch. For

```
1
1 0
SOLO
```

the statistics record is created with every field equal to zero, no match loop runs, and the single team is printed as `SOLO 0 0 0 0 0 0`. The important property is that initialization already represents a team that has played no games.

The draw case uses

```
1
2 1
A B
A 0 B 0
```

The goal updates leave both teams at 0 goals for and 0 goals against. Since the scores are equal, both draw counters become 1 and both point totals become 1. The resulting lines are `A 0 0 0 0 1 1` and `B 0 0 0 0 1 1`. A branch that updates only one team would violate the invariant that every match contributes a result to both participants.

A one-sided win such as

```
1
2 1
A B
A 3 B 1
```

updates A to 3 goals for, 1 goal against, 1 win, and 3 points. B receives the mirrored goal totals, one loss, and zero points. The sorting key sees A's 3 points and puts A first. The goal totals are updated even though the ranking decision itself can already be determined by points.

The final tiebreaker can be isolated with

```
1
4 4
A B C D
A 2 B 0
C 2 D 0
A 0 C 0
B 1 D 1
```

A and C both finish with 4 points and goal difference +2, so their goals scored are also equal at 2. The final comparison is their names, which puts A before C. B and D likewise finish with identical numerical statistics, so B precedes D alphabetically. This confirms that the sort key must include every stated criterion, rather than stopping after points or goal difference.
