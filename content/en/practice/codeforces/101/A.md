---
title: "CF 101A - Homework"
description: "We start with a lowercase string and may delete at most k characters from it. The remaining characters must stay in their original order, since deleting characters creates a subsequence."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 101
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 79 (Div. 1 Only)"
rating: 1200
weight: 101
solve_time_s: 125
verified: true
draft: false
---

[CF 101A - Homework](https://codeforces.com/problemset/problem/101/A)

**Rating:** 1200  
**Tags:** greedy  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a lowercase string and may delete at most `k` characters from it. The remaining characters must stay in their original order, since deleting characters creates a subsequence. Our goal is not to maximize the remaining length, but to minimize how many distinct letters still appear.

If a letter appears even once in the final string, that letter still counts as one distinct character. To completely remove a letter from the result, we must delete every occurrence of that letter.

This changes the problem from "which positions should we erase?" into "which character types should we erase entirely?". If a character appears 7 times, removing that character costs 7 deletions. If it appears once, removing it costs only 1 deletion.

The string length can reach `10^5`, which immediately rules out anything exponential or quadratic in `n`. We cannot try all subsets of characters to remove, and we also cannot repeatedly rebuild large strings in nested loops. An `O(n log n)` or `O(n)` solution is the right target.

There are several edge cases that are easy to mishandle.

Consider:

```
aaaaa
4
```

We are allowed to delete at most 4 characters, but deleting all 5 would exceed the limit. The answer is still 1 distinct character, not 0. A careless implementation might greedily delete as much as possible and accidentally remove the entire string.

Now consider:

```
abc
10
```

Here we can delete every character because `k` is larger than the string length. The correct answer is 0 and the resulting string is empty. Some solutions incorrectly force at least one character to remain.

Another subtle case is:

```
aabbbcccc
5
```

The frequencies are `2, 3, 4`. If we delete `'a'` and `'b'`, we spend exactly 5 deletions and reduce the answer to 1 distinct character. A naive greedy strategy that deletes the largest groups first would fail badly here, because removing `'c'` costs 4 and leaves two distinct letters instead of one.

The key observation is that removing a character type has a fixed cost equal to its frequency. To minimize the number of remaining distinct letters, we should remove the cheapest character types first.

## Approaches

A brute-force solution would try every subset of distinct characters and check whether deleting all occurrences of those characters costs at most `k`. If the alphabet subset is valid, we count how many distinct letters remain and keep the minimum.

This works because the choice is fundamentally about character types, not positions. Once we decide which letters disappear completely, the resulting subsequence is uniquely determined by keeping all other characters.

The problem is the number of subsets. Even though the alphabet only contains lowercase English letters, there are still `2^26` subsets, which is about 67 million possibilities. That is far too large for a 2-second limit.

The important structural property is that every character type has an independent deletion cost. Removing `'a'` never affects the cost of removing `'b'`. We are effectively choosing as many character types as possible whose frequencies fit within a budget `k`.

This turns into a greedy problem. Suppose two character types have frequencies 2 and 5. If we can only afford one of them, deleting the frequency-2 character is always at least as good as deleting the frequency-5 character, because both reduce the distinct count by exactly 1, but one is cheaper.

That observation completely determines the strategy:

1. Count frequencies.
2. Sort character types by frequency.
3. Remove the smallest groups first while we still have enough deletions left.
4. Rebuild the answer using only the remaining character types.

The alphabet size is only 26, so sorting frequencies is essentially constant time. The dominant work is scanning the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^26 · 26 + n) | O(26) | Too slow |
| Optimal | O(n + 26 log 26) | O(26) | Accepted |

## Algorithm Walkthrough

1. Read the string `s` and the integer `k`.
2. Count how many times each character appears in the string.

We need these frequencies because deleting a character completely costs exactly its frequency.
3. Store all `(frequency, character)` pairs and sort them in ascending order of frequency.

The cheapest character types should be considered first, because each fully removed character reduces the distinct count by exactly 1.
4. Traverse the sorted list.

If the current frequency is less than or equal to the remaining deletion budget `k`, delete that entire character type:

- subtract its frequency from `k`
- mark the character as removed

Otherwise stop removing characters.

Once we cannot afford the current smallest frequency, we also cannot afford any later frequency because the list is sorted.
5. Build the final string by keeping only characters that were not removed.

This automatically preserves the original order, so the result is a valid subsequence.
6. Count how many distinct characters remain and print:

- the number of remaining distinct characters
- the resulting subsequence

### Why it works

Each deleted character type gives exactly the same benefit, reducing the distinct count by 1. The only difference between choices is their cost, which equals their frequency.

Suppose an optimal solution deletes a character with frequency 5 but keeps another with frequency 2. Swapping these choices cannot increase the total deletions used, and still removes one distinct character. Repeating this exchange argument transforms any optimal solution into one that always deletes the smallest frequencies first.

Because of that property, the greedy strategy is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
k = int(input())

freq = [0] * 26

for ch in s:
    freq[ord(ch) - ord('a')] += 1

pairs = []

for i in range(26):
    if freq[i] > 0:
        pairs.append((freq[i], chr(i + ord('a'))))

pairs.sort()

removed = set()

for cnt, ch in pairs:
    if cnt <= k:
        k -= cnt
        removed.add(ch)
    else:
        break

result = []

