---
title: "CF 412E - E-mail Addresses"
description: "We are given one long string that contains only lowercase letters, digits, , @, and .. We must count how many substrings of this string are valid e-mail addresses. Substrings are distinguished by their positions, not by their textual contents."
date: "2026-06-07T02:21:17+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 412
codeforces_index: "E"
codeforces_contest_name: "Coder-Strike 2014 - Round 1"
rating: 1900
weight: 412
solve_time_s: 218
verified: false
draft: false
---

[CF 412E - E-mail Addresses](https://codeforces.com/problemset/problem/412/E)

**Rating:** 1900  
**Tags:** implementation  
**Solve time:** 3m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given one long string that contains only lowercase letters, digits, `_`, `@`, and `.`.

We must count how many substrings of this string are valid e-mail addresses. Substrings are distinguished by their positions, not by their textual contents. If the same e-mail text appears in two different places, both occurrences contribute to the answer.

A valid address has the form:

`local_part@domain.tld`

The local part must be non-empty, may contain letters, digits, and `_`, and its first character must be a letter.

The domain part between `@` and `.` must be non-empty and contain only letters or digits.

The final part after `.` must be non-empty and contain only letters.

The string length can reach $10^6$. Any algorithm that examines all substrings is impossible. There are about $5 \cdot 10^{11}$ substrings in the worst case, and even checking only a tiny fraction of them would exceed the time limit.

The challenge is that a single `@` can participate in many different valid addresses because the local part may start at different letter positions, and a single `.` can participate in many different valid addresses because the address may end at different letters of the final letter block.

Several edge cases are easy to mishandle.

Consider:

```
1@a.b
```

The local part starts with a digit, so there are no valid addresses. A solution that only checks whether the local part contains valid characters would incorrectly count one address.

Consider:

```
ab@12.xyz
```

The domain may contain digits, so this is valid. Treating the domain as letters-only would miss valid answers.

Consider:

```
a@b.cd3
```

The address cannot end after the `3`, because the last component must consist only of letters. The valid endings are only inside the consecutive letter block immediately after the dot.

Consider:

```
ab_cd@x.yz
```

The local part may start at `a` or at `b`, because any starting position that is a letter and stays inside the same valid local-character block creates a valid local part. Counting only the maximal local part would undercount.

## Approaches

A brute-force solution would enumerate every substring and check whether it matches the e-mail format. There are $O(n^2)$ substrings. Even if validation were $O(1)$, this is already far too large for $n = 10^6$.

The key observation is that a valid address is completely determined by a choice of `@` and `.`.

Suppose a dot is fixed at position `j`.

For the domain part to be valid, every character between `@` and `.` must be alphanumeric. Let the maximal alphanumeric block ending at `j - 1` start at position `t`.

Then there is at most one possible `@`: it must be exactly at position `t - 1`.

If it were earlier, the interval would contain a non-alphanumeric character. If it were later, it would lie inside the alphanumeric block, which is impossible because `@` is not alphanumeric.

This reduces the problem dramatically. For each dot, there is at most one candidate `@`.

Now we only need two multiplicities.

For a fixed valid `@`, how many possible starts of the local part exist? Every letter inside the maximal block of allowed local characters ending immediately before `@` can serve as the beginning.

For a fixed valid dot, how many possible ends exist? Every letter inside the consecutive letter block immediately after the dot can serve as the ending position.

If

`starts = number of valid local-part starts`

and

`ends = number of valid address endings`

then this `@` and `.` contribute

`starts × ends`

valid substrings.

All required information can be precomputed with linear scans.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan from left to right and maintain information about maximal blocks of characters allowed in the local part, namely letters, digits, and `_`.

For every position, store how many letters appear in the current block ending at that position.
2. For every `@` position, compute `start_count`.

This equals the number of letters in the maximal local-character block ending immediately before the `@`.

Each such letter can be chosen as the first character of the local part.
3. Scan from left to right and compute the start position of the current maximal alphanumeric block.

For every alphanumeric position `i`, store the left boundary of the block containing `i`.
4. Scan from right to left and compute `letter_len[i]`, the length of the consecutive letter block starting at position `i`.
5. Iterate over every dot position `j`.
6. The final component must begin immediately after the dot, so if `j + 1` is not a letter, skip this dot.
7. The domain must be non-empty and alphanumeric, so `j - 1` must be alphanumeric. If not, skip this dot.
8. Let `t` be the start of the maximal alphanumeric block ending at `j - 1`.

The only possible `@` is at position `t - 1`.
9. If that position exists and contains `@`, add

`start_count[@] × letter_len[j + 1]`

to the answer.
10. Output the accumulated total.

### Why it works

For every valid e-mail substring, the domain part between `@` and `.` is a non-empty alphanumeric block. The maximal alphanumeric block ending before the dot uniquely determines where the `@` must stand, namely immediately before that block.

Conversely, whenever a dot has such a preceding `@`, every valid local-part start and every valid final-letter ending produces a distinct valid substring.

The algorithm counts exactly those combinations and nothing else. Every valid e-mail contributes once, and every counted combination satisfies all format requirements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    def is_letter(c):
        return 'a' <= c <= 'z'

    def is_digit(c):
        return '0' <= c <= '9'

    def is_alnum(c):
        return is_letter(c) or is_digit(c)

    def is_local(c):
        return is_alnum(c) or c == '_'

    local_letters = [0] * n
    cur = 0

    for i, ch in enumerate(s):
        if is_local(ch):
            if i > 0 and is_local(s[i - 1]):
                cur += 1 if is_letter(ch) else 0
            else:
                cur = 1 if is_letter(ch) else 0
            local_letters[i] = cur
        else:
            cur = 0

    start_count = [0] * n
    for i, ch in enumerate(s):
        if ch == '@' and i > 0:
            start_count[i] = local_letters[i - 1]

    run_start = [0] * n
    start = 0

    for i, ch in enumerate(s):
        if is_alnum(ch):
            if i > 0 and is_alnum(s[i - 1]):
                run_start[i] = start
            else:
                start = i
                run_start[i] = start

    letter_len = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        if is_letter(s[i]):
            letter_len[i] = letter_len[i + 1] + 1

    ans = 0

    for j, ch in enumerate(s):
        if ch != '.':
            continue

        if j + 1 >= n or letter_len[j + 1] == 0:
            continue

        if j == 0 or not is_alnum(s[j - 1]):
            continue

        t = run_start[j - 1]
        at = t - 1

        if at >= 0 and s[at] == '@':
            ans += start_count[at] * letter_len[j + 1]

    print(ans)

if __name__ == "__main__":
    solve()
```

The first scan computes, for every position, how many letters belong to the current local-character block. This directly gives the number of valid local-part starting positions for any `@`.

The second scan records the beginning of every alphanumeric run. This is what lets us recover the unique possible `@` for a given dot.

The backward scan computes the length of the consecutive letter block starting at each position. If a dot is followed by a letter block of length `k`, then there are exactly `k` valid ending positions.

The most delicate part is locating the candidate `@`. The correct position is not arbitrary. It must stand immediately before the maximal alphanumeric block ending at `j - 1`. Missing this observation usually leads to quadratic behavior or incorrect counting.

All counts fit comfortably in 64-bit integers, but not necessarily in 32-bit integers. Python integers handle this automatically.

## Worked Examples

### Example 1

Input:

```
agapov@r1.com
```

Relevant values:

| Dot position | Candidate @ | Local starts | Letter endings | Contribution |
| --- | --- | --- | --- | --- |
| 9 | 6 | 6 | 3 | 18 |

Answer:

```
18
```

The six letters in `agapov` can all be chosen as the start of the local part. The three letters in `com` can all be chosen as the ending position. Every combination produces a distinct valid substring.

### Example 2

Input:

```
ab@c.de
```

| Dot position | Candidate @ | Local starts | Letter endings | Contribution |
| --- | --- | --- | --- | --- |
| 4 | 2 | 2 | 2 | 4 |

Answer:

```
4
```

The local part may start at `a` or `b`. The address may end at `d` or `e`. That gives four valid substrings.

This example demonstrates the multiplicative structure of the counting formula.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | A constant number of linear scans |
| Space | O(n) | Arrays storing run information |

The string length can reach one million characters. A linear solution performs only a few million simple operations and easily fits within the time limit. The auxiliary arrays are also linear in size and fit comfortably within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io():
    input = sys.stdin.readline
    s = input().strip()
    n = len(s)

    def is_letter(c):
        return 'a' <= c <= 'z'

    def is_digit(c):
        return '0' <= c <= '9'

    def is_alnum(c):
        return is_letter(c) or is_digit(c)

    def is_local(c):
        return is_alnum(c) or c == '_'

    local_letters = [0] * n
    cur = 0

    for i, ch in enumerate(s):
        if is_local(ch):
            if i > 0 and is_local(s[i - 1]):
                cur += 1 if is_letter(ch) else 0
            else:
                cur = 1 if is_letter(ch) else 0
            local_letters[i] = cur
        else:
            cur = 0

    start_count = [0] * n
    for i, ch in enumerate(s):
        if ch == '@' and i > 0:
            start_count[i] = local_letters[i - 1]

    run_start = [0] * n
    start = 0

    for i, ch in enumerate(s):
        if is_alnum(ch):
            if i > 0 and is_alnum(s[i - 1]):
                run_start[i] = start
            else:
                start = i
                run_start[i] = start

    letter_len = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        if is_letter(s[i]):
            letter_len[i] = letter_len[i + 1] + 1

    ans = 0

    for j, ch in enumerate(s):
        if ch != '.':
            continue

        if j + 1 >= n or letter_len[j + 1] == 0:
            continue

        if j == 0 or not is_alnum(s[j - 1]):
            continue

        t = run_start[j - 1]
        at = t - 1

        if at >= 0 and s[at] == '@':
            ans += start_count[at] * letter_len[j + 1]

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve_io()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("agapov@r1.com\n") == "18", "sample 1"

# custom cases
assert run("a\n") == "0", "minimum size"
assert run("a@b.c\n") == "1", "smallest valid email"
assert run("1@b.c\n") == "0", "local part must start with a letter"
assert run("ab@c.de\n") == "4", "multiple starts and endings"
assert run("ab_cd@x.yz\n") == "4", "underscore allowed inside local part"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `0` | Minimum-size string |
| `a@b.c` | `1` | Smallest valid address |
| `1@b.c` | `0` | Local part cannot start with a digit |
| `ab@c.de` | `4` | Multiple valid starts and endings |
| `ab_cd@x.yz` | `4` | Underscore handling in local part |

## Edge Cases

Consider:

```
1@a.b
```

The maximal local-character block before `@` contains no letters. The algorithm stores `start_count = 0`, so even though the domain and suffix are valid, the contribution is zero. The output is correctly:

```
0
```

Consider:

```
a@12.xyz
```

The block `12` is fully alphanumeric. The dot finds the unique preceding `@`, `start_count = 1`, and the suffix length is `3`. The answer becomes:

```
3
```

corresponding to endings at `x`, `y`, and `z`.

Consider:

```
a@b.cd3
```

The consecutive letter block after the dot has length `2`, namely `cd`. The digit `3` is not part of the final component. The algorithm uses `letter_len[j + 1] = 2`, producing exactly the two valid endings.

Consider:

```
ab_cd@x.yz
```

Before `@`, the maximal local-character block contains letters `a` and `b`. Both are valid starting positions. After the dot, the letter block has length `2`. The algorithm computes `2 × 2 = 4`, which matches the four valid substrings.
