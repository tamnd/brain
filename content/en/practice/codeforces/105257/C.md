---
title: "CF 105257C - Seats"
description: "We are given $n$ people and a fixed initial seating arrangement where person $i$ starts at seat $i$. Each seat is unique and every person occupies exactly one seat. Each person also has a preferred seat $ai$, which lies somewhere in a larger pool of seats $1 ldots 2n$."
date: "2026-06-24T05:01:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105257
codeforces_index: "C"
codeforces_contest_name: "2024 ICPC ShaanXi Provincial Contest"
rating: 0
weight: 105257
solve_time_s: 70
verified: true
draft: false
---

[CF 105257C - Seats](https://codeforces.com/problemset/problem/105257/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given $n$ people and a fixed initial seating arrangement where person $i$ starts at seat $i$. Each seat is unique and every person occupies exactly one seat.

Each person also has a preferred seat $a_i$, which lies somewhere in a larger pool of seats $1 \ldots 2n$. For each person, we are allowed to either keep them at their original seat $i$, or move them to their preferred seat $a_i$. No two people can occupy the same seat in the final arrangement.

The goal is to maximize how many people end up sitting in their preferred seat.

The output is only the maximum number of people who can be successfully placed at their preferred seats under these constraints.

The constraints allow $n$ up to $10^5$, so any solution that tries all subsets or simulates assignments with repeated conflict resolution will be too slow. Anything quadratic or involving repeated graph propagation per candidate choice will not pass.

A subtle difficulty is that choosing one person to take their preferred seat may force other people to move away from seats they would otherwise keep. For example, if two people want the same seat, only one of them can take it, and the other must fall back to their original seat. However, that fallback can itself be blocked if someone else already claimed it as a preferred seat.

The key edge cases come from collisions:

If multiple people want the same seat, only one can benefit from it, for example $a = [5, 5, 5]$ allows only one success for seat 5.

If preferences form chains like $1 \to 2 \to 3 \to 1$, all of them can still be satisfied simultaneously because they permute among themselves.

These two behaviors hint that conflicts only matter when multiple edges target the same seat, not when dependencies form cycles.

## Approaches

A brute-force approach would try to decide, for each person, whether to keep them at $i$ or move them to $a_i$, while ensuring no seat is used twice. This is essentially searching over all valid subsets of chosen moves. The state space is exponential, and even a greedy simulation would repeatedly resolve collisions that propagate through the structure of seat dependencies, leading to potentially quadratic behavior when cascades occur.

The key simplification comes from observing how conflicts actually arise. Every person contributes exactly one candidate target seat $a_i$. The only real restriction on choosing these moves is that a seat cannot be assigned to more than one person who chooses their preferred option.

If multiple people point to the same seat, at most one of them can succeed. If we select one of them, that seat becomes occupied and forces its original owner to move, but that does not reduce the number of satisfied people we can achieve elsewhere.

This means each seat $v$ can contribute at most one satisfied person among all $i$ such that $a_i = v$. Therefore, the best we can ever do is count how many distinct seats appear in the preference list.

What remains is whether this upper bound is always achievable. It is. We can assign, for every distinct seat $v$, exactly one person that wants it, and then resolve forced moves outward. These forced moves never reduce the count because they only determine where non-selected or fallback assignments go, not how many preferred-seat assignments we already fixed.

Thus the answer reduces to the number of distinct values in $a$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force search over assignments | exponential | O(n) | Too slow |
| Count distinct preferences | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We want to compute how many different seats appear among all preferred seats.

1. Read all values $a_1, a_2, \ldots, a_n$. These represent target seats people want to occupy.
2. Insert every value into a set or mark it in a boolean array. This removes duplicates automatically, ensuring each seat is counted only once.
3. The size of this set after processing all values is the answer, since each distinct seat can contribute at most one satisfied person, and this upper bound can always be realized.

The implementation does not need to construct the final seating or simulate movements because the structure of conflicts collapses into simple uniqueness counting.

### Why it works

Every successful assignment to a preferred seat consumes that seat exactly once. If two or more people target the same seat, only one of them can be selected, so duplicates cannot increase the answer beyond one per seat.

At the same time, choosing a representative person for each distinct seat never creates a blocking contradiction that reduces the number of chosen preferred-seat assignments. Any forced adjustments caused by freeing original seats only affect fallback placements, which are irrelevant to the objective.

So the maximum number of satisfied people equals the number of distinct preferred seats.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

seen = set()
for x in a:
    seen.add(x)

print(len(seen))
```

The solution reads all preferences and stores them in a set. The set automatically ensures duplicates do not affect the count. The final size of the set is printed.

The only subtle implementation detail is to avoid any unnecessary simulation of seat movements. Even though the story suggests dependencies between people when seats are taken, those dependencies do not affect how many preferred-seat assignments can be made.

## Worked Examples

Consider an input where several people share preferences:

Input:

$n = 5$, $a = [2, 2, 3, 3, 3]$

| Step | Processed value | Seen set |
| --- | --- | --- |
| 1 | 2 | {2} |
| 2 | 2 | {2} |
| 3 | 3 | {2, 3} |
| 4 | 3 | {2, 3} |
| 5 | 3 | {2, 3} |

The answer is 2, since only seats 2 and 3 are targeted. This matches the idea that each seat can contribute at most one satisfied person.

Now consider a case with no repetition:

Input:

$n = 4$, $a = [5, 6, 7, 8]$

| Step | Processed value | Seen set |
| --- | --- | --- |
| 1 | 5 | {5} |
| 2 | 6 | {5, 6} |
| 3 | 7 | {5, 6, 7} |
| 4 | 8 | {5, 6, 7, 8} |

All preferences are distinct, so every person can be satisfied.

These traces show that only collisions reduce the achievable count, and each collision collapses to a single usable slot per seat.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each preference is inserted into a hash set once |
| Space | O(n) | The set stores up to $n$ distinct seat values |

The algorithm easily fits within constraints for $n \le 10^5$, since both memory and runtime scale linearly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    return str(len(set(a)))

# provided sample-style checks
assert run("2\n1 2\n") == "2"
assert run("3\n1 1 1\n") == "1"

# custom cases
assert run("1\n5\n") == "1", "single element"
assert run("5\n1 2 3 4 5\n") == "5", "all distinct"
assert run("5\n2 2 2 2 2\n") == "1", "all equal"
assert run("6\n1 2 2 3 3 3\n") == "3", "mixed duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal boundary case |
| all distinct | n | full utilization case |
| all equal | 1 | maximal collision case |
| mixed duplicates | 3 | general correctness of deduplication |

## Edge Cases

When all preferences are identical, for example $a = [7, 7, 7, 7]$, only one person can be satisfied. The algorithm produces a set with one element, correctly capturing this limitation.

When all preferences are distinct, for example $a = [1, 2, 3, 4]$, every person can be assigned their desired seat. The set contains all values, and the answer equals $n$.

When preferences mix duplicates and unique values, such as $a = [1, 2, 2, 3, 3]$, each duplicated seat contributes only once. The set construction naturally collapses duplicates, ensuring no overcounting and no need for explicit conflict resolution logic.
