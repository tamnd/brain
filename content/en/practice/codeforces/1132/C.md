---
title: "CF 1132C - Painting the Fence"
description: "We have a fence with n sections numbered from 1 to n. Each painter covers one continuous interval [li, ri]. Originally all q painters are available, but we are forced to dismiss exactly two of them and keep the remaining q - 2."
date: "2026-06-12T04:08:40+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1132
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 61 (Rated for Div. 2)"
rating: 1700
weight: 1132
solve_time_s: 122
verified: true
draft: false
---

[CF 1132C - Painting the Fence](https://codeforces.com/problemset/problem/1132/C)

**Rating:** 1700  
**Tags:** brute force  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fence with `n` sections numbered from `1` to `n`. Each painter covers one continuous interval `[l_i, r_i]`. Originally all `q` painters are available, but we are forced to dismiss exactly two of them and keep the remaining `q - 2`.

A fence section is painted if at least one retained painter covers it. The goal is to choose which two painters to remove so that the total number of painted sections is as large as possible.

The input gives the fence length and the intervals painted by every painter. The output is the maximum number of fence sections that remain painted after removing exactly two painters.

The constraints are the first thing that drives the solution design. Both `n` and `q` are at most `5000`. A brute-force approach that tries every pair of removed painters already requires about

$$\binom{5000}{2} \approx 12.5 \text{ million}$$

pairs.

That sounds large but manageable. The real problem appears if we recompute the painted fence for every pair. Doing even `O(n)` work per pair would require roughly

$$12.5 \cdot 10^6 \cdot 5000$$

operations, which is completely infeasible.

The structure of the problem suggests that we should precompute information about coverage and then evaluate each removed pair in constant or logarithmic time.

Several edge cases are easy to mishandle.

Consider:

```
5 3
1 5
1 5
1 5
```

Removing any two painters still leaves one painter covering the whole fence, so the answer is `5`. A solution that only counts unique coverage incorrectly would underestimate the remaining painted sections.

Another important case is:

```
5 3
1 2
2 3
3 4
```

Section `2` is covered by two painters and section `3` is also covered by two painters. Removing different pairs affects different overlaps. We must carefully distinguish sections covered exactly once and exactly twice.

A third subtle case is:

```
5 3
1 1
3 3
5 5
```

Removing any two painters leaves only one painted section. Coverage is very sparse, so interval logic must handle gaps correctly.

## Approaches

The most direct idea is to try every pair of painters that could be removed.

For a fixed pair `(i, j)`, we can mark all sections painted by the remaining painters and count how many fence sections are still covered. This is correct because it literally simulates the definition of the problem.

The difficulty is the cost. There are about `12.5 million` painter pairs in the worst case. Recomputing coverage of up to `5000` fence sections for each pair would require tens of billions of operations.

The key observation is that we do not need to rebuild the entire painting configuration for every pair. What matters is how many sections become unpainted after removing two painters.

First, compute for every fence section how many painters cover it.

Let `cover[x]` be that count.

Suppose we remove painters `i` and `j`.

A section disappears from the final painting only in two situations.

If `cover[x] = 1`, then exactly one painter covers that section. Removing that painter makes the section disappear.

If `cover[x] = 2`, then exactly two painters cover that section. The section disappears only when both of those painters are removed.

Sections with coverage at least three remain painted regardless of which two painters are removed.

This transforms the problem into counting losses instead of recomputing the final painting.

Let:

`total` = number of sections initially painted by at least one painter.

For each painter `i`, define:

`one[i]` = number of sections covered exactly once and covered by painter `i`.

These sections disappear whenever painter `i` is removed.

For every pair `(i, j)`, define:

`two[i][j]` = number of sections covered exactly twice, specifically by painters `i` and `j`.

These sections disappear only when both painters are removed.

Then after removing painters `i` and `j`, the remaining painted sections equal:

$$total - one[i] - one[j] - two[i][j]$$

Now the task becomes computing `one` and `two` efficiently.

Because intervals are continuous and `n ≤ 5000`, we can process every fence position. For positions with coverage exactly one, we identify the responsible painter. For positions with coverage exactly two, we identify the responsible painter pair.

To query interval counts efficiently, we build prefix sums over positions whose coverage equals one and positions whose coverage equals two.

Then every painter pair can be evaluated in constant time after a few prefix-sum queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q²·n) or worse | O(n) | Too slow |
| Optimal | O(nq + q²) | O(q²) | Accepted |

## Algorithm Walkthrough

