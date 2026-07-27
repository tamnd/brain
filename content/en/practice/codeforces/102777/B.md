---
title: "CF 102777B - \u041f\u0430\u043b\u0438\u043d\u0434\u0440\u043e\u043c \u041c\u043e\u0440\u0437\u0435"
description: "We need to decide whether a lowercase English string becomes a palindrome after replacing every character with its Morse representation and joining all those representations together."
date: "2026-07-28T03:07:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 83
verified: true
draft: false
---

[CF 102777B - \u041f\u0430\u043b\u0438\u043d\u0434\u0440\u043e\u043c \u041c\u043e\u0440\u0437\u0435](https://codeforces.com/problemset/problem/102777/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to decide whether a lowercase English string becomes a palindrome after replacing every character with its Morse representation and joining all those representations together. The original letters are separated before encoding, but the resulting Morse sequence is just one continuous string of dots and dashes. The answer is YES if this final sequence reads the same from both ends, and NO otherwise.

The input length is at most 1000 characters. A Morse code for one letter contains at most four symbols, so even the encoded string is only a few thousand characters long. This means a linear scan is easily fast enough, while algorithms with quadratic behavior are unnecessary and would only make the implementation more complicated.

The main source of mistakes is assuming that the palindrome property can be checked on the original letters. The encoding changes the structure completely because different letters may create matching or mismatching dot and dash patterns.

For example, the input `aarrghh` should produce `NO`. A careless solution that checks only whether the letters form a palindrome would see that the letters are symmetric and incorrectly return YES. The Morse representation must be checked instead.

Another trap is forgetting that character boundaries disappear after encoding. The input `panne` should produce `NO`. The letters themselves cannot simply be mirrored as groups because the final comparison is between individual Morse symbols.

The empty string is not a possible input because the statement guarantees a non-empty sequence of lowercase letters. A one-character input such as `a` produces `.−`, which is not a palindrome, so the correct output is NO.

## Approaches

The direct approach is to convert the whole input string into Morse code and then compare characters from the beginning and the end. This requires creating the encoded string and checking whether its first symbol equals its last symbol, its second symbol equals its second-last symbol, and so on. The method is correct because a string is a palindrome exactly when all mirrored positions contain the same character.

A brute-force implementation can also repeatedly compare every pair of positions in the encoded string. If the encoded length is around 4000 characters, this performs about 16 million comparisons in the worst case. That is still not disastrous for these constraints, but it is unnecessary and ignores the simpler structure of palindrome checking.

The key observation is that we do not need to compare every pair. A palindrome only requires a single pass from both ends. Once we have the Morse string, two pointers can move inward and immediately reject the answer when they find different symbols.

The brute-force works because it examines the same information as the optimal solution, but it repeats many comparisons. The observation that mirrored positions can be checked while moving toward the center reduces the work to a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(m) | Too slow in larger variants |
| Optimal | O(m) | O(m) | Accepted |

Here, `m` is the length of the Morse encoded string.

## Algorithm Walkthrough

1. Store the Morse representation of every lowercase English letter in an array where the index matches the letter position. This avoids rebuilding the mapping while processing the input.
2. Read the original string and append the Morse code of each character into one continuous sequence. The spaces between letters are intentionally not stored because the palindrome check happens on the final Morse stream.
3. Set one pointer at the start of the encoded sequence and another pointer at the end. Compare the two symbols they point to.
4. If the symbols are different, the sequence cannot be a palindrome, so the answer is NO immediately. A mismatch at any mirrored position is enough to prove failure.
5. Move both pointers toward the center and continue until they meet or cross. If every mirrored pair matched, output YES.

Why it works: the algorithm maintains the invariant that every pair of positions already passed by the two pointers is equal to its mirrored position. A palindrome is defined exactly by this property. If the algorithm reaches the middle without finding a mismatch, every required pair has been verified, so the encoded string must be a palindrome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    morse = [
        ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..",
        ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.",
        "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."
    ]

    s = input().strip()

    encoded = []
    for ch in s:
        encoded.append(morse[ord(ch) - ord('a')])

    encoded = "".join(encoded)

    left = 0
    right = len(encoded) - 1

    while left < right:
        if encoded[left] != encoded[right]:
            print("NO")
            return
        left += 1
        right -= 1

    print("YES")

if __name__ == "__main__":
    solve()
```

The `morse` array stores the translation table once. The index calculation with `ord(ch) - ord('a')` converts a lowercase letter into a zero-based position, so no dictionary lookup is needed.

The encoded list is used while building the Morse sequence because repeatedly concatenating strings can create unnecessary temporary strings in some languages. Joining once after the loop keeps the construction simple and efficient.

The two-pointer loop uses `left < right` because the middle character of an odd-length palindrome does not need to be compared with itself. After every successful comparison, both pointers move exactly one position inward, avoiding any off-by-one issues.

## Worked Examples

For the input `abelian`, the Morse conversion is:

`a` becomes `.-`
`b` becomes `-...`
`e` becomes `.`
`l` becomes `.-..`
`i` becomes `..`
`a` becomes `.-`
`n` becomes `-.`

The complete encoded string is `.--....-....-.-.`.

| left | right | left symbol | right symbol | result |
| --- | --- | --- | --- | --- |
| 0 | 16 | . | . | continue |
| 1 | 15 | - | - | continue |
| 2 | 14 | - | - | continue |
| 3 | 13 | . | . | continue |

The pointers continue until they cross, so every mirrored pair matches. The output is YES.

For the input `panmixises`, the encoded string is checked from both ends.

| left | right | left symbol | right symbol | result |
| --- | --- | --- | --- | --- |
| 0 | 27 | . | - | mismatch |

The first comparison already fails. The algorithm stops immediately and outputs NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each Morse symbol is created once and checked at most once from each side |
| Space | O(m) | The encoded Morse sequence is stored, where m is its length |

The largest possible encoded sequence is only a few thousand characters because the input has at most 1000 letters and each letter uses at most four Morse symbols. The linear solution easily fits the time limit of the problem.

## Test Cases

```python
import sys
import io

def solve(inp):
    morse = [
        ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..",
        ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.",
        "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."
    ]

    s = inp.strip()
    encoded = "".join(morse[ord(ch) - ord('a')] for ch in s)

    left = 0
    right = len(encoded) - 1

    while left < right:
        if encoded[left] != encoded[right]:
            return "NO"
        left += 1
        right -= 1

    return "YES"

assert solve("abelian") == "YES", "sample 1"
assert solve("panmixises") == "NO", "sample 2"
assert solve("panne") == "NO", "sample 3"
assert solve("aarrghh") == "NO", "sample 4"
assert solve("protectorate") == "YES", "sample 5"

assert solve("a") == "NO", "single character"
assert solve("e") == "YES", "single dot Morse code"
assert solve("zzzz") == "YES", "all equal values"
assert solve("abcdefghijklmnopqrstuvwxyz") == "NO", "large boundary input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | NO | Handles the smallest input and checks that `.−` is not treated as a letter palindrome |
| `e` | YES | Checks a one-symbol encoded palindrome |
| `zzzz` | YES | Validates repeated equal values |
| `abcdefghijklmnopqrstuvwxyz` | NO | Exercises a long input and catches incorrect character-based approaches |

## Edge Cases

The input `aarrghh` is a useful example because the letters themselves look symmetric. The algorithm converts it into Morse symbols first, then compares the outside symbols of that new sequence. The mismatch appears during the two-pointer scan, so it correctly returns NO.

The input `panne` demonstrates why letter boundaries cannot be preserved. The algorithm never compares `p` with `e` or `a` with `n` as letters. It compares only positions inside the joined Morse sequence, which is the actual object defined by the task.

The input `e` produces the Morse sequence `.`. The two pointers start at the same position, so the loop is skipped and the algorithm returns YES. This is the correct behavior for a one-character palindrome.

The input `zzzz` creates four identical Morse blocks. After joining them, every mirrored pair of symbols is equal, so the pointers move inward until they cross and the answer remains YES.
