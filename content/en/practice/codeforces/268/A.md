---
title: "CF 268A - Games"
description: "Each football team owns two uniforms, a home uniform and a guest uniform. During a match, the host team normally wears its home uniform while the visiting team wears its guest uniform. There is one special situation."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 268
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 164 (Div. 2)"
rating: 800
weight: 268
solve_time_s: 89
verified: true
draft: false
---

[CF 268A - Games](https://codeforces.com/problemset/problem/268/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

Each football team owns two uniforms, a home uniform and a guest uniform. During a match, the host team normally wears its home uniform while the visiting team wears its guest uniform.

There is one special situation. If the host team's home color is the same as the guest team's guest color, the host team changes into its guest uniform instead.

We are given the home and guest colors for every team in the championship. Every pair of teams plays twice, once with each team acting as host. The task is to count how many games force the host team to switch to its guest uniform.

The input is simply a list of teams and their two colors. The output is one integer, the total number of matches where the host changes uniforms.

The constraints are very small. At most 30 teams participate, so there are at most $30 \cdot 29 = 870$ games in total. Even an $O(n^2)$ solution performs only a few hundred comparisons, which is trivial within the time limit. There is no need for advanced optimization.

One easy mistake is misunderstanding which colors must match. The condition is:

Host home color = Guest guest color

A careless implementation might compare home colors against home colors instead.

Consider this example:

```
2
1 2
1 3
```

The correct output is:

```
0
```

The home colors are equal, but that does not matter. The guest uniforms are 2 and 3, so no conflict occurs.

Another subtle case is counting both directions separately. Team A hosting Team B and Team B hosting Team A are different games.

Example:

```
2
1 2
2 1
```

The correct output is:

```
2
```

When team 1 hosts, its home color 1 matches team 2's guest color 1.

When team 2 hosts, its home color 2 matches team 1's guest color 2.

A buggy solution that only checks unordered pairs would incorrectly return 1.

## Approaches

The most direct approach is to simulate every possible hosted game.

For every team $i$, treat it as the host. For every other team $j$, treat it as the guest. If the host's home color equals the guest's guest color, increment the answer.

This works because the problem statement defines the condition independently for each game. We do not need to track schedules, standings, or any changing state. Each match contributes either 0 or 1 to the answer.

The brute-force solution performs $n^2$ comparisons. With $n \le 30$, that means at most 900 checks, which is tiny.

There is also a slightly more structured way to think about the same idea. Each team's home color can conflict with any other team's guest color. The task becomes counting equal pairs between the set of home colors and the set of guest colors, while preserving team direction.

This observation leads naturally to the same $O(n^2)$ solution. Since the constraints are already extremely small, there is no practical need for hashing or frequency arrays, although they would also work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n²) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of teams.
2. Store every team's home color and guest color in a list.
3. Initialize the answer to 0.
4. Iterate through every team as the host.
5. For each host team, iterate through every team again as the guest.
6. Compare the host's home color with the guest's guest color.
7. If the colors match, increment the answer because the host must switch uniforms.
8. After all pairs are checked, print the final answer.

Why it works:

Every championship game is uniquely identified by an ordered pair $(host, guest)$. The algorithm examines every such pair exactly once. A game contributes to the answer precisely when the host's home color equals the guest's guest color, which is exactly the rule from the statement. Since no valid game is skipped and no invalid game is counted, the final total is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

teams = []
for _ in range(n):
    h, a = map(int, input().split())
    teams.append((h, a))

answer = 0

for i in range(n):
    for j in range(n):
        if teams[i][0] == teams[j][1]:
            answer += 1

