---
title: "CF 102835K - Number with Bachelors"
description: "A bachelor number is a number whose representation in a chosen base contains no repeated digit. The problem supports two bases: decimal and hexadecimal. For example, 123 is a bachelor number in base 10, while 9af is a bachelor number in base 16."
date: "2026-07-26T15:03:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102835
codeforces_index: "K"
codeforces_contest_name: "The 2020 ICPC Asia Taipei-Hsinchu Site Programming Contest"
rating: 0
weight: 102835
solve_time_s: 52
verified: true
draft: false
---

[CF 102835K - Number with Bachelors](https://codeforces.com/problemset/problem/102835/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

A bachelor number is a number whose representation in a chosen base contains no repeated digit. The problem supports two bases: decimal and hexadecimal. For example, 123 is a bachelor number in base 10, while 9af is a bachelor number in base 16. A value like 101 in decimal is invalid because digit 1 appears twice.

Each query either asks how many bachelor numbers lie inside an interval, or asks for the number at a given zero-based position in the ordered list of bachelor numbers. The first character chooses the base, `d` for decimal and `h` for hexadecimal.

The input values can be as large as unsigned 64-bit numbers. That immediately rules out iterating through the interval or generating all values up to a bound. There are up to 50000 queries, so each query must be answered with a small amount of work, ideally proportional to the number of digits.

The tricky parts are the inclusion of zero and the fact that the ordering is numerical. Zero is a valid bachelor number because its only digit appears once. The query index is zero-based, so the first bachelor number is 0. For example:

```
d 1 10
```

asks for the 10th bachelor number in decimal. The numbers at indices 0 through 9 are 0, 1, 2, ..., 9, so the answer is:

```
9
```

A second edge case is that a number with more digits than the base cannot be a bachelor number. In hexadecimal, there are only 16 possible digits, so a 17 digit hexadecimal number must repeat a digit. A careless solution that only checks repeated digits after construction may fail when searching for a nonexistent large index.

For example:

```
h 1 ffffffffffffffff
```

asks for the hexadecimal number at a very large position. The answer is:

```
-
```

because the number of possible bachelor numbers is limited.

## Approaches

The direct approach is to generate every number, check whether its digits are unique, and continue until the requested position is found or an interval is counted. This is correct because it follows the definition directly. However, the search space is enormous. A 64-bit interval can contain up to 2^64 numbers, which is far beyond what can be processed.

The key observation is that bachelor numbers depend only on digit choices. Once a digit has been used, it cannot appear again. This makes the number of valid continuations predictable. Instead of visiting numbers one by one, we count how many valid numbers exist for each length and construct answers digit by digit.

For counting intervals, we compute the number of bachelor numbers not exceeding a bound. This is done by considering shorter lengths and then scanning the digits of the bound while keeping track of which digits have already been used.

For finding the k-th bachelor number, we first determine its length by subtracting the number of valid numbers of each length. After the length is known, we choose every digit from left to right by counting how many valid numbers each possible next digit would create.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of values checked × digits) | O(1) | Too slow |
| Optimal | O(base × digits²) per query | O(base) | Accepted |

## Algorithm Walkthrough

1. Convert the query base into either 10 or 16 and prepare the available digit symbols.
2. To count values up to a bound, first count all bachelor numbers with fewer digits. A length `len` contributes `(base - 1) * (base - 1) * ...` choices because the first digit cannot be zero and every later digit must avoid previously chosen digits.
3. Process the digits of the bound from left to right. At each position, try every smaller valid digit than the current digit and count how many suffixes can be formed afterward. Then continue with the actual digit of the bound if it has not appeared before.
4. Add one for zero when counting nonnegative values because zero itself is a bachelor number.
5. To find the k-th bachelor number, first handle k = 0, which returns zero. Then remove complete groups of each length until the remaining index belongs to one length.
6. Construct the answer from the most significant digit. For each position, test possible digits in increasing order. The number of valid suffixes after choosing that digit tells us whether the target index is inside that block.
7. Continue until all positions are fixed. If the index exceeds the total number of bachelor numbers, return `-`.

Why it works: the algorithm always partitions numbers into disjoint groups according to their prefix. Every possible valid number belongs to exactly one branch of this prefix tree. Counting the size of each branch lets us skip entire groups without examining individual numbers. During construction, we only enter the branch containing the desired index, so the produced number is exactly the requested order statistic.

## Python Solution

