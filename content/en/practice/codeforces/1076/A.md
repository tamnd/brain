---
title: "CF 1076A - Minimizing the String"
description: "We are given a single string made of lowercase letters, and we are allowed to delete at most one character from it. After this optional deletion, we obtain a new string, and among all possible results (including doing nothing), we want the lexicographically smallest one."
date: "2026-06-15T06:47:25+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1076
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 54 (Rated for Div. 2)"
rating: 1200
weight: 1076
solve_time_s: 88
verified: true
draft: false
---

[CF 1076A - Minimizing the String](https://codeforces.com/problemset/problem/1076/A)

**Rating:** 1200  
**Tags:** greedy, strings  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string made of lowercase letters, and we are allowed to delete at most one character from it. After this optional deletion, we obtain a new string, and among all possible results (including doing nothing), we want the lexicographically smallest one.

Lexicographic order here behaves like dictionary comparison: two strings are compared character by character from the start, and the first position where they differ decides which is smaller. If one string is a prefix of the other, the shorter string is smaller.

The constraint allows the string length to be up to 200,000. That immediately rules out any solution that tries every deletion position independently and compares strings naively, since that would lead to an O(n²) behavior in the worst case. Even a linear scan repeated per position would be too slow under tight limits.

A few edge situations matter.

If the string is already non-decreasing in a lexicographic sense when viewed as a sequence where early characters are already as small as possible, removing anything might not help. For example, in `"aaa"`, every character is identical, so all deletions give the same result.

A more subtle case is when the first “drop” in the string is very late. For example, in `"abdc"`, removing either `'d'` or `'c'` can influence the lexicographic outcome, and the optimal choice depends on where the first violation of monotonicity occurs.

Another failure case for naive reasoning is assuming we should always remove the first character that is larger than the next one. For `"bcaa"`, removing `'b'` gives `"caa"`, but removing `'c'` gives `"baa"`, which is smaller.

The core difficulty is that the decision is not local. A deletion earlier in the string can dominate any benefit gained later.

## Approaches

A brute-force approach is straightforward: try deleting each position once (plus the option of deleting nothing), build the resulting string, and compare all results to find the minimum. Each candidate construction costs O(n), and there are O(n) candidates, leading to O(n²) time. With n up to 200,000, this is completely infeasible.

The key observation is that we do not actually need to compare full candidate strings. We only need to decide where removing a character will improve the first point of lexicographic divergence. This means we are looking for the earliest position where the string stops being “locally optimal”.

More precisely, we scan from left to right and look for the first index where a character is greater than the next one. At that point, keeping the current character makes the prefix worse than necessary, because we can skip it and immediately expose a smaller character earlier in the string. Once we remove that character, any later decisions no longer affect the lexicographic minimum, because lexicographic comparison is already decided by the earliest difference.

If no such position exists, the string is non-decreasing, meaning every character is less than or equal to the next. In that case, removing the last character produces the smallest result, because it reduces length without worsening lexicographic order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Traverse the string from the first character to the second last character.

We compare each character with the next one because lexicographic improvement is only possible when a larger character precedes a smaller one.
2. Find the first index `i` such that `s[i] > s[i+1]`.

This is the first point where the string stops being optimal in prefix order.
3. If such an index exists, construct the answer by removing `s[i]`.

Removing this character exposes a smaller character earlier, which guarantees the lexicographically smallest possible prefix.
4. If no such index exists, the string is non-decreasing.

In this case, removing any internal character cannot improve lexicographic order, so we remove the last character to minimize length.

### Why it works

The algorithm relies on the fact that lexicographic comparison is determined by the first differing position. The earliest index where `s[i] > s[i+1]` is the first opportunity to improve that decisive position. Removing any character before this index would only make the prefix worse or leave it unchanged, while removing any character after it cannot influence the already-determined prefix comparison. This creates a greedy optimal substructure: the first “drop” fully determines the best possible deletion point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    drop = -1
    for i in range(n - 1):
        if s[i] > s[i + 1]:
            drop = i
            break

    if drop == -1:
        print(s[:-1])
    else:
        print(s[:drop] + s[drop + 1:])

if __name__ == "__main__":
    solve()
```

The solution reads the string and scans once to find the first position where a character is larger than the next one. That index is stored as `drop`. If no such index exists, we remove the last character by slicing `s[:-1]`.

A subtle point is that we break immediately on the first violation. This is essential because later violations are irrelevant once the lexicographically critical prefix has been fixed.

## Worked Examples

### Example 1

Input: `"aaa"`

| i | s[i] | s[i+1] | drop |
| --- | --- | --- | --- |
| 0 | a | a | - |
| 1 | a | a | - |

No drop is found, so we remove last character.

Output becomes `"aa"`.

This confirms that when all characters are equal, the best move is simply reducing length.

### Example 2

Input: `"abdc"`

| i | s[i] | s[i+1] | drop |
| --- | --- | --- | --- |
| 0 | a | b | - |
| 1 | b | d | - |
| 2 | d | c | 2 |

We stop at index 2 since `d > c`. Removing `d` gives `"abc"`.

Output: `"abc"`.

This demonstrates that the first decreasing point determines the optimal deletion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to find first decreasing pair, plus O(n) slicing |
| Space | O(n) | Output string construction |

The algorithm runs comfortably within limits for n up to 200,000 because it only performs a single linear scan and one linear reconstruction of the output string.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output

    def solve():
        n = int(input())
        s = input().strip()

        drop = -1
        for i in range(n - 1):
            if s[i] > s[i + 1]:
                drop = i
                break

        if drop == -1:
            print(s[:-1])
        else:
            print(s[:drop] + s[drop + 1:])

    solve()
    sys.stdout = old_stdout
    return output.getvalue().strip()

# provided samples
assert run("3\naaa\n") == "aa"

# custom cases
assert run("2\nba\n") == "a"        # remove first char
assert run("4\nabcd\n") == "abc"    # monotone increasing
assert run("5\ncbacd\n") == "bacd"  # early drop
assert run("3\nzyx\n") == "yx"      # drop first
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `ba` | `a` | single drop at start |
| `abcd` | `abc` | strictly increasing case |
| `cbacd` | `bacd` | first inversion rule |
| `zyx` | `yx` | immediate optimal removal |

## Edge Cases

For a fully increasing string like `"abcde"`, the algorithm never finds a position where `s[i] > s[i+1]`, so `drop` stays `-1`. The code removes the last character and returns `"abcd"`, which is correct because any internal deletion would produce a lexicographically larger prefix than simply shortening the string.

For a string with an early inversion like `"za"`, the loop immediately detects `z > a` at index 0. Removing index 0 produces `"a"`, which is the smallest possible result since any other operation would keep `'z'` as a prefix and worsen the lexicographic order.

For strings with repeated characters such as `"bbbbbb"`, no inversion exists, so the algorithm removes the last character, producing `"bbbbb"`. Every possible deletion yields the same lexicographic value, and this choice preserves correctness while being consistent.
