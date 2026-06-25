---
title: "CF 106310C - \u041c\u0430\u0433\u0438\u044f \u0441\u043b\u043e\u0432"
description: "The task gives three lowercase English words. Eliza considers a phrase magical if the three words are all different and the phrase contains one or two of the special words see, believe, and repeat, but not all three of them at the same time."
date: "2026-06-25T07:46:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106310
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, 7-8 \u043a\u043b\u0430\u0441\u0441\u044b, \u041f\u0435\u0440\u043c\u0441\u043a\u0438\u0439 \u043a\u0440\u0430\u0439, 2025"
rating: 0
weight: 106310
solve_time_s: 31
verified: true
draft: false
---

[CF 106310C - \u041c\u0430\u0433\u0438\u044f \u0441\u043b\u043e\u0432](https://codeforces.com/problemset/problem/106310/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The task gives three lowercase English words. Eliza considers a phrase magical if the three words are all different and the phrase contains one or two of the special words `see`, `believe`, and `repeat`, but not all three of them at the same time. We need decide whether the given three words satisfy these rules and print `YES` or `NO`.

The input size is deliberately tiny: there are exactly three strings, and every string has length at most 15. This means even a direct comparison against the three magical words is more than fast enough. There is no need for advanced data structures or optimization. A solution that checks every word and performs a constant amount of work is effectively instantaneous.

The main difficulty is not performance but correctly interpreting the conditions. The phrase requires three different words, so duplicate input words must be rejected even if the duplicated word is magical. At the same time, the number of magical words among the three inputs must be at least one and at most two.

Consider the input:

```
see
see
cat
```

The correct output is:

```
NO
```

A careless solution that only counts how many magical words appear might find `see` twice and incorrectly accept the phrase. The words themselves must be distinct.

Another edge case is:

```
see
believe
repeat
```

The correct output is:

```
NO
```

All three special words are present, but the rules explicitly forbid using all three.

A final case is:

```
see
cat
dog
```

The correct output is:

```
YES
```

Only one of the required magical words appears, which is allowed.

## Approaches

A straightforward approach is to compare the three input words with the three special words and count how many of them belong to the magical set. We also compare the words with each other to verify that all three are different. Since there are only three words, the brute force approach can simply try all conditions directly.

The brute force version is already the optimal practical solution here. If we describe the work in terms of operations, there are only a constant number of string comparisons, at most a few dozen character checks because each word has length at most 15. Even an exhaustive approach over the possible checks would perform only a few hundred primitive operations.

The key observation is that the problem has no hidden search space. We are not constructing a phrase or exploring combinations of words. The input already gives the entire phrase, so the answer is determined by two properties: uniqueness of the three words and the count of magical words among them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three words into an array. Keeping them together makes it easy to check both uniqueness and membership in the magical set.
2. Check whether the three words are pairwise different. If any two positions contain the same word, the phrase cannot be magical, so the answer is `NO`.
3. Count how many of the three words are equal to one of `see`, `believe`, or `repeat`. This count represents how many magical words are used in the phrase.
4. If the count is exactly one or exactly two, output `YES`. Otherwise, output `NO`.

The reason this works is that the original rules can be reduced completely to these two checks. The first check enforces that the phrase has three different words. The second check enforces that the number of special words is within the allowed range.

Why it works: the algorithm checks every rule that defines a magical phrase. If it accepts, the words are different and the number of special words is neither zero nor three, so all requirements are satisfied. If it rejects, at least one rule is violated, meaning the phrase cannot be magical.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    words = [input().strip() for _ in range(3)]

    if len(set(words)) != 3:
        print("NO")
        return

    magic = {"see", "believe", "repeat"}
    count = sum(1 for word in words if word in magic)

    if 1 <= count <= 2:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The input is read as exactly three separate lines because the problem always provides three words. The `set` conversion removes duplicates, so comparing its size with three directly checks whether all words are unique.

The magical words are stored in a set because membership checks are the natural operation here. The program then counts how many of the three inputs belong to that set.

The final condition accepts only counts of one or two. Using the range check avoids accidentally accepting zero magical words or the forbidden case where all three magical words appear.

There are no indexing operations or loops depending on input size, so there are no boundary issues. Integer overflow is also impossible because the only integer being stored is a count between zero and three.

## Worked Examples

Example 1:

Input:

```
see
cat
dog
```

| Step | Words | Unique check | Magical count | Result |
| --- | --- | --- | --- | --- |
| Initial | see, cat, dog | Three different words | 0 | Continue |
| Count | see, cat, dog | Passed | 1 | YES |

This example shows the smallest accepted situation where exactly one magical word is used.

Example 2:

Input:

```
see
believe
repeat
```

| Step | Words | Unique check | Magical count | Result |
| --- | --- | --- | --- | --- |
| Initial | see, believe, repeat | Three different words | 0 | Continue |
| Count | see, believe, repeat | Passed | 3 | NO |

This example demonstrates why counting magical words is necessary. Having all three special words is not allowed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three words are processed, each with bounded length. |
| Space | O(1) | The program stores only three words and a fixed set of three magical words. |

The constraints are small enough that the solution uses far less than the available time and memory limits. The approach would also remain efficient if the number of phrases tested were large because each individual phrase requires only constant work.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    words = [sys.stdin.readline().strip() for _ in range(3)]

    if len(set(words)) != 3:
        ans = "NO"
    else:
        magic = {"see", "believe", "repeat"}
        count = sum(1 for word in words if word in magic)
        ans = "YES" if 1 <= count <= 2 else "NO"

    sys.stdin = old_stdin
    return ans + "\n"

assert solution("see\ncat\ndog\n") == "YES\n", "one magical word"
assert solution("see\nbelieve\nrepeat\n") == "NO\n", "all magical words"
assert solution("see\nsee\ncat\n") == "NO\n", "duplicate words"
assert solution("hello\nworld\ncat\n") == "NO\n", "no magical words"
assert solution("repeat\nabc\nbelieve\n") == "YES\n", "two magical words"
assert solution("a\nb\nc\n") == "NO\n", "minimum length ordinary words"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `see, cat, dog` | `YES` | The minimum allowed magical word count |
| `see, believe, repeat` | `NO` | The forbidden case with all three magical words |
| `see, see, cat` | `NO` | Duplicate word detection |
| `hello, world, cat` | `NO` | Rejection when no magical words appear |
| `repeat, abc, believe` | `YES` | Acceptance with two magical words |
| `a, b, c` | `NO` | Handling of short ordinary words |

## Edge Cases

For duplicate words, the input

```
see
see
cat
```

is rejected immediately. The set of words has size two instead of three, so the algorithm never reaches the magical word count check. This prevents duplicated magical words from being mistaken for a valid phrase.

For the case where all three magical words are present:

```
see
believe
repeat
```

the uniqueness condition succeeds because the words are different. The magical count becomes three, and the final condition rejects it because only one or two magical words are allowed.

For a phrase containing exactly one magical word:

```
see
apple
tree
```

the uniqueness condition succeeds and the magical count is one. The algorithm accepts it because one magical word is enough.

For a phrase with no magical words:

```
apple
tree
stone
```

the uniqueness condition succeeds, but the count is zero. The algorithm rejects it because every valid phrase must contain at least one of the three special words.
