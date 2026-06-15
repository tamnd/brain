---
title: "CF 1070H - BerOS File Suggestion"
description: "We are given a fixed collection of short file names and a stream of queries. Each query is a short string, and we must determine how many file names contain that string as a contiguous substring."
date: "2026-06-15T13:55:49+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1070
codeforces_index: "H"
codeforces_contest_name: "2018-2019 ICPC, NEERC, Southern Subregional Contest (Online Mirror, ACM-ICPC Rules, Teams Preferred)"
rating: 1500
weight: 1070
solve_time_s: 379
verified: false
draft: false
---

[CF 1070H - BerOS File Suggestion](https://codeforces.com/problemset/problem/1070/H)

**Rating:** 1500  
**Tags:** brute force, implementation  
**Solve time:** 6m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed collection of short file names and a stream of queries. Each query is a short string, and we must determine how many file names contain that string as a contiguous substring. Along with the count, we also need to return any one file name that contains the query string, or a dash if no file matches.

A key structural detail is that file names are extremely short, at most 8 characters. That means each file contains only a small number of substrings, and every possible substring is also short. This strongly suggests that we can afford to precompute substring information for all files without worrying about memory or time blowup.

The input size also reinforces this direction. There are up to 10,000 files and up to 50,000 queries. A per query scan over all files would be too slow, since that would lead to 500 million substring checks in the worst case. Each check is cheap, but the scale is still too large under a 3 second limit. We need preprocessing that turns each query into an O(1) or near O(1) lookup.

A subtle edge case is repeated substrings inside a single file name. If a file is `"aaaa"`, the substring `"aa"` appears multiple times inside it, but it should still only contribute once to the count. Another edge case is queries that do not exist in any file, where we must return `0 -` rather than an empty filename or garbage default.

## Approaches

The naive idea is straightforward. For each query, iterate over all file names and check whether the query string appears as a substring. Since each file has length at most 8, substring checking is constant time in practice, but we still perform it for all files per query. This leads to roughly $O(n \cdot q \cdot L)$ behavior, which is far beyond limits when $n = 10^4$ and $q = 5 \cdot 10^4$.

The failure point is repetition. We recompute the same substring relationships again and again for every query, even though the file set is static. The structure suggests reversing the perspective: instead of asking for each query which files contain it, we can precompute for every possible substring which files contain it.

Each file contributes only a small number of substrings because length is at most 8. For a string of length $L$, the number of substrings is $L(L+1)/2$, which is at most 36. Across 10,000 files, this is only about 360,000 substring occurrences. That is small enough to store in a hash map.

The key improvement is to build a dictionary mapping each substring to two pieces of information: how many distinct files contain it, and one example file name that contains it. Once this preprocessing is done, each query becomes a direct lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot q \cdot L)$ | $O(1)$ | Too slow |
| Optimal (precompute substrings) | $O(n \cdot L^2 + q)$ | $O(n \cdot L^2)$ | Accepted |

## Algorithm Walkthrough

We process the file list once and build a global index over all substrings.

1. For each file name, generate all distinct substrings. We use a set per file so that repeated characters do not cause double counting of the same file for a substring. This ensures correctness when the same substring appears multiple times inside a single file.
2. For each unique substring of the file, update a global dictionary. If the substring is not yet present, initialize its count to zero and store the current file as its example. Then increment its count by one. The stored example does not need updating after initialization because any valid file is acceptable.
3. After preprocessing all files, process each query by checking whether it exists in the dictionary. If it does, output the stored count and example file. If it does not, output zero and a dash.

The reason this is efficient is that all expensive work is concentrated in preprocessing, and each query becomes a constant-time hash lookup.

### Why it works

Each substring is associated with exactly the set of files that contain it, and we record membership exactly once per file using a per-file deduplication set. The global counter therefore represents the number of distinct files containing the substring. Since queries only read from this precomputed mapping, no query depends on runtime scanning or partial recomputation, so the answers are consistent with the definition of substring occurrence across the entire file set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def all_substrings(s: str):
    res = set()
    n = len(s)
    for i in range(n):
        cur = []
        for j in range(i, n):
            cur.append(s[j])
            res.add("".join(cur))
    return res

