---
title: "CF 897B - Chtholly's request"
description: "We are asked to list special numbers in increasing order and take a prefix sum. A number is considered valid if it reads the same forward and backward in decimal notation and its length is even."
date: "2026-06-17T03:35:48+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 897
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 449 (Div. 2)"
rating: 1300
weight: 897
solve_time_s: 67
verified: true
draft: false
---

[CF 897B - Chtholly's request](https://codeforces.com/problemset/problem/897/B)

**Rating:** 1300  
**Tags:** brute force  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to list special numbers in increasing order and take a prefix sum.

A number is considered valid if it reads the same forward and backward in decimal notation and its length is even. This means every valid number is fully determined by its first half, because the second half is just a mirror of the first. We then take the smallest such valid numbers, add the smallest k of them, and finally output the sum modulo p.

The input gives k, the number of such smallest palindromes we need, and p, the modulus applied to the final sum. The task is not to find a single palindrome or check membership, but to generate the ordered sequence of all even-length palindromes and aggregate the first k terms.

The constraint k up to 100000 changes the problem structure significantly. A direct approach that checks every integer and tests whether it is a palindrome would be far too slow, since palindromes become sparse as numbers grow and scanning integers up to the k-th valid one could easily exceed billions of checks. Instead, we must exploit the construction of palindromes directly.

A subtle pitfall is assuming that palindromes should be generated in numeric order by brute force enumeration. That fails because most integers are not palindromes, and skipping invalid numbers still costs time proportional to the search space. Another issue is accidentally including odd-length palindromes like 12321, which are explicitly invalid even though they are palindromic. A third common mistake is forgetting that leading zeros are not allowed, which affects how we interpret the "half" representation.

## Approaches

A naive method would iterate over all integers starting from 1, check whether each is a palindrome, check whether its digit length is even, and collect those that satisfy both conditions until k are found. This is correct but extremely inefficient. In the worst case, to find 100000 valid even-length palindromes, we would need to scan far beyond 10^9 integers, since valid palindromes become less frequent as numbers grow. Each palindrome check costs O(d), where d is number of digits, so the total complexity becomes unacceptably large.

The key observation is that every even-length palindrome is uniquely determined by its first half. If we choose a number x, we can construct a palindrome by appending the reverse of x to itself. This transforms the problem into generating all positive integers grouped by digit length of their half representation.

The ordering is also structured. All 2-digit palindromes come first, then all 4-digit palindromes, then 6-digit ones, and so on. Within a fixed length group, ordering of palindromes follows the natural ordering of their first halves.

This allows us to construct the sequence directly, layer by layer, without ever checking non-palindromes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration | O(N · d) | O(1) | Too slow |
| Construct from half numbers | O(k · d) | O(1) | Accepted |

## Algorithm Walkthrough

1. We iterate over possible half-lengths starting from 1-digit halves upward. Each half-length m corresponds to palindromes of length 2m. This ordering is necessary because smaller lengths always produce smaller numbers.
2. For each half-length m, we generate all valid half numbers in increasing order. For m = 1, this is 1 to 9. For m ≥ 2, this is from 10^(m−1) to 10^m − 1. This ensures no leading zeros appear in the constructed palindromes.
3. For each half number, we construct the full even-length palindrome by concatenating the number with its reverse in decimal form. This guarantees correctness of the palindrome property.
4. We maintain a running list (or running sum) of generated palindromes. Each time we produce a palindrome, we add it to the sum modulo p.
5. We stop immediately once we have generated k palindromes. There is no need to generate further lengths once the requirement is satisfied.

The core idea behind correctness is that this generation process enumerates every valid even-length palindrome exactly once, and in strictly increasing order.

### Why it works

Each valid number is uniquely determined by its first half, so there is a bijection between valid palindromes of length 2m and integers in the range [10^(m−1), 10^m − 1] (or [1, 9] for m = 1). Since these ranges are traversed in increasing order of m and within each range in increasing numeric order, the resulting sequence is globally sorted. This guarantees that taking the first k elements of this construction is equivalent to taking the k smallest valid palindromes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def make_pal(x: int) -> int:
    s = str(x)
    return int(s + s[::-1])

k, p = map(int, input().split())

res = 0
cnt = 0
m = 1

while cnt < k:
    if m == 1:
        start, end = 1, 9
    else:
        start = 10 ** (m - 1)
        end = 10 ** m - 1

    x = start
    while x <= end and cnt < k:
        pal = make_pal(x)
        res = (res + pal) % p
        cnt += 1
        x += 1

    m += 1

print(res)
```

The solution constructs palindromes directly from their half representation. The helper function converts a number into its even-length palindrome by string reversal, which is safe here because k is at most 100000, so total string operations remain small.

The outer loop controls the digit length of the half. The inner loop enumerates all valid halves for that length. The early stopping condition ensures we never generate unnecessary palindromes once k are collected.

A common implementation mistake is forgetting to separate the m = 1 case, where the first half cannot start from 0. Another subtle issue is integer overflow, but Python naturally handles large integers, and modulo reduction prevents unbounded growth.

## Worked Examples

### Example 1

Input:

```
2 100
```

We generate even-length palindromes.

| Step | m (half length) | x (half) | palindrome | cumulative sum |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 11 | 11 |
| 2 | 1 | 2 | 22 | 33 |

We stop after 2 values.

Output:

```
33
```

This trace shows that the first layer alone already provides at least k values when k is small, and ordering is strictly increasing.

### Example 2

Input:

```
10 1000
```

We list more values:

| Step | m | x | palindrome | sum |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 11 | 11 |
| 2 | 1 | 2 | 22 | 33 |
| ... | 1 | 9 | 99 | 495 |
| 10 | 2 | 10 | 1001 | 1496 |

After 9 numbers from m = 1, we continue into m = 2.

This demonstrates how the sequence transitions between digit lengths while preserving ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · d) | Each palindrome is built from a half number and reversed once, with digit length d ≤ 5 for k ≤ 1e5 |
| Space | O(1) | Only counters and running sum are stored |

The constraints allow direct construction because k is only 100000, and each operation is cheap. Even with string reversal overhead, the total work stays well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def make_pal(x: int) -> int:
        s = str(x)
        return int(s + s[::-1])

    k, p = map(int, input().split())
    res = 0
    cnt = 0
    m = 1

    while cnt < k:
        if m == 1:
            start, end = 1, 9
        else:
            start = 10 ** (m - 1)
            end = 10 ** m - 1

        x = start
        while x <= end and cnt < k:
            res = (res + make_pal(x)) % p
            cnt += 1
            x += 1
        m += 1

    return str(res)

# provided sample
assert run("2 100\n") == "33"

# custom cases
assert run("1 100\n") == "11"
assert run("3 100\n") == "66"
assert run("10 1000\n") == str((11+22+33+44+55+66+77+88+99+1001)%1000)
assert run("5 7\n") == str((11+22+33+44+55)%7)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 100 | 11 | smallest valid palindrome |
| 3 100 | 66 | early prefix correctness |
| 10 1000 | computed | transition to next digit length |
| 5 7 | mod behavior | modular accumulation |

## Edge Cases

A key edge case is when k is small enough that only 1-digit halves are needed. For input like k = 1, the algorithm must not attempt to generate higher digit lengths at all. The loop structure naturally handles this because it stops immediately once cnt reaches k.

Another edge case is when k spans multiple digit-length layers. For example, k = 10 forces the algorithm to exhaust all 1-digit halves (9 values) and then begin 2-digit halves. The layered construction ensures that ordering remains correct across this boundary because all 1-digit palindromes are strictly smaller than all 4-digit palindromes.

Finally, modulo p = 1 is degenerate since all outputs become zero. The running modulo update handles this safely without special casing.
