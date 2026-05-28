---
title: "CF 145C - Lucky Subsequence"
description: "We are given an array of integers and must count how many subsequences of length exactly k satisfy a special restriction on lucky numbers. A number is lucky if every decimal digit is either 4 or 7. Examples are 4, 47, and 744. Numbers like 5, 17, and 467 are not lucky."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 145
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 104 (Div. 1)"
rating: 2100
weight: 145
solve_time_s: 125
verified: true
draft: false
---

[CF 145C - Lucky Subsequence](https://codeforces.com/problemset/problem/145/C)

**Rating:** 2100  
**Tags:** combinatorics, dp, math  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and must count how many subsequences of length exactly `k` satisfy a special restriction on lucky numbers.

A number is lucky if every decimal digit is either `4` or `7`. Examples are `4`, `47`, and `744`. Numbers like `5`, `17`, and `467` are not lucky.

A subsequence is formed by choosing indices from the array. Two subsequences are different if their chosen index sets differ, even if the values are identical.

The restriction is subtle. Lucky values may appear at most once inside the chosen subsequence. Unlucky values may repeat any number of times.

Suppose the array is:

```
[4, 4, 10]
```

and `k = 2`.

The subsequence formed by indices `{1,2}` is invalid because it contains two equal lucky numbers, both `4`.

The subsequences `{1,3}` and `{2,3}` are valid.

The array size reaches `10^5`, so enumerating all subsequences is impossible. There are `2^n` subsequences in total, and even checking all subsequences of size `k` would require roughly `C(100000, 50000)` operations in the worst case, which is astronomically large.

The constraints strongly suggest that we need something close to `O(n log n)` or `O(nk)` with a small constant. Since `k` can also be `10^5`, even `O(nk)` becomes dangerous unless the effective state space is much smaller than `n`.

The key structural observation is that there are very few distinct lucky numbers up to `10^9`. Every lucky number consists only of digits `4` and `7`, and has at most 10 digits. The total count is:

$\sum_{i=1}^{10} 2^i = 2046$

So although the array may contain `100000` elements, the number of distinct lucky values is at most `2046`.

Several edge cases can silently break naive implementations.

Consider:

```
3 2
4 4 4
```

The correct answer is `0`.

A careless solution might say there are `C(3,2)=3` subsequences, but every pair contains duplicate lucky value `4`, so all are invalid.

Now consider:

```
4 2
10 10 10 10
```

The correct answer is:

$\binom{4}{2}=6$

Unlucky values have no uniqueness restriction, so duplicates are completely allowed.

Another tricky case is:

```
5 3
4 4 7 10 10
```

Valid subsequences must contain at most one `4` and at most one `7`.

The valid choices are:

```
{4(first),7,10(first)}
{4(first),7,10(second)}
{4(second),7,10(first)}
{4(second),7,10(second)}
```

The answer is `4`.

A naive implementation that only tracks whether a number is lucky, instead of tracking distinct lucky values separately, would miscount.

## Approaches

The brute-force solution is straightforward conceptually. Enumerate every subsequence of size `k`, inspect its lucky elements, and reject it if some lucky value appears twice.

This works because the definition is local and easy to verify. For each chosen subset of indices, we can build a frequency map of lucky numbers and check whether all frequencies are at most one.

The problem is the number of subsets. In the worst case we would examine:

$\binom{100000}{50000}$

which is completely infeasible.

The next natural attempt is dynamic programming over positions. For each element we either take it or skip it. But if we track exactly which lucky values have already been used, the state space becomes exponential in the number of distinct lucky numbers.

The breakthrough comes from separating lucky and unlucky elements.

Unlucky numbers are easy. They have no restriction at all. If there are `u` unlucky elements and we decide to take exactly `t` of them, the number of ways is simply:

$\binom{u}{t}$

Lucky numbers are different. Suppose a lucky value `x` appears `cnt[x]` times. We may either:

1. Skip value `x` completely.
2. Choose exactly one occurrence of `x`.

If we choose it, there are `cnt[x]` different index choices.

This transforms the problem into a grouped knapsack-style DP.

Each distinct lucky value behaves like an item group contributing either:

```
0 chosen elements, 1 way
1 chosen element, cnt[x] ways
```

If there are `m` distinct lucky values, we run DP over these groups:

```
dp[j] = number of ways to choose j lucky elements
```

After computing the lucky contribution, we combine it with the unlucky contribution.

If we chose `j` lucky elements, we still need `k-j` unlucky elements. The total contribution becomes:

$dp[j] \cdot \binom{u}{k-j}$

Summing over all valid `j` gives the answer.

The crucial reduction is that the DP size depends on the number of distinct lucky values, at most `2046`, instead of `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n + m·k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read the array and classify every number as lucky or unlucky.

A number is lucky if every decimal digit is either `4` or `7`.
2. Count how many times each distinct lucky value appears.

We store frequencies in a hashmap. If value `47` appears 5 times, we remember that we may choose exactly one of those 5 positions.
3. Count the total number of unlucky elements.

These elements are unrestricted, so later we only need combinations.
4. Precompute factorials and inverse factorials modulo `10^9+7`.

This allows constant-time computation of combinations:

$\binom{n}{r}=\frac{n!}{r!(n-r)!}$
5. Initialize DP.

Let:

```
dp[j] = number of ways to choose exactly j lucky elements
```

Initially:

```
dp[0] = 1
```

because choosing nothing is always possible.
6. Process each distinct lucky value independently.

Suppose current frequency is `c`.

We iterate `j` backward and update:

```
dp[j+1] += dp[j] * c
```

The multiplication by `c` appears because we may pick any one occurrence of that lucky value.

Backward iteration prevents using the same lucky value multiple times.
7. Combine lucky and unlucky selections.

For every possible count `j` of chosen lucky elements:

```
need = k - j
```

If `0 <= need <= unlucky_count`, add:

$dp[j] \cdot \binom{unlucky}{need}$
8. Output the final sum modulo `10^9+7`.

### Why it works

The DP invariant is:

```
dp[j] = number of valid ways to choose exactly j elements
        from the processed lucky-value groups,
        using at most one occurrence from each group
```

Each distinct lucky value is processed once. During its transition we either skip the value or choose exactly one of its occurrences. Since updates go backward, the same lucky value cannot contribute twice to a single state.

After all lucky groups are processed, every valid lucky-element configuration is counted exactly once.

Unlucky elements are independent from the uniqueness restriction, so once we fix how many lucky elements are used, the remaining positions can be filled by arbitrary unlucky elements. The combination count correctly counts all such choices.

Because every valid subsequence has a unique decomposition into lucky and unlucky selections, the final summation counts every valid subsequence exactly once.

## Python Solution

```python
import sys
from collections import Counter

input = sys.stdin.readline

MOD = 10**9 + 7

def is_lucky(x):
    while x > 0:
        d = x % 10
        if d != 4 and d != 7:
            return False
        x //= 10
    return True

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    lucky_freq = Counter()
    unlucky = 0

    for x in arr:
        if is_lucky(x):
            lucky_freq[x] += 1
        else:
            unlucky += 1

    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)

    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact[n] = pow(fact[n], MOD - 2, MOD)

    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    dp = [0] * (k + 1)
    dp[0] = 1

    for cnt in lucky_freq.values():
        for j in range(k - 1, -1, -1):
            dp[j + 1] = (dp[j + 1] + dp[j] * cnt) % MOD

    ans = 0

    for lucky_taken in range(k + 1):
        need_unlucky = k - lucky_taken

        if need_unlucky <= unlucky:
            ways = dp[lucky_taken]
            ways = ways * comb(unlucky, need_unlucky) % MOD
            ans = (ans + ways) % MOD

    print(ans)

