---
title: "CF 105184A - Update"
description: "We are given a string consisting only of lowercase English letters. We are allowed to perform an operation that picks two letters x and y, then replaces every occurrence of x in the entire string with y in one global sweep. This operation can be repeated any number of times."
date: "2026-06-27T04:24:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105184
codeforces_index: "A"
codeforces_contest_name: "The 8th Hebei Collegiate Programming Contest"
rating: 0
weight: 105184
solve_time_s: 45
verified: true
draft: false
---

[CF 105184A - Update](https://codeforces.com/problemset/problem/105184/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting only of lowercase English letters. We are allowed to perform an operation that picks two letters `x` and `y`, then replaces every occurrence of `x` in the entire string with `y` in one global sweep. This operation can be repeated any number of times.

The goal is to transform the whole string so that every character becomes the letter `'i'`, and we want to minimize how many operations are needed.

The important aspect is that each operation is not local, it affects all occurrences of a chosen character simultaneously. This makes the problem about how letters can be progressively “merged” into other letters until everything collapses into `'i'`.

The constraint `|s| ≤ 10^4` means we are not expected to simulate anything per character per operation. Any solution that repeatedly scans or simulates transformations over the full string for many steps would still pass only if the number of operations is very small and bounded by alphabet size. Since there are only 26 possible letters, we should expect a solution that depends on letter types rather than string length.

A subtle point is that we are not forced to ever directly use `'i'` as an intermediate symbol during operations. Even if `'i'` is not initially present in the string, we are allowed to map any letter into `'i'`.

Edge cases worth isolating come from small alphabets:

If the string is `"i"`, the answer is `0` since nothing changes is needed.

If the string is `"abc"`, the optimal behavior is to map each of `a`, `b`, and `c` into `'i'`, giving 3 operations. A careless idea might try to first map everything into one letter and then into `'i'`, but that never improves the count.

If the string is `"aii"`, only `a` needs to be changed, so the answer is `1`.

These examples suggest the cost depends only on how many distinct letters are different from `'i'`.

## Approaches

The brute-force interpretation is to think of applying operations step by step, maintaining the full string each time. At each step, we could try all pairs `(x, y)` and simulate replacing `x` with `y`, then recurse or search for the minimum number of steps to reach a state where all characters are `'i'`. This is a shortest-path problem over all possible strings, where each state transition is one global replacement.

The state space is astronomically large. Even though each string has length up to `10^4`, the number of possible distinct strings is `26^n`, and even if we ignore structure and think only in terms of letter partitions, the transitions still form a graph over exponential states. This immediately makes brute-force impossible.

The key observation is that the operation only affects letter identities, not positions. Every position containing the same letter behaves identically forever. So the state is fully described by which letters currently exist in the string.

From this perspective, each operation removes one letter symbol `x` and replaces it with `y`. This strictly reduces the number of distinct letters unless `x` and `y` are already the same. Since we want everything to become `'i'`, the only letters that matter are the distinct letters in the original string other than `'i'`. Each such letter must be “eliminated” at least once, because nothing else can make it disappear except mapping it into another symbol, and eventually everything must collapse into `'i'`.

We can always do this optimally by directly mapping each non-`'i'` letter into `'i'` once. Any indirect chain like `a -> b -> i` does not reduce the number of operations because `a -> b` does not help reduce the number of distinct letters unless `b` is already `'i'`.

So the answer becomes purely combinational: count how many distinct letters appear in the string, and subtract one if `'i'` is among them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over string states | O(26! or exponential) | O(states) | Too slow |
| Distinct-letter counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to tracking which letters exist in the string.

1. Scan the string once and record which letters appear.

This matters because only the set of distinct characters affects the number of operations; positions are irrelevant.
2. Count how many distinct letters exist in total.
3. Check whether `'i'` is among these letters.
4. If `'i'` is present, the answer is `distinct_count - 1`, since `'i'` does not need to be removed or transformed.
5. If `'i'` is not present, the answer is `distinct_count`, since every letter must be directly transformed into `'i'`.

The decision in steps 4 and 5 reflects whether `'i'` is part of the initial alphabet of the string or must be introduced via a transformation.

### Why it works

Each operation eliminates exactly one source letter `x` by merging it into some target letter `y`. The process continues until only `'i'` remains. No operation can eliminate more than one distinct letter from the system because only one `x` is chosen per operation. Therefore, every distinct letter different from `'i'` requires at least one operation. A direct transformation from each such letter into `'i'` achieves this lower bound, making it optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    
    present = [False] * 26
    for ch in s:
        present[ord(ch) - ord('a')] = True

    distinct_count = sum(present)
    i_idx = ord('i') - ord('a')

    if present[i_idx]:
        print(distinct_count - 1)
    else:
        print(distinct_count)

if __name__ == "__main__":
    solve()
```

The implementation only tracks presence of letters, avoiding any simulation of replacements. The key subtlety is ensuring we treat `'i'` specially when it exists, since it does not need to be transformed away.

## Worked Examples

### Example 1: `s = "abc"`

| Step | Distinct letters | Contains 'i' | Answer |
| --- | --- | --- | --- |
| Initial | {a, b, c} | No | 3 |

Since `'i'` is not present, every letter must be converted into `'i'`. Each requires one operation, so the result is 3.

This confirms that indirect transformations like `a -> b -> c -> i` cannot reduce the count, because each elimination still consumes one letter.

### Example 2: `s = "aii"`

| Step | Distinct letters | Contains 'i' | Answer |
| --- | --- | --- | --- |
| Initial | {a, i} | Yes | 1 |

Only `a` needs to be transformed. One operation `a -> i` suffices.

This shows that repeated occurrences of a letter do not matter, only distinct types do.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the string to mark distinct letters |
| Space | O(1) | Fixed array of size 26 for alphabet tracking |

The constraints allow up to 10^4 characters, so a linear scan is easily sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = input().strip()
    present = [False] * 26
    for ch in s:
        present[ord(ch) - ord('a')] = True

    distinct_count = sum(present)
    i_idx = ord('i') - ord('a')

    if present[i_idx]:
        return str(distinct_count - 1)
    else:
        return str(distinct_count)

# minimal cases
assert run("i\n") == "0"
assert run("a\n") == "1"

# all same non-i
assert run("aaaa\n") == "1"

# includes i
assert run("ai\n") == "1"

# no i present, multiple letters
assert run("abc\n") == "3"

# large mixed
assert run("abcdefghijklmnopqrstuvwxyz\n") == "25"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"i"` | `0` | Already target character |
| `"aaaa"` | `1` | Single non-target letter |
| `"ai"` | `1` | Handling presence of `'i'` |
| `"abc"` | `3` | All letters need conversion |
| full alphabet | `25` | Maximum distinct case |

## Edge Cases

If the string contains only `'i'`, the algorithm marks only one distinct letter and subtracts one because `'i'` is present. The computed value becomes zero, matching the fact that no operation is needed.

For a string like `"zzzz"`, the distinct set contains only `'z'`, and since `'i'` is absent, the answer is one. The algorithm correctly performs a single conceptual transformation `z -> i`.

For a string containing every letter including `'i'`, such as `"abci"`, the distinct count is 4 and `'i'` is present, so the answer is 3. The algorithm correctly avoids counting `'i'` as a letter that needs elimination.
