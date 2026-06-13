---
title: "CF 1174A - Ehab Fails to Be Thanos"
description: "We are given a multiset of integers of size exactly twice some number n. The task is to rearrange these values into a new order such that if we split the reordered array into two consecutive halves of length n, the sum of the left half is different from the sum of the right half."
date: "2026-06-13T09:43:02+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1174
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 563 (Div. 2)"
rating: 1000
weight: 1174
solve_time_s: 161
verified: false
draft: false
---

[CF 1174A - Ehab Fails to Be Thanos](https://codeforces.com/problemset/problem/1174/A)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy, sortings  
**Solve time:** 2m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of integers of size exactly twice some number n. The task is to rearrange these values into a new order such that if we split the reordered array into two consecutive halves of length n, the sum of the left half is different from the sum of the right half. If no such rearrangement exists, we must report failure.

The key point is that we are not asked to optimize anything beyond this inequality condition. We are free to permute arbitrarily, so the structure of the solution depends entirely on how we can influence the two half sums through ordering.

The constraint n ≤ 1000 means the array size is at most 2000. This is small enough that sorting or linear scans are trivial, and even O(n²) constructions would pass. The important part is reasoning about sum structure rather than computational efficiency.

A subtle edge case appears when all elements are identical. For example, if the array is [5, 5, 5, 5], any partition into two halves produces equal sums because both halves contain the same multiset. In this case, no solution exists.

Another edge case arises when the array has very small variation, such as [1, 1, 1, 2]. A naive intuition might suggest that some clever interleaving could still equalize sums, but in fact we can always break equality unless all values are identical.

The core difficulty is recognizing when symmetry forces equality regardless of permutation.

## Approaches

A brute-force approach would attempt to permute the array and check whether a valid split exists. There are (2n)! permutations, and even evaluating one permutation is O(n), making this completely infeasible.

Even if we reduce to sampling permutations, we are still missing structure. The real observation is that the only way all permutations fail is when every element is identical. In that case, every half has identical sum n · x, so equality is unavoidable.

If at least two distinct values exist, we can deliberately construct two halves with different sums. The simplest way is to sort the array. After sorting, the smallest values are concentrated at the beginning and the largest at the end. Splitting after n elements guarantees that the second half contains at least one strictly larger element than anything in the first half, or vice versa depending on distribution. This creates a strict imbalance in sums.

More concretely, sorting ensures that we maximize separation between halves. The first half is biased toward smaller values, the second toward larger values, which forces a sum gap.

Thus, the problem reduces to a simple check for uniformity followed by sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O((2n)!) | O(n) | Too slow |
| Sort + Construct | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the array and check whether all elements are equal. If they are, output -1 because every permutation produces identical half sums, making inequality impossible.
2. Sort the array in non-decreasing order. This creates a structure where small values are grouped on the left and large values on the right.
3. Output the sorted array directly. The split into two halves of size n will now compare a lower-weight half against a higher-weight half.
4. Terminate.

### Why it works

Sorting creates a monotone arrangement where every element in the first half is less than or equal to every element in the second half. Since at least one strict inequality exists when the array is not uniform, the second half contains a strictly larger total contribution. This guarantees the sums of the two halves cannot match, because replacing any element in the first half with a larger one strictly increases the sum of the second half relative to the first.

The correctness hinges on the fact that equality of all elements is the only configuration that removes all possible strict ordering between halves.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    if len(set(a)) == 1:
        print(-1)
        return
    
    a.sort()
    print(*a)

if __name__ == "__main__":
    solve()
```

The solution first reads n and the 2n elements. The uniformity check using a set is crucial because it directly captures the only impossible case. Without it, sorting alone would still output a valid permutation, but we would fail on the all-equal edge case.

Sorting is the constructive step that enforces separation between small and large values. Printing the array as-is after sorting is sufficient because the problem does not require explicitly forming halves, only ensuring that such a split would have unequal sums.

A common mistake is trying to interleave elements or build alternating patterns. These are unnecessary because they do not improve the guarantee beyond what sorting already provides.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [1, 2, 2, 1, 3, 1]
```

Sorted array:

```
[1, 1, 1, 2, 2, 3]
```

| Step | Array state | First half sum | Second half sum |
| --- | --- | --- | --- |
| Sorted | 1 1 1 2 2 3 | 3 | 7 |

The first half contains only small values while the second half contains the largest element 3 and two 2s. This ensures the second sum is strictly larger.

### Example 2

Input:

```
n = 2
a = [4, 4, 4, 4]
```

| Step | Array state | First half sum | Second half sum |
| --- | --- | --- | --- |
| Check | all equal | 8 | 8 |

Since all values are identical, every partition yields equal sums. No rearrangement can change this, so the output is -1.

This confirms the only failure mode is complete uniformity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(1) extra | In-place sort aside from input storage |

The constraints allow up to 2000 elements, so sorting is trivially fast. The solution runs comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    if len(set(a)) == 1:
        print(-1)
        return
    a.sort()
    print(*a)

# provided sample
assert run("3\n1 2 2 1 3 1\n") != "-1"

# all equal
assert run("2\n5 5 5 5\n") == "-1", "all equal case"

# minimal n=1
assert run("1\n1 2\n") in ["1 2", "2 1"], "minimum case"

# already sorted
assert run("2\n1 2 3 4\n") == "1 2 3 4", "already sorted case"

# reverse order
assert run("2\n4 3 2 1\n") == "1 2 3 4", "reverse case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | -1 | impossibility condition |
| n=1 case | any valid order | smallest valid structure |
| sorted input | sorted output | stability of construction |
| reversed input | sorted output | correctness under permutation |

## Edge Cases

The most important edge case is when all elements are identical. For an input like:

```
3
7 7 7 7 7 7
```

The algorithm detects `len(set(a)) == 1` and immediately outputs -1. If we skipped this check and printed the array, both halves would sum to 3 × 7 = 21, violating the condition.

For a near-uniform case such as:

```
3
1 1 1 1 1 2
```

The set size is greater than 1, so we proceed to sorting:

```
1 1 1 1 1 2
```

Half sums become:

first half = 3, second half = 4, so the condition holds. This shows that even a single deviation from uniformity is enough to guarantee a valid split after sorting.

This behavior confirms that the construction only fails in the fully symmetric case and succeeds otherwise.
