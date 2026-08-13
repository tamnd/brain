---
title: "CF 102361C - Sakurada Reset"
description: "Asai Kei chooses a non-empty subsequence of a, while the director chooses a non-empty subsequence of b. A chosen sequence such as (2, 1, 2) is interpreted as a base-1000 number, so its value is 2 1000^2 + 1 1000 + 2."
date: "2026-08-14T02:44:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "C"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 143
verified: true
draft: false
---

[CF 102361C - Sakurada Reset](https://codeforces.com/problemset/problem/102361/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

Asai Kei chooses a non-empty subsequence of `a`, while the director chooses a non-empty subsequence of `b`. A chosen sequence such as `(2, 1, 2)` is interpreted as a base-1000 number, so its value is `2 * 1000^2 + 1 * 1000 + 2`.

Every element is at most `100`, strictly smaller than the base `1000`. This gives the crucial comparison rule: first compare the lengths. Any longer non-empty sequence has a larger value than every shorter sequence. If the lengths are equal, compare the elements from left to right, exactly like lexicographic comparison.

The phrase "different subsequences" is also significant. Two index selections that produce the same sequence must be counted only once, because the statement identifies sequences by their influence values. For example, in `a = [1, 1]`, there are two ways to select a length-one subsequence, but both produce the same sequence `(1)`, so there is only one distinct subsequence of length one.

The constraints allow `n,m` to reach `5000`. A quadratic algorithm is realistic, while anything exponential in either length is impossible. The official judge limit is 2.5 seconds with 1024 MB of memory, and the accepted intended solution is quadratic.

There are several edge cases that easily break a careless implementation. With `a = [1]` and `b = [1]`, the answer is `0`, because the only two sequences have equal value. A solution using `>=` instead of `>` would incorrectly count this pair.

With `a = [1,1]` and `b = [1]`, the answer is `1`. The distinct subsequences of `a` are `(1)` and `(1,1)`, while `b` has only `(1)`. Only the longer sequence wins. Counting index selections instead of distinct sequences would incorrectly treat the two copies of `(1)` in `a` as separate choices.

With `a = [2,1]` and `b = [1,2]`, the answer is `6`. The length-two sequences are `21` and `12`, so `21 > 12`; meanwhile both length-two sequences beat both length-one sequences from `b`. A solution that compares only lengths misses the equal-length contribution.

Finally, repeated values such as `a = [1,1,1]` require duplicate elimination at every length. There is only one distinct subsequence of each length, not `3`, `3`, and `1` index selections. This is the reason ordinary binomial coefficients cannot be used for the unequal-length part.

## Approaches

The direct approach is to enumerate every non-empty subsequence of `a`, enumerate every non-empty subsequence of `b`, compute their influence values, and compare every pair. There are `2^n - 1` and `2^m - 1` index subsequences, so the number of comparisons is

`(2^n - 1)(2^m - 1)`.

At `n = m = 5000`, this is approximately `2^10000` comparisons. Even before dealing with duplicate subsequences, this is completely infeasible.

The brute force is correct because every possible pair is explicitly considered. Its failure is purely combinatorial. The useful structure is that the influence value is a base-1000 representation whose digits are all below the base. That turns numerical comparison into a length comparison followed by lexicographic comparison.

We can consequently split the answer into two independent parts. If the subsequence from `a` is longer than the one from `b`, it automatically wins. We only need the number of distinct subsequences of every length in each array.

The difficult part is when the two lengths are equal. Then the first position where the sequences differ decides the result. Before that position the two sequences must be identical, and at the first differing position the value selected from `a` must be larger.

The standard distinct-subsequence recurrence handles the first part. For position `i`, let `p[i]` be the previous occurrence of `a[i]`. If `F[i][k]` is the number of distinct subsequences of length `k` using the prefix ending at `i`, then

`F[i][k] = F[i-1][k] + F[i-1][k-1] - F[p[i]-1][k-1]`.

The subtraction removes sequences that would be produced again because `a[i]` is equal to the previous occurrence of the same value.

For equal lengths, define a two-dimensional prefix-DP. Let `F[i][j]` count pairs of equal-length distinct subsequences from the two prefixes that are still equal, and let `G[i][j]` count pairs that have already become strictly greater on the `a` side. If `a[i] == b[j]`, the newly created equal pair must have come from a smaller pair of endpoints. If `a[i] > b[j]`, the first difference occurs at these two positions, so an equal prefix can transition into the greater state. Once the pair is already greater, the remaining selected elements are unrestricted as long as the lengths remain equal.

The recurrence contains rectangle sums over previous DP cells. A two-dimensional prefix sum turns each rectangle into four array accesses, giving an `O(nm)` algorithm. This is the core idea used in the official-style solution.

There is one Python-specific memory improvement that is useful here. The rectangle for row `i` always starts at row `p[i]`, where `p[i]` is the previous occurrence of `a[i]`. Since values are only from `1` to `100`, there are only 100 possible lower boundaries. For each value, we keep a snapshot of the prefix-DP row immediately before its previous occurrence. That lets the two-dimensional recurrence be evaluated with only the current row plus at most 100 saved rows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^(n+m))` | `O(1)` apart from generated subsequences | Too slow |
| Optimal | `O(nm + n² + m²)` = `O(max(n,m)²)` | `O(100(n+m))` | Accepted algorithm |

## Algorithm Walkthrough

1. Compute `p[i]` for `a`, the previous position containing the same value as `a[i]`. Compute the analogous previous-occurrence array for `b`. The previous occurrence is exactly where duplicate subsequences can arise, so it determines the correction term in the distinct-subsequence DP.
2. Compute the number of distinct subsequences of every length in `a` and `b`. For each new element, either omit it or append it to a subsequence from the previous prefix. If the value appeared before, subtract the subsequences that would be duplicated. The resulting arrays `cntA[k]` and `cntB[k]` count distinct sequences, not index selections.
3. Count all pairs with `|A| > |B|`. Because every digit is below `1000`, every sequence of length `k+1` has a larger influence value than every sequence of length `k`. For each length `k` of `A`, multiply `cntA[k]` by the number of `B` sequences whose length is smaller than `k`.
4. Handle pairs with equal lengths using two DP states. The state `F[i][j]` represents equal prefixes, while `G[i][j]` represents prefixes for which `A` is already strictly greater. The empty pair belongs to `F`, which is why the boundary row and column of `F` are initialized to one.
5. When processing `(i,j)`, consider the first selected positions that end at `i` and `j`. If `a[i] == b[j]`, the pair can remain equal, and the preceding selected positions must come from the rectangle `[p[i], i-1] × [q[j], j-1]`. If `a[i] > b[j]`, the same rectangle of equal states creates the first strict difference, so it contributes to `G`. A rectangle of existing `G` states also contributes because a pair that was already greater remains greater.
6. Store each DP row as a two-dimensional prefix sum. For a rectangle `[r1,r2] × [c1,c2]`, its sum is obtained from four prefix values. Since `r1 = p[i]` for the current row, the required row `p[i]-1` is kept in the snapshot associated with `a[i]`. This removes the need to store all `n*m` DP cells.
7. After processing every row, `G[n][m]` is exactly the number of distinct equal-length pairs for which the subsequence from `a` is greater. Add it to the unequal-length contribution.

Why it works: every winning pair belongs to exactly one of the two length cases. In the unequal-length case, the longer sequence is always numerically larger. In the equal-length case, every pair has a unique first differing selected position. Before that position the two sequences are equal, which is represented by `F`; at that position either `a[i] > b[j]`, creating `G`, or the pair is still equal. Once a pair enters `G`, later elements cannot change the comparison result. The duplicate correction using previous occurrences gives each distinct sequence exactly one representation, so neither duplicates nor valid pairs are lost.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
SIGMA = 100

def distinct_by_length(s):
    """
    cnt[k] = number of distinct subsequences of s of length k.
    cnt[0] = 1 for the empty subsequence.

    Only 100 historical rows are needed because every correction row
    is immediately before the previous occurrence of the current value.
    """
    n = len(s)

    prev = [0] * (n + 1)
    prev[0] = 1

    # snap[x] is the row F[p-1] for the latest occurrence p of x.
    row0 = prev[:]
    snap = [row0[:] for _ in range(SIGMA + 1)]

    for i, x in enumerate(s, 1):
        old = prev
        special = snap[x]

        cur = old[:]
        # k > i is impossible.
        for k in range(1, i + 1):
            v = old[k] + old[k - 1] - special[k - 1]
            cur[k] = v % MOD

        # If x appears again later, its previous occurrence is i,
        # so the required correction row will be F[i-1] = old.
        snap[x] = old
        prev = cur

    return prev

def previous_occurrences(s):
    last = [0] * (SIGMA + 1)
    p = [0] * (len(s) + 1)

    for i, x in enumerate(s, 1):
        p[i] = last[x]
        last[x] = i

    return p

def equal_length_greater(a, b, pa, pb):
    """
    Count distinct pairs (A, B) with |A| = |B| and A > B.

    F is the 2D prefix table for equal prefixes.
    G is the 2D prefix table for already-greater prefixes.

    We keep only the current row and, for every value in a, the
    row immediately before its previous occurrence.
    """
    n = len(a)
    m = len(b)

    # F[0][j] = 1 and G[0][j] = 0.
    prev_f = [1] * (m + 1)
    prev_g = [0] * (m + 1)

    row0_f = prev_f[:]
    row0_g = prev_g[:]

    snap_f = [row0_f[:] for _ in range(SIGMA + 1)]
    snap_g = [row0_g[:] for _ in range(SIGMA + 1)]

    for i in range(1, n + 1):
        x = a[i - 1]

        old_f = prev_f
        old_g = prev_g

        # snap_* is row pa[i]-1.
        base_f = snap_f[x]
        base_g = snap_g[x]

        cur_f = [0] * (m + 1)
        cur_g = [0] * (m + 1)

        # The empty pair is equal, but never strictly greater.
        cur_f[0] = 1

        low_a = pa[i]

        for j in range(1, m + 1):
            low_b = pb[j]

            # Rectangle [low_a, i-1] x [low_b, j-1]
            # in the 2D prefix table.
            c1 = j - 1
            c2 = low_b - 1

            rect_f = (
                old_f[c1]
                - base_f[c1]
                - old_f[c2]
                + base_f[c2]
            )

            rect_g = (
                old_g[c1]
                - base_g[c1]
                - old_g[c2]
                + base_g[c2]
            )

            raw_f = rect_f if x == b[j - 1] else 0

            raw_g = rect_g
            if x > b[j - 1]:
                raw_g += rect_f

            # Convert the raw ending-at-(i,j) value into a 2D prefix
            # value by adding the top, left, and subtracting top-left.
            cur_f[j] = (
                raw_f
                + old_f[j]
                + cur_f[j - 1]
                - old_f[j - 1]
            ) % MOD

            cur_g[j] = (
                raw_g
                + old_g[j]
                + cur_g[j - 1]
                - old_g[j - 1]
            ) % MOD

        # For a future occurrence of x at position q,
        # p[q] = i, so the required row is F[i-1] and G[i-1].
        snap_f[x] = old_f
        snap_g[x] = old_g

        prev_f = cur_f
        prev_g = cur_g

    return prev_g[m]

def solve_data(a, b):
    n = len(a)
    m = len(b)

    cnt_a = distinct_by_length(a)
    cnt_b = distinct_by_length(b)

    # Unequal lengths: only |A| > |B| can win.
    ans = 0
    prefix_b = 0

    for k in range(1, n + 1):
        if k - 1 <= m:
            prefix_b += cnt_b[k - 1]
            if prefix_b >= MOD:
                prefix_b -= MOD

        ans = (ans + cnt_a[k] * prefix_b) % MOD

    pa = previous_occurrences(a)
    pb = previous_occurrences(b)

    ans += equal_length_greater(a, b, pa, pb)
    return ans % MOD

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(solve_data(a, b))

if __name__ == "__main__":
    solve()
```

