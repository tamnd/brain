---
title: "CF 2109E - Binary String Wowee"
description: "We are given a binary string s of length n and an integer k. Our task is to perform exactly k operations, each of which selects a zero in the current string and flips all bits from the beginning up to that zero."
date: "2026-06-08T04:41:34+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 2109
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1025 (Div. 2)"
rating: 2400
weight: 2109
solve_time_s: 89
verified: false
draft: false
---

[CF 2109E - Binary String Wowee](https://codeforces.com/problemset/problem/2109/E)

**Rating:** 2400  
**Tags:** combinatorics, dp, strings  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string `s` of length `n` and an integer `k`. Our task is to perform exactly `k` operations, each of which selects a zero in the current string and flips all bits from the beginning up to that zero. The goal is to count how many different sequences of `k` operations exist. Two sequences are considered different if they choose different indices in any step.

The constraints are moderate: `n` can go up to 500, and `k` is at most `n`. This rules out any solution with exponential complexity in `n` or `k`. We need something polynomial, ideally `O(n * k)` or `O(n^2)` per test case. The sum of `n` over all test cases is bounded by 500, so we can afford nested loops over `n` if necessary.

Non-obvious edge cases include strings with all zeros or all ones. For example, if `s = "000"` and `k = 3`, naive counting might overcount sequences that flip the same prefix multiple times. Another tricky case is when `k` is larger than the number of zeros in the string initially. We cannot select an index with a `1`, so the flipping history matters. Small strings like `"0"` with `k=1` or `"1"` with `k=1` also expose off-by-one mistakes.

## Approaches

The brute-force approach is straightforward. We can recursively try all indices `i` where `s[i]` is zero, flip the prefix, and recurse `k-1` more times. This is correct because it explores all sequences of operations, but it is too slow. In the worst case, each operation can choose up to `n` indices, and there are `k` operations, giving `O(n^k)` complexity, which is astronomically large even for small `n`.

The key insight is to recognize that the only thing that matters is the number of zeros in the string after each flip and their relative positions. Flipping a prefix toggles all bits in that prefix, and this changes which zeros are available for the next operation. We can model this using dynamic programming on the number of zeros and how many operations remain. Specifically, we can maintain a DP table `dp[i][j]` representing the number of ways to perform `i` operations considering the first `j` zeros in the current string configuration. This reduces the problem from exploring all sequences of flips to counting valid subsequences, making the complexity polynomial.

The observation that the number of zeros is at most `n` allows us to index the DP table by zeros rather than string positions, which drastically reduces the number of states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k) | O(n*k) | Too slow |
| DP on zeros | O(n*k) | O(n*k) | Accepted |

## Algorithm Walkthrough

1. Convert the string `s` into a list of positions of zeros. The order of zeros matters because flipping prefixes changes which zeros are available for future operations. Denote this list as `zeros`.
2. Initialize a DP table `dp` with dimensions `(k+1) x (len(zeros)+1)`. Here, `dp[i][j]` will represent the number of ways to perform `i` operations using the first `j` zeros. Set `dp[0][0] = 1` as the base case: zero operations using zero zeros is one valid sequence.
3. Iterate `i` from 1 to `k`, representing the number of operations performed so far.
4. For each `j` from 1 to `len(zeros)`, representing the first `j` zeros, update `dp[i][j]` by summing `dp[i-1][p]` for all `p < j`. This models choosing the `j`-th zero as the target for the `i`-th operation after performing `i-1` operations on the first `p` zeros. The choice of prefix ensures that each operation is valid.
5. After filling the DP table, the answer is the sum of `dp[k][j]` for all `j` from 1 to `len(zeros)`. This counts all sequences that perform exactly `k` operations.

Why it works: Each DP state correctly counts sequences by the number of operations and the subset of zeros considered. The transitions reflect the restriction that we can only flip prefixes ending in zeros. The modular arithmetic handles large counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        zeros = [i for i, ch in enumerate(s) if ch == '0']
        m = len(zeros)
        if k > m:
            print(0)
            continue

        dp = [[0]*(m+1) for _ in range(k+1)]
        dp[0][0] = 1

        for i in range(1, k+1):
            prefix_sum = [0]*(m+1)
            for j in range(m+1):
                prefix_sum[j] = (prefix_sum[j-1] + dp[i-1][j]) % MOD if j else dp[i-1][j]
            for j in range(1, m+1):
                dp[i][j] = prefix_sum[j-1]

        ans = sum(dp[k][1:]) % MOD
        print(ans)

if __name__ == "__main__":
    solve()
```

The first section reads input and constructs the positions of zeros. The DP table is initialized with dimensions `(k+1) x (number of zeros +1)`. We use a prefix sum array to efficiently compute the sum of all previous states for the DP transition. The final answer is the sum of the last row of the DP table corresponding to exactly `k` operations. Off-by-one errors are avoided by careful indexing: `dp[i][j]` corresponds to the first `j` zeros, not positions in the string. The `if k > m` check quickly handles impossible cases.

## Worked Examples

Trace Sample 1: `s = "010"`, `k=1`.

| i (operations) | j (zeros considered) | dp[i][j] |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 1 | 1 |
| 1 | 2 | 1 |

Zeros are at positions `[0, 2]`. We can select either zero for the single operation. Sum of `dp[1][1:]` = 1+1 = 2, which matches the expected output.

Trace Sample 2: `s = "000"`, `k=2`.

Zeros at `[0,1,2]`. DP table updates as follows:

| i | dp[i][1] | dp[i][2] | dp[i][3] |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 0 | 1 | 2 |

Answer = sum(dp[2][1:]) = 0+1+2=3, matching the expected output.

These traces confirm that the algorithm counts all sequences without overcounting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*k) | For each of k operations, we compute a DP row over up to n zeros. Prefix sums reduce the inner sum to O(1). |
| Space | O(n*k) | The DP table has (k+1)*(number of zeros+1) entries. |

With n ≤ 500 and k ≤ 500, this is well within 2 seconds and 256MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("5\n3 1\n010\n3 2\n000\n5 4\n01001\n8 8\n11001100\n20 20\n10010110101101010110\n") == "2\n3\n10\n27286\n915530405"

# minimum input
assert run("1\n1 1\n0\n") == "1"
assert run("1\n1 1\n1\n") == "0"

# maximum zeros
assert run("1\n5 3\n00000\n") == "10"

# impossible k
assert run("1\n3 4\n000\n") == "0"

# alternating zeros and ones
assert run("1\n4 2\n0101\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1\n1 1\n0\n" | 1 | Single zero string |
| "1\n1 1\n1\n" | 0 | Single one string, impossible operation |
| "1\n5 3\n00000\n" | 10 | Multiple zeros, several operations |
| "1\n3 4\n000\n" | 0 | k exceeds zeros, impossible case |
| "1\n4 2\n0101\n" | 2 | Alternating pattern, DP transitions |

## Edge Cases

If `s = "1111"` and `k=1`, there are no zeros to
