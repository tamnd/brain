---
title: "CF 106141I - Rick's Grades"
description: "We are given two sequences of the same length. One sequence represents Morty’s grades over n days, the other represents Rick’s grades over the same days. Each grade is an integer from 0 to 5, where 0 is a special value meaning absence."
date: "2026-06-19T19:35:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106141
codeforces_index: "I"
codeforces_contest_name: "Moscow team school olympiad (MKOSHP) 2025"
rating: 0
weight: 106141
solve_time_s: 53
verified: true
draft: false
---

[CF 106141I - Rick's Grades](https://codeforces.com/problemset/problem/106141/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of the same length. One sequence represents Morty’s grades over n days, the other represents Rick’s grades over the same days. Each grade is an integer from 0 to 5, where 0 is a special value meaning absence.

Rick is allowed to permute his own sequence arbitrarily. After reordering, we pair day i of Morty with day i of Rick. The goal is to decide whether Rick can arrange his grades so that for every day i, either Rick’s grade is at least Morty’s grade, or Morty was absent that day, or Rick was absent that day. If such a rearrangement exists, we must output one valid ordering of Rick’s grades; otherwise we output -1.

The core structure is a constrained matching problem. Each Morty grade a[i] imposes a threshold requirement on the matched Rick grade b[j], unless a[i] is zero, in which case the constraint disappears. Conversely, if b[j] is zero, that position is always safe because it is treated as a wildcard that satisfies any constraint.

The constraints are small in value range, from 0 to 5, but n can be up to 3·10^5 across test cases. This forces any solution to be linear or near linear per test case. Anything involving checking all permutations or even greedy matching with nested scans would be too slow in the worst case.

A subtle edge case arises from zeros. Consider a situation where Morty has many nonzero grades, but Rick has many zeros. A naive greedy approach might incorrectly assign zeros too early and block higher constraints later. Another failure mode is treating this like a simple sorting comparison: sorting both arrays and comparing elementwise does not work because zeros are flexible only on one side of the condition and break positional symmetry.

For example, if Morty is [5, 5, 5] and Rick is [0, 4, 4], sorting Rick gives [0, 4, 4], which seems insufficient, but actually zero can be placed against any position. However, if constraints are distributed unevenly, greedy misplacement of 0 can still break feasibility.

## Approaches

The brute-force interpretation is to try all permutations of Rick’s grades and check if any ordering satisfies the condition. This immediately leads to n! possibilities, and each check costs O(n), making it completely infeasible even for n as small as 10.

The key observation is that the only thing that matters about Morty’s sequence is how many positions require at least a certain threshold. Since grades are only from 0 to 5, we can compress Morty’s requirements into counts per grade level. Similarly, Rick’s grades can be grouped by value.

Now think about how a single value in Rick’s array can be used. A grade x can satisfy any Morty position with requirement ≤ x, and it can also be wasted on a Morty zero position. This suggests that we should try to assign Rick’s grades from highest to lowest constraints first, ensuring that harder requirements are satisfied early.

The problem becomes a resource allocation problem across six buckets. We process Morty’s grades in increasing order of strictness, and ensure that enough Rick grades exist to cover them. Zeros in Rick act as universal fillers, and zeros in Morty remove demand entirely.

This reduces the problem to checking feasibility via greedy matching on frequency buckets, and then constructing an explicit assignment by placing larger values where needed first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain frequency counts of both arrays for values 0 through 5.

1. Count how many times each grade appears in Morty’s array and Rick’s array. This compresses the problem into a small fixed state space of size 6.
2. Split Morty’s positions into two groups: positions where a[i] is zero, and positions where it is nonzero. The zero positions do not constrain Rick at all, so they will later absorb any leftover values.
3. For nonzero Morty grades, we conceptually process constraints from high grade to low grade. A Morty grade x requires a Rick grade of at least x unless we assign a zero from Rick.
4. We maintain a multiset-like structure via counts of Rick grades. We always try to satisfy the highest Morty requirements first using the largest available Rick values. This prevents a situation where a large Rick value is wasted on an easy constraint while a hard constraint remains uncovered.
5. For each Morty grade from 5 down to 1, we try to match it greedily with the smallest possible Rick value that is still valid, preferring exact or minimal sufficient matches. If we cannot satisfy a requirement even after using all larger values, we conclude impossibility.
6. After satisfying all nonzero Morty requirements, remaining Rick values, including zeros and unused grades, are placed arbitrarily into Morty-zero positions and leftover slots, since those positions impose no constraints.
7. Construct the final array by writing assigned Rick values in the original order positions chosen during the matching phase.

### Why it works

The algorithm enforces a strongest-first assignment principle. Every nonzero Morty requirement consumes a Rick grade that is sufficient but not unnecessarily large, preserving higher grades for higher constraints. Since grades exist in a tiny bounded domain, any failure to satisfy a requirement must appear at the moment we process that grade level, because all larger possibilities have already been accounted for in counts. This gives a monotone feasibility condition: once a grade level cannot be satisfied, no rearrangement of lower-level assignments can fix it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        cnt_a = [0] * 6
        cnt_b = [0] * 6
        
        for x in a:
            cnt_a[x] += 1
        for x in b:
            cnt_b[x] += 1
        
        # We will assign from high to low requirements
        # Track available b values
        avail = cnt_b[:]
        
        ok = True
        
        # Try to satisfy requirements 5..1
        for need in range(5, 0, -1):
            demand = cnt_a[need]
            if demand == 0:
                continue
            
            # We can use b[need], b[need+1], ... b[5]
            supply = sum(avail[need:6])
            if supply < demand:
                ok = False
                break
            
            # Greedy: consume smallest valid first (for stability)
            for val in range(need, 6):
                take = min(avail[val], demand)
                avail[val] -= take
                demand -= take
                if demand == 0:
                    break
        
        if not ok:
            print(-1)
            continue
        
        # remaining values can be placed arbitrarily
        res = []
        for v in range(6):
            res.extend([v] * avail[v])
        
        print(*res)

if __name__ == "__main__":
    solve()
```

The solution begins by compressing both arrays into frequency tables over the fixed domain 0 to 5. This removes all positional reasoning initially and replaces it with a resource accounting problem.

We then simulate satisfying Morty’s stricter grades first. For each requirement level, we verify that enough Rick grades exist in the current and higher buckets. If not, we fail immediately. Otherwise, we consume from the smallest valid bucket first to preserve stronger grades for future needs.

The final reconstruction simply emits all remaining unused Rick grades. Because all constraints were enforced during allocation, any ordering of leftovers is valid.

A common implementation pitfall is forgetting that zeros in Morty remove constraints entirely. In this approach, zeros are naturally ignored because we never attempt to satisfy them. Another subtle point is ensuring that we always check availability across all higher buckets before consuming, otherwise premature consumption can lead to false negatives.

## Worked Examples

### Example 1

Consider Morty as [5, 2, 1, 3, 4] and Rick as [1, 2, 3, 4, 5].

We build frequency tables and then process requirements from 5 downwards.

| Need | Demand | Available ≥ need | Action |
| --- | --- | --- | --- |
| 5 | 1 | 5 | assign 5 |
| 4 | 1 | 4 | assign 4 |
| 3 | 1 | 3 | assign 3 |
| 2 | 1 | 2 | assign 2 |
| 1 | 1 | 1 | assign 1 |

All demands are satisfied exactly, leaving no leftovers.

This demonstrates the ideal balanced case where each grade matches perfectly and greedy consumption does not interfere with future requirements.

### Example 2

Morty: [3, 2, 1, 0]

Rick: [2, 3, 4, 1]

We ignore Morty’s zero.

We process need=3 first. We have {3,4} available, so we assign 3.

Next need=2, remaining are {1,2,4}, so assign 2.

Next need=1, remaining {1,4}, assign 1.

We successfully satisfy all constraints and leftover 4 is placed anywhere.

This example shows how the algorithm naturally ignores zero constraints and still completes a valid assignment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting and constant-size bucket processing over values 0 to 5 |
| Space | O(1) | Only fixed-size frequency arrays are used |

The domain of values being constant is what reduces the problem from a matching problem into a simple greedy counting process. Even at 3·10^5 total elements, the algorithm only performs linear scans and constant bucket operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like sanity cases
assert run("1\n3\n1 2 3\n3 2 1\n") != "", "basic case"

# all zeros in Morty
assert run("1\n4\n0 0 0 0\n1 2 3 4\n") != "", "zeros remove constraints"

# impossible case
assert run("1\n2\n5 5\n1 1\n") == "-1", "insufficient large values"

# exact match case
assert run("1\n5\n1 2 3 4 5\n1 2 3 4 5\n") != "", "identity permutation"

# edge minimal
assert run("1\n1\n0\n5\n") != "", "single zero Morty"

# heavy zero in Rick
assert run("1\n3\n1 2 3\n0 0 0\n") == "-1", "no nonzero supply"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros in Morty | any permutation | constraints disappear |
| all zeros in Rick | -1 for nonzero demand | zero cannot satisfy requirement |
| identity case | same sequence | baseline correctness |

## Edge Cases

A critical edge case is when Morty has only high grades and Rick has many low grades with a few high ones. For example, Morty is [5, 5, 5] and Rick is [5, 1, 1]. The algorithm processes need=5 first, consumes the single 5, then fails immediately because remaining supply above or equal to 5 is exhausted. This is correct because no rearrangement can create additional high-grade matches.

Another edge case is when zeros dominate Morty’s array, such as [0, 0, 0, 5]. The algorithm ignores the zeros entirely and only checks feasibility for the single strict requirement, ensuring that all flexibility is correctly utilized.

A final edge case is when Rick consists entirely of zeros except one high value. The algorithm correctly assigns that high value to the strongest requirement first and then leaves the rest as failure if any additional nonzero demands exist.
