---
title: "CF 2182A - New Year String"
description: "We are given a string composed of the characters 0, 2, 5, and 6. A string is considered a New Year string if it either contains the substring 2026 somewhere or does not contain the substring 2025 at all."
date: "2026-06-07T21:51:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 2182
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 186 (Rated for Div. 2)"
rating: 800
weight: 2182
solve_time_s: 117
verified: true
draft: false
---

[CF 2182A - New Year String](https://codeforces.com/problemset/problem/2182/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, implementation, strings  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string composed of the characters 0, 2, 5, and 6. A string is considered a _New Year string_ if it either contains the substring `2026` somewhere or does not contain the substring `2025` at all. For each string, we are allowed to change any character to one of the four allowed characters any number of times. Our task is to compute the minimum number of such character replacements needed to make the string a New Year string.

Each test case provides the string length `n` and the string `s`. The constraints `4 ≤ n ≤ 20` and up to `10^4` test cases imply that the strings are short enough for simple brute-force or combinatorial checks, but the number of test cases is high, so we need a solution that is efficient for each individual string.

Non-obvious edge cases arise when the string already partially contains `2025` or `2026`. For example, the string `2025` is not a New Year string and requires at least one change. Replacing the last `5` with `6` makes it `2026`, which satisfies the first condition. Another tricky case is `20252025`, which contains `2025` twice. Simply changing the last character is insufficient; we need the minimal change that either introduces `2026` or removes `2025`.

## Approaches

The naive brute-force approach is to try all possible combinations of character replacements. For each character, we could attempt all four possible replacements, generating `4^n` possible strings. For `n = 20`, this produces over a trillion possibilities, which is clearly infeasible.

The key observation is that the problem is constrained to short strings. The only substring that directly triggers a requirement is `2026` or `2025`. Therefore, we do not need to generate all strings; we only need to check every substring of length 4 in the input. For each 4-length window, we compute how many character changes are needed to make it exactly `2026`. The minimum of these values across all windows is the minimal number of changes needed to satisfy the first condition.

If the string contains `2025`, we can either modify some characters to break `2025` or directly convert one occurrence into `2026` (which simultaneously breaks `2025` and satisfies the first condition). This makes the solution much simpler: iterate all length-4 substrings, compute mismatches with `2026`, and pick the minimum. Because `n ≤ 20`, this check requires at most `17 * 4 = 68` comparisons per string, which is fast enough for `10^4` test cases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all replacements) | O(4^n) | O(n) | Too slow |
| Optimal (check length-4 substrings) | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the string `s` and its length `n`.
3. Initialize a variable `min_changes` with a large value. This will store the minimal operations needed.
4. Iterate over all substrings of length 4 in `s`. For each substring, count how many characters differ from the target string `2026`.
5. Update `min_changes` with the minimum mismatch found among all substrings.
6. If the string does not contain `2025` at all, then zero changes are needed according to the second New Year string condition.
7. Output the minimal number of operations for each test case.

Why it works: by checking all length-4 substrings against `2026`, we guarantee that if it is possible to create `2026` in the string with minimal changes, we will find the optimal number. For strings not containing `2025`, the algorithm implicitly returns zero because no changes are required to satisfy the second condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    
    if "2025" not in s:
        print(0)
        continue
    
    min_changes = float('inf')
    for i in range(n - 3):
        substring = s[i:i+4]
        changes = sum(substring[j] != target for j, target in enumerate("2026"))
        if changes < min_changes:
            min_changes = changes
    print(min_changes)
```

This code first checks if `2025` exists. If not, zero changes are required. Otherwise, it iterates through each 4-character substring and counts mismatches with `2026`. `min_changes` ensures we find the minimal operation count.

## Worked Examples

### Example 1

Input:

```
4
2025
```

| i | substring | mismatch vs 2026 | min_changes |
| --- | --- | --- | --- |
| 0 | 2025 | 1 | 1 |

Output: 1

The substring `2025` requires only the last character to change to `6` to become `2026`.

### Example 2

Input:

```
8
20252025
```

| i | substring | mismatch vs 2026 | min_changes |
| --- | --- | --- | --- |
| 0 | 2025 | 1 | 1 |
| 1 | 0252 | 3 | 1 |
| 2 | 2520 | 4 | 1 |
| 3 | 5202 | 4 | 1 |
| 4 | 2025 | 1 | 1 |

Output: 1

Even though there are two occurrences of `2025`, changing a single character in the first occurrence suffices to satisfy the first condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | For each of the `t` test cases, we iterate through up to `n-3` substrings of length 4. |
| Space | O(1) | Only a few integer variables are used; we do not store intermediate arrays. |

Given `t ≤ 10^4` and `n ≤ 20`, the total number of operations is at most `2 * 10^5`, which fits comfortably within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        
        if "2025" not in s:
            print(0)
            continue
        
        min_changes = float('inf')
        for i in range(n - 3):
            substring = s[i:i+4]
            changes = sum(substring[j] != target for j, target in enumerate("2026"))
            if changes < min_changes:
                min_changes = changes
        print(min_changes)
    return output.getvalue().strip()

# Provided samples
assert run("7\n4\n0000\n4\n2025\n4\n2026\n8\n20252026\n8\n20252025\n9\n202520256\n9\n202520265\n") == "0\n1\n0\n0\n1\n1\n0"

# Custom cases
assert run("2\n4\n2025\n4\n0002\n") == "1\n0", "handles single 2025 and no 2025"
assert run("1\n20\n20252025202520252025\n") == "1", "long repeated 2025"
assert run("1\n4\n2026\n") == "0", "already New Year string"
assert run("1\n5\n22222\n") == "0", "no 2025, no change needed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2025` | 1 | Correctly converts a single occurrence of 2025 |
| `0002` | 0 | Does not contain 2025, so zero changes |
| `20252025202520252025` | 1 | Multiple consecutive 2025, minimal change applied |
| `2026` | 0 | Already contains 2026 |
| `22222` | 0 | No forbidden substring, nothing to change |

## Edge Cases

For a string that is already valid by the second condition, such as `0000`, the algorithm checks for `2025`. Since it does not exist, it outputs zero immediately. For strings with multiple overlapping `2025`, the algorithm examines all substrings of length 4 and finds the minimal number of character changes to create `2026`, which simultaneously removes all instances of `2025` within that substring. For strings that already contain `2026`, mismatches with `2026` will be zero, so the output is zero, confirming correctness.
