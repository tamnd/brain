---
title: "CF 105937B - Nobody Can Log In"
description: "We are given several login passwords, one per team, and each password is just a string composed of printable characters like digits, uppercase and lowercase letters, underscores, and hyphens."
date: "2026-06-21T22:16:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105937
codeforces_index: "B"
codeforces_contest_name: "2025 Xian Jiaotong University Programming Contest"
rating: 0
weight: 105937
solve_time_s: 50
verified: true
draft: false
---

[CF 105937B - Nobody Can Log In](https://codeforces.com/problemset/problem/105937/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several login passwords, one per team, and each password is just a string composed of printable characters like digits, uppercase and lowercase letters, underscores, and hyphens. The system has decided that four characters are too confusing for humans during login: the digit `1`, lowercase `i`, uppercase `I`, and lowercase `l`. For every password, we must produce a cleaned version by removing every occurrence of these four characters, keeping all other characters in their original order.

The input size constraint is the key structural detail here. There are up to 50,000 characters in total across all strings, so any solution that processes each character a constant number of times is fine. However, anything that repeatedly rebuilds strings inefficiently, such as repeated concatenation inside loops without buffering, risks quadratic behavior in Python due to immutability of strings.

Edge cases are simple but still worth being explicit about.

A password may consist entirely of removable characters. For example, input `1iIl` should produce an empty line as output. A naive mistake here is forgetting to print an empty line at all, which would shift output alignment.

Another edge case is when no characters are removed, such as `abcXYZ_9-`. The output must match exactly.

A third subtle case is large inputs where removed characters are interspersed, like `1a1b1c1d1e`, where we must preserve only the letters.

## Approaches

The brute-force idea is straightforward: for each string, scan character by character and build a new string by appending only allowed characters. If implemented correctly with a list buffer per string, this is already optimal. The only danger is doing repeated string concatenation like `res += c`, which makes each append O(length of current result), leading to quadratic time per string in the worst case. With total length 5 × 10^4, that would still pass, but only barely, and it is unnecessary to risk performance issues in Python under tighter limits.

The key observation is that the operation is purely a filter over characters with no dependencies between positions. Each character is independently either kept or discarded. This means we can process the stream once, accumulate results in a list, and join once per string.

So the optimal solution is simply a linear scan with a constant-time membership check against a small forbidden set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (string concatenation) | O(n²) worst-case per string | O(n) | Risky / borderline |
| Optimal (list filtering) | O(n) total | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of passwords and process each string independently. Each string can be handled in isolation because there is no interaction between test cases.
2. Define the forbidden set `{ '1', 'i', 'I', 'l' }`. We use a set because membership checking is O(1) average time.
3. For each string, create an empty list to collect characters that should remain. We avoid building a string directly to prevent repeated reallocation cost.
4. Iterate through each character of the string. For each character, check whether it belongs to the forbidden set. If it does not, append it to the list.
5. After processing the entire string, join the list into a single string and output it. If the list is empty, the join naturally produces an empty string, so we still print a newline.

### Why it works

Each position in the string is processed exactly once, and the decision at that position depends only on whether the character is in the forbidden set. There is no transformation that depends on neighboring characters or future context. This makes the algorithm equivalent to applying a projection function over a sequence, where the output sequence preserves order but filters elements independently. Because every character is considered exactly once and either preserved or discarded immediately, the final constructed string is exactly the original string minus all forbidden symbols.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    banned = {'1', 'i', 'I', 'l'}

    out_lines = []

    for _ in range(n):
        s = input().strip()
        buf = []

        for ch in s:
            if ch not in banned:
                buf.append(ch)

        out_lines.append(''.join(buf))

    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    main()
```

The solution reads input line by line and processes each password independently. The `banned` set is precomputed once so membership checks remain constant time. Each character is appended into a list rather than concatenating strings directly, which avoids repeated copying of intermediate strings.

The final output is assembled using a single `join` over all processed lines, ensuring efficient output construction even when many test cases are present.

A subtle point is stripping newline characters on input. Since passwords do not include spaces but may include other symbols, `strip()` safely removes only trailing newline characters without affecting valid content.

## Worked Examples

### Example 1

Input:

```
3
mCj_m3sYshA
1liil1ili
Ave_mujica
```

Processing each string:

| String | Characters processed | Output buffer |
| --- | --- | --- |
| mCj_m3sYshA | keep all | mCj_m3sYshA |
| 1liil1ili | all removed | empty |
| Ave_mujica | remove i | Ave_mujca |

Final output:

```
mCj_m3sYshA

Ave_mujca
```

This confirms that the algorithm correctly handles both full retention and full deletion cases.

### Example 2

Input:

```
2
-joF4
Oblivionis
```

| String | Characters processed | Output buffer |
| --- | --- | --- |
| -joF4 | keep all | -joF4 |
| Oblivionis | remove l, i, i | Obvons |

Output:

```
-joF4
Obvons
```

This shows that filtering preserves order and removes only forbidden characters, even when they appear multiple times.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length of all strings) | Each character is checked once against a constant-size set |
| Space | O(total length of output) | We store filtered characters before joining |

The total input size is at most 5 × 10^4 characters, so a single linear pass over all data is easily within limits. Memory usage is also proportional to output size, which is unavoidable since output must be constructed anyway.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    banned = {'1', 'i', 'I', 'l'}

    out = []
    for _ in range(n):
        s = input().strip()
        buf = []
        for ch in s:
            if ch not in banned:
                buf.append(ch)
        out.append(''.join(buf))

    return '\n'.join(out)

# provided-style sample
assert run("""3
mCj_m3sYshA
1liil1ili
Ave_mujica
""") == "mCj_m3sYshA\n\nAve_mujca"

# all removed
assert run("""1
1iIl
""") == "\n"

# no removals
assert run("""1
abcXYZ_9-
""") == "abcXYZ_9-"

# mixed pattern
assert run("""1
1a1b1c1d
""") == "abcd"

# large repeated pattern
assert run("""1
""" + "1iIlabc"*10000) == "abc"*10000
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1iIl` | empty line | full deletion edge case |
| `abcXYZ_9-` | same string | no-removal case |
| `1a1b1c1d` | `abcd` | alternating filtering correctness |
| repeated pattern | repeated cleaned output | performance and linear behavior |

## Edge Cases

For a fully forbidden string like `1iIl`, the algorithm iterates through each character, finds all are in the banned set, and appends nothing. The buffer remains empty and joining produces an empty string, which is still printed correctly as a blank line.

For a string with no forbidden characters such as `abcXYZ`, every membership check fails, so every character is appended. The output buffer matches the input exactly, preserving order without modification.

For alternating patterns like `1a1b1c`, each character is independently checked. The forbidden digits are skipped while letters are appended. The resulting buffer grows only on valid characters, confirming that the algorithm does not depend on position or grouping.

For large repetitive inputs, each character is still processed once, and the constant-time set membership ensures the total runtime scales linearly with input size.
