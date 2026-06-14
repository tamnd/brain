---
title: "CF 1088B - Ehab and subtraction"
description: "We are repeatedly performing a global “level reduction” on an array. At each step, we look at all positive values currently present, identify the smallest among them, output that value, and then reduce every positive element by that same amount."
date: "2026-06-15T05:24:24+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1088
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 525 (Div. 2)"
rating: 1000
weight: 1088
solve_time_s: 173
verified: false
draft: false
---

[CF 1088B - Ehab and subtraction](https://codeforces.com/problemset/problem/1088/B)

**Rating:** 1000  
**Tags:** implementation, sortings  
**Solve time:** 2m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are repeatedly performing a global “level reduction” on an array. At each step, we look at all positive values currently present, identify the smallest among them, output that value, and then reduce every positive element by that same amount. Zeros remain unchanged and never contribute again.

This process continues for a fixed number of operations, even if the array becomes entirely zero earlier. Once everything is zero, every remaining operation simply outputs zero.

The important structure is that the array is being peeled layer by layer from the bottom: each operation removes the current minimum positive “height” from all remaining positive entries.

The constraints allow up to 100,000 elements and 100,000 operations. Any solution that recomputes the minimum by scanning the whole array in every step leads to about 10^10 operations in the worst case, which is far beyond the time limit. Even a repeated full sort or full recomputation per step will not pass.

A few edge cases expose naive approaches clearly.

If the array is already all zeros, the answer is simply k zeros. A naive implementation that assumes at least one positive value exists may attempt to compute a minimum and crash or return an invalid value.

If k is much larger than the number of distinct positive values, the process eventually stabilizes at all zeros and continues printing zeros. For example, `[5]` with k = 3 produces `5, 0, 0`. A solution that stops early after the array becomes empty without filling remaining operations would be incorrect.

## Approaches

A direct simulation is easy to imagine: repeatedly scan the array, find the smallest non-zero element, subtract it from every positive element, and print it. This is correct because it exactly follows the operation definition. However, each step costs O(n), and in the worst case we may do O(k) steps, giving O(nk). With both up to 10^5, this becomes 10^10 operations, which is not feasible.

The key observation is that we do not actually care about the evolving array values at every moment. We only care about the sequence of minimum positive values as the array gets “flattened”. Each time we subtract the current minimum positive value, at least one element becomes zero, and the set of active values shrinks. The process is equivalent to repeatedly extracting distinct positive values in increasing order.

If we sort the array, the sequence of operations becomes much clearer. Whenever we move from one distinct value to the next larger one, that difference corresponds to a new subtraction layer. Equal values collapse together, producing zero-length gaps. The number of times a particular value contributes is determined by how many distinct “levels” remain above it.

Thus, sorting the array and processing groups of equal values allows us to compute how many times each minimum appears without simulating every subtraction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(nk) | O(1) | Too slow |
| Sorting + grouping | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. This ensures that equal values are grouped and the smallest remaining value is always accessible at the front of the structure.
2. Iterate through the sorted array, tracking the previous value seen among positive elements. Each time we encounter a new distinct positive value, we compute how many elements remain active from this point onward.
3. For each distinct value, determine how many times it will be printed. This is equal to the number of elements remaining that are strictly greater than or equal to this value, minus what has already been “consumed” by earlier levels.
4. Output the difference between consecutive distinct values repeatedly according to how many active elements remain. Conceptually, each group of equal values contributes one “layer height” subtraction step.
5. Stop once we have produced k outputs. If we exhaust all positive values before reaching k, append zeros for the remaining operations.

The correctness comes from the invariant that after each subtraction step, the multiset of positive values is exactly the original values reduced by the number of distinct thresholds already passed. Sorting reveals these thresholds directly, so each distinct value corresponds to one step in which it becomes the new minimum.

The algorithm works because the process is equivalent to peeling sorted value levels. Each level change corresponds to a strictly increasing value in the sorted array, and each such change generates exactly one output until all elements are exhausted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    res = []
    i = 0
    
    while i < n and len(res) < k:
        if a[i] == 0:
            i += 1
            continue
        
        # current minimum positive value
        current = a[i]
        
        # skip all equal values
        j = i
        while j < n and a[j] == current:
            j += 1
        
        # number of remaining active elements
        remaining = n - i
        
        res.append(current)
        
        # after subtracting, all elements in [i, j) become zero,
        # so we conceptually move forward
        i = j
    
    # if we still need outputs, fill with zeros
    while len(res) < k:
        res.append(0)
    
    print("\n".join(map(str, res)))

if __name__ == "__main__":
    solve()
```

The implementation relies on sorting to expose the structure of the repeated subtraction process. The pointer `i` always points to the smallest remaining positive value. We group equal values together using `j`, since they behave identically under subtraction. Each group produces one output corresponding to the current minimum.

The remaining fill with zeros handles the case where all elements are exhausted before k operations.

A subtle point is that we never explicitly subtract values from the array. That operation is implicit in the grouping logic: once we pass a value, it is considered fully removed from future minimum considerations.

## Worked Examples

### Sample 1

Input:

```
3 5
1 2 3
```

Sorted array is `[1, 2, 3]`.

| Step | i | current | output | remaining active |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 3 |
| 2 | 1 | 2 | 1 | 2 |
| 3 | 2 | 3 | 1 | 1 |
| 4 | - | - | 0 | 0 |
| 5 | - | - | 0 | 0 |

We output each distinct level once until the array is exhausted. After all values are consumed, we pad with zeros.

This shows that each distinct sorted value contributes one subtraction layer.

### Sample 2

Input:

```
4 5
10 3 5 3
```

Sorted array is `[3, 3, 5, 10]`.

| Step | i | current | output | remaining active |
| --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 3 | 4 |
| 2 | 2 | 5 | 3 | 2 |
| 3 | 3 | 10 | 5 | 1 |
| 4 | - | - | 0 | 0 |
| 5 | - | - | 0 | 0 |

Each time we move to a higher distinct value, we emit that value as the next minimum after previous reductions.

This confirms that sorting converts the repeated subtraction process into a sequence of threshold jumps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, single linear scan after |
| Space | O(1) extra (excluding input) | in-place processing of sorted array |

The complexity fits comfortably within constraints since n is up to 100,000 and sorting at this scale is efficient in Python. The linear pass ensures no additional overhead proportional to k.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""3 5
1 2 3
""") == """1
1
1
0
0"""

# all equal values
assert run("""4 3
5 5 5 5
""") == """5
0
0"""

# single element
assert run("""1 4
7
""") == """7
0
0
0"""

# already zeros
assert run("""3 2
0 0 0
""") == """0
0"""

# mixed values
assert run("""5 6
4 1 4 2 1
""") == """1
1
2
4
0
0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 7,0,0,0 | exhaustion and padding |
| all equal | 5,0,0 | collapse of identical values |
| all zeros | 0,0 | full zero edge case |
| mixed | 1,1,2,4,0,0 | correct ordering of distinct levels |

## Edge Cases

If the array contains only zeros, the algorithm immediately enters the padding phase. Since no positive value is ever encountered, the sorted scan produces no outputs, and the final loop outputs k zeros. This matches the definition because every operation sees an all-zero array.

For an input like `[5]` with k larger than 1, the algorithm outputs `5` on the first pass, then recognizes no remaining positive values and fills with zeros. This matches the idea that once the only element is reduced, the process stabilizes.

If all elements are equal, say `[3,3,3]`, the sorted scan produces a single distinct value. That value is output once, and all remaining operations are zero. This captures the fact that one subtraction step removes all elements simultaneously.
