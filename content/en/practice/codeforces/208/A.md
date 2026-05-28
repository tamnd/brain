---
title: "CF 208A - Dubstep"
description: "We are given a single compressed string that represents a song that was modified by repeatedly inserting the marker string \"WUB\" before, after, and between the original words."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 208
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 130 (Div. 2)"
rating: 900
weight: 208
solve_time_s: 59
verified: true
draft: false
---

[CF 208A - Dubstep](https://codeforces.com/problemset/problem/208/A)

**Rating:** 900  
**Tags:** strings  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single compressed string that represents a song that was modified by repeatedly inserting the marker string `"WUB"` before, after, and between the original words. After these insertions, everything was concatenated into one continuous string, so the original word boundaries are lost and all separators are hidden inside this pattern.

The task is to reconstruct the original sequence of words. Conceptually, we need to treat `"WUB"` as a delimiter that may appear in runs of arbitrary length, and recover the words that lie between these delimiters. Once the delimiters are removed, the remaining non-empty fragments, in order, form the original song.

The input length is at most 200 characters, which immediately suggests that even quadratic or cubic solutions would pass comfortably. However, the structure of the problem is string parsing, where an optimal linear scan is both simpler and more robust than any heavier approach.

A subtle edge case comes from repeated delimiters. The string may contain consecutive `"WUB"` blocks, producing empty segments between them. For example, `"WUBWUBABC"` should yield only `"ABC"`, not empty words. Another case is trailing or leading `"WUB"`, such as `"ABCWUB"` or `"WUBABC"`, which should not introduce empty words at the boundaries. A naive split that does not filter empty tokens would incorrectly treat these as words.

Another potential pitfall is misunderstanding that `"WUB"` is not a single-character separator but a three-character pattern. Treating it as independent letters would completely break reconstruction, since the pattern must be matched exactly.

## Approaches

A direct brute-force idea is to scan the string and, at every position, attempt to detect whether a word starts there. Since we do not know word boundaries, one could imagine recursively trying all possible ways to partition the string while ensuring that every `"WUB"` appears only as a separator. This quickly turns into a combinatorial explosion: at each index, we either decide it is part of a word or the start of a `"WUB"` block, and this branching leads to exponential behavior in the worst case.

Another naive but more structured approach is repeated string replacement. One might continuously replace occurrences of `"WUB"` with a space, then normalize multiple spaces, and finally split. While this is closer to the intended solution, careless implementations can degrade to O(n²) due to repeated scanning and string reconstruction after each replacement.

The key observation is that `"WUB"` acts purely as a delimiter and has no semantic meaning in the final output. This means we do not need to simulate insertions or reversals, we only need to remove all occurrences of this pattern and treat what remains as words separated by implicit boundaries. Since the input is small, we can safely scan once, detect occurrences of `"WUB"`, and skip them, collecting non-empty sequences of letters as words.

This reduces the problem to a single linear pass over the string, building words incrementally and flushing them whenever a delimiter is encountered.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We treat the string as a stream and build the answer incrementally.

1. Start from the first character and maintain a buffer for the current word.

This buffer stores consecutive letters that are not part of `"WUB"`.
2. At each position, check whether the next three characters form `"WUB"`.

If they do, we treat this as a separator boundary.
3. When we encounter `"WUB"`, we finalize the current buffer if it is non-empty and append it to the result list, then clear the buffer.

We then skip ahead by three characters, because we consumed the entire delimiter.
4. If the current position is not `"WUB"`, we append the character to the buffer and move forward by one.
5. After the scan finishes, if the buffer still contains a word, append it to the result list.
6. Join all collected words using a single space.

The important design choice is that we never attempt to interpret partial `"WUB"` matches. We only act when the full three-character pattern is confirmed, which prevents misalignment.

### Why it works

The invariant is that at any position in the scan, everything already processed has been fully decomposed into correct original words, and the buffer contains exactly the suffix of the current word segment since the last valid `"WUB"` boundary. Every time we detect `"WUB"`, we are guaranteed that no original word contains this substring, so the boundary is real and safe to cut. Since the original construction only inserted `"WUB"` between words and not inside them, every maximal sequence of non-`"WUB"` characters corresponds exactly to one original word.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)
    
    res = []
    i = 0
    current = []
    
    while i < n:
        if i + 3 <= n and s[i:i+3] == "WUB":
            if current:
                res.append("".join(current))
                current = []
            i += 3
        else:
            current.append(s[i])
            i += 1
    
    if current:
        res.append("".join(current))
    
    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The solution reads the string once and processes it using a single pointer. The key operation is the substring check `s[i:i+3] == "WUB"`, which is constant time due to fixed length. The buffer `current` accumulates characters of the current word and is flushed whenever a delimiter is confirmed.

