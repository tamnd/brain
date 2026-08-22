---
title: "CF 102163D - Football Cup"
description: "The match result depends only on the final goal counts. For every test case, X is the number of goals scored by Bashar's team and Y is the number scored by Hamada's team."
date: "2026-08-22T18:30:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "D"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 2345
verified: true
draft: false
---

[CF 102163D - Football Cup](https://codeforces.com/problemset/problem/102163/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The match result depends only on the final goal counts. For every test case, `X` is the number of goals scored by Bashar's team and `Y` is the number scored by Hamada's team. We need to compare these two integers and print the name of the winning team, or `Iskandar` when the scores are equal.

The story about players, injuries, substitutions, and match periods does not affect the computation. Once the final scores are known, every possible result falls into exactly one of three cases: `X > Y`, `X < Y`, or `X == Y`.

The values of `X` and `Y` are at most `10^5`, so even a linear scan over one test case would be inexpensive. However, there is no reason to scan anything because the answer is determined by a single comparison. With `T` test cases, an `O(T)` solution performs only a constant amount of work per case, which is easily within a 1 second limit. Any approach that performs work proportional to the score itself would be unnecessary, and a nested process over both scores could reach roughly `10^10` operations for a single pair, which is clearly unsuitable.

There are a few simple cases that can expose careless implementations. If the scores are equal, the result must be `Iskandar`. For example, input `3 3` produces `Iskandar`; using `>=` for Bashar's win would incorrectly print `Bashar`. If Bashar scores zero and Hamada scores more, such as `0 1`, the result is `Hamada`; code that treats zero as a special winning value would be wrong. The reverse boundary case, `1 0`, must produce `Bashar`. Finally, `0 0` is a draw and must produce `Iskandar`, so equality has to be checked explicitly or represented correctly by the comparison structure.

## Approaches

A brute-force approach could simulate the score difference by repeatedly adding one goal to one team's count and eventually comparing the resulting values. For example, to determine whether `X` is larger than `Y`, one could repeatedly remove one goal from both scores until one reaches zero. This is correct because each paired removal preserves which original score was larger. However, in the worst case `X = 100000` and `Y = 99999`, this performs nearly `100000` iterations for one test case. Across a large number of test cases, that unnecessary work can become significant, even though the actual answer requires only one comparison. A more extreme nested simulation could perform up to `10^10` operations, which is far beyond the time limit.

The key observation is that the input already contains the exact quantities needed to determine the winner. There is no hidden state to reconstruct and no sequence of goals to simulate. Comparing the two final scores directly completely characterizes the result. The brute-force works because it eventually discovers the ordering between the two numbers, but the ordering is already available immediately through the comparison operators.

Thus the optimal solution reads `X` and `Y`, compares them once, and prints the corresponding result. Each test case takes constant time, giving `O(T)` total time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T × max(X, Y)) | O(1) | Unnecessarily slow |
| Optimal | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `T`, because the same comparison must be performed independently for every match.
2. For each test case, read `X` and `Y`, representing the final goals of Bashar's and Hamada's teams.
3. If `X > Y`, print `Bashar`. Bashar's team has strictly more goals, so it is the winner.
4. Otherwise, if `X < Y`, print `Hamada`. The previous condition has already ruled out Bashar's win, and Hamada has strictly more goals.
5. Otherwise, the two scores are equal, so print `Iskandar`. This covers draws such as `0 0` and `3 3`.

Why it works: throughout each test case, `X` and `Y` remain the final scores. Exactly one of `X > Y`, `X < Y`, or `X == Y` is true for two integers. The algorithm assigns each of these three mutually exclusive cases to its required output, so it cannot produce an incorrect result.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    x, y = map(int, input().split())

    if x > y:
        print("Bashar")
    elif x < y:
        print("Hamada")
    else:
        print("Iskandar")
```

The first line reads `T`, which controls exactly how many score pairs need to be processed. Using `sys.stdin.readline` provides fast input while keeping the implementation simple.

Inside the loop, `x` and `y` are parsed as integers. Python integers have no overflow issue for these constraints, and the values are far below any practical integer limit.

The comparison order handles the three possible relationships between the scores. The equality case is placed last because if neither strict inequality holds, the only remaining possibility is `x == y`. There are no off-by-one concerns because the problem asks only about the ordering of the final integer scores.

Each result is printed immediately, so there is no need to store all test cases or all answers in memory.

## Worked Examples

For the first sample, consider the first three test cases.

| Test case | `x` | `y` | Comparison | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | `1 < 5` | `Hamada` |
| 2 | 2 | 0 | `2 > 0` | `Bashar` |
| 3 | 0 | 0 | `0 == 0` | `Iskandar` |

The first case confirms that the smaller score loses. The second exercises the boundary where one team has no goals. The third confirms that equality takes the draw branch rather than either winning branch.

For the remaining sample cases:

| Test case | `x` | `y` | Comparison | Output |
| --- | --- | --- | --- | --- |
| 4 | 3 | 3 | `3 == 3` | `Iskandar` |
| 5 | 6 | 2 | `6 > 2` | `Bashar` |

The fourth case shows that a draw is handled independently of the actual score value. The fifth confirms the ordinary winning case when Bashar has a larger score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires one constant-time comparison. |
| Space | O(1) | Only the current pair of scores and the loop state are stored. |

The solution performs a tiny constant amount of work for every test case. Even with the maximum possible score values of `10^5`, the magnitude of the scores has no effect on the running time because the algorithm never iterates over the goals themselves. The memory usage is also constant and comfortably below the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())

    for _ in range(t):
        x, y = map(int, input().split())

        if x > y:
            print("Bashar")
        elif x < y:
            print("Hamada")
        else:
            print("Iskandar")

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
Bashar
""", "sample 1"

assert run("""1
0 0
""") == """Iskandar
""", "minimum scores and draw"

assert run("""3
100000 99999
99999 100000
100000 100000
""") == """Bashar
Hamada
Iskandar
""", "maximum values and adjacent boundary cases"

assert run("""4
1 0
0 1
1 1
2 1
""") == """Bashar
Hamada
Iskandar
Bashar
""", "small scores and equality boundary"

assert run("""2
100000 0
0 100000
""") == """Bashar
Hamada
""", "maximum score against zero")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `Iskandar` | Minimum scores and equality |
| `100000 99999`, `99999 100000`, `100000 100000` | `Bashar`, `Hamada`, `Iskandar` | Maximum values and all three comparison outcomes |
| `1 0`, `0 1`, `1 1`, `2 1` | `Bashar`, `Hamada`, `Iskandar`, `Bashar` | Small boundary values and strict comparisons |
| `100000 0`, `0 100000` | `Bashar`, `Hamada` | Maximum score against the minimum score |

## Edge Cases

The first non-obvious case is a draw. For input `3 3`, the algorithm first checks `3 > 3`, which is false, then checks `3 < 3`, which is also false. It reaches the final `else` branch and prints `Iskandar`. The same reasoning works for `0 0`, so zero does not require a separate special case.

The second case is when Bashar has no goals while Hamada has one. For input `0 1`, `x > y` is false and `x < y` is true, so the algorithm prints `Hamada`. This confirms that zero is treated as an ordinary score.

The reverse case, input `1 0`, reaches the first branch because `1 > 0`, producing `Bashar`. No special handling for the lower bound is needed.

At the upper boundary, input `100000 99999` produces `Bashar` because the first comparison is true. Input `99999 100000` produces `Hamada`, and `100000 100000` produces `Iskandar`. These cases demonstrate that the algorithm remains correct at the maximum allowed values and around the equality boundary.
