---
title: "CF 102419G - Large array"
description: "The array a is not given explicitly. It is an infinite-looking repetition of the shorter array b, truncated after n elements. If b = [b0, b1, ..., b(m-1)], then every block of m consecutive elements of a is another copy of b."
date: "2026-08-14T14:53:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "G"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 244
verified: true
draft: false
---

[CF 102419G - Large array](https://codeforces.com/problemset/problem/102419/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

The array `a` is not given explicitly. It is an infinite-looking repetition of the shorter array `b`, truncated after `n` elements. If `b = [b0, b1, ..., b(m-1)]`, then every block of `m` consecutive elements of `a` is another copy of `b`.

We need a nonempty contiguous segment of `a` whose sum is exactly `k`. Among all such segments, we want the shortest one, and if several have the same length, we want the one with the smallest left endpoint.

There is a small inconsistency in the archived statement: it says the answer satisfies `1 <= l <= r <= n`, while the arrays are declared 0-indexed and the official sample prints `0 3`. The intended output is 0-based inclusive endpoints, so the implementation below follows the sample and prints `l` and `r` with `0 <= l <= r < n`.

The critical constraint is `n <= 10^9`, while only `m <= 10^5` is bounded by a normal array-processing limit. Constructing `a` explicitly can require one billion elements, which is already too large for the memory limit. Even an O(n) scan is too expensive in the worst case. The sum of `m` over all test cases is at most `3 * 10^5`, so an O(m log m) algorithm per test case is practical.

The values of `b` can be negative, so techniques such as a sliding window do not apply. Prefix sums are the natural representation because a segment sum can be expressed as the difference between two prefix sums, regardless of the signs of the elements. Prefix sums can also reach roughly `10^14`, and `k` can reach `10^18`, so 32-bit arithmetic is insufficient. Python integers handle these values directly.

The first edge case is an empty segment. For example,

```
1
1 3 0
5
```

has no nonempty segment with sum zero, so the answer is `-1`. A prefix-sum implementation that allows the same prefix position to be used twice can accidentally report a zero-length segment.

The second edge case is an answer that spans an enormous number of repetitions. For

```
1
1 1000000000 1000000000
1
```

the only possible answer is the entire array, `0 999999999`. Any solution that only examines one or a few copies of `b` cannot find it.

The third edge case occurs when one complete copy of `b` has sum zero. For

```
1
2 2 0
1 -1
```

the answer is `0 1`. A search restricted to proper subarrays inside one copy would miss this full-period segment.

The fourth edge case is a negative total sum. The sample itself contains `b = [1, 1, -3]`, whose total is `-1`, and the answer is `0 3`. A derivation that assumes the number of complete periods is obtained with ordinary positive division can choose the wrong direction when the period sum is negative.

## Approaches

A direct approach would construct the full array `a`, compute its prefix sums, and look for two prefix positions whose difference is `k`. With a hash map, that would take O(n) time and O(n) memory, which is already impossible when `n` is `10^9`. Enumerating every pair of endpoints is even worse. There are `n(n+1)/2` nonempty segments, which is about `5 * 10^17` segments when `n = 10^9`.

The brute-force idea is still useful because it reveals the real structure of the problem. Every segment is determined by two prefix positions, and the only reason we cannot inspect them directly is that there are too many repeated copies of `b`.

Let `S` be the sum of one complete copy of `b`. Define prefix sums inside one copy by

`p[0] = 0`

and, for `1 <= i < m`,

`p[i] = b[0] + b[1] + ... + b[i-1]`.

A prefix position with index `q * m + r`, where `0 <= r < m`, has value

`P(q * m + r) = q * S + p[r]`.

This is the key compression. Although `q` can be as large as one billion, the non-periodic part of every prefix sum is one of only `m` values.

Consider a candidate right prefix position `y = q*m+r`. Suppose its matching left prefix position is

`x = (q-h)*m+s`.

Then

`P[y] - P[x] = h*S + p[r] - p[s]`.

For `S != 0`, the required number of complete periods is forced:

`h = (k + p[s] - p[r]) / S`.

The distance between the prefix positions is

`y-x = h*m + r-s`.

For a fixed right residue `r`, minimizing this expression means finding the smallest possible `h`, and then the largest possible `s`.

The divisibility condition gives another useful observation. We need

`p[s] ≡ p[r] - k (mod |S|)`.

Thus, for each residue modulo `|S|`, we can keep all prefix sums belonging to that residue in sorted order. If `S > 0`, increasing `p[s]` increases `h`, so we need the smallest `p[s]` above the threshold corresponding to `h >= 1`. If `S < 0`, the direction reverses, so we need the largest `p[s]` below the corresponding threshold.

The case `h = 0` is special. Then both prefix positions are in the same copy, so we must have `s < r`. We can find the latest previous occurrence of the required prefix value while scanning the residues from left to right.

If `S = 0`, complete copies contribute nothing to the prefix sum. The target condition becomes simply

`p[s] = p[r] - k`.

Inside the same copy we again need `s < r`. If no such position exists, we can use the same prefix value from the previous copy. That gives a segment of length `m+r-s`, provided its right endpoint is still inside the actual array.

The brute-force works because every valid segment corresponds to a pair of prefix sums. It fails because there are too many prefix positions. The observation that all prefix positions have the form `q*S + p[r]` lets us eliminate the huge `q` dimension and solve the remaining `m` residue cases with sorting and binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Prefix hash over `a` | O(n) | O(n) | Too slow |
| Periodic prefix compression | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum `S` of one copy of `b` and the prefix values `p[0], ..., p[m-1]`. These are enough to represent every prefix position of the huge array.
2. If `S = 0`, handle the problem separately. For each residue `r`, the required previous prefix value is `p[r] - k`. Search for the latest occurrence before `r` to obtain a segment inside the first copy. If that does not exist, use the latest occurrence anywhere and place it in the previous copy. The latter candidate ends at prefix position `m+r`, so it is usable only when `m+r <= n`.
3. If `S != 0`, group every pair `(p[s] mod |S|, p[s], s)` by its residue modulo `|S|`, and sort the complete collection by residue and then by prefix value. This lets us locate the best possible `p[s]` for every right residue using binary search.
4. Process every possible right residue `r` from `0` through `m-1`. First look for `p[s] = p[r] - k` among positions `s < r`. This is the `h = 0` case. Since its length is `r-s`, the largest valid `s` is always the best candidate for this `r`.
5. For `h >= 1`, only prefix values satisfying

`p[s] ≡ p[r] - k (mod |S|)`

can work. If `S > 0`, find the first such prefix value satisfying

`p[s] >= p[r] - k + S`.

If `S < 0`, find the last such prefix value satisfying

`p[s] <= p[r] - k + S`.

These inequalities are exactly the condition `h >= 1`, and choosing the closest possible prefix value gives the smallest `h`.
6. Once `p[s]` is selected, calculate

`h = (k + p[s] - p[r]) / S`.

The earliest occurrence of this structural candidate is obtained by choosing `q = h`. Then the left prefix position is simply `s`, and the right prefix position is `h*m+r`. The candidate is usable only when `h*m+r <= n`.
7. Convert prefix positions back to array endpoints. A prefix pair `(x,y)` represents the inclusive array segment `[x, y-1]`. Compare candidates first by their length `y-x`, then by their left endpoint `x`.
8. If no candidate was found, print `-1`. Otherwise print the best 0-based inclusive endpoints.

### Why it works

Every nonempty subarray corresponds uniquely to two prefix positions `x < y`, with sum `P[y]-P[x] = k`. For `S != 0`, writing the two positions as `(q-h)m+s` and `qm+r` gives the exact equation `h*S+p[r]-p[s]=k`. Thus every valid segment appears among the candidates considered by the algorithm.

For `h=0`, the condition `s<r` is exactly the condition that both prefix positions are in the same copy. For `h>=1`, the left prefix is automatically before the right prefix, and the congruence plus threshold search considers exactly the possible values of `s` that give a positive `h`. For a fixed `r`, the length is `h*m+r-s`, so the smallest `h` and then largest `s` give the shortest candidate. Choosing `q=h` produces the same length with the smallest possible left endpoint. The `S=0` branch considers the only two possible structural cases, same copy and previous copy. Hence every possible optimal segment is considered, and the final comparison selects exactly the required answer.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        m, n, k = map(int, input().split())
        b = list(map(int, input().split()))

        p = [0] * m
        cur = 0
        for i in range(m - 1):
            cur += b[i]
            p[i + 1] = cur

        S = sum(b)

        best_len = None
        best_l = None
        best_r = None

        def update(x, y):
            nonlocal best_len, best_l, best_r

            length = y - x
            l = x
            r = y - 1

            if best_len is None or (length, l) < (best_len, best_l):
                best_len = length
                best_l = l
                best_r = r

        if S == 0:
            last_all = {}
            for i, value in enumerate(p):
                last_all[value] = i

            last_before = {}

            for r in range(m):
                target = p[r] - k

                # h = 0, so the left prefix must be before r.
                s = last_before.get(target)
                if s is not None:
                    update(s, r)

                # Use the same prefix value in the previous copy.
                s = last_all.get(target)
                if s is not None:
                    y = m + r
                    if y <= n:
                        update(s, y)

                last_before[p[r]] = r

        else:
            D = abs(S)

            # Each item is (p[s] mod D, p[s], s).
            data = [(p[i] % D, p[i], i) for i in range(m)]
            data.sort()

            # For every residue, store the half-open interval in data.
            bounds = {}
            start = 0
            while start < m:
                key = data[start][0]
                end = start + 1
                while end < m and data[end][0] == key:
                    end += 1
                bounds[key] = (start, end)
                start = end

            last_before = {}

            for r in range(m):
                pr = p[r]
                target = pr - k

                # h = 0.
                s = last_before.get(target)
                if s is not None:
                    update(s, r)

                key = target % D
                interval = bounds.get(key)

                if interval is not None:
                    lo, hi = interval

                    if S > 0:
                        # h >= 1 means:
                        # k + p[s] - p[r] >= S
                        threshold = pr - k + S

                        idx = bisect_left(
                            data,
                            (key, threshold, -1),
                            lo,
                            hi
                        )

                        if idx < hi:
                            pval = data[idx][1]

                            # For the same pval, take the largest s,
                            # because that minimizes h*m + r - s.
                            j = bisect_right(
                                data,
                                (key, pval, m),
                                lo,
                                hi
                            ) - 1

                            s = data[j][2]
                            h = (k + pval - pr) // S
                            y = h * m + r

                            if h >= 1 and y <= n:
                                update(s, y)

                    else:
                        # h >= 1 means:
                        # k + p[s] - p[r] <= S
                        threshold = pr - k + S

                        idx = bisect_right(
                            data,
                            (key, threshold, m),
                            lo,
                            hi
                        ) - 1

                        if idx >= lo:
                            pval = data[idx][1]
                            s = data[idx][2]
                            h = (k + pval - pr) // S
                            y = h * m + r

                            if h >= 1 and y <= n:
                                update(s, y)

                last_before[pr] = r

        if best_len is None:
            out.append("-1")
        else:
            out.append(f"{best_l} {best_r}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The prefix construction stores only `m` values. `p[i]` is the sum before position `i` inside the first copy, so prefix positions in every later copy can be reconstructed algebraically instead of being materialized.

The `S == 0` branch uses two dictionaries. `last_before` contains only positions strictly before the current residue, which prevents accidentally constructing an empty segment. `last_all` supplies the latest occurrence when the matching prefix must come from the previous copy.

For `S != 0`, `data` is sorted by `p[s] mod |S|` first. Prefix values in the same residue class are exactly the values that can participate in the required equation. The binary searches implement the direction imposed by the sign of `S`. The tuple also contains `s`, so equal prefix values can be ordered by index and the latest index can be selected directly.

The calculation of `h` is performed only after the residue condition has guaranteed divisibility by `S`. Python's arbitrary-precision integers safely handle the large products involving `n`, `m`, and the prefix sums.

The code uses prefix positions internally, so a candidate `(x,y)` becomes the inclusive array interval `[x,y-1]`. This is also why the sample's `0 3` is produced for the first test case.

## Worked Examples

### Sample test 1

The input is

```
3 5 0
1 1 -3
```

The period sum is `S = -1`, and the prefix values for residues `0,1,2` are `[0,1,2]`.

| `r` | `p[r]` | target `p[r]-k` | `h=0` candidate | positive `h` candidate | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | none | none | none |
| 1 | 1 | 1 | none | `s=0, h=1, y=4` | `0 3` |
| 2 | 2 | 2 | none | `s=1, h=1, y=5` | `0 3` |

For `r=1`, choosing `s=0` gives `h=1`. The prefix positions are `x=0` and `y=4`, so the array segment is `[0,3]`, containing `1,1,-3,1` and having sum zero. The candidate for `r=2` also has length four, but starts at index `1`, so the tie-breaking rule keeps `0 3`.

### Sample test 2

The input is

```
5 5 10
1 1 1 2 2
```

Here `S=7` and

`p = [0,1,2,3,5]`.

| `r` | `p[r]` | target modulo `7` | positive candidate | right prefix `y` | usable? |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 4 | none |  | no |
| 1 | 1 | 5 | `s=4, h=2` | 11 | no |
| 2 | 2 | 6 | none |  | no |
| 3 | 3 | 0 | `s=0, h=1` | 8 | no |
| 4 | 5 | 2 | `s=2, h=1` | 9 | no |

Every algebraically valid candidate needs a right prefix position beyond `n=5`. Thus no subarray of the given array can sum to ten, and the answer is `-1`.

These traces show why `n` only appears in the final feasibility check. The potentially enormous number of copies never has to be generated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Building prefix sums is O(m), sorting the residue data is O(m log m), and each of the `m` residues performs O(log m) binary searches. |
| Space | O(m) | The prefix array, sorted data, residue boundaries, and dictionaries all contain O(m) entries. |

The total `m` over all test cases is at most `3 * 10^5`, so the solution processes only a few hundred thousand stored prefix states even when `n` is as large as `10^9`. The memory usage is linear in `m`, and the time is dominated by sorting and binary searches, which fits the 3 second and 256 MB limits much better than anything depending linearly on `n`.

## Test Cases

```python
# This harness contains the same algorithm as the submitted solution,
# but exposes solve_io() so that each test can be checked with assertions.

import sys
import io
from bisect import bisect_left, bisect_right

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        m, n, k = map(int, input().split())
        b = list(map(int, input().split()))

        p = [0] * m
        cur = 0
        for i in range(m - 1):
            cur += b[i]
            p[i + 1] = cur

        S = sum(b)

        best = None

        def update(x, y):
            nonlocal best
            cand = (y - x, x, y - 1)
            if best is None or cand[:2] < best[:2]:
                best = cand

        if S == 0:
            last_all = {}
            for i, value in enumerate(p):
                last_all[value] = i

            last_before = {}

            for r in range(m):
                target = p[r] - k

                s = last_before.get(target)
                if s is not None:
                    update(s, r)

                s = last_all.get(target)
                if s is not None:
                    y = m + r
                    if y <= n:
                        update(s, y)

                last_before[p[r]] = r

        else:
            D = abs(S)
            data = [(p[i] % D, p[i], i) for i in range(m)]
            data.sort()

            bounds = {}
            start = 0
            while start < m:
                key = data[start][0]
                end = start + 1
                while end < m and data[end][0] == key:
                    end += 1
                bounds[key] = (start, end)
                start = end

            last_before = {}

            for r in range(m):
                pr = p[r]
                target = pr - k

                s = last_before.get(target)
                if s is not None:
                    update(s, r)

                key = target % D
                interval = bounds.get(key)

                if interval is not None:
                    lo, hi = interval

                    if S > 0:
                        threshold = pr - k + S
                        idx = bisect_left(
                            data, (key, threshold, -1), lo, hi
                        )

                        if idx < hi:
                            pval = data[idx][1]
                            j = bisect_right(
                                data, (key, pval, m), lo, hi
                            ) - 1
                            s = data[j][2]
                            h = (k + pval - pr) // S
                            y = h * m + r

                            if y <= n:
                                update(s, y)

                    else:
                        threshold = pr - k + S
                        idx = bisect_right(
                            data, (key, threshold, m), lo, hi
                        ) - 1

                        if idx >= lo:
                            pval = data[idx][1]
                            s = data[idx][2]
                            h = (k + pval - pr) // S
                            y = h * m + r

                            if y <= n:
                                update(s, y)

                last_before[pr] = r

        out.append("-1" if best is None else f"{best[1]} {best[2]}")

    sys.stdin = old_stdin
    return "\n".join(out)

# Provided sample
assert solve_io("""\
2
3 5 0
1 1 -3
5 5 10
1 1 1 2 2
""") == """\
0 3
-1
""", "provided sample"

# Minimum-size input
assert solve_io("""\
1
1 1 5
5
""") == "0 0", "single element"

# Maximum n with m = 1
assert solve_io("""\
1
1 1000000000 1000000000
1
""") == "0 999999999", "huge number of repetitions"

# All equal values
assert solve_io("""\
1
4 7 6
2 2 2 2
""") == "0 2", "shortest equal-value segment"

# Zero period sum, plus an impossible large target
assert solve_io("""\
2
2 2 0
1 -1
1 3 10
1
""") == """\
0 1
-1
""", "zero total and impossible target"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 5 / 5` | `0 0` | Minimum possible array and one-element answer |
| `1 / 1 1000000000 1000000000 / 1` | `0 999999999` | Huge `n` and a segment spanning one billion elements |
| `1 / 4 7 6 / 2 2 2 2` | `0 2` | All-equal values and shortest-length selection |
| `2 / 2 2 0 / 1 -1` and `1 3 10 / 1` | `0 1`, `-1` | Zero period sum, full-period boundary, and an impossible target |

## Edge Cases

The empty-segment issue is handled by keeping `last_before` separate from the current prefix position. For

```
1
1 3 0
5
```

the only prefix values are `0` at every residue, but there is no earlier prefix position when processing the first and only residue. Since `S=5`, there is also no positive-period solution for sum zero. The algorithm prints `-1` rather than confusing a prefix with itself for a zero-length segment.

The enormous repetition case is handled without constructing `a`. For

```
1
1 1000000000 1000000000
1
```

we have `S=1` and `p[0]=0`. The equation gives `h=1000000000`. The right prefix position is `h*m+r = 1000000000`, which is exactly `n`, and the left prefix position is zero. Thus the answer is `0 999999999`. The value of `h` can be enormous, but it is only an integer calculation.

The zero-period case uses a separate branch because division by `S` would be meaningless. For

```
1
2 2 0
1 -1
```

we have `S=0` and `p=[0,1]`. At `r=0`, the target prefix value is zero, and the same value occurs at `s=0`. There is no earlier `s`, so the algorithm places that occurrence in the previous copy. The right prefix position becomes `m+r=2`, giving the array segment `[0,1]`. Its sum is `1 + (-1) = 0`, so the result is `0 1`.

A negative period sum changes the direction of the binary search. For the sample's first test, `S=-1` and `p=[0,1,2]`. At `r=1`, the required positive-period candidate has `s=0`, giving

`h = (0 + 0 - 1) / (-1) = 1`.

The right prefix position is `1*3+1=4`, so the segment is `[0,3]`. Its values are `1,1,-3,1`, whose sum is zero. The algorithm finds this candidate by searching for the largest prefix value below the negative-sum threshold, rather than using the direction valid for positive `S`.

The indexing issue is handled by converting prefix endpoints correctly. If the prefix pair is `(x,y)`, the selected array elements are exactly indices `x` through `y-1`. Thus the code prints `x` and `y-1`, which matches the official sample's 0-based output convention even though the displayed numeric bounds in the statement are inconsistent.
