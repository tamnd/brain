---
title: "CF 1334A - Level Statistics"
description: "We observe the statistics of a game level several times. At each observation we know two values: how many times the level has been played and how many times it has been cleared. A successful attempt increases both numbers by one at the same moment."
date: "2026-06-11T15:59:05+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1334
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 85 (Rated for Div. 2)"
rating: 1200
weight: 1334
solve_time_s: 120
verified: true
draft: false
---

[CF 1334A - Level Statistics](https://codeforces.com/problemset/problem/1334/A)

**Rating:** 1200  
**Tags:** implementation, math  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We observe the statistics of a game level several times. At each observation we know two values: how many times the level has been played and how many times it has been cleared.

A successful attempt increases both numbers by one at the same moment. A failed attempt increases only the play count. Between two observations any number of players may have tried the level, including zero players.

For every test case we must determine whether the recorded sequence could actually happen. If some sequence of successful and unsuccessful attempts produces exactly those observations in chronological order, we print `"YES"`. Otherwise we print `"NO"`.

The constraints are tiny. There are at most 500 test cases and each test case contains at most 100 observations. Even an algorithm that compares every pair of observations would run comfortably. There is no need for sophisticated data structures or optimization. A linear scan over the observations is more than enough.

The subtle part is understanding the relationship between plays and clears. Several situations that look harmless are actually impossible.

Suppose the number of plays stays fixed while clears increase.

Input:

```
1
3
0 0
1 1
1 2
```

The correct answer is:

```
NO
```

A new clear always comes from a new play, so the increase in clears can never exceed the increase in plays. A careless solution that only checks whether both sequences are nondecreasing would incorrectly accept this case.

Another tricky situation is when the total number of clears exceeds the total number of plays.

Input:

```
1
1
3 5
```

The answer is:

```
NO
```

Five successful attempts require at least five plays.

One more pitfall is decreasing values.

Input:

```
1
3
10 2
15 3
14 3
```

The answer is:

```
NO
```

Statistics only increase over time. Any decrease immediately makes the record impossible.

## Approaches

A brute-force interpretation would try to reconstruct every individual attempt between observations. If plays increase by 1000, we could imagine all possible ways those 1000 attempts are split into successful and unsuccessful runs. Such a method is correct because it explicitly simulates the process, but the number of possible histories grows exponentially with the number of attempts. Even one interval with 1000 new plays already has an enormous number of possibilities.

The key observation is that we never need to know the exact sequence of successes and failures. Only three conditions matter.

First, plays cannot decrease.

Second, clears cannot decrease.

Third, whenever we move from one observation to the next, the number of new clears cannot exceed the number of new plays. Every successful attempt contributes one play and one clear, so obtaining five additional clears requires at least five additional plays.

The same idea also applies to the first observation. At any moment the total number of clears cannot exceed the total number of plays.

Once these conditions are checked for every consecutive pair, the answer is determined. A single invalid pair makes the whole record impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all observations for the current test case.
2. Check the first observation. If the number of clears exceeds the number of plays, the answer is `"NO"` because every clear must come from a play.
3. Traverse the observations from left to right.
4. For each pair of consecutive observations, compute the changes in plays and clears.
5. If plays decrease, the record is impossible because statistics never go backward.
6. If clears decrease, the record is impossible for the same reason.
7. If the increase in clears is larger than the increase in plays, the record is impossible. More successful attempts cannot occur than total attempts.
8. If none of these checks fail, print `"YES"`.

### Why it works

After processing any pair of consecutive observations, the algorithm maintains the invariant that there exists at least one sequence of attempts producing all observations seen so far.

When moving from one observation to the next, the only information that matters is how many new plays and new clears appeared. As long as both quantities are nonnegative and the number of new clears does not exceed the number of new plays, we can interpret those new clears as successful attempts and the remaining new plays as failed attempts. Thus a valid extension always exists. If any of these conditions is violated, no sequence of attempts can explain that transition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    records = [tuple(map(int, input().split())) for _ in range(n)]

    ok = True

    if records[0][1] > records[0][0]:
        ok = False

    for i in range(1, n):
        prev_p, prev_c = records[i - 1]
        cur_p, cur_c = records[i]

        dp = cur_p - prev_p
        dc = cur_c - prev_c

        if dp < 0 or dc < 0 or dc > dp:
            ok = False

    print("YES" if ok else "NO")
```

The solution begins by reading all observations for one test case. Keeping them in a list makes the pairwise comparisons straightforward.

The first observation deserves special treatment. If the level already has more clears than plays, the record is impossible before considering any transitions.

For every consecutive pair we compute the increase in plays and clears. Negative differences mean that some statistic decreased, which cannot happen. The condition `dc > dp` catches the more subtle case where the number of newly completed runs exceeds the number of newly started runs.

The order of the checks does not matter because any violation makes the answer `"NO"`. There is no need to stop immediately after finding an error, although doing so would also work.

Since all values are at most 1000, integer overflow is not a concern in Python.

## Worked Examples

Consider the first sample case:

```
3
0 0
1 1
1 2
```

| Step | Previous (p,c) | Current (p,c) | dp | dc | Valid |
| --- | --- | --- | --- | --- | --- |
| Initial | - | (0,0) | - | - | Yes |
| 1 | (0,0) | (1,1) | 1 | 1 | Yes |
| 2 | (1,1) | (1,2) | 0 | 1 | No |

At the second transition we obtain one additional clear without any additional play. Since `dc > dp`, the sequence becomes impossible and the answer is `"NO"`.

Consider the sample case

```
2
1 0
1000 3
```

| Step | Previous (p,c) | Current (p,c) | dp | dc | Valid |
| --- | --- | --- | --- | --- | --- |
| Initial | - | (1,0) | - | - | Yes |
| 1 | (1,0) | (1000,3) | 999 | 3 | Yes |

Three successful attempts among 999 new plays are completely possible. Every condition holds, so the answer is `"YES"`.

These traces illustrate the invariant. Each transition is examined independently, and validity of all transitions implies validity of the entire history.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each observation is processed once |
| Space | O(1) | Only a few variables are needed besides the input storage |

Since each test case contains at most 100 observations and there are at most 500 test cases, the total work is tiny. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        records = [tuple(map(int, input().split())) for _ in range(n)]

        ok = True

        if records[0][1] > records[0][0]:
            ok = False

        for i in range(1, n):
            prev_p, prev_c = records[i - 1]
            cur_p, cur_c = records[i]

            dp = cur_p - prev_p
            dc = cur_c - prev_c

            if dp < 0 or dc < 0 or dc > dp:
                ok = False

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run(
"""6
3
0 0
1 1
1 2
2
1 0
1000 3
4
10 1
15 2
10 2
15 2
1
765 432
2
4 4
4 3
5
0 0
1 0
1 0
1 0
1 0
"""
) == """NO
YES
NO
YES
NO
YES"""

# minimum size
assert run(
"""1
1
0 0
"""
) == "YES"

# first observation invalid
assert run(
"""1
1
3 5
"""
) == "NO"

# all values equal
assert run(
"""1
4
2 1
2 1
2 1
2 1
"""
) == "YES"

# clears increase faster than plays
assert run(
"""1
2
5 2
7 5
"""
) == "NO"

# decreasing plays
assert run(
"""1
2
10 3
9 3
"""
) == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single observation (0,0) | YES | Minimum size |
| Single observation (3,5) | NO | Clears cannot exceed plays |
| Repeated identical observations | YES | Zero changes are allowed |
| Transition from (5,2) to (7,5) | NO | New clears cannot exceed new plays |
| Transition from (10,3) to (9,3) | NO | Statistics cannot decrease |

## Edge Cases

Consider a case where clears increase but plays do not.

Input:

```
1
3
0 0
1 1
1 2
```

The algorithm computes the differences between the last two observations:

`dp = 0`, `dc = 1`.

Since `dc > dp`, the transition is impossible and the output becomes:

```
NO
```

Now consider a case where the very first observation already violates the basic requirement.

Input:

```
1
1
3 5
```

Before entering the loop, the algorithm checks whether clears exceed plays. Here `5 > 3`, so it immediately marks the test case invalid and prints:

```
NO
```

Finally, consider decreasing statistics.

Input:

```
1
3
10 2
15 3
14 3
```

For the last transition:

`dp = 14 - 15 = -1`

A negative difference means the play count went backward. The algorithm rejects the sequence and prints:

```
NO
```

These examples cover the situations that most commonly cause incorrect implementations. The pairwise difference check handles all of them naturally.
