---
title: "CF 62B - Tyndex.Brome"
description: "The task is to compute a kind of \"distance\" between a user-entered address and a list of potential addresses, according to a specific error function. The user enters a string s of length k. Then there are n potential addresses, each a string of arbitrary length."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation"]
categories: ["algorithms"]
codeforces_contest: 62
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 58"
rating: 1800
weight: 62
solve_time_s: 78
verified: true
draft: false
---

[CF 62B - Tyndex.Brome](https://codeforces.com/problemset/problem/62/B)

**Rating:** 1800  
**Tags:** binary search, implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to compute a kind of "distance" between a user-entered address and a list of potential addresses, according to a specific error function. The user enters a string `s` of length `k`. Then there are `n` potential addresses, each a string of arbitrary length. For each character in a potential address, we try to match it with the closest occurrence of the same character in `s`. If the character exists in `s`, we add the minimal distance between positions. If it does not exist, we add the length of the potential address. The output for each potential address is a single number representing this total error.

The input bounds are significant. We can have up to 100,000 potential addresses, each of varying length, but the sum of all lengths is capped at 200,000. This immediately rules out any naive approach that checks each character against every character in `s` in a straightforward O(n * k * len(address)) manner, because in the worst case that could reach 10^10 operations. We need an algorithm closer to linear in the sum of all address lengths.

Edge cases that are subtle include addresses containing characters completely absent in `s`, addresses identical to `s`, and very short addresses compared to `s`. For instance, if `s = "abc"` and a potential address is `"d"`, the function `F` should return `1` because `d` does not appear in `s`. A naive implementation that does not handle missing characters correctly could return zero instead.

## Approaches

The brute-force solution is straightforward. For each potential address, we iterate over each character and scan `s` to find the closest match. This guarantees correctness, because we are literally computing the minimal distance for each character. However, if `s` has length 10^5 and we have 10^5 potential addresses, each of length up to 2, this approach could require on the order of 10^10 comparisons. This exceeds the time limit.

The key observation for optimization is that we do not need to scan `s` for each character every time. Instead, we can precompute the positions of each character in `s`. Once we have sorted lists of indices for each character, we can use binary search to find the closest position to any given index in O(log k) time. The total cost is then proportional to the sum of lengths of all addresses times log k, which is feasible for the problem constraints.

Another subtle improvement is handling characters absent from `s`. If a character is not in `s`, the minimal error contribution is the length of the address. This is simple to check during the binary search step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k * m) | O(1) | Too slow |
| Binary Search per Character | O(sum(len(addresses)) * log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read the input: integers `n` and `k`, the user-entered string `s`, and the list of potential addresses.
2. Preprocess `s` by recording, for each character 'a' to 'z', a sorted list of indices where it occurs in `s`. This allows us to quickly locate the nearest occurrence of any character.
3. For each potential address, initialize the error function `F` to zero. Iterate through its characters one by one.
4. For the current character, check if it exists in `s` using the precomputed positions. If it does not, add the length of the potential address to `F` and continue to the next character.
5. If the character exists in `s`, use binary search to find the nearest index in `s` to the current position in the potential address. Compute the absolute distance and add it to `F`.
6. After processing all characters in the potential address, print or store `F`.
7. Repeat steps 3-6 for all potential addresses.

The invariant is that after preprocessing, every character in a potential address either contributes the minimal possible distance to `F` if it exists in `s`, or contributes the full address length if it does not. Binary search guarantees we find the closest index, so the algorithm computes exactly the function as defined.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

n, k = map(int, input().split())
s = input().strip()

# Precompute positions of each character in s
pos = {chr(c): [] for c in range(ord('a'), ord('z')+1)}
for i, ch in enumerate(s):
    pos[ch].append(i)

addresses = [input().strip() for _ in range(n)]

for address in addresses:
    F = 0
    for i, ch in enumerate(address):
        if not pos[ch]:
            F += len(address)
            continue
        idx_list = pos[ch]
        insert_point = bisect.bisect_left(idx_list, i)
        min_dist = float('inf')
        if insert_point < len(idx_list):
            min_dist = abs(idx_list[insert_point] - i)
        if insert_point > 0:
            min_dist = min(min_dist, abs(idx_list[insert_point-1] - i))
        F += min_dist
    print(F)
```

In the code, `pos` holds all positions of each character in `s`. For each character in a potential address, we find the closest match using `bisect_left`, considering both the index found and the previous index, which ensures we always take the minimal distance. If a character is missing, we immediately add the full length. Off-by-one errors are avoided by careful indexing and considering both sides of the insertion point.

## Worked Examples

### Sample 1

Input:

```
2 10
codeforces
codeforces
codehorses
```

Processing the first address `codeforces`:

| Character | Index in address | Closest index in s | Distance |
| --- | --- | --- | --- |
| c | 0 | 0 | 0 |
| o | 1 | 1 | 0 |
| d | 2 | 2 | 0 |
| e | 3 | 3 | 0 |
| f | 4 | 4 | 0 |
| o | 5 | 5 | 0 |
| r | 6 | 6 | 0 |
| c | 7 | 7 | 0 |
| e | 8 | 8 | 0 |
| s | 9 | 9 | 0 |

`F = 0`

Processing the second address `codehorses`:

| Character | Index | Closest index in s | Distance |
| --- | --- | --- | --- |
| c | 0 | 0 | 0 |
| o | 1 | 1 | 0 |
| d | 2 | 2 | 0 |
| e | 3 | 3 | 0 |
| h | 4 | none | 11 |
| o | 5 | 5 | 0 |
| r | 6 | 6 | 0 |
| s | 7 | 9 | 2 |
| e | 8 | 8 | 0 |
| s | 9 | 9 | 0 |

`F = 12`

This confirms the correct computation of distances and handling of missing characters.

### Sample 2 (Edge case)

Input:

```
1 3
abc
d
```

Output:

```
1
```

Here, the character `d` does not exist in `s`, so `F = len("d") = 1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sum(len(addresses)) * log k) | Preprocessing `s` is O(k). Each character of each address requires a binary search in the position list. Sum of all address lengths ≤ 2·10^5, log k ≤ 17, acceptable. |
| Space | O(k + n) | Storing positions of each character in `s` requires O(k). Addresses require O(n) for input. |

The algorithm is comfortably within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        n, k = map(int, input().split())
        s = input().strip()
        pos = {chr(c): [] for c in range(ord('a'), ord('z')+1)}
        for i, ch in enumerate(s):
            pos[ch].append(i)
        addresses = [input().strip() for _ in range(n)]
        for address in addresses:
            F = 0
            for i, ch in enumerate(address):
                if not pos[ch]:
                    F += len(address)
                    continue
                idx_list = pos[ch]
                insert_point = bisect.bisect_left(idx_list, i)
                min_dist = float('inf')
                if insert_point < len(idx_list):
                    min_dist = abs(idx_list[insert_point] - i)
                if insert_point > 0
```