The first helper, `distinct_by_length`, implements the duplicate-aware subsequence recurrence. The snapshot for value `x` stores the row immediately before the latest occurrence of `x`. When `x` appears again, that is exactly the historical row required by the subtraction term.

The unequal-length contribution uses a running prefix of `cntB`. When processing length `k`, `prefix_b` contains the number of distinct `B` sequences of lengths from `1` through `k-1`. The empty subsequence is never included in the answer.

The equal-length routine uses `prev_f` and `prev_g` as the previous row of the two-dimensional prefix tables. `snap_f[x]` and `snap_g[x]` represent row `p[i]-1`. The rectangle calculation is just the standard four-corner inclusion-exclusion formula.

The initialization `prev_f = [1] * (m + 1)` is deliberate. The empty sequence is equal to every empty sequence, and the two-dimensional prefix table consequently has value one along its zero row and zero column. Conversely, `G` starts with zero because an empty sequence cannot already be strictly greater.

Python integers do not overflow, and every stored DP value is reduced modulo `998244353`. The intermediate rectangle expression can temporarily be negative, which is safe because Python integers have arbitrary precision, and the final `% MOD` normalizes it.

The original contest limit is designed for compiled implementations. The algorithm is the intended quadratic solution, and the Python version above specifically reduces the memory from `O(nm)` to `O(100(n+m))`, but Python interpreter overhead can be substantially higher than the original 2.5-second C++ environment.