1. Read all painter intervals.
2. Build a difference array over the fence and compute `cover[x]`, the number of painters covering each section.
3. Count `total`, the number of fence sections with `cover[x] > 0`.
4. Create an array `cnt1[x]` where `cnt1[x] = 1` if `cover[x] = 1`, otherwise `0`.
5. Create an array `cnt2[x]` where `cnt2[x] = 1` if `cover[x] = 2`, otherwise `0`.
6. Build prefix sums for `cnt1` and `cnt2`.

These allow us to count how many positions with coverage exactly one or exactly two lie inside any interval.
7. For every painter `i`, compute `one[i]`.

This equals the number of positions inside painter `i`'s interval whose total coverage is exactly one.
8. For every pair of painters `(i, j)`, compute how many positions are covered exactly twice by both painters.

Since a position covered exactly twice and belonging to both painters must lie inside the intersection of their intervals, we count positions with `cover[x] = 2` inside that intersection.
9. For every pair `(i, j)`, compute

$$total - one[i] - one[j] - two[i][j]$$

and keep the maximum value.
10. Output the maximum.

### Why it works

A fence section can disappear only if all painters covering it are removed.

When a section has coverage exactly one, removing its unique painter is sufficient to remove the section. Such sections contribute to `one[i]`.

When a section has coverage exactly two, both responsible painters must be removed simultaneously. Such sections contribute to `two[i][j]`.

When a section has coverage at least three, removing only two painters can never eliminate all coverage.

Every section that disappears belongs to exactly one of these categories, and no section is counted twice. Consequently,

$$one[i] + one[j] + two[i][j]$$

is exactly the number of sections lost after removing painters `i` and `j`. Subtracting this loss from the initially painted count gives the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, q = map(int, input().split())

    segs = []
    diff = [0] * (n + 3)

    for _ in range(q):
        l, r = map(int, input().split())
        segs.append((l, r))
        diff[l] += 1
        diff[r + 1] -= 1

    cover = [0] * (n + 1)
    cur = 0
    total = 0

    for x in range(1, n + 1):
        cur += diff[x]
        cover[x] = cur
        if cur > 0:
            total += 1

    one_pos = [0] * (n + 1)
    two_pos = [0] * (n + 1)

    for x in range(1, n + 1):
        if cover[x] == 1:
            one_pos[x] = 1
        elif cover[x] == 2:
            two_pos[x] = 1

    pref1 = [0] * (n + 1)
    pref2 = [0] * (n + 1)

    for x in range(1, n + 1):
        pref1[x] = pref1[x - 1] + one_pos[x]
        pref2[x] = pref2[x - 1] + two_pos[x]

    one = [0] * q

    for i, (l, r) in enumerate(segs):
        one[i] = pref1[r] - pref1[l - 1]

    ans = 0

    for i in range(q):
        l1, r1 = segs[i]

        for j in range(i + 1, q):
            l2, r2 = segs[j]

            left = max(l1, l2)
            right = min(r1, r2)

            both = 0
            if left <= right:
                both = pref2[right] - pref2[left - 1]

            remaining = total - one[i] - one[j] - both
            if remaining > ans:
                ans = remaining

    print(ans)

if __name__ == "__main__":
    main()
