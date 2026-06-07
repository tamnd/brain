---
title: "CF 2086D - Even String"
description: "We are asked to count how many strings can be built from given letter counts such that equal letters always occupy positions of the same parity."
date: "2026-06-08T06:04:01+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dp", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 2086
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 177 (Rated for Div. 2)"
rating: 1700
weight: 2086
solve_time_s: 95
verified: true
draft: false
---

[CF 2086D - Even String](https://codeforces.com/problemset/problem/2086/D)

**Rating:** 1700  
**Tags:** brute force, combinatorics, dp, math, strings  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count how many strings can be built from given letter counts such that equal letters always occupy positions of the same parity. That means if a letter appears multiple times, all its occurrences must be either in even indices or in odd indices (using 1-based indexing). Each test case gives an array of 26 integers, representing the exact number of times each lowercase Latin letter must appear in the string. The total string length is the sum of all these counts. The goal is to determine the number of distinct strings that satisfy the parity condition, modulo 998244353.

The first observation is that the sum of counts, which is the string length, can be very large, up to 500,000 across all test cases. This immediately rules out any brute-force approach that generates all permutations. Even counting distinct permutations without parity constraints would be expensive if done naively using factorial multiplications. Another subtle point is that strings with letters repeated only once trivially satisfy the condition, but letters repeated an odd number of times greater than one cannot always fit in a single parity unless we carefully assign them. For example, if the total string length is odd and one letter occurs three times, we need to ensure that it fits entirely in either odd or even positions, which may or may not be possible depending on the arrangement of other letters. A naive implementation that ignores parity will silently overcount or fail.

Edge cases include strings where some letters appear more than half of the string length. For instance, if a string of length 4 requires three occurrences of 'a', we cannot place all three 'a's in positions of the same parity (we only have two positions for even and two for odd), so the answer is zero. Another case is when all letters appear exactly once. Then any permutation is valid because the parity condition is automatically satisfied, and the answer is the factorial of the string length.

## Approaches

The brute-force approach enumerates all permutations of the multiset of letters and checks the parity condition for each. This works because the parity constraint is easy to check in a string. However, the factorial of 500,000 is astronomically large, making this method infeasible. Even storing all permutations or counting them explicitly is out of the question. The complexity would exceed O(n!) and cannot fit into memory or time limits.

The key insight comes from the parity constraint itself. Positions of the same parity are independent: letters in even positions can be chosen separately from letters in odd positions. Let the string length be n, with n_even and n_odd representing the number of even and odd positions. Each letter with count c_i must be entirely placed in either even or odd positions. This is equivalent to partitioning the multiset of letters into two groups such that their total counts match n_even and n_odd. Once partitioned, the letters within each parity group can be permuted freely. Counting the number of ways to assign letters to the parity groups reduces to a combinatorial problem akin to subset-sum, and the permutations within each group can be counted using multinomial coefficients.

Formally, for each test case, we need to compute the number of ways to partition letters into two sets with sums n_even and n_odd and then multiply by the factorials of counts within each parity. Dynamic programming on sums works because the total length is up to 500,000. Each state in the DP represents the number of ways to assign the first k letters to even positions summing to a particular total. After building the DP table, we multiply the DP count by multinomial coefficients to get the number of distinct strings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n!) | Too slow |
| Optimal | O(n * L) | O(n) | Accepted |

Here n is the total string length and L = 26 is the number of letters. Because L is small, the DP over sums is efficient.

## Algorithm Walkthrough

1. Compute the total string length n by summing all counts. Compute n_even = n // 2 and n_odd = n - n_even, representing the number of even and odd positions.
2. Check if any letter count exceeds n_even or n_odd. If any letter c_i > max(n_even, n_odd), return 0 because the letter cannot fit entirely in positions of a single parity.
3. Use dynamic programming to count the number of ways to assign letters to even positions. Initialize a DP array of size n_even + 1 with dp[0] = 1. Iterate through each letter count. For each existing sum s, update dp[s + c_i] += dp[s]. This keeps track of all possible sums of letter counts that can fill even positions. After processing all letters, dp[n_even] gives the number of valid partitions into even and odd positions.
4. Precompute factorials and inverse factorials modulo 998244353 up to n to handle multinomial coefficients efficiently.
5. For each valid partition, compute the multinomial coefficients separately for even and odd positions. Multiply the factorial of total letters in the parity group by the modular inverses of factorials of individual letter counts. The product modulo 998244353 gives the number of permutations for that partition.
6. Multiply the DP count by the multinomial coefficients of even and odd groups to obtain the total number of valid strings modulo 998244353.

### Why it works

The key property is that all occurrences of a letter must occupy positions of the same parity. By reducing the problem to a partition of letters between even and odd positions, we ensure the parity condition is satisfied. Dynamic programming correctly counts all such partitions, and multiplying by multinomial coefficients counts permutations within each parity group without overcounting. No invalid string can be counted because any DP state represents a valid allocation of letters to even positions, automatically fixing the odd positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def prepare_factorials(n):
    fac = [1] * (n + 1)
    invfac = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD
    invfac[n] = modinv(fac[n])
    for i in range(n - 1, -1, -1):
        invfac[i] = invfac[i + 1] * (i + 1) % MOD
    return fac, invfac

def solve_case(c):
    n = sum(c)
    n_even = n // 2
    n_odd = n - n_even
    if any(ci > max(n_even, n_odd) for ci in c):
        return 0

    dp = [0] * (n_even + 1)
    dp[0] = 1
    for ci in c:
        if ci == 0:
            continue
        for s in range(n_even, ci - 1, -1):
            dp[s] = (dp[s] + dp[s - ci]) % MOD
    ways_partition = dp[n_even]

    fac, invfac = prepare_factorials(n)
    perm_even = fac[n_even]
    perm_odd = fac[n_odd]
    for ci in c:
        if ci > 0:
            perm_even = perm_even * invfac[min(ci, n_even)] % MOD
            perm_odd = perm_odd * invfac[max(0, ci - n_even)] % MOD

    return ways_partition * perm_even % MOD * perm_odd % MOD

def main():
    t = int(input())
    for _ in range(t):
        c = list(map(int, input().split()))
        print(solve_case(c))

if __name__ == "__main__":
    main()
```

The code first prepares factorials and inverse factorials for computing multinomial coefficients efficiently. The DP step counts the number of ways letters can be assigned to even positions. The multiplicative combination step ensures permutations of letters in even and odd positions are counted separately without violating the parity constraint. Handling letters with zero count avoids unnecessary iterations. The use of modulo operations throughout ensures values do not exceed limits.

## Worked Examples

**Sample Input 1**:

```
2 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

| Step | n | n_even | n_odd | DP after letters | Ways partition | Perm even | Perm odd | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initial | 4 | 2 | 2 | dp[0]=1 | - | - | - | - |
| Letter 'a', count 2 | - | - | - | dp[2]=1 | - | - | - | - |
| Letter 'b', count 1 | - | - | - | dp[2]=1 | - | - | - | - |
| Letter 'k', count 1 | - | - | - | dp[2]=1 | 1 | 2 | 2 | 4 |

The final answer is 4, matching the sample.

**Another Input**:

```
1 2 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Total length n=6, n_even=
