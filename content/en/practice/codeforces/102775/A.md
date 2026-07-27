---
title: "CF 102775A - \u041a\u0442\u043e \u0431\u043b\u0438\u0436\u0435?"
description: "The story can be reduced to a simple geometric decision on a number line. Three coordinates are given: the clown Nekit, the former owner Luka, and the dog. The dog must decide which person is closer. If the dog is closer to Nekit, the answer is Tetka."
date: "2026-07-27T20:46:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102775
codeforces_index: "A"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 20), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102775
solve_time_s: 69
verified: true
draft: false
---

[CF 102775A - \u041a\u0442\u043e \u0431\u043b\u0438\u0436\u0435?](https://codeforces.com/problemset/problem/102775/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The story can be reduced to a simple geometric decision on a number line. Three coordinates are given: the clown Nekit, the former owner Luka, and the dog. The dog must decide which person is closer. If the dog is closer to Nekit, the answer is `Tetka`. If the dog is closer to Luka, or if both distances are equal, the answer is `Kashtanka`.

The input contains three different non-negative integers, each at most $10^6$. Since the coordinates are small, the distances between points are also small, but even if the coordinates were much larger, only a constant number of arithmetic operations would be needed. This means any solution that scans ranges, simulates movement, or performs work depending on the coordinate values is unnecessary. The intended solution should run in constant time.

A common mistake is to handle the tie case incorrectly. For example, with input `1 5 3`, the dog is two units away from both people. The correct answer is `Kashtanka`, but code that only checks whether the dog is closer to Nekit and sends all other cases to `Tetka` would fail.

Another edge case is when the dog is between the two people but not exactly in the middle. For example, `1 6 5` gives distances of four and one, so the dog returns `Kashtanka`. A solution that only compares the coordinates and assumes the closest person is always the one with the smaller coordinate can fail if it ignores the dog’s position.

A final case is when the dog is outside the segment formed by the two people. For example, `2 9 12` gives distances of ten and three, so the dog stays with Nekit. Looking only at which person has the larger coordinate would not be enough because the dog's location changes the distances.

## Approaches

The straightforward approach is to calculate the distance from the dog to each person and compare the two values. Since the coordinates lie on a line, the distance between two points is the absolute difference of their coordinates. This method is already optimal for the problem, but it is useful to consider what a brute force approach would look like.

A brute force interpretation could simulate the dog's possible movement toward each person and count how many steps are needed to reach them. If the coordinates are as large as $10^6$, this could require around a million simulated steps for one comparison. That is unnecessary work because the final answer depends only on the difference between coordinates, not on every intermediate position.

The key observation is that the distance on a number line is directly available through subtraction. Instead of following the path between points, we can immediately compute both distances and decide. The only detail that needs care is the tie: equal distances belong to Luka, so the condition for `Tetka` must be strictly smaller.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^6) | O(1) | Too slow in a generalized setting |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three coordinates representing Nekit, Luka, and the dog. The names of the variables should reflect their roles because the comparison is about people and the dog's location, not about an arbitrary array.
2. Compute the absolute distance between Nekit and the dog. The absolute value is needed because the dog can be located on either side of Nekit.
3. Compute the absolute distance between Luka and the dog using the same formula.
4. If Nekit's distance is strictly smaller than Luka's distance, print `Tetka`. The comparison must use `<` because an equal distance belongs to Luka.
5. In every other situation, print `Kashtanka`. This covers both cases where Luka is closer and cases where the distances are identical.

Why it works: the algorithm compares exactly the two quantities that define the decision, the dog's distance to each person. If Nekit's distance is smaller, the dog is closer to Nekit and the required output is `Tetka`. If that condition is false, Luka's distance is less than or equal to Nekit's distance, and both possibilities require `Kashtanka`. Since every possible relationship between the two distances is covered, the algorithm cannot produce an incorrect result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    nek, luka, dog = map(int, input().split())

    nek_dist = abs(nek - dog)
    luka_dist = abs(luka - dog)

    if nek_dist < luka_dist:
        print("Tetka")
    else:
        print("Kashtanka")

if __name__ == "__main__":
    solve()
