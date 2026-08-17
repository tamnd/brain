---
title: "CF 102254E - Essay Time"
description: "We have a sequence of n words, in exactly the order they appeared in the essay. A word matters only when its length is at least four. For every such word, the first occurrence is allowed, while every later occurrence of the same word must be erased."
date: "2026-08-17T21:10:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102254
codeforces_index: "E"
codeforces_contest_name: "IME++ Starters Try-outs 2019"
rating: 0
weight: 102254
solve_time_s: 214
verified: false
draft: false
---

[CF 102254E - Essay Time](https://codeforces.com/problemset/problem/102254/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We have a sequence of `n` words, in exactly the order they appeared in the essay. A word matters only when its length is at least four. For every such word, the first occurrence is allowed, while every later occurrence of the same word must be erased.

The output is the number of occurrences that have to be erased, followed by those words in the order in which their repeated occurrences appear. If nothing has to be erased, the required output is `SAFO` instead.

The key distinction is between a word being repeated and an occurrence being repeated. For example, if the input contains `clean clean clean`, the word `clean` appears three times, but only the second and third occurrences belong in the answer. The output is consequently `2`, followed by two copies of `clean`.

The constraints make a quadratic approach impossible. There can be as many as `8 * 10^6` input words, and the total number of characters is also at most `8 * 10^6`. A solution should consequently process each input word a constant number of times, rather than repeatedly scanning all earlier words. The total character bound is especially useful because operations such as reading, hashing, and comparing the words can be made proportional to the total input size up to the usual hashing costs.

There are several edge cases that can silently break a careless implementation. First, words shorter than four characters do not participate in the repetition rule. For example,

```
3
cat
cat
dog
```

has no repeated word under the problem's rule, so the output is

```
SAFO
```

A solution that inserts every word into its duplicate-detection structure would incorrectly report `cat`.

Second, the first occurrence of a long word must not be printed. For

```
3
clean
bad
clean
```

the output is

```
1
clean
```

The first `clean` establishes that the word has appeared, while only the second one is an occurrence that must be erased.

Third, a word appearing three or more times must be printed once for every occurrence after the first. For

```
4
enough
enough
enough
enough
```

the output is

```
3
enough
enough
enough
```

A solution that merely records which words have duplicates would incorrectly print `enough` only once.

## Approaches

The direct approach is to compare every long word with all earlier long words. When processing the `i`-th word, scan positions `1` through `i-1` and check whether an identical word has already occurred. If one is found, print or record the current word as a repetition. This is correct because a word is repeated exactly when an equal word exists somewhere earlier in the input.

The problem is the number of comparisons. If all `n` words are long and distinct, the algorithm performs

`0 + 1 + 2 + ... + (n - 1) = n(n - 1)/2`

word comparisons. With `n = 8 * 10^6`, this is about `3.2 * 10^13` comparisons. Even if each comparison were treated as constant time, that is far beyond the two-second time limit. Real string comparisons can also inspect multiple characters, making the situation worse.

The observation that unlocks the faster solution is that we do not need to know which earlier position contained a word. We only need one bit of information: has this exact word appeared before? A hash set provides precisely that operation. For each long word, check whether it is already in the set. If it is, the current occurrence is a repeated occurrence. If it is not, insert it into the set so that future occurrences will be recognized.

Short words can be ignored completely. This is more than a minor optimization: it directly implements the rule that only words of length four or greater are subject to the restriction.

Because the input must be processed in order, we can detect a repeated occurrence at the moment it is read. We still need to print the number of repeated occurrences first, so the clean implementation records the repeated words while scanning. The total input length is at most `8 * 10^6`, so storing the repeated words in a byte buffer is inexpensive compared with storing all distinct words in the set.

The resulting comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) word comparisons, up to O(n²S) with character-level comparisons | O(nS) | Too slow |
| Hash Set | Expected O(S) total hashing and input processing | O(S) for stored distinct words and output buffer | Accepted |

Here `S` denotes the total number of characters in all input words, with `S <= 8 * 10^6`. The expected linear bound for the hash-set solution assumes the usual average-case behavior of a hash table.

## Algorithm Walkthrough

