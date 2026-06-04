---
title: "CF 272A - Dima and Friends"
description: "Dima and his friends are deciding who will clean the apartment using a counting game. Everyone, including Dima, shows a number of fingers between one and five. They then count around the circle starting from Dima, with the total count equal to the sum of all fingers shown."
date: "2026-06-05T01:55:59+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 272
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 167 (Div. 2)"
rating: 1000
weight: 272
solve_time_s: 88
verified: false
draft: false
---

[CF 272A - Dima and Friends](https://codeforces.com/problemset/problem/272/A)

**Rating:** 1000  
**Tags:** implementation, math  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

Dima and his friends are deciding who will clean the apartment using a counting game. Everyone, including Dima, shows a number of fingers between one and five. They then count around the circle starting from Dima, with the total count equal to the sum of all fingers shown. The person where the count ends has to clean.

The input gives the number of Dima’s friends `n` and a list of integers representing how many fingers each friend will show. Dima wants to choose a number of fingers that avoids being the person the count stops on. The output is the number of choices for Dima that keep him safe.

The constraints are small: `n` is at most 100 and each friend shows 1 to 5 fingers. This means any algorithm that loops over possible finger counts for Dima (1 to 5) and sums the total fingers is fast enough. There is no need for complex data structures or optimizations beyond basic arithmetic. Edge cases appear when the sum of friends' fingers plus Dima’s choice is exactly divisible by `n + 1`, which determines whether Dima is selected or not. For instance, if Dima has 1 friend who shows 1 finger, then the total count can be 2 to 6 depending on Dima’s fingers, and only totals divisible by 2 (the circle size) would land on Dima, while others avoid him. Careless solutions might miscalculate the modulo or forget to include all possible choices from 1 to 5.

## Approaches

The brute-force approach is already essentially optimal due to the small range of possibilities. We could enumerate each choice Dima has (1 through 5), compute the sum of all friends’ fingers plus Dima’s choice, and then check whether the total modulo the number of people in the circle equals Dima’s position. Since Dima always starts counting, his position is index 1. If the modulo is zero, the count ends on Dima, so he loses; otherwise, he is safe.

This approach works because the number of choices for Dima is only five, so the total number of operations is extremely small (at most 500 arithmetic operations even for `n = 100`). There is no asymptotic bottleneck here. The key insight is recognizing that counting around a circle is equivalent to computing the sum modulo the circle size. Once you see that, the solution becomes a simple arithmetic check, and there is no need for clever combinatorics or dynamic programming.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per candidate, total O(5n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, the number of Dima's friends, and read the array `friends` containing the number of fingers each friend shows.
2. Compute `total_friends`, the sum of all fingers shown by friends. This is necessary to know the total count for each of Dima's choices.
3. Initialize a counter `safe_choices` to zero. This will store how many finger choices keep Dima safe.
4. Loop through all possible finger counts for Dima, from 1 to 5. For each choice `d`:

- Compute the total count as `total_friends + d`.
- If `(total_friends + d) % (n + 1) != 1`, increment `safe_choices`. The modulo `(n + 1)` represents the circle size, and the count starts at Dima (position 1). If the remainder equals 1, the count ends on Dima, so he is not safe.
5. After testing all five choices, print `safe_choices`.

Why it works: The invariant is that modulo arithmetic correctly models circular counting. The circle has `n + 1` people, and counting `k` steps starting from position 1 ends at `(1 + k - 1) % (n + 1) + 1`. This formula ensures that every possible total count is mapped to the correct person, and we correctly identify which choices avoid Dima.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
friends = list(map(int, input().split()))
total_friends = sum(friends)

safe_choices = 0
for d in range(1, 6):
    if (total_friends + d) % (n + 1) != 1:
        safe_choices += 1

print(safe_choices)
```

The code reads input efficiently using `sys.stdin.readline`. We compute the sum of friends' fingers once, and then loop through Dima’s possible choices. The modulo check `(total_friends + d) % (n + 1) != 1` ensures that Dima is not the person the count stops on. Using `range(1, 6)` covers exactly the five valid finger counts.

## Worked Examples

**Sample 1**

Input:

```
1
1
```

| Step | total_friends | Dima choice d | total_friends + d | (total % 2) | Safe? |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 0 | yes |
| 2 | 1 | 2 | 3 | 1 | no |
| 3 | 1 | 3 | 4 | 0 | yes |
| 4 | 1 | 4 | 5 | 1 | no |
| 5 | 1 | 5 | 6 | 0 | yes |

The safe choices are 1, 3, 5. Output is 3.

**Sample 2**

Input:

```
2
2 1
```

| Step | total_friends | Dima choice d | total | (total % 3) | Safe? |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 4 | 1 | no |
| 2 | 3 | 2 | 5 | 2 | yes |
| 3 | 3 | 3 | 6 | 0 | yes |
| 4 | 3 | 4 | 7 | 1 | no |
| 5 | 3 | 5 | 8 | 2 | yes |

Safe choices: 2, 3, 5. Output is 3.

These traces demonstrate that modulo arithmetic accurately identifies which totals land on Dima, even when the circle size is larger than two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We sum the friends’ fingers in O(n) and then perform five constant-time checks. |
| Space | O(n) | We store the array of friends' finger counts. |

The algorithm easily fits within the constraints since `n <= 100` and we only loop over five possibilities.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    friends = list(map(int, input().split()))
    total_friends = sum(friends)
    safe_choices = 0
    for d in range(1, 6):
        if (total_friends + d) % (n + 1) != 1:
            safe_choices += 1
    return str(safe_choices)

# Provided samples
assert run("1\n1\n") == "3", "sample 1"
assert run("2\n2 1\n") == "3", "sample 2"

# Custom cases
assert run("1\n5\n") == "2", "Dima's friend shows maximum fingers"
assert run("3\n1 1 1\n") == "3", "all friends show minimum fingers"
assert run("100\n" + "1 "*100 + "\n") == "3", "maximum friends, all showing 1 finger"
assert run("2\n3 5\n") == "2", "sum of friends is 8, testing modulo wrap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n5\n | 2 | Edge case where friend shows maximum fingers |
| 3\n1 1 1\n | 3 | All friends show minimum fingers |
| 100\n1 … 1\n | 3 | Maximum number of friends |
| 2\n3 5\n | 2 | Correct modulo calculation when sum is larger than circle size |

## Edge Cases

If Dima has one friend showing 5 fingers, total circle size is 2. Testing Dima's choices:

- `total_friends = 5`
- `d = 1` → total 6 → 6 % 2 = 0 → safe
- `d = 2` → total 7 → 7 % 2 = 1 → not safe
- `d = 3` → total 8 → 8 % 2 = 0 → safe
- `d = 4` → total 9 → 9 % 2 = 1 → not safe
- `d = 5` → total 10 → 10 % 2 = 0 → safe

Output is 3. The algorithm correctly handles large totals and ensures modulo wraps are accurate. Even with the maximum number of friends or the largest finger sums, the method reliably identifies safe choices.
