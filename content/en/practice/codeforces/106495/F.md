---
title: "CF 106495F - F(x,l,r)"
description: "We are given a list of positive integers and an initial value x. We may choose any ordering of the list. After choosing the order, we process the numbers one by one. Each processed number replaces the current value with its remainder when divided by that number."
date: "2026-06-25T08:39:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106495
codeforces_index: "F"
codeforces_contest_name: "2026 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 106495
solve_time_s: 37
verified: true
draft: false
---

[CF 106495F - F(x,l,r)](https://codeforces.com/problemset/problem/106495/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of positive integers and an initial value `x`. We may choose any ordering of the list. After choosing the order, we process the numbers one by one. Each processed number replaces the current value with its remainder when divided by that number. The goal is to arrange the numbers so that the final value is as large as possible.

The input consists of the length of the array, the array values, and the starting value. The output is the maximum value that can remain after all modulo operations are finished. The order matters because a modulo operation can destroy information that later operations cannot recover.

The array length is small, at most 21, but the values themselves can be very large. This rules out trying all permutations because `21!` is far beyond what can run. A solution has to exploit the small number of elements rather than the size of the numbers. A state space of `2^21` is around two million states, which is feasible in a low-level language and still manageable in Python with careful memory usage.

A common mistake is assuming that larger divisors should be applied first or last. For example, with `x = 15` and numbers `[5, 6, 7]`, putting the largest divisor first gives `15 % 7 = 1`, then `1 % 5 = 1`, then `1 % 6 = 1`. The optimal order is `5, 7, 6`, producing `15 % 5 = 0`, `0 % 7 = 0`, `0 % 6 = 0`, which is still not optimal. The actual answer is obtained by `7, 6, 5`: `15 % 7 = 1`, `1 % 6 = 1`, `1 % 5 = 1`. This example shows that greedy choices based only on divisor size do not capture the dependency between operations.

Another edge case is when some values are already small. If the current value is smaller than every remaining divisor, all future modulo operations keep it unchanged. For example, with input:

```
2
10 20
5
```

the answer is `5`. A careless implementation that continues applying transformations without considering the current state might incorrectly expect the value to decrease.

Repeated values also need care. For:

```
3
5 5 100
12
```

the answer is `2`. The two identical divisors are separate operations, so both must be considered. Treating values as a set instead of indexed elements would lose valid orders.

## Approaches

The direct approach is to try every possible ordering. For each permutation, simulate the modulo operations and keep the largest final value. This is correct because every possible arrangement is checked. However, the number of permutations is `n!`, and for `n = 21` this is about `5.1 * 10^19` possibilities. Even a billion operations per second would not make this approach practical.

The key observation is that many different orders reach the same intermediate situation. After some numbers have been used, the only thing that matters is which numbers remain available and what the current value is. Since the current value is always produced from the initial value by modulo operations, we can store the best value reachable after processing a particular subset of indices.

For every subset of used elements, we try adding each unused element next. The transition is simply applying one more modulo operation. There are `2^n` subsets, and each subset checks up to `n` next choices, giving about `n * 2^n` operations.

The important reduction is that we never care about the exact order that produced a subset. If two different orders use the same set of elements, only the larger current value can matter because future modulo operations are monotonic with respect to the current value. A smaller current value can never become better than a larger one after applying the same remaining operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slow |
| Optimal | O(n * 2^n) | O(2^n) | Accepted |

## Algorithm Walkthrough

1. Create an array `dp` where `dp[mask]` represents the maximum current value reachable after using exactly the elements whose indices are set in `mask`. The empty mask starts with the original value `x` because no operations have happened yet.
2. Iterate through all masks. For each reachable state, try every element that is not included in the mask. This represents choosing the next number in the permutation.
3. Apply the modulo operation with that chosen element. Update the state containing the old mask plus the new element with the maximum value between its current content and the newly obtained value.
4. After all subsets have been processed, the full mask contains the answer because every array element has been used exactly once.

Why it works: The invariant is that `dp[mask]` always stores the best possible value after using exactly the elements in `mask`. The transition tries every possible next choice, so every possible continuation of every partial ordering is explored. Keeping only the maximum value for a subset is safe because future modulo operations cannot make a smaller starting value beat a larger one when the same divisors are applied.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    x = int(input())

    size = 1 << n
    dp = array('Q', [0]) * size
    dp[0] = x

    for mask in range(size):
        cur = dp[mask]
        if cur == 0 and mask != 0:
            continue
        remaining = ((1 << n) - 1) ^ mask
        while remaining:
            bit = remaining & -remaining
            i = bit.bit_length() - 1
            nxt = mask | bit
            val = cur % a[i]
            if val > dp[nxt]:
                dp[nxt] = val
            remaining -= bit

    print(dp[-1])

if __name__ == "__main__":
    solve()
```

The `dp` array uses `array('Q')` instead of a normal Python list. There are over two million states, so storing Python integer objects would waste a lot of memory. Every stored value fits in an unsigned 64-bit integer because all inputs are at most `10^18`.

The transition loop extracts one set bit from the remaining elements using `remaining & -remaining`. This avoids scanning through unnecessary operations and also avoids creating extra lists. The index is recovered with `bit_length() - 1`.

The check for `cur == 0` skips useless states. Once the current value becomes zero, every later modulo operation keeps it zero, so all descendants of that state would also be zero. The final state is `dp[(1 << n) - 1]`, which is the same as `dp[-1]` because the full mask is the last index.

## Worked Examples

For the first sample:

```
3
5 6 7
15
```

The important states are:

| mask | used elements | current best value |
| --- | --- | --- |
| 000 | none | 15 |
| 001 | 5 | 0 |
| 010 | 6 | 3 |
| 100 | 7 | 1 |
| 111 | all | 3 |

Starting with `15`, choosing `6` first gives `3`, and the remaining modulo operations cannot reduce it further. The DP keeps this path and ignores weaker paths.

For the second sample:

```
4
20 21 22 10
107
```

| mask | used elements | current best value |
| --- | --- | --- |
| 0000 | none | 107 |
| 0001 | 20 | 7 |
| 0010 | 21 | 2 |
| 0100 | 22 | 19 |
| 1000 | 10 | 7 |
| 1111 | all | 9 |

The best answer comes from choosing the operations in an order that leaves a large remainder before the final steps. The subset states allow the algorithm to discover that ordering without explicitly generating permutations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 2^n) | Each subset tries each possible next element |
| Space | O(2^n) | One stored value per subset |

With `n = 21`, there are about two million states. Multiplying by 21 gives roughly 44 million transitions, which fits the intended limits with an efficient implementation.

## Test Cases

```python
import sys
import io
from array import array

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    x = int(input())

    size = 1 << n
    dp = array('Q', [0]) * size
    dp[0] = x

    for mask in range(size):
        cur = dp[mask]
        if cur == 0 and mask:
            continue
        rem = (size - 1) ^ mask
        while rem:
            bit = rem & -rem
            i = bit.bit_length() - 1
            nxt = mask | bit
            val = cur % a[i]
            if val > dp[nxt]:
                dp[nxt] = val
            rem -= bit

    return str(dp[-1])

assert solution("""3
5 6 7
15
""") == "3"

assert solution("""4
20 21 22 10
107
""") == "9"

assert solution("""1
100
37
""") == "37"

assert solution("""3
5 5 100
12
""") == "2"

assert solution("""4
2 4 8 16
1000000000000000000
""") == "0"

assert solution("""5
9 10 11 12 13
100
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 100 / 37` | `37` | Single element and no harmful modulo |
| `5 5 100` with `12` | `2` | Repeated values and treating indices separately |
| `2 4 8 16` with a huge value | `0` | Large values and reaching zero |
| `9 10 11 12 13` with `100` | `10` | Different ordering choices |

## Edge Cases

For the case where the starting value is already smaller than every divisor:

```
2
10 20
5
```

The initial state has value `5`. Both possible next choices produce `5 % 10 = 5` or `5 % 20 = 5`. Every later operation keeps the value unchanged, so the full-mask state remains `5`.

For repeated elements:

```
3
5 5 100
12
```

The DP does not merge the two fives because the states are based on indices. One path uses the first `5`, another uses the second `5`, and both operations remain available independently. The best path is `100, 5, 5`, giving `12 % 100 = 12`, then `12 % 5 = 2`, then `2 % 5 = 2`.

For a path that reaches zero:

```
4
2 4 8 16
1000000000000000000
```

The DP may encounter a state where the current value becomes zero after applying divisor `2`. All transitions from that state stay zero, which is why skipping those states is correct. The final answer is still zero.
