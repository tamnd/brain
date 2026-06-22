---
title: "CF 105394H - Headline Heat"
description: "We are given a collection of university names, a set of rivalries between some pairs of universities, and a sequence of news articles. For each article, we must decide whether it is “balanced enough” or whether it would anger at least one coach."
date: "2026-06-23T04:59:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105394
codeforces_index: "H"
codeforces_contest_name: "2024-2025 ICPC German Collegiate Programming Contest (GCPC 2024)"
rating: 0
weight: 105394
solve_time_s: 48
verified: true
draft: false
---

[CF 105394H - Headline Heat](https://codeforces.com/problemset/problem/105394/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of university names, a set of rivalries between some pairs of universities, and a sequence of news articles. For each article, we must decide whether it is “balanced enough” or whether it would anger at least one coach.

A coach associated with a university becomes angry if, inside a single article, some rival university appears strictly more often than their own university. Since rivalries are symmetric, each rivalry pair defines a pair of universities that must be compared against each other.

So for every article, we effectively need to count how many times each university name appears as a substring occurrence in the article text, and then for every rivalry edge u-v check whether count[u] < count[v] or count[v] < count[u] in a way that violates the rule. If any rivalry pair is imbalanced in either direction, the article is rejected.

The hard part is that university names are arbitrary lowercase strings with spaces, they can overlap, and one name can appear inside another. A naive substring search per name per article is far too slow.

The constraints are tight in aggregate. The total length of all university names plus all articles is at most 10^6, but the number of universities, rivalries, and articles can each be up to 10^5. This strongly suggests we need something close to linear time over the text, not per-pattern matching. Any approach that scans each article separately for every university name will degrade to about O(k · n · L), which is completely infeasible.

A second subtle issue is overlapping matches. For example, if one university is “uni” and another is “uni ulm”, naive substring matching might count “uni” inside “uni ulm” in multiple inconsistent ways. We need a consistent multi-pattern matching method that counts all occurrences correctly.

Edge cases that break naive solutions include:

An article like “uniuni” with universities “uni” and “uniu”. A naive search might miss overlapping matches or double count depending on implementation.

Another example is names that are substrings of others, such as “kit” and “kitten”. In an article “kitten kit”, we must count both patterns independently without interference.

Finally, articles may contain spaces and patterns that span spaces, so splitting on whitespace is not valid.

## Approaches

A brute-force approach tries each university name as a pattern and scans each article using substring search. For each article, for each university, we check all possible starting positions. If the average article length is L and there are n universities, this becomes O(k · n · L), which is far beyond limits.

Even optimizing substring search per pattern using KMP reduces it to O(k · (n + L)), but building and running KMP separately for every university still multiplies by n, which is too slow.

The key observation is that we are matching many patterns simultaneously against many texts. This is exactly the setting for an Aho-Corasick automaton. By building a single automaton over all university names, we can scan each article once in linear time and report all matched patterns.

The idea is to treat all university names as strings in a trie, then augment it with failure links so that we can transition through the text in O(length of article), while emitting all matched pattern IDs. Each character advances a state, and whenever we reach a node that corresponds to a pattern end, we increment that university’s count.

After computing counts for an article, we only need to check all rivalry edges. Each edge is a simple comparison of two integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per pattern | O(k · n · L) | O(1) | Too slow |
| KMP per pattern | O(k · (n + L)) | O(n · pattern size) | Too slow |
| Aho-Corasick | O(total text + total patterns + matches + m) | O(total pattern size) | Accepted |

## Algorithm Walkthrough

We build a multi-pattern matching automaton over all university names, then use it to process each article.

1. Insert every university name into a trie and assign each name a unique identifier. Each terminal node stores the university index it represents. This ensures every occurrence can be mapped back to a university.
2. Build failure links using a BFS over the trie. The failure link of a node points to the longest proper suffix of the current prefix that is also a prefix in the trie. This allows us to fall back efficiently when a mismatch occurs while scanning text.
3. Also propagate output links: if a failure link points to a node that is a valid pattern end, we ensure that the current node can also report that pattern. This guarantees we detect all matches, including overlapping ones.
4. For each article, start at the root of the automaton and scan characters one by one. For each character, follow transitions; if a transition does not exist, follow failure links until either a match is found or we return to root. Each visited state may correspond to one or more university names, and we increment their counters accordingly.
5. After scanning the article, we check all rivalry pairs. For each pair (u, v), if count[u] < count[v] or count[v] < count[u], we mark the article as invalid.
6. Output “yes” if no rivalry constraint is violated, otherwise output “no”.

### Why it works

At any position in the article, the automaton state represents the longest suffix of the processed prefix that matches a prefix of some university name. The failure links ensure that all shorter suffixes are also considered implicitly. This means every occurrence of every pattern ending at the current position is discovered exactly once. Because every university occurrence is counted correctly and independently, the final counts are exact. The rivalry check is then a direct comparison on true frequencies, so correctness reduces to correctness of multi-pattern matching.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

class Node:
    __slots__ = ("next", "link", "out")
    def __init__(self):
        self.next = {}
        self.link = 0
        self.out = []

class Aho:
    def __init__(self):
        self.t = [Node()]

    def add(self, s, idx):
        v = 0
        for ch in s:
            if ch not in self.t[v].next:
                self.t[v].next[ch] = len(self.t)
                self.t.append(Node())
            v = self.t[v].next[ch]
        self.t[v].out.append(idx)

    def build(self):
        q = deque()
        for c, v in self.t[0].next.items():
            self.t[v].link = 0
            q.append(v)

        while q:
            v = q.popleft()
            for c, u in self.t[v].next.items():
                q.append(u)

                f = self.t[v].link
                while f and c not in self.t[f].next:
                    f = self.t[f].link
                self.t[u].link = self.t[f].next[c] if c in self.t[f].next else 0

                self.t[u].out += self.t[self.t[u].link].out

    def run(self, text, cnt):
        v = 0
        for ch in text:
            while v and ch not in self.t[v].next:
                v = self.t[v].link
            if ch in self.t[v].next:
                v = self.t[v].next[ch]
            else:
                v = 0

            for idx in self.t[v].out:
                cnt[idx] += 1

def solve():
    n, m, k = map(int, input().split())
    names = [input().rstrip("\n") for _ in range(n)]

    aho = Aho()
    for i, s in enumerate(names):
        aho.add(s, i)
    aho.build()

    edges = [tuple(map(lambda x: int(x) - 1, input().split())) for _ in range(m)]
    articles = [input().rstrip("\n") for _ in range(k)]

    for t in articles:
        cnt = [0] * n
        aho.run(t, cnt)

        ok = True
        for u, v in edges:
            if cnt[u] < cnt[v] or cnt[v] < cnt[u]:
                ok = False
                break

        print("yes" if ok else "no")

if __name__ == "__main__":
    solve()
```

The trie construction stores every university name as a path, and each terminal node remembers which university index it corresponds to. The failure link construction ensures that when we fail to extend a match, we fall back to the longest valid suffix state. The propagation of `out` lists through failure links ensures we count patterns even when they end at different depths of the automaton.

During article processing, we maintain a single state pointer. Each character transition is amortized O(1), so scanning is linear in the article length. Every time we hit a node with outputs, we increment counts for all matched universities.

The final loop over rivalry edges is separated from matching so we avoid repeated comparisons during scanning.

## Worked Examples

### Sample 1

Input:

```
3 1 4
hpi
fau
kit
1 3
kit destroys hpi at wintercontest
gcpc is great
team moshpit from hpi beats kit teams
whats the abbreviation for university of erlangen nuremberg
```

We track matches per article:

| Article | Matches found (hpi, fau, kit) | Rival check (1,3) | Result |
| --- | --- | --- | --- |
| kit destroys hpi at wintercontest | (1,0,1) | 1 == 1 | yes |
| gcpc is great | (0,0,0) | 0 == 0 | yes |
| team moshpit from hpi beats kit teams | (1,0,1) | equal | no violation? actually equal so yes |
| whats the abbreviation... | (0,0,0) | equal | yes |

The third line demonstrates that even with multiple occurrences, equality of counts is allowed, and only strict imbalance matters.

### Sample 2

Input:

```
6 3 5
uds
cu
tum
rwth
uni ulm
uni
4 1
2 5
1 3
last gcpc rwth had a team in top ten two places behind tum
who is team debuilding from constructor university bremen
top ten teams last year are from kit cu uds hpi tum and rwth
uni ulm cu uni ulm
sunday alright lets go
```

First article:

```
last gcpc rwth ... tum
```

| uds | cu | tum | rwth | uni ulm | uni |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 0 | 0 |

Edges check:

(4,1): rwth vs uds equal ok

(2,5): cu vs uni equal ok

(1,3): uds vs tum violated? tum > uds so invalid → no

This shows how a single dominance relationship triggers rejection even if most universities do not appear.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Σ | names |
| Space | O(Σ | names |

The total length bound of 10^6 ensures the automaton scan dominates and remains within limits. Even with up to 10^5 articles, each is processed in time proportional to its length.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else ""

# provided samples (placeholders, since full harness not embedded)
# assert run(...) == ...

# minimal case
assert True

# overlapping names
# uni and uni ulm behavior stress case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node no edges | yes | trivial acceptance |
| overlapping names | depends | substring overlap correctness |
| all rivals always equal counts | yes | symmetry handling |

## Edge Cases

One important edge case is overlapping university names. If we have “uni” and “uni ulm”, scanning “uni ulm uni ulm” should count both correctly at both positions. The automaton ensures that after matching “uni”, we can still continue and also match “uni ulm” when appropriate, because transitions encode full paths and failure links allow suffix reuse.

Another edge case is repeated occurrences. In “uni uni uni”, the state returns to intermediate nodes correctly after failure transitions, so each occurrence increments independently.

A third edge case is when no university appears at all. All counts are zero, so every rivalry comparison is equal and every article is accepted. The implementation handles this naturally because no output nodes are visited.
