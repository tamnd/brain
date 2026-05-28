---
title: "CF 72E - Ali goes shopping"
description: "We are given a lowercase string and must find the substring that appears the largest number of times inside it. Occurrences may overlap. Among all substrings with the same maximum frequency, we choose the longest one."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "brute-force", "strings"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "E"
codeforces_contest_name: "Unknown Language Round 2"
rating: 1800
weight: 72
solve_time_s: 454
verified: true
draft: false
---

[CF 72E - Ali goes shopping](https://codeforces.com/problemset/problem/72/E)

**Rating:** 1800  
**Tags:** *special, brute force, strings  
**Solve time:** 7m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string and must find the substring that appears the largest number of times inside it. Occurrences may overlap. Among all substrings with the same maximum frequency, we choose the longest one. If there is still a tie, we choose the lexicographically largest substring.

For example, in `abab`, the substring `a` appears twice and `ab` also appears twice. Since both have the same frequency, we prefer the longer one, so the answer becomes `ab`.

The input size changes the entire character of the problem. The string length is at most 30, which is extremely small. A cubic or even quartic algorithm is completely fine here. The total number of substrings of a string of length `n` is `n(n+1)/2`, which is only 465 when `n = 30`. That means we can directly generate every substring and count how many times it occurs without worrying about performance.

The main difficulty is not efficiency but handling the tie-breaking rules correctly. A careless implementation can easily produce the wrong answer even if the frequencies are computed correctly.

One easy mistake is forgetting that overlaps are allowed. Consider:

```
aaaa
```

The substring `aaa` appears twice: once starting at index 0 and once at index 1. An implementation using non-overlapping matching would incorrectly count only one occurrence.

Another common mistake is handling ties incorrectly. Consider:

```
abab
```

Both `a` and `ab` appear twice. The correct answer is `ab` because longer substrings are preferred when frequencies match.

The final tie-breaker is lexicographical order. Consider:

```
ababcdcd
```

The substrings `ab` and `cd` both appear twice and both have length 2. Since `cd` is lexicographically larger, the correct answer is:

```
cd
```

An implementation that updates the answer only on strictly larger frequency or length would silently fail here.

## Approaches

The most direct approach is to generate every possible substring and count how many times it appears in the original string.

A substring is determined by its starting and ending positions, so there are `O(n^2)` substrings. For each substring, we can slide over the original string and compare character-by-character to count occurrences. Each comparison costs up to `O(n)`, and we perform it at up to `O(n)` positions, leading to `O(n^4)` complexity overall.

With `n = 30`, this is still tiny. Even `30^4 = 810000` operations is trivial within a 5-second limit.

The reason brute force works here is that the constraint is intentionally small. The problem is really about implementing the comparison logic correctly rather than inventing a sophisticated string algorithm.

We can simplify the counting step further using Python's slicing. For every candidate substring `t`, we check every starting position `i` and compare:

```
s[i:i+len(t)] == t
```

This automatically handles overlapping matches because we test every position independently.

The key observation is that the number of distinct substrings is already very small. There is no need for suffix arrays, suffix automata, Z-function tricks, or rolling hashes. A clean exhaustive search is both simpler and safer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(1) | Accepted |
| Optimal | O(n^3) to O(n^4) depending on substring comparison cost | O(1) | Accepted |

In practice, Python slicing keeps the implementation compact and fast enough for the given limits.

## Algorithm Walkthrough

1. Read the input string `s`.
2. Initialize variables storing the current best substring and its frequency.
3. Generate every possible substring using two indices `l` and `r`.

The substring is `s[l:r+1]`.
4. For the current substring, count how many times it appears in `s`.

Check every starting position `i`. If `s[i:i+len(sub)] == sub`, increase the count.

Since every position is tested independently, overlapping occurrences are counted naturally.
5. Compare the current substring with the best answer found so far.

Update the answer if:

- its frequency is larger, or
- the frequency is equal but the substring is longer, or
- both frequency and length are equal but the substring is lexicographically larger.
6. After all substrings are processed, print the best substring.

### Why it works

The algorithm explicitly checks every substring of the original string, so no candidate can be missed. For each candidate, it examines every possible starting position and counts exact matches, which guarantees the frequency is correct, including overlaps.

The update conditions exactly match the rules from the statement. At every step, the stored answer is the best substring among all candidates processed so far. After the exhaustive search finishes, the stored substring must be globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)

