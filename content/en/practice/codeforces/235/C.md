---
title: "CF 235C - Cyclical Quest"
description: "We are given one large text string s, then many query strings x. For each query, we must count how many substrings of s are cyclic rotations of x. A cyclic rotation moves some prefix of a string to the end."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 235
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 146 (Div. 1)"
rating: 2700
weight: 235
solve_time_s: 117
verified: true
draft: false
---

[CF 235C - Cyclical Quest](https://codeforces.com/problemset/problem/235/C)

**Rating:** 2700  
**Tags:** data structures, string suffix structures, strings  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one large text string `s`, then many query strings `x`. For each query, we must count how many substrings of `s` are cyclic rotations of `x`.

A cyclic rotation moves some prefix of a string to the end. For example, the rotations of `"abcd"` are `"abcd"`, `"bcda"`, `"cdab"`, and `"dabc"`.

So if the query is `"abc"`, every occurrence of `"abc"`, `"bca"`, or `"cab"` inside `s` contributes to the answer.

The input size completely rules out naive substring checking. The main string can have length up to `10^6`, and the total length of all queries is also up to `10^6`. Any algorithm that scans the whole text for every query separately would perform around `10^12` character operations in the worst case, which is far beyond the time limit.

The structure of the problem strongly suggests preprocessing the big string once, then answering all queries using that structure. Since we need substring occurrence information for many different patterns, suffix automaton is a natural fit. The difficult part is handling all cyclic rotations efficiently without counting duplicates incorrectly.

Several edge cases are easy to mishandle.

Consider the query:

```
aaaa
```

All rotations are identical. A careless solution that checks all rotations independently would count every occurrence four times instead of once.

For example:

```
s = aaaaa
x = aaaa
```

The correct answer is `2`, because `"aaaa"` appears at positions `0` and `1`.

Another tricky case is when different rotations reach the same automaton state.

Example:

```
s = ababab
x = abab
```

The rotations are `"abab"` and `"baba"`. If we simply sum occurrence counts for all rotations, repeated states may cause duplicate counting. We must deduplicate states per query.

Queries of length `1` also need attention.

Example:

```
s = abcabc
x = b
```

The only rotation is `"b"` itself, so the answer is simply the number of `'b'` characters in `s`.

Finally, queries longer than `s` must immediately return `0`.

Example:

```
s = abc
x = abcde
```

No substring of `s` can have length `5`.

## Approaches

The brute force idea is straightforward. For every query `x`, generate all rotations of `x`, then search each rotation inside `s`.

A standard substring search like KMP would find one pattern in linear time, so a query of length `m` would cost `O(m * |s|)` in the worst case because there are `m` rotations. With both total query length and `|s|` reaching `10^6`, this becomes completely infeasible.

We need to exploit two observations.

First, every rotation of `x` appears as a substring of `x + x`. For example:

```
x = abcd
x + x = abcdabcd
```

Every length-4 substring of this doubled string is a rotation.

Second, suffix automaton can tell us how many times any substring occurs in `s`. After building the automaton once for `s`, every substring query becomes a traversal problem.

The remaining challenge is counting all distinct rotations efficiently.

Suppose we traverse `x + x` through the suffix automaton using a sliding window of length `m = |x|`. Every valid window corresponds to one rotation. The automaton state reached after reading that window represents that substring in `s`, and the state's occurrence count tells us how many times it appears.

Different rotations may map to the same state. Since all substrings represented by one state have the same occurrence count, we should count each relevant state only once.

This leads to the optimal solution:

We build a suffix automaton for `s`, compute occurrence counts for every state, then for each query:

1. Traverse `x + x`.
2. Maintain the longest suffix currently matched.
3. Whenever the matched length reaches at least `m`, identify the automaton state representing the current rotation.
4. Add that state's occurrence count once.

The total work over all queries stays linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | s | × total query length²) |
| Optimal | O( | s | + total query length) |

## Algorithm Walkthrough

### 1. Build a suffix automaton for `s`

Each state stores:

- `next[26]`, transitions
- `link`, suffix link
- `len`, maximum length represented
- `occ`, number of end positions

While inserting characters from `s`, every newly created state gets `occ = 1`.

### 2. Propagate occurrence counts

The raw counts only mark string endings. To obtain the number of occurrences of every substring, process states in decreasing order of `len`.

For every state `v`:

```
occ[link[v]] += occ[v]
```

This standard suffix automaton DP accumulates occurrence frequencies upward through suffix links.

### 3. Process each query independently

Let the query length be `m`.

If `m > |s|`, answer `0` immediately.

Otherwise, form:

```
t = x + x
```

Every rotation appears as a length-`m` substring inside `t`.

### 4. Traverse `t` through the automaton

Maintain:

- `v`, current automaton state
- `l`, current matched length

For every character:

- Follow transitions if possible.
- Otherwise move through suffix links until a transition exists.
- Update the matched length accordingly.

