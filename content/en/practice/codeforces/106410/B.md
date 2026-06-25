---
title: "CF 106410B - Yash is Cross-Eyed"
description: "We are given several strings. For each string, we may repeatedly swap two neighboring characters. The question is whether these swaps can transform the string into two identical consecutive parts."
date: "2026-06-25T09:54:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106410
codeforces_index: "B"
codeforces_contest_name: "HPI 2026 Novice"
rating: 0
weight: 106410
solve_time_s: 34
verified: true
draft: false
---

[CF 106410B - Yash is Cross-Eyed](https://codeforces.com/problemset/problem/106410/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several strings. For each string, we may repeatedly swap two neighboring characters. The question is whether these swaps can transform the string into two identical consecutive parts. In other words, after rearranging the characters in any order, can the final string look like `t + t` for some string `t`?

The input contains multiple test cases. Each test case is one lowercase string, and the output for that string is `YES` when such a rearrangement exists, otherwise `NO`.

The key constraint is the total length of all strings, which is at most `2 * 10^5`. This means we can afford a solution that scans every character a constant number of times. Any approach that tries many possible rearrangements or simulates swaps is impossible, because even a single string of length `200000` has an enormous number of possible permutations.

The non-obvious part is understanding what adjacent swaps allow. Adjacent swaps can move characters around freely, but they cannot create or remove any character. The only thing that matters is the count of each letter in the original string.

A naive implementation might only check whether the length is even. For example:

```
1
aabbc
```

The length is 5, so it immediately fails, but the more interesting mistake appears when the length is even:

```
1
aabbcdef
```

A careless solution might only split the string in half and compare the two halves after sorting. However, the available characters are `a, a, b, b, c, d, e, f`. The letters `c`, `d`, `e`, and `f` appear once, so they cannot belong to the same position in both halves. The correct output is:

```
NO
```

Another edge case is a single character:

```
1
a
```

There is no way to split a length one string into two equal parts, so the answer is:

```
NO
```

The opposite edge case is a string where every character already has a matching copy:

```
1
abba
```

We can rearrange it into `ba + ba`, so the correct output is:

```
YES
```

## Approaches

The brute-force way to think about the problem is to try all possible rearrangements of the string and check whether any of them have the form `t + t`. This is correct because adjacent swaps can produce any permutation of the characters. However, a string of length `n` can have up to `n!` different permutations, which becomes impossible even for very small values of `n`.

The important observation is that we do not actually need to know the final arrangement. If the final string is `t + t`, then every character appears twice in the first half and twice in the second half in exactly the same places. That means every character in the whole string must appear an even number of times.

The reverse direction is also true. If every character appears an even number of times, we can put half of every character into the first half and the other half into the second half. Since adjacent swaps allow arbitrary rearrangement, this construction is always reachable.

The problem is reduced from searching through permutations to counting frequencies. We only need to verify whether every frequency is divisible by two.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many times each lowercase letter appears in the string. The final arrangement can only use the existing characters, so these counts contain all necessary information.
2. Check every character count. If any character appears an odd number of times, the answer is `NO`. An odd amount cannot be divided equally between the two copies of `t`.
3. If all character counts are even, output `YES`. Each character can be split into two equal groups, one for each half of the final string.

Why it works: The invariant is that adjacent swaps preserve the frequency of every character. A string of the form `t + t` requires every character to be present an even number of times because its occurrences are divided equally between two identical halves. If all counts are even, we can construct the two halves by taking exactly half of every character's occurrences for each side. Since any permutation is achievable using adjacent swaps, the required form can always be reached.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()
        freq = [0] * 26

        for ch in s:
            freq[ord(ch) - ord('a')] += 1

        ok = True
        for count in freq:
            if count % 2:
                ok = False
                break

        ans.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution reads the number of test cases and processes each string independently. The frequency array has one slot for each lowercase letter, so updating it takes constant time per character.

The final loop checks divisibility by two. There is no need to build the rearranged string because the existence of such a rearrangement depends only on character counts.

The implementation avoids any assumptions about the original order of characters. A common mistake is to compare the first half and second half of the input string, but the allowed swaps mean the input order has no special meaning.

## Worked Examples

### Sample 1

Input:

```
1
abba
```

| Step | String | Character counts | Result |
| --- | --- | --- | --- |
| Initial | abba | a:2, b:2 | Continue |
| Check a | abba | 2 is even | Continue |
| Check b | abba | 2 is even | YES |

The string already has balanced frequencies. The algorithm does not need to perform swaps because it only checks whether a valid arrangement exists.

### Sample 2

Input:

```
2
a
abcdeadbceff
```

First test case:

| Step | String | Character counts | Result |
| --- | --- | --- | --- |
| Initial | a | a:1 | Odd count found |
| Final | a | Cannot split equally | NO |

Second test case:

| Step | String | Character counts | Result |
| --- | --- | --- | --- |
| Initial | abcdeadbceff | a:2,b:2,c:2,d:2,e:2,f:2 | Continue |
| Check all letters | abcdeadbceff | Every count is even | YES |

The second example demonstrates that the original order is irrelevant. The characters are not arranged as two equal halves initially, but swaps can reorder them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is counted once and every alphabet entry is checked once. |
| Space | O(1) | The frequency array always contains only 26 integers. |

The total input size is limited to `2 * 10^5`, so a linear scan easily fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue()

# provided samples
assert run("""1
abba
""") == "YES", "sample 1"

assert run("""2
a
abcdeadbceff
""") == "NO\nYES", "sample 2"

# minimum size
assert run("""1
a
""") == "NO", "single character cannot be duplicated"

# all equal values
assert run("""1
aaaaaa
""") == "YES", "all characters split evenly"

# odd frequency hidden among many pairs
assert run("""1
aabbcccd
""") == "NO", "odd counts must fail"

# larger boundary case
assert run("""1
""" + "ab" * 100000 + "\n") == "YES", "large valid input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `NO` | Minimum length handling |
| `aaaaaa` | `YES` | All characters appearing evenly |
| `aabbcccd` | `NO` | Detecting a single odd frequency |
| `ab` repeated 100000 times | `YES` | Linear performance on maximum size |

## Edge Cases

For the single-character case:

```
1
a
```

The frequency of `a` is one. The algorithm detects that one half cannot receive the same characters as the other half, so it outputs `NO`.

For an even-length string with an odd-frequency character:

```
1
aabbcdef
```

The counts of `c`, `d`, `e`, and `f` are all one. The algorithm rejects the string because those characters cannot be split between two identical halves.

For a string that already satisfies the condition:

```
1
abba
```

The counts of `a` and `b` are both two. The algorithm accepts it, even though it never constructs the final arrangement. A possible final arrangement is `ba + ba`.

For a large valid input:

```
1
abababab...
```

where `ab` is repeated many times, the algorithm only performs one pass to count characters and one constant-sized check. It does not depend on the number of possible swaps or arrangements.
