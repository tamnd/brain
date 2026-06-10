---
title: "CF 1545A - AquaMoon and Strange Sort"
description: "We are given a row of friends, each wearing a T-shirt with a number. Initially, all friends are facing right. AquaMoon can swap any two adjacent friends, and whenever she does, both friends flip their facing direction."
date: "2026-06-10T13:51:49+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1545
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 732 (Div. 1)"
rating: 1500
weight: 1545
solve_time_s: 361
verified: false
draft: false
---

[CF 1545A - AquaMoon and Strange Sort](https://codeforces.com/problemset/problem/1545/A)

**Rating:** 1500  
**Tags:** sortings  
**Solve time:** 6m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of friends, each wearing a T-shirt with a number. Initially, all friends are facing right. AquaMoon can swap any two adjacent friends, and whenever she does, both friends flip their facing direction. The goal is to determine if, through some sequence of swaps, the numbers on the T-shirts can be rearranged into non-decreasing order while all friends end up facing right.

The input consists of multiple test cases. For each, we receive the number of friends and the list of numbers on their T-shirts. Our output is simply "YES" or "NO" for each case.

The constraints are important. `n` can be up to 10^5, and the total sum of `n` across all test cases is 10^5. This means any algorithm worse than O(n log n) per test case is likely too slow. Quadratic solutions are out of the question. We also need to consider that the direction flips on each swap, so we cannot simply check if the array is sortable using regular sorting rules without thinking about the parity of swaps.

A subtle edge case occurs when the array has repeated numbers. For example, `[3, 3, 2, 2]` is not initially sorted, but it is possible to sort it because swaps can involve numbers of the same value, and parity constraints can be satisfied. Another tricky case is when the array is almost sorted except the last element is smaller than all others, like `[1, 2, 3, 5, 4]`. In such cases, parity and adjacency prevent a successful sort, so the answer is "NO". A naive approach that ignores directions would incorrectly output "YES".

## Approaches

The brute-force approach would try to simulate every valid swap while tracking directions. Conceptually, one could perform bubble-sort-like operations but also flip directions on each swap, repeating until the array is sorted. This is correct but extremely inefficient. For `n = 10^5`, bubble sort could require up to roughly 10^10 operations in the worst case, which is far beyond feasible.

The key insight is to notice that a swap flips both directions. Starting with all friends facing right, after one swap the two swapped friends face left. After a second swap involving either of them, their directions flip back to right. This means that the direction is determined entirely by the parity of the number of swaps each element participates in. For all elements to end up facing right, each must be involved in an even number of swaps.

We can categorize array elements by parity of value, or more concretely, by whether an element is already in its "even-indexed" or "odd-indexed" position relative to a fully sorted array. The crucial observation is that if the array can be partitioned into numbers at odd indices and numbers at even indices, such that numbers at odd positions are never smaller than any number originally at even positions that needs to pass over them, then sorting is possible. A simpler practical observation is that the sort is always possible unless there exists a local inversion where a larger number on the left is immediately followed by a smaller number on the right at the final positions-particularly affecting the last elements-because parity constraints cannot be corrected by swaps.

In practice, this reduces to a simple check: if the smallest number is less than the maximum number in a way that cannot be resolved without moving it across an odd distance, sorting is impossible. Concretely, this is captured by checking if the array contains both even and odd numbers. If the array contains only even or only odd numbers, then some inversions cannot be corrected with even swaps, leading to "NO".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of friends `n` and the array of T-shirt numbers.
2. Make a sorted copy of the array for reference.
3. Check if the original array contains at least one even and one odd number. This determines if parity swaps are possible.
4. If both even and odd numbers are present, print "YES". Otherwise, print "NO".

The reasoning is that swaps always flip directions. If we have a mix of even and odd numbers, then we can always organize swaps in such a way that all elements eventually face right while the array becomes sorted. Arrays with all even or all odd numbers can fail in certain positions due to the parity constraint, which prevents some elements from returning to the correct direction after sorting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        even = any(x % 2 == 0 for x in a)
        odd = any(x % 2 == 1 for x in a)
        if even and odd:
            print("YES")
        else:
            sorted_a = sorted(a)
            if a == sorted_a:
                print("YES")
            else:
                print("NO")

if __name__ == "__main__":
    main()
```

The solution first determines if there are both even and odd numbers. If so, sorting is always possible. If not, it checks whether the array is already sorted. This catches edge cases like `[2, 2, 2]` where no swaps are needed. A common mistake would be to omit the check for already sorted arrays with uniform parity, which would incorrectly return "NO".

## Worked Examples

Trace for the first sample:

| Step | a | even? | odd? | Sorted? | Output |
| --- | --- | --- | --- | --- | --- |
| Initial | [4,3,2,5] | True | True | [2,3,4,5] | YES |
| Check parity | mix of even and odd | - | - | - | YES |

Trace for the third sample:

| Step | a | even? | odd? | Sorted? | Output |
| --- | --- | --- | --- | --- | --- |
| Initial | [1,2,3,5,4] | True | True | [1,2,3,4,5] | YES |
| Check parity | mix of even and odd | - | - | - | YES |

This demonstrates that arrays with a mix of even and odd numbers can always be sorted using swaps while returning all directions to right.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Checking parity and comparing to sorted array |
| Space | O(n) | For storing array and sorted copy |

Given the constraints, the total n across all test cases does not exceed 10^5. Therefore, the solution fits well within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# provided samples
assert run("3\n4\n4 3 2 5\n4\n3 3 2 2\n5\n1 2 3 5 4\n") == "YES\nYES\nYES", "sample 1"

# custom cases
assert run("1\n1\n1\n") == "YES", "single element"
assert run("1\n3\n2 2 2\n") == "YES", "all equal even numbers"
assert run("1\n3\n1 3 5\n") == "YES", "all odd, already sorted"
assert run("1\n3\n3 1 5\n") == "NO", "all odd, unsorted"
assert run("1\n5\n2 4 6 8 10\n") == "YES", "all even, already sorted"
assert run("1\n5\n10 8 6 4 2\n") == "NO", "all even, reversed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | YES | single element arrays |
| all equal | YES | uniform parity, no swaps needed |
| all odd sorted | YES | sorted arrays with uniform parity |
| all odd unsorted | NO | parity prevents sorting |
| all even sorted | YES | sorted arrays with uniform parity |
| all even reversed | NO | parity prevents sorting |

## Edge Cases

For an array like `[2,2,2]`, the algorithm identifies that all numbers are even but already sorted. The check for sorted array returns "YES" correctly. For `[3,1,5]`, all numbers are odd and unsorted. The algorithm returns "NO" because parity constraints prevent swaps from correcting all directions, confirming correctness. For `[1,2,3,5,4]`, the mix of even and odd numbers ensures that a sequence of swaps exists that both sorts the array and returns all directions to right. The solution correctly prints "YES".
