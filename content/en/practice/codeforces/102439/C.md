---
title: "CF 102439C - Cockroach Racing"
description: "We have n cockroaches, and each cockroach has an m digit number written on its back. Some digits are known, while every ? can independently be replaced by any digit from 0 to 9. Leading zeroes are allowed."
date: "2026-08-12T08:11:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "C"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 235
verified: true
draft: false
---

[CF 102439C - Cockroach Racing](https://codeforces.com/problemset/problem/102439/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` cockroaches, and each cockroach has an `m` digit number written on its back. Some digits are known, while every `?` can independently be replaced by any digit from `0` to `9`. Leading zeroes are allowed.

After replacing all question marks, the resulting numbers must satisfy

[
x_1 < x_2 < \dots < x_n.
]

The task is not to construct one such sequence. We have to consider every valid restoration and add the values of all `n` numbers appearing in that restoration. The final answer is this total modulo (10^9+7). The official constraints are (n,m\le 50), with a 1.5 second time limit.

Because every number has the same length, comparing two numbers numerically is exactly the same as comparing their digit strings lexicographically. The first position where the two numbers differ decides their order.

The bounds of 50 are small enough for dynamic programming over intervals of cockroaches, but far too small for anything exponential in either `n` or `m`. If all `n*m` positions are question marks, there are (10^{nm}) restorations. At the maximum size this is (10^{2500}) possibilities. Even checking one restoration in (O(nm)) time would give roughly (2450\cdot10^{2500}) digit comparisons, so brute force is completely impossible.

There are three edge cases that tend to cause silent errors.

First, the order is strictly increasing, not nondecreasing. For

```
2 1
?
?
```

the valid pairs are the 45 pairs (0<1,0<2,\ldots,8<9) and their combinations. Each digit appears in exactly 9 valid pairs, so the answer is (9(0+1+\dots+9)=405). Treating `<=` as valid would incorrectly include equal pairs and produce 495.

Second, leading zeroes are real digits and must not be discarded. For

```
2 2
0?
10
```

the first number can be `00` through `09`, while the second number is `10`. All ten restorations are valid, and their total is

[
(0+1+\dots+9)+10\cdot10=145.
]

An implementation that interprets `0?` as an invalid representation would incorrectly reject all of them.

Third, equality at an early digit does not mean the two numbers are equal. For

```
2 2
??
??
```

two numbers may have the same first digit and still form a valid pair if their second digits are strictly increasing. The equal-prefix case must continue to the next digit instead of being rejected immediately.

## Approaches

The direct approach is to replace every question mark independently, construct all resulting numbers, and test whether the sequence is strictly increasing. It is correct because it explicitly examines every possible restoration. Its problem is the search space. With `q` question marks it considers (10^q) assignments, and in the worst case (q=nm=2500). Even before considering the cost of computing the requested sum, this gives (10^{2500}) candidates, so brute force is unusable.

The useful observation is that an increasing sequence has a very specific structure when we inspect one digit position at a time.

Suppose a consecutive interval of cockroaches currently has the same prefix. At the next digit, their chosen digits must be nondecreasing. Whenever the digit strictly increases between two consecutive cockroaches, those two sides are already ordered forever, so the interval splits into two independent groups. Cockroaches receiving the same digit remain in the same group and have to be ordered by their remaining suffixes.

For example, if four cockroaches currently share the same prefix and their next digits are

[
2,2,5,8,
]

then the sequence splits into the groups `[1,2]`, `[3,3]`, and `[4,4]`. The first group still needs its suffixes to be increasing, while the other two groups each contain one cockroach and need no further ordering.

This turns the exponential set of comparison states into an interval dynamic program. Define `cnt[l][r]` as the number of valid ways to fill the remaining suffix when cockroaches `l` through `r` currently have an identical prefix. Also define `sum[l][r]` as the sum of all their number values over those ways, considering only the remaining suffix.

At one digit, an interval is divided into consecutive blocks. Every block receives one digit, the block digits are strictly increasing, and the suffixes of different blocks are independent. A block `[k,r]` is allowed to receive digit `d` exactly when every pattern from `k` through `r` accepts `d` at this position.

We can enumerate the last block and the digit assigned to it. The previous blocks must use smaller digits. Since there are only ten possible digits, we keep another small DP dimension for the last digit. This gives (O(10mn^3)) time, which is practical for `n,m <= 50`.

The same DP can carry sums as well as counts. When two independent blocks are combined, their counts multiply. Their sums combine as

[
S = S_1C_2+C_1S_2.
]

The current digit contributes its value times the appropriate power of ten, once for every cockroach in the whole interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm\cdot10^{nm})) | (O(nm)) | Too slow |
| Interval DP | (O(10mn^3)) | (O(n^2+mn)) | Accepted |

