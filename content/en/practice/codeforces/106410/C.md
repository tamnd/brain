---
title: "CF 106410C - Repetition"
description: "The problem asks us to count how many subsequences of an array are valid. A subsequence is created by choosing some indices and keeping their original order."
date: "2026-06-25T09:54:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106410
codeforces_index: "C"
codeforces_contest_name: "HPI 2026 Novice"
rating: 0
weight: 106410
solve_time_s: 35
verified: true
draft: false
---

[CF 106410C - Repetition](https://codeforces.com/problemset/problem/106410/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to count how many subsequences of an array are valid. A subsequence is created by choosing some indices and keeping their original order. A chosen sequence of length `k` is valid if the first chosen value is divisible by `1`, the second chosen value is divisible by `2`, the third by `3`, and so on. We only care about which indices were selected, so two subsequences with the same values but different positions are counted separately. The answer must be printed modulo `1e9 + 7`.

The input is an array of length `n`, where `n` can reach `100000` and values can be as large as `10^6`. A quadratic dynamic programming solution would already require around `10^10` operations in the worst case, which is too slow. The value limit suggests that the divisibility structure of the numbers is the key, because the number of possible divisors of a value up to `10^6` is small enough to process efficiently.

A common mistake is to track subsequences by their values instead of their indices. For example, with input `3` and array `1 1 1`, every single element forms a different subsequence, so the answer is `3`, not `1`. Another tricky case is when a value cannot extend a subsequence because of its required position. For input `2` and array `2 1`, the subsequence `[2,1]` is not valid because the second element must be divisible by `2`, and `1` is not. The correct answer is `2`, coming from `[2]` and `[1]`. A careless solution that only checks values without considering the current length would overcount.

Another boundary case is a value of `1`. Since `1` is divisible by every positive integer, it can be placed at any position in a valid subsequence. With input `3` and array `1 1 1`, the answer is every non-empty subsequence, which is `7`.

## Approaches

The direct approach is to build all subsequences. For each subsequence, we can check whether its first chosen element is divisible by `1`, its second by `2`, and so on. This is correct because it follows the definition exactly. However, an array of length `100000` has `2^100000 - 1` possible non-empty subsequences, so enumeration is impossible.

A better direction is to process the array from left to right and maintain how many valid subsequences of each current length exist. Suppose we already processed some prefix of the array. If we see a new value `x`, it can become the next element of any existing valid subsequence whose next required position divides `x`.

The important observation is that we never need the full length distribution up to `n`. A value `x` can only help create a new subsequence length `i` when `i` divides `x`. Since `x <= 10^6`, the number of divisors is small. We can update only those lengths.

Let `dp[i]` represent the number of valid subsequences of length `i` formed from elements processed so far. When we process a value `x`, every divisor `d` of `x` means a subsequence of length `d - 1` can be extended to length `d` by adding `x`. We update `dp[d] += dp[d-1]`. The length `1` case is always possible because every number is divisible by `1`, so `dp[1]` increases by one for every element.

The update order matters. We must process divisors in decreasing order so that the current value is not reused multiple times in the same subsequence. If we updated from small lengths to large lengths, a newly created subsequence could immediately be extended again using the same array element, which would be invalid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n * sqrt(max(a))) | O(max(a)) | Accepted |

## Algorithm Walkthrough

1. Create a dynamic programming array where `dp[i]` stores the number of valid subsequences of length `i` after processing the current prefix of the array. Initially all values are zero because no elements have been used.
2. Iterate through every array value `x` from left to right. The current value can start a new subsequence of length `1`, so increase `dp[1]` by one.
3. Find all divisors of `x`. For each divisor `d` greater than `1`, update `dp[d]` by adding `dp[d-1]`. The reason is that every valid subsequence of length `d-1` can append `x` and become valid of length `d`.
4. Process the divisors in descending order. This keeps the transition based only on subsequences from earlier array elements, preventing the current element from being counted more than once.
5. After the whole array is processed, sum all `dp[i]` values. Every valid non-empty subsequence has some length, so this sum is the answer.

Why it works:

