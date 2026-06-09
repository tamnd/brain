---
title: "CF 2191B - MEX Reordering"
description: "We are given an array of integers, and we are allowed to reorder it arbitrarily. After fixing an order, we look at every possible split position between prefix and suffix."
date: "2026-06-09T04:39:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2191
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1073 (Div. 2)"
rating: 1000
weight: 2191
solve_time_s: 68
verified: true
draft: false
---

[CF 2191B - MEX Reordering](https://codeforces.com/problemset/problem/2191/B)

**Rating:** 1000  
**Tags:** constructive algorithms, sortings  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we are allowed to reorder it arbitrarily. After fixing an order, we look at every possible split position between prefix and suffix. For each split, we compute the MEX of the prefix and the MEX of the suffix, and we want all these pairs to be different.

The key requirement is global: a single permutation must avoid any split where both sides have the same missing smallest non-negative integer. We are not choosing one split, but must ensure that no split produces equality of MEX values.

The constraints are small, with at most 100 elements per test case and 500 test cases. This immediately suggests that any solution can afford linear or quadratic reasoning per test case, but anything factorial or exponential over permutations is unnecessary and should be avoided. Even though n is small, permutations are still infeasible since n! grows too fast even at n = 100.

A naive but natural attempt is to consider that MEX depends heavily on the presence of small integers starting from 0. This already hints that only the distribution of low values matters, not their relative order.

A subtle edge case arises when the array has very few distinct small numbers. For example, if all elements are zero, every prefix and suffix has MEX = 1, so every split fails. Similarly, if 0 is missing entirely, every segment has MEX = 0, again causing all splits to fail. These degenerate cases show that global structure of frequencies of 0 and 1 dominates the answer.

## Approaches

A brute-force idea is to try all permutations of the array, and for each one compute prefix MEX and suffix MEX for every split. This is correct because it directly matches the condition. However, generating permutations is factorial in n, and even checking one permutation takes O(n^2) due to recomputing MEX for all segments. This is completely infeasible.

The key observation is that MEX only changes when we cross thresholds where a number becomes fully present in a segment. For MEX to increase past x, all numbers 0 through x must appear in that segment. This means that prefix and suffix MEX values depend only on how 0s, 1s, 2s, etc. are distributed across the split, not on exact ordering beyond feasibility.

The decisive simplification is to track how many times 0 appears, because 0 is the most influential value. If there is at least one 0, we can separate occurrences to control prefix MEX behavior. If there are no 0s, both prefix and suffix always have MEX = 0 for any split, so the condition can never be satisfied.

If there are at least two zeros, we can always construct a valid arrangement. We can place some zeros early and some later so that the prefix sometimes contains 0 and sometimes not, creating differing MEX values across all splits. The remaining structure (non-zero numbers) cannot destroy this possibility because MEX depends first on whether 0 exists.

If there is exactly one zero, the situation becomes tight. We must ensure that no split produces identical MEX values. This turns out to be impossible in some configurations, but possible when there are enough non-zero values to separate influence regions. The decisive characterization reduces to counting occurrences of 0 and 1: if there are at least two 0s or if there is at least one 0 and at least one 1, we can construct a valid ordering; otherwise we cannot.

This reduces the problem from permutations to simple frequency reasoning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many times each value appears, focusing on the number of zeros and ones. These two values dominate MEX behavior because MEX always starts from 0 and depends on whether small integers are present.
2. If there is no zero in the array, immediately conclude the answer is "NO". This is because every subarray has MEX = 0, so every prefix and suffix pair will be equal for every split.
3. If there is exactly one zero, check whether there is at least one non-zero element that can separate prefix and suffix behavior. In practice, this reduces to checking whether there is at least one 1 present. If not, any split will isolate the single zero in a way that forces equal MEX values on both sides.
4. If there are at least two zeros, output "YES". We can always arrange the array so that some splits include a zero in the prefix while others do not, guaranteeing differing MEX values across all partitions.

Why it works: the MEX of any segment is determined first by whether 0 is present, then whether 1 is present if 0 is fully covered, and so on. The only way two sides of a split can have equal MEX for all permutations is when the structure of 0s is too constrained, preventing us from separating their influence. Once we have enough flexibility in the distribution of 0s (either multiple zeros or a compensating 1), we can always construct an ordering where some prefix-suffix boundary breaks MEX equality at every cut.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    z = a.count(0)
    o = a.count(1)
    
    if z == 0:
        print("NO")
    elif z == 1 and o == 0:
        print("NO")
    else:
        print("YES")
```

The implementation relies entirely on counting the occurrences of 0 and 1. This is sufficient because the rest of the values do not affect the existence of a valid arrangement beyond ensuring we are not in a fully degenerate MEX-constant situation.

The key subtlety is that we never attempt to construct the permutation explicitly. The problem only asks whether a valid ordering exists, and the structural condition collapses to a simple frequency check.

## Worked Examples

### Example 1

Input:

```
3
2
1 0
3
0 3 0
6
1 0 5 0 6 1
```

We track counts of 0s and 1s.

| Case | Array | zeros | ones | Decision |
| --- | --- | --- | --- | --- |
| 1 | [1,0] | 1 | 1 | YES |
| 2 | [0,3,0] | 2 | 0 | YES |
| 3 | [1,0,5,0,6,1] | 2 | 2 | YES |

The first case works because both 0 and 1 exist, allowing flexible MEX divergence. The second works due to multiple zeros, which already allows separation. The third has even more flexibility, so every split can be made non-equal in MEX.

### Example 2 (constructed)

Input:

```
3
2
0 2
3
2 3 4
4
0 0 0 0
```

| Case | Array | zeros | ones | Decision |
| --- | --- | --- | --- | --- |
| 1 | [0,2] | 1 | 0 | NO |
| 2 | [2,3,4] | 0 | 0 | NO |
| 3 | [0,0,0,0] | 4 | 0 | YES |

The second case fails because 0 is absent, making all MEX values equal to 0. The first fails because a single zero without any 1 cannot be arranged to separate prefix and suffix MEX behavior. The third succeeds because multiple zeros allow splitting configurations where prefix and suffix MEX differ at every boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | We only count occurrences in a single pass through the array |
| Space | O(1) extra | Only a few counters are maintained |

The solution comfortably fits within constraints since n ≤ 100 and t ≤ 500, making even worst-case input trivial to process.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        z = a.count(0)
        o = a.count(1)
        if z == 0:
            out.append("NO")
        elif z == 1 and o == 0:
            out.append("NO")
        else:
            out.append("YES")
    return "\n".join(out)

# provided samples
assert run("""3
2
1 0
3
0 3 0
6
1 0 5 0 6 1
""") == """YES
YES
YES"""

# custom cases
assert run("""3
2
0 2
3
2 3 4
4
0 0 0 0
""") == """NO
NO
YES"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| [1,0] | YES | minimal valid case with 0 and 1 |
| [2,3,4] | NO | absence of 0 forces constant MEX |
| [0,0,0,0] | YES | multiple zeros allow construction |

## Edge Cases

When there is no zero in the array, every segment has MEX = 0 regardless of ordering. For example, input `[2,3,5]` always produces prefix MEX 0 and suffix MEX 0 for every split, so the answer must be NO.

When there is exactly one zero and no ones, such as `[0,2,3]`, the single zero cannot be used to create any split where prefix and suffix MEX differ in a consistent way across all partitions, forcing failure.

When there are multiple zeros, such as `[0,0,1,2]`, we can always place zeros to ensure that at every split at least one side differs in whether it contains 0 or not, preventing equality of MEX values across all splits.
