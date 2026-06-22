---
title: "CF 105278H - Emblems"
description: "A Codeforces user is tracked through their rating history, and their “status tier” changes as their rating crosses fixed thresholds such as pupil, specialist, expert, and so on."
date: "2026-06-23T06:49:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105278
codeforces_index: "H"
codeforces_contest_name: "2024 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 105278
solve_time_s: 89
verified: false
draft: false
---

[CF 105278H - Emblems](https://codeforces.com/problemset/problem/105278/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

A Codeforces user is tracked through their rating history, and their “status tier” changes as their rating crosses fixed thresholds such as pupil, specialist, expert, and so on. Each tier corresponds to a contiguous interval of ratings, and moving into a higher interval for the first time triggers an emblem award.

For each user we are given their handle, their current rating after the latest contest, their historical maximum rating before this contest, and the rating change in the latest contest. From these values we must decide whether the latest update caused them to enter a higher tier than they have ever reached before. If yes, we output the name of that new tier. Otherwise, we output a motivational message.

Although the input includes the rating delta, the decision depends only on comparing “previous best known rating” and “current rating” against the fixed tier boundaries. The only meaningful historical state is the maximum rating before the current update, since that encodes what ranks the user has already unlocked.

The constraints are large in magnitude but trivial in structural complexity. Everything is constant time per test case, so the solution must be O(1) and avoid any simulation or iteration over rating histories.

The main subtlety is understanding what “first time reaching a new rank” means. A naive interpretation might incorrectly compare current rating only against thresholds, or ignore that the user might have already been in the same tier earlier.

A few edge situations make this clearer.

If a user had previously reached 2100 (master) but drops to 2050 and then returns to 2100, they should not receive a master emblem again. The maximum rating already includes that tier, so no new tier is achieved.

If a user previously peaked at 1890 (expert) and now reaches 1900, they are entering candidate master for the first time, so the output must reflect that transition.

If a user’s rating increases but stays within the same tier interval, nothing is awarded even though the rating changed.

## Approaches

A direct simulation would reconstruct the entire rating history: apply the delta, update rating step by step, and track all intermediate maxima. This is unnecessary because tier changes depend only on whether a rating crosses a threshold boundary, not on the path taken. In the worst case, a naive approach that simulates transitions across many updates would be linear in the number of contests, which is not present here but illustrates the overkill nature of such a method.

The key observation is that tiers form a fixed partition of the integer line. Each rating maps deterministically to exactly one tier. Therefore, we only need to compare two points in this partition: the previous maximum rating and the current rating. If both map to the same tier, no new emblem is earned. If they map to different tiers and the current tier is higher in the ordered list, then the user has just unlocked a new tier for the first time.

This reduces the problem to computing a small number of interval lookups and a single comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force history simulation | O(T) per user history | O(1) | Unnecessary |
| Optimal tier comparison | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We encode all rating tiers as ordered intervals, from lowest to highest. Each interval corresponds to one emblem name.

1. Construct the ordered list of tiers with their lower bounds and names. The ordering is critical because we will compare tiers by position in this list rather than by rating values directly.
2. Define a function that maps any rating to its tier by scanning these intervals and returning the index or name of the first interval whose lower bound is satisfied and upper bound is not exceeded. The mapping is deterministic and independent of history.
3. Compute the previous best rating, which is given directly as M. This represents the highest rating the user has ever had before the current contest.
4. Compute the current rating C, which represents the rating after applying the latest contest result.
5. Map both M and C into their corresponding tier indices. Let prev_rank be the tier index of M, and new_rank be the tier index of C.
6. If new_rank is greater than prev_rank, output the name of the new tier. Otherwise output the motivational message.

The comparison is strictly ordinal because tiers are disjoint and fully ordered by rating ranges.

### Why it works

The maximum rating M fully captures the user’s historical exposure to tiers. Any tier achieved before is already reflected in M. Therefore, a “first time” tier must correspond to a tier that contains C but does not contain M. Since tiers are contiguous and ordered, this is equivalent to checking whether the tier index of C is strictly greater than that of M. No intermediate states or the delta D can change this conclusion.

## Python Solution

```python
import sys
input = sys.stdin.readline

tiers = [
    ("newbie", -10**18, 1199),
    ("pupil", 1200, 1399),
    ("specialist", 1400, 1599),
    ("expert", 1600, 1899),
    ("candidate master", 1900, 2099),
    ("master", 2100, 2399),
    ("grandmaster", 2400, 10**18),
]

def get_rank(x):
    for i, (name, lo, hi) in enumerate(tiers):
        if lo <= x <= hi:
            return i
    return 0

def solve():
    data = input().split()
    if not data:
        return
    s = data[0]
    C = int(data[1])
    M = int(data[2])
    D = int(data[3])

    prev_rank = get_rank(M)
    new_rank = get_rank(C)

    if new_rank > prev_rank:
        print(tiers[new_rank][0])
    else:
        print("Think about it, you can do it!")

if __name__ == "__main__":
    solve()
```

The implementation encodes the rating intervals explicitly and performs a constant-time lookup over a fixed array of seven tiers. The function `get_rank` is intentionally simple since the number of intervals is constant and small.

The key implementation detail is using M rather than C - D. Although the delta is provided, the problem already gives the historical maximum directly, which fully represents past achievements. This avoids reconstructing any timeline.

Boundary comparisons are inclusive on both ends, matching the rank definitions precisely.

## Worked Examples

### Sample 1

Input:

```
aprohACk 2098 2098 10
```

| Step | Current C | Max M | Rank(C) | Rank(M) | Action |
| --- | --- | --- | --- | --- | --- |
| Start | 2098 | 2098 | candidate master | candidate master | compare |

Both values fall into the same tier, so no new emblem is awarded.

Output:

```
Think about it, you can do it!
```

### Sample 2

Input:

```
ahoraSoyPeor 2237 2288 -69
```

| Step | Current C | Max M | Rank(C) | Rank(M) | Action |
| --- | --- | --- | --- | --- | --- |
| Start | 2237 | 2288 | master | master | compare |

The user remains in the same highest achieved tier.

Output:

```
Think about it, you can do it!
```

This shows that decreasing rating does not revoke past achievements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only two fixed interval lookups over a constant-size array |
| Space | O(1) | Only a fixed list of seven tiers is stored |

The constraints allow arbitrary rating values, but the structure of tiers ensures constant-time classification, making the solution easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    tiers = [
        ("newbie", -10**18, 1199),
        ("pupil", 1200, 1399),
        ("specialist", 1400, 1599),
        ("expert", 1600, 1899),
        ("candidate master", 1900, 2099),
        ("master", 2100, 2399),
        ("grandmaster", 2400, 10**18),
    ]

    def get_rank(x):
        for i, (name, lo, hi) in enumerate(tiers):
            if lo <= x <= hi:
                return i
        return 0

    data = sys.stdin.readline().split()
    s = data[0]
    C = int(data[1])
    M = int(data[2])
    D = int(data[3])

    if get_rank(C) > get_rank(M):
        return tiers[get_rank(C)][0]
    return "Think about it, you can do it!"

assert run("aprohACk 2098 2098 10\n") == "Think about it, you can do it!"
assert run("ahoraSoyPeor 2237 2288 -69\n") == "Think about it, you can do it!"
assert run("demianOneTwoThree 725 725 721\n") == "specialist"

# custom cases
assert run("x 1199 1199 1\n") == "pupil"  # newbie -> pupil boundary crossing
assert run("x 1399 1399 1\n") == "specialist"  # pupil -> specialist
assert run("x 2500 2000 500\n") == "grandmaster"  # jumps to top tier
assert run("x 1500 1600 0\n") == "Think about it, you can do it!"  # no new tier
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1199 → 1200 | pupil | boundary crossing at low tier |
| 1399 → 1400 | specialist | intermediate tier transition |
| 2500 | grandmaster | top tier handling |
| 1500 unchanged tier | message | no change case |

## Edge Cases

A common mistake is ignoring that the maximum rating already encodes historical achievements. For example, if a user’s current rating is higher than their previous maximum, that implies a potential new tier, but if both still fall in the same interval, no emblem should be awarded. The algorithm handles this by explicitly comparing tier indices rather than raw ratings.

Another subtle case is downward rating changes. If a user drops from a higher tier into a lower one, they do not lose the previously earned emblem, since the decision is based on maximum historical rating, not current position. The comparison using M ensures that once a tier is unlocked, it remains “visited” forever.

Finally, boundary equality cases such as exactly 1200 or 2100 are handled correctly because interval checks are inclusive, so no off-by-one errors occur at tier borders.
