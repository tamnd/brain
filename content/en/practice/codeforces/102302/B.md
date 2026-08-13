---
title: "CF 102302B - Divples"
description: "We need to find every positive integer that is simultaneously a divisor of a and a multiple of b. The input gives the two integers a and b, with b <= a and both potentially as large as 10^12."
date: "2026-08-14T04:32:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "B"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 338
verified: false
draft: false
---

[CF 102302B - Divples](https://codeforces.com/problemset/problem/102302/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We need to find every positive integer that is simultaneously a divisor of `a` and a multiple of `b`. The input gives the two integers `a` and `b`, with `b <= a` and both potentially as large as `10^12`. The output should contain all integers satisfying both conditions, arranged from smallest to largest. If no such integer exists, the required output is simply an empty line.

The two conditions interact in a useful way. Suppose a valid number is `x`. Since `x` is a multiple of `b`, we can write `x = b * k` for some positive integer `k`. Since `x` must also divide `a`, we have `b * k | a`. This is possible only when `b` itself divides `a`. When `b | a`, write `a = b * n`. Then `b * k | b * n` exactly when `k | n`. The original problem has consequently been reduced to finding all divisors `k` of `n = a / b`, then multiplying them by `b`.

The upper bound of `10^12` rules out any approach that scans all integers up to `a`. In the worst case, such a scan performs around `10^12` iterations, far beyond what a two-second limit can support. Even scanning only multiples of `b` is not sufficient, because `b` can be `1`, leaving as many as `10^12` candidates. The divisor structure lets us do much better by enumerating divisors through pairs up to the square root. Since the relevant value is at most `10^12`, its square root is at most `10^6`, which is easily manageable.

There are several edge cases that a careless implementation can mishandle. If `b` does not divide `a`, there are no answers. For example, with input `10 3`, no multiple of `3` can divide `10`, so the correct output is empty. An implementation that simply generates multiples of `3` and stops at `10` would produce `3 6 9`, even though none of those numbers divides `10`.

A second edge case occurs when `a = b`. For input `5 5`, the only valid number is `5`, because `5` divides `5` and is a multiple of `5`. After reducing by `b`, we get `n = 1`, whose only divisor is `1`. The corresponding answer is `5 * 1 = 5`.

A third edge case is a perfect square. For input `36 2`, we have `n = 18`, while for input `49 7`, we have `n = 7`. More generally, if `n` itself is a square, the divisor pair discovered at `sqrt(n)` contains the same divisor twice. The implementation must avoid adding that value twice. For example, `a = 36, b = 1` has divisors including `6`, but `6` must appear only once in the output.

## Approaches

The most direct brute-force solution is to inspect every possible integer from `1` through `a`, checking whether it is both divisible by `b` and a divisor of `a`. We could make the scan slightly smaller by checking only multiples of `b`, but in the worst case `b = 1`, so we still perform `10^12` checks. Even if every check were constant time, this is far beyond the available time. The brute-force method is correct because every possible answer is examined, but its number of operations is the fundamental problem.

The key observation is that every answer contains `b` as a factor. If `b` does not divide `a`, there cannot be any answer. If `b` divides `a`, set `n = a / b`. Every answer has the form `b * k`, and the divisibility condition becomes `k | n`. We have transformed the problem from finding special divisors of `a` into finding every ordinary divisor of the smaller number `n`.

Divisors can be enumerated in pairs. Whenever `i` divides `n`, the number `n / i` is also a divisor. We only need to test `i` up to `sqrt(n)`, because every divisor larger than the square root is paired with a divisor smaller than the square root. Thus we perform at most `10^6` divisibility checks. We collect both members of every divisor pair, multiply them by `b`, sort the resulting values, and print them.

The brute-force approach works because it checks the entire range of possible answers, but fails when that range reaches `10^12`. The observation that every valid number is `b` times a divisor of `a / b` reduces the search space to only `O(sqrt(a / b))` candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a) in the worst case | O(1) excluding output | Too slow |
| Optimal | O(sqrt(a / b) + d log d) | O(d) | Accepted |

Here `d` is the number of divisors of `a / b`. For numbers up to `10^12`, `d` is small compared with the original search range.

## Algorithm Walkthrough

1. Read `a` and `b`. Before doing any divisor enumeration, check whether `a % b` is zero. If it is not, print an empty line and stop, because a number that is a multiple of `b` cannot divide `a` unless `b` itself divides `a`.
2. Compute `n = a // b`. Every valid answer is now exactly `b * k`, where `k` is a divisor of `n`. This follows from `a = b * n` and `b * k | b * n`, which is equivalent to `k | n`.
3. Start with an empty list of answers and iterate `i` from `1` while `i * i <= n`. Testing only this range is sufficient because every divisor below the square root has a paired divisor above it.
4. Whenever `n % i == 0`, add `b * i` to the answer list. Also add `b * (n // i)`, which is the other member of the divisor pair.
5. If `i * i == n`, do not add the second value separately. In that situation `i` and `n // i` are the same divisor, so adding both would duplicate one answer.
6. Sort the collected answers. Divisors are discovered in increasing order for the small member of each pair but their paired large members are not globally ordered, so sorting gives the required numerical order.
7. Print the answers separated by spaces. If the list is empty, printing the joined string naturally produces the required blank line.

### Why it works

After the divisibility check, we know `a = b * n`. A number `x` is a valid answer exactly when it can be written as `x = b * k` and `x | a`. Substituting these expressions gives `b * k | b * n`, which is equivalent to `k | n`. Thus there is a one-to-one correspondence between valid answers and divisors of `n`, with each divisor `k` mapped to `b * k`.

