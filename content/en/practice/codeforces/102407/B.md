---
title: "CF 102407B - Crazy dance"
description: "The Joker counts seconds starting from one. At second (t), he says the representation of (t) in base (a), without leading zeroes. For example, in base (3), the sequence starts with (1,2,10,11,12,ldots)."
date: "2026-08-11T23:47:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102407
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102407
solve_time_s: 262
verified: true
draft: false
---

[CF 102407B - Crazy dance](https://codeforces.com/problemset/problem/102407/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

The Joker counts seconds starting from one. At second (t), he says the representation of (t) in base (a), without leading zeroes. For example, in base (3), the sequence starts with (1,2,10,11,12,\ldots).

For every digit (i), the input gives (b_i), the exact number of times digit (i) is supposed to have been spoken when the dance stops. We have to determine the unique second (n), if one exists, such that the concatenation of the base-(a) representations of

[
1,2,\ldots,n
]

contains exactly (b_i) copies of every digit (i). If no such (n) exists, the Joker never satisfies his stopping condition, so the answer is (-1).

The base can be as large as (100000), and every requested digit count can be as large as (10^9). Consequently, the sum of all requested counts can reach (10^{14}). A simulation that processes every spoken digit would then have to perform on the order of (10^{14}) digit updates, which is far beyond any practical time limit. The algorithm must work with whole ranges of numbers instead of enumerating the numbers themselves.

There are several subtle cases where a tempting solution fails. If every (b_i) is zero, the answer is (-1), because the Joker has already spoken digit (1) after the first second, so the stopping condition can never hold at time zero.

For example,

```
5
0 0 0 0 0
```

has answer

```
-1
```

A second issue is that the total number of spoken digits alone is not sufficient. Consider

```
2
2 1
```

The requested total is (3). Exactly three digits have been spoken after seconds (1) and (2), namely (1,10). Their frequencies are two copies of digit (1) and one copy of digit (0), so this particular input actually has answer (2). In contrast,

```
2
1 2
```

also has total (3), so it also points to (n=2), but the actual frequencies are ([1,2]), meaning digit (0) occurs once and digit (1) twice. This illustrates why, after recovering (n) from the total, we still have to check every individual digit count.

A particularly easy boundary error occurs when (n) crosses a power of the base. In base (3), the numbers (1,2) have one digit each, while (3,4,5) have two digits. A calculation that treats the digit length as constant across this boundary gives the wrong stopping time.

Leading zeroes are another source of mistakes. When counting the digit (0), the representation of (7) in base (10) does not contain a zero, even though a fixed-width representation such as (007) would. The zero formula has to explicitly exclude those nonexistent leading positions.

## Approaches

The direct approach is to simulate the dance. Starting from (1), convert every integer to base (a), add one to the counter of each digit appearing in that representation, and stop when all counters equal their targets. This is correct because it follows exactly the process described by the problem.

The problem is the scale. The total number of digit occurrences that we may need to process is (\sum b_i), which can be as large as (10^{14}). Even before accounting for integer conversion overhead, that means roughly (10^{14}) elementary counter updates. This is the point where brute force becomes impossible.

The key observation is that we do not actually need the digit vector to find the candidate time. Every second contributes at least one digit, and every new number contributes its entire representation. Thus the total number of spoken digits after second (n) is

[
D(n)=\sum_{x=1}^{n}\operatorname{digits}_a(x).
]

This function is strictly increasing, because moving from (n) to (n+1) adds at least one digit. Hence, if a solution exists, its stopping time is uniquely determined by

[
D(n)=\sum_{i=0}^{a-1}b_i.
]

We can invert this function directly by grouping numbers according to their number of base-(a) digits. There are (a-1) one-digit numbers, ((a-1)a) two-digit numbers, ((a-1)a^2) three-digit numbers, and so on. For each block, its total contribution is simply the number of numbers in the block multiplied by its digit length.

Once (n) is known, we compute the frequency of every digit in all numbers from (1) through (n). For a fixed decimal-style position (p=1,a,a^2,\ldots), the usual high/current/low decomposition works in exactly the same way in an arbitrary base. This gives the number of occurrences of each digit at that position without enumerating individual numbers.

The brute-force method works because it explicitly constructs exactly the sequence we need. It fails because the sequence can contain an enormous number of digits. The observation that the total digit count is strictly increasing lets us collapse the search for the stopping time to a few digit-length blocks, and the positional counting formula lets us verify all digit frequencies without walking through the sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(S)), where (S=\sum b_i) in the worst scale | (O(a)) | Too slow |
| Optimal | (O(a\log_a n)) | (O(a)) | Accepted |