solve()
```

The first section separates lucky and unlucky values. The `Counter` stores frequencies of distinct lucky numbers, because duplicates of the same lucky value cannot both appear in a valid subsequence.

The factorial and inverse factorial arrays support fast combination queries. Computing combinations on demand with repeated modular inverses would be too slow if done many times.

The DP array is one-dimensional because each lucky value is processed exactly once. Backward iteration is essential. If we iterated forward, the same lucky value could be used multiple times during a single transition phase.

Suppose `cnt = 5`. The transition:

```
dp[j + 1] += dp[j] * 5
```

means we choose one occurrence among the 5 identical lucky numbers.

The final loop combines lucky and unlucky selections. We must check that `need_unlucky` is valid before computing combinations. Forgetting this boundary check is a common source of wrong answers.

All arithmetic is performed modulo `10^9+7`, since intermediate values become extremely large.

## Worked Examples

### Example 1

Input:

```
3 2
10 10 10
```

There are no lucky numbers.

| Step | unlucky | lucky_freq | dp |
| --- | --- | --- | --- |
| Initial parsing | 3 | {} | [1,0,0] |
| No lucky processing | 3 | {} | [1,0,0] |
| Combine j=0 | 3 | {} | answer += C(3,2)=3 |

Final answer:

```
3
```

This example shows that repeated unlucky numbers are completely allowed. The uniqueness restriction applies only to lucky values.

### Example 2

Input:

```
5 3
4 4 7 10 10
```

| Step | Current value | Frequency | dp after step |
| --- | --- | --- | --- |
| Initial | - | - | [1,0,0,0] |
| Process 4 | 2 | [1,2,0,0] |  |
| Process 7 | 1 | [1,3,2,0] |  |

There are `2` unlucky numbers.

Now combine:

| lucky_taken | need_unlucky | Contribution |
| --- | --- | --- |
| 0 | 3 | 0 |
| 1 | 2 | 3 × C(2,2) = 3 |
| 2 | 1 | 2 × C(2,1) = 4 |
| 3 | 0 | 0 |

Final answer:

```
7
```

The trace demonstrates how duplicate lucky values are compressed into a single DP group. The value `4` appears twice, but contributes only one chosen element at a time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m·k) | Array scan plus DP over distinct lucky values |
| Space | O(k) | One DP array of size `k+1` |

Here `m` is the number of distinct lucky values, bounded by `2046`.

Even in the worst case, roughly `2046 × 100000` DP transitions are manageable in Python because the operations are very small and cache-friendly. The memory usage is tiny compared to the `256 MB` limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import Counter

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def is_lucky(x):
        while x > 0:
            d = x % 10
            if d != 4 and d != 7:
                return False
            x //= 10
        return True

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    lucky_freq = Counter()
    unlucky = 0

    for x in arr:
        if is_lucky(x):
            lucky_freq[x] += 1
        else:
            unlucky += 1

    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)

    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact[n] = pow(fact[n], MOD - 2, MOD)

    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    dp = [0] * (k + 1)
    dp[0] = 1

    for cnt in lucky_freq.values():
        for j in range(k - 1, -1, -1):
            dp[j + 1] = (dp[j + 1] + dp[j] * cnt) % MOD

    ans = 0

    for lucky_taken in range(k + 1):
        need_unlucky = k - lucky_taken

        if need_unlucky <= unlucky:
            ans = (
                ans
                + dp[lucky_taken] * comb(unlucky, need_unlucky)
            ) % MOD

    return str(ans) + "\n"

# provided sample
assert run("3 2\n10 10 10\n") == "3\n", "sample 1"

# minimum size
assert run("1 1\n4\n") == "1\n", "single lucky number"

# duplicate lucky values cannot both be used
assert run("3 2\n4 4 4\n") == "0\n", "duplicate lucky restriction"

# mix of lucky and unlucky
assert run("5 3\n4 4 7 10 10\n") == "7\n", "mixed case"

# all unlucky values
assert run("5 3\n1 2 3 5 6\n") == "10\n", "pure combinations"

# choose exactly one from repeated lucky group
assert run("4 2\n47 47 1 1\n") == "5\n", "group counting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 4` | `1` | Minimum input size |
| `3 2 / 4 4 4` | `0` | Duplicate lucky values forbidden |
| `5 3 / 4 4 7 10 10` | `7` | Mixed lucky and unlucky handling |
| `5 3 / 1 2 3 5 6` | `10` | Pure combination counting |
| `4 2 / 47 47 1 1` | `5` | Choosing one occurrence from a lucky group |

## Edge Cases

Consider:

```
3 2
4 4 4
```

The algorithm creates one lucky group:

```
freq[4] = 3
```

The DP becomes:

| Step | dp |
| --- | --- |
| Initial | [1,0,0] |
| Process frequency 3 | [1,3,0] |

There is no way to reach `dp[2]`, because the same lucky value cannot be selected twice. Since there are no unlucky numbers, the final answer is `0`.

Now consider:

```
4 2
10 10 10 10
```

There are no lucky groups at all.

```
dp = [1,0,0]
unlucky = 4
```

The answer becomes:

$\binom{4}{2}=6$

This confirms that repeated unlucky values are unrestricted.

Finally, consider:

```
5 2
4 7 47 74 10
```

All lucky values are distinct.

The DP evolves as:

| After processing | dp |
| --- | --- |
| 4 | [1,1,0] |
| 7 | [1,2,1] |
| 47 | [1,3,3] |
| 74 | [1,4,6] |

There is one unlucky value.

The final answer is:

```
dp[2] * C(1,0) + dp[1] * C(1,1)
= 6 + 4
= 10
```

Every pair of distinct lucky values is valid, and each lucky value can also pair with the unlucky number.
