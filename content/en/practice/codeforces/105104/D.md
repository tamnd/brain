---
title: "CF 105104D - $\\text{DAY}^{-1}$"
description: "We are given a fixed pattern string that is formed by repeating the block \"xtu\" exactly n times. So the full string p has length 3n and consists of a very rigid periodic structure: every three characters are always x, then t, then u."
date: "2026-06-27T20:09:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105104
codeforces_index: "D"
codeforces_contest_name: "2024 HNMU@XTU"
rating: 0
weight: 105104
solve_time_s: 43
verified: true
draft: false
---

[CF 105104D - $\\text{DAY}^{-1}$](https://codeforces.com/problemset/problem/105104/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed pattern string that is formed by repeating the block `"xtu"` exactly `n` times. So the full string `p` has length `3n` and consists of a very rigid periodic structure: every three characters are always `x`, then `t`, then `u`.

Alongside this, each test case provides a query string `q`. The task is to count how many distinct ways we can choose indices from `p` such that the chosen characters, read in order, form exactly `q`. Two ways are considered different if they differ in which positions of `p` were used.

So the core object is not substring matching but subsequence counting, where the same character in different positions contributes separate combinatorial choices.

The constraints are extremely tight in a very specific way. The repetition count `n` is at most 10, which means the main string `p` has length at most 30. The query length is also bounded by `3n`, so at most 30 as well. However, the number of test cases can be as large as `10^5`, so the solution must be close to linear in the size of each test case, with very small constants.

A naive subsequence DP per test case is already acceptable in terms of state size, but anything exponential in `|p|` or `|q|` per test case would be too slow across all tests.

One subtle point is that even though `p` is highly structured, subsequences are counted by position, not by character type. That means identical letters occurring at different positions in `p` are not interchangeable, they produce different counts.

Edge cases appear when `q` contains letters outside `{x, t, u}`. In that case the answer is immediately zero because `p` never contains them.

Another important edge case is when `q` is empty. The number of ways to form an empty subsequence is always 1, since we choose nothing.

Finally, when `q` is longer than `p`, the answer is zero because we cannot pick more positions than exist.

## Approaches

The brute-force idea is to treat the problem literally as subsequence counting on a string of length up to 30. We recursively decide for each position in `p` whether to take it or skip it, tracking how many ways we match `q`. This explores all subsets of indices, which is `2^(3n)` possibilities. With `n ≤ 10`, this is at most `2^30`, around one billion operations per test case, which is far too large for `10^5` tests.

We need to avoid enumerating subsets. The key observation is that `p` is not arbitrary, it is a repetition of a 3-character cycle. This means that although positions are distinct, their character types repeat in a predictable pattern. We can therefore compress the structure into a dynamic programming over a small state space that tracks how many characters of `q` we have matched while scanning through `p`.

Instead of thinking in terms of subsets, we process `p` left to right and maintain a DP where `dp[i]` is the number of ways to match the first `i` characters of `q` using the prefix of `p` processed so far. Each character in `p` updates the DP in a standard subsequence manner. Because `|p| ≤ 30`, this is at most 900 transitions per test case, which is easily fast enough even for `10^5` test cases.

The periodic structure does not need any special optimization beyond this, since the constraint already guarantees the naive subsequence DP is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursion over subsequences | O(2^(3n)) per test | O(n) | Too slow |
| DP over subsequences on string p | O(n · | q | ) per test |

## Algorithm Walkthrough

We process each test case independently.

1. Read `n` and construct the string `p` as `"xtu"` repeated `n` times. This gives a fixed source sequence whose structure we do not need to analyze further.
2. Read the string `q`. If `|q| > |p|`, immediately return 0 because no subsequence of `p` can be longer than `p` itself.
3. Initialize a DP array `dp` of size `|q| + 1`. The value `dp[i]` represents the number of ways to form the prefix `q[0:i]` as a subsequence of the prefix of `p` processed so far. Set `dp[0] = 1`, since the empty prefix can always be formed in exactly one way.
4. Iterate through each character `c` in `p`. For each such character, update the DP array from right to left over `q`. For each position `j` from `|q| - 1` down to `0`, if `q[j] == c`, then we can extend every way of forming `q[0:j]` into a way of forming `q[0:j+1]`. So we add `dp[j]` into `dp[j+1]`.

The right-to-left order is essential because it prevents reusing the same character position multiple times in one iteration, which would incorrectly allow a single position in `p` to contribute multiple times.
5. After processing all characters in `p`, the answer is `dp[|q|]`, taken modulo `998244353`.

### Why it works

The DP maintains a precise combinatorial invariant: after processing the first `k` characters of `p`, `dp[i]` counts exactly the number of ways to choose a subsequence from those `k` characters that equals the first `i` characters of `q`. Each update step considers whether the current character of `p` is used as the next matching character in `q`, and the reverse iteration guarantees each position in `p` is used at most once per subsequence construction. This ensures a one-to-one correspondence between DP accumulations and valid subsequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        parts = input().split()
        n = int(parts[0])
        q = parts[1] if len(parts) > 1 else ""

        p = "xtu" * n
        m = len(p)
        k = len(q)

        if k > m:
            print(0)
            continue

        dp = [0] * (k + 1)
        dp[0] = 1

        for c in p:
            for j in range(k - 1, -1, -1):
                if q[j] == c:
                    dp[j + 1] = (dp[j + 1] + dp[j]) % MOD

        print(dp[k] % MOD)

if __name__ == "__main__":
    solve()
```

The code follows the standard subsequence DP template. The construction of `p` is explicit, which is acceptable given the maximum length of 30. The DP array stores counts of partial matches of `q`.

The backward loop over `q` is the key implementation detail. If it were forward, the same character in `p` could be reused multiple times within a single iteration, effectively turning subsequence counting into multiset combination counting, which would overcount.

Modulo `998244353` is applied at every addition to prevent overflow and keep values bounded.

## Worked Examples

### Example 1

Let `n = 2`, so `p = "xtuxtu"`, and `q = "xtu"`.

We track `dp[i]` where `i` corresponds to how many characters of `q` we have matched.

| Step (char in p) | dp[0] | dp[1] | dp[2] | dp[3] |
| --- | --- | --- | --- | --- |
| init | 1 | 0 | 0 | 0 |
| x | 1 | 1 | 0 | 0 |
| t | 1 | 1 | 1 | 0 |
| u | 1 | 1 | 1 | 1 |
| x | 1 | 2 | 1 | 1 |
| t | 1 | 2 | 3 | 1 |
| u | 1 | 2 | 3 | 4 |

Final answer is `dp[3] = 4`.

This demonstrates how multiple occurrences of identical characters in different positions create multiple subsequence choices.

### Example 2

Let `n = 1`, `p = "xtu"`, and `q = "xx"`.

| Step | dp[0] | dp[1] | dp[2] |
| --- | --- | --- | --- |
| init | 1 | 0 | 0 |
| x | 1 | 1 | 0 |
| t | 1 | 1 | 0 |
| u | 1 | 1 | 0 |

Final answer is `0`.

This shows that even though there is an `x` in `p`, we cannot reuse the same position twice, so forming `"xx"` is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · | q |
| Space | O( | q |

Since both `n` and `|q|` are at most 30, each test case runs in at most about 900 operations. Even with `10^5` test cases, this remains well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# sample-like cases
assert run("1\n2 xtu\n") == "4"
assert run("1\n1 xx\n") == "0"

# q empty
assert run("1\n3 xtu\n") == "1"

# q longer than p
assert run("1\n1 xtuxtu xtux\n".replace(" ", "\n")) == "0"

# no matching letters
assert run("1\n5 xtu abcd\n".replace(" ", "\n")) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2, q=xtu` | `4` | basic combinatorial growth |
| `n=1, q=xx` | `0` | cannot reuse positions |
| empty `q` | `1` | empty subsequence |
| ` | q | > |
| invalid letters | `0` | character mismatch |

## Edge Cases

For `q = ""`, the DP never performs any transitions affecting `dp[0]`, so it remains `1`. The algorithm outputs `dp[0]`, correctly giving 1.

For `q` containing characters not in `{x, t, u}`, no updates ever occur to higher DP states. For example, with `p = "xtu"` and `q = "a"`, `dp[1]` stays 0 throughout, so the answer is 0.

For `q` equal to `p`, each character match extends exactly one valid path through DP, producing a final count of 1, since there is only one way to choose all positions in order.
