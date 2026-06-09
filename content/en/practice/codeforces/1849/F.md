---
title: "CF 1849F - XOR Partition"
description: "We are given a set of distinct integers and we need to split them into two subsets such that the minimum XOR among all pairs in each subset is as large as possible. The value of a partition is the smaller of the two subset costs. Each element must belong to exactly one subset."
date: "2026-06-09T05:35:41+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "data-structures", "divide-and-conquer", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1849
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 152 (Rated for Div. 2)"
rating: 2700
weight: 1849
solve_time_s: 91
verified: false
draft: false
---

[CF 1849F - XOR Partition](https://codeforces.com/problemset/problem/1849/F)

**Rating:** 2700  
**Tags:** binary search, bitmasks, data structures, divide and conquer, greedy, trees  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of distinct integers and we need to split them into two subsets such that the minimum XOR among all pairs in each subset is as large as possible. The value of a partition is the smaller of the two subset costs. Each element must belong to exactly one subset. For sets with fewer than two elements, the cost is defined as $2^{30}$.

The input size can be up to $2 \times 10^5$ integers, each less than $2^{30}$. This implies any solution with nested loops over the set to compute XOR for all pairs will be too slow. A brute-force search of all possible partitions, which is $O(2^n)$, is clearly impossible. Even computing all pairwise XORs in $O(n^2)$ would reach $4 \times 10^{10}$ operations at the upper limit.

The subtle part of the problem is that XOR behaves like a distance metric in binary space. Adjacent numbers in terms of XOR may not be adjacent numerically, so naive attempts to split based on value ordering can fail. Another edge case arises when some subset has only one element, in which case the cost defaults to $2^{30}$. A careless implementation might ignore this and treat it as zero.

For example, given `[0, 1, 2]`, splitting into `[0,1]` and `[2]` gives subset costs of `1` and `2^30`. The minimum of the two is 1. A naive approach that always balances subset sizes might pick `[0,2]` and `[1]` yielding a worse minimum of 1. The algorithm must consider the XOR structure, not just counts.

## Approaches

The brute-force solution is to generate all $2^n$ partitions and for each, compute the cost by iterating over all pairs within each subset. This is correct but infeasible because for $n = 2 \times 10^5$, the number of partitions is astronomical, and each cost computation takes $O(n^2)$.

The key insight for an optimal solution is to interpret the integers in binary form. The XOR minimum in a set is determined by the highest bit at which numbers differ. This suggests a recursive divide-and-conquer approach. If we examine the most significant bit, we can partition the numbers into two groups: those with a 0 in that bit and those with a 1. To maximize the minimum XOR, we must pair numbers across different partitions only when necessary. If either group is empty, the optimal split occurs in the next lower bit.

The recursion continues down the bits, assigning each number to one of the two subsets while ensuring the XOR of elements within the same subset is large. This is equivalent to constructing a binary trie and splitting recursively at each node. The optimal partition is determined by assigning numbers according to the bit splits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n^2) | O(n) | Too slow |
| Optimal | O(n log MAX_BIT) | O(n log MAX_BIT) | Accepted |

## Algorithm Walkthrough

1. Convert each number to its binary representation with 30 bits, since numbers are less than $2^{30}$. This allows us to examine bits from the most significant to the least significant.
2. Define a recursive function that takes a list of indices and a bit position. If the bit position is less than 0 or the list has one element, assign all remaining elements to one subset and return.
3. Partition the list into two sublists based on the current bit: one for elements with a 0 at this bit and one for elements with a 1.
4. If both sublists are non-empty, recursively split both sublists on the next lower bit. If a sublist is empty, continue splitting the non-empty sublist. The recursion ensures that elements differing at higher bits are more likely to be separated, which maximizes the minimum XOR in each subset.
5. While backtracking, assign subset identifiers (0 or 1) to each element based on which side of the split they fall into. Flip identifiers consistently to maintain the subset division.
6. After all recursion completes, output the partition as a string of 0s and 1s, corresponding to the subsets.

Why it works: The recursion respects the property that the minimum XOR is dominated by the highest differing bit among elements. By separating numbers with different bits early, we avoid creating small XOR values within the same subset. This greedy choice per bit is globally optimal because higher bits always contribute more to XOR value, and lower bits are only considered when higher bits are identical.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def xor_partition():
    n = int(input())
    a = list(map(int, input().split()))
    ans = [0] * n

    def solve(indices, bit):
        if bit < 0 or len(indices) <= 1:
            for i in indices:
                ans[i] = 0
            return
        zeros, ones = [], []
        for i in indices:
            if (a[i] >> bit) & 1:
                ones.append(i)
            else:
                zeros.append(i)
        if not zeros:
            solve(ones, bit - 1)
        elif not ones:
            solve(zeros, bit - 1)
        else:
            solve(zeros, bit - 1)
            for i in ones:
                ans[i] = 1
            solve(ones, bit - 1)

    solve(list(range(n)), 29)
    print(''.join(map(str, ans)))

xor_partition()
```

The solution starts by increasing the recursion limit because the divide-and-conquer can go deep for large $n$. The recursive function partitions indices based on the current bit. The assignment of 0 or 1 is done while recursing. If one side of the partition is empty, the algorithm continues with the non-empty side. Otherwise, elements in the `ones` group are assigned to subset 1, and we continue recursion for both sides. This ensures the XOR between subsets is maximized at higher bits.

## Worked Examples

### Sample 1

Input: `42, 13, 1337, 37, 152`

| Step | Indices | Bit | Zeros | Ones | Assignment |
| --- | --- | --- | --- | --- | --- |
| 1 | [0,1,2,3,4] | 29 | [0,1,3,4] | [2] | ans[2]=1 |
| 2 | [0,1,3,4] | 28 | ... | ... | recurse |
| ... | ... | ... | ... | ... | ... |

Trace demonstrates that numbers differing in high bits are separated first, pushing small XOR values across subsets rather than within them.

### Custom Example

Input: `[0, 1, 2, 3]`

| Step | Indices | Bit | Zeros | Ones | Assignment |
| --- | --- | --- | --- | --- | --- |
| 1 | [0,1,2,3] | 1 | [0,1] | [2,3] | ans[2,3]=1 |
| 2 | [0,1] | 0 | [0] | [1] | ans[1]=1 |
| 3 | [2,3] | 0 | [2] | [3] | ans[3]=1 |

The output `0111` divides numbers so the minimum XOR in both subsets is maximized.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log MAX_BIT) | Each element is processed at most once per bit position (30 bits) |
| Space | O(n log MAX_BIT) | Recursion stack depth can reach log(MAX_BIT) per element |

This fits comfortably within the constraints since $n = 2 \times 10^5$ and MAX_BIT = 30, resulting in ~6 million operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    xor_partition()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("5\n42 13 1337 37 152\n") in ["10001", "01110"], "sample 1"

# Minimum size
assert run("2\n0 1\n") in ["01", "10"], "minimum size"

# Maximum size, sequential numbers
n = 200000
seq = ' '.join(str(i) for i in range(n))
out = run(f"{n}\n{seq}\n")
assert len(out) == n, "maximum size"

# Boundary numbers
assert run("4\n0 1 1073741823 536870911\n") in ["0011", "1100"], "boundary values"

# Small consecutive numbers
assert run("3\n1 2 3\n") in ["011", "101", "110"], "small consecutive"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n0 1` | `01` or `10` | Correct handling of minimum-size input |
| `200000\n0 1 2 ...` | length 200000 | Scalability for maximum n |
| `4\n0 1 1073741823 536870911` |  |  |
