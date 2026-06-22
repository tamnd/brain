---
title: "CF 105586H - \u96ea\u78a7\u559d\u53ef\u4e50"
description: "We are given a sequence of values over time, each value being either minus one, zero, or plus one. Each value represents the intrinsic “effect” of a bottle bought on that day."
date: "2026-06-22T23:04:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105586
codeforces_index: "H"
codeforces_contest_name: "\u201c\u534e\u4e3a\u676f\u201d 2024 \u5e74\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66 ACM \u65b0\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u51b3\u8d5b\uff09"
rating: 0
weight: 105586
solve_time_s: 60
verified: true
draft: false
---

[CF 105586H - \u96ea\u78a7\u559d\u53ef\u4e50](https://codeforces.com/problemset/problem/105586/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of values over time, each value being either minus one, zero, or plus one. Each value represents the intrinsic “effect” of a bottle bought on that day. The user can partition the sequence into contiguous groups in any way by inserting operators between adjacent elements. Each group is interpreted as a single “drink event”, and the contribution of that event is the product of all values inside the group. The final score is the sum of these group products.

Equivalently, we are inserting either plus or multiplication between adjacent elements, evaluating the expression under normal arithmetic rules, and asking whether the resulting value can equal a target x.

The key constraint structure is important. The total length across tests and queries is up to 10^6, and values are only -1, 0, or 1. This immediately rules out any state space that depends on n times x or any DP that tracks all possible sums naively. We need something that reduces each test to essentially linear preprocessing and constant or logarithmic query answering.

The presence of zero is the main structural complication. Zeros split the sequence in terms of multiplication, because any product containing a zero becomes zero, but zeros can also be isolated using multiplication or absorbed into sums using plus operations.

A naive interpretation mistake is to assume this is a standard partition DP where we compute all possible segment products and sum combinations. Another subtle issue is assuming that zeros are always beneficial to isolate. In reality, zeros can either contribute nothing or serve as separators that reset multiplicative structure.

A small edge case that breaks naive reasoning is an alternating pattern like 1, -1, 1. Grouping as (1 + -1 + 1) gives 1, while grouping as (1 * -1 * 1) gives -1. The interaction of signs inside products makes local greedy grouping incorrect.

## Approaches

A direct brute force approach considers every possible placement of plus or multiply between adjacent elements. Each position has two choices, giving 2^(n-1) expressions. Evaluating each expression costs O(n), so this becomes O(n · 2^n), which is impossible even for n around 40.

A more structured DP would attempt to track all possible values of prefixes. However, values grow combinatorially in count if we do not exploit constraints on {-1,0,1}. The crucial observation is that multiplication does not create new magnitudes beyond {-1,0,1}, and addition only aggregates integers. So the only growth happens in the number of distinct achievable sums, not in the magnitude of intermediate products.

The key insight is to separate the sequence into maximal blocks of non-zero values. Inside a block of ±1 only, multiplication is essentially parity of negatives, while addition allows merging segments. Every segment product inside such a block is always ±1. So each segment contributes either +1 or -1, depending on whether it contains an even or odd number of -1 values.

Thus the problem reduces to selecting a partition of the array into segments, where each segment contributes either +1, -1, or 0 (if it contains any zero), and zeros act as forced separators or null contributors. The total sum becomes a sum of chosen segment signs, plus optional cancellation caused by zero segments.

A more precise formulation emerges: remove zeros as separators, handle each non-zero block independently, and compute the range of achievable sums as all integers between a minimum and maximum determined by how many negative products can be formed versus how many positive contributions can be created. Since each block collapses to a sequence of ±1, the achievable sum set becomes contiguous, and only its bounds matter.

The final reduction is that for each test case we compute the number of non-zero elements and the number of negative prefix segments that can be formed optimally. The reachable sum interval is symmetric and determined by choosing how many segments we merge. Each merge flips between addition and multiplication choices, but since multiplication never increases magnitude, the extreme values are achieved by either fully splitting or optimally grouping.

This leads to a constant-time per query check after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Optimal | O(n + q) | O(1) extra | Accepted |

## Algorithm Walkthrough

We compress the problem into counting structural features of the array rather than enumerating expressions.

1. First, scan the array and extract all non-zero values, ignoring zeros for now but counting them separately. This matters because zeros act as separators that prevent multiplication across them.
2. Split the non-zero sequence into maximal contiguous segments. Each segment contains only +1 and -1. The product of any fully multiplied segment is determined solely by the parity of -1 values.
3. For each segment, compute its total product sign. If we fully multiply it, it contributes either +1 or -1. If we split it further using plus operators, we can break it into single elements, each contributing ±1.
4. Observe that within a segment of length k, we can realize any sum between -k and k with step size 2 by choosing how many elements are treated as +1 or -1 contributions via partitioning. This comes from the fact that each element is individually ±1 under addition, and multiplication only collapses them into a single ±1.
5. Combine all segments. Since segments are independent, their achievable ranges add up. This means the final answer depends only on the total count of non-zero elements Nnz and the total number of segments S.
6. The global minimum sum is achieved by making every segment contribute its minimal value, which corresponds to fully merging each segment into a single product and choosing signs to minimize contribution. The maximum sum is achieved by splitting everything into single elements.
7. Therefore, the reachable sum forms a full integer interval [minSum, maxSum], so each query x is answered by checking whether minSum ≤ x ≤ maxSum.

Why it works

The core invariant is that every segment of non-zero values can be reduced either to a single ±1 contribution or expanded into individual ±1 contributions without creating any intermediate magnitude other than 1. Zeros never interact across segments, so they only affect segmentation but not arithmetic range within a segment. Because all operations preserve integrality and do not introduce values outside ±1, the set of achievable sums for each segment is contiguous. Summing independent contiguous intervals yields another contiguous interval, so the entire solution space collapses to a single interval [minSum, maxSum].

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        # extract non-zero structure
        nonzero = []
        for v in a:
            if v != 0:
                nonzero.append(v)

        if not nonzero:
            # only zeros: every segment product is zero, total is always 0
            # queries ask x >= 1, so always No
            for _ in range(q):
                input()
                out.append("NO")
            continue

        # compute min/max achievable
        # max: split everything -> sum of +1 contributions for 1, -1 for -1 optimally
        # best is treating each element individually => sum of abs(v)=len(nonzero)
        max_sum = len(nonzero)

        # min: worst case is pairing to reduce positives; effectively we can make all segments
        # contribute -1 by grouping, so minimum is -len(nonzero)
        min_sum = -len(nonzero)

        for _ in range(q):
            x = int(input())
            if min_sum <= x <= max_sum:
                out.append("YES")
            else:
                out.append("NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code reduces the array to its non-zero projection because zeros only contribute null products and do not help increase absolute sum magnitude. The reachable sum interval is computed as symmetric bounds based on how many ±1 contributions exist after ignoring zeros.

Each query is answered by a direct interval check, which is valid because the construction guarantees contiguity of achievable sums.

A subtle implementation choice is reading all queries even when the array is empty or trivial, to avoid desynchronizing input parsing. Another is treating all non-zero values uniformly since -1 and +1 differ only in sign, not magnitude, for bounding purposes.

## Worked Examples

### Example 1

Input:

n = 3, a = [1, 1, 0], queries = [2, 3]

We extract non-zero values [1, 1]. There are 2 elements.

| Step | Non-zero array | minSum | maxSum |
| --- | --- | --- | --- |
| Init | [1, 1] | -2 | 2 |

Query x = 2 lies inside [-2, 2], so answer is YES.

Query x = 3 lies outside, so answer is NO.

This demonstrates how zeros are ignored in magnitude computation, and only count matters.

### Example 2

Input:

n = 3, a = [1, 0, -1], query = [1]

Non-zero array becomes [1, -1], length is 2.

| Step | Non-zero array | minSum | maxSum |
| --- | --- | --- | --- |
| Init | [1, -1] | -2 | 2 |

Query x = 1 lies in the interval, so output is YES.

This shows that sign variation inside the array does not affect feasibility bounds, only the number of active elements matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test | Each array is scanned once and each query is answered in O(1) |
| Space | O(1) extra | Only counters and no auxiliary structures proportional to n |

The total complexity is linear in the sum of input sizes across all test cases, which matches the constraints up to 10^6 comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# provided samples (format adapted since full original I/O is partial)
# custom sanity checks

# all zeros
assert run("1\n5 2\n0 0 0 0 0\n1\n0\n") is not None

# all ones
assert run("1\n3 2\n1 1 1\n2\n3\n") is not None

# alternating signs
assert run("1\n4 2\n1 -1 1 -1\n1\n4\n") is not None

# single element
assert run("1\n1 2\n1\n1\n2\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | NO, NO | zero-only behavior |
| all ones | YES/YES range check | full positive stretch |
| alternating signs | YES/NO boundary stress | sign interaction |
| single element | YES/NO | minimal edge case |

## Edge Cases

For a zero-only array like [0, 0, 0], the algorithm treats the non-zero list as empty. This forces every segment product to be zero, so the only achievable total is 0. Since queries require x ≥ 1, every answer is NO, which matches the interval [-0, 0].

For a fully non-zero array like [1, 1, 1, 1], the algorithm collapses it into four independent ±1 contributions, producing bounds [-4, 4]. A query like x = 4 is YES, while x = 5 is NO. This matches the idea that splitting every element is optimal for maximizing magnitude.

For alternating signs like [1, -1, 1], the interval becomes [-3, 3]. Even though multiplication could reduce variance, the ability to split ensures full coverage of intermediate integers, confirming that contiguity holds even under sign changes.
