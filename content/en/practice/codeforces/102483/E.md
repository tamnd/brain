---
title: "CF 102483E - Equality Control"
description: "We are given two programs written in a small language where every expression produces a list of positive integers. The programs may contain fixed lists, concatenation, random shuffling, and sorting."
date: "2026-08-06T04:13:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102483
codeforces_index: "E"
codeforces_contest_name: "2018-2019 ICPC Northwestern European Regional Programming Contest (NWERC 2018)"
rating: 0
weight: 102483
solve_time_s: 109
verified: true
draft: false
---

[CF 102483E - Equality Control](https://codeforces.com/problemset/problem/102483/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two programs written in a small language where every expression produces a list of positive integers. The programs may contain fixed lists, concatenation, random shuffling, and sorting. The task is not to compare the text of the programs, but to decide whether they produce exactly the same probability distribution over all possible output lists.

The difficulty comes from the fact that the operations can hide information. A shuffled list does not care about the original order, while a concatenation keeps a boundary between its two parts. For example, randomly shuffling `[1,2,1,2]` is different from concatenating two independent shuffles of `[1,2]`, because the second version always contains a hidden split point.

The input strings can contain up to one million characters. This immediately rules out evaluating all possible outputs, because even a short list can have factorially many permutations. It also rules out building large intermediate distributions. The algorithm has to process the syntax almost linearly and keep only a compact description of the resulting distribution.

The main edge cases come from confusing operations that look similar. A program like `shuffle([1,2,3])` is not equivalent to `concat(shuffle([1,2]),[3])`, because the last element is fixed in the second program. A program like `shuffle([1])` should be treated as the deterministic list `[1]`, otherwise equivalent programs may receive different representations. Duplicate values are another trap. The probability of each final sequence depends on multiplicities, so treating a list as a set gives wrong answers.

## Approaches

A direct approach would be to simulate the probability distribution of every expression. For a list of length `n`, this means storing up to `n!` possible permutations after a shuffle. Even for a list with only 15 different positions this becomes impossible, and the maximum input size is many orders of magnitude larger.

The key observation is that a shuffle completely forgets the internal structure of its argument. The only information it keeps is the multiset of values. A sorted operation also only needs the multiset, but its output is deterministic. Everything else can be represented as a sequence of these two kinds of pieces.

The brute-force method works because the language semantics are small, but it fails because the number of possible outputs grows exponentially. The observation that every expression can be reduced to deterministic segments and independent shuffled segments lets us compare compact normal forms instead.

During normalization, a deterministic segment stores its exact sequence. A random segment stores only the counts of each value. Adjacent deterministic segments can be merged, and a random segment containing only one value can be converted into a deterministic segment.

The resulting representation is canonical. If two normalized representations differ, some boundary, value, or probability behavior differs, which means the original programs cannot be equivalent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of possible outputs) | O(number of possible outputs) | Too slow |
| Normal form construction | O(n) expected | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the expression recursively and return its normalized form together with its multiset of values. The multiset is needed because both `shuffle` and `sorted` discard ordering information.
2. Convert a list literal into a deterministic block. Its multiset is computed while reading the numbers.
3. For `concat(a,b)`, concatenate the normalized block sequences of both children. If two neighboring blocks are deterministic, merge them because there is no observable boundary between two fixed sequences.
4. For `shuffle(x)`, discard the block structure of `x` and create one random block containing only the multiset of all values in `x`. A random block with length one is simplified into a deterministic block.
5. For `sorted(x)`, create a deterministic block containing all values of `x` in increasing order. The original ordering information is irrelevant.
6. Compare the normalized block sequences of the two programs. Every deterministic block must have the same sequence, and every random block must have the same multiset.

The invariant is that every normalized expression describes exactly the same distribution as the original expression. Deterministic blocks represent values that are forced to appear at exact positions, while random blocks represent a uniform permutation of a multiset. The operations above preserve this meaning, so equal normalized forms imply equal distributions and different normalized forms imply different distributions.

## Python Solution

