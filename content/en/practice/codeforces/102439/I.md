---
title: "CF 102439I - Equal Mod Segments"
description: "For every contiguous segment [L, R], there are two ways to evaluate it. Starting at L, repeatedly take the remainder by the next array element: a[L] % a[L+1] % ... % a[R]. Starting at R, do the same thing in the opposite direction: a[R] % a[R-1] % ... % a[L]."
date: "2026-08-10T07:01:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "I"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 386
verified: true
draft: false
---

[CF 102439I - Equal Mod Segments](https://codeforces.com/problemset/problem/102439/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

For every contiguous segment `[L, R]`, there are two ways to evaluate it. Starting at `L`, repeatedly take the remainder by the next array element:

`a[L] % a[L+1] % ... % a[R]`.

Starting at `R`, do the same thing in the opposite direction:

`a[R] % a[R-1] % ... % a[L]`.

We have to count how many segments produce the same final value in both directions. A segment of length one always qualifies because both expressions contain only the same element.

The array contains up to `10^5` elements, while every value is at most `3 * 10^5`. A quadratic algorithm already has around `10^10` segments, so even constant-time processing per segment would be too slow. More realistically, evaluating the modulo chain itself costs linear time in the segment length, which pushes a direct solution to cubic time. The useful structure has to come from the fact that modulo operations quickly decrease their argument.

There are several edge cases that are easy to mishandle. For `n = 1`, the only segment must be counted, so the input

```
1
7
```

has answer `1`. A solution that only considers segments of length at least two would miss it.

Equal values can make a modulo operation produce zero. For

```
2
5 5
```

the two singletons qualify, and `[1,2]` also qualifies because both directions evaluate to `5 % 5 = 0`, so the answer is `3`. Treating equal values as if the current value remained unchanged would incorrectly return `2`. This is also the official first sample.

The endpoints do not need to be equal for a segment to qualify, and equal endpoints do not guarantee anything by themselves. For

```
2
6 3
```

the two singletons qualify, but `[1,2]` does not: the left-to-right result is `6 % 3 = 0`, while the right-to-left result is `3 % 6 = 3`. The correct answer is `2`.

Finally, the answer can exceed a 32-bit signed integer. If all `100000` elements are equal, every one of the `n(n+1)/2 = 5000050000` segments qualifies. Python integers handle this naturally, while a C++ implementation would need `long long`.

## Approaches

The direct approach is straightforward. For every pair `(L,R)`, evaluate the modulo chain from the left and evaluate it again from the right. If the two results match, increment the answer.

This is correct because it tests exactly the definition of a valid segment. The problem is the amount of work. There are `n(n+1)/2` segments, and the total length of all segments is

`n(n+1)(n+2)/6`.

For `n = 100000`, that is about `1.67 * 10^14` element visits for one direction and about `3.33 * 10^14` for both directions. The approach is nowhere near the 1.5 second limit.

The key observation is that a modulo chain does not really change at every position. Suppose the current value is `x` and the next array value is `y`. If `y > x`, then `x % y = x`, so the result does not change at all. The first position that can change the result is consequently the first position whose value is at most `x`.

Once such a position is found, the new value becomes `x % y`. If `y <= x`, this new value is strictly less than `x/2`. To see this, if `y <= x/2`, the remainder is smaller than `y`, hence smaller than `x/2`. If `y > x/2`, then the quotient is exactly one and the remainder is `x-y`, which is again smaller than `x/2`.

Thus every actual change cuts the current value by at least half. Since every array value is at most `3 * 10^5`, a fixed starting position can have only `O(log a[L])`, hence at most about twenty, distinct states.

For a fixed left endpoint `L`, we can consequently represent the whole sequence of left-to-right results as a small number of intervals. Each interval says that the result is some fixed value `v` for every right endpoint in `[p,q]`. The same construction, applied from the right, gives a small number of intervals for every fixed right endpoint.

This is the central reduction. Instead of considering every `(L,R)` separately, we obtain only `O(n log A)` horizontal and vertical intervals, where `A = max(a_i)`. A valid segment is exactly an intersection of a left-state interval and a right-state interval having the same value.

The remaining task is geometric counting. For one value `v`, a left-state interval has the form

`L = fixed, R in [p,q]`,

while a right-state interval has the form

`R = fixed, L in [p,q]`.

Their intersection is one valid pair `(L,R)` precisely when the fixed coordinates lie inside the corresponding intervals.

We process one value at a time with a sweep line over `R`. Every left-state interval becomes an active point at coordinate `L` while its right-endpoint range is active. Every right-state interval asks how many active points have `L` inside its interval. A Fenwick tree handles those point updates and range queries.

The same idea appears in the intended scanline formulation of the problem: the modulo states form only `O(n log A)` intervals, after which their intersections can be counted as a two-dimensional offline query problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^3)` | `O(1)` | Too slow |
| Optimal | `O(n log A log n)` | `O(n log A + A)` | Accepted |

## Algorithm Walkthrough

1. Build a segment tree storing the minimum array value in every segment. We need one operation repeatedly: given a starting position `p` and a current value `x`, find the first position at or after `p` whose array value is at most `x`. A minimum segment tree can answer this directly in `O(log n)` by skipping nodes whose minimum is greater than `x`.
2. Fix a left endpoint `L` and start with `x = a[L]`. The current right endpoint is `L`. Find the first position `p > L` with `a[p] <= x`. Every position from the current right endpoint through `p-1` leaves the value equal to `x`, because all their values are greater than `x`. Store one horizontal interval representing those right endpoints.
3. If such a position `p` exists, replace `x` with `x % a[p]` and continue from `p`. If no such position exists, the current value remains unchanged until the end of the array, so the state for this left endpoint is finished.
4. Repeat this for every left endpoint. Every state is stored in the bucket belonging to its value. A left-state record contains its right-endpoint interval `[p,q]` and its fixed left endpoint `L`.
5. Reverse the array and perform exactly the same procedure. A state in the reversed array corresponds to a fixed right endpoint in the original array. Convert the reversed interval back to original coordinates and store it as a vertical record containing the fixed `R` and the allowed range of `L`.
6. For each modulo value `v`, sort all its records by their sweep coordinate. A horizontal record starts being active at its smallest allowed `R`. Store its fixed `L` in a Fenwick tree and its expiration position in a min-heap.
7. When a vertical record with fixed right endpoint `R` is reached, first remove every active horizontal record whose maximum allowed `R` is smaller than `R`. The remaining Fenwick tree contains exactly the horizontal states whose intervals contain this `R`.
8. Query the Fenwick tree over the vertical record's allowed range `[L1,L2]`. Every point found represents one pair `(L,R)` for which both directions have the same value `v`, so add that count to the answer.
9. Process every value bucket and print the accumulated answer. Singleton segments are already present in both state representations, so they do not require a separate special case.

### Why it works

For every fixed `L`, the stored horizontal intervals form a partition of all possible right endpoints. Within one such interval, the left-to-right modulo value is constant because no encountered divisor is at most the current value. When the interval ends, the next divisor changes the value, and the new value is strictly smaller than half the old one. Hence the stored intervals contain exactly every possible left-to-right state.

The reversed construction gives the analogous exact partition for right-to-left states. Consider any segment `[L,R]`. It belongs to exactly one horizontal state with value `v` and exactly one vertical state with some value `w`. The segment is valid precisely when `v = w`. For a fixed value, the sweep line counts exactly those intersections where the horizontal state's right interval contains `R` and the vertical state's left interval contains `L`. Thus every valid segment is counted once, and no invalid segment is counted.

The halving property bounds the number of states generated from each starting position. Every time the current value changes, it becomes smaller than half its previous value, and once it reaches zero it never changes again because all array values are positive. This gives `O(log A)` states per endpoint.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**9
SHIFT = 17
MASK = (1 << SHIFT) - 1

def build_min_tree(a):
    n = len(a)
    size = 1 << (n - 1).bit_length()
    tree = [INF] * (2 * size)
    tree[size:size + n] = a

    for i in range(size - 1, 0, -1):
        left = tree[i << 1]
        right = tree[i << 1 | 1]
        tree[i] = left if left <= right else right

    return tree, size

def first_leq(tree, size, n, start, x):
    """First index >= start with a[index] <= x, or n if none exists."""
    if start >= n:
        return n

    p = start + size

    while p:
        if p & 1:
            if tree[p] <= x:
                while p < size:
                    left = p << 1
                    if tree[left] <= x:
                        p = left
                    else:
                        p = left | 1
                pos = p - size
                return pos if pos < n else n
            p += 1
        p >>= 1

    return n

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    max_a = max(a)

    # buckets[v] contains packed horizontal and vertical records
    # having modulo-state value v.
    buckets = [[] for _ in range(max_a + 1)]

    # ------------------------------------------------------------
    # Left-to-right states.
    #
    # Record:
    #   type = 0
    #   coord = first R for which the state is active
    #   field1 = last R for which the state is active
    #   field2 = fixed L
    #
    # Packed as:
    #   coord << 35 | field1 << 17 | field2
    # ------------------------------------------------------------
    tree, size = build_min_tree(a)

    for L in range(n):
        now = a[L]
        j = L

        while True:
            p = first_leq(tree, size, n, j + 1, now)

            if p == n:
                end = n - 1
                buckets[now].append((j << 35) | (end << SHIFT) | L)
                break

            end = p - 1
            buckets[now].append((j << 35) | (end << SHIFT) | L)

            now %= a[p]
            j = p

    # ------------------------------------------------------------
    # Right-to-left states.
    #
    # Generate them as left-to-right states on the reversed array.
    #
    # Record:
    #   type = 1
    #   coord = fixed R
    #   field1 = smallest allowed L
    #   field2 = largest allowed L
    #
    # The type bit is bit 34.
    # ------------------------------------------------------------
    rev = a[::-1]
    tree, size = build_min_tree(rev)

    for s in range(n):
        now = rev[s]
        j = s
        original_r = n - 1 - s

        while True:
            p = first_leq(tree, size, n, j + 1, now)

            if p == n:
                end = n - 1
                lo = n - 1 - end
                hi = n - 1 - j

                record = (
                    (original_r << 35)
                    | (1 << 34)
                    | (lo << SHIFT)
                    | hi
                )
                buckets[now].append(record)
                break

            end = p - 1
            lo = n - 1 - end
            hi = n - 1 - j

            record = (
                (original_r << 35)
                | (1 << 34)
                | (lo << SHIFT)
                | hi
            )
            buckets[now].append(record)

            now %= rev[p]
            j = p

    # ------------------------------------------------------------
    # For each value, count intersections between horizontal
    # and vertical state rectangles.
    # ------------------------------------------------------------
    bit = [0] * (n + 1)
    tag = [0] * (n + 1)
    stamp = 0
    answer = 0

    for bucket in buckets:
        if not bucket:
            continue

        bucket.sort()
        stamp += 1

        heap = []

        for rec in bucket:
            typ = (rec >> 34) & 1
            coord = rec >> 35
            x1 = (rec >> SHIFT) & MASK
            x2 = rec & MASK

            if typ == 0:
                # Horizontal state:
                # active for R in [coord, x1],
                # fixed L = x2.
                end = x1
                point = x2

                idx = point + 1
                while idx <= n:
                    if tag[idx] != stamp:
                        tag[idx] = stamp
                        bit[idx] = 1
                    else:
                        bit[idx] += 1
                    idx += idx & -idx

                heapq.heappush(heap, (end << SHIFT) | point)

            else:
                # Vertical state:
                # fixed R = coord,
                # allowed L in [x1, x2].
                while heap and (heap[0] >> SHIFT) < coord:
                    item = heapq.heappop(heap)
                    point = item & MASK

                    idx = point + 1
                    while idx <= n:
                        bit[idx] -= 1
                        idx += idx & -idx

                # Fenwick range sum [x1, x2].
                idx = x2 + 1
                right_sum = 0
                while idx:
                    if tag[idx] == stamp:
                        right_sum += bit[idx]
                    idx -= idx & -idx

                idx = x1
                left_sum = 0
                while idx:
                    if tag[idx] == stamp:
                        left_sum += bit[idx]
                    idx -= idx & -idx

                answer += right_sum - left_sum

        bucket.clear()

    print(answer)

if __name__ == "__main__":
    solve()
```