## Algorithm Walkthrough

1. Convert every pattern position into a ten-bit mask. Bit `d` is set when digit `d` can be placed at that position. This makes checking whether a whole interval can receive one digit an integer bit operation.
2. Process digit positions from right to left. At the beginning, there are no remaining digits. Thus an interval containing one cockroach has one valid empty suffix, while an interval containing at least two cockroaches has zero valid suffixes because equal complete numbers are not allowed.
3. For the current digit position, consider an interval `[l,r]` whose previous prefix is identical for every cockroach inside it. The chosen current digits must be nondecreasing. Equal digits form one block, while a strict increase separates two independent blocks.
4. Fix the digit `d` of the last block `[k,r]`. The block is legal only if every pattern from `k` through `r` accepts `d`. For each position and digit, we precompute the first index from which an interval ending at `r` can consist entirely of patterns accepting that digit. This avoids checking every character separately inside the transition.
5. The part `[l,k-1]`, if nonempty, must end with a digit smaller than `d`. For every possible `k`, the prefix DP tells us the number of ways and the total suffix sum for all such previous blocks. The block `[k,r]` contributes its already computed `cnt[k][r]` and `sum[k][r]`.
6. Combine the previous part and the final block. If their counts are `C1` and `C2`, the combined count is `C1*C2`. If their sums are `S1` and `S2`, the combined suffix sum is `S1*C2 + C1*S2`, because every assignment of the first part can be paired with every assignment of the second part.
7. After computing the DP for the current digit, add the current digit itself to the sum. If the interval contains `r-l+1` cockroaches and the current position has place value (10^{m-1-p}), assigning digit `d` contributes

[
d\cdot(r-l+1)\cdot10^{m-1-p}
]

to every assignment counted by that state.

1. After all positions have been processed, `cnt[0][n-1]` counts every valid complete sequence and `sum[0][n-1]` is exactly the requested total.

### Why it works

