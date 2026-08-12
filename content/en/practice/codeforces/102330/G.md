---
title: "CF 102330G - \u0421\u0430\u0448\u0430 \u0438 \u0441\u0442\u0430\u0436\u0438\u0440\u043e\u0432\u043a\u0438"
description: "We are given a task number written as a sequence of decimal digits. A split chooses several cut positions between digits, so every resulting piece is interpreted as a separate task number."
date: "2026-08-13T04:06:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102330
codeforces_index: "G"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2019.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102330
solve_time_s: 80
verified: true
draft: false
---

[CF 102330G - \u0421\u0430\u0448\u0430 \u0438 \u0441\u0442\u0430\u0436\u0438\u0440\u043e\u0432\u043a\u0438](https://codeforces.com/problemset/problem/102330/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a task number written as a sequence of decimal digits. A split chooses several cut positions between digits, so every resulting piece is interpreted as a separate task number. A valid piece must satisfy two conditions: its decimal representation has at most `k` digits, and its numeric value is prime. Leading zeroes are forbidden, so a piece such as `03` is invalid even though its numeric value would be 3.

The goal is to count every possible way to place the cuts so that all resulting pieces are valid. Different cut positions produce different decompositions, even when some pieces have the same numeric value. The answer is printed modulo `10^9 + 7`.

The input bound `|n| <= 10^6` is unusually restrictive for a digit-partition problem. The absolute value has at most seven decimal digits, while `k <= 6`. That means there are at most six possible cut positions and consequently at most `2^6 = 64` complete partitions. A brute-force solution is already small enough for these constraints. Still, the same recurrence can be written as a dynamic program that avoids recalculating the same prefix states and scales much better if the digit length were increased.

The absolute value is used when constructing the digit string. The minus sign is not a digit and cannot participate in a decimal task number, so the meaningful representation for splitting is the sequence of digits of `|n|`.

There are several small cases where a careless implementation can fail. For input `2` with `k = 1`, the answer is `1`, because the whole task number is the prime 2. An implementation that starts its primality test from 2 and accidentally requires a divisor can reject this case.

For input `11` with `k = 1`, the answer is `0`. Each one-digit piece is `1`, which is not prime. A solution that treats every digit except zero as a possible prime would incorrectly return `1`.

For input `103` with `k = 2`, the answer is `0`. The only possible two-digit prefixes are `10`, while the remaining digit is `3`; `10` is not prime. The alternative `1|03` is forbidden because `03` has a leading zero. A solution that converts every substring directly to an integer before checking it would silently accept this invalid representation.

For input `23` with `k = 2`, the answer is `2`. Both `23` itself and `2|3` are valid. A solution that only considers pieces of exactly length `k`, or forgets that a shorter final piece is allowed, misses one of these decompositions.

## Approaches

The direct approach is to enumerate every possible set of cuts. With `L` digits there are `L - 1` gaps, and every gap can either contain a cut or not, giving `2^(L-1)` partitions. For every partition we check each produced piece, reject pieces longer than `k`, reject leading zeroes, and test the remaining values for primality. This is correct because every possible decomposition corresponds to exactly one subset of the gaps, so enumeration neither misses nor duplicates a decomposition.

Under the actual constraint `L <= 7`, this brute force never becomes too slow. There are at most 64 complete partitions, and each partition has at most seven pieces, so there are at most 448 piece checks. Since every checked number has at most six digits, trial division needs fewer than 1000 divisor tests per piece. The resulting worst-case upper bound is roughly 448,000 elementary divisor checks, which is easily manageable. Thus the brute-force method is already accepted for this problem.

The more reusable approach is to observe that a decomposition can be built from left to right. Suppose the first `i` digits have already been split into valid prime pieces. We only need to decide which valid piece comes next. There are at most `k` possible lengths for that next piece, so we can transition from position `i` to positions `i + 1` through `i + k`. This gives a one-dimensional dynamic program.

Let `dp[i]` be the number of valid decompositions of the first `i` digits. Initially `dp[0] = 1`, representing the empty prefix. For every reachable position `i`, we take the next one, two, up to `k` digits. If the resulting substring has no leading zero and represents a prime number, it contributes `dp[i]` ways to `dp[j]`, where `j` is the position immediately after that substring.

The brute-force method works because the number of cut positions is tiny, but it repeatedly explores the same valid prefixes. The observation that every decomposition is a sequence of valid transitions between digit positions lets us merge all those repeated prefixes into a single DP state.

Primality testing does not need a large sieve here. There are at most `7 * 6 = 42` different substring candidates considered by the DP, and every candidate has at most six digits. Trial division up to the square root is more than fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^L * L * sqrt(10^k))` | `O(L)` | Accepted for `L <= 7` |
| Optimal | `O(L * k * sqrt(10^k))` | `O(L)` | Accepted |

Here `L` is the number of digits in `|n|`. The DP is preferable because its structure remains useful if the input length is increased, while the implementation is still very small.

## Algorithm Walkthrough

1. Read `n` and `k`, and convert `abs(n)` to a string `s`. The string representation is needed because splitting is performed between decimal digits, not according to numeric arithmetic.
2. Define a primality test for positive integers. Values smaller than 2 are rejected. For a value at least 2, test divisibility by integers up to its square root. If no divisor is found, the value is prime.
3. Create an array `dp` of length `len(s) + 1` and set `dp[0] = 1`. The state `dp[i]` means that the first `i` digits can already be completely divided into valid pieces in `dp[i]` different ways.
4. Process positions from left to right. If `dp[i]` is zero, there is no valid decomposition reaching this position, so there is nothing to extend from it.
5. From position `i`, try every piece length from 1 through `k`, stopping at the end of the string. This covers every possible next piece allowed by the maximum-length restriction.
6. Reject a candidate immediately when its first digit is `0`. Such a substring would have a leading zero and cannot represent a valid task number.
7. Convert the candidate substring to an integer and test whether it is prime. If it is prime, add `dp[i]` to the state corresponding to the end of the candidate. This transition means that every valid decomposition of the prefix can be extended by this particular prime piece.
8. After all positions have been processed, return `dp[len(s)]`. This state counts exactly the decompositions that consume every digit, so no unfinished prefix is included in the answer.

### Why it works

The invariant is that after processing position `i`, `dp[i]` contains exactly the number of valid decompositions of the first `i` digits. Every such decomposition has a unique final piece. Removing that final piece leaves a valid decomposition of some earlier position `j`, and the removed piece is precisely one of the substrings considered by the transition from `j` to `i`. Conversely, every transition accepted by the algorithm appends a valid prime piece to an already valid decomposition. Thus every counted decomposition is valid, and every valid decomposition is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def is_prime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False

    d = 3
    while d * d <= x:
        if x % d == 0:
            return False
        d += 2
    return True

def solve():
    n = int(input())
    k = int(input())

    s = str(abs(n))
    m = len(s)

    dp = [0] * (m + 1)
    dp[0] = 1

    for i in range(m):
        if dp[i] == 0:
            continue

        value = 0

        for length in range(1, k + 1):
            j = i + length
            if j > m:
                break

            if length > 1 and s[i] == '0':
                break

            value = value * 10 + (ord(s[j - 1]) - ord('0'))

            if is_prime(value):
                dp[j] = (dp[j] + dp[i]) % MOD

    print(dp[m])

if __name__ == "__main__":
    solve()
```

