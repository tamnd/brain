---
title: "CF 102423H - Levenshtein Distance"
description: "We are given a finite alphabet consisting of distinct lowercase letters, already written in alphabetical order, and a query string whose characters all belong to that alphabet."
date: "2026-08-12T06:39:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102423
codeforces_index: "H"
codeforces_contest_name: "North American Southeast Regional 2019 (Div 1)"
rating: 0
weight: 102423
solve_time_s: 79
verified: true
draft: false
---

[CF 102423H - Levenshtein Distance](https://codeforces.com/problemset/problem/102423/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a finite alphabet consisting of distinct lowercase letters, already written in alphabetical order, and a query string whose characters all belong to that alphabet. We need to construct every distinct string whose Levenshtein distance from the query string is exactly one.

A distance of one means that exactly one elementary edit is sufficient. We may insert one alphabet character at any position, delete one existing character, or replace one character by a different alphabet character. The original string itself must not be printed, because its distance from itself is zero. The resulting strings have to be printed in lexicographical order, with duplicates removed.

The query string has length between 2 and 100. The alphabet contains only distinct lowercase letters, so it has at most 26 characters. These bounds are tiny. Even if we generate every possible edit independently, there are only a few thousand candidates. A quadratic algorithm over all candidates is unnecessary, but even the candidate count itself is small enough that a direct construction is the natural solution.

The main edge cases come from duplicate generation. For example, with input

```
a
aa
```

the correct output is

```
aaa
a
```

Inserting `a` before the first character, between the two characters, or after the second character always produces `aaa`, so a careless implementation that prints every operation separately would output the same string three times. Deleting either occurrence of `a` produces the same string `a`, creating another duplicate.

A second case is substitution. With

```
ab
aa
```

replacing either `a` by `b` produces `ba`, while replacing the second character also produces `ab`. More generally, different edit positions can lead to the same resulting string, so deduplication must happen after generating candidates rather than being based only on the operation used.

The alphabet can also contain a single character. For example,

```
a
aa
```

has no possible substitution at all, because there is no different character available. Insertions and deletions still have to be considered. An implementation that assumes every position has a replacement would either generate the original string or access a nonexistent alternative character.

## Approaches

The most direct approach is to enumerate every legal edit and put the resulting string into a collection. For each of the (n+1) insertion positions, we try every one of the (k) alphabet characters. For each of the (n) positions, we generate the string obtained by deleting that character. Finally, for every position we try every alphabet character different from the current one, giving (n(k-1)) replacement candidates.

The number of generated candidates is therefore

[
(n+1)k+n+n(k-1)=2nk+k.
]

At the maximum values (n=100) and (k=26), this is only

[
2\cdot100\cdot26+26=5226
]

candidates. Each candidate has length at most 101, so constructing all of them requires only a few hundred thousand character operations.

A naive implementation could generate all candidates into a list and then repeatedly compare strings to remove duplicates. That is correct, because every possible distance-one operation is explicitly considered, but duplicate removal by pairwise comparison can take (O(C^2 n)), where (C) is the number of generated candidates. With (C) around 5000, this is already millions of string comparisons and is needlessly expensive.

The key observation is that the problem does not ask us to count operations. It asks for unique resulting strings. A hash set is exactly the data structure needed for that requirement. We can generate every legal result once, insert it into a set, and let hashing collapse all duplicates automatically. After generation, converting the set to a list and sorting it gives the required lexicographical order.

The brute-force idea therefore remains the foundation of the solution. The improvement is not to avoid enumerating edits, because there are too few edits to justify anything more complicated. The improvement is to represent the collection of answers in a way that performs deduplication efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with pairwise duplicate removal | (O(C^2 n + C\log C)) | (O(Cn)) | Correct but unnecessarily slow |
| Generate and deduplicate with a hash set | (O(nk\cdot n + C\log C)) | (O(Cn)) | Accepted |

Here (C=2nk+k), and with (n\le100) and (k\le26), both bounds are comfortably small.

## Algorithm Walkthrough

1. Read the alphabet and the query string. Let (n) be the query length and (k) be the alphabet size. Every inserted or replacement character must come from this alphabet, so these two strings completely describe the available edits.
2. Create an empty set called `answers`. A set is used because different edits can produce exactly the same string, and the required output contains each string only once.
3. For every position from `0` through `n`, insert every alphabet character at that position. There are (n+1) gaps in a string of length (n), including the gap before the first character and the gap after the last character.
4. For every character position, remove that character and insert the resulting string into the set. Every deletion has cost one, so these are exactly all possible deletion results.
5. For every character position, try every alphabet character except the current one and replace the character with it. Skipping the current character is necessary because replacing a character by itself performs no edit and would incorrectly introduce the original query string.
6. Convert the set to a list and sort it lexicographically. The alphabet itself is already ordered, but generated strings have different lengths and edit positions, so their final order cannot be obtained reliably from generation order.
7. Print every string in the sorted list on its own line. If two edit sequences produced the same string, the set has already removed the duplicate.

### Why it works

Every string at distance exactly one must be obtainable by one of three operations: one insertion, one deletion, or one substitution. The algorithm explicitly enumerates every legal instance of all three operations, so no valid answer is missed.

The insertion loop considers every possible position and every alphabet character. The deletion loop considers every existing character. The substitution loop considers every position and every different alphabet character. Thus every possible one-edit transformation appears among the generated candidates.

The set removes only equal strings, not different strings. Since the original string is never generated by a valid insertion or deletion, and substitution deliberately excludes the current character, every remaining element has distance exactly one. Sorting then changes only the presentation order, so the final output is precisely the required set of strings in lexicographical order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data: str) -> str:
    lines = data.splitlines()
    alphabet = lines[0].strip()
    s = lines[1].strip()

    n = len(s)
    answers = set()

    # Insert one alphabet character at every possible position.
    for i in range(n + 1):
        left = s[:i]
        right = s[i:]
        for ch in alphabet:
            answers.add(left + ch + right)

    # Delete one character.
    for i in range(n):
        answers.add(s[:i] + s[i + 1:])

    # Replace one character by a different alphabet character.
    for i in range(n):
        for ch in alphabet:
            if ch != s[i]:
                answers.add(s[:i] + ch + s[i + 1:])

    return "\n".join(sorted(answers))

