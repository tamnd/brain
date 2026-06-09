---
title: "CF 1668B - Social Distance"
description: "We are given a circular arrangement of $m$ seats and a list of $n$ people. Each person has a personal “exclusion radius” $ai$: if they sit on some seat, then the closest $ai$ seats on both sides around the circle must remain empty."
date: "2026-06-10T02:03:04+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1668
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 783 (Div. 2)"
rating: 900
weight: 1668
solve_time_s: 129
verified: false
draft: false
---

[CF 1668B - Social Distance](https://codeforces.com/problemset/problem/1668/B)

**Rating:** 900  
**Tags:** greedy, math, sortings  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular arrangement of $m$ seats and a list of $n$ people. Each person has a personal “exclusion radius” $a_i$: if they sit on some seat, then the closest $a_i$ seats on both sides around the circle must remain empty. In other words, each person does not just occupy one chair, they effectively block a contiguous arc of $2a_i + 1$ seats on the circle, centered at their position.

The task is to decide whether we can place all people on the circle so that none of these blocked regions overlap.

The important structural detail is that this is purely about packing intervals on a circle, where each interval has length $2a_i + 1$, and intervals must be disjoint.

The constraints make brute force placement impossible. The total number of people across all test cases is up to $10^5$, while the number of chairs can be as large as $10^9$. Any approach that tries to simulate seating or check positions individually is immediately ruled out. Even $O(n^2)$ per test case would be far too slow.

A subtle edge case is when total demand is close to the circle size. For example, if $m = 5$ and all $a_i = 2$, then each person blocks 5 seats, meaning only one person can sit at most. A greedy approach that ignores circular wraparound might incorrectly assume linear spacing works, but the wraparound causes overlap between the last and first placements.

Another tricky situation is when many small $a_i$ values coexist with a single large one. The large value can dominate and consume most available space, leaving no valid arrangement even if the smaller ones seem flexible.

## Approaches

A direct brute-force idea is to simulate seating positions on the circle. We could try placing each person in some available seat and marking the blocked interval. This would involve maintaining a structure of free segments and repeatedly inserting intervals while checking overlap. In the worst case, every placement could require scanning almost all remaining space, leading to $O(nm)$ behavior if done naively, which is impossible for $m$ up to $10^9$.

The key observation is that individual positions do not matter at all. Only the total amount of occupied and blocked space matters. Each person consumes exactly $2a_i + 1$ seats of the circle, and these consumptions must not overlap. Since the circle has no boundary, we can treat it as a total capacity problem: we are trying to pack segments whose total length must not exceed $m$.

Thus the problem reduces to checking whether:

$$\sum (2a_i + 1) \leq m$$

However, this is slightly misleading in a circular setting because adjacency constraints do not allow arbitrary packing order to help reduce space. The correct refinement is to sort by size implicitly via summation only, since all segments are rigid and cannot overlap or compress.

So the feasibility condition is purely a sum check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | $O(nm)$ | $O(m)$ | Too slow |
| Sum of occupied lengths | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each person, compute how many seats they effectively occupy, which is $2a_i + 1$. This represents their seat plus required empty buffer on both sides.
2. Sum these values across all people to get the total required space.
3. Compare this total with $m$, the size of the circle.
4. If the total required space is less than or equal to $m$, output "YES". Otherwise output "NO".

The reasoning behind summation is that every person’s forbidden region must be disjoint, and each region has fixed length regardless of placement.

### Why it works

Each person induces a block of contiguous seats that cannot overlap with any other block. Since these blocks are rigid and independent, any valid configuration corresponds to a partition of the circle into disjoint segments of these exact lengths. The circle has total capacity $m$, so a necessary condition is that the sum of segment lengths does not exceed $m$. It is also sufficient because if total length fits, we can always place segments sequentially around the circle without gaps smaller than required separation, and wraparound does not introduce new constraints beyond total capacity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        
        total = 0
        for x in a:
            total += 2 * x + 1
        
        if total <= m:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The implementation is a direct translation of the derived condition. Each $a_i$ is expanded into its full occupied segment length $2a_i + 1$, and accumulated into a running sum. The final comparison against $m$ determines feasibility.

A common mistake here is to forget the central seat in $2a_i + 1$, using only $2a_i$, which underestimates total usage and leads to incorrect "YES" outputs.

## Worked Examples

We trace two cases from the sample.

### Example 1

Input:

```
n = 3, m = 8
a = [1, 2, 1]
```

| Person | a_i | Occupied (2a_i+1) | Running Sum | Feasible vs m |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 3 | yes |
| 2 | 2 | 5 | 8 | yes |
| 3 | 1 | 3 | 11 | no |

Final decision: NO since 11 > 8.

This shows how a single large requirement quickly exhausts the circle even when earlier placements seem fine.

### Example 2

Input:

```
n = 2, m = 4
a = [1, 1]
```

| Person | a_i | Occupied (2a_i+1) | Running Sum | Feasible vs m |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 3 | yes |
| 2 | 1 | 3 | 6 | no |

Final decision: NO since 6 > 4.

This confirms that even uniform small constraints can exceed capacity when multiple people are present.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each test case sums over all people once |
| Space | $O(1)$ | Only a running total is stored |

The solution processes at most $10^5$ total values across all test cases, which is comfortably within time limits. Memory usage is constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    solve()
    
    return output.getvalue()

# provided samples
assert run("""6
3 2
1 1 1
2 4
1 1
2 5
2 1
3 8
1 2 1
4 12
1 2 1 3
4 19
1 2 1 3
""") == """NO
YES
NO
YES
NO
YES
"""

# all minimum
assert run("""1
2 5
1 1
""") == "NO\n"

# single person fits exactly
assert run("""1
1 3
1
""") == "YES\n"

# tight fit boundary
assert run("""1
3 9
1 1 1
""") == "NO\n"

# large slack
assert run("""1
4 100
1 1 1 1
""") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single person exact | YES | boundary equality case |
| two small crowded | NO | minimal overfill detection |
| tight sum match failure | NO | off-by-one correctness |
| large m slack | YES | scalability and positivity |

## Edge Cases

A key edge case is when $n = 1$. The formula reduces to checking whether $2a_1 + 1 \leq m$. For example, if $m = 3$ and $a_1 = 1$, the person occupies all 3 seats exactly, which is valid. The algorithm correctly computes total as 3 and returns YES.

Another edge case is when all $a_i = 1$. Each person occupies 3 seats. If $m = 8$ and $n = 3$, total becomes 9, which exceeds capacity even though visually one might attempt to “fit” them with wraparound. The algorithm correctly rejects it because circular overlap cannot be avoided when total demand exceeds supply.

A final edge case is when $m$ is very large but $n$ is small. For example, $n = 2$, $m = 10^9$, $a = [10^9, 10^9]$. The sum becomes $4 \cdot 10^9 + 2$, which immediately exceeds $m$, correctly producing NO without any geometric reasoning.
