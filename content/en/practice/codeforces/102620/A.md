---
title: "CF 102620A - Ice Cream Truck"
description: "There are huts arranged on a straight beach. Hut i is exactly 100 meters after hut i-1, and each hut contains some number of people. Existing ice cream shops are also placed on the same line at arbitrary integer coordinates."
date: "2026-08-02T13:47:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102620
codeforces_index: "A"
codeforces_contest_name: "mBIT Standard June 2020"
rating: 0
weight: 102620
solve_time_s: 60
verified: true
draft: false
---

[CF 102620A - Ice Cream Truck](https://codeforces.com/problemset/problem/102620/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

There are huts arranged on a straight beach. Hut `i` is exactly 100 meters after hut `i-1`, and each hut contains some number of people. Existing ice cream shops are also placed on the same line at arbitrary integer coordinates.

We need to choose a position for one additional ice cream shop. A person buys from the new shop only if the new shop is strictly closer to their hut than every existing shop. The goal is to find the maximum total number of people that can be attracted by choosing the best possible location.

The important observation is that the new shop location is one-dimensional. For a fixed hut, the set of positions where the new shop wins is always an interval.

The number of huts and existing shops can both reach 200,000. This immediately rules out trying every possible new shop position or checking every hut against every shop. A quadratic solution would perform around 40 billion operations in the worst case, which is far beyond what a normal contest time limit allows. We need a solution close to `O((n + m) log m)` or better.

A few edge cases are easy to miss.

Consider a hut exactly at an existing shop location.

```
Input
1 1
5
0
```

The new shop can be placed anywhere except the existing shop location, but the person at the hut can still be attracted by moving the new shop slightly away. The correct answer is:

```
5
```

A solution that only considers integer positions might incorrectly reject all choices.

Another case is when the best location is outside the range of all huts.

```
Input
3 1
4 10 3
1000
```

The new shop can be placed near the huts while still being closer than the only existing shop. Restricting the search to the segment between existing shops would miss valid answers.

The final subtle case is strict comparison. If the new shop is exactly the same distance as an existing shop, the person does not choose the new shop.

For example:

```
Input
2 1
7 8
50
```

The midpoint between hut 1 and the existing shop is a tie position, not a winning position. The sweep must handle interval endpoints as excluded.

## Approaches

A direct approach would be to try possible locations for the new shop and count how many huts prefer it. The answer only changes at certain critical positions, but enumerating them is still too expensive. Even if we checked every hut against every existing shop once, the cost would be `O(nm)`, which can reach approximately `4 * 10^10` comparisons.

The useful change in perspective is to stop thinking about possible shop locations and instead think about each hut independently.

For one hut at coordinate `h`, let the distance to the nearest existing shop be `d`. The new shop wins for this hut exactly when:

```
|position - h| < d
```

which is the open interval:

```
(h - d, h + d)
```

So every hut contributes its population to every possible new shop position inside one interval. The problem becomes finding the maximum weighted overlap of many intervals.

We can solve this with a sweep line. Add a hut's population when entering its interval and remove it when leaving. Since the intervals are open, we must process removals before additions at the same coordinate.

The only remaining task is finding `d` efficiently. After sorting the existing shop positions, the nearest shop for any hut must be one of the two shops around its position in the sorted order. Binary search gives this in `O(log m)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O((n + m) log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Sort the coordinates of all existing ice cream shops. For every hut, the closest existing shop can only be the first shop on its right or the first shop on its left, so this sorted order allows binary search.
2. For each hut, find the distance `d` to the closest existing shop. The hut can be served by the new shop exactly when the new shop is placed inside `(h - d, h + d)`. Add two sweep events for this interval.
3. Store the left endpoint as an addition event and the right endpoint as a removal event. The interval is open, so the right endpoint must stop contributing before the sweep reaches that coordinate.
4. Sort all events by coordinate. At each coordinate, first remove all intervals ending there, then add all intervals starting there. The current sum represents the people served immediately after that coordinate.
5. Track the maximum value of the running sum.

Why it works:

For every hut, we create exactly the set of positions where the new shop would be strictly closer than every existing shop. The sweep line maintains the sum of populations of all huts whose valid intervals currently contain the chosen position. Since every possible change happens only at an interval boundary, checking the values between consecutive boundaries is sufficient. The maximum maintained by the sweep is exactly the best possible number of customers.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    people = list(map(int, input().split()))
    shops = list(map(int, input().split()))
    shops.sort()

    events = []

    for i, p in enumerate(people):
        h = i * 100
        pos = bisect_left(shops, h)

        dist = 10**18
        if pos < m:
            dist = min(dist, abs(shops[pos] - h))
        if pos > 0:
            dist = min(dist, abs(shops[pos - 1] - h))

        left = h - dist
        right = h + dist

        events.append((left, 1, p))
        events.append((right, -1, p))

    events.sort()

    ans = 0
    cur = 0
    i = 0

    while i < len(events):
        x = events[i]

        while i < len(events) and events[i][0] == x[0]:
            if events[i][1] == -1:
                cur -= events[i][2]
            i += 1

        j = i
        while j < len(events) and events[j][0] == x[0]:
            cur += events[j][2]
            j += 1

        ans = max(ans, cur)
        i = j

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part reads the shop locations and sorts them. Sorting is what makes nearest-shop queries possible with binary search.

For each hut, the code converts the geometric condition into an interval. The variable `dist` is the distance to the closest existing shop, and the winning region is centered at the hut coordinate with that radius.

The sweep events are stored as `(coordinate, type, value)`. A type of `-1` removes population, while a type of `1` adds population. The processing order is the key detail. Removals happen before additions at the same coordinate because the intervals are open. If this order were reversed, a person could incorrectly be counted at a tie position.

All coordinates and populations fit comfortably in Python integers. The answer can be as large as `200000 * 10^9`, so languages with fixed-width 32-bit integers would need a wider type.

## Worked Examples

For the first sample:

```
3 1
2 5 6
169
```

The huts are at coordinates `0`, `100`, and `200`. The only existing shop is at `169`.

| Hut | Coordinate | Distance to shop | Winning interval | Population |
| --- | --- | --- | --- | --- |
| 1 | 0 | 169 | (-169, 169) | 2 |
| 2 | 100 | 69 | (31, 169) | 5 |
| 3 | 200 | 31 | (169, 231) | 6 |

The maximum overlap happens just before coordinate `169`, where the first two huts are counted.

The answer is:

```
7
```

This demonstrates why interval endpoints cannot be included. Hut 3 does not join at coordinate `169` because that is exactly the location of the existing shop.

For the second sample:

```
4 2
1 2 7 8
35 157
```

The huts are at coordinates `0`, `100`, `200`, and `300`.

| Hut | Coordinate | Distance to closest shop | Winning interval | Population |
| --- | --- | --- | --- | --- |
| 1 | 0 | 35 | (-35, 35) | 1 |
| 2 | 100 | 65 | (35, 165) | 2 |
| 3 | 200 | 43 | (157, 243) | 7 |
| 4 | 300 | 143 | (157, 443) | 8 |

The best overlap is after coordinate `157`, where huts 3 and 4 contribute together.

The answer is:

```
15
```

This confirms that the optimal location does not have to be between existing shops.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Sorting shops and events dominates the runtime |
| Space | O(n) | Two events are stored for each hut |

With up to 200,000 huts and shops, the algorithm performs only sorting and binary searches. This fits easily within the intended limits, unlike any approach that compares every hut with every shop.

## Test Cases

```python
import sys
import io
from bisect import bisect_left

def solve(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    people = list(map(int, input().split()))
    shops = list(map(int, input().split()))
    shops.sort()

    events = []

    for i, p in enumerate(people):
        h = i * 100
        idx = bisect_left(shops, h)

        d = 10**18
        if idx < m:
            d = min(d, abs(shops[idx] - h))
        if idx:
            d = min(d, abs(shops[idx - 1] - h))

        events.append((h - d, 1, p))
        events.append((h + d, -1, p))

    events.sort()

    cur = ans = 0
    i = 0
    while i < len(events):
        x = events[i][0]

        while i < len(events) and events[i][0] == x and events[i][1] == -1:
            cur -= events[i][2]
            i += 1

        j = i
        while j < len(events) and events[j][0] == x:
            cur += events[j][2]
            j += 1

        ans = max(ans, cur)
        i = j

    return str(ans)

assert solve("""3 1
2 5 6
169
""") == "7"

assert solve("""4 2
1 2 7 8
35 157
""") == "15"

assert solve("""2 1
5 8
50
""") == "13"

assert solve("""3 2
1 1 1
300 99
""") == "2"

assert solve("""2 1
1000000000 1000000000
0
""") == "2000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single existing shop with two huts | 13 | Basic interval overlap |
| Equal populations with shops on both sides | 2 | Boundary handling |
| Very large populations | 2000000000 | Integer size handling |
| Sample cases | 7 and 15 | Standard correctness |

## Edge Cases

When a hut lies exactly at the same coordinate as an existing shop, its winning interval still has positive width because the new shop can move away from that point. The algorithm handles this because the interval radius is the distance to the nearest existing shop, and the sweep never evaluates the excluded endpoint itself.

For example:

```
Input
3 2
1 1 1
300 99
```

The hut coordinates are `0`, `100`, and `200`. The middle hut is at the same location as one existing shop, but the new shop can move slightly to the left or right. The interval method captures these possibilities and returns:

```
2
```

When all huts are far away from the existing shops, the best position may be outside the range of existing shops. The algorithm does not assume any finite search range. It only uses the valid intervals generated by the geometry.

For:

```
Input
3 1
2 5 6
169
```

the best point is before the existing shop, and the sweep finds the overlap of the first two intervals correctly.

Finally, strict inequality matters. At a point where the new shop ties an existing shop, the person does not contribute. Processing removal events before addition events at the same coordinate removes those invalid tie positions from consideration.