1. Read the number of words and create an empty set called `seen`. This set will contain exactly the long words that have already occurred.
2. Create a counter `repeated_count` and an output byte buffer. The counter tells us how many occurrences must be erased, while the buffer lets us postpone printing until the counter is known.
3. Read each word in its original order. Remove only the line ending, so the word itself remains unchanged.
4. If the word has fewer than four characters, ignore it. Such a word is allowed to appear any number of times and must never enter `seen`.
5. For a word of length at least four, check whether it is already in `seen`. If it is present, increment `repeated_count` and append this occurrence to the output buffer. We append every repeated occurrence, not merely the first duplicate.
6. If the word is not already in `seen`, insert it. From this point onward, any later equal word will correctly be classified as a repetition.
7. After all words have been processed, print `SAFO` if `repeated_count` is zero. Otherwise, print the count followed by the buffered repeated words, one per line.

### Why it works

After processing any prefix of the input, the invariant is that `seen` contains exactly the distinct words of length at least four that occurred in that prefix. For the next long word, membership in `seen` is therefore equivalent to having an earlier equal occurrence. If the word is present, the current occurrence must be erased and is added to the answer. If it is absent, this is its first occurrence, so inserting it is correct. Short words never affect the invariant because the rule does not apply to them. Since words are processed from left to right, every reported occurrence appears in exactly the required order, and every occurrence after the first is reported exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    seen = set()
    repeated_count = 0
    repeated = bytearray()

    for _ in range(n):
        word = input().strip()

        if len(word) < 4:
            continue

        if word in seen:
            repeated_count += 1
            repeated.extend(word)
            repeated.append(10)  # '\n'
        else:
            seen.add(word)

    out = sys.stdout.buffer

    if repeated_count == 0:
        out.write(b"SAFO\n")
    else:
        out.write(str(repeated_count).encode())
        out.write(b"\n")
        out.write(repeated)

if __name__ == "__main__":
    solve()
```

The `seen` set corresponds directly to the first part of the algorithm. Python's set gives expected constant-time membership testing and insertion, so every relevant word can be processed without scanning previous words.

The solution uses `input = sys.stdin.readline` as requested, avoiding the much slower repeated use of higher-level input mechanisms. The words are kept as strings in the set, while the repeated output is accumulated in a `bytearray`. Using a byte buffer avoids creating a separate Python string for the complete output.

The order of operations is significant. The membership check happens before insertion. If we inserted the word first and then checked membership, every long word would appear to be a duplicate of itself. The correct sequence is to test whether it was seen, report it if so, and otherwise insert it.

The length check uses `< 4`, because a word of length exactly four is subject to the restriction. A word of length three is ignored.

There is no integer-overflow issue in Python. The counter can also safely represent the maximum possible number of repeated occurrences.

The special `SAFO` output is handled separately because the required output is not `0` followed by an empty list. When at least one repetition exists, the first line is the count and the following lines contain the repeated occurrences.

## Worked Examples

For Sample 1, the processing state is:

| Word | Length at least 4? | In `seen` before processing? | Action | `repeated_count` |
| --- | --- | --- | --- | --- |
| `not` | No | No | Ignore | 0 |
| `clean` | Yes | No | Insert | 0 |
| `bad` | No | No | Ignore | 0 |
| `posture` | Yes | No | Insert | 0 |
| `clean` | Yes | Yes | Record repetition | 1 |
| `enough` | Yes | No | Insert | 1 |

The first `clean` is inserted into `seen`. When the second `clean` arrives, membership succeeds, so only that second occurrence is recorded. The final output is:

```
1
clean
```

For Sample 2, the state becomes:

| Word | Length at least 4? | In `seen` before processing? | Action | `repeated_count` |
| --- | --- | --- | --- | --- |
| `not` | No | No | Ignore | 0 |
| `clean` | Yes | No | Insert | 0 |
| `enough` | Yes | No | Insert | 0 |
| `bad` | No | No | Ignore | 0 |
| `posture` | Yes | No | Insert | 0 |
| `clean` | Yes | Yes | Record repetition | 1 |
| `enough` | Yes | Yes | Record repetition | 2 |
| `enough` | Yes | Yes | Record repetition | 3 |

The two later occurrences of `enough` are both reported. The set does not remove or alter `enough` after the first duplicate, so every subsequent occurrence continues to be recognized. The output is:

```
3
clean
enough
enough
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected O(S) | Every word is read once, and every relevant word is hashed and checked once. |
| Space | O(S) | The distinct long words in `seen` contain at most O(S) characters, and the repeated output is also at most O(S) characters. |

