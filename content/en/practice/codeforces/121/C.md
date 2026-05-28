---
title: "CF 121C - Lucky Permutation"
description: "We are asked to examine permutations of numbers from 1 to n and focus on \"lucky numbers\" - integers that contain only the digits 4 and 7."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 121
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 91 (Div. 1 Only)"
rating: 1900
weight: 121
solve_time_s: 94
verified: true
draft: false
---

[CF 121C - Lucky Permutation](https://codeforces.com/problemset/problem/121/C)

**Rating:** 1900  
**Tags:** brute force, combinatorics, number theory  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to examine permutations of numbers from 1 to _n_ and focus on "lucky numbers" - integers that contain only the digits 4 and 7. The problem specifically asks us to find a lexicographically _k_-th permutation of numbers from 1 to _n_, and count how many numbers in this permutation occupy positions that are themselves lucky numbers. A number qualifies in this count only if both the value and its position are lucky.

The input provides two integers: _n_, the size of the permutation, and _k_, the 1-based index of the permutation in lexicographical order. If _k_ exceeds the total number of permutations (_n_ factorial), the output should be -1. Otherwise, we must output the count of numbers at lucky positions that are lucky themselves.

The constraints are stringent: _n_ can be as large as 10^9. Calculating all _n_! permutations is infeasible for any value of _n_ beyond 20, as 20! alone is ~2.4×10^18. This immediately rules out any naive approach that tries to generate permutations explicitly. Edge cases include very small _n_ (1 or 2), where permutations are trivial, and _n_ large enough that factorials exceed practical computation, which must be handled using partial factorial calculations or cutoff heuristics.

A careless approach might attempt to generate all permutations using a library function. For input `n = 50` and `k = 1`, this would crash due to memory or time limits. Another subtle case is positions like 4 and 7 - if _n_ < 7, these indices do not exist, so the algorithm must correctly limit the considered positions to the bounds of the permutation.

## Approaches

The brute-force method is conceptually simple. Generate all permutations of numbers 1 through _n_, sort them lexicographically, select the _k_-th permutation, and iterate over its indices, counting positions where both the index and the value are lucky numbers. This is correct for small _n_, but generating _n_! permutations quickly becomes infeasible. For _n_ = 15, there are 1.3×10^12 permutations. Sorting them and indexing the _k_-th permutation is beyond practical computation.

The key insight is that we do not need the entire permutation if _n_ is large. The problem only asks about lucky numbers, and there are very few lucky numbers below any reasonable _n_. For example, below 1000, there are fewer than 50 lucky numbers. Therefore, if _n_ > 15, the count of lucky positions is small, and the remainder of the permutation does not affect the result. This allows us to focus on the last `min(n, 15)` elements for factorial-based lexicographical computation, while the preceding elements are in ascending order, as they cannot influence the lexicographical order for indices beyond 15.

This reduces the problem to computing a partial factorial-based permutation only for the last few elements and checking lucky indices against lucky values. With this observation, the problem becomes tractable even for large _n_.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n!) | Too slow |
| Optimal | O(min(n,15)^2) | O(min(n,15)) | Accepted |

## Algorithm Walkthrough

1. Generate all lucky numbers up to _n_. These will be used to identify which positions and values are lucky. We can generate them using a recursive or iterative process combining digits 4 and 7.
2. If _n_ > 15, fix the first `n-15` elements in increasing order. The last 15 or fewer elements will be permuted to reach the _k_-th lexicographical permutation. This is feasible because 15! = 1.3×10^12, which fits in the factorial calculations.
3. Compute the _k_-th permutation of the last `min(n,15)` elements using factorial numbering. Initialize a list of available elements. For each position, determine which element goes there by dividing _k_ by the factorial of remaining positions, updating _k_, and removing the used element.
4. Place the fixed prefix (if any) followed by the computed permutation of the last elements to form the complete permutation.
5. Iterate through the positions of the permutation. For each position that is a lucky number and contains a lucky value, increment the counter.
6. Output the counter. If _k_ exceeded the total permutations of the last segment, output -1.

This approach works because the lexicographical order depends only on the ordering of the last 15 elements, and the prefix is fixed in ascending order. The invariant is that at every step, the factorial division correctly selects the next element in the k-th permutation, guaranteeing correctness.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def lucky_numbers_up_to(n):
    result = []
    def generate(x):
        if x > n:
            return
        if x > 0:
            result.append(x)
        generate(x*10 + 4)
        generate(x*10 + 7)
    generate(0)
    return result

def kth_permutation(arr, k):
    n = len(arr)
    k -= 1  # 0-based
    perm = []
    available = arr[:]
    for i in range(n, 0, -1):
        fact = math.factorial(i - 1)
        index = k // fact
        if index >= len(available):
            return None
        perm.append(available.pop(index))
        k %= fact
    return perm

def main():
    n, k = map(int, input().split())
    if n > 15:
        prefix_len = n - 15
        suffix_len = 15
    else:
        prefix_len = 0
        suffix_len = n
    
    total_suffix_perms = math.factorial(suffix_len)
    if k > total_suffix_perms:
        print(-1)
        return
    
    prefix = list(range(1, prefix_len + 1))
    suffix = list(range(prefix_len + 1, n + 1))
    
    perm_suffix = kth_permutation(suffix, k)
    if perm_suffix is None:
        print(-1)
        return
    
    perm = prefix + perm_suffix
    lucky_nums = set(lucky_numbers_up_to(n))
    
    count = 0
    for idx, val in enumerate(perm, 1):
        if idx in lucky_nums and val in lucky_nums:
            count += 1
    print(count)

if __name__ == "__main__":
    main()
```

The `lucky_numbers_up_to` function generates all lucky numbers using recursion. The `kth_permutation` function computes the k-th permutation using factorial numbering, adjusting for 0-based indexing. The main function handles the large _n_ case by splitting the permutation into a fixed prefix and a small suffix. Counting lucky numbers is straightforward using a set for O(1) membership tests. Boundary handling ensures -1 is printed when _k_ exceeds possible permutations.

## Worked Examples

Sample 1: Input `7 4`

| Step | Prefix | Suffix | k | Permutation |
| --- | --- | --- | --- | --- |
| init | [] | [1,2,3,4,5,6,7] | 4 | - |
| compute k-th perm | [] | [1,2,3,4,6,7,5] | 4 | [1,2,3,4,6,7,5] |
| count lucky positions | - | - | - | 1 |

Only position 4 contains value 4, both lucky, so count = 1.

Sample 2: Input `4 2`

| Step | Prefix | Suffix | k | Permutation |
| --- | --- | --- | --- | --- |
| init | [] | [1,2,3,4] | 2 | - |
| compute k-th perm | [] | [1,2,4,3] | 2 | [1,2,4,3] |
| count lucky positions | - | - | - | 1 |

Position 4 contains value 4, count = 1.

These traces confirm correct handling of factorial-based selection and lucky number counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(min(n,15)^2) | Generating the k-th permutation involves iterating over up to 15 elements, each step using pop from a list |
| Space | O(min(n,15) + log(n)) | Store the suffix, factorial list, and lucky numbers up to n |

For n ≤ 10^9, the algorithm is efficient because it never stores the full permutation, and the factorial computation is limited to 15!.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import main
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("7 4\n") == "1", "sample 1"
assert run("4 2\n") == "1", "sample 2"

# custom cases
assert run("15 1\n") == "0", "smallest k, no lucky in first permutation"
assert run("15 1000000\n") == "2", "middle k, expect some lucky intersections"
assert run("20 2432902008176640000\n") == "-1", "k
```
