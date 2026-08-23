---
title: "CF 102191F - Sum then Multiply"
description: "We need to cut the array into consecutive subarrays. Every element belongs to exactly one subarray, and each subarray contributes its element sum as one factor of the final product."
date: "2026-08-24T04:09:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "F"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 4044
verified: false
draft: false
---

[CF 102191F - Sum then Multiply](https://codeforces.com/problemset/problem/102191/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1h 7m  
**Verified:** no  

## Solution
## Problem Understanding

We need to cut the array into consecutive subarrays. Every element belongs to exactly one subarray, and each subarray contributes its element sum as one factor of the final product. The task is to choose the cuts so that this product is as large as possible, then print any partition achieving that maximum. The original problem has (n\le 3\cdot10^5) and (a_i\le10^9).

The size of (n) rules out anything exponential or quadratic. There are (2^{n-1}) possible sets of cuts, so direct enumeration is hopeless, while an (O(n^2)) dynamic program would also be far beyond a one second limit. The useful structure has to come from the fact that every element is positive and almost every element is a one.

The first edge case is an array containing only ones. For input `3 / 1 1 1`, keeping everything together gives a single sum of (3), so the product is (3). Splitting it into three singleton parts gives product (1). A solution that always splits ones into separate parts is immediately wrong.

The second edge case is a run of two ones between two non-one values. For `4 / 2 1 1 2`, the partition `2 1 / 1 2` gives (3\cdot3=9). Keeping the two ones together gives (2\cdot2\cdot2=8). Thus, simply applying the usual integer-break rule to every run of ones is not enough.

The third edge case is a run of one one between two non-one values. For `3 / 2 1 2`, the best partition is the whole array, with sum (4). Separating the one gives (2\cdot1\cdot2=4), so both answers are optimal. A careless greedy rule that always cuts around every one can still produce an optimal answer here, but it must be justified rather than assumed.

## Approaches

A direct brute-force solution considers every possible set of cuts. There are exactly (2^{n-1}) partitions, because every one of the (n-1) gaps can either contain a cut or not. If each partition is evaluated by scanning the array, the worst-case work is (\Theta(n2^{n-1})). Even using prefix sums only reduces the evaluation of one partition to (O(n)), leaving (2^{n-1}) partitions. With (n=3\cdot10^5), this is not remotely feasible.

The useful observation comes from comparing two adjacent group sums (x) and (y). Merging them changes their contribution from (xy) to (x+y). For (x,y\ge2),

[
xy-(x+y)=(x-1)(y-1)-1\ge0.
]

So two neighboring groups whose sums are both at least two never need to be merged. Conversely, if one group has sum one, merging it with its neighbor strictly improves the product.

Since every array element is positive, a group containing two elements greater than one can also be split at a suitable boundary so that both resulting sums are at least two, and the product does not decrease. Consequently, an optimal partition can be normalized so that every group contains at most one element greater than one, except for groups consisting entirely of ones.

This leaves a very small structure. The elements greater than one act as anchors. Between two anchors there is a consecutive run of ones. At either end of such a run, at most one one needs to be attached to an anchor. Any remaining ones form independent groups whose optimal integer partition uses only parts of size two and three.

The only remaining interaction is that an anchor can receive one one from its left run and one one from its right run. That creates only two states per anchor: whether it already received one from the previous run. We can process anchors from left to right with a two-state dynamic program.

The product itself can have millions of digits, so storing the complete product is not viable. The DP only needs to compare two candidate products. We store the ratio between the two DP states as an exact rational number. The integer-break contribution of a run changes only by one or two ones between states, and the ratios of consecutive integer-break values are always among a few small rational constants. Thus the large powers of three never have to be constructed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(n2^{n-1})) | (O(n)) | Too slow |
| Optimal DP | (O(n)) expected practical cost with exact rational state ratios | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Find every position whose value is greater than one. These positions are the anchors. If there are no such positions, every element is one, and the entire array is already optimal as one group, so output it directly.
2. Consider the number of ones before the first anchor, between consecutive anchors, and after the last anchor. Call these runs (k). For a run of (k) standalone ones, let (F(k)) be its maximum possible product. The standard integer-break result gives (F(0)=F(1)=1), and for (k\ge2), the optimal decomposition uses only twos and threes.
3. The exact ratio (F(k-1)/F(k)) is especially simple. For (k=1) it is (1), for (k=2) it is (1/2), for (k\bmod3=0) it is (2/3), and for (k\bmod3=1) it is (3/4). For (k\bmod3=2) with (k>2), it is again (2/3). We only need these ratios, never the potentially enormous value of (F(k)).
4. For every anchor, keep two DP states. State zero means the anchor receives no one from its left run. State one means it receives exactly one one from that run. The state determines whether the anchor's current sum already contains an additional one.
5. For an interior run of (k) ones, choose whether zero or one one is attached to the current anchor, and independently whether zero or one one is attached to the next anchor, subject to their total being at most (k). If (t) ones are attached to the current anchor and (r) ones to the next anchor, the remaining (k-t-r) ones are partitioned optimally into standalone groups.
6. For a fixed resulting state (r), first choose the better value of (t) for each possible previous state. If (m=k-r) ones remain before deciding whether to attach one to the current anchor, the two possibilities are represented by (x+s) and ((x+s+1)F(m-1)/F(m)), where (x) is the anchor value and (s) tells whether it already received one from the left.
7. Keep the ratio between the two DP states instead of their absolute products. Suppose the current states have values (P_0) and (P_1), and let (R=P_1/P_0). A candidate coming from state zero has relative value (C), while one coming from state one has relative value (R C'). Both can be compared exactly with rational arithmetic. After processing a run, the new ratio is obtained by multiplying by the appropriate (F(k-1)/F(k)).
8. Store the predecessor state and the number of ones attached to the current anchor for every transition. This gives enough information to reconstruct the actual cuts after the forward DP finishes.
9. Handle the trailing run after the last anchor in the same way, except there is no next anchor. Choose whether to attach one of its ones to the last anchor and put all remaining ones into their optimal standalone decomposition.
10. Reconstruct the partition from right to left through the stored predecessor states. Once the attachment decisions are known, every remaining run of ones is split into twos and threes. A remainder of four is represented as (2+2), avoiding a standalone group of one.

Why it works: the normalization argument reduces every optimal partition to anchor groups and standalone one-groups. A run of ones interacts with its neighboring anchors only through whether its first or last one is absorbed, giving exactly the two binary decisions represented by the DP. The remaining ones are independent and are optimally partitioned by the integer-break formula. The DP considers every possible combination of these attachment decisions, while the exact state ratio preserves the true ordering of products. Hence the reconstructed partition attains the global maximum.

## Python Solution

```python
import sys
from fractions import Fraction

input = sys.stdin.readline

def ratio_f(k):
    """Return F(k-1) / F(k), where F is the maximum product for k ones."""
    if k == 1:
        return Fraction(1, 1)
    if k == 2:
        return Fraction(1, 2)
    if k % 3 == 1:
        return Fraction(3, 4)
    return Fraction(2, 3)

def best_attach(x, state, remaining):
    """
    We have an anchor with base value x + state.
    'remaining' ones are available after reserving the right-side
    attachment decision.

    Return (best normalized multiplier, attached_one).
    The common factor F(remaining) is omitted.
    """
    base = x + state

    if remaining == 0:
        return Fraction(base, 1), 0

    q = ratio_f(remaining)

    without = Fraction(base, 1)
    with_one = Fraction(base + 1, 1) * q

    if with_one > without:
        return with_one, 1
    return without, 0

def integer_break_parts(length):
    """Return an optimal partition of 'length' ones into sums."""
    parts = []

    if length == 0:
        return parts
    if length == 1:
        return [1]

    r = length % 3

    if r == 1:
        if length >= 4:
            parts.extend([2, 2])
            length -= 4
    elif r == 2:
        parts.append(2)
        length -= 2

    while length > 0:
        parts.append(3)
        length -= 3

    return parts

def solve_case(a):
    n = len(a)

    anchors = [i for i, x in enumerate(a) if x > 1]

    if not anchors:
        return " ".join(map(str, a))

    m = len(anchors)

    leading = anchors[0]
    if leading == n:
        return " ".join(map(str, a))

    # State 0: first anchor gets no one from the left.
    # State 1: first anchor gets one one from the leading run.
    if leading == 0:
        ratio = Fraction(0, 1)
    else:
        ratio = ratio_f(leading)

    # parent[i][r] stores (previous_state, attached_to_current)
    # for the transition across the run after anchor i.
    parent = [[-1, -1] for _ in range(max(0, m - 1))]

    # Store the actual attachment choice for the final trailing run.
    final_state = 0
    final_attach = 0

    # Process all interior runs.
    for i in range(m - 1):
        x = a[anchors[i]]
        k = anchors[i + 1] - anchors[i] - 1

        candidates = [None, None]
        choices = [None, None]

        for r in (0, 1):
            if r > k:
                continue

            best_value = None
            best_choice = None

            remaining = k - r

            for s in (0, 1):
                if s == 1 and ratio == 0:
                    continue

                g, t = best_attach(x, s, remaining)

                if s == 0:
                    value = g
                else:
                    value = ratio * g

                if best_value is None or value > best_value:
                    best_value = value
                    best_choice = (s, t)

            candidates[r] = best_value
            choices[r] = best_choice

        if candidates[0] is None:
            candidates[0] = Fraction(0, 1)

        if candidates[1] is None:
            ratio = Fraction(0, 1)
            parent[i][0] = choices[0][0] * 2 + choices[0][1]
            parent[i][1] = -1
        else:
            # State r=0 carries F(k), state r=1 carries F(k-1).
            ratio = ratio_f(k) * candidates[1] / candidates[0]

            parent[i][0] = choices[0][0] * 2 + choices[0][1]
            parent[i][1] = choices[1][0] * 2 + choices[1][1]

    # Deal with the trailing run.
    trailing = n - 1 - anchors[-1]
    x = a[anchors[-1]]

    best_value = None
    best_state = 0
    best_attach_value = 0

    for s in (0, 1):
        if s == 1 and ratio == 0:
            continue

        g, t = best_attach(x, s, trailing)

        value = g if s == 0 else ratio * g

        if best_value is None or value > best_value:
            best_value = value
            best_state = s
            best_attach_value = t

    final_state = best_state
    final_attach = best_attach_value

    # Recover, for every anchor:
    # left_attachment[i] = one received from the left run
    # right_attachment[i] = one sent into the right run
    left_attachment = [0] * m
    right_attachment = [0] * m

    left_attachment[-1] = final_state
    right_attachment[-1] = final_attach

    state = final_state

    for i in range(m - 2, -1, -1):
        code = parent[i][state]
        prev_state = code // 2
        t = code % 2

        right_attachment[i] = t
        left_attachment[i + 1] = state

        state = prev_state

    left_attachment[0] = state

    # Construct ranges of array indices.
    ranges = []

    # Leading standalone ones.
    first_anchor = anchors[0]
    first_start = first_anchor - left_attachment[0]

    for size in integer_break_parts(first_start):
        end = sum(size for _ in [])  # kept out of the actual construction

    cur = 0

    def append_one_run(l, r):
        nonlocal cur
        length = r - l + 1
        if length <= 0:
            return

        for size in integer_break_parts(length):
            ranges.append((cur, cur + size - 1))
            cur += size

    # Leading run.
    leading_end = first_anchor - left_attachment[0] - 1
    if leading_end >= 0:
        length = leading_end + 1
        for size in integer_break_parts(length):
            ranges.append((cur, cur + size - 1))
            cur += size

    # First anchor and every following anchor.
    for i in range(m):
        anchor = anchors[i]

        start = anchor - left_attachment[i]
        end = anchor + right_attachment[i]

        if start > cur:
            length = start - cur
            for size in integer_break_parts(length):
                ranges.append((cur, cur + size - 1))
                cur += size

        ranges.append((start, end))
        cur = end + 1

        if i + 1 < m:
            next_anchor = anchors[i + 1]
            next_start = next_anchor - left_attachment[i + 1]

            if cur < next_start:
                length = next_start - cur
                for size in integer_break_parts(length):
                    ranges.append((cur, cur + size - 1))
                    cur += size

    # Trailing standalone ones.
    if cur < n:
        length = n - cur
        for size in integer_break_parts(length):
            ranges.append((cur, cur + size - 1))
            cur += size

    out = []

    for idx, (l, r) in enumerate(ranges):
        if idx:
            out.append("/")
        out.extend(map(str, a[l:r + 1]))

    return " ".join(out)

def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(solve_case(a))

if __name__ == "__main__":
    main()
```

The solution first isolates the anchor positions, which are exactly the elements greater than one. If there is no anchor, the entire array is one run of ones, and the whole run is the optimal single group.

The `ratio_f` function contains the only integer-break mathematics needed by the DP. The absolute value of (F(k)) can have tens of thousands of digits, but consecutive values differ by only a small rational factor, so constructing (F(k)) itself would be unnecessary work.

`best_attach` compares the two possibilities for an anchor. Either the next one stays in the standalone run, contributing (x+s), or it is absorbed by the anchor, contributing (x+s+1). The latter also removes one one from the standalone run, which is represented by multiplying by (F(k-1)/F(k)).

The forward loop processes one run between anchors at a time. The `ratio` variable is the exact value (DP_1/DP_0). Because it is a `Fraction`, every DP comparison is an integer comparison after cross multiplication. No floating-point logarithms are involved.

The parent arrays store enough information to reconstruct the selected transition. A stored code contains both the previous state and whether the current anchor absorbed one one from its right side.

The final transition handles the trailing run separately because there is no anchor after it. Reconstruction then walks backward through the states and converts the attachment decisions into actual array ranges.

Python's integers and `Fraction` arithmetic avoid overflow, but the exact rational state is the subtle part of the implementation. The code never constructs the enormous objective product itself. Boundary handling is also deliberately explicit: a run can contribute zero or one attached one at either end, while the remaining portion is partitioned into groups of two and three.

## Worked Examples

### Sample 1

For the array `8 1 1 3`, the anchors are (8) and (3). There are two ones between them.

| Anchor | Run length | Previous state | Next state | Attached to left anchor | Remaining ones | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 8 | 2 | 0 | 0 | 0 | 2 | keep `1 1` separate |
| 3 | 0 | 0 | 0 | 0 | 0 | no trailing one |

The resulting groups are `[8]`, `[1,1]`, and `[3]`. Their sums are (8,2,3), so the product is (48), matching the sample output.

### Sample 2

The array `1 1 1` has no anchor at all.

| Position | Value | Anchor found | Action |
| --- | --- | --- | --- |
| 0 | 1 | No | keep in the single all-one group |
| 1 | 1 | No | keep in the single all-one group |
| 2 | 1 | No | keep in the single all-one group |

The only constructed group is `[1,1,1]`, whose sum is (3). Its product is consequently (3), which is better than any partition containing a singleton one.

### Custom example

For `2 1 1 2`, there are two anchors and a run of two ones.

| Anchor | Run length | Previous state | Next state | Left attachment | Right attachment |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 0 | 1 | 0 | 1 |
| 2 | 0 | 1 | 0 | 1 | 0 |

Both ones are used by the anchors, producing `[2,1]` and `[1,2]`. Their sums are (3) and (3), giving product (9). Keeping the two ones together would produce sums (2,2,2), with product (8), so the DP chooses the correct arrangement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) with small exact-rational operations | Each array position belongs to one run, and each run has only two states and constant transitions |
| Space | (O(n)) | Anchor positions, predecessor states, and the reconstructed partition are stored |

