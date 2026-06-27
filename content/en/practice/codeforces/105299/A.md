---
title: "CF 105299A - Autocomplete"
description: "We are given a list of visited webpage addresses and a short prefix string that the user has already typed. The task is to simulate an autocomplete feature: among all stored page addresses that start with this prefix, we must return the one that is smallest in lexicographic…"
date: "2026-06-27T02:31:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105299
codeforces_index: "A"
codeforces_contest_name: "AGM 2024, Final Round, Day 1"
rating: 0
weight: 105299
solve_time_s: 51
verified: true
draft: false
---

[CF 105299A - Autocomplete](https://codeforces.com/problemset/problem/105299/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of visited webpage addresses and a short prefix string that the user has already typed. The task is to simulate an autocomplete feature: among all stored page addresses that start with this prefix, we must return the one that is smallest in lexicographic (dictionary) order. If no stored address begins with the prefix, we simply return the prefix itself unchanged.

The input is therefore a single string representing the partial query, followed by a small collection of candidate full strings. The output is either one of those candidates or the original prefix if none match.

Even though the statement is short, the key modeling decision is to recognize that we are not constructing strings or modifying them, only filtering a set by prefix and then taking a minimum under lexicographic order.

The constraints are small: at most around 100 stored strings with lengths up to about 100 characters. That means any solution up to roughly O(n² · L) or even O(n · L log n) is trivially fast. There is no need for suffix structures, hashing, or advanced string data structures. A linear scan over all strings is already optimal in practice.

The main edge case is when no string matches the prefix at all. In that situation, the correct behavior is not to return an empty string or a placeholder, but to return the prefix itself exactly as given. For example, if the prefix is `"find"` and all stored strings are `"fond..."`, then the output must still be `"find"`.

Another subtle case is when the prefix itself is already present in the list. Since it is lexicographically minimal among all strings starting with itself, it will naturally be chosen, but only if the implementation correctly includes equality as a valid match.

## Approaches

The brute-force approach is direct: iterate over every stored string, check whether it begins with the given prefix, and track the smallest one in lexicographic order among those that match. The check itself is a simple prefix comparison, which costs O(L) per string where L is the string length. With n strings, the total cost is O(n · L).

This is already sufficient because n is small. There is no benefit in sorting everything first, since sorting would cost O(n log n · L), and we would still need to verify the prefix condition. Similarly, building a trie would work but is unnecessary overhead for such a small dataset.

The key observation is that lexicographic order does not depend on global structure here. We only need a single minimum among filtered candidates, so we can maintain a running best string during a single pass. This avoids any preprocessing entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scan with filtering | O(n · L) | O(1) extra | Accepted |
| Sorting all strings first | O(n log n · L) | O(1)-O(n) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Read the prefix string and the number of stored addresses. We keep the prefix fixed because it defines the filtering condition for every candidate.
2. Initialize a variable `best` as empty or a sentinel state indicating “no match yet”. This will store the lexicographically smallest valid completion found so far.
3. For each stored string, check whether it starts with the prefix. This is done by comparing characters one by one up to the length of the prefix. If at any point they differ, the string is not eligible.
4. If the string matches the prefix, compare it with the current `best`. If `best` is empty, we immediately assign it. Otherwise, we update `best` only if the current string is lexicographically smaller. This comparison is the standard dictionary order: first differing character decides, or shorter string is smaller if one is a prefix of the other.
5. After processing all strings, output `best` if it exists. If no string ever matched, output the original prefix instead.

### Why it works

The algorithm maintains a single invariant: after processing each string, `best` is the lexicographically smallest string among all processed candidates that satisfy the prefix condition. Since every candidate is examined exactly once and comparisons are correct under lexicographic ordering, this invariant holds throughout. At the end of the scan, all valid candidates have been considered, so the stored `best` is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def starts_with(s, pref):
    if len(s) < len(pref):
        return False
    for i in range(len(pref)):
        if s[i] != pref[i]:
            return False
    return True

def solve():
    pref = input().strip()
    n = int(input())
    
    best = None
    
    for _ in range(n):
        s = input().strip()
        
        if not starts_with(s, pref):
            continue
        
        if best is None or s < best:
            best = s
    
    if best is None:
        print(pref)
    else:
        print(best)

if __name__ == "__main__":
    solve()
```

The helper function explicitly checks prefix matching instead of relying on slicing tricks, which makes the logic transparent and avoids subtle mistakes when string lengths differ.

The main loop maintains `best` as the current best candidate. The comparison `s < best` directly uses Python’s lexicographic string ordering, which matches the problem definition.

The final conditional handles the required fallback case where no match exists, ensuring the output is exactly the input prefix.

## Worked Examples

### Example 1

Input:

```
next
2
nextpermutation
nextelement
```

| Step | Current String | Matches Prefix | Best Before | Best After |
| --- | --- | --- | --- | --- |
| 1 | nextpermutation | yes | None | nextpermutation |
| 2 | nextelement | yes | nextpermutation | nextelement |

Final answer: `nextelement`

This demonstrates that the algorithm does not just pick the first match but correctly tracks the lexicographically smallest among all valid completions.

### Example 2

Input:

```
find
4
find
findfirstof
findit
fand
```

| Step | Current String | Matches Prefix | Best Before | Best After |
| --- | --- | --- | --- | --- |
| 1 | find | yes | None | find |
| 2 | findfirstof | yes | find | find |
| 3 | findit | yes | find | find |
| 4 | fand | no | find | find |

Final answer: `find`

This shows a case where the prefix itself is the correct output, and all longer extensions are lexicographically larger.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L) | Each of n strings is checked against the prefix of length L |
| Space | O(1) | Only a single best string is stored |

With n up to about 100 and L up to about 100, the total work is at most 10⁴ character comparisons, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io

    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""next
2
nextpermutation
nextelement
""") == "nextelement"

# sample 2
assert run("""find
4
find
findfirstof
findit
fand
""") == "find"

# no match case
assert run("""abc
3
def
ghi
xyz
""") == "abc"

# single string match
assert run("""a
1
a
""") == "a"

# prefix longer than some strings
assert run("""abcd
3
ab
abc
abce
""") == "abce"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no match case | prefix | fallback behavior |
| single string match | a | minimal input correctness |
| mixed prefix lengths | abce | lexicographic + prefix filtering |

## Edge Cases

When no stored string begins with the prefix, the algorithm keeps `best` as `None` and correctly returns the prefix itself. For example, with prefix `"abc"` and strings `["def", "ghi"]`, every prefix check fails, so the final output is `"abc"`.

When the prefix exactly matches one of the stored strings, that string will pass the prefix check and be initialized as `best`. Any longer extensions like `"abcde"` are lexicographically larger, so the algorithm will not incorrectly replace the exact match.

When multiple strings share the same prefix but differ after it, the lexicographic comparison ensures correct selection. For instance, `"nextpermutation"` and `"nextelement"` share `"next"`, but character-by-character comparison correctly identifies `"nextelement"` as smaller because `'e' < 'p'` at the first differing position.
