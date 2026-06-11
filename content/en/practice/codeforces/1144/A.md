---
title: "CF 1144A - Diverse Strings"
description: "We are given several short strings, and for each one we need to decide whether it forms a single continuous block of the alphabet without any gaps or repetition. Think of the lowercase alphabet as a line from ‘a’ to ‘z’."
date: "2026-06-12T03:30:53+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1144
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 550 (Div. 3)"
rating: 800
weight: 1144
solve_time_s: 78
verified: true
draft: false
---

[CF 1144A - Diverse Strings](https://codeforces.com/problemset/problem/1144/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several short strings, and for each one we need to decide whether it forms a single continuous block of the alphabet without any gaps or repetition. Think of the lowercase alphabet as a line from ‘a’ to ‘z’. A string is valid if, when you look at the letters it contains, they correspond to some contiguous segment of this line, and every letter appears exactly once.

So a string like “dabcef” works because its letters are {a, b, c, d, e, f}, which form a continuous interval in the alphabet. The order inside the string does not matter for the definition, only the set of characters does. On the other hand, “az” fails because it jumps over all letters between ‘a’ and ‘z’, and “babc” fails because it repeats ‘b’.

Each test case is independent, and we simply output “Yes” if the string satisfies these conditions and “No” otherwise.

The constraints are very small: at most 100 strings, each of length at most 100. This immediately rules out anything beyond linear work per string. Even an O(n^2) per string approach would still be acceptable, but anything more complicated than checking frequencies and scanning the alphabet is unnecessary overhead.

The main failure cases usually come from forgetting one of the two conditions. One is duplication, for example “aa” should be rejected even though it is a single character type. The other is gaps in the alphabet, for example “ac” must be rejected even though both letters are distinct, because ‘b’ is missing between them.

## Approaches

A brute-force way to think about the problem is to try every possible starting letter of a contiguous alphabet segment and check if the string can be rearranged into that segment. For each candidate segment, we would compare sorted characters or build frequency arrays and verify equality. This works, but it is overkill.

The key observation is that a valid string must behave like a “path” on the alphabet line. If we sort or reason about the set of characters, the minimum and maximum letters determine the only possible segment. If the string is valid, then every character between these extremes must appear exactly once, and no duplicates are allowed.

This reduces the problem to a simple check: ensure uniqueness, compute min and max characters, and verify that the number of distinct characters equals the length of the interval between them.

This is efficient because all operations are linear in the string length, and the alphabet size is constant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26 · n²) | O(1) | Accepted but unnecessary |
| Optimal | O(n) per string | O(1) | Accepted |

## Algorithm Walkthrough

For each string, we process it independently.

1. We scan the string and record whether we have seen any repeated character. If a character repeats, the string is immediately invalid. This is required because duplicates violate the “each letter exactly once” rule.
2. While scanning, we also track the minimum and maximum character encountered in terms of alphabetical order. This gives us the potential segment endpoints.
3. After the scan, we compute how many distinct characters we saw. If duplicates were detected, we already know the answer is “No”.
4. We now compare the size of the interval defined by the minimum and maximum characters. The interval length is `(max_char - min_char + 1)`.
5. If the number of distinct characters equals this interval length, then every character in the range must be present exactly once, so we return “Yes”. Otherwise, we return “No”.

### Why it works

The core invariant is that a valid string must represent a complete interval on the alphabet without missing elements. If duplicates are forbidden, then each character contributes exactly one position in that interval. If the observed set of characters has size k, but spans an interval larger than k, then at least one character in the middle is missing, breaking contiguity. Conversely, if the size matches the interval length and there are no duplicates, the set must be exactly the interval, because there is no room for gaps or extras.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_diverse(s: str) -> bool:
    seen = [False] * 26
    mn = 26
    mx = -1

    for ch in s:
        idx = ord(ch) - ord('a')
        if seen[idx]:
            return False
        seen[idx] = True
        mn = min(mn, idx)
        mx = max(mx, idx)

    # number of distinct characters
    cnt = sum(seen)

    return (mx - mn + 1) == cnt

