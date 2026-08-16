---
title: "CF 102277B - Parity of Strings"
description: "The task is to classify a lowercase string according to the parity of the frequency of every letter. A string is called even when every letter occurs an even number of times. It is called odd when every lowercase letter occurs an odd number of times."
date: "2026-08-16T19:32:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "B"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 58
verified: true
draft: false
---

[CF 102277B - Parity of Strings](https://codeforces.com/problemset/problem/102277/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to classify a lowercase string according to the parity of the frequency of every letter. A string is called even when every letter occurs an even number of times. It is called odd when every lowercase letter occurs an odd number of times. If neither condition holds, the answer is 2. The input contains one nonempty lowercase string of length at most 70, and the output is a single integer, 0 for an even string, 1 for an odd string, and 2 otherwise.

The small length bound changes the practical picture considerably. Even a solution that scans the entire string once for each of the 26 lowercase letters performs at most (26 \times 70 = 1820) character checks, which is trivial under the one-second limit. A single pass is still the cleaner solution because the required information is just the parity of each character's frequency.

The first edge case is a one-character string. For example, the input `a` should produce `1`, because `a` occurs once, while every other lowercase letter occurs zero times. Zero is even, and one is odd, so every letter has odd frequency only when every alphabet letter is present exactly an odd number of times. This means the correct result for `a` is actually `2`, not `1`. A careless implementation that checks only letters appearing in the string would incorrectly classify it as odd.

The second edge case is a string containing every lowercase letter exactly once. For example, `abcdefghijklmnopqrstuvwxyz` produces `1`. Every one of the 26 letters appears once, which is odd. An implementation that checks only whether all observed counts are odd can get this case right, while an implementation that forgets that absent letters have frequency zero will also incorrectly accept shorter strings such as `a`.

The third edge case is an all-equal string with an even length. For example, `aaaa` produces `0`, because `a` occurs four times and every other letter occurs zero times. A careless implementation that interprets "even" as merely having an even string length would happen to pass this example, but would fail on `aabbc`, whose length is also odd while its letter-frequency parities determine the actual classification.

## Approaches

A direct brute-force approach is to consider each of the 26 lowercase letters independently. For every letter, scan the whole string and count how many times that letter occurs. After all counts are known, check whether all 26 counts are even or whether all 26 counts are odd. This is correct because the definition depends only on the frequency parity of each letter. With the maximum string length of 70, the worst case performs exactly (26 \times 70 = 1820) character comparisons, plus a small amount of bookkeeping, so it is easily fast enough. There is no input size at which this particular brute-force method becomes problematic under the stated constraints.

The cleaner approach is to avoid rescanning the string. Maintain 26 counters, one for each lowercase letter, and increment the corresponding counter whenever a character is read. After one pass, inspect the parity of all 26 counters. If every counter is even, the answer is 0. Otherwise, if every counter is odd, the answer is 1. If neither condition holds, the answer is 2.

The key observation is that the actual frequency is irrelevant once its parity is known. We only need to distinguish zero, even, and odd through the parity of each count. Since the alphabet is fixed at 26 characters, checking all counters is constant work.

The brute-force works because the alphabet is tiny, but it repeatedly examines the same characters. The observation that all letters can be counted during one shared traversal removes this repetition and reduces the string processing to a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26n) = O(n) | O(26) = O(1) | Accepted |
| Optimal | O(n) | O(26) = O(1) | Accepted |

## Algorithm Walkthrough

1. Create an array `cnt` with 26 entries, initially all zero. Entry `i` stores the number of occurrences of the lowercase letter whose alphabet index is `i`.
2. Traverse every character `ch` in the string and increment `cnt[ord(ch) - ord('a')]`. This maps `a` through `z` to indices 0 through 25 without needing a dictionary.
3. Check whether every value in `cnt` is even. If so, print `0`, because every lowercase letter occurs an even number of times.
4. If the string is not even, check whether every value in `cnt` is odd. If so, print `1`, because every lowercase letter occurs an odd number of times.
5. If neither condition holds, print `2`. At least one letter has even frequency and at least one letter has odd frequency, so the string is neither even nor odd.

The invariant is that after processing any prefix of the string, `cnt[i]` is exactly the number of occurrences of the corresponding letter in that prefix. After the entire string has been processed, the array therefore contains the exact frequency of every lowercase letter. The two final parity checks directly match the definitions of the two special classifications, so the remaining case must be 2.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    cnt = [0] * 26

    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    if all(x % 2 == 0 for x in cnt):
        print(0)
    elif all(x % 2 == 1 for x in cnt):
        print(1)
    else:
        print(2)

if __name__ == "__main__":
    solve()
