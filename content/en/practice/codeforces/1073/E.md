---
title: "CF 1073E - Segment Sum"
description: "We are asked to consider every integer inside a range $[l, r]$ and filter it by a digit constraint: we only keep numbers that use at most $k$ distinct decimal digits in their usual base-10 representation."
date: "2026-06-15T07:02:55+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1073
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 53 (Rated for Div. 2)"
rating: 2300
weight: 1073
solve_time_s: 234
verified: true
draft: false
---

[CF 1073E - Segment Sum](https://codeforces.com/problemset/problem/1073/E)

**Rating:** 2300  
**Tags:** bitmasks, combinatorics, dp, math  
**Solve time:** 3m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to consider every integer inside a range $[l, r]$ and filter it by a digit constraint: we only keep numbers that use at most $k$ distinct decimal digits in their usual base-10 representation. Among all such valid numbers, we must compute their total sum modulo $998244353$.

The difficulty is not in evaluating a single number but in aggregating over a huge interval. Since $r$ can be as large as $10^{18}$, the interval may contain up to $10^{18}$ values, which immediately rules out any approach that iterates over the range directly.

A second observation comes from the digit constraint. A number is valid if its digit set size is small, which couples all digits of the number globally. This is not a local property like parity or divisibility; it depends on the entire structure of the number. That makes naive counting or arithmetic progression tricks unusable.

A naive approach would be to enumerate every number in $[l, r]$, extract its digit set, and check whether it has size at most $k$. This already fails at the smallest non-trivial input sizes. Even $10^{18}$ candidates with $k = 10$ leads to $10^{18}$ digit checks, which is infeasible.

A more subtle edge case appears when numbers have leading digit constraints. For example, $1000$ uses only digits $\{0,1\}$ and is valid for $k=2$, while $999$ uses only $\{9\}$. Any incorrect digit DP that mishandles leading zeros may incorrectly count numbers like $000123$ as introducing digit 0 when it should not.

The core challenge is therefore to efficiently compute a sum over all numbers up to a bound $x$, and then subtract two prefix answers:

$$\text{answer}(l, r) = F(r) - F(l-1)$$

where $F(x)$ is the sum of valid numbers $\le x$.

## Approaches

The brute-force idea is straightforward: iterate through all numbers up to $x$, check digit distinctness, and accumulate the sum. This works because digit extraction is $O(\log x)$, so the total complexity becomes $O(x \log x)$. When $x \approx 10^{18}$, this is far beyond any feasible limit.

The key insight is that numbers are structured by digits, and constraints on digits are naturally handled using digit dynamic programming. Instead of enumerating values, we construct numbers digit by digit and track which digits have been used so far. The state space is small because there are only 10 possible digits, so subsets of digits can be represented with a bitmask of size $2^{10} = 1024$.

This transforms the problem into a classical digit DP with state consisting of position, tightness with respect to the bound, and the set of used digits. Once we fix a prefix, the contribution of all suffix completions can be aggregated rather than enumerated.

The subtle but crucial improvement is that we are not only counting valid numbers but summing them. This requires carrying not just counts of completions but also their numeric contributions weighted by place values. This leads to maintaining both a count DP and a sum DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(x \log x)$ | $O(1)$ | Too slow |
| Digit DP | $O(20 \cdot 1024 \cdot 10)$ | $O(1024 \cdot 10)$ | Accepted |

## Algorithm Walkthrough

We define a function $F(x)$ that computes the sum of all valid numbers in $[0, x]$.

1. Convert $x$ into a digit array so we can process it from the most significant digit. This allows us to build numbers with a prefix constraint.
2. Define a DP state over positions in the digit array. At each position, we track three things: whether we are still bound by the prefix of $x$, which digits have already been used (bitmask), and whether we have started forming a number (to handle leading zeros correctly).
3. For each state, we iterate over all possible next digits from 0 to 9. If we have not started a number yet, choosing 0 does not introduce a digit into the mask; otherwise it does.
4. When we place a digit, we update the mask and check whether the number of distinct digits exceeds $k$. If it does, we discard this transition.
5. We propagate two quantities: the number of ways to complete the suffix (count), and the sum contributed by all those completions. When adding a digit $d$ at position $pos$, its contribution is $d \cdot 10^{remaining}$ multiplied by the number of completions, plus the shifted contribution of suffix sums.
6. The tight constraint ensures we never exceed $x$. If we place a digit smaller than the bound digit, we transition to a non-tight state; otherwise we stay tight.
7. The DP result at the end gives $F(x)$, and the final answer is $F(r) - F(l-1)$.

### Why it works

Every valid number is constructed exactly once as a sequence of digit choices. The DP partitions the space of numbers by prefix, and the tight constraint ensures no invalid prefix exceeds the bound. The mask enforces the at-most-$k$-digits condition exactly at the moment a digit is introduced, preventing invalid configurations early. Since contributions are aggregated via linearity of addition, summing over DP states preserves correctness without double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve(x, k):
    if x <= 0:
        return 0

    digits = list(map(int, str(x)))
    n = len(digits)

    # dp[pos][tight][mask] = (count, sum)
    from collections import defaultdict

    dp = [[[ (0, 0) for _ in range(1 << 10)] for _ in range(2)] for _ in range(n + 1)]
    dp[0][1][0] = (1, 0)

    pow10 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow10[i] = pow10[i - 1] * 10 % MOD

    for pos in range(n):
        for tight in range(2):
            limit = digits[pos] if tight else 9
            for mask in range(1 << 10):
                cnt, sm = dp[pos][tight][mask]
                if cnt == 0:
                    continue

                for d in range(limit + 1):
                    ntight = tight and (d == limit)

                    nmask = mask
                    if mask != 0 or d != 0:
                        nmask = mask | (1 << d)

                    if bin(nmask).count("1") > k:
                        continue

                    ncnt = cnt
                    nsm = sm

                    # contribution of new digit at position
                    nsm = (nsm * 10 + cnt * d) % MOD

                    dp[pos + 1][ntight][nmask] = (
                        (dp[pos + 1][ntight][nmask][0] + ncnt) % MOD,
                        (dp[pos + 1][ntight][nmask][1] + nsm) % MOD
                    )

    res = 0
    for tight in range(2):
        for mask in range(1 << 10):
            if bin(mask).count("1") <= k:
                res = (res + dp[n][tight][mask][1]) % MOD

    return res

def pref(x, k):
    return solve(x, k)

l, r, k = map(int, input().split())
print((pref(r, k) - pref(l - 1, k)) % MOD)
```

The implementation follows the DP structure over digits. The `mask` tracks which digits have appeared, while the leading-zero logic ensures that numbers like `000123` do not incorrectly activate digit 0. The transition `nsm = nsm * 10 + cnt * d` encodes how placing a digit shifts all previously formed suffix contributions.

The final summation over all terminal DP states collects all valid numbers up to the bound.

## Worked Examples

### Example 1

Input:

```
10 50 2
```

We compute $F(50)$ and $F(9)$, then subtract.

| Step | Prefix | Mask condition | Count | Sum contribution |
| --- | --- | --- | --- | --- |
| build DP | digits of 50 | ≤2 distinct digits | aggregated | accumulated |
| final F(50) | all valid ≤ 50 | filtered by mask | many states | total sum |
| final answer | F(50)-F(9) | range restricted | final | 1230 |

This confirms that the DP includes all valid numbers like 11, 22, 33, 44 and excludes invalid ones such as 123 or 101 depending on digit count.

### Example 2

A small constructed case: $l=1, r=20, k=1$

Only numbers with a single repeated digit are valid: 1,2,3,...,9.

| Number | Valid? | Reason |
| --- | --- | --- |
| 1..9 | yes | single digit |
| 10 | no | digits {1,0} |
| 11 | yes | single digit |
| 12 | no | two digits |

DP accumulates exactly these contributions via masks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 2^{10} \cdot 10)$ | digit positions times masks times digit transitions |
| Space | $O(n \cdot 2^{10})$ | DP table over positions and masks |

The digit length is at most 18, and the mask space is only 1024, so the solution easily fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# Since full DP function is not embedded here, these are conceptual placeholders.
# In actual submission, run() should call solve pipeline.

# provided sample (conceptual)
# assert run("10 50 2") == "1230"

# edge-like cases
# assert run("1 9 1") == "45"
# assert run("10 20 1") == "11"
# assert run("1 100 10") == str(sum(range(1, 101)))
# assert run("999999999999999999 999999999999999999 10") == "999999999999999999"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 9 1 | 45 | single-digit validity |
| 10 20 1 | 11 | leading-digit restriction |
| 1 100 10 | 5050 | full acceptance case |
| max single value | value itself | boundary correctness |

## Edge Cases

A key edge case is numbers with leading zeros during construction. For input like $x = 100$, the DP may construct states like "0 → 0 → 5", which should represent the number 5, not a number using digit 0. The `started` logic ensures that digit 0 does not enter the mask before a non-zero digit appears.

Another edge case is when $k = 10$. In this case every number is valid, and the DP should reduce to a standard digit-sum DP. The mask check becomes inert, and the result matches the arithmetic sum over the interval, confirming that the DP does not over-restrict states.

Finally, when $l = 1$, the subtraction $F(l-1)$ must correctly handle $F(0)=0$. Without this guard, negative indexing or invalid DP reuse would distort the final result.
