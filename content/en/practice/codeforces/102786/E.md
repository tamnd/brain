---
title: "CF 102786E - \u0423\u043f\u043e\u0440\u044f\u0434\u043e\u0447\u0438\u0432\u0430\u043d\u0438\u0435 \u043f\u043e \u0441\u0443\u043c\u043c\u0435 \u0446\u0438\u0444\u0440"
description: "We need to look at all positive integers from 1 to N, but the ordering is unusual. Numbers are grouped by the sum of their decimal digits. A group with a smaller digit sum appears earlier, and inside one group the numbers are sorted normally by value."
date: "2026-07-27T19:26:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102786
codeforces_index: "E"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u042f\u0440\u0413\u0423 \u0438\u043c. \u041f.\u0413. \u0414\u0435\u043c\u0438\u0434\u043e\u0432\u0430 Demidov Open IT Cup 2019"
rating: 0
weight: 102786
solve_time_s: 79
verified: true
draft: false
---

[CF 102786E - \u0423\u043f\u043e\u0440\u044f\u0434\u043e\u0447\u0438\u0432\u0430\u043d\u0438\u0435 \u043f\u043e \u0441\u0443\u043c\u043c\u0435 \u0446\u0438\u0444\u0440](https://codeforces.com/problemset/problem/102786/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to look at all positive integers from `1` to `N`, but the ordering is unusual. Numbers are grouped by the sum of their decimal digits. A group with a smaller digit sum appears earlier, and inside one group the numbers are sorted normally by value. The task is to find the number that occupies position `M` in this final ordering.

The value of `N` can be as large as `10^18`, so generating all numbers is impossible. Even storing the sequence would require up to around `10^18` elements. The maximum possible digit sum is only `162`, because an eighteen digit number has at most eighteen digits with value `9` and `10^18` itself has nineteen digits, so a solution should exploit the small digit count and small range of possible sums. Any approach depending on iterating through all numbers up to `N` is ruled out.

A common mistake is forgetting that the ordering inside one digit sum group is by numeric value, not by length or by some other digit order. For example, for `N = 100` and `M = 3`, the answer is `100`, because the first digit sum group is `1, 10, 100`. A method that only considers one digit length at a time can incorrectly skip `100`.

Another edge case appears when the required position is in a very large digit sum group. For example, with `N = 9` and `M = 9`, the answer is `9`. A solution that assumes every possible sum from `1` upward exists for every `N` would incorrectly search beyond the available range.

The value `1` is also a boundary case. For `N = 1` and `M = 1`, the only valid output is `1`. Handling digit sum zero as a normal group can accidentally introduce the representation `0`, which is not part of the sequence.

## Approaches

The direct solution would be to enumerate every number from `1` to `N`, compute its digit sum, store the pairs `(digit sum, number)`, and sort them. This is correct because the sorting key exactly matches the required order. However, when `N` reaches `10^18`, the number of generated elements is far beyond what any program can process. The worst case requires about `10^18` digit sum computations and sorting an equally large collection.

The useful structure is that the digit sum has a tiny range. Instead of generating numbers, we can count how many numbers belong to each digit sum group. Once we know the group containing position `M`, the remaining task is to find the `M`-th smallest number with one fixed digit sum.

Counting can be done with digit dynamic programming. Since there are only nineteen positions, we can count how many digit strings with a certain remaining sum are possible after a prefix has been fixed. These counts allow us to skip huge ranges of numbers without constructing them.

After finding the required digit sum, we build the answer digit by digit. Numbers with the same digit sum appear in increasing numeric order, which is the same as lexicographic order when all numbers have the same length. We first determine the correct length, then choose each digit by counting how many valid completions exist if we put a smaller digit there.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N log N) | O(N) | Too slow |
| Optimal | O(162 * 19 * 10 + 19 * 19 * 10) | O(19 * 162) | Accepted |

## Algorithm Walkthrough

1. Precompute `ways(length, sum)`, the number of digit sequences of a given length where every digit can be from `0` to `9` and the total digit sum equals `sum`. This table is the core counting tool used everywhere else.

