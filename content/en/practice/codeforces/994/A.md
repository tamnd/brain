---
title: "CF 994A - Fingerprints"
description: "The input describes a fixed sequence of digits, like a recorded keypad history, and a separate set of digits that correspond to keys with fingerprints."
date: "2026-06-17T00:08:50+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 994
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 488 by NEAR (Div. 2)"
rating: 800
weight: 994
solve_time_s: 251
verified: true
draft: false
---

[CF 994A - Fingerprints](https://codeforces.com/problemset/problem/994/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 4m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a fixed sequence of digits, like a recorded keypad history, and a separate set of digits that correspond to keys with fingerprints. The task is to reconstruct the longest possible code you could form by scanning the original sequence from left to right and keeping only those digits whose keys are marked as fingerprinted. The relative order of kept digits must not change, and you are not allowed to reorder or skip arbitrarily beyond filtering.

So the output is simply the original sequence filtered by membership in the fingerprint set, preserving the original ordering.

The constraints are extremely small, with both the sequence length and the number of fingerprinted digits bounded by 10. This immediately tells us that any solution from linear filtering down to even quadratic or brute-force subset checking would run instantly, but also that the intended solution is likely a straightforward implementation task rather than a search problem.

A few edge cases matter in subtle ways.

If no digit in the sequence is fingerprinted, the output is empty. For example, sequence `3 4 5` with fingerprint set `1 2 7` produces nothing. A naive implementation that assumes at least one match and prints without checking could accidentally output garbage or an extra space.

If all digits are fingerprinted, the output is the original sequence unchanged. For example, sequence `1 2 3` with fingerprint set `1 2 3` must reproduce the full sequence exactly.

Another corner case is that the fingerprint set may not appear in sorted order or may not align with the sequence order. For example, sequence `5 1 0 7` with fingerprints `0 1 7` must produce `1 0 7`, not sorted by digit value but by appearance in the sequence.

## Approaches

A brute-force way to think about the problem is to consider every subsequence of the given sequence and check whether all its elements are contained in the fingerprint set. Among those valid subsequences, we pick the longest one. This works because it explicitly explores all possibilities, but the number of subsequences of a sequence of length n is 2ⁿ, which grows quickly even though n is small here. Each validity check also requires scanning elements, so this becomes unnecessary overhead.

The key observation is that we do not actually need to search among subsequences at all. The problem does not impose any additional constraints such as maximizing lexicographic order or choosing among conflicting options. The only requirement is that every chosen digit must be allowed and that order is preserved. This removes any combinatorial choice: for each position in the sequence, we independently decide whether to keep it based solely on membership in the fingerprint set.

So the problem reduces to a single linear pass: filter elements by set membership.

The brute-force approach works conceptually because it enumerates all possibilities, but fails in efficiency due to exponential growth. The observation that there is no dependency between decisions at different positions transforms the task into a simple membership test per element, which is O(1) using a set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ · n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the sequence length, fingerprint count, the sequence itself, and the fingerprint digits. The goal is to quickly identify which digits are allowed.
2. Store the fingerprint digits in a hash set. This is done so that membership queries for a digit can be answered in constant time.
3. Iterate through the original sequence from left to right. For each digit, check whether it exists in the fingerprint set.
4. If the digit is in the set, append it to the output sequence. If not, ignore it completely.
5. After processing all digits, print the resulting filtered sequence separated by spaces. If nothing was collected, output an empty line.

The reasoning behind this procedure is that each position in the sequence is independent. Whether a digit is included depends only on whether it is allowed, not on what came before or after.

### Why it works

The constructed output contains exactly those elements from the original sequence that satisfy the fingerprint condition. Since we iterate left to right without reordering, the relative order is preserved automatically. There is no possibility of producing a longer valid sequence than this one, because every valid subsequence can only use digits already appearing in order, and we include every valid candidate individually.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    allowed = set(map(int, input().split()))

    res = []
    for x in a:
        if x in allowed:
            res.append(str(x))

    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The solution reads input using fast I/O to avoid overhead, though it is not strictly necessary given the constraints.

The fingerprint digits are stored in a set called `allowed`, which enables O(1) membership checks. This is the central optimization that replaces any need for searching or nested loops.

The loop over `a` is a direct filter. Each digit is converted to a string only when it is kept, since final output formatting requires space-separated integers.

The join operation handles both non-empty and empty outputs correctly. If `res` is empty, `" ".join(res)` produces an empty string, which satisfies the requirement of printing nothing or a blank line.

## Worked Examples

Consider the sample sequence `7 5 3 1 6 2 8` with fingerprint digits `1 2 7`.

At each step we check membership:

| Index | Digit | In fingerprints | Output so far |
| --- | --- | --- | --- |
| 0 | 7 | yes | 7 |
| 1 | 5 | no | 7 |
| 2 | 3 | no | 7 |
| 3 | 1 | yes | 7 1 |
| 4 | 6 | no | 7 1 |
| 5 | 2 | yes | 7 1 2 |
| 6 | 8 | no | 7 1 2 |

The final output is `7 1 2`, demonstrating that order is preserved while filtering is purely local per element.

Now consider a constructed example: sequence `4 0 9 1` with fingerprints `0 1`.

| Index | Digit | In fingerprints | Output so far |
| --- | --- | --- | --- |
| 0 | 4 | no |  |
| 1 | 0 | yes | 0 |
| 2 | 9 | no | 0 |
| 3 | 1 | yes | 0 1 |

This confirms that the algorithm correctly handles cases where valid digits are interleaved with invalid ones, without losing ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the sequence with O(1) membership checks per element |
| Space | O(m) | Set stores fingerprint digits |

The input bounds are extremely small, so this linear scan is far below any performance limit. Even for much larger constraints, the approach would remain efficient due to constant-time filtering.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    allowed = set(map(int, input().split()))

    res = []
    for x in a:
        if x in allowed:
            res.append(str(x))
    print(" ".join(res))

assert run("7 3\n3 5 7 1 6 2 8\n1 2 7\n") == "7 1 2", "sample 1"
assert run("3 2\n1 2 3\n4 5\n") == "", "no matches"
assert run("4 3\n1 2 3 4\n1 2 3\n") == "1 2 3", "prefix match"
assert run("5 2\n9 8 7 6 5\n5 9\n") == "9 5", "scattered matches"
assert run("1 1\n0\n0\n") == "0", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2 / 1 2 3 / 4 5 | empty | no valid digits case |
| 4 3 / 1 2 3 4 / 1 2 3 | 1 2 3 | partial prefix preservation |
| 5 2 / 9 8 7 6 5 / 5 9 | 9 5 | non-monotonic selection |

## Edge Cases

When no digit matches the fingerprint set, the algorithm builds an empty result list. For example, input `3 2 / 3 4 5 / 1 2` never triggers any append, so `res` stays empty and printing produces a blank line as required.

When every digit matches, such as `4 4 / 1 2 3 4 / 1 2 3 4`, every iteration appends to the result. The final output exactly mirrors the input sequence, confirming that filtering does not distort ordering.

When matches are sparse and separated, like `6 2 / 1 0 1 0 1 0 / 1 0`, the algorithm alternates between appending and skipping. Each decision is local, so the output becomes `1 0 1 0 1 0`, preserving full structure without needing any backtracking or reconstruction.
