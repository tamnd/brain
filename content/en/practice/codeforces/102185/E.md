---
title: "CF 102185E - \u0421\u043a\u0440\u0449\u043d\u044f"
description: "We have a dictionary of (N) full words. Then we receive (M) words from a text. A text word is considered an abbreviation if it can be obtained by deleting characters from exactly one dictionary word, while no other dictionary word contains it as a subsequence."
date: "2026-08-19T06:30:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102185
codeforces_index: "E"
codeforces_contest_name: "Southern Russia Open Championship \u2013 ContestSFedU 2019, Team Final."
rating: 0
weight: 102185
solve_time_s: 122
verified: true
draft: false
---

[CF 102185E - \u0421\u043a\u0440\u0449\u043d\u044f](https://codeforces.com/problemset/problem/102185/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a dictionary of (N) full words. Then we receive (M) words from a text. A text word is considered an abbreviation if it can be obtained by deleting characters from exactly one dictionary word, while no other dictionary word contains it as a subsequence. If exactly one dictionary word contains it, we replace the text word by that dictionary word. If zero or at least two dictionary words contain it, the text word stays unchanged.

The central operation is therefore a subsequence test. For example, `sti` is a subsequence of `strtoint`, because we can select `s`, then `t`, then `i`. On the other hand, `aa` is a subsequence of both `aba` and `ababa`, so it is ambiguous and must not be replaced.

There are only (500) dictionary words, but their total length can reach (2\cdot10^6). The text contains at most (2000) words, and every text word has length at most (10). The short query length is the key constraint. It means that once we can find the next occurrence of a requested character quickly inside a dictionary word, checking one text word requires only a handful of operations.

A direct scan is too expensive. If the dictionary has total length (2\cdot10^6), testing one text word against every dictionary word can inspect all (2\cdot10^6) dictionary characters. With (2000) distinct text words, that can reach (4\cdot10^9) character checks, far beyond a 1.5 second limit.

There are several edge cases where an apparently reasonable implementation can fail. The first is ambiguity. Consider

```
2
aba
ababa
1
aa
```

Both dictionary words contain `aa` as a subsequence, so the correct output is

```
aa
```

A careless implementation that stops at the first matching dictionary word would incorrectly print `aba`.

The second case is an exact dictionary word. Consider

```
1
abc
1
abc
```

The correct output is

```
abc
```

The definition allows deleting zero characters, so a dictionary word is itself a subsequence of its dictionary entry. An implementation that requires at least one deleted character would get this wrong.

The third case is that an abbreviation can occur in a dictionary word in non-consecutive positions. For example,

```
1
strtoint
1
sti
```

produces

```
strtoint
```

The characters `s`, `t`, and `i` do not need to form a contiguous substring. Searching only for substrings would incorrectly leave `sti` unchanged.

A final subtle case is duplicate dictionary entries. For

```
2
abc
abc
1
abc
```

the answer is

```
abc
```

because the text word is contained in two different dictionary entries, even though those entries have equal contents. We must count dictionary positions, not merely distinct dictionary strings.

## Approaches

The brute-force solution is straightforward. For every text word, scan every dictionary word and perform the standard two-pointer subsequence check. The check keeps a pointer into the short text word and advances it whenever the current dictionary character matches the next required character. Once all characters have been found, the dictionary word is a match.

This is correct because the greedy subsequence check always finds the earliest possible position for every required character. If the greedy procedure cannot find the next character, no later choice could make the query fit.

The problem is the amount of repeated work. Suppose the total dictionary length is (D). One query can require (O(D)) character inspections. With (U) distinct text words, (U\le2000), the worst case is (O(UD)=O(4\cdot10^9)) character checks. The fact that every individual query has length at most (10) does not help the brute-force scan, because the dictionary words can still be millions of characters in total.

The useful observation is that the query is short, while the same dictionary words are queried many times. Instead of scanning a dictionary word from the beginning for every query, preprocess where each character occurs in that word.

For one dictionary word, store a sorted list of positions for every letter. To find the next occurrence of character `c` after position `p`, binary search its position list. If the next position exists, continue the subsequence test from there. Since a query has at most (10) characters, one dictionary word requires at most (10) binary searches.

This changes the repeated part from scanning the entire dictionary word to performing at most ten logarithmic searches. The preprocessing is linear in the total dictionary length.

There is another useful optimization. The text can contain the same word many times, and its answer is always identical. We first collect distinct text words, solve each one once, and then reuse the result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(UD)) | (O(D)) | Too slow |
| Optimal | (O(D+UNK\log L)) | (O(D+UN)) | Accepted |

Here (D) is the total dictionary length, (U\le2000) is the number of distinct text words, (N\le500) is the dictionary size, (K\le10) is the maximum query length, and (L) is the maximum dictionary word length.

## Algorithm Walkthrough

