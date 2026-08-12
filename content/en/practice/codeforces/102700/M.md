---
title: "CF 102700M - Magic spells"
description: "We have one reference string s. Every non-empty subsequence of s is considered a valid spell. For each input string a, some original spell has been followed by an arbitrary suffix, so the useful part of a is exactly its longest prefix that can still be embedded as a subsequence…"
date: "2026-08-12T19:13:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102700
codeforces_index: "M"
codeforces_contest_name: "2020 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102700
solve_time_s: 787
verified: true
draft: false
---

[CF 102700M - Magic spells](https://codeforces.com/problemset/problem/102700/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have one reference string `s`. Every non-empty subsequence of `s` is considered a valid spell. For each input string `a`, some original spell has been followed by an arbitrary suffix, so the useful part of `a` is exactly its longest prefix that can still be embedded as a subsequence of `s`.

The task is thus a prefix-subsequence problem. Starting from the beginning of `a`, we want to keep taking characters as long as they can appear in `s` in strictly increasing positions. The moment a character cannot be placed after the previous matched position, no longer prefix can work. If even the first character cannot be matched, the answer is `IMPOSSIBLE`.

The reference string has at most `2 * 10^5` characters, there can be up to `10^5` queries, and the total length of all modified strings is also at most `2 * 10^5`. The last bound is the one that makes a linear or near-linear solution possible: across all queries, we only need to process `2 * 10^5` characters. An approach that spends `O(|s|)` work for every query character can still reach about `2 * 10^5 * 2 * 10^5 = 4 * 10^10` character inspections, which is far beyond a two-second limit.

A first edge case is when the first character does not occur in `s`. For example,

```
abc
1
d
```

has output

```
IMPOSSIBLE
```

There is no non-empty prefix that is a subsequence. A careless implementation might print an empty string, but the required output explicitly uses `IMPOSSIBLE` when no non-empty spell can be formed.

A second edge case occurs when a character exists in `s`, but not after the position used for the previous character. For example,

```
abc
1
ca
```

has output

```
c
```

The `c` can be matched at the last position, but there is no `a` after it. Checking only whether every character appears somewhere in `s` would incorrectly accept `ca`.

A third edge case is when the entire input string is a valid subsequence. For example,

```
abc
1
abc
```

has output

```
abc
```

The algorithm must not require the query to contain an extra modified suffix. A query can already be exactly the original spell.

A fourth edge case is repeated characters. For example,

```
aaa
2
aaaa
ba
```

has output

```
aaa
IMPOSSIBLE
```

The first query can use all three occurrences of `a`, but the fourth one cannot be placed. The second query fails immediately because `b` never occurs. Treating character presence as a boolean is not enough when order and multiplicity matter.

## Approaches

The direct solution is to process every query independently and simulate the definition of a subsequence. Keep a pointer into `s`. For each character of the query, scan forward in `s` until that character is found. If it is found, move the pointer past it and continue. If the end of `s` is reached first, stop and return the prefix matched so far.

This brute-force method is correct because a subsequence is defined precisely by choosing increasing positions in `s`. For each query character, choosing its first available occurrence is optimal: choosing a later occurrence can only leave fewer positions available for the remaining characters. The problem is its running time. A single character may require scanning almost all of `s`, and this can happen independently for many queries. With `|s| = 2 * 10^5` and total query length `2 * 10^5`, the worst case is on the order of `4 * 10^10` character comparisons.

The useful observation is that the expensive part of the brute force is repeatedly searching through the same fixed string `s`. The string never changes between queries, so all information about where characters occur can be prepared once.

For every lowercase character, store the sorted list of positions where it occurs in `s`. Suppose the previous matched position is `p` and the next query character is `c`. We need the first occurrence of `c` whose position is greater than `p`. Since the occurrence list is sorted, this is exactly a binary search for the first position greater than `p`.

That changes each character lookup from a scan of `s` to a binary search among occurrences of one character. Since there are only `2 * 10^5` query characters in total, the whole computation becomes `O(|s| + L log |s|)`, where `L` is the total length of all queries. With these limits, that is easily fast enough.

The same idea can also be implemented with a full next-occurrence table, giving `O(|s| + L)` time, but in Python such a table can consume substantially more memory because it stores information for 26 characters at every position. Occurrence lists are simpler and comfortably fit the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O( | s | * L)` in the worst case | `O(1)` besides input | Too slow |
| Occurrence lists + binary search | `O( | s | + L log | s | )` | `O( | s | )` | Accepted |

## Algorithm Walkthrough

1. Read `s` and build 26 occurrence lists. For every position `i` in `s`, append `i` to the list belonging to `s[i]`. Because positions are processed from left to right, every list is automatically sorted.
2. Process each modified spell `a` independently. Set `pos = -1`, meaning that no character of `a` has been matched yet. Also create an empty list for the answer.
3. For every character `c` in `a`, take the occurrence list belonging to `c` and binary-search for the first position strictly greater than `pos`. This is the earliest possible location where `c` can be placed while preserving the subsequence order.
4. If such a position does not exist, stop processing this query. Every longer prefix contains the same unmatched character, so it cannot possibly be a subsequence either.
5. If the position exists, append `c` to the answer and update `pos` to that occurrence. Choosing the earliest possible occurrence leaves the largest possible suffix of `s` available for later characters.
6. After processing the query, print the matched prefix if it is non-empty. If the first character already failed, the answer list is empty, so print `IMPOSSIBLE`.

### Why it works

The invariant is that after processing the first `k` characters of a query, `pos` is the earliest possible position in `s` at which that prefix can end. This is true initially because no characters have been matched. When processing the next character, binary search chooses its earliest occurrence after `pos`, so the new position is again the earliest possible ending position.

If that occurrence does not exist, there is no way to place the next character after any valid placement of the previous prefix. Since we already kept the previous characters as early as possible, choosing any other placement could only move farther right and cannot help. Thus the current prefix is the longest valid one, and no longer prefix can be a spell.

## Python Solution

```python
import sys
input = sys.stdin.readline

from bisect import bisect_right

def solve():
    s = input().strip()
    n = int(input())

    positions = [[] for _ in range(26)]

    for i, ch in enumerate(s):
        positions[ord(ch) - ord('a')].append(i)

    output = []

    for _ in range(n):
        a = input().strip()

        pos = -1
        answer = []

        for ch in a:
            occ = positions[ord(ch) - ord('a')]

            # First occurrence strictly after pos.
            idx = bisect_right(occ, pos)

            if idx == len(occ):
                break

            pos = occ[idx]
            answer.append(ch)

        if answer:
            output.append(''.join(answer))
        else:
            output.append("IMPOSSIBLE")

    sys.stdout.write('\n'.join(output))

if __name__ == "__main__":
    solve()
```

The `positions` array contains one sorted list for each lowercase letter. For example, if `s = "abracadabra"`, the list for `a` contains all indices at which `a` appears, in increasing order.

For each query, `pos` represents the position in `s` used by the last successfully matched character. It starts at `-1`, so the first character is allowed to use position `0`.

The subtle operation is `bisect_right(occ, pos)`. We need a position strictly greater than `pos`, not greater than or equal to it, because two subsequence characters must use different positions. If `pos` is `4` and the next character occurs at positions `4, 7, 9`, the correct choice is `7`, so `bisect_right` gives exactly the required index.

When binary search returns `len(occ)`, there is no valid occurrence after the previous match. We immediately stop because the answer must be a prefix. Continuing to inspect later characters could not produce a valid longer prefix.

There is no integer overflow issue in Python, and the position values never exceed `len(s) - 1`. The output is accumulated in a list and written once at the end, avoiding repeated flushing or expensive output operations.

## Worked Examples

For the provided sample, the reference string is `abracadabra`.

The query `abra` can be matched completely. The query `cadabra` can also be matched completely, while `dcba` can only match its first character because after the chosen `d` there is no `c`.

| Query character | Occurrences considered | Previous position | Chosen position | Matched prefix |
| --- | --- | --- | --- | --- |
| `a` | `a` positions | `-1` | `0` | `a` |
| `b` | `b` positions | `0` | `1` | `ab` |
| `r` | `r` positions | `1` | `2` | `abr` |
| `a` | `a` positions | `2` | `3` | `abra` |

For `dcba`, the first `d` is found near the end of `s`. Once that position has been chosen, the next search for `c` has no valid position, so the algorithm stops and returns `d`.

| Query character | Previous position | Chosen position | Result |
| --- | --- | --- | --- |
| `d` | `-1` | `6` | `d` |
| `c` | `6` | none | stop |

The complete sample produces `abra`, `cadabra`, `abcd`, `d`, and `IMPOSSIBLE`, matching the required output.

A second example demonstrates repeated characters and a character that appears only before the previous match.

```
abcba
4
abba
cba
bbbbb
ac
```

The results are:

```
abba
cba
bb
ac
```

For `abba`, the positions chosen are `0, 1, 3, 4`, so the whole string is valid.

| Query character | Previous position | Chosen position | Matched prefix |
| --- | --- | --- | --- |
| `a` | `-1` | `0` | `a` |
| `b` | `0` | `1` | `ab` |
| `b` | `1` | `3` | `abb` |
| `a` | `3` | `4` | `abba` |

For `bbbbb`, only two `b` characters can be matched because `s` contains only two occurrences of `b`.

| Query character | Previous position | Chosen position | Matched prefix |
| --- | --- | --- | --- |
| `b` | `-1` | `1` | `b` |
| `b` | `1` | `3` | `bb` |
| `b` | `3` | none | stop |

This trace demonstrates why the algorithm must search for the next occurrence after the previous position rather than merely checking whether the character occurs somewhere in `s`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O( | s | + L log | s | )` | Building occurrence lists costs `O( | s | )`, and each of the `L` query characters performs one binary search. |
| Space | `O( | s | )` | Every position of `s` appears in exactly one occurrence list, besides the input and output storage. |

Here `L` is the total length of all modified spells, and the problem guarantees `L <= 2 * 10^5` and `|s| <= 2 * 10^5`. The preprocessing is linear, while binary searches are performed only for characters that actually appear in the input queries. This keeps the solution comfortably within the stated two-second and 512 MB limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_right

def solve():
    input = sys.stdin.readline

    s = input().strip()
    n = int(input())

    positions = [[] for _ in range(26)]

    for i, ch in enumerate(s):
        positions[ord(ch) - ord('a')].append(i)

    out = []

    for _ in range(n):
        a = input().strip()

        pos = -1
        answer = []

        for ch in a:
            occ = positions[ord(ch) - ord('a')]
            idx = bisect_right(occ, pos)

            if idx == len(occ):
                break

            pos = occ[idx]
            answer.append(ch)

        out.append(''.join(answer) if answer else "IMPOSSIBLE")

    sys.stdout.write('\n'.join(out))

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
    """abracadabra
5
abra
cadabra
abcd
dcba
magic
"""
) == """abra
cadabra
abcd
d
IMPOSSIBLE""", "sample 1"