The segment tree stores minima rather than the actual modulo results. That is enough because the next position that can change a current value `x` is exactly the first position whose array value is at most `x`. The `first_leq` routine searches the suffix directly, avoiding a separate binary search around an RMQ query.

The left-to-right loop records `[j,end]` because every right endpoint in that interval sees exactly the same accumulated value. The state changes only at `p`, where `a[p] <= now`, and the modulo operation is performed before continuing from `p`.

The reversed pass deserves careful attention to coordinates. Reversed index `q` corresponds to original index `n-1-q`. Thus a reversed interval `[j,end]` becomes the original left-endpoint interval `[n-1-end,n-1-j]`, while the original right endpoint is fixed at `n-1-s`.

The packed integers are used instead of Python tuples because there can be `O(n log A)` records. Packing the fields substantially reduces memory consumption and also gives the records a natural sorting order by sweep coordinate and record type. Type `0` is used for horizontal records and type `1` for vertical records, so horizontal records beginning at the same coordinate are processed before a vertical query at that coordinate.

The Fenwick tree stores one count for every active fixed left endpoint. The heap tracks when those horizontal intervals stop being active. Before processing a vertical query at `R`, every horizontal interval ending before `R` is removed. Intervals ending exactly at `R` remain active, which is the required inclusive boundary condition.

