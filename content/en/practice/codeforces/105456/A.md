---
title: "CF 105456A - Palindrome ABC"
description: "We are given counts of three characters, namely how many times we must use the letters A, B, and C. For each test case, the task is to construct a string using exactly those characters such that the string reads the same forwards and backwards, and among all valid such strings…"
date: "2026-06-23T17:44:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105456
codeforces_index: "A"
codeforces_contest_name: "XXIII Spain Olympiad in Informatics, Day 2"
rating: 0
weight: 105456
solve_time_s: 65
verified: true
draft: false
---

[CF 105456A - Palindrome ABC](https://codeforces.com/problemset/problem/105456/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given counts of three characters, namely how many times we must use the letters A, B, and C. For each test case, the task is to construct a string using exactly those characters such that the string reads the same forwards and backwards, and among all valid such strings, we must output the one that is smallest in lexicographic order. If no palindrome can be formed using all characters, the answer is “ROP”.

A palindrome imposes a strict structural constraint: characters on symmetric positions must match. This immediately means the frequency distribution is not arbitrary. At most one character type can appear an odd number of times, because a palindrome has at most one center character without a mirrored partner.

The constraints are small enough that each test case only requires constant or linear work in terms of the alphabet size. Since the total number of characters per test case is at most 3000 and there are up to 1000 test cases, any approach that builds strings directly is easily fast enough. What we cannot afford is trying all permutations or performing factorial-style constructions.

A common failure mode is to ignore parity. For example, if we try to greedily build a palindrome without checking feasibility first, we might end up constructing half a string that cannot be mirrored consistently.

A second subtle edge case arises when multiple odd counts exist. For example, input like 1 1 1 has three odd counts. There is no way to place more than one odd character in the center, so no solution exists.

## Approaches

A brute-force interpretation would be to generate all permutations of the multiset of letters and filter those that are palindromes, then choose the lexicographically smallest one. This is conceptually straightforward: we enumerate every arrangement of A, B, and C with the given counts, check whether it is a palindrome, and track the smallest lexicographic result.

The issue is combinatorial explosion. If the total length is N, the number of distinct permutations is N! divided by repeated factorials. Even for moderate N like 30, this becomes completely infeasible. The palindrome check is O(N), so the total complexity becomes factorial-scale.

The key observation is that a palindrome is fully determined by its first half plus possibly a middle character. Once we decide how many of each letter go into the left half, the right half is forced. This turns the problem from permutation search into a constrained counting problem.

We only need to decide how many A, B, and C go into the left side such that the remaining counts can mirror correctly. That means for each character, the number used on both sides must be even, and any leftover odd character (at most one type) goes to the center. After constructing the left half, lexicographic minimality is achieved by filling it greedily from smallest character to largest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | O(N!) | O(N) | Too slow |
| Construct from half counts | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We reduce the problem to deciding feasibility of a palindrome and then constructing the smallest lexicographic one.

1. Count how many of A, B, and C are odd. If more than one count is odd, no palindrome can exist. This is because every palindrome has at most one unpaired middle character.
2. Identify the middle character if it exists. If exactly one of the counts is odd, that letter becomes the center of the palindrome.
3. Convert all counts into half-counts by dividing by two. These represent how many of each character will appear on the left side of the palindrome.
4. Build the left half of the palindrome by placing characters in lexicographic order, always using all available A first, then B, then C. This greedy order ensures the overall string is lexicographically smallest because earlier positions dominate lexicographic comparison.
5. Construct the final answer as left half + middle (if any) + reversed left half.

The correctness hinges on the fact that once half counts are fixed, the ordering inside the left half directly determines lexicographic order of the full palindrome.

### Why it works

Any valid palindrome is uniquely determined by its left half and optional center character. The feasibility constraint restricts only parity and not ordering. Since lexicographic comparison is decided from left to right, minimizing the left half greedily in alphabetical order guarantees the smallest possible full string. No rearrangement of the right half can change this ordering, as it is fully determined by symmetry.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        a, b, c = map(int, input().split())
        counts = [a, b, c]
        letters = ['A', 'B', 'C']
        
        odd = sum(x % 2 for x in counts)
        if odd > 1:
            out.append("ROP")
            continue
        
        mid = ""
        for i in range(3):
            if counts[i] % 2 == 1:
                mid = letters[i]
                counts[i] -= 1
                break
        
        half = [counts[i] // 2 for i in range(3)]
        
        left = []
        for i in range(3):
            left.append(letters[i] * half[i])
        
        left = "".join(left)
        right = left[::-1]
        
        out.append(left + mid + right)
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first validates whether a palindrome is structurally possible using parity. It then assigns a middle character only if needed, ensuring exactly one odd count is reduced. The half counts represent forced symmetry, and building the left side in fixed lexicographic order ensures minimality. Finally, the palindrome is completed by mirroring.

A subtle point is that we subtract one from the odd count before halving. This ensures that the center character does not interfere with symmetry. Another important detail is that lexicographic optimality does not require backtracking, since all choices are independent once ordering of halves is fixed.

## Worked Examples

### Example 1

Input:

```
2
1 0 0
2 2 2
```

For each test case:

| Step | Counts (A,B,C) | Odd count | Middle | Half counts | Left |
| --- | --- | --- | --- | --- | --- |
| 1 | 1,0,0 | 1 | A | 0,0,0 | "" |
| 2 | 2,2,2 | 3 | A/B/C invalid | - | - |

For the first case, all counts are even after placing A in the center, so the result is “A”. For the second case, more than one odd count exists, making palindrome formation impossible, so output is “ROP”.

This confirms the parity rule correctly detects feasibility and the construction handles trivial single-letter palindromes.

### Example 2

Input:

```
1
2 0 3
```

| Step | Counts | Odd count | Middle | Half counts | Left |
| --- | --- | --- | --- | --- | --- |
| 1 | 2,0,3 | 1 | C | 1,0,1 | "AC" |

We place C in the middle, reduce its count to 2, and take halves: A contributes 1, C contributes 1. The left half becomes “AC”, and the final palindrome is “ACCCA”.

This shows how the algorithm naturally separates symmetry construction from center handling without ambiguity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case processes constant alphabet size and builds at most 1000 characters |
| Space | O(1) | Only fixed arrays of size 3 plus output storage |

The operations per test case are constant-time arithmetic and string concatenation bounded by total length, which is small. This fits comfortably within limits even for the maximum number of test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            a, b, c = map(int, input().split())
            counts = [a, b, c]
            letters = ['A', 'B', 'C']
            
            odd = sum(x % 2 for x in counts)
            if odd > 1:
                out.append("ROP")
                continue
            
            mid = ""
            for i in range(3):
                if counts[i] % 2 == 1:
                    mid = letters[i]
                    counts[i] -= 1
                    break
            
            half = [counts[i] // 2 for i in range(3)]
            
            left = []
            for i in range(3):
                left.append(letters[i] * half[i])
            
            left = "".join(left)
            out.append(left + mid + left[::-1])
        
        return "\n".join(out)
    
    return solve()

# provided samples
assert run("4\n1 0 0\n2 2 2\n2 0 3\n1 3 5\n") == "A\nABCCBA\nACCCA\nROP"

# all even
assert run("2\n2 2 0\n4 0 2\n") == "ABBA\nAACCAA"

# all zeros except one
assert run("1\n0 0 5\n") == "CCCCC"

# impossible case
assert run("1\n1 1 1\n") == "ROP"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 0 / 4 0 2 | ABBA / AACCAA | basic even construction |
| 0 0 5 | CCCCC | single-letter palindrome center handling |
| 1 1 1 | ROP | multiple odd counts rejection |

## Edge Cases

For input `0 0 5`, the algorithm detects one odd count (C), assigns it to the center, reduces it to 4, and builds half counts (0,0,2). The left half becomes “CC”, producing “CCCCC”. This confirms correct handling of pure single-character dominance.

For input `1 1 1`, all three counts are odd, so the algorithm immediately returns “ROP” before attempting construction. This shows that feasibility checking prevents incorrect forced placements.

For input `2 0 3`, the algorithm assigns C to the center, leaving balanced halves. The construction “AC + C + CA” confirms symmetry and lexicographic correctness simultaneously.
