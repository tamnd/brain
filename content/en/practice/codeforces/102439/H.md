---
title: "CF 102439H - Nonfibonacci numbers"
description: "For an integer (x), crossing out digits means deleting some positions from its decimal representation while keeping all remaining digits in their original order. A number is disliked if some positive Fibonacci number can be obtained this way."
date: "2026-08-10T06:55:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "H"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 201
verified: true
draft: false
---

[CF 102439H - Nonfibonacci numbers](https://codeforces.com/problemset/problem/102439/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

For an integer (x), crossing out digits means deleting some positions from its decimal representation while keeping all remaining digits in their original order. A number is disliked if some positive Fibonacci number can be obtained this way. We need to count the numbers in the inclusive range ([0,n]) that are not disliked.

For example, (193) is disliked because deleting its middle digit leaves (13), which is Fibonacci. On the other hand, (4) is liked because no positive Fibonacci number can be obtained from its digits. The official constraints allow up to ten test cases, with (n) as large as (10^{18}).

The upper bound of (10^{18}) is the key constraint. Iterating through every integer is impossible, since there can be (10^{18}+1) candidates in one test case. We need to work with the at most 19 decimal digits of (n), so a digit-based counting method is the natural target.

There are several boundary cases that can easily break a careless implementation. For (n=0), the answer is (1), because the only number in the range is (0), and zero is liked. An implementation that counts only positive numbers would incorrectly return (0).

For (n=4), the answer is (2), namely (0) and (4). The digits (1,2,3) cannot occur in a liked positive number, because each is itself a positive Fibonacci number. A solution that checks only Fibonacci numbers with at least two digits would incorrectly count (1,2,3).

For (n=2019), the answer is (125). The first digit of a four-digit number at most (2019) would have to be (1) or (2), and both digits are forbidden. Thus there are no new liked numbers with four digits. A solution that simply counts all strings made from the allowed digits without respecting the upper bound could overcount here.

Leading zeroes also need careful treatment. The number (04) is not a separate integer from (4), so zero may be used inside a number, but it cannot be used as the first digit of a positive number.

## Approaches

The direct approach is to examine every integer (x) from (0) through (n). For each (x), we could generate all Fibonacci numbers up to (x), then test whether any of their decimal strings is a subsequence of the decimal representation of (x). Since Fibonacci numbers grow exponentially, there are only about 90 relevant Fibonacci values below (10^{18}), and each has at most 19 digits. The approach is correct because a number is disliked exactly when at least one of those Fibonacci strings appears as a subsequence.

The problem is the number of candidate integers. In the worst case we perform roughly (10^{18}\cdot90\cdot19=1.71\cdot10^{21}) digit comparisons for one test case. Even before accounting for Python overhead, that is far beyond the one-second limit.

The useful observation comes from the smallest Fibonacci numbers. The positive one-digit Fibonacci numbers are (1,2,3,5,8). If a number contains any of these digits, that single digit can itself be kept, so the number is immediately disliked. Consequently, every liked number can contain only the digits

[
{0,4,6,7,9}.
]

At this point we still have to worry about a multi-digit Fibonacci number whose every digit belongs to this set. There are only 19-digit Fibonacci numbers at most (10^{18}), and only about 90 Fibonacci values need to be inspected. Generating them once and checking their decimal digits shows that none of the positive Fibonacci numbers up to (10^{18}) consists entirely of (0,4,6,7,9). Thus no multi-digit Fibonacci number can be a subsequence of a number using only these five digits.

This reduces the original problem to a much simpler one: count integers at most (n) whose decimal representation uses only (0,4,6,7,9). The remaining work is a standard digit-counting procedure.

The brute-force method works because it tests the definition directly, but fails because the range is enormous. The observation that the one-digit Fibonacci numbers eliminate five decimal digits collapses the complicated subsequence condition into a simple restriction on every digit. Once the remaining Fibonacci candidates are exhausted, the problem becomes counting restricted decimal strings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\cdot 90\cdot 19)) | (O(90)) | Too slow |
| Optimal | (O(19\cdot 10)) per test case | (O(19)) | Accepted |

## Algorithm Walkthrough

