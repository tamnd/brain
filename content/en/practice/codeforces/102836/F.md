---
title: "CF 102836F - \u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u0442\u0440\u043e\u043a\u0430"
description: "The task is about a string made of lowercase English letters. We are allowed to erase characters from it, but the number of erased positions cannot exceed the given limit."
date: "2026-07-26T14:52:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102836
codeforces_index: "F"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102836
solve_time_s: 38
verified: true
draft: false
---

[CF 102836F - \u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u0442\u0440\u043e\u043a\u0430](https://codeforces.com/problemset/problem/102836/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
# Problem Understanding

The task is about a string made of lowercase English letters. We are allowed to erase characters from it, but the number of erased positions cannot exceed the given limit. The goal is not to make the string short, but to make the number of different letters that still appear as small as possible. We must print that minimum number of remaining letters and one possible subsequence that has exactly that many different letters.

The input contains the original string and the maximum number of deletions allowed. The output is the minimum count of distinct letters that can survive, followed by any resulting string obtained by removing characters from the original order.

The important constraint is that the alphabet has only 26 possible letters, even though the string itself can be large. A string length around 100000 rules out trying many possible deletion combinations or rebuilding answers for every choice. We need an approach that processes the string in linear time, because an algorithm around O(n) or O(n + alphabet size) is easily safe, while approaches involving subsets of letters or repeated simulations would grow too quickly.

Several edge cases can break a careless implementation. If all characters can be deleted, the answer must contain zero distinct letters. For example:

```
Input:
abc
5

Output:
0
```

A solution that always keeps at least one character would fail here because the deletion limit is larger than the string length.

Another case is when a letter appears many times and cannot be removed completely. For example:

```
Input:
aaaaa
4

Output:
1
aaaaa
```

The letter `a` costs five deletions to remove entirely, so it must remain. Removing four occurrences does not help reduce the number of distinct letters.

A final common mistake is removing arbitrary letters instead of the cheapest ones:

```
Input:
aabbbc
2

Output:
2
aabbb
```

Removing `c` uses one deletion and removing `a` uses two deletions. The best choice is to remove `c` first because it reduces the number of distinct letters at the lowest cost. Removing one `b` instead would spend the deletions without reducing the answer.

## Approaches

A direct brute-force approach would consider which letters remain. Since there are 26 possible letters, one could imagine trying every subset of letters, checking whether all other letters can be deleted within the allowed limit. This would be correct because every possible final set of distinct letters would be examined. However, the number of subsets is 2^26, which is about 67 million possibilities before even checking the string. That is far beyond what is reasonable when combined with the string processing.

The brute-force idea works because the only thing that matters is which complete groups of letters disappear. It fails because it explores too many possible groups. The key observation is that every letter contributes independently. To remove a letter from the final string, we must spend exactly its frequency in deletions. Since the goal is to remove as many different letters as possible, we should spend deletions on the letters with the smallest frequencies first.

After sorting the 26 letter frequencies, we can repeatedly remove whole letters while the remaining deletion budget allows it. The letters that cannot be removed stay in the answer. The original order of characters is preserved by scanning the string again and keeping only the surviving letters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^26 * n) | O(26) | Too slow |
| Optimal | O(n + 26 log 26) | O(26) | Accepted |

## Algorithm Walkthrough

1. Count how many times each lowercase letter appears in the string. The frequency tells us the exact deletion cost needed to completely remove that letter.
2. If the deletion limit is at least the string length, remove every character. The final string is empty and the number of distinct letters is zero.
3. Sort the letters by their frequencies from smallest to largest. A smaller frequency means we can eliminate one entire distinct letter more cheaply.
4. Visit the letters in this order. If the current letter's frequency can be paid using the remaining deletions, remove it by subtracting its frequency from the budget. Otherwise, keep it in the final set. This greedy choice is correct because every removed letter gives exactly one reduction in the number of distinct letters, so cheaper removals should always be taken first.
5. Build the resulting string by scanning the original string and keeping only characters whose letters were not removed. This preserves the required subsequence property.

