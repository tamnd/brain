---
title: "CF 1468N - Waste Sorting"
description: "Monocarp needs to throw away several items of different types into three containers with fixed capacities. The first container accepts only paper items, the second only plastic, and the third all other types."
date: "2026-06-11T01:33:25+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1468
codeforces_index: "N"
codeforces_contest_name: "2020-2021 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules)"
rating: 900
weight: 1468
solve_time_s: 109
verified: true
draft: false
---

[CF 1468N - Waste Sorting](https://codeforces.com/problemset/problem/1468/N)

**Rating:** 900  
**Tags:** greedy, implementation  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

Monocarp needs to throw away several items of different types into three containers with fixed capacities. The first container accepts only paper items, the second only plastic, and the third all other types. Monocarp has some items that are strictly paper, strictly plastic, or strictly other, but he also has items that are partially paper or partially plastic, which can go either into their respective primary container or into the third container. The question is whether all items can fit without exceeding any container's capacity.

The input gives multiple test cases. Each test case specifies the capacities of the three containers and the counts of each type of item Monocarp has. The output is YES if it is possible to place all items respecting the capacities, otherwise NO.

The constraints allow up to $3 \cdot 10^4$ test cases, and each value can be as large as $10^8$. This rules out any solution that tries to enumerate combinations of partial items because the number of possibilities could be astronomical. The solution must rely on arithmetic checks and simple comparisons.

An edge case arises when a container's capacity is smaller than the mandatory items for that container. For example, if the paper container can hold only 1 item but Monocarp has 2 strict paper items, no distribution of partially-paper items can compensate. Another subtle scenario occurs when partially-paper or partially-plastic items must overflow into the third container. If the third container is already near capacity due to other items, we must check that adding these flexible items still fits.

## Approaches

A brute-force approach would try every possible allocation of partially-paper and partially-plastic items between their primary containers and the third container. For instance, if there are $a_4$ partially-paper items, we could try all splits from 0 in the first container to all in the first container. The total combinations would be $(a_4+1) \cdot (a_5+1)$, which is infeasible when $a_4$ or $a_5$ can be $10^8$.

The optimal approach recognizes that we do not need to enumerate splits. For the first container, we must place all strict paper items. Any remaining capacity can be filled with partially-paper items, and the rest must go into the third container. A similar logic applies to the second container and partially-plastic items. Finally, we check whether the third container can accommodate all its base items plus the overflow from partial items. This reduces the problem to simple arithmetic comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a4 * a5) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the capacities $c_1$, $c_2$, $c_3$ and the item counts $a_1$ through $a_5$.
2. Check if the strict paper items fit in the first container. Compute the remaining capacity after placing all strict paper items: `rem1 = c1 - a1`. If `rem1` is negative, print NO and continue to the next test case.
3. Use the remaining capacity in the first container to place partially-paper items. If `a4` exceeds `rem1`, the excess must go to the third container. Compute this overflow: `overflow_paper = max(0, a4 - rem1)`.
4. Repeat the same logic for the second container with strict plastic items and partially-plastic items. Compute the overflow into the third container: `overflow_plastic = max(0, a5 - (c2 - a2))`. If the strict items do not fit, print NO.
5. Finally, check if the third container can hold all strict other items plus the overflows from partially-paper and partially-plastic items: `total_in_third = a3 + overflow_paper + overflow_plastic`. If `total_in_third > c3`, print NO. Otherwise, print YES.

Why it works: at each step, we always place mandatory items in their required containers first. Partially flexible items are only moved to the third container if their primary container cannot hold them. This guarantees that no container exceeds capacity and that we respect item restrictions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    c1, c2, c3 = map(int, input().split())
    a1, a2, a3, a4, a5 = map(int, input().split())
    
    rem1 = c1 - a1
    if rem1 < 0:
        print("NO")
        continue
    overflow_paper = max(0, a4 - rem1)
    
    rem2 = c2 - a2
    if rem2 < 0:
        print("NO")
        continue
    overflow_plastic = max(0, a5 - rem2)
    
    if a3 + overflow_paper + overflow_plastic <= c3:
        print("YES")
    else:
        print("NO")
```

The code first subtracts mandatory items from their containers, then computes how many flexible items spill into the third container. Using `max(0, ...)` ensures we never subtract more than the available capacity. Each comparison directly corresponds to a container capacity constraint.

## Worked Examples

### Sample Input 1

```
c1=2, c2=2, c3=3
a1=1, a2=2, a3=3, a4=1, a5=0
```

| Step | rem1 | overflow_paper | rem2 | overflow_plastic | total_in_third | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2-1=1 | max(0,1-1)=0 | 2-2=0 | max(0,0-0)=0 | 3+0+0=3 | YES |

The strict paper fits in the first container, partially-paper item fits there as well, third container can hold all items.

### Sample Input 2

```
c1=2, c2=2, c3=3
a1=1, a2=2, a3=3, a4=0, a5=1
```

| Step | rem1 | overflow_paper | rem2 | overflow_plastic | total_in_third | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2-1=1 | max(0,0-1)=0 | 2-2=0 | max(0,1-0)=1 | 3+0+1=4 | NO |

The partially-plastic item overflows to the third container, which then exceeds its capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a few arithmetic operations. |
| Space | O(1) | No additional memory scales with input size. |

Given the constraints $t \le 3\cdot10^4$, each test case uses only constant time, so the solution runs well within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        c1, c2, c3 = map(int, input().split())
        a1, a2, a3, a4, a5 = map(int, input().split())
        
        rem1 = c1 - a1
        if rem1 < 0:
            output.append("NO")
            continue
        overflow_paper = max(0, a4 - rem1)
        
        rem2 = c2 - a2
        if rem2 < 0:
            output.append("NO")
            continue
        overflow_plastic = max(0, a5 - rem2)
        
        if a3 + overflow_paper + overflow_plastic <= c3:
            output.append("YES")
        else:
            output.append("NO")
    return "\n".join(output)

# Provided samples
assert run("7\n1 2 3\n1 2 3 0 0\n2 2 3\n1 2 3 1 0\n2 2 3\n1 2 3 0 1\n1 2 5\n1 2 3 1 1\n0 0 0\n0 0 0 0 0\n0 0 4\n1 0 0 0 0\n13 37 42\n0 0 0 40 47\n") == "YES\nYES\nNO\nYES\nYES\nNO\nYES"

# Custom cases
assert run("1\n0 0 0\n0 0 0 0 0\n") == "YES"  # all zero capacities, no items
assert run("1\n1 1 1\n1 0 0 0 0\n") == "YES"  # exactly fits in first container
assert run("1\n1 1 1\n2 0 0 0 0\n") == "NO"   # first container over capacity
assert run("1\n1 1 1\n0 0 1 1 1\n") == "
```
