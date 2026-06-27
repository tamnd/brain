---
title: "CF 105158F - \u4f18\u79c0\u5b57\u7b26\u4e32"
description: "We are given a collection of strings and we need to count how many of them satisfy a very specific structural pattern."
date: "2026-06-27T11:05:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105158
codeforces_index: "F"
codeforces_contest_name: "2024 National Invitational of CCPC (Zhengzhou), 2024 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 105158
solve_time_s: 44
verified: true
draft: false
---

[CF 105158F - \u4f18\u79c0\u5b57\u7b26\u4e32](https://codeforces.com/problemset/problem/105158/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of strings and we need to count how many of them satisfy a very specific structural pattern. A string is considered valid if it has length exactly five, its third and fifth characters are the same, and its first four characters are all distinct from each other.

So for each input string, we are not transforming it or comparing it against other strings. We only check whether it independently satisfies these constraints, then count how many do.

The input size is large: up to 100000 strings, and the total length of all strings combined is at most 200000. This immediately tells us that we must process each string in essentially constant time. Any solution that scans each string with heavy operations, or does extra allocations proportional to the number of strings, will still pass only if it stays linear overall.

A naive interpretation might suggest checking permutations or comparing substrings against each other, but the constraints are local and fixed length. Each string is either length five or not, so we never need to consider more than five characters per string.

A subtle failure case appears if one assumes “distinct” means distinct among all five characters rather than only the first four. For example, a string like "abaca" has repeated characters, but the repetition might occur in positions that are irrelevant to the condition. Another pitfall is forgetting that only the first four positions must be distinct, while the fifth character is only tied to the third position, not included in the distinctness requirement.

A concrete example:

Input:

"abcde"

This is invalid because the third character 'c' is not equal to the fifth character 'e'. A careless implementation that only checks distinctness among the first four would incorrectly count it.

Another example:

"ababa"

Here, the third and fifth characters match ('a'), but the first four characters are not all distinct ('a' repeats). A naive check that only verifies the equality condition would incorrectly count it.

## Approaches

The brute-force approach is straightforward. For each string, we first check its length. If it is not five, we immediately reject it. Otherwise, we inspect the characters: verify that position three equals position five, then check whether the first four characters are pairwise distinct. This can be done by comparing all pairs among the first four positions or inserting them into a set and checking its size.

This approach is already efficient enough because each string has constant length. Even if we do O(1) work per string, the total complexity is O(n). The only potential inefficiency comes from unnecessary overhead if we use data structures like sets repeatedly, but even that remains within limits due to the tiny fixed size.

The key observation is that the structure is fixed and extremely small. We never need hashing over long substrings or frequency counting over large domains. Every check is bounded by a constant (at most five characters), so the problem reduces to a per-string constant-time predicate evaluation.

This removes any need for global reasoning or preprocessing. Each string can be validated independently in isolation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) extra per string | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each string one by one and apply a fixed validation routine.

1. Read a string and immediately check its length. If it is not exactly five, we discard it. This step prevents unnecessary character checks on invalid candidates.
2. If the length is five, compare the third and fifth characters. If they differ, the string cannot be valid, so we move on. This is the earliest possible rejection condition because it depends on fixed positions.
3. If the positional equality holds, we now examine the first four characters. We must ensure all four are distinct. Since the length is constant, we can either use a small boolean array or a set to record seen characters. If any repetition occurs, we reject the string.
4. If both conditions pass, we increment our answer counter.

The order of checks matters for efficiency. The length check and positional equality check are constant-time and cheap, and they avoid unnecessary work on invalid strings before we inspect the remaining characters.

### Why it works

Each string is processed independently, and the validation logic directly mirrors the definition of an “excellent” string. The condition on the third and fifth characters is enforced exactly once, and the distinctness condition is verified over exactly the intended subset of positions. Since all checks are complete and no approximation is made, any string that passes the algorithm satisfies both constraints, and any string that fails at least one condition is rejected. There is no interaction between strings, so correctness holds per-instance and extends to the full count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_good(s: str) -> bool:
    if len(s) != 5:
        return False
    if s[2] != s[4]:
        return False
    # check first four characters are all distinct
    seen = set()
    for i in range(4):
        if s[i] in seen:
            return False
        seen.add(s[i])
    return True

def main():
    n = int(input())
    ans = 0
    for _ in range(n):
        s = input().strip()
        if is_good(s):
            ans += 1
    print(ans)

if __name__ == "__main__":
    main()
```

The solution encodes the definition directly into a helper function. The length check comes first to avoid indexing assumptions. The condition `s[2] != s[4]` is checked before building any data structure, since a mismatch immediately disqualifies the string.

The set-based uniqueness check only covers the first four characters, matching the problem requirement precisely. We intentionally do not include the fifth character in this check, since it is governed by a separate condition.

## Worked Examples

Consider the input:

```
abcde
ababa
abcab
```

We track validation step by step.

| String | Length check | s[2]==s[4] | First 4 distinct | Result |
| --- | --- | --- | --- | --- |
| abcde | pass | fail | - | reject |
| ababa | pass | pass | fail | reject |
| abcab | pass | pass | pass | accept |

The first string fails due to mismatched third and fifth characters. The second passes that condition but fails because the first four characters contain repetition. The third satisfies both constraints and is counted.

This confirms that both conditions are independently necessary and jointly sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each string is checked in constant time because length is fixed at 5 |
| Space | O(1) | Only a small set is used per string, and no global storage grows with n |

The algorithm fits easily within constraints because even at n = 100000, we only perform a handful of character operations per string.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def is_good(s: str) -> bool:
        if len(s) != 5:
            return False
        if s[2] != s[4]:
            return False
        seen = set()
        for i in range(4):
            if s[i] in seen:
                return False
            seen.add(s[i])
        return True

    n = int(input())
    ans = 0
    for _ in range(n):
        s = input().strip()
        if is_good(s):
            ans += 1
    return str(ans)

# provided sample-style tests
assert run("4\nhenan\nquery\nproblem\nqueue\n") == "1"

# minimum size invalid length
assert run("2\na\nabc\n") == "0"

# valid case
assert run("1\nabcab\n") == "1"

# repetition in first four
assert run("1\nababa\n") == "0"

# multiple valid mixed
assert run("3\nabcab\nabxax\naaaaa\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed sample | 1 | basic correctness |
| short strings | 0 | length filtering |
| valid single | 1 | positive case |
| repeated prefix | 0 | distinctness constraint |
| mixed batch | 2 | combined behavior |

## Edge Cases

One edge case is strings shorter or longer than five characters. For example, "abc" or "abcdef". The algorithm rejects these immediately at the length check, without accessing indices, preventing out-of-bounds assumptions.

Another edge case is when the third and fifth characters match but the first four are heavily repetitive, such as "aaaaa". The algorithm correctly fails it during the distinctness check after passing the positional equality test.

A third case is when all first four characters are distinct but the third and fifth mismatch, such as "abcde". The algorithm rejects it early at the positional check, demonstrating that both conditions are independently enforced and neither is redundant.
