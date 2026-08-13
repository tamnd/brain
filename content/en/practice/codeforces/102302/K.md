---
title: "CF 102302K - Candies"
description: "We have an integer array C of length N. A candy sequence is any non-empty contiguous part of this array, and its value is the sum of its elements. The required answer is not the number of positions where a valid sequence occurs."
date: "2026-08-13T23:32:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "K"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 191
verified: true
draft: false
---

[CF 102302K - Candies](https://codeforces.com/problemset/problem/102302/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an integer array `C` of length `N`. A candy sequence is any non-empty contiguous part of this array, and its value is the sum of its elements. The required answer is not the number of positions where a valid sequence occurs. Equal value sequences are merged, so `[4]` occurring five times still counts as one distinct sequence, while `[4]` and `[4, 4]` are different because their lengths differ.

The first line gives `N`, followed by the lower and upper allowed sums `L` and `R`. The second line contains the candy values. We need the number of different contiguous arrays whose sum lies in the inclusive interval `[L, R]`.

With `N` as large as `5 * 10^5`, enumerating all `N(N+1)/2` intervals already gives about `1.25 * 10^11` candidates in the worst case. A quadratic algorithm is far beyond what a 4 second limit can support. The candy values can also be negative, so techniques based on a monotonic sliding window do not apply. The bounds on `L` and `R` reach `10^18`, while individual values reach `10^9`, so prefix sums and comparisons must be handled with 64-bit arithmetic in languages with fixed-width integers.

There are three cases that commonly cause incorrect solutions.

Consider

```
2 2 2
2 2
```

There are two occurrences of `[2]`, but they represent the same distinct sequence. The correct answer is `1`. A solution that counts valid intervals instead of distinct sequences returns `2`.

Negative values break the usual two-pointer argument. For example,

```
3 -1 1
1 -1 1
```

The valid distinct sequences are `[1]`, `[-1]`, `[1,-1]`, `[-1,1]`, and `[1,-1,1]`, giving `5`. A sliding window that assumes extending the right endpoint always increases the sum cannot reason correctly about this array.

The boundaries are inclusive. For

```
2 2 2
2 3
```

only `[2]` has sum exactly `2`, so the answer is `1`. A solution that accidentally uses a strict inequality for either boundary loses this sequence.

## Approaches

The direct approach considers every pair of endpoints and maintains the current sum with prefix sums. For each interval, we can check whether its sum is in `[L,R]` and insert the corresponding sequence into a set. This is correct because every contiguous sequence has exactly one pair of endpoints, and the set removes repeated sequences. The problem is the number of intervals: with `N = 500000`, there are `N(N+1)/2 = 125000250000` of them. Even representing each interval by a hash would leave us with roughly `1.25 * 10^11` candidates, which is already impossible, before accounting for the cost of maintaining or comparing the actual sequences.

The key observation is that a contiguous sequence is a prefix of some suffix of the original array. Suppose we fix a suffix starting at position `i`. Its prefixes have lengths `1, 2, ..., N-i`. If we process suffixes in lexicographic order, the prefixes that were already represented by an earlier suffix are exactly the prefixes up to the longest common prefix with the previous suffix.

Let `lcp[i]` be the LCP length associated with the suffix starting at `i`, where the previous suffix means the suffix immediately before it in suffix-array order. Then suffix `i` contributes exactly the prefix lengths

[
lcp[i]+1,\ lcp[i]+2,\ \ldots,\ N-i.
]

This is the usual suffix-array way of counting distinct substrings, but here we cannot simply count all these lengths. We must keep only those whose sums lie in `[L,R]`.

Prefix sums turn that condition into a range query. Define

[
P[0]=0,\qquad P[j]=C_0+C_1+\cdots+C_{j-1}.
]

A prefix of length `k` of the suffix beginning at `i` ends at prefix-sum position `j=i+k`, and its sum is

[
P[j]-P[i].
]

Thus the prefix is valid exactly when

[
P[i]+L \le P[j] \le P[i]+R.
]

For each suffix, we therefore need to count endpoint positions `j` inside the index range

[
i+lcp[i]+1 \le j \le N
]

whose prefix sum belongs to the value interval `[P[i]+L, P[i]+R]`.

The queries become two-dimensional: one coordinate is the endpoint position `j`, and the other is its prefix sum `P[j]`. We can process them offline. Sort suffix starting positions by `P[i]`. Then both query boundaries `P[i]+L` and `P[i]+R` move monotonically. Maintain in a Fenwick tree exactly those endpoint positions whose prefix sums currently lie inside the required value interval. A Fenwick prefix query then removes endpoints that occur before the allowed starting endpoint.

The suffix array itself is constructed with the standard doubling algorithm and counting sort, giving `O(N log N)` construction time. Kasai's algorithm then computes all LCP values in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) or worse | O(N²) in a direct set representation | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build the suffix array of `C`. The suffix array stores all starting positions sorted according to the lexicographic order of the suffixes beginning there. A unique sentinel smaller than every candy value is appended internally so the standard cyclic-shift doubling algorithm can be used.
2. Compute the LCP value for every suffix using Kasai's algorithm. For a suffix at position `i`, `lcp[i]` is the length of its common prefix with the suffix immediately before it in suffix-array order. If there is no previous suffix, its value is zero.
3. Build the prefix-sum array `P`. For an endpoint `j`, the sum of the subarray beginning at `i` and ending at `j-1` is `P[j] - P[i]`.
4. For a suffix beginning at `i`, set

[
left_i=i+lcp[i]+1.
]

Only endpoints `j >= left_i` represent substrings that are new when this suffix is processed. Endpoints before `left_i` correspond to prefixes already represented by an earlier suffix.

1. Sort all suffix starting positions `i` by `P[i]`, and independently sort all endpoint positions `j` from `1` through `N` by `P[j]`. This gives a common order in which prefix-sum thresholds can be processed.
2. Sweep the suffixes in increasing `P[i]`. Maintain a Fenwick tree containing endpoint positions `j` satisfying

[
P[i]+L \le P[j] \le P[i]+R.
]

Because the suffixes are processed in increasing `P[i]`, both bounds only move to the right in the sorted endpoint list. Add endpoints when they enter the upper bound and remove them when they fall below the lower bound.

1. For the current suffix, let `active` be the number of endpoints currently in the Fenwick tree. A Fenwick prefix query at `left_i-1` counts active endpoints that occur too early, so

[
active-\operatorname{prefixSum}(left_i-1)
]

is exactly the number of new, distinct prefixes of this suffix whose sums belong to `[L,R]`.

1. Add this contribution to the answer for every suffix. The sum is the required number of distinct valid consecutive sequences.

**Why it works.** Every contiguous sequence is a prefix of exactly one suffix occurrence, but the same sequence may be a prefix of several suffixes. In suffix-array order, all suffixes sharing a prefix form a contiguous group. Consequently, for a suffix, every prefix of length at most its LCP with the previous suffix has already been represented, while every longer prefix is new. The value `left_i` captures exactly this distinction. The Fenwick sweep counts precisely those new prefix endpoints whose sums satisfy both inclusive bounds. Since every distinct valid sequence is new at exactly one suffix, and every counted prefix is valid, the accumulated answer contains each required sequence exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_suffix_array(a):
    """Suffix array of an integer array using doubling + counting sort."""
    values = sorted(set(a))
    compress = {x: i + 1 for i, x in enumerate(values)}

    # 0 is a unique sentinel smaller than every real value.
    s = [compress[x] for x in a] + [0]
    m = len(s)

    # Initial counting sort by the first value.
    alphabet = len(values) + 1
    cnt = [0] * alphabet
    for x in s:
        cnt[x] += 1

    pos = [0] * alphabet
    total = 0
    for i in range(alphabet):
        pos[i] = total
        total += cnt[i]

    p = [0] * m
    for i, x in enumerate(s):
        p[pos[x]] = i
        pos[x] += 1

    # Initial equivalence classes.
    c = [0] * m
    classes = 1
    c[p[0]] = 0
    for i in range(1, m):
        if s[p[i]] != s[p[i - 1]]:
            classes += 1
        c[p[i]] = classes - 1

    length = 1

    while length < m:
        # Shift every suffix start left by 'length'.
        pn = [0] * m
        for i, x in enumerate(p):
            y = x - length
            if y < 0:
                y += m
            pn[i] = y

        # Counting sort by the first half's class.
        cnt = [0] * classes
        for x in pn:
            cnt[c[x]] += 1

        pos = [0] * classes
        total = 0
        for i in range(classes):
            pos[i] = total
            total += cnt[i]

        p_new = [0] * m
        for x in pn:
            cl = c[x]
            p_new[pos[cl]] = x
            pos[cl] += 1

        # Recompute classes for pairs of length 2 * length.
        c_new = [0] * m
        new_classes = 1
        c_new[p_new[0]] = 0

        for i in range(1, m):
            cur = p_new[i]
            prev = p_new[i - 1]

            cur_second = cur + length
            if cur_second >= m:
                cur_second -= m

            prev_second = prev + length
            if prev_second >= m:
                prev_second -= m

            if (
                c[cur] != c[prev]
                or c[cur_second] != c[prev_second]
            ):
                new_classes += 1

            c_new[cur] = new_classes - 1

        p = p_new
        c = c_new
        classes = new_classes
        length <<= 1

    # The sentinel suffix is always first.
    return p[1:]

def build_lcp(a, sa):
    """lcp[i] = LCP of suffix i with its previous suffix in SA order."""
    n = len(a)
    rank = [0] * n

    for r, pos in enumerate(sa):
        rank[pos] = r

    lcp = [0] * n
    h = 0

    for i in range(n):
        r = rank[i]

        if r == 0:
            h = 0
            continue

        j = sa[r - 1]

        while i + h < n and j + h < n and a[i + h] == a[j + h]:
            h += 1

        lcp[i] = h

        if h:
            h -= 1

    return lcp

def solve():
    n, L, R = map(int, input().split())
    a = list(map(int, input().split()))

    if n == 0:
        print(0)
        return

    sa = build_suffix_array(a)
    lcp = build_lcp(a, sa)

    # P[j] is the sum of a[0:j].
    pref = [0] * (n + 1)
    s = 0
    for i, x in enumerate(a):
        s += x
        pref[i + 1] = s

    # Query suffixes by P[i].
    query_order = sorted(range(n), key=pref.__getitem__)

    # Endpoint j is represented by prefix sum P[j], j in [1, n].
    endpoint_order = sorted(range(1, n + 1), key=pref.__getitem__)

    # Fenwick tree over endpoint positions.
    bit = [0] * (n + 1)

    def add(idx, delta):
        while idx <= n:
            bit[idx] += delta
            idx += idx & -idx

    def prefix_sum(idx):
        result = 0
        while idx > 0:
            result += bit[idx]
            idx -= idx & -idx
        return result

    hi = 0
    lo = 0
    active = 0
    answer = 0

    for i in query_order:
        low_value = pref[i] + L
        high_value = pref[i] + R

        # Add all endpoints that have entered the upper bound.
        while hi < n and pref[endpoint_order[hi]] <= high_value:
            j = endpoint_order[hi]
            add(j, 1)
            hi += 1
            active += 1

        # Remove endpoints that are below the lower bound.
        while lo < hi and pref[endpoint_order[lo]] < low_value:
            j = endpoint_order[lo]
            add(j, -1)
            lo += 1
            active -= 1

        # Only lengths greater than lcp[i] are new.
        left = i + lcp[i] + 1

        if left <= n:
            too_early = prefix_sum(left - 1)
            answer += active - too_early

    print(answer)

if __name__ == "__main__":
    solve()
```

The suffix-array construction first compresses the candy values so that the sentinel can safely be represented by zero and all real values by positive integers. The doubling loop sorts cyclic shifts by pairs of equivalence classes. Because the sentinel is unique and smallest, removing its suffix at the end leaves the ordinary suffix array of the original array.

The LCP construction uses the inverse suffix array to find the previous suffix of each starting position. Kasai's reuse of the previous match length makes the total number of character comparisons linear, even though individual LCP values can be large.

The prefix sum `pref[j]` represents the array endpoint immediately after the subarray. This is why the endpoint indices used by the Fenwick tree are `1` through `N`, while suffix starting positions are `0` through `N-1`. Mixing these two coordinate systems is a common source of off-by-one errors.

The Fenwick sweep maintains a value interval rather than merely an upper bound. For a suffix starting at `i`, an endpoint `j` is valid exactly when `pref[j]` is between `pref[i] + L` and `pref[i] + R`. Since the suffixes are ordered by `pref[i]`, both boundaries are monotone, so every endpoint enters and leaves the Fenwick tree at most once.

The `left` expression contains the other critical boundary. A prefix whose length equals `lcp[i]` is already present in the previous suffix, so the first new length is `lcp[i] + 1`. Since the endpoint is `i + length`, the first new endpoint is `i + lcp[i] + 1`.

Python integers have arbitrary precision, so sums up to roughly `5 * 10^14` and the final answer around `1.25 * 10^11` require no special overflow handling. In a fixed-width language, a signed 64-bit integer is sufficient.

## Worked Examples

For Sample 1,

```
5 5 10
1 2 3 4 5
```

the prefix sums are `[0, 1, 3, 6, 10, 15]`. Every suffix is different from every other suffix, so all LCP values are zero. The table shows the direct `[L,R]` sweep.

| i | lcp[i] | P[i] | Valid P[j] range | left | active | too early | contribution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | [5, 10] | 1 | 2 | 0 | 2 |
| 1 | 0 | 1 | [6, 11] | 2 | 2 | 0 | 2 |
| 2 | 0 | 3 | [8, 13] | 3 | 1 | 0 | 1 |
| 3 | 0 | 6 | [11, 16] | 4 | 1 | 0 | 1 |
| 4 | 0 | 10 | [15, 20] | 5 | 1 | 0 | 1 |

The five contributions are `2 + 2 + 1 + 1 + 1 = 7`. They correspond to `[3,4]`, `[1,2,3,4]`, `[2,3,4]`, `[4,5]`, and `[5]` in the appropriate suffix-prefix representation. Every one has sum between `5` and `10`.

For Sample 2,

```
5 5 10
1 2 3 4 4
```

the prefix sums are `[0, 1, 3, 6, 10, 14]`. The suffixes beginning at positions `3` and `4` are `[4,4]` and `[4]`. In suffix-array order, `[4]` comes before `[4,4]`, so `lcp[3] = 1`. This is precisely what prevents the occurrence of `[4]` inside the longer suffix from being counted a second time.

| i | lcp[i] | P[i] | Valid P[j] range | left | active | too early | contribution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | [5, 10] | 1 | 2 | 0 | 2 |
| 1 | 0 | 1 | [6, 11] | 2 | 2 | 0 | 2 |
| 2 | 0 | 3 | [8, 13] | 3 | 1 | 0 | 1 |
| 3 | 1 | 6 | [11, 16] | 5 | 1 | 0 | 1 |
| 4 | 0 | 10 | [15, 20] | 5 | 0 | 0 | 0 |

The contributions sum to `2 + 2 + 1 + 1 = 6`. The repeated value `4` illustrates why occurrences cannot simply be counted independently. The single-candy sequence `[4]` has already been represented by the suffix starting at the last position, while `[4,4]` is a genuinely new sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Suffix-array construction takes O(N log N), LCP construction is O(N), sorting prefix sums takes O(N log N), and the Fenwick sweep performs O(N) updates and queries, each in O(log N). |
| Space | O(N) | The suffix array, LCP array, prefix sums, sorting orders, equivalence classes, and Fenwick tree each use linear space. |

For `N = 5 * 10^5`, quadratic enumeration would require about `1.25 * 10^11` intervals, while the optimal solution performs a logarithmic number of passes over linear-sized arrays. The memory limit of 1024 MB is comfortably above the linear collection of arrays used here. The 4 second limit is designed for an `O(N log N)` solution rather than any approach that enumerates all subarrays.

## Test Cases

```python
# This test harness assumes the solution above has been placed in the
# same Python file and that solve() is available.

import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided samples
assert run("5 5 10\n1 2 3 4 5\n") == "7", "sample 1"
assert run("5 5 10\n1 2 3 4 4\n") == "6", "sample 2"

# Minimum-size input
assert run("1 1 1\n1\n") == "1", "single candy"

# Duplicate occurrences must count only once
assert run("2 2 2\n2 2\n") == "1", "duplicate sequence"

# Negative values, with inclusive lower and upper bounds
assert run("3 -1 1\n1 -1 1\n") == "5", "negative values"

# Maximum-size, all-equal input.
# Every distinct sequence is determined only by its length.
n = 500000
max_input = f"{n} 0 0\n" + " ".join(["0"] * n) + "\n"
assert run(max_input) == str(n), "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1` | `1` | Minimum array size and a single valid sequence |
| `2 2 2 / 2 2` | `1` | Duplicate occurrences must not be counted twice |
| `3 -1 1 / 1 -1 1` | `5` | Negative values and inclusive sum boundaries |
| `500000 0 0 / 500000 zeros` | `500000` | Maximum size, all-equal values, and performance |

## Edge Cases

For the duplicate-occurrence case,

```
2 2 2
2 2
```

the suffixes are `[2]` and `[2,2]`. In suffix-array order, `[2]` comes first and `[2,2]` has an LCP of `1` with it. The first suffix contributes `[2]`, while the second suffix is forbidden from contributing its length-one prefix and can only contribute `[2,2]`. Since `[2,2]` has sum `4`, only `[2]` remains valid, giving `1`.

For negative values,

```
3 -1 1
1 -1 1
```

the prefix sums are `0,1,0,1`. The algorithm never assumes that prefix sums increase with the endpoint. Instead, it sorts all prefix sums and performs value-range queries. The suffix-array part handles duplication independently of the numerical sums, while the Fenwick tree handles the arbitrary ordering of prefix sums. The five distinct valid sequences are `[1]`, `[-1]`, `[1,-1]`, `[-1,1]`, and `[1,-1,1]`, so the result is `5`.

For an exact boundary,

```
2 2 2
2 3
```

the prefix sums are `0,2,5`. For the suffix beginning at the first position, the required prefix-sum interval is `[4,4]`, so no endpoint is accepted. For the suffix beginning at the second position, the interval is `[4,4]` as well, and its single endpoint has prefix sum `5`, so it is also outside the range. This example actually has no valid sequence, so the output is `0`. If the array is instead

```
2 2 2
2 3
```

the single element `2` has sum exactly `2` and must be accepted. The correct interpretation of the endpoint condition is `P[i]+L <= P[j] <= P[i]+R`, not either strict inequality.

For the maximum-size all-equal case,

```
500000 0 0
0 0 0 ... 0
```

every non-empty sequence has sum zero. However, the only distinct sequences are the strings consisting of one zero, two zeros, three zeros, and so on up to `500000` zeros. The suffix-array LCP values remove the repeated prefixes, leaving exactly one contribution for each possible length. The answer is consequently `500000`, while the algorithm still processes the entire input in `O(N log N)` time.
