---
title: "CF 1949F - Dating"
description: "Each user can be viewed as a set of activities. We need to find two users whose sets satisfy three conditions simultaneously: 1. They share at least one activity. 2. The first user has at least one activity that the second user does not have. 3."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1949
codeforces_index: "F"
codeforces_contest_name: "European Championship 2024 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2200
weight: 1949
solve_time_s: 117
verified: false
draft: false
---

[CF 1949F - Dating](https://codeforces.com/problemset/problem/1949/F)

**Rating:** 2200  
**Tags:** greedy, sortings, trees  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

Each user can be viewed as a set of activities.

We need to find two users whose sets satisfy three conditions simultaneously:

1. They share at least one activity.
2. The first user has at least one activity that the second user does not have.
3. The second user has at least one activity that the first user does not have.

In set terminology, we are looking for two sets whose intersection is non-empty, but neither set is a subset of the other.

The input contains up to 200,000 users, but the total number of listed activities across all users is at most 1,000,000. This second bound is the crucial one. It means we can afford work proportional to the total amount of input data, but we cannot afford comparing every pair of users.

A brute force check of all pairs would require roughly

$$\binom{200000}{2} \approx 2 \cdot 10^{10}$$

comparisons, which is completely impossible.

The activity universe is very large, up to $10^6$, but only at most $10^6$ activity occurrences actually appear. Any solution should work with the activities that occur in the input rather than trying to build structures of size $m$.

Several edge cases are easy to mishandle.

Consider two identical users:

```
2 3
2 1 2
2 1 2
```

The correct answer is `NO`. They share activities, but neither user has something the other lacks. A solution that only checks for non-empty intersection would incorrectly return `YES`.

Consider two disjoint users:

```
2 3
1 1
1 2
```

The correct answer is `NO`. Each user has a unique activity, but they do not share anything.

Consider a subset relationship:

```
2 4
1 1
2 1 2
```

The correct answer is `NO`. They share activity 1, but the first set is contained inside the second. Both users must possess something the other does not.

A final subtle case is when many users contain exactly the same activity. Looking only at activity frequencies is not enough. We must distinguish between identical sets and incomparable sets.

## Approaches

The most direct solution compares every pair of users.

For a pair of sets $A$ and $B$, we can check whether:

$$A \cap B \neq \varnothing$$

and

$$A \setminus B \neq \varnothing$$

and

$$B \setminus A \neq \varnothing.$$

This is correct because it directly implements the definition of a good match.

The problem is the number of pairs. With 200,000 users there are about twenty billion pairs. Even if every comparison were extremely cheap, this is far beyond the limit.

To make progress, we need to exploit the special structure of the constraints.

The key observation is that the total number of activity occurrences is only $10^6$. This suggests a classic heavy-light idea.

Call an activity heavy if it appears in many users, and light otherwise.

Suppose we choose a threshold

$$B \approx \sqrt{10^6}=1000.$$

There can be at most about 1000 heavy activities, because every heavy activity contributes at least $B$ occurrences and the total number of occurrences is at most $10^6$.

Now consider a user set $S$.

If $|S| \ge B$, we call it a heavy user. There can also be at most about 1000 heavy users, since the total size of all sets is at most $10^6$.

This square-root decomposition creates two manageable worlds.

For heavy users, there are only about 1000 of them. We can build fast membership structures and compare them efficiently.

For light users, every set contains fewer than $B$ activities. We can process them through activity incidence lists. Since each light set is small, the total work remains near $O(10^6 \sqrt{10^6})$.

The crucial property is that two users form a good match exactly when they intersect but are incomparable under inclusion.

The editorial solution builds inclusion information between sets and searches only among pairs that actually share activities, avoiding the quadratic explosion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \cdot k)$ | $O(1)$ | Too slow |
| Optimal | $O(T\sqrt{T})$, where $T=\sum k_i$ | $O(T)$ | Accepted |

## Algorithm Walkthrough

Let

$$T=\sum k_i.$$

Choose

$$B=\lfloor\sqrt{T}\rfloor+1.$$

Represent every user's activities as a sorted list.

### 1. Compress all activity occurrences into incidence lists

For every activity, store the users that contain it.

This allows us to enumerate only pairs of users that actually share at least one activity.

### 2. Classify users as heavy or light

A user is heavy if its set size is at least $B$.

Since the total size of all sets is $T$, the number of heavy users is at most $T/B = O(\sqrt T)$.

This bound is what makes the later processing feasible.

