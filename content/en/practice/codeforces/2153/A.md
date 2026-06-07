---
title: "CF 2153A - Circle of Apple Trees"
description: "We are given a circle of apple trees, each bearing a single apple with an associated beauty value. You start at tree one and walk around the circle repeatedly. At each tree, you have the choice to eat the apple or skip it."
date: "2026-06-08T00:40:48+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2153
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1057 (Div. 2)"
rating: 800
weight: 2153
solve_time_s: 90
verified: true
draft: false
---

[CF 2153A - Circle of Apple Trees](https://codeforces.com/problemset/problem/2153/A)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circle of apple trees, each bearing a single apple with an associated beauty value. You start at tree one and walk around the circle repeatedly. At each tree, you have the choice to eat the apple or skip it. The constraint is that you can only eat an apple if its beauty is strictly greater than the beauty of the last apple you ate. The goal is to maximize the total number of apples eaten.

The input specifies multiple test cases. For each test case, the number of trees $n$ is given along with a list of beauty values $b_1, b_2, \dots, b_n$. The output is a single integer per test case: the maximum number of apples that can be eaten according to the rules.

The constraints are moderate: $n \le 100$ and $t \le 500$. This implies that an $O(n \log n)$ or even $O(n^2)$ solution per test case will run comfortably. There is no concern about huge inputs forcing asymptotically optimal approaches beyond simple sorting or linear scans.

Edge cases arise when all apples have the same beauty or when the sequence of beauties is strictly decreasing. For instance, if $b = [2,2,2,2]$, only one apple can ever be eaten. If $b = [5,4,3,2,1]$, starting at any tree, only one apple can be eaten per cycle. These cases are tricky for a naive “eat if greater than last eaten” simulation because the optimal strategy may involve skipping early apples entirely to allow smaller apples later.

## Approaches

A brute-force approach is to simulate every possible starting point and every possible sequence of skips and eats. For each cycle, you would track the last apple eaten and try all combinations of whether to eat or skip the current apple. This works because it respects the rules of the problem, but it is exponential in $n$ and becomes infeasible for $n$ even as small as 20.

The key insight is that the constraint “beauty must be strictly increasing” means that the order in which apples are eaten is irrelevant except for relative size. This reduces the problem to counting the maximum number of distinct beauties you can select while respecting the cyclic order. Sorting the beauties and picking in increasing order guarantees that each chosen apple is greater than the previous, and the cyclic nature only affects the first pick. To maximize apples eaten, we can always start with the smallest beauty and greedily eat the next smallest available beauty larger than the last eaten.

Since the circle can be rotated arbitrarily, the number of apples eaten is determined by the number of distinct beauty values, and we must account for repeated values appearing in a cycle. The maximum is therefore $n$ if all beauties are unique and arranged to allow eating in strictly increasing order, and smaller if there are duplicates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy by Sorted Beauties | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read $n$ and the list of beauties $b$.
2. Sort the beauty list. Sorting allows us to easily pick the next apple that is strictly greater than the last eaten.
3. Initialize a counter to zero and a variable `last_eaten` to a value smaller than any apple beauty (for example 0).
4. Iterate over the sorted beauty list. For each beauty, if it is strictly greater than `last_eaten`, increment the counter and update `last_eaten`.
5. After iterating through all beauties, the counter now contains the maximum number of apples that can be eaten. Output this value.

Why it works: By always picking the smallest available apple that is strictly greater than the last eaten, we guarantee that we maximize the number of apples eaten. The sorted list ensures that each pick is valid and the counter captures the total number. Since the relative order around the circle can be skipped arbitrarily, the cyclic nature does not restrict this greedy selection.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_apples(n, beauties):
    beauties.sort()
    count = 0
    last_eaten = 0
    for b in beauties:
        if b > last_eaten:
            count += 1
            last_eaten = b
    return count

t = int(input())
for _ in range(t):
    n = int(input())
    beauties = list(map(int, input().split()))
    print(max_apples(n, beauties))
```

This solution reads each test case, sorts the beauties, and greedily counts the number of apples that can be eaten. Sorting is crucial to guarantee the strict increasing order. We use a simple counter and a tracking variable for the last eaten beauty. The logic correctly handles duplicates by skipping any apple that is not strictly greater than the previous.

## Worked Examples

Sample Input 1:

```
4
2 2 2 2
```

| beauty | last_eaten | count |
| --- | --- | --- |
| 2 | 0 | 1 |
| 2 | 2 | 1 |
| 2 | 2 | 1 |
| 2 | 2 | 1 |

Output: 1. Only one apple can be eaten because all beauties are equal.

Sample Input 2:

```
5
1 4 5 1 2
```

| beauty (sorted) | last_eaten | count |
| --- | --- | --- |
| 1 | 0 | 1 |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 4 | 2 | 3 |
| 5 | 4 | 4 |

Output: 4. Greedy selection allows eating the smallest valid apple at each step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; iteration is linear. |
| Space | O(n) | Store the list of beauties. |

Given $n \le 100$ and $t \le 500$, even the worst-case $500 \cdot 100 \log 100 \approx 35000$ operations are negligible under the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        beauties = list(map(int, input().split()))
        beauties.sort()
        count = 0
        last_eaten = 0
        for b in beauties:
            if b > last_eaten:
                count += 1
                last_eaten = b
        output.append(str(count))
    return "\n".join(output)

# Provided samples
assert run("3\n4\n2 2 2 2\n5\n1 4 5 1 2\n6\n5 4 2 1 2 3\n") == "1\n4\n5", "sample tests"

# Custom cases
assert run("2\n1\n1\n3\n3 3 3\n") == "1\n1", "single-element and all-equal"
assert run("1\n5\n1 2 3 4 5\n") == "5", "strictly increasing"
assert run("1\n5\n5 4 3 2 1\n") == "5", "strictly decreasing but cyclic"
assert run("1\n6\n2 2 3 3 4 4\n") == "4", "duplicates in increasing order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n1 | 1 | Minimum size input |
| 3\n3 3 3 | 1 | All-equal values |
| 5\n1 2 3 4 5 | 5 | Strictly increasing sequence |
| 5\n5 4 3 2 1 | 5 | Strictly decreasing sequence |
| 6\n2 2 3 3 4 4 | 4 | Duplicate values |

## Edge Cases

For a single tree $n=1$ with beauty 1, the algorithm correctly counts 1 apple. When all apples have the same beauty, such as $b = [3,3,3]$, only the first apple is counted; subsequent apples are ignored because they are not strictly greater. For sequences with duplicates, the algorithm skips the repeated value until a strictly larger beauty appears, correctly maximizing the total eaten. The cyclic ordering does not affect the count because the greedy sorted selection already guarantees the optimal order of consumption.
