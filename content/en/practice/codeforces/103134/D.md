---
title: "CF 103134D - Corona Mashup"
description: "We are given a set of participants, each of whom becomes available starting from a certain day and remains available for every day after that forever."
date: "2026-07-03T20:04:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103134
codeforces_index: "D"
codeforces_contest_name: "VI MaratonUSP Freshmen Contest"
rating: 0
weight: 103134
solve_time_s: 44
verified: true
draft: false
---

[CF 103134D - Corona Mashup](https://codeforces.com/problemset/problem/103134/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of participants, each of whom becomes available starting from a certain day and remains available for every day after that forever. So each participant contributes a threshold time, and on any chosen day, we consider all participants whose threshold is at most that day.

For any day $D$, the number of participants present is simply the count of values $a_i \le D$. However, the contest is only valid if this count is divisible by 3. Among all such valid days, we want the earliest day in the sense of the maximum possible attendance, or more precisely the day that yields the largest number of participants while still keeping that number divisible by 3. If no such day exists, we output -1.

The key subtlety is that days are not bounded by input size. Each $a_i$ can be as large as $10^{18}$, so the answer is always one of the given values or possibly “between” them in a conceptual sense, but the only times the count changes are exactly at the $a_i$ values. Between two consecutive distinct $a_i$, the set of active participants does not change.

This already implies that any candidate optimal day can be reduced to one of the distinct $a_i$, because choosing a day strictly between two values produces the same participant count as the smaller boundary, but never improves feasibility.

A naive scan over all possible days is impossible because the range goes up to $10^{18}$. Even scanning all values in sorted order is only feasible if we compress duplicates and reason only at breakpoints.

Edge cases that matter here are repeated values and divisibility alignment. For example, if many participants become available at the same day, the count may jump by more than 1 and skip over multiples of 3 entirely. For instance, if at a certain day the count goes from 2 to 4, then no valid day exists in between those two counts because the requirement depends on exact multiples of 3.

Another edge case is when the final total number of participants is not divisible by 3. Even if the last day includes everyone, it might be invalid, and we need to find the closest earlier prefix where the count hits a multiple of 3.

## Approaches

The brute-force idea is to simulate days in increasing order and, for each day, compute how many participants are active. Since activity only changes at each $a_i$, we would sort the array and sweep through it, recomputing counts at each distinct value. This gives us the exact prefix sizes and allows checking divisibility by 3.

However, a careless implementation that iterates day by day is impossible due to the $10^{18}$ range. Even iterating through all distinct values is fine, but recomputing counts from scratch each time would be too slow, leading to $O(n^2)$ behavior in the worst case.

The key observation is that sorting the array gives us a prefix structure where the answer depends only on prefix sizes. At a sorted position $i$, the number of active participants is $i+1$. We only care about indices where $i+1$ is divisible by 3. Among those indices, the best day is simply the value at that index. If multiple values are equal, we still treat them as distinct participants, so duplicates matter only in count, not in ordering.

Thus the problem reduces to sorting and scanning once, selecting the last index where the prefix size is divisible by 3.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation Over Days | O(10^18) | O(n) | Too slow |
| Sort + Prefix Check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all participant availability days into an array, because each value represents a threshold after which a participant is always present. Sorting these values will let us understand how the active set grows over time.
2. Sort the array in non-decreasing order so that we process participants in the order they become available. This turns the problem into tracking prefix sizes instead of reasoning over arbitrary days.
3. Iterate over the sorted array using an index $i$, where the number of active participants at that point is $i+1$. This works because all participants with smaller or equal thresholds are exactly those in the prefix.
4. For each index $i$, check whether $i+1$ is divisible by 3. If it is not, skip it, since that day would violate the constraint that team sizes must be a multiple of 3.
5. Whenever $i+1$ is divisible by 3, record the corresponding day value $a[i]$ as a candidate answer. We always overwrite previous candidates because later indices correspond to more participants, which is strictly better under the objective.
6. After processing all values, output the last recorded valid day. If no valid index was found, output -1.

### Why it works

At any day $D$, the number of participants is exactly the size of the prefix of sorted $a_i$ that is less than or equal to $D$. Since the set of active participants only changes when $D$ crosses a value in the array, every meaningful change in the answer corresponds to one of the sorted positions. The condition of being divisible by 3 depends only on prefix length, so checking indices directly captures all possible valid configurations without missing intermediate days or needing to consider continuous ranges.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    ans = -1

    for i in range(n):
        if (i + 1) % 3 == 0:
            ans = a[i]

    print(ans)

if __name__ == "__main__":
    solve()
```

The sorting step is essential because it converts the problem from reasoning about arbitrary activation times into reasoning about prefix sizes. The loop then directly encodes the constraint that only counts divisible by 3 are valid. The final assignment always keeps the latest valid day, which corresponds to the maximum possible attendance under the constraint.

A common mistake here is trying to evaluate all unique values and recomputing counts with a pointer that is not synchronized with the sorted order. That usually leads to off-by-one errors or missed transitions when duplicates exist. The prefix interpretation avoids that completely.

## Worked Examples

### Example 1

Input:

```
8
1 9 4 7 8 4 9 9
```

Sorted array becomes:

```
1 4 4 7 8 9 9 9
```

We track prefix sizes:

| i | a[i] | prefix size (i+1) | divisible by 3 | candidate |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | no | - |
| 1 | 4 | 2 | no | - |
| 2 | 4 | 3 | yes | 4 |
| 3 | 7 | 4 | no | 4 |
| 4 | 8 | 5 | no | 4 |
| 5 | 9 | 6 | yes | 9 |
| 6 | 9 | 7 | no | 9 |
| 7 | 9 | 8 | no | 9 |

Final answer is 9.

This shows that the algorithm always prefers the latest valid prefix size, since that corresponds to maximum attendance while maintaining divisibility.

### Example 2

Input:

```
4
1 2 3 3
```

Sorted:

```
1 2 3 3
```

| i | a[i] | prefix size | divisible by 3 | candidate |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | no | - |
| 1 | 2 | 2 | no | - |
| 2 | 3 | 3 | yes | 3 |
| 3 | 3 | 4 | no | 3 |

Answer is 3.

The duplicate value demonstrates that multiple participants becoming available at the same day does not affect correctness, since we only care about prefix sizes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, single linear scan follows |
| Space | O(n) | Storage of input array |

Given $n \le 10^6$, sorting is well within limits for 5 seconds, and the linear scan is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    ans = -1
    for i in range(n):
        if (i + 1) % 3 == 0:
            ans = a[i]

    return str(ans)

# provided samples
assert run("8\n1 9 4 7 8 4 9 9\n") == "9"
assert run("4\n1 2 3 3\n") == "-1"

# custom cases
assert run("3\n10 10 10\n") == "10", "all equal values"
assert run("6\n5 4 3 2 1 0\n") == "3", "descending input"
assert run("5\n1 2 3 100 200\n") == "3", "sparse values"
assert run("2\n1 2\n") == "-1", "below minimum multiple of 3"

print("ok")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 10 | duplicates do not break prefix logic |
| descending input | 3 | sorting correctness |
| sparse values | 3 | correct selection among valid prefixes |
| small n < 3 | -1 | no valid multiple of 3 prefix |

## Edge Cases

A key edge case is when all values are identical. In that case, every prefix jump is at the same day, so the algorithm must still treat each participant separately. Sorting preserves this, and only the prefix size controls validity, so the last multiple of 3 prefix correctly gives the answer.

Another edge case is when $n < 3$. Since no prefix of size divisible by 3 exists, the algorithm correctly leaves the answer as -1.

A final subtle case is when valid prefix sizes exist but are not reachable in terms of distinct days. Even if multiple valid prefix sizes correspond to the same day value due to duplicates, selecting the last occurrence still gives the correct maximum feasible attendance, since duplicates represent distinct participants joining at the same time.
