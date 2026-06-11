---
title: "CF 1215C - Swap Letters"
description: "We are given two strings, s and t, of equal length composed only of the letters \"a\" and \"b\". The task is to make s and t identical using a sequence of allowed swap operations. Each operation lets us pick one character from s and one from t and swap them."
date: "2026-06-11T22:56:25+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1215
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 585 (Div. 2)"
rating: 1500
weight: 1215
solve_time_s: 102
verified: true
draft: false
---

[CF 1215C - Swap Letters](https://codeforces.com/problemset/problem/1215/C)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings, `s` and `t`, of equal length composed only of the letters "a" and "b". The task is to make `s` and `t` identical using a sequence of allowed swap operations. Each operation lets us pick one character from `s` and one from `t` and swap them. The goal is to achieve equality in the fewest number of swaps or determine that it is impossible.

The key observation is that a swap only affects two positions: one in `s` and one in `t`. If at a position the characters are already equal, we do not need to swap them. Therefore, we only need to consider positions where `s[i] != t[i]`. This reduces the problem to a set of mismatched pairs. Each mismatch can be classified into one of two types: `s[i] = a, t[i] = b` (call this type AB) and `s[i] = b, t[i] = a` (type BA).

Given that `n` can be up to 200,000 and we have a 2-second time limit, a solution that checks all possible swaps naively would be too slow. A brute-force approach of trying all combinations would be O(n²), which is not acceptable. We need a linear-time solution. Edge cases include having an odd number of a certain mismatch type, which may make the problem unsolvable. For example, if there is only one AB mismatch and no BA mismatch, no swap can resolve it, so the output must be -1.

## Approaches

A brute-force approach would iterate through all positions in `s` and `t` and swap whenever there is a mismatch, trying every possible combination until `s` equals `t`. This is correct because eventually, all mismatches would be resolved if possible. However, this approach is too slow because in the worst case, the number of operations considered could approach n², which is far too many for n = 200,000.

The optimal approach is based on the insight that we can pair mismatches of the same type to reduce the number of swaps. Specifically, two AB mismatches can be resolved by swapping one character from `s` in the first mismatch with the same from the second, which fixes both. Similarly, two BA mismatches can be resolved the same way. If there is one leftover AB and one leftover BA mismatch, we can first perform a "self-swap" within the string `s` to transform it into a resolvable pair, then swap across `s` and `t`. This approach ensures we minimize the number of swaps and runs in linear time because we only iterate over the mismatched positions and process them in pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two lists, `ab` and `ba`, to store indices where mismatches of type AB and BA occur, respectively. This step ensures we categorize mismatches efficiently.
2. Iterate through the strings `s` and `t` in parallel. Whenever `s[i] != t[i]`, append `i` to the appropriate list (`ab` if `s[i]='a'` and `t[i]='b'`, `ba` if `s[i]='b'` and `t[i]='a'`). This separates the problem into independent subproblems for each mismatch type.
3. If the total number of mismatches is odd, it is impossible to resolve all mismatches because each swap resolves two mismatches. Return -1 in this case. Concretely, if `(len(ab) + len(ba)) % 2 != 0`, we output -1.
4. Pair up indices within the `ab` list in consecutive order. Each pair `(i, j)` requires a single swap between `s[i]` and `t[j]`. Repeat the same process for the `ba` list. This reduces the number of operations by resolving two mismatches per swap.
5. If both `ab` and `ba` have odd lengths, there will be one leftover index in each. First perform a swap within `s` at the leftover AB index and the same index in `t` to transform the problem into a pair of BA mismatches. Then perform a swap between these transformed positions. This requires exactly two additional swaps. This trick ensures all mismatches are resolved with minimal operations.
6. Output the total number of swaps and the list of swap operations in order. Each operation is represented by indices `(pos_s, pos_t)`.

Why it works: At each step, we are either pairing mismatches of the same type or converting an unmatched pair into a resolvable configuration. No operation introduces new mismatches. The invariant is that after processing all pairs, all mismatches are resolved, and the strings are equal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()
t = input().strip()

ab = []
ba = []

for i in range(n):
    if s[i] != t[i]:
        if s[i] == 'a' and t[i] == 'b':
            ab.append(i + 1)  # using 1-based indexing
        else:
            ba.append(i + 1)

if (len(ab) + len(ba)) % 2 != 0:
    print(-1)
else:
    ops = []

    for i in range(0, len(ab) - len(ab) % 2, 2):
        ops.append((ab[i], ab[i + 1]))
    for i in range(0, len(ba) - len(ba) % 2, 2):
        ops.append((ba[i], ba[i + 1]))

    if len(ab) % 2 == 1:
        last_ab = ab[-1]
        last_ba = ba[-1]
        ops.append((last_ab, last_ab))
        ops.append((last_ab, last_ba))

    print(len(ops))
    for x, y in ops:
        print(x, y)
```

The solution first identifies mismatches, then resolves them efficiently by pairing, and finally handles any remaining odd pair with a two-step swap. The subtle point is ensuring 1-based indexing for the output and handling the single leftover pair correctly.

## Worked Examples

Sample Input 1:

```
4
abab
aabb
```

| i | s[i] | t[i] | ab | ba |
| --- | --- | --- | --- | --- |
| 1 | a | a |  |  |
| 2 | b | a |  | 2 |
| 3 | a | b | 3 |  |
| 4 | b | b |  |  |

Processing:

- Pair ab indices: [3] (odd)
- Pair ba indices: [2] (odd)
- Perform self-swap at 3, then swap 3 with 2
- Total operations: 2

Sample Input 2:

```
2
ab
bb
```

| i | s[i] | t[i] | ab | ba |
| --- | --- | --- | --- | --- |
| 1 | a | b | 1 |  |
| 2 | b | b |  |  |

Total mismatches = 1 (odd), impossible.

This trace shows how the algorithm detects impossibility and handles leftover odd mismatches correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to classify mismatches and linear pairing operations. |
| Space | O(n) | Storage for AB and BA index lists. |

The algorithm scales linearly with string length, suitable for n up to 200,000 within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution code here
    n = int(input())
    s = input().strip()
    t = input().strip()

    ab = []
    ba = []

    for i in range(n):
        if s[i] != t[i]:
            if s[i] == 'a' and t[i] == 'b':
                ab.append(i + 1)
            else:
                ba.append(i + 1)

    if (len(ab) + len(ba)) % 2 != 0:
        print(-1)
    else:
        ops = []

        for i in range(0, len(ab) - len(ab) % 2, 2):
            ops.append((ab[i], ab[i + 1]))
        for i in range(0, len(ba) - len(ba) % 2, 2):
            ops.append((ba[i], ba[i + 1]))

        if len(ab) % 2 == 1:
            last_ab = ab[-1]
            last_ba = ba[-1]
            ops.append((last_ab, last_ab))
            ops.append((last_ab, last_ba))

        print(len(ops))
        for x, y in ops:
            print(x, y)
    return output.getvalue().strip()

# Provided samples
assert run("4\nabab\naabb\n") == "2\n3 3\n3 2", "sample 1"
assert run("2\nab\nbb\n") == "-1",
```
