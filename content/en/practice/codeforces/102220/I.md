---
title: "CF 102220I - Temperature Survey"
description: "We are given the already sorted temperature sequence of city A, a1, a2, ..., an. We need to count how many different sequences b1, b2, ..., bn could have produced the observations, where B's temperatures are also non-decreasing and bi <= ai for every day."
date: "2026-08-17T22:39:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102220
codeforces_index: "I"
codeforces_contest_name: "The 13th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102220
solve_time_s: 189
verified: true
draft: false
---

[CF 102220I - Temperature Survey](https://codeforces.com/problemset/problem/102220/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the already sorted temperature sequence of city A, `a1, a2, ..., an`. We need to count how many different sequences `b1, b2, ..., bn` could have produced the observations, where B's temperatures are also non-decreasing and `bi <= ai` for every day. Every temperature is an integer from `1` to `n`, and the answer is required modulo `998244353`. The official limits are `n <= 2 * 10^5`, with total `n` over all test cases at most `5 * 10^5`, an 8 second time limit, and 512 MB of memory.

The monotonicity is the key structural property. A valid `b` is not an arbitrary choice of one value per position. Once `b_i` is chosen, all later values must be at least it, while every position also has a different upper bound. A direct enumeration is already hopeless: even without the upper bounds, the number of non-decreasing sequences of length `n` over `n` values is `C(2n-1,n)`, so checking every candidate would require roughly `n * C(2n-1,n)` operations in the worst case. A straightforward dynamic program with `dp[i][j]` would reduce this to `O(n^2)`, but `n = 2 * 10^5` means about `4 * 10^10` states, far beyond what the time limit permits. The total input size of `5 * 10^5` also rules out algorithms whose quadratic cost is merely spread across test cases.

There are several boundary cases that expose common incorrect interpretations. For `n = 1` and `a = [1]`, the only possible sequence is `b = [1]`, so the answer is `1`. A method that accidentally allows zero or treats the first position differently can produce an incorrect count.

For `a = [1, 2, 3, 4]`, the answer is `14`. A tempting grid interpretation is to count paths only to `(n, a_n)`, which gives `5`, but that loses the freedom of choosing `b_n`. The correct construction adds one extra row and column so that the final downward move represents `b_n`; the resulting count is the Catalan number `C_4 = 14`.

For `a = [4, 4, 4, 4]`, every valid `b` is simply a non-decreasing sequence of four values from `{1,2,3,4}`. Its count is `C(7,4) = 35`. Treating the four positions as independent would give `4^4 = 256`, while multiplying local choices such as `4 * 3 * 2 * 1` also gives the wrong answer because the choice at one position changes the lower bound at every later position.

Repeated values also matter. For `a = [2,2,3]`, the possible pairs `(b1,b2)` are `(1,1)`, `(1,2)`, and `(2,2)`. They allow respectively `3`, `2`, and `2` choices for `b3`, giving `7`. A divide and conquer implementation that splits equal values without treating the whole plateau together can double-count or miss paths along that flat boundary.

## Approaches

The most direct solution enumerates every non-decreasing sequence `b`, checks `bi <= ai`, and counts the valid ones. This is correct because it literally examines the complete set of candidates, but even before checking the upper bounds there are `C(2n-1,n)` non-decreasing sequences. For `n = 2 * 10^5`, that number is exponential in `n`, so this approach is unusable.

The natural improvement is dynamic programming. Let `dp[i][j]` be the number of valid prefixes ending with `b_i = j`. Then

`dp[i][j] = dp[i-1][1] + dp[i-1][2] + ... + dp[i-1][j]`

whenever `j <= ai`. Prefix sums make each transition constant time, but there are still `O(n^2)` states. The brute-force works because the constraints are local, but fails when the number of possible temperature values becomes large.

The observation that unlocks the faster solution is that this DP is exactly a lattice-path problem. Draw row `i` with `ai` cells, left aligned. A path moves only right or down. Whenever the path moves from row `i` to row `i+1`, record the column where that downward move occurs. Those recorded columns form a non-decreasing sequence, and the fact that row `i` contains only `ai` cells gives `bi <= ai`.

To represent all `n` values of `b`, append one extra value `a_{n+1}=n+1`. The extra downward move then represents the original final value `b_n`, and the path ends at the bottom-right corner. We can reverse the rows, turning the non-decreasing boundary into a non-increasing staircase. The resulting problem is counting monotone paths inside a Ferrers-shaped region.

For a rectangular part of this region, ordinary DP has the recurrence

`F(i,j) = F(i-1,j) + F(i,j-1)`.

If we know values on the top and left boundaries of a rectangle, every value on its bottom and right boundaries can be expressed as a binomial convolution. For a rectangle with height `h` and width `w`, the contribution from a top boundary value `x_j` to a bottom position `i` is

`x_j * C(i-j+h-1, h-1)`,

while the contribution from a left boundary value `y_j` to a bottom position `i` is

`y_j * C(i+h-1-j, i)`.

The corresponding formulas for the right boundary are symmetric.

The binomial coefficients contain factorials, so each convolution can be transformed into an ordinary polynomial multiplication. For example,

`C(i-j+h-1, h-1) = (i-j+h-1)! / ((h-1)! (i-j)!)`.

After reversing one factor and multiplying by factorial or inverse-factorial sequences, the entire transition becomes one polynomial convolution. Since the modulus `998244353` supports NTT, each convolution costs `O(k log k)` rather than quadratic time.

The boundary itself is handled by divide and conquer. At each recursion level we select the middle height of the monotone boundary, extract the maximal rectangle having that height, solve its boundary transitions with NTT, and recurse on the two remaining parts. Equal adjacent values are kept in the same rectangle, which is what handles plateaus correctly.

At any fixed recursion depth, the rectangles are disjoint, so the sum of their widths and heights is `O(n)`. There are `O(log n)` levels, and each level performs `O(n log n)` work in total. The resulting complexity is `O(n log^2 n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all `b` | `O(n C(2n-1,n))` | `O(n)` | Too slow |
| Full DP | `O(n^2)` | `O(n^2)` or `O(n)` with rolling rows | Too slow |
| Rectangle divide and conquer + NTT | `O(n log^2 n)` | `O(n log n)` in the sparse boundary representation | Accepted |

## Algorithm Walkthrough

1. Interpret every valid sequence `b` as a lattice path. Create a grid whose `i`-th row has `ai` cells. Moving down from row `i` at column `j` records `bi = j`. Moving right increases the column, so the recorded values are non-decreasing. The row width restriction gives `bi <= ai`.
2. Append one extra row with width `n+1`. This final row lets the last downward step encode `b_n`, so the answer becomes the number of paths from the upper-left corner to the new lower-right corner.
3. Reverse the row sequence. The original `a` is non-decreasing, so after reversal it is non-increasing. This makes the boundary a staircase that can be decomposed into maximal horizontal rectangles.
4. Precompute factorials and inverse factorials modulo `998244353` up to `2n+2`. Every binomial coefficient used by a rectangle transition can then be evaluated in constant time.
5. For a rectangle with height `h` and width `w`, store the values on its top boundary in an array `top` and the values on its left boundary in an array `left`. The number of paths from each boundary position to a destination is a binomial coefficient because a path is determined by the positions of its right and down moves.
6. Compute the bottom boundary from the top boundary with the convolution

`bottom[i] += sum(top[j] * C(i-j+h-1,h-1))`.

The left boundary also contributes to the bottom:

`bottom[i] += sum(left[j] * C(i+h-1-j,i))`.

The first sum is an ordinary convolution with the sequence `C(k+h-1,h-1)`. The second becomes a convolution after multiplying `left[j]` by `1/(h-1-j)!` and multiplying the other factor by factorials.

1. Compute the right boundary symmetrically. The top boundary contributes through

`right[i] += sum(top[j] * C(i+w-1-j,i))`,

and the left boundary contributes through

`right[i] += sum(left[j] * C(i-j+w-1,w-1))`.

These are the same two convolution patterns with width and height exchanged.

1. Use NTT for each sufficiently large convolution. For short arrays, direct multiplication is faster in Python, so the implementation switches to the quadratic method below a small threshold.
2. Divide the staircase by taking the middle row. If several consecutive rows have the same boundary height, treat them as one maximal plateau. Recursively solve the part above the plateau, solve the rectangle occupied by the plateau, then recursively solve the part below it. Keeping the plateau intact prevents the same boundary path from being processed twice.
3. The initial state is the top-left corner. After the entire staircase has been processed, the required answer is the DP value at the final lower-right corner.

### Why it works

The grid construction gives a bijection between legal `b` sequences and monotone paths. Inside every rectangle, the standard lattice-path recurrence is exact, so the binomial formulas compute exactly the same DP values that a full `O(n^2)` table would contain. The divide and conquer only changes the order in which boundary values are computed. Its invariant is that every value needed by a child rectangle is already present on its top or left boundary. Since the staircase is partitioned into disjoint rectangles and the rectangle transition counts every path entering through either boundary exactly once, every legal path reaches the final corner once and no illegal path is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
G = 3
NAIVE_LIMIT = 4096

def ntt(a, invert):
    n = len(a)

    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)

        half = length >> 1
        for start in range(0, n, length):
            w = 1
            end = start + half
            for i in range(start, end):
                u = a[i]
                v = a[i + half] * w % MOD

                x = u + v
                if x >= MOD:
                    x -= MOD
                y = u - v
                if y < 0:
                    y += MOD

                a[i] = x
                a[i + half] = y
                w = w * wlen % MOD

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b):
    if not a or not b:
        return []

    need = len(a) + len(b) - 1

    if len(a) * len(b) <= NAIVE_LIMIT:
        c = [0] * need
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    c[i + j] = (c[i + j] + x * y) % MOD
        return c

    size = 1
    while size < need:
        size <<= 1

    fa = a[:] + [0] * (size - len(a))
    fb = b[:] + [0] * (size - len(b))

    ntt(fa, False)
    ntt(fb, False)

    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)
    return fa[:need]

def count_arrays(original):
    n = len(original)

    # Add the extra row, then reverse the staircase.
    a = [0] + original + [n + 1]
    a[1:] = reversed(a[1:])

    max_fact = 2 * n + 2
    fac = [1] * (max_fact + 1)
    invfac = [1] * (max_fact + 1)

    for i in range(1, max_fact + 1):
        fac[i] = fac[i - 1] * i % MOD

    invfac[max_fact] = pow(fac[max_fact], MOD - 2, MOD)
    for i in range(max_fact, 0, -1):
        invfac[i - 1] = invfac[i] * i % MOD

    def comb(x, y):
        if y < 0 or y > x:
            return 0
        return fac[x] * invfac[y] % MOD * invfac[x - y] % MOD

    # dp[row] stores only boundary values that are needed later.
    dp = [dict() for _ in range(n + 2)]

    def add_dp(row, col, value):
        d = dp[row]
        d[col] = (d.get(col, 0) + value) % MOD

    def rect(l, r, bot, top):
        if l == 1 and r == 1 and top == n + 1:
            for col in range(bot, top + 1):
                dp[1][col] = 1
            return

        width = r - l + 1
        height = top - bot + 1

        # Top boundary.
        upper = [
            dp[l + i].get(top + 1, 0)
            for i in range(width)
        ]

        # Left boundary.
        left = [
            dp[l - 1].get(top - i, 0)
            for i in range(height)
        ]

        bottom = [0] * width
        right = [0] * height

        # Left -> bottom.
        x = [
            left[i] * invfac[height - 1 - i] % MOD
            for i in range(height)
        ]
        y = fac[:width + height - 1]
        z = convolution(x, y)

        for i in range(width):
            bottom[i] = (
                bottom[i]
                + z[height - 1 + i] * invfac[i]
            ) % MOD

        # Top -> bottom.
        kernel = [
            comb(i + height - 1, height - 1)
            for i in range(width)
        ]
        z = convolution(upper, kernel)

        for i in range(width):
            bottom[i] = (bottom[i] + z[i]) % MOD

        # Top -> right.
        x = [
            upper[i] * invfac[width - 1 - i] % MOD
            for i in range(width)
        ]
        y = fac[:width + height - 1]
        z = convolution(x, y)

        for i in range(height):
            right[i] = (
                right[i]
                + z[width - 1 + i] * invfac[i]
            ) % MOD

        # Left -> right.
        kernel = [
            comb(i + width - 1, width - 1)
            for i in range(height)
        ]
        z = convolution(left, kernel)

        for i in range(height):
            right[i] = (right[i] + z[i]) % MOD

        for i in range(width):
            add_dp(l + i, bot, bottom[i])

        # The lower-right corner belongs to both boundaries.
        for i in range(top, bot, -1):
            add_dp(r, i, right[top - i])

    def solve_staircase(l, r, bot):
        if l > r:
            return

        mid = (l + r) >> 1

        x = mid
        while x - 1 >= l and a[x - 1] == a[mid]:
            x -= 1

        y = mid
        while y + 1 <= r and a[y + 1] == a[mid]:
            y += 1

        solve_staircase(l, x - 1, a[mid] + 1)
        rect(l, y, bot, a[mid])
        solve_staircase(y + 1, r, bot)

    solve_staircase(1, n + 1, 1)
    return dp[n + 1].get(1, 0)

def solve_data(data):
    it = iter(map(int, data.split()))
    t = next(it)
    out = []

    for _ in range(t):
        n = next(it)
        a = [next(it) for _ in range(n)]
        out.append(str(count_arrays(a)))

    return "\n".join(out)

def solve():
    data = sys.stdin.buffer.read()
    sys.stdout.write(solve_data(data))

if __name__ == "__main__":
    solve()
```

The factorial initialization comes first because every rectangle transition uses binomial coefficients. The largest factorial index is at most `2n+2`, since a rectangle has at most `n+1` rows and `n+1` columns.

The `convolution` routine deliberately has a small direct-multiplication branch. NTT has a fixed overhead from bit reversal and several transform passes, so multiplying two tiny arrays directly is faster. Large products use the modulus-specific primitive root `3`, which is valid because `998244353 = 119 * 2^23 + 1`.

The rectangle routine follows the four boundary transfers exactly. The `height - 1 + i` and `width - 1 + i` indices are the most delicate parts. They come from shifting the convolution so that factorials turn the binomial coefficient into a product of two one-dimensional sequences.

The `dp` structure is sparse because the full grid has quadratic size. Only values lying on boundaries of rectangles are stored. When a new value belongs to an existing boundary, `add_dp` adds to it instead of overwriting it. The lower-right corner is generated by both the bottom and right calculations, so the implementation deliberately skips it in the second insertion.

Python integers do not overflow, but every multiplication is still reduced modulo `998244353` immediately. The recursion depth is logarithmic because each staircase region is divided around its middle, so normal Python recursion limits are sufficient for the divide and conquer itself.

The implementation follows the same rectangle and NTT strategy as the accepted contest approach. The original problem and its official limits are available on Codeforces.

## Worked Examples

### Sample 1

The first sample has `n = 4` and `a = [1,1,1,1]`. After adding the extra boundary value and reversing, the row widths are `[5,1,1,1,1]`. The path has no choice about its column while it passes through the four width-one rows, so exactly one path survives.

| Stage | Reversed row boundary | Rectangle height | Rectangle width | Result |
| --- | --- | --- | --- | --- |
| Initial state | `5,1,1,1,1` | 1 | 5 | Five initial boundary states have value `1` |
| Plateau | `1,1,1,1` | 4 | 1 | Only column `1` remains reachable |
| Final corner | `(5,1)` |  |  | `dp[5][1] = 1` |

The trace demonstrates why equal boundary values must be handled as one plateau. There is no branching in the original sequence, so the algorithm must preserve exactly one path.

### Sample 2

For `a = [1,2,3,4]`, the extended sequence is `[1,2,3,4,5]`. The resulting grid is a staircase, and the valid paths are exactly the paths from the upper-left to the lower-right corner that never leave that staircase. There are `14` such paths.

| Stage | Grid boundary | Number of paths |
| --- | --- | --- |
| Start | `(1,1)` | `1` |
| After first staircase level | width `1` | `1` |
| After second level | width `2` | `2` |
| After third level | width `3` | `5` |
| After fourth level | width `4` | `14` |

The sequence `1, 2, 5, 14` is the beginning of the Catalan sequence. This example also demonstrates why the extra row is necessary. Counting paths only through the original fourth row would stop before encoding the final free choice represented by `b4`.

The third official sample, `a = [4,4,4,4]`, has answer `35`, matching the direct stars-and-bars count of four non-decreasing values selected from four possible temperatures. The official sample outputs are `1`, `14`, and `35`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log^2 n)` | Each divide and conquer level has total rectangle boundary size `O(n)`, and each boundary transition uses NTT convolution |
| Space | `O(n log n)` | Factorials use `O(n)`, while sparse rectangle boundaries require at most logarithmically many stored layers per position |

The total `n` over all test cases is at most `5 * 10^5`, so the logarithmic factors are shared across a bounded total input size. The intended C++ implementation is comfortably within the official 8 second and 512 MB limits.

## Test Cases

```
# The solution is assumed to be saved as solution.py.
# It exposes solve_data(data), which returns the complete output string.

