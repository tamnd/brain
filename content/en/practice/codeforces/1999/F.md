---
title: "CF 1999F - Expected Median"
description: "We are given a binary array containing only 0 and 1. For every subsequence of length k, where k is odd, we compute its median and add all these medians together. The array is binary, which changes the nature of the median completely."
date: "2026-06-08T14:22:34+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1999
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 964 (Div. 4)"
rating: 1500
weight: 1999
solve_time_s: 128
verified: true
draft: false
---

[CF 1999F - Expected Median](https://codeforces.com/problemset/problem/1999/F)

**Rating:** 1500  
**Tags:** combinatorics, math  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary array containing only `0` and `1`. For every subsequence of length `k`, where `k` is odd, we compute its median and add all these medians together.

The array is binary, which changes the nature of the median completely. A median of an odd-length binary sequence can only be `0` or `1`. After sorting such a sequence, the median is `1` exactly when more than half of its elements are `1`.

Let

- `z` be the number of zeros in the original array.
- `o` be the number of ones in the original array.

The task is to count how many length-`k` subsequences have median `1`, because every such subsequence contributes exactly `1` to the sum, while every subsequence with median `0` contributes `0`.

The constraints are large. The total sum of `n` over all test cases is at most `2·10^5`. Enumerating all subsequences is impossible because even `C(200000,100000)` is astronomically large. Any solution involving explicit generation of subsequences is ruled out immediately.

The limit suggests a solution around `O(n)` or `O(n log MOD)` per test case after some global preprocessing. Since the modulus is prime and combinations appear naturally, precomputing factorials and inverse factorials is a strong hint.

A few edge cases deserve attention.

Consider:

```
n = 5, k = 1
array = [1,1,1,1,1]
```

Every element itself is a subsequence. The answer is `5`. Any formula that assumes at least two elements are chosen from the subsequence would fail here.

Consider:

```
n = 5, k = 5
array = [0,1,0,1,0]
```

There is only one subsequence, the whole array. It contains two ones and three zeros, so its median is `0`. The answer is `0`. A careless implementation might count all ways to choose a majority of ones without respecting the available number of ones.

Consider:

```
n = 4, k = 3
array = [1,0,1,1]
```

Every length-3 subsequence has at least two ones, so every median equals `1`. The answer is `4`. This case checks whether the threshold for a majority is computed correctly as `(k+1)/2`.

## Approaches

The most direct approach is to generate every length-`k` subsequence, sort it, compute its median, and accumulate the result.

This is correct because it follows the definition exactly. Unfortunately, the number of subsequences is

$$\binom{n}{k}$$

which is already enormous for moderate values of `n`. Even for `n = 50` and `k = 25`, the count exceeds $10^{14}$. The brute-force approach is completely infeasible.

The key observation is that the positions of zeros and ones do not matter. Only how many zeros and ones are chosen matters.

Since the array is binary, the median of a length-`k` subsequence is `1` if and only if the subsequence contains at least

$$\frac{k+1}{2}$$

ones.

Let

$$m=\frac{k+1}{2}.$$

Suppose a subsequence contains exactly `i` ones. Then it contains `k-i` zeros. Such subsequences exist in

$$\binom{o}{i}\binom{z}{k-i}$$

ways, because we independently choose which ones and which zeros participate.

Every subsequence with `i ≥ m` contributes `1` to the answer. Every subsequence with `i < m` contributes `0`.

So the answer becomes

$$\sum_{i=m}^{k} \binom{o}{i} \binom{z}{k-i}.$$

Now the problem is reduced to evaluating a combinatorial sum.

Since `n` across all test cases is at most `2·10^5`, we can precompute factorials and inverse factorials once and answer every combination query in `O(1)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O\left(\binom{n}{k}\cdot k\log k\right)$ | $O(k)$ | Too slow |
| Optimal | $O(n + k)$ per test case after preprocessing | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Count the number of ones `o` in the array.
2. Compute the number of zeros as `z = n - o`.
3. Let

$$m=\frac{k+1}{2}.$$

Any subsequence with at least `m` ones has median `1`.
4. Precompute factorials and inverse factorials modulo `10^9+7` up to `2·10^5`.

This allows every combination value to be evaluated in constant time.
5. Iterate `i` from `m` to `k`.
6. For each `i`, interpret it as the number of ones chosen.
7. The number of valid subsequences with exactly `i` ones equals

$$\binom{o}{i}\binom{z}{k-i}.$$

If either combination is impossible, treat it as zero.
8. Add this quantity to the answer modulo `10^9+7`.
9. Output the final sum.

### Why it works

A binary subsequence has median `1` exactly when strictly more than half of its elements are `1`. Since `k` is odd, this condition is equivalent to having at least `(k+1)/2` ones.

Every valid subsequence can be uniquely classified by the exact number `i` of ones it contains. For a fixed `i`, choosing the subsequence is equivalent to choosing `i` elements from the `o` available ones and `k-i` elements from the `z` available zeros. This gives exactly

$$\binom{o}{i}\binom{z}{k-i}$$

subsequences.

The categories for different values of `i` are disjoint and cover all subsequences whose median is `1`. Summing over all `i ≥ (k+1)/2` counts every contributing subsequence exactly once, which is precisely the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAXN = 200000

fact = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    fact[i] = fact[i - 1] * i % MOD

inv_fact = [1] * (MAXN + 1)
inv_fact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)

for i in range(MAXN, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

t = int(input())

for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    ones = sum(a)
    zeros = n - ones

    need = (k + 1) // 2

    ans = 0

    for i in range(need, k + 1):
        ans = (ans + C(ones, i) * C(zeros, k - i)) % MOD

    print(ans)
```

The preprocessing computes factorials and inverse factorials once. Since the modulus is prime, Fermat's little theorem gives

$$x^{-1}=x^{MOD-2}\pmod{MOD}.$$

The helper function `C(n,r)` returns zero whenever the combination is impossible. This is crucial because values such as `C(3,5)` must contribute nothing to the sum.

For each test case, only the counts of zeros and ones matter. The actual arrangement of elements never appears in the formula.

The loop over `i` starts at `(k+1)//2` because this is the smallest number of ones that can make the median equal to `1`.

## Worked Examples

### Example 1

Input:

```
n = 4
k = 3
array = [1,0,0,1]
```

We have:

- `ones = 2`
- `zeros = 2`
- `need = 2`

| i | C(ones,i) | C(zeros,k-i) | Contribution |
| --- | --- | --- | --- |
| 2 | 1 | 2 | 2 |
| 3 | 0 | 1 | 0 |

Answer = `2`.

This matches the sample. There are exactly two length-3 subsequences whose median equals `1`.

### Example 2

Input:

```
n = 6
k = 3
array = [1,0,1,0,1,1]
```

We have:

- `ones = 4`
- `zeros = 2`
- `need = 2`

| i | C(4,i) | C(2,3-i) | Contribution |
| --- | --- | --- | --- |
| 2 | 6 | 2 | 12 |
| 3 | 4 | 1 | 4 |
| 4 | 1 | 0 | 0 |

Total answer:

$$12 + 4 = 16.$$

This equals the sample output.

The example demonstrates the central idea: count subsequences by how many ones they contain rather than enumerating them individually.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(200000) + O(k)$ per test case | Preprocessing once, then one summation loop |
| Space | $O(200000)$ | Factorial and inverse-factorial arrays |

The global preprocessing costs about two hundred thousand operations. Across all test cases, the total input size is at most `2·10^5`, so the solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 10**9 + 7
MAXN = 200000

fact = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    fact[i] = fact[i - 1] * i % MOD

inv_fact = [1] * (MAXN + 1)
inv_fact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)

