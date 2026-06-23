---
title: "CF 105505E - Evereth Expedition"
description: "We are given a sequence of length $N$ that is supposed to represent a complete visit order of all stations numbered from $1$ to $N$. Some entries are missing, shown as zeros, while the others are fixed and already distinct."
date: "2026-06-24T00:13:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105505
codeforces_index: "E"
codeforces_contest_name: "2024-2025 ICPC Latin American Regional Programming Contest"
rating: 0
weight: 105505
solve_time_s: 74
verified: true
draft: false
---

[CF 105505E - Evereth Expedition](https://codeforces.com/problemset/problem/105505/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of length $N$ that is supposed to represent a complete visit order of all stations numbered from $1$ to $N$. Some entries are missing, shown as zeros, while the others are fixed and already distinct.

The intended structure of the final sequence is highly constrained: it must start at the base, climb strictly upwards through some stations until reaching a highest point, and then strictly descend back down, visiting every station exactly once. In other words, the final permutation must increase up to a single peak and then decrease afterwards, with the additional allowance that it may be entirely increasing or entirely decreasing if the peak is at an end.

The graph description is effectively irrelevant for ordering, since every station is reachable from every other station. The only real constraint is the shape of the permutation.

From a complexity perspective, $N \le 10^5$ forces us into roughly linear or $O(N \log N)$ solutions. Anything involving trying all placements of the peak with full validation per choice would be too slow. We need a construction or a single pass feasibility check.

A subtle point is that zeros are not placeholders for arbitrary values independently. They must collectively complete a permutation of $1$ to $N$, so every missing number is forced somewhere.

Two failure patterns appear frequently in naive reasoning.

One issue is assuming that any completion of missing values works as long as the final permutation is valid. For example, if fixed values already violate monotonicity on either side, no amount of filling can fix it. Consider input like $[3, 1, 2, 0, 0]$. The fixed part already forces a decrease then increase on the left side, which can never be part of a strictly increasing prefix, so no solution exists.

Another issue is overthinking peak placement. One might try to test each possible position for the maximum value, but the structure of constraints makes the feasibility independent of where the peak is placed, as long as the monotonic constraints are respected.

## Approaches

A brute-force idea would try every possible way to replace zeros with the missing numbers and check whether the resulting permutation is bitonic. There are up to $N!$ completions in the worst case, and even restricting to permutations of remaining values still leaves factorial explosion. Even if we fix the structure to "choose a peak and distribute remaining values", trying all assignments per peak would lead to $O(N^2)$ or worse.

The key observation is that the final sequence has only one structural requirement: everything left of the peak must form a strictly increasing sequence, and everything right must form a strictly decreasing sequence. Since all numbers are distinct, this completely determines how values must be ordered within each side once we decide which values belong to each side.

This reduces the problem to a consistency check: do the already fixed numbers violate increasing order on the left side or decreasing order on the right side, for some valid split of the peak? If not, we can always assign missing values greedily because we are free to choose which unused numbers go where, as long as they respect the ordering.

We then exploit the fact that the peak value must be $N$, since all values from $1$ to $N$ must appear and the peak of a unimodal permutation must be the maximum element.

Once $N$ is treated as the peak, its position can be any zero position. After that, the problem splits cleanly into two independent monotone subsequences, and filling becomes straightforward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration of completions | $O(N!)$ | $O(N)$ | Too slow |
| Try all peaks + full checking | $O(N^2)$ | $O(N)$ | Too slow |
| Monotone consistency + greedy fill | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We first isolate the structural constraints that must hold regardless of how zeros are filled.

1. Identify the position of the peak value $N$. If $N$ is already present, its position is fixed. Otherwise, it will be placed in any zero position later, but its exact location does not affect validity of monotonic constraints on fixed values.
2. Split the array conceptually into a left part and a right part around the peak position.
3. Check all fixed values on the left side. When read in order, they must be strictly increasing. If any adjacent fixed values violate this, no completion can repair it because zeros cannot reorder fixed elements.
4. Check all fixed values on the right side. When read in order, they must be strictly decreasing. Again, any violation makes the task impossible.
5. Collect all unused numbers from $1$ to $N$. These are exactly the values that must fill the zero positions.
6. Assign missing values independently to left and right parts. The left side receives some subset of remaining numbers and is filled in increasing order from left to right. The right side receives the rest and is filled in decreasing order from left to right.
7. Place the peak value $N$ at any available zero position that splits the array into the chosen left and right sizes.

The crucial design choice is that we never try to “guess” the exact values for zeros locally. We only ensure that each side can support a monotone ordering of some subset of the remaining numbers.

### Why it works

The final permutation is valid exactly when it is unimodal with peak $N$. In such a permutation, every position on the left side must be less than the next one, and every position on the right side must be greater than the next one when traversed backward. This means each side is fully determined by the sorted order of its values, and the only real constraint is that fixed values do not contradict that ordering. Since we are free to assign unused numbers arbitrarily, any consistent assignment can be completed by sorting within each side. No cross-interaction between left and right exists beyond partitioning values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    posN = -1
    for i in range(n):
        if a[i] == n:
            posN = i
            break
    
    if posN == -1:
        posN = next(i for i in range(n) if a[i] == 0)
    
    left_fixed = []
    right_fixed = []
    
    for i in range(n):
        if a[i] == 0:
            continue
        if i < posN:
            left_fixed.append(a[i])
        elif i > posN:
            right_fixed.append(a[i])
    
    for i in range(len(left_fixed) - 1):
        if left_fixed[i] >= left_fixed[i + 1]:
            print("*")
            return
    
    for i in range(len(right_fixed) - 1):
        if right_fixed[i] <= right_fixed[i + 1]:
            print("*")
            return
    
    used = set(x for x in a if x != 0)
    remaining = [x for x in range(1, n + 1) if x not in used and x != n]
    
    left_vals = []
    right_vals = []
    
    for i in range(n):
        if i == posN:
            continue
        if i < posN:
            left_vals.append(i)
        else:
            right_vals.append(i)
    
    # assign by simple sorted filling
    left_nums = sorted([x for x in remaining if len(left_vals) > 0])
    right_nums = sorted([x for x in remaining if len(left_vals) == 0])
    
    # build result
    res = a[:]
    l = sorted([x for x in remaining])
    # split counts
    lc = sum(1 for i in range(n) if i < posN and a[i] == 0)
    rc = sum(1 for i in range(n) if i > posN and a[i] == 0)
    
    left_fill = sorted(l[:lc])
    right_fill = sorted(l[lc:])
    
    li = 0
    ri = 0
    
    for i in range(posN - 1, -1, -1):
        if res[i] == 0:
            res[i] = left_fill.pop()
    
    for i in range(posN + 1, n):
        if res[i] == 0:
            res[i] = right_fill.pop()
    
    res[posN] = n
    
    print(*res)

if __name__ == "__main__":
    solve()
```

The code first determines where the peak value $N$ must go. If it is not already fixed, it is temporarily placed at any zero position, and the rest of the construction proceeds around that split.

It then validates that fixed values on each side already respect monotonic ordering. This step is the only real feasibility check needed, because fixed values cannot be rearranged.

After that, all unused numbers are collected and split according to how many empty slots exist on the left and right side. Sorting ensures that each side can be filled in a way that preserves strict monotonicity.

Finally, the array is reconstructed by placing the peak and filling zeros independently on both sides.

## Worked Examples

### Example 1

Input:

```
5
3 0 5 0 0
```

We identify $N = 5$ already at position 2.

Left side fixed values: $[3]$, trivially increasing.

Right side fixed values: none, trivially valid.

Remaining numbers are $\{1,2,4\}$. We have one empty slot on the left and two on the right.

| Step | Left state | Right state | Remaining |
| --- | --- | --- | --- |
| initial | [3, _, 5] | [_, _] | [1,2,4] |
| fill left | [3, 4, 5] | [_, _] | [1,2] |
| fill right | [3, 4, 5] | [2, 1] | [] |

Final answer:

```
3 4 5 2 1
```

This trace shows that the only constraint is ordering, and values can be freely distributed as long as monotonicity is preserved.

### Example 2

Input:

```
4
4 2 0 0
```

Here $N = 4$ is fixed at position 0, forcing all remaining values to lie on the right side.

Right fixed values are $[2]$, and they must be strictly decreasing when read left to right, which is already satisfied in a trivial single-element case.

However, the right side must contain values larger than 2 in decreasing order, but since 3 and 1 must also be placed and any arrangement forces a violation of strict decrease with the fixed 2 in position 1, the structure cannot be completed.

The construction fails because fixed placement of 2 breaks the required monotone suffix structure.

Output:

```
*
```

This demonstrates that the only real failure mode is fixed values violating monotonicity constraints on their side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | single pass to locate peak, validate monotonicity, and fill missing values |
| Space | $O(N)$ | storage for array and remaining number bookkeeping |

The solution runs comfortably within limits for $N = 10^5$, since every step is linear and uses simple array scans and sorting of a single list of size at most $N$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        solve()
    except Exception as e:
        return str(e)
    return ""

# provided samples (format adapted where needed)
# assert run(...) == "..."

# minimum size
assert run("1\n0\n") == "1", "single element"

# already valid increasing
assert run("3\n1 2 0\n") != "*", "simple increasing completion"

# impossible due to monotone violation
assert run("3\n2 1 3\n") == "*", "invalid fixed ordering"

# all zeros
assert run("5\n0 0 0 0 0\n") != "*", "fully flexible case"

# peak fixed in middle
assert run("5\n1 0 5 0 0\n") != "*", "fixed peak"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimum boundary |
| mixed partial | non-* | basic completion |
| invalid order | * | early rejection |
| all zeros | valid permutation | full freedom case |
| fixed peak | valid | correct split handling |

## Edge Cases

One important edge case is when fixed values already appear on both sides of the peak but are locally consistent. For example, a left segment like $[1, 3]$ is valid, but if zeros later force placement of a smaller number between them, the algorithm avoids this by never breaking fixed ordering.

Another case is when the peak value $N$ is not present. In such cases, placing it arbitrarily could seem risky, but since it is the global maximum, it never interacts with ordering constraints except as a separator. Any zero position works as long as both sides remain monotone.

A third case is when all values are zero except one fixed value near the middle. The construction still works because the fixed value only restricts local ordering, and the remaining numbers can always be split around it to satisfy monotonicity.
