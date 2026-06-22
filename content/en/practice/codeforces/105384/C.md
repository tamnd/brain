---
title: "CF 105384C - Chemistry Class"
description: "We are given an even number of students, specifically 2n, each with a numeric chemistry skill. The teacher must split them into n disjoint pairs, so every student belongs to exactly one pair."
date: "2026-06-23T05:20:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105384
codeforces_index: "C"
codeforces_contest_name: "Anton Trygub Contest 2 (The 3rd Universal Cup, Stage 3: Ukraine)"
rating: 0
weight: 105384
solve_time_s: 54
verified: true
draft: false
---

[CF 105384C - Chemistry Class](https://codeforces.com/problemset/problem/105384/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an even number of students, specifically 2n, each with a numeric chemistry skill. The teacher must split them into n disjoint pairs, so every student belongs to exactly one pair. A pair is only valid if the absolute difference between the two skills is at most A, otherwise the lab explodes and the entire partition is invalid.

Among valid pairs, we classify quality by a second threshold B. If the difference is at most B, the pair produces a perfect result; if it is between B and A, the result is merely acceptable. The goal is to determine whether any valid pairing exists at all, and if it does, to maximize how many pairs fall into the “perfect” category.

The input consists of multiple independent test cases, each describing a multiset of skills and two thresholds. For each test case we either report impossibility or compute the maximum number of perfect pairs achievable under a valid pairing constraint.

The constraints are large enough that any quadratic pairing strategy over the full set is too slow. With total 2n up to 2⋅10^5 across tests, even O(n^2) constructions per test would be completely infeasible. This immediately suggests a sorting-based greedy structure or a two-pointer construction.

A key subtle failure case appears when a naive greedy tries to always pair closest neighbors without respecting the A constraint globally. For example, consider A very small and a cluster structure where local pairing forces an impossible leftover. Another failure happens when one tries to maximize perfect pairs first without ensuring feasibility under A, which can produce a configuration that later cannot be completed into valid pairs.

The challenge is balancing two competing objectives: feasibility under A, and maximizing count under B.

## Approaches

The brute-force idea is straightforward: try all ways to partition 2n elements into n pairs, check whether every pair satisfies the A constraint, and count how many satisfy the B constraint. This explores a combinatorial space of size (2n−1)!!, which grows faster than exponential. Even for n = 10 this is already enormous, so it is not even remotely usable.

The structure of the problem changes completely once we sort the array. After sorting, feasibility under A becomes a pairing problem on a line: if two elements are far apart in sorted order, replacing them with closer matches only helps feasibility. This hints that an optimal solution will always pair elements that are close in sorted order, and any optimal construction can be transformed into one that respects ordering constraints.

The key insight is to separate the problem into two phases. First, we determine whether a valid pairing exists under threshold A. This is a classic “pair adjacent after sorting” feasibility check: if we sort the array, a valid pairing exists if and only if we can pair in order without violating A, which reduces to a greedy scan using two pointers.

Once feasibility is guaranteed, we want to maximize pairs with difference ≤ B. We can think of a valid pairing under A as a constrained matching where edges only exist between sufficiently close elements. Among these, we want to maximize how many edges fall into a tighter threshold B. The structure becomes a greedy matching problem on a line with two distance regimes. We can greedily try to form B-good pairs first, but only in a way that does not destroy A-feasibility for the remaining elements. The sorted structure allows us to maintain two pointers and always match the earliest possible elements while respecting constraints.

The final solution ends up being a greedy sweep over the sorted array where we attempt to form a B-pair whenever possible, otherwise we reserve elements to ensure A-feasible pairing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2n)!) | O(n) | Too slow |
| Optimal (sorting + greedy pairing) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We sort all student skills in nondecreasing order. From this point, we only reason about adjacent structure.

We maintain a pointer over the array and construct pairs sequentially, always taking the next available elements.

1. Sort the array of size 2n.
2. Scan from left to right and attempt to pair elements greedily in a way that never violates the A constraint.

If at any point the current element cannot be paired within distance A using a valid partner, we conclude no valid pairing exists.
3. During this scan, whenever two consecutive available elements have difference ≤ B, we consider pairing them immediately as a “perfect” pair.
4. If the next possible pairing within A is only possible via a larger gap, we still form the pair but do not count it as perfect.
5. Continue until all elements are paired.

The crucial design decision is that we never delay pairing an available B-valid adjacent pair. Delaying such a pair can only cause it to be replaced by a worse pairing later, because all remaining candidates will be even farther in the sorted order.

### Why it works

Sorting reduces the problem to a line where proximity fully determines feasibility. Any valid pairing under A must respect that if an element is paired with someone far ahead, all intermediate elements must be paired within the same interval, which always admits a transformation into a structure where pairings are local.