```

The first line reads the only string and removes the trailing newline. The input is guaranteed to contain lowercase letters, so no additional validation is necessary.

The `cnt` array corresponds directly to the 26 letters. The expression `ord(ch) - ord('a')` converts `a` to 0, `b` to 1, and so on through `z` to 25. Every character is processed exactly once.

The first `all` checks the even condition for the entire alphabet, including letters that do not appear. An absent letter has count zero, and zero is even, so those letters must be included in the test.

The second `all` checks the odd condition. This is why a string such as `a` is not classified as odd: the other 25 letters have count zero, which is even.

There are no integer-overflow concerns in Python, and the maximum count is only 70. The input contains a single test case, so no test-case loop is required.

## Worked Examples

For Sample 1, the string is `coachessoaehwwwwww`. The relevant frequency counts are shown below.

| Character | Count | Parity |
| --- | --- | --- |
| a | 1 | odd |
| c | 1 | odd |
| e | 2 | even |
| h | 1 | odd |
| o | 2 | even |
| s | 2 | even |
| w | 6 | even |
| all other letters | 0 | even |

The string contains both odd and even frequencies, so it is neither even nor odd. The output is `2`.

For Sample 2, the string is `coachesc`.

| Character | Count | Parity |
| --- | --- | --- |
| a | 1 | odd |
| c | 2 | even |
| e | 2 | even |
| h | 1 | odd |
| o | 1 | odd |
| s | 1 | odd |
| all other letters | 0 | even |

Again, the frequency parities are mixed. The output is `2`.

The other supplied sample input `coachessoaehwwwwww` has every letter count even, so it produces `0`. The sample `coachesarefun` has mixed parity and produces `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once, followed by a constant-size check over 26 letters. |
| Space | O(1) | The frequency array always contains exactly 26 counters. |

With (n \le 70), the algorithm performs only a few dozen character operations and a constant number of parity checks. It is comfortably within the one-second time limit and uses negligible memory compared with the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    s = input().strip()

    cnt = [0] * 26

    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    if all(x % 2 == 0 for x in cnt):
        print(0)
    elif all(x % 2 == 1 for x in cnt):
        print(1)
    else:
        print(2)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        solve()
        result = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return result
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run("coachessoaehwwwwww\n") == "0\n", "sample 1"
assert run("coachesarefun\n") == "2\n", "sample 2"
assert run("coachessoaehwwwwww\n") == "0\n", "sample 3"
assert run("coachesc\n") == "2\n", "sample 4"

# Minimum-size input
assert run("a\n") == "2\n", "single character"

# All 26 letters occur exactly once
assert run("abcdefghijklmnopqrstuvwxyz\n") == "1\n", "every letter once"

# All equal, even frequency
assert run("aaaa\n") == "0\n", "all equal with even count"

# Boundary length, all characters occur an even number of times
assert run("aabbccddeeffgghhiijjkkllmm\n") == "0\n", "26-letter boundary"

# Mixed parity
assert run("aab\n") == "2\n", "mixed frequency parity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `2` | Minimum length and the requirement to consider absent letters |
| `abcdefghijklmnopqrstuvwxyz` | `1` | Every alphabet character has odd frequency |
| `aaaa` | `0` | All-equal string with an even frequency |
| `aabbccddeeffgghhiijjkkllmm` | `0` | All 26 letters present with even frequencies |
| `aab` | `2` | Mixture of even and odd frequencies |

## Edge Cases

For the single-character input `a`, the algorithm creates counts with `a = 1` and every other letter equal to zero. The even test fails because `a` has odd frequency. The odd test also fails because the other 25 letters have frequency zero. The result is `2`, which avoids the common mistake of checking only characters that appear.

For the input `abcdefghijklmnopqrstuvwxyz`, every counter is exactly one. The even test fails for every letter, while the odd test succeeds for all 26 counters. The result is `1`. This exercises the full alphabet and confirms that the algorithm does not accidentally ignore letters near the end of the alphabet.

For `aaaa`, the counter for `a` becomes four and every other counter remains zero. All 26 counts are even, so the result is `0`. The case also confirms that the algorithm checks frequencies rather than the number of distinct characters.

For `aabbccddeeffgghhiijjkkllmm`, every lowercase letter appears exactly twice. Every counter is even, including all letters explicitly represented in the input, so the result is `0`. This is a useful boundary case because it contains the entire alphabet while keeping every frequency even.

For `aab`, the frequencies are `a = 2`, `b = 1`, and all remaining letters equal to zero. Some counts are even and some are odd, so neither global condition holds and the algorithm prints `2`. This catches implementations that incorrectly decide the answer from the parity of the total string length instead of the parity of each individual letter frequency.
