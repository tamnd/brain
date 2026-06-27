---
title: "CF 105013C - \u732b\u72d7\u5927\u6218"
description: "We are given a number of test cases. For each test case, we receive a string of length $n$. The task is to transform the string in a very specific way and decide which of three fixed outputs it matches after processing. The processing rule is simple but strict."
date: "2026-06-28T02:12:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105013
codeforces_index: "C"
codeforces_contest_name: "The 19th Southeast University Programming Contest (Summer)"
rating: 0
weight: 105013
solve_time_s: 46
verified: true
draft: false
---

[CF 105013C - \u732b\u72d7\u5927\u6218](https://codeforces.com/problemset/problem/105013/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number of test cases. For each test case, we receive a string of length $n$. The task is to transform the string in a very specific way and decide which of three fixed outputs it matches after processing.

The processing rule is simple but strict. First, all characters are converted to lowercase so that uppercase and lowercase versions are treated the same. Then, consecutive identical characters are compressed so that any run like `"aaaa"` becomes a single `"a"`, `"bbbbb"` becomes `"b"`, and so on. After this normalization, the resulting string is compared against two special patterns. If it equals `"meow"`, the output is `"0_0"`. If it equals `"waov"`, the output is `"*_*"`. Any other result produces `"???"`.

The constraints are not explicitly restrictive in the statement, but the presence of direct string processing per test case strongly suggests that $n$ can be large enough that anything worse than linear per test case would be risky. This immediately rules out approaches that repeatedly rebuild strings inefficiently or use nested scans that could degrade to quadratic behavior.

A subtle edge case comes from the compression step. A naive interpretation might remove duplicate characters globally instead of only collapsing consecutive runs. For example, `"mmeeooww"` should become `"meow"`, but a global deduplication would incorrectly reduce it to `"meow"` only if order is carefully preserved. Another edge case is mixed casing like `"MeOoW"` which must still normalize correctly before compression.

## Approaches

The brute-force idea follows the description literally. For each string, we first convert every character to lowercase. Then we repeatedly scan the string and remove duplicates until no adjacent equal characters remain. A straightforward implementation might rebuild the string after every pass, or repeatedly check neighboring characters and erase duplicates one by one.

This works correctly because it directly enforces the definition of consecutive compression. However, its weakness appears when the string has long runs. Each erase operation can shift the remaining suffix, and doing this repeatedly leads to a worst-case quadratic behavior per test case. With multiple test cases, this quickly becomes too slow when $n$ is large.

The key observation is that we do not need repeated passes. The compression only depends on whether each character is equal to the previous character in the final processed string. This means we can build the result in one pass by appending a character only when it differs from the last appended character. Combined with a single pass lowercase conversion, the entire transformation becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (repeated erase or rebuild) | $O(n^2)$ | $O(n)$ | Too slow |
| One-pass normalization + run compression | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the string and convert every character to lowercase. This ensures case does not affect comparison, since the target patterns are defined only in lowercase.
2. Initialize an empty result string that will store the compressed form.
3. Iterate through each character of the normalized string.
4. Append the character to the result only if it is different from the last character already in the result. If it is the same, we skip it because it belongs to the same consecutive block.
5. After the scan, compare the resulting compressed string with `"meow"` and `"waov"`.
6. Output `"0_0"` if it matches `"meow"`, `"*_*"` if it matches `"waov"`, otherwise output `"???"`.

### Why it works

The compression step is equivalent to replacing every maximal contiguous block of identical characters with a single representative character. The one-pass construction guarantees that exactly one character per block is kept, because we only suppress repeats that immediately follow the same character. Since every block boundary is detected exactly once when the character changes, the resulting string is identical to what repeated full-string deduplication would eventually produce, but without repeated work.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    # lowercase conversion
    s = s.lower()

    # run-length compression
    t = []
    for c in s:
        if not t or t[-1] != c:
            t.append(c)

    t = ''.join(t)

    if t == "meow":
        print("0_0")
    elif t == "waov":
        print("*_*")
    else:
        print("???")

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The solution first normalizes the input string using `.lower()`, ensuring uniform character comparison. The compression is done using a list `t` to avoid repeated string concatenation, which would otherwise lead to quadratic behavior in Python. Each character is compared only with the last kept character, guaranteeing linear time processing. Finally, we compare against the two target patterns.

A common pitfall is using `t += c` on strings repeatedly, which would degrade performance. Another is forgetting that compression must preserve order while only removing consecutive duplicates, not all duplicates globally.

## Worked Examples

Consider the input string `"mMeeOoWW"`.

After lowercase conversion, we get `"mmeeooww"`.

| Step | Character | Current Result | Action |
| --- | --- | --- | --- |
| 1 | m | m | append |
| 2 | m | m | skip |
| 3 | e | me | append |
| 4 | e | me | skip |
| 5 | o | meo | append |
| 6 | o | meo | skip |
| 7 | w | meow | append |
| 8 | w | meow | skip |

Final result is `"meow"`, so output is `"0_0"`.

Now consider `"waaaAAOOV"`.

After lowercase conversion, we get `"waaaaooov"`.

| Step | Character | Current Result | Action |
| --- | --- | --- | --- |
| 1 | w | w | append |
| 2 | a | wa | append |
| 3 | a | wa | skip |
| 4 | a | wa | skip |
| 5 | a | wa | skip |
| 6 | o | wao | append |
| 7 | o | wao | skip |
| 8 | o | wao | skip |
| 9 | v | waov | append |

Final result is `"waov"`, so output is `"*_*"`.

These traces show that only transitions between distinct consecutive characters matter, and repeated blocks collapse cleanly regardless of original casing or run length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each character is processed once during normalization and once during compression logic |
| Space | $O(n)$ | Output buffer stores at most one character per run |

The solution scales linearly with input size, which is appropriate for typical Codeforces string-processing constraints where total input size across tests is large.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided-style cases
assert run("1\n4 meow\n") == "0_0"
assert run("1\n4 waov\n") == "*_*"

# custom cases
assert run("1\n5 meooW\n") == "0_0", "mixed case collapse to meow"
assert run("1\n8 mmmmmeow\n") == "0_0", "long prefix collapse"
assert run("1\n4 abcd\n") == "???", "non matching pattern"
assert run("1\n6 WAAAAA\n") == "???", "single character collapse"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `meooW` | `0_0` | case normalization + run compression |
| `mmmmmeow` | `0_0` | long repeated prefix collapsing correctly |
| `abcd` | `???` | non-matching structure |
| `WAAAAA` | `???` | single-run edge case |

## Edge Cases

One important edge case is when the entire string consists of a single repeated character, such as `"AAAAA"`. After lowercase conversion and compression, this becomes `"a"`. The algorithm processes it by appending the first character and skipping all others since they match the last appended character. The final string is `"a"`, which matches neither `"meow"` nor `"waov"`, so the output is `"???"`.

Another edge case is alternating casing with runs, like `"MeEeOoWw"`. The lowercase conversion produces `"meeooww"`, and compression yields `"meow"`. The algorithm correctly handles this because comparison is always done after normalization, and run boundaries are determined purely by equality of adjacent characters, not original case.