The timestamp array prevents us from clearing the entire Fenwick tree after processing every value. Only positions touched during the current value bucket are considered initialized. This matters because there can be up to `3 * 10^5` different possible modulo values.

Python's arbitrary-precision integers also remove the overflow issue in the answer. The maximum possible answer is `5000050000`.

## Worked Examples

### Sample 1

The official first sample is

```
2
5 5
```

and its answer is `3`.

The left states and right states can be summarized as follows.

| Direction | Fixed endpoint | State value | Variable endpoint interval |
| --- | --- | --- | --- |
| Left | `L=1` | `5` | `R=1..1` |
| Left | `L=1` | `0` | `R=2..2` |
| Left | `L=2` | `5` | `R=2..2` |
| Right | `R=1` | `5` | `L=1..1` |
| Right | `R=2` | `5` | `L=2..2` |
| Right | `R=2` | `0` | `L=1..1` |

For value `5`, the sweep finds `(1,1)` and `(2,2)`. For value `0`, it finds `(1,2)`. The total is `3`.

The example demonstrates why equal adjacent values must create a new state. The operation `5 % 5` changes the accumulated value from `5` to `0`, so treating equal divisors as harmless would lose the length-two segment.

### Sample 2

The second sample is

```
3
8 3 5
```

with answer `4`.

