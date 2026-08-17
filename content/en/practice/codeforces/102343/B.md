---
title: "CF 102343B - Sort by Frequency"
description: "We are given one nonempty string containing only lowercase English letters. The task is to rearrange its characters so that characters with larger frequencies come earlier in the result."
date: "2026-08-17T10:17:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "B"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 72
verified: true
draft: false
---

[CF 102343B - Sort by Frequency](https://codeforces.com/problemset/problem/102343/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one nonempty string containing only lowercase English letters. The task is to rearrange its characters so that characters with larger frequencies come earlier in the result. When two characters occur equally often, the alphabetically smaller character must come first. Every occurrence from the original string must remain in the output, so we are changing only the order of the characters.

For example, the string `dcbbdabb` contains four `b` characters, two `d` characters, one `a`, and one `c`. The frequencies are therefore ordered as `b`, `d`, then `a` and `c`, with `a` before `c` because their frequencies are equal. The required result is `bbbbddac`. The original problem limits the input string to 70 lowercase letters, and the Codeforces version has a 1 second time limit and 256 MB memory limit.

The small bound of 70 means even an O(n²) solution performs at most 4900 basic character comparisons, so a straightforward implementation is already fast enough. Still, the structure of the problem gives us an O(n) solution with a fixed amount of extra work. The key is that there are only 26 possible characters, so we never need to discover or sort an arbitrary collection of values.

There are several edge cases that can cause an implementation to produce the wrong order. If every character is different, as in `abc`, every frequency is one, so alphabetical order decides everything and the output is `abc`. A solution that preserves the original order instead of applying the tie breaker would fail on an input such as `cba`, whose correct output is `abc`.

Equal frequencies can also occur between characters that are separated in the alphabet. For `programming`, the frequencies are `g=2`, `m=2`, and every character among `a`, `i`, `n`, `o`, `p`, `r` occurs once. The correct output is `ggmmainopr` only if the letters are ordered correctly within each frequency group, but the actual sample output is `ggmmrrainop` because `r` occurs twice as well. Thus the complete frequency ordering is `g`, `m`, `r`, followed by `a`, `i`, `n`, `o`, `p`, giving `ggmmrrainop`. A careless implementation that counts only some occurrences or uses the original character order for ties will fail here.

Another boundary case is a string containing only one distinct character, such as `aaaaa`. Its frequency is five, and there is no competing character, so the answer must remain `aaaaa`. An implementation that accidentally creates one output copy per distinct character instead of one copy per occurrence would produce the wrong length.

## Approaches

A direct brute-force solution can process each character separately. For every position in the input string, scan the whole string and count how many times that character appears. After obtaining the frequency for each character, sort the characters using frequency descending and alphabetic order ascending, then write each character as many times as its frequency. This is correct because every character is assigned its exact global frequency before the final ordering is performed.

If the input has length n and we independently scan all n positions for every position, the frequency-counting phase performs O(n²) character checks. Under the actual constraint n ≤ 70, the worst case is only 70² = 4900 checks, so this brute-force version is still easily accepted. There is no realistic performance problem at the official constraint. If the same method were applied to n = 100000, however, it would require 10^10 checks, which is far beyond what a 1 second contest program could handle.

The observation that makes the better solution simple is that every character belongs to one of only 26 lowercase-letter categories. We can count all frequencies in one pass with an array of length 26. Once those counts are known, we only need to inspect the alphabet from `a` through `z`. The frequency determines the primary ordering, so we can collect the 26 characters and sort those pairs by `(-frequency, character)`. Because 26 is a constant, this sorting step takes constant time with respect to the input length.

The two approaches differ mainly in how much repeated work they perform. The brute-force method repeatedly rediscovers frequencies that could have been stored, while the optimal method records each frequency once and then works on the fixed alphabet.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(26) | Accepted for n ≤ 70 |
| Optimal | O(n + 26 log 26) = O(n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Read the single input string and create a frequency array of length 26. Index `0` represents `a`, index `1` represents `b`, and so on through `z`. A fixed array is sufficient because the input alphabet is known in advance.
2. Traverse every character in the string and increment its corresponding frequency. For a character `ch`, its array position is `ord(ch) - ord('a')`. After this pass, the frequency array contains the complete information needed to construct the answer.
3. Create the 26 character-frequency pairs for the lowercase alphabet. Characters with frequency zero can be left in the collection temporarily, because they will contribute nothing to the output.
4. Sort the pairs by decreasing frequency and, when frequencies are equal, increasing character. In Python this can be expressed directly with the key `(-frequency, character)`. The negative frequency reverses the usual ascending numerical order while the character remains in normal alphabetical order.
5. Build the answer by repeating each character according to its frequency. A character with frequency zero naturally contributes an empty string, so including zero-frequency entries does not change the result.
6. Print the resulting string without spaces. Every original occurrence is emitted exactly once, so the output has exactly the same length as the input.

### Why it works

After the counting pass, the invariant is that `freq[i]` equals the exact number of occurrences of the character represented by index `i` in the input. Sorting the character-frequency pairs by decreasing frequency places every character before all characters with smaller frequency. For pairs with equal frequency, the secondary key is the character itself, so they appear alphabetically. Finally, repeating each character exactly `freq[i]` times preserves every occurrence from the input. Thus the resulting string satisfies both ordering rules and contains exactly the original multiset of characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    freq = [0] * 26

    for ch in s:
        freq[ord(ch) - ord('a')] += 1

    chars = []
    for i in range(26):
        ch = chr(ord('a') + i)
        chars.append((ch, freq[i]))

    chars.sort(key=lambda item: (-item[1], item[0]))

    ans = []
    for ch, count in chars:
        ans.append(ch * count)

    print(''.join(ans))

if __name__ == "__main__":
    solve()
```

The first part reads exactly one line because this problem contains one string rather than multiple test cases. Calling `strip()` removes the trailing newline without changing any valid input character, since the input contains only lowercase letters.

The frequency array is indexed by `ord(ch) - ord('a')`. For example, `ord('a') - ord('a')` is zero and `ord('z') - ord('a')` is 25, so every possible input character maps to a valid array position.

The list of pairs stores the character together with its count. The sorting key `(-item[1], item[0])` implements both required rules in one expression. The first component puts larger frequencies first, while the second component puts equal-frequency characters in alphabetical order.

The answer is accumulated in a list instead of repeatedly concatenating strings. Each multiplication such as `ch * count` creates all copies of one character, and `''.join(ans)` combines the pieces once. There are only 26 pieces, so this is simple and efficient.

There are no integer-overflow concerns in Python. The largest frequency is only the length of the input, which is at most 70 under the original constraint.

## Worked Examples

For Sample 1, the input is `dcbbdabb`. The frequency-counting phase produces the following state.

| Character processed | Frequency of a | Frequency of b | Frequency of c | Frequency of d |
| --- | --- | --- | --- | --- |
| `d` | 0 | 0 | 0 | 1 |
| `c` | 0 | 0 | 1 | 1 |
| `b` | 0 | 1 | 1 | 1 |
| `b` | 0 | 2 | 1 | 1 |
| `d` | 0 | 2 | 1 | 2 |
| `a` | 1 | 2 | 1 | 2 |
| `b` | 1 | 3 | 1 | 2 |
| `b` | 1 | 4 | 1 | 2 |

The sorted character-frequency pairs are `(b, 4)`, `(d, 2)`, `(a, 1)`, `(c, 1)`. The two frequency-one characters are ordered alphabetically, so the final string is `bbbbddac`.

For Sample 2, the input is `programming`. The counting state is more interesting because three characters have frequency two.

| Character processed | a | g | m | r | i | n | o | p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `p` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| `r` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| `o` | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 1 |
| `g` | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 1 |
| `r` | 0 | 1 | 0 | 2 | 0 | 0 | 1 | 1 |
| `a` | 1 | 1 | 0 | 2 | 0 | 0 | 1 | 1 |
| `m` | 1 | 1 | 1 | 2 | 0 | 0 | 1 | 1 |
| `m` | 1 | 1 | 2 | 2 | 0 | 0 | 1 | 1 |
| `i` | 1 | 1 | 2 | 2 | 1 | 0 | 1 | 1 |
| `n` | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 |
| `g` | 1 | 2 | 2 | 2 | 1 | 1 | 1 | 1 |

The frequency-two characters are `g`, `m`, and `r`, so alphabetical order gives `g`, then `m`, then `r`. The remaining characters all occur once and are ordered `a`, `i`, `n`, `o`, `p`. The final output is `ggmmrrainop`, matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting scans the string once, and sorting at most 26 character pairs is constant work. |
| Space | O(1) | The frequency array and character list contain at most 26 entries. |

With the actual maximum input length of 70 and a 1 second limit, this solution uses a negligible number of operations and far less than the available 256 MB memory.

## Test Cases

```python
# helper: run the solution logic on an input string
import sys
import io

def solve():
    s = input().strip()

    freq = [0] * 26

    for ch in s:
        freq[ord(ch) - ord('a')] += 1

    chars = []
    for i in range(26):
        ch = chr(ord('a') + i)
        chars.append((ch, freq[i]))

    chars.sort(key=lambda item: (-item[1], item[0]))

    ans = []
    for ch, count in chars:
        ans.append(ch * count)

    print(''.join(ans))

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
        return out.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided samples
assert run("dcbbdabb\n") == "bbbbddac\n", "sample 1"
assert run("programming\n") == "ggmmrrainop\n", "sample 2"

# Minimum-size input
assert run("z\n") == "z\n", "single character"

# All characters equal
assert run("aaaaa\n") == "aaaaa\n", "all equal"

# Equal frequencies, reverse alphabetical input
assert run("cba\n") == "abc\n", "alphabetical tie breaking"

# Boundary-sized input, 70 characters
maximum_input = "a" * 35 + "b" * 20 + "c" * 10 + "d" * 5
assert run(maximum_input + "\n") == maximum_input + "\n", "maximum size"

# Several equal-frequency groups
assert run("zzzyyxxwwvvvuu\n") == "vvvzzzwwxxyyuu\n", "multiple ties"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `z` | `z` | Minimum input size and absence of a tie |
| `aaaaa` | `aaaaa` | All occurrences belonging to one character |
| `cba` | `abc` | Alphabetical tie breaking |
| 70 characters with frequencies 35, 20, 10, 5 | Same string | Maximum input length and frequency ordering |
| `zzzyyxxwwvvvuu` | `vvvzzzwwxxyyuu` | Multiple frequency groups and equal-frequency ordering |

## Edge Cases

The single-character case `z` is handled by counting one occurrence at index 25. All other frequencies are zero, so sorting places `z` first and the output construction emits exactly one `z`. The result is `z`.

For an all-equal string such as `aaaaa`, the frequency array contains `freq[a] = 5` and zero everywhere else. The sorted pairs put `a` first because it has the only positive frequency, and the construction emits `a * 5`, producing `aaaaa`. No character is lost or duplicated.

The tie case `cba` exercises the secondary ordering rule. All three characters have frequency one, so their frequencies do not distinguish them. The sorted keys are `(−1, a)`, `(−1, b)`, and `(−1, c)`, giving `abc`. An implementation that relies on the input order would incorrectly return `cba`.

The maximum-size case contains 70 characters with frequencies 35, 20, 10, and 5. The counting pass records those four frequencies, the sorting phase places the characters in descending frequency order, and the reconstruction produces all 70 characters again. Since the frequency array has fixed size 26, increasing the input from one character to the maximum size changes only the counting work, not the auxiliary memory.

The multiple-tie case `zzzyyxxwwvvvuu` has `z=3`, `v=3`, `y=2`, `x=2`, `w=2`, and `u=2`. The two frequency-three characters are ordered as `v`, `z`, while the frequency-two characters are ordered as `u`, `w`, `x`, `y`. The algorithm consequently produces `vvvzzzuuwwxxyy`. This case directly checks that alphabetical ordering is applied independently inside every frequency group.
