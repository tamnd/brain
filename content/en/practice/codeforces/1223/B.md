---
title: "CF 1223B - Strings Equalization"
description: "Each query gives two strings of the same length. You are allowed to repeatedly apply an operation on either string: pick two neighboring characters and overwrite one with the other."
date: "2026-06-15T19:29:18+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 1223
codeforces_index: "B"
codeforces_contest_name: "Technocup 2020 - Elimination Round 1"
rating: 1000
weight: 1223
solve_time_s: 314
verified: true
draft: false
---

[CF 1223B - Strings Equalization](https://codeforces.com/problemset/problem/1223/B)

**Rating:** 1000  
**Tags:** strings  
**Solve time:** 5m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

Each query gives two strings of the same length. You are allowed to repeatedly apply an operation on either string: pick two neighboring characters and overwrite one with the other. This means information can flow along adjacent positions, but only by copying existing letters, not by introducing new ones.

From a structural point of view, each string behaves like a line of cells where any letter can spread across the entire string through repeated propagation. However, no operation ever introduces a character that was not already present in that string at the start.

The task is to determine whether, after any number of such propagation steps applied independently to both strings, they can be made identical.

The constraints are small: at most 100 queries, each string length up to 100. This immediately rules out any exponential exploration of transformations or state simulation over strings. Even a cubic or quadratic simulation per query would pass comfortably, but the real goal is to find the underlying invariant rather than simulate anything.

A common incorrect intuition is to think order matters or that we must match frequencies. That leads to overcomplicated reasoning. Another mistake is assuming we need to simulate shifting characters, which quickly becomes messy and still does not capture the real freedom of the operation.

A subtle edge case appears when the strings share no letters at all except indirectly through transformations. For example, if one string is composed only of `a` and the other only of `b`, there is no way to reconcile them. On the other hand, if they share even one letter, both can be turned entirely into that letter, making them trivially equal.

## Approaches

A brute force idea would attempt to model all reachable strings from `s` and from `t`. Since each position can be overwritten by neighbors repeatedly, each step branches into multiple possibilities. The number of possible strings grows exponentially with length, and even for length 100 this becomes completely infeasible.

The key observation is that the operation never creates new characters, it only copies existing ones. This means the only information that survives transformation is which distinct characters exist in each string initially. Once a character exists anywhere in a string, it can be propagated to every position, effectively erasing any structure inside the string.

This reduces each string to a simple set of letters. If the two sets have at least one letter in common, we can choose that letter as a target and propagate it across both strings independently until both become uniform. If there is no common letter, there is no way to synchronize them.

The problem therefore collapses to a set intersection check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | Exponential | Too slow |
| Set Intersection | O(n) per query | O(1) | Accepted |

## Algorithm Walkthrough

We process each query independently.

First, we scan string `s` and record which letters appear in it. We do the same for string `t`. Since the alphabet is only lowercase English letters, we can represent this using a fixed boolean array of size 26.

Next, we check whether there exists any character that appears in both sets. This is equivalent to checking whether the intersection of these two character sets is non-empty.

If we find at least one shared character, we immediately conclude that both strings can be transformed into a string consisting entirely of that character, and we output `YES`. Otherwise, we output `NO`.

### Why it works

The operation allows unrestricted propagation of any existing character across the entire string. This makes every character in the initial string effectively globally available within that string. Since no new characters can ever appear, the only constraint on a final common string is that every character used must exist in both original strings. A single shared character is sufficient because it can be expanded to fill both strings completely.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    out = []
    
    for _ in range(q):
        s = input().strip()
        t = input().strip()
        
        seen_s = [False] * 26
        seen_t = [False] * 26
        
        for ch in s:
            seen_s[ord(ch) - 97] = True
        for ch in t:
            seen_t[ord(ch) - 97] = True
        
        ok = False
        for i in range(26):
            if seen_s[i] and seen_t[i]:
                ok = True
                break
        
        out.append("YES" if ok else "NO")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution processes each query independently. For each string, it builds a presence array over the alphabet. The final loop checks for any shared index. The early exit ensures constant-time behavior once a common character is found.

A common implementation mistake is trying to compare full strings or frequencies. Frequencies are irrelevant because the operation does not preserve counts. Another mistake is attempting to simulate transformations step by step, which is unnecessary since reachability depends only on character existence.

## Worked Examples

Consider a query where `s = "xabb"` and `t = "aabx"`.

We track character sets as follows.

| Step | s characters | t characters | Common character found |
| --- | --- | --- | --- |
| After scan | {x, a, b} | {a, b, x} | yes |

Since there is at least one shared character, both strings can be reduced to all `a` for example, so the answer is `YES`.

Now consider `s = "a"` and `t = "z"`.

| Step | s characters | t characters | Common character found |
| --- | --- | --- | --- |
| After scan | {a} | {z} | no |

There is no overlap, so no sequence of allowed operations can bridge the gap, giving `NO`.

The first example demonstrates that structure and ordering are irrelevant, while the second shows that disjoint alphabets make transformation impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 · q · n) | Each string is scanned once and alphabet checks are constant |
| Space | O(1) | Fixed-size boolean arrays for alphabet tracking |

Given the constraints of at most 100 queries and string length up to 100, this runs trivially within limits. The operations are effectively constant-factor work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    q = int(input())
    out = []
    for _ in range(q):
        s = input().strip()
        t = input().strip()
        seen_s = [False]*26
        seen_t = [False]*26
        for ch in s:
            seen_s[ord(ch)-97] = True
        for ch in t:
            seen_t[ord(ch)-97] = True
        ok = False
        for i in range(26):
            if seen_s[i] and seen_t[i]:
                ok = True
                break
        out.append("YES" if ok else "NO")
    return "\n".join(out)

assert run("""3
xabb
aabx
technocup
technocup
a
z
""") == """YES
YES
NO"""

assert run("""2
abc
def
abc
a
""") == """NO
YES"""

assert run("""1
zzzz
zzzz
""") == """YES"""

assert run("""1
ab
cd
""") == """NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed overlap cases | YES/NO mix | correctness of intersection logic |
| disjoint alphabets | NO | impossible transformation case |
| identical strings | YES | identity preservation |
| full mismatch small case | NO | base edge behavior |

## Edge Cases

One edge case occurs when both strings are already identical. For input like `s = "abba"` and `t = "abba"`, the algorithm marks the same set of characters for both strings, so the intersection is non-empty and the output is `YES`. The process does not rely on equality but still correctly accepts it.

Another edge case is when strings contain repeated characters but disjoint sets, such as `s = "aaaa"` and `t = "bbbb"`. Even though both are uniform, there is no shared character, so no propagation sequence can reconcile them. The algorithm correctly returns `NO` because the intersection check fails immediately.

A third case is when strings are long but share exactly one letter, such as `s = "abcabc..."` and `t = "zzzazzz..."`. Even though most characters differ, the shared `a` is sufficient to collapse both strings into a uniform string of `a`, which the algorithm captures through the non-empty intersection condition.
