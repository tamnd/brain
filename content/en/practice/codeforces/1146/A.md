---
title: "CF 1146A - Love \"A\"
description: "The problem gives us a string consisting of lowercase letters, and Alice wants to transform it into a “good” string. A good string is one in which strictly more than half of the characters are the letter 'a'."
date: "2026-06-12T03:18:42+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1146
codeforces_index: "A"
codeforces_contest_name: "Forethought Future Cup - Elimination Round"
rating: 800
weight: 1146
solve_time_s: 87
verified: true
draft: false
---

[CF 1146A - Love \"A\](https://codeforces.com/problemset/problem/1146/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives us a string consisting of lowercase letters, and Alice wants to transform it into a “good” string. A good string is one in which strictly more than half of the characters are the letter 'a'. Alice can delete any number of characters, including zero, but cannot add new ones. The goal is to determine the maximum length of a good string she can obtain after deleting characters.

Given that the string length is at most 50, we can reason about all possible deletions without worrying about performance for brute-force approaches. However, the problem has a hidden mathematical structure that allows a simple and direct solution. The string is guaranteed to contain at least one 'a', which ensures that a good string is always possible. Edge cases include strings that are already dominated by 'a's, strings with just one 'a' among many other letters, and strings that contain only 'a's.

A naive implementation might try to generate all subsets of characters, count the 'a's in each subset, and check if the subset satisfies the majority condition. This approach would work for small strings but is unnecessary and overcomplicated.

For example, consider the input `abbb`. There is one 'a' and three other letters. To make the string good, we need more 'a's than non-'a's. If we keep all four letters, we have one 'a' and three non-'a's, which is not good. Deleting two 'b's leaves `abb` with one 'a' and two non-'a's, still not good. Deleting three 'b's leaves `a`, which is good. So the answer is 1.

## Approaches

The brute-force method works by considering every possible subset of characters, counting 'a's and other letters, and checking if more than half of the remaining characters are 'a'. This approach is correct because it explores all possibilities, but its complexity is O(2^n) in the worst case, which is unnecessary even for n=50.

The optimal approach comes from observing that deleting non-'a' characters increases the proportion of 'a's. Let `count_a` be the number of 'a's and `count_other` be the number of non-'a' characters. To satisfy the “good” condition, the number of 'a's must be greater than the number of other characters that remain. If we delete enough non-'a' characters such that `count_a > count_other_remaining`, we maximize the resulting string length by retaining all 'a's and just enough non-'a's to satisfy the strict majority.

Mathematically, if we keep all 'a's and `k` other letters, the condition `count_a > k` must hold. The maximum possible k is `count_a - 1` since keeping `count_a` or more other letters would violate the majority condition. Therefore, the maximum length of a good string is `count_a + min(count_other, count_a - 1)`. This reduces the problem to a single scan counting 'a's and subtracting from the total length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the total number of 'a's in the string and store it in `count_a`. This identifies the characters we want to dominate the final string.
2. Compute the total number of non-'a' characters as `count_other = len(s) - count_a`. These are candidates for deletion.
3. Determine the maximum number of non-'a' characters that can remain while still keeping the string good. The strict majority condition requires `count_a > count_other_remaining`, so the maximum `count_other_remaining` is `count_a - 1`.
4. The maximum length of the resulting good string is therefore `count_a + min(count_other, count_a - 1)`. If there are fewer non-'a' characters than `count_a - 1`, keep all of them; otherwise, keep only `count_a - 1`.
5. Print the result.

Why it works: the algorithm guarantees that the number of 'a's is always strictly more than the number of other letters in the final string. This invariant satisfies the definition of a good string and maximizes the length by retaining as many other letters as possible without violating the strict majority.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
count_a = s.count('a')
count_other = len(s) - count_a
# maximum number of non-'a's we can keep while keeping 'a's in strict majority
max_good_length = count_a + min(count_other, count_a - 1)
print(max_good_length)
```

The code first counts the number of 'a's and non-'a's. The formula `count_a + min(count_other, count_a - 1)` ensures the maximum good string length. Using `min` handles cases where there are fewer non-'a's than `count_a - 1`, avoiding negative lengths. Stripping the input avoids trailing newline issues.

## Worked Examples

### Sample 1: `xaxxxxa`

| Step | count_a | count_other | min(count_other, count_a-1) | max_good_length |
| --- | --- | --- | --- | --- |
| Initial | 2 | 5 | min(5,1)=1 | 2+1=3 |

The trace confirms we keep both 'a's and one non-'a', matching the expected output 3.

### Sample 2: `aa`

| Step | count_a | count_other | min(count_other, count_a-1) | max_good_length |
| --- | --- | --- | --- | --- |
| Initial | 2 | 0 | min(0,1)=0 | 2+0=2 |

All letters are 'a', so the string is already good. The formula correctly returns the length 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting 'a's requires scanning the string once |
| Space | O(1) | Only a few integer variables are used |

Given the maximum string length of 50, this algorithm executes in microseconds and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    count_a = s.count('a')
    count_other = len(s) - count_a
    return str(count_a + min(count_other, count_a - 1))

# provided samples
assert run("xaxxxxa\n") == "3", "sample 1"
assert run("aa\n") == "2", "sample 2"

# custom cases
assert run("a\n") == "1", "single 'a'"
assert run("baba\n") == "3", "two 'a's, two other letters"
assert run("aaaaa\n") == "5", "all 'a's"
assert run("abbbbb\n") == "1", "one 'a', many non-'a's"
assert run("abcde\n") == "1", "one 'a', four others"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | 1 | Minimum-size input |
| `baba` | 3 | Correct deletion of non-'a's to achieve majority |
| `aaaaa` | 5 | All letters are 'a' |
| `abbbbb` | 1 | Only one 'a' dominates |
| `abcde` | 1 | Edge case with multiple non-'a's |

## Edge Cases

For a single 'a', `s = "a"`, `count_a = 1`, `count_other = 0`. The formula gives `1 + min(0, 0) = 1`, which is correct.

For `s = "abbbbb"`, `count_a = 1`, `count_other = 5`. The maximum non-'a's we can keep is `count_a - 1 = 0`. The formula gives `1 + 0 = 1`. Deleting all 'b's except keeping 'a' ensures the strict majority, which aligns with the problem requirements. This demonstrates the algorithm handles extreme imbalance correctly.