```

The first phase computes the coverage count for every fence section using a difference array. This avoids marking every interval individually and gives all coverage counts in `O(n + q)` time.

The arrays `one_pos` and `two_pos` identify positions whose coverage is exactly one or exactly two. Prefix sums then allow interval queries in constant time.

The value `one[i]` is obtained by querying the number of coverage-one positions inside painter `i`'s interval. Every such position disappears whenever painter `i` is removed.

For a painter pair, only the intersection of their intervals matters. A section with coverage exactly two disappears only if it belongs to both painters, which means it lies in that intersection. Querying the number of coverage-two positions in the intersection gives `two[i][j]`.

The most common implementation mistake is forgetting that the intersection may be empty. In that case `both` must remain zero.

Another easy off-by-one error comes from prefix-sum queries. Using

```
pref[r] - pref[l - 1]
```

requires arrays indexed from `1` and a valid zero-th prefix entry.

## Worked Examples

### Example 1

Input:

```
7 5
1 4
4 5
5 6
6 7
3 5
```

Coverage counts:

| Position | Coverage |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 3 |
| 6 | 2 |
| 7 | 1 |

Thus `total = 7`.

Unique-cover counts:

| Painter | Interval | one[i] |
| --- | --- | --- |
| 1 | [1,4] | 2 |
| 2 | [4,5] | 0 |
| 3 | [5,6] | 0 |
| 4 | [6,7] | 1 |
| 5 | [3,5] | 0 |

If painters 2 and 3 are removed, their intersection contains position 5 only, but coverage there is 3, so `both = 0`.

Remaining:

| Removed Pair | Loss | Remaining |
| --- | --- | --- |
| (2,3) | 0 | 7 |
| (1,4) | 3 | 4 |
| (1,5) | 3 | 4 |

The maximum is `7`.

This example shows that removing painters with no uniquely critical sections can leave the entire fence painted.

### Example 2

Input:

```
5 3
1 3
2 4
3 5
```

Coverage counts:

| Position | Coverage |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 2 |
| 5 | 1 |

`total = 5`.

| Painter | one[i] |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 1 |

For pair `(1,2)`, intersection is `[2,3]`.

Only position `2` has coverage exactly two.

| Pair | one[i] | one[j] | both | Remaining |
| --- | --- | --- | --- | --- |
| (1,2) | 1 | 0 | 1 | 3 |
| (1,3) | 1 | 1 | 0 | 3 |
| (2,3) | 0 | 1 | 1 | 3 |

Answer = `3`.

This trace demonstrates how coverage-two positions are charged only to the specific painter pair responsible for them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q²) | Coverage computation is linear, pair evaluation examines all painter pairs |
| Space | O(n + q) | Coverage arrays, prefix sums, and interval storage |

With `q ≤ 5000`, the dominant term is roughly

$$\binom{5000}{2} \approx 12.5 \text{ million}$$

pair evaluations. Each evaluation performs only a few arithmetic operations and constant-time prefix-sum queries, which comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, q = map(int, input().split())

    segs = []
    diff = [0] * (n + 3)

    for _ in range(q):
        l, r = map(int, input().split())
        segs.append((l, r))
        diff[l] += 1
        diff[r + 1] -= 1

    cover = [0] * (n + 1)
    cur = 0
    total = 0

    for i in range(1, n + 1):
        cur += diff[i]
        cover[i] = cur
        if cur:
            total += 1

    one_pos = [0] * (n + 1)
    two_pos = [0] * (n + 1)

    for i in range(1, n + 1):
        if cover[i] == 1:
            one_pos[i] = 1
        elif cover[i] == 2:
            two_pos[i] = 1

    pref1 = [0] * (n + 1)
    pref2 = [0] * (n + 1)

    for i in range(1, n + 1):
        pref1[i] = pref1[i - 1] + one_pos[i]
        pref2[i] = pref2[i - 1] + two_pos[i]

    one = [0] * q
    for i, (l, r) in enumerate(segs):
        one[i] = pref1[r] - pref1[l - 1]

    ans = 0

    for i in range(q):
        l1, r1 = segs[i]
        for j in range(i + 1, q):
            l2, r2 = segs[j]

            L = max(l1, l2)
            R = min(r1, r2)

            both = 0
            if L <= R:
                both = pref2[R] - pref2[L - 1]

            ans = max(ans, total - one[i] - one[j] - both)

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run(
"""7 5
1 4
4 5
5 6
6 7
3 5
"""
) == "7", "sample 1"

# minimum sizes
assert run(
"""3 3
1 1
2 2
3 3
"""
) == "1", "minimum q"

# all intervals equal
assert run(
"""5 3
1 5
1 5
1 5
"""
) == "5", "all equal intervals"

# sparse intervals
assert run(
"""5 3
1 1
3 3
5 5
"""
) == "1", "disjoint painters"

# off-by-one boundary coverage
assert run(
"""5 3
1 2
2 3
3 5
"""
) == "3", "endpoint intersections"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three single-cell painters | 1 | Minimum valid size |
| All intervals `[1,5]` | 5 | Heavy overlap everywhere |
| Three disjoint intervals | 1 | Sparse coverage |
| Endpoint-touching intervals | 3 | Correct intersection boundaries |

## Edge Cases

Consider:

```
5 3
1 5
1 5
1 5
```

Coverage is `3` at every position. There are no coverage-one or coverage-two positions. Every `one[i]` equals `0`, every `two[i][j]` equals `0`, and

$$5 - 0 - 0 - 0 = 5$$

for every pair. The algorithm correctly returns `5`.

Now consider:

```
5 3
1 1
3 3
5 5
```

Coverage-one positions are exactly `{1,3,5}`. Each painter owns one such position. Removing any two painters loses two painted sections, leaving exactly one. The algorithm computes:

$$3 - 1 - 1 = 1$$

and returns `1`.

Finally consider:

```
5 3
1 2
2 3
3 4
```

Coverage counts are `[1,2,2,1,0]`. Positions `2` and `3` have coverage exactly two. Removing painters `1` and `2` loses position `1` from unique coverage and position `2` from double coverage. The algorithm counts these losses separately through `one` and `both`, avoiding double counting and producing the correct result.
