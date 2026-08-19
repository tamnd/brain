---
title: "CF 102163D - Football Cup"
description: "The match result depends only on the final goal counts. For each test case, X is the number of goals scored by Bashar's team and Y is the number scored by Hamada's team."
date: "2026-08-19T14:43:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "D"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 279
verified: false
draft: false
---

[CF 102163D - Football Cup](https://codeforces.com/problemset/problem/102163/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 39s  
**Verified:** no  

## Solution
## Problem Understanding

The match result depends only on the final goal counts. For each test case, `X` is the number of goals scored by Bashar's team and `Y` is the number scored by Hamada's team. The task is to compare these two integers and print `Bashar` when `X` is larger, `Hamada` when `Y` is larger, and `Iskandar` when they are equal.

The original story contains many details about players, injuries, substitutions, and match duration, but none of those values affect the requested result. Once the two final scores are provided, the entire problem reduces to one comparison.

Each score is between `0` and `100000`, so the values fit comfortably in standard integer types. More importantly, the range does not need to be explored at all. Even if there are many test cases, a solution that performs a constant amount of work per case is easily fast enough for a 1 second limit. An approach that spends `O(100000)` operations on every test case would already be unnecessarily expensive, while anything quadratic in the score range would be completely inappropriate.

There are a few simple cases where an implementation can go wrong. When Bashar has more goals, such as

```
1
6 2
```

the correct output is `Bashar`. A careless implementation that checks only whether the scores are equal could incorrectly treat every non-draw as the same result.

When Hamada has more goals, such as

```
1
1 5
```

the correct output is `Hamada`. Reversing the comparison would silently produce the wrong winner.

The equality case is also essential:

```
1
3 3
```

The correct output is `Iskandar`. An implementation using only `if X > Y` and `else` would incorrectly print `Hamada`, because equality must be handled separately.

Finally, zero is a valid score for either team. For

```
1
0 0
```

the result is `Iskandar`, so the comparison must work without assuming that either team scored at least once.

## Approaches

A deliberately brute-force approach could examine score values one by one and try to determine which of the two given scores is larger by scanning through the possible range from `0` to `100000`. This eventually gives the correct answer because every valid score lies inside that range, but it completely ignores the fact that the two actual values are already available. In the worst case, this performs `100001` iterations for one test case. If there were `100000` test cases, that would reach about `10^10` iterations, which is far beyond what a 1 second limit allows.

The brute-force works because it eventually encounters the relevant score values, but fails because it spends time exploring values that have nothing to do with the answer. The key observation is that determining the winner requires no search at all. The relationship between the two given scores is already the complete answer: greater means that team wins, smaller means the other team wins, and equality means a draw.

Thus each test case needs exactly one comparison and one output decision. This reduces the work from depending on the score range to a constant amount per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(T * 100000)` | `O(1)` | Too slow and unnecessary |
| Optimal | `O(T)` | `O(T)` for collected output | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `T`. Each following test case contains the final scores of the two teams.
2. For every test case, read `X` and `Y`. No simulation of the football match is necessary because the input already gives the final result of the scoring process.
3. Compare `X` and `Y`. If `X > Y`, Bashar's team has more goals, so the answer is `Bashar`.
4. If `X < Y`, Hamada's team has more goals, so the answer is `Hamada`.
5. If neither score is larger, they must be equal. In that case, print `Iskandar`.
6. Store each answer and print all answers after processing the input. Collecting the strings also avoids repeatedly calling `print` for every individual test case.

### Why it works

For every test case, exactly one of three mutually exclusive relationships holds between `X` and `Y`: `X > Y`, `X < Y`, or `X = Y`. The algorithm maps these three possibilities directly to the three required outcomes, `Bashar`, `Hamada`, and `Iskandar`. Since the winner is defined solely by which final score is greater, the selected result is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        x, y = map(int, input().split())

        if x > y:
            answers.append("Bashar")
        elif x < y:
            answers.append("Hamada")
        else:
            answers.append("Iskandar")

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The first line reads `T`, which tells the program exactly how many score pairs follow. The loop then processes one complete match result at a time.

The three-way `if` structure directly implements the algorithm. The strict comparisons handle the two possible winners, while the final `else` represents equality. There is no need for special handling of zero or the maximum score because ordinary integer comparison already handles both boundaries correctly.

The scores are at most `100000`, so integer overflow is not a concern in Python. In fact, the program never performs arithmetic on the scores at all, only comparisons.

The answers are accumulated in a list and joined with newline characters at the end. This keeps output handling efficient when the number of test cases is large.

## Worked Examples

Consider the first two test cases from Sample 1.

| Test case | `X` | `Y` | Comparison | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | `1 < 5` | `Hamada` |
| 2 | 2 | 0 | `2 > 0` | `Bashar` |

For the first match, Hamada has five goals against Bashar's one, so the second branch produces `Hamada`. For the second match, Bashar has two goals while Hamada has none, so the first branch produces `Bashar`. These cases demonstrate both directions of the comparison.

The equality case from Sample 1 gives another useful trace.

| Test case | `X` | `Y` | Comparison | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | `0 == 0` | `Iskandar` |
| 2 | 3 | 3 | `3 == 3` | `Iskandar` |

Neither strict comparison succeeds for either row. The algorithm reaches the equality case and outputs `Iskandar`. This confirms that a zero-zero score and a positive draw are treated identically, as required.

The final two rows of Sample 1 exercise both the larger-score boundary direction and another ordinary win.

| Test case | `X` | `Y` | Comparison | Answer |
| --- | --- | --- | --- | --- |
| 1 | 6 | 2 | `6 > 2` | `Bashar` |
| 2 | 2 | 0 | `2 > 0` | `Bashar` |

The invariant throughout every row is that the answer is determined solely by the ordering of the two current scores. No information from another test case affects the current decision.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(T)` | Each test case performs one comparison and constant additional work |
| Space | `O(T)` | The output strings are stored before being printed |

The score limit of `100000` does not affect the running time because the algorithm never iterates over possible scores. Even a large number of test cases requires only one constant-time comparison per case, which comfortably fits the 1 second limit. The memory usage is also small because each test case contributes only one short output string.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    answers = []

    for _ in range(t):
        x, y = map(int, input().split())

        if x > y:
            answers.append("Bashar")
        elif x < y:
            answers.append("Hamada")
        else:
            answers.append("Iskandar")

    sys.stdout.write("\n".join(answers))

def run(inp: str) -> str:
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

# Provided sample
assert run("""5
1 5
2 0
0 0
3 3
6 2
""") == """Hamada
Bashar
Iskandar
Iskandar
Bashar""", "sample 1"

# Minimum-size scores
assert run("""1
0 0
""") == "Iskandar", "minimum scores"

# Maximum-size scores
assert run("""2
100000 99999
99999 100000
""") == """Bashar
Hamada""", "maximum scores"

# Several equal scores
assert run("""3
1 1
50000 50000
100000 100000
""") == """Iskandar
Iskandar
Iskandar""", "all equal"

# Boundary and near-boundary comparisons
assert run("""4
0 1
1 0
99999 100000
100000 99999
""") == """Hamada
Bashar
Hamada
Bashar""", "boundary comparisons"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0` | `Iskandar` | Minimum scores and the equality branch |
| `2 / 100000 99999 / 99999 100000` | `Bashar / Hamada` | Maximum allowed values and both comparison directions |
| `3 / 1 1 / 50000 50000 / 100000 100000` | `Iskandar` three times | Equality at several score sizes |
| `4 / 0 1 / 1 0 / 99999 100000 / 100000 99999` | `Hamada / Bashar / Hamada / Bashar` | Values immediately around the boundaries and reversed comparisons |

## Edge Cases

For equal scores, consider the input

```
1
3 3
```

The algorithm first checks `3 > 3`, which is false, then checks `3 < 3`, which is also false. The remaining possibility is equality, so it outputs `Iskandar`. The same reasoning works for `0 0` and `100000 100000`.

For a zero score on one side, consider

```
1
0 7
```

The first comparison, `0 > 7`, is false. The second comparison, `0 < 7`, is true, so the output is `Hamada`. There is no special zero case because zero behaves normally under integer comparison.

The reversed situation is

```
1
7 0
```

Here `7 > 0` is true, so the output is `Bashar`. Testing both `0 7` and `7 0` catches implementations that accidentally swap the two input variables or winner names.

At the upper boundary,

```
1
100000 99999
```

gives `Bashar`, while

```
1
99999 100000
```

gives `Hamada`. The algorithm performs the same two comparisons as it does for smaller values, so there is no off-by-one issue at `100000`.

The central edge case is equality, because a two-branch implementation such as `if X > Y: Bashar else: Hamada` treats equality as a Hamada win. The explicit third outcome is what separates a correct solution from that common mistake.
