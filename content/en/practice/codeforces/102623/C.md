---
title: "CF 102623C - Cheat Sheet"
description: "The cheat sheet has a fixed capacity measured in characters. Setsuna has a collection of keywords, but repeated keywords only matter once because the final sheet cannot contain duplicates."
date: "2026-08-04T17:11:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "C"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 73
verified: true
draft: false
---

[CF 102623C - Cheat Sheet](https://codeforces.com/problemset/problem/102623/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The cheat sheet has a fixed capacity measured in characters. Setsuna has a collection of keywords, but repeated keywords only matter once because the final sheet cannot contain duplicates. If several keywords are placed on the sheet, they need a single space between neighboring words, so the total occupied length is the sum of the chosen keyword lengths plus one separator for every connection between two chosen keywords.

The task is to choose the largest possible number of different keywords whose total written length does not exceed the available space.

The number of keywords is at most 1000, and each keyword length is at most 100. This means the input is small enough for sorting and linear scans, but it is not suitable for trying every subset. With 1000 different keywords, the number of possible choices is 2^1000, which is far beyond what can be explored in the time limit.

There are several details that can cause wrong answers. Duplicate words must not be counted twice. For example:

```
n = 10, m = 3
hello hello hi
```

The correct answer is 2 because the available words are only `hello` and `hi`. A careless implementation that processes every input word separately might count three possible keywords.

The spaces between words also affect the answer. For example:

```
n = 7, m = 2
abc defg
```

The correct answer is 1. The two words together need 3 + 1 + 4 = 8 characters, so they cannot both fit. An implementation that only compares the sum of word lengths with `n` would incorrectly return 2.

The order of uppercase and lowercase letters matters. For example:

```
n = 5, m = 2
A a
```

The correct answer is 2 because these are different keywords and they fit exactly with one space: 1 + 1 + 1 = 3 characters.

## Approaches

A direct solution would consider every possible group of keywords, remove duplicates inside the group, calculate its total length, and keep the largest group that fits. This approach is correct because it checks every possible answer. However, the number of subsets grows exponentially. Even with only 60 keywords, there would already be more than 10^18 possible subsets, making this strategy unusable.

The key observation is that every keyword has the same cost structure except for its length. If we decide to put `k` keywords on the cheat sheet, the spaces contribute exactly `k - 1` characters. The goal is not to maximize the total length used, but to maximize the number of chosen keywords. Since every chosen keyword contributes exactly one to the answer, the best choice is always to spend the available space on the shortest keywords.

After removing duplicates, sort the remaining keywords by length. Taking keywords from shortest to longest gives the maximum possible count. If a longer keyword can fit at some point, replacing any selected shorter keyword with it would not increase the number of selected words and could only consume more space. This greedy ordering captures all useful choices without needing to try combinations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m * m) | O(m) | Too slow |
| Optimal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read all keywords and insert them into a set. The set removes repeated keywords because writing the same keyword multiple times is never allowed and never increases the answer.
2. Convert the distinct keywords into a list and sort it by length in increasing order. Shorter keywords are preferred because each selected keyword has equal value, but shorter ones consume less space.
3. Keep a variable representing the number of characters currently used and another variable for the number of selected keywords. Initially both values are zero.
4. Iterate through the sorted keywords. For the current keyword, calculate the additional space needed. If no keyword has been selected yet, the cost is only its length. Otherwise, the cost is its length plus one because a separating space is required.
5. Add the keyword if the new total still fits inside the cheat sheet limit. Increase the selected count and continue. If the keyword does not fit, stop checking further keywords because all remaining keywords are at least as long.

Why it works:

After sorting, the algorithm always considers keywords from the cheapest to the most expensive. Suppose an optimal answer contains a longer keyword while a shorter unchosen keyword exists. Replacing the longer keyword with the shorter one keeps the number of chosen keywords unchanged and does not increase the used space. Repeating this exchange means there is always an optimal solution containing the shortest available keywords. The algorithm constructs exactly this set, so the number it returns is maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    words = input().split()

    words = list(set(words))
    words.sort(key=len)

    used = 0
    answer = 0

    for word in words:
        add = len(word)
        if answer > 0:
            add += 1

        if used + add <= n:
            used += add
            answer += 1
        else:
            break

    print(answer)

