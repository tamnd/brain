---
title: "CF 1007A - Reorder the Array"
description: "We are given an array of numbers and allowed to freely reorder them. After rearranging, we compare the new array against the original array position by position."
date: "2026-06-16T23:06:50+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "math", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1007
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 497 (Div. 1)"
rating: 1300
weight: 1007
solve_time_s: 191
verified: true
draft: false
---

[CF 1007A - Reorder the Array](https://codeforces.com/problemset/problem/1007/A)

**Rating:** 1300  
**Tags:** combinatorics, data structures, math, sortings, two pointers  
**Solve time:** 3m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of numbers and allowed to freely reorder them. After rearranging, we compare the new array against the original array position by position. A position is considered “good” if the value placed there after permutation is strictly larger than the value that originally occupied that position.

The task is to choose a permutation that maximizes the number of such good positions. In other words, we want to match elements so that as many positions as possible receive a strictly larger value than before, while still using every element exactly once.

The constraint $n \le 10^5$ immediately rules out any approach that tries all permutations, since $n!$ grows far beyond feasible limits. Even $O(n^2)$ solutions are borderline too slow in Python for this size, so the solution must be essentially linear or $n \log n$.

A naive mistake is to think locally, for each position, we can always find some larger unused element. This fails when large elements get “wasted” early.

For example, consider the array:

```
[1, 2, 3, 100, 101]
```

If we greedily assign the largest elements to the smallest positions without care, we might use 100 and 101 too early, leaving no valid improvement for intermediate positions. The correct answer depends on global matching, not local pairing.

Another subtle failure case is when duplicates dominate:

```
[5, 5, 5, 1, 1]
```

Even though there are large values, once they are assigned, the number of strictly improving matches is capped by how many strictly smaller values exist in the original structure.

The key difficulty is that we are effectively matching two copies of the array under a strict inequality constraint.

## Approaches

A brute-force approach would generate every permutation and count how many positions improve relative to the original array. For each permutation, we compare element-wise with the original array, costing $O(n)$ per permutation. Since there are $n!$ permutations, this becomes $O(n \cdot n!)$, which is completely infeasible even for $n = 10$.

The structure of the problem suggests a matching interpretation. We want to pair original values with permuted values such that $b[i] > a[i]$ for as many indices as possible, where $b$ is a permutation of $a$. This is a bipartite matching problem on a sorted multiset.

Once the arrays are sorted, we can think in terms of assigning the smallest possible “winning” elements to beat slightly smaller originals. The greedy idea becomes clear: if we always try to beat the smallest remaining original value using the smallest available larger value, we avoid wasting large numbers on already-easy matches.

This is a classic two-pointer strategy over sorted arrays. We sort the array, then try to match a larger element to a smaller element from the other end, advancing pointers carefully to maximize successful strict inequalities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot n!)$ | $O(n)$ | Too slow |
| Optimal (sorting + greedy matching) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the problem as matching elements of the array against a permuted copy of itself.

1. Sort the array in non-decreasing order. This gives a structured view where comparisons become predictable and greedy choices are safe.
2. Use two pointers: one pointer `i` representing the “smaller side” we want to beat, and another pointer `j` representing candidates that can beat it.
3. Initialize `i = 0` and `j = 0`, and maintain a counter `ans = 0`.
4. Move through the array trying to find matches. If `a[j] > a[i]`, we can form a successful pair, so we increment `ans`, and advance both pointers. This represents assigning a strictly larger value to beat the current smallest unmatched value.
5. If `a[j] <= a[i]`, then `a[j]` is not useful for beating `a[i]`, so we only advance `j`. This skips values that cannot contribute to increasing matches for this target.
6. Continue until either pointer reaches the end of the array.

The process ensures every successful match is valid and no potential improvement is skipped prematurely.

### Why it works

After sorting, any valid assignment corresponds to pairing a larger element with a smaller one. The greedy strategy always matches the smallest possible “winner” with the smallest possible “loser” it can beat. If a value cannot beat the current smallest remaining target, it also cannot beat any later (larger) target, so skipping it does not reduce optimality. This creates a monotonic matching process where each successful pair is irreversibly optimal in the sense that it preserves maximum flexibility for remaining elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort()
    
    i = 0
    j = 0
    ans = 0
    
    while i < n and j < n:
        if a[j] > a[i]:
            ans += 1
            i += 1
            j += 1
        else:
            j += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The sorting step is essential because it turns the problem into a monotone matching task. Without sorting, the greedy rule “use the smallest possible element that works” would not be well-defined.

The two-pointer loop maintains a clear separation: pointer `i` tracks the next smallest element that still needs to be beaten, while `j` searches for a candidate strictly larger than it. The condition `a[j] > a[i]` ensures strict improvement, matching the problem requirement exactly.

The key subtlety is that `i` only advances when a match is found. This guarantees that every successful increment corresponds to a unique pair and no element is reused.

## Worked Examples

### Example 1

Input:

```
7
10 1 1 1 5 5 3
```

Sorted array:

```
[1, 1, 1, 3, 5, 5, 10]
```

| i | j | a[i] | a[j] | Action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | j++ (not greater) | 0 |
| 0 | 1 | 1 | 1 | j++ | 0 |
| 0 | 2 | 1 | 1 | j++ | 0 |
| 0 | 3 | 1 | 3 | match | 1 |
| 1 | 4 | 1 | 5 | match | 2 |
| 2 | 5 | 1 | 5 | match | 3 |
| 3 | 6 | 3 | 10 | match | 4 |

Output:

```
4
```

This shows how duplicates on the left are gradually consumed by progressively larger values, and only strict improvements are counted.

### Example 2

Input:

```
4
4 4 4 4
```

Sorted array:

```
[4, 4, 4, 4]
```

| i | j | a[i] | a[j] | Action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 4 | 4 | j++ | 0 |
| 0 | 1 | 4 | 4 | j++ | 0 |
| 0 | 2 | 4 | 4 | j++ | 0 |
| 0 | 3 | 4 | 4 | j++ | 0 |

Output:

```
0
```

No element can strictly exceed another, so no valid matches exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; two-pointer scan is linear |
| Space | $O(1)$ or $O(n)$ | In-place sort or storage of array |

The constraints allow up to $10^5$ elements, so an $O(n \log n)$ solution is comfortably fast. The algorithm uses only sorting and a linear scan, both well within typical limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline()  # placeholder, replace with actual solve()

# provided samples (conceptual placeholders)
# assert run("7\n10 1 1 1 5 5 3\n") == "4\n"

# custom cases
assert run("1\n5\n") == "0\n", "single element"
assert run("3\n1 2 3\n") == "2\n", "strictly increasing"
assert run("4\n4 4 4 4\n") == "0\n", "all equal"
assert run("5\n5 1 4 2 3\n") == "4\n", "mixed permutation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | minimal boundary |
| sorted increasing | 2 | maximal matching potential |
| all equal | 0 | strict inequality constraint |
| shuffled mix | 4 | general correctness |

## Edge Cases

For a single-element array like `[7]`, the sorted array remains `[7]`. The pointer `j` cannot find any strictly greater value for `i = 0`, so no increments happen and the output remains 0.

For a uniform array such as `[2, 2, 2, 2]`, every comparison fails the strict inequality check, so the algorithm only advances `j`, never increasing `ans`. This directly reflects the impossibility of improving any position when all values are identical.
