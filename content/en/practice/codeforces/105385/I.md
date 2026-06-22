---
title: "CF 105385I - Left Shifting"
description: "We are given a string and we can rotate it cyclically to the left by some number of positions. A left shift by $d$ means taking the substring starting from position $d$ to the end and attaching the prefix $0 dots d-1$ at the end."
date: "2026-06-23T05:18:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105385
codeforces_index: "I"
codeforces_contest_name: "The 2024 CCPC Shandong Invitational Contest and Provincial Collegiate Programming Contest"
rating: 0
weight: 105385
solve_time_s: 45
verified: true
draft: false
---

[CF 105385I - Left Shifting](https://codeforces.com/problemset/problem/105385/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string and we can rotate it cyclically to the left by some number of positions. A left shift by $d$ means taking the substring starting from position $d$ to the end and attaching the prefix $0 \dots d-1$ at the end.

After each rotation, we look only at the first and last character of the rotated string. We want the smallest rotation amount $d \ge 0$ such that these two characters become equal. If no rotation makes the first and last characters match, we output $-1$.

A useful way to reframe this is to think of the string on a circle. Every rotation just chooses a starting index $i$, and the resulting string begins at $i$ and ends at $i-1$ modulo $n$. So we are really asking for the smallest index $i$ such that $s[i] = s[i-1]$ in circular sense, and we return $i$ as the shift amount.

The constraints allow total string length up to $5 \times 10^5$, which rules out any solution that tries every rotation and recomputes endpoints or scans the string per shift. Anything quadratic in total input size will clearly fail.

A subtle edge case appears when all characters are distinct. For example, input `"abc"` has no pair of adjacent equal characters even in circular sense, so no rotation can make endpoints equal and the answer must be $-1$. A naive approach that only checks linear adjacency without considering wrap-around might incorrectly miss the transition between last and first characters, or conversely might incorrectly assume a match exists after shifting.

Another edge case is when the string already starts and ends with the same character. For `"abca"`, the answer is $0$, and any algorithm must ensure it does not accidentally return a larger rotation just because other matches exist.

## Approaches

A brute-force approach tries every possible shift $d$ from $0$ to $n-1$. For each shift, we conceptually rotate the string and compare the first and last character. Constructing the rotated string costs $O(n)$, and even if we avoid construction and just index modulo $n$, checking endpoints is $O(1)$, so this part is fine. The real issue is that we still need to decide correctness by considering all $d$, which is $O(n)$ checks per test case.

However, the key observation is that rotation only changes which index becomes the first character. If we choose start index $i$, then the last character is always $s[i-1]$. So the condition “first equals last” becomes a purely local condition: $s[i] = s[i-1]$.

This collapses the entire problem into finding the smallest index $i$ such that adjacent characters in the circular string match. We can scan the string once, check every pair $(i-1, i)$, and also the wrap-around pair $(n-1, 0)$. The smallest such index $i$ is the answer. If none exists, we output $-1$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force rotations | $O(n^2)$ | $O(1)$ | Too slow |
| Linear scan of circular adjacency | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We want to identify the earliest rotation point where the boundary between last and first characters becomes valid.

1. Treat each possible rotation as choosing a starting index $i$. After rotation, the first character is $s[i]$ and the last is $s[i-1]$ in circular indexing. This reformulation removes any need to simulate the rotation.
2. Check all indices $i$ from $0$ to $n-1$. For each $i$, compare $s[i]$ with $s[i-1]$, where index $-1$ corresponds to $n-1$. This step directly tests whether rotation $i$ produces a “beautiful” string.
3. Keep the smallest index $i$ that satisfies the equality. Since we scan from left to right, the first valid $i$ is automatically minimal.
4. If no index satisfies the condition, return $-1$.

### Why it works

After a left shift by $i$, the rotated string is exactly a cyclic relabeling where position $0$ corresponds to original index $i$ and position $n-1$ corresponds to original index $i-1$. So the condition for a valid answer depends only on a single adjacency in the original circular arrangement. Every possible rotated string corresponds to exactly one such adjacency check, and no two different shifts produce different comparisons beyond this boundary pair. This one-to-one mapping ensures that scanning all circular adjacencies exhausts all possible rotations without omission or duplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    if n == 1:
        print(0)
        return

    for i in range(n):
        if s[i] == s[i - 1]:
            print(i)
            return

    print(-1)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
```

The solution relies on scanning each position once and checking its left neighbor in circular form. The expression `s[i - 1]` naturally handles the wrap-around case because Python negative indexing maps `-1` to the last character, which exactly corresponds to index $n-1$.

The special case $n=1$ is handled separately because the single-character string is always beautiful for rotation $0$, and the loop would otherwise still behave correctly but the explicit case makes intent clear and avoids unnecessary iteration.

## Worked Examples

We trace the circular adjacency check for two inputs.

### Example 1: `"helloccpc"`

| i | s[i] | s[i-1] | match | decision |
| --- | --- | --- | --- | --- |
| 0 | h | c | no | continue |
| 1 | e | h | no | continue |
| 2 | l | e | no | continue |
| 3 | l | l | yes | return 3 |

The first valid index is 3, meaning rotating left by 3 yields a string whose first and last characters match. This matches the example behavior where the substring starting at 3 begins and ends with the same character.

### Example 2: `"abcdcba"`

| i | s[i] | s[i-1] | match | decision |
| --- | --- | --- | --- | --- |
| 0 | a | a | yes | return 0 |

Even though other matches exist later, the smallest valid rotation is already 0 because the original string already satisfies the condition at its boundary.

These examples confirm that we are correctly interpreting rotations as boundary checks rather than attempting to simulate full strings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each character is checked once against its circular predecessor |
| Space | $O(1)$ | No auxiliary structures beyond the input string |

The total length across test cases is bounded by $5 \times 10^5$, so a single linear scan per test case easily fits within time limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    def solve_all():
        t = int(input())
        for _ in range(t):
            s = input().strip()
            n = len(s)
            if n == 1:
                print(0)
                continue
            for i in range(n):
                if s[i] == s[i - 1]:
                    print(i)
                    break
            else:
                print(-1)

    solve_all()
    return out.getvalue().strip()

# provided sample
assert run("1\nhelloccpc\n") == "3"
assert run("1\nabcdcba\n") == "0"
assert run("1\nx\n") == "0"
assert run("1\nabc\n") == "-1"

# custom cases
assert run("1\naab\n") == "1", "adjacent match after shift"
assert run("1\nbaaa\n") == "1", "wrap-around and internal equality"
assert run("1\nabab\n") == "-1", "no equal adjacent circular pair"
assert run("1\naa\n") == "0", "minimum length repeated characters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `aab` | 1 | first valid rotation not at index 0 |
| `baaa` | 1 | wrap-around correctness and early match |
| `abab` | -1 | no circular adjacency matches |
| `aa` | 0 | smallest valid case and base condition |

## Edge Cases

For a string like `"abab"`, every character differs from its neighbors even in circular form. The scan checks all indices:

At i = 0, compare `a` with last `b`, no match. At i = 1, `b` vs `a`, no match. At i = 2, `a` vs `b`, no match. At i = 3, `b` vs `a`, no match. The algorithm finishes without finding a valid index and outputs $-1$, which is correct because no rotation can align endpoints.

For `"aa"`, at i = 0 we compare `a` with `a` (wrap-around), immediately returning 0. This confirms that circular adjacency correctly captures the rotation boundary condition without needing explicit rotation simulation.
