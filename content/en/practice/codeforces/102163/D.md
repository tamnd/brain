---
title: "CF 102163D - Football Cup"
description: "The match result depends only on the final goal counts. For each test case, X is the number of goals scored by Bashar's team and Y is the number scored by Hamada's team. We must compare these two integers and print the name of the team with more goals."
date: "2026-08-19T07:43:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "D"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 136
verified: false
draft: false
---

[CF 102163D - Football Cup](https://codeforces.com/problemset/problem/102163/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

The match result depends only on the final goal counts. For each test case, `X` is the number of goals scored by Bashar's team and `Y` is the number scored by Hamada's team. We must compare these two integers and print the name of the team with more goals. If the two values are equal, the result is a draw and we print `Iskandar`.

The input contains `T` independent matches, so each pair of scores can be processed without knowing anything about the other test cases. The score of either team can be as large as `10^5`, which is tiny for integer comparison. Even if `T` is large, a constant amount of work per test case is easily fast enough for a 1 second limit. There is no need for loops over the possible score values, simulation of the match, or any data structure. Any approach more complicated than linear in the number of test cases is solving information that the problem never asks for.

The main edge cases come from equality and the smallest possible scores. A score of `0 0` must produce `Iskandar`, because neither team has more goals. A careless implementation that checks only whether `X > Y` and otherwise prints `Hamada` would incorrectly report a Hamada win.

For example:

```
1
0 0
```

The correct output is:

```
Iskandar
```

Equality also matters when both teams have positive scores. For `3 3`, the correct result is again `Iskandar`. Treating `X >= Y` as a Bashar win would silently turn this draw into a win for Bashar.

Finally, the comparison must be symmetric. For `1 5`, Hamada wins, while for `5 1`, Bashar wins. An implementation that accidentally reverses the two variables will produce the opposite result on both cases.

## Approaches

A brute-force approach could simulate the possible outcomes by repeatedly comparing or processing score values until one team is established as the winner. Such a method is unnecessary, but even a simple loop that performs one operation per possible goal would take up to `10^5` operations for one test case. With `T` test cases, that becomes `10^5 T` operations in the worst case. If `T` were also large, this would quickly become excessive, despite the actual problem requiring only one comparison per test case.

The reason the brute-force idea works is that eventually it can determine which score is larger. The problem is that the final scores already contain exactly that information. There is no hidden state to reconstruct and no sequence of scoring events that affects the answer. The observation that the result is completely determined by the ordering of `X` and `Y` reduces the entire task to three cases: `X > Y`, `X < Y`, and `X == Y`.

This gives a constant amount of work for every test case, so the complete algorithm is linear in the number of test cases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T · 10^5) in the worst case | O(1) | Unnecessarily slow |
| Optimal | O(T) | O(1) auxiliary | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `T`. We need to process exactly that many score pairs.
2. For each test case, read `X` and `Y`, representing Bashar's and Hamada's goal counts respectively.
3. Compare `X` and `Y`. If `X > Y`, Bashar's team has more goals, so print `Bashar`.
4. If `X < Y`, Hamada's team has more goals, so print `Hamada`.
5. If neither value is larger, they must be equal. Print `Iskandar` because the match is a draw.

### Why it works

For every test case, exactly one of the three relations `X > Y`, `X < Y`, or `X == Y` is true. The algorithm assigns the required output to each of these mutually exclusive cases. Since the final score alone determines the winner, there is no other information that could change the result. Thus every test case receives exactly the correct result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        x, y = map(int, input().split())

        if x > y:
            print("Bashar")
        elif x < y:
            print("Hamada")
        else:
            print("Iskandar")

if __name__ == "__main__":
    solve()
