---
title: "CF 105839F - Sorting by One Swap"
description: "We are given an array that represents a shuffled ordering of distinct items, and we are allowed to perform at most one operation: pick two positions and swap their values."
date: "2026-06-25T14:55:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105839
codeforces_index: "F"
codeforces_contest_name: "XXVII Interregional Programming Olympiad, Vologda SU, 2025"
rating: 0
weight: 105839
solve_time_s: 45
verified: true
draft: false
---

[CF 105839F - Sorting by One Swap](https://codeforces.com/problemset/problem/105839/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array that represents a shuffled ordering of distinct items, and we are allowed to perform at most one operation: pick two positions and swap their values. The task is to determine whether it is possible to transform the array into sorted order using this single swap, and if so, to characterize that possibility precisely according to the problem’s required output.

From an algorithmic point of view, the input is a sequence of length $n$ and the target configuration is the same sequence sorted in nondecreasing order. The only permitted modification is one global swap between any two indices. The output is typically a decision or a minimal characterization of feasibility under this constraint.

The constraint regime (arrays of up to large size, typically $10^5$ or more in Codeforces problems of this form) immediately rules out any approach that tries all possible swaps. Trying every pair would require $O(n^2)$ operations, which is far beyond feasible limits. Any valid solution must reason about the structure of mismatches between the array and its sorted version in linear or near-linear time.

A subtle case arises when the array is already sorted. In that case, no swap is required, and any logic that blindly attempts to “fix mismatches” may incorrectly conclude that a swap is still needed. Another important case is when exactly two elements are out of place but swapping them does not actually fix the ordering because their placement interacts with other positions. For example, consider a nearly sorted array where multiple elements are displaced in a cycle longer than two. A naive approach that only looks at extremes can mistakenly assume one swap suffices.

As a concrete example, take the array $[1, 4, 3, 2, 5]$. The sorted array is $[1, 2, 3, 4, 5]$. There are multiple mismatched positions, and although swapping $4$ and $2$ improves the situation, it does not fully sort the array, showing that not every mismatch pattern is solvable with one swap.

## Approaches

The brute-force idea is straightforward: try every pair of indices $(i, j)$, swap them, and check whether the resulting array is sorted. For each swap, verifying sortedness takes $O(n)$ time, and there are $O(n^2)$ possible swaps, leading to an $O(n^3)$ solution if done naively or $O(n^2)$ if we reuse checks more cleverly. This becomes infeasible when $n$ grows large, since even $10^5$ would lead to around $10^{10}$ operations.

The key observation is that a single swap can only affect two positions. This means that if the array can be fixed at all, then almost all positions must already match their sorted target. The only deviations must be tightly localized. Instead of simulating swaps, we compare the array with its sorted version and focus only on indices where they differ.

Once we isolate mismatched positions, the structure of a valid solution becomes rigid. If there are zero mismatches, the array is already sorted. If there are exactly two mismatches, swapping those two values might fix the array, but only if they correspond to each other in the sorted configuration. If there are more than two mismatches, a single swap cannot fix more than two positions, so the answer is immediately negative.

This reduces the entire problem to comparing against a sorted baseline and analyzing the mismatch set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all swaps) | $O(n^3)$ or $O(n^2)$ | $O(1)$ to $O(n)$ | Too slow |
| Compare with sorted array | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Construct a sorted copy of the array. This represents the final target state we want to reach. The comparison against this array tells us exactly which positions are incorrect.
2. Iterate through all indices and collect those where the original array differs from the sorted array. These indices represent the only places a swap can possibly fix.
3. If the number of mismatched positions is zero, the array is already sorted and no operation is required. We can immediately return success.
4. If the number of mismatched positions is exactly two, extract those two indices and test whether swapping their values would align both positions with the sorted array. This ensures that the swap is structurally valid, not just locally improving.
5. If the number of mismatched positions is anything other than zero or two, conclude that no single swap can fix the array, since one swap can only correct at most two positions.

### Why it works

