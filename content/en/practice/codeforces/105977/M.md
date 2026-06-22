---
title: "CF 105977M - \u81f4\u8c22"
description: "The problem gives a fixed historical table describing 11 editions of a programming contest series in Fujian. Each edition has an organizing university, and each university is associated with a short English abbreviation."
date: "2026-06-22T16:29:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105977
codeforces_index: "M"
codeforces_contest_name: "2025 National Invitational of CCPC (Fujian), The 12th Fujian Collegiate Programming Contest"
rating: 0
weight: 105977
solve_time_s: 46
verified: true
draft: false
---

[CF 105977M - \u81f4\u8c22](https://codeforces.com/problemset/problem/105977/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives a fixed historical table describing 11 editions of a programming contest series in Fujian. Each edition has an organizing university, and each university is associated with a short English abbreviation. The input is a single integer `n`, representing which edition of the contest we are interested in. The task is to output the abbreviation of the university that organized the `n`-th edition.

Even though the statement contains a lot of noise and garbled characters, the actual structure is simple: there is a static list of 11 entries, and the answer is a direct lookup by index.

The constraint `1 ≤ n ≤ 11` is extremely small, which immediately rules out any need for preprocessing, searching, or algorithmic optimization. Any solution that performs even a constant-time array indexing operation is sufficient.

There are no hidden edge cases involving large input sizes or multiple queries. The only subtle issue a careless implementation might run into is off-by-one indexing, since contest problems like this often number editions starting from 1 while programming languages index arrays from 0.

For example, if someone mistakenly treats the first edition as index 0, then input `1` would incorrectly map to the second university instead of the first, producing a wrong abbreviation even though the logic looks correct.

## Approaches

The structure of the problem is essentially a static mapping from integers to strings. The brute-force interpretation would be to reconstruct the mapping dynamically by parsing the full table of universities and extracting abbreviations each time, but that is unnecessary overhead. The table is fixed and tiny, so recomputing or parsing it repeatedly would only add complexity without benefit.

The key observation is that nothing changes across test cases and there is no computation required beyond selecting the correct pre-known value. Once we recognize that the problem is a direct indexing task, the solution reduces to storing the 11 abbreviations in an array and returning the `(n-1)`-th element.

The brute-force idea fails in terms of elegance rather than speed: it would involve re-reading structured text or simulating parsing logic, which is fragile given the encoding noise in the statement. The direct indexing approach is robust and minimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force parsing | O(1) per query but complex implementation | O(1) | Unnecessary |
| Direct lookup | O(1) | O(11) | Accepted |

## Algorithm Walkthrough

1. Construct a list `abbr` containing the 11 known abbreviations in order of contest editions. This list is derived directly from the problem’s table, where each position corresponds to one edition.
2. Read the integer `n` from input.
3. Output `abbr[n - 1]`, converting from 1-based indexing in the problem statement to 0-based indexing in the array representation.

### Why it works

The contest editions form a fixed sequence with no transformations or dependencies between entries. Each query is simply asking for the value stored at a known position in that sequence. Because the mapping is static and total over the domain `1..11`, storing it explicitly guarantees correctness. The only transformation required is adjusting indexing, and once that is handled, the lookup is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

abbr = [
    "FZU",
    "FNU",
    "FZU",
    "FZU",
    "FAFU",
    "HQU",
    "MJU",
    "XMUT",
    "QZNU",
    "JMU",
    "FZU"
]

n = int(input().strip())
print(abbr[n - 1])
```

The solution hardcodes the abbreviation sequence in the exact order of the contest editions. This is intentional because the dataset is fixed by the problem statement itself.

The only implementation detail that matters is the `n - 1` adjustment. Since Python lists are zero-indexed but the problem defines the first edition as `1`, failing to subtract one would shift every answer by one position.

## Worked Examples

Consider the input `1`. The algorithm reads `n = 1` and accesses `abbr[0]`, which is `"FZU"`. This matches the first edition’s organizer.

Now consider `2`. The algorithm accesses `abbr[1]`, returning `"FNU"`. This corresponds to the second edition in the table.

| Step | n | Index used | Value |
| --- | --- | --- | --- |
| Example 1 | 1 | 0 | FZU |
| Example 2 | 2 | 1 | FNU |

These examples confirm that the mapping is purely positional and that indexing is the only transformation required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single array lookup after reading input |
| Space | O(1) | Fixed list of 11 strings |

The constraints ensure that constant-time lookup is sufficient. Even if the input were extended slightly, this approach would remain optimal since no computation beyond indexing is needed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    abbr = [
        "FZU","FNU","FZU","FZU","FAFU",
        "HQU","MJU","XMUT","QZNU","JMU","FZU"
    ]
    n = int(sys.stdin.readline().strip())
    return abbr[n - 1]

# provided samples
assert run("1\n") == "FZU"
assert run("2\n") == "FNU"

# boundary cases
assert run("11\n") == "FZU"
assert run("5\n") == "FAFU"
assert run("7\n") == "MJU"
assert run("9\n") == "QZNU"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | FZU | First element correctness |
| 2 | FNU | Second element correctness |
| 11 | FZU | Upper boundary indexing |
| 5 | FAFU | Middle mapping correctness |

## Edge Cases

The only meaningful edge case is the boundary indexing at the ends of the list. For input `1`, the algorithm computes index `0`, which correctly retrieves the first abbreviation. For input `11`, it computes index `10`, which retrieves the last entry.

For example, when `n = 11`, the computation is:

The list access becomes `abbr[10]`, which returns `"FZU"`. Since the list is explicitly constructed in the correct order, no out-of-range access occurs and no special handling is required beyond the indexing shift.