This is the standard online matching procedure on a suffix automaton.

### 5. Keep only windows of size `m`

After extending with a new character, the matched substring may become longer than `m`.

We need the state corresponding exactly to the last `m` characters.

While:

```
len[link[v]] >= m
```

move:

```
v = link[v]
```

After this adjustment, state `v` represents the current rotation.

### 6. Count every state once

Different rotations may produce the same state.

Use a hash set or timestamp array to avoid duplicates.

Whenever a valid rotation is found:

- If state `v` was not counted before for this query:

- add `occ[v]`
- mark it visited

### 7. Output the accumulated answer

The sum of occurrence counts of all distinct rotation states is the final answer.

### Why it works

Every cyclic rotation of `x` appears exactly once as a length-`m` substring of `x + x` starting within the first `m` positions.

During traversal, the automaton maintains the longest suffix of the processed prefix that appears in `s`. After shrinking through suffix links until the parent length becomes smaller than `m`, the current state represents exactly the current length-`m` window.

All substrings represented by one suffix automaton state have identical occurrence counts in `s`. If multiple rotations map to the same state, they are actually the same substring in `s`, so they must only contribute once. Deduplicating states guarantees correct counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 2_000_005

nexts = [[-1] * 26]
link = [-1]
length = [0]
occ = [0]

last = 0

def extend(ch):
    global last

    c = ord(ch) - 97

    cur = len(nexts)

    nexts.append(nexts[last][:])
    nexts[cur] = [-1] * 26

    length.append(length[last] + 1)
    link.append(0)
    occ.append(1)

    p = last

    while p != -1 and nexts[p][c] == -1:
        nexts[p][c] = cur
        p = link[p]

    if p == -1:
        link[cur] = 0
    else:
        q = nexts[p][c]

        if length[p] + 1 == length[q]:
            link[cur] = q
        else:
            clone = len(nexts)

            nexts.append(nexts[q][:])
            length.append(length[p] + 1)
            link.append(link[q])
            occ.append(0)

            while p != -1 and nexts[p][c] == q:
                nexts[p][c] = clone
                p = link[p]

            link[q] = clone
            link[cur] = clone

    last = cur

s = input().strip()

for ch in s:
    extend(ch)

size = len(nexts)

cnt = [0] * (len(s) + 1)

for v in range(size):
    cnt[length[v]] += 1

for i in range(1, len(cnt)):
    cnt[i] += cnt[i - 1]

order = [0] * size

for v in range(size - 1, -1, -1):
    l = length[v]
    cnt[l] -= 1
    order[cnt[l]] = v

for v in range(size - 1, 0, -1):
    state = order[v]
    parent = link[state]

    if parent >= 0:
        occ[parent] += occ[state]

n = int(input())

vis = [0] * size
timer = 0

answers = []

for _ in range(n):
    x = input().strip()

    m = len(x)

    if m > len(s):
        answers.append("0")
        continue

    timer += 1

    t = x + x

    v = 0
    l = 0

    ans = 0

    for i, ch in enumerate(t[:-1]):
        c = ord(ch) - 97

        while v != 0 and nexts[v][c] == -1:
            v = link[v]
            l = length[v]

        if nexts[v][c] != -1:
            v = nexts[v][c]
            l += 1
        else:
            v = 0
            l = 0

        while v != 0 and length[link[v]] >= m:
            v = link[v]

        if l >= m:
            if vis[v] != timer:
                vis[v] = timer
                ans += occ[v]

    answers.append(str(ans))

print("\n".join(answers))
```

The suffix automaton construction follows the standard online algorithm. Each insertion either extends directly or creates a clone state when the transition structure would otherwise violate automaton properties.

The occurrence propagation step is essential. During construction, `occ[v]` counts how many suffixes end at state `v`. After processing states in decreasing length order, it becomes the number of occurrences of every substring represented by that state.

The query processing uses the classic automaton matching technique. The variables `v` and `l` always describe the longest suffix of the processed prefix that exists in `s`.

The line:

```
while v != 0 and length[link[v]] >= m:
    v = link[v]