The `is_prime` function handles `0` and `1` before testing divisibility, and treats `2` separately so that the even-number shortcut does not reject the smallest prime. After that, only odd divisors need to be considered.

The DP uses `dp[0] = 1` as the empty-prefix base case. Without this value, a valid first piece would have no state from which to receive its contribution.

The candidate value is constructed incrementally rather than repeatedly converting substrings. For example, while extending from position `i`, the values `3`, `37`, and `377` are obtained successively. This is both simpler for the transition loop and avoids unnecessary string slicing.

The leading-zero check is deliberately performed before accepting a multi-digit candidate. A one-digit `0` is also rejected naturally by `is_prime`, so `0` does not need a separate special case. If `s[i] == '0'`, no longer substring starting there can be valid, because every longer substring would still have that leading zero. That is why the loop can stop immediately.

The longest candidate has at most six digits, so `value` is at most `999999`. Python integers have no overflow concern here, and the modulo operation on every DP transition follows the required output convention even though the actual number of decompositions is at most 64 for this problem.

## Worked Examples

For the provided sample, the input is `37735` with `k = 2`. The DP can choose one or two digits at every position, subject to primality.

| Position `i` | `dp[i]` | Candidate | Prime? | Updated state |
| --- | --- | --- | --- | --- |
| 0 | 1 | `3` | Yes | `dp[1] += 1` |
| 0 | 1 | `37` | Yes | `dp[2] += 1` |
| 1 | 1 | `7` | Yes | `dp[2] += 1` |
| 1 | 1 | `77` | No | none |
| 2 | 2 | `7` | Yes | `dp[3] += 2` |
| 2 | 2 | `73` | Yes | `dp[4] += 2` |
| 3 | 2 | `3` | Yes | `dp[4] += 2` |
| 3 | 2 | `35` | No | none |
| 4 | 4 | `5` | Yes | `dp[5] += 4` |

