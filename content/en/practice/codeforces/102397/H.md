---
title: "CF 102397H - Mahmoud and the flagstones"
description: "We have a sequence of n flagstones, and each flagstone has a color a[i]. We need to count every nonempty subset of positions whose flagstones all have exactly the same color."
date: "2026-08-10T18:07:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "H"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 269
verified: true
draft: false
---

[CF 102397H - Mahmoud and the flagstones](https://codeforces.com/problemset/problem/102397/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of `n` flagstones, and each flagstone has a color `a[i]`. We need to count every nonempty subset of positions whose flagstones all have exactly the same color. The positions are distinct, so choosing different flagstones gives different subsets even when their colors are equal.

Suppose a particular color appears `c` times. Every valid subset using this color is simply a nonempty subset of those `c` flagstones. There are `2^c` subsets in total, including the empty subset, so this color contributes `2^c - 1` valid choices. The final answer is the sum of this quantity over every color that appears.

The sequence can contain up to `10^5` flagstones, while each color is at most `10^5`. With this input size, an algorithm that examines all subsets is impossible because there can be `2^100000 - 1` nonempty subsets. Even an `O(n^2)` solution would perform around `10^10` operations in the worst case, far beyond what a roughly two-second competitive programming limit can support. We need an algorithm whose work is essentially linear in the number of flagstones.

There are several edge cases that can cause a careless implementation to fail. With a single flagstone, such as `1` followed by `5`, there is exactly one valid subset, the flagstone itself. A formula that forgets to remove the empty subset would return `2` instead of `1`.

With all colors different, for example `3` followed by `1 2 3`, every valid subset contains exactly one flagstone, so the answer is `3`. A solution that counts all subsets without grouping by color would incorrectly include mixed-color subsets such as `{1, 2}`.

With repeated colors, such as `5` followed by `5 5 1 2 3`, the two flagstones colored `5` produce three valid subsets: either one of them, or both together. The total is `3 + 1 + 1 + 1 = 6`. Counting only one subset per color would miss the combinations formed by choosing multiple flagstones of that color.

Finally, colors can occur at the maximum allowed value. For example, `2` followed by `1 100000` has answer `2`, because both colors occur once. An implementation that allocates a frequency array smaller than `100001` would access outside its intended range.

## Approaches

The direct approach is to consider every nonempty subset of the `n` positions. There are exactly `2^n - 1` such subsets. For each subset, we can inspect its selected flagstones and check whether all of their colors are equal. This is correct because every possible subset is examined and accepted precisely when it satisfies the condition.

The problem is the number of subsets. When `n = 100000`, there are `2^100000 - 1` nonempty subsets, which is already far beyond any feasible amount of work. If checking a subset requires looking at up to `n` positions, the total worst-case work is `Θ(n 2^n)`. Even with a more clever subset representation that reduces the checking cost, the `2^n` enumeration itself is already impossible.

The useful observation is that the actual positions of flagstones do not matter once we know how many times each color occurs. If color `x` appears `c` times, every valid subset whose color is `x` must choose some nonempty collection from exactly those `c` positions. The number of ways to choose such a collection is `2^c - 1`.

This turns the original subset problem into a frequency-counting problem. We first count how many flagstones have each color, then calculate `2^c - 1` for each frequency and add those contributions modulo `10^9 + 7`.

For example, in `3 5 5 1 2`, color `3` occurs once and contributes `1`, color `5` occurs twice and contributes `3`, color `1` occurs once and contributes `1`, and color `2` occurs once and contributes `1`. The total is `1 + 3 + 1 + 1 = 6`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n 2^n)` | `O(n)` | Too slow |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Create a frequency structure that records how many flagstones have each color. Since every color is between `1` and `100000`, an array of size `100001` is sufficient. Counting frequencies takes one pass over the input.
2. Precompute powers of two from `2^0` through `2^n`, always taking the result modulo `10^9 + 7`. We need `2^c` for every possible frequency `c`, and no color can occur more than `n` times.
3. Iterate over the colors and look at their frequencies. If a color occurs `c` times, there are `2^c` ways to choose a subset of those flagstones because each of the `c` positions independently has two choices, selected or not selected.
4. Subtract one from `2^c` to exclude the empty subset. Thus the contribution of this color is `2^c - 1`.
5. Add every color's contribution to the answer modulo `10^9 + 7`. Colors with frequency zero contribute nothing, so they can simply be skipped.

### Why it works

For every color `x`, let its frequency be `c`. A subset whose flagstones all have color `x` can contain only the `c` positions carrying `x`. Each of those positions has two independent choices, so there are exactly `2^c` subsets of these positions. Exactly one of them is empty, leaving `2^c - 1` nonempty valid subsets.

Every valid subset has exactly one color, so it belongs to the contribution of exactly one color. Conversely, every subset counted by a color's `2^c - 1` term contains only flagstones of that color and is therefore valid. The contributions are consequently disjoint and collectively contain every valid subset exactly once, which proves that their sum is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAX_COLOR = 100000

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    freq = [0] * (MAX_COLOR + 1)

    for color in a:
        freq[color] += 1

    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    ans = 0

    for color in range(1, MAX_COLOR + 1):
        c = freq[color]
        if c:
            ans = (ans + pow2[c] - 1) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part of `solve` reads the number of flagstones and their colors. The frequency array uses the fact that `a[i]` is at most `100000`, so `freq[color]` directly stores the number of occurrences of that color.

The `pow2` array contains every power of two that can be needed. `pow2[0]` is `1`, and each later value is obtained by doubling the previous one modulo `MOD`. This avoids recomputing powers repeatedly and keeps every stored integer small.

The answer loop uses `pow2[c] - 1`, exactly matching the combinatorial argument. The subtraction is performed before the final modulo operation in the expression, but the accumulated result is normalized with `% MOD` on every iteration. Python integers do not overflow, although modular arithmetic is still required because the requested answer is explicitly modulo `10^9 + 7`.

The frequency condition `if c:` prevents adding anything for colors that do not appear. The loop starts at `1` and ends at `100000`, so both extremes of the allowed color range are handled.

The problem has only one test case, so there is no test-case loop. The supplied statement's displayed sample formatting is inconsistent, but the intended sample is `n = 5` with colors `3 5 5 1 2`.

## Worked Examples

### Sample 1

The intended sample input is:

```
5
3 5 5 1 2
```

The frequencies are `1` for colors `1`, `2`, and `3`, and `2` for color `5`.

| Color | Frequency `c` | `2^c` | Contribution `2^c - 1` | Running answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | 1 |
| 2 | 1 | 2 | 1 | 2 |
| 3 | 1 | 2 | 1 | 3 |
| 5 | 2 | 4 | 3 | 6 |

The three colors that occur once each contribute their individual flagstones. Color `5` contributes three subsets: choosing the first `5`, choosing the second `5`, or choosing both. The final answer is `6`.

### Sample 2

Consider:

```
4
7 7 7 2
```

Color `7` occurs three times, while color `2` occurs once.

| Color | Frequency `c` | `2^c` | Contribution `2^c - 1` | Running answer |
| --- | --- | --- | --- | --- |
| 2 | 1 | 2 | 1 | 1 |
| 7 | 3 | 8 | 7 | 8 |

There are seven nonempty subsets of the three flagstones colored `7`, plus one subset containing the flagstone colored `2`. The answer is `8`.

This trace demonstrates why repeated colors are handled by powers of two rather than by simply counting how many distinct colors exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + C)` | Counting takes `O(n)`, precomputing powers takes `O(n)`, and scanning the color range takes `O(C)` where `C = 100000` |
| Space | `O(n + C)` | The powers array has `n + 1` elements and the frequency array has `100001` elements |

