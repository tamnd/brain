---
title: "CF 102775G - \u041c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0440\u0430\u0432\u0435\u043d\u0441\u0442\u0432\u043e"
description: "The task is to split a given natural number N into several positive integers. Every part of the split must have exactly the same sum of decimal digits. The number of parts must be at least two, cannot reach N itself, and cannot exceed one million."
date: "2026-07-27T20:40:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102775
codeforces_index: "G"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 20), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102775
solve_time_s: 72
verified: true
draft: false
---

[CF 102775G - \u041c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0440\u0430\u0432\u0435\u043d\u0441\u0442\u0432\u043e](https://codeforces.com/problemset/problem/102775/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to split a given natural number `N` into several positive integers. Every part of the split must have exactly the same sum of decimal digits. The number of parts must be at least two, cannot reach `N` itself, and cannot exceed one million. If such a split exists, we print the amount of parts and the parts themselves. Otherwise, we print `-1`.

The limit `N <= 10^18` immediately rules out trying possible summands or searching over partitions. Even iterating over all values up to `N` is impossible because the input can contain a number around one quintillion. The useful observation has to depend only on the number of digits, because `N` has at most 19 decimal digits.

The difficult cases are not large values, but values with very few possible decompositions. For example, `N = 1` cannot be split because there is no way to create at least two positive summands. A careless implementation that always prints the decimal digits as powers of ten would output one summand for this case.

For `N = 10`, the decimal digit decomposition gives only one summand, `10`, which is invalid. The correct output is `2` followed by `5 5`, because both summands have digit sum `5`. A careless implementation that only counts decimal digits would miss all powers of ten.

For `N = 2`, the decomposition into digit-value copies works correctly: `1 + 1`. Both numbers have digit sum `1`, and the number of summands is valid.

## Approaches

A direct approach would try to find some digit sum `S`, generate numbers with digit sum `S`, and search for a combination adding up to `N`. This is correct because any valid answer must use numbers with one common digit sum. However, the search space is enormous. Even generating all candidates below `10^18` is impossible, and a partition search would have far more possibilities than can be handled in one second.

The structure of decimal representation gives a much simpler route. Any digit `d` at position `10^k` can be viewed as `d` copies of the number `10^k`. Each such copy has digit sum `1`. For example, `352` becomes `3 * 100 + 5 * 10 + 2 * 1`, which can be written as ten digit-sum-one numbers:

`100, 100, 100, 10, 10, 10, 10, 10, 1, 1`

Every summand has the same digit sum, so this is a valid construction whenever the decimal digit sum of `N` is at least two. The number of produced terms is exactly the sum of the digits of `N`, which is at most `171` for the given limits.

The only failure of this construction happens when the digit sum is one. Such numbers are exactly powers of ten. For `N = 1`, no answer exists. For any other power of ten, splitting it into two equal halves works. The number `10^k / 2` has digit sum `5`, so the two halves always satisfy the requirement.

The brute force works because it searches for the same property we exploit, equal digit sums, but it tries to discover a structure that the decimal representation already gives us. The observation that powers of ten naturally have digit sum one lets us construct almost every answer immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of possible partitions) | O(number of candidates) | Too slow |
| Optimal | O(number of digits + answer size) | O(answer size) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of the decimal digits of `N`. This tells us whether the straightforward digit decomposition will contain one or multiple summands.
2. If `N` is `1`, print `-1`. There is no way to create two positive numbers whose sum is `1`.
3. If the digit sum of `N` is `1`, print two copies of `N / 2`. The only such values are powers of ten, and every power of ten greater than one is even. Each half has digit sum `5`.
4. Otherwise, scan the decimal digits of `N` from right to left. For every digit `d` at position `10^k`, add `d` copies of `10^k` to the answer.

The reason this works is that each generated value has only one non-zero digit, so every generated value has digit sum `1`. Adding the copies reconstructs the original decimal number exactly.
5. Print the number of generated summands and the summands themselves.

The invariant behind the construction is that every produced summand has the same digit sum. The only special case is when the natural digit decomposition would contain one summand, which happens exactly for powers of ten. The separate handling of those numbers preserves the same invariant while satisfying the requirement of having at least two parts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_sum(x):
    return sum(map(int, str(x)))

