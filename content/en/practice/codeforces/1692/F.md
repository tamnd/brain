---
title: "CF 1692F - 3SUM"
description: "We are given an array of positive integers, and we want to know if we can select three distinct elements whose sum ends with the digit 3. In other words, if we denote the chosen elements as $ai$, $aj$, and $ak$, then $(ai + aj + ak) mod 10 = 3$."
date: "2026-06-09T23:03:08+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1692
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 799 (Div. 4)"
rating: 1300
weight: 1692
solve_time_s: 117
verified: true
draft: false
---

[CF 1692F - 3SUM](https://codeforces.com/problemset/problem/1692/F)

**Rating:** 1300  
**Tags:** brute force, math  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers, and we want to know if we can select three distinct elements whose sum ends with the digit 3. In other words, if we denote the chosen elements as $a_i$, $a_j$, and $a_k$, then $(a_i + a_j + a_k) \mod 10 = 3$. The input consists of multiple test cases, each specifying the array size and the elements themselves, and the output is "YES" if such a triple exists or "NO" otherwise.

The constraints allow up to $2 \cdot 10^5$ total elements across all test cases. A naive triple nested loop would check $O(n^3)$ combinations per test case, which is clearly infeasible because $n^3$ could reach $10^{15}$ operations in the worst case. Even $O(n^2)$ approaches would be too slow for the largest arrays. Thus, we need a strategy that avoids iterating over every possible triple directly.

One subtlety arises because the sum is only concerned with the last digit. For instance, in an array $[11, 12, 13]$, the sums of all three-element triples modulo 10 are determined solely by the digits $[1, 2, 3]$. This indicates that we can reduce the problem to working with the last digits of each element rather than their full values, which drastically reduces the number of distinct possibilities. Another edge case to consider is when there are multiple identical numbers. For example, an array $[10, 10, 10]$ has sum 30, which ends with 0, not 3. A careless implementation might incorrectly assume that using repeated numbers always helps, but the indices must be distinct.

## Approaches

The brute-force solution is straightforward: iterate over every combination of three distinct indices and check if their sum ends with 3. This approach is guaranteed to be correct because it explicitly tests all possibilities, but it fails for large arrays due to $O(n^3)$ complexity. For instance, with $n = 2000$, this would require roughly $1.3 \cdot 10^9$ checks, which exceeds typical time limits.

The key insight is that only the last digit of each number affects the outcome. Since digits range from 0 to 9, we can reduce the array to a list of at most three occurrences per last digit. Using more than three numbers with the same last digit is unnecessary because any valid triple can be formed using at most three copies. This reduces the number of candidates to at most 30 elements. At this reduced size, we can safely apply a triple nested loop, because $30^3 = 27,000$ operations per test case are acceptable.

The story of the solution is this: brute force works but is slow because of the large array size. By observing that the problem only cares about the last digit, we can safely discard redundant numbers and reduce the array to a manageable size without losing any valid triples. This allows us to combine simplicity and correctness efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow for large n |
| Optimal | O(1) after reduction to 30 elements | O(30) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array of numbers.
2. Transform each number to its last digit using modulo 10.
3. Build a list containing at most three numbers per last digit. This step ensures we do not lose any triple that could sum to a last digit of 3, because using more than three numbers of the same digit cannot create a new sum modulo 10.
4. Enumerate all triples from the reduced list. For each triple, compute the sum of its elements modulo 10.
5. If any triple sums to a number ending in 3, immediately output "YES" for that test case and move to the next one.
6. If no valid triple is found after checking all possibilities, output "NO".

Why it works: every combination of three numbers that could potentially sum to a last digit of 3 is guaranteed to include at most three instances of each last digit. By keeping only three elements per digit, we do not remove any candidate triple. The modulo operation ensures that we only focus on the relevant part of each number, and iterating over all triples in the reduced set guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        digits = [[] for _ in range(10)]
        for num in a:
            d = num % 10
            if len(digits[d]) < 3:
                digits[d].append(d)
        
        candidates = []
        for lst in digits:
            candidates.extend(lst)
        
        found = False
        m = len(candidates)
        for i in range(m):
            for j in range(i+1, m):
                for k in range(j+1, m):
                    if (candidates[i] + candidates[j] + candidates[k]) % 10 == 3:
                        found = True
                        break
                if found:
                    break
            if found:
                break
        
        print("YES" if found else "NO")

solve()
```

The solution first groups numbers by their last digit and truncates each group to three elements. This ensures that all possible last-digit triples are preserved while keeping the candidate set small. The triple nested loop then explicitly checks sums modulo 10, avoiding any off-by-one errors with indices. Using modulo at the right moment prevents integer overflow issues for large numbers.

## Worked Examples

### Example 1

Input: `[20, 22, 19, 84]`

| Step | Candidates | Triple checked | Sum mod 10 | Result |
| --- | --- | --- | --- | --- |
| 1 | [0,2,9,4] | (0,2,9) | 11 → 1 | - |
| 2 | [0,2,9,4] | (0,2,4) | 6 → 6 | - |
| 3 | [0,2,9,4] | (0,9,4) | 13 → 3 | YES |

We successfully find a valid triple (20, 19, 84) reduced to last digits (0,9,4) summing to 13, last digit 3.

### Example 2

Input: `[12, 34, 56, 78, 90]`

| Step | Candidates | Triple checked | Sum mod 10 | Result |
| --- | --- | --- | --- | --- |
| 1 | [2,4,6,8,0] | (2,4,6) | 12 → 2 | - |
| 2 | ... | (2,4,8) | 14 → 4 | - |
| ... | ... | ... | ... | NO |

No triple sums to a last digit of 3, so the algorithm correctly outputs NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case after reduction | At most 30 candidates, triple nested loop checks at most 27,000 triples |
| Space | O(30) | The reduced candidate array plus digit buckets |

The reduction to at most 30 numbers ensures that we never exceed feasible operations even for the largest inputs. Memory usage is minimal, fitting easily within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("6\n4\n20 22 19 84\n4\n1 11 1 2022\n4\n1100 1100 1100 1111\n5\n12 34 56 78 90\n4\n1 9 8 4\n6\n16 38 94 25 18 99\n") == "YES\nYES\nNO\nNO\nYES\nYES"

# Custom cases
assert run("1\n3\n1 1 1\n") == "NO", "all equal digits"
assert run("1\n3\n1 2 0\n") == "YES", "minimum n with valid triple"
assert run("1\n6\n10 10 10 10 10 3\n") == "YES", "last digit 3 included"
assert run("1\n5\n7 7 7 7 7\n") == "NO", "no triple ends with 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 numbers all 1 | NO | Cannot form sum ending in 3 |
| 3 numbers [1,2,0] | YES | Smallest valid triple |
| 6 numbers with last digit 3 | YES | Ensures inclusion of single 3 works |
| All 7s | NO | Triple sum does not end in 3, avoids false positives |

## Edge Cases

The algorithm handles small arrays correctly by checking all triples after reduction, so even if $n=3$, it still works. For arrays with repeated numbers, such as `[10,10,