```

The first line gives the number of independent test cases, so the `for` loop executes exactly `T` times. Each iteration reads two integers in the order specified by the problem, with `x` always representing Bashar's score and `y` representing Hamada's score.

The three branches correspond directly to the three possible relationships between two integers. The equality check is placed in the final `else`, because once both `x > y` and `x < y` are false, the only remaining possibility is `x == y`.

There are no off-by-one concerns because the algorithm does not iterate over score values. Python integers also have no overflow issue for these constraints. The use of `sys.stdin.readline` provides fast input handling, while the output is produced once per test case.

## Worked Examples

For the first sample test case, the scores are `1` for Bashar and `5` for Hamada.

| Step | X | Y | Comparison | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | `1 < 5` | `Hamada` |

Hamada's score is larger, so the second branch is selected. This demonstrates that the variable order matters: `X` is always Bashar's score and `Y` is always Hamada's.

For the third and fourth sample cases, both teams have equal scores.

| Step | X | Y | Comparison | Output |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | `0 == 0` | `Iskandar` |
| 2 | 3 | 3 | `3 == 3` | `Iskandar` |

Both cases reach the equality branch. The first uses the minimum possible scores, while the second confirms that equality must also be handled correctly when the scores are positive.

For the final sample case, Bashar scores `6` and Hamada scores `2`.

| Step | X | Y | Comparison | Output |
| --- | --- | --- | --- | --- |
| 1 | 6 | 2 | `6 > 2` | `Bashar` |

The first comparison succeeds, so the algorithm immediately identifies Bashar's team as the winner.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires one integer comparison and constant additional work. |
| Space | O(1) auxiliary | Only the current pair of scores and a few control variables are needed. |

The scores are at most `10^5`, so the integer operations are trivial. More importantly, the algorithm performs only one comparison per test case, making it comfortably fast even when the number of test cases is large. The solution also uses constant auxiliary memory, far below the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        x, y = map(int, input().split())

        if x > y:
            out.append("Bashar")
        elif x < y:
            out.append("Hamada")
        else:
            out.append("Iskandar")

    print("\n".join(out))

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            solve()
            return sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
    finally:
        sys.stdin = old_stdin
        input = old_input

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
100000 0
0 100000
100000 100000
""") == """Bashar
Hamada
Iskandar
""", "maximum scores and equality"

assert run("""4
1 2
2 1
99999 100000
100000 99999
""") == """Hamada
Bashar
Hamada
Bashar
""", "boundary comparisons"

assert run("""3
7 7
1 1
99999 99999
""") == """Iskandar
Iskandar
Iskandar
""", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0` | `Iskandar` | Minimum possible scores and equality |
| `3 / 100000 0 / 0 100000 / 100000 100000` | `Bashar / Hamada / Iskandar` | Maximum score boundary and all three comparison outcomes |
| `4 / 1 2 / 2 1 / 99999 100000 / 100000 99999` | `Hamada / Bashar / Hamada / Bashar` | Adjacent scores and correct comparison direction |
| `3 / 7 7 / 1 1 / 99999 99999` | `Iskandar / Iskandar / Iskandar` | Equality for different positive scores |

## Edge Cases

The `0 0` case is the smallest possible input for the score values:

```
1
0 0
```

The algorithm first checks `0 > 0`, which is false, then `0 < 0`, which is also false. It reaches the `else` branch and prints `Iskandar`. This prevents the common mistake of treating every non-Bashar result as a Hamada win.

For equal positive scores, consider:

```
1
3 3
```

Again, neither strict comparison succeeds. Since both scores are exactly equal, the algorithm prints `Iskandar`. This catches implementations that use `>=` instead of `>` for the Bashar branch.

The maximum-score boundary can be tested with:

```
2
100000 0
0 100000
```

The first pair satisfies `X > Y`, producing `Bashar`, while the second satisfies `X < Y`, producing `Hamada`. The bound of `10^5` does not require any special handling because ordinary integer comparison is sufficient.

Finally, adjacent scores expose reversed comparison mistakes:

```
2
1 2
2 1
```

The first test prints `Hamada` because `1 < 2`, and the second prints `Bashar` because `2 > 1`. No simulation is needed. The complete problem is exactly the ordering relationship between the two final scores.