print(answer)
```

The program first stores all home and guest colors in a list of pairs. This makes later comparisons simple and readable.

The nested loops enumerate every ordered pair of teams. The outer loop chooses the host team, while the inner loop chooses the guest team.

The comparison:

```
teams[i][0] == teams[j][1]
```

checks whether the host's home color equals the guest's guest color.

One detail that sometimes confuses people is whether we should skip `i == j`. We do not need to. The statement guarantees that each team's home and guest colors are different, so a team can never conflict with itself. Keeping the condition simple avoids unnecessary branching.

The answer easily fits inside a normal integer because the total number of games is at most 870.

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

| Team | Home | Guest |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 3 | 4 |

Trace:

| Host Team | Guest Team | Host Home | Guest Guest | Match? | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | No | 0 |
| 1 | 2 | 1 | 4 | No | 0 |
| 1 | 3 | 1 | 4 | No | 0 |
| 2 | 1 | 2 | 2 | Yes | 1 |
| 2 | 2 | 2 | 4 | No | 1 |
| 2 | 3 | 2 | 4 | No | 1 |
| 3 | 1 | 3 | 2 | No | 1 |
| 3 | 2 | 3 | 4 | No | 1 |
| 3 | 3 | 3 | 4 | No | 1 |

Final answer:

```
1
```

This example shows the exact interpretation of the rule. Only one hosted game creates a color conflict.

### Sample 2

Input:

```
4
1 2
2 4
3 4
4 5
```

Trace:

| Host Team | Guest Team | Host Home | Guest Guest | Match? | Running Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | No | 0 |
| 1 | 2 | 1 | 4 | No | 0 |
| 1 | 3 | 1 | 4 | No | 0 |
| 1 | 4 | 1 | 5 | No | 0 |
| 2 | 1 | 2 | 2 | Yes | 1 |
| 2 | 2 | 2 | 4 | No | 1 |
| 2 | 3 | 2 | 4 | No | 1 |
| 2 | 4 | 2 | 5 | No | 1 |
| 3 | 1 | 3 | 2 | No | 1 |
| 3 | 2 | 3 | 4 | No | 1 |
| 3 | 3 | 3 | 4 | No | 1 |
| 3 | 4 | 3 | 5 | No | 1 |
| 4 | 1 | 4 | 2 | No | 1 |
| 4 | 2 | 4 | 4 | Yes | 2 |
| 4 | 3 | 4 | 4 | Yes | 3 |
| 4 | 4 | 4 | 5 | No | 3 |

Final answer:

```
3
```

This trace demonstrates that one host team can conflict with multiple visiting teams if several guest uniforms share the same color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every ordered pair of teams is checked once |
| Space | O(1) | Only a few variables besides the input list are used |

With at most 30 teams, the algorithm performs fewer than 900 comparisons. This is far below the limits, so the solution comfortably fits within both the time and memory constraints.

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
            if teams[i][0] == teams[j][1]:
                ans += 1

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
"""3
1 2
2 4
3 4
"""
) == "1\n", "sample 1"

# minimum size, no matches
assert run(
"""2
1 2
3 4
"""
) == "0\n", "minimum case"

# both directions match
assert run(
"""2
1 2
2 1
"""
) == "2\n", "direction matters"

# multiple guests matching same host
assert run(
"""4
1 5
2 1
3 1
4 1
"""
) == "3\n", "one host conflicts multiple times"

# maximum style repeated structure
assert run(
"""5
1 2
2 3
3 4
4 5
5 1
"""
) == "5\n", "cyclic matching"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 teams with unrelated colors | 0 | No false positives |
| 2 teams with swapped colors | 2 | Ordered games counted separately |
| One guest color repeated many times | 3 | Multiple conflicts for same host |
| Cyclic color structure | 5 | Counting across many different pairs |

## Edge Cases

Consider the case where home colors match each other, but guest colors do not:

```
2
1 2
1 3
```

The algorithm checks:

| Host | Guest | Compare |
| --- | --- | --- |
| 1 | 2 | 1 == 3 |
| 2 | 1 | 1 == 2 |

Both comparisons fail, so the answer remains 0.

This confirms that only host-home versus guest-guest comparisons matter.

Now consider directional counting:

```
2
1 2
2 1
```

The algorithm performs these checks:

| Host | Guest | Compare | Counted |
| --- | --- | --- | --- |
| 1 | 2 | 1 == 1 | Yes |
| 2 | 1 | 2 == 2 | Yes |

The final answer becomes 2.

This confirms that games are treated independently depending on who hosts.

Finally, consider self-comparisons:

```
3
1 2
2 3
3 1
```

When `i == j`, the algorithm compares:

```
1 == 2
2 == 3
3 == 1
```

All fail because each team's home and guest colors are guaranteed distinct. Self-checks never accidentally increase the answer.