With `n <= 100000` and the color range also bounded by `100000`, both arrays are small enough for the `256 MB` memory limit. The total amount of work is linear in the input size and color range, so it is easily suitable for the stated time limit.

## Test Cases

```python
import sys
import io

MOD = 10**9 + 7
MAX_COLOR = 100000

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    freq = [0] * (MAX_COLOR + 1)

    for color in a:
        freq[color] += 1

    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    ans = 0

    for color in range(1, MAX_COLOR + 1):
        c = freq[color]
        if c:
            ans = (ans + pow2[c] - 1) % MOD

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("5\n3 5 5 1 2\n") == "6", "sample 1"

# Single flagstone
assert run("1\n1\n") == "1", "minimum-size input"

# All flagstones have the same color
assert run("5\n7 7 7 7 7\n") == "31", "all equal"

# Every flagstone has a different color
assert run("4\n1 2 3 4\n") == "4", "all different"

# Boundary colors 1 and 100000
assert run("6\n1 100000 100000 1 100000 1\n") == "14", "color boundaries"

# Maximum-size all-equal case
assert run("100000\n" + "100000 " * 99999 + "100000\n") == "607723519", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 / 3 5 5 1 2` | `6` | Provided sample and repeated color counting |
| `1 / 1` | `1` | Minimum input and exclusion of the empty subset |
| `5 / 7 7 7 7 7` | `31` | All-equal case, using `2^5 - 1` |
| `4 / 1 2 3 4` | `4` | All colors different, so only singleton subsets work |
| `6 / 1 100000 100000 1 100000 1` | `14` | Both color boundaries and multiple repeated colors |
| `100000 / all 100000` | `607723519` | Maximum input size and modular exponentiation |

The maximum-size expected value comes from `2^100000 - 1` modulo `10^9 + 7`. It checks both performance and the fact that the implementation performs modular arithmetic instead of attempting to materialize the enormous exact number.

## Edge Cases

A single flagstone is the smallest possible input. For `n = 1` and the array `1`, the frequency of color `1` is `1`, so its contribution is `2^1 - 1 = 1`. The algorithm prints `1`. The subtraction by one is essential here because the second subset generated by the binary choice is the empty subset, which is not allowed.

When all colors are distinct, for example `4` followed by `1 2 3 4`, every frequency is `1`. Each color contributes `2^1 - 1 = 1`, giving a total of `4`. A subset containing two different positions is rejected automatically by the frequency-based counting because no single color receives such a subset.

When every flagstone has the same color, for example `5` followed by `7 7 7 7 7`, the entire problem reduces to choosing any nonempty subset of five positions. There are `2^5 - 1 = 31` such subsets, and the algorithm obtains exactly that value from the single frequency `c = 5`.

For boundary colors, consider `6` followed by `1 100000 100000 1 100000 1`. Color `1` appears three times and contributes `7`, while color `100000` also appears three times and contributes another `7`. The answer is `14`. The frequency array has indices through `100000`, so both boundary values are represented correctly.

For the maximum input size, if all `100000` flagstones have the same color, the algorithm does not enumerate any subsets. It stores the frequency `100000`, computes `2^100000` modulo `10^9 + 7`, subtracts one, and returns `607723519`. The execution remains linear even though the mathematical number of valid subsets has about thirty thousand decimal digits.