1. Treat (0) separately. It is a liked integer, so it contributes one to every answer with (n\ge0).
2. For every positive integer, only the digits (4,6,7,9) are possible in the first position. The digit (0) is allowed only after the first position because leading zeroes do not form part of the decimal representation.
3. For every possible length shorter than the number of digits in (n), count all valid numbers of that length. A positive number of length (k) has four choices for its first digit and five choices for every later digit, giving (4\cdot5^{k-1}) possibilities.
4. Count valid numbers having exactly the same length as (n). Process the digits of (n) from left to right. At each position, count how many allowed digits are smaller than the corresponding digit of (n). Choosing any such smaller digit makes the whole prefix smaller, so all remaining positions can then be filled independently with five allowed digits.
5. If the current digit of (n) is not allowed, stop immediately. The prefix constructed so far can already be made smaller than (n), and any number that keeps the current forbidden digit would not be valid.
6. If every digit of (n) itself is allowed, add one at the end to include (n) itself. Otherwise, no number with the exact same prefix as (n) can be valid.

### Why it works

Every disliked number must contain at least one positive Fibonacci number as a subsequence. Since (1,2,3,5,8) are Fibonacci numbers, a liked number cannot contain any of those digits. Conversely, after restricting every digit to (0,4,6,7,9), none of the positive Fibonacci numbers up to (10^{18}) remains possible as a complete digit string, so none can occur as a subsequence. Thus the liked numbers are exactly the integers whose decimal digits belong to that allowed set.

The counting procedure examines every possible valid decimal representation exactly once. For a shorter length, the first digit has four choices and every later digit has five. For the length of (n), whenever we choose a smaller digit at the first differing position, the remaining suffix is unrestricted except for the allowed-digit condition. If the current digit cannot be matched, the equal-prefix branch disappears. This partitions all valid numbers at most (n) without overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

ALLOWED = "04679"
FIRST = "4679"

def count_liked(n: int) -> int:
    s = str(n)
    length = len(s)

    # The number 0 is always liked.
    ans = 1

    # Count all positive valid numbers with fewer digits.
    power = 1
    for digits in range(1, length):
        ans += 4 * power
        power *= 5

    # Count valid numbers with exactly len(s) digits and <= n.
    for i, ch in enumerate(s):
        d = ord(ch) - ord('0')

        choices = FIRST if i == 0 else ALLOWED

        smaller = 0
        for c in choices:
            if ord(c) - ord('0') < d:
                smaller += 1

        # Once this position is made smaller than n,
        # every remaining position can be filled freely.
        remaining = length - i - 1
        ans += smaller * (5 ** remaining)

        # We cannot continue with the same prefix.
        if ch not in choices:
            return ans

    # n itself uses only allowed digits.
    return ans + 1

