---
title: "CF 24B - F1 Champions"
description: "We are given the results of an entire Formula One season. Each race lists drivers from first place to last place. The ch"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 24
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 24"
rating: 1500
weight: 24
solve_time_s: 139
verified: true
draft: false
---

[CF 24B - F1 Champions](https://codeforces.com/problemset/problem/24/B)

**Rating:** 1500  
**Tags:** implementation  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the results of an entire Formula One season. Each race lists drivers from first place to last place. The championship winner depends on one of two ranking systems.

In the original system, drivers are ranked primarily by total points. The top 10 positions in each race award fixed points: 25, 18, 15, 12, 10, 8, 6, 4, 2, 1. If two drivers have the same number of points, we compare how many first-place finishes they have. If that is still tied, we compare second places, then third places, and so on.

The alternative system flips the first two priorities. Drivers are ranked first by number of wins. If wins are equal, we compare total points. If still tied, we again compare counts of second places, third places, and so on.

The input gives every race in order. For each race, we receive the list of participating drivers sorted by finishing position. A driver may skip some races, and we must still consider them in the final standings if they appeared at least once.

The constraints are very small. There are at most 20 races and at most 50 drivers overall. Even if every race contains all 50 drivers, the total number of race results is only 1000. That means we do not need advanced optimization techniques or complicated data structures. A direct implementation of the ranking rules is fast enough.

The real difficulty is implementing the tie-breaking correctly. A careless implementation often fails because the comparison rules are lexicographic, not just based on points and wins.

Consider this example:

```
2
3
A
B
C
3
B
A
C
```

Both A and B score 43 points and both have one win. The champion should be determined by comparing second places. Each has one second place as well, so they are still tied. The statement guarantees this will not happen in official tests, but our comparison logic must still follow the correct order.

Another easy mistake is forgetting positions outside the top 10. These positions give zero points, but they still matter for tie-breaking because counts of placements are compared all the way down.

Example:

```
2
11
A
B
C
D
E
F
G
H
I
J
K
11
B
A
C
D
E
F
G
H
I
J
K
```

A and B both have one win and one second place. Their points are also equal. The remaining placements are identical. A buggy solution that stores only top-10 finishes could incorrectly conclude the comparison early.

Another subtle issue is drivers missing races. If a driver never appears in a race, we must not accidentally create fake placements for them. Missing a race simply means they gain no points and no placement count.

## Approaches

The most direct approach is to simulate the entire season exactly as written. For every driver, we store total points and how many times they finished in each position. After processing all races, we compare every pair of drivers according to the required ranking rules.

A brute-force version could recompute all statistics from scratch whenever comparing two drivers. Suppose we compare drivers A and B. We could scan every race, count points and placements for both, then decide who ranks higher. With at most 50 drivers, we may perform roughly 2500 comparisons, and each comparison could scan up to 1000 race results. Even this stays within limits, around a few million operations.

Still, recomputing the same information repeatedly is unnecessary. Every comparison depends only on accumulated season statistics. Once we realize this, the problem becomes much cleaner.

The key observation is that each driver's season can be represented by a compact record:

1. Total points.
2. Number of first places.
3. Number of second places.
4. Number of third places.
5. And so on.

Then ranking drivers becomes a pure lexicographic comparison between these records, with slightly different priority orders for the two scoring systems.

For the original system, the comparison key is:

```
(points, first_places, second_places, ...)
```

For the alternative system, the comparison key is:

```
(first_places, points, second_places, ...)
```

Because the number of drivers and races is tiny, we can simply iterate over all drivers and keep the best one according to the chosen comparator.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(D² × R × N) | O(1) | Accepted |
| Optimal | O(R × N + D² × N) | O(D × N) | Accepted |

Here, `D` is the number of drivers, `R` is the number of races, and `N` is the maximum number of classified drivers in a race.

## Algorithm Walkthrough

1. Create a dictionary for all drivers.

For each driver, store:

- Total points.
- An array where `places[i]` counts how many times the driver finished in position `i`.

We need full placement counts because tie-breaking may continue beyond wins.
2. Process every race from top to bottom.

The first driver is the winner, the second driver finished second, and so on. Update:

- The placement counter for that position.
- The driver's points if the position is inside the top 10.
3. Define a comparison function for the original system.

Compare two drivers in this order:

- Total points.
- Number of first places.
- Number of second places.
- Number of third places.
- Continue until a difference appears.

This exactly matches the championship rules.
4. Define another comparison function for the alternative system.

Compare in this order:

- Number of wins.
- Total points.
- Number of second places.
- Number of third places.
- Continue further if needed.

Wins are checked first because the alternative rules prioritize victories over consistency.
5. Iterate over all drivers to find the best driver under each system.

Start with any driver as current champion. For every other driver, apply the comparison function. Replace the champion if the new driver ranks higher.
6. Output both champions.

### Why it works

Every race contributes independently to each driver's season statistics. The total points and placement counts fully determine the official ranking rules. No additional information from race order or race identity matters.

The comparison functions exactly mirror the problem statement. If one driver has more points, they win immediately in the original system. If points are equal, the first differing placement count decides the ranking. The alternative system follows the same logic with wins checked first.

Because every driver's statistics are accumulated correctly and comparisons follow the official tie-breaking order, the selected champion must be correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

def solve():
    t = int(input())

    drivers = {}

    for _ in range(t):
        n = int(input())

        for pos in range(n):
            name = input().strip()

            if name not in drivers:
                drivers[name] = {
                    "points": 0,
                    "places": [0] * 55
                }

            drivers[name]["places"][pos + 1] += 1

            if pos < 10:
                drivers[name]["points"] += POINTS[pos]

    names = list(drivers.keys())

    def better_original(a, b):
        da = drivers[a]
        db = drivers[b]

        if da["points"] != db["points"]:
            return da["points"] > db["points"]

        for place in range(1, 55):
            if da["places"][place] != db["places"][place]:
                return da["places"][place] > db["places"][place]

        return False

    def better_alternative(a, b):
        da = drivers[a]
        db = drivers[b]

        if da["places"][1] != db["places"][1]:
            return da["places"][1] > db["places"][1]

        if da["points"] != db["points"]:
            return da["points"] > db["points"]

        for place in range(2, 55):
            if da["places"][place] != db["places"][place]:
                return da["places"][place] > db["places"][place]

        return False

    champion_original = names[0]
    champion_alternative = names[0]

    for name in names[1:]:
        if better_original(name, champion_original):
            champion_original = name

        if better_alternative(name, champion_alternative):
            champion_alternative = name

    print(champion_original)
    print(champion_alternative)

solve()
```

The solution first builds season statistics for every driver. The `places` array stores how many times a driver finished in each position. Index `1` represents wins, index `2` represents second places, and so on.

Using a fixed-size array is simpler and safer than dynamically resizing structures during comparisons. Since there are at most 50 drivers in a race, an array of size 55 comfortably covers every possible placement.

The two comparison functions directly encode the ranking systems. The original system compares points first, while the alternative system compares wins first. After those primary criteria, both continue lexicographically through placement counts.

One subtle detail is the loop ranges in the tie-breakers. The original system starts checking from place `1` because wins are the first tie-break after points. The alternative system already handled wins separately, so its loop starts from place `2`.

Another important implementation choice is storing all placements, not just top-10 finishes. Drivers outside the points still affect later tie-breakers.

## Worked Examples

### Example 1

Input:

```
3
3
Hamilton
Vettel
Webber
2
Webber
Vettel
2
Hamilton
Vettel
```

Processing races:

| Race | Position | Driver | Points Added | Total Points | Wins | Seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | Hamilton | 25 | 25 | 1 | 0 |
| 1 | 2 | Vettel | 18 | 18 | 0 | 1 |
| 1 | 3 | Webber | 15 | 15 | 0 | 0 |
| 2 | 1 | Webber | 25 | 40 | 1 | 0 |
| 2 | 2 | Vettel | 18 | 36 | 0 | 2 |
| 3 | 1 | Hamilton | 25 | 50 | 2 | 0 |
| 3 | 2 | Vettel | 18 | 54 | 0 | 3 |

Final standings:

| Driver | Points | Wins | Seconds |
| --- | --- | --- | --- |
| Hamilton | 50 | 2 | 0 |
| Vettel | 54 | 0 | 3 |
| Webber | 40 | 1 | 0 |

Original system chooses Vettel because points matter most. Alternative system chooses Hamilton because wins matter most.

This trace demonstrates that the two ranking systems may produce different champions even with the same race results.

### Example 2

Input:

```
2
3
A
B
C
3
B
A
C
```

Processing races:

| Race | Position | Driver | Total Points | Wins | Seconds |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | A | 25 | 1 | 0 |
| 1 | 2 | B | 18 | 0 | 1 |
| 2 | 1 | B | 43 | 1 | 1 |
| 2 | 2 | A | 43 | 1 | 1 |

Final standings:

| Driver | Points | Wins | Seconds |
| --- | --- | --- | --- |
| A | 43 | 1 | 1 |
| B | 43 | 1 | 1 |

The drivers remain tied even after comparing wins and second places. The official problem guarantees that real test cases avoid this situation.

This example shows why the comparison logic must continue through every placement level instead of stopping early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R × N + D² × N) | Processing races plus comparing drivers through placement counts |
| Space | O(D × N) | Storing placement statistics for every driver |

The constraints are tiny, so this solution easily fits within limits. At most we store statistics for 50 drivers, and each comparison examines at most 50 placement positions.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

def solve():
    input = sys.stdin.readline

    t = int(input())

    drivers = {}

    for _ in range(t):
        n = int(input())

        for pos in range(n):
            name = input().strip()

            if name not in drivers:
                drivers[name] = {
                    "points": 0,
                    "places": [0] * 55
                }

            drivers[name]["places"][pos + 1] += 1

            if pos < 10:
                drivers[name]["points"] += POINTS[pos]

    names = list(drivers.keys())

    def better_original(a, b):
        da = drivers[a]
        db = drivers[b]

        if da["points"] != db["points"]:
            return da["points"] > db["points"]

        for place in range(1, 55):
            if da["places"][place] != db["places"][place]:
                return da["places"][place] > db["places"][place]

        return False

    def better_alternative(a, b):
        da = drivers[a]
        db = drivers[b]

        if da["places"][1] != db["places"][1]:
            return da["places"][1] > db["places"][1]

        if da["points"] != db["points"]:
            return da["points"] > db["points"]

        for place in range(2, 55):
            if da["places"][place] != db["places"][place]:
                return da["places"][place] > db["places"][place]

        return False

    best1 = names[0]
    best2 = names[0]

    for name in names[1:]:
        if better_original(name, best1):
            best1 = name

        if better_alternative(name, best2):
            best2 = name

    print(best1)
    print(best2)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""3
3
Hamilton
Vettel
Webber
2
Webber
Vettel
2
Hamilton
Vettel
"""
) == "Vettel\nHamilton\n", "sample 1"

# minimum input
assert run(
"""1
1
Alice
"""
) == "Alice\nAlice\n", "single driver"

# wins matter more in alternative system
assert run(
"""2
2
A
B
2
B
A
"""
) == "A\nA\n", "tie resolved by first encountered equal stats"

# driver outside top 10 still affects tie-break
assert run(
"""2
11
A
B
C
D
E
F
G
H
I
J
K
11
B
A
C
D
E
F
G
H
I
J
K
"""
) == "A\nA\n", "full placement tracking"

# consistency beats wins in original system
assert run(
"""3
3
A
B
C
3
B
A
C
3
B
A
C
"""
) == "B\nB\n", "points and wins"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single race with one driver | Same driver twice | Minimum-size input |
| Two symmetric races | Same driver twice | Stable handling of equal statistics |
| Two races with 11 drivers | Same driver twice | Placements outside top 10 are tracked |
| Three races with repeated podiums | B twice | Correct accumulation of points and wins |

## Edge Cases

Consider the case where drivers tie on points but not on wins.

```
2
2
A
B
2
B
A
```

After processing both races:

- A has 43 points and 1 win.
- B has 43 points and 1 win.

The comparison proceeds to second places. Both drivers also have one second place, so they remain tied. The implementation keeps checking all placement counts exactly as required.

Now consider placements outside the top 10:

```
2
11
A
B
C
D
E
F
G
H
I
J
K
11
B
A
C
D
E
F
G
H
I
J
K
```

Drivers A and B receive identical points and identical top-10 finishes. A buggy implementation that ignores 11th place onward might incorrectly stop tracking data too early. Our solution stores every finishing position, so the tie-breaking remains correct.

Another important edge case is drivers skipping races:

```
2
2
A
B
1
B
```

A scores 25 points from one race. B scores 43 points across two races. Missing a race simply means no updates occur for that driver in that race. Since all statistics are accumulated independently, the implementation handles absent drivers naturally without any special cases.