The implementation avoids repeated string concatenation by using a list for `current`, which ensures linear behavior when joining at the end. The pointer advancement by three positions on encountering `"WUB"` is essential, since failing to skip correctly would reprocess characters and risk incorrect grouping.

## Worked Examples

### Example 1

Input:

```
WUBWUBABCWUB
```

| i | substring | action | current | result |
| --- | --- | --- | --- | --- |
| 0 | WUB | skip, flush empty | [] | [] |
| 3 | WUB | skip, flush empty | [] | [] |
| 6 | ABC | add chars | [A,B,C] | [] |
| 9 | WUB | flush word | [] | [ABC] |

Final output: `ABC`

This trace shows how consecutive delimiters do not produce empty words and only meaningful character sequences are preserved.

### Example 2

Input:

```
WUBWEWUBAREWUBTHEWUBCHAMPIONS
```

| i | substring | action | current | result |
| --- | --- | --- | --- | --- |
| 0 | WUB | skip | [] | [] |
| 3 | WE | build | [W,E] | [] |
| 5 | WUB | flush WE | [] | [WE] |
| 8 | ARE | build | [A,R,E] | [WE] |
| 11 | WUB | flush ARE | [] | [WE, ARE] |
| 14 | THE | build | [T,H,E] | [WE, ARE] |
| 17 | WUB | flush THE | [] | [WE, ARE, THE] |
| 20 | CHAMPIONS | build | [C,H,A,M,P,I,O,N,S] | [WE, ARE, THE] |

Final output:

```
WE ARE THE CHAMPIONS
```

This example demonstrates repeated delimiters between words and confirms that word order is preserved exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once, and each `"WUB"` match is checked in constant time |
| Space | O(n) | Output and temporary buffer store characters of the original words |

The input size is at most 200, so a linear scan is trivially fast. Even if implemented inefficiently, the constraints are forgiving, but the presented solution is both clean and optimal.

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

# provided samples
assert run("WUBWUBABCWUB\n") == "ABC", "sample 1"

# custom cases
assert run("ABC\n") == "ABC", "single word"
assert run("WUBABC\n") == "ABC", "leading WUB"
assert run("ABCWUB\n") == "ABC", "trailing WUB"
assert run("WUBWUB\n") == "", "only separators"
assert run("WUBWEWUBAREWUB\n") == "WE ARE", "multiple words"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"ABC"` | `"ABC"` | No delimiters |
| `"WUBABC"` | `"ABC"` | Leading delimiter |
| `"ABCWUB"` | `"ABC"` | Trailing delimiter |
| `"WUBWUB"` | `""` | Only separators |
| `"WUBWEWUBAREWUB"` | `"WE ARE"` | Multiple word reconstruction |

## Edge Cases

A leading `"WUB"` block such as `"WUBABC"` demonstrates that the algorithm correctly ignores empty buffers at the start. The scan sees the delimiter first, finds no accumulated characters, and simply continues, so no empty word is produced.

A trailing `"WUB"` like `"ABCWUB"` confirms that the final flush logic is correct. The word `"ABC"` is appended before the delimiter is processed, and the final empty buffer is discarded after the loop ends.

A string composed only of `"WUB"` repeats such as `"WUBWUBWUB"` shows that repeated delimiters do not generate phantom words. Each detection triggers a flush only if the buffer contains characters, which it never does in this case, so the output is correctly empty.
