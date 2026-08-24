---
title: "CF 102219C - I Don't Want To Pay For The Late Jar!"
description: "Nina has a list of restaurants. For each restaurant, she knows two values: fi, the amount of money she considers the restaurant worth, and ti, the number of minutes she needs to have lunch there. Her available lunch time is S minutes, and she must choose exactly one restaurant."
date: "2026-08-24T07:26:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102219
codeforces_index: "C"
codeforces_contest_name: "2019 ICPC Malaysia National"
rating: 0
weight: 102219
solve_time_s: 2304
verified: false
draft: false
---

[CF 102219C - I Don't Want To Pay For The Late Jar!](https://codeforces.com/problemset/problem/102219/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 38m 24s  
**Verified:** no  

## Solution
## Problem Understanding

Nina has a list of restaurants. For each restaurant, she knows two values: `f_i`, the amount of money she considers the restaurant worth, and `t_i`, the number of minutes she needs to have lunch there. Her available lunch time is `S` minutes, and she must choose exactly one restaurant.

If a restaurant fits completely inside the lunch break, meaning `t_i <= S`, Nina keeps the full value `f_i`. If the restaurant takes longer, the extra `t_i - S` minutes are treated as money paid to the late jar, so her final saving becomes `f_i - (t_i - S)`. The task is simply to find the largest final saving among all restaurants.

The expression can be written more compactly as

`value_i = f_i - max(0, t_i - S)`.

The number of restaurants is at most `10^4`, and there are at most `10` days. Even checking every restaurant once per day requires only about `10^5` evaluations, which is tiny for a 1 second time limit. The values themselves can reach `10^9`, and subtracting the lateness penalty can make the answer negative, so the implementation must use integer arithmetic without assuming the answer is nonnegative. Python integers handle this range directly.

The main edge cases come from the boundary at exactly `S` minutes and from restaurants that are late enough to produce a negative saving.

Consider a restaurant that takes exactly the available time:

```
1
1 5
10 5
```

The correct output is:

```
Case #1: 10
```

A careless implementation using `t_i >= S` as the condition for being late would subtract a penalty of one or more minutes incorrectly. The penalty is zero when `t_i == S`.

A restaurant can also have a negative final value:

```
1
1 5
1 7
```

The correct output is:

```
Case #1: -1
```

There is no requirement that Nina can choose to skip lunch or choose a restaurant with nonnegative value. She must choose exactly one restaurant, so the maximum can legitimately be negative.

Another useful boundary case has several restaurants with the same best value:

```
1
3 5
10 5
8 3
20 8
```

The first restaurant gives `10`, the second gives `8`, and the third gives `17`. The correct answer is `17`. The algorithm only needs the maximum value, so ties require no special handling.

## Approaches

The direct approach is already the right approach here. For every restaurant, calculate how much of its nominal value survives after paying for any minutes beyond the available lunch time. If `t_i <= S`, the candidate value is simply `f_i`. Otherwise, it is `f_i - (t_i - S)`. Keep the largest candidate seen so far.

This is correct because the choice consists of exactly one restaurant. Every possible choice is examined, and its final saving is calculated according to the rules. Once all restaurants have been considered, the largest candidate is exactly the best possible choice.

A brute-force interpretation might suggest trying every restaurant and performing some additional search or sorting, but none of that is necessary. The quantity associated with a restaurant depends only on that restaurant and the fixed value `S`. There is no interaction between two restaurants, so evaluating one restaurant gives all the information needed about that restaurant.

For one day with `N` restaurants, the algorithm performs exactly `N` candidate evaluations and `N` maximum comparisons in the worst case. Across `D` days, this is at most `D * N`, which is at most `10 * 10^4 = 10^5` restaurant evaluations. Any approach that sorts the restaurants would add unnecessary `O(N log N)` work.

The key observation is that this problem does not require a sophisticated optimization technique. The formula converts every restaurant into one independent score, and the required answer is simply the maximum score. A single pass is both sufficient and asymptotically optimal because every restaurant must be considered at least once: an unseen restaurant could always have a better value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(DN) | O(1) | Accepted |
| Optimal single pass | O(DN) | O(1) | Accepted |

Here the so-called brute force and optimal solution are effectively the same algorithm. The distinction is that there is no hidden combinatorial search to eliminate. The important optimization is recognizing that checking every restaurant once is already enough.

## Algorithm Walkthrough

1. Read the number of days `D`. Each day is an independent problem, so the answer for one day does not affect any other day.
2. For the current day, read `N` and `S`. `N` tells us how many restaurants must be examined, while `S` is the common lunch-time limit used to calculate every restaurant's penalty.
3. Initialize the best saving to a value smaller than any possible candidate. Since the answer may be negative, initializing it to zero would be incorrect. Using a very small integer, or initializing from the first restaurant, avoids silently discarding negative answers.
4. Read each restaurant's `f_i` and `t_i`. If `t_i <= S`, calculate the candidate as `f_i`. Otherwise calculate it as `f_i - (t_i - S)`. The subtraction is exactly the number of late minutes that Nina has to pay for.
5. Compare the candidate with the best saving found so far and retain the larger value. Since every restaurant is independent, there is no reason to retain any information about a restaurant after its candidate has been compared with the current maximum.
6. After all `N` restaurants have been processed, print the maximum using the required `Case #x:` format. Repeat the same process for every day.

### Why it works

After processing any prefix of the restaurants, the maintained `best` value is the maximum final saving among exactly those restaurants. The next restaurant is converted into its correct final saving and compared with that maximum, so after the comparison the invariant remains true for the larger prefix. Once all restaurants have been processed, `best` is consequently the maximum final saving over every legal choice. Since Nina must choose exactly one restaurant, that maximum is precisely the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    d = int(input())

    answers = []

    for case in range(1, d + 1):
        n, s = map(int, input().split())

        best = -10**30

        for _ in range(n):
            f, t = map(int, input().split())

            late = max(0, t - s)
            value = f - late

            if value > best:
                best = value

        answers.append(f"Case #{case}: {best}")

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The outer loop processes each independent day and also supplies the case number required by the output format. The restaurant loop processes exactly `N` pairs for that day.

The expression `max(0, t - s)` handles both sides of the boundary in one operation. When `t < s`, the penalty is zero. When `t == s`, it is also zero, which is the crucial boundary condition. Only when `t > s` does the penalty become positive.

The initial value `-10**30` is deliberately negative. Since `f_i` and `t_i` are at most `10^9`, the worst possible candidate is `1 - (10^9 - 1) = -999999999`, so `-10**30` is safely below every valid answer. Python also has arbitrary-precision integers, so there is no overflow concern.

The code does not store the restaurants. Each one is used immediately to calculate a candidate and then discarded. This gives constant auxiliary space.

The input contains blank lines in the sample between test cases, but `map(int, input().split())` handles ordinary nonempty lines correctly. Codeforces inputs for this problem provide the expected structured lines, so no special blank-line parser is needed.

## Worked Examples

For the first sample, the first day has `S = 5` and two restaurants. The relevant state changes are:

| Restaurant | `f` | `t` | `late = max(0, t-S)` | `value` | `best` |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 0 | 3 | 3 |
| 2 | 4 | 5 | 0 | 4 | 4 |

Both restaurants finish within the available five minutes. The second restaurant has the larger nominal value, so the answer is `4`.

For the second day, there is one restaurant with `S = 5`:

| Restaurant | `f` | `t` | `late = max(0, t-S)` | `value` | `best` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 7 | 2 | -1 | -1 |

The restaurant takes two minutes longer than the allowed time, so Nina loses `2` from its value of `1`. The resulting saving is `-1`, and because she must choose a restaurant, `-1` is the answer.

The complete sample output is consequently:

```
Case #1: 4
Case #2: -1
```

This trace demonstrates why `best` cannot start at zero. On the second day, every available choice has a negative value, and the correct answer must preserve that negative result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(DN) | Every restaurant is read and evaluated exactly once. |
| Space | O(1) | Only the current restaurant, the current maximum, and a few scalar variables are stored. |

With at most `10` days and `10^4` restaurants per day, the algorithm performs at most `10^5` restaurant evaluations. This is comfortably within the time limit, and the constant auxiliary memory is far below the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    d = int(input())
    answers = []

    for case in range(1, d + 1):
        n, s = map(int, input().split())
        best = -10**30

        for _ in range(n):
            f, t = map(int, input().split())
            value = f - max(0, t - s)
            best = max(best, value)

        answers.append(f"Case #{case}: {best}")

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
assert run("""\
2
2 5
3 3
4 5

1 5
1 7
""") == """\
Case #1: 4
Case #2: -1
""", "sample"

# Minimum-size input
assert run("""\
1
1 1
1 1
""") == """\
Case #1: 1
""", "minimum-size case"

# Boundary and negative-answer case
assert run("""\
1
3 5
10 4
7 5
1 6
""") == """\
Case #1: 7
""", "boundary at exactly S"

# All values equal, with different lunch times
assert run("""\
1
4 10
10 10
10 8
10 11
10 15
""") == """\
Case #1: 10
""", "all equal nominal values"

# Large values and a late restaurant with a better final score
assert run("""\
1
3 1000000000
1000000000 1000000000
999999999 1
1000000000 1000000001
""") == """\
Case #1: 1000000000
""", "large boundary values"

# Multiple days and all answers negative
assert run("""\
2
2 3
1 5
2 6
3 4
1 10
""") == """\
Case #1: -1
Case #2: -6
""", "negative answers across multiple cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1 1` | `Case #1: 1` | Minimum input size and exact-time boundary |
| `1 / 3 5 / 10 4 / 7 5 / 1 6` | `Case #1: 7` | Restaurants before, exactly at, and after `S` |
| `1 / 4 10 / 10 10 / 10 8 / 10 11 / 10 15` | `Case #1: 10` | Equal nominal values and zero penalty |
| `1 / 3 1000000000 / ...` | `Case #1: 1000000000` | Values near the maximum constraint and large `S` |
| Two days with late restaurants | `Case #1: -1`, `Case #2: -6` | Negative answers and independent test cases |

## Edge Cases

The exact-time boundary is handled by the condition inside `max(0, t - S)`. For

```
1
1 5
10 5
```

the penalty is `max(0, 5 - 5) = 0`, so the candidate is `10` and the output is `Case #1: 10`. Treating equality as late would incorrectly reduce the answer.

A negative answer is handled because the initial `best` is deliberately below every possible candidate. For

```
1
1 5
1 7
```

the penalty is `7 - 5 = 2`, giving `1 - 2 = -1`. The comparison updates `best` from the initial sentinel to `-1`, producing `Case #1: -1`. Initializing `best` to zero would incorrectly output zero, which represents an option Nina does not have.

A restaurant that is comfortably within the lunch limit incurs no penalty. For

```
1
2 10
8 3
10 10
```

the first restaurant produces `8` and the second produces `10`, so the answer is `Case #1: 10`. The algorithm never subtracts the unused lunch time because only time beyond `S` is charged.

Finally, the restaurant with the largest `f_i` does not necessarily win. For

```
1
3 5
10 5
100 200
20 6
```

the candidate values are `10`, `-95`, and `19`. The third restaurant wins even though its nominal value is much smaller than `100`. The algorithm compares the final savings rather than sorting or selecting restaurants by `f_i` alone, which is exactly what the problem asks for.
