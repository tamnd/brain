---
title: "CF 1674C - Infinite Replacement"
description: "The problem gives you two strings for each test case: a string s composed entirely of the letter 'a' and another string t composed of arbitrary lowercase letters. You are allowed to repeatedly replace any single 'a' in s with the string t."
date: "2026-06-10T01:12:59+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1674
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 786 (Div. 3)"
rating: 1000
weight: 1674
solve_time_s: 89
verified: true
draft: false
---

[CF 1674C - Infinite Replacement](https://codeforces.com/problemset/problem/1674/C)

**Rating:** 1000  
**Tags:** combinatorics, implementation, strings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives you two strings for each test case: a string `s` composed entirely of the letter 'a' and another string `t` composed of arbitrary lowercase letters. You are allowed to repeatedly replace any single 'a' in `s` with the string `t`. After any number of such replacements, you are asked to count how many distinct strings can be obtained. If the process can generate infinitely many distinct strings, you should output -1.

The constraints are modest. Each string has length at most 50, and there can be up to 10,000 test cases. This suggests that we need an algorithm that is linear in the size of each string, because a solution that tries to generate all possible strings explicitly would explode combinatorially, especially when `t` contains letters other than 'a'.

There are some edge cases that require careful reasoning. If `t` consists only of 'a', then every replacement is effectively a no-op. Replacing an 'a' with `t` changes nothing, so no new strings are generated beyond the original `s`. Conversely, if `t` contains at least one letter other than 'a', then each replacement introduces a non-'a' letter. Since replacements can continue indefinitely wherever 'a's remain, the number of possible strings becomes unbounded - there is no upper limit on string length or variety. Finally, if `s` contains only one 'a' and `t` contains letters other than 'a', you can produce only two strings: the original `s` and the string `t` after replacing the single 'a'.

A naive implementation that attempts to simulate all replacements will fail on modest inputs because the number of possible strings can grow exponentially or infinitely. Recognizing the structure of `t` is therefore the key to a simple solution.

## Approaches

A brute-force approach would try to enumerate all possible sequences of replacements. For each 'a' in `s`, you could replace it with `t` or leave it as is, recursively generating new strings until no 'a's remain. While this is conceptually correct, the worst-case number of strings is exponential in the length of `s`. Specifically, for `n = 50` and `t` containing letters other than 'a', you can quickly exceed `2^50` possible strings, which is far beyond feasible computation.

The optimal approach relies on a simple observation: the number of distinct strings is determined entirely by whether `t` contains only 'a' or any other letter. If `t` contains a letter different from 'a', the replacement can produce infinitely many distinct strings, because each new 'a' that appears can be replaced again, growing the string indefinitely. Otherwise, if `t` is composed only of 'a's, no replacement ever changes the string, so only the original `s` exists as a distinct string. For the case where `s` has length 1 and `t` contains non-'a' letters, only two distinct strings exist: the original 'a' and the replacement `t`.

This reduces the problem to a simple check: scan `t` for non-'a' letters. If any exist, the answer is -1 (infinite) unless `s` has length 1, in which case there are exactly two possibilities. If all letters of `t` are 'a', the answer is 1, because replacements do not produce new strings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n * 2^n) | Too slow |
| Optimal | O( | t | ) per test case |

## Algorithm Walkthrough

1. Read the number of test cases `q`. This controls the main loop over all test cases.
2. For each test case, read strings `s` and `t`. The string `s` will only contain 'a', and `t` may contain any lowercase letters.
3. Check if `t` consists entirely of 'a'. This can be done by comparing the set of characters in `t` to `{'a'}`.
4. If `t` contains only 'a', print 1. No replacements change the string, so only the original string exists.
5. Otherwise, if `t` contains any letter other than 'a', check the length of `s`.
6. If `s` has length 1, print 2. The only distinct strings are the original 'a' and the replacement `t`.
7. If `s` has length greater than 1, print -1. The replacement process can generate infinitely many strings because each 'a' can recursively produce `t` containing non-'a' letters.

Why it works: the invariant is that the replacement process only introduces new letters if `t` contains letters other than 'a'. This immediately causes either a finite small set of possible strings or an infinite number, depending solely on the content of `t` and the length of `s`. There is no need to simulate string construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())
for _ in range(q):
    s = input().strip()
    t = input().strip()
    
    if set(t) == {'a'}:
        print(1)
    elif len(s) == 1:
        print(2)
    else:
        print(-1)
```

The solution first reads the number of test cases. For each case, it reads `s` and `t`. The `set(t) == {'a'}` check determines if all characters in `t` are 'a'. If so, replacements do not change the string, so we print 1. If `t` contains other letters and `s` has only one 'a', the string can be either the original or the replacement, so we print 2. Otherwise, replacements can continue indefinitely, and we print -1. Using `strip()` ensures no trailing newlines interfere with string comparison.

## Worked Examples

Sample 1:

| Step | s | t | Set(t) | len(s) | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | aaaa | a | {'a'} | 4 | 1 |
| 2 | aa | abc | {'a','b','c'} | 2 | -1 |
| 3 | a | b | {'b'} | 1 | 2 |

The table confirms that the logic correctly distinguishes between purely 'a' replacements, single-letter s, and multi-letter s with non-'a' replacements.

Sample 2:

Input:

```
2
a
a
aa
b
```

| Step | s | t | Set(t) | len(s) | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | a | a | {'a'} | 1 | 1 |
| 2 | aa | b | {'b'} | 2 | -1 |

This confirms that the algorithm handles minimum-size strings and multi-'a' cases correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | t |
| Space | O(1) | Only a few variables and the set of characters from t are stored per test case. |

The solution is comfortably within time and memory limits. At most 10^4 * 50 = 5×10^5 character inspections occur, trivial for modern processors.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    q = int(input())
    for _ in range(q):
        s = input().strip()
        t = input().strip()
        if set(t) == {'a'}:
            print(1)
        elif len(s) == 1:
            print(2)
        else:
            print(-1)
    return output.getvalue().strip()

# provided samples
assert run("3\naaaa\na\naa\nabc\na\nb\n") == "1\n-1\n2", "sample 1"

# custom cases
assert run("2\na\na\naa\nb\n") == "1\n-1", "minimum and infinite"
assert run("1\na\nb\n") == "2", "single a, non-a t"
assert run("1\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\na\n") == "1", "max length s, t all a"
assert run("1\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nb\n") == "-1", "max length s, t non-a"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\na\na\naa\nb | 1\n-1 | minimum-size strings and infinite generation |
| 1\na\nb | 2 | single 'a' with non-'a' replacement |
| 1\na...a\na | 1 | maximum length s, t all 'a' |
| 1\na...a\nb | -1 | maximum length s, t contains non-'a' |

## Edge Cases

If `s = "a"` and `t = "b"`, the algorithm prints 2. Step trace: `set(t) != {'a'}`, `len(s) == 1`,
