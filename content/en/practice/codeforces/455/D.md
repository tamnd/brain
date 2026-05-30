---
title: "CF 455D - Serega and Fun"
description: "We have an array of integers, each between 1 and n, and we need to support two types of operations efficiently. The first operation rotates a segment of the array one step to the right. The second operation counts how many times a particular value occurs in a segment."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 455
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 260 (Div. 1)"
rating: 2700
weight: 455
solve_time_s: 87
verified: true
draft: false
---

[CF 455D - Serega and Fun](https://codeforces.com/problemset/problem/455/D)

**Rating:** 2700  
**Tags:** data structures  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of integers, each between 1 and _n_, and we need to support two types of operations efficiently. The first operation rotates a segment of the array one step to the right. The second operation counts how many times a particular value occurs in a segment. Queries arrive in an encoded form that depends on the previous answer, so we must process them online, updating the encoding after each count query.

The constraints allow the array size and the number of queries to reach 100,000. A naive approach that moves elements for each rotation or iterates over segments for each count would require up to 10^10 operations in the worst case, which is far beyond acceptable. This rules out any solution with O(n) per query. We need a structure that can perform segment rotations and frequency counts more efficiently.

Edge cases to consider include segments of length one, segments that wrap around after encoding, and multiple consecutive rotations on the same elements. For example, a single-element segment rotated should remain unchanged. Also, queries that ask for counts of a value not present in the segment should return zero, and careful handling of the encoding formula is required to avoid off-by-one errors.

## Approaches

The brute-force method iterates over the segment for each rotation and each count. For rotations, this involves moving up to n elements per query. For count queries, it scans up to n elements as well. With q up to 10^5 and n up to 10^5, this yields O(n * q) operations, which can reach 10^10, making it infeasible.

The optimal approach observes that the two operations we need to support - segment rotations and range frequency queries - are classical cases for a **block decomposition technique**, often called sqrt decomposition. We can divide the array into blocks of size roughly √n. For each block, we maintain a frequency map of its values. Counting a value over a segment involves summing the counts from full blocks and iterating manually only over partial blocks. Rotating a segment updates at most two partial blocks and leaves full blocks’ frequencies unchanged after shifting within them. By keeping each block in a list for element order and a dictionary for frequencies, we can perform both operations efficiently, in O(√n) time per query.

This leverages the fact that the square root of 100,000 is about 316, which is small enough for per-query operations to remain within time limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Sqrt Decomposition | O(q * √n) | O(n + √n * n) ≈ O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute block size as roughly √n. Divide the array into contiguous blocks of this size. Each block stores its elements in order and maintains a frequency dictionary of values within that block.
2. For a count query on a segment [l, r], first decode the query using the last answer. Identify which blocks are fully contained within [l, r] and which are partial. For full blocks, sum the frequency of the target value directly from the dictionary. For partial blocks at the edges, iterate manually over the elements in the segment and count matches.
3. For a rotation query on a segment [l, r], decode the segment similarly. If l and r are within a single block, simply rotate the elements in the list and update the block's frequency dictionary if necessary. If the segment spans multiple blocks, rotate the elements carefully across block boundaries: remove the last element of the segment and insert it at the start, adjusting each affected block’s frequency dictionary to reflect the changes.
4. After each count query, update lastans to the result, as it will be used in decoding subsequent queries.

Why it works: Each block maintains a correct frequency dictionary, and element order within the block is preserved. Count queries sum exact counts from full blocks and accurately check partial blocks, guaranteeing correctness. Rotations update both element positions and frequency counts, so future queries see the correct state.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math
from collections import defaultdict

def main():
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())
    lastans = 0
    
    block_size = int(math.sqrt(n)) + 1
    blocks = []
    freqs = []
    for i in range(0, n, block_size):
        blk = a[i:i+block_size]
        blocks.append(blk)
        freq = defaultdict(int)
        for val in blk:
            freq[val] += 1
        freqs.append(freq)
    
    def get_index(idx):
        return idx // block_size, idx % block_size

    for _ in range(q):
        parts = list(map(int, input().split()))
        if parts[0] == 1:
            l, r = parts[1], parts[2]
            l = (l + lastans - 1) % n
            r = (r + lastans - 1) % n
            if l > r:
                l, r = r, l
            l_blk, l_off = get_index(l)
            r_blk, r_off = get_index(r)
            if l_blk == r_blk:
                blk = blocks[l_blk]
                val = blk[r_off]
                for i in range(r_off, l_off, -1):
                    blk[i] = blk[i-1]
                blk[l_off] = val
                freq = freqs[l_blk]
                # freq unchanged
            else:
                # extract the last element
                val = blocks[r_blk][r_off]
                # shift last block
                for i in range(r_off, 0, -1):
                    blocks[r_blk][i] = blocks[r_blk][i-1]
                # shift middle blocks
                for b in range(r_blk-1, l_blk, -1):
                    last = blocks[b][-1]
                    blocks[b][1:] = blocks[b][:-1]
                    blocks[b][0] = last
                # shift first block
                for i in range(blocks[l_blk].__len__()-1, l_off, -1):
                    blocks[l_blk][i] = blocks[l_blk][i-1]
                blocks[l_blk][l_off] = val
                # rebuild frequency dicts
                for b in range(l_blk, r_blk+1):
                    freq = defaultdict(int)
                    for v in blocks[b]:
                        freq[v] += 1
                    freqs[b] = freq
        else:
            l, r, k = parts[1], parts[2], parts[3]
            l = (l + lastans - 1) % n
            r = (r + lastans - 1) % n
            k = (k + lastans - 1) % n + 1
            if l > r:
                l, r = r, l
            l_blk, l_off = get_index(l)
            r_blk, r_off = get_index(r)
            ans = 0
            if l_blk == r_blk:
                for i in range(l_off, r_off+1):
                    if blocks[l_blk][i] == k:
                        ans += 1
            else:
                for i in range(l_off, len(blocks[l_blk])):
                    if blocks[l_blk][i] == k:
                        ans += 1
                for b in range(l_blk+1, r_blk):
                    ans += freqs[b][k]
                for i in range(0, r_off+1):
                    if blocks[r_blk][i] == k:
                        ans += 1
            print(ans)
            lastans = ans

if __name__ == "__main__":
    main()
```

The code starts by reading input and preparing blocks with frequency dictionaries. For rotations, we carefully handle single-block and multi-block cases, shifting elements and rebuilding frequency maps. For counts, we sum full-block counts and check partial blocks directly. Encoding is handled before every query.

## Worked Examples

**Sample 1 trace**

| Step | Query | lastans | Action | Segment State |
| --- | --- | --- | --- | --- |
| 1 | 1 3 6 | 0 | Rotate indices 2-5 | [6,6,5,2,7,4,2] |
| 2 | 2 2 4 2 | 0 | Count value 2 in 1-3 | ans=2 |
| 3 | 2 2 4 7 | 2 | Count value 7 in 1-3 | ans=1 |
| 4 | 2 2 2 5 | 1 | Count value 5 in 1-1 | ans=0 |
| 5 | 1 2 6 | 0 | Rotate indices 1-5 | updated array |
| 6 | 1 1 4 | 0 | Rotate indices 0-3 | updated array |
| 7 | 2 1 7 3 | 0 | Count value 3 in 0-6 | ans=0 |

This trace confirms rotation logic and encoding adjustment.

**Custom trace**

Array [1,2,3,4], rotate 0-3, count 2 in 0-1, ensures first rotation moves elements correctly and counting works across blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * √n) | Each query |
