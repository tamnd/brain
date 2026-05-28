---
title: "CF 43A - Football"
description: "We are given the sequence of goals scored during a football match. Every line after the first contains the name of the team that scored one goal. The task is to determine which team scored more goals overall."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 43
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 42 (Div. 2)"
rating: 1000
weight: 43
solve_time_s: 89
verified: true
draft: false
---
[CF 43A - Football](https://codeforces.com/problemset/problem/43/A)

**Rating:** 1000  
**Tags:** strings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the sequence of goals scored during a football match. Every line after the first contains the name of the team that scored one goal. The task is to determine which team scored more goals overall.

The input guarantees that at most two distinct team names appear, and the match never ends in a draw. That means one team always has a strictly larger number of goals than the other.

The constraints are very small. The number of goals is at most 100, and each team name has length at most 10. Even an inefficient solution that compares every goal against every other goal would still fit comfortably within the time limit. This gives us freedom to focus on clarity instead of aggressive optimization.

The main challenge is not performance, it is correctly counting goals for each team.

One easy mistake is assuming there are always exactly two teams. Consider:

```
1
ABC
```

The correct answer is:

```
ABC
```

A careless implementation that immediately reads two distinct names would fail because only one team appears.

Another subtle issue is updating counts incorrectly when the same team appears multiple times. For example:

```
5
A
B
A
A
B
```

The correct output is:

```
A
```

If we overwrite counts instead of incrementing them, the final result becomes wrong.

A different pitfall comes from comparing only adjacent goals. Consider:

```
4
A
B
B
A
```

The final score is tied here, which the problem says will never happen, but this example shows why adjacency tells us nothing about the winner. We must count all occurrences globally.

## Approaches

The most direct brute-force idea is to examine each team name and count how many times it appears in the full list. For every goal entry, we scan the entire array again and compute its frequency.

If there are `n` goals, this performs `n * n` comparisons in the worst case. With `n = 100`, that is only 10,000 operations, which is perfectly acceptable here. The brute-force approach is correct because the winner is exactly the team with the largest frequency.

The inefficiency comes from recomputing the same counts repeatedly. If `"A"` appears 50 times, we still recount all 100 entries every time we encounter `"A"`.

The key observation is that this problem is fundamentally a frequency-counting problem. Instead of repeatedly scanning the list, we can maintain a running count for each team while reading the input.

A hash map, implemented as a Python dictionary, is ideal here. Every time we read a team name, we increase its stored count by one. After processing all goals, the dictionary contains the exact number of goals scored by every team.

Since there are at most two teams, finding the winner afterward is trivial. We simply select the team with the larger count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(k) | Accepted |

Here, `k` is the number of distinct teams, which is at most 2.

## Algorithm Walkthrough

1. Read the integer `n`, the number of goals scored during the match.
2. Create an empty dictionary called `count`.

The dictionary maps a team name to the number of goals scored by that team.
3. Repeat `n` times:

1. Read a team name.
2. Increase its frequency inside the dictionary.

If the team has not appeared before, initialize its count to zero first.
4. After processing all goals, iterate through the dictionary entries and track the team with the maximum count.
5. Print the team with the highest frequency.

### Why it works

The algorithm maintains the invariant that after processing the first `i` goals, the dictionary stores the exact number of goals scored by every team within those `i` entries.

Each new goal updates exactly one team's count by one, so the invariant remains true throughout the process.

At the end, all goals have been processed, meaning the dictionary contains the final score for every team. Since the problem guarantees there is no tie, the team with the largest count is uniquely the winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    count = {}
    
    for _ in range(n):
        team = input().strip()
        count[team] = count.get(team, 0) + 1
    
    winner = ""
    best = 0
    
    for team, goals in count.items():
        if goals > best:
            best = goals
            winner = team
    
    print(winner)

solve()
```

The solution starts by reading the number of goals. A dictionary named `count` stores how many times each team appears.

The expression:

```
count.get(team, 0) + 1
```

is important because it handles both cases cleanly. If the team already exists in the dictionary, we increment its current value. Otherwise, `get` returns `0`, and the team starts with one goal.

After counting all goals, we scan the dictionary once more to find the maximum frequency. Since the problem guarantees a unique winner, we never need tie-handling logic.

Using `strip()` when reading team names avoids accidental newline characters becoming part of the string. Forgetting this is a common bug in string problems.

## Worked Examples

### Example 1

Input:

```
1
ABC
```

Trace:

| Step | Team Read | count Dictionary | Current Winner |
| --- | --- | --- | --- |
| 1 | ABC | {"ABC": 1} | ABC |

Output:

```
ABC
```

This example demonstrates the smallest valid input. Only one team appears, so it automatically wins.

### Example 2

Input:

```
5
A
B
A
A
B
```

Trace:

| Step | Team Read | count Dictionary | Current Leader |
| --- | --- | --- | --- |
| 1 | A | {"A": 1} | A |
| 2 | B | {"A": 1, "B": 1} | Tie |
| 3 | A | {"A": 2, "B": 1} | A |
| 4 | A | {"A": 3, "B": 1} | A |
| 5 | B | {"A": 3, "B": 2} | A |

Output:

```
A
```

This trace shows that the dictionary always reflects the exact score after every processed goal. Even though team `B` scores again at the end, team `A` still finishes with more goals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each goal is processed once |
| Space | O(k) | The dictionary stores one entry per distinct team |

Since `n ≤ 100`, the solution easily fits within the limits. The dictionary contains at most two entries, so memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    count = {}

    for _ in range(n):
        team = input().strip()
        count[team] = count.get(team, 0) + 1

    winner = ""
    best = 0

    for team, goals in count.items():
        if goals > best:
            best = goals
            winner = team

    print(winner)

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
assert run("1\nABC\n") == "ABC\n", "sample 1"

# minimum size input
assert run("1\nTEAM\n") == "TEAM\n", "single team"

# alternating goals
assert run("5\nA\nB\nA\nB\nA\n") == "A\n", "alternating sequence"

# all goals by same team
assert run("4\nX\nX\nX\nX\n") == "X\n", "all equal"

# long names
assert run("3\nBARCELONA\nREALMADRID\nBARCELONA\n") == "BARCELONA\n", "string handling"

# winner decided late
assert run("7\nA\nB\nB\nA\nA\nB\nA\n") == "A\n", "late lead"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / TEAM` | `TEAM` | Minimum valid input |
| Alternating A/B goals | `A` | Correct cumulative counting |
| All goals by one team | `X` | Single distinct team handling |
| Long uppercase names | `BARCELONA` | Proper string processing |
| Winner decided near end | `A` | Correct final comparison |

## Edge Cases

Consider the case where only one team appears:

```
1
ABC
```

Execution trace:

1. Read `"ABC"`.
2. Store `count["ABC"] = 1`.
3. The dictionary contains only one entry.
4. That entry is selected as the winner.

The algorithm correctly prints:

```
ABC
```

No special-case handling is needed because the dictionary naturally supports a single team.

Now consider repeated updates to the same team:

```
5
A
B
A
A
B
```

The dictionary evolves as:

```
{"A": 1}
{"A": 1, "B": 1}
{"A": 2, "B": 1}
{"A": 3, "B": 1}
{"A": 3, "B": 2}
```

The algorithm never overwrites counts incorrectly because every occurrence increments the previous value.

Finally, consider a case where the winner changes during processing:

```
7
A
B
B
A
A
B
A
```

Intermediate leaders fluctuate, but the algorithm does not rely on temporary leaders. It only uses the final frequencies:

```
A -> 4
B -> 3
```

The final output is:

```
A
```

This confirms that counting globally across the full input is the correct strategy.
