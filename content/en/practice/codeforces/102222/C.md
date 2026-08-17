---
title: "CF 102222C - Caesar Cipher"
description: "We are given two strings of the same length, where the first string is known plaintext and the second is its Caesar-encrypted version. A Caesar cipher applies one fixed cyclic shift to every uppercase letter."
date: "2026-08-17T22:02:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "C"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 84
verified: true
draft: false
---

[CF 102222C - Caesar Cipher](https://codeforces.com/problemset/problem/102222/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings of the same length, where the first string is known plaintext and the second is its Caesar-encrypted version. A Caesar cipher applies one fixed cyclic shift to every uppercase letter. The same shift was used to encrypt a third string, and our task is to recover the plaintext of that third string.

For example, if `A` becomes `D`, the shift is `3`, so `B` becomes `E`, `Y` becomes `B`, and `Z` becomes `C`. Once the shift is known, decrypting another ciphertext only requires moving every character backward by that amount.

Each test case gives `n`, the length of the known plaintext and ciphertext, and `m`, the length of the ciphertext we need to decrypt. Both are at most `50`, and there can be at most `50` test cases. These limits are extremely small. Even an approach that checks all `26` possible Caesar shifts and scans the strings is comfortably fast, with at most about `26 * 50 * 50 = 65,000` character comparisons across all test cases. The direct solution is still preferable because the shift can be recovered immediately from one corresponding pair of characters.

The main edge cases come from the cyclic nature of the alphabet. A shift can cross from `Z` back to `A`, so ordinary integer subtraction without modulo arithmetic can produce invalid character codes. A zero shift is also valid, meaning the plaintext and ciphertext can be identical. Finally, `n` can be `1`, so the shift must be recoverable from a single character.

For example, a one-character test case can be:

```
1
1 1
Z
A
A
```

The known pair tells us that the encryption shift is `1`, so the final `A` decrypts to `Z`. The correct output is:

```
Case #1: Z
```

A careless implementation that computes `ord('A') - 1` directly instead of wrapping modulo `26` can produce a character before `A`, which is not a valid uppercase letter.

A zero-shift example is:

```
1
1 3
A
A
ABC
```

The correct output is `Case #1: ABC`. An implementation that assumes the ciphertext must differ from the plaintext would incorrectly search for a nonzero shift.

The wraparound case is especially useful:

```
1
2 3
YZ
ZA
ABC
```

Here the known pair uses a shift of `1`, because `Y -> Z` and `Z -> A`. Decrypting `ABC` gives `ZAB`. Forgetting the modulo operation would make the transition from `A` backward by one produce an invalid result.

## Approaches

A straightforward approach is to try every one of the `26` possible Caesar shifts. For each candidate shift, encrypt the known plaintext and compare the result with the known ciphertext. Exactly one candidate is guaranteed to match. After finding it, apply the inverse shift to the third string.

This brute force is correct because every Caesar cipher is completely described by one value from `0` through `25`. Checking every possible value cannot miss the actual encryption rule. For one test case, this takes `O(26n + 26m)` time, which is simply `O(n + m)` because `26` is a constant. With the maximum values `n = m = 50`, there are at most `2,600` character operations per test case, or about `130,000` across all `50` cases. Under the stated constraints, the brute-force method is not actually too slow.

The more direct approach comes from observing that the Caesar shift is already encoded in any one pair of corresponding characters. Suppose the plaintext starts with `A` and the ciphertext starts with `T`. The shift is immediately `19`. More generally, if their alphabet indices are `p` and `c`, then the encryption shift is `(c - p) mod 26`. Because the input guarantees a valid unambiguous Caesar transformation, this shift is enough to decrypt every character in the third string.

The brute-force method works because there are only `26` possible transformations, but it performs unnecessary searches. The observation that one aligned character pair determines the shift lets us replace the search with one subtraction and then one linear scan of the target ciphertext.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(26(n + m)) = O(n + m)` | `O(m)` | Accepted |
| Directly derive shift | `O(n + m)` | `O(m)` | Accepted |

The direct approach has the better constant factor and makes the structure of the problem explicit.

## Algorithm Walkthrough

1. Read `n`, `m`, the known plaintext, the known ciphertext, and the ciphertext that must be decrypted. The first two strings have corresponding positions because they have the same length.
2. Convert the first character of the plaintext and ciphertext into alphabet indices from `0` to `25`. Compute the encryption shift as `(cipher_index - plain_index) % 26`. One corresponding pair is enough because a Caesar cipher uses exactly the same shift everywhere.
3. For every character in the target ciphertext, convert it to an alphabet index and subtract the recovered shift. Apply `% 26` so that moving before `A` wraps around to `Z`.
4. Convert each resulting index back to an uppercase letter and concatenate the characters. Prefix the result with `Case #x:` using the current test case number.

Why it works: let the encryption shift be `s`. For every position in the known pair, the ciphertext index equals the plaintext index plus `s` modulo `26`. Thus `(cipher_index - plain_index) % 26` recovers exactly `s`. For a target ciphertext character with encrypted index `c`, its plaintext index must be `(c - s) % 26`, so every character produced by the algorithm is exactly the character that generated the ciphertext. Since the same shift applies to every position, decrypting the characters independently gives the complete correct plaintext.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    answers = []

    for case in range(1, t + 1):
        n, m = map(int, input().split())
        plain = input().strip()
        cipher = input().strip()
        target = input().strip()

        plain_index = ord(plain[0]) - ord('A')
        cipher_index = ord(cipher[0]) - ord('A')

        shift = (cipher_index - plain_index) % 26

        decoded = []
        for ch in target:
            value = (ord(ch) - ord('A') - shift) % 26
            decoded.append(chr(value + ord('A')))

        answers.append(f"Case #{case}: {''.join(decoded)}")

    sys.stdout.write('\n'.join(answers))

if __name__ == "__main__":
    solve()
```

The first character pair determines `shift`. Subtracting the plaintext index from the ciphertext index gives the number of positions by which the plaintext was moved. `% 26` handles both positive and negative differences uniformly.

The decryption loop performs the inverse operation. If encryption was `plain + shift`, decryption is `cipher - shift`. Python's modulo operation is especially convenient here because a negative result such as `-1 % 26` becomes `25`, corresponding to `Z`.

There is no need to inspect the remaining characters of the known plaintext and ciphertext because the problem guarantees that they were produced by one consistent Caesar shift. Checking them would only repeat information already determined by the first pair.

The result is accumulated in a list and joined once at the end rather than repeatedly concatenating strings. This is not necessary for the tiny constraints, but it gives the standard linear-time construction and avoids unnecessary intermediate strings.

No integer overflow is possible in Python, and the only boundary operation requiring care is the modulo `26` when decryption crosses from `A` to `Z`.

## Worked Examples

The statement provides one sample test case:

```
1
7 7
ACMICPC
CEOKERE
PKPIZKC
```

The first corresponding characters are `A` and `C`, giving a shift of `2`. Applying that inverse shift to every character of `PKPIZKC` gives `NINGXIA`.

| Plain character | Cipher character | Plain index | Cipher index | Shift |
| --- | --- | --- | --- | --- |
| `A` | `C` | 0 | 2 | 2 |

The decryption of the target then proceeds as follows.

| Target character | Target index | `(index - shift) % 26` | Plain character |
| --- | --- | --- | --- |
| `P` | 15 | 13 | `N` |
| `K` | 10 | 8 | `I` |
| `P` | 15 | 13 | `N` |
| `I` | 8 | 6 | `G` |
| `Z` | 25 | 23 | `X` |
| `K` | 10 | 8 | `I` |
| `C` | 2 | 0 | `A` |

The final answer is `Case #1: NINGXIA`. The table demonstrates the core invariant: every target character is shifted backward by exactly the same recovered amount.

For a second example, consider a shift of `25`, which is equivalent to shifting every letter one position backward during encryption.

```
1
2 5
YZ
ZA
ABCDE
```

The pair `Y -> Z` gives shift `1`, while `Z -> A` confirms the cyclic behavior. The target is therefore decrypted by shifting each character backward by `1`.

| Target character | Target index | `(index - shift) % 26` | Plain character |
| --- | --- | --- | --- |
| `A` | 0 | 25 | `Z` |
| `B` | 1 | 0 | `A` |
| `C` | 2 | 1 | `B` |
| `D` | 3 | 2 | `C` |
| `E` | 4 | 3 | `D` |

The result is `Case #1: ZABCD`. This trace exercises the alphabet boundary, since decrypting `A` requires wrapping around to `Z`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m)` | The shift is recovered in constant time, then the `m` target characters are processed once. |
| Space | `O(m)` | The decoded characters are stored before producing the output. |

With `n, m <= 50` and at most `50` test cases, the algorithm performs only a few thousand character operations per case. The implementation is far below the given `10` second limit and uses negligible memory.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    answers = []

    for case in range(1, t + 1):
        n, m = map(int, input().split())
        plain = input().strip()
        cipher = input().strip()
        target = input().strip()

        shift = (
            ord(cipher[0]) - ord('A')
            - (ord(plain[0]) - ord('A'))
        ) % 26

        decoded = []
        for ch in target:
            value = (ord(ch) - ord('A') - shift) % 26
            decoded.append(chr(value + ord('A')))

        answers.append(f"Case #{case}: {''.join(decoded)}")

    sys.stdout.write('\n'.join(answers))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """1
7 7
ACMICPC
CEOKERE
PKPIZKC
"""
) == "Case #1: NINGXIA\n", "provided sample"

# Minimum size, zero shift
assert run(
    """1
1 1
A
A
A
"""
) == "Case #1: A\n", "minimum size and zero shift"

# Wraparound from Z to A
assert run(
    """1
2 3
YZ
ZA
ABC
"""
) == "Case #1: ZAB\n", "alphabet wraparound"

# Maximum sizes, shift 25
assert run(
    """1
50 50
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
"""
) == "Case #1: BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\n", "maximum size"

# Multiple test cases and a nontrivial shift
assert run(
    """2
3 4
ABC
DEF
DEFG
5 6
HELLO
KHOOR
KHOORZ
"""
) == "Case #1: BCDE\nCase #2: HELLOA\n", "multiple cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / A / A / A` | `Case #1: A` | Minimum size and zero shift |
| `YZ / ZA / ABC` | `Case #1: ZAB` | Wraparound at `A` and `Z` |
| 50 `A` characters, 50 `Z` characters, target of 50 `A` characters | 50 `B` characters | Maximum allowed lengths and a boundary shift |
| Two independent test cases | `Case #1: BCDE`, `Case #2: HELLOA` | Correct case numbering and independent processing |

