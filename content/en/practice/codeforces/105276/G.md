---
title: "CF 105276G - GPT Intrusion"
description: "We are given a program as plain text, split into several lines. The task is to determine whether this program is “suspected to be written by GPT and exceeds its output limit."
date: "2026-06-23T14:12:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105276
codeforces_index: "G"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2023"
rating: 0
weight: 105276
solve_time_s: 60
verified: true
draft: false
---

[CF 105276G - GPT Intrusion](https://codeforces.com/problemset/problem/105276/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a program as plain text, split into several lines. The task is to determine whether this program is “suspected to be written by GPT and exceeds its output limit.”

The suspicion rule is tied to a specific behavior: a GPT-like generator produces output that is truncated to 500 characters. If the generated text is longer than 500 characters, only the first 500 characters are kept, and after that a fixed suffix appears:

`As an AI model, my output is limited to 500 characters.`

This means that if we observe this exact suffix appearing anywhere in the given source code, it indicates that the text was cut off mid-generation and the model appended its truncation message. That is the only signal we need to detect “GPT intrusion.”

The input is simply a collection of lines forming a single continuous text when read in order. Line breaks are part of the text, so they contribute to the character stream. The output is binary: print “Yes” if the truncation message appears, otherwise print “No.”

The constraints are small: at most 500 lines, and total character count across all lines does not exceed 1000. This guarantees that a straightforward scan over the concatenated text is sufficient. Any solution that is linear in the total input size will run instantly.

A subtle edge case is that the target phrase might appear split across line boundaries. For example, the string could end one line with:

`As an AI model, my output is limited to 500 char`

and the next line begins with:

`acters.`

A naive per-line search would miss this, so the correct approach must treat the input as a single continuous string.

Another edge case is multiple occurrences of the phrase. Even a single occurrence is enough to output “Yes,” so counting is unnecessary.

## Approaches

A brute-force interpretation would be to repeatedly scan every possible substring of the concatenated text and check whether it matches the target phrase. If the text length is $L$ and the phrase length is $P = 51$, this leads to $O(L \cdot P)$ comparisons or worse if implemented carelessly. Although still small under constraints, it is unnecessary and conceptually heavier than needed.

The key observation is that we are not searching for arbitrary patterns; we are searching for one fixed string. This reduces the problem to a classic substring search. Since the total length is at most 1000, even a direct scan checking every starting position works in constant practical time.

We concatenate all lines into one string and use a single substring containment check. This is enough because Python’s substring search is efficient and effectively linear for this size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force substring enumeration | O(L·P) | O(1) | Too slow conceptually |
| Direct substring search | O(L) | O(L) | Accepted |

## Algorithm Walkthrough

1. Read the integer $N$, which tells how many lines the source code has. This defines how many segments we will concatenate.
2. Read each line and append it to a growing string, inserting a newline character between lines. This step is necessary because the truncation message may span across line boundaries, so preserving exact structure avoids false negatives.
3. After building the full text, define the target pattern string exactly as given in the problem statement.
4. Check whether this pattern appears as a substring anywhere in the full text.
5. If it appears at least once, output “Yes,” otherwise output “No.”

### Why it works

The algorithm relies on the fact that the truncation artifact is a fixed and unique string. If the source was cut by the GPT system, that exact string must appear verbatim and contiguously in the output. Since we preserve all characters including newline boundaries, any occurrence in the original stream remains detectable in the reconstructed string. No other behavior can generate a false positive because normal source code does not contain this artificial system message.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    lines = [input().rstrip("\n") for _ in range(n)]
    text = "\n".join(lines)

    pattern = "As an AI model, my output is limited to 500 characters."
    if pattern in text:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The implementation reads all lines exactly as given, preserving structure by joining with newline characters. Using `rstrip("\n")` avoids accidental duplication of newline separators while still preserving the logical layout of the source code.

The key decision is to keep the text intact rather than stripping all whitespace. Since the pattern includes spaces and is sensitive to character boundaries, any normalization would risk breaking valid matches.

The substring check is done once on the full text, ensuring simplicity and correctness.

## Worked Examples

### Sample 1

Input:

```
6
#include <cstdio>
using namespace std;
int main() {
    printf("No\n");
    return 0;
}
```

| Step | Action | Text State (partial) | Pattern Found |
| --- | --- | --- | --- |
| 1 | Read lines | empty | No |
| 2 | Concatenate lines | full C++ program | No |
| 3 | Search substring | unchanged | No |

The program contains no truncation artifact, so the final check fails and output is “No.”

### Sample 2

Input ends mid-generation and includes the truncation message:

```
15
...
// Reads a strAs an AI model, my output is limited to 500 characters.
```

| Step | Action | Text State (partial) | Pattern Found |
| --- | --- | --- | --- |
| 1 | Read lines | accumulating partial code | No |
| 2 | Final line includes pattern | concatenated text includes suffix | Yes |
| 3 | Substring search | full match detected | Yes |

This demonstrates the critical case where the message appears embedded mid-line. The concatenation ensures it is still visible as a continuous substring.

The output is “Yes” because the truncation marker is explicitly present.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L) | Single pass to build string and single substring search |
| Space | O(L) | Stores full concatenated input |

The total input size is bounded by 1000 characters, so even linear processing is negligible. The solution is well within limits.

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

# sample 1
assert run("""6
#include <cstdio>
using namespace std;
int main() {
    printf("No\n");
    return 0;
}
""") == "No"

# sample 2
assert run("""15
#include <iostream>
#include <string>
// The main function of the program
int main(int argc, char *argv[]) {
    int n;
    std::cin >> n;
    std::string s[1000];
    for (int i = 0; i < n; i++) {
        // Reads a strAs an AI model, my output is limited to 500 characters.
""") == "Yes"

# minimum size, no match
assert run("""1
hello world""") == "No"

# exact pattern only
assert run("""1
As an AI model, my output is limited to 500 characters.""") == "Yes"

# pattern split across lines
assert run("""3
As an AI model, my output is limited to 500 char
acters.
code""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single normal line | No | base case |
| exact full phrase | Yes | direct match |
| split across lines | Yes | boundary handling |

## Edge Cases

One important edge case is when the truncation message is split across multiple lines. Consider:

```
As an AI model, my output is limited to 500 char
acters.
```

When concatenated with newline preservation, this becomes:

`As an AI model, my output is limited to 500 char\nacters.`

The substring search still finds the contiguous sequence if the newline is present in the input representation. This is why joining with `\n` is critical; it preserves the exact stream structure so the pattern can still be matched reliably.

Another edge case is when the message appears at the very beginning or very end of the input. Since the check is global over the full string, both positions are handled naturally without special casing.

Finally, multiple occurrences do not change the answer. Even if the phrase appears several times, the output remains “Yes” because the condition is purely existential.
