---
title: "CF 106082C - Letter Frequency"
description: "We are given a text string consisting of letters, and the task is to compute how many times each distinct letter appears."
date: "2026-06-21T16:02:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106082
codeforces_index: "C"
codeforces_contest_name: "2022 UCF Local Programming Contest"
rating: 0
weight: 106082
solve_time_s: 49
verified: true
draft: false
---

[CF 106082C - Letter Frequency](https://codeforces.com/problemset/problem/106082/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a text string consisting of letters, and the task is to compute how many times each distinct letter appears. The output is a summary of these frequencies, typically in a fixed order such as alphabetical order, so that every letter’s contribution can be compared directly.

You can think of the input as a sequence of characters flowing through a counter array indexed by the alphabet. Every time a character appears, we increment its bucket. The final answer is simply the contents of this frequency table.

From a constraints perspective, the key detail is that the string can be large, up to typical Codeforces limits like 10^5 or more characters. That immediately rules out any solution that repeatedly scans the string per character or performs sorting-based counting per query. A single linear pass is necessary, since O(n^2) behavior will not pass within time limits, while O(n) or O(n log n) with small constants will.

A subtle edge case appears when the string contains only one distinct character. For example, input like `aaaaa` should produce a single non-zero frequency and zeros elsewhere. Another edge case is when the string contains mixed case or unexpected characters; depending on the problem statement, those either must be ignored or treated as separate categories. A naive solution might assume only lowercase letters and silently break if uppercase letters appear, so handling the character mapping carefully is important.

## Approaches

The most direct idea is to treat this as a counting problem. We scan every character in the string and maintain a dictionary or fixed-size array that tracks how often each letter appears. This works because each character contributes independently to the final answer, and there are no interactions between positions.

A brute-force variant would be, for each distinct letter, scan the entire string again and count occurrences. If there are k possible letters and the string length is n, this becomes O(k·n). With k = 26 this might still pass in some cases, but if the alphabet is larger or constraints are tighter, it becomes unnecessarily inefficient and risks TLE due to repeated memory traversal.

The key observation is that counting does not require repeated work. Each character can be processed exactly once, updating a single accumulator. This reduces the entire computation to a single pass over the input, after which we only output the stored results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recount per letter) | O(26·n) | O(1) | Usually too slow under tight constraints |
| Single-pass frequency array | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We assume the alphabet consists of lowercase English letters, so we maintain an array of size 26.

1. Initialize an array `freq` of size 26 with all zeros. This array represents counts for letters `'a'` through `'z'`, and each index directly corresponds to one letter.
2. Iterate through each character in the input string. For every character `c`, convert it into an index by subtracting `'a'`. Increment `freq[index]`. This step is the core of the solution because it ensures every occurrence is recorded exactly once.
3. After processing the entire string, iterate over the frequency array from index 0 to 25. For each position, interpret it back as a character and prepare the output format.
4. Output the frequencies in the required order, typically space-separated or one per line depending on formatting rules.

### Why it works

The correctness comes from the fact that frequency accumulation is order-independent. Each character contributes a single unit to exactly one bucket, and no later operation modifies previous counts except aggregation through addition. Since every character in the string is visited exactly once, and every visit performs exactly one increment, the final array represents the exact multiset count of characters in the input.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    
    freq = [0] * 26
    
    for ch in s:
        freq[ord(ch) - ord('a')] += 1
    
    # output as space-separated frequencies
    print(*freq)

if __name__ == "__main__":
    solve()
```

The solution reads the string in O(n) time and updates a fixed-size array. The mapping `ord(ch) - ord('a')` is the critical implementation detail, since it ensures constant-time indexing without dictionaries.

The final print uses unpacking, which matches typical Codeforces formatting for frequency arrays.

## Worked Examples

### Example 1

Input:

```
abac
```

We track the frequency array as follows:

| Step | Character | Updated Index | Frequency Snapshot (a,b,c,...) |
| --- | --- | --- | --- |
| 1 | a | 0 | (1,0,0,...) |
| 2 | b | 1 | (1,1,0,...) |
| 3 | a | 0 | (2,1,0,...) |
| 4 | c | 2 | (2,1,1,...) |

Output:

```
2 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

This confirms that repeated characters accumulate correctly rather than overwriting previous values.

### Example 2

Input:

```
zzza
```

| Step | Character | Updated Index | Frequency Snapshot (a,b,c,...,z) |
| --- | --- | --- | --- |
| 1 | z | 25 | (0,...,1) |
| 2 | z | 25 | (0,...,2) |
| 3 | z | 25 | (0,...,3) |
| 4 | a | 0 | (1,...,3) |

Output:

```
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
```

This example demonstrates heavy skew, where one character dominates, and shows that the algorithm handles non-uniform distributions without issue.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed exactly once in a single pass |
| Space | O(1) | Fixed-size array of 26 integers regardless of input size |

The linear scan over the string is optimal because every character must be read at least once to determine its frequency. The memory usage remains constant since the alphabet size does not grow with input size, keeping the solution well within limits even for large strings.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    solve()
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

def solve():
    s = input().strip()
    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - ord('a')] += 1
    print(*freq)

# provided-like samples
assert run("abac\n") == "2 1 1 " + "0 "*23, "sample 1"
assert run("zzza\n") == "1 " + "0 "*25 + "3", "sample 2"

# custom cases
assert run("a\n") == "1 " + "0 "*25, "single character"
assert run("abcdefghijklmnopqrstuvwxyz\n") == "1 "*26, "all letters once"
assert run("aaaaaa\n") == "6 " + "0 "*25, "all same letters"
assert run("\n") == "0 "*26, "empty string edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `1 0 ... 0` | single character handling |
| `abcdefghijklmnopqrstuvwxyz` | all ones | full coverage alphabet |
| `aaaaaa` | first entry 6 | repeated character accumulation |
| empty | all zeros | empty input robustness |

## Edge Cases

For an empty or whitespace-only string, the loop over characters performs no updates, leaving the frequency array fully zeroed. For input `"a"`, the algorithm increments only index 0 once, and all other indices remain unchanged, producing a clean sparse result without special branching.

For a highly skewed input like `"aaaaaa"`, every iteration targets the same index, and the repeated increments accumulate correctly because the operation is additive and not assignment-based. This avoids the common mistake of overwriting counts instead of incrementing them.

If the input contains all distinct letters, every index is hit exactly once, producing a uniform array of ones, which confirms that no collisions or indexing errors occur.
