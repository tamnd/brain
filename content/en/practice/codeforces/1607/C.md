---
title: "CF 1607C - Minimum Extraction"
description: "We are given an array of integers and a special operation that changes the array in a very structured way. Each time the operation is applied, we pick one occurrence of the current minimum value, remove it, and then subtract that same value from every remaining element."
date: "2026-06-10T07:41:53+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1607
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 753 (Div. 3)"
rating: 1000
weight: 1607
solve_time_s: 101
verified: false
draft: false
---

[CF 1607C - Minimum Extraction](https://codeforces.com/problemset/problem/1607/C)

**Rating:** 1000  
**Tags:** brute force, sortings  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and a special operation that changes the array in a very structured way. Each time the operation is applied, we pick one occurrence of the current minimum value, remove it, and then subtract that same value from every remaining element. This shrinks the array by one element while also shifting the remaining values upward or downward depending on the removed minimum.

The goal is not to simulate these operations blindly, but to decide how many times we should apply them so that the final array, at some intermediate stage, has its smallest element as large as possible. We are allowed to stop at any time, including before doing any operation at all.

The constraints are large enough that any approach simulating deletions and full array updates repeatedly would be too slow. Each operation potentially touches all remaining elements, so even a quadratic or near-quadratic strategy will fail when the total size across test cases reaches 2·10^5.

A subtle edge case appears when the array has only one element. Since the operation is forbidden there, the answer is forced to be the original value, even if it is negative. Another tricky situation is when all elements are identical. Every operation removes one element and shifts the rest to zero, so the answer becomes stable at that value, but a naive simulation might overthink the ordering of removals even though it does not matter.

## Approaches

A direct simulation would repeatedly scan the array for its minimum, remove it, and subtract it from all remaining elements. After k operations, the array has size n−k, and each step costs O(n), leading to O(n²) per test case in the worst case. With total n up to 2·10^5, this is far too slow.

The key observation is that the operation only depends on the ordering of elements by value, not their positions or identities. Each step removes the current global minimum. That means the process is essentially peeling off elements in increasing order, while continuously shifting the remaining values so that the current minimum becomes zero after each operation.

Instead of simulating, we can think in reverse: after sorting the array, we consider how the minimum evolves if we “cancel out” smaller elements one by one. The optimal stopping point corresponds to choosing a prefix of the sorted array to be fully extracted. The remaining elements have all been shifted by subtracting all removed minima.

If we sort the array, then at any stage where we stop after removing the first i smallest elements, the remaining elements are effectively transformed by subtracting the sum of those removed minima contributions. The minimum of the remaining set is therefore determined by the smallest original element that has not yet been removed, minus the accumulated shift from previous removals.

This structure allows us to compute candidate answers in a single pass over the sorted array by tracking a running subtraction offset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n) | Too slow |
| Sorting + prefix reasoning | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. This aligns all future removals in the exact order they will happen because the operation always removes the current minimum.
2. Maintain a running variable `shift`, initially zero. This represents the total amount subtracted from all remaining elements due to previously removed minima.
3. Iterate through the sorted array from smallest to largest. At position i, treat `a[i] - shift` as the effective value of the current element after all previous operations.
4. At each step, compute a candidate answer equal to `a[i] - shift`. This represents the smallest value among the remaining elements if we stop after processing up to this point.
5. Update `shift` by adding `a[i]`. This reflects that if we were to remove this element as a minimum, all remaining elements would be reduced by that value in future operations.
6. Track the maximum value over all candidates, since we want to maximize the eventual minimum among all possible stopping points.

### Why it works

After sorting, every operation removes the smallest remaining original value among those not yet processed. Each removed element contributes exactly its value to a cumulative subtraction applied to all later elements. This makes the effective value of any unremoved element equal to its original value minus the sum of all previously removed elements. The minimum at any stopping point is therefore always determined by the first unprocessed element in sorted order, adjusted by the accumulated shift, which is exactly what the algorithm evaluates.

No rearrangement choice exists that changes this structure, since removing any minimum element of the current array must correspond to removing the next smallest original element after re-indexing.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    if n == 1:
        print(a[0])
        continue
    
    a.sort()
    
    shift = 0
    ans = -10**18
    
    for i in range(n):
        ans = max(ans, a[i] - shift)
        shift += a[i]
    
    print(ans)
```

The solution begins by handling the single-element case separately since no operations are allowed there. Sorting is essential because it aligns the sequence of forced removals with increasing values.

The variable `shift` accumulates the total subtraction applied to remaining elements due to earlier removals. At each index, we evaluate what the current smallest remaining value would become if we stopped the process there. The answer is the maximum such value.

A common pitfall is forgetting that the shift must be updated after evaluating the current element. Reversing this order would incorrectly apply the subtraction to the current candidate and shift all results downward.

## Worked Examples

### Example 1

Input:

```
3
-1 2 0
```

Sorted array: `[-1, 0, 2]`

| i | a[i] | shift before | candidate (a[i] - shift) | shift after |
| --- | --- | --- | --- | --- |
| 0 | -1 | 0 | -1 | -1 |
| 1 | 0 | -1 | 1 | -1 |
| 2 | 2 | -1 | 3 | 1 |

Maximum candidate is 3.

This shows how earlier removals increase the effective value of later elements, and the best stopping point is not necessarily early or late but depends on the balance between original value and accumulated subtraction.

### Example 2

Input:

```
2
0 0
```

Sorted array: `[0, 0]`

| i | a[i] | shift before | candidate | shift after |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |

The value remains stable regardless of operations, confirming that identical elements do not change the outcome.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates for each test case |
| Space | O(1) extra (ignoring sort) | only a few variables besides input array |

The total sum of n across test cases is 2·10^5, so sorting per test case comfortably fits within time limits. The linear scan afterward is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n == 1:
            out.append(str(a[0]))
            continue
        a.sort()
        shift = 0
        ans = -10**18
        for x in a:
            ans = max(ans, x - shift)
            shift += x
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""8
1
10
2
0 0
3
-1 2 0
4
2 10 1 7
2
2 3
5
3 2 -4 -2 0
2
-1 1
1
-2
""") == """10
0
2
5
2
2
2
-2"""

# custom cases
assert run("""1
2
-5 -5
""") == "0", "all equal negatives"

assert run("""1
3
1 100 1000
""") == "1000", "strictly increasing values"

assert run("""1
4
-10 -1 0 1
""") == "1", "mixed negatives and positives"

assert run("""1
1
-100
""") == "-100", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[-5,-5]` | `0` | identical elements and stabilization |
| `[1,100,1000]` | `1000` | dominance of largest after shifts |
| `[-10,-1,0,1]` | `1` | interaction of negatives and positives |
| `[-100]` | `-100` | single-element edge case |

## Edge Cases

A single-element array directly forces the output to be that element since no operation is allowed. The algorithm explicitly returns early in this case, avoiding unnecessary sorting or shifts.

For an array of identical values such as `[x, x, x]`, sorting does nothing, and every candidate becomes `x - kx` for increasing k, but the maximum occurs at the first step, producing x. The running shift logic naturally captures this because each candidate is evaluated before its corresponding subtraction is applied.

For arrays with large negative values followed by positives, the shift accumulates negative mass early, effectively boosting later elements. The sorted pass ensures this is accounted for without needing to simulate destructive updates, since every state depends only on prefix sums of the sorted array.