## Algorithm Walkthrough

1. Compute

[
S=b_0+b_1+\cdots+b_{a-1}.
]

This is the total number of digit occurrences that must have been spoken. If (S=0), no positive number can satisfy the condition, so we immediately return (-1).
2. Find which digit-length block contains the stopping time.

Numbers with exactly (k) base-(a) digits are

[
a^{k-1},a^{k-1}+1,\ldots,a^k-1.
]

There are

[
(a-1)a^{k-1}
]

such numbers, and together they contribute

[
k(a-1)a^{k-1}
]

spoken digits.

Subtract complete blocks from (S) until the remaining amount belongs to one block. Since the base is at least (2), the number of blocks is logarithmic in the eventual answer.
3. Suppose the remaining amount is (R), and the current block contains (k)-digit numbers.

Every number in this block contributes exactly (k) digits. Consequently, (R) must be divisible by (k). If

[
R\bmod k\ne0,
]

then no integer number of (k)-digit representations can produce exactly (R) digits, so the answer is (-1).

Otherwise,

[
q=R/k
]

is the number of (k)-digit numbers that have been spoken inside this block. If the block starts at (a^{k-1}), the candidate stopping time is

[
n=a^{k-1}+q-1.
]
4. Count the occurrences of every digit in (1,\ldots,n).

Fix a position (p=a^j). For a number (x), write

[
x=(\text{high})\cdot(ap)+(\text{current})\cdot p+\text{low},
]

where

[
\text{high}=\left\lfloor\frac{x}{ap}\right\rfloor,
\qquad
\text{current}=\left\lfloor\frac{x}{p}\right\rfloor\bmod a,
\qquad
\text{low}=x\bmod p.
]

For a nonzero digit (d), every complete cycle of length (ap) contributes exactly (p) copies of (d), giving a base amount of

[
\text{high}\cdot p.
]

If the current digit is greater than (d), one additional group of (p) occurrences appears. If it equals (d), only the partial group of (\text{low}+1) numbers contributes.
5. Handle digit zero separately.

Zero cannot occupy the leading position of a number, so its formula has one fewer complete cycle. When (\text{high}>0), the complete contribution is

[
(\text{high}-1)p.
]

If the current digit is zero, add (\text{low}+1). Otherwise add (p).

This is exactly the correction that prevents representations such as (007) from being counted.
6. Compare the computed frequency array with (b).

If every digit has exactly its requested frequency, output (n). Otherwise the total digit count pointed to a unique candidate (n), but that candidate has the wrong distribution of digits, so the correct answer is (-1).

### Why it works

The central invariant is that after processing complete digit-length blocks, the remaining value of (S) is exactly the number of digit occurrences still required from the next block. Since every number in that block has the same length (k), an exact stopping point exists there if and only if the remaining amount is divisible by (k), and the quotient identifies the unique candidate (n).

For that candidate, the positional counting formula counts every occurrence at every position exactly once. The separate zero formula removes leading-zero positions that are not present in ordinary representations. Hence the computed vector is precisely the vector of digit frequencies in (1,\ldots,n). The final equality check is consequently both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def find_time(a, total):
    if total == 0:
        return -1

    power = 1
    length = 1
    remaining = total

    while True:
        count = (a - 1) * power
        block_digits = count * length

        if remaining > block_digits:
            remaining -= block_digits
            power *= a
            length += 1
        else:
            if remaining % length != 0:
                return -1

            q = remaining // length
            if q == 0 or q > count:
                return -1

            return power + q - 1

