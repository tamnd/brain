---
title: "CF 1584C - Two Arrays"
description: "We are given two integer arrays of equal length. The allowed operation on the first array is quite specific: we may choose some subset of positions and increase each chosen element by exactly one. After that, we are allowed to freely reorder the array."
date: "2026-06-10T09:36:51+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1584
codeforces_index: "C"
codeforces_contest_name: "Technocup 2022 - Elimination Round 2"
rating: 900
weight: 1584
solve_time_s: 102
verified: true
draft: false
---

[CF 1584C - Two Arrays](https://codeforces.com/problemset/problem/1584/C)

**Rating:** 900  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integer arrays of equal length. The allowed operation on the first array is quite specific: we may choose some subset of positions and increase each chosen element by exactly one. After that, we are allowed to freely reorder the array.

The question is whether we can transform the first array into the second array using exactly one such operation phase.

The reordering step is crucial because it removes any positional constraints. After the increment step, only the multiset of values matters, not where they came from. This means the problem is fundamentally about whether we can turn one multiset of integers into another by adding one to some of the elements of the first multiset.

The constraints are small, with array size up to 100 and at most 100 test cases. A direct exponential search over subsets of elements would already be borderline acceptable in raw form for a single test, but not when reasoning cleanly across all cases. Still, the small limits suggest that sorting and linear checks are likely sufficient, and any solution involving combinatorial enumeration of subsets is unnecessary.

A subtle pitfall comes from overthinking the permutation step. For example, one might try to match indices directly and decide greedily per position. That fails because the final permutation allows arbitrary reassignment.

Another common mistake is assuming we can independently decide for each position whether it must be incremented or not based on a fixed ordering. Since permutation happens after increments, the correct perspective is to compare sorted structures, not original indices.

Consider this failure mode: if we try to match elements in original order, we might incorrectly conclude impossibility even when a valid permutation exists after increments. The reordering destroys positional meaning completely.

## Approaches

A brute-force approach would try every subset of indices to increment. For each subset, we would apply the increment, then sort and compare with the target array. There are 2^n subsets, and each check costs O(n log n), which quickly becomes infeasible even if n is only 100, because the constant factor is enormous and the structure is unnecessary.

The key observation is that the operation only changes values by +1 and does not introduce any other transformations. This means each element in the final array must come from an element in the original array, either unchanged or incremented once. After sorting both arrays, we are effectively trying to decide whether each element of the target array can be matched to an element of the source array with a difference of either 0 or 1, and each +1 operation is used exactly once per selected element.

Once both arrays are sorted, the natural pairing becomes the optimal structure to test feasibility. The smallest elements must align with smallest targets; otherwise, a mismatch at the low end cannot be repaired by reordering later. This reduces the problem to a linear scan after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (subset enumeration) | O(2^n · n log n) | O(n) | Too slow |
| Sorting + greedy matching | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reduce each test case to a comparison between two sorted arrays.

1. Sort both arrays in non-decreasing order. This removes all positional ambiguity introduced by the final permutation step.
2. Compute the total difference between sums of the arrays. This value represents how many elements must have been incremented, since each operation increases the total sum by exactly one.
3. Compare corresponding elements of the sorted arrays from left to right. For each position, check whether the target value is at least the source value. If any target value is smaller, no sequence of +1 operations can fix this.
4. For each pair, compute the difference. Every difference must be either 0 or 1, since each element can be incremented at most once.
5. Verify that the total number of +1 differences matches the sum difference computed earlier.

The decision depends on consistency between local feasibility (each element can only be increased by one) and global feasibility (total increments must match required sum increase).

### Why it works

After sorting, we are pairing the smallest available values together. If a smaller element in the target array is paired with a larger element from the source, swapping partners cannot fix the mismatch because all larger source elements would only worsen future pairings. This greedy alignment ensures that if any valid transformation exists, it will appear under sorted order pairing. The restriction that each element can only be incremented by one enforces a binary choice per position in the sorted pairing, which fully characterizes the transformation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        a.sort()
        b.sort()
        
        diff_sum = 0
        ok = True
        
        for i in range(n):
            if b[i] < a[i]:
                ok = False
            diff_sum += (b[i] - a[i])
            if b[i] - a[i] > 1:
                ok = False
        
        print("YES" if ok and diff_sum == sum(b) - sum(a) else "NO")

if __name__ == "__main__":
    solve()
```

The solution starts by sorting both arrays so that we can reason about them as multisets. The loop then checks two constraints simultaneously: whether any target value is smaller than its paired source value, and whether any element requires more than one increment to reach its target. The accumulated difference tracks how many +1 operations would be needed if we followed this pairing.

The final comparison ensures consistency between local constraints and the global requirement that exactly `sum(b) - sum(a)` increments must be performed.

## Worked Examples

### Example 1

Input:

```
a = [-1, 1, 0]
b = [0, 0, 2]
```

After sorting:

```
a = [-1, 0, 1]
b = [0, 0, 2]
```

| i | a[i] | b[i] | b[i] - a[i] | valid |
| --- | --- | --- | --- | --- |
| 0 | -1 | 0 | 1 | yes |
| 1 | 0 | 0 | 0 | yes |
| 2 | 1 | 2 | 1 | yes |

All differences are within allowed range, and exactly two elements require increment, matching the required total increase. This confirms that a valid subset of elements can be chosen for increment.

### Example 2

Input:

```
a = [0]
b = [2]
```

After sorting:

```
a = [0]
b = [2]
```

| i | a[i] | b[i] | b[i] - a[i] | valid |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | no |

The single element would require two increments, but each element can only be increased once. This immediately violates the structure of the operation, so no transformation is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates, while the scan is linear |
| Space | O(n) | Storage for arrays |

Given n up to 100 and t up to 100, this easily fits within limits. Even the sorting overhead is negligible at this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(sys.stdin.readline())
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        b = list(map(int, sys.stdin.readline().split()))
        
        a.sort()
        b.sort()
        
        ok = True
        total_diff = 0
        
        for i in range(n):
            if b[i] < a[i]:
                ok = False
            if b[i] - a[i] > 1:
                ok = False
            total_diff += (b[i] - a[i])
        
        required = sum(b) - sum(a)
        output.append("YES" if ok and total_diff == required else "NO")
    
    return "\n".join(output)

# provided samples
assert run("""3
3
-1 1 0
0 0 2
1
0
2
5
1 2 3 4 5
1 2 3 4 5
""") == """YES
NO
YES"""

# all equal
assert run("""1
4
1 1 1 1
1 1 1 1
""") == "YES"

# impossible large jump
assert run("""1
3
0 0 0
3 0 0
""") == "NO"

# requires multiple increments but not allowed per element
assert run("""1
2
0 1
2 1
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal arrays | YES | zero-operation case |
| large single jump | NO | element cannot exceed +1 |
| mixed mismatch | NO | per-element constraint enforcement |

## Edge Cases

A common edge case is when the total sum difference matches the number of elements but one element requires more than one increment. For example, transforming `[0, 0]` into `[2, 0]` has equal sums difference 2, but still fails because a single element would need two increments. Sorting makes this failure visible immediately since one pair becomes `(0, 2)`.

Another edge case occurs when values are equal in total but mismatched locally. For instance, `[1, 3]` to `[2, 2]` preserves sum, but sorted pairing produces `(1, 2)` and `(3, 2)`, revealing a violation where a target is smaller than a source, which cannot be repaired by permutation.

The algorithm correctly rejects both cases because it enforces both local feasibility per element and global consistency through sum tracking.