from solution import solve_data

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Official samples.
assert run(
    """3
4
1 1 1 1
4
1 2 3 4
4
4 4 4 4
"""
) == "1\n14\n35", "official samples"

# Minimum size.
assert run(
    """1
1
1
"""
) == "1", "minimum-size case"

# Repeated values with a non-trivial transition.
# Valid pairs (b1,b2) are (1,1), (1,2), (2,2),
# giving 3, 2, 2 choices for b3 respectively.
assert run(
    """1
3
2 2 3
"""
) == "7", "repeated boundary values"

# Boundary case where every A value is maximal.
assert run(
    """1
4
4 4 4 4
"""
) == "35", "all values equal to n"

# Large input, all values equal to 1.
# There is exactly one possible B array.
n = 200000
large = "1\n{}\n{}\n".format(n, " ".join(["1"] * n))
assert run(large) == "1", "maximum-size all-one case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `1` | Minimum size and lower boundary |
| `3 / 2 2 3` | `7` | Repeated values and plateau handling |
| `4 / 4 4 4 4` | `35` | All values equal to the maximum |
| `200000 / 1 1 ... 1` | `1` | Maximum `n`, memory handling, and extreme flat boundary |

## Edge Cases

For `n = 1` and `a = [1]`, the extended sequence is `[1,2]`. There is only one possible value for `b1`, namely `1`. The grid has exactly one valid path, so the algorithm reaches the final corner with value `1`.

For `a = [1,2,3,4]`, the extended boundary is `[1,2,3,4,5]`. The staircase path count is `14`. A construction that stops at the original row `n` would count only `5` paths, because it has not yet represented the choice of `b_n`. The extra row fixes this boundary mistake by turning `b_n` into the final downward transition.

For `a = [4,4,4,4]`, every non-decreasing four-element sequence over `{1,2,3,4}` is valid. The count is `C(4+4-1,4) = C(7,4) = 35`. In the reversed grid the boundary is mostly flat, so the maximal-plateau logic handles the entire repeated section as one rectangle rather than treating each equal row as an independent boundary change.

For `a = [2,2,3]`, the answer is `7`. The first two positions can be `(1,1)`, `(1,2)`, or `(2,2)`. Once those are fixed, the final value has respectively `3`, `2`, or `2` possible values. The rectangle transition adds these path families without merging distinct paths incorrectly, producing `7`.

For the maximum-size case `n = 200000` with every `ai = 1`, every `bi` must also equal `1`, so the answer remains `1`. The algorithm never constructs the full `200000 × 200000` DP table. It stores only the sparse boundary values and uses the flat staircase to keep the divide and conquer shallow.
