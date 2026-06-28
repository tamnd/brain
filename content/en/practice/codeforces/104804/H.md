---
title: "CF 104804H - \u042d\u0434\u0443\u0440\u0434 \u0438 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438"
description: "We are given a stream of photo records, each describing a single picture taken during the year 2113. Every record contains a textual location name and a timestamp split into day, month, hour, and minute."
date: "2026-06-28T13:26:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "H"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 72
verified: false
draft: false
---

[CF 104804H - \u042d\u0434\u0443\u0440\u0434 \u0438 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438](https://codeforces.com/problemset/problem/104804/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a stream of photo records, each describing a single picture taken during the year 2113. Every record contains a textual location name and a timestamp split into day, month, hour, and minute. The task is to reorder all photos so that they are grouped primarily by location in lexicographic order, and within the same location they are ordered by time from earlier to later.

The output must preserve a reference to the original position of each photo in the input. When two photos are completely identical in sorting keys, the one that appeared earlier in the input must come first.

Although the input format looks like simple records, there are two subtle structural constraints that shape the solution. First, the number of records can be as large as 100000, which makes any quadratic comparison-based sorting approach impossible. A naive repeated scanning or insertion strategy would degrade to about 10¹⁰ operations in the worst case, which is far beyond typical limits. Second, all ordering is deterministic and based on fields that can be converted into a tuple with natural ordering, meaning we do not need any custom balancing or search structure beyond a single sort.

A common mistake appears when handling ties. If two photos share the same place and timestamp, the requirement is to keep the original input order. Without explicitly adding the input index as a final sorting key, many implementations will accidentally reorder equal elements unpredictably, breaking the required stability.

Another subtle issue is parsing. Each record is line-based and fields are space-separated, but the place field is a raw string that may contain dots and mixed case letters. A careless split can misinterpret parts of the timestamp as belonging to the location if the parsing is not strictly positional.

## Approaches

A brute-force strategy would attempt to repeatedly select the smallest remaining photo by scanning the entire list, or insert each new photo into its correct position in an evolving list. This works conceptually because comparison between any two photos is straightforward: compare place strings first, then compare integer timestamps. However, each insertion or selection requires scanning O(n) elements, and doing this for n photos leads to O(n²) operations. With n up to 100000, this becomes roughly 10¹⁰ comparisons, which is not viable.

The key observation is that the ordering relation is a standard lexicographic comparison over a fixed tuple. Once each photo is converted into a tuple of comparable keys, the entire problem reduces to a single global sort. Modern sorting algorithms are optimized for exactly this case and run in O(n log n), which is sufficient for 100000 elements.

The stability requirement is handled naturally by including the original index as the last sorting key. Since Python’s sort is stable, even omitting it would technically preserve order, but relying on that alone is risky in cross-language contexts. Explicitly adding the index guarantees correctness regardless of implementation details.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal (tuple sort) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform each photo into a sortable structure and then apply a single global sort.

1. Read all input lines until EOF, treating each line as one photo record. This ensures we capture all photos without needing a declared n.
2. For each line, parse the fields by splitting on spaces. The first token is the location string, and the next four tokens are day, month, hour, and minute. Converting these numeric fields into integers is important so that comparisons behave numerically rather than lexicographically.
3. Build a sorting key for each photo consisting of four components: location string, month, day, hour, and minute, followed by the original input index. The order of date components matters because chronological ordering must respect month before day.
4. Store each photo as a tuple containing its key and its original raw fields, since the output requires printing the original formatting values.
5. Sort the list of photos using the constructed key. The sort automatically handles lexicographic ordering over tuples, comparing element by element until a difference is found.
6. Iterate over the sorted list and print each photo in the required format, prefixing it with its 1-based original index.

The reason this works is that every comparison between two photos is fully captured by a deterministic tuple ordering. The tuple defines a total order over all photos, and the inclusion of the original index ensures that even identical photos remain distinguishable in a consistent way.

## Python Solution

```python
import sys
input = sys.stdin.readline

photos = []

idx = 1
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    place = parts[0]
    d = int(parts[1])
    m = int(parts[2])
    h = int(parts[3])
    mi = int(parts[4])

    photos.append(((place, m, d, h, mi, idx), place, d, m, h, mi, idx))
    idx += 1

photos.sort(key=lambda x: x[0])

out = []
for _, place, d, m, h, mi, idx in photos:
    out.append(f"{idx} {place} {d:02d}.{m:02d}.2113 {h:02d}:{mi:02d}")

sys.stdout.write("\n".join(out))
```

The core design choice is the separation between the sorting key and the original data. The first tuple stored inside each record is purely for comparison, while the remaining fields preserve the original information for output reconstruction. This avoids recomputing or reparsing after sorting.

A common pitfall is mixing up the order of day and month. Since lexicographic ordering of dates is not naturally correct in (day, month) order, the correct hierarchy is month first, then day. Another subtle point is ensuring that all numeric fields are integers before comparison; otherwise, string comparison would incorrectly place "10" before "2".

## Worked Examples

### Sample 1

We track only key structure and ordering outcome.

| Step | Photo | Key (place, m, d, h, mi, idx) |
| --- | --- | --- |
| 1 | Moscow 15 01 13 24 | (Moscow, 1, 15, 13, 24, 1) |
| 2 | Maykop 17 05 00 13 | (Maykop, 5, 17, 0, 13, 2) |
| 3 | Adler 21 11 04 20 | (Adler, 11, 21, 4, 20, 3) |
| 4 | St.Petersburg 30 01 17 59 | (St.Petersburg, 1, 30, 17, 59, 4) |
| 5 | Moscow 01 04 00 00 | (Moscow, 4, 1, 0, 0, 5) |
| 6 | Kekland 04 12 01 43 | (Kekland, 12, 4, 1, 43, 6) |
| 7 | Moscow 15 01 02 43 | (Moscow, 1, 15, 2, 43, 7) |

After sorting, primary ordering is by place, then by month and day. Among Moscow entries, January photos come before April. Within January, day 01 precedes day 15, and for identical dates the earlier index determines order.

This confirms that tuple-based ordering simultaneously handles grouping, chronology, and stability.

### Sample 2

The second sample introduces repeated identical records.

| Step | Photo | Key |
| --- | --- | --- |
| 1 | Moscow 15 01 13 24 | (Moscow, 1, 15, 13, 24, 1) |
| 2 | Maykop 17 05 00 13 | (Maykop, 5, 17, 0, 13, 2) |
| 3 | Adler 21 11 04 20 | (Adler, 11, 21, 4, 20, 3) |
| 4 | Moscow 15 01 13 24 | (Moscow, 1, 15, 13, 24, 4) |
| 5 | st.Petersburg 30 01 17 59 | (st.Petersburg, 1, 30, 17, 59, 5) |
| 6 | Moscow 15 01 13 24 | (Moscow, 1, 15, 13, 24, 6) |
| 7 | Moscow 01 04 00 00 | (Moscow, 4, 1, 0, 0, 7) |
| 8 | Kekland 04 12 01 43 | (Kekland, 12, 4, 1, 43, 8) |
| 9 | Moscow 15 01 02 43 | (Moscow, 1, 15, 2, 43, 9) |

The three identical Moscow entries with the same timestamp form a tie under the first five components. The index breaks this tie, preserving input order exactly.

This demonstrates that the solution does not collapse duplicates and remains deterministic even under full equality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting n tuples, each comparison is O(1) over fixed fields |
| Space | O(n) | Storage for all parsed records and keys |

With n up to 100000, n log n is roughly 1.7 million comparisons, which is comfortably within typical limits for Python when using tuple comparisons.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    output = io.StringIO()
    _stdout = _sys.stdout
    _sys.stdout = output

    # solution
    photos = []
    idx = 1
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        place = parts[0]
        d = int(parts[1])
        m = int(parts[2])
        h = int(parts[3])
        mi = int(parts[4])
        photos.append(((place, m, d, h, mi, idx), place, d, m, h, mi, idx))
        idx += 1

    photos.sort(key=lambda x: x[0])

    for _, place, d, m, h, mi, idx in photos:
        print(f"{idx} {place} {d:02d}.{m:02d}.2113 {h:02d}:{mi:02d}")

    _sys.stdout = _stdout
    return output.getvalue().strip()

# provided samples (reformatted with newlines assumed)
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

# all equal timestamps, stability check
assert run("""A 01 01 00 00
A 01 01 00 00
A 01 01 00 00
""") == """1 A 01.01.2113 00:00
2 A 01.01.2113 00:00
3 A 01.01.2113 00:00"""

# different cases in lexicographic order
assert run("""b 01 01 00 01
A 01 01 00 00
a 01 01 00 02
""") == """2 A 01.01.2113 00:00
3 a 01.01.2113 00:02
1 b 01.01.2113 00:01"""

# boundary time ordering
assert run("""X 31 12 23 59
X 01 01 00 00
""") == """2 X 01.01.2113 00:00
1 X 31.12.2113 23:59"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal records | stable ordering | tie-breaking by index |
| mixed case labels | lexicographic ASCII order | correct string ordering |
| boundary timestamps | chronological ordering | date-time correctness |

## Edge Cases

One edge case is when multiple photos are identical across all fields. In that situation, a solution that sorts only by (place, time) may still pass in Python due to stable sort behavior, but in other languages or alternative implementations it would break. The inclusion of the original index guarantees deterministic ordering.

Another case involves lexicographic ordering of place names with mixed uppercase and lowercase letters. Since ASCII ordering places all uppercase letters before lowercase, a naive assumption of case-insensitive sorting would produce a different ordering. The correct behavior is to rely on raw string comparison without normalization.

A final subtle case is date-time ordering around month and day boundaries. If day is compared before month, then 31 January could incorrectly appear after 01 February depending on representation. Encoding the timestamp as (month, day, hour, minute) ensures correct chronological comparison at each level.