def solve():
    n = int(input())

    if n == 1:
        print(-1)
        return

    if digit_sum(n) == 1:
        print(2)
        print(n // 2, n // 2)
        return

    ans = []
    x = n
    power = 1

    while x > 0:
        digit = x % 10
        for _ in range(digit):
            ans.append(power)
        power *= 10
        x //= 10

    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The first branch handles the only impossible input. The condition is checked before the power-of-ten case because `1` also has digit sum one, but dividing it into two positive integers is impossible.

The second branch handles all powers of ten greater than one. The division is exact because these numbers are even, and the resulting halves have equal digit sums.

The main loop extracts digits from right to left. `power` always stores the current decimal place value. If the current digit is `d`, appending `d` copies of `power` contributes exactly the same amount as that digit contributed in the original number. The answer size stays tiny because the maximum possible decimal digit sum for this input range is `171`.

Python integers do not overflow, so the half of `10^18` and all intermediate values are safe. The loop also avoids converting the number into a list of digits, which keeps the implementation direct.

## Worked Examples

### Example 1

Input:

```
1
```

| Step | Current value | Digit sum | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Check impossible case | -1 |

The algorithm immediately rejects the input because one cannot create at least two positive summands from `1`.

### Example 2

Input:

```
352
```

| Step | Current digit | Power | Copies added | Current answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1, 1 | 1, 1 |
| 2 | 5 | 10 | 10, 10, 10, 10, 10 | 1, 1, 10, 10, 10, 10, 10 |
| 3 | 3 | 100 | 100, 100, 100 | 1, 1, 10, 10, 10, 10, 10, 100, 100, 100 |

The generated numbers sum to `352`. Every element has digit sum `1`, so the invariant is maintained.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(number of digits + answer size) | The number has at most 19 digits, and at most 171 summands are generated. |
| Space | O(answer size) | The stored output contains only the generated summands. |

The algorithm performs a constant amount of work for this problem's limits. The largest possible output is only a few hundred integers, far below the one million limit.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def digit_sum(x):
        return sum(map(int, str(x)))

    n = int(sys.stdin.readline())

    if n == 1:
        return "-1"

    if digit_sum(n) == 1:
        return f"2\n{n // 2} {n // 2}"

    ans = []
    x = n
    power = 1
    while x > 0:
        d = x % 10
        for _ in range(d):
            ans.append(power)
        power *= 10
        x //= 10

    return str(len(ans)) + "\n" + " ".join(map(str, ans))

def check(inp):
    out = solve_case(inp)
    if out == "-1":
        return out

    lines = out.splitlines()
    m = int(lines[0])
    values = list(map(int, lines[1].split()))

    assert len(values) == m
    assert 2 <= m
    assert all(v > 0 for v in values)
    assert sum(values) == int(inp)
    assert len({sum(map(int, str(v))) for v in values}) == 1
    return out

# provided samples
assert check("1\n") == "-1", "sample 1"
assert check("2\n").splitlines()[0] == "2", "sample 2"

# custom cases
check("10\n")
check("1000000000000000000\n")
check("999999999999999999\n")
check("101010101010101010\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10` | Two equal halves | Power-of-ten special handling |
| `1000000000000000000` | Two valid large halves | Maximum input boundary |
| `999999999999999999` | Many digit-sum-one terms | Large answer construction |
| `101010101010101010` | Repeated decimal positions | Correct digit extraction |

## Edge Cases

For `N = 1`, the algorithm reaches the first condition and prints `-1`. There are no positive values that can be used twice while keeping their sum equal to one.

For `N = 10`, the ordinary digit decomposition would incorrectly give only `[10]`. The algorithm detects that the digit sum is one, uses the special case, and outputs `5 5`. Both numbers have digit sum five and together form ten.

For `N = 2`, the digit sum is two, so the decomposition creates two copies of `1`. The output contains two summands with digit sum one, and their sum is exactly the original number.

For `N = 10^18`, the digit sum is one, so the algorithm does not attempt to create a single summand. It outputs two copies of `500000000000000000`, which satisfy all restrictions while avoiding an invalid one-element answer.
