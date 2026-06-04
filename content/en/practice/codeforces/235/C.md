---
title: "CF 235C - Cyclical Quest"
description: "We are given one large text string s, which is fixed for the entire input. Then we receive many query strings x. For a query x, we are not interested only in x itself. Any cyclic rotation of x is considered equivalent."
date: "2026-06-04T16:31:32+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 235
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 146 (Div. 1)"
rating: 2700
weight: 235
solve_time_s: 156
verified: true
draft: false
---

[CF 235C - Cyclical Quest](https://codeforces.com/problemset/problem/235/C)

**Rating:** 2700  
**Tags:** data structures, string suffix structures, strings  
**Solve time:** 2m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one large text string `s`, which is fixed for the entire input. Then we receive many query strings `x`.

For a query `x`, we are not interested only in `x` itself. Any cyclic rotation of `x` is considered equivalent. For example, for `x = "abcd"`, the strings `"abcd"`, `"bcda"`, `"cdab"`, and `"dabc"` all belong to the same cyclic class.

For each query we must count how many substrings of `s` are equal to any rotation of `x`.

The length of `s` can reach `10^6`, and the total length of all queries is also at most `10^6`. A solution that scans the whole text separately for every query is immediately impossible. Even an `O(|s|)` procedure per query would require around `10^12` operations in the worst case.

The constraints strongly suggest a heavy preprocessing step on `s`, followed by nearly linear processing in the total query length.

There are a few subtle situations that a naive solution can mishandle.

Consider:

```
s = "aaaaa"
x = "aa"
```

The rotations of `"aa"` are still `"aa"`. If we generate all rotations and sum their occurrence counts, we would count the same string twice. The correct answer is `4`, not `8`.

Another example:

```
s = "ababab"
x = "abab"
```

The rotations are:

```
abab
baba
abab
baba
```

Only two distinct strings exist. Counting all four rotations separately produces duplicates.

A different pitfall appears when a rotation does not occur in `s` at all. For example:

```
s = "abc"
x = "de"
```

Every rotation should contribute zero, and the algorithm must detect this efficiently without searching the whole text.

The main difficulty is simultaneously handling all occurrences in `s`, all cyclic rotations of the query, and duplicate rotations.

## Approaches

The brute force idea is straightforward.

For a query of length `m`, generate all `m` rotations. For each rotation, count how many times it appears in `s`. A suffix array, suffix automaton, or hashing structure could answer one occurrence query quickly.

The problem is that a query of length `m` has `m` rotations. Since the total query length can reach `10^6`, the total number of generated rotations can reach roughly `10^12`. Even if each rotation were processed in constant time, this is far beyond the limit.

The key observation is that all rotations of a string appear as length-`m` substrings inside `x + x`.

For example:

```
x      = abcd
x + x  = abcdabcd
```

The rotations are exactly the length-4 substrings whose starting position lies in the first half.

This transforms the problem into:

> Among all distinct length-`m` substrings of `x + x` corresponding to rotations, sum their numbers of occurrences inside `s`.

Now a suffix automaton becomes very natural.

After building a suffix automaton on `s`, every state represents an end-position equivalence class. If we propagate occurrence counts through suffix links, each state stores the number of occurrences of every string represented by that state.

While scanning `x + x`, we can maintain the longest suffix currently matched in the automaton. Whenever the matched length is at least `m`, we know that a rotation of length `m` ends here.

The remaining challenge is identifying the state corresponding to that exact length-`m` string.

In a suffix automaton, a state `v` represents all lengths in the interval:

```
(len(link(v)) + 1) ... len(v)
```

So for a string of length exactly `m`, we climb suffix links until the parent length becomes smaller than `m`. The resulting state uniquely represents that length-`m` substring.

Different occurrences of the same rotation may appear many times while scanning `x + x`. We only want each distinct rotation once, so we timestamp states and count each state at most once per query.

This yields a solution linear in the total query length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total query length²) or worse | O(1) | Too slow |
| Optimal SAM Solution | O( | s | + total query length) |

