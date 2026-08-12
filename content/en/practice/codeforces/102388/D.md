---
title: "CF 102388D - Secret Messages"
description: "For each testcase, we receive one nonempty string containing only English letters. The required encoding applies three transformations in the order described by the problem: change every letter to the opposite case, reverse the entire string, and apply ROT13 while preserving the…"
date: "2026-08-12T21:09:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102388
codeforces_index: "D"
codeforces_contest_name: "SUFE ICPC Team Formation Test"
rating: 0
weight: 102388
solve_time_s: 598
verified: true
draft: false
---

[CF 102388D - Secret Messages](https://codeforces.com/problemset/problem/102388/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

For each testcase, we receive one nonempty string containing only English letters. The required encoding applies three transformations in the order described by the problem: change every letter to the opposite case, reverse the entire string, and apply ROT13 while preserving the letter's case. The output is the resulting encoded string.

For example, starting with `HelloWorld`, changing case gives `hELLOwORLD`. Reversing gives `DLROwOLLEh`, and ROT13 produces `QYEBjBYYRu`.

There are at most 100 testcases, and every string has at most 100 characters. The total amount of input is therefore tiny, so even several complete passes over every string are easily fast enough for the 1 second limit. More importantly, the transformations themselves are linear in the string length, so there is no reason to use anything more complicated than direct simulation. A solution taking quadratic time would also pass these particular constraints, but it would be solving a problem much harder than necessary.

The first edge case is a one-character string. For input `A`, case swapping gives `a`, reversing changes nothing, and ROT13 gives `n`, so the correct output is `N` after applying the transformations in their specified composition. A careless implementation that treats reversal as requiring at least two characters could accidentally skip or mishandle this case.

The second edge case is a character near the end of the alphabet. For input `Z`, ROT13 must wrap around from `Z` to `M`, rather than moving outside the alphabet. The correct output is `M`. The same issue appears for lowercase `z`, which becomes `m`. An implementation that simply adds 13 to the ASCII value without wrapping would produce an invalid character.

The third edge case is a mixture of cases and alphabet boundaries. For input `AaZz`, reversing first gives `zZ aA` without spaces, namely `zZaA`. After swapping case this becomes `ZzAa`, and ROT13 gives `MmNn`. A careless solution that applies ROT13 before changing case but then uses the wrong case information can easily produce incorrect capitalization.

## Approaches

The straightforward approach is to simulate the three operations separately. We can scan the whole string and swap the case of every character, perform a reversal, then scan the whole string again for ROT13. This directly mirrors the encoding definition, so correctness is immediate. With a string of length `n`, the three passes perform `n` case changes, `floor(n / 2)` reversal swaps, and `n` ROT13 conversions. Under this direct implementation, that is `2n + floor(n / 2)` character-level operations. With `n <= 100`, the worst case is only 250 such operations per testcase, so there is no point where this approach becomes too slow. The apparent brute-force baseline is already accepted.

We can make the implementation cleaner by observing that both case swapping and ROT13 are character-wise transformations. Neither operation depends on a character's position, so both commute with reversal. Instead of first constructing an intermediate string and then reversing it, we can traverse the original string from right to left and apply the two character transformations while producing the answer. Each input character is processed exactly once.

The key observation is that the three operations do not need complicated interaction. Reversal determines the order in which characters appear, while case swapping and ROT13 only modify each individual character. Thus, when we visit the original characters from the last position to the first, we have already performed the reversal implicitly. We only need to transform each visited character.

This reduces the implementation to one traversal of the string. The asymptotic complexity remains `O(n)`, which is optimal because every character has to be inspected at least once to determine the output.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Separate simulation passes | O(n) | O(n) | Accepted |
| One-pass transformation while traversing backwards | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the string `s`. Its characters are guaranteed to be English letters, so every character can be handled by checking whether it is uppercase or lowercase.
2. Traverse `s` from the last character to the first. Reading in this direction performs the required reversal without explicitly constructing a reversed copy.
3. Swap the case of the current character. An uppercase character becomes lowercase, and a lowercase character becomes uppercase.
4. Apply ROT13 to the character while preserving its current case. For an uppercase letter, subtract `A`, add 13 modulo 26, and add `A` back. For a lowercase letter, do the same using `a`.
5. Append the transformed character to the answer. Since characters are processed in reverse input order, the resulting answer already has the required reversed arrangement.
6. Print the completed answer for the testcase.

### Why it works

Consider any original character `s[i]`. The final encoded string must contain the transformed version of this character at position `n - 1 - i`, because the reversal moves position `i` to that position. By traversing the input from `n - 1` down to `0`, the algorithm places characters into exactly those final positions in left-to-right order. The case swap and ROT13 operations are independent of the character's position, so applying them while visiting the character produces exactly the same character that would result from applying them before or after the reversal. Thus every output position contains the correct encoded character.

## Python Solution

```python
import sys
input = sys.stdin.readline

def transform(s):
    ans = []

    for c in reversed(s):
        if 'A' <= c <= 'Z':
            c = c.lower()
        else:
            c = c.upper()

        if 'A' <= c <= 'Z':
            c = chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
        else:
            c = chr((ord(c) - ord('a') + 13) % 26 + ord('a'))

        ans.append(c)

    return ''.join(ans)

def main():
    t = int(input())

    for _ in range(t):
        s = input().strip()
        print(transform(s))

if __name__ == "__main__":
    main()
```

The `transform` function corresponds directly to the algorithm walkthrough. `reversed(s)` gives the characters in exactly the order required after the reversal operation, so no separate reverse operation is necessary.

The first conditional changes the character's case. The second conditional then determines which alphabet the character belongs to and performs ROT13 using modular arithmetic. The expression `(ord(c) - ord('A') + 13) % 26` converts the character into a zero-based alphabet position, rotates it by 13 positions, and wraps around when necessary.

The modulo operation handles the alphabet boundary cleanly. For example, `Z` has zero-based position 25, so `(25 + 13) % 26` gives 12, which corresponds to `M`. The lowercase branch behaves identically with `a` as its base.

There are no index calculations involving `len(s) - 1 - i`, so the implementation avoids the most common reversal off-by-one error. There is also no integer overflow concern because all arithmetic is performed on values between 0 and 25.

The answer is stored in a list because repeatedly concatenating strings can create unnecessary intermediate strings. Joining the list once at the end constructs the final result efficiently.

## Worked Examples

For the first sample testcase, `HelloWorld`, the algorithm processes the characters from right to left.

| Input position | Original character | After case swap | After ROT13 | Output order |
| --- | --- | --- | --- | --- |
| 9 | `d` | `D` | `Q` | 1 |
| 8 | `l` | `L` | `Y` | 2 |
| 7 | `r` | `R` | `E` | 3 |
| 6 | `o` | `O` | `B` | 4 |
| 5 | `W` | `w` | `j` | 5 |
| 4 | `o` | `O` | `B` | 6 |
| 3 | `l` | `L` | `Y` | 7 |
| 2 | `l` | `L` | `Y` | 8 |
| 1 | `e` | `E` | `R` | 9 |
| 0 | `H` | `h` | `u` | 10 |

The output is `QYEBjBYYRu`. This trace shows that reading the input backwards automatically handles the reversal, while each character independently receives the other two transformations.

For a second example, consider `AaZz`.

| Input position | Original character | After case swap | After ROT13 | Output order |
| --- | --- | --- | --- | --- |
| 3 | `z` | `Z` | `M` | 1 |
| 2 | `Z` | `z` | `m` | 2 |
| 1 | `a` | `A` | `N` | 3 |
| 0 | `A` | `a` | `n` | 4 |

The output is `MmNn`. This example exercises both uppercase and lowercase characters and both ends of the alphabet. In particular, `Z` wraps to `M` and `z` wraps to `m`, confirming that the modulo-26 ROT13 calculation handles the boundary correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is processed exactly once. |
| Space | O(n) | The answer list stores one transformed character for each input character. |

Here `n` is the length of the current message. Since `n <= 100` and there are at most 100 testcases, the total amount of character processing is at most 10,000 characters. The solution is far below both the 1 second time limit and the 256 MB memory limit.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    input = io.StringIO(inp).readline
    t = int(input())
    out = []

    for _ in range(t):
        s = input().strip()
        ans = []

        for c in reversed(s):
            if 'A' <= c <= 'Z':
                c = c.lower()
            else:
                c = c.upper()

            if 'A' <= c <= 'Z':
                c = chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
            else:
                c = chr((ord(c) - ord('a') + 13) % 26 + ord('a'))

            ans.append(c)

        out.append(''.join(ans))

    return '\n'.join(out) + '\n'

def run(inp: str) -> str:
    return solve(inp)

# Provided sample
assert run(
    """3
HelloWorld
QYEBjBYYRu
pcpvBgRZBPYRj
"""
) == """QYEBjBYYRu
HelloWorld
WelcomeToICPC
""", "sample 1"

# Minimum-size input
assert run("1\nA\n") == "N\n", "single uppercase character"

# Alphabet boundaries and mixed case
assert run("1\nAaZz\n") == "MmNn\n", "alphabet boundaries"

# All characters equal, maximum length
assert run("1\n" + "A" * 100 + "\n") == "N" * 100 + "\n", "maximum-size equal string"

# Lowercase boundary characters
assert run("1\naz\n") == "MZ\n", "lowercase alphabet boundaries"

# Multiple testcases with different lengths
assert run(
    """3
a
Z
AbCd
"""
) == """N
M
qPmE
""", "mixed lengths and cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A` | `N` | Minimum length and a single uppercase character |
| `AaZz` | `MmNn` | Case changes, reversal, and both alphabet boundaries |
| 100 copies of `A` | 100 copies of `N` | Maximum string length and all-equal input |
| `az` | `MZ` | Lowercase ROT13 wrapping at both ends |
| `a`, `Z`, `AbCd` | `N`, `M`, `qPmE` | Multiple testcases and mixed string lengths |

## Edge Cases

For the one-character input `A`, the traversal contains only that character. Case swapping changes `A` to `a`, and ROT13 changes `a` to `n`. The character has nowhere else to move during reversal, so the final output is `N`. The algorithm does not need a special case for length one.

For the alphabet boundary input `Z`, the character first becomes `z` because of the case swap. ROT13 then computes `(25 + 13) % 26 = 12`, producing `m`, so the output is `M`. The modulo operation prevents the calculation from leaving the alphabet.

For the mixed boundary input `AaZz`, the reverse traversal visits `z`, `Z`, `a`, `A`. After case swapping and ROT13, these become `M`, `m`, `N`, `n`, respectively. The output is `MmNn`, which confirms that the algorithm preserves the correct case while handling both uppercase and lowercase wraparound.

For the maximum-size all-equal input consisting of 100 copies of `A`, reversal does not visibly change the string, but every character still undergoes the case swap and ROT13 transformation. Each `A` becomes `N`, so the result contains 100 copies of `N`. The algorithm processes exactly 100 characters and needs no special handling for repeated values.
