---
title: "CF 223A - Bracket Sequence"
description: "We are given a string consisting only of four bracket characters: (, ), [ and ]. The string is not necessarily balanced. Among all substrings of this string, we need to find one that forms a correct bracket sequence."
date: "2026-06-04T05:41:47+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 223
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 138 (Div. 1)"
rating: 1700
weight: 223
solve_time_s: 108
verified: true
draft: false
---

[CF 223A - Bracket Sequence](https://codeforces.com/problemset/problem/223/A)

**Rating:** 1700  
**Tags:** data structures, expression parsing, implementation  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting only of four bracket characters: `(`, `)`, `[` and `]`. The string is not necessarily balanced.

Among all substrings of this string, we need to find one that forms a correct bracket sequence. A correct bracket sequence must satisfy the usual nesting rules, meaning every opening bracket is matched by a closing bracket of the same type and the pairs are properly nested.

The objective is not to maximize the length of the substring. Instead, we want the valid substring containing the largest number of opening square brackets `'['`. After finding such a substring, we must output both the count of `'['` characters inside it and the substring itself.

The string length can reach $10^5$. A quadratic algorithm would require examining roughly $10^{10}$ substrings, which is completely infeasible. Even an $O(n^2)$ validation strategy is far beyond the time limit. The solution must be close to linear time.

Several edge cases make the problem trickier than ordinary bracket matching.

Consider:

```
([)]
```

The substring spans balanced counts of brackets, but it is not a correct bracket sequence because the nesting order is wrong. Any solution based only on counting bracket types would incorrectly accept it.

Consider:

```
][
```

There is no non-empty correct substring. The answer must be:

```
0
```

with an empty second line. A careless implementation might try to output one of the characters.

Consider:

```
[]()[]
```

The whole string is valid and contains two `'['` characters. If we only search for the longest valid substring, we would still succeed here, but in general the optimum is determined by the number of `'['`, not by length.

Consider:

```
([[]])
```

The entire string is valid and contains two opening square brackets. A solution must correctly count square brackets inside nested structures, not merely at the top level.

## Approaches

The brute-force idea is straightforward. Enumerate every substring, check whether it is a correct bracket sequence, count how many `'['` characters it contains, and keep the best one.

Correctness is immediate because every candidate substring is examined. The problem is the cost. There are $O(n^2)$ substrings. Even if validity checking took only $O(n)$, the total complexity becomes $O(n^3)$. With $n = 10^5$, this is hopeless.

The key observation is that we do not need to validate every substring independently.

A correct bracket sequence can be recognized using the standard stack process. While scanning the string from left to right, each closing bracket either matches the current stack top or breaks the validity of any substring crossing that position.

This is very similar to the classic "longest valid parentheses" problem. We can maintain a stack of opening brackets together with their positions. Whenever a matching pair is found, we obtain a valid segment ending at the current position. By tracking the nearest position that invalidates a segment, we can determine the maximal valid substring ending at every index.

The remaining requirement is maximizing the number of `'['` characters. This can be handled with a prefix sum array. Once we know the boundaries of a valid substring, the number of opening square brackets inside it is obtained in constant time.

The stack identifies all maximal valid segments in linear time, and the prefix sums allow efficient scoring of each candidate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array where `pref[i]` stores the number of `'['` characters among the first `i` characters.

This allows counting opening square brackets inside any substring in constant time.
2. Maintain a stack containing pairs `(position, bracket)` for unmatched opening brackets.
3. Maintain an array `dp` where `dp[i]` represents the length of the longest correct bracket sequence ending exactly at position `i`.
4. Scan the string from left to right.
5. When an opening bracket is encountered, push its position and type onto the stack.
6. When a closing bracket is encountered, check whether the stack top contains the matching opening bracket.

If not, clear the stack. Any future valid substring cannot cross this mismatched position.
7. If a match exists, pop the opening bracket position `j`.
8. The pair `(j, i)` forms a valid block. Set:

```
dp[i] = i - j + 1
```
9. If there is a valid block ending immediately before `j`, extend through it:

```
dp[i] += dp[j - 1]
```

This merges adjacent valid pieces into one larger valid substring.
10. The valid substring ending at `i` has left boundary:

```
L = i - dp[i] + 1
```
11. Count opening square brackets inside this substring using the prefix sums:

```
count = pref[i + 1] - pref[L]
```
12. If this count is larger than the best answer found so far, store the substring boundaries.
13. After processing all positions, output the best count and the corresponding substring.

### Why it works

The stack guarantees that every matched pair respects the nesting rules of a correct bracket sequence. Whenever a mismatch occurs, all partially constructed sequences crossing that position become impossible, so clearing the stack is correct.

For every closing bracket that successfully matches an opening bracket at position `j`, the segment from `j` to the current position is valid. If another valid segment ends immediately before `j`, concatenating the two segments remains valid, which is exactly what the `dp` extension step captures.

Thus `dp[i]` always equals the length of the longest valid bracket substring ending at position `i`. Every maximal valid substring appears as one of these candidates. Since the prefix sums compute the number of `'['` characters inside each candidate exactly, the algorithm examines all relevant valid substrings and selects the one with the maximum score.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    pref = [0] * (n + 1)
    for i, ch in enumerate(s):
        pref[i + 1] = pref[i] + (1 if ch == '[' else 0)

    dp = [0] * n
    stack = []

    best_count = 0
    best_l = 0
    best_r = -1

    match = {
        ')': '(',
        ']': '['
    }

    for i, ch in enumerate(s):
        if ch in '([':
            stack.append((i, ch))
        else:
            if stack and stack[-1][1] == match[ch]:
                j, _ = stack.pop()

                dp[i] = i - j + 1
                if j > 0:
                    dp[i] += dp[j - 1]

                l = i - dp[i] + 1
                cnt = pref[i + 1] - pref[l]

                if cnt > best_count:
                    best_count = cnt
                    best_l = l
                    best_r = i
            else:
                stack.clear()

    print(best_count)
    if best_r >= best_l:
        print(s[best_l:best_r + 1])
    else:
        print()

if __name__ == "__main__":
    solve()
```

The prefix sum section allows constant-time counting of opening square brackets inside any interval. Without it, we would need to scan every candidate substring again, increasing the complexity.

The stack stores both the bracket type and its position. The position is required because once a match is found, we need the exact start of the newly formed valid block.

The `dp` array is the same idea used in classic valid-parentheses problems. When a pair matches between positions `j` and `i`, the segment length is initially `i - j + 1`. If another valid sequence ends at `j - 1`, the two segments are adjacent and can be merged, so we add `dp[j - 1]`.

The left boundary is reconstructed from the length:

```
left = i - dp[i] + 1
```

This avoids storing boundaries explicitly for every state.

A subtle point is clearing the stack on mismatches. Leaving unmatched opening brackets in the stack would allow future matches to cross an invalid position, producing substrings that are not actually correct bracket sequences.

## Worked Examples

### Example 1

Input:

```
([])
```

| i | char | stack after step | dp[i] | valid substring | '[' count |
| --- | --- | --- | --- | --- | --- |
| 0 | ( | [(0,'(')] | 0 | - | - |
| 1 | [ | [(0,'('),(1,'[')] | 0 | - | - |
| 2 | ] | [(0,'(')] | 2 | [] | 1 |
| 3 | ) | [] | 4 | ([]) | 1 |

The best candidate first becomes `[]`, then expands to the whole string. The final answer is one opening square bracket and substring `([])`.

### Example 2

Input:

```
([)]
```

| i | char | stack after step | dp[i] |
| --- | --- | --- | --- |
| 0 | ( | [(0,'(')] | 0 |
| 1 | [ | [(0,'('),(1,'[')] | 0 |
| 2 | ) | [] | 0 |
| 3 | ] | [] | 0 |

At position 2, `)` does not match `'['`, so the stack is cleared. No valid substring survives across this position. The answer remains zero.

This example demonstrates why bracket counts alone are insufficient. The nesting order matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once, each stack element is pushed and popped at most once |
| Space | O(n) | Prefix sums, DP array, and stack may all contain O(n) elements |

With $n \le 10^5$, linear time easily fits within the 2-second limit. The memory usage is also comfortably below the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    s = inp.strip()

    n = len(s)

    pref = [0] * (n + 1)
    for i, ch in enumerate(s):
        pref[i + 1] = pref[i] + (ch == '[')

    dp = [0] * n
    stack = []

    best_count = 0
    best_l = 0
    best_r = -1

    match = {')': '(', ']': '['}

    for i, ch in enumerate(s):
        if ch in '([':
            stack.append((i, ch))
        else:
            if stack and stack[-1][1] == match[ch]:
                j, _ = stack.pop()

                dp[i] = i - j + 1
                if j > 0:
                    dp[i] += dp[j - 1]

                l = i - dp[i] + 1
                cnt = pref[i + 1] - pref[l]

                if cnt > best_count:
                    best_count = cnt
                    best_l = l
                    best_r = i
            else:
                stack.clear()

    out = str(best_count) + "\n"
    if best_r >= best_l:
        out += s[best_l:best_r + 1] + "\n"
    else:
        out += "\n"

    return out

# provided sample
assert run("([])\n") == "1\n([])\n", "sample 1"

# custom cases
assert run("][\n") == "0\n\n", "no valid substring"

assert run("[]\n") == "1\n[]\n", "minimum non-empty valid sequence"

assert run("([[]])\n") == "2\n([[]])\n", "nested square brackets"

assert run("()()\n") == "0\n\n", "valid sequence but no square brackets"

assert run("[]()[]\n") == "2\n[]()[]\n", "whole string optimal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `][` | `0` and empty string | No valid substring exists |
| `[]` | `1`, `[]` | Smallest useful valid sequence |
| `([[]])` | `2`, `([[]])` | Nested matching brackets |
| `()()` | `0` and empty string | Valid substring exists but contains no `[` |
| `[]()[]` | `2`, `[]()[]` | Concatenation of valid segments |

## Edge Cases

Consider:

```
([)]
```

Processing reaches `)` while the stack top is `'['`. The brackets do not match, so the stack is cleared. No future substring may extend across this position. Every `dp` value remains zero and the answer is correctly reported as zero.

Consider:

```
][
```

The first character is a closing bracket with no matching opener. The stack is empty and remains empty. The second character is merely pushed but never matched. No valid substring is discovered, so the output is:

```
0
```

Consider:

```
()()
```

The entire string is a correct bracket sequence, but it contains no opening square brackets. The best count remains zero. The official solution also outputs an empty string in this situation because no valid substring has a strictly positive score. The algorithm naturally produces that behavior.

Consider:

```
([[]])
```

The matches occur in the order `[ ]`, `[ ]`, then `( )`. Each successful match extends earlier valid blocks through the `dp[j - 1]` transition. The final valid substring becomes the entire string, and the prefix sum correctly counts two opening square brackets.
