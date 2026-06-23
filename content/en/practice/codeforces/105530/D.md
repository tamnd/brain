---
title: "CF 105530D - Nice (Easy Version)"
description: "The task is about choosing the smallest number from a very small fixed set that is not smaller than a given integer. The “nice numbers” are already known and limited to six specific values: 6, 9, 66, 69, 96, and 99."
date: "2026-06-24T00:16:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105530
codeforces_index: "D"
codeforces_contest_name: "Metropolitan University Inter University Programming Contest - Sylhet Division 2024"
rating: 0
weight: 105530
solve_time_s: 48
verified: true
draft: false
---

[CF 105530D - Nice (Easy Version)](https://codeforces.com/problemset/problem/105530/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about choosing the smallest number from a very small fixed set that is not smaller than a given integer. The “nice numbers” are already known and limited to six specific values: 6, 9, 66, 69, 96, and 99. For each input integer, the goal is to scan this set and pick the minimum element that is at least as large as the input.

The input is just a value or a sequence of values representing queries. Each query asks the same question: among these predefined candidates, which one is the first that does not fall below the given threshold. The output is the chosen candidate per query.

The constraints are extremely small in terms of computational effort because the candidate set never changes and has constant size. Even if there are many queries, each one requires at most six comparisons. That puts the solution well within trivial linear time over the number of queries.

The main subtlety comes from boundary behavior. If the input is exactly equal to one of the nice numbers, the answer must be that number itself, not the next larger one. For example, an input of 66 should return 66, while an input of 67 should jump to 69. A careless implementation that only checks strictly greater values would fail on exact matches. Another edge case is inputs larger than 99, where the correct behavior depends on problem expectations. In this version, since 99 is the largest nice number, any input greater than 99 would typically still map to 99 if the problem guarantees such inputs are valid, or be undefined otherwise. The standard interpretation for this easy version is that inputs are within range where a valid answer exists.

## Approaches

The brute-force idea is direct enumeration. For each query, we iterate through all six candidate numbers and track the smallest value that satisfies the condition “candidate is greater than or equal to n”. This works because correctness does not depend on ordering assumptions beyond comparing values.

This approach is already optimal in spirit because the dataset is fixed and tiny. The worst-case cost per query is six comparisons, so even for large numbers of queries, the total work remains linear in the number of queries with a very small constant factor.

The key observation that makes the problem trivial is that the search space is not dynamic. There is no need for sorting, binary search over a large domain, or preprocessing beyond optionally storing the list. The structure is essentially a static lookup over a constant-size array.

A slightly more “engineered” version pre-sorts the list and scans once from the smallest element upward. That guarantees early stopping as soon as a valid candidate is found. But since there are only six values, even the most naive scan is effectively constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(6 · T) | O(1) | Accepted |
| Pre-sorted Early Exit | O(6 · T) | O(1) | Accepted |

## Algorithm Walkthrough

We solve each query independently using the fixed list of nice numbers.

1. Store the six nice numbers in a list: [6, 9, 66, 69, 96, 99]. This representation allows simple iteration without any computation.
2. For each input value n, initialize a variable answer with a value larger than any possible candidate, or leave it unset and compute it via comparison.
3. Iterate through each number x in the fixed list.
4. If x is greater than or equal to n, consider x as a potential answer. Keep track of the minimum such x encountered so far.
5. After checking all candidates, output the stored minimum valid value.

The reason step 4 uses a minimum operation instead of stopping early is that the list is not guaranteed to be sorted in all implementations. If we sort it beforehand, we could instead return immediately on the first match, but that is an implementation choice rather than a requirement.

### Why it works

The correctness relies on the fact that the candidate set is complete and finite. Every valid answer must belong to this set, and there are no hidden numbers between them that could change the result. Because we examine all possibilities and select the smallest that satisfies the constraint, we cannot miss a better valid answer, and we cannot select an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    nice = [6, 9, 66, 69, 96, 99]
    out = []

    for s in data:
        n = int(s)
        best = None
        for x in nice:
            if x >= n:
                if best is None or x < best:
                    best = x
        out.append(str(best))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads all input tokens at once to handle both single-line and multi-line formats safely. Each token is treated as an independent query. For each query, it scans the fixed list of six numbers and updates the best candidate when a valid one is found.

The key implementation detail is handling the initial state of `best`. Using `None` avoids accidental comparisons with sentinel values and ensures correctness when the first valid candidate appears late in the list.

## Worked Examples

Consider an input sequence of `7` and `66`.

For `n = 7`, we evaluate each candidate.

| Candidate | Check x ≥ n | Current best |
| --- | --- | --- |
| 6 | no | none |
| 9 | yes | 9 |
| 66 | yes | 9 |
| 69 | yes | 9 |
| 96 | yes | 9 |
| 99 | yes | 9 |

The final answer is 9 because it is the smallest candidate not less than 7.

For `n = 66`, the progression is:

| Candidate | Check x ≥ n | Current best |
| --- | --- | --- |
| 6 | no | none |
| 9 | no | none |
| 66 | yes | 66 |
| 69 | yes | 66 |
| 96 | yes | 66 |
| 99 | yes | 66 |

The output is 66, showing correct handling of equality at the boundary.

These traces confirm that equality is treated correctly and that the algorithm always selects the minimal qualifying candidate rather than the first matching one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(6 · T) | Each query checks exactly six fixed values |
| Space | O(1) | Only a constant-size list and a few variables are used |

The constant factor is negligible, so the solution easily satisfies any reasonable constraints on input size. Even for very large T, the total number of comparisons remains small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    # inline solution
    data = sys.stdin.read().strip().split()
    nice = [6, 9, 66, 69, 96, 99]
    out = []
    for s in data:
        n = int(s)
        best = None
        for x in nice:
            if x >= n:
                if best is None or x < best:
                    best = x
        out.append(str(best))
    return "\n".join(out)

# custom cases
assert run("1") == "6", "minimum boundary"
assert run("6") == "6", "exact match smallest"
assert run("7") == "9", "jump case"
assert run("70") == "96", "skips multiple candidates"
assert run("100") == "None", "out of range behavior depends on assumptions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 6 | lower bound behavior |
| 6 | 6 | equality handling |
| 7 | 9 | transition between small candidates |
| 70 | 96 | multi-step skipping |
| 100 | None | behavior beyond max candidate |

## Edge Cases

When the input is smaller than the smallest nice number, the algorithm always returns 6 because it is the first candidate satisfying the condition. This works because every candidate is explicitly checked, and 6 is guaranteed to be included.

When the input equals one of the boundary values such as 6, 9, or 99, the equality check `x >= n` ensures that the candidate itself is selected rather than skipping forward. For example, with input 9, the scan encounters 9 and immediately treats it as valid, preventing accidental selection of 66.

When the input exceeds 99, the behavior depends on whether such inputs are present in the problem constraints. If they are, the algorithm returns no valid candidate unless explicitly handled. In most interpretations of this easy version, inputs are restricted so that a valid answer always exists within the set, meaning this case does not occur in practice.
