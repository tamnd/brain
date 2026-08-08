---
title: "CF 102460D - Tapioka"
description: "A dish name contains exactly three lowercase words. Some of those words are part of the tapioka decoration and must be removed. The removable words are exactly bubble and tapioka."
date: "2026-08-08T10:02:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102460
codeforces_index: "D"
codeforces_contest_name: "2019-2020 ICPC Asia Taipei-Hsinchu Regional Contest"
rating: 0
weight: 102460
solve_time_s: 194
verified: true
draft: false
---

[CF 102460D - Tapioka](https://codeforces.com/problemset/problem/102460/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

A dish name contains exactly three lowercase words. Some of those words are part of the tapioka decoration and must be removed. The removable words are exactly `bubble` and `tapioka`. Every other word belongs to the actual dish and must remain in its original position relative to the other surviving words.

For example, `bubble tea pizza` becomes `tea pizza`, while `tapioka cake tapiokas` becomes `cake tapiokas`. The second example is deliberately useful because `tapiokas` is not the same word as `tapioka`, so it must not be removed.

After filtering all three words, there may be nothing left. In that case the required output is the word `nothing`.

The input is extremely small: there are exactly three words, and each word has length at most 32. Even an algorithm that repeatedly scans the whole input would perform only a constant number of operations. The 2-second time limit and large memory limit are therefore not restrictive for this problem. More generally, if the same task were extended to an array of up to (10^5) words, an (O(n)) solution would be the natural target, while repeatedly scanning the entire array after every deletion could become (O(n^2)).

There are a few cases where a careless implementation can produce the wrong result. First, a word must match exactly. For `tapioka cake tapiokas`, the correct output is `cake tapiokas`. A substring-based replacement could incorrectly treat `tapiokas` as containing the removable word `tapioka`, which would delete a word that should remain.

Second, all removable words may disappear. For `tapioka bubble tapioka`, every word is removable, so the correct output is `nothing`. A solution that simply joins the remaining list would produce an empty line instead.

Third, the order of surviving words must not change. For `bubble ramen cake`, the correct output is `ramen cake`. Filtering in place or constructing a new list both work, but sorting or otherwise rearranging the words would violate the required order.

## Approaches

A direct brute-force interpretation is to repeatedly look through the current list, remove every word equal to `bubble` or `tapioka`, and continue until no removable word remains. This is correct because every occurrence is eventually deleted, while every other word is preserved. With exactly three words, the worst case performs at most three full scans, each examining at most three positions, so there are at most 9 word comparisons. It is impossible for this version to become too slow under the actual constraints.

If we imagine the same operation on (n) words, however, repeatedly scanning after deletions could require (O(n^2)) comparisons in the worst case. The structure of this problem gives us a simpler observation: removing a word does not affect whether any other word should be removed. Each word can be classified independently by checking whether it is exactly `bubble` or exactly `tapioka`. That means there is no need to simulate removal at all.

The optimal solution makes one pass over the three words. If a word is removable, we skip it. Otherwise, we append it to the answer. At the end, an empty answer is replaced by `nothing`. This reduces the generalized version of the problem to linear time and is simpler than modifying the input repeatedly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) in a generalized version, at most 9 comparisons here | (O(n)) | Accepted here |
| Optimal | (O(n)) | (O(n)) | Accepted |

Here (n=3) for the actual problem, so both approaches are easily fast enough. The one-pass version is preferable because its correctness follows directly from the independent treatment of each word.

## Algorithm Walkthrough

1. Read the single input line and split it into its three words. Splitting by whitespace gives us the individual dish components without needing to handle character positions manually.
2. Create an empty list for the words that belong to the actual dish.
3. Examine each input word once. If it is exactly `bubble` or exactly `tapioka`, discard it. Otherwise, append it to the result list. Exact equality is necessary because words such as `tapiokas` must survive.
4. After all three words have been processed, check whether the result list is empty. If it is empty, print `nothing`, because the entire dish consisted of removable words.
5. Otherwise, join the surviving words with single spaces and print them. Since words are appended in their original order, the output order is automatically correct.

### Why it works

After processing any prefix of the input, the result list contains exactly those words from that prefix that are neither `bubble` nor `tapioka`, in their original order. When the next word is removable, skipping it preserves this property. When the next word is not removable, appending it also preserves the property. By the time all three words have been processed, the result contains exactly every required word and no removable word. If the result is empty, every input word was removable, so `nothing` is exactly the required output.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    words = input().split()

    result = []

    for word in words:
        if word != "bubble" and word != "tapioka":
            result.append(word)

    if result:
        print(" ".join(result))
    else:
        print("nothing")