The invariant is that `cnt[l][r]` and `sum[l][r]` describe exactly all valid suffix assignments for cockroaches `l..r` under the assumption that their already processed prefixes are equal. At the current digit, every valid assignment has a unique partition into maximal consecutive blocks with equal current digits. Those block digits are strictly increasing, and different blocks can be completed independently. The transition enumerates every possible last block and every possible digit for it, so every valid assignment is counted exactly once. Conversely, every transition creates nondecreasing current digits and recursively valid suffixes, so it creates a strictly increasing sequence. Carrying both counts and sums through the same decomposition gives the requested total without enumerating individual assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n, m = map(int, input().split())
    patterns = [input().strip() for _ in range(n)]

    # allowed[pos][i] is a bit mask of digits allowed for cockroach i.
    allowed = [[0] * n for _ in range(m)]

    for i in range(n):
        s = patterns[i]
        for p, ch in enumerate(s):
            if ch == '?':
                allowed[p][i] = (1 << 10) - 1
            else:
                allowed[p][i] = 1 << (ord(ch) - ord('0'))

    # next_cnt[l][r], next_sum[l][r]:
    # valid completions for positions p+1 ... m-1,
    # assuming positions before p are equal for l..r.
    next_cnt = [[0] * n for _ in range(n)]
    next_sum = [[0] * n for _ in range(n)]

    for i in range(n):
        next_cnt[i][i] = 1

    pow10 = [1] * m
    for i in range(1, m):
        pow10[i] = pow10[i - 1] * 10 % MOD

    for p in range(m - 1, -1, -1):
        # start[d][r] is the first k such that every pattern k..r
        # accepts digit d at position p.
        start = [[0] * n for _ in range(10)]
        last_bad = [-1] * 10

        for r in range(n):
            mask = allowed[p][r]
            for d in range(10):
                if not (mask >> d) & 1:
                    last_bad[d] = r
                start[d][r] = last_bad[d] + 1

        cur_cnt = [[0] * n for _ in range(n)]
        cur_sum = [[0] * n for _ in range(n)]

        for l in range(n):
            # fcnt[r][d]:
            # ways for [l,r] where the last current-digit block uses d.
            #
            # fsum[r][d]:
            # corresponding sum, including positions p+1..m-1,
            # but not yet the current digit at p.
            fcnt = [[0] * 10 for _ in range(n)]
            fsum = [[0] * 10 for _ in range(n)]

            # Prefix sums over the possible last digit.
            pref_cnt = [[0] * 10 for _ in range(n)]
            pref_sum = [[0] * 10 for _ in range(n)]

            weight = pow10[m - 1 - p]

            for r in range(l, n):
                row_sum = 0

                for d in range(10):
                    lo = max(l, start[d][r])
                    if lo > r:
                        continue

                    ways = 0
                    total = 0

                    for k in range(lo, r + 1):
                        block_cnt = next_cnt[k][r]
                        if block_cnt == 0:
                            continue

                        block_sum = next_sum[k][r]

                        if k == l:
                            prev_cnt = 1
                            prev_sum = 0
                        elif d == 0:
                            continue
                        else:
                            prev_cnt = pref_cnt[k - 1][d - 1]
                            prev_sum = pref_sum[k - 1][d - 1]

                        ways += prev_cnt * block_cnt
                        total += prev_sum * block_cnt + prev_cnt * block_sum

                    fcnt[r][d] = ways % MOD
                    fsum[r][d] = total % MOD

                    row_sum += fsum[r][d]

                # Build prefix sums for this r.
                pc = 0
                ps = 0
                for d in range(10):
                    pc += fcnt[r][d]
                    ps += fsum[r][d]
                    pref_cnt[r][d] = pc % MOD
                    pref_sum[r][d] = ps % MOD

                total_cnt = pc % MOD

                # Add the current digit to every cockroach in [l,r].
                size = r - l + 1
                digit_contribution = 0

                for d in range(10):
                    digit_contribution += (
                        d * size * weight * fcnt[r][d]
                    )

                cur_cnt[l][r] = total_cnt
                cur_sum[l][r] = (
                    row_sum + digit_contribution
                ) % MOD

        next_cnt = cur_cnt
        next_sum = cur_sum

    print(next_sum[0][n - 1] % MOD)

if __name__ == "__main__":
    solve()
