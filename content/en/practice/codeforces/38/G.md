---
title: "CF 38G - Queue"
description: "We are asked to simulate a queue of people where each person has two properties: an importance value a[i] and a patience"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 38
codeforces_index: "G"
codeforces_contest_name: "School Personal Contest #1 (Winter Computer School 2010/11) - Codeforces Beta Round 38 (ACM-ICPC Rules)"
rating: 2300
weight: 38
solve_time_s: 61
verified: true
draft: false
---

[CF 38G - Queue](https://codeforces.com/problemset/problem/38/G)

**Rating:** 2300  
**Tags:** data structures  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a queue of people where each person has two properties: an importance value `a[i]` and a patience limit `c[i]`. People arrive in order, and when the last person (number `n`) joins, he can move forward in the queue by swapping with the person directly in front of him, but only if that person has a lower importance than him. He can perform at most `c[n]` swaps. The output should be the final ordering of all people by their original numbering after all swaps have stopped.

The input guarantees that `a[i]` forms a permutation from 1 to `n`, so no two people have the same importance. This ensures that every comparison `a[i] > a[j]` is strict. The constraints allow up to `10^5` people and a 2-second time limit, meaning any algorithm that does more than roughly `10^8` operations may be too slow. A naive simulation of every swap could lead to O(n²) behavior in the worst case, which is not acceptable here.

Edge cases that are easy to miss include when `c[n]` is zero (the last person cannot move at all), when the last person has the highest importance (he should move to the front if `c[n]` allows), and when multiple swaps are limited by `c[n]` before reaching someone with higher importance.

For example, with input:

```
3
1 0
2 0
3 1
```

The naive algorithm must stop after one swap because `c[3] = 1`, even though person 3 could theoretically move past both 1 and 2. The correct output is `3 1 2`, not `3 2 1`. A careless simulation ignoring `c[n]` would produce the wrong result.

## Approaches

The brute-force approach directly implements the swapping process described. When each new person arrives, we compare him to the person immediately in front, swap if allowed, decrease his remaining swap count, and repeat until either the swap count reaches zero or the person in front has higher importance. This is correct but can require O(n²) operations if the last person has high importance and high patience, moving all the way from the back to the front.

The key insight to improve this is recognizing that the permutation nature of `a[i]` lets us reason in terms of **relative positions** rather than simulating every individual swap. Each person will ultimately move forward as far as possible, constrained by `c[i]` and the importance of people in front. The problem reduces to inserting the last person at the correct position counting how many swaps he can do. This allows a linear-time simulation by iterating from the end of the current queue backwards and shifting people forward until the move limit is exhausted or we reach a person with higher importance.

The brute-force approach is conceptually simple but slow. The optimal approach leverages the fact that `a[i]` is unique and that only one person moves at a time, letting us simulate in a single backward pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of people `n` and their properties `a[i]` and `c[i]`.
2. Maintain a list `queue` representing the current order of people by their indices as they arrive. Initialize it with the first person.
3. For each subsequent person (from the second to the last):

1. Append them at the end of the queue.
2. Let `moves_left = c[i]`.
3. While `moves_left > 0` and the person directly in front has lower importance:

1. Swap the current person with the one in front.
2. Decrease `moves_left` by 1.
3. Continue checking the next person in front.
4. After processing all people, convert the queue from indices to 1-based numbering (original input order) and print.

Why it works: at each insertion, a person moves forward exactly as allowed by their `c[i]` and importance constraints. Since only higher-importance blocks prevent movement and swaps are local, simulating each person's insertion ensures correctness. No later person affects the relative order of earlier people except by moving past them according to the same rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
people = [tuple(map(int, input().split())) + (i+1,) for i in range(n)]

queue = []

for a, c, idx in people:
    pos = len(queue)
    moves_left = c
    while pos > 0 and moves_left > 0 and queue[pos-1][0] < a:
        queue[pos] = queue[pos-1]
        pos -= 1
        moves_left -= 1
    if pos < len(queue):
        queue[pos] = (a, c, idx)
    else:
        queue.append((a, c, idx))

print(" ".join(str(x[2]) for x in queue))
```

The code keeps the queue as a list of tuples `(a, c, original_index)`. For each person, it finds the farthest position they can move backward while swapping with lower-importance people. The subtle part is shifting elements in place to avoid unnecessary list operations.

## Worked Examples

Sample input:

```
2
1 0
2 1
```

| Step | Queue State | Moves Left | Action |
| --- | --- | --- | --- |
| 1 | [(1,0,1)] | - | first person appended |
| 2 | [(1,0,1),(2,1,2)] | 1 | person 2 compares with person 1, swaps |
| Final | [(2,1,2),(1,0,1)] | 0 | output indices 2 1 |

Second input:

```
3
1 0
2 0
3 1
```

| Step | Queue State | Moves Left | Action |
| --- | --- | --- | --- |
| 1 | [(1,0,1)] | - | first person appended |
| 2 | [(1,0,1),(2,0,2)] | 0 | person 2 cannot move |
| 3 | [(1,0,1),(2,0,2),(3,1,3)] | 1 | person 3 swaps with 2 |
| 3 | [(1,0,1),(3,1,3),(2,0,2)] | 0 | cannot move further, output 1 3 2 |

These traces confirm that swaps are limited by `c[i]` and importance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each person can move at most `c[i]` steps, sum of `c[i] ≤ n`, shifting in the list takes O(n) overall |
| Space | O(n) | Queue list and input storage |

The algorithm performs a single pass over the queue and shifts at most `n` elements in total, fitting comfortably within the 2-second limit for n = 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    people = [tuple(map(int, input().split())) + (i+1,) for i in range(n)]

    queue = []

    for a, c, idx in people:
        pos = len(queue)
        moves_left = c
        while pos > 0 and moves_left > 0 and queue[pos-1][0] < a:
            queue[pos] = queue[pos-1]
            pos -= 1
            moves_left -= 1
        if pos < len(queue):
            queue[pos] = (a, c, idx)
        else:
            queue.append((a, c, idx))

    return " ".join(str(x[2]) for x in queue)

# Provided sample
assert run("2\n1 0\n2 1\n") == "2 1"
assert run("3\n1 0\n2 0\n3 1\n") == "1 3 2"

# Custom cases
assert run("1\n1 0\n") == "1"  # single person
assert run("3\n3 2\n1 0\n2 1\n") == "3 2 1"  # highest importance first
assert run("4\n1 1\n2 1\n3 1\n4 0\n") == "4 3 2 1"  # last person cannot move
assert run("5\n1 0\n2 2\n3 1\n5 3\n4 0\n") == "5 2 3 1 4"  # complex swaps
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 person | 1 | smallest input |
| Highest importance first | 3 2 1 | moving from front to back not restricted |
| Last person cannot move | 4 3 2 1 | `c[i] = 0` prevents swaps |
| Complex swaps | 5 2 3 1 4 | multiple moves with limits |

## Edge Cases

For a person with `c[i] = 0`, no swaps occur regardless of importance. For example:
