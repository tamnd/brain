---
title: "CF 105129A - Khepri and the Counting Problem"
description: "For each test case, we are given a positive integer n. We must count how many positive integers in the range from 1 to n have an odd number of decimal digits. The value of n can be as large as 10^18. That immediately rules out any solution that examines every number individually."
date: "2026-06-27T19:23:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105129
codeforces_index: "A"
codeforces_contest_name: "Shorouk Academy 2024 Collegiate Programming Contest"
rating: 0
weight: 105129
solve_time_s: 167
verified: true
draft: false
---

[CF 105129A - Khepri and the Counting Problem](https://codeforces.com/problemset/problem/105129/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we are given a positive integer `n`. We must count how many positive integers in the range from `1` to `n` have an odd number of decimal digits.

The value of `n` can be as large as `10^18`. That immediately rules out any solution that examines every number individually. Even a loop over the first billion numbers would already be far too slow, while the largest input contains one quintillion possible values. The algorithm must depend only on the number of digits of `n`, which is at most `19`.

The decimal representation naturally groups numbers by their digit count. Every number with the same number of digits forms one continuous interval, so instead of counting individual numbers, we can count whole digit-length ranges.

One easy place to make a mistake is when `n` lies inside an odd-length range rather than at its end.

For example:

```
n = 234
```

The correct answer is:

```
9 + (99 - 10 + 1) + (234 - 100 + 1)
= 9 + 90 + 135
= 234
```

A careless implementation that counts only complete digit ranges would count only one-digit numbers and return `9`, missing the partial three-digit range.

Another common mistake happens exactly at powers of ten.

For example:

```
n = 100
```

The answer is:

```
9 + 1 = 10
```

The number `100` is the first three-digit number, so it must be included. Using `<` instead of `<=` when computing the last range would incorrectly return `9`.

The largest inputs also deserve attention.

For example:

```
n = 10^18
```

This is a 19-digit number. Although there is only one such number up to `10^18`, it still contributes to the answer because 19 is odd. Languages with fixed-size integers could overflow while computing powers of ten, but Python integers grow automatically.

## Approaches

The most direct solution is to iterate through every integer from `1` to `n`, compute its number of decimal digits, and increase the answer whenever that digit count is odd. This method is obviously correct because every candidate is checked exactly once.

Its running time is `O(n)`. With `n` reaching `10^18`, this would require roughly one quintillion iterations, making it completely infeasible.

The key observation is that numbers with the same number of digits always form one contiguous interval.

The interval of `d`-digit numbers is:

```
[10^(d-1), 10^d - 1]
```

except that one-digit numbers start at `1`.

Whenever `d` is odd, every number in that interval contributes to the answer. If the entire interval lies below `n`, we simply add its size. If `n` falls inside that interval, we only add the prefix ending at `n`.

Since a number up to `10^18` has at most `19` digits, there are only `19` possible digit lengths to inspect. This reduces the work for each test case to a tiny constant amount.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the value of `n`.
2. Compute the number of decimal digits in `n`. This determines how many digit lengths need to be considered.
3. Initialize the answer to zero.
4. Iterate through every digit length `d` from `1` up to the digit count of `n`.
5. Skip even values of `d`, since only odd digit lengths contribute.
6. Compute the smallest number having `d` digits. This is `1` when `d = 1`, otherwise it is `10^(d-1)`.
7. Compute the largest number that should be counted for this digit length. It is the smaller of `n` and `10^d - 1`.
8. If the computed upper bound is at least the lower bound, add the interval size `upper - lower + 1` to the answer. This correctly handles both complete ranges and the final partial range.
9. Output the accumulated answer.

### Why it works

Each positive integer belongs to exactly one digit-length interval. The algorithm visits every odd digit length exactly once and counts precisely the numbers from that interval that do not exceed `n`. No number is omitted because every eligible interval is processed. No number is counted twice because different digit lengths correspond to disjoint intervals. The final sum is exactly the number of integers from `1` to `n` whose decimal representation has an odd number of digits.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        digits = len(str(n))
        ans = 0

        for d in range(1, digits + 1, 2):
            if d == 1:
                low = 1
            else:
                low = 10 ** (d - 1)

            high = min(n, 10 ** d - 1)

            if high >= low:
                ans += high - low + 1

        print(ans)

solve()
```

The solution begins by reading all test cases. For each value of `n`, it determines how many decimal digit lengths must be examined.

The loop advances by two each time, so only odd digit lengths are processed. This avoids unnecessary work and directly reflects the problem requirement.

For each odd digit length, the code computes the interval occupied by numbers of that length. The lower bound requires special handling for one-digit numbers because they begin at `1` instead of `10^0`.

The upper bound is the smaller of `n` and the largest number having that many digits. When `n` lies inside the current interval, this naturally counts only the valid prefix.

The condition `high >= low` prevents adding a negative interval size. This happens when `n` has fewer digits than the current range.

Python integers automatically support values beyond `10^18`, so computing powers of ten is completely safe.

## Worked Examples

### Example 1

Suppose:

```
n = 234
```

| Digit length | Lower bound | Upper bound | Numbers added | Running answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 9 | 9 | 9 |
| 3 | 100 | 234 | 135 | 144 |

The answer is `144`.

This example shows how complete odd-length ranges and one partial odd-length range are combined into a single result.

### Example 2

Suppose:

```
n = 100000
```

| Digit length | Lower bound | Upper bound | Numbers added | Running answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 9 | 9 | 9 |
| 3 | 100 | 999 | 900 | 909 |
| 5 | 10000 | 99999 | 90000 | 90909 |

The answer is `90909`.

This trace demonstrates that whenever an entire odd-length interval fits inside the limit, the algorithm adds the whole interval at once instead of inspecting individual numbers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | At most 19 digit lengths are examined. |
| Space | O(1) | Only a few integer variables are maintained. |

The running time depends only on the number of decimal digits, not on the magnitude of `n`. Since `10^18` has only `19` digits, each test case performs only a handful of arithmetic operations, easily satisfying the limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        digits = len(str(n))
        ans = 0

        for d in range(1, digits + 1, 2):
            low = 1 if d == 1 else 10 ** (d - 1)
            high = min(n, 10 ** d - 1)
            if high >= low:
                ans.append if False else None
                ans += high - low + 1

        out.append(str(ans))

    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    res = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return res

# minimum input
assert run("1\n1\n") == "1\n"

# boundary at first two-digit number
assert run("1\n10\n") == "9\n"

# boundary at first three-digit number
assert run("1\n100\n") == "10\n"

# end of three-digit range
assert run("1\n999\n") == "909\n"

# maximum constraint
assert run("1\n1000000000000000000\n") == "909090909090909091\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum input value |
| `10` | `9` | Transition from one to two digits |
| `100` | `10` | First three-digit number is included |
| `999` | `909` | Entire three-digit range is counted |
| `10^18` | `909090909090909091` | Largest allowed input |

## Edge Cases

Consider the transition to a new odd digit length.

```
Input
1
100
```

The algorithm processes one-digit numbers first and adds `9`. For three-digit numbers, the interval becomes `[100, 100]`, contributing one more value. The final answer is `10`, correctly including the first three-digit number.

Now consider a value inside an odd-length interval.

```
Input
1
234
```

The one-digit interval contributes `9`. The three-digit interval becomes `[100, 234]`, whose size is `135`. Adding them produces `144`. The algorithm automatically truncates the last interval at `n`, so no larger three-digit numbers are counted.

Finally, consider the largest possible input.

```
Input
1
1000000000000000000
```

The algorithm counts every complete odd-digit interval from one digits through seventeen digits. It then processes the nineteen-digit interval, which is simply `[10^18, 10^18]`, adding one final value. Since Python integers have arbitrary precision, all arithmetic remains correct without overflow.
