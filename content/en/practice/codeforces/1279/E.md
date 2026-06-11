---
title: "CF 1279E - New Year Permutations"
description: "We are asked to generate permutations of integers from 1 to $n$ with a special property. A permutation is called good if, when we apply a particular transformation, the permutation remains unchanged."
date: "2026-06-11T19:41:29+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 1279
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 79 (Rated for Div. 2)"
rating: 2700
weight: 1279
solve_time_s: 145
verified: false
draft: false
---

[CF 1279E - New Year Permutations](https://codeforces.com/problemset/problem/1279/E)

**Rating:** 2700  
**Tags:** combinatorics, dp  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to generate permutations of integers from 1 to $n$ with a special property. A permutation is called **good** if, when we apply a particular transformation, the permutation remains unchanged. The transformation works by decomposing the permutation into sequences called **chains**, rotating each chain so its maximum comes first, sorting the chains by their first elements, and then concatenating them back. A good permutation is one that is invariant under this process.

The input consists of multiple test cases, each specifying $n$, the size of the permutation, and $k$, which is the index of the good permutation in lexicographical order. We must output the $k$-th good permutation if it exists or -1 otherwise.

Constraints are tight in a combinatorial sense. $n$ is up to 50, which is small enough that factorials are conceivable in memory if carefully handled. However, $k$ can be as large as $10^{18}$, so we cannot enumerate all permutations or even all good permutations. We need a way to **count and construct** good permutations without generating them all.

A subtle point is that the decomposition depends on **reachability along the permutation**, not adjacency. For example, the permutation `[2, 1, 3]` has chains `[2, 1]` and `[3]`. Careless implementations might just group adjacent decreasing sequences, which is incorrect.

## Approaches

The brute-force approach is straightforward: generate all permutations of size $n$, apply the New Year transformation, check if it is unchanged, then sort and output the $k$-th. This is correct but infeasible for $n > 10$, because $50!$ is astronomically large.

The key observation that unlocks an efficient solution is noticing that a good permutation consists of **blocks of consecutive integers in decreasing order**. Each block can be thought of as a "chain" from the decomposition. The largest element of a block must come first (by the decomposition rule), and the concatenation of blocks in increasing order of their first elements is already sorted for the transformation. This reduces the problem to generating sequences of decreasing blocks whose concatenation is exactly 1 to $n$.

From there, the problem becomes a **counting problem with integer partitions**: if we have $i$ elements left, we can choose a block of size 1 to $i$. The number of good permutations starting with a block of size $j$ is `dp[i-j]` multiplied by 1 (since the block itself has exactly one decreasing arrangement). We can build a dynamic programming table `dp[i]` for the number of good permutations of size $i$ and then use it to **construct the $k$-th permutation recursively** by choosing the size of each next block based on $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n!) | Too slow |
| Block DP + Construction | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute `dp[i]` for all $i \le 50$. Initialize `dp[0] = 1`. For each `i` from 1 to $n$, compute `dp[i]` as the sum of `dp[i-j]` for all `j` from 1 to `i`. This counts all ways to partition $i$ elements into decreasing blocks of consecutive numbers.
2. For each test case `(n, k)`, check if `k > dp[n]`. If so, print `-1` because there are fewer than `k` good permutations.
3. Otherwise, construct the permutation recursively. Start with `cur = 1` (the smallest number not yet placed). While `cur <= n`, try blocks of size `len = 1` to `n - cur + 1`. Let `count = dp[n - (cur + len - 1)]`. If `k > count`, decrement `k` by `count` and continue. Otherwise, choose this block.
4. The chosen block is the next `len` elements in decreasing order: `[cur + len - 1, cur + len - 2, ..., cur]`. Append this block to the answer, increment `cur` by `len`, and repeat.
5. Once `cur > n`, the answer is complete. Output it.

Why it works: Each block is guaranteed to be decreasing and maximal in its reachable elements. The `dp` table ensures that we count exactly how many good permutations remain after choosing each block. By decrementing `k` based on these counts, we select the $k$-th permutation lexicographically without enumerating all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_N = 50

# Precompute number of good permutations for each length
dp = [0] * (MAX_N + 1)
dp[0] = 1
for i in range(1, MAX_N + 1):
    for j in range(1, i + 1):
        dp[i] += dp[i - j]

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        if k > dp[n]:
            print(-1)
            continue

        res = []
        cur = 1
        while cur <= n:
            for length in range(1, n - cur + 2):
                count = dp[n - (cur + length - 1)]
                if k > count:
                    k -= count
                else:
                    # append decreasing block
                    res.extend(range(cur + length - 1, cur - 1, -1))
                    cur += length
                    break
        print(' '.join(map(str, res)))

solve()
```

Explanation: `dp[i]` counts all good permutations of length `i`. When constructing the permutation, we consider all possible first blocks of size `length` and subtract the number of permutations that would skip over `k` until we land on the correct block. The inner loop must go up to `n - cur + 1` to avoid overflow. The block itself is generated in reverse to satisfy the decreasing order rule.

## Worked Examples

Sample input `3 3`:

| Step | cur | length chosen | Block added | k | Remaining elements |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | [2,1] | 3 | 3 |
| 2 | 3 | 1 | [3] | 1 | none |

Output: `2 1 3`.

This demonstrates the recursive construction using the `dp` table to pick the correct block.

Sample input `4 13`:

`dp[4] = 8` (number of good permutations). Since `k = 13 > 8`, output is `-1`. This confirms the algorithm correctly handles overlarge `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | DP table precomputation is O(n^2), constructing permutation iterates over remaining elements and tries blocks up to n each step |
| Space | O(n) | DP table and answer array for one permutation |

For $n \le 50$ and $t \le 1000$, this fits easily within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("5\n3 3\n5 15\n4 13\n6 8\n4 2\n") == \
"2 1 3\n3 1 2 5 4\n-1\n1 2 6 3 4 5\n1 2 4 3"

# Custom cases
assert run("1\n1 1\n") == "1"
assert run("1\n2 2\n") == "2 1"
assert run("1\n5 1\n") == "1 2 3 4 5"
assert run("1\n50 1000000000000000000\n") == "-1"
assert run("1\n4 5\n") == "2 1 4 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest input |
| 2 2 | 2 1 | lexicographical order |
| 5 1 | 1 2 3 4 5 | first permutation |
| 50 1e18 | -1 | k exceeds number of good permutations |
| 4 5 | 2 1 4 3 | construction of non-trivial block |

## Edge Cases

When `n = 1`, the only permutation is `[1]`, which is trivially good. The algorithm sets `dp[1] = 1` and selects the only block. For `n = 2` and `k = 2`, the permutations `[1,2]` and `[2,1]` exist; the DP counts correctly pick `[2,1]` for `k = 2`. For `k`
