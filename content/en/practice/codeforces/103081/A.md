---
title: "CF 103081A - Gratitude"
description: "We are given a chronological log of Ben’s daily gratitude notes. Each day contributes exactly three independent text entries, and across all days we therefore have a sequence of 3N strings in total. Each string represents one “thing” Ben wrote down."
date: "2026-07-03T23:16:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103081
codeforces_index: "A"
codeforces_contest_name: "2020-2021 ICPC Southwestern European Regional Contest (SWERC 2020)"
rating: 0
weight: 103081
solve_time_s: 49
verified: true
draft: false
---

[CF 103081A - Gratitude](https://codeforces.com/problemset/problem/103081/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronological log of Ben’s daily gratitude notes. Each day contributes exactly three independent text entries, and across all days we therefore have a sequence of 3N strings in total. Each string represents one “thing” Ben wrote down.

The task is to summarize this collection by identifying the K most frequently occurring strings. Frequency alone is not enough to fully determine ordering. When two different strings appear the same number of times, the one whose last occurrence happens later in the input must come first.

The output is a ranked list of distinct strings, sorted primarily by decreasing frequency, and secondarily by decreasing last occurrence index, and we only print the top K of them.

The input size reaches up to 100,000 lines of text. Any solution that repeatedly sorts or scans the entire dataset per string would be too slow. The natural constraint suggests we should aim for something close to O(N log N) or O(N), since O(N^2) over strings is impossible.

A subtle issue is that ordering depends not only on counts but also on last occurrence position. This means we must track both aggregates during a single pass. A naive frequency map is insufficient unless it also stores positional information.

A few edge cases matter:

If all strings are unique, every frequency is 1, so ordering depends entirely on last occurrence, which effectively becomes reverse input order of unique elements.

If all strings are identical, there is only one output line regardless of K.

If K exceeds the number of distinct strings, we output all distinct strings.

A naive mistake is to sort only by frequency and ignore the tie-breaking rule. For example, if "A" and "B" both appear twice, but "A" last appears earlier than "B", then "B" must come first even if their counts are equal.

## Approaches

The brute-force idea is straightforward: first collect all 3N strings, then for each distinct string, scan the entire list again to count occurrences and track its last position. After that, sort all distinct strings using these computed values.

This is correct, but extremely expensive. If there are U distinct strings, each requiring O(N) scanning, the preprocessing alone costs O(UN). In the worst case U is Θ(N), giving O(N²), which is far beyond feasible for N up to 100,000.

The key observation is that both required statistics, frequency and last occurrence index, can be computed in a single linear scan. Instead of recomputing counts per string, we maintain a hash map from string to a pair: its count and the last index where it appeared. Each update is O(1) average, so the full preprocessing is O(N).

Once we have this map, we transform it into a list and sort it once using the required ordering key: higher frequency first, then higher last index first. This reduces the problem to a standard sorting task over U items.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

### Steps

1. Read all 3N strings in order, keeping a running index i from 0 to 3N−1. The index is essential because tie-breaking depends on the last occurrence position.
2. Maintain a dictionary keyed by string. For each string s at position i, update its entry by incrementing its frequency and setting its last position to i. Overwriting last position is correct because we always want the most recent occurrence.
3. After processing all lines, convert the dictionary into a list of tuples of the form (frequency, last_position, string). This format makes sorting straightforward.
4. Sort this list using a custom ordering: higher frequency first, and for equal frequency, higher last_position first. The string itself is only carried for output.
5. Output the first K strings from the sorted list.

### Why it works

The algorithm maintains an invariant that after processing the i-th line, every string in the dictionary stores exactly its total frequency in the prefix [0, i] and the index of its most recent occurrence in that prefix. Since every update is local and overwrites only the last position, no historical information is lost that could affect correctness. After the final iteration, these values are exact for the full sequence, so sorting them globally produces the required ranking.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    
    freq = {}
    last = {}
    
    for i in range(3 * n):
        s = input().rstrip('\n')
        if s in freq:
            freq[s] += 1
        else:
            freq[s] = 0
            freq[s] = 1
        last[s] = i
    
    items = []
    for s in freq:
        items.append((freq[s], last[s], s))
    
    items.sort(key=lambda x: (-x[0], -x[1]))
    
    out = []
    for i in range(min(k, len(items))):
        out.append(items[i][2])
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution uses two dictionaries, one for frequency and one for last occurrence index. They could be merged into a single structure, but keeping them separate makes the logic explicit: one tracks quantity, the other tracks recency.

The sorting key directly encodes the problem’s ordering rule. Negating both frequency and last index turns the default ascending sort into the required descending order.

A subtle point is that we store the last index as the loop counter i over raw input lines. This ensures correct chronological comparison even though days are grouped in threes.

## Worked Examples

### Example 1

Input:

```
2 2
A
B
C
D
C
E
```

We process 6 entries.

| i | string | freq state | last state |
| --- | --- | --- | --- |
| 0 | A | A:1 | A:0 |
| 1 | B | B:1 | B:1 |
| 2 | C | C:1 | C:2 |
| 3 | D | D:1 | D:3 |
| 4 | C | C:2 | C:4 |
| 5 | E | E:1 | E:5 |

Final items before sorting:

A(1,0), B(1,1), C(2,4), D(1,3), E(1,5)

Sorted:

C(2,4), E(1,5), D(1,3), B(1,1), A(1,0)

Taking K=2 gives:

C

E

This shows frequency dominates, while ties are resolved by last occurrence index.

### Example 2

Input:

```
1 5
X
Y
Z
```

All frequencies are 1, last positions are X:0, Y:1, Z:2.

Sorted order becomes Z, Y, X.

Since K=5 but only 3 distinct items exist, we output all of them.

This confirms that K acts as an upper bound rather than forcing padding.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Single pass builds hashmap in O(N), sorting U ≤ 3N items costs O(N log N) |
| Space | O(N) | Stores frequency and last position for each distinct string |

The input bound of 100,000 lines makes this approach comfortably safe. The hashing step is linear, and the sort dominates but remains within typical constraints for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    import sys
    from io import StringIO
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = StringIO(inp)
    sys.stdout = StringIO()
    
    def solve():
        n, k = map(int, input().split())
        freq = {}
        last = {}
        for i in range(3 * n):
            s = input().rstrip('\n')
            if s in freq:
                freq[s] += 1
            else:
                freq[s] = 1
            last[s] = i
        
        items = [(freq[s], last[s], s) for s in freq]
        items.sort(key=lambda x: (-x[0], -x[1]))
        k2 = min(k, len(items))
        print("\n".join(items[i][2] for i in range(k2)))
    
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.strip()

# provided samples
assert solve_capture("""2 2
A
B
C
D
C
E
""") == "C\nE"

# all equal
assert solve_capture("""3 2
A
A
A
A
A
A
A
A
A
""") == "A"

# all distinct
assert solve_capture("""1 3
A
B
C
""") == "C\nB\nA"

# tie by last occurrence
assert solve_capture("""1 3
A
B
A
""") == "A\nB"

# K exceeds distinct
assert solve_capture("""1 10
X
Y
Z
""") == "Z\nY\nX"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal strings | single line | collapse of duplicates |
| all distinct | reverse order | tie-breaking by recency |
| repeated with tie | A before B | last occurrence rule |
| K > distinct | full list | truncation behavior |

## Edge Cases

A common failure case is ignoring the last occurrence rule. Consider:

```
1 2
A
B
A
```

Here A and B both appear once, but A must come before B because its last occurrence is at index 2, while B is at index 1. The algorithm correctly updates last positions during the scan, so A gets higher priority.

Another edge case is when K exceeds the number of unique strings. The sorting step produces only distinct items, so slicing with min(k, len(items)) prevents out-of-range output.
