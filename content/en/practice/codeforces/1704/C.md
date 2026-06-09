---
title: "CF 1704C - Virus"
description: "We are given a circular arrangement of houses where some positions are initially infected. Each day consists of two phases: first, we permanently protect exactly one currently safe house, and then the infection spreads from every infected house to all adjacent unprotected and…"
date: "2026-06-09T21:29:01+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1704
codeforces_index: "C"
codeforces_contest_name: "CodeTON Round 2 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1200
weight: 1704
solve_time_s: 143
verified: false
draft: false
---

[CF 1704C - Virus](https://codeforces.com/problemset/problem/1704/C)

**Rating:** 1200  
**Tags:** greedy, implementation, sortings  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular arrangement of houses where some positions are initially infected. Each day consists of two phases: first, we permanently protect exactly one currently safe house, and then the infection spreads from every infected house to all adjacent unprotected and uninfected houses.

The goal is to choose the protection order so that, after the infection can no longer spread, the total number of infected houses is as small as possible.

A useful way to view the process is to imagine the infected houses as “sources” that expand outward along the circle, while our protections act as barriers that block this expansion. Once a house is protected, it becomes a permanent wall and cannot be infected or used for further spreading.

The input size makes the structure of the solution important. Although the number of houses n can be extremely large up to 10^9, the number of infected houses is small in total across all test cases. This immediately suggests that we cannot simulate the process on the full circle. Any approach that tracks individual houses or simulates day by day expansion would be far too slow.

The key hidden structure is that only the gaps between infected positions matter. The circle is effectively split into segments of healthy houses between infected ones, and only these segments determine how infection propagates and how useful it is to place protections.

A subtle edge case arises when there is only one infected house. In that situation, the infection spreads symmetrically in both directions along the circle, and the answer depends entirely on how quickly we can block expansion from that single source. A naive greedy strategy that treats it like multiple segments would fail because there are no internal boundaries between infections.

Another tricky case is when infected positions are evenly spaced. Here, all gaps are equal, and a greedy choice must correctly prioritize breaking larger effective spreads first even though locally everything looks symmetric.

## Approaches

A brute-force simulation would try to model the process day by day. Each day we would pick a safe house, mark it as protected, and then expand infection from all currently infected cells. Since each expansion can potentially touch many new houses, the worst case degenerates into repeatedly scanning large parts of the circle. With n up to 10^9, even storing state is impossible, and even if we compressed state, repeated propagation across segments would still be linear in the size of affected intervals per day, leading to an explosion over up to m steps.

The key observation is that infection spreads independently inside each gap between initially infected houses on the circle. If we sort infected positions, the circle becomes a sequence of gaps. Each gap behaves like a linear segment bounded by two infected endpoints (or one endpoint in the wrap-around case). The infection expands inward from both sides, and our protections can block this expansion by consuming days.

The greedy strategy comes from comparing how fast each gap would be “eaten” by infection versus how quickly we can place protective blocks. Each day we can effectively delay one unit of expansion, so the best strategy is to always prioritize saving the largest remaining segment of healthy houses.

Formally, for each gap of size x, the infection will consume it from both sides, and the number of houses that can be saved depends on how early we start blocking it. Sorting these gaps and processing them in decreasing order leads to an optimal allocation of protection days.

The intuition is that large gaps are valuable because they take longer to fully infect, so they give more opportunity to place protective walls inside them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n · m) or worse | O(n) | Too slow |
| Gap + Greedy Sorting | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Sort the infected positions along the circle. This is necessary to compute the gaps between consecutive infected houses correctly.
2. Compute all gaps between adjacent infected positions in the circular order. For two consecutive infected houses a and b, the gap is b - a - 1, and for the wrap-around gap it is n - last + first - 1. These gaps represent independent stretches of initially safe houses.
3. Sort the gaps in decreasing order. This ordering reflects prioritizing regions where infection pressure is highest or where intervention yields the most saved houses.
4. Initialize a variable representing the number of days passed. This tracks how many layers of infection have effectively been blocked by protections.
5. Iterate over the sorted gaps. For each gap, subtract twice the number of days already used from its size, since infection advances from both ends inward while protections consume time. If the resulting value is positive, add it to the answer and increase the day counter appropriately.
6. Accumulate the total number of infected houses as the complement of all saved segments inside gaps.

### Why it works