# Minimum-size input
assert run(
    """a
1
a
"""
) == "a", "minimum-size valid spell"

# All equal characters, including one character too many
assert run(
    """aaaa
3
aaaaa
aa
b
"""
) == """aaaa
aa
IMPOSSIBLE""", "repeated characters"

# Boundary and ordering cases
assert run(
    """abc
5
abc
abca
c
ac
bc
"""
) == """abc
abc
c
ac
bc""", "boundary positions and subsequence order"

# Maximum n and maximum total query length.
# The reference string and all queries use the same character.
s = "a" * 100000
queries = "\n".join(["a"] * 100000)
large_input = s + "\n100000\n" + queries + "\n"
large_output = ("a\n" * 99999) + "a"

assert run(large_input) == large_output, "large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / 1 / a` | `a` | Smallest possible reference string and query. |
| `aaaa / aaaaa, aa, b` | `aaaa`, `aa`, `IMPOSSIBLE` | Repeated characters, exhausting occurrences, and a missing first character. |
| `abc / abc, abca, c, ac, bc` | `abc`, `abc`, `c`, `ac`, `bc` | Exact match, invalid suffix, first/last positions, and ordered subsequences. |
| `100000` copies of `a` in both `s` and the queries | `100000` lines containing `a` | Maximum number of queries and large total input size. |

