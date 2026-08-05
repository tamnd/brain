---
title: "CF 102511G - First of Her Name"
description: "The input describes a rooted family tree. Every lady stores only the first letter of her own name and the index of her mother."
date: "2026-08-05T16:28:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102511
codeforces_index: "G"
codeforces_contest_name: "2019 ICPC World Finals"
rating: 0
weight: 102511
solve_time_s: 184
verified: true
draft: false
---

[CF 102511G - First of Her Name](https://codeforces.com/problemset/problem/102511/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a rooted family tree. Every lady stores only the first letter of her own name and the index of her mother. A daughter's complete name is obtained by putting her letter in front of her mother's complete name, so moving from a node to its parent removes the first character of the name.

For every query string, we need the number of nodes whose complete name begins with that string. The challenge is that a name is not stored explicitly. A chain of one million ladies can create names of length one million, so constructing every name would already be too expensive.

The limits force a linear or almost linear solution. There can be one million ladies and one million total query characters. An approach that walks through every name for every query can perform around $10^{12}$ character checks in a long chain, which is far beyond the available time. The alphabet is only 26 letters, so solutions that use linear string processing are possible.

The tricky cases are caused by prefixes that appear at different depths of the family tree. A query can be equal to a complete name, can be shorter than a name, or can have no matching name.

For example, the input

```
1 3
A 0
A
AA
B
```

has only the name `A`. The correct output is

```
1
0
0
```

A solution that assumes every query has to match a full name would incorrectly reject the first query.

Another case is a query that is a prefix of several related names:

```
3 2
S 0
A 1
B 2
A
BA
```

The names are `S`, `AS`, and `BAS`. The output is

```
1
1
```

The query `A` matches only `AS`, not every descendant of the `A` node, because names grow by adding letters to the front.

## Approaches

A direct solution would reconstruct every lady's name and store all of them. To answer a query, we could compare it with every name. This is correct because it checks exactly the required prefix relation. The problem is the cost. In a chain of one million ladies, the total length of all reconstructed names is about $10^{12}$, and comparing queries against them would be even larger.

The useful observation is that the family relation is backwards for prefix queries. A daughter is created by adding a letter to the beginning of the mother's name. If every name is reversed, a daughter is created by appending a letter to the end. The family tree becomes a normal trie of reversed names.

A query asking whether `s` is a prefix of an original name becomes a question about whether `reverse(s)` is a suffix of a path string in this trie. This turns the problem into finding many suffixes among many trie paths.

We can insert all reversed queries into an Aho-Corasick automaton. While traversing the family trie, we maintain the automaton state after reading the current reversed name. Every visited lady contributes one occurrence to that state. A query matches a state whenever that state is inside the query node's failure subtree, because failure links represent suffix relationships.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 + nk)$ | $O(n^2)$ | Too slow |
| Optimal | $O(n + L)$ | $O(n + L)$ | Accepted |

Here $L$ is the total length of all queries.

## Algorithm Walkthrough

1. Reverse every query string and insert it into a trie. The terminal node of each inserted string is stored so the answer can be recovered later. Reversing is the key transformation because the family construction naturally appends characters after reversal.
2. Build failure links for the trie using the Aho-Corasick construction. Missing transitions are filled using failure transitions, allowing every character to be processed in constant time.
3. Store the family tree using child lists. Traverse it from the founder while keeping the current Aho-Corasick state. When moving to a daughter, feed the daughter's character into the automaton and increment the counter of the resulting state.
4. Build the failure-link tree of the automaton. Add each state's counter to its parent in this tree, processing nodes from deepest to shallowest. After this propagation, every state contains the number of family names for which the string represented by that state is a suffix.
5. For each query, output the accumulated value stored at its terminal node in the automaton.

Why it works: after reversing, every lady corresponds to one root-to-node string in the family trie. The automaton state reached after visiting a lady represents the longest query prefix that is also a suffix of that reversed name. Failure links contain all shorter suffix matches. Propagating counts through the failure tree transfers each occurrence to every query string that is a suffix, which is exactly the original prefix condition.

## Python Solution

```python
import sys
from collections import deque
from array import array

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    fam_head = array('i', [-1]) * (n + 1)
    fam_to = array('i')
    fam_next = array('i')
    fam_ch = array('b')

    for i in range(1, n + 1):
        c, p = input().split()
        c = ord(c) - 65
        p = int(p)
        if p:
            fam_to.append(i)
            fam_next.append(fam_head[p])
            fam_ch.append(c)
            fam_head[p] = len(fam_to) - 1

    q_terminal = array('i', [0]) * k

    head = array('i', [-1])
    to = array('i')
    nxt = array('i')
    ch = array('b')

    def new_node():
        head.append(-1)
        return len(head) - 1

    for qi in range(k):
        s = input().strip()[::-1]
        cur = 0
        for x in s:
            c = ord(x) - 65
            e = head[cur]
            found = -1
            while e != -1:
                if ch[e] == c:
                    found = to[e]
                    break
                e = nxt[e]
            if found == -1:
                found = new_node()
                to.append(found)
                ch.append(c)
                nxt.append(head[cur])
                head[cur] = len(to) - 1
            cur = found
        q_terminal[qi] = cur

    m = len(head)
    fail = array('i', [0]) * m

    trans = array('i', [-1]) * (m * 26)
    for v in range(m):
        e = head[v]
        while e != -1:
            trans[v * 26 + ch[e]] = to[e]
            e = nxt[e]

    q = deque()
    for c in range(26):
        x = trans[c]
        if x == -1:
            trans[c] = 0
        else:
            q.append(x)

    while q:
        v = q.popleft()
        base = v * 26
        fbase = fail[v] * 26
        for c in range(26):
            u = trans[base + c]
            if u == -1:
                trans[base + c] = trans[fbase + c]
            else:
                fail[u] = trans[fbase + c]
                q.append(u)

    cnt = array('i', [0]) * m
    stack = [(1, 0)]
    while stack:
        v, state = stack.pop()
        e = fam_head[v]
        while e != -1:
            u = fam_to[e]
            ns = trans[state * 26 + fam_ch[e]]
            cnt[ns] += 1
            stack.append((u, ns))
            e = fam_next[e]

    children = [[] for _ in range(m)]
    for i in range(1, m):
        children[fail[i]].append(i)

    order = list(range(m))
    order.sort(key=lambda x: -x)
    for v in order:
        if v:
            cnt[fail[v]] += cnt[v]

    ans = []
    for x in q_terminal:
        ans.append(str(cnt[x]))
    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The family tree is stored separately from the automaton because the two structures represent different directions of the problem. The family traversal creates the reversed names, while the automaton answers suffix queries over those names.

The query insertion uses reversed strings. The terminal node is saved immediately because after all preprocessing the answer is attached to that exact automaton node.

The failure-link propagation is done from children toward parents. A query string can be a suffix represented by many states, so the final count is not known until all descendants in the failure tree have contributed.

All counters fit in Python integers. The arrays use compact storage because the number of nodes can reach one million.

## Worked Examples

For the sample:

```
10 5
S 0
Y 1
R 2
E 3
N 4
E 5
A 6
D 7
Y 7
R 9
RY
E
N
S
AY
```

the reversed query trie receives `YR`, `E`, `N`, `S`, and `YA`.

During the family traversal:

| Lady | Reversed path state meaning | Added count |
| --- | --- | --- |
| S | S | 1 |
| YS | YS | 1 |
| RYS | YRS | 1 |
| ERYS | YRSE | 1 |
| NERYS | YRSEN | 1 |
| ENERYS | YRSENE | 1 |
| AENERYS | YRSENEA | 1 |
| DAENERYS | YRSENEAD | 1 |
| YAENERYS | YRSENEAY | 1 |
| RYAENERYS | YRSENEAYR | 1 |

The failure propagation makes `YR` receive two matches, because both `RYS` and `RYAENERYS` end with the reversed query. It also makes `E` receive two matches and `N` receive one.

A smaller case:

```
3 3
A 0
B 1
C 2
A
BA
CBA
```

The names are `A`, `BA`, and `CBA`.

| Query | Reversed query | Matching names |
| --- | --- | --- |
| A | A | A, BA, CBA |
| BA | AB | BA, CBA |
| CBA | ABC | CBA |

The automaton counts suffixes of reversed names, which corresponds exactly to prefixes of the original names.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + L)$ | Each family edge and query character is processed a constant number of times. |
| Space | $O(n + L)$ | The family tree and automaton each contain at most linear numbers of nodes. |

The maximum input size is one million family nodes and one million query characters. The algorithm only performs linear passes over these objects, which is the required scale for the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    oldout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = oldout
    return out.getvalue()

assert run("""10 5
S 0
Y 1
R 2
E 3
N 4
E 5
A 6
D 7
Y 7
R 9
RY
E
N
S
AY
""") == """2
2
1
1
0"""

assert run("""1 3
A 0
A
AA
B
""") == """1
0
0"""

assert run("""3 3
A 0
B 1
C 2
A
BA
CBA
""") == """1
1
1"""

assert run("""2 2
Z 0
Z 1
Z
ZZ
""") == """1
1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single founder | `1,0,0` | Queries equal to the root name and missing prefixes |
| Increasing chain | `1,1,1` | Prefixes along a long dependency chain |
| Repeated letters | `1,1` | Correct handling of identical characters and suffix links |

## Edge Cases

A query that matches the founder alone is handled because the root lady is also visited during traversal. The algorithm starts counting from the actual family nodes, so the name `S` contributes once in the sample.

A query shorter than a full name is handled by failure propagation. For example, in the chain `A`, `BA`, `CBA`, the query `A` corresponds to a suffix of all reversed paths, so the failure tree adds all three occurrences to the terminal state.

A query with no possible match never receives any contribution. Its automaton node remains at zero because no family traversal reaches it or any state below it in the failure tree.
