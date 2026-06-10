---
title: "CF 1482C - Basic Diplomacy"
description: "We have m days. On each day, a specific set of friends is available, and we must choose exactly one available friend for that day. The assignment must satisfy a fairness condition. Let limit = ceil(m / 2). No friend may be chosen more than limit times across all days."
date: "2026-06-10T23:26:28+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1482
codeforces_index: "C"
codeforces_contest_name: "\u0422\u0435\u0445\u043d\u043e\u043a\u0443\u0431\u043e\u043a 2021 - \u0424\u0438\u043d\u0430\u043b"
rating: 1600
weight: 1482
solve_time_s: 368
verified: false
draft: false
---

[CF 1482C - Basic Diplomacy](https://codeforces.com/problemset/problem/1482/C)

**Rating:** 1600  
**Tags:** brute force, constructive algorithms, greedy, implementation  
**Solve time:** 6m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We have `m` days. On each day, a specific set of friends is available, and we must choose exactly one available friend for that day.

The assignment must satisfy a fairness condition. Let `limit = ceil(m / 2)`. No friend may be chosen more than `limit` times across all days.

For every day, the input provides the list of friends who can play on that day. Our task is to either construct a valid assignment or determine that none exists.

The constraints are the first clue that the solution cannot be complicated. The total number of days across all test cases is at most `100000`, and the total number of availability entries across all lists is at most `200000`. This means we should aim for a solution that processes each availability list only a constant number of times. Anything exponential is immediately impossible, and even quadratic work in `m` would exceed the limit.

The tricky part is that the choices are not independent. Picking a friend today affects whether we can still use that friend tomorrow without violating the maximum frequency constraint.

A few edge cases deserve attention.

Consider a case where every day has only one available friend:

```
m = 3

Day 1: {1}
Day 2: {1}
Day 3: {1}
```

The only possible assignment is friend `1` three times. Since `ceil(3/2)=2`, friend `1` would be chosen more than the allowed limit. The correct answer is `NO`.

Another subtle case is when one friend appears in many lists, but those lists also contain alternatives:

```
m = 5

{1}
{1,2}
{1,2}
{1,3}
{1,4}
```

A greedy strategy that always picks the first available friend would choose friend `1` five times and fail. A valid assignment exists by redirecting some flexible days to other friends.

A final important scenario is when exactly one friend exceeds the limit after an initial assignment:

```
m = 6

{1}
{1}
{1}
{1,2}
{1,3}
{1,4}
```

Here `limit = 3`. Friend `1` is forced on the first three days and would initially be selected on all six days. We must recognize that only the days with multiple options can be reassigned. If there are enough such days, the answer is possible. If not, it is impossible.

## Approaches

A brute-force solution would try all possible assignments. For each day, choose one available friend and recursively continue. If a day contains up to `n` candidates, the search space becomes roughly

$$\prod_{i=1}^{m} k_i$$

which is exponential in the number of days. Even with only twenty days and two options per day, there are already over one million assignments to examine. With up to one hundred thousand days, this approach is completely infeasible.

The key observation comes from asking what can actually cause failure.

Suppose we initially assign every day to the first friend in its availability list. Count how many times each friend is chosen.

If no friend exceeds `ceil(m/2)`, we are already done.

Now suppose some friend `x` exceeds the limit. Can more than one friend exceed the limit simultaneously?

No. If two different friends each appeared more than `m/2` times, their total occurrences would exceed `m`, which is impossible because there are only `m` days.

This dramatically simplifies the problem. At most one friend can violate the restriction.

Assume friend `x` is chosen too many times. The only way to reduce `x`'s count is to change days currently assigned to `x`. Days with a single available friend cannot be changed. Days whose availability list contains additional friends can be reassigned to somebody else.

So the strategy becomes:

1. Initially assign every day to its first listed friend.
2. Find whether some friend `x` exceeds the limit.
3. If not, answer `YES`.
4. Otherwise, repeatedly move flexible days assigned to `x` toward another available friend until `x`'s count falls to the limit.
5. If we run out of flexible days before reaching the limit, answer `NO`.

The reason this works is that only one friend can ever be problematic, and changing a day away from that friend can never create a new violation because every other friend's count only increases from a value that was already at most the limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential recursion/state | Too slow |
| Optimal | O(Σkᵢ) | O(m + n) | Accepted |

## Algorithm Walkthrough

1. Let `limit = (m + 1) // 2`.
2. For every day, initially choose the first friend listed in that day's availability list.
3. Count how many times each friend is currently selected.
4. Find a friend `x` whose count exceeds `limit`.
5. If no such friend exists, print `YES` and the current assignment.
6. Otherwise, compute

```
excess = count[x] - limit
```

This is the number of selections that must be moved away from friend `x`.
7. Scan all days.

If a day is currently assigned to `x` and the day has at least two available friends, reassign that day to any other available friend, for example the second friend in the list.
8. After each reassignment, decrease `excess` by one.
9. Stop once `excess` becomes zero.
10. If `excess` is still positive after examining all days, print `NO`.
11. Otherwise print `YES` and the final assignment.

### Why it works

The initial assignment may violate the limit for at most one friend. Let that friend be `x`.

Every valid solution must reduce the number of times `x` is selected by exactly `count[x] - limit`. The only days that can help are days assigned to `x` that have multiple available choices. Reassigning any such day decreases `x`'s count by one.

No reassignment can create a new violation. Before modification, every friend other than `x` already appears at most `limit` times. During the process we increase their counts, but the total number of increases is exactly the amount by which `x` exceeded the limit. Once `x` reaches the limit, every other friend still remains at most the limit.

Thus, if enough flexible days exist, the construction succeeds. If not enough flexible days exist, no solution can exist because the required reductions of `x` are impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())

        days = []
        ans = []
        cnt = [0] * (n + 1)

        for _ in range(m):
            arr = list(map(int, input().split()))
            k = arr[0]
            friends = arr[1:]

            days.append(friends)

            chosen = friends[0]
            ans.append(chosen)
            cnt[chosen] += 1

        limit = (m + 1) // 2

        bad = -1
        for friend in range(1, n + 1):
            if cnt[friend] > limit:
                bad = friend
                break

        if bad == -1:
            print("YES")
            print(*ans)
            continue

        need = cnt[bad] - limit

        for i in range(m):
            if need == 0:
                break

            friends = days[i]

            if ans[i] == bad and len(friends) > 1:
                cnt[bad] -= 1
                ans[i] = friends[1]
                need -= 1

        if need > 0:
            print("NO")
        else:
            print("YES")
            print(*ans)