```

is the subtle part. The current state may represent substrings longer than `m`. Climbing suffix links shrinks the represented interval until `m` becomes the smallest valid length inside the state.

Another easy mistake is iterating over all of `x + x`. We use:

```
t[:-1]
```

because the doubled string contains exactly `m` distinct rotation windows starting in the first `m` positions. Processing the last character would duplicate the first rotation.

The timestamp array avoids clearing a boolean array for every query. This matters because the automaton may contain about `2 * 10^6` states.

## Worked Examples

### Example 1

Input:

```
s = baabaabaaa
x = baa
```

Rotations are:

```
baa
aab
aba
```

Traversal over `"baabaa"`:

| Position | Character | Current Window | SAM State Counted | occ |
| --- | --- | --- | --- | --- |
| 0 | b | b | No | - |
| 1 | a | ba | No | - |
| 2 | a | baa | Yes | 3 |
| 3 | b | aab | Yes | 2 |
| 4 | a | aba | Yes | 2 |
| 5 | a | baa | Already counted | - |

Final answer:

```
3 + 2 + 2 = 7
```

This trace shows why deduplication matters. The last `"baa"` rotation appears again in the doubled string, but it must not be counted twice.

### Example 2

Input:

```
s = aaaaa
x = aaaa
```

Traversal over `"aaaaaaa"` excluding the last character:

| Position | Character | Current Window | State Counted? | occ |
| --- | --- | --- | --- | --- |
| 0 | a | a | No | - |
| 1 | a | aa | No | - |
| 2 | a | aaa | No | - |
| 3 | a | aaaa | Yes | 2 |
| 4 | a | aaaa | Already counted | - |
| 5 | a | aaaa | Already counted | - |

Final answer:

```
2
```

All rotations are identical, so every valid window reaches the same automaton state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O( | s |

The limits allow around a few million operations comfortably. The suffix automaton stays linear in size, and every query character is processed amortized `O(1)` times through suffix links.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    nexts = [[-1] * 26]
    link = [-1]
    length = [0]
    occ = [0]

    last = 0

    def extend(ch):
        nonlocal last

        c = ord(ch) - 97

        cur = len(nexts)

        nexts.append([-1] * 26)
        length.append(length[last] + 1)
        link.append(0)
        occ.append(1)

        p = last

        while p != -1 and nexts[p][c] == -1:
            nexts[p][c] = cur
            p = link[p]

        if p == -1:
            link[cur] = 0
        else:
            q = nexts[p][c]

            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = len(nexts)

                nexts.append(nexts[q][:])
                length.append(length[p] + 1)
                link.append(link[q])
                occ.append(0)

                while p != -1 and nexts[p][c] == q:
                    nexts[p][c] = clone
                    p = link[p]

                link[q] = clone
                link[cur] = clone

        last = cur

    s = input().strip()

    for ch in s:
        extend(ch)

    size = len(nexts)

    cnt = [0] * (len(s) + 1)

    for v in range(size):
        cnt[length[v]] += 1

    for i in range(1, len(cnt)):
        cnt[i] += cnt[i - 1]

    order = [0] * size

    for v in range(size - 1, -1, -1):
        l = length[v]
        cnt[l] -= 1
        order[cnt[l]] = v

    for v in range(size - 1, 0, -1):
        state = order[v]
        occ[link[state]] += occ[state]

    n = int(input())

    vis = [0] * size
    timer = 0

    out = []

    for _ in range(n):
        x = input().strip()

        m = len(x)

        if m > len(s):
            out.append("0")
            continue

        timer += 1

        t = x + x

        v = 0
        l = 0

        ans = 0

        for ch in t[:-1]:
            c = ord(ch) - 97

            while v != 0 and nexts[v][c] == -1:
                v = link[v]
                l = length[v]

            if nexts[v][c] != -1:
                v = nexts[v][c]
                l += 1
            else:
                v = 0
                l = 0

            while v != 0 and length[link[v]] >= m:
                v = link[v]

            if l >= m and vis[v] != timer:
                vis[v] = timer
                ans += occ[v]

        out.append(str(ans))

    return "\n".join(out)

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
) == \
"""7
5
7
3
5"""

# minimum size
assert run(
"""a
1
a
"""
) == \
"""1"""

# query longer than string
assert run(
"""abc
1
abcd
"""
) == \
"""0"""

# all equal characters
assert run(
"""aaaaa
2
aa
aaaa
"""
) == \
"""4
2"""

# cyclic duplicates
assert run(
"""ababab
1
abab
"""
) == \
"""3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `s="a"` | `1` | Minimum valid input |
| Query longer than text | `0` | Early rejection logic |
| All equal characters | Correct duplicate handling | Rotations collapsing into one state |
| `abab` in `ababab` | `3` | Multiple distinct rotations |

## Edge Cases

Consider:

```
s = aaaaa
x = aaaa
```

The doubled string is:

```
aaaaaaaa
```

Every length-4 window is `"aaaa"` again. During traversal, all valid windows end in the same suffix automaton state. The timestamp array prevents adding its occurrence count repeatedly. The algorithm outputs `2`, which is correct.

Now consider:

```
s = ababab
x = abab
```

The rotations are:

```
abab
baba
```

Both appear in `s`. Traversing `x + x = abababab` produces repeated windows:

```
abab
baba
abab
baba
```

Without deduplication, the answer would become `6`. The visited marking guarantees each corresponding automaton state contributes once, producing the correct answer `3`.

Finally, consider a query longer than the text:

```
s = abc
x = abcde
```

No substring of `s` can match length `5`. The algorithm immediately returns `0` before any traversal, avoiding unnecessary work and preventing invalid window handling.