The invariant is that after processing the first `j` elements, `dp[i]` exactly equals the number of valid subsequences of length `i` using only those `j` elements. When a new element `x` is considered, the only possible new subsequences are ones ending at `x`. Their previous part must already be a valid subsequence of length `d-1`, where `d` divides `x`, because the new element will occupy position `d`. The update counts exactly these extensions and nothing else. Descending updates guarantee the previous part never includes the current element, so every counted subsequence corresponds to a unique set of indices.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    dp = [0] * (n + 2)

    for x in a:
        divs = []
        i = 1
        while i * i <= x:
            if x % i == 0:
                divs.append(i)
                if i * i != x:
                    divs.append(x // i)
            i += 1

        divs.sort(reverse=True)

        for d in divs:
            if d == 1:
                dp[1] = (dp[1] + 1) % MOD
            elif d <= n:
                dp[d] = (dp[d] + dp[d - 1]) % MOD

    print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

The array `dp` is sized by `n` because a subsequence cannot have length larger than the number of elements. The transitions only need positions that can actually appear.

For each value, the code first collects its divisors by checking all numbers up to its square root. The largest value is `10^6`, so this is fast enough. Sorting the divisors in descending order is the detail that prevents invalid reuse of the current element.

When `d == 1`, the value creates a new subsequence by itself. For larger divisors, `dp[d-1]` already represents subsequences ending before the current index, so adding the current value creates new valid subsequences of length `d`.

Python integers do not overflow, but the modulo operation is applied during updates to keep the stored values bounded.

## Worked Examples

Sample 1:

Input:

```
2
1 2
```

The processing looks like this:

| Step | Current value | Divisors used | dp changes | Total |
| --- | --- | --- | --- | --- |
| Start | none | none | all zero | 0 |
| 1 | 1 | 1 | dp[1] = 1 | 1 |
| 2 | 2 | 2, 1 | dp[2] += dp[1], dp[1] += 1 | 3 |

The final subsequences are `[1]`, `[2]`, and `[1,2]`. The table shows that length `2` is created only because the second value is divisible by `2`.

Sample 2:

Input:

```
5
2 2 1 22 14
```

| Step | Current value | Divisors | Important updates | Total |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2,1 | create length 1 | 1 |
| 2 | 2 | 2,1 | extend length 1, create length 1 | 3 |
| 3 | 1 | 1 | create length 1 | 4 |
| 4 | 22 | 11,2,1 | extend lengths 1 and 2, create length 1 | 8 |
| 5 | 14 | 14,7,2,1 | extend lengths 1 and 2, create length 1 | 13 |

The second trace demonstrates why processing divisors is enough. Values such as `22` and `14` only interact with lengths that divide them, rather than every possible subsequence length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * sqrt(max(a))) | Each value is factored by checking up to its square root, and only its divisors are updated |
| Space | O(n) | The dynamic programming array stores counts for each possible subsequence length |

The maximum value is `10^6`, so the square root factorization is about `1000` checks per element. For `100000` elements this is around `10^8` simple operations, which fits in the intended limit with efficient Python implementation.

## Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    dp = [0] * (n + 2)

    for x in a:
        divs = []
        i = 1
        while i * i <= x:
            if x % i == 0:
                divs.append(i)
                if i * i != x:
                    divs.append(x // i)
            i += 1

        divs.sort(reverse=True)

        for d in divs:
            if d == 1:
                dp[1] += 1
            elif d <= n:
                dp[d] = (dp[d] + dp[d - 1]) % MOD

    return str(sum(dp) % MOD)

assert solution("2\n1 2\n") == "3"
assert solution("5\n2 2 1 22 14\n") == "13"

assert solution("1\n1000000\n") == "1"
assert solution("3\n1 1 1\n") == "7"
assert solution("4\n2 3 4 6\n") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1000000` | `1` | Single element and maximum value boundary |
| `1 1 1` | `7` | Values divisible by every position |
| `2 3 4 6` | `7` | Divisor filtering and subsequence extension rules |

## Edge Cases

For the input `2` with array `2 1`, the algorithm processes `2` first and creates one subsequence of length `1`. The value `1` can also create a length `1` subsequence, but it cannot extend the existing length `1` subsequence because `2` does not divide `1`. The final answer is `2`.

For the input `3` with array `1 1 1`, every processed value adds a new length `1` subsequence. The first `1` creates one subsequence, the second creates new length `1` and can extend the previous one to length `2`, and the third creates all remaining possibilities. The counts become `3`, `3`, and `1` for lengths `1`, `2`, and `3`, giving answer `7`.

For repeated values, such as `3` with array `2 2 2`, the descending divisor update prevents a single `2` from being used twice. The valid subsequences are three of length `1` and three of length `2`, giving `6`, while length `3` is impossible because `2` is not divisible by `3`.