solve()
```

The implementation follows the proof almost directly.

The first friend in every availability list becomes the temporary assignment. This is important because it gives us a concrete starting point and guarantees that only one friend can ever become problematic.

After counting frequencies, we locate the friend whose count exceeds the limit. If no such friend exists, the current assignment is already valid.

When a problematic friend exists, we only inspect days currently assigned to that friend. Days with a single available option cannot help because changing them is impossible. For a flexible day, assigning the second friend in the list is sufficient. We do not need to search for the best replacement because the proof shows that reducing the problematic friend's count is the only thing that matters.

The variable `need` tracks exactly how many more selections must be moved away from the overused friend. Once it reaches zero, the assignment satisfies the frequency constraint.

## Worked Examples

### Example 1

Input:

```
4 6
1 1
2 1 2
3 1 2 3
4 1 2 3 4
2 2 3
1 3
```

`limit = 3`.

Initial assignment:

| Day | Available | Chosen |
| --- | --- | --- |
| 1 | {1} | 1 |
| 2 | {1,2} | 1 |
| 3 | {1,2,3} | 1 |
| 4 | {1,2,3,4} | 1 |
| 5 | {2,3} | 2 |
| 6 | {3} | 3 |

Counts:

| Friend | Count |
| --- | --- |
| 1 | 4 |
| 2 | 1 |
| 3 | 1 |
| 4 | 0 |

Friend `1` exceeds the limit by `1`.

Reassign day 2 from `1` to `2`.

| Day | New Choice |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
| 4 | 1 |
| 5 | 2 |
| 6 | 3 |

Friend `1` now appears exactly `3` times, so the assignment is valid.

This example shows how only a single adjustment is needed even though many days involve friend `1`.

### Example 2

Input:

```
2 2
1 1
1 1
```

`limit = 1`.

Initial assignment:

| Day | Available | Chosen |
| --- | --- | --- |
| 1 | {1} | 1 |
| 2 | {1} | 1 |

Counts:

| Friend | Count |
| --- | --- |
| 1 | 2 |

Friend `1` exceeds the limit by `1`.

There are no days with more than one available friend, so no reassignment is possible.

The algorithm finishes with `need = 1` and prints `NO`.

This demonstrates the situation where all excessive selections are forced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Σkᵢ) | Each availability list is read once, and each day is scanned at most once more |
| Space | O(m + n) | Stores the assignment, counts, and availability lists |

The total number of availability entries across all test cases is at most `200000`, so linear processing easily fits within the two-second limit. The memory usage is also comfortably below the limit because we store only the input lists and a few auxiliary arrays.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def run(inp: str) -> str:
    from collections import defaultdict

    data = inp.strip().split()
    p = 0
    t = int(data[p])
    p += 1

    out = []

    for _ in range(t):
        n = int(data[p]); p += 1
        m = int(data[p]); p += 1

        days = []
        ans = []
        cnt = [0] * (n + 1)

        for _ in range(m):
            k = int(data[p]); p += 1
            cur = list(map(int, data[p:p+k]))
            p += k

            days.append(cur)
            ans.append(cur[0])
            cnt[cur[0]] += 1

        limit = (m + 1) // 2

        bad = -1
        for i in range(1, n + 1):
            if cnt[i] > limit:
                bad = i
                break

        if bad == -1:
            out.append("YES")
            out.append(" ".join(map(str, ans)))
            continue

        need = cnt[bad] - limit

        for i in range(m):
            if need == 0:
                break
            if ans[i] == bad and len(days[i]) > 1:
                ans[i] = days[i][1]
                need -= 1

        if need:
            out.append("NO")
        else:
            out.append("YES")
            out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# minimum size
assert run("""1
1 1
1 1
""").startswith("YES")

# impossible because all days force same friend
assert run("""1
2 2
1 1
1 1
""") == "NO"

# already valid
assert run("""1
3 3
1 1
1 2
1 3
""").startswith("YES")

# one reassignment fixes everything
assert run("""1
4 6
1 1
2 1 2
3 1 2 3
4 1 2 3 4
2 2 3
1 3
""").startswith("YES")

# boundary: exactly ceil(m/2) appearances
assert run("""1
2 3
1 1
1 1
1 2
""").startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single day, single friend | YES | Minimum input size |
| Two forced days for same friend | NO | Impossible because no flexible day exists |
| Different forced friends | YES | Already satisfies the limit |
| Overused friend with alternatives | YES | Reassignment logic |
| Friend used exactly ceil(m/2) times | YES | Correct boundary handling |

## Edge Cases

Consider the fully forced case:

```
1
1 3
1 1
1 1
1 1
```

The limit is `2`. Friend `1` is selected three times. Every day contains only one candidate, so the algorithm finds no day eligible for reassignment. The remaining excess is positive, and the answer is `NO`. Any valid solution would also need to reduce friend `1`'s count, which is impossible.

Consider a case where the overused friend can be repaired:

```
1
3 5
1 1
2 1 2
2 1 2
2 1 3
2 1 3
```

The limit is `3`. The initial assignment chooses friend `1` five times. The excess equals `2`. The algorithm reassigns two flexible days away from friend `1`, reducing its count to exactly `3`. The resulting assignment is valid.

Consider the boundary case:

```
1
2 5
1 1
1 1
1 1
1 2
1 2
```

The limit is `3`. Friend `1` already appears exactly three times. Since the count is not strictly greater than the limit, the algorithm performs no modifications and immediately outputs `YES`. This avoids the common mistake of treating equality as a violation.

Finally, consider:

```
1
4 6
1 1
1 1
1 1
2 1 2
2 1 3
2 1 4
```

The limit is `3`. Friend `1` initially appears six times, so the excess is `3`. Exactly three flexible days exist, and reassigning all three reduces friend `1` to the limit. The algorithm succeeds, showing that every flexible occurrence can be used independently to remove one unit of excess.