def main():
    n = int(input())
    for _ in range(n):
        s = input().strip()
        print("Yes" if is_diverse(s) else "No")

if __name__ == "__main__":
    main()
```

The implementation directly follows the algorithm. The boolean array `seen` ensures constant-time detection of duplicates. Tracking `mn` and `mx` avoids sorting or set-based range reconstruction. The final comparison checks whether the characters fill the entire interval without gaps.

A subtle point is that we only rely on the set of characters, not their order in the string. This is safe because the condition depends solely on adjacency in the alphabet, not adjacency in the string itself.

## Worked Examples

We trace two inputs: one valid and one invalid.

### Example 1: `"dabcef"`

| Step | Character | Seen set size | Min index | Max index | Duplicate? |
| --- | --- | --- | --- | --- | --- |
| 1 | d | 1 | 3 | 3 | No |
| 2 | a | 2 | 0 | 3 | No |
| 3 | b | 3 | 0 | 3 | No |
| 4 | c | 4 | 0 | 3 | No |
| 5 | e | 5 | 0 | 4 | No |
| 6 | f | 6 | 0 | 5 | No |

After processing, `cnt = 6`, `mn = 0`, `mx = 5`. Interval size is `5 - 0 + 1 = 6`, which matches the number of distinct characters, so the result is “Yes”.

This confirms that unordered inputs still form a contiguous alphabet block.

### Example 2: `"babc"`

| Step | Character | Seen set size | Min index | Max index | Duplicate? |
| --- | --- | --- | --- | --- | --- |
| 1 | b | 1 | 1 | 1 | No |
| 2 | a | 2 | 0 | 1 | No |
| 3 | b | - | - | - | Yes |

At the third character, we detect that ‘b’ was already seen, so we immediately return “No”.

This demonstrates that duplication alone is sufficient to invalidate a string, even if the alphabet interval condition could otherwise be satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L) | Each string is scanned once, and all operations are O(1) per character |
| Space | O(1) | Only a fixed 26-length array is used |

Given that total input size is at most 10,000 characters, this runs comfortably within limits. The constant-factor operations are minimal and dominated by simple array indexing.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    def is_diverse(s: str) -> bool:
        seen = [False] * 26
        mn = 26
        mx = -1

        for ch in s:
            idx = ord(ch) - ord('a')
            if seen[idx]:
                return False
            seen[idx] = True
            mn = min(mn, idx)
            mx = max(mx, idx)

        cnt = sum(seen)
        return (mx - mn + 1) == cnt

    n = int(input())
    for _ in range(n):
        s = input().strip()
        print("Yes" if is_diverse(s) else "No")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""8
fced
xyz
r
dabcef
az
aa
bad
babc
""") == """Yes
Yes
Yes
Yes
No
No
No
No"""

# single letter
assert run("""1
a
""") == "Yes"

# simple invalid gap
assert run("""1
ac
""") == "No"

# full alphabet segment shuffled
assert run("""1
cba
""") == "Yes"

# duplicate inside otherwise valid range
assert run("""1
abca
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single `a` | Yes | minimum length case |
| `ac` | No | missing middle letter |
| `cba` | Yes | shuffled valid segment |
| `abca` | No | duplicate detection |

## Edge Cases

A string of length one is always valid because it trivially forms a contiguous segment with no gaps and no duplicates. The algorithm handles this because `mn == mx` and `cnt == 1`, so the interval check passes.

A case like “az” demonstrates why range checking is necessary. The scan finds `mn = 0`, `mx = 25`, and `cnt = 2`. The interval size is 26, which does not match, so it correctly returns “No” even though there are no duplicates.

A case like “aa” demonstrates the duplicate rule. The second character triggers immediate rejection before range logic matters, ensuring correctness without relying on interval checks.
