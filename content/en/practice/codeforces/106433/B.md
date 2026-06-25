---
title: "CF 106433B - Twin Works"
description: "The problem describes a hallway containing works of art. Each work has an old identifier, and some works are twins because they share the same identifier."
date: "2026-06-25T09:37:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106433
codeforces_index: "B"
codeforces_contest_name: "XXX Spain Olympiad in Informatics, online qualifier"
rating: 0
weight: 106433
solve_time_s: 39
verified: true
draft: false
---

[CF 106433B - Twin Works](https://codeforces.com/problemset/problem/106433/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a hallway containing works of art. Each work has an old identifier, and some works are twins because they share the same identifier. The new identifiers must preserve exactly these groups: two works that had the same old identifier must still have the same new identifier, while two different old identifiers must receive different new identifiers.

The order of works in the hallway cannot change. The inspector reads the new identifiers from left to right, and a pair of positions is considered bad when an earlier work has a larger identifier than a later work. The task is to assign new identifiers so that this number of inversions is as small as possible. Any assignment with the minimum number of inversions is accepted.

The key restriction is that every old identifier appears at most twice. The total number of works across all test cases is at most $10^5$, so a solution must be close to linear. Sorting the whole array is acceptable, but comparing every pair of works is not. A quadratic method would reach around $10^{10}$ operations for the largest input, which is far beyond a typical one second limit.

The tricky cases come from duplicated identifiers appearing in different positions. A careless solution may assign identifiers according only to the first occurrence or according to the numeric value of the old code, but the original values have no meaning after the grouping is fixed.

For example:

```
1
3
3 2 1
```

The correct output can be:

```
1 2 3
```

A solution that keeps the original values would output `3 2 1`, creating unnecessary inversions. The old labels only describe which works are twins.

Another case is:

```
1
4
2 1 1 2
```

The correct output can be:

```
1 2 2 1
```

The two pairs must remain together. Giving the first `2` a different value from the second `2` would violate the twin requirement.

## Approaches

A direct approach would try every possible ordering of the groups and assign new numbers according to that ordering. The idea is correct because once the groups are placed in an increasing order, the inversions are minimized. However, with many distinct groups, trying all orders is factorial and becomes impossible immediately.

A more practical brute force would repeatedly count inversions while trying different assignments. Even if we only considered a small set of possible assignments, counting all pairs would require $O(n^2)$ work. With $n = 10^5$, that is about $10^{10}$ comparisons.

The important observation is that we do not need to search over assignments. Each old identifier represents one indivisible group. If we choose an ordering of these groups, assigning consecutive new numbers in that order, the inversion count between groups depends only on the relative order of those groups in the hallway. To minimize inversions, groups should appear in the new numbering order according to their first appearance from left to right.

Imagine scanning the hallway. The first new group encountered should receive code `1`, because putting any other group before it would create inversions with this first occurrence. The next unseen group should receive the next code, and so on. Repeated appearances reuse the code already assigned to that group.

This works because every group can be treated as a single object. Assigning a smaller code to a group that first appears earlier never creates more inversions than swapping it with a group whose first appearance is later. Repeating this exchange argument leads to the order of first appearances.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an empty mapping from old codes to new codes. The mapping represents the preserved twin groups. Every occurrence of the same old code must receive the same value.
2. Scan the works from left to right. When an old code appears for the first time, assign it the next available new code. This follows the order in which groups naturally appear in the hallway.
3. When an old code appears again, reuse the previously assigned new code. The second occurrence cannot influence the ordering because its group has already been placed.
4. Output the assigned codes in the original hallway order.

Why it works:

The first occurrence of every group determines the earliest position where that group can affect inversions. Suppose two groups A and B have first occurrences where A appears before B. Assigning B a smaller new code than A would create an inversion between those first occurrences. Swapping their new codes removes that inversion and does not harm any pair involving later occurrences because all members of a group move together. Applying this argument repeatedly means the optimal ordering is exactly the first appearance order of groups. The algorithm assigns precisely that ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        mapping = {}
        nxt = 1
        res = []

        for x in a:
            if x not in mapping:
                mapping[x] = nxt
                nxt += 1
            res.append(mapping[x])

        ans.append(" ".join(map(str, res)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The dictionary stores the relationship between old identifiers and new identifiers. The first time a value appears, the code assigns the next number. This is the only moment where a decision is needed.

The scan order is the main implementation detail. If the array were sorted first, the original hallway order would be lost and the produced assignment could increase inversions. The algorithm only relabels, it never rearranges the works.

The variable `nxt` starts at one because all new identifiers must be positive. Python integers are used naturally here, so there is no overflow concern.

## Worked Examples

For the input:

```
1
4
2 1 1 2
```

the trace is:

| Position | Old code | Mapping | Next code | Assigned |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 → 1 | 2 | 1 |
| 2 | 1 | 1 → 2 | 3 | 2 |
| 3 | 1 | 1 → 2 | 3 | 2 |
| 4 | 2 | 2 → 1 | 3 | 1 |

The output is:

```
1 2 2 1
```

The trace shows that the second appearance of each twin group does not create a new identifier.

For the input:

```
1
6
5 5 3 7 3 7
```

the trace is:

| Position | Old code | Mapping | Next code | Assigned |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 → 1 | 2 | 1 |
| 2 | 5 | 5 → 1 | 2 | 1 |
| 3 | 3 | 3 → 2 | 3 | 2 |
| 4 | 7 | 7 → 3 | 4 | 3 |
| 5 | 3 | 3 → 2 | 4 | 2 |
| 6 | 7 | 7 → 3 | 4 | 3 |

The output is:

```
1 1 2 3 2 3
```

This demonstrates that the numeric values of the old identifiers are irrelevant. Only the order of first appearances matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every work is processed once, and dictionary operations are expected O(1). |
| Space | O(n) | The mapping stores one entry for every distinct old identifier. |

The total number of works over all test cases is $10^5$, so a linear solution easily fits the limits. The memory usage is also linear because the dictionary contains at most one entry per work.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("""2
3
3 2 1
4
2 1 1 2
""") == """1 2 3
1 2 2 1
""", "samples"

assert run("""1
1
10
""") == """1
""", "single element"

assert run("""1
5
4 4 4 4 4
""") == """1 1 1 1 1
""", "all equal"

assert run("""1
6
6 5 6 4 5 4
""") == """1 2 1 3 2 3
""", "interleaved twins"

assert run("""1
5
1 2 3 4 5
""") == """1 2 3 4 5
""", "all different"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 1` | `1 2 3` | Groups must follow first appearance, not old values. |
| `2 1 1 2` | `1 2 2 1` | Twin occurrences must receive identical codes. |
| `10` | `1` | Minimum size case. |
| `4 4 4 4 4` | `1 1 1 1 1` | All elements belong to one group. |
| `6 5 6 4 5 4` | `1 2 1 3 2 3` | Handles alternating duplicate groups. |

## Edge Cases

For:

```
1
3
3 2 1
```

the algorithm starts with an empty map. It sees `3` first and assigns code `1`, then `2` receives code `2`, and `1` receives code `3`. The result is `1 2 3`, which removes the inversions created by the original labels.

For:

```
1
4
2 1 1 2
```

the first `2` receives code `1`, and the first `1` receives code `2`. When the algorithm reaches the third position, it finds that `1` already exists in the map, so it reuses code `2`. The final `2` also reuses code `1`. The result keeps both twin pairs intact.

For:

```
1
5
7 7 7 7 7
```

there is only one group. The first position creates the only mapping entry, and every later position reuses it. The output is:

```
1 1 1 1 1
```

No other assignment could improve this because there are no separate groups to reorder.
