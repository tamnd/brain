---
title: "CF 1365B - Trouble Sort"
description: "We are given a sequence of numbers ai each tagged with a type bi that is either 0 or 1. The task is to determine if it is possible to sort the sequence in non-decreasing order by only swapping elements of different types."
date: "2026-06-11T12:15:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1365
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 648 (Div. 2)"
rating: 1300
weight: 1365
solve_time_s: 105
verified: true
draft: false
---

[CF 1365B - Trouble Sort](https://codeforces.com/problemset/problem/1365/B)

**Rating:** 1300  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers `a_i` each tagged with a type `b_i` that is either 0 or 1. The task is to determine if it is possible to sort the sequence in non-decreasing order by only swapping elements of different types. In other words, a swap is allowed between positions `i` and `j` only if `b_i != b_j`. The input consists of multiple test cases, each with the length of the array, the values array, and the type array. The output should be "Yes" if sorting is possible under these constraints, or "No" otherwise.

Given the constraints, `n` can be up to 500 and there can be up to 100 test cases. Sorting each sequence directly is fast, but simulating all possible swaps would be far too slow because the number of potential swaps grows combinatorially. We need a more analytical approach to determine if sorting is feasible without actually performing all swaps.

A subtle edge case occurs when all elements are of the same type. In that scenario, no swaps are allowed, so the array can only be considered sortable if it is already in non-decreasing order. For example, if `a = [3, 1, 2]` and `b = [0, 0, 0]`, the correct output is "No" because no swaps can occur. A careless approach might ignore type constraints and incorrectly say "Yes" after sorting the array internally.

## Approaches

A brute-force approach would attempt every sequence of valid swaps until the array becomes sorted or all possibilities are exhausted. This is correct in principle, because any sequence of swaps allowed by the rules could eventually sort the array. However, the number of swaps grows exponentially with `n`, making this method infeasible even for `n = 20`. The worst-case scenario could involve checking factorial combinations of swaps, far exceeding the allowed computation time.

The key insight is to notice that the only thing that can block sorting is a lack of type diversity. If there is at least one element of type 0 and one of type 1, we can effectively swap any pair of elements by repeatedly using intermediate swaps, which allows full reordering. If the array contains both types, the answer is trivially "Yes". If all elements have the same type, the answer is "Yes" only if the array is already sorted.

This observation reduces the problem to a simple check: either the array is already sorted, or it contains both types. No actual swapping simulation is necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n!)^2) | O(n) | Too slow |
| Optimal | O(n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`, the array `a`, and the type array `b`.
2. Check if the array `a` is already sorted in non-decreasing order. If it is, print "Yes" and move to the next test case. Sorting is trivially possible in this case.
3. If the array is not sorted, check if both type 0 and type 1 are present in the array `b`. If both types exist, print "Yes" because any permutation of `a` can be achieved using swaps between different types.
4. If only one type exists and the array is not already sorted, print "No". Sorting is impossible because no swaps are allowed.
5. Repeat for all test cases.

Why it works: The invariant is that having both types allows any element to be swapped indirectly with any other element through a sequence of allowed swaps. This guarantees that any unsorted array can be transformed into the sorted order. If only one type exists, no swaps are allowed, so the sortedness of the array is the only criterion.

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
        
        if a == sorted(a):
            print("Yes")
            continue
        
        has_zero = 0 in b
        has_one = 1 in b
        
        if has_zero and has_one:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    solve()
```

This solution first checks whether the array is already sorted to handle trivial cases quickly. It then scans the type array to see if both types exist. The check `0 in b` and `1 in b` is simple and sufficient because the only thing that matters is the presence of both types, not their counts.

## Worked Examples

### Sample Input 1

```
4
10 20 20 30
0 1 0 1
```

| Step | a | sorted(a) | has_zero | has_one | Output |
| --- | --- | --- | --- | --- | --- |
| Initial | [10,20,20,30] | [10,20,20,30] | True | True | Yes |

Array is already sorted, so no swaps are needed.

### Sample Input 2

```
3
3 1 2
0 1 1
```

| Step | a | sorted(a) | has_zero | has_one | Output |
| --- | --- | --- | --- | --- | --- |
| Initial | [3,1,2] | [1,2,3] | True | True | Yes |

Array is unsorted, but both types exist. Swaps between different types allow full reordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Checking sortedness and presence of both types requires linear scans. |
| Space | O(n) | Storing the arrays `a` and `b`. No extra structures are needed. |

Given `n <= 500` and `t <= 100`, the worst-case total operations are 50,000, which fits well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("5\n4\n10 20 20 30\n0 1 0 1\n3\n3 1 2\n0 1 1\n4\n2 2 4 8\n1 1 1 1\n3\n5 15 4\n0 0 0\n4\n20 10 100 50\n1 0 0 1\n") == "Yes\nYes\nYes\nNo\nYes"

# Custom cases
assert run("1\n1\n100\n0\n") == "Yes", "single element"
assert run("1\n3\n2 1 3\n1 1 1\n") == "No", "all same type, unsorted"
assert run("1\n3\n2 1 3\n0 1 0\n") == "Yes", "mixed types, unsorted"
assert run("1\n5\n5 5 5 5 5\n0 0 0 0 0\n") == "Yes", "all equal elements"
assert run("1\n2\n2 1\n0 0\n") == "No", "two elements same type, unsorted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | Yes | Trivial sorted array |
| 3 elements same type, unsorted | No | Cannot swap |
| 3 elements mixed types, unsorted | Yes | Swaps allowed |
| 5 elements all equal | Yes | Already sorted |
| 2 elements same type, unsorted | No | Minimal unsorted with single type |

## Edge Cases

When all elements are the same type, no swaps can occur. For example, `a = [3, 1, 2]` and `b = [0, 0, 0]`. The array is unsorted, `0 in b` is True, `1 in b` is False, so the algorithm prints "No". If an array is already sorted, such as `a = [1, 2, 2]` with `b = [1, 1, 1]`, it prints "Yes". When both types exist, like `a = [4, 3, 2]` and `b = [0, 1, 0]`, the algorithm prints "Yes" because swaps allow reordering. These cases confirm the correctness for all subtle input configurations.