The left-to-right states are

| Fixed `L` | Current state value | Right endpoints |
| --- | --- | --- |
| `1` | `8` | `1..1` |
| `1` | `2` | `2..3` |
| `2` | `3` | `2..3` |
| `3` | `5` | `3..3` |

For example, starting at `L=1`, the first value at most `8` is `3`, so `8 % 3 = 2`. Since the remaining value `5` is greater than `2`, the result stays `2` through `R=3`.

The right-to-left states are

| Fixed `R` | Current state value | Left endpoints |
| --- | --- | --- |
| `1` | `8` | `1..1` |
| `2` | `3` | `1..2` |
| `3` | `5` | `3..3` |
| `3` | `2` | `1..2` |

The matching intersections are

| Value | Segment |
| --- | --- |
| `8` | `[1,1]` |
| `3` | `[2,2]` |
| `5` | `[3,3]` |
| `2` | `[1,3]` |

So the answer is `4`.

The triple `[1,3]` is the interesting case. From the left its value is `8 % 3 % 5 = 2`, while from the right it is `5 % 3 % 8 = 2`. The scanline finds it as the intersection of the horizontal state `L=1, R in [2,3]` with the vertical state `R=3, L in [1,2]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log A log n)` | Each endpoint has `O(log A)` states, each state uses a segment-tree search, and all state records are processed with sorting and Fenwick operations |
| Space | `O(n log A + A)` | There are `O(n log A)` packed state records and `O(A)` value buckets |

