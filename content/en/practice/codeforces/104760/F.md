---
title: "CF 104760F - \u0427\u0435\u0433\u043e-\u0442\u043e \u043d\u0435 \u0445\u0432\u0430\u0442\u0430\u0435\u0442..."
description: "We are given a multiset of integer “types” representing items in a warehouse. Most types are perfectly balanced: every such type appears the same number of times, say $S$. Exactly one exceptional type breaks this pattern and appears fewer times, say $P$, where $P < S$."
date: "2026-06-28T22:36:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "F"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 55
verified: true
draft: false
---

[CF 104760F - \u0427\u0435\u0433\u043e-\u0442\u043e \u043d\u0435 \u0445\u0432\u0430\u0442\u0430\u0435\u0442...](https://codeforces.com/problemset/problem/104760/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of integer “types” representing items in a warehouse. Most types are perfectly balanced: every such type appears the same number of times, say $S$. Exactly one exceptional type breaks this pattern and appears fewer times, say $P$, where $P < S$.

The task is to identify this underrepresented type. We are not told $P$ or $S$, and there is no ordering or structure beyond raw counts. The input is simply a list of integers, and exactly one distinct integer has a frequency strictly smaller than all others, which are equal.

The constraints allow up to $10^5$ elements. This immediately rules out anything quadratic like comparing every pair of frequencies or repeatedly scanning the array for each distinct value. An $O(N \log N)$ approach is acceptable, but there is enough slack for a linear solution if we use hashing.

The most subtle edge case is when there are only two distinct values and their counts differ by 1. For example, if one value appears 2 times and another appears 3 times, the answer is still the smaller one even though the difference is minimal. Another edge case is when negative numbers or large magnitude integers are present; the solution must rely only on equality comparisons, not ordering assumptions.

A naive mistake would be assuming the minimum or maximum value corresponds to the missing type. For example, in `[5, -3, 5, 5, -3]`, the answer is `-3`, even though it is smaller than 5; the correct reasoning comes from frequency, not value.

## Approaches

The brute-force strategy is to compute the frequency of every distinct value by scanning the entire list for each element. For each position $i$, we count how many times $t_i$ appears by iterating over the full array. This gives us the frequency of every candidate, and then we select the value with the smallest frequency.

This approach is correct because it directly follows the definition of the problem: we explicitly measure occurrences. However, its cost is prohibitive. For each of $N$ elements, we perform another $O(N)$ scan, leading to $O(N^2)$ operations. With $N = 10^5$, this becomes $10^{10}$ comparisons, which is far beyond typical limits.

The improvement comes from recognizing that frequency counting does not require repeated scans. If we aggregate counts in a single pass using a hash map, we can compute all frequencies in $O(N)$. Once we have counts, we simply iterate over them once to find the minimum frequency value. This transforms repeated work into shared work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Hash Map Counting | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all values and build a frequency table mapping each integer type to its number of occurrences. This ensures we compress all repeated scanning into a single pass over the data.
2. Iterate over the frequency table and track the value with the smallest frequency. Since exactly one value is underrepresented, this minimum is well-defined and unique.
3. Output the value corresponding to that minimum frequency.

### Why it works

The guarantee is that all values except one share the same frequency $S$, while exactly one value has frequency $P < S$. This creates a strict separation in the frequency space: one unique minimum and several identical larger values. A hash map preserves exact counts without collision ambiguity for equality, so the frequency table is exact. Selecting the minimum frequency from this table must return the unique underrepresented type.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    freq = {}
    for x in arr:
        freq[x] = freq.get(x, 0) + 1
    
    # find the element with smallest frequency
    best_val = None
    best_freq = float('inf')
    
    for val, cnt in freq.items():
        if cnt < best_freq:
            best_freq = cnt
            best_val = val
    
    print(best_val)

if __name__ == "__main__":
    solve()
```

The first phase builds the frequency dictionary in one linear scan. Each insertion or update is expected $O(1)$, so the total remains linear.

The second phase searches for the smallest frequency among distinct keys. This is safe because the number of distinct values is at most $N$, and we only scan this reduced set once.

A subtle implementation detail is initialization of `best_freq` to infinity. Using a large integer instead would also work, but infinity avoids accidental overflow or incorrect sentinel choices.

## Worked Examples

### Example 1

Input:

```
5
5 -3 5 5 -3
```

Frequency construction:

| Value | Count |
| --- | --- |
| 5 | 3 |
| -3 | 2 |

| Step | Current best | Best frequency |
| --- | --- | --- |
| Start | None | inf |
| Check 5 | 5 | 3 |
| Check -3 | -3 | 2 |

The algorithm first sees 5 with count 3, then updates when encountering -3 with count 2. The final answer is -3 because it has the smallest frequency.

### Example 2

Input:

```
6
10 10 10 7 7 7
```

Frequency construction:

| Value | Count |
| --- | --- |
| 10 | 3 |
| 7 | 3 |

| Step | Current best | Best frequency |
| --- | --- | --- |
| Start | None | inf |
| Check 10 | 10 | 3 |
| Check 7 | 10 or 7 (tie) | 3 |

In this case, both frequencies are equal. However, the problem guarantee forbids full equality among all values with no exception; there must be exactly one underrepresented type. This example shows that in a valid input, ties for minimum cannot occur, so the first minimum encountered is safe.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One pass to build frequencies and one pass over distinct keys |
| Space | O(N) | Hash map stores at most N distinct values |

With $N \le 10^5$, both time and memory are comfortably within limits. A linear scan over 100k elements is trivial for Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("5\n5 -3 5 5 -3\n") == "-3"

# minimum size case
assert run("3\n1 1 2\n") == "2"

# negative values
assert run("5\n-1 -1 -1 2 2\n") == "2"

# larger skew
assert run("7\n4 4 4 4 9 9 9\n") == "9"

# already balanced except one
assert run("4\n8 8 8 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5 -3 5 5 -3 | -3 | basic frequency separation |
| 3 1 1 2 | 2 | minimum size case |
| -1 -1 -1 2 2 | 2 | negative values handling |
| 7 4 4 4 4 9 9 9 | 9 | uneven frequency gap |
| 4 8 8 8 1 | 1 | single minority element |

## Edge Cases

A key edge case is when the minority frequency differs from the majority by exactly one. Consider input:

```
4
7 7 7 8
```

The frequency table is `{7: 3, 8: 1}`. The algorithm scans the map and sets `best_val = 8` because 1 is smaller than 3. There is no reliance on ordering of keys or values, only on counts.

Another edge case is negative values:

```
5
-10 -10 -10 -3 -3
```

Frequencies are `{ -10: 3, -3: 2 }`. The algorithm correctly selects `-3` because its frequency is smaller, even though its numeric value is larger. This confirms correctness under arbitrary integer ranges.

A final case is large input with many duplicates. Since hashing handles aggregation in expected constant time per insertion, the algorithm remains linear and does not degrade even when all values are identical except one.