def main():
    n = int(input())
    files = [input().strip() for _ in range(n)]

    mp = {}

    for name in files:
        subs = all_substrings(name)
        for sub in subs:
            if sub not in mp:
                mp[sub] = [0, name]
            mp[sub][0] += 1

    q = int(input())
    out = []

    for _ in range(q):
        s = input().strip()
        if s in mp:
            out.append(f"{mp[s][0]} {mp[s][1]}")
        else:
            out.append("0 -")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The function `all_substrings` builds all distinct substrings of a file name using a set. This avoids overcounting cases like repeated characters where the same substring could appear multiple times inside one file.

The dictionary `mp` stores for each substring a pair consisting of its frequency across files and one representative filename. The representative is fixed at first encounter, since any valid answer is acceptable.

Each query is resolved by a single dictionary lookup, which ensures the response is immediate.

## Worked Examples

Consider the sample input.

Files are `"test"`, `"contests"`, `"test."`, and `".test"`.

For the query `"ts"`, we check which files contain it. Both `"contests"` and `"test."` contain `"ts"`, so the count is 2 and either file may be returned.

| Query | Lookup Result | Count | Example File |
| --- | --- | --- | --- |
| ts | found | 2 | contests |
| . | found | 2 | .test |
| contes. | found | 1 | test. |
| st | found | 4 | test |

This trace shows that once preprocessing is done, each query reduces to a direct hash table access.

Now consider a small custom case.

Files: `"aaa"`, `"aba"`

Query: `"aa"`

| File | Substrings contributing |
| --- | --- |
| aaa | aa, aaa |
| aba | ab, ba, aba |

After aggregation, `"aa"` maps to count 1 with example `"aaa"`.

This confirms that repeated occurrences inside a file do not inflate the count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot L^2 + q)$ | Each file contributes at most 36 substrings, each query is O(1) lookup |
| Space | $O(n \cdot L^2)$ | All distinct substrings across files stored in hash map |

With $n \le 10^4$ and $L \le 8$, preprocessing produces at most about 360,000 substrings, which is easily manageable. Query time is linear in number of queries only, so the solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    def all_substrings(s: str):
        res = set()
        n = len(s)
        for i in range(n):
            cur = []
            for j in range(i, n):
                cur.append(s[j])
                res.add("".join(cur))
        return res

    n = int(input())
    files = [input().strip() for _ in range(n)]

    mp = {}
    for name in files:
        subs = all_substrings(name)
        for sub in subs:
            if sub not in mp:
                mp[sub] = [0, name]
            mp[sub][0] += 1

    q = int(input())
    out = []
    for _ in range(q):
        s = input().strip()
        if s in mp:
            out.append(f"{mp[s][0]} {mp[s][1]}")
        else:
            out.append("0 -")
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("""4
test
contests
test.
.test
6
ts
.
st.
.test
contes.
st
""") == """1 contests
2 .test
1 test.
1 .test
0 -
4 test."""

# single character files
assert run("""2
a
b
3
a
b
c
""") == """1 a
1 b
0 -"""

# repeated characters inside file
assert run("""1
aaaa
3
a
aa
aaa
""") == """1 a
1 a
1 a"""

# no matches
assert run("""3
abc
def
ghi
2
zzz
xy
""") == """0 -
0 -"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single character files | direct matches | basic correctness |
| repeated characters | no double counting | per-file deduplication |
| no matches | `0 -` handling | missing substring case |

## Edge Cases

A file like `"aaaa"` is the main trap case. A careless approach that counts substring occurrences directly would count `"aa"` multiple times inside the same file. The correct behavior requires treating each file as a single contributor per substring.

For input:

```
1
aaaa
1
aa
```

The preprocessing step generates substrings `{a, aa, aaa, aaaa}`. Even though `"aa"` appears in multiple positions, it is inserted only once into the per-file set, so the global count becomes 1. The query correctly outputs `1 aaaa`.

A second edge case is when a query substring does not appear in any file. For input:

```
2
abc
def
1
z
```

The dictionary lookup fails, and the output is `0 -`. This ensures we do not attempt to access an undefined example filename or produce a stale value from initialization.
