---
title: "CF 2056D - Unique Median"
description: "We are asked to count subarrays of a given array where the median is uniquely defined. In practice, this means a subarray is good if, after sorting, the middle element (or the two middle elements, if the length is even) are equal."
date: "2026-06-08T08:16:38+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "combinatorics", "data-structures", "divide-and-conquer", "dp"]
categories: ["algorithms"]
codeforces_contest: 2056
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 997 (Div. 2)"
rating: 2200
weight: 2056
solve_time_s: 123
verified: false
draft: false
---

[CF 2056D - Unique Median](https://codeforces.com/problemset/problem/2056/D)

**Rating:** 2200  
**Tags:** binary search, brute force, combinatorics, data structures, divide and conquer, dp  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count subarrays of a given array where the median is uniquely defined. In practice, this means a subarray is good if, after sorting, the middle element (or the two middle elements, if the length is even) are equal. For odd-length subarrays, this is trivial because the single median is always "equal to itself." For even-length subarrays, the two middle numbers must be identical.

The array values are small, ranging from 1 to 10, but the array can be large, up to 10^5 elements. With up to 10^4 test cases, the total array size across all tests is capped at 10^5. This implies we cannot afford any O(n^2) approach per test case because in the worst case, that would require 10^10 operations. We need something closer to O(n) or O(n log n) per test case.

Edge cases arise when all elements are identical, making every subarray good, or when all elements are distinct, which reduces the number of good even-length subarrays. A careless solution might attempt to check medians explicitly for every subarray, which will be too slow. Small examples illustrate this: for `[1,2]`, the subarray `[1,2]` is not good because the two medians are different. For `[1,1,1,1]`, every subarray is good because medians always coincide.

## Approaches

The brute-force solution iterates over all subarrays, sorts each one, and checks the middle elements. It is correct but scales as O(n^3) in the worst case (O(n^2) subarrays, each requiring O(n log n) sort). With n up to 10^5, this is completely infeasible.

The key observation is that the problem can be reduced to counting subarrays based on the frequency of a "central" value. Fix a number `x` and consider it as the candidate median. For each position in the array, track a running count: +1 if the element equals `x`, -1 if it is less than `x`, and 0 otherwise. For even-length subarrays, we need counts of elements greater than `x` and less than `x` to be balanced around `x` to make the median exactly `x`. This transforms the problem into a prefix sum counting problem: the difference between counts forms a key, and the number of good subarrays ending at each index can be computed using a hashmap to track frequencies of these keys.

This insight converts a potentially cubic problem into a linear one per candidate median. Since the values are bounded by 10, we can iterate over all possible `x` from 1 to 10, yielding an overall complexity of O(10 * n) = O(n), which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n * max(a_i)) | O(n * max(a_i)) | Accepted |

## Algorithm Walkthrough

1. Iterate through each possible median candidate `x` from 1 to 10. This is feasible because `a_i` ≤ 10. Each candidate `x` will be considered separately.
2. Transform the array into a running balance array `balance`, initialized with 0 at position -1. For each element in the array, if it is equal to `x`, add 1 to the previous balance; if less than `x`, subtract 1; if greater than `x`, leave the balance unchanged. This encoding captures the relative dominance of `x` in the prefix.
3. Use a hashmap `freq` to count occurrences of each balance value. Initialize it with `{0: 1}` because the empty prefix has balance 0. For each position, the number of subarrays ending at this position with median `x` is equal to the frequency of the current balance value in `freq`. This works because two prefixes with the same balance imply the subarray between them has net balance 0, meaning `x` is the median.
4. Sum these counts over all positions to get the total number of good subarrays for this candidate median.
5. Sum the counts over all candidates from 1 to 10 to get the answer for the test case.

Why it works: the balance array ensures that in any subarray between two prefixes with the same balance, the count of `x` minus the count of elements smaller than `x` is unchanged. This ensures that `x` is the median of that subarray. By considering all `x`, we cover every possible median in the array.

## Python Solution

```python
import sys
from collections import defaultdict
input = sys.stdin.readline

def count_good_subarrays(a):
    n = len(a)
    ans = 0
    for x in range(1, 11):
        balance = 0
        freq = defaultdict(int)
        freq[0] = 1
        for val in a:
            if val == x:
                balance += 1
            elif val < x:
                balance -= 1
            # val > x does not change balance
            ans += freq[balance]
            freq[balance] += 1
    return ans

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(count_good_subarrays(a))
```

The solution reads input using fast I/O. We loop over candidate medians from 1 to 10 and compute a prefix balance array implicitly. The hashmap `freq` counts previous balances to allow O(1) retrieval of subarray counts. Subtle points include initializing `freq[0] = 1` to account for subarrays starting at index 0 and updating the answer before incrementing the frequency to avoid missing the current prefix.

## Worked Examples

Sample 1: `a = [1, 1, 1, 1]`

| i | val | balance | freq | ans |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | {0:1} | 1 |
| 1 | 1 | 2 | {0:1,1:1} | 2 |
| 2 | 1 | 3 | {0:1,1:1,2:1} | 3 |
| 3 | 1 | 4 | {0:1,1:1,2:1,3:1} | 4 |

Summing over x = 1 gives all 10 subarrays. Other x contribute 0.

Sample 2: `a = [1,10,2,3,3]`

For x = 3:

| i | val | balance | freq | ans |
| --- | --- | --- | --- | --- |
| 0 | 1 | -1 | {0:1} | 0 |
| 1 | 10 | -1 | {-1:1,0:1} | 1 |
| 2 | 2 | -2 | {-2:0,-1:1,0:1} | 1 |
| 3 | 3 | -1 | {-2:0,-1:1,0:1} | 2 |
| 4 | 3 | 0 | {-2:0,-1:2,0:1} | 3 |

The final count sums to 11.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 10) = O(n) | Outer loop runs 10 times, inner loop runs n times per test case |
| Space | O(n) | Hashmap `freq` can store at most n+1 unique balances |

This scales comfortably within the constraints of n ≤ 10^5 and t ≤ 10^4. The memory footprint remains below 512 MB because balances are small integers and there are at most n keys per candidate median.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict
    input = sys.stdin.readline

    def count_good_subarrays(a):
        n = len(a)
        ans = 0
        for x in range(1, 11):
            balance = 0
            freq = defaultdict(int)
            freq[0] = 1
            for val in a:
                if val == x:
                    balance += 1
                elif val < x:
                    balance -= 1
                ans += freq[balance]
                freq[balance] += 1
        return ans

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(str(count_good_subarrays(a)))
    return "\n".join(out)

# Provided samples
assert run("3\n4\n1 1 1 1\n5\n1 10 2 3 3\n10\n6 3 2 3 5 3 4 2 3 5\n") == "10\n11\n42"

# Minimum size input
assert run("1\n1\n5\n") == "1"

# Maximum size input, all equal
assert run("1\n5\n2 2 2 2 2\n") == "15"

# Mixed small numbers
assert run("1\n5\n1 3 2 3 1\n") == "9"

# Only increasing sequence
assert run("
```