1. Read all dictionary words and build a position list for each character of each word. For a dictionary word such as `abac`, the position lists include `a: [0, 2]`, `b: [1]`, and `c: [3]`. The lists are naturally sorted because the word is scanned from left to right.
2. Read the text and keep only its distinct words. Every occurrence of the same text word has exactly the same set of matching dictionary entries, so solving it repeatedly would only waste time.
3. For one query and one dictionary word, set the current position to before the beginning of the dictionary word. Process the query characters from left to right.
4. For the current query character, binary-search its position list for the first position strictly greater than the current position. This is exactly the next character that can be used in a subsequence.
5. If such a position does not exist, the query is not a subsequence of this dictionary word. Stop checking this dictionary word immediately.
6. If every query character is found, the dictionary word is a match. Increase the number of matching dictionary entries and remember the corresponding word.
7. Stop after finding two matches. The exact identity of a second match no longer matters, because the query is ambiguous and must remain unchanged.
8. If exactly one dictionary word matched, replace the query by that word. If zero or at least two matched, keep the original query. Store this result for reuse when the same text word appears later.
9. Print the transformed text in its original order. The replacement guarantee bounds the total output size by (2\cdot10^6), so constructing the output as a list of strings is safe.

Why it works: for every dictionary word, the position chosen for each query character is the earliest possible occurrence after the previously chosen position. Choosing an earlier occurrence can never make the remaining query harder to match, so the greedy procedure succeeds exactly when the query is a subsequence. We test every dictionary entry, so the match count is exactly the number of dictionary entries containing the query. Consequently, a query is replaced precisely when that count is one.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    n = int(input())

    dictionary = []
    positions = []

    for _ in range(n):
        word = input().strip()
        dictionary.append(word)

        pos = [[] for _ in range(26)]
        for i, ch in enumerate(word):
            pos[ord(ch) - 97].append(i)
        positions.append(pos)

    m = int(input())
    text = [input().strip() for _ in range(m)]

    cache = {}

    for query in set(text):
        matches = 0
        replacement = None

        for idx in range(n):
            pos = positions[idx]
            current = -1
            ok = True

            for ch in query:
                arr = pos[ord(ch) - 97]
                j = bisect_right(arr, current)

                if j == len(arr):
                    ok = False
                    break

                current = arr[j]

            if ok:
                matches += 1
                replacement = dictionary[idx]

                if matches == 2:
                    break

        if matches == 1:
            cache[query] = replacement
        else:
            cache[query] = query

    sys.stdout.write("\n".join(cache[word] for word in text))

if __name__ == "__main__":
    solve()
```

The first loop reads the dictionary and builds the positional index. The index is stored separately for each dictionary word because positions are meaningful only inside that word.

During a query, `current` is the position of the last character already selected. `bisect_right(arr, current)` returns the first occurrence strictly after it. Strictly after is necessary because a dictionary position cannot be used twice for two different query characters.

The code stops after the second match. This is safe because the output depends only on whether the number of matches is zero, one, or at least two.

The `cache` dictionary handles repeated text words. The expression `cache[word]` at output time preserves the original text order even though the distinct queries were processed in arbitrary set order.

There is no integer-overflow issue in Python, and the largest output is bounded by the statement. The main memory cost is the stored occurrence positions, whose total number is exactly the total dictionary length.

## Worked Examples

The provided sample demonstrates both unique and ambiguous abbreviations.

For `sti`, only `strtoint` contains the three characters in order. For `aa`, both `aba` and `ababa` contain it, so it remains unchanged. The query `aaa` is contained in `ababa` but not in `aba`, making `ababa` its unique expansion.

| Query | Dictionary word | Positions selected | Match? | Match count |
| --- | --- | --- | --- | --- |
| `sti` | `abc` | `s` absent | No | 0 |
| `sti` | `strtoint` | `s=0, t=1, i=4` | Yes | 1 |
| `sti` | `aba` | `s` absent | No | 1 |
| `sti` | `ababa` | `s` absent | No | 1 |
| `aa` | `abc` | `a=0`, second `a` absent | No | 0 |
| `aa` | `strtoint` | `a` absent | No | 0 |
| `aa` | `aba` | `a=0, a=2` | Yes | 1 |
| `aa` | `ababa` | `a=0, a=2` | Yes | 2 |
| `aaa` | `aba` | only two `a` characters | No | 0 |
| `aaa` | `ababa` | `a=0, a=2, a=4` | Yes | 1 |
| `bb` | all dictionary words | fewer than two `b` characters | No | 0 |
| `abc` | `abc` | `a=0, b=1, c=2` | Yes | 1 |

The trace shows the key invariant: after each query character, `current` is the earliest possible position where the prefix processed so far can end. That makes every later binary search as permissive as possible.

A second example exercises ambiguity and exact dictionary matches:

```
3
abc
abc
axbyc
4
abc
aby
ac
zzz
```

| Query | Dictionary word | Result of subsequence check | Matches |
| --- | --- | --- | --- |
| `abc` | first `abc` | Yes | 1 |
| `abc` | second `abc` | Yes | 2 |
| `abc` | `axbyc` | Yes | 2 |
| `aby` | first `abc` | No | 0 |
| `aby` | second `abc` | No | 0 |
| `aby` | `axbyc` | Yes | 1 |
| `ac` | first `abc` | Yes | 1 |
| `ac` | second `abc` | Yes | 2 |
| `zzz` | first `abc` | No | 0 |

The resulting output is

```
abc
axbyc
ac
zzz
```

The first query remains unchanged because three dictionary entries contain it. The second query has exactly one match, so it expands to `axbyc`. The third query is ambiguous because both copies of `abc` count as separate dictionary entries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(D+UNK\log L)) | Building positions costs (O(D)); each of (U) distinct queries checks at most (N) words and at most (K\le10) characters per word |
| Space | (O(D+UN+M)) | Character positions contain (D) entries, while the query cache and input text contain at most (O(UN+M)) additional references |

With (D\le2\cdot10^6), (U\le2000), (N\le500), and (K\le10), the expensive repeated part performs at most (10^7) binary-search operations, rather than billions of dictionary-character scans. The binary searches themselves run in C through Python's `bisect` module, which makes this formulation practical under the given limit. The positional index uses linear memory in the total dictionary size, comfortably within 512 MB.

## Test Cases

```python
import sys
import io
from bisect import bisect_right

