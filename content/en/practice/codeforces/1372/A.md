---
title: "CF 1372A - Omkar and Completion"
description: "We are asked to construct an integer array of length n where every element is positive, does not exceed 1000, and satisfies a global restriction on sums: if we pick any three positions (they may coincide), the sum of two chosen elements is never equal to any element of the array."
date: "2026-06-16T12:43:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1372
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 655 (Div. 2)"
rating: 800
weight: 1372
solve_time_s: 404
verified: false
draft: false
---

[CF 1372A - Omkar and Completion](https://codeforces.com/problemset/problem/1372/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation  
**Solve time:** 6m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct an integer array of length `n` where every element is positive, does not exceed 1000, and satisfies a global restriction on sums: if we pick any three positions (they may coincide), the sum of two chosen elements is never equal to any element of the array.

In more concrete terms, no value in the array is allowed to be representable as the sum of two values from the array, including the possibility of doubling a single element. So if `a[i] + a[j]` appears anywhere in the array, even at some other index `k`, the array is invalid.

The input gives multiple test cases, each providing only `n`, and for each we must output any valid array of that length.

The constraints are small. The sum of all `n` across test cases is at most 1000, and each `n` is at most 1000. This immediately tells us that we are not dealing with performance pressure. Any solution up to roughly `O(n^2)` or even slightly worse per test case would pass comfortably, but the structure of the condition suggests we should avoid unnecessary pairwise checks entirely.

The non-obvious failure case for naive construction is the increasing sequence. If we try `[1, 2, 3, 4, 5]`, we immediately get `1 + 2 = 3`, which violates the condition. A more subtle failed attempt is any dense set of small numbers, since small values naturally combine into other small values that are also present.

A second subtle trap is trying to randomize values without structure. Even if values are within bounds, random choices will frequently create accidental sum collisions like `a[i] + a[j] = a[k]`, especially when numbers are small or repeated.

## Approaches

A brute-force approach would try to build the array incrementally. For each new element, we could test all candidate values from `1` to `1000` and check whether adding it violates the condition with any previously chosen pair. This requires checking all pairs in the current prefix, so for each placement we may do up to `O(n^2)` checks, leading to `O(n^3)` total work per test case in the worst case. This is unnecessary because the condition is global and does not require maintaining exact combinational structure dynamically.

The key observation is that we are not required to use distinct values or maximize variety. We only need to avoid sum collisions. A simple way to guarantee this is to make all elements equal to a constant value. If every element is the same number `x`, then every sum of two elements is `2x`, which is not present in the array as long as `x != 2x`. Since `x > 0`, this is always true.

We also need to respect the upper bound of 1000, but choosing `x = 1` already satisfies all constraints. Then the array consists entirely of ones, and the only possible sum is `2`, which is not in the array.

This makes the problem essentially a constant construction task.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force incremental checking | O(n^3) | O(n) | Too slow |
| Constant array construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the array independently for each test case.

1. Read `n` for the test case. We only need to determine how many elements to output, not their structure beyond satisfying the condition.
2. Choose a fixed value `1` for all positions. This ensures every element is positive and within the required bound of 1000.
3. Fill the array with `n` copies of `1`. No additional checks are needed because the structure guarantees validity.
4. Output the array.

### Why it works

The only possible sums formed from the array are of the form `1 + 1 = 2`. Since every array element is `1`, and `2` never appears in the array, there is no triple of indices such that `a[x] + a[y] = a[z]`. Because all elements are identical, every possible pair sum is the same, and it is guaranteed to lie outside the set of values used in the array. This invariant holds regardless of `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        print(" ".join(["1"] * n))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the construction. The only subtlety is handling multiple test cases and ensuring fast I/O using `sys.stdin.readline`.

The expression `["1"] * n` builds the required array efficiently as strings, avoiding integer-to-string conversion inside loops. Since output size is the limiting factor, this is optimal in practice.

## Worked Examples

### Example 1

Input:

```
n = 5
```

We construct five ones.

| Step | Action | Array |
| --- | --- | --- |
| 1 | Start | [] |
| 2 | Add 1 | [1] |
| 3 | Add 1 | [1, 1] |
| 4 | Add 1 | [1, 1, 1] |
| 5 | Add 1 | [1, 1, 1, 1] |
| 6 | Add 1 | [1, 1, 1, 1, 1] |

All pair sums equal 2, which is not in the array, confirming validity.

### Example 2

Input:

```
n = 4
```

| Step | Action | Array |
| --- | --- | --- |
| 1 | Start | [] |
| 2 | Add 1 | [1] |
| 3 | Add 1 | [1, 1] |
| 4 | Add 1 | [1, 1, 1] |
| 5 | Add 1 | [1, 1, 1, 1] |

Again, all sums are 2, which does not appear in the array, so the condition holds.

These traces show that no interaction between elements ever introduces a forbidden equality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We output exactly `n` values and do constant work per value |
| Space | O(1) extra | Aside from output buffering, no additional data structures are used |

The total output size across all test cases is at most 1000 elements, so the construction is trivially fast under the constraints.

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
        out.append(" ".join(["1"] * n))
    return "\n".join(out)

# provided samples (format adapted since output is not unique)
assert run("2\n5\n4\n") == "1 1 1 1 1\n1 1 1 1", "sample-like check"

# custom cases
assert run("1\n1\n") == "1", "minimum size"
assert run("1\n10\n") == "1 1 1 1 1 1 1 1 1 1", "uniform larger case"
assert run("1\n1000\n") == " ".join(["1"] * 1000), "maximum n case"
assert run("3\n2\n3\n4\n") == "1 1\n1 1 1\n1 1 1 1", "multiple small cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` | `[1]` | minimal valid construction |
| `n=1000` | 1000 ones | maximum size handling |
| multiple test cases | repeated ones | multi-case correctness |

## Edge Cases

The only meaningful edge case is when `n = 1`. The construction still outputs `[1]`. There are no pairs to form sums, so the condition is vacuously satisfied.

For `n = 1000`, we output 1000 ones. Even though there are many pairs, every sum remains `2`, which is not present in the array, so no violation arises.

The case of repeated test cases does not change behavior since each test case is independent and uses the same construction logic.
