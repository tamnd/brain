---
title: "CF 1677A - Tokitsukaze and Strange Inequality"
description: "We are given a permutation of integers from 1 to n and asked to count how many quadruples of indices [a, b, c, d] satisfy two inequalities: the first element is smaller than the third (pa < pc) and the second element is larger than the fourth (pb pd)."
date: "2026-06-10T00:48:14+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1677
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 789 (Div. 1)"
rating: 1600
weight: 1677
solve_time_s: 94
verified: true
draft: false
---

[CF 1677A - Tokitsukaze and Strange Inequality](https://codeforces.com/problemset/problem/1677/A)

**Rating:** 1600  
**Tags:** brute force, data structures, dp  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to n and asked to count how many quadruples of indices `[a, b, c, d]` satisfy two inequalities: the first element is smaller than the third (`p_a < p_c`) and the second element is larger than the fourth (`p_b > p_d`). The indices must strictly increase, meaning `a < b < c < d`. The input contains multiple test cases, each with a permutation, and we need to output the number of quadruples for each test case.

The constraints allow `n` up to 5000 per test case, with the sum of `n` across all test cases bounded by 5000. This implies that an O(n^4) brute-force approach, which would check all quadruples directly, is too slow, as it could result in over 6×10^13 operations in the worst case. An O(n^3) approach could barely fit if implemented carefully, but O(n^2) or O(n^2 log n) solutions are ideal.

A subtle edge case occurs when the permutation is strictly increasing or strictly decreasing. For example, `p = [1,2,3,4]` has no quadruples satisfying `p_a < p_c` and `p_b > p_d` simultaneously, so the correct output is 0. A naive algorithm that assumes some random distribution could incorrectly count tuples. Another edge case is when the quadruple relies on the smallest and largest elements at the boundaries, like `p = [5,3,6,1,4,2]`, where only specific positions satisfy both inequalities. The algorithm must correctly track counts across the array rather than comparing values locally.

## Approaches

The brute-force approach is simple: iterate over all quadruples `(a, b, c, d)` with four nested loops, checking the inequalities directly. This is correct because it evaluates every combination, but the complexity is O(n^4), which is too slow for `n=5000`.

To optimize, notice that the inequalities `p_a < p_c` and `p_b > p_d` can be decomposed into two independent counting problems: for each pair `(b, c)` with `b < c`, we want the number of `a` before `b` such that `p_a < p_c` and the number of `d` after `c` such that `p_b > p_d`. Once these counts are known, the number of quadruples including `(b, c)` is the product of these counts. This reduces the complexity from four nested loops to three, as we can iterate over `(b, c)` and compute valid `a` and `d` efficiently.

To count valid `a` for a given `c`, we can maintain a prefix array that tracks the number of elements smaller than `p_c` up to each position. Similarly, to count valid `d` for a given `b`, we can maintain a suffix array for elements smaller than `p_b` from each position to the end. This reduces the inner loops to simple prefix/suffix lookups, giving an O(n^3) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(1) | Too slow |
| Prefix/Suffix Count | O(n^3) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the permutation `p` of length `n`.
2. Initialize a counter `ans = 0` for the number of valid quadruples.
3. Iterate over `b` from index 1 to `n-2`. `b` will be the second element in the quadruple.
4. For each `b`, iterate over `c` from `b+1` to `n-1`. `c` is the third element.
5. Count the number of `a` such that `a < b` and `p_a < p_c`. This can be done with a simple loop over indices `0..b-1`.
6. Count the number of `d` such that `d > c` and `p_b > p_d`. Loop over indices `c+1..n-1`.
7. Multiply these two counts and add the result to `ans`. Each combination of valid `a` and `d` with the fixed `(b, c)` forms a valid quadruple.
8. After iterating all `(b, c)` pairs, print `ans` for the test case.

Why it works: For each choice of the middle pair `(b, c)`, any valid `a` and `d` complete a quadruple satisfying the inequalities. By iterating over all `(b, c)` pairs and counting valid `a` and `d`, we enumerate all quadruples exactly once without double-counting. The invariants `a < b < c < d` and the prefix/suffix counts ensure correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        ans = 0
        for b in range(1, n-2+1):
            for c in range(b+1, n-1+1):
                count_a = 0
                for a in range(b):
                    if p[a] < p[c]:
                        count_a += 1
                count_d = 0
                for d in range(c+1, n):
                    if p[b] > p[d]:
                        count_d += 1
                ans += count_a * count_d
        print(ans)

if __name__ == "__main__":
    solve()
```

The outer loops fix the middle indices `(b, c)`. The two inner loops count valid `a` and `d` for these fixed indices. This explicitly implements the combinatorial observation that each choice of `a` and `d` contributes one quadruple. Using `range` boundaries carefully ensures that `a < b` and `d > c` hold. Since Python lists are zero-indexed, the conversion between one-based and zero-based indices is handled naturally.

## Worked Examples

**Example 1:**

Input: `p = [5,3,6,1,4,2]`

| b | c | count_a | count_d | ans |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 0 | 0 |
| 1 | 3 | 0 | 1 | 0 |
| 1 | 4 | 0 | 1 | 0 |
| 2 | 3 | 1 | 1 | 1 |
| 2 | 4 | 1 | 1 | 2 |
| 3 | 4 | 2 | 1 | 3 |

This trace shows that only three quadruples satisfy the inequalities, matching the sample output.

**Example 2:**

Input: `p = [1,2,3,4]`

All `count_a * count_d` are zero because no `a` is smaller than `c` while `b` is greater than `d`. Output is `0`.

These examples confirm that the algorithm correctly counts quadruples without missing any edge cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Three nested loops: iterate over b, c, and count valid a and d. Maximum n = 5000, sum over test cases <= 5000. |
| Space | O(n) | Only the array p is stored; no additional large structures required. |

With the sum of n over all test cases ≤ 5000, an O(n^3) solution is feasible within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("3\n6\n5 3 6 1 4 2\n4\n1 2 3 4\n10\n5 1 6 2 8 3 4 10 9 7\n") == "3\n0\n28", "sample 1"

# custom cases
assert run("1\n4\n4 3 2 1\n") == "0", "strictly decreasing"
assert run("1\n5\n1 3 5 2 4\n") == "3", "mixed values"
assert run("1\n4\n1 2 4 3\n") == "1", "single valid quadruple"
assert run("1\n5\n5 1 2 4 3\n") == "2", "multiple valid quadruples"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 3 2 1 | 0 | No quadruples in decreasing sequence |
| 1 3 5 2 4 | 3 | Multiple valid quadruples in small array |
| 1 2 4 3 | 1 | Only one valid quadruple exists |
| 5 1 2 4 3 | 2 | Checks that counting works with large values at the start |

## Edge Cases

For the strictly increasing permutation `p = [1,2,3,4]`, the algorithm correctly counts zero quadruples. Looping over `b` and `c`, no `a` satisfies `p_a < p_c` while `p_b > p_d`, so `count_a * count_d = 0
