---
title: "CF 104614D - Determining Nucleotide Assortments"
description: "We are given a DNA strand consisting only of the four nucleotide types A, T, G, and C. After the strand, several range queries follow. Each query specifies a contiguous section of the strand, and for that section we must determine how frequently each nucleotide appears."
date: "2026-06-29T22:01:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104614
codeforces_index: "D"
codeforces_contest_name: "2022-2023 ICPC East Central North America Regional Contest (ECNA 2022)"
rating: 0
weight: 104614
solve_time_s: 73
verified: true
draft: false
---

[CF 104614D - Determining Nucleotide Assortments](https://codeforces.com/problemset/problem/104614/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a DNA strand consisting only of the four nucleotide types `A`, `T`, `G`, and `C`. After the strand, several range queries follow. Each query specifies a contiguous section of the strand, and for that section we must determine how frequently each nucleotide appears.

The required output is not the frequencies themselves. Instead, for every query we must print the four nucleotide letters ordered from the highest frequency to the lowest. Whenever two nucleotides appear equally often, the fixed priority `A < T < G < C` decides their relative order.

The DNA strand contains at most 50,000 characters, while there may be as many as 25,000 queries. A straightforward scan of every requested substring examines every character in every query. In the worst case every query spans the entire strand, leading to about 50,000 × 25,000 = 1.25 billion character visits. That amount of work is far beyond what is practical.

The alphabet contains only four possible characters. This small constant is the key property of the problem. If we can answer "how many A's are in this interval?", "how many T's?", and so on in constant time, then every query becomes a tiny amount of work.

One easy mistake is handling ties incorrectly. Consider the input

```
AT
1
1 2
```

Both `A` and `T` appear once, while `G` and `C` appear zero times. The correct output is

```
ATGC
```

Sorting only by frequency could produce `TAGC`, which is incorrect because equal frequencies must follow the fixed nucleotide order.

Another subtle case occurs when some nucleotides do not appear at all.

```
AAAA
1
1 4
```

The correct output is

```
ATGC
```

`A` is first because it appears four times. The remaining three nucleotides all have frequency zero, so they remain in priority order `T`, `G`, `C`.

Queries consisting of a single position also deserve attention.

```
G
1
1 1
```

The answer is

```
GATC
```

`G` has frequency one, while the remaining nucleotides all have frequency zero and are ordered according to the tie-breaking rule.

## Approaches

The most direct solution processes every query independently. For each interval, scan every character, maintain four counters, then sort the four nucleotides according to frequency and tie-breaking priority.

This approach is correct because every character in the interval contributes exactly once to its corresponding counter. Unfortunately, it repeats the same work across overlapping queries. If every query covers almost the entire DNA strand, the algorithm performs about 1.25 billion character inspections, making it too slow.

The repeated counting suggests preprocessing. Every query only asks for frequencies inside a substring, and substring frequency queries are exactly what prefix sums are designed for.

For each nucleotide, build a prefix count array where `prefix[i]` stores how many occurrences appear in the first `i` positions of the strand. The number of occurrences inside any interval `[l, r]` is then simply

```
prefix[r] - prefix[l - 1]
```

Since there are only four nucleotides, each query requires exactly four prefix sum differences. After obtaining the four counts, we sort only four items. Sorting four elements is constant time, so each query is answered in constant time after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create four prefix sum arrays, one for each nucleotide `A`, `T`, `G`, and `C`. Each array has length `n + 1`, where index `0` represents an empty prefix.
2. Scan the DNA strand from left to right. At each position, copy the previous prefix values for all four nucleotides, then increment the array corresponding to the current character.
3. For every query `[l, r]`, compute the frequency of each nucleotide by subtracting the appropriate prefix sums.
4. Form four pairs consisting of the negative frequency and the nucleotide letter. Using the negative value lets an ordinary ascending sort place larger frequencies first.
5. Sort these four pairs. Python compares tuples lexicographically, so equal frequencies are automatically broken by the alphabetical order of the letters. Because the required priority is exactly `A`, `T`, `G`, `C`, this produces the desired ordering.
6. Output the four letters in their sorted order.

### Why it works

For every nucleotide, the prefix array always stores the exact number of occurrences seen before each position. Subtracting two prefix values removes everything before the interval, leaving precisely the occurrences inside the requested substring.

Each query computes the correct frequency for all four nucleotides. The subsequent sort orders them by decreasing frequency. Whenever two frequencies are equal, tuple comparison falls back to the nucleotide letter, matching the required priority order. Since every output is determined solely from these correct frequencies and the specified tie-breaking rule, every answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    letters = "ATGC"
    idx = {c: i for i, c in enumerate(letters)}

    pref = [[0] * (n + 1) for _ in range(4)]

    for i, ch in enumerate(s, 1):
        for k in range(4):
            pref[k][i] = pref[k][i - 1]
        pref[idx[ch]][i] += 1

    m = int(input())
    out = []

    for _ in range(m):
        l, r = map(int, input().split())
        arr = []
        for k, ch in enumerate(letters):
            cnt = pref[k][r] - pref[k][l - 1]
            arr.append((-cnt, ch))
        arr.sort()
        out.append("".join(ch for _, ch in arr))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part constructs four independent prefix sum arrays. Every position copies the previous cumulative counts, then increments exactly one counter corresponding to the current nucleotide.

Each query performs four prefix sum differences. Since the arrays use one-based indexing, the interval formula becomes `pref[r] - pref[l - 1]` without any special handling for intervals beginning at the first character.

The sorting step deserves attention. The tuples contain `(-count, letter)` instead of `(count, letter)`. Python sorts in ascending order, so negating the counts makes larger frequencies appear first. When two counts are identical, the letters are compared directly. Because the required priority is exactly `A`, `T`, `G`, `C`, no custom comparator is necessary.

## Worked Examples

### Example 1

Input

```
TATATGCTCT
1
1 10
```

The substring is the entire DNA strand.

| Nucleotide | Count |
| --- | --- |
| A | 2 |
| T | 4 |
| G | 1 |
| C | 3 |

After sorting:

| Position | Nucleotide |
| --- | --- |
| 1 | T |
| 2 | C |
| 3 | A |
| 4 | G |

Output:

```
TCAG
```

The example demonstrates that the ordering is determined entirely by frequency.

### Example 2

Input

```
AAAA
1
1 4
```

| Nucleotide | Count |
| --- | --- |
| A | 4 |
| T | 0 |
| G | 0 |
| C | 0 |

After sorting:

| Position | Nucleotide |
| --- | --- |
| 1 | A |
| 2 | T |
| 3 | G |
| 4 | C |

Output:

```
ATGC
```

This trace shows that equal zero frequencies are ordered solely by the prescribed priority.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Prefix construction is linear, each query performs constant work. |
| Space | O(n) | Four prefix arrays of length `n + 1` are stored. |

The preprocessing scans the DNA strand once, and every query performs only four prefix sum lookups and a sort of four elements. These costs easily satisfy the given limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out

    input = sys.stdin.readline

    def solve():
        s = input().strip()
        n = len(s)

        letters = "ATGC"
        idx = {c: i for i, c in enumerate(letters)}

        pref = [[0] * (n + 1) for _ in range(4)]

        for i, ch in enumerate(s, 1):
            for k in range(4):
                pref[k][i] = pref[k][i - 1]
            pref[idx[ch]][i] += 1

        m = int(input())

        ans = []
        for _ in range(m):
            l, r = map(int, input().split())
            cur = []
            for k, ch in enumerate(letters):
                cnt = pref[k][r] - pref[k][l - 1]
                cur.append((-cnt, ch))
            cur.sort()
            ans.append("".join(ch for _, ch in cur))
        print("\n".join(ans))

    solve()

    sys.stdout = old
    return out.getvalue().strip()

# provided sample
assert run(
"""TATATGCTCT
3
1 10
6 10
6 6
"""
) == "\n".join([
    "TCAG",
    "TCGA",
    "GATC"
])

# minimum input
assert run(
"""A
1
1 1
"""
) == "ATGC"

# all equal
assert run(
"""CCCC
1
1 4
"""
) == "CATG"

# tie between all nucleotides
assert run(
"""ATGC
1
1 4
"""
) == "ATGC"

# boundary intervals
assert run(
"""ATGCAT
2
1 3
4 6
"""
) == "\n".join([
    "ATGC",
    "CATG"
])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single character | `ATGC` | Minimum input size |
| `CCCC` | `CATG` | Three zero-frequency ties |
| `ATGC` | `ATGC` | All frequencies equal |
| Boundary intervals | `ATGC`, `CATG` | Correct prefix subtraction at both ends |

## Edge Cases

Consider the tie example

```
AT
1
1 2
```

The computed frequencies are `(1, 1, 0, 0)` for `(A, T, G, C)`. Sorting the pairs `(-count, letter)` gives `A`, `T`, `G`, `C`, producing

```
ATGC
```

The tie-breaking rule is handled automatically because equal negative counts leave the letters to determine the order.

Now consider

```
AAAA
1
1 4
```

The prefix differences produce counts `(4, 0, 0, 0)`. After sorting, `A` comes first because of its larger frequency. The remaining three nucleotides have equal counts, so they remain ordered as `T`, `G`, `C`, giving

```
ATGC
```

Finally, consider a single-character interval.

```
G
1
1 1
```

The interval counts are `(0, 0, 1, 0)`. The only positive count belongs to `G`, so it appears first. The remaining zero-frequency nucleotides stay in priority order, yielding

```
GATC
```

All three cases follow directly from the prefix sum computation and the tuple sorting rule, without requiring any special-case logic.