best = ""
best_count = -1

for l in range(n):
    for r in range(l, n):
        sub = s[l:r + 1]
        m = len(sub)

        cnt = 0

        for i in range(n - m + 1):
            if s[i:i + m] == sub:
                cnt += 1

        if cnt > best_count:
            best_count = cnt
            best = sub
        elif cnt == best_count:
            if len(sub) > len(best):
                best = sub
            elif len(sub) == len(best) and sub > best:
                best = sub

print(best)
```

The outer two loops generate every substring. Using `l` and `r` makes the boundaries explicit and avoids off-by-one mistakes.

The counting loop iterates only until `n - m`, where `m` is the substring length. This guarantees the slice `s[i:i+m]` always stays inside the string.

The comparison logic is the subtle part. The order matters:

First compare frequency. Only if frequencies match do we compare lengths. Only if both frequency and length match do we compare lexicographical order.

Changing this order produces incorrect answers on tie-heavy cases such as `ababcdcd`.

Python string comparison already follows lexicographical order, so `sub > best` directly implements the final tie-breaker.

## Worked Examples

### Example 1

Input:

```
abab
```

| Substring | Frequency | Current Best |
| --- | --- | --- |
| a | 2 | a |
| ab | 2 | ab |
| aba | 1 | ab |
| abab | 1 | ab |
| b | 2 | ab |
| ba | 1 | ab |
| bab | 1 | ab |

The substring `a` first becomes the best because it appears twice. Later `ab` also appears twice, but it is longer, so it replaces `a`.

This trace demonstrates the second tie-break rule.

### Example 2

Input:

```
aaaa
```

| Substring | Frequency | Current Best |
| --- | --- | --- |
| a | 4 | a |
| aa | 3 | a |
| aaa | 2 | a |
| aaaa | 1 | a |

The substring `aa` appears three times because overlaps are allowed:

- positions 0-1
- positions 1-2
- positions 2-3

The final answer remains `a` because frequency dominates length.

This example confirms that overlapping occurrences are counted correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^4) | There are O(n^2) substrings, and each may require O(n^2) total comparison work |
| Space | O(1) | Only a few variables are stored besides the input string |

Even the worst-case input length is only 30, so fewer than one million primitive operations are needed. This easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    n = len(s)

    best = ""
    best_count = -1

    for l in range(n):
        for r in range(l, n):
            sub = s[l:r + 1]
            m = len(sub)

            cnt = 0

            for i in range(n - m + 1):
                if s[i:i + m] == sub:
                    cnt += 1

            if cnt > best_count:
                best_count = cnt
                best = sub
            elif cnt == best_count:
                if len(sub) > len(best):
                    best = sub
                elif len(sub) == len(best) and sub > best:
                    best = sub

    print(best)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("abab\n") == "ab", "sample 1"

# minimum size
assert run("a\n") == "a", "single character"

# overlapping occurrences
assert run("aaaa\n") == "a", "overlapping matches"

# lexicographical tie-break
assert run("ababcdcd\n") == "cd", "same count and length"

# all distinct
assert run("abcd\n") == "d", "all substrings appear once"

# boundary length case
assert run("abcabcabc\n") == "abc", "repeated pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum-size input |
| `aaaa` | `a` | Overlapping occurrences |
| `ababcdcd` | `cd` | Lexicographical tie-break |
| `abcd` | `d` | All substrings appear once |
| `abcabcabc` | `abc` | Longer repeated substring wins |

## Edge Cases

Consider the input:

```
aaaa
```

The substring `aaa` appears twice because overlaps count:

- `s[0:3]`
- `s[1:4]`

The algorithm checks every starting position independently, so both matches are counted. The frequencies become:

- `a` → 4
- `aa` → 3
- `aaa` → 2
- `aaaa` → 1

The final answer is `a`.

Now consider:

```
abab
```

Both `a` and `ab` appear twice. The algorithm first stores `a` as the best substring. Later, when processing `ab`, it sees that frequencies are equal but `ab` is longer, so it updates the answer.

The final output becomes:

```
ab
```

Finally, consider:

```
ababcdcd
```

The substrings `ab` and `cd` both appear twice and both have length 2.

When `ab` is processed, it becomes the current best. Later, `cd` matches both frequency and length, but `cd > ab` lexicographically, so the algorithm replaces the answer.

The final output is:

```
cd
```