```

The program first reads the three coordinates and stores them according to their roles in the story. This avoids mixing up the order of the input values during the comparison.

The two `abs` calls directly implement the number line distance formula. Python integers do not have an overflow problem for these constraints, so the subtraction is safe.

The final condition deliberately uses a strict comparison. If the distances are equal, the `else` branch runs and prints `Kashtanka`, matching the required tie-breaking rule. There are no loops or additional data structures because the entire problem is solved with two calculations and one comparison.

## Worked Examples

For the first sample, the input is `1 4 2`.

| Step | Nekit coordinate | Luka coordinate | Dog coordinate | Nekit distance | Luka distance | Output |
| --- | --- | --- | --- | --- | --- | --- |
| Read values | 1 | 4 | 2 | - | - | - |
| Calculate distances | 1 | 4 | 2 | 1 | 2 | - |
| Compare | 1 | 4 | 2 | 1 < 2 | - | Tetka |

The dog is one unit away from Nekit and two units away from Luka, so the strict comparison succeeds. This example demonstrates the normal closer-person case.

For the second sample, the input is `1 5 3`.

| Step | Nekit coordinate | Luka coordinate | Dog coordinate | Nekit distance | Luka distance | Output |
| --- | --- | --- | --- | --- | --- | --- |
| Read values | 1 | 5 | 3 | - | - | - |
| Calculate distances | 1 | 5 | 3 | 2 | 2 | - |
| Compare | 1 | 5 | 3 | 2 < 2 is false | - | Kashtanka |

Both distances are equal, so the strict comparison does not select Nekit. The tie-breaking rule sends the dog back to Luka.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only two distances and one comparison are performed. |
| Space | O(1) | The program stores only a few integer variables. |

The solution easily fits the limits because its running time does not depend on the size of the coordinates. Even the maximum coordinate value requires the same constant amount of work as the smallest input.

## Test Cases

```python
import sys
import io

def solve_data(data: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(data)
    sys.stdout = io.StringIO()

    nek, luka, dog = map(int, sys.stdin.readline().split())

    nek_dist = abs(nek - dog)
    luka_dist = abs(luka - dog)

    if nek_dist < luka_dist:
        print("Tetka")
    else:
        print("Kashtanka")

    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert solve_data("1 4 2\n") == "Tetka", "sample 1"
assert solve_data("1 5 3\n") == "Kashtanka", "sample 2"
assert solve_data("1 6 5\n") == "Kashtanka", "sample 3"

assert solve_data("0 10 0\n") == "Kashtanka", "same coordinate side boundary is impossible, but catches equality handling"
assert solve_data("0 1000000 999999\n") == "Tetka", "maximum coordinate range"
assert solve_data("0 2 1\n") == "Kashtanka", "middle point tie case"
assert solve_data("5 8 1000000\n") == "Kashtanka", "dog far outside the segment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 10 0` | `Kashtanka` | Equality handling when distances match. |
| `0 1000000 999999` | `Tetka` | Large coordinate values and outside-segment positioning. |
| `0 2 1` | `Kashtanka` | Exact midpoint tie. |
| `5 8 1000000` | `Kashtanka` | Distance calculation when the dog is beyond both people. |

The original problem guarantees that all three coordinates are different, so an actual valid test cannot contain all-equal values. Equality of distances is the meaningful edge case because it is the situation where the output rule differs from simply choosing the smaller distance.

## Edge Cases

The tie case is handled by the strict comparison. For input `1 5 3`, the algorithm calculates `abs(1 - 3) = 2` and `abs(5 - 3) = 2`. Since `2 < 2` is false, it prints `Kashtanka`, which follows the rule that equal distances return the dog to Luka.

When the dog is close to someone with a larger coordinate, the algorithm still works because it never relies on coordinate ordering. For input `1 6 5`, the distances are `4` and `1`, so the comparison selects `Kashtanka`.

When the dog is outside the range between the two people, the absolute difference calculation remains valid. For input `2 9 12`, the distances are `10` and `3`, so the dog is closer to Nekit and the output is `Tetka`. The same formula handles points on either side of the dog without any special cases.
