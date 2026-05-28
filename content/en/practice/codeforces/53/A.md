---
title: "CF 53A - Autocomplete"
description: "We are asked to implement a simplified autocomplete function. The input consists of a string s, which represents the text the user has typed so far, followed by a list of previously visited pages."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 53
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 49 (Div. 2)"
rating: 1100
weight: 53
solve_time_s: 208
verified: true
draft: false
---

[CF 53A - Autocomplete](https://codeforces.com/problemset/problem/53/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 3m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to implement a simplified autocomplete function. The input consists of a string `s`, which represents the text the user has typed so far, followed by a list of previously visited pages. The goal is to extend `s` into a complete page URL from the visited list, selecting the lexicographically smallest option if multiple pages start with `s`. If no page starts with `s`, we return `s` unchanged.

The input bounds are small: at most 100 visited pages, each of length at most 100. This implies that even a simple linear scan comparing prefixes will run comfortably within the time limit, because the worst-case total number of character comparisons is roughly 100 * 100 = 10,000, which is negligible for a 2-second time limit.

Non-obvious edge cases include the situation where `s` is already equal to some page in the list, or when multiple pages have `s` as a prefix and only one is lexicographically smallest. For example, if `s = "a"` and the visited pages are `["apple", "apricot", "banana"]`, the correct output is `"apple"`, not `"apricot"`. Another subtle case occurs when no pages start with `s`, e.g., `s = "xyz"` and pages are `["abc", "def"]`; the output must be `"xyz"`.

## Approaches

The brute-force approach is straightforward: iterate through all visited pages and check if each page starts with `s`. Collect all matches and select the lexicographically smallest one. This works because the number of pages is small. The check for prefix can be done using Python’s built-in `startswith` method. In the worst case, we compare every character of every page with `s`, resulting in roughly `n * len(page)` comparisons, which is acceptable here.

The optimal approach relies on the same linear scan but avoids unnecessary storage. Instead of collecting all matching pages, we maintain a variable for the current best candidate. For each page that starts with `s`, we update this candidate if it is lexicographically smaller than the previous one. This reduces space complexity and simplifies the logic. The problem constraints are small enough that there is no need for advanced data structures like tries.

The brute-force works because iterating through all pages guarantees that we will find every candidate. The optimization reduces memory usage and improves clarity, but the fundamental time complexity remains linear in the total size of all pages.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n * m) | Accepted |
| Optimized Linear Scan | O(n * m) | O(1) | Accepted |

Here `n` is the number of pages and `m` is the average length of a page.

## Algorithm Walkthrough

1. Read the input string `s` and the number of visited pages `n`. Reading the input first ensures we know what prefix to match and how many candidates exist.
2. Initialize a variable `best_candidate` as `None`. This will hold the current lexicographically smallest page starting with `s`.
3. Iterate through the list of `n` pages. For each page, check if it starts with `s` using the `startswith` method. This step identifies valid candidates for autocomplete.
4. If a page starts with `s` and `best_candidate` is `None`, assign this page to `best_candidate`. This ensures we always have at least one candidate if any page matches.
5. If a page starts with `s` and `best_candidate` is not `None`, compare the page with `best_candidate` lexicographically. If it is smaller, update `best_candidate`. This step maintains the invariant that `best_candidate` is always the smallest matching page so far.
6. After iterating through all pages, check if `best_candidate` is still `None`. If so, no pages matched, and we print `s` unchanged. Otherwise, print `best_candidate`.

Why it works: The algorithm maintains the invariant that at any point, `best_candidate` is the lexicographically smallest page encountered that starts with `s`. Iterating through all pages guarantees we do not miss any candidate, so by the end, `best_candidate` contains the correct answer if any page matches.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = int(input())
best_candidate = None

for _ in range(n):
    page = input().strip()
    if page.startswith(s):
        if best_candidate is None or page < best_candidate:
            best_candidate = page

print(best_candidate if best_candidate is not None else s)
```

The code first reads the typed string `s` and the number of visited pages. Each page is read and stripped of whitespace. The `startswith` method identifies matches efficiently. The comparison `page < best_candidate` ensures the lexicographically smallest page is selected. Using `None` for the initial candidate avoids pre-setting it to a value that could incorrectly compare with actual pages.

## Worked Examples

Using Sample 1:

| Step | Page | Starts with `s`? | Best candidate | Reason |
| --- | --- | --- | --- | --- |
| 1 | nextpermutation | yes | nextpermutation | First match |
| 2 | nextelement | yes | nextelement | Smaller than previous candidate |

Output: `nextelement`. This demonstrates the algorithm correctly picks the smallest lexicographical match.

Another example:

Input:

```
abc
3
abcd
abce
abd
```

| Step | Page | Starts with `s`? | Best candidate | Reason |
| --- | --- | --- | --- | --- |
| 1 | abcd | yes | abcd | First match |
| 2 | abce | yes | abcd | abce > abcd, no change |
| 3 | abd | yes | abcd | abd > abcd, no change |

Output: `abcd`. The algorithm preserves the smallest prefix match throughout iteration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | Each of the n pages is checked character by character up to length m for prefix matching |
| Space | O(1) | Only a single string variable is maintained regardless of input size |

Given n ≤ 100 and m ≤ 100, the algorithm performs at most 10,000 character comparisons, which is well within the 2-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    n = int(input())
    best_candidate = None
    for _ in range(n):
        page = input().strip()
        if page.startswith(s):
            if best_candidate is None or page < best_candidate:
                best_candidate = page
    return best_candidate if best_candidate is not None else s

# provided sample
assert run("next\n2\nnextpermutation\nnextelement\n") == "nextelement", "sample 1"

# s matches exactly one page
assert run("abc\n3\nabcd\nabce\nabd\n") == "abcd", "smallest lex first"

# s matches no page
assert run("xyz\n3\nabc\ndef\nghi\n") == "xyz", "no match"

# multiple identical pages
assert run("go\n4\ngo\ngo\ngone\ngood\n") == "go", "multiple identical pages"

# s equals a page exactly
assert run("home\n2\nhome\nhomepage\n") == "home", "exact match"

# minimum input size
assert run("a\n1\na\n") == "a", "single page"

# maximum page length
assert run("longprefix\n2\nlongprefixaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nlongprefixbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n") == "longprefixaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "max length comparison"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abc\n3\nabcd\nabce\nabd\n` | `abcd` | Lexicographically smallest prefix |
| `xyz\n3\nabc\ndef\nghi\n` | `xyz` | No match case |
| `go\n4\ngo\ngo\ngone\ngood\n` | `go` | Multiple identical pages |
| `home\n2\nhome\nhomepage\n` | `home` | Exact match handling |
| `a\n1\na\n` | `a` | Minimum-size input |
| long prefixes | first lex smallest | Maximum length handling |

## Edge Cases

When `s` matches no visited pages, such as `s = "xyz"` and pages `["abc", "def"]`, the algorithm never updates `best_candidate`, leaving it `None`. The final check prints `s`, correctly handling this scenario.

When multiple pages start with `s` and are identical, the first match sets `best_candidate`, and subsequent identical pages do not alter it. For `s = "go"` and pages `["go", "go", "gone", "good"]`, the algorithm returns `"go"` because it is already lexicographically smallest.

When `s` exactly equals a page, such as `s = "home"` and pages `["home", "homepage"]`, the algorithm selects `"home"` correctly because it starts with `s` and is the smallest in
