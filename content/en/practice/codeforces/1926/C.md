---
title: "CF 1926C - Vlad and a Sum of Sum of Digits"
description: "For every test case, we are given a number n. Vlad writes all integers from 1 through n on the board. Then each integer is replaced by the sum of its decimal digits. The task is to compute $$sum{i=1}^{n} text{digitSum}(i)$$ where digitSum(i) is the sum of the digits of i."
date: "2026-06-08T18:59:20+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1926
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 928 (Div. 4)"
rating: 1200
weight: 1926
solve_time_s: 119
verified: true
draft: false
---

[CF 1926C - Vlad and a Sum of Sum of Digits](https://codeforces.com/problemset/problem/1926/C)

**Rating:** 1200  
**Tags:** dp, implementation  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

For every test case, we are given a number `n`. Vlad writes all integers from `1` through `n` on the board. Then each integer is replaced by the sum of its decimal digits.

The task is to compute

$$\sum_{i=1}^{n} \text{digitSum}(i)$$

where `digitSum(i)` is the sum of the digits of `i`.

For example, when `n = 12`, the digit sums are:

$$1,2,3,4,5,6,7,8,9,1,2,3$$

and their total is `51`.

The constraints are the key observation. There can be up to `10^4` test cases, and each `n` can be as large as `200000`. Computing the answer independently for every test case by iterating from `1` to `n` would repeat the same work many times. Even though `200000` is not huge by itself, doing that for `10000` test cases would require roughly two billion operations, which is far beyond what fits in a `0.5` second time limit.

The maximum value of `n` is only `200000`, which suggests a different strategy. Since every query asks for a prefix sum over the same range of numbers, we can preprocess answers for all values from `1` to `200000` once, then answer each test case in constant time.

A few edge cases deserve attention.

Consider `n = 1`.

Input:

```
1
1
```

The answer is:

```
1
```

A prefix array must be initialized correctly so that the first value is not skipped.

Consider `n = 10`.

The digit sums are:

$$1+2+3+4+5+6+7+8+9+1 = 46$$

A common mistake is forgetting that `digitSum(10) = 1`, not `10`.

Consider `n = 99999` and `n = 100000`.

The digit sum drops sharply when crossing a power of ten:

$$digitSum(99999)=45,\qquad digitSum(100000)=1$$

Any attempt to derive values using simple arithmetic patterns without properly handling carries will fail around such boundaries.

## Approaches

The most direct solution is to process each test case independently. For a given `n`, iterate through all numbers from `1` to `n`, compute each digit sum, and accumulate the result.

This works because the answer is exactly the sum of all digit sums in that range. The problem is cost. Computing a digit sum takes about `O(log n)` operations, and we must do it for every number up to `n`. For one test case the complexity is roughly `O(n log n)`. With `n = 200000` and `10000` test cases, the amount of work becomes enormous.

The crucial observation is that every test case asks for the same kind of prefix query:

$$\text{answer}(n)=\sum_{i=1}^{n}\text{digitSum}(i)$$

Instead of recomputing these sums repeatedly, we can build them once.

Let

$$dp[i] = \text{digitSum}(i)$$

and

$$pref[i] = \sum_{j=1}^{i} dp[j]$$

Then the answer for any test case is simply `pref[n]`.

Since the largest possible `n` is only `200000`, we can precompute all digit sums and all prefix sums up to that limit before reading the queries.

There is another useful observation. The digit sum of a number can be computed recursively:

$$digitSum(i)=digitSum(i//10)+(i\bmod 10)$$

This allows all digit sums from `1` to `200000` to be computed efficiently in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) per test case | O(1) | Too slow |
| Optimal | O(MAXN) preprocessing + O(1) per query | O(MAXN) | Accepted |

## Algorithm Walkthrough

1. Read all test cases and store their values.
2. Find the maximum possible value needed for preprocessing. In this problem it is always `200000`, but using the largest queried value also works.
3. Create an array `digit` where `digit[i]` stores the sum of digits of `i`.
4. Compute digit sums using the recurrence

$$digit[i] = digit[i // 10] + (i \% 10)$$

The last digit contributes `i % 10`, and the remaining digits are exactly `i // 10`.
5. Create a prefix sum array `pref`.
6. For each `i`, compute

$$pref[i] = pref[i-1] + digit[i]$$

After this step, `pref[i]` equals the required answer for `i`.
7. For every test case, output `pref[n]`.

### Why it works

The recurrence for `digit[i]` is correct because every decimal number consists of its last digit plus all preceding digits. Splitting a number into `i // 10` and `i % 10` separates those two parts exactly.

The prefix array maintains the invariant that after processing index `i`,

$$pref[i]=\sum_{k=1}^{i} digit[k]$$

This is true initially for `i=0`, and each step adds precisely one new digit sum. Consequently `pref[n]` equals the sum of digit sums from `1` through `n`, which is exactly the quantity required by the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    queries = [int(input()) for _ in range(t)]

    mx = max(queries)

    digit = [0] * (mx + 1)
    pref = [0] * (mx + 1)

    for i in range(1, mx + 1):
        digit[i] = digit[i // 10] + (i % 10)
        pref[i] = pref[i - 1] + digit[i]

    out = [str(pref[n]) for n in queries]
    sys.stdout.write("\n".join(out))

solve()
```

The first step reads every query so we know how far preprocessing must go. There is no reason to build arrays up to `200000` if all queries are smaller.

The `digit` array uses the recurrence

```
digit[i] = digit[i // 10] + (i % 10)
```

Because `i // 10` is always smaller than `i`, the needed value has already been computed.

The prefix array is built simultaneously. After calculating the digit sum for `i`, we immediately extend the running total.

Python integers are sufficient because the largest answer is only a few million. No special handling for overflow is required.

A common implementation mistake is starting the loop at `0`. The recurrence is valid there as well, but the prefix definition is cleaner when `pref[0] = 0` and processing starts from `1`.

## Worked Examples

### Example 1

Input:

```
12
```

| i | digit[i] | pref[i] |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 3 | 6 |
| 4 | 4 | 10 |
| 5 | 5 | 15 |
| 6 | 6 | 21 |
| 7 | 7 | 28 |
| 8 | 8 | 36 |
| 9 | 9 | 45 |
| 10 | 1 | 46 |
| 11 | 2 | 48 |
| 12 | 3 | 51 |

The final value is `pref[12] = 51`, which matches the sample. This trace shows how the prefix sum accumulates exactly the digit sums of all numbers up to `12`.

### Example 2

Input:

```
2024
```

Near the end of preprocessing:

| i | digit[i] |
| --- | --- |
| 2020 | 4 |
| 2021 | 5 |
| 2022 | 6 |
| 2023 | 7 |
| 2024 | 8 |

The answer is obtained directly as `pref[2024]`, which equals `28170`.

This example demonstrates that once preprocessing is complete, answering a query requires only a single array lookup.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M + t) | `M` is the largest queried value, preprocessing is linear and each query is O(1) |
| Space | O(M) | Arrays for digit sums and prefix sums |

With `M ≤ 200000`, preprocessing performs only a few hundred thousand operations. After that, each test case is answered instantly. This easily fits within both the memory limit and the unusually strict time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    queries = [int(input()) for _ in range(t)]

    mx = max(queries)

    digit = [0] * (mx + 1)
    pref = [0] * (mx + 1)

    for i in range(1, mx + 1):
        digit[i] = digit[i // 10] + (i % 10)
        pref[i] = pref[i - 1] + digit[i]

    return "\n".join(str(pref[n]) for n in queries)

# provided sample
assert run(
"""7
12
1
2
3
1434
2024
200000
"""
) == (
"""51
1
3
6
18465
28170
4600002"""
), "sample"

# minimum value
assert run(
"""1
1
"""
) == "1", "minimum n"

# crossing 10
assert run(
"""1
10
"""
) == "46", "digit carry boundary"

# small prefix
assert run(
"""1
9
"""
) == "45", "sum of first nine digits"

# power of ten boundary
assert run(
"""2
99999
100000
"""
) == "2250000\n2250001", "carry transition"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1` | `1` | Smallest valid input |
| `n = 9` | `45` | Pure single-digit range |
| `n = 10` | `46` | Transition from one digit to two digits |
| `99999, 100000` | `2250000, 2250001` | Correct handling of large carry chains |

## Edge Cases

Consider the smallest possible input:

```
1
1
```

The preprocessing loop computes:

```
digit[1] = digit[0] + 1 = 1
pref[1] = pref[0] + 1 = 1
```

The algorithm outputs `pref[1] = 1`, which is correct.

Consider the first carry boundary:

```
1
10
```

The computed values are:

```
digit[9] = 9
digit[10] = digit[1] + 0 = 1
```

The prefix sum becomes:

```
45 + 1 = 46
```

The answer is correct because the digit sum of `10` is `1`, not `10`.

Consider a long carry chain:

```
1
100000
```

The recurrence gives:

```
digit[100000]
= digit[10000] + 0
= digit[1000] + 0
= digit[100] + 0
= digit[10] + 0
= digit[1] + 0
= 1
```

The algorithm handles this naturally without any special cases. The prefix sum already contains the contribution of all previous numbers, so adding this final value produces the correct result.