The divisor enumeration examines every `i <= sqrt(n)`. If `i` divides `n`, its paired divisor `n / i` is also found, so every divisor is generated either as the small member or the large member of a pair. The square case is handled separately so a divisor equal to `sqrt(n)` appears exactly once. Consequently, after multiplication by `b` and sorting, the output contains every valid integer exactly once and contains no invalid integer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())

    if a % b != 0:
        print()
        return

    n = a // b
    ans = []

    i = 1
    while i * i <= n:
        if n % i == 0:
            ans.append(b * i)

            other = n // i
            if other != i:
                ans.append(b * other)

        i += 1

    ans.sort()
    print(*ans)

if __name__ == "__main__":
    solve()
```

The first condition checks the necessary divisibility of `a` by `b`. Without it, there is no reason to search for divisors because every candidate would have to contain `b` as a factor.

The variable `n` is the reduced problem size, `a / b`. The loop tests possible small divisors from `1` through `sqrt(n)`. The condition `i * i <= n` avoids floating-point square roots and is safe for Python's arbitrary-precision integers.

When `i` divides `n`, both `i` and `n // i` are divisors. Multiplying each by `b` converts them back to the actual numbers required by the original problem. The `other != i` check handles perfect squares, preventing the square root from being inserted twice.

The final sort is necessary because divisor pairs are discovered in a mixed order. For example, when `n = 12`, the iteration finds `1, 12`, then `2, 6`, then `3, 4`. This particular sequence happens to be nearly ordered, but in general the transformed values need not arrive in the required global order. Sorting makes the output condition explicit.

Python integers do not overflow, so values such as `b * (n // i)` are safe even when they are as large as `10^12`.

## Worked Examples

### Sample 1: `12 3`

Here `b` divides `a`, so the problem reduces to finding the divisors of `n = 12 / 3 = 4`.

| `i` | `i * i <= n` | `n % i` | Small divisor | Paired divisor | Answers collected |
| --- | --- | --- | --- | --- | --- |
| 1 | true | 0 | 1 | 4 | 3, 12 |
| 2 | true | 0 | 2 | 2 | 3, 12, 6 |
| 3 | false | not checked |  |  | 3, 12, 6 |

After sorting, the answers are `3 6 12`.

The trace shows the divisor-pair invariant directly. The divisors of `4` are `1`, `2`, and `4`, and multiplying them by `3` produces exactly the required numbers. The value `2` is the square root of `4`, so it is added only once.

### Sample 2: `10 3`

The first divisibility test already settles the problem because `10 % 3 = 1`.

| `a` | `b` | `a % b` | `n` | Answers |
| --- | --- | --- | --- | --- |
| 10 | 3 | 1 | not computed | empty |

The algorithm prints an empty line. This is the case that catches an incorrect solution that merely generates multiples of `b`. Values such as `3`, `6`, and `9` are multiples of `3`, but none divides `10`, so none is a valid answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(a / b) + d log d) | We test divisors up to `sqrt(a / b)`, generate `d` answers, then sort them. |
| Space | O(d) | The answer list stores the valid values. |

Since `a / b <= 10^12`, the divisor search performs at most about `10^6` loop iterations. The number of divisors `d` is much smaller than `10^6`, so the sorting cost is also modest. The algorithm comfortably fits the two-second time limit and stays well within the 64 MB memory limit.

## Test Cases

```python
import sys
import io

def solve():
    a, b = map(int, input().split())

    if a % b != 0:
        print()
        return

    n = a // b
    ans = []

    i = 1
    while i * i <= n:
        if n % i == 0:
            ans.append(b * i)

            other = n // i
            if other != i:
                ans.append(b * other)

        i += 1

    ans.sort()
    print(*ans)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        from io import StringIO

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            solve()
            return sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
    finally:
        sys.stdin = old_stdin
        input = old_input

assert run("12 3\n") == "3 6 12\n", "sample 1"
assert run("10 3\n") == "\n", "sample 2"
assert run("128 2\n") == "2 4 8 16 32 64 128\n", "sample 3"

assert run("1 1\n") == "1\n", "minimum-size input"
assert run("5 5\n") == "5\n", "all-equal values"
assert run("36 1\n") == "1 2 3 4 6 9 12 18 36\n", "perfect square"
assert run("1000000000000 1000000000000\n") == "1000000000000\n", "maximum-size equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum values and the `n = 1` case |
| `5 5` | `5` | Equal `a` and `b` |
| `36 1` | `1 2 3 4 6 9 12 18 36` | Perfect-square divisor pairing and sorted output |
| `1000000000000 1000000000000` | `1000000000000` | Maximum input size and boundary arithmetic |

## Edge Cases

When `b` does not divide `a`, the algorithm exits before divisor enumeration. For input `10 3`, the first calculation is `10 % 3 = 1`, so the answer list remains empty and the program prints a blank line. This prevents the common mistake of treating every multiple of `b` as an answer without checking whether it actually divides `a`.

When `a = b`, the reduced value is `n = 1`. For input `5 5`, the loop starts with `i = 1`, and `1 * 1 <= 1` is true. Since `1` divides `1`, the algorithm adds `5 * 1 = 5`. The paired divisor is also `1`, so `other != i` is false and no duplicate is inserted. The loop then ends, producing `5`.

When `n` is a perfect square, the duplicate guard is essential. Consider `36 1`. The relevant reduced number is `36`, and when `i = 6`, both divisor expressions give `6`. The algorithm adds `6` once and skips the second insertion because `other == i`. The complete sorted output is `1 2 3 4 6 9 12 18 36`.

At the largest possible values, such as `1000000000000 1000000000000`, the reduced number is only `1`. The algorithm does not loop anywhere near `10^12` times. It performs a single divisor check and outputs the original value. This illustrates why reducing the problem by `b` is useful even before applying square-root divisor enumeration.
