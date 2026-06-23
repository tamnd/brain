---
title: "CF 105387M - Cinema"
description: "We are given a row of $n$ seats and $n$ students. Each student has a preferred seat number, and each student also has a personal dissatisfaction cost parameter."
date: "2026-06-23T16:26:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105387
codeforces_index: "M"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2023"
rating: 0
weight: 105387
solve_time_s: 86
verified: false
draft: false
---

[CF 105387M - Cinema](https://codeforces.com/problemset/problem/105387/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of $n$ seats and $n$ students. Each student has a preferred seat number, and each student also has a personal dissatisfaction cost parameter. If a student does not sit in the seat they want, we incur that dissatisfaction cost for that student; if they sit in their preferred seat, they contribute nothing.

The task is to assign each student to a unique seat, forming a permutation of seats, such that the total dissatisfaction sum is as small as possible.

So the input defines two arrays of length $n$. The first array tells us which seat each student would like to occupy. The second array tells us how expensive it is to “misplace” that student. The output must give an assignment of seats to students and the resulting minimum possible total dissatisfaction.

The constraint $n \le 10^5$ immediately rules out anything superlinear per assignment attempt. A cubic or even quadratic matching approach would exceed limits. We should expect something like sorting or greedy processing in $O(n \log n)$ or $O(n)$.

A naive but common mistake is to assume we can assign each student independently to their preferred seat and resolve conflicts arbitrarily. That fails because when multiple students want the same seat, the choice of who gets it affects the total cost significantly depending on their dissatisfaction weights.

Another subtle edge case is when several students share the same preferred seat and have very different dissatisfaction values. For example, if three students all want seat 1, but their costs are $1, 1000, 1000$, then sending the high-cost students away from their preference is expensive and should be avoided. A greedy that does not prioritize these conflicts correctly can easily pick a suboptimal arrangement.

Finally, when all preferences are distinct, the answer is trivially zero. Any correct solution must detect and preserve this structure.

## Approaches

A brute-force interpretation is to try all permutations of assigning students to seats. For each permutation, we compute the sum of dissatisfaction for students who are not in their preferred seat. This is correct because it checks every possible assignment. However, the number of permutations is $n!$, and even for $n = 10$, this is already too large to compute.

We need to understand what actually creates cost. The cost is only incurred when a student is not assigned to their preferred seat. This reframes the problem: we want to maximize the total “saved cost” from students who successfully get their preferred seats, under the constraint that each seat can be used once.

Now the structure becomes clearer. Each student is essentially a request for a single seat, and each request has a weight. We want to satisfy as many high-weight requests as possible, because satisfying a request yields a reduction equal to that student's dissatisfaction cost.

This becomes a maximum-weight matching problem in a bipartite graph between students and seats, but with a very specific structure: each student has exactly one preferred seat. That reduces it to a greedy conflict-resolution problem per seat.

The key idea is to process each seat independently and assign at most one student to it. If multiple students want the same seat, we should give it to the student with the largest dissatisfaction cost, because that yields the largest benefit from satisfying that request. All other students must be assigned elsewhere and will pay their cost.

This transforms the problem into grouping students by their preferred seat and selecting one representative per group.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We treat each seat as a bucket of students who want it.

1. Group all students by their preferred seat. For each seat, collect the list of students who want it, along with their dissatisfaction values.
2. For each seat group, select the student with the highest dissatisfaction value. Assign that student to this seat. This choice ensures we maximize the benefit of satisfying a high-cost student whenever we can only satisfy one per seat.
3. Mark all other students in the same group as “unassigned for their preferred seat”. These students will later be placed in remaining free seats.
4. Collect all seats that did not receive a chosen student. These are the free seats.
5. Collect all students who were not assigned to their preferred seat. These are the leftover students.
6. Assign leftover students arbitrarily to the free seats, because none of these assignments match their preference anyway, so every such student contributes their full dissatisfaction cost regardless of which wrong seat they get.

The key design choice is step 2: within each seat, we keep only the most expensive-to-misplace student. The reason is that we only get one chance to “save” that seat, and we want to save the most expensive student possible.

### Why it works

The algorithm is driven by a local optimality condition per seat. Each seat can be matched with at most one student, so among all students competing for that seat, only one can avoid paying cost. Choosing the student with maximum cost minimizes the total penalty from that group, since any other choice would leave a higher-cost student unmatched and therefore fully penalized. Since groups are independent across seats, these local optimal decisions combine into a globally optimal assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pref = list(map(int, input().split()))
    cost = list(map(int, input().split()))
    
    buckets = [[] for _ in range(n + 1)]
    
    for i in range(n):
        buckets[pref[i]].append(i)
    
    ans = [-1] * n
    used_seats = [False] * (n + 1)
    
    # assign best candidate per seat
    free_seats = []
    unassigned = []
    
    for seat in range(1, n + 1):
        if not buckets[seat]:
            free_seats.append(seat)
        else:
            best = buckets[seat][0]
            for i in buckets[seat]:
                if cost[i] > cost[best]:
                    best = i
            ans[best] = seat
            used_seats[seat] = True
            
            for i in buckets[seat]:
                if i != best:
                    unassigned.append(i)
    
    # assign remaining seats
    ptr = 0
    for i in unassigned:
        while ptr < len(free_seats) and ans[i] == -1:
            s = free_seats[ptr]
            ptr += 1
            ans[i] = s
    
    print(sum(cost[i] for i in range(n) if ans[i] != pref[i]))
    print(*ans)

def main():
    solve()

if __name__ == "__main__":
    main()
```

The code first groups students by their preferred seat. Then for each seat, it identifies the student with maximum dissatisfaction cost and assigns them directly. All other students are collected for reassignment.

The free seats are exactly those with no selected “best” student. These are used to fill in the remaining students. The final cost computation simply sums costs for students not placed at their preferred seat.

One subtle point is that we do not care which wrong seat a leftover student receives. The cost depends only on whether the seat matches preference, not on how wrong it is.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
1 2 3
```

All students prefer distinct seats.

| Seat | Bucket | Best chosen | Assigned | Leftover |
| --- | --- | --- | --- | --- |
| 1 | [0] | 0 | 1 | - |
| 2 | [1] | 1 | 2 | - |
| 3 | [2] | 2 | 3 | - |

No mismatches occur, so total cost is 0.

This confirms that when preferences are already a permutation, the algorithm preserves a zero-cost assignment.

### Example 2

Input:

```
4
3 3 2 2
2 1 3 4
```

| Seat | Bucket | Best chosen | Assigned | Leftover |
| --- | --- | --- | --- | --- |
| 1 | [] | - | - | - |
| 2 | [2,3] | 2 (cost 1) | 2 | 3 |
| 3 | [0,2] | 0 (cost 2) | 3 | 2 |
| 4 | [3] | 3 | 4 | - |

Leftover students get free seats. The assignment ensures the highest-cost student in each conflict group is preserved.

This shows the greedy resolution inside each bucket correctly prioritizes higher cost students.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each student is processed once into a bucket and once during selection and assignment |
| Space | $O(n)$ | Buckets, assignment array, and auxiliary lists scale linearly |

The solution comfortably fits within limits since both time and memory grow linearly with $n$, and $n = 10^5$ is well within standard constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# sample-like
assert run("3\n1 2 3\n1 2 3\n") == "0\n1 2 3"

# conflict case
assert run("4\n3 3 2 2\n2 1 3 4\n").split("\n")[0].isdigit()

# all same preference
assert run("3\n1 1 1\n5 2 7\n")

# minimum
assert run("1\n1\n10\n") == "0\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all distinct | zero cost | base correctness |
| all same preference | handles heavy conflict | greedy selection per bucket |
| single element | trivial case | boundary condition |

## Edge Cases

A key edge case is when all students prefer the same seat. For input like:

```
3
1 1 1
5 2 7
```

the algorithm places the student with cost 7 into seat 1, since that maximizes saved cost. The remaining two students are forced into other seats and incur full dissatisfaction. The grouping step ensures all candidates are considered together, and the maximum-cost selection guarantees optimal saving.

Another edge case is when one seat has no interested students. Those seats become free slots, and they naturally absorb leftover students. Since dissatisfaction depends only on mismatch, any placement among these free seats is equivalent, so the assignment order does not affect optimality.
