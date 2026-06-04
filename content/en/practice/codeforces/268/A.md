---
title: "CF 268A - Games"
description: "We are given the uniform colors of all teams in a football championship. Each team has a home color and an away color. Every ordered pair of distinct teams plays exactly one match, with one team acting as the host and the other as the guest."
date: "2026-06-05T01:18:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 268
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 164 (Div. 2)"
rating: 800
weight: 268
solve_time_s: 94
verified: true
draft: false
---

[CF 268A - Games](https://codeforces.com/problemset/problem/268/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the uniform colors of all teams in a football championship. Each team has a home color and an away color.

Every ordered pair of distinct teams plays exactly one match, with one team acting as the host and the other as the guest. Normally, the host wears its home uniform and the guest wears its away uniform.

The only special situation happens when the host's home color is exactly the same as the guest's away color. In that case, the host switches and wears its away uniform instead.

The task is to count how many matches during the entire championship trigger this switch.

The input provides the home and away colors for each team. The output is a single integer, the total number of matches where the host wears its away uniform.

The constraints are very small. There are at most 30 teams, so the total number of possible host-guest pairs is at most:

$$30 \cdot 29 = 870$$

Even a straightforward examination of every possible match is easily fast enough. There is no need for sophisticated data structures or optimization.

A common mistake is to think about unordered pairs of teams. The championship contains ordered matches. If team A hosts team B and team B hosts team A, those are two different games and must be considered separately.

Consider this example:

```
2
1 2
2 1
```

There are two matches:

Team 1 hosts Team 2:

host home = 1, guest away = 1, switch occurs.

Team 2 hosts Team 1:

host home = 2, guest away = 2, switch occurs.

The correct answer is:

```
2
```

A solution that only checks each pair once would incorrectly return 1.

Another subtle case is when several teams share the same home color.

```
3
1 2
1 3
4 1
```

Both Team 1 and Team 2 have home color 1. Team 3 has away color 1.

The matches where Team 3 visits Team 1 and Team 3 visits Team 2 both contribute to the answer. We must count every valid host-guest combination independently.

The correct answer is:

```
2
```

## Approaches

The most direct approach is to simulate the condition for every possible match.

For every team $i$ acting as host and every different team $j$ acting as guest, we check whether:

$$home_i = away_j$$

If the colors match, the host switches uniforms and we increase the answer.

This approach is correct because the problem definition depends only on the host's home color and the guest's away color. Every match can be evaluated independently.

The worst case contains 30 teams, so we perform at most:

$$30 \cdot 29 = 870$$

comparisons. That is tiny.

There is also a counting interpretation. Every occurrence of a home color can be matched with every occurrence of the same value as an away color. One could count color frequencies and multiply them. That also works, but it is unnecessary given the small constraints.

The brute-force solution is already optimal for this problem because the input size is so small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Frequency Counting | O(n + C) | O(C) | Accepted |

Here $C$ is the number of possible colors. Since $n \le 30$, the simpler quadratic solution is the natural choice.

## Algorithm Walkthrough

1. Read the number of teams.
2. Store every team's home color and away color in a list.
3. Initialize `answer = 0`.
4. For every team `i`, treat it as the host.
5. For every team `j`, treat it as the guest.
6. Skip the case where `i == j`, since a team never plays itself.
7. Check whether the host's home color equals the guest's away color.
8. If they are equal, increment `answer` by one because the host must switch to its away uniform.
9. After all pairs have been processed, print `answer`.

### Why it works

The championship contains one match for every ordered pair of distinct teams. The algorithm examines exactly those pairs.

For a particular match `(i, j)`, the problem states that the host changes uniforms if and only if the host's home color equals the guest's away color. The algorithm checks exactly this condition and adds one precisely when the match contributes to the answer.

Since every match is checked once and only once, the final count is exactly the number of matches where the host wears its away uniform.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
teams = [tuple(map(int, input().split())) for _ in range(n)]

answer = 0

for i in range(n):
    home_i = teams[i][0]

    for j in range(n):
        if i == j:
            continue

        away_j = teams[j][1]

        if home_i == away_j:
            answer += 1

print(answer)
```

The first part reads and stores all uniform colors. Each entry contains `(home_color, away_color)`.

The nested loops enumerate every ordered host-guest pair. The condition `i == j` is skipped because no team plays against itself.

The key comparison is:

```
home_i == away_j
```

This directly matches the rule from the statement. Whenever it is true, the current match contributes exactly one to the answer.

No special handling for duplicate colors is required. If several teams have the same color, every valid match is naturally counted by the loops.

Integer overflow is impossible because the maximum answer is at most $30 \cdot 29 = 870$.

## Worked Examples

### Sample 1

Input:

```
3
1 2
2 4
3 4
```

Teams:

| Team | Home | Away |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 3 | 4 |

Trace:

| Host | Guest | Host Home | Guest Away | Match? | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 4 | No | 0 |
| 1 | 3 | 1 | 4 | No | 0 |
| 2 | 1 | 2 | 2 | Yes | 1 |
| 2 | 3 | 2 | 4 | No | 1 |
| 3 | 1 | 3 | 2 | No | 1 |
| 3 | 2 | 3 | 4 | No | 1 |

Final answer:

```
1
```

This demonstrates that matches are ordered. The match where Team 2 hosts Team 1 contributes, while the reverse match does not.

### Sample 2

Input:

```
4
1 2
2 4
3 4
4 5
```

Teams:

| Team | Home | Away |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 3 | 4 |
| 4 | 4 | 5 |

Trace of contributing matches:

| Host | Guest | Host Home | Guest Away |
| --- | --- | --- | --- |
| 2 | 1 | 2 | 2 |
| 4 | 2 | 4 | 4 |
| 4 | 3 | 4 | 4 |

Total:

```
3
```

This example shows that one host color can match multiple guest away colors, and every such match must be counted separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every ordered pair of teams is checked once |
| Space | O(n) | Storage of the team color pairs |

With at most 30 teams, the algorithm performs fewer than 900 comparisons. This is far below the limits, so the solution runs comfortably within both the time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    teams = [tuple(map(int, input().split())) for _ in range(n)]

    ans = 0

    for i in range(n):
        for j in range(n):
            if i != j and teams[i][0] == teams[j][1]:
                ans += 1

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("3\n1 2\n2 4\n3 4\n") == "1", "sample 1"

# minimum size, no match
assert run("2\n1 2\n3 4\n") == "0", "minimum case"

# two matches because games are ordered
assert run("2\n1 2\n2 1\n") == "2", "ordered matches"

# multiple hosts matching same away color
assert run("3\n1 2\n1 3\n4 1\n") == "2", "duplicate home colors"

# all possible ordered matches contribute
assert run("3\n1 2\n2 1\n1 2\n") == "4", "multiple contributions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / (1,2) (3,4)` | `0` | Minimum size with no matching colors |
| `2 / (1,2) (2,1)` | `2` | Ordered matches are counted separately |
| `3 / (1,2) (1,3) (4,1)` | `2` | Duplicate home colors |
| `3 / (1,2) (2,1) (1,2)` | `4` | Multiple matches sharing the same color |

## Edge Cases

### Ordered matches matter

Input:

```
2
1 2
2 1
```

The algorithm checks:

| Host | Guest | Condition |
| --- | --- | --- |
| 1 | 2 | 1 = 1 |
| 2 | 1 | 2 = 2 |

Both matches contribute.

Output:

```
2
```

A solution that only considers each pair once would incorrectly count only one match.

### Multiple teams sharing a color

Input:

```
3
1 2
1 3
4 1
```

The algorithm finds:

| Host | Guest | Condition |
| --- | --- | --- |
| 1 | 3 | 1 = 1 |
| 2 | 3 | 1 = 1 |

Two different host teams match the same guest away color.

Output:

```
2
```

The nested-loop approach naturally counts both occurrences.

### No matching colors

Input:

```
3
1 2
3 4
5 6
```

Every comparison fails because no home color appears as an away color of another team.

Output:

```
0
```

The algorithm simply never increments the counter, producing the correct result.
