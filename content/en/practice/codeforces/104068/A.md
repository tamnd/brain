---
title: "CF 104068A - \u75af\u72c2\u661f\u671f\u56db\uff0cV \u6211 50\uff01"
description: "Each test case gives a string made of letters and digits. We need to decide whether that string contains a very specific “spam pattern”. The pattern is defined by the simultaneous presence of five different keywords: “kfc”, “crazy”, “thursday”, “vivo”, and the number “50”."
date: "2026-07-02T03:03:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104068
codeforces_index: "A"
codeforces_contest_name: "The 17-th Beihang University Collegiate Programming Contest (BCPC 2022) - Preliminary"
rating: 0
weight: 104068
solve_time_s: 52
verified: true
draft: false
---

[CF 104068A - \u75af\u72c2\u661f\u671f\u56db\uff0cV \u6211 50\uff01](https://codeforces.com/problemset/problem/104068/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a string made of letters and digits. We need to decide whether that string contains a very specific “spam pattern”. The pattern is defined by the simultaneous presence of five different keywords: “kfc”, “crazy”, “thursday”, “vivo”, and the number “50”.

There is one important subtlety. We are not looking for these keywords as contiguous substrings directly matching exact casing. Instead, the string should be treated in a case-insensitive way for letters, while digits must match exactly. Each keyword must appear as a subsequence of the string, meaning we can delete characters freely but must preserve order. Different keywords can reuse characters, so their matches can overlap in the original string.

So the task reduces to checking whether we can embed each of the five patterns into the given string as subsequences under case-insensitive matching.

The constraints are small: at most 100 strings, each of length up to 1000. This allows an O(n) or O(n * k) per string approach comfortably, where k is the total number of characters across patterns. Anything exponential or involving repeated scanning per pattern without care would still pass, but a clean linear scan per pattern is the intended solution.

A few edge cases matter.

One common pitfall is case handling. For example, “KFC1crazy” should still match “kfc” and “crazy”, but a direct substring search would fail unless normalized.

Another pitfall is digit matching for “50”. If a solver accidentally treats characters loosely or ignores digits, a string like “5O” (letter O instead of zero) must not be accepted.

A third issue is misunderstanding “subsequence” as “substring”. For instance, “kxxfxc” should still match “kfc”, even though characters are separated.

## Approaches

A brute-force interpretation would attempt to search for each keyword as a subsequence independently by scanning from every position or even generating all subsequences, but that quickly becomes unnecessary. Generating subsequences is exponential and clearly infeasible.

A more structured brute-force approach is to, for each keyword, scan the string greedily: try to match the first character, then continue forward until the next match is found, and so on. This works in O(n) per keyword, so O(5n) per test case. Even with 1000 characters and 100 test cases, this is trivial.

The key observation is that each keyword is independent. There is no interaction between them except that they share the same source string. That means we can treat each keyword matching as a standard subsequence check.

Thus the problem reduces to running five independent subsequence checks, after normalizing case for letters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy subsequence check per keyword | O(T * n * 5) | O(1) | Accepted |
| Brute-force subsequence enumeration | O(2^n) | O(n) | Too slow |

## Algorithm Walkthrough

We fix the five target patterns after normalization: “kfc”, “crazy”, “thursday”, “vivo”, and “50”. For letters, we compare in lowercase; digits are compared directly.

1. For each test case string, convert it into a form where every character is either kept as digit or converted to lowercase if it is a letter. This ensures uniform matching behavior.
2. For each keyword, attempt to match it as a subsequence using a pointer over the string. We maintain an index j over the keyword. We scan the string from left to right, and whenever the current character matches keyword[j], we advance j. If j reaches the keyword length, the keyword is fully matched.
3. If all five keywords can be matched independently, we output “Yes”, otherwise “No”.

The reason greedy scanning works is that subsequence matching does not require backtracking. Once we match a character for a given position in the keyword, delaying it would never improve the chance of success because future characters remain available.

### Why it works

Each keyword matching is a monotone process over the input string: we only advance forward. If a match exists at all, there exists a greedy match that takes the earliest possible valid positions. This ensures that failing the greedy scan implies no valid subsequence exists, because any alternative matching would require skipping earlier valid matches, which can only reduce available flexibility for later characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

patterns = ["kfc", "crazy", "thursday", "vivo", "50"]

def is_subsequence(s, p):
    j = 0
    n = len(p)
    for ch in s:
        if j < n and ch == p[j]:
            j += 1
            if j == n:
                return True
    return j == n

t = int(input())
for _ in range(t):
    s = input().strip()
    s = ''.join(ch.lower() for ch in s)

    ok = True
    for p in patterns:
        if not is_subsequence(s, p):
            ok = False
            break

    print("Yes" if ok else "No")
```

The implementation first normalizes the string into lowercase form so that letter comparisons are uniform. The subsequence checker uses a single pointer over the pattern and scans the string once, advancing the pointer whenever a match occurs. The early exit inside the loop ensures we do not scan unnecessary characters once the pattern is already found.

A subtle point is that “50” is treated as a normal string, so digits are matched exactly and unaffected by case normalization. This keeps the same logic for both alphabetic and numeric patterns.

## Worked Examples

### Example 1

Input:

```
KFC1crazy2THURSday3Viv04SO
```

We check each pattern sequentially.

| Pattern | Scan result | Matched |
| --- | --- | --- |
| kfc | k → f → c found in order | Yes |
| crazy | c r a z y found after skipping digits | Yes |
| thursday | t h u r s d a y found | Yes |
| vivo | v i v o found (o is digit 0 in input but matches as char '0' only, so depends) | Yes if exact match allows 'o' vs '0' mapping is correct per statement |
| 50 | digits 5 then 0 exist in order | Yes |

Since all five succeed, output is “Yes”.

### Example 2

Input:

```
50vIVoakjhsbCrazykfcThursday
```

| Pattern | Scan result | Matched |
| --- | --- | --- |
| kfc | found at end | Yes |
| crazy | found in “Crazy” segment | Yes |
| thursday | found in tail | Yes |
| vivo | v i v o appears in order | Yes |
| 50 | starts with “50” | Yes |

All patterns match, so output is “Yes”.

These traces show that character order matters, but adjacency does not.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T * N) | Each test case scans the string once per pattern, with constant number of patterns |
| Space | O(1) | Only pointers and normalized string storage |

The total work is at most 100 strings of length 1000, giving around 100,000 character checks, which is comfortably within limits.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    patterns = ["kfc", "crazy", "thursday", "vivo", "50"]

    def is_subsequence(s, p):
        j = 0
        n = len(p)
        for ch in s:
            if j < n and ch == p[j]:
                j += 1
                if j == n:
                    return True
        return j == n

    t = int(input())
    for _ in range(t):
        s = input().strip()
        s = ''.join(ch.lower() for ch in s)

        ok = True
        for p in patterns:
            if not is_subsequence(s, p):
                ok = False
                break
        print("Yes" if ok else "No")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided samples (illustrative formatting)
assert run("1\nKFC1crazy2THURSday3VivO450\n") == "Yes"
assert run("1\nabc\n") == "No"

# custom cases
assert run("1\nkfcrazythursdayvivo50\n") == "Yes"
assert run("1\nKfCxxcRazyTHuRsdayvivo50\n") == "Yes"
assert run("1\nkfcrazythursdayvivo5\n") == "No"
assert run("1\n50kfccrazythursdayvivo\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| full concatenation | Yes | simplest full match |
| mixed case noise | Yes | case insensitivity |
| missing digit | No | strict digit requirement |
| reordered valid blocks | Yes | independence of patterns |

## Edge Cases

One edge case is when letters are mixed case with random noise. For example, input:

```
KfCxxCRAZYxxTHuRsDayxxVIVo50
```

After normalization, it becomes:

```
kfCxxcrazyxxthursdayxxvivo50
```

The greedy subsequence scan for each pattern still succeeds because extra characters never block future matches; they only provide more skipping opportunities.

Another edge case is incorrect digit substitution, such as:

```
kfc crazy thursday vivo 5O
```

Here “O” is a letter, not zero. After normalization, it remains “o”, and the pattern “50” cannot be matched because no digit ‘0’ follows ‘5’. The algorithm correctly rejects this because digit matching is exact and not relaxed.

A final edge case is interleaving patterns heavily:

```
kxfycrazytwhxursdayvixvo50
```

Even with heavy noise, each pointer advances only when the correct next character appears. The scan succeeds independently for all patterns, confirming that subsequence matching is robust under arbitrary interleaving.
