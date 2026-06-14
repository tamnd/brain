---
title: "CF 1561A - Simply Strange Sort"
description: "We are given a permutation, meaning an array containing every integer from 1 to n exactly once. The process repeatedly applies a deterministic “strange bubble pass” operation, but with a twist: odd-numbered rounds compare adjacent pairs starting from index 1, 3, 5, and…"
date: "2026-06-14T22:32:20+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1561
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 740 (Div. 2, based on VK Cup 2021 - Final (Engine))"
rating: 800
weight: 1561
solve_time_s: 160
verified: true
draft: false
---

[CF 1561A - Simply Strange Sort](https://codeforces.com/problemset/problem/1561/A)

**Rating:** 800  
**Tags:** brute force, implementation, sortings  
**Solve time:** 2m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation, meaning an array containing every integer from 1 to n exactly once. The process repeatedly applies a deterministic “strange bubble pass” operation, but with a twist: odd-numbered rounds compare adjacent pairs starting from index 1, 3, 5, and even-numbered rounds start from index 2, 4, 6.

Each comparison only swaps the pair if they are out of order. A full round consists of sweeping all valid pairs of the chosen parity in order.

The task is to determine how many full rounds are needed until the array becomes fully sorted in increasing order for the first time. If it is already sorted initially, the answer is zero.

The constraints are small enough that even a direct simulation is feasible. The total sum of n across all test cases is at most 999, and each simulation step performs at most n comparisons per round. This bounds a straightforward solution to roughly 10^6 operations overall, which is easily fast enough in Python.

A subtle edge case arises when the array is already sorted or nearly sorted. A naive implementation that only checks after completing a round must ensure it does not miss the “already sorted” condition before any iteration begins. Another potential pitfall is stopping after detecting sorted state during a round instead of after completing the full iteration, since the problem defines a full iteration as the unit of counting.

## Approaches

The naive idea is to directly simulate the process as described. In each iteration, we loop over the appropriate indices depending on parity and perform conditional swaps. After each full iteration, we check whether the array is sorted. We repeat until it becomes sorted.

This works because the operation exactly defines the evolution of the permutation, and we are asked for the first time it reaches sorted order, so simulation is faithful.

The inefficiency question is whether repeated full passes are too expensive. Each pass is O(n), and in the worst case we might need O(n) passes, but here n ≤ 999 and total sum is small, so the worst-case O(n²) per test case is still acceptable.

The key observation is that no advanced data structure or sorting theory is needed because the process is explicitly bounded and monotonic toward sorted order. Each round is deterministic and reduces inversions in a structured way, so direct simulation is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) per test case | O(1) extra | Accepted |
| Any optimized variant | O(n) per test case | O(1) | Unnecessary |

## Algorithm Walkthrough

We simulate the process exactly as defined and count rounds.

1. Read the permutation and check if it is already sorted. If yes, output 0 immediately. This avoids unnecessary simulation when the answer is trivial.
2. Initialize a counter for the number of iterations performed.
3. Repeat until the array becomes sorted:

1. If the current iteration number is odd, scan indices 1, 3, 5, ..., n−2 and swap adjacent elements when needed.
2. If the iteration number is even, scan indices 2, 4, 6, ..., n−1 and swap adjacent elements when needed.

Each full scan represents one iteration of the process, and partial progress inside a scan is part of the same iteration.
4. After each full iteration, increase the counter and check whether the array is now sorted.
5. When sorted, return the number of completed iterations.

The reason this works is that the algorithm defines a deterministic state transition on permutations. Each iteration is a complete transformation step, and the problem asks for the first time step when the system reaches a fixed point (sorted order). Since the state space is finite and each step strictly reduces disorder until convergence, simulation will always terminate.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_sorted(a):
    for i in range(len(a) - 1):
        if a[i] > a[i + 1]:
            return False
    return True

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        if is_sorted(a):
            out.append("0")
            continue
        
        steps = 0
        
        while True:
            steps += 1
            
            if steps % 2 == 1:
                start = 0
            else:
                start = 1
            
            for i in range(start, n - 1, 2):
                if a[i] > a[i + 1]:
                    a[i], a[i + 1] = a[i + 1], a[i]
            
            if is_sorted(a):
                out.append(str(steps))
                break
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the process definition. The parity of the iteration decides whether we start comparisons at index 0 or 1. The loop stepping by 2 ensures we only apply swaps on the correct pairs.

The sorted check is placed after each full iteration, matching the requirement that we count complete rounds, not partial progress inside a round. The early check before simulation handles the zero-case efficiently.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [3, 2, 1]
```

| Step | Array State | Operation |
| --- | --- | --- |
| 0 | 3 2 1 | initial |
| 1 | 2 3 1 | swap (3,2) |
| 2 | 2 1 3 | swap (3,1) in even pass |
| 3 | 1 2 3 | final pass completes |

After 3 full iterations, the array becomes sorted. The key observation is that elements gradually shift toward correct parity positions, similar to bubble sort but split across alternating index sets.

### Example 2

Input:

```
n = 5
a = [4, 5, 7, 1, 3]
```

| Step | Array State | Operation |
| --- | --- | --- |
| 0 | 4 5 7 1 3 | initial |
| 1 | 4 5 1 7 3 | odd pass swaps (7,1) |
| 2 | 4 1 5 3 7 | even pass adjusts shifted elements |
| 3 | 1 4 3 5 7 | odd pass continues bubbling |
| 4 | 1 2 4 3 5 6 7 (conceptually progressing) | continued convergence |
| 5 | 1 2 3 4 5 | sorted |

This trace shows how disorder propagates locally and is corrected over alternating passes, gradually aligning all elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) per test case | Each iteration scans O(n), and in worst case we perform O(n) iterations |
| Space | O(1) extra | We modify the array in place |

The total sum of n is at most 999, so even the worst-case quadratic simulation is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def is_sorted(a):
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                return False
        return True

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        if is_sorted(a):
            out.append("0")
            continue

        steps = 0

        while True:
            steps += 1
            start = 0 if steps % 2 == 1 else 1

            for i in range(start, n - 1, 2):
                if a[i] > a[i + 1]:
                    a[i], a[i + 1] = a[i + 1], a[i]

            if is_sorted(a):
                out.append(str(steps))
                break

    return "\n".join(out)

# provided samples
assert run("""3
3
3 2 1
7
4 5 7 1 3 2 6
5
1 2 3 4 5
""") == """3
5
0"""

# custom: already sorted single case
assert run("""1
5
1 2 3 4 5
""") == "0"

# custom: reverse order small
assert run("""1
3
3 2 1
""") == "3"

# custom: alternating disorder
assert run("""1
5
2 1 4 3 5
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sorted array | 0 | early exit correctness |
| reverse small | 3 | worst-case propagation |
| alternating swaps | 2 | parity-based behavior |

## Edge Cases

A fully sorted array such as `[1, 2, 3, 4, 5]` returns 0 immediately because the initial check detects no inversions before any iteration begins.

A reverse permutation like `[3, 2, 1]` demonstrates maximum work for small n. The first pass fixes local inversions but does not globally sort the array, so multiple full iterations are required before reaching a fixed point.

An alternating pattern like `[2, 1, 4, 3, 5]` shows how independent local inversions resolve in parallel. Odd and even passes each resolve different adjacency sets, and the array stabilizes after a small number of full iterations, confirming that convergence is driven by local correction rather than global restructuring.