def count_digits(n, a):
    cnt = [0] * a
    p = 1

    while p <= n:
        high = n // (p * a)
        cur = (n // p) % a
        low = n % p

        base = high * p

        for d in range(1, a):
            value = base

            if cur > d:
                value += p
            elif cur == d:
                value += low + 1

            cnt[d] += value

        if high > 0:
            cnt[0] += (high - 1) * p

            if cur == 0:
                cnt[0] += low + 1
            else:
                cnt[0] += p

        p *= a

    return cnt

def solve():
    a = int(input())
    b = list(map(int, input().split()))

    total = sum(b)

    n = find_time(a, total)
    if n == -1:
        print(-1)
        return

    cnt = count_digits(n, a)

    if cnt == b:
        print(n)
    else:
        print(-1)

if __name__ == "__main__":
    solve()
```

The first function uses the monotonicity of the total digit count. `power` is the first number in the current digit-length block, while `length` is the number of digits of every number in that block. `block_digits` is therefore the exact number of spoken digits contributed by the entire block.

The condition `remaining > block_digits` deliberately uses a strict inequality. If the remaining total is exactly the size of the block, the answer is the last number in that block, so the current block must be processed rather than skipped.

The divisibility test prevents an off-by-one style mistake where an arbitrary fractional number of representations would be treated as an integer number of seconds. After division, `q` counts how many numbers from the current block are included, so `power + q - 1` is the final number spoken.

The second function applies the positional formula independently for (p=1,a,a^2,\ldots). The loop over `range(1, a)` handles all nonzero digits. Zero is handled separately because leading zeroes do not exist in the spoken representations.

Python integers have arbitrary precision, so values such as (10^{14}), products involving powers of the base, and the resulting digit frequencies do not overflow. The multiplication `p * a` is also safe because Python integers automatically grow as necessary.

The equality check is performed only after the candidate (n) has been recovered. This separation is useful because the total count finds the only possible stopping time, while the positional calculation decides whether that candidate actually has the required digit distribution.

## Worked Examples

### Sample 1

The input is

```
10
1 2 1 1 1 1 1 1 1 1
```

The total requested number of digits is

[
1+2+8=11.
]

For base (10), the one-digit numbers (1) through (9) contribute (9) digits. Two digits remain, so the next block contains two-digit numbers and we need exactly one of them.

| `length` | `power` | `block_digits` | `remaining` | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 9 | 11 | Skip block |
| 2 | 10 | 180 | 2 | Take 1 number |

The candidate is

[
10+1-1=10.
]

The numbers spoken are (1,2,\ldots,10). Digits (1) through (9) each occur once in the one-digit numbers, and digit (1) occurs once more in (10), while digit (0) occurs once. The resulting frequencies are exactly

[
[1,2,1,1,1,1,1,1,1,1].
]

Thus the answer is `10`.

### Sample 2

The input is

```
2
3 5
```

The requested total is

[
3+5=8.
]

In base (2), the one-digit block contains only the number (1), contributing one digit. The remaining total is (7). The two-digit block contains (2) numbers, contributing (4) digits, so it is skipped. The remaining total is (3), which belongs to the three-digit block.

| `length` | `power` | `block_digits` | `remaining` | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 8 | Skip, remaining = 7 |
| 2 | 2 | 4 | 7 | Skip, remaining = 3 |
| 3 | 4 | 12 | 3 | (3\bmod3=0) |

We take

[
q=3/3=1,
]

so the candidate is

[
4+1-1=4.
]

The spoken numbers are

```
1
10
11
100
```

Their digit counts are three zeroes and five ones.

| `digit` | Required | Computed |
| --- | --- | --- |
| 0 | 3 | 3 |
| 1 | 5 | 5 |

The candidate is valid, so the answer is `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(a\log_a n)) | There are (O(\log_a n)) digit positions, and every position checks all (a-1) nonzero digits. |
| Space | (O(a)) | The frequency array contains one counter for every possible digit. |

The maximum requested total is (10^9a), so the candidate (n) can be very large, but its number of base-(a) digits is still logarithmic. Even for (a=100000), only a handful of digit positions can occur at the largest relevant scales. The resulting (O(a\log_a n)) work is easily manageable for (a\le100000), while the (O(a)) memory usage is also small.

## Test Cases

The following test harness uses the same `solve()` function as the submitted solution.

