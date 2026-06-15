---
title: "CF 1234D - Distinct Characters Queries"
description: "We are maintaining a string of lowercase letters under two kinds of operations. One operation modifies a single position in the string, changing its character."
date: "2026-06-15T20:02:04+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1234
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 590 (Div. 3)"
rating: 1600
weight: 1234
solve_time_s: 177
verified: true
draft: false
---

[CF 1234D - Distinct Characters Queries](https://codeforces.com/problemset/problem/1234/D)

**Rating:** 1600  
**Tags:** data structures  
**Solve time:** 2m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a string of lowercase letters under two kinds of operations. One operation modifies a single position in the string, changing its character. The other operation asks about a segment of the string and requires counting how many different letters appear inside that segment.

The key difficulty is that both updates and range queries are interleaved. A static solution that recomputes answers from scratch for every query would repeatedly scan substrings of length up to 100,000, which is far too slow when there are also up to 100,000 queries.

The constraints imply a total input size on the order of 200,000 operations over a structure of size up to 100,000. Any solution that performs linear work per query would reach about 10¹⁰ character inspections in the worst case, which is infeasible under a 2 second limit. This immediately rules out naive substring scanning.

A second subtle issue is that updates affect future queries. A query depends on the current version of the string, not the initial one. Any approach must maintain a dynamic structure rather than recomputing from a fixed snapshot.

One subtle edge case comes from repeated updates to the same position. For example, if we repeatedly change a single index back and forth and query around it, a correct solution must always reflect the latest character, not assume monotonic behavior.

Another case that breaks naive solutions is overlapping queries after updates. For example, if we change a character inside a previously queried range, the answer must reflect the new string state, not cached results.

## Approaches

A brute-force solution processes each query independently. For a type 2 query on range `[l, r]`, we scan the substring and mark which of the 26 letters appear. We then count how many were seen. This is correct because the definition of the answer is purely local to the substring.

However, this approach costs O(r - l + 1) per query. In the worst case, a single query scans 100,000 characters, and with 100,000 queries the total work becomes quadratic. This fails immediately.

The key observation is that the alphabet size is constant and small. Instead of tracking full substrings, we can maintain, for each character, the set of positions where it occurs. Then a range query becomes: does this character appear at least once in the interval?

To support dynamic updates efficiently, we need a structure that maintains membership of indices in sorted order and supports fast insertion, deletion, and range counting. A Fenwick Tree (Binary Indexed Tree) works well if we maintain 26 separate BITs, one for each letter. Each BIT stores a 1 at positions where that letter currently appears and 0 elsewhere.

A point update removes the old character at position `pos` from its BIT and inserts the new one. A query checks each of the 26 BITs and counts how many have a nonzero sum in `[l, r]`.

Since 26 is constant, each query becomes O(26 log n), which is effectively O(log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per query | O(1) | Too slow |
| 26 BITs | O(26 log n) per query | O(26n) | Accepted |

## Algorithm Walkthrough

We maintain 26 Fenwick Trees, each representing one character. We also maintain the current string so we know what character is currently stored at each position.

1. Initialize 26 Fenwick Trees of size n, and build them using the initial string. For each position `i`, we add 1 to the BIT corresponding to `s[i]`. This ensures each tree reflects where its character appears.
2. For a type 1 query `pos c`, we first locate the previous character at `pos`. We remove it from its corresponding BIT by subtracting 1 at that index. Then we insert the new character into its BIT by adding 1 at the same position. Finally, we update the stored string.
3. For a type 2 query `l r`, we iterate over all 26 characters. For each character, we compute the sum on its BIT in range `[l, r]`. If the sum is greater than zero, that character appears at least once in the substring, so we count it.
4. Output the accumulated count for each query of type 2.

The non-obvious part is why a sum greater than zero correctly represents existence. Each BIT stores exactly the indicator function of positions where a character occurs, so the sum over a range is precisely the number of occurrences in that segment.

### Why it works

At every moment, each position in the string is represented exactly once across the 26 BITs. Updates preserve this invariant by removing the old character before inserting the new one. Therefore, each BIT always contains a correct indicator array for its character. Range sums on this indicator array directly correspond to presence checks, and summing over all characters yields the number of distinct letters in the segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def main():
    s = list(input().strip())
    n = len(s)

    bits = [Fenwick(n) for _ in range(26)]

    for i, ch in enumerate(s, 1):
        bits[ord(ch) - 97].add(i, 1)

    q = int(input())
    out = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            pos = int(tmp[1])
            c = tmp[2]
            old = s[pos - 1]
            if old != c:
                bits[ord(old) - 97].add(pos, -1)
                bits[ord(c) - 97].add(pos, 1)
                s[pos - 1] = c
        else:
            l, r = int(tmp[1]), int(tmp[2])
            ans = 0
            for i in range(26):
                if bits[i].range_sum(l, r) > 0:
                    ans += 1
            out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution keeps the string in a mutable list so updates are O(1) at the array level. Each Fenwick Tree uses 1-based indexing to simplify parent navigation. The update operation carefully removes the old character before inserting the new one, which prevents double counting.

Range queries rely on `range_sum(l, r)` which computes prefix differences. The final loop over 26 characters is safe because alphabet size is fixed.

## Worked Examples

### Example 1

Input:

```
abacaba
5
2 1 4
1 4 b
1 5 b
2 4 6
2 1 7
```

Initial state is `"abacaba"`.

| Step | Operation | Range/String | Key BIT changes | Distinct result |
| --- | --- | --- | --- | --- |
| 1 | query | [1,4] = "abac" | none | {a,b,c} = 3 |
| 2 | update | pos 4 -> b | remove a at 4, add b at 4 | string = "abbcaba" |
| 3 | update | pos 5 -> b | remove a at 5, add b at 5 | string = "abbcbba" |
| 4 | query | [4,6] = "cbb" | none | {c,b} = 2 |
| 5 | query | [1,7] | none | {a,b,c} = 3 |

The trace shows how updates only affect local BITs while queries remain independent and fast.

### Example 2

Input:

```
aaaa
3
2 1 4
1 2 b
2 1 4
```

| Step | Operation | String | Distinct letters |
| --- | --- | --- | --- |
| 1 | query | "aaaa" | {a} = 1 |
| 2 | update | "abaa" | removes a at 2, adds b |
| 3 | query | "abaa" | {a,b} = 2 |

This demonstrates that a single update immediately affects future range queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 log n) per query | Each update touches one BIT, each query checks 26 BIT ranges |
| Space | O(26 n) | 26 Fenwick trees storing n positions each |

With n, q ≤ 100,000, this fits comfortably within limits. The constant factor 26 is small and the logarithmic factor is fast in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

        def range_sum(self, l, r):
            return self.sum(r) - self.sum(l - 1)

    s = list(input().strip())
    n = len(s)
    bits = [Fenwick(n) for _ in range(26)]

    for i, ch in enumerate(s, 1):
        bits[ord(ch) - 97].add(i, 1)

    q = int(input())
    out = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            pos = int(tmp[1])
            c = tmp[2]
            old = s[pos - 1]
            if old != c:
                bits[ord(old) - 97].add(pos, -1)
                bits[ord(c) - 97].add(pos, 1)
                s[pos - 1] = c
        else:
            l, r = int(tmp[1]), int(tmp[2])
            ans = 0
            for i in range(26):
                if bits[i].range_sum(l, r) > 0:
                    ans += 1
            out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run("""abacaba
5
2 1 4
1 4 b
1 5 b
2 4 6
2 1 7
""") == "3\n2\n3"

# all same characters
assert run("""aaaaa
3
2 1 5
1 3 b
2 1 5
""") == "1\n2"

# single character string
assert run("""a
2
2 1 1
1 1 b
""") == "1"

# alternating updates
assert run("""abc
4
2 1 3
1 2 a
2 1 3
2 2 2
""") == "3\n2\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all a’s | 1 then 2 | repeated updates correctness |
| single char | 1 | boundary handling |
| alternating updates | multiple values | consistency under interleaving |

## Edge Cases

A dense update case occurs when the same position is repeatedly changed. For example, starting with `"aaaaa"`, updating position 3 to `'b'`, then back to `'a'`, then to `'c'` tests whether the structure avoids accumulating stale counts. The Fenwick update logic removes the previous character before inserting the new one, so each state transition maintains a clean single presence per index in exactly one tree.

A minimal range query case like querying `[1,1]` checks whether a single-character substring is correctly counted. Since each BIT represents exact positions, the range sum for a single index is either 0 or 1, and the algorithm correctly maps this to 0 or 1 distinct character.

A full-range query after multiple updates ensures that aggregation across all 26 trees remains consistent. Because each tree is independent and updated symmetrically, no character is double counted or lost.
