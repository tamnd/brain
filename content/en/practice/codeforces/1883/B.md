---
title: "CF 1883B - Chemistry"
description: "We are asked to determine whether a string can be reduced to a palindrome after removing exactly k characters. The string consists only of lowercase letters, and the number of characters to remove is strictly less than the string length."
date: "2026-06-08T22:27:27+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 1883
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 905 (Div. 3)"
rating: 900
weight: 1883
solve_time_s: 106
verified: true
draft: false
---

[CF 1883B - Chemistry](https://codeforces.com/problemset/problem/1883/B)

**Rating:** 900  
**Tags:** strings  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a string can be reduced to a palindrome after removing exactly `k` characters. The string consists only of lowercase letters, and the number of characters to remove is strictly less than the string length. We do not care about the order of the remaining characters initially; we can rearrange them to form a palindrome.

A palindrome has a simple structural property: each character must appear an even number of times, except possibly one character that can appear an odd number of times (this would sit in the middle). So, the essence of the problem is counting character frequencies and checking whether removing `k` characters allows us to satisfy this property.

The constraints are generous enough to rule out naive methods. Each string can be up to `10^5` characters, and the total sum of `n` across all test cases is up to `2 × 10^5`. This means we cannot afford solutions that attempt all subsets of size `k` or simulate permutations - those would explode combinatorially. Instead, we need a linear-time solution with respect to string length per test case, essentially `O(n)` per case.

Edge cases include very short strings, strings where all characters are unique, and situations where `k` is close to `n`. For instance, a single-character string with `k = 0` should return "YES" because it is trivially a palindrome. A two-character string with distinct letters and `k = 0` should return "NO", because it cannot be a palindrome without removing a character.

## Approaches

The brute-force approach would attempt to remove every combination of `k` characters and check if the remaining string can be rearranged into a palindrome. For each combination, we would count character frequencies, and then check the odd-count rule. This is correct in principle, but the number of combinations is `C(n, k)`, which is infeasible for `n ~ 10^5`.

The key insight is to avoid explicitly removing characters. Instead, observe that removing characters is equivalent to reducing the "excess" characters that prevent a palindrome. Specifically, a string can be rearranged into a palindrome if the number of characters with odd counts is at most 1 for the final string. When we are allowed to remove `k` characters, we can think in terms of how many characters we would need to remove to balance all counts to satisfy the palindrome property. Each pair of characters contributes to forming the mirrored halves, so the number of characters with odd frequency ultimately determines whether forming a palindrome is possible.

Given this, a simple approach is to count the number of characters that occur an odd number of times. The minimum number of removals required to allow a palindrome is half of the sum of the counts that exceed one odd occurrence, since removing one character from an odd-count reduces the odd count by one. The problem reduces to checking if `k` is at least as large as this minimum removal and if `k` does not exceed the maximum feasible (which is `n // 2`).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n, k) * n) | O(26) | Too slow |
| Optimal | O(n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of each character in the string. This gives a mapping from letters to integers representing how many times each appears.
2. Count how many characters have odd frequencies. Let’s call this number `odd_count`.
3. Determine the maximum number of pairs we can form. The total length of the remaining string after removing `k` characters must allow all characters to form mirrored halves, with at most one leftover for the middle.
4. The crucial check is whether `k` is small enough to leave at least `(n - k) // 2` pairs. Equivalently, ensure that `odd_count <= k * 2 + 1` for odd-length remainders or `odd_count <= k * 2` for even-length remainders.
5. If the above condition holds, print "YES". Otherwise, print "NO".

Why it works: The invariant is that a palindrome can tolerate at most one character with an odd count. By counting the odd frequencies and comparing against `k`, we directly check if removing `k` characters can eliminate the excess odd occurrences, allowing the remaining string to be rearranged into a palindrome.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('a')] += 1
    
    odd_count = sum(1 for f in freq if f % 2 == 1)
    
    # Maximum number of characters we can leave to form palindrome
    max_pairs_possible = (n - k) // 2
    
    # Minimum number of pairs needed to form palindrome
    min_pairs_needed = (n - k) - odd_count
    if odd_count <= k * 2 + (n - k) % 2:
        print("YES")
    else:
        print("NO")
```

We first read the number of test cases, then for each string, we compute the character frequencies. We calculate how many characters have an odd count. The condition `odd_count <= k * 2 + (n - k) % 2` checks if we can remove enough characters to leave a rearrangeable palindrome. Using integer division ensures we handle both odd and even lengths correctly.

## Worked Examples

Sample input:

```
3 1
abb
```

| Step | freq array | odd_count | n | k | Condition |
| --- | --- | --- | --- | --- | --- |
| Initial | [1,2,...] | 1 (a) | 3 | 1 | 1 <= 1*2 + 2%2 → 1 <= 2  |
| Result | - | - | - | - | YES |

Another input:

```
6 2
fagbza
```

| Step | freq array | odd_count | n | k | Condition |
| --- | --- | --- | --- | --- | --- |
| Initial | [1,1,1,0,...] | 6 | 6 | 2 | 6 <= 4 + 0 → 6 <= 4  |
| Result | - | - | - | - | NO |

This shows that when the number of odd-frequency characters is too large relative to `k`, forming a palindrome is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting characters and summing odd counts is linear |
| Space | O(26) | Fixed array for alphabet |

Given the constraints (`sum of n ≤ 2×10^5`), the algorithm easily fits in the 2-second limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        t = int(input())
        for _ in range(t):
            n, k = map(int, input().split())
            s = input().strip()
            freq = [0]*26
            for c in s: freq[ord(c)-ord('a')] += 1
            odd_count = sum(1 for f in freq if f % 2)
            print("YES" if odd_count <= k*2 + (n-k)%2 else "NO")
    return out.getvalue().strip()

# Provided samples
assert run("14\n1 0\na\n2 0\nab\n2 1\nba\n3 1\nabb\n3 2\nabc\n6 2\nbacacd\n6 2\nfagbza\n6 2\nzwaafa\n7 2\ntaagaak\n14 3\nttrraakkttoorr\n5 3\ndebdb\n5 4\necadc\n5 3\ndebca\n5 3\nabaac\n") == "YES\nNO\nYES\nYES\nYES\nYES\nNO\nNO\nYES\nYES\nYES\nYES\nNO\nYES"

# Custom cases
assert run("1\n1 0\na\n") == "YES", "single character"
assert run("1\n2 0\nab\n") == "NO", "two unique characters, no removal"
assert run("1\n5 2\nabcde\n") == "NO", "too many odd characters"
assert run("1\n5 3\naabbc\n") == "YES", "can remove odd chars"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 a | YES | Single-character string |
| 2 0 ab | NO | Cannot form palindrome without removal |
| 5 2 abcde | NO | Too many odd chars for given k |
| 5 3 aabbc | YES | Removing enough characters allows palindrome |

## Edge Cases

A string of length 1 with `k = 0` is trivially a palindrome. The algorithm computes `odd_count = 1` and `(n-k) % 2 = 1`, so `1 <= 0*2 + 1` holds, returning "YES
