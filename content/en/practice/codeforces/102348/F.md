---
title: "CF 102348F - The Number of Products"
description: "We have an array of (n) integers, and every contiguous subarray contributes according to the sign of its product. For each pair of endpoints (l le r), the product of (al,a{l+1},ldots,ar) is either negative, zero, or positive."
date: "2026-08-16T16:02:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "F"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 880
verified: false
draft: false
---

[CF 102348F - The Number of Products](https://codeforces.com/problemset/problem/102348/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of (n) integers, and every contiguous subarray contributes according to the sign of its product. For each pair of endpoints (l \le r), the product of (a_l,a_{l+1},\ldots,a_r) is either negative, zero, or positive. We need to count how many subarrays belong to each category and print the three counts in that order.

The actual value of a nonzero product is irrelevant. Only its sign matters. A product is negative exactly when the subarray contains an odd number of negative elements, and it is positive when it contains an even number of negative elements. Any subarray containing at least one zero has product zero.

The array can contain up to (2\cdot10^5) elements. A quadratic algorithm would inspect roughly (n(n+1)/2) subarrays, which is about (2\cdot10^{10}) when (n=2\cdot10^5). That is far beyond what a 2-second limit can handle. We need an (O(n)) or (O(n\log n)) solution. The answer itself can also be around (n(n+1)/2), so 64-bit integers are required in languages with fixed-width integer types. Python integers already handle these values safely.

Zeros need separate treatment because a zero destroys the sign information. For example, with input

```
1
0
```

the correct answer is

```
0 1 0
```

A sign-parity algorithm that treats zero as neither positive nor negative but continues the previous prefix state would incorrectly allow subarrays to cross the zero and classify them by their old sign. A zero must split the array into independent nonzero segments.

Another easy case to mishandle is an array containing only positive values. For

```
3
1 1 1
```

every one of the (6) subarrays has positive product, so the answer is

```
0 0 6
```

A method that only counts products changing sign can forget to count single-element and even-length combinations of positive elements.

Negative values also require counting the empty prefix correctly. For

```
3
-1 -1 -1
```

the correct answer is

```
4 0 2
```

The negative-product subarrays have odd length, giving (3+1=4), while the two even-length subarrays have positive products. Forgetting the prefix before the first element loses subarrays starting at index (1).

Finally, zeros can occur at the boundaries. For

```
3
0 1 0
```

the correct answer is

```
0 5 1
```

There are six total subarrays, and only ([2,2]) has a nonzero positive product. The other five contain a zero. Any solution that counts zero-containing subarrays only when it encounters the zero can miss subarrays that continue beyond that zero.

## Approaches

The direct approach is to enumerate every pair of endpoints ((l,r)). For a fixed left endpoint, we can extend the right endpoint one position at a time and maintain the current product sign. Multiplying the actual values is unnecessary, since only whether the number of negative elements is odd or even matters, and zero can be detected immediately.

This brute-force method is correct because every contiguous subarray is considered exactly once. The problem is the number of subarrays. There are (n(n+1)/2) of them, which reaches (20,000,100,000) for (n=200,000). Even constant-time processing per subarray is too much, so the quadratic approach is ruled out.

The key observation is that the sign of a nonzero subarray depends only on the parity of the number of negative elements inside it. We can encode this parity as (0) for an even number of negatives and (1) for an odd number.

Consider prefix parities. Let (p_i) be the parity of the number of negative elements among the current nonzero segment up to position (i). For a subarray from (l) to (r), its number of negative elements modulo (2) is

[
p_r \oplus p_{l-1}.
]

Thus, if the two prefix parities are equal, the subarray has a positive product. If they differ, the subarray has a negative product.

While scanning from left to right, we only need to know how many previous prefixes have even and odd parity. If the current prefix parity is even, every previous even prefix forms a positive-product subarray ending here, while every previous odd prefix forms a negative-product subarray. The situation is reversed when the current parity is odd.

Zeros simply separate independent segments. When a zero appears, no valid nonzero subarray may cross it, so the prefix-parity counts are reset to their initial state.

Once all nonzero products have been counted, every remaining subarray must have product zero. There are (n(n+1)/2) subarrays in total, so

[
\text{zero} =
\frac{n(n+1)}2-\text{negative}-\text{positive}.
]

This avoids having to count zero-containing subarrays directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(1)) | Too slow |
| Prefix Sign Parity | (O(n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Start with one even prefix and zero odd prefixes. The initial prefix represents the empty sequence before the first element, whose number of negative values is zero.
2. Maintain `even` and `odd`, the numbers of previous prefix states with even and odd negative-count parity. Also maintain the current parity, where `0` means even and `1` means odd.
3. For every array element, first check whether it is zero. If it is zero, reset `even` to (1), `odd` to (0), and the current parity to even. A zero separates the nonzero portions of the array, so prefixes before it must not be paired with prefixes after it.
4. If the element is negative, flip the current parity. If the element is positive, leave the parity unchanged. Only the sign matters, so the magnitude of the element never enters the calculation.
5. If the current parity is even, add `even` to the positive count and `odd` to the negative count. Every previous even prefix produces an even number of negatives between the two prefixes, while every previous odd prefix produces an odd number.
6. If the current parity is odd, add `odd` to the positive count and `even` to the negative count. The two cases are reversed because equal prefix parities still cancel to an even difference.
7. Add the current prefix to the appropriate counter. This must happen after counting the subarrays ending at the current position, because the current prefix cannot be used as the left boundary of a subarray ending at the same position.
8. After processing the entire array, compute the total number of subarrays as (n(n+1)/2). Subtract the positive and negative counts to obtain the number whose product is zero.

### Why it works

For every nonzero subarray, its sign is determined by the parity of its number of negative elements. The parity of the negative count inside ([l,r]) is the XOR of the prefix parities immediately after (r) and immediately before (l). Equal prefix parities consequently represent positive products, while different prefix parities represent negative products. The counters `even` and `odd` contain exactly the required previous prefixes, so every nonzero subarray is counted once when its right endpoint is processed. Resetting after a zero prevents any zero-containing subarray from entering these counts. Since every subarray is either positive, negative, or zero, subtracting the two nonzero counts from the total gives exactly the zero count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_products(a):
    n = len(a)

    # Number of previous prefix parities in the current nonzero segment.
    even = 1
    odd = 0

    parity = 0

    negative = 0
    positive = 0

    for x in a:
        if x == 0:
            # No nonzero subarray can cross a zero.
            even = 1
            odd = 0
            parity = 0
            continue

        if x < 0:
            parity ^= 1

        if parity == 0:
            positive += even
            negative += odd
            even += 1
        else:
            positive += odd
            negative += even
            odd += 1

    total = n * (n + 1) // 2
    zero = total - positive - negative

    return negative, zero, positive

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    negative, zero, positive = count_products(a)
    print(negative, zero, positive)

if __name__ == "__main__":
    solve()
```

The function `count_products` contains the entire linear scan. `even = 1` represents the prefix before the first element. This initialization is what allows a subarray beginning at the first array position to be counted.

For a negative value, `parity ^= 1` flips the parity because one more negative element has been encountered. Positive values leave the parity unchanged. The actual magnitude of a nonzero value is never used.

The additions to `positive` and `negative` happen before incrementing `even` or `odd`. At that moment, those counters describe only prefixes strictly before the current element, which is exactly what the endpoint formula requires. Updating them first would introduce an invalid empty-length contribution.

When `x == 0`, the current nonzero segment ends. Resetting to `even = 1`, `odd = 0`, and `parity = 0` starts a new prefix sequence immediately after the zero. Subarrays containing the zero are intentionally excluded from the positive and negative counts.

The expression `n * (n + 1) // 2` counts every possible pair of endpoints. Python's arbitrary-precision integers make the potentially large answer safe without any special handling.

## Worked Examples

For Sample 1, the array is

```
5 -3 3 -1 0
```

The table records the prefix state after each processed element. `even` and `odd` are the prefix counts after the current position has been incorporated.

| Position | Value | Parity | Added Positive | Added Negative | Even | Odd | Positive | Negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Start |  | 0 |  |  | 1 | 0 | 0 | 0 |
| 1 | 5 | 0 | 1 | 0 | 2 | 0 | 1 | 0 |
| 2 | -3 | 1 | 0 | 2 | 2 | 1 | 1 | 2 |
| 3 | 3 | 1 | 1 | 2 | 2 | 2 | 2 | 4 |
| 4 | -1 | 0 | 2 | 2 | 3 | 2 | 4 | 6 |
| 5 | 0 | reset | 0 | 0 | 1 | 0 | 4 | 6 |

There are (5\cdot6/2=15) total subarrays. The scan finds (6) negative and (4) positive products, so (15-6-4=5) products are zero. The result is

```
6 5 4
```

The zero at position (5) demonstrates why the prefix counters must be reset. The first four elements form one independent nonzero segment, and every subarray reaching the zero belongs to the zero category rather than being classified by its sign parity.

For Sample 2, the array is

```
4 0 -4 3 1 2 -4 3 0 3
```

| Position | Value | Parity | Added Positive | Added Negative | Even | Odd | Positive | Negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Start |  | 0 |  |  | 1 | 0 | 0 | 0 |
| 1 | 4 | 0 | 1 | 0 | 2 | 0 | 1 | 0 |
| 2 | 0 | reset | 0 | 0 | 1 | 0 | 1 | 0 |
| 3 | -4 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |
| 4 | 3 | 1 | 1 | 1 | 1 | 2 | 2 | 2 |
| 5 | 1 | 1 | 2 | 1 | 1 | 3 | 4 | 3 |
| 6 | 2 | 1 | 3 | 1 | 1 | 4 | 7 | 4 |
| 7 | -4 | 0 | 1 | 4 | 2 | 4 | 8 | 8 |
| 8 | 3 | 0 | 2 | 4 | 3 | 4 | 10 | 12 |
| 9 | 0 | reset | 0 | 0 | 1 | 0 | 10 | 12 |
| 10 | 3 | 0 | 1 | 0 | 2 | 0 | 11 | 12 |

There are (10\cdot11/2=55) total subarrays. The scan gives (12) negative and (11) positive products, leaving (55-12-11=32) zero products. The result is

```
12 32 11
```

The trace also shows why the two zero positions are useful separators. The first positive element is counted independently, the six-element segment between the zeros is processed using its own prefix parity counts, and the final element starts another independent segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every array element is processed exactly once with constant-time operations. |
| Space | (O(1)) | Only a fixed number of counters and the current parity are maintained. |

With (n\le2\cdot10^5), a linear scan performs only a few operations per element, which is easily within the 2-second limit. The algorithm uses constant auxiliary space, and Python's integer representation safely handles answers as large as (20,000,100,000).

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    n = data[0]
    a = data[1:1 + n]

    even = 1
    odd = 0
    parity = 0

    negative = 0
    positive = 0

    for x in a:
        if x == 0:
            even = 1
            odd = 0
            parity = 0
            continue

        if x < 0:
            parity ^= 1

        if parity == 0:
            positive += even
            negative += odd
            even += 1
        else:
            positive += odd
            negative += even
            odd += 1

    total = n * (n + 1) // 2
    zero = total - positive - negative

    return f"{negative} {zero} {positive}"

def run(inp: str) -> str:
    return solve_data(inp)

# provided samples
assert run("5\n5 -3 3 -1 0\n") == "6 5 4", "sample 1"
assert run("10\n4 0 -4 3 1 2 -4 3 0 3\n") == "12 32 11", "sample 2"
assert run("5\n-1 -2 -3 -4 -5\n") == "9 0 6", "sample 3"

# minimum-size input
assert run("1\n0\n") == "0 1 0", "single zero"

# all equal positive values
assert run("3\n1 1 1\n") == "0 0 6", "all positive"

# all equal negative values
assert run("4\n-1 -1 -1 -1\n") == "6 0 4", "all negative"

# zeros at both boundaries
assert run("3\n0 1 0\n") == "0 5 1", "zeros at boundaries"

# zero splitting two nonzero segments
assert run("5\n1 -1 0 -1 1\n") == "2 11 2", "zero separator"

# maximum-size input
n = 200000
inp = f"{n}\n" + " ".join(["1"] * n) + "\n"
assert run(inp) == "0 0 20000100000", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0 1 0` | Minimum size and a single zero |
| `3 / 1 1 1` | `0 0 6` | All equal positive values |
| `4 / -1 -1 -1 -1` | `6 0 4` | Odd and even negative-count parity |
| `3 / 0 1 0` | `0 5 1` | Zeros at both boundaries |
| `5 / 1 -1 0 -1 1` | `2 11 2` | Resetting state around an internal zero |
| (n=200000), all `1` | `0 0 20000100000` | Maximum input size and large answer |

## Edge Cases

For a single zero, the input is

```
1
0
```

The initial state is `even = 1`, `odd = 0`. The zero triggers a reset, leaving the nonzero counts at zero. There is exactly one total subarray, so `zero = 1 - 0 - 0 = 1`. The output is `0 1 0`.

For all positive values,

```
3
1 1 1
```

the parity never changes. The first element pairs with the initial even prefix, the second pairs with two even prefixes, and the third pairs with three even prefixes. The positive count becomes (1+2+3=6), which is every subarray. The output is `0 0 6`.

For all negative values,

```
4
-1 -1 -1 -1
```

the parity alternates between odd and even. The negative count receives (1), (2), (1), and (2) contributions, totaling (6). The positive count receives (1), (0), (2), and (1) contributions, totaling (4). There are no zeros, so the result is `6 0 4`.

For zeros at both boundaries,

```
3
0 1 0
```

the first zero resets the state before any nonzero subarray is counted. The `1` then creates exactly one positive subarray. The final zero resets the state again. Since there are six total subarrays and only one is nonzero, the zero count is (5). The output is `0 5 1`.

For an internal zero,

```
5
1 -1 0 -1 1
```

the first segment `[1,-1]` contributes one positive and one negative subarray. The zero prevents any subarray crossing position (3) from entering either nonzero category. The second segment `[-1,1]` contributes the same counts. Thus there are (2) positive and (2) negative subarrays. With (15) total subarrays, the remaining (11) have product zero, giving `2 11 2`.

For the maximum-size positive array, all (200000) elements can be `1`. The parity remains even throughout, and the positive count becomes

# \frac{200000\cdot200001}{2}

20000100000.
]

No negative or zero product exists, so the output is `0 0 20000100000`. This confirms both the linear running time and the need for an integer type capable of storing the full number of subarrays.
