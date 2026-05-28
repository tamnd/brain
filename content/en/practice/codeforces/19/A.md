---
title: "CF 19A - World Football Cup"
description: "We are given the full results of a football tournament where every pair of teams plays exactly one match. For each match"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 19
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 19"
rating: 1400
weight: 19
solve_time_s: 351
verified: true
draft: false
---

[CF 19A - World Football Cup](https://codeforces.com/problemset/problem/19/A)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 5m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the full results of a football tournament where every pair of teams plays exactly one match. For each match, we know how many goals each side scored. Using the tournament rules, we must determine which teams advance to the knockout stage.

Each team earns points from matches. A win gives 3 points, a draw gives 1 point, and a loss gives 0 points. Teams are ranked by three criteria, checked in order:

1. Total points.
2. Goal difference, goals scored minus goals conceded.
3. Total goals scored.

The statement guarantees these rules always produce a strict ordering, so no two teams are completely tied after applying all three comparisons.

After computing the standings, the top `n / 2` teams qualify. The output must contain those qualifying team names sorted lexicographically, not by ranking order.

The constraints are very small. At most 50 teams participate, which means the number of matches is at most `50 * 49 / 2 = 1225`. Even an `O(n²)` or `O(n² log n)` solution is easily fast enough inside a 2 second limit. The main challenge is not optimization, it is implementing the ranking rules correctly and parsing the match format safely.

A common mistake is outputting the qualifiers in ranking order instead of alphabetical order. Consider this example:

```
4
Brazil
Argentina
Spain
Italy
Brazil-Argentina 1:0
Brazil-Spain 0:0
Brazil-Italy 2:0
Argentina-Spain 1:0
Argentina-Italy 1:0
Spain-Italy 3:0
```

Suppose the ranking order becomes:

```
Brazil
Spain
Argentina
Italy
```

The qualified teams are Brazil and Spain, but the required output is:

```
Brazil
Spain
```

If the qualifiers had been Spain and Argentina, the correct output would still need alphabetical sorting:

```
Argentina
Spain
```

Another easy bug appears when updating goal difference directly instead of tracking goals scored and conceded separately. Imagine:

```
2
A
B
A-B 2:1
```

Team A has:

- points = 3
- scored = 2
- conceded = 1
- difference = 1

If we only store difference and forget total goals scored, we cannot apply the third tie-breaker later.

Parsing also deserves attention because names contain uppercase and lowercase letters. The match line:

```
RealMadrid-PSG 3:2
```

must be split correctly into:

- team1 = `RealMadrid`
- team2 = `PSG`
- score1 = `3`
- score2 = `2`

A careless split on spaces alone loses the structure of the names and scores.

## Approaches

The most direct approach is to simulate the entire tournament exactly as described. For every team, maintain its accumulated statistics:

- points
- goals scored
- goals conceded

Then process every match one by one. Update both teams according to the result, then sort all teams using the ranking rules.

This brute-force method is already fast enough because there are at most 1225 matches. Processing each match takes constant time, and sorting 50 teams costs almost nothing. The total work is comfortably below a million operations.

Some beginners overcomplicate this problem by trying to recompute rankings repeatedly after every match or by comparing teams pairwise multiple times. That still works under these constraints, but it obscures the real structure of the problem.

The key observation is that the ranking criteria depend only on aggregated statistics. Once all matches are processed, every team is fully described by:

- total points
- goal difference
- goals scored

Nothing else matters. We never need the individual match history again.

That lets us reduce the entire problem to:

1. Build statistics from all games.
2. Sort teams using the official comparator.
3. Take the first `n / 2`.
4. Output them alphabetically.

The solution is mostly careful implementation rather than algorithmic difficulty.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with repeated comparisons | O(n³) | O(n) | Accepted |
| Optimal aggregation + single sort | O(n² + n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of teams and store all team names.

We need the names both for indexing statistics and for final output.
2. Create a statistics table for every team.

For each team store:

- points
- goals scored
- goals conceded

Goal difference can always be computed as:

```
scored - conceded
```
3. Process every match line.

Each line has the form:

```
team1-team2 x:y
```

Split the line into the team part and score part, then extract:

- `team1`
- `team2`
- `x`
- `y`
4. Update goals for both teams.

If team1 scores `x` and concedes `y`:

- add `x` to scored
- add `y` to conceded

Do the symmetric update for team2.
5. Update points according to the result.

If `x > y`, team1 gets 3 points.

If `x < y`, team2 gets 3 points.

Otherwise both teams get 1 point.
6. After all matches are processed, sort teams by ranking rules.

The comparator is:

- higher points first
- higher goal difference first
- higher goals scored first

Since Python sorts ascending by default, we sort using negative values.
7. Take the first `n / 2` teams from the sorted standings.

These are the qualified teams.
8. Sort the qualified team names lexicographically.

The output format requires alphabetical order, not ranking order.
9. Print the names one per line.

### Why it works

Every ranking criterion depends only on accumulated tournament statistics. Processing each match updates those statistics exactly according to the rules of football scoring. After all matches are processed, each team's stored values match its true tournament record.

Sorting by:

1. points,
2. goal difference,
3. goals scored,

exactly reproduces the official standings definition. Since the statement guarantees no complete ties, the sorted order is unique. Selecting the first `n / 2` teams gives precisely the qualifiers. Sorting those names alphabetically matches the required output format.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    stats = {}

    for _ in range(n):
        name = input().strip()
        stats[name] = {
            "points": 0,
            "scored": 0,
            "conceded": 0
        }

    matches = n * (n - 1) // 2

    for _ in range(matches):
        line = input().strip()

        teams_part, score_part = line.split()
        team1, team2 = teams_part.split('-')

        g1, g2 = map(int, score_part.split(':'))

        stats[team1]["scored"] += g1
        stats[team1]["conceded"] += g2

        stats[team2]["scored"] += g2
        stats[team2]["conceded"] += g1

        if g1 > g2:
            stats[team1]["points"] += 3
        elif g1 < g2:
            stats[team2]["points"] += 3
        else:
            stats[team1]["points"] += 1
            stats[team2]["points"] += 1

    teams = list(stats.keys())

    teams.sort(
        key=lambda name: (
            -stats[name]["points"],
            -(stats[name]["scored"] - stats[name]["conceded"]),
            -stats[name]["scored"]
        )
    )

    qualified = teams[: n // 2]
    qualified.sort()

    print('\n'.join(qualified))

solve()
```

The first section reads all team names and initializes a dictionary of statistics. Using a dictionary keyed by team name avoids any indexing issues and makes updates straightforward.

Each match line is split into two pieces:

- `"A-B"`
- `"1:0"`

Then each piece is parsed independently. This is safer than trying to split everything at once because team names may contain both uppercase and lowercase letters.

Goals scored and conceded are updated before points. Keeping scored and conceded separately avoids mistakes in tie-break calculations. Goal difference is derived only during sorting.

The sorting key directly encodes the tournament rules. Negative values reverse the order so larger statistics come first.

One subtle detail is the final alphabetical sort of qualified teams. Many incorrect submissions print teams in ranking order instead.

## Worked Examples

### Example 1

Input:

```
4
A
B
C
D
A-B 1:1
A-C 2:2
A-D 1:0
B-C 1:0
B-D 0:3
C-D 0:3
```

### Match Processing Trace

| Match | Team | Points | Scored | Conceded | Difference |
| --- | --- | --- | --- | --- | --- |
| A-B 1:1 | A | 1 | 1 | 1 | 0 |
| A-B 1:1 | B | 1 | 1 | 1 | 0 |
| A-C 2:2 | A | 2 | 3 | 3 | 0 |
| A-C 2:2 | C | 1 | 2 | 2 | 0 |
| A-D 1:0 | A | 5 | 4 | 3 | 1 |
| A-D 1:0 | D | 0 | 0 | 1 | -1 |
| B-C 1:0 | B | 4 | 2 | 1 | 1 |
| B-C 1:0 | C | 1 | 2 | 3 | -1 |
| B-D 0:3 | B | 4 | 2 | 4 | -2 |
| B-D 0:3 | D | 3 | 3 | 1 | 2 |
| C-D 0:3 | C | 1 | 2 | 6 | -4 |
| C-D 0:3 | D | 6 | 6 | 1 | 5 |

### Final Ranking

| Team | Points | Difference | Goals Scored |
| --- | --- | --- | --- |
| D | 6 | 5 | 6 |
| A | 5 | 1 | 4 |
| B | 4 | -2 | 2 |
| C | 1 | -4 | 2 |

Top two teams are `D` and `A`. After alphabetical sorting:

```
A
D
```

This example confirms that qualification order and output order are different concepts.

### Example 2

Input:

```
4
Alpha
Beta
Gamma
Delta
Alpha-Beta 1:0
Alpha-Gamma 0:2
Alpha-Delta 3:1
Beta-Gamma 1:1
Beta-Delta 2:0
Gamma-Delta 0:1
```

### Match Processing Trace

| Team | Points | Scored | Conceded | Difference |
| --- | --- | --- | --- | --- |
| Alpha | 6 | 4 | 3 | 1 |
| Beta | 4 | 3 | 2 | 1 |
| Gamma | 4 | 3 | 2 | 1 |
| Delta | 3 | 2 | 5 | -3 |

Beta and Gamma are tied on points and goal difference. The third tie-breaker, goals scored, is also tied here, which would violate the statement guarantee. Such inputs never appear officially.

If we slightly modify:

```
Gamma-Delta 1:1
```

then Gamma becomes:

| Team | Points | Difference | Goals Scored |
| --- | --- | --- | --- |
| Gamma | 5 | 1 | 4 |

Now the ordering is unique.

This trace demonstrates why all three statistics must be stored correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² + n log n) | Processing all matches takes O(n²), sorting teams takes O(n log n) |
| Space | O(n) | Only team statistics are stored |

With at most 50 teams, the number of matches is at most 1225. The solution performs only a few thousand operations, which is far below the time limit. Memory usage is tiny because only one statistics record per team is needed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        stats = {}

        for _ in range(n):
            name = input().strip()
            stats[name] = {
                "points": 0,
                "scored": 0,
                "conceded": 0
            }

        matches = n * (n - 1) // 2

        for _ in range(matches):
            line = input().strip()

            teams_part, score_part = line.split()
            team1, team2 = teams_part.split('-')

            g1, g2 = map(int, score_part.split(':'))

            stats[team1]["scored"] += g1
            stats[team1]["conceded"] += g2

            stats[team2]["scored"] += g2
            stats[team2]["conceded"] += g1

            if g1 > g2:
                stats[team1]["points"] += 3
            elif g1 < g2:
                stats[team2]["points"] += 3
            else:
                stats[team1]["points"] += 1
                stats[team2]["points"] += 1

        teams = list(stats.keys())

        teams.sort(
            key=lambda name: (
                -stats[name]["points"],
                -(stats[name]["scored"] - stats[name]["conceded"]),
                -stats[name]["scored"]
            )
        )

        qualified = teams[: n // 2]
        qualified.sort()

        return '\n'.join(qualified)

    return solve()

# provided sample
assert run(
"""4
A
B
C
D
A-B 1:1
A-C 2:2
A-D 1:0
B-C 1:0
B-D 0:3
C-D 0:3
"""
) == "A\nD", "sample 1"

# minimum size
assert run(
"""2
X
Y
X-Y 5:0
"""
) == "X", "minimum teams"

# draw with goal difference tie
assert run(
"""4
A
B
C
D
A-B 1:0
A-C 0:1
A-D 2:0
B-C 0:0
B-D 3:0
C-D 2:0
"""
) == "A\nC", "tie-break by goals scored"

# alphabetical output check
assert run(
"""4
Zebra
Apple
Monkey
Bear
Zebra-Apple 0:1
Zebra-Monkey 0:1
Zebra-Bear 1:0
Apple-Monkey 1:0
Apple-Bear 1:0
Monkey-Bear 2:0
"""
) == "Apple\nMonkey", "alphabetical output"

# larger balanced case
assert run(
"""6
A
B
C
D
E
F
A-B 1:0
A-C 1:0
A-D 1:0
A-E 1:0
A-F 1:0
B-C 1:0
B-D 1:0
B-E 1:0
B-F 1:0
C-D 1:0
C-E 1:0
C-F 1:0
D-E 1:0
D-F 1:0
E-F 1:0
"""
) == "A\nB\nC", "strict ranking chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-team tournament | X | Minimum valid input |
| Tie-break scenario | A C | Correct secondary and tertiary ranking |
| Alphabetical qualifier output | Apple Monkey | Output order differs from ranking order |
| 6-team strict chain | A B C | Larger standings computation |

## Edge Cases

Consider the case where output order differs from ranking order:

```
4
Z
A
M
B
Z-A 0:1
Z-M 0:1
Z-B 1:0
A-M 1:0
A-B 1:0
M-B 2:0
```

The ranking becomes:

```
A
M
Z
B
```

The qualifiers are `A` and `M`. The algorithm first extracts the top half from ranking order, then sorts only those names alphabetically before printing:

```
A
M
```

This handles the required formatting correctly.

Now consider a tie resolved by goal difference:

```
4
A
B
C
D
A-B 1:0
A-C 0:2
A-D 1:0
B-C 1:0
B-D 2:0
C-D 0:1
```

Final statistics:

| Team | Points | Difference | Goals |
| --- | --- | --- | --- |
| A | 6 | 0 | 2 |
| B | 6 | 2 | 3 |
| C | 3 | 1 | 2 |
| D | 3 | -3 | 1 |

Although A and B have equal points, B advances above A because of superior goal difference. Since the algorithm sorts using all three ranking keys in order, it reproduces the official standings exactly.

Finally, consider the smallest possible tournament:

```
2
A
B
A-B 0:0
```

Both teams draw and earn one point. Their goal difference and goals scored are also equal, which would violate the guarantee of unique ordering. Official test data avoids such cases. The algorithm still processes the input consistently, but the problem guarantees we never need to resolve impossible ties.