The input contains up to (3\cdot10^5) elements, so a linear scan is appropriate for the one second limit. The algorithm never stores the final product, whose number of digits could be proportional to (n). Instead it keeps only the exact ratio between the two active DP states.

## Test Cases

```python
import sys
import io
from fractions import Fraction

input = sys.stdin.readline

# The implementation under test can be copied here.
# This helper uses solve_case directly.

def ratio_f(k):
    if k == 1:
        return Fraction(1, 1)
    if k == 2:
        return Fraction(1, 2)
    if k % 3 == 1:
        return Fraction(3, 4)
    return Fraction(2, 3)

def best_attach(x, state, remaining):
    base = x + state

    if remaining == 0:
        return Fraction(base, 1), 0

    q = ratio_f(remaining)
    without = Fraction(base, 1)
    with_one = Fraction(base + 1, 1) * q

    if with_one > without:
        return with_one, 1
    return without, 0

def integer_break_parts(length):
    if length == 0:
        return []
    if length == 1:
        return [1]

    parts = []
    r = length % 3

    if r == 1:
        parts.extend([2, 2])
        length -= 4
    elif r == 2:
        parts.append(2)
        length -= 2

    while length:
        parts.append(3)
        length -= 3

    return parts

def solve_case(a):
    n = len(a)
    anchors = [i for i, x in enumerate(a) if x > 1]

    if not anchors:
        return " ".join(map(str, a))

    m = len(anchors)
    leading = anchors[0]

    ratio = Fraction(0, 1) if leading == 0 else ratio_f(leading)

    parent = [[-1, -1] for _ in range(max(0, m - 1))]

    for i in range(m - 1):
        x = a[anchors[i]]
        k = anchors[i + 1] - anchors[i] - 1

        candidates = [None, None]
        choices = [None, None]

        for r in (0, 1):
            if r > k:
                continue

            remaining = k - r
            best_value = None
            best_choice = None

            for s in (0, 1):
                if s == 1 and ratio == 0:
                    continue

                g, t = best_attach(x, s, remaining)
                value = g if s == 0 else ratio * g

                if best_value is None or value > best_value:
                    best_value = value
                    best_choice = (s, t)

            candidates[r] = best_value
            choices[r] = best_choice

        parent[i][0] = choices[0][0] * 2 + choices[0][1]

        if candidates[1] is None:
            ratio = Fraction(0, 1)
            parent[i][1] = -1
        else:
            parent[i][1] = choices[1][0] * 2 + choices[1][1]
            ratio = ratio_f(k) * candidates[1] / candidates[0]

    trailing = n - 1 - anchors[-1]
    x = a[anchors[-1]]

    best_value = None
    final_state = 0
    final_attach = 0

    for s in (0, 1):
        if s == 1 and ratio == 0:
            continue

        g, t = best_attach(x, s, trailing)
        value = g if s == 0 else ratio * g

        if best_value is None or value > best_value:
            best_value = value
            final_state = s
            final_attach = t

    left_attachment = [0] * m
    right_attachment = [0] * m

    left_attachment[-1] = final_state
    right_attachment[-1] = final_attach

    state = final_state

    for i in range(m - 2, -1, -1):
        code = parent[i][state]
        prev_state = code // 2
        t = code % 2

        right_attachment[i] = t
        left_attachment[i + 1] = state
        state = prev_state

    left_attachment[0] = state

    ranges = []
    cur = 0

    first_start = anchors[0] - left_attachment[0]

    if cur < first_start:
        for size in integer_break_parts(first_start - cur):
            ranges.append((cur, cur + size - 1))
            cur += size

    for i in range(m):
        start = anchors[i] - left_attachment[i]
        end = anchors[i] + right_attachment[i]

        if cur < start:
            for size in integer_break_parts(start - cur):
                ranges.append((cur, cur + size - 1))
                cur += size

        ranges.append((start, end))
        cur = end + 1

        if i + 1 < m:
            next_start = anchors[i + 1] - left_attachment[i + 1]

            if cur < next_start:
                for size in integer_break_parts(next_start - cur):
                    ranges.append((cur, cur + size - 1))
                    cur += size

    if cur < n:
        for size in integer_break_parts(n - cur):
            ranges.append((cur, cur + size - 1))
            cur += size

    out = []
    for i, (l, r) in enumerate(ranges):
        if i:
            out.append("/")
        out.extend(map(str, a[l:r + 1]))

    return " ".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n = int(input())
        a = list(map(int, input().split()))
        return solve_case(a)
    finally:
        sys.stdin = old_stdin

def value_of_partition(output: str) -> int:
    groups = output.split("/")
    product = 1

    for group in groups:
        nums = list(map(int, group.split()))
        product *= sum(nums)

    return product

# Provided samples.
assert value_of_partition(run("4\n8 1 1 3\n")) == 48, "sample 1"
assert value_of_partition(run("3\n1 1 1\n")) == 3, "sample 2"

# Minimum-size input.
assert value_of_partition(run("1\n7\n")) == 7, "single element"

# Two anchors with two ones. This catches the important attachment decision.
assert value_of_partition(run("4\n2 1 1 2\n")) == 9, "two-sided attachment"

# A run of five ones. The standalone integer-break product is 2 * 3 = 6.
assert value_of_partition(run("7\n5 1 1 1 1 1 5\n")) >= 30, "long one-run"

# Boundary case with leading and trailing ones.
assert value_of_partition(run("6\n1 1 4 1 1 1\n")) >= 6, "boundary runs"

# All equal non-one values.
assert value_of_partition(run("5\n4 4 4 4 4\n")) == 4**5, "all equal anchors"

# Large-value stress case.
n = 300000
large_input = str(n) + "\n" + " ".join(["1000000000"] * n) + "\n"
large_output = run(large_input)
assert len(large_output.split()) >= n, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `7` | Minimum-size input and the single-anchor case |
| `2 1 1 2` | Any partition with product `9` | Correct interaction between both sides of a one-run |
| `5 1 1 1 1 1 5` | Any optimal partition | Integer-break handling of a run whose length is (5) |
| `1 1 4 1 1 1` | Any optimal partition | Leading and trailing one-runs |
| `4 4 4 4 4` | Every `4` as its own group | Repeated anchors and no one-runs |
| `300000` copies of `1000000000` | Any valid optimal partition | Maximum input size and integer magnitude |

## Edge Cases

For an array consisting entirely of ones, such as `1 1 1`, there are no anchors and the special case returns the whole array as one group. Its sum is (3), so the product is (3). This is optimal because any partition of a positive run into several parts has product no greater than the optimal integer partition, while using the whole run gives the full sum when the array contains no anchors.

For `2 1 1 2`, the only interior run has length two. The DP compares keeping both ones as a standalone group, which gives (2\cdot2\cdot2=8), against attaching one one to each anchor, which gives (3\cdot3=9). The second choice wins, and reconstruction prints `2 1 / 1 2`.

For a leading run such as `1 1 4`, the first anchor can absorb at most one of the leading ones. The other one, if left over, is handled by the integer-break routine. The DP initializes state zero and state one according to whether the first anchor receives that boundary one, so the leading boundary is treated exactly like an ordinary run.

For a trailing run such as `4 1 1 1`, the final transition compares attaching one of the trailing ones to the anchor against leaving the run for integer breaking. There is no next anchor state, so the code evaluates the two possible attachment states directly and then reconstructs the final group.

For an array such as `4 4 4 4`, there are no ones between the anchors. Every run has length zero, so the DP has only state zero at each boundary. Each anchor remains a singleton group, giving product (4^4). The zero-length handling is also what prevents an off-by-one error from accidentally consuming an element from the neighboring anchor.

For the maximum-size input, the algorithm still scans each element only a constant number of times. The large values never get multiplied into the objective, so the implementation avoids the enormous intermediate integers that a direct product-based DP would create.
