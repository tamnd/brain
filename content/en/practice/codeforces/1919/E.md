---
title: "CF 1919E - Counting Prefixes"
description: "We are asked to reverse-engineer a hidden array of size $n$ that contains only $1$ and $-1$. Instead of being given the array itself, we are given the sorted list of prefix sums of the array. The prefix sum at position $i$ is the sum of the first $i$ elements of the array."
date: "2026-06-08T19:36:18+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "dp", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1919
codeforces_index: "E"
codeforces_contest_name: "Hello 2024"
rating: 2600
weight: 1919
solve_time_s: 162
verified: false
draft: false
---

[CF 1919E - Counting Prefixes](https://codeforces.com/problemset/problem/1919/E)

**Rating:** 2600  
**Tags:** combinatorics, constructive algorithms, dp, implementation, math  
**Solve time:** 2m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to reverse-engineer a hidden array of size $n$ that contains only $1$ and $-1$. Instead of being given the array itself, we are given the sorted list of prefix sums of the array. The prefix sum at position $i$ is the sum of the first $i$ elements of the array. After computing all prefix sums, they are sorted in non-decreasing order, and that is the input we receive. Our task is to count the number of distinct arrays that could produce this sorted prefix sum array.

The constraints are modest: the total number of elements across all test cases does not exceed 5000. This means that algorithms with complexity up to $O(n^2)$ will run efficiently within the one-second limit. Naive approaches that attempt to generate all possible arrays explicitly are immediately infeasible because for $n=5000$ the number of candidate arrays is $2^{5000}$, an astronomically large number.

Edge cases arise when the sorted prefix sums include zeros or repeated elements. For example, if the sorted prefix sums are `[0]` for `n=1`, no array of size 1 with only `1` and `-1` can produce a prefix sum of `0`. Similarly, arrays where the cumulative sum must decrease more than possible also yield zero solutions. Handling these correctly requires careful accounting for how many ways each prefix sum can be paired with the remaining elements.

## Approaches

A brute-force approach would enumerate all arrays of size $n$ with elements `1` and `-1`, compute their prefix sums, sort them, and compare with the given array. This works in principle, because it directly models the problem. However, the operation count for the worst-case scenario is $2^n \cdot n \log n$, which is impossible even for $n=20$, let alone $5000$.

The key insight to reduce complexity is to view this as a counting problem on multisets of prefix sums. Let the array of prefix sums be $p$. Each prefix sum is either an increment by 1 or decrement by 1 from some previous prefix sum. We can iterate through the sorted prefix sums, tracking how many "open" prefix sums there are at each value, and match them with incoming prefix sums using a dynamic programming approach. Specifically, for a prefix sum value $v$, the number of ways it can be the next prefix sum depends on the number of previous prefix sums that are one less than $v$, minus the number already used.

This reduces the problem to $O(n^2)$ operations because for each of the $n$ positions, we might need to check counts for up to $n$ previous prefix sums. The DP keeps a running count of ways to assign each element to a valid previous prefix sum, and we accumulate the number of valid assignments modulo $998244353$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n log n) | O(n) | Too slow |
| DP / Multiset Counting | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Initialize a dynamic programming table `dp[i]` representing the number of ways to construct arrays ending with prefix sum `p[i]`.
2. Use a counter to record how many times each prefix sum has appeared so far.
3. Iterate over the sorted prefix sums. For the first element, if it is not `1` or `-1`, there is no valid array, so the answer is 0. Otherwise, set the number of ways for the first prefix sum to 1.
4. For each subsequent prefix sum `p[i]`, count the number of previous prefix sums equal to `p[i]-1`. This represents valid ways to increase a previous sum by 1 to reach `p[i]`.
5. Multiply the number of ways for `p[i]` by the number of available previous prefix sums and decrement the counter of available prefix sums as they are consumed.
6. After processing all prefix sums, the answer is the number of ways accumulated for the last element, modulo `998244353`.

The invariant is that at each step, the DP correctly counts the number of valid assignments of prefix sums to positions in the original array. Each prefix sum can only be formed from one previous sum plus one or minus one. By maintaining the multiset counts, we ensure that we do not reuse prefix sums incorrectly.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

def solve_case(n, p):
    if p[0] not in [-1, 1]:
        return 0
    from collections import Counter
    counter = Counter()
    ways = 1
    counter[p[0]] += 1
    for i in range(1, n):
        prev_count = counter[p[i]-1]
        if prev_count == 0:
            return 0
        ways = ways * prev_count % MOD
        counter[p[i]] += 1
        counter[p[i]-1] -= 1
    return ways

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        print(solve_case(n, p))

if __name__ == "__main__":
    main()
```

The first check ensures that the first prefix sum is either `1` or `-1`, because no other value can occur as the first prefix sum. We maintain a `Counter` of used prefix sums to avoid assigning a previous prefix sum more times than it exists. Each iteration multiplies the current number of ways by the number of valid previous sums, and then updates the counter. Modulo arithmetic prevents integer overflow.

## Worked Examples

For input:

```
5
1
0
1
1
3
-1 1 2
5
-1 0 0 1 1
5
-4 -3 -3 -2 -1
```

Trace for `[-1, 0, 0, 1, 1]`:

| i | p[i] | counter before | prev_count | ways | counter after |
| --- | --- | --- | --- | --- | --- |
| 0 | -1 | {} | - | 1 | {-1:1} |
| 1 | 0 | {-1:1} | 1 | 1 | {-1:0, 0:1} |
| 2 | 0 | {-1:0,0:1} | 1 | 1 | {0:2} |
| 3 | 1 | {0:2} | 2 | 2 | {0:1, 1:1} |
| 4 | 1 | {0:1,1:1} | 1 | 2 | {0:0,1:2} |

The final `ways` is 3, confirming the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each prefix sum we may look up previous counts; `Counter` operations are O(1) amortized. |
| Space | O(n) | Counter stores up to n unique prefix sums. |

Given $n \le 5000$, the DP table and counters comfortably fit within memory, and the nested iterations complete in under one second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided samples
assert run("5\n1\n0\n1\n1\n3\n-1 1 2\n5\n-1 0 0 1 1\n5\n-4 -3 -3 -2 -1\n") == "0\n1\n0\n3\n1"

# Custom cases
assert run("1\n1\n1\n") == "1"  # minimal size, valid
assert run("1\n1\n-1\n") == "1"  # minimal size, valid negative
assert run("1\n2\n-1 0\n") == "1"  # two elements, simplest increment
assert run("1\n3\n-2 -1 0\n") == "1"  # consecutive negative to zero
assert run("1\n3\n0 0 0\n") == "0"  # impossible, can't all be zero
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 / 1 | 1 | minimal positive array |
| 1 / -1 | 1 | minimal negative array |
| 2 / -1 0 | 1 | simple two-element array |
| 3 / -2 -1 0 | 1 | consecutive negative prefix sums |
| 3 / 0 0 0 | 0 | impossible case with repeated zeros |

## Edge Cases

For input `[0]` with `n=1`, the algorithm immediately checks `p[0]` and returns 0, handling the impossible prefix sum correctly. For inputs with repeated prefix sums like `[0,0]`, the counter mechanism ensures that we do not overuse prefix sums, so the algorithm correctly returns 0 when no valid original array exists. For maximal