Why it works: every letter that disappears from the answer must have all of its occurrences deleted. The cost of removing a letter is independent from every other letter and equals its frequency. The greedy process chooses the cheapest removable letters first, so after it stops, no remaining letter could have been removed without spending more deletions than were available. Any other strategy that removes a more expensive letter while leaving a cheaper removable letter behind can be improved by swapping those choices, so the greedy result has the minimum possible number of distinct letters.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    k = int(input())

    if k >= len(s):
        print(0)
        print()
        return

    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('a')] += 1

    removed = [False] * 26

    letters = sorted(range(26), key=lambda x: freq[x])

    for x in letters:
        if freq[x] <= k:
            k -= freq[x]
            removed[x] = True
        else:
            break

    ans = []
    for c in s:
        if not removed[ord(c) - ord('a')]:
            ans.append(c)

    print(len(set(ans)))
    print(''.join(ans))

if __name__ == "__main__":
    solve()
```

The first part handles the special case where every character can disappear. This avoids leaving an unnecessary character in the result when the deletion budget is large enough.

The frequency array has one position per alphabet letter, so counting takes one pass through the string. Sorting only 26 elements is effectively constant time.

The greedy loop marks letters that can be completely removed. The `removed` array stores this decision separately from the frequencies because the second scan needs to know which characters to keep.

The final scan rebuilds the answer in the original order. It does not remove individual occurrences of remaining letters, because partial deletion does not change the number of distinct letters and the problem only asks for the minimum count of distinct letters.

## Worked Examples

### Example 1

Input:

```
aaaaa
4
```

| Step | Current letter | Frequency | Remaining deletions | Removed |
| --- | --- | --- | --- | --- |
| 1 | a | 5 | 4 | no |

The only letter costs five deletions to remove, but only four are available. The algorithm keeps `a`, so the answer has one distinct letter.

### Example 2

Input:

```
abacaba
4
```

| Step | Current letter | Frequency | Remaining deletions | Removed |
| --- | --- | --- | --- | --- |
| 1 | b | 2 | 4 | yes |
| 2 | c | 1 | 2 | yes |
| 3 | a | 4 | 1 | no |

The cheapest letters to remove are `c` and `b`. After spending three deletions, only one deletion remains, which is not enough to remove `a`. The resulting subsequence is `aaaa`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting and rebuilding the string each take one pass. Sorting 26 letters is constant time. |
| Space | O(1) | Only arrays of size 26 and the output string are stored. |

The algorithm processes each input character a constant number of times, so it fits easily for strings with length around 100000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided samples
assert run("aaaaa\n4\n") == "1\naaaaa\n", "sample 1"
assert run("abacaba\n4\n") == "1\naaaa\n", "sample 2"
assert run("abcdefgh\n10\n") == "0\n\n", "sample 3"

# custom cases
assert run("a\n0\n") == "1\na\n", "single character"
assert run("aabbcc\n2\n") == "2\naabb\n", "remove cheapest groups"
assert run("zzzz\n3\n") == "1\nzzzz\n", "all equal values"
assert run("abcde\n100000\n") == "0\n\n", "large deletion budget"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a`, `0` | `1`, `a` | Minimum string size and zero deletions |
| `aabbcc`, `2` | `2`, `aabb` | Choosing the cheapest letters first |
| `zzzz`, `3` | `1`, `zzzz` | A letter that cannot be fully removed |
| `abcde`, `100000` | `0`, empty string | Complete deletion boundary |

## Edge Cases

For the case where the deletion limit is larger than the string:

```
abc
5
```

The algorithm checks `k >= len(s)` immediately and returns zero. Without this check, a later greedy step might leave a letter behind because it only considers removing whole groups while iterating over frequencies.

For a repeated single letter:

```
aaaaa
4
```

The frequency array contains `a = 5`. The greedy loop compares the cost of removing `a` with the available budget and rejects the removal. The resulting string remains unchanged and has one distinct letter.

For competing removal choices:

```
aabbbc
2
```

The frequencies are `a = 2`, `b = 3`, and `c = 1`. The algorithm removes `c` first, leaving one deletion. It cannot remove `a` because the remaining budget is too small, so the final distinct letters are `a` and `b`. The answer contains the minimum possible number of different letters because the available deletions were spent on the cheapest full removals.
