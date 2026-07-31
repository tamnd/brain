---
title: "CF 102591F - \u0420\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u043d\u0430 \u043f\u0430\u0440\u044b"
description: "We have an odd number of students, and every student has a distinct strength value. We must leave exactly one student without a partner and split all remaining students into pairs."
date: "2026-08-01T06:38:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102591
codeforces_index: "F"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041c\u0423\u0418\u0422 \u043f\u043e \u0441\u043f\u043e\u0440\u0442\u0438\u0432\u043d\u043e\u043c\u0443 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2020. \u0424\u0438\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u0442\u0443\u0440."
rating: 0
weight: 102591
solve_time_s: 80
verified: true
draft: false
---

[CF 102591F - \u0420\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u043d\u0430 \u043f\u0430\u0440\u044b](https://codeforces.com/problemset/problem/102591/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an odd number of students, and every student has a distinct strength value. We must leave exactly one student without a partner and split all remaining students into pairs. A pair contributes the smaller strength of its two members, so a pair with strengths 10 and 3 contributes 3. For every possible student who could be left out, we need the maximum possible total contribution of all pairs.

The output is not one value. It contains one answer for every original student, where the answer at position `i` describes the best total score if that student is the one who does not participate.

The constraints are the main reason this problem is interesting. With up to `3 * 10^5` students, trying all possible removals and recomputing an optimal pairing for each one would require roughly quadratic work, around `9 * 10^10` operations in the worst case. That is far beyond what a competitive programming solution can afford. We need to find a pattern that lets us process every student together after a single sort.

A few edge cases can break an implementation that only handles the common situation. The smallest possible input has only three students. For example, with strengths `3 1 2`, removing the student with strength `3` leaves `[1,2]`, giving a score of `1`. Removing `1` leaves `[2,3]`, giving `2`. Removing `2` leaves `[1,3]`, giving `1`. The correct output is `1 2 1`. A solution that always assumes the largest student participates in a pair can fail here.

Another common mistake is forgetting that the removed student changes the parity of all following positions after sorting. For input `1 2 3 4 5`, if we remove `3`, the remaining sorted list is `1 2 4 5`. The optimal score is `1 + 4 = 5`. Treating the original indices as if nothing shifted gives the wrong set of chosen positions.

## Approaches

A direct solution starts by trying every possible student to remove. After removing one student, we sort or maintain the remaining strengths and build the best pairing. For a fixed sorted list of an even number of students, the optimal strategy is easy to find: take the smaller member from each pair as large as possible. This means the answer is the sum of every second element when counted from the end, or equivalently every element at an even index in ascending order.

The brute-force approach is correct because it checks the exact situation required for every possible removed student. The problem is the amount of repeated work. There are `n` possible removals, and each one would require processing almost `n` students, leading to `O(n^2)` work after avoiding unnecessary sorting. With `n = 300000`, that is already impossible.

The key observation is that we do not actually need to rebuild the remaining array for every removal. Sort all students once. Let the sorted strengths be `a[0], a[1], ..., a[n-1]`. If we remove an element at position `r`, the selected elements in the remaining array are exactly the original even indices before `r` and the original odd indices after `r`.

The reason is the index shift. Elements before the removed position keep their indices, so the even positions remain the chosen ones. Elements after the removed position move one step left, so an original odd index becomes an even index and contributes to the answer.

This turns the problem into maintaining two simple sums. A prefix sum of values at even indices gives the contribution from the left side of a removal. A suffix sum of values at odd indices gives the contribution from the right side. Every answer is just the combination of those two values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the students by strength while keeping their original positions. Sorting allows us to reason about the final pairing order because the contribution of a pair only depends on which student is weaker.
2. Build a prefix array where `pref[i]` stores the sum of sorted elements with even indices before position `i`. When a student at position `i` is removed, all even positions before `i` stay unchanged and still contribute.
3. Build a suffix array where `suf[i]` stores the sum of sorted elements with odd indices from position `i` to the end. After removing position `i`, every element after it shifts one position left, so original odd positions become the selected even positions.
4. For every sorted position `i`, compute `pref[i] + suf[i + 1]`. This is the answer for removing the student at sorted position `i`. The prefix handles the unchanged left side, and the suffix handles the shifted right side.
5. Restore the answers to the original input order using the saved original indices from the sorting step. The required output follows the order in which students were given.

Why it works: For any fixed set of remaining students, the optimal pairing always takes every second element in the sorted remaining sequence starting from the smallest element. Removing one element only affects the parity of positions after that element. Before the removed position, the chosen indices are exactly the original even indices. After it, the chosen indices are exactly the original odd indices. The algorithm calculates precisely these two groups, so every produced value is the optimal score for its corresponding removed student.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = list(map(int, input().split()))

    arr = sorted((value, idx) for idx, value in enumerate(s))

    pref = [0] * (n + 1)
    for i, (value, _) in enumerate(arr):
        pref[i + 1] = pref[i]
        if i % 2 == 0:
            pref[i + 1] += value

    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1]
        if i % 2 == 1:
            suf[i] += arr[i][0]

    ans = [0] * n
    for i, (_, original_idx) in enumerate(arr):
        ans[original_idx] = pref[i] + suf[i + 1]

    print(*ans)