The final value is `dp[5] = 4`. These four paths correspond to `3|7|7|3|5`, `37|7|3|5`, `37|73|5`, and `3|7|73|5`. The trace shows why multiple ways can reach the same position and why those ways must be accumulated rather than replaced.

For a second example, consider `23` with `k = 2`.

| Position `i` | `dp[i]` | Candidate | Prime? | Updated state |
| --- | --- | --- | --- | --- |
| 0 | 1 | `2` | Yes | `dp[1] = 1` |
| 0 | 1 | `23` | Yes | `dp[2] = 1` |
| 1 | 1 | `3` | Yes | `dp[2] = 2` |

The answer is `2`, representing `2|3` and `23`. The example demonstrates that the transition must consider every length from 1 through `k`, including the case where the entire remaining suffix forms one prime piece.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(L * k * sqrt(10^k))` | At most `k` candidate pieces are tested from each of `L` positions, and primality testing takes square-root time |
| Space | `O(L)` | The DP array contains one state for each digit position |

Here `L <= 7` and `k <= 6`. Even the loose bound gives only 42 primality tests, with each test involving at most about 500 odd divisors for a six-digit number. The algorithm is comfortably within the one-second and 256 MB limits.

## Test Cases

```python
import sys
import io

MOD = 1_000_000_007

def is_prime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False

    d = 3
    while d * d <= x:
        if x % d == 0:
            return False
        d += 2
    return True

def solution(inp):
    data = inp.split()
    n = int(data[0])
    k = int(data[1])

    s = str(abs(n))
    m = len(s)

    dp = [0] * (m + 1)
    dp[0] = 1

    for i in range(m):
        if dp[i] == 0:
            continue

        value = 0

        for length in range(1, k + 1):
            j = i + length
            if j > m:
                break

            if length > 1 and s[i] == '0':
                break

            value = value * 10 + int(s[j - 1])

            if is_prime(value):
                dp[j] = (dp[j] + dp[i]) % MOD

    return str(dp[m])

def run(inp: str) -> str:
    return solution(inp).strip()

# Provided sample
assert run("37735\n2\n") == "4", "provided sample"

# Minimum-size prime task number
assert run("2\n1\n") == "1", "single-digit prime"

# All equal digits, every digit is prime but every two-digit block is composite
assert run("777777\n2\n") == "1", "all-equal values"

# Both the whole number and the one-digit split are valid
assert run("23\n2\n") == "2", "boundary on k"

# Leading zero must not be accepted as a multi-digit prime
assert run("103\n2\n") == "0", "leading zero"

# Maximum absolute value allowed by the statement
assert run("1000000\n6\n") == "0", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1` | `1` | Smallest possible prime and the `2` primality boundary |
| `777777 / 2` | `1` | Repeated digits and distinction between `7` and composite `77` |
| `23 / 2` | `2` | Both a one-digit split and the maximum allowed piece length |
| `103 / 2` | `0` | Leading-zero rejection and composite multi-digit pieces |
| `1000000 / 6` | `0` | Maximum allowed absolute input and many zero-containing candidates |

## Edge Cases

For `2` with `k = 1`, the DP starts with `dp[0] = 1`. It forms the candidate `2`, and `is_prime(2)` returns true, so `dp[1]` becomes 1. The final answer is `1`. The special handling of 2 in the primality test prevents an incorrect rejection as an even number.

For `11` with `k = 1`, the only candidates are the two individual digits `1` and `1`. Both fail the `x < 2` condition in `is_prime`, so no transition reaches position 1 or position 2. The final answer is `0`.

For `103` with `k = 2`, the first position allows `1` and `10`, neither of which is prime. The transition from position 1 would start at digit `0`, but because it is a multi-digit candidate, the leading-zero check stops the loop immediately. The complete number cannot be used because its length is three while `k = 2`. The answer is consequently `0`.

For `23` with `k = 2`, the first position produces both `2` and `23`. The first transition gives `dp[1] = 1`, while the second gives `dp[2] = 1`. From position 1, the remaining `3` is prime, so another way reaches `dp[2]`. The final state contains `2`, exactly matching the two valid decompositions.

For `1000000` with `k = 6`, every candidate beginning at the first digit is either `1`, `10`, `100`, and so on. Only `1` could be a prefix of a valid decomposition, but it is not prime. Once the DP reaches a zero digit there is no valid multi-digit piece beginning there, and zero itself is not prime. No transition reaches the final position, so the answer is `0`.
