---
title: "CF 105859G - Club Pizza"
description: "The problem describes a student choosing club meetings to attend. Each club has a meeting hour and gives a certain number of pizza slices. Two clubs at the same hour cannot both be attended because the meetings overlap."
date: "2026-06-25T14:41:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105859
codeforces_index: "G"
codeforces_contest_name: "Mines HSPC 2025 Open Division"
rating: 0
weight: 105859
solve_time_s: 37
verified: true
draft: false
---

[CF 105859G - Club Pizza](https://codeforces.com/problemset/problem/105859/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a student choosing club meetings to attend. Each club has a meeting hour and gives a certain number of pizza slices. Two clubs at the same hour cannot both be attended because the meetings overlap. The student also has a maximum number of slices he can eat before becoming full. The goal is to choose a set of clubs that maximizes the number of attended clubs while keeping the total pizza within the limit.

The input gives the number of clubs, the pizza capacity, and then one record per club containing its meeting hour and pizza amount. The output is the largest possible count of clubs that can be selected.

The number of clubs can reach 1000. A solution that tries every subset of clubs would require checking up to $2^{1000}$ possibilities, which is completely impossible. The number of hours, however, is only 24, so the time dimension is tiny. This strongly suggests that the state should be based on hours rather than individual clubs. A dynamic programming solution with roughly $24 \times c$ states is feasible when the pizza capacity is at most $10^6$, because the number of operations stays around a few tens of millions.

There are several easy mistakes. One is forgetting the overlap rule. For example:

```
3 10
5 2
5 3
6 5
```

The correct output is:

```
2
```

A greedy approach that picks the cheapest pizza first could take both clubs at hour 5 and count them as two choices, but that is invalid because only one meeting at hour 5 can be attended.

Another issue is treating clubs with zero pizza incorrectly. Consider:

```
2 0
1 0
2 1
```

The correct output is:

```
1
```

The second club cannot be attended because the student has no remaining capacity, but the first one is free and should be counted.

A final edge case is when several clubs share an hour and the best one is not the one with the smallest pizza. For example:

```
3 5
7 5
7 1
8 4
```

The correct output is:

```
2
```

Choosing the one-slice club at hour 7 allows attending hour 8 as well. A method that processes clubs independently can miss this interaction.

## Approaches

The most direct idea is to try every possible collection of clubs. For every subset, we check whether no two chosen clubs share the same hour and whether the total pizza is within the limit. If it is valid, we keep the maximum number of chosen clubs. This is correct because every possible answer appears among the subsets. The problem is that there are $2^n$ subsets, which becomes impossible even for a few dozen clubs, while here $n$ can be 1000.

The key observation is that the restriction on overlapping meetings only depends on the 24 possible hours. For each hour, we only need to decide which single club to take, if any. The order of processing hours does not matter because selecting a club at one hour never affects the available choices at another hour, except through the total pizza consumed.

This transforms the problem into a knapsack-style dynamic program. We process hours one by one. The state represents how much pizza has been used after considering some prefix of hours, and stores the maximum number of clubs achievable with that amount. For each hour, we either skip the hour or choose one of the clubs happening during it.

The total number of clubs is 1000, but there are only 24 groups of clubs. For each hour we may try all clubs at that hour and all possible pizza amounts, giving a practical bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal DP | $O(24 \times n \times c)$ in the worst case | $O(c)$ | Accepted |

## Algorithm Walkthrough

1. Group all clubs by their meeting hour. Each hour will have a list of possible clubs that can be selected.
2. Create a dynamic programming array where `dp[x]` stores the maximum number of clubs that can be attended using exactly `x` slices of pizza after processing some hours. Initially, only zero pizza used is possible, so `dp[0] = 0`.
3. Process the 24 hours one at a time. For the current hour, create a new array that starts as the previous state. This represents the choice of attending no club at this hour.
4. Try every club at the current hour. For every previous pizza amount `x`, if adding this club's pizza does not exceed the capacity, update the new state with one more attended club.
5. Replace the old state with the new state and continue to the next hour.
6. After all hours are processed, the maximum value stored anywhere in the DP array is the answer, because the student may have any final amount of leftover pizza.

The reason this works is that after processing some hours, the only information needed about the past is how much pizza has been consumed and the maximum number of clubs obtained. The exact choices that created that state do not matter anymore. Every valid schedule corresponds to one path through the hour transitions, and every transition respects the rule that only one club can be selected from each hour.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, c = map(int, input().split())

    hours = [[] for _ in range(24)]

    for _ in range(n):
        t, p = map(int, input().split())
        if p <= c:
            hours[t].append(p)

    dp = [-10**9] * (c + 1)
    dp[0] = 0

    for clubs in hours:
        ndp = dp[:]

        for pizza in clubs:
            for used in range(c - pizza + 1):
                if dp[used] != -10**9:
                    ndp[used + pizza] = max(
                        ndp[used + pizza],
                        dp[used] + 1
                    )

        dp = ndp

    print(max(dp))

if __name__ == "__main__":
    solve()
```

The input is grouped immediately by hour. Clubs with more pizza than the total capacity are ignored because they can never appear in a valid answer.

The DP array uses an impossible negative value for unreachable states. This avoids accidentally extending a state that cannot exist.

For each hour, the copy into `ndp` is necessary. If updates were made directly to `dp`, taking a club could affect later choices in the same hour, allowing multiple clubs from one hour to be counted. The separate array represents the rule that every hour contributes either zero or one club.

The loop over `used` stops at `c - pizza`, which prevents indexing beyond the capacity. Since the maximum capacity is large but the number of hours is fixed, the memory usage stays manageable.

## Worked Examples

For the first sample:

```
3 6
18 3
19 2
20 1
```

The DP evolution can be viewed as follows.

| Hour processed | Available choices | Best club counts by used pizza |
| --- | --- | --- |
| Start | none | pizza 0 gives 0 clubs |
| 18 | 3 slices | pizza 3 gives 1 club |
| 19 | 2 slices | pizza 5 gives 2 clubs |
| 20 | 1 slice | pizza 6 gives 3 clubs |

The final state uses all six slices and attends all three meetings.

For the second sample:

```
3 3
18 3
19 2
20 1
```

| Hour processed | Available choices | Best club counts by used pizza |
| --- | --- | --- |
| Start | none | pizza 0 gives 0 clubs |
| 18 | 3 slices | pizza 3 gives 1 club |
| 19 | 2 slices | pizza 2 gives 1 club |
| 20 | 1 slice | pizza 3 gives 2 clubs |

The student cannot take the three-slice and two-slice clubs together because the capacity would be exceeded. The best choice is the two-slice club and the one-slice club.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(24 \times n \times c)$ | Every hour processes its clubs against all possible pizza amounts |
| Space | $O(c)$ | Only the previous and current DP arrays are stored |

The small number of hours is the key factor. Even with the maximum number of clubs, the number of DP transitions is bounded enough for the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    n = int(next(it))
    c = int(next(it))

    hours = [[] for _ in range(24)]

    for _ in range(n):
        t = int(next(it))
        p = int(next(it))
        if p <= c:
            hours[t].append(p)

    dp = [-10**9] * (c + 1)
    dp[0] = 0

    for clubs in hours:
        ndp = dp[:]
        for pizza in clubs:
            for used in range(c - pizza + 1):
                if dp[used] >= 0:
                    ndp[used + pizza] = max(ndp[used + pizza], dp[used] + 1)
        dp = ndp

    return str(max(dp))

assert solve("""3 6
18 3
19 2
20 1
""") == "3"

assert solve("""3 3
18 3
19 2
20 1
""") == "2"

assert solve("""1 0
5 0
""") == "1"

assert solve("""3 5
7 5
7 1
8 4
""") == "2"

assert solve("""4 10
1 4
1 4
2 6
3 0
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three clubs at different hours with enough pizza | 3 | Basic selection across hours |
| Capacity too small for all clubs | 2 | Pizza limit handling |
| Zero pizza club | 1 | Free club selection |
| Multiple clubs at one hour | 2 | Correct handling of overlap |
| Same-hour alternatives | 2 | Choosing the better hour combination |

## Edge Cases

For the overlapping-hour case:

```
3 10
5 2
5 3
6 5
```

The algorithm creates one group for hour 5 containing two possible choices. When processing hour 5, both choices are considered, but only one transition can survive into the next hour because the next hour starts from the unchanged previous state. The final best state takes one club from hour 5 and the club from hour 6, producing 2.

For the zero-pizza case:

```
2 0
1 0
2 1
```

The club with one slice is removed before DP because it cannot fit. The zero-slice club keeps the transition from pizza 0 to pizza 0 with one more attended club, so the answer becomes 1.

For the case where the cheapest pizza is not enough by itself:

```
3 5
7 5
7 1
8 4
```

Processing hour 7 creates states for taking either 5 slices or 1 slice. The later hour can only be combined with the 1-slice state, giving a total of 5 slices and 2 clubs. This is exactly the decision the DP is designed to preserve.
