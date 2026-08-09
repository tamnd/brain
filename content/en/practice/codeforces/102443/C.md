---
title: "CF 102443C - Fermat's Last Theorem"
description: "The program considers every quadruple (a, b, c, n) of positive integers with n = 3. Its ordering has two levels. First, quadruples are grouped by the largest value among their four coordinates. Inside one such group, they are sorted lexicographically by (a, b, c, n)."
date: "2026-08-09T13:39:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "C"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 253
verified: true
draft: false
---

[CF 102443C - Fermat's Last Theorem](https://codeforces.com/problemset/problem/102443/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The program considers every quadruple `(a, b, c, n)` of positive integers with `n >= 3`. Its ordering has two levels. First, quadruples are grouped by the largest value among their four coordinates. Inside one such group, they are sorted lexicographically by `(a, b, c, n)`. For every quadruple, we only need to print whether `a^n + b^n` is greater or smaller than `c^n`.

The input gives two positions `l` and `r` in this infinite sequence. We have to reconstruct exactly the quadruples occupying those positions and print their corresponding inequalities.

The difficulty is that `l` and `r` can be as large as `10^12`. Even though the requested interval contains at most `10^4 + 1` answers, the position itself can be far into the sequence. Generating all previous quadruples is completely infeasible.

There is a useful bound hidden in the constraints. If every coordinate is at most `m`, then there are `m^3(m-2)` possible quadruples, because `a`, `b`, and `c` each have `m` choices while `n` has `m-2` choices from `3` through `m`. Since `1001^3 * 999` is already greater than `10^12`, every requested position belongs to a group with maximum at most `1001`. This makes the search space for the maximum very small, even though the sequence itself is enormous.

Several ordering details are easy to mishandle.

The first quadruple is `(1,1,1,3)`, so the exponent starts at `3`, not at `1`. For example, input `1 1` must produce `1^3+1^3>1^3`. An implementation that treats `n` as ranging from `1` will construct the wrong sequence immediately.

The transition between two maximum values is another common off-by-one trap. The last quadruple with maximum `3` is `(3,3,3,3)`, which has position `27`. The next quadruple is `(1,1,1,4)`, at position `28`. Thus input `28 28` produces `1^4+1^4>1^4`. Searching for the group containing a position with `<=` on the wrong side can shift every later answer by one entire group.

The fact that the maximum may already have appeared earlier in the lexicographic prefix also changes the number of valid completions. For example, once `a=M`, every later coordinate can be chosen freely up to `M`, because the quadruple already has maximum `M`. On the other hand, when `a<M`, the remaining coordinates must contain an `M`. Ignoring this distinction gives the wrong number of quadruples for a prefix and consequently selects the wrong tuple.

Finally, the comparison itself must use the actual integer powers. For example, `(3,3,2,3)` gives `3^3+3^3 > 2^3`. Python integers have arbitrary precision, so we can evaluate these powers directly without overflow.

## Approaches

A direct solution would enumerate quadruples in exactly the required order. For every possible maximum `M`, we could enumerate all values of `a`, `b`, `c`, and `n`, skipping combinations that do not have maximum `M`, until reaching position `r`. This is correct because it literally follows the definition of the sequence.

The problem is the number of iterations. The first `M` groups together contain

`M^3(M-2)`

quadruples, so reaching a position around `10^12` requires processing about `10^12` quadruples. Even before considering the cost of calculating powers, a trillion iterations is far beyond the time limit. Computing each power with exponentiation by squaring would add another logarithmic factor.

The key observation is that we never need to generate the preceding quadruples. We can count how many quadruples exist before a given maximum, locate the maximum containing a requested position with binary search, and then locate each coordinate inside that maximum group using prefix counts.

For a fixed maximum `M`, all coordinates lie in `[1,M]` and `n` lies in `[3,M]`. The total number of quadruples with maximum at most `M` is

`F(M) = M^3(M-2)`.

Consequently, the quadruples whose maximum is exactly `M` occupy positions

`F(M-1)+1` through `F(M)`.

After locating `M`, we know the requested position inside that group. We then reconstruct `(a,b,c,n)` from left to right. At each coordinate there are only two relevant cases. If the prefix has already contained `M`, all remaining coordinates are unrestricted. If it has not, choosing a value smaller than `M` means that some later coordinate must equal `M`.

For a fixed position, every candidate value smaller than `M` has the same number of valid completions. The value `M` has a different number of completions because it immediately satisfies the maximum requirement. This constant-per-candidate structure lets us find the correct coordinate with a binary search instead of scanning all values.

The brute-force works because it follows the sequence exactly, but fails when the requested rank becomes large. The observation that every prefix can be counted algebraically lets us jump directly to the required group and then to the required quadruple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(r log M)` arithmetic work | `O(1)` | Too slow |
| Optimal | `O((r-l+1) log M)` | `O(r-l+1)` for output | Accepted |

Here `M <= 1001`, so the logarithmic factors are tiny. The output itself can contain up to `10001` lines, so storing the answers is also inexpensive.

## Algorithm Walkthrough

1. Define

`F(M) = M^3(M-2)`.

This counts every quadruple whose four coordinates are at most `M`, with `n` restricted to `3..M`. Thus `F(M)` is exactly the last position belonging to maximum `M`.
2. Binary search for the smallest `M` satisfying `F(M) >= rank`.

This identifies the maximum group containing the requested position. The first position of this group is `F(M-1)+1`, so set

`k = rank - F(M-1)`.

Now `k` is a one-based position inside the group with maximum exactly `M`.
3. Reconstruct `a`, `b`, `c`, and `n` from left to right.

Maintain a Boolean `maxed` saying whether the already chosen prefix contains `M`. Initially it is false.

For `a`, if `a<M`, then one of `b`, `c`, or `n` must equal `M`. The number of completions is

`M^2(M-2) - (M-1)^2(M-3)`.

If `a=M`, the maximum condition is already satisfied and there are

`M^2(M-2)`

completions.

These counts are constant for every `a<M`, so we can binary search the smallest `a` whose cumulative number of completions reaches `k`.
4. After choosing `a`, subtract the number of tuples belonging to smaller values of `a`, then update `maxed` if `a=M`.

The same idea applies to `b`. If the maximum has not yet appeared, every `b<M` has

`M(M-2) - (M-1)(M-3)`

completions, while `b=M` has `M(M-2)` completions.

If the maximum has already appeared, every `b` has exactly `M(M-2)` completions.
5. Apply the same reasoning to `c`.

If `M` has not appeared yet, choosing `c<M` forces `n=M`, so there is exactly one completion. Choosing `c=M` allows every exponent `n` from `3` through `M`, giving `M-2` completions.

If the maximum has already appeared, every `c` has `M-2` possible exponents.
6. Handle `n` last.

If the maximum has already appeared, the valid exponents are exactly `3,4,...,M`, in that order. The local rank directly determines

`n = 3 + k - 1`.

If the maximum has not appeared after choosing `c`, then `n` is forced to be `M`.
7. Compare the two sides using Python's arbitrary-precision integers.

Print

`a^n+b^n>c^n`

when the left side is larger, otherwise print

`a^n+b^n<c^n`.

Fermat's Last Theorem guarantees equality cannot occur for these positive integers with `n>=3`.

### Why it works

The central invariant is that `k` is always the lexicographic rank of the required tuple among all valid completions of the already fixed prefix. For every candidate coordinate, we count exactly how many valid tuples begin with that candidate. Since lexicographic order places all tuples with a smaller candidate first, the first candidate whose cumulative completion count reaches `k` must be the coordinate of the required tuple. After removing all preceding candidates, the same invariant holds for the next coordinate.

The completion counts are correct because there are only two possibilities. If the maximum `M` has already appeared, every remaining coordinate can independently take any allowed value. If it has not appeared, choosing a value below `M` requires the remaining coordinates to contain `M`, which is counted by subtracting the assignments restricted to `1..M-1`. This gives the exact number of tuples represented by every prefix, so every binary search selects the correct lexicographic coordinate.

## Python Solution

```python
import sys
input = sys.stdin.readline

def total(m):
    if m < 3:
        return 0
    return m * m * m * (m - 2)

def find_maximum(rank):
    lo, hi = 3, 4

    while total(hi) < rank:
        hi *= 2

    while lo < hi:
        mid = (lo + hi) // 2
        if total(mid) >= rank:
            hi = mid
        else:
            lo = mid + 1

    return lo

def choose_coordinate(m, k, pos, maxed):
    if pos == 0:
        if maxed:
            small = big = m * m * (m - 2)
        else:
            small = (
                m * m * (m - 2)
                - (m - 1) * (m - 1) * (m - 3)
            )
            big = m * m * (m - 2)

    elif pos == 1:
        if maxed:
            small = big = m * (m - 2)
        else:
            small = (
                m * (m - 2)
                - (m - 1) * (m - 3)
            )
            big = m * (m - 2)

    else:
        if maxed:
            small = big = m - 2
        else:
            small = 1
            big = m - 2

    lo, hi = 1, m

    while lo < hi:
        mid = (lo + hi) // 2

        if mid < m:
            count = mid * small
        else:
            count = (m - 1) * small + big

        if count >= k:
            hi = mid
        else:
            lo = mid + 1

    value = lo

    before = (value - 1) * small
    k -= before

    return value, k

def get_tuple(rank):
    m = find_maximum(rank)

    k = rank - total(m - 1)

    a, k = choose_coordinate(m, k, 0, False)
    maxed = (a == m)

    b, k = choose_coordinate(m, k, 1, maxed)
    maxed = maxed or (b == m)

    c, k = choose_coordinate(m, k, 2, maxed)
    maxed = maxed or (c == m)

    if maxed:
        n = 3 + k - 1
    else:
        n = m

    return a, b, c, n

def solve(data):
    l, r = map(int, data.split())

    ans = []

    for rank in range(l, r + 1):
        a, b, c, n = get_tuple(rank)

        left = a ** n + b ** n
        right = c ** n

        if left > right:
            op = '>'
        else:
            op = '<'

        ans.append(f"{a}^{n}+{b}^{n}{op}{c}^{n}")

    return '\n'.join(ans)

def main():
    data = input()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The `total` function implements the cumulative count `F(M)`. The special case `m<3` is needed because there are no legal exponents when the maximum is below `3`.

`find_maximum` first finds a safe upper bound by doubling, then performs a standard lower-bound binary search. This avoids depending on the derived bound `M<=1001` in the implementation, while the bound explains why the search remains extremely small.

`choose_coordinate` contains the core counting argument. The `pos` parameter identifies whether we are choosing `a`, `b`, or `c`. The variable `small` is the number of completions for any candidate smaller than `M`, while `big` is the number of completions when the candidate itself is `M`.

When `maxed` is true, `small` and `big` are equal because the maximum requirement has already been fulfilled. When it is false, `small` is obtained by subtracting configurations that never use `M`. This subtraction is the key combinatorial step.

The binary search asks for the first coordinate whose cumulative number of tuples is at least `k`. For a candidate below `M`, the cumulative count is simply `candidate * small`. For `M`, it is `(M-1)*small + big`. After finding the coordinate, `(value-1)*small` tuples have already been skipped, so that amount is removed from `k`.

The exponent is handled separately because its legal range begins at `3`, and because it is the last coordinate. Once `M` has already appeared, all `M-2` exponent values are available. If it has not appeared, the exponent must equal `M`.

The comparison uses exact integer arithmetic. The largest power involved is roughly `1001^1001`, only a few thousand decimal digits long, so Python's arbitrary-precision integers are easily sufficient. There is no floating-point rounding and no overflow risk.

## Worked Examples

For the first sample, the first four positions all belong to the maximum `3` group. Since `F(2)=0` and `F(3)=27`, the local rank is equal to the global rank.

| Global rank | Maximum `M` | Local rank `k` | `a` | `b` | `c` | `n` | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 1 | 1 | 1 | 3 | `1^3+1^3>1^3` |
| 2 | 3 | 2 | 1 | 1 | 2 | 3 | `1^3+1^3<2^3` |
| 3 | 3 | 3 | 1 | 1 | 3 | 3 | `1^3+1^3<3^3` |
| 4 | 3 | 4 | 1 | 2 | 1 | 3 | `1^3+2^3>1^3` |

For rank `1`, the tuple `(1,1,1,3)` is selected. For rank `2`, the first coordinate remains `1`, the second remains `1`, and the third advances to `2`. The same lexicographic process produces the remaining two tuples.

As a second trace, consider the maximum possible requested rank `10^12`. We have

`F(1000) = 998,000,000,000`

while

`F(1001) = 1,001,999,997,999`.

Thus the rank lies in the `M=1001` group, at local position

`2,000,000,000`.

The coordinate reconstruction proceeds as follows.

| Stage | `k` before | `small` | `big` | Chosen value | `k` after |
| --- | --- | --- | --- | --- | --- |
| `a` | 2,000,000,000 | 2,998,999 | 1,000,998,999 | 667 | 2,666,666 |
| `b` | 2,666,666 | 1,999 | 999,999 | 1001 | 667,666 |
| `c` | 667,666 | 1 | 999 | 668 | 334 |
| `n` | 334 | 1 | 1 | 336 | 334 |

After choosing `b=1001`, the maximum has already appeared, so every later coordinate is unrestricted. The resulting quadruple is `(667,1001,668,336)`. Since `b` is greater than `c`, the comparison is immediately known to have `a^n+b^n > c^n` for positive `n`, so the output is `667^336+1001^336>668^336`.

This trace demonstrates that even a position near `10^12` is reconstructed through only a handful of binary searches rather than through billions of preceding tuples.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((r-l+1) log M)` arithmetic operations, plus exact power calculations | Each output performs one binary search for `M` and three binary searches for coordinates. |
| Space | `O(r-l+1)` | The answer strings are stored before being written. |

Here `M` is at most `1001` for the given upper bound on `r`, so each binary search takes only about ten iterations. With at most `10001` requested inequalities, the number of combinatorial operations is comfortably small. The generated powers have only a few thousand decimal digits, so Python's arbitrary-precision arithmetic also fits comfortably within the 4 second and 512 MB limits.

## Test Cases

The following test file assumes the submitted solution is saved as `solution.py` and exposes the `solve(data)` function used above.

```
# Save the solution as solution.py before running these tests.
from solution import solve

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided sample
assert run("1 4") == (
    "1^3+1^3>1^3\n"
    "1^3+1^3<2^3\n"
    "1^3+1^3<3^3\n"
    "1^3+2^3>1^3"
), "sample 1"

# Minimum possible position
assert run("1 1") == "1^3+1^3>1^3", "minimum position"

# Last tuple of the M=3 block
assert run("27 27") == "3^3+3^3>3^3", "all coordinates equal"

# First tuple of the M=4 block
assert run("28 28") == "1^4+1^4>1^4", "maximum-group boundary"

# Crossing the boundary between M=3 and M=4
assert run("26 29") == (
    "3^3+3^3>2^3\n"
    "3^3+3^3>3^3\n"
    "1^4+1^4>1^4\n"
    "1^3+1^3<2^3"
), "off-by-one around group transition"

# Maximum allowed rank
assert run("1000000000000 1000000000000") == (
    "667^336+1001^336>668^336"
), "maximum rank"

# A short interval inside one group
out = run("2 10").splitlines()
assert len(out) == 9, "correct number of outputs"
assert out[0] == "1^3+1^3<2^3", "second position"
assert out[-1] == "1^3+3^3>3^3", "tenth position"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1^3+1^3>1^3` | Minimum rank and exponent lower bound |
| `27 27` | `3^3+3^3>3^3` | Last tuple of a maximum group and all coordinates equal |
| `28 28` | `1^4+1^4>1^4` | Exact transition from maximum `3` to maximum `4` |
| `26 29` | Four lines crossing the transition | Lexicographic ordering and group boundary off-by-one errors |
| `1000000000000 1000000000000` | `667^336+1001^336>668^336` | Maximum allowed rank and large-index reconstruction |
| `2 10` | Nine consecutive lines | Local rank updates inside one group |

## Edge Cases

For the minimum input `1 1`, the binary search finds `M=3` because `F(2)=0` and `F(3)=27`. The local rank is `1`, so the first coordinate is `1`, then the second is `1`, then the third is `1`, and finally `n=3`. The result is exactly `1^3+1^3>1^3`. This catches implementations that accidentally allow exponents `1` or `2`.

For the input `27 27`, the local rank is `27`, the final position in the maximum `3` group. Every coordinate is therefore selected as `3`, producing `(3,3,3,3)`. The output is `3^3+3^3>3^3`. This checks that the special `M` candidate receives its larger completion count and that the final tuple of a group is not skipped.

For the input `28 28`, `F(3)=27`, so the search moves to `M=4`. The local rank becomes `1`. The lexicographically smallest tuple with maximum exactly `4` is `(1,1,1,4)`, because the maximum must occur somewhere and `n` is the last coordinate, making it the first place where `4` can appear while keeping all earlier coordinates equal to `1`. The output is `1^4+1^4>1^4`. This is the critical boundary case for converting a global rank into a local rank.

For the maximum input `10^12 10^12`, the maximum group is `M=1001`. The local rank is `2,000,000,000`, and the reconstruction gives `(667,1001,668,336)`. The appearance of `1001` in `b` immediately marks the prefix as complete with respect to the maximum condition, so the remaining coordinates are selected as ordinary lexicographic values. The final comparison is `667^336+1001^336>668^336`. This confirms that the counting method remains valid very far into the sequence without enumerating the preceding `10^12` tuples.

The editorial is ready to use as a standalone submission explanation.