for ch in s:
    if ch not in removed:
        result.append(ch)

answer = ''.join(result)

print(len(set(answer)))
print(answer)
```

The first section counts frequencies using a fixed-size array of length 26. This is faster and simpler than using a dictionary because the alphabet is known in advance.

The `(frequency, character)` pairs are sorted so that the cheapest character types appear first. The greedy loop removes entire character groups while the budget allows it.

The stopping condition is important. Once a frequency is too large, every later frequency is also too large because the array is sorted. Continuing the loop would accomplish nothing.

The final reconstruction step scans the original string and skips removed characters. This preserves relative order automatically, so the result remains a subsequence.

One subtle point is the empty-string case. If every character type is removed, `answer` becomes `""`, and `len(set(answer))` correctly evaluates to `0`.

## Worked Examples

### Example 1

Input:

```
aaaaa
4
```

Frequencies:

| Character | Frequency |
| --- | --- |
| a | 5 |

Sorted pairs:

| Step | Current Pair | k Before | Can Remove? | k After | Removed |
| --- | --- | --- | --- | --- | --- |
| 1 | (5, a) | 4 | No | 4 | {} |

Rebuilding the string keeps all characters:

| Position | Character | Removed? | Result |
| --- | --- | --- | --- |
| 1 | a | No | a |
| 2 | a | No | aa |
| 3 | a | No | aaa |
| 4 | a | No | aaaa |
| 5 | a | No | aaaaa |

Final answer:

```
1
aaaaa
```

This example shows why we cannot always delete everything possible. The only character type costs 5 deletions, but the budget is only 4.

### Example 2

Input:

```
aaaabbb
4
```

Frequencies:

| Character | Frequency |
| --- | --- |
| a | 4 |
| b | 3 |

Sorted pairs:

| Step | Current Pair | k Before | Can Remove? | k After | Removed |
| --- | --- | --- | --- | --- | --- |
| 1 | (3, b) | 4 | Yes | 1 | {b} |
| 2 | (4, a) | 1 | No | 1 | {b} |

Rebuilding the string:

| Position | Character | Removed? | Result |
| --- | --- | --- | --- |
| 1 | a | No | a |
| 2 | a | No | aa |
| 3 | a | No | aaa |
| 4 | a | No | aaaa |
| 5 | b | Yes | aaaa |
| 6 | b | Yes | aaaa |
| 7 | b | Yes | aaaa |

Final answer:

```
1
aaaa
```

This trace demonstrates the greedy principle clearly. Removing the cheaper character group first gives the best reduction in distinct letters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 26 log 26) | Counting and rebuilding scan the string once, sorting at most 26 frequencies |
| Space | O(26) | Frequency storage and removed-character tracking |

Since the alphabet size is fixed, the sorting cost is effectively constant. The solution is dominated by linear scans over the string, which easily fits within the limits for `n = 10^5`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    k = int(input())

    freq = [0] * 26

    for ch in s:
        freq[ord(ch) - ord('a')] += 1

    pairs = []

    for i in range(26):
        if freq[i] > 0:
            pairs.append((freq[i], chr(i + ord('a'))))

    pairs.sort()

    removed = set()

    for cnt, ch in pairs:
        if cnt <= k:
            k -= cnt
            removed.add(ch)
        else:
            break

    ans = ''.join(ch for ch in s if ch not in removed)

    print(len(set(ans)))
    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("aaaaa\n4\n") == "1\naaaaa\n", "sample 1"

# delete one entire character group
assert run("aaaabbb\n4\n") == "1\naaaa\n", "remove b"

# delete everything
assert run("abc\n10\n") == "0\n\n", "empty result"

# minimum size input
assert run("a\n0\n") == "1\na\n", "single character"

# exact budget match
assert run("aabbbcccc\n5\n") == "1\ncccc\n", "remove a and b"

# no deletions allowed
assert run("abac\n0\n") == "3\nabac\n", "unchanged string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / 0` | `a` remains | Minimum-size input |
| `abc / 10` | Empty string | Full deletion case |
| `aaaabbb / 4` | Keep only `a` | Greedy removes smaller frequency |
| `aabbbcccc / 5` | Keep only `cccc` | Exact budget consumption |
| `abac / 0` | Original string | Zero-deletion boundary |

## Edge Cases

Consider the case where deleting all characters is impossible:

```
aaaaa
4
```

The frequency list contains only `(5, 'a')`. Since `5 > 4`, the greedy loop removes nothing. The reconstruction step keeps every character, producing `"aaaaa"` with 1 distinct letter. This confirms the algorithm never exceeds the deletion budget.

Now consider the opposite extreme:

```
abc
10
```

The sorted frequencies are `(1, 'a')`, `(1, 'b')`, `(1, 'c')`.

The algorithm removes all three groups:

| Character | Cost | Remaining k |
| --- | --- | --- |
| a | 1 | 9 |
| b | 1 | 8 |
| c | 1 | 7 |

The rebuilt string is empty. The distinct count becomes 0, which is valid because deleting all characters costs only 3.

Another subtle scenario is when several character types share the same frequency:

```
aabbcc
2
```

All frequencies are 2. The algorithm may remove any one of them, depending on sorting order. If it removes `'a'`, the result becomes `"bbcc"` with 2 distinct letters.

This is still optimal because every deletion choice costs the same. The problem accepts any valid answer, so ties do not matter.
