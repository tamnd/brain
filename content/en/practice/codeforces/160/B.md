---
title: "CF 160B - Unlucky Ticket"
description: "We are given a ticket represented as a string of 2n digits, where n is between 1 and 100. The first half of the ticket contains the first n digits and the second half contains the remaining n digits. We are asked to determine whether the ticket is “definitely unlucky."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 160
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 111 (Div. 2)"
rating: 1100
weight: 160
solve_time_s: 89
verified: true
draft: false
---

[CF 160B - Unlucky Ticket](https://codeforces.com/problemset/problem/160/B)

**Rating:** 1100  
**Tags:** greedy, sortings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a ticket represented as a string of 2_n_ digits, where _n_ is between 1 and 100. The first half of the ticket contains the first _n_ digits and the second half contains the remaining _n_ digits. We are asked to determine whether the ticket is “definitely unlucky.” A ticket is definitely unlucky if it is possible to pair each digit in the first half with a digit in the second half such that either every first-half digit is strictly smaller than its paired second-half digit or every first-half digit is strictly larger than its paired second-half digit. Each digit must be used exactly once in the pairing.

The input guarantees that the total length of the ticket is at most 200 digits. This is small, which means even approaches with a quadratic time complexity could technically work, but a linearithmic solution using sorting is far more natural and efficient.

A subtle point is that the ticket could have repeated digits. For instance, the first half could be `11` and the second half `22`. Here a naive check that only compares sums or uses greedy matching without sorting could fail. Another edge case is when both halves are identical, such as `1234` split as `12` and `34`. We need to verify strict inequalities for each corresponding pair after sorting to avoid incorrect “YES” answers.

## Approaches

The brute-force approach would attempt all possible permutations of the second half to find a bijection where one of the two strict inequality conditions is satisfied. For _n_ up to 100, the number of permutations is 100!, which is astronomically large and infeasible. Brute force is conceptually correct because it checks all possible pairings, but it fails because of combinatorial explosion.

The key insight is that the relative order of digits matters more than the specific positions. If we sort both halves in ascending order, we can compare the digits pairwise: either the first-half sorted digits are all strictly smaller than the second-half sorted digits, or all strictly larger. Sorting guarantees that each smallest digit is matched against the smallest digit of the other half, which is necessary and sufficient to check the unluckiness criterion. This reduces the problem to a simple linear scan after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slow |
| Sorting + Pairwise Check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer _n_ and the ticket string of length 2_n_. Split the string into two halves, `first_half` and `second_half`. This separation allows us to reason about the two groups independently.
2. Convert each half into a list of integer digits. This makes comparisons straightforward and avoids dealing with string character codes.
3. Sort both halves in ascending order. Sorting is the core step that reduces the problem from considering all permutations to a single canonical pairing.
4. Compare the sorted digits pairwise. Initialize two flags: `all_first_less` and `all_first_greater`. For each index `i` from 0 to n-1, if the digit from `first_half` is not less than the corresponding `second_half` digit, set `all_first_less` to false. Similarly, if the digit from `first_half` is not greater than the corresponding `second_half` digit, set `all_first_greater` to false.
5. After the scan, if either `all_first_less` or `all_first_greater` remains true, print `YES`. Otherwise, print `NO`.

Why it works: Sorting ensures that each first-half digit is paired with the smallest remaining second-half digit. If any strict inequality fails after sorting, no other permutation can satisfy the condition. Therefore, the sorted comparison is necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
ticket = input().strip()

first_half = sorted(int(x) for x in ticket[:n])
second_half = sorted(int(x) for x in ticket[n:])

all_first_less = True
all_first_greater = True

for a, b in zip(first_half, second_half):
    if a >= b:
        all_first_less = False
    if a <= b:
        all_first_greater = False

print("YES" if all_first_less or all_first_greater else "NO")
```

The solution first reads the input and separates the ticket into two halves. Sorting ensures we can compare corresponding digits directly. The loop checks the strict inequality conditions simultaneously. Using `zip` is a clear and concise way to pair digits, avoiding off-by-one errors. The final conditional prints the correct result based on the flags.

## Worked Examples

Sample Input 1:

```
2
2421
```

| first_half | second_half | a >= b | a <= b | all_first_less | all_first_greater |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | True | False | False | True |
| 4 | 2 | True | False | False | True |

The algorithm outputs `YES` because `all_first_greater` remains True, confirming the ticket meets the unluckiness criterion.

Sample Input 2:

```
2
1234
```

| first_half | second_half | a >= b | a <= b | all_first_less | all_first_greater |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | False | True | True | False |
| 2 | 4 | False | True | True | False |

The algorithm outputs `YES` because `all_first_less` remains True. Sorting ensures that each smallest first-half digit is compared with the smallest second-half digit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting both halves dominates; comparison scan is linear |
| Space | O(n) | Storing the digit lists |

With n up to 100, sorting and scanning are trivial within 2 seconds. Memory usage is also minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    ticket = input().strip()
    first_half = sorted(int(x) for x in ticket[:n])
    second_half = sorted(int(x) for x in ticket[n:])
    all_first_less = True
    all_first_greater = True
    for a, b in zip(first_half, second_half):
        if a >= b:
            all_first_less = False
        if a <= b:
            all_first_greater = False
    return "YES" if all_first_less or all_first_greater else "NO"

# Provided sample
assert run("2\n2421\n") == "YES", "sample 1"

# Custom cases
assert run("2\n1234\n") == "YES", "increasing halves"
assert run("2\n1221\n") == "NO", "mixed digits"
assert run("1\n12\n") == "YES", "minimum size, first less"
assert run("1\n21\n") == "YES", "minimum size, first greater"
assert run("3\n111222\n") == "YES", "all equal in halves, first less"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n1234 | YES | Pairwise strict less condition after sorting |
| 2\n1221 | NO | Mixed digits cannot satisfy strict inequalities |
| 1\n12 | YES | Minimum n=1, first less |
| 1\n21 | YES | Minimum n=1, first greater |
| 3\n111222 | YES | Multiple equal digits, sorted comparison works |

## Edge Cases

For a ticket like `1221` (first half `12`, second half `21`), sorting produces `12` and `12`. Comparing pairwise, the first digit 1 vs 1 violates strict inequality for both less and greater, so both flags become false. The algorithm correctly outputs `NO`.

For minimum-size tickets, such as `12`, the comparison is immediate: first-half 1 < second-half 2, so `all_first_less` remains True, yielding `YES`.

For tickets with repeated digits across halves, such as `111222`, sorting ensures that the smallest digits are paired. First-half `111`, second-half `222`, all first-half digits are strictly less, producing `YES`. The algorithm handles duplicates correctly.
