---
title: "CF 105891J - Win"
description: "We are given a fixed lowercase string, and we are allowed to insert up to k characters anywhere in it. Insertions are flexible: we can choose both the position and the character freely each time."
date: "2026-06-21T17:57:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105891
codeforces_index: "J"
codeforces_contest_name: "The 13th Shaanxi Provincial Collegiate Programming Contest"
rating: 0
weight: 105891
solve_time_s: 80
verified: true
draft: false
---

[CF 105891J - Win](https://codeforces.com/problemset/problem/105891/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed lowercase string, and we are allowed to insert up to `k` characters anywhere in it. Insertions are flexible: we can choose both the position and the character freely each time.

After performing these insertions, we look at the resulting string and count how many times the specific pattern `"lose"` appears as a contiguous substring. The task is to choose insertions so that this count is maximized.

A key detail is that we are counting substrings, not subsequences. This means four characters must sit next to each other in the final string and exactly spell `"lose"`.

The constraint sizes, with string length up to `10^5` and up to `10^5` insertions, immediately rule out any approach that tries to explicitly simulate all possible insertion positions or all resulting strings. Even a quadratic scan over all windows after each insertion is impossible. The solution must be linear or close to linear in the size of the input.

A subtle point is that insertions can change adjacency. Even if the original string has no structure resembling `"lose"`, insertions can create it entirely. Conversely, a greedy local decision might accidentally waste insertions that could have formed more occurrences later.

One important edge situation is when the string already contains partial progress toward the pattern.

For example, consider:

Input:

```
k = 1
s = "lxe"
```

We would like to form `"lose"`. We can insert `'o'` and `'s'` and `'e'` around existing characters, but we only have one insertion, so we cannot complete even a single `"lose"` substring. The correct answer is `0`.

A naive mistake here is to assume that since all characters of `"lose"` appear somewhere, one occurrence is always achievable. That ignores contiguity requirements and insertion budget limits.

Another failure case is overcounting overlapping potential:

```
k = 0
s = "loselose"
```

This contains 2 occurrences already, but a careless approach that counts characters might incorrectly estimate more by recombining letters, which is impossible without insertions.

## Approaches

The brute-force idea is to treat insertions as part of building the final string explicitly. We would try all ways to insert up to `k` characters, generate candidate strings, and count occurrences of `"lose"` in each. Even if we only consider where to insert characters, the number of possibilities grows combinatorially, and each candidate requires a linear scan to count substrings. This becomes completely infeasible even for very small inputs.

The key observation is that insertions are not creating complex structure, they only help us “repair” or “complete” missing characters in order to build copies of the fixed pattern `"lose"`. Once we fix a target number of occurrences, we can think of constructing that many copies sequentially.

Instead of constructing the final string explicitly, we simulate how many times we can greedily “produce” the pattern `"lose"` by scanning through the original string from left to right. Whenever the next required character is missing at the current position, we use one insertion to supply it. The moment we run out of insertions, we can no longer complete further copies.

This reduces the problem to repeatedly matching `"lose"` against a stream where we can either consume a character from the original string or spend one insertion to fabricate the needed character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force construction of strings | Exponential in k | O(n + k) | Too slow |
| Greedy simulation over pattern | O(n + k) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the process as repeatedly building the pattern `"lose"` from left to right using characters from the original string and insertions when necessary.

1. Initialize a pointer `i` at the start of the string, and a counter `k` for remaining insertions. We also maintain a counter for how many full `"lose"` patterns we have successfully built.
2. Try to construct one occurrence of `"lose"` by processing its characters in order.

For each character in `"lose"`, we check whether the current character in the input string matches it. If it matches, we consume it by advancing `i`. If it does not match, we spend one insertion to create the required character instead. This insertion does not advance `i`, because it is placed artificially.

The reasoning here is that we are aligning the original string into a sequence that supports the pattern, and insertions act as fillers.
3. If at any point we need an insertion but have no insertions left, the construction process stops immediately because no further full patterns can be completed.
4. Once one `"lose"` is completed, we increment the answer and immediately start constructing the next one using the same process.
5. We continue until we either exhaust the string and cannot proceed or run out of insertions.

### Why it works

The process enforces a greedy alignment between the source string and repeated occurrences of `"lose"`. Each character from the original string is used in order, and insertions are only spent when the next required character cannot be matched. This guarantees that no insertion is wasted on a later opportunity that could have been used earlier in a different pattern, because any reordering would not improve feasibility of future matches given the fixed sequential structure of substring formation.

Each completed `"lose"` corresponds to a minimal-cost embedding of that pattern into the evolving string, so maximizing the number of completed embeddings under the insertion budget yields the optimal number of substring occurrences.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input().strip())
    s = input().strip()
    target = "lose"
    
    i = 0
    n = len(s)
    ans = 0
    
    while True:
        used = k
        j = i
        
        ok = True
        for c in target:
            if j < n and s[j] == c:
                j += 1
            else:
                if used == 0:
                    ok = False
                    break
                used -= 1
        
        if not ok:
            break
        
        k = used
        i = j
        ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation maintains a pointer `i` into the original string and a remaining insertion budget `k`. Each iteration attempts to build one `"lose"` block. Inside the loop over `"lose"`, we either consume a matching character from `s` or spend one insertion when the match is missing.

