---
title: "CF 105170I - The Easiest Problem"
description: "The task gives a single fixed sentence as input: “Scan the QR code to sign in now.”. The goal is not to transform it or interpret it, but to compute a simple property of this exact text, namely how many characters in it are lowercase English letters from a to z."
date: "2026-06-27T08:33:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105170
codeforces_index: "I"
codeforces_contest_name: "The 2024 CCPC National Invitational Contest (Changchun) , The 17th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 105170
solve_time_s: 125
verified: true
draft: false
---

[CF 105170I - The Easiest Problem](https://codeforces.com/problemset/problem/105170/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The task gives a single fixed sentence as input: “Scan the QR code to sign in now.”. The goal is not to transform it or interpret it, but to compute a simple property of this exact text, namely how many characters in it are lowercase English letters from a to z.

The input is always just one line, so there is no parsing complexity beyond reading a string. The output is a single integer representing the count of characters that are lowercase letters. Uppercase letters, spaces, punctuation marks, and any other symbols are ignored.

Since the input length is constant and small, there are no algorithmic constraints in the usual competitive programming sense. Any approach from a direct scan to even multiple passes over the string is fast enough. The only meaningful risk is off-by-one or misclassifying characters, for example accidentally counting uppercase letters or including spaces.

A common mistake is treating all alphabetic characters as valid without distinguishing case. For example, in the substring “QR”, both characters are uppercase and should not contribute to the answer, even though they are letters. Another mistake is forgetting to ignore the final period.

## Approaches

The brute-force interpretation is to iterate through every character in the string and test whether it belongs to the range ‘a’ to ‘z’. If it does, we increment a counter. This works because each character can be independently classified without needing any context from neighbors or global structure.

The cost of this approach is linear in the length of the sentence. Since the sentence is fixed and short, this is already optimal in practice. Even if the input were much larger, a single scan remains sufficient because the operation per character is constant time.

The key observation is that the problem reduces to character classification. There is no need for parsing words, splitting tokens, or handling grammar. The sentence structure is irrelevant except as a source of characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(n) | O(1) | Accepted |
| Direct Python count/filter | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal strategy

1. Read the input line as a string. This preserves spaces and punctuation exactly as given, which is necessary because every character position matters for classification.
2. Initialize a counter to zero. This variable tracks how many valid lowercase letters have been seen so far.
3. Iterate over each character in the string. Each character is checked independently, since membership in the valid set does not depend on position.
4. For each character, check whether it lies between ‘a’ and ‘z’. If it does, increment the counter. This condition naturally excludes uppercase letters, spaces, and punctuation without needing special cases for each type.
5. After finishing the scan, output the counter.

### Why it works

The algorithm relies on the fact that the classification condition partitions the character set into two disjoint groups: valid lowercase letters and everything else. Each character is processed exactly once, and its contribution to the final answer is independent of all other characters. This guarantees that summing local decisions produces the correct global count.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().rstrip("\n")

ans = 0
for ch in s:
    if 'a' <= ch <= 'z':
        ans += 1

print(ans)
```

The solution reads the entire line including spaces, then removes only the trailing newline. The loop checks each character using direct ASCII range comparison, which is faster and more explicit than calling methods like `islower`, which would also include non-English lowercase letters in some environments.

The counter `ans` is updated only when the character is strictly in the lowercase English range, ensuring uppercase letters like ‘S’, ‘Q’, and ‘R’ are excluded even though they are alphabetic.

## Worked Examples

### Example 1

Input:

```
Scan the QR code to sign in now.
```

We process characters sequentially:

| Character | Lowercase a-z? | Count |
| --- | --- | --- |
| S | No | 0 |
| c | Yes | 1 |
| a | Yes | 2 |
| n | Yes | 3 |
| space | No | 3 |
| t | Yes | 4 |
| h | Yes | 5 |
| e | Yes | 6 |
| space | No | 6 |
| Q | No | 6 |
| R | No | 6 |
| space | No | 6 |
| c | Yes | 7 |
| o | Yes | 8 |
| d | Yes | 9 |
| e | Yes | 10 |
| space | No | 10 |
| t | Yes | 11 |
| o | Yes | 12 |
| space | No | 12 |
| s | Yes | 13 |
| i | Yes | 14 |
| g | Yes | 15 |
| n | Yes | 16 |
| space | No | 16 |
| i | Yes | 17 |
| n | Yes | 18 |
| space | No | 18 |
| n | Yes | 19 |
| o | Yes | 20 |
| w | Yes | 21 |
| . | No | 21 |

Final answer is 21.

This trace confirms that only lowercase English letters are counted, and all structural characters are ignored.

### Example 2

Input:

```
abcXYZ.
```

| Character | Lowercase a-z? | Count |
| --- | --- | --- |
| a | Yes | 1 |
| b | Yes | 2 |
| c | Yes | 3 |
| X | No | 3 |
| Y | No | 3 |
| Z | No | 3 |
| . | No | 3 |

Output is 3.

This shows that uppercase letters do not contribute even when they are adjacent to valid lowercase letters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is checked once in a single linear scan |
| Space | O(1) | Only a counter is stored regardless of input size |

The input length is fixed and small, so the solution is trivially within limits. Even for much larger inputs, a single pass character scan remains efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    input = sys.stdin.readline

    s = input().rstrip("\n")
    ans = 0
    for ch in s:
        if 'a' <= ch <= 'z':
            ans += 1
    return str(ans)

# provided sample (as described)
assert run("Scan the QR code to sign in now.\n") == "21"

# all uppercase only
assert run("ABCDEF.\n") == "0"

# all lowercase letters
assert run("abcdef\n") == "6"

# mixed sentence
assert run("aA bB cC.\n") == "3"

# single character edge
assert run("z\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| “Scan the QR code to sign in now.” | 21 | main mixed-case sentence |
| “ABCDEF.” | 0 | no lowercase letters |
| “abcdef” | 6 | all valid characters |
| “aA bB cC.” | 3 | case filtering correctness |
| “z” | 1 | minimal input |

## Edge Cases

The main edge case is when letters appear in uppercase form. For example, in the input “QR”, both characters are alphabetic but must be excluded. The algorithm handles this correctly because it explicitly restricts the range to lowercase ‘a’ through ‘z’, so uppercase ASCII values fall outside the condition.

Another edge case is punctuation adjacency. In “now.” the period immediately follows a valid sequence of letters. Since the check is character-based, punctuation never affects neighboring characters, and only ‘n’, ‘o’, and ‘w’ are counted.

Finally, spaces are frequent separators in the sentence. The algorithm naturally ignores them because they do not fall within the lowercase range, so no special handling is required.
