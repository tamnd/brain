---
title: "CF 104295D - \u0421\u0435\u043c\u044c\u044f \u041c\u044e\u043c\u043b\u044b"
description: "We are given a fixed collection of existing family names, each written as a string of lowercase letters and hyphens. Then we are given several candidate names for a newborn. For each candidate, we must decide whether it is acceptable. A candidate is rejected in two situations."
date: "2026-07-01T20:19:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104295
codeforces_index: "D"
codeforces_contest_name: "vkoshp.letovo"
rating: 0
weight: 104295
solve_time_s: 51
verified: true
draft: false
---

[CF 104295D - \u0421\u0435\u043c\u044c\u044f \u041c\u044e\u043c\u043b\u044b](https://codeforces.com/problemset/problem/104295/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed collection of existing family names, each written as a string of lowercase letters and hyphens. Then we are given several candidate names for a newborn. For each candidate, we must decide whether it is acceptable.

A candidate is rejected in two situations. First, if it is already present among the existing names, it cannot be reused. Second, even if it is new, it is still invalid if it “ends like” any existing name, in the sense described by the statement: we look at suffix structure where matching ignores an arbitrary prefix but respects the internal structure of hyphen-separated parts. In practice, this reduces to checking whether one name can be seen as a suffix pattern of another name when aligned on hyphens, meaning that the ending sequence of segments matches exactly.

A useful way to rephrase the condition is that we care about suffixes at the character level, but with the constraint that hyphens are part of the structure. So two names are considered matching at the end if we can strip some prefix (possibly empty) from both strings in a way consistent with the definition, leaving identical remaining strings.

The constraints are large: up to 10,000 existing names and 10,000 queries, each up to length 50. A naive comparison of every query against every stored name with full string checks would require up to 100 million comparisons, each up to 50 characters, which is still borderline but becomes risky if we do repeated substring operations or rebuild strings per check. More importantly, naive suffix matching per pair could devolve into repeated scanning.

The key structural issue is that we are not comparing arbitrary substrings, but checking membership of full strings and their suffixes. This strongly suggests a preprocessing structure like a hash set for full strings and another set for all suffixes that correspond to valid “family endings”.

A subtle edge case arises when a candidate equals an existing name exactly. That must be immediately rejected even though it also matches its own suffix condition. Another edge case is when two names share the same suffix but differ in prefix, for example “anna-katerina-mymla” and “mymla”. A candidate equal to “mymla” is invalid, and any longer name ending in “mymla” is also invalid.

Finally, names are relatively short (≤ 50), so generating all suffixes per name is feasible, but we must ensure we generate them in a controlled way rather than repeatedly slicing strings inside nested loops.

## Approaches

The brute-force approach is straightforward. For each query name, we compare it with every existing name. We first check equality, then check whether the query matches the suffix condition against that existing name. A direct suffix check requires scanning from the end of both strings, potentially aligning after a delimiter-consistent cut. Each comparison costs O(L) where L ≤ 50, so the total cost becomes O(nqL), which in worst case is 10,000 × 10,000 × 50, far too large.

The key observation is that suffix invalidity depends only on whether the query appears as a valid suffix pattern of any existing name. Instead of recomputing this for every query, we can preprocess all suffixes of existing names and store them in a hash set. Then each query reduces to two constant-time checks: full membership in the existing set, and membership in the suffix set.

We generate suffixes by iterating over each position in a name and taking the substring starting there. Because names are short, at most 50 suffixes per name exist, so total preprocessing is about 500,000 substrings, well within limits.

This transforms the problem into a membership query problem over two sets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nqL) | O(1) | Too slow |
| Optimal (hash sets of names and suffixes) | O((n + q)L) | O(nL) | Accepted |

## Algorithm Walkthrough

We maintain two hash sets, one for all existing names and one for all suffixes derived from them.