if __name__ == "__main__":
    solve()
```

The input is read as one line and split into individual words, matching the fact that the dish name contains exactly three words. The `result` list stores only words that survive the filtering step from the algorithm.

The condition uses exact string equality rather than substring checks. This is the subtle part of the implementation: `tapiokas`, `bubbletea`, and other words containing a removable word are still valid dish words and must remain untouched.

The loop processes every word exactly once, so there are no index manipulations or deletion operations that could introduce off-by-one errors. Python's strings are compared directly, and there are no numeric calculations, so integer overflow is irrelevant.

Finally, checking `if result` distinguishes the two possible output forms. A nonempty result is joined with spaces, while an empty result becomes `nothing`.

## Worked Examples

### Sample 1

For the input `bubble tea pizza`, the first word is removable, while the other two words survive.

| Word | Removable? | Result after step |
| --- | --- | --- |
| `bubble` | Yes | `[]` |
| `tea` | No | `[`tea`]` |
| `pizza` | No | `[`tea`, `pizza`]` |

The final list contains `tea` and `pizza`, so joining it with spaces produces `tea pizza`. This demonstrates that filtering preserves the original order of the surviving words.

### Sample 2

For the input `tapioka cake tapiokas`, the first word is removed. The second and third words survive because `cake` is unrelated to tapioka and `tapiokas` is not exactly `tapioka`.

| Word | Removable? | Result after step |
| --- | --- | --- |
| `tapioka` | Yes | `[]` |
| `cake` | No | `[`cake`]` |
| `tapiokas` | No | `[`cake`, `tapiokas`]` |

The final output is `cake tapiokas`. This trace specifically confirms that the comparison must be for the complete word rather than a substring.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every input word is checked exactly once, with (n=3) here. |
| Space | (O(n)) | The surviving words are stored in the result list. |

For the actual problem, (n) is always 3 and every word has at most 32 characters, so the algorithm performs only a handful of string comparisons and uses negligible memory. It is comfortably within the given limits.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    words = inp.split()

    result = []
    for word in words:
        if word != "bubble" and word != "tapioka":
            result.append(word)

    if result:
        return " ".join(result)
    return "nothing"

# Provided samples
assert solve("bubble tea pizza") == "tea pizza", "sample 1"
assert solve("tapioka cake tapiokas") == "cake tapiokas", "sample 2"
assert solve("tapioka jasmine tea") == "jasmine tea", "sample 3"
assert solve("tapioka bubble tapioka") == "nothing", "sample 4"

# Minimum-size style case: three words with two removable words.
assert solve("bubble tapioka cake") == "cake", "two removable words"

# All three words are removable.
assert solve("tapioka tapioka tapioka") == "nothing", "all removable"

# Exact-word boundary: tapiokas must not be removed.
assert solve("bubble tapiokas bubble") == "tapiokas", "exact word matching"

# Maximum word length and non-removable words.
w = "a" * 32
x = "b" * 32
assert solve(f"bubble {w} {x}") == f"{w} {x}", "maximum word length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `bubble tapioka cake` | `cake` | Multiple removable words and a single surviving word |
| `tapioka tapioka tapioka` | `nothing` | Every word is removed |
| `bubble tapiokas bubble` | `tapiokas` | Exact matching rather than substring matching |
| `bubble` followed by two 32-letter words | The two long words | Maximum word length and preservation of ordinary words |

## Edge Cases

The first important edge case is when every word is removable. For `tapioka bubble tapioka`, the loop skips all three words, leaving `result` empty. The final check detects this and prints `nothing` instead of printing an empty line.

The second edge case is exact word matching. For `tapioka cake tapiokas`, the first word satisfies `word == "tapioka"` and is removed. The word `tapiokas` fails that comparison and is appended to the result. The final output is `cake tapiokas`. A substring replacement such as replacing every occurrence of `"tapioka"` inside the line would incorrectly damage this word.

The third edge case is that removable words can appear next to ordinary words in any allowed position. For `bubble tapiokas bubble`, the first and third words are discarded, while the middle word remains. The algorithm produces `tapiokas`, showing that it does not rely on the removable words being confined to one particular position.

The fourth edge case is the maximum word length. With a 32-character ordinary word, the comparison logic does not change at all. Since Python handles the complete strings directly, the word length only affects the small cost of the string comparison and does not create any boundary issue.
