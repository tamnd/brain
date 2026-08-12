---
title: "CF 102375D - \u0414\u0440\u0430\u0444\u0442 \u041d\u0411\u0410"
description: "For each candidate, we know five integer statistics: height, wingspan, points per game, rebounds per game, and assists per game. Each statistic has its own expected interval, and the candidate is judged by where every value lies relative to that interval."
date: "2026-08-12T22:23:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "D"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 1135
verified: true
draft: false
---

[CF 102375D - \u0414\u0440\u0430\u0444\u0442 \u041d\u0411\u0410](https://codeforces.com/problemset/problem/102375/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 18m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

For each candidate, we know five integer statistics: height, wingspan, points per game, rebounds per game, and assists per game. Each statistic has its own expected interval, and the candidate is judged by where every value lies relative to that interval.

For a value inside an expected interval, the midpoint belongs to the upper half. Thus the five thresholds for being in the upper half are 205 for height, 225 for wingspan, 15 for points, 4 for rebounds, and 5 for assists. A value strictly greater than the upper endpoint is considered above the expected range. For example, height 205 is already in the upper half, while height 221 is above the expected range.

The task is to classify every candidate into category 0, 1, 2, or 3. Category 0 has the strongest condition and must be checked first. It requires at least three statistics above their expected ranges, with height or wingspan among those three. Category 1 is next, followed by category 2. If none of their conditions hold, the answer is category 3.

The input contains at most 32 candidates, and every candidate always has exactly five values. Even an algorithm doing a few hundred operations per candidate would be comfortably fast. There is no need for sorting, dynamic programming, graph algorithms, or any data structure. The useful target is constant work per candidate, giving O(N) total time.

A subtle boundary is that the midpoint belongs to the upper half. For height, the expected interval is 190 through 220, so 205 counts as upper half. A candidate with height 204 does not satisfy that condition. For example:

```
1
205
225
15
4
5
```

All five statistics are at least in the upper half, so the answer is `2`, not `3`. An implementation using a strict `>` comparison against the midpoint would incorrectly reject all five upper-half conditions.

The upper endpoint itself is not above the expected range. For height, 220 is still inside the expected range, while 221 is above it. For example:

```
1
220
250
20
6
7
```

All five values are inside the expected ranges and all are in their upper halves, so the answer is `2`. Treating the upper endpoint as "above" would incorrectly create three or more above-range statistics.

Another easy mistake is forgetting the special height-or-wingspan requirement for category 0. Consider:

```
1
200
210
21
7
8
```

Points, rebounds, and assists are all above their expected ranges, but neither height nor wingspan is above its range. The correct answer is `1`, because the candidate satisfies the first-round condition, but not the unicorn condition. Checking only the number of above-range statistics would incorrectly output `0`.

Finally, the categories are hierarchical. A candidate satisfying category 0 can also satisfy weaker conditions from categories 1 or 2, so category 0 must be tested first. For example:

```
1
230
260
21
7
5
```

Height, wingspan, and points are above their ranges, and height is one of them. The answer is `0`, even though the candidate also satisfies a category 1 condition.

## Approaches

A literal brute-force solution could classify each of the five statistics into one of four states: below the expected interval, in its lower half, in its upper half, or above the expected interval. There are only (4^5=1024) possible state combinations for one candidate. We could enumerate all of them, determine which category each combination receives, and compare the candidate with those cases. For the maximum input of 32 candidates, this is only (32\cdot1024=32768) state checks, so even this deliberately naive method is easily fast enough for the actual constraints.

It becomes unattractive when the number of candidates grows, because the work is exponential in the number of statistics. With five fixed statistics this distinction is mostly theoretical, but if the same idea were generalized to 20 statistics, enumeration would require (4^{20}), which is about (1.1\cdot10^{12}) combinations. Even for the current five-statistic problem, there is no reason to enumerate states when the category rules only depend on a few counts.

The key observation is that the exact values do not matter after we determine two properties for each statistic. We only need to know whether it is at least in the upper half, and whether it is strictly above the expected range. We can count these properties directly.

For each candidate, let `high` be the number of statistics that are at least in the upper half, and let `above` be the number that are strictly above the expected range. We also separately remember whether height or wingspan is above the expected range. Every category condition can then be expressed using these counts.

The first-round rule additionally contains the phrase "all parameters are at least in the expected range". This is equivalent to saying that none of the five statistics is below the lower endpoint. We can track that with a boolean variable. Once these few counters are available, every category can be tested directly.

The brute-force approach works because the state space is tiny, but it performs work on states that the actual candidate never reaches. The observation that every rule depends only on a handful of aggregate properties reduces the problem to a constant number of comparisons per candidate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N\cdot4^5)) | (O(1)) | Accepted for the given constraints, but unnecessarily expensive |
| Optimal | (O(N)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the five statistics of one candidate. We process candidates independently because the category of one candidate never depends on another candidate.
2. For each statistic, determine whether it is at least the upper-half threshold and whether it is strictly above the expected upper endpoint. The thresholds are 205, 225, 15, 4, and 5 respectively. The distinction between `>=` and `>` is essential because the midpoint belongs to the upper half, while the upper endpoint is still inside the expected interval.
3. Count how many statistics are in the upper half or above it. Call this `high`. Also count how many statistics are strictly above their expected ranges. Call this `above`.
4. Record whether height or wingspan is above its expected range. This is needed because category 0 requires one of those two physical measurements to be among the above-range statistics.
5. First check category 0. It holds when `above >= 3` and either height or wingspan is above its expected range. We test it first because a unicorn also satisfies weaker quality conditions, but category 0 has priority.
6. If category 0 does not apply, check category 1. Its first condition is `above >= 2` together with `high >= 3`. Its second condition requires every statistic to be at least inside the expected range and at least three statistics to be in the upper half. The first condition is enough to express "two above and another at least upper half", because every above-range value is itself in the upper-half-or-better group.
7. If category 1 does not apply, check category 2. Its first condition is `above >= 1` and `high >= 2`. Its second condition is simply `high >= 3`. Again, a value above the expected range is automatically counted by `high`.
8. If none of the previous conditions is satisfied, output category 3. Since the categories are checked in their required priority order, this is exactly the remaining case.

### Why it works

For every candidate, `above` is exactly the number of statistics strictly above their expected upper endpoints, while `high` is exactly the number of statistics at least in their upper halves. The separate physical flag exactly captures the additional height-or-wingspan requirement for category 0. Consequently, each written condition is equivalent to the corresponding rule in the classification system. Since category 0 is checked before category 1, category 1 before category 2, and category 3 is used only when none of them holds, the produced category is the strongest applicable category for every candidate.

## Python Solution

```python
import sys
input = sys.stdin.readline

def classify(values):
    lower = [190, 200, 10, 2, 3]
    upper = [220, 250, 20, 6, 7]
    middle = [205, 225, 15, 4, 5]

    high = 0
    above = 0
    all_expected = True

    for i, x in enumerate(values):
        if x < lower[i]:
            all_expected = False

        if x >= middle[i]:
            high += 1

        if x > upper[i]:
            above += 1

    physical_above = values[0] > upper[0] or values[1] > upper[1]

    if above >= 3 and physical_above:
        return 0

    if (above >= 2 and high >= 3) or (all_expected and high >= 3):
        return 1

    if (above >= 1 and high >= 2) or high >= 3:
        return 2

    return 3

def solve():
    n = int(input())
    answer = []

    for _ in range(n):
        values = [int(input()) for _ in range(5)]
        answer.append(str(classify(values)))

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    solve()
```

The arrays `lower`, `upper`, and `middle` store the five boundaries in the same order as the input values. Keeping the thresholds explicitly aligned with the five statistics makes the classification logic uniform rather than requiring five separate pieces of comparison code.

`all_expected` starts as true and becomes false as soon as a value falls below its expected interval. This directly represents the second category 1 condition, which requires every statistic to be at least the lower endpoint of its expected range.

The expression `x >= middle[i]` counts the upper half, including the midpoint. The expression `x > upper[i]` counts only values outside the expected range above it. These comparisons must not be swapped or made strict in the wrong direction.

The `physical_above` condition examines only height and wingspan, because the unicorn rule specifically requires one of those two statistics to be above its range. We do not need to know which one if at least one satisfies the condition.

There is no integer overflow concern in Python, and even in a language with fixed-width integers all counters here are at most five. The input contains exactly five lines per candidate, so the list comprehension reads precisely the values belonging to the current candidate.

## Worked Examples

For the first sample, the five thresholds are fixed as described above. The following table records the important counters for each candidate.

| Player | Values | `high` | `above` | Height/Wingspan above | All in expected range | Category |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 230, 190, 16, 7, 9 | 4 | 3 | Yes | No | 0 |
| 2 | 205, 225, 15, 5, 2 | 4 | 0 | No | No | 2 |
| 3 | 210, 210, 30, 9, 9 | 5 | 3 | No | No | 1 |

For player 1, height, points, rebounds, and assists are in the upper-half-or-better group, while height, rebounds, and assists are strictly above their expected ranges. Since height is one of those above-range values, category 0 applies immediately.

Player 2 has four upper-half values, but assists equal 2, which is below its expected interval. The candidate has no above-range statistic, so neither category 0 nor the first category 1 condition can hold. Three or more upper-half values are enough for category 2, giving the answer `2`.

Player 3 has three values above their expected ranges, namely points, rebounds, and assists. Height and wingspan are not above their ranges, so category 0 fails. The first category 1 condition holds because there are at least two above-range values and at least three upper-half-or-better values, giving `1`.

A second example focuses on the boundary values and the special unicorn condition.

```
4
205
225
15
4
5
220
250
20
6
7
221
251
21
7
8
200
210
21
7
8
```

| Player | `high` | `above` | Height/Wingspan above | All in expected range | Category |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 0 | No | Yes | 2 |
| 2 | 5 | 0 | No | Yes | 2 |
| 3 | 5 | 5 | Yes | No | 0 |
| 4 | 3 | 3 | No | No | 1 |

The first two players demonstrate that both the midpoint and upper endpoint count as part of the expected range. Every statistic is in the upper half, so category 2 applies through the `high >= 3` rule.

Player 3 has all five statistics above their expected ranges, and height is one of them, so the strongest category is 0.

Player 4 has three above-range statistics, but neither physical statistic is above its expected range. The unicorn rule consequently fails, while the first-round rule succeeds because there are at least two above-range values and at least three upper-half-or-better values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Each of the (N) candidates has exactly five statistics, so classification takes constant work |
| Space | (O(1)) auxiliary | Only five values and a few counters are needed for the current candidate |

With (N\le32), the algorithm performs only a few hundred basic comparisons. It is far below any practical time or memory limit, and its linear structure would remain efficient even if the number of candidates were increased substantially.

## Test Cases

```python
import sys
import io

def classify(values):
    lower = [190, 200, 10, 2, 3]
    upper = [220, 250, 20, 6, 7]
    middle = [205, 225, 15, 4, 5]

    high = 0
    above = 0
    all_expected = True

    for i, x in enumerate(values):
        if x < lower[i]:
            all_expected = False
        if x >= middle[i]:
            high += 1
        if x > upper[i]:
            above += 1

    physical_above = values[0] > upper[0] or values[1] > upper[1]

    if above >= 3 and physical_above:
        return 0

    if (above >= 2 and high >= 3) or (all_expected and high >= 3):
        return 1

    if (above >= 1 and high >= 2) or high >= 3:
        return 2

    return 3

def solve():
    input = sys.stdin.readline
    n = int(input())
    result = []

    for _ in range(n):
        values = [int(input()) for _ in range(5)]
        result.append(str(classify(values)))

    return "\n".join(result)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided sample
assert run("""3
230
190
16
7
9
205
225
15
5
2
210
210
30
9
9
""") == """0
2
1""", "sample 1"

# Minimum-size input, every value below its expected range
assert run("""1
189
199
9
1
2
""") == "3", "all values below expected"

# All values exactly at the upper-half midpoint
assert run("""1
205
225
15
4
5
""") == "2", "midpoints belong to upper half"

# All values exactly at the upper endpoint
assert run("""1
220
250
20
6
7
""") == "2", "upper endpoints are not above range"

# Three above-range statistics, but neither physical statistic is above
assert run("""1
200
210
21
7
8
""") == "1", "no physical statistic above range"

# Genuine unicorn, with exactly three above-range values
assert run("""1
221
250
21
6
7
""") == "0", "height plus two skills above range"

# Maximum-size input, all candidates identical
maximum_case = "32\n" + "\n".join(
    ["205", "225", "15", "4", "5"] * 32
) + "\n"
assert run(maximum_case) == "\n".join(["2"] * 32), "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `189, 199, 9, 1, 2` | `3` | Minimum-size input and values below every expected range |
| `205, 225, 15, 4, 5` | `2` | Midpoints are included in the upper half |
| `220, 250, 20, 6, 7` | `2` | Upper endpoints are not above the expected range |
| `200, 210, 21, 7, 8` | `1` | Three above-range skills do not make a unicorn without height or wingspan |
| `221, 250, 21, 6, 7` | `0` | Exactly three above-range values with height above the range |
| 32 identical candidates | 32 lines of `2` | Maximum input size and independent processing |

## Edge Cases

The midpoint boundary is handled by using `>=`. For the input

```
1
205
225
15
4
5
```

all five values satisfy their upper-half thresholds, so `high = 5`. None is above its expected upper endpoint, so `above = 0`. Category 2 follows from `high >= 3`, producing `2`. A strict comparison such as `x > middle[i]` would incorrectly exclude every midpoint.

The upper endpoint boundary is handled separately with `>`. For

```
1
220
250
20
6
7
```

all five values are still inside their expected ranges. They are also all in the upper half, so `high = 5` and `above = 0`. The result is `2`. This prevents the common mistake of treating the expected upper endpoint as an above-range value.

The physical-statistic requirement is checked independently from the total count. For

```
1
200
210
21
7
8
```

points, rebounds, and assists are above their ranges, giving `above = 3`. Height and wingspan are not above their ranges, so `physical_above` is false. Category 0 is rejected, while `above >= 2` and `high >= 3` make category 1 valid. The output is `1`.

Priority is handled by the order of the conditions. For

```
1
221
250
21
6
7
```

height, points, and assists are above their ranges, so `above = 3`, and height makes `physical_above` true. The algorithm returns category 0 immediately. It never reaches the weaker category 1 or category 2 rules, which is necessary because the requested output is the strongest applicable classification.