1. Read all existing names and insert each full name into a set called `names`. This allows constant-time equality checks for rejection.
2. For each existing name, generate all suffixes by taking substrings starting from every index to the end, and insert each suffix into a second set called `suffixes`. This captures every possible ending pattern that should invalidate a candidate.
3. For each query name, first check whether it exists in `names`. If it does, output “Bad” immediately because duplication is forbidden.
4. Otherwise, check whether the query exists in `suffixes`. If it does, output “Bad” because it matches the ending pattern of an existing family member.
5. If neither condition holds, output “Good”.

The order matters: equality must be checked first, since equality also implies suffix membership but represents a stronger invalid condition.

### Why it works

The suffix set contains exactly all strings that can appear as a valid ending of some existing name. Any invalid candidate must either be identical to an existing name or appear as one of these suffixes. Because suffix generation enumerates all possible tail substrings, no invalid pattern is missed. Conversely, any string in the suffix set corresponds to an actual suffix of some existing name, so marking it invalid is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    names = set()
    suffixes = set()

    for _ in range(n):
        s = input().strip()
        names.add(s)
        L = len(s)
        for i in range(L):
            suffixes.add(s[i:])

    q = int(input())
    out = []

    for _ in range(q):
        t = input().strip()
        if t in names:
            out.append("Bad")
        elif t in suffixes:
            out.append("Bad")
        else:
            out.append("Good")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution uses two sets to separate exact matches from suffix-based invalidation. The suffix generation loop is the only preprocessing-heavy part, but it remains linear in total string length across all inputs. Each query is reduced to two hash lookups.

A subtle point is that we store raw suffix strings directly. Because the maximum string length is 50, slicing cost is bounded and does not affect asymptotic performance.

## Worked Examples

Consider a small input:

```
3
anna-katerina-mymla
mymla
snus-mumrik
3
mymla
anna-mymla
katerina-mymla
```

We build:

| Name | Inserted into names | Suffixes generated |
| --- | --- | --- |
| anna-katerina-mymla | yes | katerina-mymla, mymla, ... |
| mymla | yes | mymla, ... |
| snus-mumrik | yes | mumrik, ... |

Now queries:

| Query | In names | In suffixes | Result |
| --- | --- | --- | --- |
| mymla | yes | yes | Bad |
| anna-mymla | no | no | Good |
| katerina-mymla | no | yes | Bad |

The first query is rejected due to equality. The second passes because it does not match any full suffix pattern. The third is rejected because it matches a suffix of the first name.

This demonstrates that suffix-based invalidation is independent of whether the query is itself a full name in the database.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nL + q) | Each name contributes O(L) suffix generation, each query is O(1) average set lookup |
| Space | O(nL) | All suffixes plus full names stored in hash sets |

The constraints allow up to 10,000 names with length up to 50, so storing about 500,000 suffix strings is acceptable. The solution fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    solve()
    return sys.stdout.getvalue().strip()

# provided sample (adapted format if needed)
assert run("""3
anna-katerina-mymla
mymla
snus-mumrik
6
mymla
my
anna-mymla
katerina-mymla
anna-katerina
snu-snusmumrik
""") == """Bad
Good
Good
Bad
Good
Good"""

# minimum case
assert run("""1
a
2
a
b
""") == """Bad
Good"""

# no suffix collisions
assert run("""2
abc
def
2
x
y
""") == """Good
Good"""

# all queries invalid via suffix
assert run("""1
abcde
3
abcde
bcde
cde
""") == """Bad
Bad
Bad"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char duplication | Bad/Good | equality vs non-existence |
| disjoint names | Good/Good | no suffix matches |
| cascading suffixes | all Bad | suffix propagation |

## Edge Cases

One important case is when the query is exactly equal to an existing name. For input:

```
1
mymla-my
1
mymla-my
```

The algorithm inserts the name into `names`, then checks the query. The first condition `t in names` is true, so output is “Bad” immediately. Even though it is also in the suffix set, the early equality check correctly classifies it.

Another case is a query that is not a full name but is a suffix of multiple different names:

```
2
a-b-c
x-b-c
1
b-c
```

Both existing names generate suffix “b-c”. The suffix set contains it once, but that is sufficient. The query is not in `names`, but it is in `suffixes`, so it is rejected. This shows that duplicates across different sources do not matter because sets collapse them automatically.
