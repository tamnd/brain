---
title: "CF 34C - Page Numbers"
description: "We are asked to process a user-entered sequence of page numbers for printing. The input is a single string of positive i"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "expression-parsing", "implementation", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 34
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 34 (Div. 2)"
rating: 1300
weight: 34
solve_time_s: 67
verified: true
draft: false
---

[CF 34C - Page Numbers](https://codeforces.com/problemset/problem/34/C)

**Rating:** 1300  
**Tags:** expression parsing, implementation, sortings, strings  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to process a user-entered sequence of page numbers for printing. The input is a single string of positive integers separated by commas, such as `1,2,3,1,1,2,6,6,2`. Some numbers may repeat, possibly non-consecutively. Our goal is to produce a condensed, canonical representation: consecutive numbers are merged into ranges, duplicates are removed, and single pages are represented without a dash.

For instance, from `1,2,3,1,1,2,6,6,2`, after removing duplicates we get `1,2,3,6`, and then consecutive numbers `1,2,3` are merged into `1-3`, giving the final output `1-3,6`.

The input has at most 100 numbers, each not exceeding 1000. These constraints mean we do not need highly optimized data structures; even O(n log n) solutions will run comfortably within a 2-second limit. A naive algorithm that scans the array multiple times would also work, but we still want to be careful with duplicates and consecutive ranges.

Subtle edge cases include sequences where all numbers are the same, sequences with gaps, and sequences with repeated duplicates interleaved with other numbers. For example, `5,5,5` should output `5`, and `1,3,2` after deduplication and sorting would be `1-3` because the output must be in ascending order. A careless implementation might miss deduplication or incorrectly format single numbers.

## Approaches

The brute-force approach would be to iterate over the input, check each number against all previous numbers to remove duplicates, sort the resulting list, then iterate again to merge consecutive numbers. This works for the given constraints, but it requires repeated scanning and sorting. Worst-case operation count is roughly `O(n^2)` for duplicate removal plus `O(n log n)` for sorting, which is acceptable for n ≤ 100 but inelegant.

The key insight is that we can maintain uniqueness while preserving order by using a set to track seen numbers and a list to preserve insertion order. Once we have the deduplicated list, merging consecutive numbers is straightforward. This reduces redundant work, is easy to implement, and clearly separates the two concerns: removing duplicates and formatting ranges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Accepted for n ≤ 100, but inefficient |
| Optimal | O(n log n) | O(n) | Accepted, clean and maintainable |

## Algorithm Walkthrough

1. Parse the input string by splitting on commas and converting each piece to an integer. This gives a list of integers in the order entered.
2. Iterate through this list while maintaining a `seen` set. For each number, if it is not in `seen`, append it to a new list `unique_pages` and add it to `seen`. This preserves the first occurrence order and removes duplicates.
3. Sort `unique_pages` in ascending order. Sorting is necessary because ranges only make sense on ordered sequences.
4. Initialize an empty list `ranges` and a pointer `start` at the first element. Iterate over the sorted list from the second element onward. For each element, if it is consecutive to the previous element, continue. If it is not consecutive, close the current range by appending either `start` or `start-end` to `ranges`, then start a new range at the current element.
5. After the loop, append the final range in the same manner.
6. Join the `ranges` list with commas and print. This produces the canonical format requested.

Why it works: at every step, `unique_pages` contains each number exactly once, and the list is sorted. Every consecutive sequence is merged into a single range, while non-consecutive numbers naturally form separate ranges. The invariant is that `ranges` always contains properly formatted ranges covering all numbers seen so far.

## Python Solution

```python
import sys
input = sys.stdin.readline

pages = list(map(int, input().strip().split(',')))

seen = set()
unique_pages = []
for p in pages:
    if p not in seen:
        unique_pages.append(p)
        seen.add(p)

unique_pages.sort()

ranges = []
start = unique_pages[0]
end = unique_pages[0]

for p in unique_pages[1:]:
    if p == end + 1:
        end = p
    else:
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")
        start = end = p

if start == end:
    ranges.append(str(start))
else:
    ranges.append(f"{start}-{end}")

print(','.join(ranges))
```

The code first parses input into integers, removes duplicates while preserving order, then sorts the list. It then builds ranges by tracking consecutive numbers with `start` and `end`. The final print statement formats the list correctly. A subtle point is handling the final range after the loop, which is easy to forget and would lead to missing the last pages.

## Worked Examples

Sample Input 1: `1,2,3,1,1,2,6,6,2`

| Step | unique_pages | sorted | start | end | ranges |
| --- | --- | --- | --- | --- | --- |
| parse/dedup | [1,2,3,6] | [1,2,3,6] | 1 | 1 | [] |
| 2nd elem | - | - | 1 | 2 | [] |
| 3rd elem | - | - | 1 | 3 | [] |
| 4th elem | - | - | 6 | 6 | ['1-3'] |
| final | - | - | 6 | 6 | ['1-3','6'] |

This trace shows that duplicates are removed first, then consecutive numbers form a single range, and the last single number forms its own entry.

Sample Input 2: `5,5,5,5`

| Step | unique_pages | sorted | start | end | ranges |
| --- | --- | --- | --- | --- | --- |
| parse/dedup | [5] | [5] | 5 | 5 | [] |
| final | - | - | 5 | 5 | ['5'] |

This demonstrates that repeated identical numbers correctly collapse into a single entry.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Deduplication with a set is O(n), sorting takes O(n log n), merging ranges is O(n) |
| Space | O(n) | Storing unique pages and ranges requires linear space in the number of input numbers |

With n ≤ 100, O(n log n) is trivial, and memory usage is well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    pages = list(map(int, input().strip().split(',')))
    seen = set()
    unique_pages = []
    for p in pages:
        if p not in seen:
            unique_pages.append(p)
            seen.add(p)
    unique_pages.sort()
    ranges = []
    start = unique_pages[0]
    end = unique_pages[0]
    for p in unique_pages[1:]:
        if p == end + 1:
            end = p
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = end = p
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")
    return ','.join(ranges)

# provided sample
assert run("1,2,3,1,1,2,6,6,2") == "1-3,6", "sample 1"
# all equal
assert run("5,5,5,5") == "5", "all equal"
# single element
assert run("42") == "42", "single element"
# max value
assert run(",".join(map(str, range(1,101)))) == "1-100", "consecutive max"
# gaps
assert run("1,3,2,5,6") == "1-3,5-6", "gaps"
# unordered input
assert run("10,1,3,2,7,6,8") == "1-3,6-8,10", "unordered input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5,5,5,5 | 5 | duplicates |
| 42 | 42 | single element |
| 1..100 | 1-100 | large consecutive sequence |
| 1,3,2,5,6 | 1-3,5-6 | handling gaps |
| 10,1,3,2,7,6,8 | 1-3,6-8,10 | unordered input |

## Edge Cases

Input: `5,5,5`

`unique_pages = [5]`, sorted `[5]`, start = end = 5, ranges = [] initially. After final append, ranges = ['5']. Output is `5`. The algorithm correctly collapses all duplicates into a single entry.

Input: `1,3,2`

`unique_pages = [1,3
