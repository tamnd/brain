---
title: "CF 102397I - Dr.Hjjawi and the MCQ"
description: "There are n multiple-choice questions, and Ayoub answered each question with one letter from a through e. The crucial extra information is that the correct answer is the same letter for every question. We do not know which of the five letters it is."
date: "2026-08-10T18:13:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "I"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 322
verified: true
draft: false
---

[CF 102397I - Dr.Hjjawi and the MCQ](https://codeforces.com/problemset/problem/102397/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` multiple-choice questions, and Ayoub answered each question with one letter from `a` through `e`. The crucial extra information is that the correct answer is the same letter for every question. We do not know which of the five letters it is.

For any fixed choice of the correct letter, Ayoub gets a question right exactly when his answer at that position equals the chosen letter. Thus, if the correct letter were `c`, his score would simply be the number of `c` characters in his answer string.

We need to consider all five possible correct letters. The minimum possible score is the smallest frequency among `a`, `b`, `c`, `d`, and `e`, while the maximum possible score is the largest frequency.

The number of questions satisfies `1 <= n <= 1000`. This is a very small input size, so even checking all five possible correct letters against every question requires only `5 * 1000 = 5000` character comparisons. A linear scan is more than fast enough, and even the straightforward five-pass solution is comfortably within the time limit. There is no need for sorting, dynamic programming, or any more complicated data structure.

There are a few cases where an implementation can silently go wrong. With the input `3` and `aaa`, the answer is `0 3`. If the correct letter is `a`, all three answers are correct, but if it is any other letter, none are correct. A careless implementation that assumes the correct letter must occur in the string could incorrectly produce a minimum of `1`.

Another edge case is when every possible letter appears equally often. For example, with `5` questions and the string `abcde`, every possible correct letter gives exactly one correct answer, so the output is `1 1`. An implementation that initializes the minimum or maximum from the wrong frequency can fail on this case.

The smallest valid input is also useful. For `n = 1` and `s = a`, the possible scores are `1, 0, 0, 0, 0`, so the answer is `0 1`. The four letters that do not occur in the string must still be considered.

## Approaches

A direct brute-force solution can try each of the five possible correct letters. For a chosen letter, it scans the entire answer string and counts how many positions contain that letter. After doing this for `a`, `b`, `c`, `d`, and `e`, it takes the minimum and maximum of the five scores. This is correct because the statement guarantees that the actual exam has exactly one common correct letter, and there are only five possible choices for it.

The worst case performs `5n` character comparisons. With `n <= 1000`, that is at most `5000` comparisons, so this brute-force method does not actually become too slow under the given constraints. Its asymptotic complexity is still `O(n)`, because the factor of five is constant.

We can make the same reasoning cleaner by observing that the score for a candidate letter is exactly its frequency in the string. Instead of scanning the entire string once for every candidate, we can scan the string once and maintain five counters. Every character increments exactly one counter. Once the frequencies are known, the minimum and maximum frequencies immediately give the required answer.

The brute-force works because there are only five possible correct answers, but it repeatedly examines the same characters. The observation that a candidate's score is simply its frequency lets us collect all five scores during one scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(5n) = O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

The optimal version is preferable because its relationship with the problem is direct: count each letter once, then inspect the five counts.

## Algorithm Walkthrough

1. Create five counters representing the frequencies of `a`, `b`, `c`, `d`, and `e`. Every possible correct answer needs its own count because each count represents the score Ayoub would receive if that letter were the universal correct answer.
2. Scan every character in the answer string and increment the counter corresponding to that character. After processing any prefix of the string, each counter equals the number of times its letter has appeared in that prefix.
3. After the entire string has been processed, find the smallest and largest among the five counters. These values are exactly the minimum and maximum scores because choosing a particular letter as the correct answer gives Ayoub a correct answer precisely at the positions containing that letter.
4. Print the minimum frequency followed by the maximum frequency.

### Why it works

Let `count[x]` be the number of questions Ayoub answered with letter `x`. If `x` is the actual common correct answer, Ayoub is correct on exactly those questions where his answer is `x`, so his score is `count[x]`. Since the common correct answer can be any of the five letters, the set of all possible scores is exactly the five frequencies. Taking their minimum gives the smallest possible score, and taking their maximum gives the largest possible score. The counting pass computes every one of these frequencies exactly, so the final pair is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

count = [0] * 5

for ch in s:
    count[ord(ch) - ord('a')] += 1

print(min(count), max(count))
```

The first line reads `n`, although the algorithm does not need it after reading the string. The string itself contains all information needed to calculate the five possible scores.

The `count` array has five positions. Since the input contains only letters from `a` through `e`, the expression `ord(ch) - ord('a')` maps these characters to indices `0` through `4`. Thus `a` updates `count[0]`, `b` updates `count[1]`, and so on.

The loop processes every character exactly once. There is no need to compare each character against all five letters because its own character determines exactly which counter must increase.

The zero initialization is significant because a letter may never appear. For example, with `aaa`, the counters become `[3, 0, 0, 0, 0]`. Those zero values represent valid possibilities where the correct letter is absent from Ayoub's answers.

Python integers do not have an overflow issue here, and every counter is at most `1000`. The input string is stripped so that the newline from standard input is not treated as an answer character.

## Worked Examples

### Sample 1

The input is:

```
10
aaaaaabcde
```

The string contains six `a` characters and one occurrence of each of `b`, `c`, `d`, and `e`. The scan evolves as follows.

| Processed character | a | b | c | d | e |
| --- | --- | --- | --- | --- | --- |
| `a` | 1 | 0 | 0 | 0 | 0 |
| `a` | 2 | 0 | 0 | 0 | 0 |
| `a` | 3 | 0 | 0 | 0 | 0 |
| `a` | 4 | 0 | 0 | 0 | 0 |
| `a` | 5 | 0 | 0 | 0 | 0 |
| `a` | 6 | 0 | 0 | 0 | 0 |
| `b` | 6 | 1 | 0 | 0 | 0 |
| `c` | 6 | 1 | 1 | 0 | 0 |
| `d` | 6 | 1 | 1 | 1 | 0 |
| `e` | 6 | 1 | 1 | 1 | 1 |

The five possible scores are `6, 1, 1, 1, 1`. Hence the minimum is `1` and the maximum is `6`, producing `1 6`.

This trace demonstrates the central invariant: each counter always stores the number of occurrences of its corresponding answer.

### Sample 2

The input is:

```
3
aaa
```

The scan gives the following state.

| Processed character | a | b | c | d | e |
| --- | --- | --- | --- | --- | --- |
| `a` | 1 | 0 | 0 | 0 | 0 |
| `a` | 2 | 0 | 0 | 0 | 0 |
| `a` | 3 | 0 | 0 | 0 | 0 |

The possible scores are `3, 0, 0, 0, 0`. The minimum is `0` and the maximum is `3`, so the output is `0 3`.

This example exercises the case where four possible correct letters never appear in the answer string. Their zero frequencies must not be discarded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character in the answer string is processed once. |
| Space | O(1) | Only five frequency counters are stored, regardless of `n`. |

With `n <= 1000`, the algorithm performs only a thousand character updates and a constant amount of additional work. It is far below the available time limit and uses negligible memory compared with the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    count = [0] * 5

    for ch in s:
        count[ord(ch) - ord('a')] += 1

    print(min(count), max(count))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run("10\naaaaaabcde\n") == "1 6", "sample 1"
assert run("3\naaa\n") == "0 3", "sample 2"

# Minimum-size input
assert run("1\na\n") == "0 1", "single question"

# All five letters occur equally often
assert run("5\nabcde\n") == "1 1", "all letters equally frequent"

# All answers are the same
assert run("7\nbbbbbbb\n") == "0 7", "all equal values"

# Maximum-size input
assert run("1000\n" + "a" * 1000 + "\n") == "0 1000", "maximum n"

# Boundary distribution that catches incorrect min/max initialization
assert run("5\naaaab\n") == "0 4", "zero-frequency letters and maximum frequency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a` | `0 1` | Minimum input size and absent letters |
| `5 / abcde` | `1 1` | Equal frequencies and equal minimum and maximum |
| `7 / bbbbbbb` | `0 7` | All answers identical |
| `1000 / a...a` | `0 1000` | Maximum input size and large frequency |
| `5 / aaaab` | `0 4` | Zero-frequency candidates and correct extrema |

## Edge Cases

For the single-question case, consider `n = 1` and `s = a`. The counters become `[1, 0, 0, 0, 0]`. If `a` is the correct answer, Ayoub gets one point. If any other letter is correct, he gets zero points. The algorithm prints `0 1`, correctly accounting for all five possible correct answers.

For an answer string containing only one distinct letter, consider `n = 3` and `s = aaa`. The counters become `[3, 0, 0, 0, 0]`. The maximum score is `3`, obtained when `a` is correct, while the minimum is `0`, obtained for any of the other four possible correct letters. The result is `0 3`.

For the case where every letter appears exactly once, consider `n = 5` and `s = abcde`. The counters are `[1, 1, 1, 1, 1]`. Regardless of which letter was the universal correct answer, Ayoub gets exactly one question right. Both extrema are consequently `1`, giving `1 1`.

For the maximum input size, consider `n = 1000` and a string containing one thousand `a` characters. The counters are `[1000, 0, 0, 0, 0]`, so the result is `0 1000`. The loop still performs only one operation per character, demonstrating that the solution scales directly with the input size.
