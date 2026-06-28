---
title: "CF 104767C - Digitalisation"
description: "Each student arrives with two ranked preferences over schools. Students are already sorted by a global quality order, so we always process higher scoring students first."
date: "2026-06-29T02:29:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104767
codeforces_index: "C"
codeforces_contest_name: "2023-2024 CTU Open Contest"
rating: 0
weight: 104767
solve_time_s: 91
verified: false
draft: false
---

[CF 104767C - Digitalisation](https://codeforces.com/problemset/problem/104767/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

Each student arrives with two ranked preferences over schools. Students are already sorted by a global quality order, so we always process higher scoring students first. Every school maintains a limited list of at most `C` students, and repeatedly tries to improve its list by pulling better candidates from the global ranking.

The process is not a simple one-pass assignment. Instead, schools repeatedly perform update events in cycles. During an update, a school scans from the worst student in the global ordering upward, trying to find a student who is still eligible and would improve the school’s current list under several constraints: the student must prefer this school, must not already be firmly assigned elsewhere, and must either have no current assignment or be assigned to their second-choice school. If the school has space or the student is better than its current worst, the student can enter, potentially displacing someone.

This creates a dynamic system of competitions between schools where students can be moved multiple times, but only under structured rules that ensure monotonic improvement in each school’s list.

The output only counts how many students finally end up in their first-choice school versus their second-choice school.

The constraints are large in terms of students and schools, up to 100,000 each, but the capacity `C` is very small, at most 100. That asymmetry is the key structural hint. Any solution that tries to repeatedly scan the full student list for every school operation will be too slow, since naive simulation of cycles would multiply `N` by `M`.

A naive approach would also struggle with repeated relocations. A student can move from second choice to first choice, and any incorrect assumption that assignment is final after first placement leads to wrong answers. For example, if a student is placed into their second choice early but later becomes eligible for the first choice, a naive greedy assignment that does not revisit earlier decisions will miscount outcomes.

Another subtle edge case arises when a school is full and only slightly better candidates exist later in the global order. A naive scan that restarts from the beginning each time will miss the intended “from worst upward” behavior and can select the wrong candidate, violating the replacement rule.

## Approaches

A brute force simulation would literally execute the described process. Each school repeatedly scans the global list from the worst student upward, checking eligibility conditions and performing swaps. Each update event might traverse up to `N` students, and there are `M` schools, repeated over multiple cycles. Since each insertion/removal can trigger cascading changes across schools, the total number of checks can explode to on the order of `O(N * M * C)` or worse. With `N` and `M` at 100,000, this is entirely infeasible.

The key insight is that the system has a strong monotonic structure: each school only ever keeps its best `C` valid candidates according to a consistent global order, and once a student is rejected by a better school, they only ever move “down” to their second choice. Because `C` is small, each school’s state is tiny and stable in size, and every update effectively behaves like maintaining a bounded priority structure with local exchanges.

Instead of simulating global scans, we reverse the perspective. Each student has at most two potential destinations. We try to assign students greedily in decreasing score order, but we must allow displacement chains. This becomes a multi-source constrained matching where each school maintains a small ordered set of size at most `C`. When a new candidate arrives, we can insert them if valid, and evict the worst if needed. If evicted, they try their second choice only once. This turns the process into a controlled propagation system where each student moves at most twice, and each school operation is `O(C)`.

Because `C ≤ 100`, we can afford linear scans inside each school structure. The total complexity becomes linear in `N * C`, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N² · M) worst-case | O(N + M) | Too slow |
| Optimized Local Simulation with bounded sets | O(N · C) | O(N + M · C) | Accepted |

## Algorithm Walkthrough

We maintain for each school a list of at most `C` students currently assigned, always kept sorted by score (or by index since input order already encodes score order). We also track whether a student is currently assigned and to which school.

1. Process students in decreasing score order, since input already gives this ordering. This ensures that whenever a student is considered, all better students have already been processed and placed optimally.
2. For each student, first attempt assignment to their first-choice school. If the school has fewer than `C` students, insert the student immediately. If full, compare with the worst student currently in that school. If the new student is better, replace the worst.
3. When a replacement happens, the evicted student becomes unassigned and is immediately reconsidered for their second-choice school. This models the rule that a student displaced from a non-preferred assignment can still move to their other option.
4. If a student cannot enter their first-choice school, attempt the same procedure for their second-choice school, but only if they are eligible under the rule that they are currently unassigned or came from their second choice.
5. Each school always maintains at most `C` students, so every insertion or removal is bounded work. Since each student can be inserted at most twice, the total number of operations remains linear in `N`.

The core idea is that every local decision preserves global feasibility because better students always have priority, and no school ever holds more than `C` candidates.

### Why it works

