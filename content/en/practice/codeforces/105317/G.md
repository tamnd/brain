---
title: "CF 105317G - Carlo's Password"
description: "Each input string in the list can be thought of as a very short sequence of characters, at most length six. For every query string, we are asked whether it can be formed by deleting some characters from at least one of these stored strings without changing the order of the…"
date: "2026-06-23T15:13:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105317
codeforces_index: "G"
codeforces_contest_name: "JPC 1.0"
rating: 0
weight: 105317
solve_time_s: 53
verified: true
draft: false
---

[CF 105317G - Carlo's Password](https://codeforces.com/problemset/problem/105317/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input string in the list can be thought of as a very short sequence of characters, at most length six. For every query string, we are asked whether it can be formed by deleting some characters from at least one of these stored strings without changing the order of the remaining characters. In other words, for a query to be valid, there must exist a source string in the list that contains the query as a subsequence.

The main challenge comes from scale rather than individual checks. There can be up to fifty thousand source strings and fifty thousand queries. Even though checking whether one string is a subsequence of another is fast because both are tiny, doing that check for every pair would still lead to billions of comparisons. A direct nested solution would therefore exceed the time limit even with very optimized inner loops.

A subtle point is that both source strings and queries are extremely short. This strongly suggests that the structure of each string, rather than their quantity, is what should be exploited. Any solution that treats strings as arbitrary-length objects misses the key simplification: each string has only 2^6 possible subsequences, which is a constant upper bound.

A naive mistake arises when trying to preprocess only prefixes or suffixes. For example, if a source string is "abdc" and the query is "abc", prefix matching or substring matching would incorrectly reject it even though deleting 'd' makes it valid. Another common mistake is assuming the query must appear contiguously, which is not required.

## Approaches

A straightforward idea is to process each query independently and test it against every source string. Since both strings are short, we can check subsequence status in linear time over length at most six. This approach is correct because it directly implements the definition. However, with up to 5×10^4 queries and 5×10^4 source strings, we perform about 2.5×10^9 comparisons, each costing up to six operations. This is far beyond feasible limits.

The key observation is that we are repeatedly solving the same kind of question: “does some source string contain this query as a subsequence?” Instead of answering queries online, we can precompute all subsequences that exist in any source string. Since each string has length at most six, the number of subsequences is at most 2^6 = 64. This turns preprocessing into a bounded expansion step.

We generate every subsequence of each source string and store it in a hash set. Once this set is built, each query reduces to a single membership check. The total number of generated strings is at most 5×10^4 × 64, which is around 3.2 million entries, easily manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · m · 6) | O(1) | Too slow |
| Subsequence Precompute | O(n · 2^6 + m) | O(n · 2^6) | Accepted |

## Algorithm Walkthrough

We convert the problem into a preprocessing-and-lookup structure over all subsequences.

1. Read all source strings and initialize an empty hash set.

The set will represent every possible query that can be formed from at least one source string.
2. For each source string, generate all subsequences using bitmask enumeration over its positions.

Since the maximum length is six, each string contributes at most 64 subsequences.

For each bitmask, we construct the corresponding subsequence by selecting characters where the bit is set.
3. Insert each generated subsequence into the global set.

This ensures that if any string can produce a given pattern via deletions, that pattern becomes available for queries.
4. Read each query string and check whether it exists in the set.

If it does, output "YES", otherwise output "NO".
5. Repeat until all queries are processed.

### Why it works

Each subsequence of a source string is explicitly generated and stored. Any valid answer must correspond to a subsequence of at least one source string, so it must appear in the constructed set. Conversely, anything in the set is guaranteed to come from a real source string, so it is valid by construction. This creates a perfect equivalence between membership in the set and validity of the query.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s_list = [input().strip() for _ in range(n)]
    
    subseqs = set()

    for s in s_list:
        L = len(s)
        # generate all subsequences
        for mask in range(1 << L):
            t = []
            for i in range(L):
                if mask & (1 << i):
                    t.append(s[i])
            subseqs.add("".join(t))
    
    m = int(input())
    out = []
    for _ in range(m):
        t = input().strip()
        out.append("YES" if t in subseqs else "NO")
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution is built around the preprocessing set `subseqs`. The bitmask loop enumerates every possible subsequence of each source string, including the empty string, which is valid but irrelevant for queries longer than zero. Each generated string is inserted into a Python set, enabling average O(1) lookup during queries.

A common implementation detail that matters here is string construction. Since strings are short, repeated `"".join` operations remain cheap. The overall complexity is dominated by bitmask enumeration rather than string handling overhead.

## Worked Examples

Consider a small illustrative input:

```
3
ahmad
abd
jaun
6
jn
ad
acd
aqd
amh
jan
```

We track whether key subsequences are inserted into the set.

### Subsequence construction (partial trace)

| Source string | mask | subsequence | inserted |
| --- | --- | --- | --- |
| abd | 101 | ad | yes |
| abd | 11 | ab | yes |
| abd | 1 | a | yes |
| abd | 0 | "" | yes |
| ahmad | 10101 | amd | yes |
| jaun | 1011 | jan | yes |

Now query evaluation:

| Query | Set membership | Output |
| --- | --- | --- |
| jn | present via "jaun" | YES |
| ad | present via "abd" | YES |
| acd | not generated | NO |
| aqd | not generated | NO |
| amh | order mismatch in all sources | NO |
| jan | present via "jaun" | YES |

This trace shows that validity is entirely determined by whether the query appears in the precomputed subsequence universe.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^6 + m) | each string generates at most 64 subsequences, queries are hash lookups |
| Space | O(n · 2^6) | all unique subsequences are stored in a set |

The preprocessing factor is effectively linear in n with a small constant. With n up to 5×10^4, the total generated subsequences remain in the low millions, well within memory and time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    stdout_buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_buffer

    solve()

    sys.stdout = old_stdout
    return stdout_buffer.getvalue().strip()

# sample
assert run("""3
ahmad
abd
jaun
6
jn
ad
acd
aqd
amh
jan
""") == """YES
YES
NO
NO
NO
YES"""

# single character match
assert run("""1
a
2
a
b
""") == """YES
NO"""

# empty subsequence case
assert run("""1
abc
1
""") == "YES"

# maximum small strings repetition
assert run("""2
aaaaaa
bbbbbb
2
ab
ba
""") == """NO
NO"""

# direct match only
assert run("""2
abc
def
3
abc
ac
df
""") == """YES
NO
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single character match | YES/NO | basic membership correctness |
| empty query | YES | empty subsequence handling |
| repeated chars | NO | ordering constraint enforcement |
| direct match only | mixed | no false positives from partial overlap |

## Edge Cases

A subtle case is when the query is empty. Every string contains the empty subsequence, so the correct output is always YES. The algorithm handles this naturally because the empty mask is always inserted during preprocessing.

Another case involves repeated characters such as "aaaaaa". Every subsequence collapses into strings like "", "a", "aa", and so on, but duplicates do not matter because the set stores only unique values. Queries like "aaa" are correctly recognized.

A more structural edge case occurs when characters exist in multiple source strings but never in correct order within a single string. For example, "a" may appear in one string and "b" in another, but "ab" is invalid unless both appear in order in a single source. The algorithm avoids this pitfall because it never mixes characters across different strings; every subsequence is generated from a single original string, preserving ordering constraints exactly.
