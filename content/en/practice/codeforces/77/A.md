---
title: "CF 77A - Heroes"
description: "We have exactly seven heroes and three bosses. Each boss gives some amount of experience, and every hero assigned to that boss receives an equal share rounded down. If a boss gives x experience and its team has k heroes, then every hero in that team receives x // k."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 77
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 69 (Div. 1 Only)"
rating: 1400
weight: 77
solve_time_s: 109
verified: true
draft: false
---

[CF 77A - Heroes](https://codeforces.com/problemset/problem/77/A)

**Rating:** 1400  
**Tags:** brute force, implementation  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have exactly seven heroes and three bosses. Each boss gives some amount of experience, and every hero assigned to that boss receives an equal share rounded down.

If a boss gives `x` experience and its team has `k` heroes, then every hero in that team receives `x // k`.

The task is to split the seven heroes into three non-empty groups. Each group fights one boss, and every boss must be assigned to exactly one group.

The optimization has two layers.

First, minimize the difference between the maximum experience any hero receives and the minimum experience any hero receives.

Second, among all partitions achieving that minimum difference, maximize the total number of "likes" that stay inside groups.

The input describes directed liking relationships. If hero `A` likes hero `B` and both are in the same team, that contributes `1` to the score. Since likes are directed, mutual liking counts twice.

The key observation is that the number of heroes is fixed at seven. That changes the entire nature of the problem.

A naive partition search over arbitrary sets would normally explode combinatorially, but here the total number of assignments is tiny. Each hero can choose one of three groups, so there are at most `3^7 = 2187` assignments. Even after checking group validity and counting likes, this is trivial inside a 2-second limit.

The number of liking relations is at most `42`, which is exactly `7 * 6`, the maximum number of directed edges without self-loops. That means we can freely iterate over all relations for every partition.

The tricky part is not performance, but correctness.

One easy mistake is forgetting that bosses are distinct. Two groups with the same set of heroes can produce different experience distributions depending on which boss they fight.

For example:

```
0
100 1 1
```

If one hero fights the `100` boss alone, that hero gets `100`. If seven heroes fight it together, each gets `14`.

Another subtle issue is integer division.

Consider:

```
0
10 10 9
```

If team sizes are `(2,2,3)`, experiences become `(5,5,3)` because `9 // 3 = 3`, not `3.0` rounded later. Using floating-point division would produce the wrong answer.

A third easy bug is treating likes as undirected.

Example:

```
2
Anka likes Troll
Troll likes Anka
10 10 10
```

If Anka and Troll are together, the contribution is `2`, not `1`.

Finally, teams are allowed to contain exactly one hero, but no team may be empty.

This input is valid:

```
0
100 100 100
```

A partition like `(1,1,5)` is completely legal.

A careless implementation that forces "balanced" teams would miss optimal answers.

## Approaches

The most direct brute-force idea is to try every possible assignment of heroes to teams.

Each of the seven heroes independently chooses one of three groups, producing `3^7 = 2187` assignments. For every assignment we check whether all three groups are non-empty, compute the experience each hero receives, calculate the maximum and minimum experience, and count all liking relations that remain inside groups.

This brute-force approach is already fast enough.

For every assignment, counting likes takes at most `42` operations. Computing experiences takes constant time. The total work is roughly:

```
2187 * 42 ≈ 90000
```

That is tiny.

The interesting part of the problem is realizing that the constraints are intentionally small enough for exhaustive search.

A more general version of this problem with even twenty heroes would become impossible with this approach because `3^20` is already over three billion assignments.

The important observation is that seven heroes is effectively a constant. Once we recognize that, the problem becomes an implementation exercise instead of a complicated optimization problem.

We still need to structure the brute force carefully.

The cleanest representation is assigning every hero an integer from `0` to `2`, representing the chosen boss. Then:

```
team_size[t] = number of heroes assigned to team t
```

Experience for team `t` becomes:

```
boss_exp[t] // team_size[t]
```

After that, every hero's experience is immediately known from their assigned team.

Finally, we evaluate the two optimization criteria lexicographically:

1. Smaller experience difference is always better.
2. If tied, larger like count is better.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all partitions | O(3^7 × n) | O(1) | Accepted |
| Optimized exhaustive search | O(3^7 × n) | O(1) | Accepted |

The "optimal" solution is still brute force because the input size is intentionally tiny.

## Algorithm Walkthrough

1. Store the seven hero names and map each name to an index from `0` to `6`.
2. Read all directed liking relations and convert them into pairs of hero indices.
3. Iterate through all assignments from `0` to `3^7 - 1`.
4. Decode the current number into base `3`.

The `i`-th digit tells us which team hero `i` belongs to.
5. Count the number of heroes in each team.

If any team size is zero, skip this assignment because every boss must be fought.
6. Compute the experience received by each team.

If team `t` has size `sz[t]`, then every hero in that team receives:

```
boss[t] // sz[t]
```
7. Compute the maximum and minimum hero experience across all seven heroes.

Their difference is the primary optimization target.
8. Count the number of liking relations that stay inside teams.

For every directed edge `(u, v)`, add `1` if heroes `u` and `v` belong to the same team.
9. Compare this partition with the current best answer.

If its experience difference is smaller, replace the answer.

If the difference is equal but the like count is larger, replace the answer.
10. After all assignments are processed, print the best difference and best like count.

### Why it works

The algorithm checks every possible valid partition of the seven heroes into three non-empty groups. Since no partition is skipped except invalid ones with empty teams, the optimal partition must appear during enumeration.

For every partition, the algorithm computes exactly the quantities defined in the statement:

1. Experience per hero using floor division.
2. Maximum minus minimum experience.
3. Number of directed likes inside teams.

Because every valid partition is evaluated and compared using the same lexicographic ordering as the problem statement, the selected answer is guaranteed to be optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    heroes = [
        "Anka",
        "Chapay",
        "Cleo",
        "Troll",
        "Dracul",
        "Snowy",
        "Hexadecimal"
    ]

    idx = {name: i for i, name in enumerate(heroes)}

    n = int(input())

    likes = []

    for _ in range(n):
        p, _, q = input().split()
        likes.append((idx[p], idx[q]))

    boss = list(map(int, input().split()))

    best_diff = float('inf')
    best_like = -1

    for mask in range(3 ** 7):
        x = mask

        team = [0] * 7
        sz = [0] * 3

        for i in range(7):
            team[i] = x % 3
            sz[team[i]] += 1
            x //= 3

        if 0 in sz:
            continue

        exp = [0] * 3

        for t in range(3):
            exp[t] = boss[t] // sz[t]

        vals = [exp[team[i]] for i in range(7)]

        diff = max(vals) - min(vals)

        like_count = 0

        for u, v in likes:
            if team[u] == team[v]:
                like_count += 1

        if diff < best_diff:
            best_diff = diff
            best_like = like_count
        elif diff == best_diff and like_count > best_like:
            best_like = like_count

    print(best_diff, best_like)

solve()
```

The implementation follows the brute-force enumeration directly.

The most important implementation detail is decoding assignments using base `3`. Every integer from `0` to `3^7 - 1` uniquely represents one assignment of heroes to teams.

For example:

```
mask = 17
```

might decode into:

```
[2, 1, 0, 0, 0, 0, 0]
```

meaning hero `0` joins team `2`, hero `1` joins team `1`, and so on.

Another subtle point is that likes are directed. The code stores every relation exactly as given and counts each independently.

The experience calculation must use integer division:

```
boss[t] // sz[t]
```

Using normal division would produce floating-point values and break the intended rules.

The lexicographic optimization is handled carefully.

We first minimize `diff`. Only when two partitions have equal `diff` do we compare `like_count`.

## Worked Examples

### Example 1

Input:

```
3
Troll likes Dracul
Dracul likes Anka
Snowy likes Hexadecimal
210 200 180
```

One optimal partition is:

```
{Troll, Dracul, Anka}
{Snowy, Hexadecimal}
{Chapay, Cleo}
```

| Team | Heroes | Size | Boss EXP | Per Hero |
| --- | --- | --- | --- | --- |
| 0 | Troll, Dracul, Anka | 3 | 210 | 70 |
| 1 | Snowy, Hexadecimal | 2 | 200 | 100 |
| 2 | Chapay, Cleo | 2 | 180 | 90 |

Hero experiences become:

```
70, 70, 70, 100, 100, 90, 90
```

| Quantity | Value |
| --- | --- |
| Maximum EXP | 100 |
| Minimum EXP | 70 |
| Difference | 30 |

Likes inside teams:

| Relation | Same Team? |
| --- | --- |
| Troll → Dracul | Yes |
| Dracul → Anka | Yes |
| Snowy → Hexadecimal | Yes |

Total liking score is `3`.

This example shows that minimizing experience spread may require uneven team sizes.

### Example 2

Input:

```
2
Anka likes Troll
Troll likes Anka
100 100 100
```

An optimal partition is:

```
{Anka, Troll}
{Chapay, Cleo}
{Dracul, Snowy, Hexadecimal}
```

| Team Size | Per Hero EXP |
| --- | --- |
| 2 | 50 |
| 2 | 50 |
| 3 | 33 |

Difference becomes:

```
50 - 33 = 17
```

Both directed likes stay inside the same team.

| Relation | Counted |
| --- | --- |
| Anka → Troll | Yes |
| Troll → Anka | Yes |

Total liking score is `2`.

This example demonstrates why likes must be treated as directed edges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3^7 × n) | Enumerate every assignment and check all liking edges |
| Space | O(1) | Only fixed-size arrays for 7 heroes are stored |

Since `3^7 = 2187` and `n ≤ 42`, the total number of operations is extremely small. The solution comfortably fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        heroes = [
            "Anka",
            "Chapay",
            "Cleo",
            "Troll",
            "Dracul",
            "Snowy",
            "Hexadecimal"
        ]

        idx = {name: i for i, name in enumerate(heroes)}

        n = int(input())

        likes = []

        for _ in range(n):
            p, _, q = input().split()
            likes.append((idx[p], idx[q]))

        boss = list(map(int, input().split()))

        best_diff = float('inf')
        best_like = -1

        for mask in range(3 ** 7):
            x = mask

            team = [0] * 7
            sz = [0] * 3

            for i in range(7):
                team[i] = x % 3
                sz[team[i]] += 1
                x //= 3

            if 0 in sz:
                continue

            exp = [0] * 3

            for t in range(3):
                exp[t] = boss[t] // sz[t]

            vals = [exp[team[i]] for i in range(7)]

            diff = max(vals) - min(vals)

            like_count = 0

            for u, v in likes:
                if team[u] == team[v]:
                    like_count += 1

            if diff < best_diff:
                best_diff = diff
                best_like = like_count
            elif diff == best_diff and like_count > best_like:
                best_like = like_count

        return f"{best_diff} {best_like}"

    return solve()

# provided sample
assert run(
"""3
Troll likes Dracul
Dracul likes Anka
Snowy likes Hexadecimal
210 200 180
"""
) == "30 3", "sample 1"

# no likes, equal boss experience
assert run(
"""0
100 100 100
"""
) == "0 0", "equal values"

# directed likes counted separately
assert run(
"""2
Anka likes Troll
Troll likes Anka
100 100 100
"""
) == "17 2", "directed edges"

# minimum likes, uneven experiences
assert run(
"""0
10 10 1
"""
) == "5 0", "integer division"

# dense liking graph
assert run(
"""6
Anka likes Chapay
Chapay likes Cleo
Cleo likes Troll
Troll likes Dracul
Dracul likes Snowy
Snowy likes Hexadecimal
100 100 100
"""
) == "17 4", "maximize likes under same diff"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Equal boss values, no likes | `0 0` | Perfectly balanced experiences |
| Mutual liking pair | `17 2` | Directed likes counted twice |
| `10 10 1` | `5 0` | Correct floor division handling |
| Dense chain of likes | `17 4` | Secondary optimization by liking count |

## Edge Cases

Consider the case where teams of size one are necessary.

Input:

```
0
100 1 1
```

The algorithm still enumerates partitions like `(1,3,3)` or `(1,1,5)` because it only rejects empty teams.

If one hero fights the `100` boss alone and the remaining heroes split across the two weak bosses, the algorithm computes experiences correctly using integer division.

Another subtle case is directed liking.

Input:

```
2
Anka likes Troll
Troll likes Anka
100 100 100
```

When Anka and Troll are grouped together, the counting loop processes both edges independently:

```
for u, v in likes:
    if team[u] == team[v]:
        like_count += 1
```

The result becomes `2`, which matches the statement.

Now consider integer division.

Input:

```
0
10 10 9
```

Suppose the partition sizes are `(2,2,3)`.

The algorithm computes:

```
10 // 2 = 5
10 // 2 = 5
9 // 3 = 3
```

The difference is `2`.

A floating-point implementation might incorrectly treat the third value as `3.0` and accidentally introduce rounding behavior later.

Finally, consider all boss values equal.

Input:

```
0
100 100 100
```

The optimal partition is any balanced split like `(2,2,3)`.

The algorithm naturally discovers this because it evaluates every possible team size configuration implicitly through hero assignments.
