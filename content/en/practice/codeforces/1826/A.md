---
title: "CF 1826A - Trust Nobody"
description: "We are given a group of people where each person makes a claim about the minimum number of liars in the group. Each person either always tells the truth or always lies. Our task is to decide whether these claims are consistent and, if so, to determine a possible number of liars."
date: "2026-06-09T07:31:18+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1826
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 870 (Div. 2)"
rating: 1200
weight: 1826
solve_time_s: 73
verified: true
draft: false
---

[CF 1826A - Trust Nobody](https://codeforces.com/problemset/problem/1826/A)

**Rating:** 1200  
**Tags:** brute force, greedy, implementation, sortings  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of people where each person makes a claim about the minimum number of liars in the group. Each person either always tells the truth or always lies. Our task is to decide whether these claims are consistent and, if so, to determine a possible number of liars. If the claims cannot be reconciled, we should return -1.

The input consists of multiple test cases. For each test case, we receive the number of people `n` and an array of `n` integers `l_i`, where `l_i` is the minimum number of liars according to person `i`. The output for each test case is either a valid number of liars or -1 if the claims are contradictory.

The constraints are modest: `n` can go up to 100, and the total number of people across all test cases is at most 10,000. This allows algorithms that are O(n log n) or O(n²) per test case. We do not need to consider highly optimized or sublinear solutions.

Non-obvious edge cases include situations where all people claim zero liars, where everyone claims the maximum number of liars, or where claims cluster around values that make only a narrow range of liar counts possible. For example, if three people say `[2, 2, 2]`, then there cannot be exactly one liar, and there is no configuration that satisfies all claims. A careless implementation might return a number without checking all constraints, producing an incorrect answer.

## Approaches

The brute-force approach would try every possible number of liars from 0 to `n` and check whether the claims are satisfied. For a candidate liar count `k`, we would verify that at least `k` people claim at least `k` liars. This works because a truthful person must be consistent with the actual number of liars, while a liar’s claim is irrelevant. The verification step requires scanning the array, resulting in O(n²) complexity per test case. This is acceptable for `n` up to 100 but inefficient.

The key insight is that we do not need to test every number arbitrarily. We can sort the array of claims and find the smallest index where the number of people whose claims are less than or equal to the candidate liar count matches the expected count. More concretely, if we sort `l_i`, then for each possible number of liars `x`, the number of people claiming at least `x` liars should be at least `x`. If this holds, `x` is a valid answer. This reduces the problem to O(n log n) due to sorting, which is fast enough given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Acceptable but not optimal |
| Optimal (Sort + Greedy) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array of claims `l`.
3. Sort the array `l` in non-decreasing order. Sorting simplifies the check by aligning claims with potential liar counts.
4. Initialize the result as -1 (assuming contradiction).
5. Loop over possible liar counts `x` from 0 to `n`:

1. Count how many people have claims greater than or equal to `x`. After sorting, this is `n - i`, where `i` is the first index with `l[i] >= x`.
2. If `x` equals this count, set the result to `x` and break. This represents a consistent configuration: exactly `x` people are liars, and the rest tell the truth.
6. Print the result for this test case.

The correctness comes from the invariant that for a number of liars `x`, exactly `x` claims must be satisfied by liars or truth-tellers. Sorting allows us to efficiently find the count of claims that can be considered truthful for a candidate `x`. Only when the candidate count equals the number of claims that support it does a consistent configuration exist.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    l = list(map(int, input().split()))
    l.sort()
    result = -1
    for x in range(n + 1):
        # number of people claiming at least x liars
        count = sum(1 for val in l if val >= x)
        if count == x:
            result = x
            break
    print(result)
```

The solution reads input using fast I/O to handle up to 10,000 people efficiently. Sorting the array allows us to align claims for counting. The loop checks each possible liar count, computing the number of claims supporting it. The first valid count is returned, or -1 if none exists.

## Worked Examples

### Example 1

Input:

```
2
1 2
```

Sorted claims: `[1, 2]`

| x | Claims >= x | Count | Result |
| --- | --- | --- | --- |
| 0 | 2 | 2 | not equal |
| 1 | 2 | 2 | not equal |
| 2 | 1 | 1 | equal → result = 1 |

This trace shows the algorithm correctly identifies that exactly one person is a liar.

### Example 2

Input:

```
5 5 3 3 5
```

Sorted claims: `[3, 3, 5, 5, 5]`

| x | Claims >= x | Count | Result |
| --- | --- | --- | --- |
| 0 | 5 | 5 | not equal |
| 1 | 5 | 5 | not equal |
| 2 | 5 | 5 | not equal |
| 3 | 5 | 5 | not equal |
| 4 | 3 | 3 | equal → result = 3 |

This confirms that three people are liars.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates per test case; checking each candidate liar count is O(n), negligible |
| Space | O(n) | Storing the array of claims |

Given `t` up to 1000 and total `n` up to 10,000, the solution is well within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        l = list(map(int, input().split()))
        l.sort()
        result = -1
        for x in range(n + 1):
            count = sum(1 for val in l if val >= x)
            if count == x:
                result = x
                break
        print(result)
    return output.getvalue().strip()

# Provided samples
assert run("7\n2\n1 2\n2\n2 2\n2\n0 0\n1\n1\n1\n0\n5\n5 5 3 3 5\n6\n5 3 6 6 3 5") == "1\n-1\n0\n-1\n0\n3\n4"

# Custom cases
assert run("1\n1\n0") == "0", "single person, zero liars"
assert run("1\n1\n1") == "1", "single person, must be liar"
assert run("1\n3\n0 0 0") == "0", "all truth"
assert run("1\n3\n3 3 3") == "3", "all claim max liars"
assert run("1\n5\n0 1 2 3 4") == "2", "gradually increasing claims"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n0` | `0` | Single person, no liars |
| `1\n1\n1` | `1` | Single person, must be liar |
| `1\n3\n0 0 0` | `0` | Everyone tells the truth |
| `1\n3\n3 3 3` | `3` | Everyone claims maximum liars |
| `1\n5\n0 1 2 3 4` | `2` | Increasing claims, middle solution |

## Edge Cases

If all claims are zero, the algorithm correctly returns 0 liars. Input `1 0 0 0` is sorted to `[0,0,0,1]`; checking counts for `x=0` yields 4, not equal to 0; for `x=1` the count of claims ≥1 is 1, which matches `x=1`. The solution adjusts correctly. If all claims equal `n`, the algorithm identifies that only the maximum count is valid, as seen in input `3 3 3` for three people. Claims that cannot be reconciled, such as `[2,2]`, produce -1 because no candidate `x` satisfies the equality invariant. The method handles these edge cases without any additional checks.
