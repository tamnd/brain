---
title: "CF 1073A - Diverse Substring"
description: "We are given a single string consisting of lowercase letters, and we are asked to find any contiguous segment of this string such that no single character dominates that segment by appearing more than half of its length. If such a segment exists, we may output any one of them."
date: "2026-06-15T14:11:30+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1073
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 53 (Rated for Div. 2)"
rating: 1000
weight: 1073
solve_time_s: 289
verified: true
draft: false
---

[CF 1073A - Diverse Substring](https://codeforces.com/problemset/problem/1073/A)

**Rating:** 1000  
**Tags:** implementation, strings  
**Solve time:** 4m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string consisting of lowercase letters, and we are asked to find any contiguous segment of this string such that no single character dominates that segment by appearing more than half of its length. If such a segment exists, we may output any one of them. If none exists, we must report impossibility.

The key object is not the full string but its substrings. For each substring, we are checking a frequency condition: if the substring has length $L$, then every character must appear at most $L/2$ times. This is equivalent to saying that the substring cannot be made up mostly of one repeated character.

The constraint $n \le 1000$ means that an $O(n^3)$ brute force over substrings with frequency counting would be borderline but still potentially pass in optimized Python, while $O(n^2)$ solutions are comfortably safe. This strongly suggests that we should try to reason about small structured substrings rather than complicated global constructions.

A subtle point is that the answer is not required to be long or maximal. This removes any need for optimization over length. Any valid substring is sufficient, which often allows a construction argument instead of a search.

Edge cases arise when the string is uniform. For example, if $s = "aaaa"$, every substring is also uniform, so the majority condition is always violated. In such cases, the correct output is "NO". A naive approach that only checks full string diversity would fail here because even if the full string fails, shorter substrings might still work, but in this specific case none do.

Another important edge case is when the string has mixed characters but is still dominated locally. For instance, "aaab" has valid answer "ab" or "ba", but "aaa" alone has no valid substring at all. This highlights that we are not looking for global diversity but local balance.

## Approaches

A brute-force strategy is to enumerate all substrings and check each one by counting character frequencies. For each substring $s[l:r]$, we compute 26 counts and verify whether any count exceeds half the length. This is correct because it directly matches the definition.

The issue is complexity. There are $O(n^2)$ substrings, and each check costs $O(n)$ if we recompute counts from scratch, leading to $O(n^3)$. Even with prefix sums reducing checks to $O(1)$ per character, we still have $O(26n^2)$, which is borderline but acceptable at $n=1000$. However, this is unnecessary because the structure of the problem allows a much simpler observation.

The key insight is that if a valid substring exists, then we can always find one of length at most 2. If we take any two adjacent distinct characters, the substring of length 2 already satisfies the condition, because each character appears exactly once and $1 \le 2/2$ is false only if a character appears more than once. Therefore any pair of different adjacent characters is valid.

This reduces the entire problem to scanning for any index $i$ such that $s[i] \ne s[i+1]$. If such a pair exists, we output it. If no such pair exists, the string is uniform, and no valid substring exists at all.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ or $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Scan the string from left to right, examining each adjacent pair of characters.
2. At position $i$, compare $s[i]$ and $s[i+1]$.
3. If they differ, immediately output the substring $s[i:i+2]$ and terminate.
4. If the scan completes without finding any differing adjacent pair, conclude that all characters are identical.
5. In that case, output "NO".

The reason step 3 is sufficient is that any two distinct characters form a substring where no character can appear more than once, which automatically satisfies the diversity condition.

### Why it works

The invariant is that if a valid substring exists anywhere in the string, then either there is an adjacent mismatch or the string is fully uniform. In a uniform string, every substring has the same character repeated, so no substring can satisfy the condition. In a non-uniform string, at least one adjacent pair must differ, and that pair itself forms a valid solution. Therefore scanning adjacent pairs is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
s = input().strip()

for i in range(n - 1):
    if s[i] != s[i + 1]:
        print("YES")
        print(s[i:i+2])
        sys.exit(0)

print("NO")
```

The solution relies entirely on detecting the first transition between different characters. The early exit ensures we do not scan unnecessarily after finding a valid answer. The slice `s[i:i+2]` is safe because Python handles boundaries cleanly and we only iterate up to `n-2`.

## Worked Examples

### Example 1

Input: `codeforces`

| i | s[i] | s[i+1] | action |
| --- | --- | --- | --- |
| 0 | c | o | mismatch found, output "co" |

The algorithm stops immediately at the first pair. This demonstrates that the earliest valid substring is always acceptable, regardless of position.

### Example 2

Input: `aaaaa`

| i | s[i] | s[i+1] | action |
| --- | --- | --- | --- |
| 0 | a | a | continue |
| 1 | a | a | continue |
| 2 | a | a | continue |
| 3 | a | a | continue |

No mismatches are found, so the algorithm outputs "NO". This confirms that uniform strings have no valid substrings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass over adjacent pairs |
| Space | $O(1)$ | only constant extra variables used |

The linear scan is optimal because every character must be inspected at least once in the worst case to determine whether any adjacent mismatch exists. With $n \le 1000$, this is trivially fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        n = int(input().strip())
        s = input().strip()
        for i in range(n - 1):
            if s[i] != s[i + 1]:
                print("YES")
                print(s[i:i+2])
                return out.getvalue().strip()
        print("NO")
    return out.getvalue().strip()

# provided sample
assert run("10\ncodeforces\n") == "YES\nco"

# custom cases
assert run("1\na\n") == "NO"
assert run("2\naa\n") == "NO"
assert run("2\nab\n") == "YES\nab"
assert run("5\nabcde\n") in {"YES\nab", "YES\nbc", "YES\ncd", "YES\nde"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"1 a"` | NO | single-character edge case |
| `"aa"` | NO | minimal uniform string |
| `"ab"` | YES ab | minimal valid case |
| `"abcde"` | any adjacent pair | multiple valid answers |

## Edge Cases

A single-character string such as `"z"` is automatically invalid because any substring has length 1 and the only character appears more than half the time. The algorithm correctly outputs "NO" since there are no adjacent pairs to inspect.

A fully uniform string like `"kkkkk"` behaves similarly. The scan never finds a mismatch, and the output is correctly "NO". Every substring inherits the same imbalance.

A mixed string like `"ba"` demonstrates the positive case at minimal length. The first comparison already yields a mismatch, and the substring `"ba"` is immediately valid because both characters appear once and neither exceeds half of 2.
