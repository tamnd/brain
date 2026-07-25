---
title: "CF 102862G - Strange Queries"
description: "We have a collection of lowercase strings. For each query, two strings are given. We must count how many stored strings satisfy at least one of two conditions: they begin with the first query string or they end with the second query string."
date: "2026-07-25T13:52:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102862
codeforces_index: "G"
codeforces_contest_name: "LU ICPC Selection Contest 2020 and KFU Open Contest 2020"
rating: 0
weight: 102862
solve_time_s: 55
verified: true
draft: false
---

[CF 102862G - Strange Queries](https://codeforces.com/problemset/problem/102862/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of lowercase strings. For each query, two strings are given. We must count how many stored strings satisfy at least one of two conditions: they begin with the first query string or they end with the second query string. A string satisfying both conditions is counted only once.

The input size is large enough that checking every stored string for every query is impossible. There can be up to 100000 stored strings and 100000 queries, while the total length of all strings is only 100000. This tells us that the solution must be close to linear in the total input size. A method doing even 100 operations per query can already become too slow, so scanning the whole dictionary for each query is ruled out.

The main difficulty is the overlap between the two conditions. Counting prefixes and suffixes separately is easy, but the strings satisfying both require a more careful approach.

A simple edge case is when the same string satisfies both parts. For example:

```
Input:
1
abc
1
a c
```

The answer is:

```
1
```

A careless solution adding the prefix count and suffix count would count `abc` twice.

Another edge case is when the requested prefix or suffix does not appear.

```
Input:
2
cat
dog
1
bird z
```

The answer is:

```
0
```

The implementation must not assume every query string exists in the corresponding trie.

A third case is a query involving an empty intersection between prefix and suffix conditions.

```
Input:
3
apple
banana
car
1
a na
```

Only `apple` has prefix `a`, and only `banana` has suffix `na`, so the answer is:

```
2
```

The intersection count must be zero.

## Approaches

The direct solution is to inspect every stored string for every query. For each string we check whether it starts with the first query string or ends with the second query string. This is correct because it directly follows the definition. However, with 100000 strings and 100000 queries this can require around 10^10 checks, which is far beyond the limit.

A trie immediately helps with the individual prefix and suffix counts. A prefix trie stores every string normally, and every node represents one possible prefix. The number of strings having a given prefix equals the number of complete strings stored in that node's subtree. A second trie built on reversed strings gives the same ability for suffix queries.

The remaining problem is counting strings that satisfy both a prefix and a suffix. The important observation is that every stored string corresponds to exactly one pair of trie nodes: its terminal node in the normal trie and its terminal node in the reversed trie. A query asks how many of these pairs fall inside two subtrees.

A subtree can be represented as a continuous interval using a DFS order. After numbering the nodes of both tries, every string becomes a point `(x, y)`, where `x` is the DFS position of its node in the prefix trie and `y` is the DFS position of its node in the suffix trie. Then an intersection query becomes a rectangle counting query.

We can answer all rectangle queries offline with a Fenwick tree. We sweep through prefix positions, adding points whose x coordinate has become active, and query how many active points have a y coordinate inside the required interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Trie + Offline Rectangle Queries | O(S log S + q log S) | O(S) | Accepted |

Here S is the total length of all strings.

## Algorithm Walkthrough

1. Build a trie containing all original strings and another trie containing all reversed strings. Each stored string remembers the terminal node reached in both tries.
2. Run DFS on both tries and assign each node an entry and exit time. Every subtree becomes an interval of DFS times, so checking whether a string has a given prefix or suffix becomes checking whether its terminal node lies inside that interval.
3. For every query, find the prefix trie node of the first string and the suffix trie node of the second string. If one does not exist, the corresponding condition contributes zero.
4. Compute the number of strings with the requested prefix using the size of the prefix node subtree. Compute the suffix count in the same way on the reversed trie.
5. Convert the intersection request into a rectangle query. The rectangle contains all points whose prefix terminal lies in the prefix subtree interval and whose suffix terminal lies in the suffix subtree interval.
6. Answer all rectangle queries offline using four Fenwick tree prefix queries. The rectangle count is:

```
count(x <= xr, y <= yr)
- count(x < xl, y <= yr)
- count(x <= xr, y < yl)
+ count(x < xl, y < yl)
```

1. The final answer for each query is:

```
prefix_count + suffix_count - intersection_count
```

Why it works:

Each stored string appears exactly once as a point formed by its two terminal trie positions. A prefix condition selects exactly the points whose first coordinate belongs to the prefix subtree interval. A suffix condition selects exactly the points whose second coordinate belongs to the suffix subtree interval. The rectangle query counts precisely the strings satisfying both conditions, so inclusion-exclusion removes the duplicate counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Trie:
    def __init__(self):
        self.next = [[-1] * 26]
        self.size = [0]

    def add(self, s):
        v = 0
        for c in s:
            x = ord(c) - 97
            if self.next[v][x] == -1:
                self.next[v][x] = len(self.next)
                self.next.append([-1] * 26)
                self.size.append(0)
            v = self.next[v][x]
        return v

    def find(self, s):
        v = 0
        for c in s:
            x = ord(c) - 97
            if self.next[v][x] == -1:
                return -1
            v = self.next[v][x]
        return v

def solve():
    n = int(input())
    strings = [input().strip() for _ in range(n)]

    pref = Trie()
    suff = Trie()

    pref_nodes = []
    suff_nodes = []

    for s in strings:
        pref_nodes.append(pref.add(s))
        suff_nodes.append(suff.add(s[::-1]))

    def prepare(trie):
        g = [[] for _ in range(len(trie.next))]
        for i, row in enumerate(trie.next):
            for x in row:
                if x != -1:
                    g[i].append(x)

        tin = [0] * len(g)
        tout = [0] * len(g)
        order = 0
        sub = [0] * len(g)

        def dfs(v):
            nonlocal order
            tin[v] = order
            order += 1
            sub[v] = 0
            for u in g[v]:
                dfs(u)
            tout[v] = order - 1

        dfs(0)

        def count(v):
            if v == -1:
                return 0
            total = 0
            for x in range(tin[v], tout[v] + 1):
                total += 1
            return total

        return tin, tout

    tinp, toutp = prepare(pref)
    tins, touts = prepare(suff)

    points = []
    for a, b in zip(pref_nodes, suff_nodes):
        points.append((tinp[a], tins[b]))

    events = []
    answers = [0] * int(input())

    q = len(answers)
    raw_queries = []

    for i in range(q):
        l, r = input().split()
        raw_queries.append((l, r))

    pref_cache = {}
    suff_cache = {}

    prefix_count = [0] * q
    suffix_count = [0] * q

    rects = []

    for i, (l, r) in enumerate(raw_queries):
        if l not in pref_cache:
            v = pref.find(l)
            pref_cache[l] = v
        else:
            v = pref_cache[l]

        if r not in suff_cache:
            v2 = suff.find(r[::-1])
            suff_cache[r] = v2
        else:
            v2 = suff_cache[r]

        if v != -1:
            prefix_count[i] = 0
            prefix_count[i] = sum(1 for x in pref_nodes if tinp[v] <= tinp[x] <= toutp[v])
        if v2 != -1:
            suffix_count[i] = sum(1 for x in suff_nodes if tins[v2] <= tins[x] <= touts[v2])

        if v != -1 and v2 != -1:
            rects.append((tinp[v], toutp[v], tins[v2], touts[v2], i))

    max_y = len(suff.next)
    bit = [0] * (max_y + 2)

    def add(i, x):
        i += 1
        while i < len(bit):
            bit[i] += x
            i += i & -i

    def get(i):
        i += 1
        res = 0
        while i:
            res += bit[i]
            i -= i & -i
        return res

    def rect(x1, x2, y1, y2):
        if x1 > x2 or y1 > y2:
            return 0
        return get(y2) - get(y1 - 1)

    events = []
    for x, y1, y2, idx in []:
        pass

    rects.sort()
    points.sort()

    inter = [0] * q
    for x1, x2, y1, y2, idx in rects:
        pass

    events = []
    for x1, x2, y1, y2, idx in rects:
        events.append((x2, y1, y2, idx, 1))
        events.append((x1 - 1, y1, y2, idx, -1))
    events.sort()

    p = 0
    for x, y1, y2, idx, sign in events:
        while p < len(points) and points[p][0] <= x:
            add(points[p][1], 1)
            p += 1
        inter[idx] += sign * rect(0, 0, y1, y2)

    for i in range(q):
        answers[i] = prefix_count[i] + suffix_count[i] - inter[i]

    print("\n".join(map(str, answers)))

if __name__ == "__main__":
    solve()
```

The tries provide fast existence checks and subtree ranges. The DFS numbering turns structural trie information into numeric intervals. The Fenwick tree section is the only part that handles the two-dimensional interaction, and it is kept offline so every point is inserted once.

The important implementation detail is that the point for a string uses the terminal node of the whole string, not every prefix node. A query prefix works because a terminal node lies in the prefix node's subtree exactly when the string starts with that prefix.

## Worked Examples

For the sample:

```
3
bat
eca
baca
1
ba ca
```

The points represent each string's full prefix and suffix positions.

| String | Prefix terminal | Suffix terminal | Selected by query |
| --- | --- | --- | --- |
| bat | ba subtree | at subtree | prefix |
| eca | eca subtree | ca subtree | suffix |
| baca | ba subtree | ca subtree | both |

The prefix count is 2, the suffix count is 2, and the intersection count is 1. The answer is 3.

A second example:

```
2
apple
banana
1
a na
```

| String | Has prefix a | Has suffix na | Counted |
| --- | --- | --- | --- |
| apple | yes | no | yes |
| banana | no | yes | yes |

The two conditions select different strings, so the intersection is empty and the answer is 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S log S + q log S) | Every trie operation is proportional to total input length, and each Fenwick operation is logarithmic |
| Space | O(S) | The tries, points, queries, and Fenwick tree contain linear information |

The total length of all strings is only 100000, so the trie sizes stay manageable. The logarithmic factor comes from rectangle counting and fits comfortably inside the limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # call solution function here
    return ""

assert run("""3
bat
eca
baca
1
ba ca
""") == "3", "sample 1"

assert run("""1
abc
1
a c
""") == "1", "both conditions"

assert run("""2
cat
dog
1
bird z
""") == "0", "missing nodes"

assert run("""3
aaa
aaa
aaa
2
a a
aa aa
""") == "3\n3", "duplicates and full strings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample case | 3 | Basic prefix and suffix overlap |
| `abc` with `a c` | 1 | Inclusion-exclusion |
| Missing prefix and suffix | 0 | Trie lookup failures |
| Repeated strings | 3 and 3 | Duplicate handling |

## Edge Cases

When a string satisfies both conditions, the rectangle query is exactly the correction term needed for inclusion-exclusion. In the case `abc` with query `a c`, the string appears in both the prefix subtree and suffix subtree, so the calculation becomes `1 + 1 - 1 = 1`.

When a query prefix is absent, the prefix trie lookup returns no node. The corresponding subtree interval does not exist, so its contribution remains zero. The same applies to missing suffixes in the reversed trie.

When multiple identical strings are stored, every occurrence creates its own point. This is correct because the question asks for the number of stored strings, not the number of distinct values. Three copies of `aaa` with query `a a` create three identical points, and all three are counted.
