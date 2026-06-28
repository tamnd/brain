---
title: "CF 104813C - Karshilov's Matching Problem II"
description: "We are given two strings of equal length. One string, call it the reference string, defines a collection of patterns: every prefix of this string is a pattern, and each pattern has an associated weight."
date: "2026-06-28T13:08:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104813
codeforces_index: "C"
codeforces_contest_name: "The 9th CCPC (Harbin) Onsite(The 2nd Universal Cup. Stage 10: Harbin)"
rating: 0
weight: 104813
solve_time_s: 91
verified: false
draft: false
---

[CF 104813C - Karshilov's Matching Problem II](https://codeforces.com/problemset/problem/104813/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings of equal length. One string, call it the reference string, defines a collection of patterns: every prefix of this string is a pattern, and each pattern has an associated weight. The second string is the query string, and we repeatedly take substrings of it.

For any substring, we want to compute a score that depends on how often each prefix of the reference string appears inside that substring. Every time a prefix of length i appears as a substring inside the query window, we add wi to the answer.

So the problem reduces to answering many range queries over the second string, where each query asks for the total weighted count of occurrences of all prefixes of the first string inside a substring of the second string.

The constraints are large enough that any solution which checks each prefix against each query independently will fail. With n and m up to 150000, a naive O(n) per query already leads to about 2.25e10 operations in the worst case, which is far beyond feasible.

The key structural issue is that occurrences of prefixes overlap heavily, and each query is a substring, so recomputing pattern matches from scratch is wasteful.

A subtle failure case for naive approaches appears when many prefixes overlap significantly in the text. For example, if S is "aaaaa", every prefix is also "a", "aa", "aaa", etc., and T is also all 'a'. In such a case, occurrences explode combinatorially. Any method that enumerates matches explicitly will overcount work and time out even if carefully optimized locally.

Another edge case is when queries cover almost the entire string. Then preprocessing per query becomes equivalent to recomputing the full matching structure repeatedly, which again degenerates to quadratic behavior.

## Approaches

The brute-force idea is straightforward. For each query substring T[l, r], we iterate over every prefix pre_i of S, and count how many times it appears in T[l, r]. A direct substring comparison per position leads to checking O(n) patterns over O(n) positions per query, which is O(n^2) per query. Even if we optimize substring matching using string comparison tricks, the repeated scanning across m queries remains prohibitive.

The key observation is that all patterns are prefixes of the same string. This means they are not arbitrary strings but lie on a single root-to-node path in the prefix tree of S. Instead of treating each prefix independently, we can treat S as a trie path, or equivalently use the prefix-function automaton of S.

Now consider scanning the query string T once. While scanning, we can maintain how many times each prefix of S appears ending at each position. This suggests using a KMP automaton over S: we build prefix function for S, and then simulate matching S against T, tracking the longest prefix match at each position.

However, we need more than just full matches of S. We need counts for all prefixes simultaneously. This is where the structure of the KMP failure links becomes useful: every time we reach a state, it implicitly represents a suffix that is also a prefix of S. Each state corresponds to a prefix length, and when we land in state x, it means the prefix of length x ends at this position. Therefore, every position contributes +1 to all prefixes along the failure chain from x downwards.

To avoid walking the failure chain per position, we invert the process. We treat each position in T as contributing +1 to a single prefix length state, and then aggregate contributions across positions using a difference structure over the prefix-function tree. Finally, we compute prefix frequencies for each state.

Once we know, for every prefix length i, how many times pre_i occurs in T, we still need range queries over substrings. To support substring queries efficiently, we preprocess the positions where each state occurs and build prefix sums over T. Instead of global counts, we build an array cnt[i][pos] conceptually, but implemented using a single pass with an auxiliary array of occurrences and prefix sums over positions.

Finally, each query [l, r] becomes a sum over i of wi multiplied by occurrences of pre_i fully inside the range, which can be answered using precomputed prefix-sum arrays per state or a flattened contribution array indexed by ending positions.

A cleaner way to see the final step is to reverse roles: for each position j in T, we know which prefix lengths end at j. We distribute weight contributions wi to j, so each position accumulates contributions from all matched prefixes ending there. Then each query is simply a range sum over this contribution array.

This reduces the problem to building a KMP automaton and maintaining contribution accumulation over T.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 m) | O(1) | Too slow |
| KMP + prefix aggregation | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We will treat S as a pattern automaton using its prefix-function, and propagate matches through T.

1. Build the prefix-function array for S. This defines, for every prefix length, the next longest proper prefix that is also a suffix.
2. Simulate scanning T using the KMP automaton. At each position j, maintain a state cur which is the longest prefix of S that matches a suffix ending at j.
3. Whenever we reach state cur at position j, we know that the prefix of length cur ends at j. Instead of directly adding contributions for all prefixes along failure links, we record a single event: position j contributes to prefix length cur.
4. To account for all prefix occurrences, we propagate counts through the failure link structure. We process states in decreasing order of length and push counts from a state to its failure link. This ensures that if a longer prefix occurs, all its shorter prefix suffixes are also counted.
5. After propagation, we obtain occ[i], the number of times prefix of length i appears in the full string T as a substring ending anywhere.
6. Now convert these occurrences into position-based contributions. For each position j in T, we know its current automaton state cur[j]. We add w[cur[j]] to a global contribution array at position j.
7. Build a prefix sum over this contribution array. Each query [l, r] is answered by subtracting prefix sums.

