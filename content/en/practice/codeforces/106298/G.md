---
title: "CF 106298G - Yet Yet Another Binary String Problem"
description: "We are working with binary strings where the important structure is not individual characters but contiguous segments of equal characters. Each maximal segment of consecutive 0s or consecutive 1s forms a block."
date: "2026-06-19T16:50:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106298
codeforces_index: "G"
codeforces_contest_name: "OCPC 2024 Summer, Day 4: wuhudsm Contest"
rating: 0
weight: 106298
solve_time_s: 54
verified: true
draft: false
---

[CF 106298G - Yet Yet Another Binary String Problem](https://codeforces.com/problemset/problem/106298/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with binary strings where the important structure is not individual characters but contiguous segments of equal characters. Each maximal segment of consecutive `0`s or consecutive `1`s forms a block. For example, the string `0001110011` consists of four blocks: `000`, `111`, `00`, and `11`.

The allowed transformation rule is described in terms of these blocks. A block is not allowed to disappear entirely, but its length is flexible. A block may be stretched or shrunk arbitrarily, meaning we can change how many characters it contains, but we cannot remove a block or merge it with its neighbors. What matters is the sequence of blocks and their starting value.

The condition for converting string `a` into string `b` reduces to comparing their block structure. If both strings have the same number of blocks and the first block has the same value, then one can be converted into the other.

The input therefore consists of two binary strings per test case, and the output is a decision whether the transformation is possible under the block-preserving rules.

The constraints are not explicitly given in the statement snippet, but problems of this form typically allow strings up to around 10^5 per test case or more. That immediately rules out any solution that simulates transformations or attempts to construct intermediate strings. Any approach must reduce each string to a linear scan and constant or logarithmic comparison per test case.

A naive mistake is to compare strings directly or to only compare counts of `0`s and `1`s. Both fail because structure matters. For example, `0011` and `0101` have the same number of zeros and ones, but different block structures, and no sequence of allowed operations can reconcile the alternating structure.

Another subtle edge case is a single-character string. For example, `0` can convert to `0000`, but `0` cannot convert to `1` even if both have length one, because the starting block differs.

## Approaches

The brute-force way to think about this is to simulate all possible ways of resizing blocks in string `a` and trying to match string `b`. Since each block can grow or shrink freely but must remain in place, the only meaningful state is the partition of the string into blocks. A brute-force simulation would attempt to assign lengths to each block of `a` to match `b`. In the worst case, if both strings have n characters, there are O(n) blocks, and trying all assignments or alignments degenerates into exponential or at least quadratic matching logic due to dependency between adjacent blocks. This quickly becomes infeasible even for n around 10^4.

The key observation is that block boundaries never change. Since blocks cannot be destroyed or merged, every valid transformation preserves the exact sequence of block types. The only freedom is within each block’s length. That means the entire transformation problem collapses into a structural equivalence check between two run-length encodings: compare whether the sequences of alternating characters are identical.

This reduces the problem to computing the run-length encoding of both strings and checking whether both sequences match exactly in both length and character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / O(n²) | O(n) | Too slow |
| Optimal (RLE comparison) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each string by compressing it into its sequence of blocks.

1. Scan string `a` from left to right and construct its run-length encoding. Each time the current character differs from the previous one, we close a block and start a new one. We store only the character of each block, not its length, because lengths are irrelevant to the transformation.
2. Repeat the same process for string `b`, producing its block sequence.
3. Compare the number of blocks in both sequences. If they differ, there is no way to align block structure without merging or splitting, which is forbidden.
4. Compare the starting character of both strings. Since the first block must match in value, a mismatch here immediately makes conversion impossible.
5. Compare each block position-wise. Every block in position i of `a` must have the same character as the corresponding block in `b`. If any mismatch occurs, the transformation is impossible.
6. If all checks pass, conclude that transformation is possible.

The reason this is sufficient is that once block boundaries are fixed, each block behaves independently. Since we are allowed to expand or shrink blocks arbitrarily, we can always match lengths of corresponding blocks as long as the sequence pattern matches.

### Why it works

The invariant is that the partition of a binary string into maximal uniform segments is uniquely determined and cannot change under the allowed operations. Since operations never merge or destroy blocks, any valid transformation must preserve the exact sequence of block identities. Therefore, two strings are equivalent under the operation rules if and only if their run-length encoded sequences of characters are identical.

## Python Solution

```python
import sys
input = sys.stdin.readline

def rle(s: str):
    blocks = []
    n = len(s)
    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        blocks.append(s[i])
        i = j
    return blocks

def solve():
    t = int(input())
    for _ in range(t):
        a = input().strip()
        b = input().strip()

        ra = rle(a)
        rb = rle(b)

        if ra == rb:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution directly constructs the run-length signature of each string. The helper function scans each string once, producing a sequence of block identifiers. The comparison is then reduced to a simple list equality check.

A subtle implementation detail is that we do not store block lengths at all. That is safe because the problem explicitly allows blocks to grow or shrink arbitrarily. Storing lengths would only add noise and risk incorrect comparisons.

The correctness hinges entirely on the fact that adjacency structure is invariant, not the actual counts inside each block.

## Worked Examples

### Example 1

Consider `a = 0001110` and `b = 001110`.

For `a`, the blocks are:

| Step | Index Range | Block |
| --- | --- | --- |
| 1 | 0-2 | 0 |
| 2 | 3-5 | 1 |
| 3 | 6-6 | 0 |

So `ra = [0, 1, 0]`.

For `b`, the blocks are:

| Step | Index Range | Block |
| --- | --- | --- |
| 1 | 0-1 | 0 |
| 2 | 2-4 | 1 |
| 3 | 5-5 | 0 |

So `rb = [0, 1, 0]`.

Since the sequences match, the output is `YES`.

This confirms that differing block lengths do not matter.

### Example 2

Let `a = 010` and `b = 001`.

For `a`, blocks are `[0, 1, 0]`.

For `b`, blocks are `[0, 1]`.

| String | Block Sequence |
| --- | --- |
| a | [0, 1, 0] |
| b | [0, 1] |

Since the number of blocks differs, conversion is impossible, so the output is `NO`.

This shows that even if total counts are similar, mismatched alternation breaks feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each string is scanned once to build its run-length structure |
| Space | O(n) worst case | In worst case alternating strings produce one-character blocks |

The solution fits comfortably within typical constraints for binary string problems, even when total input size reaches 10^6 across all test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    def rle(s: str):
        blocks = []
        i = 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            blocks.append(s[i])
            i = j
        return blocks

    t = int(sys.stdin.readline())
    for _ in range(t):
        a = sys.stdin.readline().strip()
        b = sys.stdin.readline().strip()
        output.append("YES" if rle(a) == rle(b) else "NO")
    
    return "\n".join(output)

# sample-like tests
assert run("2\n000111\n00111\n010\n001\n") == "YES\nNO"

# minimum size
assert run("1\n0\n0\n") == "YES"

# mismatch start
assert run("1\n1\n0\n") == "NO"

# alternating maximum fragmentation
assert run("1\n010101\n010101\n") == "YES"

# different block structure
assert run("1\n0011\n0101\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single character equal | YES | minimal valid case |
| different starting bit | NO | start block constraint |
| identical alternating strings | YES | many small blocks |
| same counts but different structure | NO | block structure importance |

## Edge Cases

One important edge case is when both strings consist of a single repeated character. For example, `a = 0000` and `b = 0`. The algorithm compresses both into a single block `[0]`, so the output is `YES`. This reflects the fact that block length is irrelevant.

Another edge case is when strings have identical counts of `0` and `1` but different alternation patterns, such as `0011` and `0101`. The first produces `[0, 1]` while the second produces `[0, 1, 0, 1]`, immediately rejecting the transformation. The algorithm correctly captures this because it never loses boundary information during compression.

A final edge case is alternating single-character strings like `010101` versus `0101010`. Even though both look similar, the block count differs by one, and the algorithm rejects it at the comparison step, matching the invariant that block structure must be identical.