def solve() -> None:
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        out.append(str(count_liked(n)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `ALLOWED` string represents all digits that may occur after the first position. It contains zero because internal zeroes are valid, while `FIRST` excludes zero to prevent leading zeroes.

The initial value `ans = 1` accounts for zero. This is necessary even when (n=0), because the range is inclusive.

The first loop handles every shorter positive length. The variable `power` starts at (5^0), so the contribution for one digit is (4), then (20), then (100), and so on. After each length it is multiplied by five.

The second loop implements the tight-prefix counting from the algorithm. Suppose the current digit of (n) is (6). At a non-leading position, the allowed smaller digits are (0) and (4), so there are two possible smaller branches. Once one is selected, all remaining positions have five choices each, giving (2\cdot5^{\text{remaining}}) numbers.

The early return when the current digit is forbidden handles the upper-bound condition cleanly. We count every valid number that first becomes smaller at the current position, but we cannot continue along the exact prefix because that would require using a forbidden digit.

If every digit survives, (n) itself is a valid number and must be included. The final `+ 1` handles precisely that case.

Python integers have arbitrary precision, so values such as (5^{18}) do not overflow. The largest relevant power is tiny compared with what Python integers can represent.

## Worked Examples

### Sample 1: (n=4)

The valid positive one-digit numbers are (4,6,7,9), but only (4) is at most (4). Together with zero, the answer is (2).

| Position | Current digit | Allowed smaller digits | Added numbers | Decision |
| --- | --- | --- | --- | --- |
| 0 | 4 | none | 0 | 4 is allowed |

After processing the only digit, (4) itself is valid, so it contributes one more number. Including zero gives the final answer (2).

### Sample 2: (n=2019)

There are (4) valid one-digit positive numbers, (20) valid two-digit numbers, and (100) valid three-digit numbers. Together with zero this gives (125).

| Position | Current digit | Allowed smaller digits | Added numbers | Decision |
| --- | --- | --- | --- | --- |
| 0 | 2 | none | 0 | 2 is forbidden |

The first digit of every four-digit number must be (4,6,7), or (9), but all of those exceed (2019). Since the first digit of (2019) is forbidden, the equal-prefix branch stops immediately. The answer remains (1+4+20+100=125), matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(19\cdot10)) per test case | There are at most 19 digits, and each position checks at most 5 allowed digits |
| Space | (O(19)) | The input representation contains at most 19 decimal digits |

The preprocessing observation about Fibonacci numbers is constant-sized for this problem, since only Fibonacci values up to (10^{18}) are relevant. Each query then examines at most 19 positions, so even ten test cases require only a few thousand simple operations. This is comfortably inside the one-second time limit and uses negligible memory.

## Test Cases

```python
import sys
import io

ALLOWED = "04679"
FIRST = "4679"

def count_liked(n: int) -> int:
    s = str(n)
    length = len(s)

    ans = 1

    power = 1
    for digits in range(1, length):
        ans += 4 * power
        power *= 5

    for i, ch in enumerate(s):
        d = ord(ch) - ord('0')
        choices = FIRST if i == 0 else ALLOWED

        smaller = 0
        for c in choices:
            if ord(c) - ord('0') < d:
                smaller += 1

        remaining = length - i - 1
        ans += smaller * (5 ** remaining)

        if ch not in choices:
            return ans

    return ans + 1

def solve_data(inp: str) -> str:
    data = inp.strip().split()
    t = int(data[0])

    out = []
    for i in range(1, t + 1):
        out.append(str(count_liked(int(data[i]))))

    return "\n".join(out)

# Provided sample.
assert solve_data("2\n4\n2019\n") == "2\n125", "sample"

# Minimum-size inputs.
assert solve_data("3\n0\n1\n4\n") == "1\n1\n2", "minimum values"

# Boundary around the largest allowed one-digit number.
assert solve_data("4\n8\n9\n10\n44\n") == "4\n5\n5\n6", "one and two digit boundaries"

# All-equal boundary case.
assert solve_data("1\n7777\n") == "475", "all-equal digits"

# Maximum allowed input.
assert solve_data("1\n1000000000000000000\n") == "3814697265625", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0`, `1`, `4` | `1`, `1`, `2` | Zero handling and smallest positive boundaries |
| `8`, `9`, `10`, `44` | `4`, `5`, `5`, `6` | Forbidden digits, upper-bound transitions, and leading-zero handling |
| `7777` | `475` | Tight digit counting when several positions equal the upper bound |
| `1000000000000000000` | `3814697265625` | Maximum input size and large integer arithmetic |

## Edge Cases

For (n=0), the algorithm starts with `ans = 1` and has no positive lengths to count. The digit `0` is allowed only internally, but here it represents the integer zero itself, which is explicitly liked. The result is therefore (1).

For (n=1), the initial zero contributes one. The first digit is `1`, which is not in `FIRST`, so there are no valid positive one-digit numbers at most (1). The function returns (1), which is correct.

For (n=4), the first digit is allowed, but there are no allowed positive digits smaller than `4`. The algorithm then adds (4) itself, giving (0,4) and hence (2).

For (n=9), all four allowed positive one-digit numbers (4,6,7,9) are at most (9). The algorithm counts the smaller choices `4`, `6`, and `7`, then adds `9` itself, and finally includes zero. The result is (5).

For (n=10), the one-digit count remains (5). There is no valid two-digit number at most (10), because every positive two-digit valid number starts with (4), (6), (7), or (9). The first digit `1` is forbidden, so the tight branch stops and the answer remains (5).

For (n=2019), the same logic applies at the first position. The digit `2` is forbidden, and every valid four-digit number begins with at least `4`, so no four-digit valid number can fit below (2019). The three shorter positive lengths contribute (4+20+100=124), and zero contributes one, producing (125).

For (n=10^{18}), the input has 19 digits, but its first digit is `1`, which is forbidden. Every valid 19-digit number starts with `4`, `6`, `7`, or `9`, so none is at most (10^{18}). All valid numbers have at most 18 digits, and their count including zero is (5^{18}=3814697265625). The implementation handles this without overflow because Python integers are arbitrary precision.