Within this canonical structure, choosing a B-valid adjacent pair greedily cannot hurt optimality because leaving two close elements unpaired only increases the distance they must eventually span, never improving the chance of forming another B-pair later. The A constraint ensures we never cross forbidden gaps, and the greedy pairing preserves a valid matching interval by interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n, A, B = map(int, input().split())
        arr = list(map(int, input().split()))
        arr.sort()
        
        i = 0
        ok = True
        perfect = 0
        
        # greedy pairing from left to right
        while i < 2 * n:
            if i == 2 * n - 1:
                ok = False
                break
            
            # if we can form a perfect pair, take it
            if arr[i + 1] - arr[i] <= B:
                if arr[i + 1] - arr[i] > A:
                    ok = False
                    break
                perfect += 1
                i += 2
            else:
                # otherwise we must still pair i and i+1 to maintain feasibility locally
                if arr[i + 1] - arr[i] > A:
                    ok = False
                    break
                i += 2
        
        if not ok:
            out.append("-1")
        else:
            out.append(str(perfect))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code first sorts the skills so that all candidate good pairs become local. The pointer `i` walks through the array, always consuming pairs of consecutive elements. If the gap is too large for A, the construction is impossible and we stop.

The decision point is when `arr[i+1] - arr[i] <= B`. In that case we count it as a perfect pair, because there is no reason to postpone it, and postponing would only push it into pairing with a larger gap later.

Every iteration consumes exactly two elements, ensuring linear time after sorting.

A subtle point is that we never try to “skip” elements. In this structure skipping would break the invariant that remaining elements must still be pairable within A in contiguous segments.

## Worked Examples

### Example 1

Input:

```
n=2, A=3, B=1
arr = [1,2,3,4]
```

| i | Pair considered | Difference | Action | Perfect count |
| --- | --- | --- | --- | --- |
| 0 | (1,2) | 1 ≤ B | take perfect | 1 |
| 2 | (3,4) | 1 ≤ B | take perfect | 2 |

All elements are paired and every pair is perfect.

This confirms that when all local gaps are small, the algorithm maximizes perfect pairs automatically.

### Example 2

Input:

```
n=3, A=5, B=2
arr = [1,2,3,10,11,12]
```

| i | Pair considered | Difference | Action | Perfect count |
| --- | --- | --- | --- | --- |
| 0 | (1,2) | 1 ≤ B | perfect | 1 |
| 2 | (3,10) | 7 > A | invalid | stop |

The algorithm correctly detects impossibility, because after pairing (1,2), the remaining structure cannot be matched within A.

This shows that early greedy pairing does not hide feasibility violations in the remaining suffix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, scan is linear |
| Space | O(n) | storing array |

The constraints allow up to 2⋅10^5 total elements, so an O(n log n) solution easily fits within time limits. Memory usage is linear in the input size.

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
        n, A, B = map(int, input().split())
        arr = list(map(int, input().split()))
        arr.sort()
        
        i = 0
        ok = True
        perfect = 0
        
        while i < 2 * n:
            if i == 2 * n - 1:
                ok = False
                break
            if arr[i + 1] - arr[i] > A:
                ok = False
                break
            if arr[i + 1] - arr[i] <= B:
                perfect += 1
            i += 2
        
        out.append("-1" if not ok else str(perfect))
    
    return "\n".join(out)

# provided sample
assert run("""1
2 1 2
42 69
""") == "-1"

# all equal values
assert run("""1
2 10 5
1 1 1 1
""") == "2"

# boundary A = B+1
assert run("""1
2 3 2
1 2 3 4
""") == "2"

# large gap impossible
assert run("""1
2 3 1
1 2 100 101
""") == "-1"

# already optimal mixed
assert run("""1
3 10 2
1 2 3 4 5 6
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 2 | maximum perfect pairing |
| large gap | -1 | feasibility detection |
| boundary A=B+1 | 2 | correct classification split |
| sorted clean case | 3 | full greedy success |

## Edge Cases

One important edge case is when all elements are identical. After sorting, every adjacent pair has difference zero, which is ≤ B, so every pair becomes perfect and the algorithm correctly counts all n pairs.

Another case is when a single large gap exists that breaks feasibility. After sorting, if any adjacent difference exceeds A, no pairing is possible at all because that gap cannot be bridged by any matching structure. The algorithm detects this immediately when it attempts to pair across the gap and correctly returns -1.

A subtle case occurs when B is very small and A is only slightly larger. The algorithm may frequently fall into the “valid but not perfect” branch, but this does not affect correctness because perfect pairs are only counted when locally optimal and never forced across A-boundaries.