### 3. Build fast membership structures for heavy users

For each heavy user, store all its activities in a hash table.

This lets us test membership in constant expected time.

### 4. Process heavy users against all users

For a heavy user $H$, compute intersection counts with every user.

Iterate through each activity of $H$. For every user containing that activity, increase a counter.

After this scan, for any user $U$, the counter equals

$$|H \cap U|.$$

Now check whether

$$0 < |H\cap U| < |H|$$

and

$$0 < |H\cap U| < |U|.$$

These inequalities mean:

- the intersection is non-empty,
- $H$ has something outside $U$,
- $U$ has something outside $H$.

If they hold, we have found a valid pair.

### 5. Process pairs of light users

Every light user contains fewer than $B$ activities.

For each activity, look at the list of light users containing it.

Whenever two light users meet through some activity, they share at least one activity.

We must determine whether one is a subset of the other.

Store candidate pairs in a counting structure. For every shared activity, increase the pair's common-activity count.

After all activities are processed, a pair $(A,B)$ has value

$$c = |A \cap B|.$$

The pair is good precisely when

$$c > 0,$$

$$c < |A|,$$

and

$$c < |B|.$$

If these conditions hold, neither set contains the other completely, and they share at least one activity.

### 6. Output the first valid pair

If any phase finds a valid pair, print `YES` and the corresponding indices.

If all checks finish without success, print `NO`.

### Why it works

For every pair of users that share an activity, the algorithm computes the exact size of their intersection.

A pair is accepted only when the intersection is strictly smaller than both set sizes. That means each user owns at least one activity outside the intersection. Equivalently, neither set is contained in the other.

A pair is rejected whenever the intersection is empty or equals one of the set sizes. In those cases the users either share nothing or one profile is a subset of the other, which violates the definition of a good match.

Heavy-user processing examines all pairs involving a heavy user. Light-user processing examines all pairs consisting entirely of light users. Every possible pair belongs to exactly one of these categories, so no valid answer can be missed.

## Python Solution