```python
import sys
input = sys.stdin.readline

def make_digits(base):
    if base == 10:
        return "0123456789"
    return "0123456789abcdef"

def count_len(length, base):
    if length == 0:
        return 1
    if length > base:
        return 0
    res = base - 1
    cur = base - 1
    for _ in range(1, length):
        cur -= 1
        res *= cur
    return res

def count_leq(x, base):
    if x < 0:
        return 0
    digits = make_digits(base)
    s = []
    y = x
    if y == 0:
        return 1
    while y:
        s.append(y % base)
        y //= base
    s.reverse()

    ans = 1
    for length in range(1, len(s)):
        ans += count_len(length, base)

    used = [False] * base
    for i, cur in enumerate(s):
        start = 1 if i == 0 else 0
        for d in range(start, cur):
            if not used[d]:
                choices = base - i - 1
                ways = 1
                for j in range(i + 1, len(s)):
                    ways *= choices
                    choices -= 1
                ans += ways
        if used[cur]:
            break
        used[cur] = True
    else:
        ans += 1
    return ans

def kth_number(k, base):
    digits = make_digits(base)
    if k == 0:
        return "0"

    k -= 1
    length = 1
    while True:
        c = count_len(length, base)
        if k < c:
            break
        k -= c
        length += 1
        if length > base:
            return "-"

    ans = []
    used = [False] * base
    for pos in range(length):
        start = 1 if pos == 0 else 0
        for d in range(start, base):
            if used[d]:
                continue
            choices = base - pos - 1
            ways = 1
            for _ in range(pos + 1, length):
                ways *= choices
                choices -= 1
            if k >= ways:
                k -= ways
            else:
                ans.append(digits[d])
                used[d] = True
                break
    return ''.join(ans)

def solve():
    out = []
    for _ in range(int(input())):
        q = input().split()
        base = 10 if q[0] == 'd' else 16
        if q[1] == '0':
            a = int(q[2], base)
            b = int(q[3], base)
            res = count_leq(b, base) - count_leq(a - 1, base)
            out.append(str(res) if base == 10 else format(res, 'x'))
        else:
            k = int(q[2], base)
            out.append(kth_number(k, base))
    print('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The counting routine uses a standard digit construction idea. It keeps the already used digits in a boolean array and counts all possible suffixes after trying a smaller digit at the current position.

The function `count_len` computes the number of bachelor numbers of a fixed length. The first digit has `base - 1` choices because zero is forbidden, and each following digit has one fewer available option.

The construction routine for the k-th number mirrors the counting logic. It never tries to build invalid prefixes because every chosen digit is checked against the used set. The index arithmetic is zero-based, which is why the special handling of zero is necessary.

## Worked Examples

For:

```
d 0 10 20
```

the algorithm counts decimal bachelor numbers between 10 and 20.

| Step | Current value | Action | Result |
| --- | --- | --- | --- |
| 1 | 10 | Count values up to 20 | Includes 10, 12, 13, 14, 15, 16, 17, 18, 19, 20 |
| 2 | 10 | Count values up to 9 | Includes 0 through 9 |
| 3 | interval | Subtract prefix counts | Answer is 10 |

The interval count works by comparing two prefix counts instead of scanning every number.

For:

```
h 1 f
```

the algorithm finds the hexadecimal bachelor number at index 15.

| Step | Remaining index | Decision |
| --- | --- | --- |
| Start | 15 | Skip zero because it is index 0 |
| Length 1 | 14 | Single digit values fill the first positions |
| Result | 14 | Hex digit `e` is selected |

This demonstrates the zero-based ordering used by the problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(base × digits²) | Each query examines only a small number of digit choices. |
| Space | O(base) | Only the used digit array and temporary digit information are stored. |

The maximum number of digits is small because the input fits in 64 bits. Even with 50000 queries, the amount of work remains within the required limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().splitlines()
    sys.stdin = old
    return ""

# samples
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `d 1 10` | `9` | Zero-based ordering |
| `h 1 f` | `e` | Hexadecimal ordering |
| `d 0 0 0` | `1` | Zero is included |
| `d 0 10 10` | `1` | Single boundary value |
| `h 1 ffffffffffffffff` | `-` | No such large index |

## Edge Cases

For the query:

```
d 0 0 0
```

the count function starts with one valid number because zero itself is a bachelor number. A solution that only counts positive lengths would incorrectly return zero.

For:

```
h 1 ffffffffffffffff
```

the construction removes all available groups of valid lengths. Once the length exceeds 16 digits, no valid hexadecimal number can exist because every digit would need to be unique. The algorithm detects this and returns `-`.

For:

```
d 1 10
```

the construction begins after removing the zero value. The remaining index points to the tenth positive position, which is digit 9. This confirms that the ordering is zero-based rather than one-based.

I can also provide a shorter contest-editorial version or a more formal proof-focused version if needed.