```

The first part of the implementation converts every pattern position into a digit mask. A `?` gets all ten bits, while a fixed digit gets exactly one bit. The DP never has to inspect the original characters again.

`next_cnt` and `next_sum` represent the state after the current position has been removed. The diagonal entries are initialized to one because a single cockroach always has exactly one empty suffix. Intervals of length at least two start at zero because equal complete numbers cannot satisfy a strict ordering.

For each position, `start[d][r]` records how far left a block ending at `r` may extend while still allowing digit `d`. If pattern `r` rejects `d`, no such block exists. Otherwise the boundary is determined by the most recent pattern rejecting `d`. This is the interval-validity condition used by the transition.

For a fixed starting point `l`, `fcnt[r][d]` and `fsum[r][d]` describe all partitions of `[l,r]` whose last block receives digit `d`. The transition chooses the beginning `k` of that last block. The earlier part must end with a smaller digit, which is why `pref_cnt[k-1][d-1]` and `pref_sum[k-1][d-1]` are used.

The `k == l` case represents an empty prefix before the final block. Its count is one and its sum is zero. This boundary case is necessary for intervals whose first block occupies the whole interval.

The sum transition uses multiplication of counts because the two blocks are independent after their current digits differ. The corresponding sums use `prev_sum * block_cnt + prev_cnt * block_sum`, which accounts for the fact that each assignment on one side can be paired with every assignment on the other.

Finally, `digit_contribution` adds the current digit to every cockroach in the interval. The multiplication by `pow10[m-1-p]` is what converts a digit into its actual numeric place value. Python integers do not overflow, but all DP values are reduced modulo (10^9+7) so intermediate values remain small enough for efficient arithmetic.

## Worked Examples

### Sample 1

The input is

```
2 2
??
??
```

At the last position, two single cockroaches each have ten choices. For the interval containing both cockroaches, the last digits must satisfy `a < b`, giving 45 possibilities.

| Position | Interval | Count | Suffix sum |
| --- | --- | --- | --- |
| 1 | `[0,0]` | 10 | 45 |
| 1 | `[1,1]` | 10 | 45 |
| 1 | `[0,1]` | 45 | 405 |
| 0 | `[0,0]` | 100 | 4500 |
| 0 | `[1,1]` | 100 | 4500 |
| 0 | `[0,1]` | 4950 | 490050 |

At position 0, two different first digits immediately establish the ordering, while equal first digits leave the suffix comparison to the state computed for position 1. The final sum is

```
490050
```

which matches the sample.

### Sample 2

The input is

```
2 3
4??
??2
```

At the last digit, the first cockroach can use `0` or `1` when the prefixes are still equal, because the second cockroach is forced to use `2`. This gives two suffix pairs and a suffix sum of `5`.

At the next position, the two digits can already be different, or they can be equal and let the final position decide the order.

| Position | Interval | Count | Sum from current suffix onward |
| --- | --- | --- | --- |
| 2 | `[0,1]` | 2 | 5 |
| 1 | `[0,1]` | 470 | 45275 |
| 0 | `[0,1]` | 5470 | 6403775 |

At position 0, the first number starts with `4`. If the second number starts with `5` through `9`, the ordering is already decided and both remaining suffixes are independent. If it also starts with `4`, the suffix state with 470 valid completions is reused. Combining these cases gives the final answer `6403775`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(10mn^3)) | For every digit position, starting interval, ending interval, digit, and possible final block boundary, one transition is processed. |
| Space | (O(n^2+mn)) | Two `n x n` DP layers are stored, together with the input masks and small per-position auxiliary arrays. |

With (n,m\le50), the cubic factor is manageable because the digit dimension is only ten and the interval transitions contain only about (O(n^3)) combinations per position. The algorithm avoids every dependence on (10^{nm}), which is the key requirement for these constraints.

## Test Cases

```python
import sys
import io

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    patterns = [input().strip() for _ in range(n)]

    allowed = [[0] * n for _ in range(m)]

    for i in range(n):
        s = patterns[i]
        for p, ch in enumerate(s):
            if ch == '?':
                allowed[p][i] = (1 << 10) - 1
            else:
                allowed[p][i] = 1 << (ord(ch) - ord('0'))

    next_cnt = [[0] * n for _ in range(n)]
    next_sum = [[0] * n for _ in range(n)]

    for i in range(n):
        next_cnt[i][i] = 1

    pow10 = [1] * m
    for i in range(1, m):
        pow10[i] = pow10[i - 1] * 10 % MOD

    for p in range(m - 1, -1, -1):
        start = [[0] * n for _ in range(10)]
        last_bad = [-1] * 10

        for r in range(n):
            mask = allowed[p][r]
            for d in range(10):
                if not ((mask >> d) & 1):
                    last_bad[d] = r
                start[d][r] = last_bad[d] + 1

        cur_cnt = [[0] * n for _ in range(n)]
        cur_sum = [[0] * n for _ in range(n)]

        weight = pow10[m - 1 - p]

        for l in range(n):
            fcnt = [[0] * 10 for _ in range(n)]
            fsum = [[0] * 10 for _ in range(n)]
            pref_cnt = [[0] * 10 for _ in range(n)]
            pref_sum = [[0] * 10 for _ in range(n)]

            for r in range(l, n):
                row_sum = 0

                for d in range(10):
                    lo = max(l, start[d][r])
                    if lo > r:
                        continue

                    ways = 0
                    total = 0

                    for k in range(lo, r + 1):
                        block_cnt = next_cnt[k][r]
                        if block_cnt == 0:
                            continue

                        block_sum = next_sum[k][r]

                        if k == l:
                            prev_cnt = 1
                            prev_sum = 0
                        elif d == 0:
                            continue
                        else:
                            prev_cnt = pref_cnt[k - 1][d - 1]
                            prev_sum = pref_sum[k - 1][d - 1]

                        ways += prev_cnt * block_cnt
                        total += prev_sum * block_cnt
                        total += prev_cnt * block_sum

                    fcnt[r][d] = ways % MOD
                    fsum[r][d] = total % MOD
                    row_sum += fsum[r][d]

                pc = 0
                ps = 0

                for d in range(10):
                    pc += fcnt[r][d]
                    ps += fsum[r][d]
                    pref_cnt[r][d] = pc % MOD
                    pref_sum[r][d] = ps % MOD

                size = r - l + 1
                digit_sum = 0

                for d in range(10):
                    digit_sum += d * size * weight * fcnt[r][d]

                cur_cnt[l][r] = pc % MOD
                cur_sum[l][r] = (row_sum + digit_sum) % MOD

        next_cnt = cur_cnt
        next_sum = cur_sum

    print(next_sum[0][n - 1] % MOD)

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