for i in range(MAXN, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        ones = sum(a)
        zeros = n - ones
        need = (k + 1) // 2

        ans = 0
        for i in range(need, k + 1):
            ans = (ans + C(ones, i) * C(zeros, k - i)) % MOD

        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run(
"""8
4 3
1 0 0 1
5 1
1 1 1 1 1
5 5
0 1 0 1 0
6 3
1 0 1 0 1 1
4 3
1 0 1 1
5 3
1 0 1 1 0
2 1
0 0
34 17
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
"""
) == """2
5
0
16
4
7
0
333606206"""

# minimum size
assert run(
"""1
1 1
0
"""
) == "0"

# single one
assert run(
"""1
1 1
1
"""
) == "1"

# all ones
assert run(
"""1
5 3
1 1 1 1 1
"""
) == "10"

# all zeros
assert run(
"""1
5 3
0 0 0 0 0
"""
) == "0"

# boundary majority
assert run(
"""1
3 3
1 1 0
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `0` | Smallest possible instance |
| `1 1 / 1` | `1` | Length-1 subsequences |
| Five ones, `k=3` | `10` | Every subsequence contributes |
| Five zeros, `k=3` | `0` | No subsequence contributes |
| `[1,1,0]`, `k=3` | `1` | Majority threshold equals `(k+1)/2` |

## Edge Cases

Consider:

```
1
5 1
1 1 1 1 1
```

Here `need = 1`. The summation contains only `i = 1`:

$$\binom{5}{1}\binom{0}{0}=5.$$

The algorithm returns `5`, matching the fact that every element forms a valid subsequence.

Consider:

```
1
5 5
0 1 0 1 0
```

We have `ones = 2`, `zeros = 3`, and `need = 3`.

Every term requires choosing at least three ones, which is impossible:

$$\binom{2}{3}=0.$$

All contributions vanish, producing answer `0`. The algorithm naturally handles this through the combination function.

Consider:

```
1
4 3
1 0 1 1
```

We have `ones = 3`, `zeros = 1`, and `need = 2`.

The computation is

$$\binom{3}{2}\binom{1}{1} + \binom{3}{3}\binom{1}{0} = 3+1 = 4.$$

All four length-3 subsequences contribute, so the answer is `4`. This confirms that the majority threshold is implemented correctly and that every valid composition is counted exactly once.