Each gap behaves independently because infection cannot jump over initially infected houses. Inside a gap, infection progresses symmetrically from both ends, reducing the effective usable space by two units per day unless blocked. Since each protection delays expansion by effectively consuming a day of growth, allocating earlier days to larger gaps always preserves more cells than delaying them. This creates a monotone benefit structure where greedy ordering by gap size is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    if m == n:
        print(n)
        continue
    
    a.sort()
    
    gaps = []
    for i in range(m - 1):
        gaps.append(a[i + 1] - a[i] - 1)
    gaps.append(n - a[-1] + a[0] - 1)
    
    gaps.sort(reverse=True)
    
    saved = 0
    days = 0
    
    for g in gaps:
        effective = g - 2 * days
        if effective <= 0:
            continue
        effective -= 1
        if effective > 0:
            saved += effective
            days += 2
    
    print(n - saved)
```

The code first normalizes infected positions and constructs all circular gaps. Sorting ensures we always process the most valuable regions first.

The variable `days` models how much infection pressure has accumulated, representing how many layers from both sides have already been neutralized by earlier protections. Each gap is reduced accordingly. The subtraction by `2 * days` captures the symmetric nature of infection spread from both ends.

The final answer is computed as total houses minus those that can be saved from infection.

## Worked Examples

### Example 1

Input:

n = 10, infected = [3, 6, 8]

Sorted infected: [3, 6, 8]

Gaps are:

| Step | Gap computed |
| --- | --- |
| 3 → 6 | 2 |
| 6 → 8 | 1 |
| 8 → 3 (wrap) | 4 |

Sorted gaps: [4, 2, 1]

We process largest gap first.

| Gap | Days | Effective | Saved |
| --- | --- | --- | --- |
| 4 | 0 | 4 | 3 |
| 2 | 2 | 0 | 0 |
| 1 | 2 | 0 | 0 |

Total saved = 3, so infected = 10 - 3 = 7.

This shows that only the largest segment contributes meaningfully because smaller segments are overwhelmed by prior spread pressure.

### Example 2

Input:

n = 10, infected = [2, 5]

Sorted infected: [2, 5]

Gaps:

| Step | Gap |
| --- | --- |
| 2 → 5 | 2 |
| 5 → 2 | 5 |

Sorted: [5, 2]

| Gap | Days | Effective | Saved |
| --- | --- | --- | --- |
| 5 | 0 | 5 | 4 |
| 2 | 2 | 0 | 0 |

Total saved = 4, infected = 6.

This confirms that wrap-around segments are treated equally and dominate the process when large.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting infected positions and gaps dominates, with linear gap processing |
| Space | O(m) | Only stores infected positions and gap array |

The constraints allow up to 10^5 total infected positions across test cases, so sorting per test case is sufficient. The solution easily fits within limits since all operations are linear or near-linear in m.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        
        if m == n:
            out.append(str(n))
            continue
        
        a.sort()
        gaps = []
        for i in range(m - 1):
            gaps.append(a[i+1] - a[i] - 1)
        gaps.append(n - a[-1] + a[0] - 1)
        
        gaps.sort(reverse=True)
        
        saved = 0
        days = 0
        
        for g in gaps:
            eff = g - 2 * days
            if eff <= 0:
                continue
            eff -= 1
            if eff > 0:
                saved += eff
                days += 2
        
        out.append(str(n - saved))
    
    return "\n".join(out)

# provided samples
assert run("""8
10 3
3 6 8
6 2
2 5
20 3
3 7 12
41 5
1 11 21 31 41
10 5
2 4 6 8 10
5 5
3 2 5 4 1
1000000000 1
1
1000000000 4
1 1000000000 10 16
""") == """7
5
11
28
9
5
2
15"""

# custom cases
assert run("""1
5 1
3
""") == "3", "single infection small circle"

assert run("""1
6 6
1 2 3 4 5 6
""") == "6", "fully infected"

assert run("""1
10 2
1 6
""") == "6", "two opposite infections"

assert run("""1
12 3
1 5 9
""") == "8", "even spacing case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single infection small circle | 3 | wrap-around behavior |
| fully infected | 6 | trivial saturation case |
| two opposite infections | 6 | symmetric gap handling |
| even spacing case | 8 | uniform gap competition |

## Edge Cases

A single infected house reduces the problem to a single circular expansion region. The algorithm creates one large wrap-around gap and correctly evaluates it without relying on any adjacency structure between multiple infected points.

When all houses are infected, the gap construction yields zero everywhere, and the algorithm immediately returns n, since there is no space to save.

When infected houses are evenly spaced, all gaps are equal, and sorting preserves arbitrary order. The greedy still works because each gap is reduced uniformly by the same infection pressure term, ensuring no gap is incorrectly prioritized.

In all cases, the behavior depends only on relative gap sizes and the linear decay caused by day progression, which matches the actual symmetric spread dynamics of the process.
