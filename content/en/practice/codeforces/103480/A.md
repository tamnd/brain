---
title: "CF 103480A - \u89e3\u5f00\u675f\u7f1a\u7f20\u4e1d\u2161"
description: "We are given several test cases. In each case, we receive a multiset of single characters. Each character can be used at most once, and we are allowed to rearrange the chosen characters in any order."
date: "2026-07-03T06:30:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103480
codeforces_index: "A"
codeforces_contest_name: "The 4th Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 103480
solve_time_s: 41
verified: true
draft: false
---

[CF 103480A - \u89e3\u5f00\u675f\u7f1a\u7f20\u4e1d\u2161](https://codeforces.com/problemset/problem/103480/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases. In each case, we receive a multiset of single characters. Each character can be used at most once, and we are allowed to rearrange the chosen characters in any order. The goal is to select some subset of these characters and arrange them into a string that is a palindrome, maximizing the length of that palindrome.

A palindrome is fully determined by how many characters can be paired symmetrically around the center, plus possibly one unpaired character placed in the middle. This structure forces the core constraint: characters contribute to a palindrome only through pairs, except for at most one leftover character that can sit in the center.

The input size allows up to 10 test cases, each with up to 100,000 characters. This immediately rules out any solution that tries to construct permutations or perform combinatorial search. A linear scan per test case is acceptable, but anything quadratic in the number of characters per test case would exceed limits.

A subtle edge case appears when all characters are distinct. For example, input like `A B C D` allows only one character in the palindrome, because no pairs exist. Another edge case is when one character appears many times and others appear once, for instance `a a a b c`. Here, the best palindrome uses all even pairs of `a` and ignores singletons except possibly one center character. A naive approach that greedily alternates or tries to “build outward” without counting frequencies would miscount these contributions.

## Approaches

The brute-force idea is to consider all subsets of characters and all permutations of each subset, checking whether each arrangement forms a palindrome and tracking the maximum length. This is conceptually straightforward because it explores the entire search space of valid constructions. However, even choosing subsets alone already gives 2^n possibilities, and permutations multiply this by factorial growth. With n up to 100,000, this approach is infeasible.

The structure of a palindrome simplifies the problem significantly. A palindrome is determined entirely by character frequencies, not ordering. Each character contributes as many mirrored pairs as possible. Every pair contributes two characters to the final answer. After forming all possible pairs, if at least one character remains unused, we can place exactly one such character in the center, increasing the length by one.

This reduces the problem from combinatorial arrangement to frequency counting. The key observation is that optimal construction never depends on which specific positions are chosen, only how many pairs can be formed across all letters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Frequency Counting | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many times each character appears in the input. This captures all relevant structure because arrangement is irrelevant once frequencies are known.
2. For each character frequency, compute how many full pairs can be formed by taking the integer division by 2. Each pair contributes exactly two characters to the palindrome.
3. Sum all these pair contributions multiplied by 2. This gives the total length contributed by symmetric sides of the palindrome.
4. Track whether there exists at least one character with an odd remaining count after pairing. This indicates that at least one character can serve as a center.
5. If any odd remainder exists, add one to the answer to place a central character.
6. Output the final computed length.

Why it works: the construction of a palindrome enforces symmetry, so every character used on the left side must have a matching counterpart on the right side. This partitions usage into disjoint pairs. Any leftover characters cannot be symmetrically placed except for one, which becomes the center. Since pairing is independent per character and maximized greedily per frequency, the resulting construction is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        freq = {}
        
        arr = input().split()
        for c in arr:
            freq[c] = freq.get(c, 0) + 1
        
        length = 0
        has_odd = False
        
        for v in freq.values():
            length += (v // 2) * 2
            if v % 2 == 1:
                has_odd = True
        
        if has_odd:
            length += 1
        
        print(length)

if __name__ == "__main__":
    solve()
```

The solution is structured around a single pass frequency accumulation. The dictionary stores counts for each character, which is sufficient since characters are independent.

The key computation is `(v // 2) * 2`, which converts frequency into usable symmetric contribution. Multiplying by 2 explicitly avoids losing clarity about left-right pairing.

The boolean `has_odd` is critical because it encodes whether we can place a center character. Any single odd occurrence across all characters is enough, since only one center slot exists.

## Worked Examples

### Example 1

Input:

```
1
3
a v a
```

We track frequencies:

| Character | Frequency | Pairs used | Contribution | Odd leftover |
| --- | --- | --- | --- | --- |
| a | 2 | 1 | 2 | no |
| v | 1 | 0 | 0 | yes |

Total symmetric length is 2. Since there is an odd leftover (`v`), we add 1 center character.

Final answer is 3.

This confirms that multiple different characters can still contribute correctly, even if only one of them becomes the center.

### Example 2

Input:

```
1
4
A a b c
```

Frequencies are all 1.

| Character | Frequency | Pairs used | Contribution | Odd leftover |
| --- | --- | --- | --- | --- |
| A | 1 | 0 | 0 | yes |
| a | 1 | 0 | 0 | yes |
| b | 1 | 0 | 0 | yes |
| c | 1 | 0 | 0 | yes |

Symmetric length is 0. At least one odd exists, so we place one center character.

Final answer is 1.

This demonstrates the extreme case where no pairing is possible, and the palindrome degenerates to a single character.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is counted once, and each frequency is processed once |
| Space | O(k) | k is number of distinct characters, bounded by alphabet size |

The constraints allow up to 100,000 characters per test case, so a linear scan comfortably fits within the time limit. Memory usage is minimal since only a frequency map over characters is stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    input = stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = input().split()
        freq = {}
        for c in arr:
            freq[c] = freq.get(c, 0) + 1

        length = 0
        has_odd = False
        for v in freq.values():
            length += (v // 2) * 2
            if v % 2:
                has_odd = True
        if has_odd:
            length += 1

        out.append(str(length))

    return "\n".join(out)

# provided samples (interpreted)
assert run("2\n1\nA\n3\na v a\n") == "1\n3"

# all same character
assert run("1\n5\na a a a a\n") == "5"

# no pairs at all
assert run("1\n4\na b c d\n") == "1"

# mixed frequencies
assert run("1\n6\na a b b b c\n") == "5"

# maximum-like balanced
assert run("1\n8\na a b b c c d d\n") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all identical letters | full length | maximal pairing case |
| all distinct letters | 1 | only center possible |
| mixed frequencies | correct pair aggregation | uneven distribution |
| perfectly balanced pairs | full usage | no leftovers |

## Edge Cases

One important edge case is when there are no repeated characters. For input like `a b c d`, the frequency map produces all ones. The algorithm computes zero from pair contributions and detects at least one odd value, so it correctly outputs 1.

Another case is when exactly one character has a large frequency and others are singletons, such as `a a a a b c d`. The algorithm forms two pairs from `a`, contributing 4, and uses one of the singletons as the center, giving 5. The remaining singletons do not affect the result because they cannot form additional pairs.

A final edge case is a single-element input. With input `A`, the pair sum is zero and an odd exists, so the answer becomes 1, which matches the only possible palindrome.