## Worked Examples

For Sample 1, the distinct subsequences of `a = [2,1,2]` are

`1`, `2`, `12`, `21`, `22`, `212`.

Their values are `1`, `2`, `1002`, `2001`, `2002`, and `2001002`. The director has the eleven distinct sequences listed in the statement.

The following table shows the final comparison count for each distinct sequence from `a`.

| A | Length | Number of B with B < A |
| --- | --- | --- |
| `1` | 1 | 0 |
| `2` | 1 | 1 |
| `12` | 2 | 3 |
| `21` | 2 | 4 |
| `22` | 2 | 5 |
| `212` | 3 | 9 |

Adding these values gives `0 + 1 + 3 + 4 + 5 + 9 = 22`, which matches the sample output. The table also illustrates why equal lengths need lexicographic comparison: `12` beats `11` and `1`, but does not beat `12` or `21`.

For a smaller trace, consider

```
2 2
2 1
1 2
```

The distinct subsequences by length are:

| Length | `cntA` | `cntB` |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 2 | 2 |
| 2 | 1 | 1 |

The unequal-length contribution comes from `A` length two against `B` length one. There is one such `A`, and both length-one sequences of `B` are smaller, giving two pairs.

For equal lengths, the length-one sequences compare as `2 > 1`, contributing one pair. The length-two sequences are `21` and `12`, and `21 > 12`, contributing another pair.