## Algorithm Walkthrough

1. Build a suffix automaton for the text string `s`.
2. For every newly created non-clone state, initialize its occurrence count to `1`.
3. Sort states by length and propagate counts from longer states to their suffix-link parents. After this step, every state stores the number of occurrences of its represented substrings inside `s`.
4. For a query `x` of length `m`, construct `t = x + x`.
5. Scan only the first `2m - 1` characters of `t`. These positions generate exactly the `m` cyclic rotations.
6. Maintain:

- `p`, the current automaton state.
- `cur_len`, the length of the longest matched suffix.
7. For each character, perform the standard suffix automaton matching transition. If the transition does not exist, follow suffix links until it does or return to the root.
8. Whenever `cur_len >= m`, climb suffix links while `len(link(p)) >= m`.

After this adjustment, state `p` is the unique state whose interval contains length `m`. That state represents the current rotation.
9. If this state has not been counted during the current query, add its occurrence count to the answer and mark it with the current query timestamp.
10. Output the accumulated answer.

### Why it works

Every cyclic rotation of `x` appears exactly once as a length-`m` substring ending at some position inside the first `2m - 1` characters of `x + x`.

During the scan, the suffix automaton maintains the longest suffix of the processed prefix that occurs in `s`. When that matched suffix has length at least `m`, the length-`m` suffix ending at the current position is a rotation of `x`.

A suffix automaton state represents all substring lengths in a contiguous interval. Climbing suffix links until the parent length becomes smaller than `m` selects the unique state whose interval contains length `m`. That state corresponds exactly to the current rotation.

The occurrence count stored in that state equals the number of times the represented string appears in `s`. Duplicate rotations map to the same state, and timestamping prevents counting them multiple times. Hence every distinct rotation contributes exactly once, and the answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

max_states = 2 * len(s) + 5

link = [-1] * max_states
length = [0] * max_states
occ = [0] * max_states
nxt = [[0] * 26 for _ in range(max_states)]

size = 1
last = 0
link[0] = -1

for ch in s:
    c = ord(ch) - 97

    cur = size
    size += 1

    length[cur] = length[last] + 1
    occ[cur] = 1

    p = last
    while p != -1 and nxt[p][c] == 0:
        nxt[p][c] = cur
        p = link[p]

    if p == -1:
        link[cur] = 0
    else:
        q = nxt[p][c]
        if length[p] + 1 == length[q]:
            link[cur] = q
        else:
            clone = size
            size += 1

            length[clone] = length[p] + 1
            link[clone] = link[q]
            nxt[clone] = nxt[q][:]

            while p != -1 and nxt[p][c] == q:
                nxt[p][c] = clone
                p = link[p]

            link[q] = clone
            link[cur] = clone

    last = cur

max_len = len(s)

cnt = [0] * (max_len + 1)
for v in range(size):
    cnt[length[v]] += 1

for i in range(1, max_len + 1):
    cnt[i] += cnt[i - 1]

order = [0] * size
for v in range(size - 1, -1, -1):
    cnt[length[v]] -= 1
    order[cnt[length[v]]] = v

for i in range(size - 1, 0, -1):
    v = order[i]
    parent = link[v]
    if parent >= 0:
        occ[parent] += occ[v]

vis = [0] * size
timer = 0

q = int(input())

out = []

for _ in range(q):
    x = input().strip()
    m = len(x)

    t = x + x

    timer += 1
    ans = 0

    p = 0
    cur_len = 0

    for i in range(2 * m - 1):
        c = ord(t[i]) - 97

        while p != -1 and nxt[p][c] == 0:
            p = link[p]

        if p == -1:
            p = 0
            cur_len = 0
            continue

        cur_len = min(cur_len, length[p]) + 1
        p = nxt[p][c]

        while link[p] != -1 and length[link[p]] >= m:
            p = link[p]

        if cur_len >= m and vis[p] != timer:
            vis[p] = timer
            ans += occ[p]

    out.append(str(ans))

