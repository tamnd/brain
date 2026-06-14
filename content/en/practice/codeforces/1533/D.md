---
title: "CF 1533D - String Searching"
description: "We are given a fixed collection of strings, all of the same length, and we are asked to answer many queries about a slightly longer string. Each stored string has length $m$. Each query string has length $m+1$."
date: "2026-06-14T18:34:48+07:00"
tags: ["codeforces", "competitive-programming", "*special", "hashing"]
categories: ["algorithms"]
codeforces_contest: 1533
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes: Episode 7"
rating: 0
weight: 1533
solve_time_s: 211
verified: true
draft: false
---

[CF 1533D - String Searching](https://codeforces.com/problemset/problem/1533/D)

**Rating:** -  
**Tags:** *special, hashing  
**Solve time:** 3m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed collection of strings, all of the same length, and we are asked to answer many queries about a slightly longer string.

Each stored string has length $m$. Each query string has length $m+1$. For a query string $t$, we want to count how many of the original strings $s_i$ can be turned into $t$ by inserting exactly one character somewhere in $s_i$. The inserted character can go in any position, so we are effectively checking whether removing one character from $t$ can produce $s_i$.

So each query asks: among all dictionary strings of length $m$, how many are equal to some length-$m$ subsequence obtained by deleting exactly one character from the query string.

The constraints immediately shape the solution. The number of strings and queries can both reach $10^5$, while the length of each string is at most 10. That last detail is decisive: although the input size is large, the strings are extremely short. This suggests that any solution should preprocess all strings in a way that allows constant or near-constant query time, and that exponential dependence on $m$ is acceptable since $m \le 10$.

A naive approach would compare each query against every stored string and try deleting each possible position. For each pair $(s_i, t)$, we would check whether removing one character from $t$ yields $s_i$. That costs $O(m)$ per check, and there are $nq = 10^{10}$ pairs in the worst case, which is far too large.

A more subtle issue appears if we try to “normalize” strings incorrectly. For example, if we precompute hashes of strings but forget that the deletion position varies, we may conflate different embeddings. Another pitfall is assuming we can match prefixes or suffixes only, but the inserted character can appear anywhere, so splitting strictly by prefix/suffix alone is insufficient unless we enumerate the split position.

Edge cases are simple but worth being explicit about. If all strings are identical, every query counts all matches depending on how many deletion positions match that string. If the query contains repeated letters, multiple deletion positions may produce identical resulting strings, and counting must avoid double counting via a set or hash frequency map.

## Approaches

The brute force solution iterates over every string and, for each query, tries removing each position from the query string to form a candidate string, then checks if that candidate exists in a set of input strings. Since each query has $m+1$ possible deletions and each check is $O(1)$ average using a hash set, this reduces query cost to $O(m)$. However, this ignores multiplicity across different ways of matching a single stored string, and more importantly it still requires careful counting per string, which becomes inefficient if implemented naively per pair.

The key insight is to reverse the perspective. Instead of asking whether each stored string can match a query, we precompute all “nearby superstrings” of stored strings. For every stored string $s$, we consider all possible ways of inserting one character into it. That produces a set of length $m+1$ strings, but explicitly enumerating all 26 choices per position would be too large.

Instead, we observe a cleaner symmetry: a query matches a stored string if and only if removing exactly one position from the query yields the stored string. Therefore, we can preprocess all stored strings in a hash set. Then, for each query, we generate all $m+1$ candidates obtained by deleting one character, and count how many of these candidates exist in the set.

Since $m \le 10$, each query requires only up to 11 substring checks, which is constant time. We just need to ensure duplicates are not counted twice when different deletions produce the same resulting string (which happens when the query has repeated characters). A local set per query solves this.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairwise | $O(nqm)$ | $O(n)$ | Too slow |
| Deletion Enumeration + Hash Set | $O(nm + qm)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all stored strings and insert them into a hash set.

This allows constant-time membership checks when comparing against generated candidates.
2. For each query string $t$, initialize an empty local set to track which candidate results have already been counted.

This prevents double counting when two different deletion positions produce the same string.
3. Iterate over every index $i$ in the query string from $0$ to $m$.

For each index, construct a candidate string by removing $t[i]$.

This corresponds to testing the inverse of the allowed operation.
4. If this candidate string exists in the stored set and has not been counted yet for this query, increment the answer and mark it as seen.
5. Output the final count for the query.

### Why it works

Each stored string $s_i$ can appear in the answer for a query $t$ if and only if there exists an index in $t$ whose removal yields exactly $s_i$. The algorithm explicitly enumerates all such possibilities. Because every valid match corresponds to exactly one deletion position in at least one way, and duplicates are filtered within a query, every match is counted once and only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    st = set()

    for _ in range(n):
        st.add(input().strip())

    q = int(input())
    for _ in range(q):
        t = input().strip()
        seen = set()
        ans = 0

        for i in range(m + 1):
            cand = t[:i] + t[i+1:]
            if cand in st and cand not in seen:
                seen.add(cand)
                ans += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first stores all dictionary strings in a hash set. Each query then constructs all possible length-$m$ strings formed by deleting one character. The `seen` set ensures that repeated deletions producing the same string do not inflate the answer. This is essential when the query contains repeated characters, since different deletion positions can yield identical results.

The slicing operation `t[:i] + t[i+1:]` directly implements the deletion logic, and since $m \le 10$, its cost is negligible.

## Worked Examples

### Example 1

Input:

```
2 1
a
c
4
aa
ca
mm
cf
```

For each query:

| Query | i deleted | candidate | in set | seen before | count |
| --- | --- | --- | --- | --- | --- |
| aa | 0 | a | yes | no | 1 |
| aa | 1 | a | yes | yes | 1 |
| ca | 0 | a | yes | no | 1 |
| ca | 1 | c | yes | no | 2 |
| mm | 0 | m | no | - | 0 |
| mm | 1 | m | no | - | 0 |
| cf | 0 | f | no | - | 0 |
| cf | 1 | c | yes | no | 1 |

Outputs:

```
1
2
0
1
```

This confirms that duplicate deletions do not double count the same string and that matching depends only on membership in the dictionary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm + qm)$ | building set is linear in input size, each query checks at most $m+1 \le 11$ deletions |
| Space | $O(n)$ | hash set stores all input strings |

The constraints allow up to $10^5$ strings and queries, but the small fixed string length makes this linear solution easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    old = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# provided sample
assert run("""2 1
a
c
4
aa
ca
mm
cf
""") == "1\n2\n0\n1"

# minimum case
assert run("""1 1
a
1
aa
""") == "1"

# all identical strings
assert run("""3 2
ab
ab
ab
1
aab
""") == "1"

# no matches
assert run("""2 2
ab
cd
1
xyz
""") == "0"

# repeated letters causing duplicate deletions
assert run("""1 2
ab
1
aab
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single string | 1 | basic match |
| duplicates in dictionary | 1 | handling identical entries |
| no valid matches | 0 | negative case |
| repeated letters in query | 1 | duplicate deletion handling |

## Edge Cases

A subtle case arises when the query contains repeated characters, such as `"aab"`. Deleting the first or second `'a'` produces the same candidate `"ab"`. Without a `seen` set, this would incorrectly count the same dictionary string multiple times.

For input:

```
1 2
ab
1
aab
```

The algorithm processes deletions:

First deletion gives `"ab"`, which is in the set, so count becomes 1. Second deletion gives `"ab"` again, but it is already marked in `seen`, so it is ignored. Third deletion gives `"aa"`, which is not in the set. The final answer is correctly 1.

This behavior guarantees correctness even when multiple deletion positions collapse into the same string.