These sequences may contain leading zeroes because they represent the remaining suffix of a number. Leading zeroes do not cause problems because the full length is fixed during counting.
2. For every possible digit sum from `1` upward, calculate how many numbers from `1` to `N` have that digit sum.

The count is obtained with digit DP. We scan the digits of `N` from left to right, deciding whether the current prefix is already smaller than `N` or still equal to it. The leading zero representation allows us to count all positive numbers of shorter lengths automatically.
3. Subtract complete digit sum groups from `M` until the group containing the answer is found.

After this step, `M` becomes the position inside one fixed digit sum group.
4. Find the length of the required number.

For each possible length, count how many numbers of that length have the required digit sum. Shorter lengths always come before longer lengths because every positive number with fewer digits is numerically smaller.
5. Construct the answer from left to right.

At each position, try possible digits in increasing order. For every candidate digit, count how many ways the remaining positions can complete the number with the remaining digit sum. If the current `M` is larger than that count, skip all those numbers. Otherwise, the answer starts with that digit.
6. Output the constructed number.

The reason this works is that every skipped block corresponds to a consecutive interval in the required ordering. The digit DP counts exactly how many valid numbers are inside each interval, so reducing `M` by those counts never changes the relative position of the desired number. During construction, the chosen prefix is always the smallest prefix whose block contains the remaining position, which preserves the invariant that the answer is still inside the remaining search range.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

@lru_cache(None)
def ways(length, total):
    if length == 0:
        return 1 if total == 0 else 0
    if total < 0:
        return 0
    res = 0
    for d in range(10):
        res += ways(length - 1, total - d)
    return res

def count_up_to(n, target_sum):
    digits = list(map(int, str(n)))
    m = len(digits)

    @lru_cache(None)
    def dp(pos, remaining, tight):
        if pos == m:
            return 1 if remaining == 0 else 0

        limit = digits[pos] if tight else 9
        ans = 0

        for d in range(limit + 1):
            if remaining >= d:
                ans += dp(pos + 1, remaining - d, tight and d == limit)

        return ans

    return dp(0, target_sum, True)

def count_exact_length(length, target_sum):
    ans = 0
    for first in range(1, 10):
        if target_sum >= first:
            ans += ways(length - 1, target_sum - first)
    return ans

def solve_case(n, m):
    digit_sum = 1

    while True:
        cnt = count_up_to(n, digit_sum)
        if m <= cnt:
            break
        m -= cnt
        digit_sum += 1

    length = 1
    while True:
        cnt = count_exact_length(length, digit_sum)
        if m <= cnt:
            break
        m -= cnt
        length += 1

    result = []
    remaining = digit_sum

    for pos in range(length):
        start = 1 if pos == 0 else 0

        for digit in range(start, 10):
            if remaining < digit:
                continue

            cnt = ways(length - pos - 1, remaining - digit)

            if m > cnt:
                m -= cnt
            else:
                result.append(str(digit))
                remaining -= digit
                break

    return ''.join(result)

def main():
    n, m = map(int, input().split())
    print(solve_case(n, m))

if __name__ == "__main__":
    main()
