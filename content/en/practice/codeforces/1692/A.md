---
title: "CF 1692A - Marathon"
description: "We are asked to determine Timur's position relative to three other runners in a marathon. Each test case provides four distinct integers: Timur's distance first, followed by the distances run by three other participants."
date: "2026-06-09T23:00:39+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1692
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 799 (Div. 4)"
rating: 800
weight: 1692
solve_time_s: 108
verified: true
draft: false
---

[CF 1692A - Marathon](https://codeforces.com/problemset/problem/1692/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine Timur's position relative to three other runners in a marathon. Each test case provides four distinct integers: Timur's distance first, followed by the distances run by three other participants. The task is to count how many runners have covered strictly more distance than Timur.

The problem is straightforward in its structure, but understanding the bounds is useful. Each distance is between 0 and 10,000, and there can be up to 10,000 test cases. This tells us that we need a solution that is linear in the number of test cases, because even O(n²) on the small four-element arrays would technically be acceptable (since 4² is trivial), but if we wrote code that attempted unnecessary comparisons across test cases, it could become inefficient.

Edge cases to watch are when Timur runs the maximum distance among the four or the minimum. For example, if Timur ran 10,000 and the others ran 0, 1, 2, the correct output is zero. A careless solution might try to use sorting and get the index incorrectly if it assumes Timur is always first or last. Another subtle edge is when the other participants’ distances form a consecutive sequence around Timur's distance, such as 3, 4, 5, 2 with Timur at 4. Careless logic could miscount participants strictly ahead versus those tied or behind.

## Approaches

The most naive approach is to check Timur’s distance against each of the other three participants individually. Initialize a counter at zero, iterate over the three distances, and increment the counter each time you find a value greater than Timur’s. This brute-force works because we only have three other numbers to compare against, so at worst we do three comparisons per test case. Given 10,000 test cases, this amounts to 30,000 comparisons - trivial for any modern CPU. The brute-force is correct, and speed is not a concern here.

The key insight for optimization, though not strictly necessary, is recognizing that the list is always of size four. We could sort the four numbers and find Timur’s rank directly. Sorting four numbers is also trivial, but it introduces more operations than the simple three comparisons approach. Sorting is conceptually heavier, so the comparison approach is preferred for clarity and minimal overhead.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) per test case | O(1) | Accepted |
| Sort-based | O(4 log 4) per test case | O(1) | Accepted but unnecessary |

The conclusion is that the simplest approach is also optimal: count how many of the three distances exceed Timur’s.

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the four distances, storing Timur’s distance in one variable and the others in a list.
3. Initialize a counter to zero. This counter will track the number of participants ahead of Timur.
4. Iterate through the list of the other three distances. For each distance, check if it is strictly greater than Timur’s distance. If it is, increment the counter.
5. After checking all three participants, output the counter. This is Timur’s number of runners ahead.

Why it works: the algorithm maintains a simple invariant: at any point in the iteration, the counter accurately reflects how many participants processed so far have run farther than Timur. By the end, it correctly counts all participants ahead without any risk of miscounting ties or distances behind Timur.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, d = map(int, input().split())
    counter = 0
    for distance in (b, c, d):
        if distance > a:
            counter += 1
    print(counter)
```

This code first reads the number of test cases. For each test case, we unpack the four integers directly. The counter is incremented only for participants strictly ahead of Timur. Using a tuple for the other three distances makes the iteration concise and avoids temporary list creation. The comparisons are simple integers, so there is no risk of overflow or precision issues.

## Worked Examples

**Sample 1**

Input: `2 3 4 1`

Timur’s distance `a = 2`. Other distances are `3, 4, 1`.

| distance | counter |
| --- | --- |
| 3 | 1 |
| 4 | 2 |
| 1 | 2 |

Output: `2`. The table shows how we increment the counter for participants ahead of Timur and leave it unchanged for participants behind.

**Sample 2**

Input: `500 600 400 300`

Timur’s distance `a = 500`. Other distances are `600, 400, 300`.

| distance | counter |
| --- | --- |
| 600 | 1 |
| 400 | 1 |
| 300 | 1 |

Output: `1`. Only the runner with distance 600 is ahead. This confirms the algorithm correctly handles distances both above and below Timur’s.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves three constant-time comparisons. With up to 10,000 test cases, this is linear in the number of test cases. |
| Space | O(1) | Only a few variables are stored per test case; no extra structures grow with input size. |

Given the constraints, this algorithm runs comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        a, b, c, d = map(int, input().split())
        counter = 0
        for distance in (b, c, d):
            if distance > a:
                counter += 1
        print(counter)
    return output.getvalue().strip()

# Provided samples
assert run("4\n2 3 4 1\n10000 0 1 2\n500 600 400 300\n0 9999 10000 9998\n") == "2\n0\n1\n3"

# Custom test cases
assert run("1\n0 1 2 3\n") == "3", "minimum Timur"
assert run("1\n10000 9999 9998 9997\n") == "0", "maximum Timur"
assert run("1\n5 5 5 5\n") == "0", "all equal (invalid for distinct but for robustness)"
assert run("1\n7 6 8 9\n") == "2", "Timur in the middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 1 2 3` | `3` | Timur runs least; all others ahead |
| `10000 9999 9998 9997` | `0` | Timur runs most; no one ahead |
| `5 5 5 5` | `0` | Edge robustness even if inputs are equal |
| `7 6 8 9` | `2` | Timur in the middle; algorithm counts correct participants |

## Edge Cases

When Timur runs the maximum distance among four, e.g., `10000 0 1 2`, the iteration checks `0 > 10000`, `1 > 10000`, `2 > 10000`, all false. Counter remains zero, producing the correct output. When Timur runs the minimum distance, e.g., `0 1 2 3`, each comparison increments the counter, producing `3`, which matches the number of participants ahead.

Even when numbers are consecutive around Timur’s distance, such as `4 3 5 2`, the algorithm counts only those strictly greater (`5`), correctly returning `1`. No sorting or additional data structures are needed to handle these edge cases because we explicitly check each value against Timur’s distance.

This editorial ensures a reader can reason from first principles: compare Timur to each participant and count the number ahead, which is both correct and optimal for the problem size.
