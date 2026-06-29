---
title: "CF 104636G - Pangram"
description: "We are given a string of Latin letters where both uppercase and lowercase characters may appear. The task is to determine whether the string is a pangram, meaning that every letter from 'a' to 'z' appears at least once somewhere in the string, ignoring case differences."
date: "2026-06-29T17:07:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104636
codeforces_index: "G"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u043c\u0430\u0441\u0441\u0438\u0432\u044b, \u0441\u0442\u0440\u043e\u043a\u0438"
rating: 0
weight: 104636
solve_time_s: 59
verified: true
draft: false
---

[CF 104636G - Pangram](https://codeforces.com/problemset/problem/104636/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of Latin letters where both uppercase and lowercase characters may appear. The task is to determine whether the string is a pangram, meaning that every letter from `'a'` to `'z'` appears at least once somewhere in the string, ignoring case differences.

In more concrete terms, we scan a single sequence of characters and want to check whether the set of distinct letters present covers all 26 letters of the English alphabet. Case does not matter, so `'A'` and `'a'` are treated as the same symbol for the purpose of checking coverage.

The input size is small, at most 100 characters. This immediately rules out any need for optimization beyond a single pass through the string. Even an $O(n \cdot 26)$ or $O(n^2)$ approach would technically pass, but the natural solution is linear time with constant additional memory.

The main edge cases come from how letters are normalized and how completeness is checked. A naive mistake is treating uppercase and lowercase as different characters, which would incorrectly mark strings like `"TheQuickBrownFoxJumpsOverTheLazyDog"` as not containing all letters if case is not normalized. Another subtle issue is incorrectly assuming the string length guarantees coverage, which is false since repetition does not imply diversity.

## Approaches

A brute-force way to solve the problem is to, for each letter from `'a'` to `'z'`, scan the entire string and check whether that letter appears in either lowercase or uppercase form. This is correct because it directly verifies the definition of a pangram. However, for each of the 26 letters, we may scan up to 100 characters, leading to at most 2600 character checks. This is already trivial in practice, but the structure is inefficient compared to what is necessary.

A better approach is to reverse the perspective. Instead of asking “does each letter appear in the string?”, we process the string once and record which letters we have seen. Each character is normalized to lowercase and inserted into a set or marked in a boolean array of size 26. At the end, we simply check whether all 26 positions are marked. This works because the property we care about is membership in a fixed universe of size 26, so repeated scanning is unnecessary.

The key observation is that the alphabet size is constant. Once we recognize that the domain of interest is fixed and small, we can reduce the problem to a single pass accumulation problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26 · n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string character by character and maintain a structure that tracks which letters have appeared.

1. Initialize a boolean array `seen` of size 26, all set to false. Each index corresponds to a letter from `'a'` to `'z'`. This gives us constant-time membership tracking.
2. Iterate over every character in the input string. For each character, convert it to lowercase so that uppercase and lowercase versions map to the same index space. This normalization ensures that we do not double count letters based on case.
3. Compute the index of the character as `ord(c) - ord('a')`. This maps `'a'` to 0, `'b'` to 1, and so on up to `'z'` at 25. Mark `seen[index] = true`. This records that the letter has been encountered at least once.
4. After processing all characters, check whether every entry in `seen` is true. If any position remains false, at least one letter is missing from the string, so the string is not a pangram.
5. Output `"YES"` if all entries are true, otherwise output `"NO"`.

The correctness hinges on the fact that each letter is treated independently and only its presence matters, not frequency.

### Why it works

The algorithm maintains the invariant that after processing the first k characters, `seen[i]` is true if and only if the letter corresponding to index i has appeared in those k characters. This invariant holds because every character updates exactly one index, and no operation ever clears a value once set. At the end of the scan, the state exactly represents the set of all letters in the string, so checking whether all entries are true is equivalent to checking whether the string contains all 26 letters at least once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    seen = [False] * 26

    for c in s:
        if c.isalpha():
            idx = ord(c.lower()) - ord('a')
            seen[idx] = True

    if all(seen):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads the length and the string, though the length is not strictly necessary for correctness. The core logic is the fixed-size boolean array that tracks letter coverage.

The call to `lower()` ensures case-insensitive handling. The `all(seen)` check is a direct translation of the requirement that every alphabet letter must appear at least once.

One subtle point is that we never rely on frequency, only presence. This is why a boolean array is sufficient instead of a counter array.

## Worked Examples

### Sample 1

Input string: `"toosmallword"`

We track the evolution of `seen` conceptually as letters appear.

| Character | Lowercase | Index | Seen update |
| --- | --- | --- | --- |
| t | t | 19 | mark 19 |
| o | o | 14 | mark 14 |
| o | o | 14 | already marked |
| s | s | 18 | mark 18 |
| m | m | 12 | mark 12 |
| a | a | 0 | mark 0 |
| l | l | 11 | mark 11 |
| l | l | 11 | already marked |
| w | w | 22 | mark 22 |
| o | o | 14 | already marked |
| r | r | 17 | mark 17 |
| d | d | 3 | mark 3 |

After processing, only a small subset of letters are marked. Many entries remain false, so the output is `"NO"`.

This trace shows that repetition of a few letters does not help unless all 26 distinct indices are reached.

### Sample 2

Input string: `"TheQuickBrownFoxJumpsOverTheLazyDog"`

As we scan through, each letter eventually contributes to filling the 26 positions.

| Character | Lowercase | Index | Seen update |
| --- | --- | --- | --- |
| T | t | 19 | mark |
| h | h | 7 | mark |
| e | e | 4 | mark |
| Q | q | 16 | mark |
| u | u | 20 | mark |
| i | i | 8 | mark |
| c | c | 2 | mark |
| k | k | 10 | mark |
| ... | ... | ... | ... |
| g | g | 6 | mark |

By the end, all indices from 0 to 25 have been set to true at least once.

The final check confirms full coverage, so the output is `"YES"`.

These examples illustrate the key distinction between partial coverage and complete alphabet coverage, which is the entire decision criterion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once and mapped to a constant-time update |
| Space | O(1) | The `seen` array has fixed size 26 regardless of input |

Given that $n \le 100$, the algorithm runs in constant practical time. Even under far larger constraints, the linear scan remains efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    input = sys.stdin.readline

    def solve():
        n = int(input().strip())
        s = input().strip()

        seen = [False] * 26

        for c in s:
            seen[ord(c.lower()) - ord('a')] = True

        print("YES" if all(seen) else "NO")

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("12\ntoosmallword") == "NO"
assert run("35\nTheQuickBrownFoxJumpsOverTheLazyDog") == "YES"

# custom cases
assert run("1\na") == "NO"
assert run("52\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") == "YES"
assert run("26\nabcdefghijklmnopqrstuvwxyz") == "YES"
assert run("3\nabc") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"1\na"` | NO | Minimum input, single letter cannot be pangram |
| `"52\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"` | YES | Case insensitivity and full coverage |
| `"26\nabcdefghijklmnopqrstuvwxyz"` | YES | Exact minimal valid pangram |
| `"3\nabc"` | NO | Partial alphabet coverage fails |

## Edge Cases

A subtle edge case is case sensitivity. If the algorithm does not normalize characters, then `"AaBbCc...Zz"` would incorrectly appear as missing many letters because uppercase and lowercase would map to different indices. In our approach, `lower()` ensures both forms map to the same slot, so `"A"` and `"a"` both set index 0.

Another edge case is duplicate-heavy input such as `"aaaaaaaaaaaaaaaaaa"`. Here, only one index is ever marked. The boolean array prevents overcounting from misleading the algorithm, since repeated updates do not change correctness.

A final edge case is minimal coverage input like `"abcdefghijklmnopqrstuvwxyz"` versus missing one letter such as `"abcdefghijklmnopqrstuvwxy"`. In the first case, all indices are filled exactly once and the result is `"YES"`. In the second, index 25 remains false, and the final check correctly yields `"NO"`.
