---
title: "CF 1714C - Minimum  Varied Number"
description: "We are given a target sum for digits, and for each query we need to construct the smallest possible positive integer whose digits are all different and whose digit sum equals that target."
date: "2026-06-09T20:04:29+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1714
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 811 (Div. 3)"
rating: 800
weight: 1714
solve_time_s: 92
verified: true
draft: false
---

[CF 1714C - Minimum  Varied Number](https://codeforces.com/problemset/problem/1714/C)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a target sum for digits, and for each query we need to construct the smallest possible positive integer whose digits are all different and whose digit sum equals that target. Among all valid numbers that satisfy these two constraints, we want the one that is smallest in the usual numeric order.

A number is “valid” only if every digit appears at most once, so we are essentially choosing a subset of distinct digits from 1 to 9 and arranging them into the smallest possible number. Zeros do not help in minimizing anything here because including zero would only increase digit count without contributing to sum efficiency, and also the construction naturally prefers nonzero digits.

The constraints are extremely small: the sum is at most 45 and there are at most 45 test cases. A brute-force search over subsets of digits is feasible in theory since there are only $2^9 = 512$ subsets, but we must also ensure ordering produces the smallest number, which adds a combinational check per subset.

A naive approach might try permutations or backtracking over digits to match the sum. While correct, it risks unnecessary exploration of permutations that differ only in ordering, even though ordering has a deterministic optimal choice. Another potential mistake is greedily taking smallest digits first without considering that larger digits may be necessary to reach the sum exactly with uniqueness constraints.

A subtle edge case is when the sum is large, like 45. A greedy approach that tries to pack small digits first fails because it cannot reach the required sum without duplicates, for example repeatedly using 9. The correct construction must balance uniqueness with sum feasibility.

## Approaches

The brute-force view is to consider every subset of digits from 1 to 9, check whether its sum equals the target, and among all valid subsets construct the smallest number by sorting digits and interpreting them as a number. This works because the search space is tiny, but it still involves iterating over 512 subsets and computing sums repeatedly, which is unnecessary given the structure.

The key observation is that the problem is equivalent to selecting distinct digits whose sum is exactly $s$, and then arranging them in increasing order to minimize the resulting number. Once the set of digits is fixed, the best arrangement is always sorted ascending, since smaller digits should appear earlier to minimize lexicographic and numeric value simultaneously.

This reduces the problem to subset selection with a strong monotonic structure. Instead of exploring all subsets, we can greedily construct the answer from the largest digit downward. We try digits from 9 to 1, and include a digit if it does not exceed the remaining sum. This works because choosing a larger digit earlier preserves flexibility for remaining smaller digits, and ensures we minimize digit count first with high-value contributions.

The greedy process is optimal because we always prefer fewer digits over more digits, and among equal cardinality, placing smaller digits earlier gives a smaller number. The descending selection guarantees we never miss a feasible representation, since any sum up to 45 can be decomposed uniquely into distinct digits chosen this way.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | O(512 · 9) | O(1) | Accepted but unnecessary |
| Greedy from 9 to 1 | O(9) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Start from digit 9 and move downward to 1, maintaining the remaining sum $s$. We do this because larger digits reduce the number of digits needed, which is beneficial for minimizing the final number.
2. For each digit $d$, check whether $d \leq s$. If it is, select this digit and subtract it from $s$. This ensures that every chosen digit contributes exactly and does not violate the remaining required sum.
3. Continue this process until all digits have been considered. At the end, either the remaining sum becomes zero or no valid combination exists. Given the constraints $s \le 45$, a valid decomposition always exists.
4. Collect all selected digits. These digits form a valid subset with distinct values and correct sum.
5. Sort the selected digits in increasing order. This step is necessary because while we selected digits greedily in descending order for feasibility, the minimal numeric value requires ascending arrangement.
6. Output the concatenation of the sorted digits as the answer.

### Why it works

The algorithm constructs a subset of digits that sum exactly to $s$, always preferring larger digits when possible. This ensures that we minimize the number of digits in the result, since larger digits cover more sum per element. Once the subset is fixed, sorting it in ascending order yields the smallest possible number for that digit multiset. Any alternative subset either uses more digits or replaces a larger digit with smaller ones, which forces inclusion of additional digits and leads to a larger overall number.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = int(input())
    
    digits = []
    
    for d in range(9, 0, -1):
        if d <= s:
            digits.append(d)
            s -= d
    
    digits.sort()
    print("".join(map(str, digits)))
```

The implementation directly follows the greedy construction. We iterate from 9 down to 1, subtracting digits whenever possible. This ensures we pack the sum efficiently with the largest available digits first. After constructing the set, sorting is essential because the greedy selection order is not the final numeric order required for minimality.

A common mistake is to skip the sorting step and print digits in reverse selection order. That produces a valid sum but not the minimal number.

## Worked Examples

### Example 1: s = 20

We track selected digits while iterating from 9 to 1.

| Digit | Remaining Sum (before) | Take digit? | Remaining Sum (after) | Chosen set |
| --- | --- | --- | --- | --- |
| 9 | 20 | yes | 11 | {9} |
| 8 | 11 | yes | 3 | {9,8} |
| 7 | 3 | no | 3 | {9,8} |
| 6 | 3 | no | 3 | {9,8} |
| 5 | 3 | no | 3 | {9,8} |
| 4 | 3 | no | 3 | {9,8} |
| 3 | 3 | yes | 0 | {9,8,3} |

After sorting: 3, 8, 9 → output is 389.

This trace shows how the greedy method prioritizes large digits while still ensuring the exact sum is achievable.

### Example 2: s = 10

| Digit | Remaining Sum (before) | Take digit? | Remaining Sum (after) | Chosen set |
| --- | --- | --- | --- | --- |
| 9 | 10 | yes | 1 | {9} |
| 8 | 1 | no | 1 | {9} |
| 7 | 1 | no | 1 | {9} |
| 6 | 1 | no | 1 | {9} |
| 5 | 1 | no | 1 | {9} |
| 4 | 1 | no | 1 | {9} |
| 3 | 1 | no | 1 | {9} |
| 2 | 1 | no | 1 | {9} |
| 1 | 1 | yes | 0 | {9,1} |

After sorting: 1, 9 → output is 19.

This example highlights that greedy selection can leave a small remainder, and the algorithm correctly fills it with the smallest possible digit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(9 · t) | For each test case we scan digits 9 to 1 once |
| Space | O(1) | Only a small list of at most 9 digits is stored |

The computation is constant-time per test case and easily fits within limits, even for repeated queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        s = int(input())
        digits = []
        for d in range(9, 0, -1):
            if d <= s:
                digits.append(d)
                s -= d
        digits.sort()
        out.append("".join(map(str, digits)))
    return "\n".join(out)

# provided samples
assert run("4\n20\n8\n45\n10\n") == "389\n8\n123456789\n19"

# custom cases
assert run("1\n1\n") == "1"
assert run("1\n9\n") == "9"
assert run("1\n17\n") == "89"
assert run("1\n2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum nonzero case |
| 9 | 9 | single-digit upper boundary |
| 17 | 89 | need of greedy combination |
| 2 | 2 | smallest nontrivial sum |

## Edge Cases

For the smallest input $s = 1$, the algorithm iterates from 9 downwards, rejects all digits except 1, and selects only digit 1. Sorting is trivial and output is 1.

For a near-maximum case like $s = 45$, every digit from 9 to 1 is selected since their sum exactly matches 45. The resulting set is {9,8,7,6,5,4,3,2,1}, and sorting produces 123456789. The algorithm handles this cleanly because no digit is skipped.

For cases where the sum forces a non-obvious combination like $s = 17$, the greedy process picks 9 first, leaving 8, then picks 8 exactly, producing {9,8}. Sorting yields 89, which is optimal because any alternative would require more digits and thus a larger number.