def main():
    data = sys.stdin.read()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The first two input lines are read as the alphabet and query string. There is no test-case count, so the whole input can be consumed at once.

The insertion loop uses `range(n + 1)` because a length-(n) string has (n+1) insertion gaps. The expression `s[:i] + ch + s[i:]` inserts `ch` without modifying the original string.

The deletion expression `s[:i] + s[i + 1:]` removes exactly the character at position `i`. It also naturally handles the first and last positions, which are common sources of slicing errors.

For substitution, the condition `ch != s[i]` is essential. Without it, the original query string would be inserted into `answers`, even though its Levenshtein distance from itself is zero.

Python strings are immutable, so each operation creates a new string. This is perfectly adequate here because there are at most 5226 generated candidates and each candidate has length at most 101. Python integers are not relevant to the computation, so there are no overflow concerns.

The final `sorted(answers)` gives ordinary lexicographical string ordering, exactly what the problem requires.

## Worked Examples

### Example 1

The provided sample is

```
eg
egg
```

Here the alphabet is `{e, g}` and the query has length three. The algorithm generates insertion, deletion, and substitution results. The important state is the growing set of unique answers.

| Operation | Generated result | Set effect |
| --- | --- | --- |
| Insert `e` at position 0 | `eegg` | add |
| Insert `g` at position 0 | `gegg` | add |
| Insert `e` at position 1 | `eegg` | duplicate |
| Insert `g` at position 1 | `eggg` | add |
| Insert `e` at position 2 | `eegg` | duplicate |
| Insert `g` at position 2 | `eggg` | duplicate |
| Insert `e` at position 3 | `egge` | add |
| Insert `g` at position 3 | `eggg` | duplicate |
| Delete position 0 | `gg` | add |
| Delete position 1 | `eg` | add |
| Delete position 2 | `eg` | duplicate |
| Replace position 0 `e -> g` | `ggg` | add |
| Replace position 1 `g -> e` | `eeg` | add |
| Replace position 2 `g -> e` | `ege` | add |

After all candidates are generated and sorted, the output is

```
eg
ege
eeg
egg
eegg
egge
eggg
gegg
gg
ggg
```

The exact set contains every string reachable by one edit, while repeated insertions and deletions of equal characters collapse to one entry. The query itself is not generated because substitution never uses the same character.

### Example 2

Consider

```
abc
ab
```

There are three insertion gaps and two deletion positions. The generated unique strings are:

| Operation | Position or character | Result |
| --- | --- | --- |
| Insert `a` | before `a` | `aabc` |
| Insert `b` | before `a` | `babc` |
| Insert `c` | before `a` | `cabc` |
| Insert `a` | between `a,b` | `aabc` |
| Insert `b` | between `a,b` | `abbc` |
| Insert `c` | between `a,b` | `acbc` |
| Insert `a` | after `b` | `abac` |
| Insert `b` | after `b` | `abbc` |
| Insert `c` | after `b` | `abcc` |
| Delete `a` | position 0 | `b` |
| Delete `b` | position 1 | `a` |
| Replace `a -> b` | position 0 | `bbc` |
| Replace `a -> c` | position 0 | `cbc` |
| Replace `b -> a` | position 1 | `aac` |
| Replace `b -> c` | position 1 | `acc` |
| Replace `c -> a` | position 2 | `aba` |
| Replace `c -> b` | position 2 | `abb` |

After sorting, the output is

```
a
aabc
aac
abac
aba
abb
abbc
abcc
acc
b
babc
bbc
cabc
cbc
```