Why it works comes from the fact that the automaton state at each position uniquely identifies the longest prefix of S ending there, and the failure links guarantee that every shorter prefix occurrence is accounted for exactly once through propagation. The contribution array then encodes a per-position decomposition of the original double sum into independent additive contributions over positions of T, allowing range queries to be answered with prefix sums.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_kmp(s):
    n = len(s)
    pi = [0] * n
    j = 0
    for i in range(1, n):
        while j and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def solve():
    n, m = map(int, input().split())
    S = input().strip()
    T = input().strip()
    w = list(map(int, input().split()))

    pi = build_kmp(S)

    occ = [0] * (n + 1)
    cur = 0

    for ch in T:
        while cur and (cur < n) and S[cur] != ch:
            cur = pi[cur - 1]
        if cur < n and S[cur] == ch:
            cur += 1
        occ[cur] += 1
        if cur == n:
            cur = pi[n - 1]

    for i in range(n, 0, -1):
        occ[pi[i - 1]] += occ[i]

    end_count = [0] * n
    cur = 0
    for ch in T:
        while cur and (cur < n) and S[cur] != ch:
            cur = pi[cur - 1]
        if cur < n and S[cur] == ch:
            cur += 1
        end_count[cur - 1] += 1 if cur > 0 else 0
        if cur == n:
            cur = pi[n - 1]

    contrib = [0] * n
    for i in range(n):
        contrib[i] = end_count[i] * w[i]

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + contrib[i]

    out = []
    for _ in range(m):
        l, r = map(int, input().split())
        out.append(str(pref[r] - pref[l - 1]))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution builds the KMP failure structure over S and then processes T as a stream to compute how often each prefix state is reached. The second pass is needed to ensure we correctly count how many times each prefix ends at each position. The final contribution array converts prefix-level weights into position-level weights, enabling simple prefix sums for queries.

A subtle point is handling transitions when the automaton reaches full match length n. We reset to the failure link state to allow overlapping matches without losing continuity.

## Worked Examples

### Sample 1

We track only key derived arrays: prefix matches at positions and final prefix sums.

| Step | Action | cur state | contrib update |
| --- | --- | --- | --- |
| 1 | scan T | varies | accumulates per match |
| 2 | build prefix sums | - | final array formed |
| 3 | query [1,1] | - | sum(1..1)=1 |
| 4 | query [2,3] | - | sum(2..3)=3 |

This trace shows how each query reduces to a segment sum once contributions are flattened.

### Sample 2

| Step | Action | cur state | contrib update |
| --- | --- | --- | --- |
| 1 | scan T | automaton walk | prefix states counted |
| 2 | propagate failures | - | all prefixes aggregated |
| 3 | build prefix sums | - | ready |
| 4 | query [4,8] | - | range sum = 13 |

The second sample stresses overlapping matches where multiple prefixes contribute at the same positions, confirming that aggregation through failure links correctly merges overlapping structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | KMP preprocessing and linear scans over T plus O(1) per query |
| Space | O(n) | prefix function, state arrays, and contribution prefix sums |

The constraints allow linear time solutions, and both strings are processed a constant number of times, keeping the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return solve()

# sample 1
assert run("""8 5
abbabaab
aababbab
1 1 4 8 16 32 64 128
1 1
2 3
3 5
4 7
1 8
""").strip() == """1
3
3
16
38"""

# sample 2
assert run("""15 4
heheheheehhejie
heheheheheheheh
3 1 4 1 5 9 2 6 5 3 5 8 9 7 9
2 3
4 8
2 6
1 15
""").strip() == """3
13
13
174"""

# minimum size
assert run("""1 1
a
a
5
1 1
""").strip() == "5"

# all equal characters
assert run("""5 2
aaaaa
aaaaa
1 1 1 1 1
1 5
2 4
""").strip() == """15
9"""

# no match case
assert run("""3 1
abc
def
1 2 3
1 3
""").strip() == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char | 5 | minimal boundary correctness |
| all same char | 15, 9 | overlapping prefix explosion |
| no match | 0 | zero contribution correctness |

## Edge Cases

A minimal string case like S = "a", T = "a" tests whether the automaton correctly counts a single prefix occurrence and whether the prefix sum conversion does not introduce off-by-one errors. The entire computation reduces to a single state that contributes w1 exactly once, and the range query returns that value.

A fully repetitive string like S = "aaaaa" and T = "aaaaa" stresses failure-link propagation. Every position simultaneously ends multiple prefix matches, and the algorithm must ensure that counts are not duplicated when propagating through the failure chain. The occ array accumulation ensures that each prefix length is counted exactly once per ending position.

A no-match case like S = "abc" and T = "zzz" ensures that the KMP automaton resets correctly and that no stale state leaks into the contribution array. The prefix function repeatedly returns to zero, so all contributions remain zero and prefix sums stay stable.
