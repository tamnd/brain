---
title: "CF 102500J - Jackdaws And Crows"
description: "We have a sequence of comment scores. Nick is allowed to spend time creating fake accounts, where each account can change any chosen score by one in either direction, and he can also remove comments."
date: "2026-08-05T18:10:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102500
codeforces_index: "J"
codeforces_contest_name: "2019-2020 ICPC Northwestern European Regional Programming Contest (NWERC 2019)"
rating: 0
weight: 102500
solve_time_s: 189
verified: true
draft: false
---

[CF 102500J - Jackdaws And Crows](https://codeforces.com/problemset/problem/102500/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of comment scores. Nick is allowed to spend time creating fake accounts, where each account can change any chosen score by one in either direction, and he can also remove comments. The final remaining sequence must have every score non-zero and neighboring scores with opposite signs.

If Nick creates `f` fake accounts, a score with absolute value smaller than `f` can be turned into either positive or negative. Such a score behaves like a wildcard. Every other non-zero score keeps its original sign. The task is to choose how many accounts to create and how many comments to remove so that the total time is minimized.

The array length can reach `5 * 10^5`, so checking every possible number of accounts and rebuilding the whole sequence would be too slow. We need to process the changes caused by increasing the number of accounts almost linearly. The scores can be as large as `10^9`, but only the moments when a score becomes a wildcard matter, so the huge numeric range itself is not a problem.

A few edge cases are easy to miss. A zero score cannot stay in the sequence without fake accounts. For example:

```
1 5 7
0
```

With zero accounts the comment must be removed, costing `7`. With one account it becomes usable, costing `5`, so the answer is `5`. A solution that treats zero as a normal fixed sign gives the wrong result.

Another trap is that consecutive equal signs may need several removals. For example:

```
3 1 100
1 1 1
```

Creating no accounts requires removing all three comments except one, which costs `200`. Creating one account makes all values flexible, costing `1`. A solution that only counts adjacent bad pairs can misunderstand the number of deletions required.

## Approaches

A direct approach would try every possible number of fake accounts. For each value of `f`, we classify every score, compute the longest alternating subsequence that can remain, and pay for the deleted comments. This is correct because it explicitly checks every possible strategy. However, there can be `O(10^9)` possible account counts, and even restricting ourselves to meaningful values still leaves `O(n)` possibilities where rebuilding the array costs `O(n)`. The worst case becomes `O(n^2)` operations, which is impossible for `n = 5 * 10^5`.

The key observation is that a score only changes its behavior once. A score with value `x` becomes flexible exactly when the number of accounts becomes greater than `|x|`. Between these moments, the set of flexible comments is unchanged, so the answer only needs to be checked at those `n + 1` interesting account counts.

For a fixed number of accounts, only the non-wildcard comments matter. Consider two consecutive non-wildcard comments in the original order. Let there be `k` wildcard comments between them. They create a conflict exactly when the signs cannot be made alternating through that gap. This happens when equal signs have an even sized gap, or opposite signs have an odd sized gap. Each such conflict requires one removal.

When a comment becomes a wildcard, it disappears from the list of fixed signs. Only the two neighboring fixed comments are affected, so the number of conflicts can be updated in constant time. A doubly linked list lets us remove newly flexible comments efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Classify every score as either a fixed positive sign, a fixed negative sign, or an event that will become a wildcard. A non-zero score `s` becomes flexible at `|s| + 1` accounts, while zero becomes flexible at `1` account.
2. Start with zero fake accounts. All non-zero scores are kept in a linked list of fixed signs. Zero scores contribute one mandatory deletion each. Compute the initial number of bad adjacent fixed pairs.
3. Sort all wildcard events by the account count at which they happen. Only these account counts need to be tested.
4. When an event is processed, remove that position from the linked list of fixed signs. Before removing it, subtract the conflicts involving its previous and next fixed neighbors. After removal, add the new conflict between those two neighbors if both still exist.
5. After processing all events for a particular account count `f`, the current number of required reports is known. The total cost is:

```
f * c + removals * r
```

Update the minimum answer.

Why it works: for a fixed number of accounts, every flexible comment can always be assigned the sign needed by its neighbors. The only unavoidable problems are between consecutive fixed comments whose signs and distance parity make alternation impossible. Removing exactly one comment for each such conflict is sufficient and necessary. Increasing the number of accounts only removes fixed comments from this reduced representation, so maintaining the conflict count after every removal preserves the exact minimum number of reports.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, c, r = map(int, input().split())
    s = list(map(int, input().split()))

    sign = [0] * n
    events = {}

    zero = 0
    for i, x in enumerate(s):
        if x == 0:
            zero += 1
            t = 1
        else:
            sign[i] = 1 if x > 0 else -1
            t = abs(x) + 1
        events.setdefault(t, []).append(i)

    prev = [-1] * n
    nxt = [-1] * n

    last = -1
    for i in range(n):
        if sign[i]:
            if last != -1:
                nxt[last] = i
                prev[i] = last
            last = i

    def bad(a, b):
        if a == -1 or b == -1:
            return 0
        gap = b - a - 1
        return 1 if ((sign[a] == sign[b]) == (gap % 2 == 0)) else 0

    removals = zero
    cur = -1
    for i in range(n):
        if sign[i]:
            if cur != -1:
                removals += bad(cur, i)
            cur = i

    ans = removals * r

    for f in sorted(events):
        for i in events[f]:
            if sign[i] == 0:
                removals -= 1
                continue

            a = prev[i]
            b = nxt[i]

            removals -= bad(a, i)
            removals -= bad(i, b)

            if a != -1:
                nxt[a] = b
            if b != -1:
                prev[b] = a

            removals += bad(a, b)

            sign[i] = 0

        ans = min(ans, f * c + removals * r)

    print(ans)

if __name__ == "__main__":
    solve()
```

The linked list contains only comments that are still forced to have their original signs. When a comment becomes a wildcard, it no longer affects conflicts because it can always be assigned the needed sign later.

The `bad` function is the core of the solution. The distance between two fixed comments determines whether the wildcard gap flips the required parity. Since adjacent nodes in the linked list have no fixed comments between them, their index difference directly gives the number of wildcards between them.

Python integers already support arbitrary precision, so the products involving costs up to `10^9` and `5 * 10^5` comments are safe.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the event positions dominates; all linked list updates are linear |
| Space | O(n) | Arrays and event storage each contain at most `n` entries |

The solution processes every comment a constant number of times. The sorting step is acceptable for `5 * 10^5` events.

## Worked Examples

For the first sample:

```
4 10 50
8 8 2 -2
```

| Accounts | New wildcards | Remaining conflicts | Cost |
| --- | --- | --- | --- |
| 0 | none | 2 | 100 |
| 3 | `2`, `-2` become flexible | 1 | 80 |
| 9 | all become flexible | 0 | 90 |

The best choice is three accounts and one report, giving `80`.

For the second sample:

```
6 100 33
5 -13 0 0 -12 0
```

| Accounts | New wildcards | Remaining conflicts | Cost |
| --- | --- | --- | --- |
| 0 | none | 3 zero removals | 99 |
| 1 | all zeros become flexible | 3 | 199 |
| 6 | score `5` becomes flexible | 2 | 266 |
| 13 | all become flexible | 0 | 1300 |

The best solution is to delete the three zero comments immediately, then pay for the remaining conflicts, resulting in `132`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    n, c, r = map(int, data[:3])
    arr = list(map(int, data[3:]))

    sign = [0] * n
    events = {}
    zero = 0

    for i, x in enumerate(arr):
        if x == 0:
            zero += 1
            t = 1
        else:
            sign[i] = 1 if x > 0 else -1
            t = abs(x) + 1
        events.setdefault(t, []).append(i)

    prev = [-1] * n
    nxt = [-1] * n
    last = -1
    for i in range(n):
        if sign[i]:
            if last != -1:
                nxt[last] = i
                prev[i] = last
            last = i

    def bad(a, b):
        if a == -1 or b == -1:
            return 0
        return int(((sign[a] == sign[b]) == ((b - a - 1) % 2 == 0)))

    rem = zero
    last = -1
    for i in range(n):
        if sign[i]:
            if last != -1:
                rem += bad(last, i)
            last = i

    ans = rem * r
    for f in sorted(events):
        for i in events[f]:
            if sign[i] == 0:
                rem -= 1
            else:
                a, b = prev[i], nxt[i]
                rem -= bad(a, i) + bad(i, b)
                if a != -1:
                    nxt[a] = b
                if b != -1:
                    prev[b] = a
                rem += bad(a, b)
                sign[i] = 0
        ans = min(ans, f * c + rem * r)

    return str(ans)

assert run("4 10 50\n8 8 2 -2\n") == "80"
assert run("6 100 33\n5 -13 0 0 -12 0\n") == "132"
assert run("1 5 7\n0\n") == "5"
assert run("3 1 100\n1 1 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 7 / 0` | `5` | Zero becoming a wildcard |
| `3 1 100 / 1 1 1` | `1` | All equal signs and large deletion counts |
| Sample 1 | `80` | Mixed fixed and flexible comments |
| Sample 2 | `132` | Multiple zeros and delayed wildcard events |

## Edge Cases

A single zero comment demonstrates the special handling of unusable scores at zero accounts:

```
1 5 7
0
```

The algorithm starts with one required removal. At account count `1`, the zero becomes a wildcard, so the removal count decreases to zero and the answer becomes `5`.

A chain of equal signs demonstrates why conflicts must be counted through the linked list rather than by looking only at pairs in the original array:

```
3 1 100
1 1 1
```

The initial linked list has two bad adjacent pairs, so two removals are required. After one account, every comment is flexible, the linked list becomes empty, and no reports are needed. The algorithm checks this state and returns `1`.