if __name__ == "__main__":
    solve()
```

The set conversion handles duplicate keywords before any calculation begins. This is necessary because duplicates cannot appear together on the cheat sheet.

Sorting by `len` puts the words in the exact order needed by the greedy choice. During the scan, `used` stores the complete current size of the cheat sheet, including all spaces already placed between words.

The variable `answer` also tells us whether a separator is needed before the next word. The first chosen word has no space before it, while every later chosen word adds one extra character.

When a word cannot fit, the loop ends immediately. All later words have equal or greater length, so they cannot possibly fit either. This avoids unnecessary checks and also avoids mistakes involving separator counting.

Python integers do not have overflow issues here because the maximum possible total size is only around 101000 characters.

## Worked Examples

For the first sample, after removing duplicates the keywords are:

```
myworld lusto KR12138 oneman233 SetsunaQAQ
```

The sorted order by length is `lusto`, `myworld`, `KR12138`, `oneman233`, `SetsunaQAQ`.

| Current keyword | Added length | Used characters | Selected count |
| --- | --- | --- | --- |
| lusto | 5 | 5 | 1 |
| myworld | 8 | 13 | 2 |
| KR12138 | 8 | 21 | 3 |
| oneman233 | 10 | 31 | 4 |
| SetsunaQAQ | 11 | 42 | 4 |

The final word does not fit because the total would exceed 40. The trace shows why sorting by length is enough: the first four shortest words are exactly the best four choices.

For the second sample:

```
n = 7
^_^ ^_^
```

After removing duplicates, only one keyword remains.

| Current keyword | Added length | Used characters | Selected count |
| --- | --- | --- | --- |
| ^_^ | 3 | 3 | 1 |

The result is 1 because duplicate keywords do not create additional choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Removing duplicates takes linear expected time, and sorting the distinct keywords dominates the complexity |
| Space | O(m) | The set and list store the distinct keywords |

The maximum number of input keywords is only 1000, so sorting is easily within the limits. The memory usage is also small because each keyword has limited length.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n, m = map(int, sys.stdin.readline().split())
    words = sys.stdin.readline().split()

    words = list(set(words))
    words.sort(key=len)

    used = 0
    answer = 0

    for word in words:
        add = len(word) + (1 if answer > 0 else 0)
        if used + add <= n:
            used += add
            answer += 1
        else:
            break

    sys.stdin = old_stdin
    return str(answer)

assert solve("40 5\nmyworld lusto KR12138 oneman233 SetsunaQAQ\n") == "4", "sample 1"
assert solve("7 2\n^_^ ^_^\n") == "1", "sample 2"

assert solve("1 1\na\n") == "1", "minimum size"
assert solve("10 3\nhello hello hi\n") == "2", "duplicates"
assert solve("7 2\nabc defg\n") == "1", "separator boundary"
assert solve("1000 1000\n" + " ".join(["x"] * 1000) + "\n") == "1", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `40 5` sample input | 4 | Normal greedy selection with several different lengths |
| `7 2` duplicate input | 1 | Duplicate removal |
| `1 1` with `a` | 1 | Smallest possible capacity |
| `10 3` with `hello hello hi` | 2 | Handling repeated keywords |
| `7 2` with `abc defg` | 1 | Correct separator accounting |
| 1000 identical one-character words | 1 | All-equal values and set behavior |

## Edge Cases

A repeated keyword is reduced to a single choice before sorting. For:

```
10 3
hello hello hi
```

the set contains only `hello` and `hi`. The algorithm sorts them as `hi`, `hello`, takes `hi`, and then takes `hello` because the total is 8 characters including the separator. The output is 2.

A separator can be the reason a word does not fit. For:

```
7 2
abc defg
```

the algorithm first accepts `abc`, using 3 characters. The next keyword needs 1 space plus 4 characters, so the new total would be 8. It is rejected, producing 1.

Uppercase and lowercase keywords remain separate because the set compares strings exactly. For:

```
5 2
A a
```

the sorted list contains both words. The first uses 1 character and the second adds 1 separator plus 1 character, so the answer becomes 2.

The first keyword has a special boundary condition because it does not need a preceding space. The implementation handles this by adding a separator only when at least one word has already been chosen.

You can adjust the editorial length or make the explanation more contest-style if needed.
