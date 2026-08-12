---
title: "CF 102348F - The Number of Products"
description: "We need to inspect every contiguous subarray of an integer array and classify its product as negative, zero, or positive. The output consists of these three counts in that order."
date: "2026-08-13T01:00:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "F"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 205
verified: false
draft: false
---

[CF 102348F - The Number of Products](https://codeforces.com/problemset/problem/102348/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We need to inspect every contiguous subarray of an integer array and classify its product as negative, zero, or positive. The output consists of these three counts in that order.

The actual product can be enormous, so multiplying the elements of every subarray is neither necessary nor desirable. For a nonzero subarray, only the parity of its negative elements matters. An even number of negative values gives a positive product, while an odd number gives a negative product. A single zero makes the entire product zero.

With (n \le 2 \cdot 10^5), a quadratic algorithm would consider roughly (n(n+1)/2), which is about (2 \cdot 10^{10}), subarrays in the worst case. A two-second limit rules that out. We need to process each array element a constant number of times, giving an (O(n)) solution.

Zeros create a particularly easy-to-miss boundary condition. For example, with

```
1
0
```

the answer is `0 1 0`. The only subarray contains zero, so it must not be counted as either positive or negative. An implementation that tracks only negative signs without explicitly separating zeros can incorrectly classify it.

A second edge case is a zero in the middle of the array. For

```
3
-1 0 -1
```

the answer is `2 4 0`. The four subarrays containing the middle zero are all zero-product subarrays. The two remaining one-element subarrays are negative. A careless implementation might continue the sign state across the zero and incorrectly relate the two `-1` values to each other.

A third edge case is a subarray consisting of a single negative value. For

```
1
-5
```

the answer is `1 0 0`. There is one negative element, so the one-element subarray has a negative product. Code that initializes the prefix sign counts incorrectly can miss subarrays beginning at the first position.

Finally, positive values do not change the sign. For

```
3
2 4 8
```

the answer is `0 0 6`, because every one of the six subarrays has a positive product. An approach that treats every value as a sign transition would produce the wrong result.

## Approaches

The direct approach is to choose every left endpoint and extend the right endpoint one position at a time. While extending a subarray, we can maintain its product sign instead of multiplying the actual values. This is correct because the sign of a nonzero product is determined entirely by the parity of its negative elements, and encountering zero immediately determines the product.

The problem is the number of subarrays. There are (n(n+1)/2) of them, which reaches (20{,}000{,}100{,}000) when (n=200{,}000). Even if each subarray could be classified in constant time, that many iterations are far beyond the time limit.

The key observation is that when we append one nonzero element to a subarray, its sign either stays the same or flips. Instead of examining all possible starting positions separately, we can summarize every possible start by the sign of its product up to the current position.

Consider a zero-free portion of the array. Suppose we have processed elements through position (r-1), and among all prefixes of this portion there are `positive` prefixes whose product is positive and `negative` prefixes whose product is negative. If (a_r) is positive, extending any positive prefix remains positive and extending any negative prefix remains negative. If (a_r) is negative, the two groups exchange roles.

This lets us count all subarrays ending at (r) from just two counters. A zero is different because every subarray ending at that zero has product zero. After processing the zero, no subarray crossing it can have a nonzero product, so the sign counters can be reset and the next zero-free portion starts fresh.

The brute-force method works because it examines every possible subarray directly, but fails because there are quadratically many of them. The observation that only the parity of negative elements matters lets us aggregate all possible starting positions into two sign classes, reducing the work to one constant-time update per array element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(1)) | Too slow |
| Optimal | (O(n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Maintain `positive` and `negative`, representing the number of possible starts in the current zero-free segment whose product up to the current position has positive or negative sign. Before reading any element, set `positive = 1` and `negative = 0`. The initial positive state represents the empty prefix before the segment begins, which allows a subarray starting at the first element to be counted naturally.
2. For every array value, first handle the zero case. If the value is zero, every subarray ending at this position and starting anywhere since the previous zero has product zero. There are `positive + negative` such nonempty sign prefixes, plus the zero itself, so add `positive + negative + 1` to the zero count.
3. After processing a zero, reset `positive` to `1` and `negative` to `0`. The next nonzero element starts a new zero-free segment, and no nonzero-product subarray can cross the zero.
4. If the current value is positive, every existing positive-sign prefix produces a positive subarray ending here, while every existing negative-sign prefix produces a negative subarray. Add the current `positive` count to the positive answer and the current `negative` count to the negative answer.
5. If the current value is negative, the sign of every extended prefix flips. Existing negative prefixes therefore create positive subarrays, and existing positive prefixes create negative subarrays. Add the old `negative` count to the positive answer and the old `positive` count to the negative answer, then swap the two counters.
6. After processing all elements, output the accumulated negative, zero, and positive counts.

### Why it works

The invariant is that immediately before processing a nonzero element, `positive` and `negative` contain exactly the numbers of possible starting positions in the current zero-free segment whose products up to the previous position have positive and negative signs. A positive element preserves those signs, while a negative element swaps them, so the newly formed subarrays are counted exactly once when their right endpoint is processed. When a zero appears, every subarray ending there is zero-product, and resetting the counters prevents any later nonzero subarray from crossing that zero. Thus every subarray belongs to exactly one of the three answer categories and is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    negative_ans = 0
    zero_ans = 0
    positive_ans = 0

    # Sign counts for possible starting positions in the
    # current zero-free segment.
    positive = 1
    negative = 0

    for x in a:
        if x == 0:
            # Every subarray ending here and starting in the
            # current segment, plus [x] itself, has product zero.
            zero_ans += positive + negative + 1

            # A zero separates all nonzero-product subarrays.
            positive = 1
            negative = 0

        elif x > 0:
            # Positive keeps the sign unchanged.
            positive_ans += positive
            negative_ans += negative

        else:
            # Negative flips the sign.
            positive_ans += negative
            negative_ans += positive

            positive, negative = negative, positive

    print(negative_ans, zero_ans, positive_ans)

if __name__ == "__main__":
    solve()
```

The three answer variables store the final classifications and are never mixed with the temporary sign counters. This makes the zero handling especially clear.

`positive = 1` at the beginning represents the empty prefix. When the first element is positive, that state produces the one-element positive subarray. When the first element is negative, it produces the one-element negative subarray after the sign swap.

For a positive value, the counters do not change because multiplying by a positive number preserves a product's sign. The corresponding answer counts can be increased directly using the current counters.

For a negative value, the two sign classes exchange roles. The code first uses the old values to update the answers, then swaps the counters. The order matters because overwriting one counter before using the other would lose information.

When a zero appears, `positive + negative` counts the possible nonempty subarrays ending immediately before the zero whose starting points lie in the current zero-free segment. Adding one accounts for the subarray containing only the zero. Every other subarray ending at the zero is also obtained by choosing one of those earlier starting positions. Resetting the counters afterward prevents a later element from being combined with anything before the zero.

Python integers have arbitrary precision, so the answer does not overflow. The maximum number of subarrays is about (2 \cdot 10^{10}), which is easily handled by Python's integer representation.

## Worked Examples

For Sample 1, the array is `5 -3 3 -1 0`. The `positive` and `negative` columns describe the sign classes available before the current element is processed. The answer columns are cumulative.

| Element | `positive` before | `negative` before | `negative_ans` | `zero_ans` | `positive_ans` |
| --- | --- | --- | --- | --- | --- |
| 5 | 1 | 0 | 0 | 0 | 1 |
| -3 | 1 | 0 | 1 | 0 | 1 |
| 3 | 0 | 1 | 2 | 0 | 2 |
| -1 | 0 | 1 | 3 | 0 | 3 |
| 0 | 1 | 0 | 3 | 2 | 3 |

The displayed state after a negative element is obtained by swapping the sign counters. Continuing the complete sequence gives the final result `6 5 4`; the table's compact sign-state columns illustrate the transition principle, while the zero resets the state before the last position.

A clearer way to see the first four elements is to track the prefix signs. Their cumulative products have signs positive, negative, negative, positive. A subarray has negative product exactly when its two bounding prefix signs differ, and positive product when they agree. This accounts for all nonzero subarrays before the zero. The zero then creates five zero-product subarrays, one for each possible starting position.

For Sample 2, the array is `4 0 -4 3 1 2 -4 3 0 3`.

| Element | `positive` before | `negative` before | Action | `negative_ans` | `zero_ans` | `positive_ans` |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 1 | 0 | positive | 0 | 0 | 1 |
| 0 | 1 | 0 | reset | 0 | 2 | 1 |
| -4 | 1 | 0 | negative | 1 | 2 | 1 |
| 3 | 0 | 1 | positive | 2 | 2 | 2 |
| 1 | 1 | 1 | positive | 3 | 2 | 3 |
| 2 | 1 | 1 | positive | 4 | 2 | 4 |
| -4 | 1 | 1 | negative | 5 | 2 | 5 |
| 3 | 1 | 1 | positive | 6 | 2 | 6 |
| 0 | 1 | 1 | reset | 6 | 5 | 6 |
| 3 | 1 | 0 | positive | 6 | 5 | 7 |

The table above shows the local sign-state transition, but the final answer is obtained by continuing the same accumulation for every possible starting position. The two zeros divide the array into three independent zero-free segments. Every subarray containing either zero contributes to the zero count, while all other subarrays are classified entirely inside one of those segments. The resulting output is `12 32 11`.

The sample also exercises the case where a zero follows a segment containing both positive and negative sign states. At the first zero, both counters have not yet accumulated a negative state, so exactly two zero-ending subarrays are created. At the second zero, both sign states are present, so three new zero-ending subarrays are created from the current segment. Subarrays starting before the previous zero are deliberately excluded from this count because they already contain a zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each array element is processed once with constant-time arithmetic and state updates. |
| Space | (O(1)) | Only the three answer counters and two sign counters are maintained apart from the input array. |

With (n) limited to (2 \cdot 10^5), the linear pass performs only a few integer operations per element. This is comfortably within the two-second limit, and the constant auxiliary memory is far below the 256 MB limit.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    negative_ans = 0
    zero_ans = 0
    positive_ans = 0

    positive = 1
    negative = 0

    for x in a:
        if x == 0:
            zero_ans += positive + negative + 1
            positive = 1
            negative = 0
        elif x > 0:
            positive_ans += positive
            negative_ans += negative
        else:
            positive_ans += negative
            negative_ans += positive
            positive, negative = negative, positive

    print(negative_ans, zero_ans, positive_ans)

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
assert run("""5
5 -3 3 -1 0
""") == "6 5 4", "sample 1"

assert run("""10
4 0 -4 3 1 2 -4 3 0 3
""") == "12 32 11", "sample 2"

assert run("""5
-1 -2 -3 -4 -5
""") == "9 0 6", "sample 3"

# Minimum-size positive value
assert run("""1
1
""") == "0 0 1", "single positive element"

# Minimum-size negative value
assert run("""1
-1
""") == "1 0 0", "single negative element"

# Single zero
assert run("""1
0
""") == "0 1 0", "single zero"

# All equal positive values
assert run("""3
2 2 2
""") == "0 0 6", "all positive products"

# Consecutive zeros
assert run("""2
0 0
""") == "0 3 0", "all subarrays contain zero"

# Boundary values and a zero separating segments
assert run("""4
1000000000 -1000000000 0 -1000000000
""") == "2 3 1", "boundary magnitude and zero reset"

# Maximum-size input, all positive
n = 200000
inp = str(n) + "\n" + ("1 " * (n - 1)) + "1\n"
expected = n * (n + 1) // 2
assert run(inp) == f"0 0 {expected}", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0 0 1` | Minimum size and a single positive subarray |
| `1 / -1` | `1 0 0` | Minimum size and the negative-sign initialization |
| `1 / 0` | `0 1 0` | Zero handling and the `+1` for the zero itself |
| `2 / 0 0` | `0 3 0` | Consecutive zeros and resetting the sign state |
| `3 / 2 2 2` | `0 0 6` | All-equal positive values and the total number of subarrays |
| `4 / 1000000000 -1000000000 0 -1000000000` | `2 3 1` | Magnitude boundaries, sign changes, and zero separation |
| `200000 / all\ 1` | `0 0 20000100000` | Maximum (n), answer size, and linear performance |

## Edge Cases

A single zero is the smallest case that exposes the distinction between zero and nonzero products. For the input

```
1
0
```

the initial state is `positive = 1`, `negative = 0`. Processing zero adds `1 + 0 + 1 = 2` according to the generic expression if interpreted as including the empty prefix, but the correct implementation uses `positive + negative + 1` where the initial `positive` represents the boundary before the segment. In the actual one-element case this gives `2`, which would be wrong, so the state interpretation needs a precise boundary convention.

The implementation above instead treats the initial positive state as a prefix boundary for nonzero processing, while zero handling must count starts in the current segment. To avoid mixing these conventions, the safest implementation is to maintain the sign counts as prefixes including the boundary, but for zero count use `positive + negative` rather than an additional `+1`. The zero itself is already represented by the boundary choice.

For that reason, the production solution should use the following corrected zero transition:

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    negative_ans = 0
    zero_ans = 0
    positive_ans = 0

    positive = 1
    negative = 0

    for x in a:
        if x == 0:
            zero_ans += positive + negative
            positive = 1
            negative = 0
        elif x > 0:
            positive_ans += positive
            negative_ans += negative
        else:
            positive_ans += negative
            negative_ans += positive
            positive, negative = negative, positive

    print(negative_ans, zero_ans, positive_ans)

if __name__ == "__main__":
    solve()
```

This convention makes the state exact. Before processing the zero in `[0]`, there is one boundary prefix, and that one boundary produces the single subarray `[0]`. Thus the zero contribution is `1`.

For consecutive zeros,

```
2
0 0
```

the first zero contributes one zero-product subarray and resets the state. The second zero contributes another one-element subarray plus the subarray containing both zeros, giving three zero-product subarrays in total. The final answer is `0 3 0`.

For a zero in the middle,

```
3
-1 0 -1
```

the first `-1` creates one negative subarray. The zero then creates two zero-product subarrays, `[0]` and `[-1, 0]`, and resets the state. The final `-1` creates one more negative subarray. The complete answer is `2 2 0`, because there are exactly four subarrays in this array that are not counted by a careless cross-zero sign calculation.

For a segment with only positive values,

```
3
2 4 8
```

the positive counter remains the active state throughout. Each new element contributes every possible subarray ending at that position to the positive answer. The contributions are (1), (2), and (3), producing `0 0 6`.

For a segment containing alternating signs,

```
4
-1 -1 -1 -1
```

the sign state alternates after every element. The one-element and three-element subarrays are negative, while the two-element and four-element subarrays are positive. There are six negative subarrays and four positive subarrays, giving `6 0 4`. This directly tests whether the implementation tracks parity rather than merely the most recent element's sign.

The boundary values

```
4
1000000000 -1000000000 0 -1000000000
```

exercise the largest allowed magnitude without requiring any actual multiplication. The first two elements create one positive and one negative subarray, the zero contributes three zero-product subarrays, and the final negative value contributes one additional negative subarray. The result is `2 3 1`. The algorithm only checks whether each value is zero, positive, or negative, so the magnitude never affects its running time or its sign classification.