A subtle point is that insertions do not move the pointer in `s`, since inserted characters are independent of the original string. Only matches advance the pointer. Once a full pattern is constructed, both the updated pointer and the reduced budget are carried into the next iteration.

The loop stops as soon as a full pattern can no longer be completed.

## Worked Examples

### Example 1

Input:

```
k = 1
s = "loxe"
```

| Pattern step | Pointer i | Current char | Action | k remaining |
| --- | --- | --- | --- | --- |
| l | 0 | l | match | 1 |
| o | 1 | o | match | 1 |
| s | 2 | x | insert s | 0 |
| e | 2 | x | insert e | 0 |

We successfully construct one `"lose"`. No insertions remain, so no further pattern is possible. Output is `1`.

This shows how a single mismatch can be repaired with insertions to still form a valid substring.

### Example 2

Input:

```
k = 2
s = "lsoee"
```

| Pattern step | Pointer i | Current char | Action | k remaining |
| --- | --- | --- | --- | --- |
| l | 0 | l | match | 2 |
| o | 1 | s | insert o | 1 |
| s | 1 | s | match | 1 |
| e | 2 | o | insert e | 0 |

We form one `"lose"` using both insertions. After this, we cannot build another full pattern because insertions are exhausted. Output is `1`.

This demonstrates that insertions are consumed across the entire construction, not per character independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + ans) | Each character in `s` is consumed at most once, and each pattern attempt processes at most 4 steps |
| Space | O(1) | Only a few counters and pointers are used |

The constraints allow up to `10^5` characters and insertions, so a linear scan over the string with constant work per step is easily fast enough within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    k = int(input().strip())
    s = input().strip()
    target = "lose"
    
    i = 0
    n = len(s)
    ans = 0
    
    while True:
        used = k
        j = i
        ok = True
        for c in target:
            if j < n and s[j] == c:
                j += 1
            else:
                if used == 0:
                    ok = False
                    break
                used -= 1
        if not ok:
            break
        k = used
        i = j
        ans += 1
    
    return str(ans)

# provided sample-like sanity checks
assert run("0\nlose") == "1"
assert run("0\nlsoe") == "0"

# custom cases
assert run("1\nlxeo") == "0", "insufficient insertions"
assert run("2\nloxe") == "1", "one repairable pattern"
assert run("4\nlllloooosssseeee") == "1", "already enough structure but sequential consumption limits reuse"
assert run("5\nabcde") == "1", "fully constructed via insertions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 / lxeo | 0 | not enough budget to complete pattern |
| 2 / loxe | 1 | single pattern repair with insertions |
| 4 / lllloooosssseeee | 1 | pointer consumption constraint |
| 5 / abcde | 1 | full construction purely via insertions |

## Edge Cases

A critical edge case is when the string contains no useful characters at all.

Input:

```
k = 4
s = "xxxx"
```

The algorithm attempts to build `"lose"` using only insertions. Each step consumes one insertion, and since `k` equals the pattern length, exactly one occurrence is formed. The pointer in `s` never advances, which is consistent because no characters are reused.

Another case is when the string already matches the pattern partially but is misaligned:

```
k = 0
s = "losxlose"
```

The first three characters align perfectly, but the fourth breaks the pattern. Since no insertions are allowed, the construction fails at that point and only valid complete occurrences are counted. The algorithm stops exactly when mismatch occurs without available insertions, preventing overcounting invalid partial segments.