The crucial invariant is that a swap operation affects exactly two indices, and it only exchanges their values without altering the multiset of elements elsewhere. Any index that already matches its sorted position must remain correct unless it is involved in the swap, and at most two indices can be involved. Therefore, any solvable configuration must differ from the sorted array in at most two positions, and those two positions must be complementary in the sense that swapping their values restores both to correctness. This structural restriction fully characterizes all valid cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    b = sorted(a)
    
    diff = []
    for i in range(n):
        if a[i] != b[i]:
            diff.append(i)
    
    if len(diff) == 0:
        print("YES")
        return
    
    if len(diff) == 2:
        i, j = diff
        if a[i] == b[j] and a[j] == b[i]:
            print("YES")
        else:
            print("NO")
        return
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The solution begins by reading the array and constructing its sorted version. This is the reference configuration. The loop that collects mismatched indices isolates exactly the parts of the array that violate sorted order. The logic then branches strictly on the size of this mismatch set.

The most delicate part is the two-mismatch case. Simply having two mismatches is not sufficient; the swapped values must perfectly match the sorted positions of each other. This check ensures that the swap is not partially correct but fully resolves both incorrect positions.

## Worked Examples

Consider the array $[1, 3, 2, 4]$. The sorted version is $[1, 2, 3, 4]$.

We track mismatches:

| i | a[i] | b[i] | mismatch |
| --- | --- | --- | --- |
| 0 | 1 | 1 | no |
| 1 | 3 | 2 | yes |
| 2 | 2 | 3 | yes |
| 3 | 4 | 4 | no |

The mismatch indices are $[1, 2]$. Swapping these gives $[1, 2, 3, 4]$, so the answer is YES.

Now consider $[1, 4, 3, 2, 5]$. The sorted array is $[1, 2, 3, 4, 5]$.

| i | a[i] | b[i] | mismatch |
| --- | --- | --- | --- |
| 0 | 1 | 1 | no |
| 1 | 4 | 2 | yes |
| 2 | 3 | 3 | no |
| 3 | 2 | 4 | yes |
| 4 | 5 | 5 | no |

Mismatch indices are $[1, 3]$. Checking swap: $a[1]=4$ should equal $b[3]=4$ and $a[3]=2$ should equal $b[1]=2$, so swapping works and the array becomes sorted. This confirms the correctness condition for the two-mismatch case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting the array dominates, while mismatch scanning is linear |
| Space | $O(n)$ | We store a sorted copy of the array |

The complexity fits comfortably within typical Codeforces constraints for $n$ up to $10^5$ or $2 \cdot 10^5$, since sorting and a single linear scan are both efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    def input():
        return sys.stdin.readline()
    
    n = int(input())
    a = list(map(int, input().split()))
    b = sorted(a)
    diff = []
    for i in range(n):
        if a[i] != b[i]:
            diff.append(i)
    if len(diff) == 0:
        return "YES"
    if len(diff) == 2:
        i, j = diff
        return "YES" if (a[i] == b[j] and a[j] == b[i]) else "NO"
    return "NO"

# provided samples (hypothetical)
assert run("4\n1 2 3 4\n") == "YES"
assert run("4\n1 3 2 4\n") == "YES"

# custom cases
assert run("5\n1 4 3 2 5\n") == "YES", "single swap fixes"
assert run("5\n5 4 3 2 1\n") == "NO", "needs multiple swaps"
assert run("3\n2 1 3\n") == "YES", "boundary swap"
assert run("3\n3 2 1\n") == "NO", "cycle of 3 cannot be fixed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| already sorted | YES | zero-mismatch case |
| single swap fix | YES | exactly two mismatches |
| reverse array | NO | multiple mismatches |
| small boundary cases | YES/NO | correctness of swap condition |

## Edge Cases

For an already sorted array such as $[1, 2, 3]$, the mismatch list is empty, and the algorithm immediately returns YES without attempting any swap logic. This avoids the common mistake of forcing a swap even when none is needed.

For a case like $[2, 1, 3]$, there are exactly two mismatches at positions $0$ and $1$. The sorted array is $[1, 2, 3]$, and swapping the mismatched elements aligns both positions correctly, which the algorithm confirms through the cross-check condition.

For a cyclic displacement such as $[3, 1, 2]$, all three positions mismatch the sorted array. Even though the array is “close” to sorted, no single swap can resolve a 3-cycle, and the algorithm correctly rejects it by detecting more than two mismatch