Here `A = max(a_i) <= 3 * 10^5`, so each endpoint creates only a small number of states. With `n = 10^5`, the logarithmic factor from the modulo reduction is about twenty. The offline sweep avoids any quadratic enumeration of segments and fits the intended `O(n log n log A)` approach described for this problem.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function from the solution above.

```python
# Test harness for solution.py
import sys
import io

from solution import solve

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
assert run("2\n5 5\n") == "3", "sample 1"
assert run("3\n8 3 5\n") == "4", "sample 2"

# Minimum-size input
assert run("1\n7\n") == "1", "single element"

# All values equal.
# Every segment evaluates to 5 for a singleton and 0 for length >= 2.
# Both directions are identical for every segment.
assert run("3\n5 5 5\n") == "6", "all equal"

# Equal modulo can produce zero, and the boundaries are inclusive.
assert run("4\n4 2 3 2\n") == "6", "zero and boundary handling"

# A length-two segment can fail even when one direction becomes zero.
assert run("2\n6 3\n") == "2", "different two-element results"

# Maximum n and maximum answer.
n = 100000
inp = str(n) + "\n" + " ".join(["300000"] * n) + "\n"
assert run(inp) == "5000050000", "maximum size and 64-bit answer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `1` | Minimum size and singleton handling |
| `3 / 5 5 5` | `6` | Equal values and modulo results becoming zero |
| `4 / 4 2 3 2` | `6` | Multiple state changes and inclusive interval boundaries |
| `2 / 6 3` | `2` | Different left and right modulo results |
| `100000 / 300000 ... 300000` | `5000050000` | Maximum size and large answer |

## Edge Cases

The single-element case `1 / 7` produces one left state and one right state, both with value `7` and both fixed at position `1`. The sweep intersects them once, giving answer `1`.

For `2 / 5 5`, the first left state is value `5` only at `R=1`. At `R=2`, the divisor is equal to the current value, so the state changes to zero. The right-to-left construction behaves symmetrically. The value `5` contributes both singleton segments, while value `0` contributes `[1,2]`, giving `3`.

For `2 / 6 3`, the left state for `L=1` changes from `6` to `0` at the second element. The right state for `R=2` remains `3` over both possible left endpoints because `3 % 6 = 3`. Since the state values never match for the length-two segment, only the two singleton intersections remain, giving `2`.

For `4 / 4 2 3 2`, the segment `[2,4]` is particularly useful for testing interval boundaries. Its left result is `2 % 3 % 2 = 0`, while its right result is `2 % 3 % 2 = 0`, so it must be counted. The algorithm represents the left result `0` as an interval ending at `R=4` and the right result `0` as an interval beginning at `L=2`. Because both scanline boundaries are inclusive, their intersection is retained.

For the maximum input consisting entirely of `300000`, every pair `(L,R)` has equal results in both directions. There are `100000 * 100001 / 2 = 5000050000` such pairs. The state compression is especially effective here: each endpoint has only a few states because the first equal value immediately changes the accumulated value to zero, after which it stays zero.

If you want, I can also provide a **more contest-style condensed version** of this editorial, keeping the same proof and Python implementation but reducing the exposition substantially.
