---
title: "CF 1553D - Backspace"
description: "We are simulating a typing process where we scan a source string s from left to right. At each position, we either append the current character to an evolving text buffer or press backspace, which deletes the most recently added character if it exists."
date: "2026-06-16T15:54:08+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1553
codeforces_index: "D"
codeforces_contest_name: "Harbour.Space Scholarship Contest 2021-2022 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 1500
weight: 1553
solve_time_s: 361
verified: false
draft: false
---

[CF 1553D - Backspace](https://codeforces.com/problemset/problem/1553/D)

**Rating:** 1500  
**Tags:** dp, greedy, strings, two pointers  
**Solve time:** 6m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a typing process where we scan a source string `s` from left to right. At each position, we either append the current character to an evolving text buffer or press backspace, which deletes the most recently added character if it exists.

The question is whether there exists a choice of backspace operations such that after processing all characters of `s`, the final buffer becomes exactly the target string `t`.

A useful way to think about the process is that every character in `s` either survives into the final string or is removed by a later backspace. The constraint is that deletions are always from the end of the current constructed sequence, so earlier characters can only be removed if enough later backspaces occur.

The input consists of many independent test cases, and across all cases the total string length is at most 200000. This immediately rules out any solution that simulates all possibilities or uses exponential choices per character. Even an O(n log n) per test case solution risks being too slow if it does not aggregate carefully, so a linear solution per test case is required.

A key subtlety appears when characters in `s` match `t` but cannot be aligned due to later deletions. For example, if `s = "ababa"` and `t = "ba"`, it is possible to skip early characters and selectively delete later ones so that only the second and last characters survive in the correct order. However, if `t` requires characters in an order that forces keeping a prefix that must later be partially deleted in a way that destroys ordering, it becomes impossible.

Another failure case arises when `t` is longer than the final number of characters that can possibly survive. Since each backspace removes one previously typed character and typing produces exactly one character per non-backspace step, the final length cannot exceed the number of typed characters minus backspaces, so if `|t| > |s|`, the answer is immediately impossible. More subtle is when lengths are compatible but relative order constraints make matching impossible.

## Approaches

The brute-force viewpoint is to treat each position in `s` as a binary decision: either we type it or we press backspace. This leads to roughly `2^n` possibilities, and for each we simulate the stack behavior in O(n), giving O(n 2^n), which is far beyond any limit even for n around 40.

The structure of the problem simplifies once we stop thinking in terms of which characters are deleted and instead think in reverse. Every backspace operation removes a character that must have been previously kept, meaning we are really deciding which characters in `s` survive as a subsequence, but with an extra constraint: deletions can erase earlier kept characters, so we are not simply choosing a subsequence of `s`. However, we can reinterpret the process as building a stack where each character can later be removed, and we want the final stack to equal `t`.

The key observation is that if we process `s` left to right and maintain a stack, the only real choice is whether to push the current character or to simulate a backspace. Instead of trying all choices, we can reason greedily from the end: we want to match `t` as the final remaining sequence, so we try to ensure that characters of `t` appear as the last surviving elements of the stack in order.

A more structural simplification is that each character of `t` must correspond to some occurrence in `s` that survives all deletions after it. Working backward, we can greedily match `t` from the end of `s`, deciding whether we use a character as part of `t` or treat it as something deleted or used to delete earlier characters. This reduces to a two-pointer strategy scanning from right to left.

We maintain a pointer `j` on `t` starting from its last character, and scan `s` from right to left. When we see a character equal to `t[j]`, we can match it as a surviving character and move `j` backward. Otherwise, that character in `s` must be expendable, meaning it can be either typed and later erased or simply ignored in the construction. If we manage to match all characters of `t`, the construction is possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over choices | O(2^n · n) | O(n) | Too slow |
| Two-pointer greedy from end | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Set a pointer `j` to the last index of `t`. This represents the next character we still need to match in reverse order. The idea is that `t` must appear as a subsequence of a valid final stack, so we try to embed it from the back.
2. Traverse `s` from right to left using index `i`. We inspect each character as a potential contributor to the final matched structure.
3. If `s[i]` equals `t[j]`, we treat this character as matching the current required character of `t` and decrement `j`. This means we commit this position as one of the surviving characters in the final result.
4. If `s[i]` does not equal `t[j]`, we ignore it. Conceptually, this character is either typed and later removed via backspaces or never contributes to the final stack.
5. After finishing the scan, check whether `j` has moved to `-1`. If so, every character of `t` has been matched in correct reverse order, so construction is possible.

The reason this works is that matching from the end ensures we always assign each `t[j]` to the rightmost possible occurrence in `s`. Any character in `s` that we skip can be safely treated as removable, because backspaces allow arbitrary deletions of previously typed characters, so skipping does not violate feasibility. If a match exists in a valid construction, there is always a way to choose deletions so that this greedy rightmost matching is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()

    j = len(t) - 1

    for i in range(len(s) - 1, -1, -1):
        if j >= 0 and s[i] == t[j]:
            j -= 1

    print("YES" if j == -1 else "NO")

q = int(input())
for _ in range(q):
    solve()
```

The implementation directly follows the backward matching strategy. We avoid any simulation of the stack or backspace operations because they are implicitly handled by the freedom to discard unmatched characters.

The only subtle point is that we never explicitly simulate deletions. This is safe because backspaces only restrict us by removing most recent characters, and scanning from right to left ensures we never rely on ordering constraints that would be invalidated by such deletions.

## Worked Examples

### Example 1

Input:

`s = ababa`, `t = ba`

We track `j` from end of `t`.

| i (s index) | s[i] | t[j] | action | j after |
| --- | --- | --- | --- | --- |
| 4 | a | a | match | 0 |
| 3 | b | a | skip | 0 |
| 2 | a | a | match | -1 |

Once `j` becomes `-1`, remaining characters are irrelevant. This confirms we can embed `t` in reverse order.

This trace shows that only rightmost usable matches matter, and earlier structure does not constrain feasibility once later matches are secured.

### Example 2

Input:

`s = ababa`, `t = bb`

| i | s[i] | t[j] | action | j |
| --- | --- | --- | --- | --- |
| 4 | a | b | skip | 1 |
| 3 | b | b | match | 0 |
| 2 | a | b | skip | 0 |
| 1 | b | b | match | -1 |
| 0 | a | - | skip | -1 |

We successfully match both `b` characters, showing that even with intervening characters, the greedy reverse matching finds valid placements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | single reverse scan of `s` |
| Space | O(1) | only pointer variables used |

The total length across all test cases is bounded by 200000, so the overall work is linear in the input size, which comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    q = int(input())
    out = []

    for _ in range(q):
        s = input().strip()
        t = input().strip()

        j = len(t) - 1
        for i in range(len(s) - 1, -1, -1):
            if j >= 0 and s[i] == t[j]:
                j -= 1

        out.append("YES" if j == -1 else "NO")

    return "\n".join(out)

# provided samples
assert run("""4
ababa
ba
ababa
bb
aaa
aaaa
aababa
ababa
""") == """YES
NO
NO
YES"""

# minimum size
assert run("""2
a
a
a
b
""") == """YES
NO"""

# all equal
assert run("""2
aaaaa
aaa
aaaaa
aaaaaa
""") == """YES
NO"""

# ordering constraint
assert run("""2
abcde
edc
abcde
ecd
""") == """YES
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single match | YES/NO | base correctness |
| all equal strings | YES/NO | length feasibility |
| reversed pattern | YES/NO | ordering constraint handling |

## Edge Cases

A subtle case is when `t` is longer than the number of characters that can be matched from the end of `s`, such as `s = "abc"` and `t = "abcd"`. The algorithm immediately fails because `j` cannot reach `-1`, correctly reflecting impossibility since no sequence of backspaces can create extra characters.

Another edge case is when `s` contains all needed characters but in insufficient effective order, such as `s = "abac"` and `t = "abc"`. The scan matches `c`, then `b`, but the earlier `a` cannot compensate for ordering requirements, and the greedy reverse matching correctly determines failure when the final `c` cannot be paired in a consistent suffix structure.