sys.stdout.write("\n".join(out))
```

The first section builds a suffix automaton for the text string. Every non-clone state starts with occurrence count `1`, corresponding to one suffix ending position.

The counting-sort pass orders states by increasing length. Processing this order backwards propagates occurrence counts through suffix links, producing the standard SAM occurrence statistics.

For each query, we scan `x + x` while maintaining the longest suffix that currently appears in the automaton. The update

```
cur_len = min(cur_len, length[p]) + 1
```

is the standard SAM matching formula. It correctly adjusts the current matched length after suffix-link jumps.

The loop

```
while link[p] != -1 and length[link[p]] >= m:
    p = link[p]
```

is the crucial step. After it finishes, state `p` is the unique state whose represented interval contains length `m`.

The timestamp array avoids clearing a boolean array of size up to two million for every query. Each query receives a unique identifier, and a state is counted only once for that identifier.

## Worked Examples

### Example 1

Input:

```
s = baabaabaaa
x = baa
```

Then:

```
x + x = baabaa
```

We scan the first `2m - 1 = 5` characters.

| Position | Character | Matched length ≥ 3? | Rotation represented |
| --- | --- | --- | --- |
| 0 | b | No | - |
| 1 | a | No | - |
| 2 | a | Yes | baa |
| 3 | b | Yes | aab |
| 4 | a | Yes | aba |

The distinct rotations are:

```
baa
aab
aba
```

Their occurrence counts in `s` are:

```
3 + 2 + 2 = 7
```

Answer:

```
7
```

This example shows how every rotation appears as a length-`m` window in `x + x`.

### Example 2

Input:

```
s = aaaaa
x = aa
```

Then:

```
x + x = aaaa
```

We scan the first three characters.

| Position | Rotation | Already counted? |
| --- | --- | --- |
| 1 | aa | No |
| 2 | aa | Yes |

Although two rotation positions exist, both represent the same string. The timestamp mechanism counts it only once.

The occurrence count of `"aa"` in `"aaaaa"` is `4`, so the answer is:

```
4
```

This example demonstrates why duplicate rotations must be removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O( | s |

The text length and the total query length are both at most `10^6`. A suffix automaton contains at most about `2 · 10^6` states, which fits comfortably inside the memory limit. The linear running time is well within the available 3 seconds for a highly optimized implementation.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    # paste solution into solve()
    pass

# provided sample
assert run(
"""baabaabaaa
5
a
ba
baa
aabaa
aaba
"""
) == """7
5
7
3
5"""

# single character
assert run(
"""a
1
a
"""
) == """1"""

# duplicate rotations
assert run(
"""aaaaa
1
aa
"""
) == """4"""

# no rotation appears
assert run(
"""abc
1
de
"""
) == """0"""

# periodic query, many identical rotations
assert run(
"""ababab
1
abab
"""
) == """3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `s="a", x="a"` | `1` | Minimum size |
| `s="aaaaa", x="aa"` | `4` | Duplicate rotations |
| `s="abc", x="de"` | `0` | Missing strings |
| `s="ababab", x="abab"` | `3` | Periodic rotations and deduplication |

## Edge Cases

Consider:

```
aaaaa
1
aa
```

The rotations are:

```
aa
aa
```

Both rotations correspond to the same string. While scanning `x + x`, the same suffix automaton state is reached multiple times. The timestamp array allows only the first visit to contribute. The algorithm outputs `4`, which is the number of occurrences of `"aa"` in `"aaaaa"`.

Consider:

```
abc
1
de
```

During matching, no transition for `'d'` exists from the root. The automaton immediately resets the current match length to zero. No state ever satisfies `cur_len >= m`, so nothing is added to the answer. The result is correctly `0`.

Consider:

```
ababab
1
abab
```

The four rotation positions generate only two distinct strings:

```
abab
baba
```

Both map to fixed suffix automaton states. Repeated visits are ignored by timestamping, so each distinct rotation contributes exactly once. The answer is the sum of the occurrence counts of those two strings.
