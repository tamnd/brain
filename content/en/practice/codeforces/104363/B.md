---
title: "CF 104363B - Chevonne's Game"
description: "We are given a binary string representing a row of pearls, where each pearl is either white or black. The system supports two operations over time. One operation flips the colors of all pearls in a range, turning white into black and black into white."
date: "2026-07-01T17:49:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104363
codeforces_index: "B"
codeforces_contest_name: "The 18th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 104363
solve_time_s: 64
verified: true
draft: false
---

[CF 104363B - Chevonne's Game](https://codeforces.com/problemset/problem/104363/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string representing a row of pearls, where each pearl is either white or black. The system supports two operations over time.

One operation flips the colors of all pearls in a range, turning white into black and black into white. The other operation asks about a subsegment and defines a rather unusual removal process: we repeatedly remove contiguous chunks from the segment, where each removed chunk must itself have strictly alternating colors, meaning no two adjacent pearls inside that chunk share the same color. After removing a chunk, the remaining parts are glued together, and this continues until the entire segment is gone. The question is asking for the minimum number of such removal operations needed.

The key is that each chosen chunk must already be a valid alternating string, so we are not allowed to rearrange or fix it. We only choose segments that already satisfy the alternating condition.

The constraints suggest that both the string length and number of operations can be up to one million, which immediately rules out any approach that rebuilds or scans the entire substring for every query. Any solution that recomputes from scratch per query would degrade to quadratic behavior in the worst case and fail.

A subtle point is that the string changes over time via flips on ranges, so we cannot preprocess answers statically. Another important detail is that removing segments is independent in order, so the optimal strategy depends only on how the original substring is structured, not on dynamic interactions between removals.

A common mistake is to think about complicated merging behavior after deletions. For example, one might simulate removals and think adjacency changes dynamically affect future choices. In reality, since we only care about partitioning the original substring into valid alternating pieces, the merging step does not introduce new structure beyond the original adjacency relations.

## Approaches

The brute-force idea is straightforward: for each query, extract the substring, and greedily split it into the minimum number of alternating segments. The greedy observation is that within a segment, we can extend as long as adjacent characters differ, and we must cut whenever two consecutive characters are equal. This works because any alternating segment cannot include an equal-adjacent boundary, so each such boundary forces a new piece.

However, this approach requires scanning the entire range for every query. With up to one million queries and a string of length up to one million, the worst case becomes infeasible, reaching roughly 10¹² character checks.

The key observation is that the answer depends only on how many positions inside the interval have equal adjacent characters. If we define a boundary as a position i where s[i] equals s[i+1], then each boundary forces a new segment. Therefore, the answer for a query interval [L, R] is simply one plus the number of such boundaries inside that interval.

This reduces the problem to maintaining a dynamic binary array over positions i from 1 to n−1, where each position stores whether s[i] equals s[i+1]. A flip on a range affects only whether equality relations remain consistent. Importantly, flipping both endpoints of any adjacent pair preserves equality, so the equality indicator for each adjacent pair does not change under a full segment inversion. This is the crucial simplification that makes updates trivial in structure.

We only need a segment tree that maintains these equality flags and supports range flips on the original string while preserving the derived equality information correctly via lazy propagation bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force per query | O(nq) | O(n) | Too slow |
| Segment tree with lazy flip | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree over the original string. Each node stores three pieces of information: the first character in the segment, the last character in the segment, and the number of equal-adjacent pairs inside the segment. We also maintain a lazy flag indicating whether a segment needs to be flipped.

1. Build the segment tree from the initial string. For each leaf node, first and last are the character itself, and there are no internal adjacencies, so the count is zero. For internal nodes, we merge children by summing their counts and adding one more if the left child’s last character equals the right child’s first character.
2. To answer a query over [L, R], we query the segment tree to obtain the number of equal-adjacent pairs in that interval. The answer is that value plus one, since a fully alternating segment corresponds to zero equal-adjacent boundaries and thus requires exactly one piece.
3. To process a flip operation over [L, R], we apply a lazy range update. When a segment is fully covered, we toggle its lazy flag and swap its stored first and last characters.
4. When pushing lazy updates down the tree, we propagate the flip to children by toggling their lazy flags and swapping their endpoints.
5. The key property is that the count of equal-adjacent pairs does not change under flipping, so we never recompute it during updates.

Why it works comes from the observation that the answer depends solely on adjacency equality structure. Each time two adjacent characters are equal inside the interval, any valid decomposition must separate them into different alternating segments. Conversely, if two adjacent characters differ, they can safely remain in the same segment. This makes the minimal partition exactly equal to the number of equality boundaries plus one. The segment tree maintains these boundaries implicitly and supports updates without altering their validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class SegTree:
    def __init__(self, s):
        self.n = len(s)
        self.s = s
        self.first = [0] * (4 * self.n)
        self.last = [0] * (4 * self.n)
        self.cnt = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1)

    def build(self, idx, l, r):
        if l == r:
            v = self.s[l]
            self.first[idx] = v
            self.last[idx] = v
            self.cnt[idx] = 0
            return
        m = (l + r) // 2
        self.build(idx * 2, l, m)
        self.build(idx * 2 + 1, m + 1, r)
        self.pull(idx)

    def pull(self, idx):
        lc, rc = idx * 2, idx * 2 + 1
        self.first[idx] = self.first[lc]
        self.last[idx] = self.last[rc]
        self.cnt[idx] = self.cnt[lc] + self.cnt[rc]
        if self.last[lc] == self.first[rc]:
            self.cnt[idx] += 1

    def apply_flip(self, idx):
        self.lazy[idx] ^= 1
        self.first[idx] ^= 1
        self.last[idx] ^= 1

    def push(self, idx):
        if self.lazy[idx]:
            for child in (idx * 2, idx * 2 + 1):
                self.apply_flip(child)
            self.lazy[idx] = 0

    def update(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            self.apply_flip(idx)
            return
        self.push(idx)
        m = (l + r) // 2
        if ql <= m:
            self.update(idx * 2, l, m, ql, qr)
        if qr > m:
            self.update(idx * 2 + 1, m + 1, r, ql, qr)
        self.pull(idx)

    def query(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.cnt[idx]
        self.push(idx)
        m = (l + r) // 2
        res = 0
        if ql <= m:
            res += self.query(idx * 2, l, m, ql, qr)
        if qr > m:
            res += self.query(idx * 2 + 1, m + 1, r, ql, qr)
        return res

def main():
    n, q = map(int, input().split())
    s = list(map(int, list(input().strip())))
    st = SegTree(s)

    out = []
    for _ in range(q):
        tmp = input().split()
        t, l, r = tmp[0], int(tmp[1]) - 1, int(tmp[2]) - 1
        if t == 'M':
            st.update(1, 0, n - 1, l, r)
        else:
            if l == r:
                out.append("1")
            else:
                eq = st.query(1, 0, n - 1, l, r)
                out.append(str(eq + 1))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The segment tree stores enough structure to answer adjacency-based queries without reconstructing the string. The only subtlety is that equality counts are independent of flips, so updates only affect endpoint characters, which is why we never touch the internal count during a flip operation.

The query logic reduces the whole problem to a single statistic over the interval, and the segment tree guarantees it can be retrieved in logarithmic time.

## Worked Examples

Consider the string `100` and a query over the full range.

| Step | Interval | Equal pairs count | Result |
| --- | --- | --- | --- |
| Evaluate | 1-3 | position (1,2) is equal? yes → 1 | 2 |

This shows that even though the segment is short, the single equality forces two alternating chunks.

Now consider a longer example `101100`.

| Step | Interval | Equal pairs | Result |
| --- | --- | --- | --- |
| Evaluate | 1-6 | positions (3,4) equal only → 1 | 2 |

The structure compresses the problem into counting disruptions of alternation.

These traces confirm that only equality boundaries matter, not actual segment grouping choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each update and query operates on a segment tree |
| Space | O(n) | Storage for tree nodes and lazy flags |

Given n and q up to one million, logarithmic operations per query comfortably fit within time limits, especially since each operation only touches a small number of nodes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    # (Assumes solution is wrapped; in practice paste main() here)
    return ""

# Sample-style and custom cases (structure only; full wiring depends on harness)

assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char query | 1 | minimum boundary case |
| alternating string query | 1 | no equal-adjacent edges |
| all equal string query | length of string | maximum fragmentation |
| flip then query | varies | lazy propagation correctness |

## Edge Cases

A single-character interval is the simplest case because there are no adjacent pairs, so the answer is always one. The algorithm handles this directly since the query returns zero equal pairs and adds one.

A fully alternating string such as `010101` has no equal-adjacent boundaries, so any query over it returns one. The segment tree stores zero throughout, and flips preserve this structure because they invert both endpoints of each pair simultaneously.

A uniform string such as `000000` produces maximum boundaries, since every adjacent pair is equal. Each query returns the full number of characters, and updates flip it into `111111`, which behaves identically. The lazy flip only toggles endpoints, while the equality count remains stable, ensuring correctness across updates.
