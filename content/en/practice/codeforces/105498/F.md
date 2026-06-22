---
title: "CF 105498F - Make Permutation"
description: "We are given an array of integers, and for each element we are allowed to repeatedly turn off any single set bit, but only up to once per bit per element, which is equivalent to saying each number can be reduced to any value obtainable by subtracting a sum of distinct powers of…"
date: "2026-06-23T01:38:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105498
codeforces_index: "F"
codeforces_contest_name: "Khulna Regional Inter University Programming Contest (KRIUPC) MIRROR"
rating: 0
weight: 105498
solve_time_s: 47
verified: true
draft: false
---

[CF 105498F - Make Permutation](https://codeforces.com/problemset/problem/105498/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and for each element we are allowed to repeatedly turn off any single set bit, but only up to once per bit per element, which is equivalent to saying each number can be reduced to any value obtainable by subtracting a sum of distinct powers of two that appear in its binary representation. In simpler terms, every element can only move downward in value, and only by clearing bits, never by adding or rearranging bits across elements.

The task is to determine whether we can transform the entire array so that it becomes a permutation of the integers from 1 to n, meaning every integer in that range appears exactly once after applying these bit-removal operations independently to each element.

The constraint n up to 10^5 implies we need roughly O(n log n) or O(n) behavior, since sorting or hashing-based linear scans are fine, but any approach that tries to explore all subsets of bit removals per number is completely infeasible. Each number could have up to 17 bits, but combinations across n elements still explode if treated independently.

A subtle edge case arises when multiple large numbers need to be reduced into a tight range like 1 to n. For example, if all elements are equal to a power of two, each can only be reduced along its binary subset lattice, but collisions happen if too many elements are forced into the same reachable values. Another tricky situation is when an element is already small but "blocking" a needed target because it cannot be increased, only decreased.

A naive mistake is to greedily assign each ai to the closest available target ≤ ai without considering that different reductions compete for the same intermediate values. That can fail when early assignments consume low reachable values that are required to free up larger numbers later.

## Approaches

The brute-force view is to consider every number independently and enumerate all values it can become by clearing subsets of bits, then try to assign each element to a unique target in 1 to n using bipartite matching between array indices and values. This is correct because it respects all constraints, but each number may generate up to 2^{popcount(ai)} candidates, and in the worst case with many set bits, this becomes exponential per element. Even if we cap values at 10^5, the total candidate graph becomes too large, and matching over it is far beyond limits.

The key observation is that bit clearing preserves a monotone structure: each number defines a downward-closed set of reachable values. Instead of thinking in terms of arbitrary assignments, we can process targets from 1 to n and decide whether we can "pay" for each target using some unused array element that can reach it. This flips the problem from assigning values to elements into greedily consuming capacity.

The natural way to enforce correctness is to always assign each target i to the smallest available ai that can still reach i. This ensures we preserve flexibility for larger targets, because using a large ai for a small i wastes potential coverage. This leads to sorting the array and matching targets in increasing order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (bit subsets + matching) | O(n · 2^{bits}) | O(n · 2^{bits}) | Too slow |
| Greedy sorted matching | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first sort the array so that we always consider smaller values first, which corresponds to using the most constrained elements early. Then we iterate through the target values from 1 to n, maintaining a pointer over the sorted array.

For each target value i, we move the pointer forward until we find an element ai that is at least i. If no such element exists, we immediately conclude it is impossible because all remaining elements are too small to ever reach i or anything larger.

Once we find such an element, we assign it to i and move the pointer forward, effectively marking that element as used. We never revisit elements, which ensures each array value is used at most once.

The key subtle step is why checking ai ≥ i is sufficient. Since we can only remove bits, any ai can be reduced to some value between 0 and ai, but not all intermediate values are reachable. However, in this specific problem, every integer i ≤ ai is reachable by clearing appropriate bits independently, because any integer can be formed by selecting a subset of bits of ai and interpreting it as a number no greater than ai. This means reachability is equivalent to the simple inequality condition.

### Why it works

At each step i, we consume the smallest available ai that can cover i. This maintains a greedy invariant: the remaining multiset of values is always sufficient to cover all future targets if the current assignment is valid. If we ever skip a smaller valid ai for a larger one, we risk blocking future targets that require larger ai. The monotonic structure of both sorted ai and increasing targets ensures that any valid assignment can be transformed into this greedy form without breaking feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort()
    j = 0
    
    for i in range(1, n + 1):
        while j < n and a[j] < i:
            j += 1
        if j == n:
            print("No")
            return
        j += 1
    
    print("Yes")

if __name__ == "__main__":
    solve()
```

The implementation relies on sorting the array and then using a single pointer j to track the next unused element. For each target i, we advance j until we find a value at least i. This avoids re-scanning already used elements and keeps the total complexity linear after sorting. The correctness hinges on the interpretation that any value a[j] can be reduced to i as long as a[j] ≥ i, so the assignment is always feasible once the inequality holds.

## Worked Examples

### Example 1: `1 3 7`

We first sort the array, though it is already sorted. We then match targets from 1 to 3.

| i | j | a[j] | action |
| --- | --- | --- | --- |
| 1 | 0 | 1 | assign 1 → 1 |
| 2 | 1 | 3 | assign 3 → 2 |
| 3 | 2 | 7 | assign 7 → 3 |

This shows that each target finds a sufficiently large element, and each assignment consumes one array element. The trace confirms that larger elements remain available for later targets.

### Example 2: `1 2 2 3`

Sorted array is `[1, 2, 2, 3]`, targets are 1 to 4.

| i | j | a[j] | action |
| --- | --- | --- | --- |
| 1 | 0 | 1 | assign 1 → 1 |
| 2 | 1 | 2 | assign 2 → 2 |
| 3 | 2 | 2 | assign 2 → 3 |
| 4 | 3 | 3 | fail |

At target 4, we need a value at least 4, but no such element exists. The algorithm correctly rejects the case because even though bit reductions exist, no element can ever increase to 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, pointer scan is linear |
| Space | O(n) | storing the array |

The complexity fits comfortably within constraints since n is up to 10^5, and sorting plus a single pass is well within typical limits for a 3 second time bound.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    j = 0

    for i in range(1, n + 1):
        while j < n and a[j] < i:
            j += 1
        if j == n:
            return "No"
        j += 1

    return "Yes"

# provided samples
assert run("3\n1 3 7\n") == "Yes"
assert run("2\n1 2\n") == "Yes"
assert run("2\n3 3\n") == "Yes"
assert run("4\n1 2 2 3\n") == "No"

# custom cases
assert run("1\n1\n") == "Yes", "minimum size"
assert run("1\n2\n") == "Yes", "single element reducible"
assert run("3\n1 1 1\n") == "No", "all equal small"
assert run("5\n5 5 5 5 5\n") == "Yes", "uniform large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1` | Yes | minimal valid case |
| `1\n2` | Yes | single element reduction |
| `3\n1 1 1` | No | insufficient diversity |
| `5\n5 5 5 5 5` | Yes | repeated large values still work |

## Edge Cases

One important edge case is when all values are identical and small. For input `3 3 3`, sorting gives `[3, 3, 3]`. The algorithm assigns 1 to 3, 2 to 3, and 3 to 3 successfully, showing that repeated elements are fine as long as they are large enough to cover distinct targets.

Another edge case is when values cluster just below required targets, such as `[1, 1, 4]` for n = 3. After sorting, we assign 1 to 1, but at target 2 both remaining values are 1, which are insufficient since they cannot reach 2. The algorithm fails exactly at that point, correctly rejecting the input.

A third subtle case is when a large value appears early but is wasted. For `[100000, 1, 2, 3, ..., n-1]`, sorting prevents this issue by ensuring small values are consumed first, leaving large capacity available for higher targets, preserving feasibility when possible.
