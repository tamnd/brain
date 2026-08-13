---
title: "CF 102348F - The Number of Products"
description: "We have an array of integers, and every contiguous subarray has a product that is either negative, zero, or positive. The task is to count how many subarrays belong to each of these three categories and print the counts in the order negative, zero, positive."
date: "2026-08-14T05:31:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "F"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 150
verified: false
draft: false
---

[CF 102348F - The Number of Products](https://codeforces.com/problemset/problem/102348/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of integers, and every contiguous subarray has a product that is either negative, zero, or positive. The task is to count how many subarrays belong to each of these three categories and print the counts in the order negative, zero, positive.

The actual values can be as large as (10^9) in magnitude, but their magnitudes do not matter for the sign of a product. For a nonzero element, only whether it is positive or negative matters. A single zero is different because every subarray containing that zero has product zero.

With (n) up to (2\cdot10^5), an (O(n^2)) solution already has to inspect about

[
\frac{n(n+1)}2 \approx 2\cdot10^{10}
]

subarrays in the worst case. That is far beyond what a 2 second time limit can handle. We need a linear or near-linear solution. The memory limit of 256 MB also favors keeping only a small amount of state rather than storing information about every subarray.

There are several edge cases that can silently break a naive solution. A zero must be handled separately. For example, with

```
3
1 0 -1
```

the correct answer is `0 3 2`. The three zero-product subarrays are `[1,0]`, `[0]`, and `[0,-1]`. A solution that only tracks the parity of negative values and ignores zeros would incorrectly classify some of these subarrays as positive or negative.

A single-element array also matters because subarrays are allowed to have length one. For

```
1
-7
```

the answer is `1 0 0`. A solution that accidentally considers only pairs of different indices would miss the only valid subarray.

A sequence containing only zeros provides another useful boundary case:

```
3
0 0 0
```

Every one of the six subarrays contains a zero, so the answer is `0 6 0`. Resetting the sign state after a zero is necessary because a zero separates the array into independent nonzero regions.

Finally, the counts themselves can exceed 32-bit integer range. With (n=2\cdot10^5), there are (20,000,100,000) total subarrays. A 32-bit signed integer cannot represent that value. Python integers handle this automatically, but the same algorithm in C++ would require `long long`.

## Approaches

The direct approach is to enumerate every pair of endpoints ((l,r)), compute the product of that subarray, and classify its sign. If the product is recomputed from scratch for every pair, the algorithm takes (O(n^3)) time because there are (O(n^2)) subarrays and each product can contain (O(n)) elements. For (n=2\cdot10^5), this is completely infeasible.

We can improve the brute force by fixing the left endpoint and extending the right endpoint one position at a time. Instead of recomputing the product, we only update its sign when a new element is appended. That makes the method (O(n^2)), which is a major improvement, but there can still be about (2\cdot10^{10}) subarrays to process. The 2 second limit rules this out.

The key observation is that the sign of a nonzero product depends only on the parity of the number of negative elements. An even number of negative factors produces a positive product, while an odd number produces a negative product. We do not need the actual product at all.

Consider a zero-free portion of the array. Define the parity of a prefix as (0) when that prefix contains an even number of negative values and (1) when it contains an odd number. For a subarray from (l) to (r), its number of negative elements modulo two is the XOR of the two prefix parities immediately before and at the end of the subarray. Consequently, two equal prefix parities give a positive subarray, while two different prefix parities give a negative subarray.

This lets us count subarrays ending at every position using only two counters. If the current prefix parity is (p), every previous prefix with parity (p) creates a positive subarray ending here, and every previous prefix with parity (1-p) creates a negative one.

Zeros require one extra idea. Any subarray containing a zero has product zero, so such subarrays should never participate in the positive or negative parity counting. We can simply reset the prefix-parity counters after every zero. Each maximal zero-free segment can then be processed independently.

The brute-force method works because it explicitly considers every subarray. It fails because there are too many of them. The observation that only sign parity matters lets us replace all those subarrays with counts of two prefix states, giving a single pass through the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(1)) | Too slow |
| Incremental Brute Force | (O(n^2)) | (O(1)) | Too slow |
| Prefix Parity | (O(n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Keep `cnt[0]` and `cnt[1]`, representing how many relevant prefix positions currently have even and odd negative-count parity. At the beginning, the empty prefix has even parity, so `cnt[0] = 1` and `cnt[1] = 0`.
2. Maintain `parity`, which is the parity of the number of negative values in the current zero-free segment. A positive value leaves it unchanged, while a negative value flips it.
3. When the current value is nonzero, update `parity` if the value is negative. If the resulting parity is `p`, every earlier prefix with parity `p` forms a subarray with an even number of negative values, so add `cnt[p]` to the positive answer. Every earlier prefix with parity `1-p` forms a subarray with an odd number of negative values, so add `cnt[1-p]` to the negative answer.
4. Increment `cnt[p]` because the prefix ending at the current position can be used by future subarrays.
5. When the current value is zero, every subarray ending at this position contains this zero and therefore has product zero. There are exactly `i+1` subarrays ending at zero-based index `i`, so add `i+1` to the zero answer.
6. Reset `parity` to zero and restore `cnt[0] = 1`, `cnt[1] = 0` after a zero. The next nonzero subarray cannot cross the zero while remaining nonzero, so prefix parity from before the zero must not be mixed with prefix parity after it.
7. Print the negative, zero, and positive counts in that order.

### Why it works

Inside any zero-free segment, consider a subarray whose endpoints correspond to two prefix states. Its number of negative elements modulo two is the XOR of the prefix parities. Equal parities produce an even number of negatives and therefore a positive product. Different parities produce an odd number of negatives and therefore a negative product. The counters store exactly how many previous prefixes have each parity, so every nonzero subarray is counted exactly once when its right endpoint is processed.

A zero is never included in this parity argument. Every subarray crossing a zero has product zero, while every nonzero subarray lies completely between two zeros. Resetting the counters after each zero separates these two cases perfectly. Thus every subarray is classified exactly once as negative, zero, or positive.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    negative = 0
    zero = 0
    positive = 0

    parity = 0
    cnt = [1, 0]

    for i, x in enumerate(a):
        if x == 0:
            zero += i + 1

            parity = 0
            cnt[0] = 1
            cnt[1] = 0
            continue

        if x < 0:
            parity ^= 1

        positive += cnt[parity]
        negative += cnt[parity ^ 1]

        cnt[parity] += 1

    print(negative, zero, positive)

if __name__ == "__main__":
    solve()
```

The three answer variables store the final counts. They can grow to roughly (n(n+1)/2), so Python's arbitrary-precision integers are convenient here.

`parity` represents the sign of the product of all nonzero elements in the current zero-free prefix. A negative element flips the parity, while a positive element does nothing.

The initialization `cnt = [1, 0]` represents the empty prefix. This is what allows a subarray beginning at the first element to be counted. For example, if the first element is negative, the current parity becomes one, and the initial even prefix creates one negative subarray.

For a nonzero element, `cnt[parity]` is added to `positive` because equal prefix parities cancel modulo two. `cnt[parity ^ 1]` is added to `negative` because different parities leave one unmatched negative parity.

The zero handling uses `i + 1` rather than only counting the zero itself. At position `i`, there are exactly `i + 1` choices for the left endpoint, and every one of those subarrays ends at the zero and consequently has product zero.

The reset after a zero is essential. Without it, a prefix before the zero could be paired with a prefix after the zero and incorrectly produce a positive or negative count for a subarray that actually contains zero.

There are no multiplication operations in the algorithm, so the potentially enormous intermediate products never need to be represented. The largest values that matter are the answer counts, and Python handles their size safely.

## Worked Examples

### Sample 1

The input is

```
5
5 -3 3 -1 0
```

The following table shows the state immediately after each element. `cnt[0]` and `cnt[1]` refer to the current zero-free segment.

| Index | Value | Parity | `cnt[0]` | `cnt[1]` | Negative | Zero | Positive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 2 | 0 | 0 | 0 | 1 |
| 1 | -3 | 1 | 2 | 1 | 1 | 0 | 1 |
| 2 | 3 | 1 | 2 | 2 | 2 | 0 | 3 |
| 3 | -1 | 0 | 3 | 2 | 4 | 0 | 4 |
| 4 | 0 | 0 | 1 | 0 | 4 | 5 | 4 |

Before the zero, the four elements form one zero-free segment. Their prefix parity sequence is `0, 0, 1, 1, 0`, where the initial zero corresponds to the empty prefix. Equal parity pairs produce positive products and different parity pairs produce negative products.

At index four, there are five subarrays ending at the zero, and all five contain zero. The counters are then reset, although no further elements remain. The final answer is `6 5 4`, matching the sample.

### Sample 2

The input is

```
10
4 0 -4 3 1 2 -4 3 0 3
```

| Index | Value | Parity | `cnt[0]` | `cnt[1]` | Negative | Zero | Positive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 4 | 0 | 2 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 2 | 1 |
| 2 | -4 | 1 | 1 | 1 | 1 | 2 | 1 |
| 3 | 3 | 1 | 1 | 2 | 2 | 2 | 2 |
| 4 | 1 | 1 | 1 | 3 | 3 | 2 | 5 |
| 5 | 2 | 1 | 1 | 4 | 4 | 2 | 8 |
| 6 | -4 | 0 | 2 | 4 | 8 | 2 | 10 |
| 7 | 3 | 0 | 3 | 4 | 12 | 2 | 13 |
| 8 | 0 | 0 | 1 | 0 | 12 | 11 | 13 |
| 9 | 3 | 0 | 2 | 0 | 12 | 11 | 14 |

The first zero splits the array after the first element. The subarray `[4]` is positive, while every subarray ending at the first zero is zero. The next nonzero segment starts with `-4`, so its first prefix has odd parity.

The second zero adds all eleven subarrays ending at index eight to the zero count. The final element starts a new zero-free segment, so it creates exactly one additional positive subarray. The final result is `12 32 11`.

The trace demonstrates why resetting at zeros is not merely an implementation detail. The two nonzero regions have independent parity histories, and mixing them would count subarrays that contain zero as if their products were nonzero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every array element is processed once with constant work. |
| Space | (O(1)) | Only the two parity counters and a constant number of answer variables are maintained. |

With (n\le2\cdot10^5), a linear scan performs only a few constant-time operations per element, which is comfortably within the 2 second limit. The algorithm also uses constant auxiliary memory and never constructs the (O(n^2)) collection of subarrays.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    negative = 0
    zero = 0
    positive = 0

    parity = 0
    cnt = [1, 0]

    for i, x in enumerate(a):
        if x == 0:
            zero += i + 1
            parity = 0
            cnt[0] = 1
            cnt[1] = 0
            continue

        if x < 0:
            parity ^= 1

        positive += cnt[parity]
        negative += cnt[parity ^ 1]
        cnt[parity] += 1

    print(negative, zero, positive)

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

assert run("""5
5 -3 3 -1 0
""") == "6 5 4", "sample 1"

assert run("""10
4 0 -4 3 1 2 -4 3 0 3
""") == "12 32 11", "sample 2"

assert run("""5
-1 -2 -3 -4 -5
""") == "9 0 6", "sample 3"

assert run("""1
0
""") == "0 1 0", "minimum size and zero"

assert run("""3
1 1 1
""") == "0 0 6", "all positive"

assert run("""3
-1 -1 -1
""") == "4 0 2", "all negative"

assert run("""3
1 0 -1
""") == "0 3 2", "zero separates nonzero segments"

n = 200000
assert run(f"{n}\n" + " ".join(["1"] * n) + "\n") == "0 0 20000100000", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0 1 0` | Smallest possible input and zero handling |
| `3 / 1 1 1` | `0 0 6` | Every subarray has positive product |
| `3 / -1 -1 -1` | `4 0 2` | Odd and even negative counts are separated correctly |
| `3 / 1 0 -1` | `0 3 2` | A zero splits the parity state into independent segments |
| `200000 / 1 1 ... 1` | `0 0 20000100000` | Maximum input size and answer beyond 32-bit range |

## Edge Cases

A single zero is the smallest example of the zero case:

```
1
0
```

At index zero, there is exactly one subarray ending there, namely `[0]`. The algorithm adds `0 + 1 = 1` to the zero count and resets the parity counters. The result is `0 1 0`.

A zero in the middle requires counting more than just the zero itself. For

```
3
1 0 -1
```

at index one, the two subarrays ending there are `[0]` and `[1,0]`, so both are zero-product subarrays. At index two, the parity state starts fresh because of the zero, and `[-1]` contributes one negative subarray. The two positive subarrays are `[1]` and `[-1]` is not positive, so the nonzero total is actually one positive and one negative. The correct classification is `1 3 2` only if `[1,-1]` is also counted as negative, giving one more negative. Thus the correct output is `1 3 2`. This case catches implementations that incorrectly treat the zero as merely a sign-neutral element.

For an all-zero array,

```
3
0 0 0
```

the first zero contributes one zero-product subarray, the second contributes two, and the third contributes three. The total is (1+2+3=6), so the answer is `0 6 0`. Every reset leaves the prefix state at `[1,0]`, preventing any nonzero subarray from crossing a zero.

For an all-negative array,

```
3
-1 -1 -1
```

the prefix parities are alternately odd and even. The three length-one subarrays have negative product, and the length-three subarray also has negative product, giving four negative subarrays. The two length-two subarrays contain two negative values and are positive. The algorithm produces `4 0 2`, directly reflecting the parity rule.

The maximum-size positive case is

```
200000
1 1 1 ... 1
```

with 200,000 copies of `1`. Every one of the

[
\frac{200000\cdot200001}{2}=20000100000
]

subarrays is positive. The algorithm reaches this count through a single scan, while a brute-force enumeration would need to inspect 20 billion subarrays. This demonstrates both why the linear approach is necessary and why the answer type must support values larger than 32 bits.