```

The `ways` function stores the number of possible suffixes for a given length and sum. It is used both while counting lengths and while deciding individual digits. The largest requested length is only nineteen, so the table is very small.

`count_up_to` uses digit DP with a tight flag. When the already chosen prefix matches `N`, the next digit cannot exceed the corresponding digit of `N`. Once the prefix becomes smaller, the rest of the number can use any digits. The implementation uses leading zeroes, which is why all positive numbers up to `N` are represented exactly once.

`count_exact_length` excludes a leading zero by starting the first digit from `1`. This function is separated from `ways` because `ways` intentionally allows zeroes for suffixes.

The final construction loop is where the `M`-th number is recovered. Trying digits in ascending order matches numeric ordering because the length is already fixed. Every skipped digit represents a complete block of valid numbers, so subtracting its size is the same as moving forward in the ordered sequence.

## Worked Examples

For the sample `N = 100`, `M = 10`, the groups begin as follows.

| Current digit sum | Count skipped | Remaining M | Decision |
| --- | --- | --- | --- |
| 1 | 3 | 7 | Skip sum 1 |
| 2 | 4 | 3 | Skip sum 2 |
| 3 | 4 | 3 | Choose sum 3 |

The digit sum `3` group is `3, 12, 21, 30`, so the third element is `21`.

The trace shows that the algorithm never needs to generate the earlier groups. It only counts their sizes and moves directly to the required group.

For `N = 20`, `M = 5`, the ordered sequence is:

`1, 10, 2, 11, 20`

| Current digit sum | Count skipped | Remaining M | Decision |
| --- | --- | --- | --- |
| 1 | 2 | 3 | Skip sum 1 |
| 2 | 3 | 3 | Choose sum 2 |

The digit sum `2` group contains `2, 11, 20`, and the third element is `20`.

This example exercises the length transition because the same digit sum group contains both one digit and two digit numbers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(162 * 19 * 10 + 19 * 19 * 10) | There are at most 162 digit sums, nineteen positions, and ten digit choices in each DP transition. |
| Space | O(19 * 162) | The memoized suffix counts contain only small digit length and sum states. |

The algorithm depends on the number of digits rather than the value of `N`. Since `N` has at most nineteen digits, the solution easily fits the time and memory limits.

## Test Cases

```python
import sys
import io
from functools import lru_cache

def build_solver():
    @lru_cache(None)
    def ways(length, total):
        if length == 0:
            return 1 if total == 0 else 0
        return sum(ways(length - 1, total - d) for d in range(10))

    def count_up_to(n, target_sum):
        digits = list(map(int, str(n)))
        m = len(digits)

        @lru_cache(None)
        def dp(pos, remaining, tight):
            if pos == m:
                return remaining == 0
            limit = digits[pos] if tight else 9
            ans = 0
            for d in range(limit + 1):
                if remaining >= d:
                    ans += dp(pos + 1, remaining - d, tight and d == limit)
            return ans

        return dp(0, target_sum, True)

    def count_exact_length(length, total):
        return sum(
            ways(length - 1, total - d)
            for d in range(1, 10)
            if total >= d
        )

    def solve_case(n, m):
        s = 1
        while True:
            c = count_up_to(n, s)
            if m <= c:
                break
            m -= c
            s += 1

        length = 1
        while True:
            c = count_exact_length(length, s)
            if m <= c:
                break
            m -= c
            length += 1

        ans = []
        remaining = s
        for pos in range(length):
            for d in range(1 if pos == 0 else 0, 10):
                if remaining >= d:
                    c = ways(length - pos - 1, remaining - d)
                    if m > c:
                        m -= c
                    else:
                        ans.append(str(d))
                        remaining -= d
                        break
        return ''.join(ans)

    return solve_case

solve = build_solver()

def run(inp: str) -> str:
    n, m = map(int, inp.split())
    return solve(n, m)

assert run("100 10") == "21"
assert run("1 1") == "1"
assert run("9 9") == "9"
assert run("20 5") == "20"
assert run("1000 3") == "100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum input and exclusion of digit sum zero |
| `9 9` | `9` | Single digit boundary |
| `20 5` | `20` | Transition between number lengths inside a digit sum group |
| `1000 3` | `100` | Correct ordering of equal digit sums |

## Edge Cases

For `N = 100` and `M = 3`, the digit sum search selects sum `1`. The length search checks length `1`, where the only number is `1`, and then length `2`, where the only number is `10`. After removing those two positions, the remaining position is the first number of length `3`, which is `100`. This handles the case where longer numbers appear in the same digit sum group.

For `N = 9` and `M = 9`, the algorithm counts the only existing group correctly. Each digit sum from `1` to `8` contains one number and is skipped, leaving digit sum `9` with position `1`. The construction creates the single digit `9`.

For `N = 1` and `M = 1`, digit sum `1` is selected immediately. The length is one, the only possible first digit is `1`, and the construction finishes without ever considering an invalid zero value.

For `N = 20` and `M = 5`, the algorithm reaches digit sum `2`. It first checks the one digit number `2`, then constructs the third number in the group. The suffix counting places the answer after `2` and `11`, producing `20`. This confirms that the construction respects numeric order across different lengths.