## Edge Cases

When the first character is absent, the algorithm looks at its occurrence list and immediately finds it empty. For

```
abc
1
d
```

the list for `d` has length zero, so `bisect_right` returns zero and the algorithm prints `IMPOSSIBLE`. No empty string is ever emitted.

When the required character exists only before the previous match, the binary search correctly ignores those occurrences. For

```
abc
1
ca
```

`c` is matched at position `2`. The occurrence list for `a` contains only position `0`, and searching for a position greater than `2` fails. The stored answer is therefore `c`.

When a query is longer than the number of available repeated characters, the binary search naturally runs out of occurrences. For

```
aaa
1
aaaa
```

the first three searches select positions `0`, `1`, and `2`. The fourth search finds no position greater than `2`, so the answer is `aaa`.

When a query is already a valid subsequence, no special handling is needed. For

```
abc
1
abc
```

the searches select positions `0`, `1`, and `2`, and the entire query is returned.

The boundary condition in the binary search is strict. Suppose `s = "ab"` and the query is `bb`. The first `b` uses position `1`. The second search must look for a position greater than `1`, not greater than or equal to `1`. Since no such position exists, the result is just `b`. Reusing position `1` would be an invalid subsequence and is the most common off-by-one mistake in this solution.

Finally, if a query contains arbitrary characters after the first impossible one, those characters must never be considered. For example,

```
abc
1
adzzzz
```

has answer `a`. Once `d` fails, every longer prefix also contains the invalid `d`, so processing `z`, `z`, `z`, `z` cannot change the answer. This is exactly why stopping at the first failed character gives the longest valid prefix.
