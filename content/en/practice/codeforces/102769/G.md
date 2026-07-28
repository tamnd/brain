---
title: "CF 102769G - Good Number"
description: "A direct solution would iterate over every integer x from 1 to n. For each number, we would compute a = floor(x^(1/k)) and test whether x % a == 0. This is correct because it follows the definition exactly."
date: "2026-07-28T23:20:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102769
codeforces_index: "G"
codeforces_contest_name: "2020 China Collegiate Programming Contest Qinhuangdao Site"
rating: 0
weight: 102769
solve_time_s: 69
verified: true
draft: false
---

[CF 102769G - Good Number](https://codeforces.com/problemset/problem/102769/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Approaches

A direct solution would iterate over every integer `x` from 1 to `n`. For each number, we would compute `a = floor(x^(1/k))` and test whether `x % a == 0`. This is correct because it follows the definition exactly. However, when `n` reaches `10^9`, this requires about one billion checks for a single test case, which is far beyond the available time.

The useful observation is that many consecutive values of `x` have the same value of `floor(x^(1/k))`. If `m = floor(x^(1/k))`, then all such numbers lie in the interval:

`m^k <= x < (m + 1)^k`.

Instead of looking at every number, we can look at every possible root value `m`. Inside one interval, we only need to count multiples of `m`. The number of possible `m` values is `floor(n^(1/k))`, which is at most about 31623 because the slowest case is `k = 2`.

For a fixed `m`, the interval is:

`[m^k, min(n, (m+1)^k - 1)]`.

The count of multiples of `m` in this interval is:

`floor(high / m) - floor((m^k - 1) / m)`.

For `m >= 1`, this can be computed directly. The lower bound expression simplifies to `m^(k-1) - 1`, so the contribution becomes:

`floor(high / m) - m^(k-1) + 1`.

The brute-force works because every number is examined individually, but fails because `n` is too large. The interval observation compresses all numbers sharing the same root into one calculation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(n^(1/k) * log k) | O(1) | Accepted |

## Algorithm Walkthrough

1. If `k = 1`, return `n` immediately. Every positive integer has itself as the floor first root, so every number is good.
2. Find `r = floor(n^(1/k))` using binary search. We cannot use floating point arithmetic because values near powers can be rounded incorrectly.
3. Iterate over every possible root value `m` from 1 to `r`. Each `m` represents one complete block of numbers whose floor `k`-th root equals `m`.
4. Compute the right endpoint of the block as `min(n, (m+1)^k - 1)`. The left endpoint is `m^k`, and every multiple of `m` in this range contributes one good number.
5. Add the number of multiples of `m` inside this interval using integer division. Repeating this for all possible roots counts every good number exactly once.

The reason this partition is correct is that every positive integer has exactly one value of `floor(x^(1/k))`. The intervals do not overlap, so a number cannot be counted twice, and every valid number appears in the interval belonging to its root.

Why it works: the algorithm maintains the invariant that after processing all root values up to `m`, the answer contains exactly all good numbers whose floor `k`-th root is at most `m`. The next interval contains only numbers with root `m+1`, and the multiple counting formula exactly matches the definition of a good number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def power_limit(a, b, limit):
    result = 1
    while b:
        if b & 1:
            result *= a
            if result > limit:
                return limit + 1
        b >>= 1
        if b:
            a *= a
            if a > limit:
                a = limit + 1
    return result

def kth_root(n, k):
    if k == 1:
        return n
    lo, hi = 1, n
    ans = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if power_limit(mid, k, n) <= n:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans

def solve_case(n, k):
    if k == 1:
        return n

    r = kth_root(n, k)
    ans = 0

    for m in range(1, r + 1):
        high = min(n, power_limit(m + 1, k, n) - 1)
        lower_power = power_limit(m, k, n)
        ans += high // m - (lower_power - 1) // m

    return ans

def main():
    t = int(input())
    out = []
    for case in range(1, t + 1):
        n, k = map(int, input().split())
        out.append(f"Case #{case}: {solve_case(n, k)}")
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The `power_limit` function is used instead of Python's normal exponentiation because the algorithm only needs to know whether a power exceeds `n`. Stopping early avoids creating unnecessarily large integers during binary search.

The `kth_root` function performs a binary search over the possible root values. The monotonic property comes from the fact that `x^k` increases as `x` increases, so once a value is too large, every larger value is also too large.

Inside `solve_case`, each iteration handles one root interval. The expression `high // m - (lower_power - 1) // m` counts multiples of `m` without iterating through the interval. The subtraction uses `lower_power - 1` because the interval starts at `m^k`, and we need the count of multiples strictly before that point.

Python integers do not overflow, but the early cutoff in `power_limit` is still necessary for performance because values such as `2^1000000000` should never be constructed.

## Worked Examples

For `n = 233, k = 2`, the first few intervals look like this:

| Root m | Interval start | Interval end | Multiples counted | Running answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 3 | 3 |
| 2 | 4 | 8 | 3 | 6 |
| 3 | 9 | 15 | 3 | 9 |
| 4 | 16 | 24 | 3 | 12 |
| 5 | 25 | 35 | 2 | 14 |

The algorithm continues through all roots up to 15. The final answer is 43, matching the sample output. This trace shows that we count only multiples inside each root block, not every number in the block.

For `n = 16, k = 2`:

| Root m | Interval start | Interval end | Multiples counted | Running answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 3 | 3 |
| 2 | 4 | 8 | 3 | 6 |
| 3 | 9 | 15 | 3 | 9 |
| 4 | 16 | 16 | 1 | 10 |

The last interval is truncated because the input limit stops at 16. This confirms that the upper bound must always be clipped by `n`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^(1/k) * log k) | We process one iteration per possible root and each power calculation is logarithmic in the exponent. |
| Space | O(1) | Only a constant number of integer variables are stored. |