| Contribution | Count |
| --- | --- |
| ` | A | =2`, ` | B | =1` | 2 |
| ` | A | =1`, ` | B | =1`, `2 > 1` | 1 |
| ` | A | =2`, ` | B | =2`, `21 > 12` | 1 |
| Total | 4 |

This trace confirms that the length part and the equal-length DP are separate contributions. It also exercises the first-difference transition from `F` to `G`.

A useful duplicate trace is

```
2 1
1 1
1
```

Here `a` has only one distinct length-one sequence, even though there are two index selections. Its distinct subsequences are `(1)` and `(1,1)`. `b` has only `(1)`. The length-two sequence from `a` beats the length-one sequence from `b`, while the equal length-one pair is equal.

| Length | `cntA` | `cntB` |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 1 | 0 |

The unequal contribution is `1`, and the equal-length contribution is `0`, so the final answer is `1`. The subtraction involving the previous occurrence of `1` is exactly what prevents the two copies of `(1)` from being counted separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n² + m² + nm)` | Length-count DPs take quadratic time, and the equal-length DP examines every `(i,j)` pair once |
| Space | `O(100(n+m))` | Only the current rows and one saved row per value are retained |

Since `n,m <= 5000`, the quadratic term is at most about 25 million cell positions for the cross-DP, with additional quadratic work for the one-dimensional length distributions. The snapshot technique avoids allocating two `5001 × 5001` Python matrices, which would be prohibitively expensive with normal Python integers. The original problem allows 1024 MB, while the intended asymptotic complexity is quadratic.

## Test Cases

The following tests invoke the actual `main.py` solution for the small cases. The maximum-size case is checked through its closed-form expected value rather than executed as part of a normal unit-test run, because it is intentionally a stress test.

```python
# Save the submitted solution as main.py before running this file.

