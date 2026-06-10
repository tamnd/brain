---
title: "CF 1453A - Cancel the Trains"
description: "We are asked to manage a train system on a 100×100 grid. Trains can move either vertically from the bottom to the top or horizontally from the left to the right."
date: "2026-06-11T03:02:16+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1453
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 688 (Div. 2)"
rating: 800
weight: 1453
solve_time_s: 85
verified: true
draft: false
---

[CF 1453A - Cancel the Trains](https://codeforces.com/problemset/problem/1453/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to manage a train system on a 100×100 grid. Trains can move either vertically from the bottom to the top or horizontally from the left to the right. Each train has a unique number from 1 to 100 depending on its starting point, and all trains move at the same constant speed. At a given moment, some subset of trains is scheduled to depart from the bottom and some from the left. If a vertical train and a horizontal train occupy the same coordinate at the same time, a crash occurs.

The goal is to determine the minimum number of trains to cancel to avoid all collisions. Each test case specifies how many vertical and horizontal trains are scheduled, along with their train numbers. The output is a single integer per test case: the smallest number of cancellations needed.

The constraints are small: a maximum of 100 trains on each side and up to 100 test cases. This immediately implies that any algorithm with roughly O(n·m) operations per test case, where n and m are the numbers of trains, will be fast enough. Each train number is between 1 and 100, so we can efficiently represent train schedules with arrays or sets.

An edge case to be wary of is when the smallest train number on the bottom matches the largest on the left. For example, if bottom trains = [1] and left trains = [1], a naive approach might assume no crash occurs because numbers are different lists, but in reality, the grid position overlaps at (1,1). Another scenario is when either n=1 or m=1; we must ensure we do not try to compare nonexistent elements.

## Approaches

A brute-force approach would simulate every train’s trajectory and check for collisions at every possible coordinate. For each bottom train, you would compare its path to every left train. Since a train moves from (i,0) to (i,101) and the other from (0,j) to (101,j), their paths intersect only at the point (i,j). This reduces the problem: a collision occurs if a train from the bottom has the same number as a train from the left. Using this insight, we can count the number of train numbers that appear in both lists; that is the maximum number of potential collisions. Canceling one train from each conflicting pair is enough to avoid the crash.

The key observation is that only the intersection of train numbers matters. If a number appears in both the bottom and left schedules, those two trains will collide. Since we can cancel any one of the conflicting trains to resolve a collision, the minimum cancellations required is the smaller of the counts of vertical or horizontal trains involved in collisions. However, because each number is unique, at most one vertical and one horizontal train share a number, so the minimum cancellations is exactly the size of the intersection.

This insight reduces the algorithm from a potential O(n·m) simulation to a simple set intersection computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all paths) | O(n·m) | O(n·m) | Works for small n, m, acceptable here but unnecessary |
| Optimal (set intersection) | O(n+m) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of bottom trains `n` and left trains `m`.
2. Read the list of scheduled bottom train numbers and store them in a set for fast lookup.
3. Read the list of scheduled left train numbers and store them in another set.
4. Compute the intersection of the two sets. This gives all train numbers scheduled on both axes that would collide.
5. The size of the intersection is the minimum number of trains to cancel. Print this number.

Why it works: every potential collision is represented by a train number appearing in both lists. Canceling one train from each conflicting pair eliminates the collision. Since each train number occurs at most once per side, there is a one-to-one mapping between intersecting train numbers and collisions. This guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        bottom_trains = set(map(int, input().split()))
        left_trains = set(map(int, input().split()))
        collisions = bottom_trains & left_trains
        print(len(collisions))

if __name__ == "__main__":
    main()
```

The solution reads the number of test cases first. Each test case is processed by reading two lists of train numbers. Converting lists to sets allows O(1) average membership checks and direct computation of intersections. Using `&` computes the set intersection efficiently. The length of the intersection gives the minimum number of cancellations needed.

## Worked Examples

### Sample Input 1

```
1 2
1
3 4
```

| bottom_trains | left_trains | intersection | result |
| --- | --- | --- | --- |
| {1} | {3,4} | {} | 0 |

There are no common train numbers, so no cancellations are needed.

### Sample Input 2

```
3 2
1 3 4
2 4
```

| bottom_trains | left_trains | intersection | result |
| --- | --- | --- | --- |
| {1,3,4} | {2,4} | {4} | 1 |

The intersection contains train number 4, which would collide. Canceling one of the trains resolves the collision.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Converting lists to sets and computing intersection is linear in the total number of trains |
| Space | O(n + m) per test case | Storing sets of trains |

Given the constraints (n,m ≤ 100, t ≤ 100), the total number of operations is at most 100×(100+100) = 20,000, which is trivial for modern processors.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided samples
assert run("3\n1 2\n1\n3 4\n3 2\n1 3 4\n2 4\n9 14\n2 7 16 28 33 57 59 86 99\n3 9 14 19 25 26 28 35 41 59 85 87 99 100\n") == "0\n1\n3", "Sample 1"

# Custom test cases
assert run("1\n1 1\n1\n1\n") == "1", "single collision"
assert run("1\n2 2\n1 2\n3 4\n") == "0", "no collision"
assert run("1\n3 3\n1 2 3\n1 2 3\n") == "3", "all collide"
assert run("1\n1 3\n100\n98 99 100\n") == "1", "boundary numbers"
assert run("1\n2 1\n50 60\n60\n") == "1", "one collision in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 / 1 | 1 | Single train collision |
| 2 2 / 1 2 / 3 4 | 0 | No collision case |
| 3 3 / 1 2 3 / 1 2 3 | 3 | All trains collide |
| 1 3 / 100 / 98 99 100 | 1 | Edge number collision |
| 2 1 / 50 60 / 60 | 1 | Collision in the middle |

## Edge Cases

If either the bottom or left list contains only one train, the algorithm still works. For input `1 1 / 1 / 2`, the sets are `{1}` and `{2}`, their intersection is empty, and the output is 0. For input `1 1 / 1 / 1`, both sets are `{1}`, intersection size is 1, correctly identifying a collision. The algorithm naturally handles the smallest and largest train numbers without special casing.
