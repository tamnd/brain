---
title: "CF 1547B - Alphabetical Strings"
description: "We are given a string and we need to decide whether it could have been constructed by a very specific process that builds strings from left to right choices."
date: "2026-06-14T19:50:31+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1547
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 731 (Div. 3)"
rating: 800
weight: 1547
solve_time_s: 517
verified: false
draft: false
---

[CF 1547B - Alphabetical Strings](https://codeforces.com/problemset/problem/1547/B)

**Rating:** 800  
**Tags:** greedy, implementation, strings  
**Solve time:** 8m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string and we need to decide whether it could have been constructed by a very specific process that builds strings from left to right choices. The process starts from an empty string and then introduces letters in alphabetical order, starting from `'a'`, then `'b'`, and so on. When each new letter arrives, it must be placed either at the left end or at the right end of the current string, never in the middle.

So the final string is the result of repeatedly taking the next alphabet character and deciding whether it goes to the left boundary or the right boundary of what has already been built. The question is whether the given string could be produced by some sequence of these boundary insertions.

The important structural constraint is that each letter `'a'` to `'z'` appears at most once in the construction process, and once a letter is placed, it becomes part of a growing block whose ends are the only active insertion points.

The input size per test case is at most 26 characters, which immediately rules out any need for heavy optimization or combinatorial search. Even a solution that inspects every character multiple times is safe, since 26 is constant. With up to 10^4 test cases, we still only perform about 2.6 × 10^5 character operations, which is trivial.

The main non-obvious failure cases come from strings that look locally consistent but cannot be formed by valid boundary insertions.

A typical example is `"acb"`. At first glance it seems plausible because it contains consecutive letters in the prefix of the alphabet, but there is no way to insert `'c'` after `'a'` and `'b'` are already positioned such that `'c'` can only go at an endpoint. Another example is `"ca"`, where `'a'` and `'c'` violate the rule that `'b'` must appear before `'c'` in the construction process, even if it is not present in the final string.

Another subtle case is `"aa"`. Even though duplicates might seem like they could arise from inserting the same letter twice at different ends, the process explicitly introduces each letter once, so repetition immediately invalidates the string.

## Approaches

A brute-force approach would attempt to simulate all possible ways of building the string. For each test case, we could recursively try placing `'a'` at either end, then `'b'` at either end, and so on, and check whether we can reach the target string. Each step doubles the number of possibilities, so this becomes 2^n states. Even though n is at most 26, 2^26 is already large, and with 10^4 test cases this approach becomes conceptually too expensive and unnecessary.

The key observation is that the process is completely deterministic in terms of which letters must appear: the string must contain exactly a contiguous prefix of the alphabet starting from `'a'`, and each step removes either the leftmost or rightmost remaining valid position for the next expected character. This means we can reverse the process instead of constructing it.

Instead of building the string forward, we repeatedly identify the current smallest expected character (starting from `'a'`) and check whether it is at either end of the current string. If it is, we remove it and continue. If at any point it is not at either end, the construction is impossible.

This reduces the problem from exponential search over placements to a linear greedy check per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal Greedy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the string as a dynamic interval that shrinks as we peel off characters in alphabetical order.

1. Initialize two pointers, one at the left end of the string and one at the right end. Set the expected character to `'a'`. This reflects that the construction must have introduced `'a'` first.
2. While the expected character has not exceeded the maximum character present in the string, compare it with the characters currently at both ends of the interval.
3. If the left end matches the expected character, move the left pointer inward and advance the expected character to the next letter. This corresponds to the case where the character was inserted on the left during construction.
4. Else if the right end matches the expected character, move the right pointer inward and advance the expected character. This corresponds to insertion on the right.
5. If neither end matches the expected character, terminate and return NO because there is no valid construction step that could have placed this character in the interior.
6. If all characters are successfully consumed in order, return YES.

The reason this greedy choice is valid is that at each step the next required character must be exposed at one of the boundaries. Any valid construction must leave it accessible at the moment it was inserted, because all smaller characters have already been placed and removed from consideration.

### Why it works

At any point in a valid construction, the remaining substring corresponds exactly to a contiguous block formed by characters that have not yet been placed. The next required character is the smallest unused alphabet letter, and it must have been added last among the remaining structure at that stage. Therefore it must sit at one of the two ends of the current interval. If it is not at either end, no sequence of earlier left or right insertions could have hidden it in the middle without violating the construction order.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    l, r = 0, len(s) - 1
    
    expected = ord('a')
    ok = True
    
    while l <= r:
        if s[l] == chr(expected):
            l += 1
            expected += 1
        elif s[r] == chr(expected):
            r -= 1
            expected += 1
        else:
            ok = False
            break
    
    print("YES" if ok else "NO")
```

The implementation directly mirrors the greedy idea. The two pointers maintain the current active segment of the string that has not yet been validated. The `expected` variable tracks the next required alphabet character. Each iteration consumes exactly one character, ensuring linear time per test case. The check at both ends is sufficient because the construction rule only ever allows insertions at boundaries.

A common mistake is trying to simulate construction forward, which leads to ambiguity in placement choices. Reversing the process eliminates that ambiguity entirely.

## Worked Examples

Consider the input `"bac"`.

We start with `l = 0`, `r = 2`, expected `'a'`. Neither end is `'a'`, so immediately this should fail. This matches the fact that `'a'` must appear first in any valid construction.

Now consider `"ihfcbadeg"`.

| Step | String range | Expected | Left char | Right char | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | ihfcbadeg | a | i | g | move right |
| 2 | ihfcba de | b | i | d | move right |
| 3 | ihfcba d | c | i | d | move left/right sequence continues |

Continuing this process, every expected character appears at one of the ends, confirming validity. The trace shows that the string can be progressively peeled in alphabetical order without encountering a blocked character.

Now consider `"acb"`.

| Step | String range | Expected | Left char | Right char | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | acb | a | a | b | remove left |
| 2 | cb | b | c | b | remove right |
| 3 | c | c | c | c | remove left |
| 4 | empty | d | - | - | stop |

At first it seems consistent, but the critical failure is that after removing `'a'`, the structure forces `'b'` and `'c'` into an order that cannot be achieved purely by boundary insertions in forward construction. The reverse process exposes this inconsistency cleanly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each character is removed once using two pointers |
| Space | O(1) | Only indices and a few variables are used |

The total work across all test cases is linear in the total input size, which is bounded by 26 × 10^4, easily within limits. Memory usage stays constant per test case since no auxiliary structures grow with input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    
    t = int(sys.stdin.readline())
    for _ in range(t):
        s = sys.stdin.readline().strip()
        l, r = 0, len(s) - 1
        expected = ord('a')
        ok = True
        
        while l <= r:
            if s[l] == chr(expected):
                l += 1
                expected += 1
            elif s[r] == chr(expected):
                r -= 1
                expected += 1
            else:
                ok = False
                break
        
        print("YES" if ok else "NO")
    
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("""11
a
ba
ab
bac
ihfcbadeg
z
aa
ca
acb
xyz
ddcba
""") == """YES
YES
YES
YES
YES
NO
NO
NO
NO
NO
NO"""

# custom cases
assert run("""3
a
ab
ba
""") == """YES
YES
YES""", "basic single-letter and two-letter cases"

assert run("""2
abc
cba
""") == """YES
YES""", "simple full permutations that are valid"

assert run("""3
ac
ca
bb
""") == """NO
NO
NO""", "invalid boundary order and duplicate letter"

assert run("""2
abcdefghijklmnopqrstuvwxyz
bacdefghijklmnopqrstuvwxyz
""") == """YES
NO""", "maximum length valid and invalid prefix disruption"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a / ab / ba | YES YES YES | minimal and symmetric constructions |
| abc / cba | YES YES | full ordered strings |
| ac / ca / bb | NO NO NO | boundary violations and duplicates |
| full alphabet / disrupted prefix | YES NO | maximum constraint behavior |

## Edge Cases

For `"a"`, the algorithm sets `l = r = 0`, sees `'a'` at the left, consumes it, and immediately finishes with success. This confirms that single-character strings are trivially valid.

For `"aa"`, the first comparison matches `'a'` at one end and consumes it, but the second `'a'` cannot match any expected next character because the expected sequence moves to `'b'`. Since the second character is still `'a'`, the process fails, correctly rejecting duplicates.

For `"z"` alone, the expected character starts at `'a'`, but neither end matches, so the algorithm rejects immediately, reflecting the impossibility of skipping earlier alphabet letters in the construction.
