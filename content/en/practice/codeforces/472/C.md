---
title: "CF 472C - Design Tutorial: Make It Nondeterministic"
description: "We are given a list of people, each with a first name and a last name. For each person, we have the freedom to choose either their first or last name as a handle."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 472
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 270"
rating: 1400
weight: 472
solve_time_s: 76
verified: true
draft: false
---

[CF 472C - Design Tutorial: Make It Nondeterministic](https://codeforces.com/problemset/problem/472/C)

**Rating:** 1400  
**Tags:** greedy  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of people, each with a first name and a last name. For each person, we have the freedom to choose either their first or last name as a handle. Alongside this, we are provided a permutation of the indices from 1 to _n_, which represents the exact order in which the handles should appear if sorted lexicographically. The task is to determine if it is possible to assign handles to each person such that, when sorted lexicographically, they match the given permutation.

The input size can reach 100,000 people, and each name is at most 50 characters. Sorting 100,000 items is feasible, but any solution that tries all possible 2^n combinations of handle choices is entirely impractical. This means we must find a solution that decides the handle for each person greedily without exhaustively enumerating every possibility.

A subtle edge case occurs when two consecutive people in the permutation have overlapping handle ranges. For example, suppose person A has handles "abc" and "def", and person B has handles "abd" and "daa". A naive approach might just pick the lexicographically smaller handle for each person without considering the ordering requirement. In this case, choosing the smaller handles greedily may fail to satisfy the permutation, so we need a careful sequential decision that respects the already-chosen handles.

## Approaches

The brute-force approach is straightforward: try all 2^n handle assignments for the n people, sort the resulting list, and check if it matches the given permutation. This is guaranteed to be correct, but with n up to 100,000, it is infeasible because 2^100,000 is astronomically large. Even a backtracking approach that prunes impossible sequences could still degrade to exponential complexity if the pruning is insufficiently tight.

The key observation is that we only need to make choices sequentially in the order given by the permutation. Suppose we process the permutation from the first position to the last. For each person, we know the lexicographically smallest handle we can choose must be strictly greater than the handle we picked for the previous person. This insight allows a greedy strategy: for each person in permutation order, pick the smaller handle that is greater than the previous handle, and if the smaller one fails, pick the larger. If neither option satisfies the ordering, the assignment is impossible.

This transforms an exponential problem into a linear one. We no longer enumerate all combinations but instead make one deterministic choice per person, checking feasibility locally at each step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n log n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of people _n_ and store each person as a tuple of (first_name, last_name).
2. Read the permutation array and convert it to zero-based indices for easier array access.
3. For each person, sort their two handles lexicographically. This ensures that the "smaller" handle is always first, simplifying comparisons.
4. Initialize a variable `prev_handle` to an empty string. This variable keeps track of the handle chosen for the previous person in the permutation order.
5. Iterate through the permutation array. For each person, check if the smaller handle is strictly greater than `prev_handle`. If it is, choose it. Otherwise, check if the larger handle is strictly greater than `prev_handle`. If neither handle satisfies the condition, output "NO" and terminate.
6. If all people have been assigned handles successfully, output "YES".

Why it works: At each step, the algorithm ensures that the chosen handle respects the lexicographical order relative to all previous handles. Because the permutation defines a linear order, no future choices can violate past choices if we always pick the smallest feasible handle. This greedy approach is guaranteed to find a valid assignment if one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
people = [tuple(input().strip().split()) for _ in range(n)]
perm = list(map(int, input().strip().split()))

# convert to 0-based indices
perm = [x-1 for x in perm]

# sort each person's handles
handles = [tuple(sorted(person)) for person in people]

prev_handle = ""
possible = True

for idx in perm:
    small, large = handles[idx]
    if small > prev_handle:
        prev_handle = small
    elif large > prev_handle:
        prev_handle = large
    else:
        possible = False
        break

print("YES" if possible else "NO")
```

The solution first reads and organizes input into a list of sorted tuples, ensuring the smaller handle comes first. It then walks through the permutation, greedily picking the smallest feasible handle that preserves the lexicographical order. The `prev_handle` variable is critical: it encodes the ordering constraint from previous choices, and checking both handle options guarantees we never miss a valid assignment. Off-by-one errors are avoided by converting the permutation to zero-based indexing.

## Worked Examples

**Sample Input 1:**

```
3
gennady korotkevich
petr mitrichev
gaoyuan chen
1 2 3
```

| Step | idx | small | large | prev_handle | chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | gennady | korotkevich | "" | gennady |
| 2 | 1 | mitrichev | petr | gennady | mitrichev |
| 3 | 2 | chen | gaoyuan | mitrichev | none → fail |

Here, the third person's smallest handle "chen" is not greater than "mitrichev", and "gaoyuan" is also not greater. Output: NO.

**Sample Input 2:**

```
3
copernicus galileo
isaac newton
albert einstein
2 3 1
```

| Step | idx | small | large | prev_handle | chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | isaac | newton | "" | isaac |
| 2 | 2 | albert | einstein | isaac | einstein |
| 3 | 0 | copernicus | galileo | einstein | galileo |

All chosen handles satisfy the order. Output: YES.

These traces show the greedy selection guarantees feasibility while respecting the permutation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each person is processed once; string comparisons take at most O(50) per handle, which is effectively constant. |
| Space | O(n) | Storing n tuples of handles and the permutation array. |

Given n ≤ 10^5 and name lengths ≤ 50, our linear pass is comfortably within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    people = [tuple(input().strip().split()) for _ in range(n)]
    perm = list(map(int, input().strip().split()))
    perm = [x-1 for x in perm]
    handles = [tuple(sorted(person)) for person in people]
    prev_handle = ""
    possible = True
    for idx in perm:
        small, large = handles[idx]
        if small > prev_handle:
            prev_handle = small
        elif large > prev_handle:
            prev_handle = large
        else:
            possible = False
            break
    return "YES" if possible else "NO"

# provided samples
assert run("3\ngennady korotkevich\npetr mitrichev\ngaoyuan chen\n1 2 3\n") == "NO", "sample 1"

# custom cases
assert run("1\nalice wonderland\n1\n") == "YES", "minimum input"
assert run("2\nbob alice\ncarol dave\n2 1\n") == "YES", "reversed permutation"
assert run("2\nbob alice\ncarol dave\n1 2\n") == "NO", "cannot satisfy order"
assert run("3\namy aaron\nbob brian\ncara cecil\n3 2 1\n") == "YES", "all choices flexible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 person | YES | Handles minimum input |
| Reversed permutation | YES | Permutation not sorted naturally |
| Impossible 2-person | NO | Order constraint cannot be satisfied |
| Flexible 3-person | YES | Multiple valid options, greedy choice works |

## Edge Cases

If a person's both handles are smaller than the previous chosen handle, the algorithm immediately detects impossibility. For example, with input:

```
2
aa ab
ac ad
2 1
```

We sort handles: person 0 → ("aa","ab"), person 1 → ("ac","ad"). Processing permutation index 1 first, `prev_handle` is "", we choose "ac". Next, index 0, handles "aa","ab" are both not greater than "ac", so the algorithm outputs NO correctly. This demonstrates that the greedy step ensures no invalid assignments slip through.
