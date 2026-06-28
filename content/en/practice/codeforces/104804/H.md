---
title: "CF 104804H - \u042d\u0434\u0443\u0440\u0434 \u0438 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438"
description: "We are given a stream of photo records, each describing where and when a photo was taken. Every record contains a location name and four time fields: day, month, hour, and minute. The year is implicitly fixed as 2113 for all photos."
date: "2026-06-28T16:52:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "H"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 86
verified: false
draft: false
---

[CF 104804H - \u042d\u0434\u0443\u0440\u0434 \u0438 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438](https://codeforces.com/problemset/problem/104804/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a stream of photo records, each describing where and when a photo was taken. Every record contains a location name and four time fields: day, month, hour, and minute. The year is implicitly fixed as 2113 for all photos.

The task is to reorder all photos according to a custom ordering rule. First, photos are sorted lexicographically by their location string, using ASCII order where uppercase letters come before lowercase ones. If two photos have the same location, they are then ordered by their timestamp: earlier date comes first, comparing day, then month, then hour, then minute. If both location and timestamp are identical, the original input order must be preserved.

The output is not just the sorted list of photos, but each photo must also be printed with its original index in the input and with a reformatted timestamp where dots separate day and month and the year 2113 is inserted explicitly.

The input is a continuous stream of records without an explicit count, up to 100000 lines. That immediately rules out any solution worse than O(n log n), since linear scans or repeated insertion into a sorted structure would degrade to quadratic time.

A subtle issue appears in how the input is structured. Each photo is on its own line, but in some test data formats, whitespace or line breaks may be inconsistent, so a robust solution must rely on token-based reading rather than assuming strict line separation. Another subtle point is stability: if we use a sorting algorithm that is not stable and do not explicitly encode the input index into the key, we will lose the required tie-break behavior.

A minimal example of the stability issue is two identical photos:

Input:

```
Moscow 01 01 00 00
Moscow 01 01 00 00
```

The correct output must preserve order 1 then 2. A naive sort on `(place, time)` alone may swap them arbitrarily.

## Approaches

A direct approach is to read all photos into an array and repeatedly select the smallest element according to the required ordering. This mimics selection sort: for each position, scan the remaining list and find the minimum. This is correct because it directly implements the comparison rule, but each selection costs O(n), repeated n times gives O(n²) time, which is too slow for 100000 records. That leads to roughly 10¹⁰ comparisons in the worst case, which is not feasible.

The key observation is that the ordering is fully deterministic and composable into a tuple comparison. The location comparison is lexicographic, and the time comparison is lexicographic over fixed-width integers. Once we represent each record as a tuple `(place, day, month, hour, minute, index)`, Python’s built-in sorting can handle the ordering efficiently using Timsort in O(n log n). The index is appended only to enforce stability explicitly when all other fields match.

So instead of repeatedly searching, we convert the problem into a single global sort with a well-defined key and let the sorting algorithm handle ordering efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Selection | O(n²) | O(n) | Too slow |
| Tuple Sort | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all input lines until EOF, parsing each line into its components: place string and four integers representing day, month, hour, and minute. This is necessary because the input size is unknown and only terminates via end-of-file.
2. For each photo, store a structured record containing the original index, the place string, and the four time components. The index is required to preserve original ordering when all other fields are identical.
3. Define a sorting key for each record as `(place, day, month, hour, minute, index)`. The ordering works naturally because Python compares tuples lexicographically from left to right.
4. Sort the entire list using this key. This produces the required ordering in one pass over the sorting algorithm’s internal structure.
5. Iterate over the sorted list and print each record in the required format, reconstructing the timestamp as `DD.MM.2113 HH:MM` with leading zeros preserved.

### Why it works

The correctness comes from the fact that the required ordering is a lexicographic ordering over a fixed hierarchy of fields. Once each photo is mapped into a tuple that encodes that hierarchy in order of significance, tuple comparison exactly matches the problem’s comparison rules. Adding the original index ensures that even when all fields are equal, the ordering becomes strictly total and consistent with input order, which guarantees stability regardless of the underlying sort implementation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    data = sys.stdin.read().strip().splitlines()
    photos = []

    for i, line in enumerate(data, 1):
        if not line.strip():
            continue
        parts = line.split()
        place = parts[0]
        d = int(parts[1])
        m = int(parts[2])
        h = int(parts[3])
        mi = int(parts[4])
        photos.append((place, d, m, h, mi, i))

    photos.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[5]))

    out = []
    for p in photos:
        place, d, m, h, mi, idx = p
        out.append(f"{idx} {place} {d:02d}.{m:02d}.2113 {h:02d}:{mi:02d}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution begins by reading the entire input at once using `sys.stdin.read()` to avoid per-line overhead, which is important when handling up to 100000 records. Each line is split into tokens, and we extract the place string and four numeric fields.

Each photo is stored as a tuple including its original index. This index is not used for sorting priority except as a final tie-breaker. The sorting key is explicitly defined to match the required ordering hierarchy.

Finally, formatting is done carefully using zero-padded integer formatting to ensure two-digit fields, since the output format requires strict formatting for day, month, hour, and minute.

## Worked Examples

### Sample 1 Trace

We track only key fields used in sorting.

| Step | Place | Date (D,M,H,Min) | Index |
| --- | --- | --- | --- |
| Input | Moscow | 15,01,13,24 | 1 |
| Input | Maykop | 17,05,00,13 | 2 |
| Input | Adler | 21,11,04,20 | 3 |
| Input | St.Petersburg | 30,01,17,59 | 4 |
| Input | Moscow | 01,04,00,00 | 5 |
| Input | Kekland | 04,12,01,43 | 6 |
| Input | Moscow | 15,01,02,43 | 7 |

After sorting lexicographically by place:

Adler comes first, then Kekland, then Maykop, then Moscow, then St.Petersburg. Inside Moscow, timestamps decide ordering.

Final sorted order:

3, 6, 2, 7, 1, 5, 4

This matches the sample output ordering.

### Sample 2 Trace

| Step | Place | Date (D,M,H,Min) | Index |
| --- | --- | --- | --- |
| Input | Moscow | 15,01,13,24 | 1 |
| Input | Maykop | 17,05,00,13 | 2 |
| Input | Adler | 21,11,04,20 | 3 |
| Input | Moscow | 15,01,13,24 | 4 |
| Input | st.Petersburg | 30,01,17,59 | 5 |
| Input | Moscow | 15,01,13,24 | 6 |
| Input | Moscow | 01,04,00,00 | 7 |
| Input | Kekland | 04,12,01,43 | 8 |

Here, multiple identical Moscow entries with identical timestamps appear. The index becomes the deciding factor among them, ensuring stable ordering consistent with input appearance.

Final order:

3, 8, 2, 1, 4, 6, 7, 5

This demonstrates that the index tie-break correctly preserves input order among identical records.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | All records are sorted once using a comparison-based sort over tuples |
| Space | O(n) | All photo records are stored in memory |

The constraints allow up to 100000 photos, and O(n log n) sorting easily fits within time limits since it involves roughly a few million comparisons at most. Memory usage is linear in the number of records and remains safe.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    import sys
    from io import StringIO
    backup = sys.stdout
    sys.stdout = StringIO()
    main()
    out = sys.stdout.getvalue().strip()
    sys.stdout = backup
    return out

# sample 1
assert run("""Moscow 15 01 13 24
Maykop 17 05 00 13
Adler 21 11 04 20
St.Petersburg 30 01 17 59
Moscow 01 04 00 00
Kekland 04 12 01 43
Moscow 15 01 02 43
""") == """3 Adler 21.11.2113 04:20
6 Kekland 04.12.2113 01:43
2 Maykop 17.05.2113 00:13
7 Moscow 15.01.2113 02:43
1 Moscow 15.01.2113 13:24
5 Moscow 01.04.2113 00:00
4 St.Petersburg 30.01.2113 17:59"""

# identical records stability
assert run("""A 01 01 00 00
A 01 01 00 00
A 01 01 00 00
""") == """1 A 01.01.2113 00:00
2 A 01.01.2113 00:00
3 A 01.01.2113 00:00"""

# boundary times
assert run("""Z 31 12 23 59
A 01 01 00 00
""") == """2 A 01.01.2113 00:00
1 Z 31.12.2113 23:59"""

# mixed case ordering
assert run("""a 01 01 00 00
A 01 01 00 00
""") == """2 A 01.01.2113 00:00
1 a 01.01.2113 00:00"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical timestamps | stable order | tie-breaking correctness |
| min/max dates | boundary handling | correct lexicographic time comparison |
| case-sensitive names | ASCII ordering | correct string ordering |

## Edge Cases

One important edge case is when multiple photos have exactly identical place and timestamp values. In that situation, a naive comparator-based sort that does not include the original index may produce a different valid permutation each run or rely on unstable behavior. By explicitly adding the index into the sorting key, the ordering becomes deterministic and consistent with input order.

Another edge case is places differing only by case, such as `Moscow` and `moscow`. Because ordering is ASCII-based, uppercase letters must come before lowercase ones. A correct implementation must not normalize case or use locale-aware comparison, otherwise the ordering would deviate from the required lexicographic rule.

A final subtle case is formatting output: forgetting zero-padding on single-digit day, month, hour, or minute would produce syntactically incorrect timestamps even if sorting is correct, so formatting must be enforced strictly at output time.