# Provided samples
assert run("""2 2
??
??
""") == "490050", "sample 1"

assert run("""2 3
4??
??2
""") == "6403775", "sample 2"

assert run("""4 1
0
?
4
8
""") == "42", "sample 3"

# Minimum-size input
assert run("""1 1
?
""") == "45", "single question mark"

# Strict inequality boundary
assert run("""2 1
?
?
""") == "405", "strictly increasing, not nondecreasing"

# Leading zeroes are valid
assert run("""2 2
0?
10
""") == "145", "leading zeroes"

# Fixed increasing sequence
assert run("""3 1
1
2
3
""") == "6", "fixed increasing sequence"

# All equal values give no valid sequence
assert run("""3 1
7
7
7
""") == "0", "equal values"

# Maximum-size input, deliberately impossible
maximum = "50 50\n" + ("0" * 50 + "\n") * 50
assert run(maximum) == "0", "maximum-size impossible input"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / ?` | `45` | Minimum size and single-interval DP |
| `2 1 / ? / ?` | `405` | Strict inequality and equal-value rejection |
| `2 2 / 0? / 10` | `145` | Leading zeroes |
| `3 1 / 1 / 2 / 3` | `6` | Completely fixed valid sequence |
| `3 1 / 7 / 7 / 7` | `0` | All-equal values |
| `50 50` with all zeroes | `0` | Maximum-size input and impossible intervals |

## Edge Cases

The strict-inequality case

```
2 1
?
?
```

starts with the base state for two single-element intervals. At the only digit position, the two elements must form two different blocks, with the first block's digit smaller than the second's. There are 45 such digit pairs. The sum of the two digits over all pairs is 405, so the DP returns exactly `405`. Equal digits never enter the transition because the final digit position has no suffix left to separate them.

For leading zeroes,

```
2 2
0?
10
```

the first pattern represents the ten values `00,01,...,09`, while the second is `10`. The first number is always smaller, so there are ten valid sequences. Their total is 145. The DP treats `0` as an ordinary allowed digit and never converts the pattern into an integer prematurely, so the leading zero causes no special case.

For equal prefixes,

```
2 2
??
??
```

the first digit may be equal for both cockroaches. In that situation the interval remains a single block, and the DP uses the state from the next digit. At the second digit, only strictly increasing pairs survive. This is exactly why the recurrence can handle equal prefixes without storing an explicit comparison state for every adjacent pair.

For an impossible sequence such as

```
3 1
7
7
7
```

the base state contains no valid interval of length greater than one. Processing the only digit cannot split the three cockroaches into different digits because every pattern accepts only `7`. The resulting count and sum are both zero.

For the maximum-size all-zero input, every interval containing two or more cockroaches remains impossible at every position. The DP still processes the full `50 x 50` instance, but all non-singleton states stay zero. The answer is consequently `0`, and the memory usage remains quadratic in `n`.
