---
title: "CF 104670K - Knot Knowledge"
description: "We are given a small fixed universe of knot identifiers, numbered from 1 to 1000. Sonja was assigned a list of exactly n distinct knots that she must learn."
date: "2026-06-29T09:37:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104670
codeforces_index: "K"
codeforces_contest_name: "2021-2022 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2021)"
rating: 0
weight: 104670
solve_time_s: 56
verified: true
draft: false
---

[CF 104670K - Knot Knowledge](https://codeforces.com/problemset/problem/104670/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small fixed universe of knot identifiers, numbered from 1 to 1000. Sonja was assigned a list of exactly `n` distinct knots that she must learn. She has already learned `n-1` of them, also given as a list, and exactly one required knot is missing from what she has learned.

The task is to identify that single missing number, knowing that every learned knot is guaranteed to be part of the original required set.

The constraints are very small, with `n` up to 50 and values up to 1000. This immediately tells us that even very simple approaches are sufficient. Any solution that runs in linear or near-linear time in `n` will be instantaneous. Even quadratic or nested scanning over 50 elements is still negligible.

There are no tricky hidden constraints like duplicates or missing multiple values. Both lists are explicitly stated to contain distinct values, so we do not need to handle multiplicities or frequency ambiguities.

The main edge case is structural rather than computational. Because the missing value is guaranteed to exist and be unique, any approach must preserve exact membership reasoning. A naive mistake would be to assume ordering or alignment between the two lists. For example, if one tries to compare positions instead of set membership, the result will fail since the order of inputs is arbitrary.

A second subtle edge case is forgetting that the missing element is always from the first list. If someone incorrectly computes a symmetric difference or compares against the full range 1 to 1000, they might accidentally pick a number not relevant to the input constraint.

Example where naive positional comparison fails:

Input:

```
4
1 2 3 4
4 2 3
```

Correct output:

```
1
```

If one incorrectly subtracts by index alignment (comparing first elements only), they would mistakenly think `1` vs `4` mismatch implies something unrelated.

## Approaches

The brute-force idea is straightforward: for every knot in the required list, scan through the learned list and check whether it appears. If we find a required knot that does not appear in the learned list, that is the answer.

This works because membership is the only condition defining correctness. However, for each of the `n` required knots, scanning the learned list costs `O(n)`, leading to an `O(n^2)` solution. With `n ≤ 50`, this is still completely fine in practice, but it is conceptually unnecessary overhead for such a simple structure.

A cleaner observation is that we are comparing two sets that differ by exactly one element. Instead of repeated membership checks, we can aggregate the difference using arithmetic. Since all values are integers, we can sum all required knots and subtract the sum of learned knots. The result is exactly the missing value.

This works because every common element cancels out when subtracting the two sums, leaving only the missing term.

Another equivalent viewpoint is using XOR. XORing all required values with all learned values also cancels duplicates, leaving the missing value. Both approaches rely on the same cancellation property, but summation is simpler and more directly readable.

The sum-based method reduces the problem to a single pass over both lists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (membership scan) | O(n²) | O(1) | Accepted |
| Sum or XOR cancellation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, then read the list of required knots and the list of learned knots. We keep both as simple arrays of integers.
2. Compute the sum of all required knots. This represents the total "mass" of what should be present.
3. Compute the sum of all learned knots. This represents what Sonja already has.
4. Subtract learned sum from required sum. The difference is the missing knot, since all shared elements cancel exactly once.
5. Output the resulting value.

The reason subtraction works cleanly is that every knot that appears in both lists contributes equally to both sums, so it disappears in the difference. Only the one missing element remains unpaired.

### Why it works

We are effectively using the fact that addition over integers is associative and commutative, so order does not matter. If we write the required set as `A` and learned set as `B`, and we know `B` is exactly `A` without one element `x`, then:

`sum(A) = sum(B) + x`

Rearranging gives `x = sum(A) - sum(B)`. No other structure of the input affects this identity, so the computed value must be exactly the missing knot.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    required = list(map(int, input().split()))
    learned = list(map(int, input().split()))

    total_required = sum(required)
    total_learned = sum(learned)

    print(total_required - total_learned)

if __name__ == "__main__":
    main()
```

The solution is split into three logical parts: input parsing, aggregation, and output. The key implementation detail is ensuring both lists are fully consumed as integers. Since constraints are small, there is no need for streaming or incremental updates.

A common mistake would be forgetting to convert input strings into integers before summing, which would result in string concatenation instead of arithmetic addition in some languages. In Python, `map(int, ...)` avoids that issue entirely.

Another subtle issue is assuming both lists are sorted or aligned, which they are not. The algorithm intentionally avoids any dependence on ordering.

## Worked Examples

### Example 1

Input:

```
4
1 2 4 3
4 2 3
```

We compute sums step by step.

| Step | Required List | Learned List | Required Sum | Learned Sum | Difference |
| --- | --- | --- | --- | --- | --- |
| Start | [1,2,4,3] | [] | 0 | 0 | 0 |
| After required | [1,2,4,3] | [] | 10 | 0 | 10 |
| After learned | [1,2,4,3] | [4,2,3] | 10 | 9 | 1 |

Output:

```
1
```

This trace shows how all common elements cancel, leaving only the missing value.

### Example 2

Input:

```
3
10 101 999
1 999 101
```

| Step | Required List | Learned List | Required Sum | Learned Sum | Difference |
| --- | --- | --- | --- | --- | --- |
| Start | [10,101,999] | [] | 0 | 0 | 0 |
| After required | [10,101,999] | [] | 1110 | 0 | 1110 |
| After learned | [10,101,999] | [1,999,101] | 1110 | 1101 | 9 |

Output:

```
9
```

This demonstrates that the method does not depend on ordering or position, only on value cancellation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each list is summed once in a single pass |
| Space | O(1) | Only a few integer accumulators are used |

The constraints allow up to 50 elements, so even the most straightforward loop-based solution is effectively instantaneous. The algorithm is well within both time and memory limits, with constant overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return sys.stdout.getvalue()

# helper for clean execution in standalone runs is omitted here

# sample 1
assert run("""4
1 2 4 3
4 2 3
""").strip() == "1"

# sample 2
assert run("""3
10 101 999
1 999 101
""").strip() == "9"

# minimum case
assert run("""2
5 7
7
""").strip() == "5"

# already near full range
assert run("""3
1 2 3
2 3
""").strip() == "1"

# unordered heavy mix
assert run("""5
100 200 300 400 500
500 300 100 200
""").strip() == "400"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 5 7 / 7 | 5 | minimum valid structure |
| 1 2 3 / 2 3 | 1 | simple cancellation |
| 100 200 300 400 500 / 500 300 100 200 | 400 | unordered correctness |

## Edge Cases

One edge case is the smallest valid `n = 2`, where exactly one value is missing. For example:

Input:

```
2
5 7
7
```

Required sum is 12, learned sum is 7, so output is 5. The algorithm still behaves correctly because subtraction does not depend on list size.

Another case is when values are near boundaries of the allowed range, such as 1 and 1000. For instance:

Input:

```
3
1 1000 500
1000 500
```

Required sum is 1501, learned sum is 1500, producing 1. Even extreme values do not affect correctness since no overflow or ordering assumptions are involved.

A final structural edge case is when the missing value is the largest or smallest in the set. Since the algorithm does not rely on sorting or indexing, it treats all positions uniformly, so the missing extremum is handled identically to any other element.
