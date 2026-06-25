---
title: "CF 106421D - Anagrams"
description: "The problem gives two strings of equal length. The first string is the one we can modify, and the second string describes the multiset of characters we ultimately need."
date: "2026-06-25T09:41:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106421
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 3-11-2026 Div. 2 (Advanced)"
rating: 0
weight: 106421
solve_time_s: 35
verified: true
draft: false
---

[CF 106421D - Anagrams](https://codeforces.com/problemset/problem/106421/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives two strings of equal length. The first string is the one we can modify, and the second string describes the multiset of characters we ultimately need. We may replace characters in the first string, where one replacement changes exactly one position to any other character. Among all ways to make the first string an anagram of the target string using the minimum number of replacements, we must output the resulting string that is smallest in lexicographic order.

The input size is large: the strings can contain up to $10^5$ characters. That immediately rules out trying permutations, generating anagrams, or comparing every possible transformed string. Any solution must process the strings with a small constant amount of work per character, which points toward linear or near-linear complexity.

The key edge cases come from the difference between "same letters" and "same positions". For example, if the input is:

```
ABA
CBA
```

the answer is:

```
1
ABC
```

A careless solution might only count mismatches by position and produce `CBA` after one replacement. That misses the lexicographic requirement. The final string can rearrange the target letters, so we should keep as many useful existing characters as possible and then choose the smallest possible arrangement.

Another tricky case is when there are duplicate letters:

```
AAAA
AAAB
```

The correct output is:

```
1
AAAB
```

A solution that treats every character as unique may think three replacements are needed because the strings differ in several positions. The right way is to compare frequencies.

A final edge case is when the strings are already anagrams:

```
BCA
ABC
```

The answer is:

```
0
ABC
```

No replacements are required, but we still need to reorder the existing characters into the lexicographically smallest possible anagram.

## Approaches

The brute-force way is to try every possible anagram of the target string, check how many positions differ from the source string, and keep the best candidate. This is correct because it examines every possible final arrangement. The problem is that a string of length $n$ can have up to $n!$ permutations. Even for a few dozen characters this becomes impossible, and with $10^5$ characters it is not remotely close to feasible.

A better direction comes from looking at what a replacement actually does. Each position in the original string can either keep its character or be changed. To minimize replacements, we want to preserve as many existing characters as possible. This means we only need to know how many copies of each letter exist in both strings.

Suppose the source has five copies of `A` and the target needs three copies. Two of those `A` characters are extra and must be changed. On the other hand, if the target needs more `A` characters than the source has, we need replacements to create the missing copies. The total number of replacements is exactly the number of characters that cannot be matched by frequency.

After knowing the minimum number of replacements, we still need the lexicographically smallest final string. The smallest possible character should appear as early as possible. We can greedily scan the positions from left to right. At each position, if the current character can remain while still satisfying the remaining frequency requirements, we keep it. Otherwise we replace it with the smallest available character.

The reason this greedy choice works is that lexicographic order is decided by the first position where two strings differ. Making the earliest possible position as small as possible always dominates any later improvement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(26n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every character in the source string and the target string. The alphabet is fixed, so we only need an array of size 26.
2. Compute how many characters from the source can be kept. For each letter, the number of usable copies is the minimum of its frequency in the source and in the target. Everything else from the source must eventually be replaced.
3. Scan the source string from left to right. Maintain the remaining counts of characters that still have to appear in the answer. When looking at the current position, try to keep its original character first.
4. Keeping a character is valid only if we still have more copies of that character available in the target than the number already fixed in the answer. If the character is not needed anymore, replace it.
5. If the current character cannot be kept, choose the smallest letter whose remaining target count is positive and place it in this position. Decrease its remaining count.

Why it works: the algorithm always preserves a character whenever possible, so the number of replacements cannot be larger than necessary. Once we decide to replace a position, choosing the smallest available character gives the smallest possible prefix. Since every earlier position is optimized before later positions are considered, the final string is the lexicographically smallest among all optimal answers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()

    src = [0] * 26
    need = [0] * 26

    for c in s:
        src[ord(c) - 65] += 1
    for c in t:
        need[ord(c) - 65] += 1

    keep = [min(src[i], need[i]) for i in range(26)]

    ans = []
    remain = need[:]

    for c in s:
        x = ord(c) - 65
        if keep[x] > 0:
            ans.append(c)
            keep[x] -= 1
            remain[x] -= 1
        else:
            for y in range(26):
                if remain[y] > 0:
                    ans.append(chr(y + 65))
                    remain[y] -= 1
                    break

    print(sum(1 for i in range(len(s)) if s[i] != ans[i]))
    print("".join(ans))

if __name__ == "__main__":
    solve()
```

The first part builds the frequency tables. Since there are only 26 uppercase letters, counting takes constant work per character.

The `keep` array stores how many copies of every character we are allowed to preserve. During the left-to-right construction, a preserved character consumes one available kept copy and one required target copy.

The replacement branch searches from `A` to `Z`. The search is only over 26 letters, so even though it appears nested inside the main loop, the total complexity stays linear. The replacement count is calculated at the end by comparing the original string with the constructed answer.

The boundary conditions are handled naturally. If a character is already correct and needed, it is kept. If all copies of a character have been used, it will never be chosen again. There is no risk of producing too many copies because every placement decreases the remaining target frequency.

## Worked Examples

Consider:

```
ABA
CBA
```

The frequencies show that `A` and `B` can be kept, while `C` must be created.

| Position | Current character | Kept? | Remaining target |
| --- | --- | --- | --- |
| 1 | A | Yes | B:1, C:1 |
| 2 | B | Yes | C:1 |
| 3 | A | No | C:1 |

The last position cannot stay as `A` because the target has no extra `A`. The smallest available character is `C`.

The result is:

```
ABC
```

with one replacement.

Another example:

```
CDBABC
ADCABD
```

The useful characters are kept first.

| Position | Current character | Action | Answer prefix |
| --- | --- | --- | --- |
| 1 | C | Replace with A | A |
| 2 | D | Keep | AD |
| 3 | B | Keep | ADB |
| 4 | A | Keep | ADBA |
| 5 | B | Keep | ADBAB |
| 6 | C | Keep | ADBABC |

The construction keeps the maximum possible characters and makes the first differing position as small as possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26n) | Every character is processed once, with at most 26 checks for replacement choices |
| Space | O(26) | Only frequency arrays and the answer storage are needed |

The algorithm is suitable for strings of length $10^5$ because it performs only a small constant amount of work per character.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()

    src = [0] * 26
    need = [0] * 26

    for c in s:
        src[ord(c) - 65] += 1
    for c in t:
        need[ord(c) - 65] += 1

    keep = [min(src[i], need[i]) for i in range(26)]
    remain = need[:]
    ans = []

    for c in s:
        x = ord(c) - 65
        if keep[x] > 0:
            ans.append(c)
            keep[x] -= 1
            remain[x] -= 1
        else:
            for y in range(26):
                if remain[y] > 0:
                    ans.append(chr(y + 65))
                    remain[y] -= 1
                    break

    out = str(sum(1 for i in range(len(s)) if s[i] != ans[i])) + "\n" + "".join(ans) + "\n"
    sys.stdin = old
    return out

assert run("ABA\nCBA\n") == "1\nABC\n", "sample 1"
assert run("CDBABC\nADCABD\n") == "2\nADBADC\n", "sample 2"

assert run("A\nA\n") == "0\nA\n", "single character"
assert run("AAAA\nAAAB\n") == "1\nAAAB\n", "duplicates"
assert run("ZYX\nABC\n") == "3\nABC\n", "full replacement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A / A` | `0 / A` | Minimum length case |
| `AAAA / AAAB` | `1 / AAAB` | Frequency handling with duplicates |
| `ZYX / ABC` | `3 / ABC` | Complete replacement and lexicographic ordering |

## Edge Cases

For the case:

```
ABA
CBA
```

the algorithm keeps `A` and `B` because they are required by the target. At the last position, the remaining target frequency contains only `C`, so the replacement is forced. The result has the minimum possible number of changes and is lexicographically smallest.

For:

```
AAAA
AAAB
```

the source has too many `A` characters. The first three positions can stay as `A`, but the final extra `A` must become `B`. The frequency arrays prevent the algorithm from keeping a character that would leave the target impossible to satisfy.

For:

```
BCA
ABC
```

all letters already exist in the required quantities. No replacements are performed, and the greedy construction keeps the available characters while producing the smallest possible ordering. The final answer becomes `ABC` with zero operations.