The maximum number of root values appears when `k = 2`, where it is about 31623 for `n = 10^9`. This keeps the number of operations small enough for the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve(inp):
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    t = int(next(it))
    ans = []
    for case in range(1, t + 1):
        n = int(next(it))
        k = int(next(it))
        ans.append(f"Case #{case}: {solve_case(n, k)}")
    return "\n".join(ans)

# provided samples
assert solve("""2
233 1
233 2
""") == """Case #1: 233
Case #2: 43""", "sample"

# minimum-size cases
assert solve("""2
1 1
1 100
""") == """Case #1: 1
Case #2: 1""", "minimum values"

# all values are handled by k=1
assert solve("""1
1000000000 1
""") == """Case #1: 1000000000", "k equals one"

# square-root boundary cases
assert solve("""1
16 2
""") == """Case #1: 10""", "perfect power boundary"

# all equal root interval behavior
assert solve("""1
8 2
""") == """Case #1: 6""", "single completed interval"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest possible input |
| `1 100` | `1` | Very large exponent where only root 1 exists |
| `1000000000 1` | `1000000000` | Special handling of `k = 1` |
| `16 2` | `10` | Exact power boundary handling |
| `8 2` | `6` | Counting multiples inside one root interval |

## Edge Cases

When `k = 1`, the root interval idea collapses because every number has its own root. The algorithm avoids the loop and returns `n`, which matches the definition directly. For input `233 1`, it outputs `233`.

When the root is 1, all numbers before the next power belong to the first interval. For input `5 2`, the interval is `[1, 3]`, and all three values are counted. The algorithm starts iteration from `m = 1`, so these values are included.

When `n` ends in the middle of an interval, the interval must be shortened. For input `16 2`, the root 4 interval would normally be `[16, 24]`, but only `16` is inside the allowed range. The algorithm uses `min(n, (m+1)^k - 1)`, so it counts only the valid part.

When `k` is very large, the root value is usually 1. For input `1,000,000,000 1000000000`, the algorithm's binary search quickly finds that no root greater than 1 can have its power within the limit, and only the first interval is processed.