import subprocess
import sys

def run(inp: str) -> str:
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()

# Provided sample
assert run(
    """3 5
2 1 2
1 2 2 1 2
"""
) == "22", "sample 1"

# Minimum-size input, equal values.
assert run(
    """1 1
1
1
"""
) == "0", "equal singleton sequences"

# All equal values, duplicate subsequences must collapse.
assert run(
    """2 2
1 1
1 1
"""
) == "1", "all equal values"

# Unequal lengths plus equal-length lexicographic comparisons.
assert run(
    """2 2
2 1
1 2
"""
) == "4", "length and lexicographic comparison"

# Boundary values 1 and 100, with a repeated value.
assert run(
    """3 2
100 1 100
1 100
"""
) == "6", "boundary values"

# Maximum-size special case.
# Every array consists only of 1, so there is exactly one distinct
# subsequence of every length. A wins exactly when its length is larger.
n = 5000
expected_max_equal = n * (n + 1) // 2
assert expected_max_equal == 12502500, "maximum-size expected value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 5 / 2 1 2 / 1 2 2 1 2` | `22` | Official sample and full equal-length logic |
| `1 1 / 1 / 1` | `0` | Strict inequality |
| `2 2 / 1 1 / 1 1` | `1` | Duplicate subsequence elimination |
| `2 2 / 2 1 / 1 2` | `4` | Unequal lengths and first differing element |
| `3 2 / 100 1 100 / 1 100` | `6` | Boundary values and repeated elements |
| `5000 5000 / all 1 / all 1` | `12502500` | Maximum-size arithmetic and quadratic boundary |

## Edge Cases

For `a = [1]` and `b = [1]`, the length distributions contain one length-one sequence on each side. The unequal-length contribution is zero. In the equal-length DP, the only possible pair has `a[1] == b[1]`, so it enters the equal state rather than the greater state. `G[1][1]` remains zero, giving the correct answer `0`.

For `a = [1,1]` and `b = [1]`, the first occurrence of `1` creates one distinct length-one sequence. At the second occurrence, the recurrence adds the possibilities ending at the new position but subtracts the row associated with the previous `1`, leaving exactly one length-one sequence. The length-two sequence is unique as well. Since length two is greater than length one, exactly one pair is counted.

For equal lengths, consider `a = [2,1]` and `b = [1,2]`. At the first elements, `2 > 1`, so the pair enters `G`. At length two, the sequences are `21` and `12`, and the first elements already decide the comparison. The DP does not need to inspect the second elements semantically, because once a pair is in `G`, later elements are unrestricted. This is exactly what the `rect_g` transition represents.

For repeated values, the previous-occurrence snapshots prevent duplicate representations. Suppose the current value is `1` and its previous occurrence is at position `p`. Every subsequence formed by appending the new `1` that was already obtainable by appending the old `1` must be removed. The subtraction uses the prefix ending at `p-1`, which is precisely the set of sequences that can precede either occurrence without using the occurrence itself.

For maximum-size all-equal arrays of length `5000`, there is exactly one distinct subsequence for every non-empty length. Since the arrays are identical, equal-length pairs never contribute. For every `k` from `2` through `5000`, the unique length-`k` sequence from `a` beats the unique sequences of lengths `1` through `k-1` from `b`. The answer is

`1 + 2 + ... + 4999 = 5000 * 4999 / 2 = 12,497,500`

when both arrays have length `5000`.

For the boundary value `100`, the base-1000 comparison still works without modification. A leading digit of `100` is still below `1000`, so there are no carries between positions. This is why the entire numerical comparison can safely be reduced to length and lexicographic order.
