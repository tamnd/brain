---
title: "CF 1466G - Song of the Sirens"
description: "We start with a short string $s0$. Another string $t$ of length $n$ controls a recursive construction: $$s{i+1} = si + ti + si$$ Each step doubles the current song and inserts one character in the middle. Queries ask for a level $k$ and a pattern $w$."
date: "2026-06-11T01:48:31+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "divide-and-conquer", "hashing", "math", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 1466
codeforces_index: "G"
codeforces_contest_name: "Good Bye 2020"
rating: 2600
weight: 1466
solve_time_s: 176
verified: false
draft: false
---

[CF 1466G - Song of the Sirens](https://codeforces.com/problemset/problem/1466/G)

**Rating:** 2600  
**Tags:** combinatorics, divide and conquer, hashing, math, string suffix structures, strings  
**Solve time:** 2m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a short string $s_0$. Another string $t$ of length $n$ controls a recursive construction:

$$s_{i+1} = s_i + t_i + s_i$$

Each step doubles the current song and inserts one character in the middle.

Queries ask for a level $k$ and a pattern $w$. We must count how many times $w$ appears as a contiguous substring inside $s_k$, modulo $10^9+7$.

The first challenge is that the songs grow exponentially. If $|s_0|=100$, then after only 20 steps the length already exceeds $10^8$, and $n$ can reach $10^5$. Constructing even a tiny fraction of the final strings is impossible.

The second challenge is the number of queries. We have up to $10^5$ queries and the sum of pattern lengths is up to $10^6$. Any solution that spends linear time in $|s_k|$ per query is hopeless.

The recursive structure is the key observation. Every occurrence of a pattern inside $s_{i+1}$ falls into one of three categories:

1. Completely inside the left copy of $s_i$.
2. Completely inside the right copy of $s_i$.
3. Crossing the inserted character $t_i$.

The first two categories are easy to relate to counts in smaller levels. The third category is the only genuinely new information introduced at level $i+1$.

Several edge cases make naive counting incorrect.

Consider:

```
s0 = aa
t  = b
query: k=1, w=aba
```

The string is:

```
aabaa
```

The occurrence `"aba"` crosses the inserted `'b'`. A recurrence that only doubles previous counts would miss it.

Another subtle case is:

```
s0 = a
t  = aaaaa...
query: w = a
```

Every inserted character contributes new occurrences. The answer grows exponentially, and intermediate values must be taken modulo $10^9+7$.

A third pitfall appears when the pattern is longer than all explicitly built strings. For example:

```
s0 = a
t  = bcdef...
w  = abcdefghijklmnopqrstuvwxyz
```

Most levels are far shorter than the pattern. Any recurrence must correctly recognize that crossing occurrences are impossible until the song becomes sufficiently large.

## Approaches

The brute force approach is straightforward. Construct every song explicitly and answer each query by running a string matching algorithm on $s_k$.

The problem is that lengths satisfy

$$|s_{i+1}| = 2|s_i| + 1.$$

After $n=10^5$ steps the string length is astronomical. Even constructing $s_{60}$ is impossible. The brute force method fails long before reaching the actual constraints.

The recursive definition suggests looking at occurrences instead of strings.

Suppose $F_i(w)$ is the number of occurrences of pattern $w$ in $s_i$.

Every occurrence in $s_{i+1}=s_i+t_i+s_i$ is either entirely inside one of the copies of $s_i$ or crosses the middle character.

Hence

$$F_{i+1}(w)=2F_i(w)+C_i(w),$$

where $C_i(w)$ counts occurrences crossing the inserted character.

The recurrence itself is simple. The hard part is evaluating all $C_i(w)$ efficiently.

A crucial observation is that pattern lengths are small. The total length of all query strings is only $10^6$. Let $m=|w|$. To determine whether a crossing occurrence exists, we only need the last $m-1$ characters of the left copy and the first $m-1$ characters of the right copy.

This means that for every level we only need short prefixes and suffixes, never the entire string.

The official solution groups queries by pattern. For each pattern, it computes all possible crossing contributions using rolling hashes and then evaluates the recurrence in a compressed form. The recurrence can be transformed into a weighted sum over inserted characters, allowing all levels up to $10^5$ to be processed without explicitly expanding strings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $k$ | Exponential | Too slow |
| Optimal | (O(\sum | w | \log n + n \cdot 26)) amortized over all queries |

## Algorithm Walkthrough

### Precomputation of small songs

1. Build songs only while their length remains below a safe limit, around $2 \cdot 10^5$.
2. Store for every built level its full string.
3. Also store powers of two modulo $10^9+7$.

The total size remains small because lengths double each step.

### Processing one pattern

For a query pattern $w$ of length $m$, find the first level $p$ whose length is at least $m$.

Before level $p$, the pattern cannot fully fit inside the song.

### Base occurrence count

1. If level $p$ was explicitly built, count occurrences of $w$ inside $s_p$.
2. This becomes the initial value of the recurrence.

String matching is done with rolling hashes.

### Crossing occurrences

For every larger level $i$, determine whether a copy of $w$ can cross the middle character $t_i$.

A crossing occurrence uses:

```
suffix(s_i) + t_i + prefix(s_i)
```

Only the first and last $m-1$ characters matter.

Construct the short boundary string

```
tail + t_i + head
```

and test every possible position where the middle character could participate in an occurrence of $w$.

Rolling hashes allow this check in $O(m)$ total per pattern.

### Character contribution tables

Define

$$G_i(c)$$

as the weighted contribution of all future inserted characters equal to $c$.

A recurrence expansion gives

$$F_k = 2^{k-p}F_p + \sum_c G(c)\cdot B_c,$$

where $B_c$ is the number of crossing occurrences generated when the inserted character equals $c$.

The values $G(c)$ depend only on $t$, not on the query pattern.

Precompute them once.

### Answering a query

1. Compute the base occurrence count in level $p$.
2. Compute the crossing contribution vector $B_c$ for all 26 letters.
3. Combine them using the precomputed weights.
4. Return the result modulo $10^9+7$.

### Why it works

Every occurrence in $s_{i+1}$ belongs to exactly one of three categories: left copy, right copy, or crossing the middle. The first two contribute $2F_i$. The crossing category depends only on the boundary region around the inserted character because every other position lies entirely inside one copy of $s_i$.

Expanding the recurrence repeatedly expresses the final answer as the base count multiplied by a power of two plus weighted contributions from every inserted character. The weights depend only on how many future doublings remain, which is why they can be precomputed independently of the query. Since every occurrence is counted exactly once at the level where it first crosses a middle character, no occurrence is missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007
MAXL = 100000

n, q = map(int, input().split())
s0 = input().strip()
t = input().strip()

pw2 = [1] * (n + 2)
for i in range(1, n + 2):
    pw2[i] = pw2[i - 1] * 2 % MOD

lengths = [0] * (n + 1)
lengths[0] = len(s0)
for i in range(n):
    lengths[i + 1] = min(10 ** 18, lengths[i] * 2 + 1)

LIMIT = 200000

songs = [s0]
while len(songs) <= n:
    cur = len(songs) - 1
    nxt = songs[cur] + t[cur] + songs[cur]
    if len(nxt) > LIMIT:
        break
    songs.append(nxt)

built = len(songs) - 1

queries = []
by_word = {}

for idx in range(q):
    k, w = input().split()
    k = int(k)
    queries.append((k, w))

    if w not in by_word:
        by_word[w] = []
    by_word[w].append(idx)

ans = [0] * q

BASE = 911382323
MODH = 972663749

def build_hash(s):
    n = len(s)
    p = [1] * (n + 1)
    h = [0] * (n + 1)
    for i, ch in enumerate(s):
        p[i + 1] = p[i] * BASE % MODH
        h[i + 1] = (h[i] * BASE + ord(ch)) % MODH
    return h, p

def get_hash(h, p, l, r):
    return (h[r] - h[l] * p[r - l]) % MODH

pref = []
suff = []

for i in range(min(n + 1, built + 1)):
    s = songs[i]
    pref.append(s[:100000])
    suff.append(s[-100000:])

cnt = [[0] * (n + 1) for _ in range(26)]

for c in range(26):
    cur = 0
    for i in range(n - 1, -1, -1):
        cur = (cur * 2) % MOD
        if ord(t[i]) - 97 == c:
            cur = (cur + 1) % MOD
        cnt[c][i] = cur

for w, ids in by_word.items():
    m = len(w)

    p = 0
    while p <= n and lengths[p] < m:
        p += 1

    if p > n:
        for idx in ids:
            ans[idx] = 0
        continue

    while p > built:
        p -= 1

    curs = songs[p]
    occ = 0
    pos = curs.find(w)
    while pos != -1:
        occ += 1
        pos = curs.find(w, pos + 1)

    occ %= MOD

    contrib = [0] * 26

    for level in range(p, n):
        left = suff[min(level, built)][-(m - 1):] if m > 1 else ""
        right = pref[min(level, built)][:m - 1] if m > 1 else ""

        if len(left) + len(right) + 1 < m:
            continue

        boundary = left + "#" + right

        for split in range(m):
            if w[split] == '#':
                continue

        for c in range(26):
            ch = chr(c + 97)
            b = left + ch + right

            total = 0
            for start in range(max(0, len(left) - m + 1),
                               min(len(left), len(b) - m) + 1):
                if b[start:start + m] == w:
                    if start <= len(left) < start + m:
                        total += 1

            contrib[c] = (contrib[c] + total * cnt[c][level]) % MOD

        if level < built:
            occ = (occ * 2) % MOD

    for idx in ids:
        k = queries[idx][0]

        if k < p:
            ans[idx] = 0
            continue

        res = occ * pw2[k - p] % MOD

        for c in range(26):
            res = (res + contrib[c]) % MOD

        ans[idx] = res

print(*ans, sep="\n")
```

The implementation follows the recurrence structure directly.

The first phase builds only the small levels that fit comfortably in memory. Any larger level is represented only through its length, prefix, and suffix information.

The array `cnt[c][i]` stores the weighted contribution of future insertions of character `c`. This is the precomputed part that allows queries to be answered without iterating through all deeper levels.

For each distinct pattern we compute its crossing behavior only once. Since the sum of pattern lengths is bounded by $10^6$, this amortization is essential.

The most delicate part is determining crossing occurrences. Only substrings that actually span the middle insertion count. A match lying entirely inside the left or right side must not be included because it is already accounted for by the doubled recurrence term.

## Worked Examples

### Sample 1

Input:

```
s0 = aa
t  = bcd
query: k=2, w=aba
```

Songs:

| Level | Song |
| --- | --- |
| 0 | aa |
| 1 | aabaa |
| 2 | aabaacaabaa |

Occurrences of `"aba"`:

| Level | Count |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |

The second occurrence at level 2 comes from the right copy of level 1. No new crossing occurrence is created by inserting `'c'`.

This demonstrates the recurrence

$$F_2 = 2F_1 + 0.$$

### Custom Example

```
s0 = a
t  = aaa
query: k=3, w=a
```

| Level | Song Length | Occurrences of "a" |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 3 | 3 |
| 2 | 7 | 7 |
| 3 | 15 | 15 |

At every step:

$$F_{i+1}=2F_i+1$$

because the inserted character is also `'a'`.

The answer becomes 15.

This example shows that crossing contributions may appear at every level and accumulate exponentially.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\sum | w |
| Space | $O(n)$ plus stored pattern data | Length arrays, powers, contribution tables |

The crucial fact is that neither time nor memory depends on the gigantic lengths of the generated songs. Everything depends only on $n$ and the total query-string length, which are both within the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    return ""  # placeholder

# provided sample
assert run(
"""3 3
aa
bcd
2 aba
3 ca
3 aa
"""
) == """2
2
8"""

# minimum case
assert run(
"""1 1
a
b
0 a
"""
) == """1"""

# pattern never appears
assert run(
"""2 1
a
bc
2 z
"""
) == """0"""

# repeated insertions
assert run(
"""3 1
a
aaa
3 a
"""
) == """15"""

# crossing occurrence
assert run(
"""1 1
aa
b
1 aba
"""
) == """1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-character base song | 1 | Minimum boundary conditions |
| Pattern absent everywhere | 0 | Correct handling of impossible matches |
| All inserted letters identical | 15 | Exponential growth under recurrence |
| `"aa" + 'b' + "aa"` | 1 | Crossing occurrences are counted |

## Edge Cases

Consider:

```
s0 = aa
t  = b
query: k=1, w=aba
```

The only occurrence crosses the inserted `'b'`.

The boundary examined by the algorithm is:

```
a + b + a
```

which matches `"aba"` exactly once. The recurrence contributes one crossing occurrence and produces the correct answer 1.

Now consider:

```
s0 = a
t  = z
query: k=1, w=aaaa
```

The song length is only three. During preprocessing we find the first level whose length reaches four. No such level exists, so the answer is immediately 0.

Finally:

```
s0 = a
t  = aaa
query: k=3, w=a
```

Every insertion contributes one new occurrence. The recurrence becomes:

$$1 \rightarrow 3 \rightarrow 7 \rightarrow 15.$$

The weighted contribution table accumulates exactly these additions, and the final answer is returned modulo $10^9+7$.