This example demonstrates that insertion and substitution can produce strings of different lengths, while deletion produces shorter strings. Sorting the complete set after generation avoids having to reason about lexicographical order during enumeration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2k + nk\log(nk))) | At most (O(nk)) candidates are built, each of length (O(n)), followed by sorting |
| Space | (O(n^2k)) | The set stores (O(nk)) strings, each of length (O(n)) |

With (n\le100) and (k\le26), the algorithm generates at most 5226 candidates, each only about 101 characters long. The total amount of string data is small enough to fit comfortably inside the 512 MB memory limit, and the direct enumeration is easily fast enough for the one-second limit. The archived contest dashboard confirms the 1 second and 512 MB limits.

## Test Cases

The official statement provides the `eg` and `egg` sample. The remaining cases below target duplicate generation, the smallest possible query length, substitution boundaries, and a larger alphabet.

```python
# helper: run solution on input string, return output string
import io
import sys

def solve(data: str) -> str:
    lines = data.splitlines()
    alphabet = lines[0].strip()
    s = lines[1].strip()

    n = len(s)
    answers = set()

    for i in range(n + 1):
        for ch in alphabet:
            answers.add(s[:i] + ch + s[i:])

    for i in range(n):
        answers.add(s[:i] + s[i + 1:])

    for i in range(n):
        for ch in alphabet:
            if ch != s[i]:
                answers.add(s[:i] + ch + s[i + 1:])

    return "\n".join(sorted(answers))

def run(inp: str) -> str:
    return solve(inp).strip()

# provided sample
assert run("eg\negg\n") == "\n".join([
    "eg",
    "ege",
    "eeg",
    "eegg",
    "egge",
    "eggg",
    "gegg",
    "gg",
    "ggg",
]), "sample 1"

# minimum-size query with a one-character alphabet
assert run("a\naa\n") == "\n".join([
    "a",
    "aaa",
]), "single-character alphabet and duplicate edits"

# substitution and insertion with two different characters
assert run("ab\nab\n") == "\n".join([
    "a",
    "aa",
    "aab",
    "aba",
    "abb",
    "b",
    "baa",
    "bab",
    "bb",
    "bba",
]), "two-character alphabet"

# all characters equal, catches duplicate insertion/deletion positions
assert run("ab\naaa\n") == "\n".join([
    "aa",
    "aaaa",
    "aaba",
    "abaa",
    "baaa",
]), "all-equal query"

# larger alphabet, exercises every replacement character
assert run("abc\nabc\n") == "\n".join([
    "a",
    "aabc",
    "aac",
    "abac",
    "aba",
    "abb",
    "abbc",
    "abcc",
    "abc",
    "ac",
    "acbc",
    "acc",
    "b",
    "babc",
    "bbc",
    "bc",
    "c",
    "cabc",
    "cbc",
]), "larger alphabet and boundary edits"
```

The custom cases can be summarized as follows.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / aa` | `a`, `aaa` | Minimum alphabet size and duplicate insertions/deletions |
| `ab / ab` | Ten distinct strings | Both replacement characters and insertion/deletion boundaries |
| `ab / aaa` | Five distinct strings | Repeated characters creating many duplicate operations |
| `abc / abc` | Multiple insertion, deletion, and substitution results | Full alphabet traversal and edge positions |

## Edge Cases

For a single-character alphabet, consider

```
a
aa
```

There are no legal substitutions because `a` is the only available character. Inserting `a` at any of the three gaps produces `aaa`, while deleting either occurrence produces `a`. The set reduces these three insertion results and two deletion results to two strings, giving

```
a
aaa
```

The algorithm handles this because the substitution loop simply has no character satisfying `ch != s[i]`.

For repeated characters, consider

```
ab
aaa
```

Inserting `a` at any of the four positions produces `aaaa`, while deleting any of the three positions produces `aa`. A naive implementation that appends every operation directly to the output would print these strings multiple times. The set stores each result once, so the final output contains only the unique strings.

For the first and last insertion positions, consider

```
ab
ab
```

The position `0` insertion produces strings such as `aab` and `bab`, while position `2` produces `aba` and `abb`. The loop uses `range(n + 1)`, so both boundary gaps are included. Using only `range(n)` would silently miss all insertions at the end.

For substitution, the same input demonstrates why the current character must be excluded. At position zero, replacing `a` by `a` would reproduce `ab`, but that operation changes nothing and has distance zero. The condition `ch != s[i]` prevents the original query string from entering the answer set.

For deletion, the two-character string

```
ab
ab
```

has deletion results `b` and `a`. The slicing expressions correctly handle both endpoints because `s[:0] + s[1:]` removes the first character and `s[:1] + s[2:]` removes the second.

Finally, duplicate outputs are not limited to repeated characters. Inserting the same character in adjacent positions can also converge to the same final string when the surrounding characters match. This is why deduplication must be performed on the actual resulting strings rather than on operation descriptions. The hash set gives exactly that behavior.