```python
import sys
from collections import Counter

input = sys.stdin.readline
sys.setrecursionlimit(3000000)

def merge_blocks(a, b):
    if not a:
        return b
    if not b:
        return a
    if a[-1][0] == 'D' and b[0][0] == 'D':
        return a[:-1] + [('D', a[-1][1] + b[0][1])] + b[1:]
    return a + b

def normalize_block(kind, data):
    if kind == 'R':
        if sum(data.values()) == 1:
            x = next(iter(data))
            return [('D', (x,))]
        return [('R', tuple(sorted(data.items())))]
    return [('D', tuple(data))]

def parse(s):
    n = len(s)
    pos = 0

    def dfs():
        nonlocal pos

        if s[pos] == '[':
            pos += 1
            vals = []
            cnt = Counter()
            while s[pos] != ']':
                start = pos
                while s[pos].isdigit():
                    pos += 1
                x = int(s[start:pos])
                vals.append(x)
                cnt[x] += 1
                if s[pos] == ',':
                    pos += 1
            pos += 1
            return [('D', tuple(vals))], cnt

        start = pos
        while s[pos].isalpha():
            pos += 1
        op = s[start:pos]
        pos += 1

        if op == 'concat':
            left, c1 = dfs()
            pos += 1
            right, c2 = dfs()
            pos += 1
            return merge_blocks(left, right), c1 + c2

        child, cnt = dfs()
        pos += 1

        if op == 'shuffle':
            return normalize_block('R', cnt), cnt

        arr = []
        for x, c in sorted(cnt.items()):
            arr.extend([x] * c)
        return [('D', tuple(arr))], cnt

    return dfs()[0]

a = input().strip()
b = input().strip()

print("equal" if parse(a) == parse(b) else "not equal")
```

The parser follows the grammar directly. A list literal is handled by collecting its values and counting occurrences at the same time. The counter is necessary because a shuffled result depends on multiplicity, not just the distinct values.

The `merge_blocks` function is the only simplification needed after concatenation. Two deterministic neighbors are indistinguishable from one larger deterministic block, while random blocks must stay separated because the independence between them changes the distribution.

The `normalize_block` function handles the subtle singleton case. A shuffle of one value cannot introduce randomness, so keeping it as a random block would create multiple representations for the same behavior.

The parser uses recursion because the grammar is naturally recursive. The recursion limit is increased to support deeply nested expressions.

## Worked Examples

For the first sample, compare:

`concat(shuffle([1,2]),shuffle([1,2]))`

and

`shuffle([1,2,1,2])`

| Step | First program | Second program |
| --- | --- | --- |
| Parse first shuffle | Random block `{1:1,2:1}` |  |
| Parse second shuffle | Two independent random blocks |  |
| Parse outer shuffle |  | Random block `{1:2,2:2}` |
| Normal form | `R(1,2), R(1,2)` | `R(1,1,2,2)` |
| Result | Different | Different |

The trace shows why keeping the random block boundaries matters. The two expressions have the same total multiset but different probabilities.

For the second sample:

`sorted(concat([3,2,1],[4,5,6]))`

and

`[1,2,3,4,5,6]`

| Step | First program | Second program |
| --- | --- | --- |
| Read literals | Multiset `{1,2,3,4,5,6}` | Sequence `(1,2,3,4,5,6)` |
| Apply sorted | Deterministic `(1,2,3,4,5,6)` | Deterministic `(1,2,3,4,5,6)` |
| Result | Equal | Equal |

The example demonstrates that sorting removes all previous ordering information.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) expected | Every character is parsed once, and hash map operations for counts are expected O(1). |
| Space | O(n) | The normalized representation stores information proportional to the input size. |

The input limit of one million characters requires avoiding enumeration of outputs and keeping parsing close to linear. The solution only stores compressed information about ordering and value frequencies, so it fits comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()
    sys.stdin = old
    return "equal\n" if parse(a) == parse(b) else "not equal\n"

assert run("concat(shuffle([1,2]),shuffle([1,2]))\nshuffle([1,2,1,2])\n") == "not equal\n"

assert run("sorted(concat([3,2,1],[4,5,6]))\n[1,2,3,4,5,6]\n") == "equal\n"

assert run("concat(sorted([4,3,2,1]),shuffle([1]))\nconcat(concat([1,2,3],shuffle([4])),sorted([1]))\n") == "equal\n"

assert run("[5]\nshuffle([5])\n") == "equal\n"

assert run("shuffle([1,1,2])\nconcat([1],shuffle([1,2]))\n") == "not equal\n"

assert run("sorted([9,9,1])\n[1,9,9]\n") == "equal\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `shuffle([1,2])` versus two shuffles concatenated | not equal | Independent randomness cannot be merged |
| `sorted([9,9,1])` versus sorted order | equal | Sorting uses only the multiset |
| `shuffle([5])` versus `[5]` | equal | Singleton randomness simplification |
| Duplicate values in different structures | not equal | Multiplicity affects probabilities |

## Edge Cases

For `shuffle([5])` compared with `[5]`, the algorithm creates a random block with one element and immediately converts it into a deterministic block. Both normalize to `D(5)`, so the output is correctly `equal`.

For `shuffle([1,1,2])` compared with `concat([1],shuffle([1,2]))`, both expressions contain the same values, but their normalized forms are different. The first becomes one random block with counts `{1:2,2:1}`, while the second becomes a deterministic block followed by a random block. The hidden split changes the possible outputs, so the algorithm returns `not equal`.

For duplicate values, such as `sorted([9,9,1])` versus `[1,9,9]`, the multiset counter stores two copies of `9` and one copy of `1`. Sorting produces the exact deterministic sequence, so both programs receive the same canonical representation.
