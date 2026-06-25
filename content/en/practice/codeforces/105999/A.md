---
title: "CF 105999A - Ace Race"
description: "The problem models a race on an infinite number line. Alice starts at position a. The prize appears at one of two possible positions, x or y, and Bob must choose a different integer starting position before knowing which one occurs."
date: "2026-06-25T13:20:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105999
codeforces_index: "A"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2024"
rating: 0
weight: 105999
solve_time_s: 39
verified: true
draft: false
---

[CF 105999A - Ace Race](https://codeforces.com/problemset/problem/105999/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a race on an infinite number line. Alice starts at position `a`. The prize appears at one of two possible positions, `x` or `y`, and Bob must choose a different integer starting position before knowing which one occurs. Bob wins if his chosen position is strictly closer to both possible prize locations than Alice's starting position.

For each test case, the input gives the three positions `a`, `x`, and `y`. The output asks whether there exists a valid starting position for Bob that guarantees a win. The positions are small, but the number of test cases can be large, so the solution should avoid exploring too many possible positions per test case. With up to thousands of cases, an approach that checks a constant number of candidates is ideal, while a scan over a large coordinate range would be unnecessary.

The main difficulty is that Bob needs one position that beats Alice for both destinations at the same time. Checking only one destination can be misleading because a point close to `x` might be too far from `y`.

A common mistake is forgetting that Bob cannot start at Alice's position. For example:

```
1
5 3 1
```

The correct output is:

```
YES
```

A careless approach might try to always choose the midpoint or choose Alice's opposite side without checking the exact distances. Here Bob can choose position `2`, which is distance `1` from both targets. Alice is distance `2` from `3` and distance `4` from `1`.

Another edge case is when Alice is already between the two possible prize positions:

```
1
3 1 5
```

The correct output is:

```
NO
```

Any position that moves closer to `1` moves farther from `5`, and any position that moves closer to `5` moves farther from `1`. Since Alice is exactly in the middle, Bob cannot beat her on both sides.

## Approaches

A direct brute force idea is to try every possible integer starting position for Bob. For each candidate position `b`, we check whether:

```
|b - x| < |a - x|
and
|b - y| < |a - y|
```

If some position satisfies both inequalities, the answer is yes. This is correct because the conditions directly describe the winning requirement.

The issue is deciding how many positions to test. If coordinates were large, checking every possible point would be too slow. Even though this particular version has small coordinates, the intended observation is that the answer depends only on where `a` lies relative to `x` and `y`.

The two target positions divide the line into regions. If Alice is not between the two targets, Bob can choose a point closer to the middle of the interval between `x` and `y`, because that direction reduces both distances. If Alice is between the two targets, she is already on the best possible side for one of the targets and any movement makes one side worse.

The key insight is that the only thing that matters is whether `a` lies outside the segment formed by `x` and `y`. If `a` is outside, moving one step toward the segment decreases the distance to both endpoints. If `a` is inside, no such movement exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(range of coordinates) | O(1) | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three positions `a`, `x`, and `y`.
2. Find the smaller and larger prize positions. Let them be `low` and `high`. This gives the segment where the prize may appear.
3. Check whether Alice's position is outside this segment. If `a < low` or `a > high`, Bob can move one step toward the segment and become closer to both possible prizes.
4. Print `YES` if Alice is outside the segment, otherwise print `NO`.

The reason this works is based on how distances behave on a line. When Alice is outside the two targets, every movement toward the interval reduces both distances. When she is inside, the two targets are on opposite sides, so improving one distance requires worsening the other.

Why it works:

The invariant is that Bob needs a position that is closer to every possible prize location. The segment between `x` and `y` contains all positions that balance the two targets. From outside this segment, moving inward decreases the distance to both ends. From inside the segment, every position is already between the targets, so there is no direction that decreases both distances at once. This exactly matches the condition checked by the algorithm.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        a, x, y = map(int, input().split())

        low = min(x, y)
        high = max(x, y)

        if a < low or a > high:
            ans.append("YES")
        else:
            ans.append("NO")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The code first reads the number of test cases and processes each one independently. For every case, it creates the interval containing the two possible prize locations.

The condition `a < low or a > high` checks whether Alice is outside that interval. If she is, Bob can move inward and improve both distances. If not, Alice is between the targets and Bob cannot guarantee winning.

There are no loops over positions, so there are no boundary or overflow concerns. The only implementation detail to avoid is comparing against `x` and `y` directly without ordering them, because the two target positions may appear in either order.

## Worked Examples

Sample 1:

```
3
1 3 4
5 3 1
3 1 5
```

For the first case:

| a | low | high | Decision |
| --- | --- | --- | --- |
| 1 | 3 | 4 | Outside, YES |

Alice is left of both targets. Moving right makes Bob closer to both possible prizes.

For the second case:

| a | low | high | Decision |
| --- | --- | --- | --- |
| 5 | 1 | 3 | Outside, YES |

Alice is right of both targets. Moving left improves both distances.

For the third case:

| a | low | high | Decision |
| --- | --- | --- | --- |
| 3 | 1 | 5 | Inside, NO |

Alice is between the two possible prize positions, so no single Bob position dominates.

Sample 2:

Input:

```
1
10 2 7
```

Trace:

| a | low | high | Decision |
| --- | --- | --- | --- |
| 10 | 2 | 7 | Outside, YES |

Bob can move left from `10` toward the interval. The distance to both `2` and `7` becomes smaller.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case only performs a few comparisons. |
| Space | O(1) | Only the current test case values are stored, aside from the output list. |

The solution easily fits the limits because it does not depend on the size of the coordinate range. Even a very large number of test cases only requires a constant amount of work per case.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        a, x, y = map(int, input().split())
        low = min(x, y)
        high = max(x, y)

        if a < low or a > high:
            ans.append("YES")
        else:
            ans.append("NO")

    return "\n".join(ans)

# provided samples
assert solve("""3
1 3 4
5 3 1
3 1 5
""") == """YES
YES
NO""", "sample cases"

# minimum style case
assert solve("""1
1 2 3
""") == "YES", "outside left boundary"

# inside interval
assert solve("""1
5 1 10
""") == "NO", "cannot beat middle"

# reversed target order
assert solve("""1
10 8 2
""") == "YES", "target ordering"

# multiple cases with same answer
assert solve("""3
4 1 2
2 1 3
8 3 7
""") == """YES
NO
YES""", "mixed cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 2 3` | `YES` | Alice is outside on the left boundary side. |
| `1 / 5 1 10` | `NO` | Alice is inside the possible prize interval. |
| `1 / 10 8 2` | `YES` | Target positions can appear in any order. |
| `3 / mixed cases` | `YES NO YES` | Multiple independent test cases. |

## Edge Cases

For the case:

```
1
5 3 1
```

The algorithm sorts the prize positions into `low = 1` and `high = 3`. Alice is at `5`, which is greater than `high`, so she is outside the segment. The algorithm returns `YES`. Bob can choose position `2`, giving distances `1` and `1`, while Alice has distances `2` and `4`.

For the case:

```
1
3 1 5
```

The sorted interval is `[1, 5]`. Alice is exactly inside it. The algorithm returns `NO`. Any movement toward the left target increases the distance to the right target, and movement toward the right target increases the distance to the left target.

For equal spacing cases such as:

```
1
0 2 4
```

Alice is also between the targets, so the answer is `NO`. The important point is that being exactly in the middle does not create an advantage for Bob. A single starting point cannot improve both sides simultaneously.
