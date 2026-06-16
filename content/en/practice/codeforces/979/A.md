---
title: "CF 979A - Pizza, Pizza, Pizza!!!"
description: "We are given a number of friends attending a pizza party, and the host must divide a circular pizza into exactly equal slices so that there are one slice per person, including the host. If there are $n$ friends, the pizza must be split into $n + 1$ equal parts."
date: "2026-06-17T01:18:45+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 979
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 482 (Div. 2)"
rating: 1000
weight: 979
solve_time_s: 66
verified: true
draft: false
---

[CF 979A - Pizza, Pizza, Pizza!!!](https://codeforces.com/problemset/problem/979/A)

**Rating:** 1000  
**Tags:** math  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number of friends attending a pizza party, and the host must divide a circular pizza into exactly equal slices so that there are one slice per person, including the host. If there are $n$ friends, the pizza must be split into $n + 1$ equal parts.

The operation allowed is a straight cut across the pizza, and each cut contributes to forming these equal sectors. The goal is to minimize how many such straight cuts are required to produce $n + 1$ identical slices.

The input is a single integer $n$, potentially as large as $10^{18}$, which immediately rules out any approach that simulates cuts or builds geometry explicitly. Any solution must reduce the problem to a direct mathematical computation.

A few edge cases reveal the structure of the problem. When $n = 0$, there is only one person, so no cut is needed. When $n = 3$, we need 4 equal slices, which requires 2 straight cuts through the center. When $n = 4$, we need 5 equal slices, and the sample suggests 5 cuts, indicating that parity or divisibility properties matter. A naive assumption that each cut always increases the number of slices by a fixed amount would fail, because cuts behave differently depending on whether they intersect the center and how they are arranged.

## Approaches

A brute-force interpretation would try to simulate placing straight cuts and tracking how many regions the circle is divided into. Each new cut can intersect all previous cuts, increasing the number of slices in a nontrivial way. One could attempt to model this incrementally: start with one piece, then try all possible orientations of cuts, and count how many regions are formed.

The problem is that each cut can intersect all previous cuts, so after $k$ cuts, the number of pieces can grow quadratically with respect to $k$. Trying to simulate or search for the minimum configuration that yields exactly $n + 1$ equal angular sectors quickly becomes intractable, especially since $n$ can be up to $10^{18}$.

The key observation is that we are not actually optimizing geometry in a continuous sense, but instead matching a very rigid combinatorial structure: equal angular partitions of a circle. The only meaningful configurations come from either drawing diameters through the center or using a special construction where all cuts are arranged symmetrically like spokes of a wheel. This reduces the problem to asking how many symmetric straight cuts are needed to form $n + 1$ equal angles around a circle.

From this structure, the answer reduces to a simple parity rule. If $n + 1$ is odd, we cannot pair slices symmetrically using diametrical cuts, so we must draw a full set of radial cuts, one per sector. If $n + 1$ is even, each straight line through the center produces two opposite slices, so each cut contributes more efficiently.

This leads to a direct formula based on whether $n + 1$ is even or odd, which simplifies further to checking whether $n$ is even or odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(1) | Too slow |
| Parity-based formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$, which represents the number of friends.
2. Compute $k = n + 1$, the number of equal pizza slices required.
3. If $n = 0$, output 0 immediately because a single slice needs no cuts.
4. If $k = 2$, output 1 because one straight diameter cut divides the pizza into exactly two equal halves.
5. If $k$ is even, output $k // 2$, since each diameter-like cut produces two equal opposite slices.
6. If $k$ is odd and greater than 1, output $k$, since each slice must be formed independently by a radial boundary.

The reasoning behind the even case comes from symmetry: a straight line through the center always produces exactly two equal halves, and multiple such lines can be arranged to partition the circle into pairs of opposite sectors. When the number of sectors is even, this pairing structure fits perfectly. When it is odd, one cannot pair all sectors, forcing a degenerate configuration where each sector boundary must be explicitly introduced.

### Why it works

The circle can only be partitioned into equal angular regions using straight lines in configurations that respect rotational symmetry. A straight cut always introduces a line of symmetry that divides existing angular regions in pairs. This means that valid constructions must align with pairing structure around the center. When the number of required slices is even, every slice can be paired with an opposite slice, so each cut contributes maximally. When it is odd, no complete pairing exists, so the construction degenerates into one cut per boundary direction, forcing linear growth.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
k = n + 1

if k == 1:
    print(0)
elif k == 2:
    print(1)
elif k % 2 == 0:
    print(k // 2)
else:
    print(k)
```

The code directly implements the parity-based rule derived above. The first two conditions handle trivial cases where no geometric reasoning is needed. The even-case branch encodes the pairing argument, while the odd-case branch reflects the lack of symmetry, forcing one cut per slice boundary direction.

Care must be taken with the $k = 1$ case, since no cut is needed when there is only one slice. Another subtlety is distinguishing $k = 2$ from the general even case, since the formula $k // 2$ would otherwise incorrectly suggest a fractional reasoning if misapplied without interpretation.

## Worked Examples

### Example 1: $n = 3$

We need $k = 4$ slices.

| Step | n | k = n+1 | parity | decision |
| --- | --- | --- | --- | --- |
| 1 | 3 | 4 | even | output k/2 = 2 |

This matches the idea of two perpendicular cuts through the center forming four equal quadrants.

### Example 2: $n = 4$

We need $k = 5$ slices.

| Step | n | k = n+1 | parity | decision |
| --- | --- | --- | --- | --- |
| 1 | 4 | 5 | odd | output k = 5 |

This reflects that a symmetric pairing is impossible, so each sector boundary must be independently introduced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic and a few conditional checks are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within constraints since it performs constant-time computation even for values up to $10^{18}$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline
    n = int(input().strip())
    k = n + 1

    if k == 1:
        return "0"
    elif k == 2:
        return "1"
    elif k % 2 == 0:
        return str(k // 2)
    else:
        return str(k)

# provided sample
assert run("3\n") == "2"

# custom cases
assert run("0\n") == "0", "single person needs no cut"
assert run("1\n") == "1", "two slices require one cut"
assert run("2\n") == "3", "odd slice count behavior"
assert run("999999999999999999\n") == str(500000000000000000), "large even k case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | minimum edge case |
| 1 | 1 | smallest non-trivial cut |
| 2 | 3 | odd structure behavior |
| large n | k//2 | performance and overflow safety |

## Edge Cases

For $n = 0$, we have $k = 1$. The algorithm immediately returns 0, which corresponds to no cuts needed for a single slice.

For $n = 1$, we have $k = 2$. The condition explicitly returns 1, matching a single straight diameter cut.

For large even values, such as $n = 10^{18} - 1$, the computation reduces to integer division of $k$ by 2, which remains safe in Python due to arbitrary precision integers.

For odd values like $n = 4$, where $k = 5$, the fallback branch returns $k$, reflecting that no pairing structure exists and each slice direction must be independently realized.
