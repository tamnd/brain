---
title: "CF 106125D - Dralinpome"
description: "We are given a single lowercase string and asked to decide whether its letters can be rearranged to form a palindrome. The task is not to construct the palindrome, only to determine whether such a rearrangement exists."
date: "2026-06-20T01:40:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106125
codeforces_index: "D"
codeforces_contest_name: "Delft Algorithm Programming Contest 2025 (DAPC 2025)"
rating: 0
weight: 106125
solve_time_s: 52
verified: true
draft: false
---

[CF 106125D - Dralinpome](https://codeforces.com/problemset/problem/106125/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single lowercase string and asked to decide whether its letters can be rearranged to form a palindrome. The task is not to construct the palindrome, only to determine whether such a rearrangement exists.

A palindrome has the property that characters mirror around its center. This immediately constrains how many times each character may appear. Characters must be paired symmetrically, except possibly for one middle character when the length is odd.

The input length can be up to 100000, which rules out any quadratic or worse approach. Anything that tries to simulate permutations or build candidate strings would explode combinatorially. Even sorting-based constructions are fine, but anything involving rearranging all permutations is impossible.

A naive mistake appears when focusing only on whether the string itself is a palindrome rather than whether it can be permuted into one. For example, a string like `cacao` is not a palindrome as written, but it can be rearranged into `acoca`, which is valid.

Another subtle edge case is strings where multiple characters have odd frequencies. For example, `aabbcc` cannot form any palindrome because more than one character would need to occupy a center position. A careless implementation that only checks total length parity would incorrectly accept such cases.

## Approaches

A brute-force strategy would try all permutations of the string and test whether any of them is a palindrome. This is conceptually correct because it directly matches the definition of a dralinpome, but it is infeasible. The number of permutations is n factorial, and each palindrome check is linear, leading to an astronomical runtime even for moderate n like 20.

The key observation is that we do not care about arrangement, only about frequency counts. In a palindrome, characters must appear in mirrored pairs around the center. This means every character count must be even, except possibly one character which can have an odd count if the string length is odd.

So the entire problem reduces to counting how many characters appear an odd number of times. If this count is at most one, a palindrome rearrangement exists. This avoids any structural construction and compresses the problem into a single frequency pass over the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Frequency counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string by counting occurrences of each character, then evaluate how many of those counts are odd.

1. Count the frequency of every character in the string. This gives a complete summary of how many times each letter appears, independent of order.
2. Traverse the frequency table and count how many characters have an odd frequency. Each odd frequency indicates an unpaired character that would need to occupy a mirrored position in a palindrome.
3. If the number of odd-frequency characters is greater than one, immediately conclude that no palindrome rearrangement is possible.
4. Otherwise, conclude that a valid rearrangement exists.

### Why it works

A palindrome pairs characters symmetrically around its center. Every position i from the left must match a corresponding position from the right. This enforces that occurrences of each character must be divisible into pairs, except possibly one leftover character that can sit in the middle when the length is odd. If more than one character has an unpaired occurrence, there is no way to place them without breaking symmetry, so no permutation can form a palindrome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    s = input().strip()
    
    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - ord('a')] += 1
    
    odd_count = 0
    for f in freq:
        if f % 2 == 1:
            odd_count += 1
    
    if odd_count <= 1:
        print("yes")
    else:
        print("no")

if __name__ == "__main__":
    main()
```

The solution begins by reading the string and building a fixed-size frequency array for lowercase letters. This avoids dictionary overhead and keeps operations constant per character.

We then scan the 26 counts and accumulate how many are odd. The decision logic is a direct translation of the palindrome rearrangement condition.

A common implementation pitfall is using the string length parity instead of frequency parity. That is incorrect because even-length strings can still be impossible (for example `abcabcx`), and odd-length strings can still be valid.

## Worked Examples

### Example 1: `zoo`

We compute character frequencies.

| Character | Count | Odd? |
| --- | --- | --- |
| z | 1 | yes |
| o | 2 | no |

The number of odd counts is 1.

This demonstrates the case where a single middle character is allowed. The string can be rearranged into `oz o` style palindrome such as `oz o` → `ozo`.

### Example 2: `racecars`

| Character | Count | Odd? |
| --- | --- | --- |
| r | 2 | no |
| a | 2 | no |
| c | 2 | no |
| e | 1 | yes |
| s | 2 | no |

Odd count is 1, so the answer is valid.

This shows that even longer strings with structure irregularities can still form a palindrome as long as only one character is unpaired.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once, and we scan a fixed 26-size array |
| Space | O(1) | Frequency array size is constant |

The linear scan is optimal given that every character must be read at least once. The constraints allow up to 100000 characters, which is comfortably handled in a single pass.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    
    s = input().strip()
    freq = [0]*26
    for c in s:
        freq[ord(c)-97] += 1
    
    odd = 0
    for f in freq:
        if f % 2:
            odd += 1
    
    print("yes" if odd <= 1 else "no")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (conceptual, since formatting may vary)
assert run("zoo\n") == "yes"
assert run("racecars\n") == "no"

# custom cases
assert run("a\n") == "yes"
assert run("ab\n") == "no"
assert run("aabbcc\n") == "yes"
assert run("abcabcx\n") == "yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | yes | single character edge case |
| `ab` | no | multiple odd counts |
| `aabbcc` | yes | all even frequencies |
| `abcabcx` | yes | exactly one odd frequency |

## Edge Cases

A minimal string like `a` contains one character with odd frequency, and the algorithm correctly counts one odd entry and accepts it. This corresponds to a trivial palindrome.

A string like `ab` produces two odd frequencies, one for each character. The scan over the frequency array increments the odd counter twice, and the final condition rejects it, matching the impossibility of pairing both characters in a symmetric structure.

A larger structured case like `abcabcx` shows that order is irrelevant. Frequencies are `{a:2, b:2, c:2, x:1}`, so only one odd count exists. The algorithm accepts it, correctly reflecting that `abcxcba` is a valid rearrangement.
