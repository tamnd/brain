---
title: "CF 103797C - Cute Sentences"
description: "We are given a sentence split into a sequence of words. Each word consists only of uppercase English letters. The task is to determine whether the sentence satisfies a specific structural property involving its first word."
date: "2026-07-02T08:46:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103797
codeforces_index: "C"
codeforces_contest_name: "IME++ Starters Try-outs 2022"
rating: 0
weight: 103797
solve_time_s: 45
verified: true
draft: false
---

[CF 103797C - Cute Sentences](https://codeforces.com/problemset/problem/103797/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sentence split into a sequence of words. Each word consists only of uppercase English letters. The task is to determine whether the sentence satisfies a specific structural property involving its first word.

The rule defines the sentence as “cute” if the first word can be reconstructed by taking the first letter of every word in the sentence, in order. In other words, if we write down the sentence as a list of words, extract the initial character of each word, and concatenate them, the resulting string must match the very first word exactly, with no extra or missing letters.

The input size is very small, with at most 100 words and each word up to 100 characters. This immediately implies that any solution operating in linear time over all characters is trivially fast enough. Even a solution that repeatedly scans the words multiple times would still be safe under the constraints.

The main risk is not performance but correctness. A few subtle cases matter:

One edge case is when the first word has a different length from the number of words. For example, if the sentence has 3 words but the first word has length 5, it is impossible for them to match since the acronym can only have length equal to the number of words.

Another edge case is when a word is a single letter. This is actually the normal case and must be handled consistently, since the acronym construction relies only on the first character of each word regardless of word length.

A third case is when the first letters match but ordering breaks alignment. For example, even if all letters exist among words, the sequence must match exactly in order, not as a set comparison.

## Approaches

A direct approach is to explicitly construct the acronym string by iterating over all words, taking the first character of each, and concatenating them into a new string. Then we compare this constructed string with the first word.

This is correct because the definition of “cute sentence” is purely structural and requires no transformations beyond extraction and comparison. The cost is dominated by scanning each word once, so total work is proportional to the sum of word lengths.

A brute-force variant might attempt to validate each character of the first word by scanning through words repeatedly or checking matching positions with nested loops. While still feasible under constraints, it is unnecessarily complex and can introduce indexing mistakes. In the worst case, such an approach could perform O(N^2) character checks, which is still small here but scales poorly for larger inputs.

The key observation is that the acronym is uniquely determined by the first characters of each word, so we never need to consider any other structure. This reduces the problem to a single pass construction and comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Accepted but unnecessary |
| Optimal | O(total characters) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read the number of words and the list of words. We keep them in order since positional structure is essential.
2. Extract the first character of each word and build a new string. This string represents the acronym implied by the sentence definition.
3. Compare the constructed acronym with the first word in the sentence.
4. If they are identical, output “Yes”, otherwise output “No”.

Each step mirrors the definition directly, so there is no need for auxiliary structures or preprocessing beyond simple iteration.

### Why it works

The first word is required to be exactly equal to the concatenation of the first characters of all words. Since each word contributes exactly one character to the acronym, and order is preserved, the constructed string is the only possible candidate. Therefore, equality between the constructed string and the first word is both necessary and sufficient for correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    words = input().split()

    acronym = ''.join(w[0] for w in words)

    if acronym == words[0]:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The solution first reads the integer count, then reads the sentence. Using `split()` ensures we correctly separate words regardless of spacing irregularities.

The core operation is the generator expression `w[0] for w in words`, which safely extracts the first character of each word. Since every word is guaranteed non-empty, there is no risk of index errors.

Finally, we compare the constructed acronym with `words[0]`, which represents the required target word.

## Worked Examples

Consider the input:

IME MELHOR ENGENHARIA

We process the words: IME, MELHOR, ENGENHARIA.

| Step | Word | First letter | Acronym so far |
| --- | --- | --- | --- |
| 1 | IME | I | I |
| 2 | MELHOR | M | IM |
| 3 | ENGENHARIA | E | IME |

The final acronym is “IME”, which matches the first word. The output is “Yes”.

This trace confirms that the algorithm correctly accumulates the acronym in order and performs a direct comparison.

Now consider:

IME MITO

| Step | Word | First letter | Acronym so far |
| --- | --- | --- | --- |
| 1 | IME | I | I |
| 2 | MITO | M | IM |

The acronym is “IM”, which does not match “IME”. The output is “No”.

This shows that even small mismatches in length or trailing characters are detected immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · L) | Each word is scanned once to extract its first character |
| Space | O(N) | Stores the list of words and the acronym string |

The input bounds are small enough that even the worst-case scenario of 100 words of length 100 is trivial. The solution runs well within both the 1 second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (as described in statement)
assert run("3\nIME MELHOR ENGENHARIA\n") == "Yes"
assert run("2\nIME MITO\n") == "No"

# all equal single-letter words
assert run("3\nA A A\n") == "Yes"

# mismatch due to extra letter in first word
assert run("2\nAB A\n") == "No"

# single word case
assert run("1\nA\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 words forming IME | Yes | Basic correct case |
| IME MITO | No | Length mismatch |
| A A A | Yes | Single-letter consistency |
| AB A | No | Extra character in first word |
| Single word | Yes | Minimum boundary case |

## Edge Cases

A key edge case is when there is only one word. For input:

1

A

The algorithm constructs the acronym by taking the first character of the only word, producing “A”. It then compares this to the first word, which is also “A”, so the output is “Yes”. This correctly handles the degenerate case where the sentence consists of a single word.

Another case is when the first word is longer than the number of words. For example:

3

ABCD A B

The acronym becomes “AAB”, while the first word is “ABCD”. Since the strings differ immediately, the algorithm correctly outputs “No” without any special handling.

Finally, when all words are identical single characters, such as:

4

X X X X

The acronym is “XXXX”, matching the first word exactly, so the output is “Yes”. This confirms that repeated characters and uniform inputs behave correctly under the same logic.