Here `S` is the total length of all words and is at most `8 * 10^6`. The solution therefore scales with the actual input size instead of the square of the number of words. The memory limit is 1024 MB, which gives Python enough room for the hash set and the compact output buffer for this input bound.

## Test Cases

```python
import sys
import io

def solve():
    n = int(input())

    seen = set()
    repeated_count = 0
    repeated = bytearray()

    for _ in range(n):
        word = input().strip()

        if len(word) < 4:
            continue

        if word in seen:
            repeated_count += 1
            repeated.extend(word.encode())
            repeated.append(10)
        else:
            seen.add(word)

    out = sys.stdout
    if repeated_count == 0:
        out.write("SAFO\n")
    else:
        out.write(str(repeated_count) + "\n")
        out.write(repeated.decode())

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

# Provided sample 1
assert run(
    """6
not
clean
bad
posture
clean
enough
"""
) == "1\nclean\n", "sample 1"

# Provided sample 2
assert run(
    """8
not
clean
enough
bad
posture
clean
enough
enough
"""
) == "3\nclean\nenough\nenough\n", "sample 2"

# Minimum size
assert run(
    """1
abcd
"""
) == "SAFO\n", "minimum-size input"

# Short words are never considered repeated
assert run(
    """6
a
a
abc
abc
abcd
abcd
"""
) == "1\nabcd\n", "short words must be ignored"

# All equal long words: every occurrence after the first is repeated
assert run(
    """5
word
word
word
word
word
"""
) == "4\nword\nword\nword\nword\n", "all equal values"

# Boundary around length four, including several distinct words
assert run(
    """7
aaa
aaaa
aaa
aaaa
bbbb
bbbb
ccc
"""
) == "2\naaaa\nbbbb\n", "length-four boundary"

# Maximum n permitted by the constraints. All words have length one,
# so the total input length is 8 * 10^6 and none of them are relevant.
max_n = 8_000_000
maximum_input = str(max_n) + "\n" + ("a\n" * max_n)
assert run(maximum_input) == "SAFO\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / abcd` | `SAFO` | Minimum input and first occurrence handling |
| Repeated `a` and `abc`, repeated `abcd` | `1 / abcd` | Words shorter than four characters must be ignored |
| Five copies of `word` | Four copies of `word` | Every occurrence after the first must be reported |
| `aaa`, `aaaa`, `bbbb`, `ccc` combinations | `2 / aaaa / bbbb` | Exact four-character boundary |
| Eight million one-character words | `SAFO` | Maximum `n` and the total-length constraint |

The maximum-size assertion deliberately uses one-character words. Eight million words of length four would violate the total-length limit, since that would require 32 million characters. Eight million one-character words satisfy the bound and also verify that irrelevant short words can be processed without entering the hash set.

## Edge Cases

A repeated short word must not be reported. For

```
3
cat
cat
dog
```

both copies of `cat` have length three, so the algorithm reaches the length check and immediately ignores each one. `seen` remains empty, `repeated_count` remains zero, and the output is:

```
SAFO
```

This catches the common mistake of interpreting "repeated word" without applying the four-character restriction.

A word of exactly four characters must be treated as a relevant word. For

```
2
aaaa
aaaa
```

the first `aaaa` is inserted into `seen`. The second is found there and is recorded. The result is:

```
1
aaaa
```

The `< 4` condition is what makes length three and length four behave differently.

A word repeated more than twice must produce multiple output entries. For

```
4
same
same
same
same
```

the first occurrence enters `seen`, while the next three all find `same` already present. The counter reaches three and the buffer contains three copies, producing:

```
3
same
same
same
```

This is why the set alone is not enough to describe the output. It tells us whether a word has appeared, while the counter and output buffer track every later occurrence.

Finally, the output order follows directly from the left-to-right scan. For

```
5
alpha
beta
alpha
beta
alpha
```

the first `alpha` and `beta` are inserted. The third input word produces `alpha`, the fourth produces `beta`, and the fifth produces `alpha` again. The result is:

```
3
alpha
beta
alpha
```

The algorithm never sorts the repeated words and never groups equal words together. It records them at the moment their repeated occurrence is encountered, which preserves exactly the order required by the problem.