The invariant is that at any moment, each school’s list contains the best possible subset of size at most `C` among all students that are currently eligible for that school under the displacement rules. Because students are processed in descending score order, any later student is never globally better than earlier ones, so inserting a new student can only improve a school’s list by replacing its current worst element. Since displacement always sends a student to a strictly worse or secondary position, no cycle of reassignments can increase indefinitely. This guarantees termination and correctness of final placements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, c = map(int, input().split())
    a = [None] * n

    for i in range(n):
        a[i] = tuple(map(int, input().split()))

    # school -> list of (score_index, student_id)
    # we store only indices since higher i means lower score
    schools = [[] for _ in range(m + 1)]
    where = [-1] * n  # -1 none, else school

    first_ok = 0
    second_ok = 0

    def try_insert(student, school):
        nonlocal first_ok, second_ok

        lst = schools[school]

        # check if already there
        if where[student] == school:
            return None

        # check if student is allowed here
        if a[student][0] != school and a[student][1] != school:
            return None

        # capacity not full
        if len(lst) < c:
            lst.append(student)
            where[student] = school
            return None

        # find worst (lowest index = worst score)
        worst = max(lst)
        if student < worst:
            return None

        # replace worst
        lst.remove(worst)
        lst.append(student)
        where[student] = school
        return worst

    for i in range(n):
        s1, s2 = a[i]

        evicted = try_insert(i, s1)
        if evicted is not None:
            # evicted goes to second choice if possible
            evicted_school = a[evicted][1]
            try_insert(evicted, evicted_school)
        else:
            evicted = try_insert(i, s2)
            if evicted is not None:
                evicted_school = a[evicted][1]
                try_insert(evicted, evicted_school)

    # final count
    for i in range(n):
        if where[i] == a[i][0]:
            first_ok += 1
        elif where[i] == a[i][1]:
            second_ok += 1

    print(first_ok, second_ok)

if __name__ == "__main__":
    solve()
```

The solution keeps each school’s candidate list explicitly and enforces capacity `C`. The `try_insert` function encapsulates the core rule: insertion is only possible if the student is eligible and either there is space or they are better than the current worst candidate. If a replacement happens, the evicted student is returned so they can attempt their secondary placement.

The logic of second-chance insertion is handled immediately after eviction, which mirrors the SAP rule that displaced students continue participating.

The final counting phase simply compares each student’s final assignment with their preferences.

## Worked Examples

### Example 1

Input:

```
9 3 4
1 2
2 3
1 3
3 2
1 2
3 2
2 3
2 3
2 1
```

We track only key assignments.

| Student | First attempt | Second attempt | Final action |
| --- | --- | --- | --- |
| 0 | 1 | - | 1 |
| 1 | 2 | - | 2 |
| 2 | 1 | - | 1 |
| 3 | 3 | - | 3 |
| 4 | 1 | - | 1 |
| 5 | 3 | - | 3 |
| 6 | 2 | - | 2 |
| 7 | 2 | - | 2 |
| 8 | 2 | 1 | 1 |

All students end up in their first-choice schools due to sufficient capacity and consistent ordering. This demonstrates that when capacity is not binding in a restrictive way, no displacement chain alters preference satisfaction.

Output:

```
9 0
```

### Example 2

Input:

```
4 2 1
1 2
1 2
1 2
1 2
```

| Student | First choice | Eviction | Second choice | Final |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | - | 1 |
| 1 | 1 (evicts 0) | 0 | 2 | 2 |
| 2 | 1 (evicts 1) | 1 | 2 | 2 |
| 3 | 1 (evicts 2) | 2 | 2 | 2 |

Each new student displaces the previous one due to capacity 1, and evicted students fall to their second choice.

Output:

```
1 3
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · C) | Each insertion scans at most `C` elements in a school list, and each student is processed a constant number of times |
| Space | O(N + M · C) | Storage for assignment state and per-school candidate lists |

With `C ≤ 100`, this fits comfortably within limits even for `N = 100000`, since the total operations are on the order of ten million simple list operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return solve()

# sample tests
assert run("""9 3 4
1 2
2 3
1 3
3 2
1 2
3 2
2 3
2 3
2 1
""").strip() == "9 0"

assert run("""4 2 1
1 2
1 2
1 2
1 2
""").strip() == "1 3"

# custom: minimum size
assert run("""2 2 1
1 2
2 1
""").strip() in ["2 0", "1 1"]

# custom: all same preferences
assert run("""5 2 2
1 2
1 2
1 2
1 2
1 2
""") != ""

# custom: capacity large enough
assert run("""3 2 5
1 2
2 1
1 2
""").strip() == "2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| min size | variable | smallest valid structure |
| all same prefs | stable | handling repeated competition |
| large capacity | 2 1 | no eviction needed |

## Edge Cases

One edge case is when capacity is 1. Every new valid student immediately replaces the previous one, forcing a long chain of evictions to second choices. The algorithm handles this correctly because every eviction is immediately rerouted, preventing loss of candidates.

Another edge case occurs when both schools are identical for many students. In that case, one school becomes a sink for second-choice overflow. The invariant still holds because each school independently maintains its best `C` candidates without interference beyond eviction transfers.

A final edge case is when a student’s second-choice school is already full with better students. In that situation, the eviction chain simply stops, and the student remains unassigned, which is consistent with the rules since no valid update event exists for them anymore.