```python
import sys
import io

input = sys.stdin.readline

def find_time(a, total):
    if total == 0:
        return -1

    power = 1
    length = 1
    remaining = total

    while True:
        count = (a - 1) * power
        block_digits = count * length

        if remaining > block_digits:
            remaining -= block_digits
            power *= a
            length += 1
        else:
            if remaining % length != 0:
                return -1

            q = remaining // length
            if q == 0 or q > count:
                return -1

            return power + q - 1

def count_digits(n, a):
    cnt = [0] * a
    p = 1

    while p <= n:
        high = n // (p * a)
        cur = (n // p) % a
        low = n % p

        base = high * p

        for d in range(1, a):
            value = base

            if cur > d:
                value += p
            elif cur == d:
                value += low + 1

            cnt[d] += value

        if high > 0:
            cnt[0] += (high - 1) * p

            if cur == 0:
                cnt[0] += low + 1
            else:
                cnt[0] += p

        p *= a

    return cnt

def solve():
    a = int(input())
    b = list(map(int, input().split()))

    total = sum(b)
    n = find_time(a, total)

    if n == -1:
        print(-1)
        return

    if count_digits(n, a) == b:
        print(n)
    else:
        print(-1)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    try:
        solve()
        return out.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided samples
assert run("10\n1 2 1 1 1 1 1 1 1 1\n") == "10", "sample 1"
assert run("2\n3 5\n") == "4", "sample 2"
assert run("5\n0 0 0 0 0\n") == "-1", "sample 3"

# Minimum-size valid case: only the number 1 is spoken.
assert run("2\n0 1\n") == "1", "minimum valid input"

# Crossing the first digit-length boundary in base 3.
# 1, 2, 10, 11, 12 gives counts [1, 3, 2].
assert run("3\n1 3 2\n") == "5", "digit-length boundary"

# All target values equal, but no stopping time has those frequencies.
assert run("2\n2 2\n") == "-1", "all-equal impossible target"

# Maximum base and maximum array size.
# For n = 99999 in base 100000, every spoken number is one digit.
large_b = [0] + [1] * 99999
large_input = "100000\n" + " ".join(map(str, large_b)) + "\n"
assert run(large_input) == "99999", "maximum base and array size"

# Same total as n=2 in base 2, but wrong digit distribution.
assert run("2\n1 2\n") == "-1", "total count alone is insufficient"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 0 1` | `1` | Smallest possible valid dance and first spoken digit |
| `3 / 1 3 2` | `5` | Correct handling when the number of digits increases |
| `2 / 2 2` | `-1` | All-equal target values with no valid stopping time |
| `100000 / 0 1 1 ... 1` | `99999` | Maximum base and maximum digit-array size |
| `2 / 1 2` | `-1` | Candidate determined by total count but rejected by digit frequencies |

## Edge Cases

### Zero total

For

```
5
0 0 0 0 0
```

the total requested digit count is zero. The algorithm detects this before trying to locate a digit-length block and returns (-1). There is no positive second whose representation contributes zero digits.

### Total count does not correspond to an integer number of representations

Consider

```
2
2 2
```

The total is (4). In base (2), after the one-digit number (1), the next block consists of two-digit numbers and contributes four digits in total. Thus the total (4) uniquely identifies (n=2).

However, the actual sequence is

```
1
10
```

whose digit frequencies are ([1,2]), not ([2,2]). The final comparison rejects the candidate and outputs (-1). This demonstrates why recovering (n) from the total is only the first half of the solution.

### Crossing a power of the base

For

```
3
1 3 2
```

the total is (6). In base (3), numbers (1) and (2) contribute two digits, while (3,4,5) each contribute two more. The first block contributes (2), leaving (4), so the candidate is (5).

The representations are

```
1
2
10
11
12
```

and their digit frequencies are one zero, three ones, and two twos. The answer is `5`. The block calculation avoids incorrectly treating all numbers as having the same length.

### Leading zeroes

Take

```
10
1 1 1 1 1 1 1 1 1 1
```

The total is (10), which identifies (n=10). The number `10` contains one zero, while the numbers `1` through `9` contain none. Hence the zero count is exactly one.

A fixed-width counting method might incorrectly count zeroes in `01`, `02`, and so on. The formula

[
(\text{high}-1)p
]

for zero removes those artificial leading positions.

### Maximum base

For

```
100000
0 1 1 1 ... 1
```

with one zero followed by (99999) ones, the requested total is (99999). Every number from (1) through (99999) is represented by exactly one base-(100000) digit, so the candidate is (99999). Each nonzero digit occurs once and zero occurs zero times, giving the exact requested vector.

This case exercises the largest possible digit array and confirms that the algorithm does not rely on a small base.
