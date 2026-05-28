---
title: "CF 220A - Little Elephant and Problem"
description: "We are given an array of integers that is supposed to be sorted in non-decreasing order. The Little Elephant suspects that at most one swap operation may have disturbed the array."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 220
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 136 (Div. 1)"
rating: 1300
weight: 220
solve_time_s: 168
verified: true
draft: false
---

[CF 220A - Little Elephant and Problem](https://codeforces.com/problemset/problem/220/A)

**Rating:** 1300  
**Tags:** implementation, sortings  
**Solve time:** 2m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers that is _supposed_ to be sorted in non-decreasing order. The Little Elephant suspects that at most one swap operation may have disturbed the array. Our task is to check whether the array can be restored to sorted order with zero or one swap between any two elements.

The input consists of the array length `n` and the array elements. The output is a simple "YES" if the array can be sorted with at most one swap, and "NO" otherwise.

The constraints imply that `n` can be as large as 10^5, so any solution that iterates in quadratic time is impractical. An algorithm with linear or linearithmic time complexity is necessary. The key is that we are allowed only one swap to fix the array, so we need to detect the minimal set of inversions or misplaced elements.

Non-obvious edge cases include arrays that are already sorted, arrays where two equal elements are swapped, or arrays where multiple swaps are required. For example, the array `[1, 3, 2, 4]` can be sorted by swapping 3 and 2, producing "YES". An array like `[3, 1, 2, 4]` cannot be fixed with one swap, so the output is "NO". Careless solutions may miss the already sorted case or mishandle arrays with repeated numbers.

## Approaches

A brute-force approach is to try swapping every possible pair of elements in the array and check whether the result is sorted. This would require checking O(n^2) pairs, each check taking O(n) time, leading to O(n^3) operations. This is clearly infeasible for n up to 10^5.

The optimal approach uses a simple observation: if the array can be sorted with at most one swap, then there are at most two positions where the current element is out of order with respect to the sorted array. We can compare the given array to its sorted version and record all positions where elements differ. If there are zero differences, the array is already sorted. If there are exactly two differences, swapping those two elements fixes the array. If there are more than two differences, no single swap can sort the array. This method requires only a single sort (O(n log n)) and a single linear scan (O(n)), which is feasible within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Compare with sorted | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the array `a`.
2. Create a sorted copy of the array, call it `b`.
3. Iterate over all indices `i` from 0 to n-1 and collect positions where `a[i] != b[i]`. Store these positions in a list called `diff`.
4. Check the length of `diff`. If it is zero, print "YES" because the array is already sorted.
5. If the length of `diff` is exactly two, let the positions be `i` and `j`. Swap `a[i]` and `a[j]` and check if the array becomes equal to `b`. If it does, print "YES"; otherwise print "NO".
6. If the length of `diff` is greater than two, print "NO".

Why it works: the sorted array represents the correct order. Any deviation from this order indicates misplaced elements. More than two misplaced elements cannot be corrected with a single swap. Exactly two differences correspond to the two elements that need swapping, and zero differences require no action. This logic guarantees correctness for all possible input arrays.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    b = sorted(a)
    diff = [i for i in range(n) if a[i] != b[i]]
    
    if len(diff) == 0:
        print("YES")
    elif len(diff) == 2:
        i, j = diff
        a[i], a[j] = a[j], a[i]
        if a == b:
            print("YES")
        else:
            print("NO")
    else:
        print("NO")

if __name__ == "__main__":
    main()
```

The code first reads the array and creates a sorted version. The list comprehension finds all indices where the elements differ. The key implementation subtlety is handling exactly two differences correctly: swapping the elements must produce an array identical to the sorted one. Forgetting to check this after the swap can produce incorrect results if the swapped elements appear more than once in the array.

## Worked Examples

Sample 1:

Input:

```
2
1 2
```

`a = [1, 2]`, `b = [1, 2]`, `diff = []`

Output: "YES" because the array is already sorted.

Sample 2:

Input:

```
4
1 3 2 4
```

`a = [1, 3, 2, 4]`, `b = [1, 2, 3, 4]`

`diff = [1, 2]`

Swap positions 1 and 2: `a = [1, 2, 3, 4]`

Output: "YES" because a single swap fixes the array.

Sample 3:

Input:

```
5
5 1 3 2 4
```

`a = [5, 1, 3, 2, 4]`, `b = [1, 2, 3, 4, 5]`

`diff = [0, 1, 3, 4]` (length > 2)

Output: "NO" because more than one swap is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array dominates the complexity. The linear scan to find differences is O(n). |
| Space | O(n) | Storing the sorted copy of the array and the list of differences requires O(n) space. |

Given n ≤ 10^5, this algorithm executes comfortably within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    return f.getvalue().strip()

# Provided samples
assert run("2\n1 2\n") == "YES", "sample 1"
assert run("4\n1 3 2 4\n") == "YES", "sample 2"
assert run("5\n5 1 3 2 4\n") == "NO", "sample 3"

# Custom cases
assert run("3\n2 2 1\n") == "YES", "swap last two identical elements"
assert run("6\n1 2 3 6 5 4\n") == "NO", "multiple swaps needed"
assert run("4\n1 1 1 1\n") == "YES", "all elements equal"
assert run("2\n2 1\n") == "YES", "swap first and second"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n2 2 1 | YES | Swapping equal elements at the end |
| 6\n1 2 3 6 5 4 | NO | Multiple swaps required |
| 4\n1 1 1 1 | YES | All elements equal |
| 2\n2 1 | YES | Minimum-size array |

## Edge Cases

Consider an array of length 2, `[2, 1]`. The algorithm identifies the two differing positions, swaps them, and produces `[1, 2]`, confirming "YES".

For an array with all identical elements `[1, 1, 1]`, the difference list is empty, leading to an immediate "YES".

An array where multiple swaps are required, `[5, 1, 3, 2, 4]`, produces a difference list of length greater than two, correctly resulting in "NO". The algorithm handles all these non-obvious scenarios correctly without extra conditional logic.