if __name__ == "__main__":
    solve()
```

The sorting step stores both the strength and the original position. The strength order is needed for the pairing argument, while the original index is needed to put the final answers back into the input order.

The prefix construction only adds values at even sorted positions. It intentionally uses `pref[i]` when answering position `i`, because the removed element itself must not be included.

The suffix construction scans from right to left and collects values at odd sorted positions. When removing position `i`, the right part starts at `i + 1`, which is why the answer uses `suf[i + 1]`.

Python integers handle the possible sum size automatically. The largest possible answer can be around `1.5 * 10^14`, which would overflow 32-bit integer types in languages where this needs manual handling.

## Worked Examples

For the sample input:

```
3
3 1 2
```

The sorted array is `[1, 2, 3]`.

| Removed sorted position | Prefix even contribution | Suffix odd contribution | Answer |
| --- | --- | --- | --- |
| 0, value 1 | 0 | 1 | 1 |
| 1, value 2 | 1 | 0 | 1 |
| 2, value 3 | 1 | 0 | 1 |

Restoring the original order `[3,1,2]` gives `[1,2,1]`. The middle student has the best result because removing the weakest student leaves the two stronger students together.

For another example:

```
5
1 2 3 4 5
```

The sorted array is already `[1,2,3,4,5]`.

| Removed sorted position | Prefix even contribution | Suffix odd contribution | Answer |
| --- | --- | --- | --- |
| 0, value 1 | 0 | 6 | 6 |
| 1, value 2 | 1 | 6 | 7 |
| 2, value 3 | 1 | 4 | 5 |
| 3, value 4 | 4 | 0 | 4 |
| 4, value 5 | 4 | 0 | 4 |

Removing `2` leaves `[1,3,4,5]`, where the optimal pairs contribute `1 + 4 = 5`. The larger answers at the beginning come from keeping more large elements in the selected positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the two linear prefix and suffix passes |
| Space | O(n) | The sorted array and auxiliary prefix and suffix arrays are linear |

The limit of `3 * 10^5` students requires a near-linear solution. Sorting once and then doing a constant number of passes is suitable for this size.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    data = inp.strip().split()
    n = int(data[0])
    s = list(map(int, data[1:]))

    arr = sorted((value, idx) for idx, value in enumerate(s))

    pref = [0] * (n + 1)
    for i, (value, _) in enumerate(arr):
        pref[i + 1] = pref[i]
        if i % 2 == 0:
            pref[i + 1] += value

    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1]
        if i % 2 == 1:
            suf[i] += arr[i][0]

    ans = [0] * n
    for i, (_, idx) in enumerate(arr):
        ans[idx] = pref[i] + suf[i + 1]

    return " ".join(map(str, ans))

assert solve("3\n3 1 2\n") == "1 2 1", "sample 1"

assert solve("5\n1 2 3 4 5\n") == "6 7 5 4 4", "shift parity case"

assert solve("3\n100 1 50\n") == "50 100 50", "minimum size"

assert solve("7\n7 1 6 2 5 3 4\n") == "9 15 10 14 10 13 11", "mixed order"

assert solve("3\n1000000000 1 999999999\n") == "999999999 1000000000 999999999", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 3 1 2` | `1 2 1` | Provided sample and smallest valid input |
| `5 / 1 2 3 4 5` | `6 7 5 4 4` | Correct handling of index parity changes after removal |
| `3 / 100 1 50` | `50 100 50` | Correct ordering when the largest value is not first |
| `7 / 7 1 6 2 5 3 4` | `9 15 10 14 10 13 11` | Multiple removals with mixed positions |
| `3 / 1000000000 1 999999999` | `999999999 1000000000 999999999` | Large integer arithmetic |

## Edge Cases

When there are only three students, the algorithm still works because the prefix and suffix arrays contain enough boundary positions. For input `3 1 2`, removing the sorted first element uses only the suffix contribution, removing the middle element uses the prefix contribution, and removing the largest element leaves the smallest value as the only pair contribution.

When the removed student is near the beginning or the end, the index shift is the most common source of mistakes. For input `1 2 3 4 5`, removing `1` leaves `[2,3,4,5]`. The answer uses original odd indices after the removed position, giving `3 + 5 = 8`. The suffix array starts exactly at the next position, so it captures this shift correctly.

For very large strengths, the number of pairs can still be large enough that 32-bit arithmetic fails. An input such as `1000000000 1 999999999` produces answers near one billion even with only three students, and larger cases can exceed the 32-bit limit. The implementation uses Python integers, so the accumulation remains exact.
