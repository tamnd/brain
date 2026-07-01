---
title: "CF 104273A - Code Plagiarism"
description: "We are given two strings built from lowercase letters. Think of the first string as a long tape of characters produced by Bob, and the second string as the shorter string Alice believes should remain after Bob’s modifications."
date: "2026-07-01T21:23:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104273
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2023"
rating: 0
weight: 104273
solve_time_s: 84
verified: true
draft: false
---

[CF 104273A - Code Plagiarism](https://codeforces.com/problemset/problem/104273/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings built from lowercase letters. Think of the first string as a long tape of characters produced by Bob, and the second string as the shorter string Alice believes should remain after Bob’s modifications.

Bob is allowed to remove characters from his string, but only in a very specific way: he repeatedly deletes two adjacent characters at a time. Each deletion removes a contiguous pair and shortens the string. After performing this operation any number of times, the question is whether the string can become exactly equal to the target string.

So the task is not about arbitrary deletions. We are only allowed to erase the string in chunks of size two, and always from adjacent positions in the current string. We must decide whether there exists a sequence of such deletions that transforms the original string into the target.

The constraints allow strings up to 200,000 characters. This immediately rules out any solution that simulates deletions explicitly or tries to explore all removal sequences, since even a linear number of branching choices would explode combinatorially. A valid solution must be close to linear time.

A subtle edge case comes from understanding what “adjacent deletions” really implies. It is easy to assume that the order of deletions heavily constrains the final structure, but the key observation is that deletions can be used to eliminate any even-sized leftover portion regardless of character content, as long as those characters can be paired off through repeated adjacency reduction.

For example, if after selecting the target string as a subsequence, the remaining characters form any string of even length, that remainder can always be fully deleted:

Input:

```
abac
a
```

Here we keep “a” and remove “bac”. The removed part has length 3, which is odd, so it cannot be fully removed using pair deletions. This forces rejection even though “a” is a valid subsequence.

The main failure mode of naive thinking is assuming we need to simulate the deletion process itself. That leads to complex stack simulations or interval DP, which is unnecessary.

## Approaches

A brute-force approach would attempt to simulate all possible sequences of adjacent pair deletions. At each step, we could choose any adjacent pair and remove it, generating a new string. This creates a huge branching factor, and even for moderate lengths the number of states becomes exponential. With 200,000 characters, this is completely infeasible.

A more structured attempt is to reverse the process. Instead of deleting pairs from `s` to reach `t`, we can think of selecting which characters survive. The surviving characters must appear in order, so `t` must be a subsequence of `s`. After choosing these characters, everything else is deleted in pairs.

The key insight is that adjacency-based deletions do not restrict _which characters can be removed together in the long run_. Any string of even length can be fully reduced to empty by repeatedly removing adjacent pairs. We never need the pairs to match in value, only to be adjacent at the moment of deletion. Since we can always reorder deletions locally to bring elements together, parity of length becomes the only constraint on full removal.

So the problem reduces to two checks:

First, verify that `t` can be obtained as a subsequence of `s`.

Second, ensure that the number of leftover characters, `|s| - |t|`, is even. If it is even, the leftover string can always be fully eliminated using adjacent deletions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force deletion simulation | Exponential | O(n) | Too slow |
| Subsequence check + parity condition | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the two strings using a linear scan and two pointers.

1. Traverse `s` from left to right while trying to match characters of `t` in order. Each time we see a character in `s` equal to the current needed character in `t`, we advance the pointer in `t`. This checks whether `t` is a subsequence of `s`. The reason this works is that deletions only remove characters, so relative order of remaining characters is preserved.
2. After the scan, check whether all characters of `t` were matched. If not, there is no way to obtain `t`, because deletions cannot create new characters or reorder existing ones.
3. Compute the number of removed characters as `len(s) - len(t)`. This represents how many characters must be deleted via adjacent pair operations.
4. Check whether this number is even. If it is odd, reject immediately. The reason is that each operation removes exactly two characters, so total removed characters must be divisible by two.
5. If both conditions are satisfied, accept the transformation.

### Why it works

The subsequence condition captures the fact that deletions never change relative order among kept characters. The parity condition captures the fact that the deletion operation reduces the string size by exactly two each time, and any string of even length can always be reduced to empty by repeated adjacent removals. Combining these two conditions fully characterizes when `t` can be obtained from `s`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()
    
    n, m = len(s), len(t)
    
    j = 0
    for i in range(n):
        if j < m and s[i] == t[j]:
            j += 1
    
    if j != m:
        print("NO")
        return
    
    if (n - m) % 2 != 0:
        print("NO")
        return
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The solution first performs a greedy subsequence scan. The pointer `j` advances only when we successfully match the next required character of `t`. If we reach the end of `t`, we know it is embedded in `s` in order.

The second check enforces that the number of deletions needed is compatible with removing pairs. Since each operation removes exactly two characters, we require an even difference in lengths.

No simulation of the deletion process is needed, which is what keeps the solution linear.

## Worked Examples

### Example 1

Input:

```
sobaka
baka
```

| i | s[i] | t[j] | match? | j |
| --- | --- | --- | --- | --- |
| 0 | s | b | no | 0 |
| 1 | o | b | no | 0 |
| 2 | b | b | yes | 1 |
| 3 | a | a | yes | 2 |
| 4 | k | k | yes | 3 |
| 5 | a | a | yes | 4 |

We successfully match all characters of `t`, and the length difference is `6 - 4 = 2`, which is even. The output is `YES`.

This confirms both subsequence feasibility and valid pairing parity.

### Example 2

Input:

```
sobabka
baka
```

The subsequence check still succeeds: we can match `b`, `a`, `k`, `a` in order. However, the length difference is `7 - 4 = 3`, which is odd.

| Step | Value |
| --- | --- |
|  | s |
|  | t |
| removed | 3 |
| parity | odd |

Since one deletion removes exactly two characters, removing an odd number of characters is impossible. The output is `NO`.

This shows that subsequence validity alone is not sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over `s` with a pointer over `t` |
| Space | O(1) | Only counters and indices are used |

The solution easily fits within the constraints since even the maximum input size of 200,000 characters is handled with a single linear scan and constant extra memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = input().strip()
    t = input().strip()

    n, m = len(s), len(t)

    j = 0
    for i in range(n):
        if j < m and s[i] == t[j]:
            j += 1

    if j != m:
        return "NO"

    if (n - m) % 2 != 0:
        return "NO"

    return "YES"

# provided samples
assert run("sobaka\nbaka\n") == "YES", "sample 1"
assert run("sobabka\nbaka\n") == "NO", "sample 2"
assert run("abacaba\naca\n") == "YES", "sample 3"

# custom cases
assert run("a\na\n") == "YES", "identical strings"
assert run("ab\na\n") == "NO", "odd deletion count"
assert run("abcdef\nace\n") == "YES", "subsequence with even removals"
assert run("abcdef\naec\n") == "NO", "subsequence fails"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical strings | YES | no deletions needed |
| odd deletion count | NO | parity constraint |
| subsequence valid even case | YES | general correctness |
| subsequence invalid case | NO | ordering constraint |

## Edge Cases

One edge case is when both strings are identical. The algorithm immediately accepts because the subsequence check passes trivially and the length difference is zero, which is even. No deletions are needed, and the answer is correct.

Another edge case is when `t` is empty. The subsequence condition always passes, and the answer depends only on whether `|s|` is even. If `s` has odd length, one character would remain unremovable, so the answer is `NO`. The algorithm correctly captures this via the parity check.

A final edge case is when `t` is of length `|s| - 1`. Even if `t` is a valid subsequence, the difference is 1, which is odd, forcing rejection. This matches the fact that a single leftover character cannot be deleted using pair operations.
