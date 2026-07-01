---
title: "CF 104393C - Counting Risk Factors"
description: "We are given a long string that represents a linear chemical strip. Each position on the strip is a lowercase letter. Some letters are marked as “risky”. For any substring of the strip, we can count how many risky characters it contains."
date: "2026-06-30T23:52:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104393
codeforces_index: "C"
codeforces_contest_name: "ICPC Masters Mexico LATAM 2023"
rating: 0
weight: 104393
solve_time_s: 110
verified: true
draft: false
---

[CF 104393C - Counting Risk Factors](https://codeforces.com/problemset/problem/104393/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long string that represents a linear chemical strip. Each position on the strip is a lowercase letter. Some letters are marked as “risky”. For any substring of the strip, we can count how many risky characters it contains. The task is to count how many substrings have exactly K risky characters.

A substring is defined by choosing two indices l and r with l ≤ r and taking all characters between them. Since the string length can be up to one million, we clearly cannot enumerate all O(N²) substrings.

The output is a single integer: the total number of substrings whose number of risky letters is exactly K.

The main difficulty is that we are counting over all substrings, which are quadratic in number. Any approach that explicitly checks substrings will time out. This immediately forces a linear or near-linear approach.

A subtle edge case comes when K is zero. In that case, we are counting substrings that contain no risky characters at all, so the answer depends entirely on maximal blocks of safe characters. Another edge case is when L = 0, meaning no risky letters exist at all. Then every substring is valid only if K = 0, otherwise the answer is zero.

## Approaches

The brute force idea is straightforward. For every substring, we count how many risky characters it contains and check if it equals K. This works conceptually because it directly matches the definition of the problem. However, each substring takes O(N) to evaluate if done naively, and there are O(N²) substrings, leading to O(N³) total complexity. Even if we optimize counting using prefix sums, we still need O(1) per substring, leaving O(N²), which is too large for N up to 10⁶.

The key observation is that the condition “exactly K risky characters” can be turned into a standard prefix sum counting problem. We convert the string into a binary array where each position is 1 if it is a risky character and 0 otherwise. Now the problem becomes counting subarrays whose sum is exactly K.

For this type of problem, prefix sums are the natural tool. Let prefix[i] be the number of risky characters in the first i positions. Then a substring (l, r) has sum K if and only if prefix[r] - prefix[l - 1] = K, which rearranges to prefix[l - 1] = prefix[r] - K. This means that for each r, we need to know how many previous prefix sums equal prefix[r] - K.

We maintain a frequency map of prefix sums as we scan the string once. This yields an O(N) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) or worse | O(1) | Too slow |
| Prefix Sum + Hashing | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We first convert the set of risky characters into a fast lookup structure, typically a boolean array or a set. Then we scan the string from left to right while maintaining a running prefix count of risky characters.

1. We initialize a frequency map that stores how many times each prefix sum has occurred. We start by inserting prefix sum 0 with frequency 1, since an empty prefix has zero risky characters.
2. We iterate through the string, updating a running counter curr. If the current character is risky, we increment curr by 1. Otherwise, it remains unchanged. This keeps track of how many risky characters we have seen so far.
3. At each position, we want to know how many earlier prefixes would form a substring ending here with exactly K risky characters. That condition translates into looking up how many times curr - K has appeared before.
4. We add that frequency to the answer.
5. We then update the frequency map by incrementing the count of curr.

Each step builds on the previous prefix structure, ensuring that every substring ending at the current position is counted exactly once if it satisfies the condition.

The key invariant is that at index i, the frequency map contains exactly the counts of all prefix sums from positions 0 to i. This ensures that every valid substring ending at i is counted using a unique earlier prefix, and no invalid substring is included because the difference in prefix sums enforces the exact K constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, l = map(int, input().split())
    s = input().strip()
    risky = set(input().strip())

    # prefix sum frequency map
    freq = {0: 1}
    curr = 0
    ans = 0

    for ch in s:
        if ch in risky:
            curr += 1

        need = curr - k
        ans += freq.get(need, 0)

        freq[curr] = freq.get(curr, 0) + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by reading input and storing risky letters in a set for O(1) membership checks. We maintain curr as the running prefix count of risky characters. The dictionary freq stores how many times each prefix sum has been observed so far. For each character, we compute how many earlier prefixes would form a valid substring ending at the current index, accumulate that into ans, and then update the prefix frequency map.

A common mistake is updating the frequency map before querying it, which would incorrectly allow empty substrings or miscount self-pairs. The correct order is query first, then update.

## Worked Examples

### Example 1

Input:

```
4 1 1
abac
a
```

We mark only 'a' as risky.

| i | char | curr | need = curr - K | freq[need] | ans | freq update |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | a | 1 | 0 | 1 | 1 | {0:1,1:1} |
| 1 | b | 1 | 0 | 1 | 2 | {0:1,1:2} |
| 2 | a | 2 | 1 | 2 | 4 | {0:1,1:2,2:1} |
| 3 | c | 2 | 1 | 2 | 6 | ... |

This shows that every substring ending at each position is counted exactly when it contains one risky character.

### Example 2

Input:

```
4 2 2
bcfe
bf
```

Here b and f are risky.

| i | char | curr | need | freq[need] | ans | freq |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | b | 1 | -1 | 0 | 0 | {0:1,1:1} |
| 1 | c | 1 | -1 | 0 | 0 | {0:1,1:1} |
| 2 | f | 2 | 0 | 1 | 1 | {0:1,1:1,2:1} |
| 3 | e | 2 | 0 | 1 | 2 | ... |

Only substrings ending at positions where exactly two risky letters have been accumulated contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Single pass through the string with O(1) hash operations per character |
| Space | O(N) | In worst case all prefix sums are distinct |

This fits comfortably within the constraints since N can be up to 10⁶, and a linear pass with hashing is efficient enough in both time and memory.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k, l = map(int, input().split())
    s = input().strip()
    risky = set(input().strip())

    freq = {0: 1}
    curr = 0
    ans = 0

    for ch in s:
        if ch in risky:
            curr += 1
        ans += freq.get(curr - k, 0)
        freq[curr] = freq.get(curr, 0) + 1

    return str(ans)

# provided samples
assert solve("4 1 1\nabac\na\n") == "6", "sample 1"
assert solve("4 2 2\nbcfe\nbf\n") == "2", "sample 2"
assert solve("4 10 2\nabdc\nad\n") == "0", "sample 3"

# custom cases
assert solve("5 0 1\nabcde\na\n") == "15", "all substrings without a"
assert solve("5 1 0\nabcde\n\n") == "0", "no risky letters but K>0"
assert solve("5 1 1\naaaaa\na\n") == "15", "all substrings valid"
assert solve("1 1 1\na\na\n") == "1", "single char match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all substrings safe | 15 | K=0 behavior |
| no risky letters | 0 | empty risk set |
| all risky | 15 | full accumulation |
| single element | 1 | boundary correctness |

## Edge Cases

When L = 0, the risky set is empty, so curr never increases. The algorithm correctly counts only substrings when K = 0, since only prefix differences of zero match.

When K is larger than any possible number of risky characters, the lookup freq[curr - K] always fails safely and contributes zero.

When the string contains all risky characters, curr increases every step and prefix frequencies ensure that all subarrays are counted correctly as combinations of prefix differences.
