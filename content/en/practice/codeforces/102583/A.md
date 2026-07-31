---
title: "CF 102583A - \u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438 \u043d\u0430 \u043f\u0430\u043c\u044f\u0442\u044c"
description: "We have a group of creatures whose heights are given. The photographer wants to split them into the smallest possible number of photos. A photo can contain one, two, or three creatures, but the allowed height differences depend on the number of creatures in the photo."
date: "2026-07-31T07:17:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102583
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102583
solve_time_s: 544
verified: true
draft: false
---

[CF 102583A - \u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438 \u043d\u0430 \u043f\u0430\u043c\u044f\u0442\u044c](https://codeforces.com/problemset/problem/102583/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a group of creatures whose heights are given. The photographer wants to split them into the smallest possible number of photos. A photo can contain one, two, or three creatures, but the allowed height differences depend on the number of creatures in the photo.

For two creatures, the difference between their heights must be at most 20. For three creatures, the difference between the shortest and tallest among them must be at most 10. A single creature can always be photographed alone.

The input contains the number of creatures and their heights. The task is to output the minimum number of photos needed to include everyone exactly once.

The number of creatures is at most 1000, and each height is between 100 and 1000. This means an O(n^2) solution would still be acceptable because one million operations is small, but we should still look for a simpler structure because the problem has sorting properties. A brute force search over all possible groupings would be impossible because the number of ways to partition 1000 creatures grows extremely quickly.

The important edge cases come from the difference between the limits for two and three creatures. A group of three can be invalid even when every pair inside it looks acceptable. For example:

```
3
100 110 120
```

The correct answer is 2. The three creatures cannot share one photo because the total height range is 20, but the two pairs 100 and 110, and 110 and 120 can each be photographed together.

Another case is when only two creatures are close enough:

```
3
100 115 200
```

The correct answer is 2. A careless solution that only checks whether the smallest and largest height difference is small enough might incorrectly reject the pair 100 and 115 and produce 3 photos.

A final boundary case is when all creatures have the same height:

```
4
500 500 500 500
```

The correct answer is 2 because every group of three is valid, but one photo cannot contain four creatures.

## Approaches

A direct approach is to try every possible way to divide the creatures into groups of one, two, and three, checking whether each group satisfies the photo rules. This approach is correct because it examines every possible arrangement and chooses the smallest number of photos. However, the number of partitions is enormous. Even with only 1000 creatures, exploring all groupings is far beyond feasible limits.

The useful observation comes from the fact that only height differences matter. After sorting the heights, creatures that are close enough to be together will appear next to each other. There is no advantage in placing a shorter creature together with a much taller creature while leaving a nearby creature alone.

After sorting, the problem becomes a dynamic programming problem over prefixes. Let dp[i] be the minimum number of photos needed for the first i sorted creatures. When considering creature i as the last creature in the prefix, there are only three possible endings: the last photo contains one creature, two creatures, or three creatures. These are the only cases because a photo cannot contain more than three creatures.

The transition checks whether the last two or last three sorted heights satisfy the required limits. Taking the minimum over valid choices gives the optimal answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Dynamic Programming after sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all heights in nondecreasing order. After sorting, any valid group of several creatures can be considered as a consecutive segment, because separating close heights while grouping farther ones cannot improve the number of photos.
2. Create a dynamic programming array where dp[i] represents the minimum number of photos required for the first i creatures in sorted order.
3. Initialize dp[0] as 0 because no creatures require no photos.
4. For each position i from 1 to n, first consider taking the i-th creature alone. This gives the transition dp[i] = dp[i - 1] + 1.
5. If the last two creatures form a valid pair, update dp[i] using dp[i - 2] + 1. The pair is valid when the difference between their heights is at most 20.
6. If the last three creatures form a valid group, update dp[i] using dp[i - 3] + 1. The triple is valid when the difference between the largest and smallest of these three heights is at most 10.
7. The value dp[n] is the answer because it describes the minimum number of photos needed for all sorted creatures.

Why it works:

The dynamic programming state considers every possible way the final photo can be formed. Any optimal solution for the first i creatures must end with either one, two, or three creatures in the final photo. Removing that final photo leaves an optimal solution for a smaller prefix, because otherwise we could replace it with a better one and improve the original solution. The transitions test exactly these possible endings, so dp[i] always stores the true minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    inf = 10**9
    dp = [inf] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + 1

        if i >= 2 and a[i - 1] - a[i - 2] <= 20:
            dp[i] = min(dp[i], dp[i - 2] + 1)

        if i >= 3 and a[i - 1] - a[i - 3] <= 10:
            dp[i] = min(dp[i], dp[i - 3] + 1)

    print(dp[n])

if __name__ == "__main__":
    solve()
```

The sorting step places similar heights next to each other, which allows the dynamic programming transitions to examine only the last few creatures. Without sorting, a valid group could be spread across the array and the local transitions would not represent all possibilities.

The array has size n + 1 because dp[0] represents the empty prefix. The checks for pairs and triples use i as a count of processed creatures, so the last processed index is i - 1. The conditions use these indices carefully to avoid accessing elements before the beginning of the array.

The single creature transition is always available, so every state receives an initial valid value. The pair and triple transitions only improve that value when their height restrictions are satisfied.

## Worked Examples

For the first sample:

```
3
100 300 200
```

After sorting, the heights are 100, 200, 300.

| i | Processed heights | Single photo option | Pair option | Triple option | dp[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | none | 0 | not checked | not checked | 0 |
| 1 | 100 | 1 | not checked | not checked | 1 |
| 2 | 100, 200 | 2 | invalid, difference 100 | not checked | 2 |
| 3 | 100, 200, 300 | 3 | invalid | invalid, range 200 | 3 |

The three creatures are too far apart, so each one needs its own photo.

For the second sample:

```
3
110 120 130
```

The sorted order is already 110, 120, 130.

| i | Processed heights | Single photo option | Pair option | Triple option | dp[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | none | 0 | not checked | not checked | 0 |
| 1 | 110 | 1 | not checked | not checked | 1 |
| 2 | 110, 120 | 2 | valid, gives 1 | not checked | 1 |
| 3 | 110, 120, 130 | 2 | valid, gives 2 | invalid, range 20 | 2 |

The first two creatures can share a photo, and the third one joins the remaining photo with either neighbor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the linear dynamic programming pass |
| Space | O(n) | The dp array stores one value for each prefix |

With n equal to 1000, this solution is easily within the limits. The sorting step is the most expensive operation, while the dynamic programming part performs only a constant amount of work per creature.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    dp = [10**9] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + 1
        if i >= 2 and a[i - 1] - a[i - 2] <= 20:
            dp[i] = min(dp[i], dp[i - 2] + 1)
        if i >= 3 and a[i - 1] - a[i - 3] <= 10:
            dp[i] = min(dp[i], dp[i - 3] + 1)

    sys.stdin = old_stdin
    return str(dp[n])

assert solve_data("3\n100 300 200\n") == "3"
assert solve_data("3\n110 120 130\n") == "2"
assert solve_data("6\n100 210 250 255 220 260\n") == "3"

assert solve_data("1\n500\n") == "1"
assert solve_data("4\n500 500 500 500\n") == "2"
assert solve_data("3\n100 115 200\n") == "2"
assert solve_data("6\n100 101 102 103 104 105\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 500` | 1 | The smallest possible input |
| `4 / 500 500 500 500` | 2 | Groups of three are allowed, groups of four are not |
| `3 / 100 115 200` | 2 | Pair boundary with difference 15 |
| `6 / 100 101 102 103 104 105` | 2 | Multiple valid triples and greedy-looking traps |

## Edge Cases

For the case:

```
3
100 110 120
```

Sorting does nothing. The triple transition checks the range 120 - 100, which is 20, so the group of three is rejected. The pair transition accepts 100 and 110, giving two photos. The algorithm returns 2.

For the case:

```
3
100 115 200
```

The sorted array is 100, 115, 200. The pair of the first two creatures is valid because the difference is 15. The last creature cannot join either group because its difference is too large. The dynamic programming values become 1 for the first two creatures and 2 after adding the third, giving the correct result.

For the case:

```
4
500 500 500 500
```

Every possible pair and triple check succeeds. The best arrangement is one triple and one single creature, because the rules limit each photo to three creatures. The dynamic programming transitions find dp[3] = 1 and then dp[4] = 2, which is optimal.

I can also provide a shorter Codeforces-style editorial version if you want one closer to what would appear on the contest page.