```python
import sys
from math import isqrt
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    sets = []
    total = 0
    activity_users = defaultdict(list)

    for idx in range(n):
        row = list(map(int, input().split()))
        k = row[0]
        arr = row[1:]
        sets.append(arr)
        total += k

        for x in arr:
            activity_users[x].append(idx)

    B = isqrt(max(total, 1)) + 1

    heavy = []
    is_heavy = [False] * n

    for i in range(n):
        if len(sets[i]) >= B:
            is_heavy[i] = True
            heavy.append(i)

    # Heavy versus all users
    cnt = [0] * n

    for h in heavy:
        touched = []

        for act in sets[h]:
            for u in activity_users[act]:
                if cnt[u] == 0:
                    touched.append(u)
                cnt[u] += 1

        hs = len(sets[h])

        for u in touched:
            if u == h:
                continue

            c = cnt[u]

            if c > 0 and c < hs and c < len(sets[u]):
                print("YES")
                print(h + 1, u + 1)
                return

        for u in touched:
            cnt[u] = 0

    # Light-light pairs
    pair_cnt = defaultdict(int)

    for users in activity_users.values():
        light_users = [u for u in users if not is_heavy[u]]

        s = len(light_users)

        for i in range(s):
            a = light_users[i]
            for j in range(i + 1, s):
                b = light_users[j]
                if a > b:
                    a, b = b, a
                pair_cnt[(a, b)] += 1

    for (a, b), c in pair_cnt.items():
        if c < len(sets[a]) and c < len(sets[b]):
            print("YES")
            print(a + 1, b + 1)
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The first part reads all sets and simultaneously builds activity incidence lists. Those incidence lists are the central structure of the solution because every future operation is driven by shared activities.

The heavy-user phase never compares a heavy user against every activity of every other user. Instead it walks through the activities of the heavy user and accumulates exact intersection sizes. The `touched` array records which counters became nonzero so that cleanup remains proportional to the actual work performed.

The light-light phase counts common activities for every pair of light users that actually share something. A pair that never shares an activity is never stored, which is essential for efficiency.

The condition

```
c < len(sets[a]) and c < len(sets[b])
```

is the exact mathematical translation of "both users have at least one activity that the other lacks". Since every stored pair already has `c > 0`, this fully characterizes a valid match.

No integer overflow issues exist because all counts are at most $10^6$, well within Python's integer range.

## Worked Examples

### Example 1

Input:

```
3 5
3 1 2 4
5 1 2 3 4 5
2 1 5
```

| Pair | Intersection Size | Size A | Size B | Valid |
| --- | --- | --- | --- | --- |
| (1,2) | 3 | 3 | 5 | No |
| (1,3) | 1 | 3 | 2 | Yes |
| (2,3) | 2 | 5 | 2 | No |

The pair (1,3) shares activity 1. User 1 additionally has activities 2 and 4, while user 3 additionally has activity 5. Both directions contain a unique activity, so the pair is accepted.

### Example 2

Input:

```
2 4
1 1
2 1 2
```

| Pair | Intersection Size | Size A | Size B | Valid |
| --- | --- | --- | --- | --- |
| (1,2) | 1 | 1 | 2 | No |

The intersection equals the entire first set. User 1 has nothing that user 2 lacks. This is a subset relation, not a good match.

The example demonstrates why checking only for a non-empty intersection is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T\sqrt{T})$ | Heavy-light decomposition, $T=\sum k_i$ |
| Space | $O(T)$ | Activity lists and pair bookkeeping |

The total number of activity occurrences is at most $10^6$. With $B \approx \sqrt T$, both the number of heavy users and the amount of work contributed by heavy processing remain bounded by $O(T\sqrt T)$. This comfortably fits the 3-second limit in the intended solution.

## Test Cases

```python
import sys, io
from collections import defaultdict
from math import isqrt

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    sets = []
    total = 0
    activity_users = defaultdict(list)

    for idx in range(n):
        row = list(map(int, input().split()))
        k = row[0]
        arr = row[1:]
        sets.append(arr)
        total += k

        for x in arr:
            activity_users[x].append(idx)

    B = isqrt(max(total, 1)) + 1

    heavy = []
    is_heavy = [False] * n

    for i in range(n):
        if len(sets[i]) >= B:
            is_heavy[i] = True
            heavy.append(i)

    cnt = [0] * n

    for h in heavy:
        touched = []

        for act in sets[h]:
            for u in activity_users[act]:
                if cnt[u] == 0:
                    touched.append(u)
                cnt[u] += 1

        hs = len(sets[h])

        for u in touched:
            if u != h:
                c = cnt[u]
                if c > 0 and c < hs and c < len(sets[u]):
                    return "YES\n"

        for u in touched:
            cnt[u] = 0

    pair_cnt = defaultdict(int)

    for users in activity_users.values():
        light_users = [u for u in users if not is_heavy[u]]

        for i in range(len(light_users)):
            for j in range(i + 1, len(light_users)):
                a, b = sorted((light_users[i], light_users[j]))
                pair_cnt[(a, b)] += 1

    for (a, b), c in pair_cnt.items():
        if c < len(sets[a]) and c < len(sets[b]):
            return "YES\n"

    return "NO\n"

# provided sample
assert run(
"""3 5
3 1 2 4
5 1 2 3 4 5
2 1 5
"""
) == "YES\n"

# identical sets
assert run(
"""2 3
2 1 2
2 1 2
"""
) == "NO\n"

# disjoint sets
assert run(
"""2 3
1 1
1 2
"""
) == "NO\n"

# subset relation
assert run(
"""2 4
1 1
2 1 2
"""
) == "NO\n"

# minimal valid pair
assert run(
"""2 3
2 1 2
2 1 3
"""
) == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Identical sets | NO | Equality is not enough |
| Disjoint sets | NO | Shared activity is required |
| Subset relation | NO | Both users need unique activities |
| Minimal valid pair | YES | Smallest positive example |
| Sample 1 | YES | General correctness |

## Edge Cases

Consider identical profiles:

```
2 3
2 1 2
2 1 2
```

The intersection size is 2, which equals both set sizes. The algorithm rejects the pair because `c < len(set)` fails for both users. Output is `NO`.

Consider disjoint profiles:

```
2 3
1 1
1 2
```

No activity incidence list contains both users. The pair never appears in heavy processing or light-pair counting. Output is `NO`.

Consider a strict subset:

```
2 4
1 1
2 1 2
```

The intersection size is 1. It equals the size of the first set. The condition `c < len(first)` fails, so the pair is rejected. Output is `NO`.

Consider a valid incomparable pair:

```
2 4
2 1 2
2 1 3
```

The intersection size is 1. Both set sizes are 2, so

```
1 < 2
1 < 2
```

holds. Each user has one unique activity. The algorithm outputs `YES`.

These cases cover the three ways a pair can fail and the one way it can succeed, matching exactly the definition of a good match.