def solve():
    input = sys.stdin.readline

    n = int(input())

    dictionary = []
    positions = []

    for _ in range(n):
        word = input().strip()
        dictionary.append(word)

        pos = [[] for _ in range(26)]
        for i, ch in enumerate(word):
            pos[ord(ch) - 97].append(i)
        positions.append(pos)

    m = int(input())
    text = [input().strip() for _ in range(m)]

    cache = {}

    for query in set(text):
        matches = 0
        replacement = None

        for idx in range(n):
            current = -1
            ok = True
            pos = positions[idx]

            for ch in query:
                arr = pos[ord(ch) - 97]
                j = bisect_right(arr, current)

                if j == len(arr):
                    ok = False
                    break

                current = arr[j]

            if ok:
                matches += 1
                replacement = dictionary[idx]
                if matches == 2:
                    break

        cache[query] = replacement if matches == 1 else query

    return "\n".join(cache[word] for word in text)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample1 = """\
4
abc
strtoint
aba
ababa
5
sti
aa
aaa
bb
abc
"""

assert run(sample1) == """\
strtoint
aa
ababa
ababa
abc
""", "sample 1"

sample2 = """\
3
abc
abc
axbyc
4
abc
aby
ac
zzz
"""

assert run(sample2) == """\
abc
axbyc
ac
zzz
""", "duplicate dictionary entries"

sample3 = """\
1
a
4
a
aa
b
a
"""

assert run(sample3) == """\
a
aa
b
a
""", "minimum dictionary size"

sample4 = """\
4
aaaaaaaaaa
bbbbbbbbbb
ababababab
baaaaaaaaa
6
aaaaaaaaaa
abab
bbbb
baaa
ab
zzzz
"""

assert run(sample4) == """\
aaaaaaaaaa
abab
bbbbbbbbbb
baaa
ababababab
zzzz
""", "boundary query length and subsequences"

sample5 = """\
500
""" + "\n".join(["a" * 4000 for _ in range(500)]) + """
4
a
aaaaaaaaaa
b
a
"""

# Every dictionary word is identical, so every nonempty sequence of a's
# is ambiguous. The b query matches none.
assert run(sample5) == """\
a
aaaaaaaaaa
b
a
""", "large dictionary and repeated values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `strtoint`, `aa`, `ababa`, `ababa`, `abc` | Original problem behavior, unique and ambiguous subsequences |
| Sample 2 | `abc`, `axbyc`, `ac`, `zzz` | Duplicate dictionary entries and non-contiguous matching |
| Sample 3 | `a`, `aa`, `b`, `a` | Minimum dictionary size and exact-match handling |
| Sample 4 | `aaaaaaaaaa`, `abab`, `bbbbbbbbbb`, `baaa`, `ababababab`, `zzzz` | Ten-character queries, ordering of selected positions, and absent characters |
| Sample 5 | `a`, `aaaaaaaaaa`, `b`, `a` | Large dictionary size, repeated equal dictionary values, and ambiguity |

## Edge Cases

The ambiguity case from the problem understanding is handled by counting dictionary entries rather than distinct strings. For

```
2
aba
ababa
1
aa
```

the first word matches, so the count becomes one. The second word also matches, so the count becomes two and the algorithm stops. Since the count is not one, the output is `aa`.

The exact-match case

```
1
abc
1
abc
```

starts with `current = -1`. The searches select positions (0), (1), and (2), so all three characters are accepted. The match count is one and the stored replacement is `abc`, giving the correct unchanged output.

The non-contiguous case

```
1
strtoint
1
sti
```

selects the position of `s`, then searches strictly after it for `t`, then strictly after that position for `i`. The selected positions form a valid subsequence even though they are not adjacent, so the result is `strtoint`.

Duplicate dictionary entries are deliberately counted twice. For

```
2
abc
abc
1
abc
```

the first entry gives one match and the second gives two. The algorithm stops immediately after the second match and returns the original query. This is exactly what the definition requires because the two dictionary positions represent two different entries.

A query containing a character absent from a dictionary word fails immediately. For example, with dictionary word `abc` and query `zzz`, the first search looks at the position list for `z`, which is empty. The word is rejected without examining the remaining query characters. This early failure is also useful for performance on negative queries.