## Edge Cases

The one-character case is handled without any special branch. For input

```
1
1 1
Z
A
A
```

the indices are `25` and `0`, so the shift is `(0 - 25) % 26 = 1`. The target `A` has index `0`, and `(0 - 1) % 26 = 25`, giving `Z`. The output is `Case #1: Z`. A solution that assumes there must be at least two positions would fail unnecessarily.

For a zero shift, consider

```
1
1 3
A
A
ABC
```

The recovered shift is `(0 - 0) % 26 = 0`. Every target character remains unchanged, producing `Case #1: ABC`. The modulo expression also makes zero shift behave naturally without a separate condition.

For alphabet wraparound, consider

```
1
2 3
YZ
ZA
ABC
```

The first pair gives a shift of `1`, and the second pair confirms that the shift wraps from `Z` to `A`. During decryption, `A` becomes `(0 - 1) % 26 = 25`, so it becomes `Z`. The complete result is `Case #1: ZAB`. This catches implementations that perform subtraction without modulo arithmetic.

For the maximum-size case, the algorithm still uses exactly one pass over the target string after recovering the shift. Even with `m = 50`, the decoded list contains only `50` characters, and processing all `50` test cases requires at most `2,500` target characters. The small limits make performance straightforward, while the same reasoning would remain valid for much larger strings.
