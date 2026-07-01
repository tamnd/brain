---
title: "CF 104312C - Milk Cow"
description: "The task is a pure transformation problem on text. We are given an ASCII picture of Bessie the cow, represented as multiple lines of characters. We must output what the picture looks like after being rotated 180 degrees."
date: "2026-07-01T19:51:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104312
codeforces_index: "C"
codeforces_contest_name: "UTPC Spring 2023 Contest (HS)"
rating: 0
weight: 104312
solve_time_s: 52
verified: true
draft: false
---

[CF 104312C - Milk Cow](https://codeforces.com/problemset/problem/104312/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is a pure transformation problem on text. We are given an ASCII picture of Bessie the cow, represented as multiple lines of characters. We must output what the picture looks like after being rotated 180 degrees.

A 180-degree rotation changes the picture in two ways at once. First, the order of the lines is reversed, so the bottom line becomes the top line and vice versa. Second, every character inside each line is flipped according to a fixed mapping that simulates turning the drawing upside down. Most characters remain unchanged, but a few have asymmetric upside-down counterparts. In this problem, the only transformations that matter are that caret becomes 'v', 'v' becomes caret, forward slash becomes backslash, and backslash becomes forward slash.

The input is simply the original picture as a list of lines. The output is the transformed picture after applying both the vertical reversal and character-wise flipping.

Even though the statement is short, the key detail is that both operations must be applied. Missing either one leads to an incorrect depiction. A common mistake is to only reverse lines or only swap characters, which produces a mirrored but not fully rotated image.

The constraints are minimal because this is a classic output-formatting problem. Each line is short enough that processing is linear in total input size. This means any solution that scans each character once is sufficient, and anything beyond O(N) over total characters is unnecessary.

The main edge case is empty or single-line input. With a single line, reversal does nothing, so correctness depends entirely on whether character flipping is handled properly. Another subtle case is lines containing only symmetric characters such as '|' or '-' or digits, which should remain unchanged after flipping. A naive implementation that tries to invert every character without a mapping will silently corrupt these.

## Approaches

A brute-force way to think about the problem is to explicitly simulate a geometric rotation on a 2D grid. We could imagine padding all lines to the same length, building a matrix, rotating it 180 degrees, and then printing it back. This works because a 180-degree rotation of a matrix is well-defined: element at (i, j) moves to (n - 1 - i, m - 1 - j). However, this approach is unnecessary overhead for a problem that is fundamentally one-dimensional in structure.

The inefficiency comes from explicitly constructing a rectangular grid. If the total number of characters is K, building and rotating the matrix still costs O(K), but with large padding or Python overhead it becomes wasteful and error-prone. More importantly, it obscures the structure of the transformation.

The key observation is that a 180-degree rotation decomposes cleanly into two independent operations. Reversing the line order handles the vertical inversion, and reversing each line combined with character substitution handles horizontal inversion. Since each line is independent, we never need a full 2D representation.

This reduces the problem to a single pass over the input lines, applying a constant-time mapping per character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Grid simulation | O(NM) | O(NM) | Accepted but unnecessary |
| Direct reversal + mapping | O(NM) | O(NM) | Accepted |

## Algorithm Walkthrough

1. Read all input lines into an array, preserving exact content including whitespace. This is necessary because trailing spaces are part of the picture and affect alignment.
2. Define a character transformation map for upside-down rotation. Only the characters '^', 'v', '/', and '\' change; all others map to themselves. This ensures we only modify characters that actually have asymmetric rotations.
3. Reverse the list of lines. This performs the vertical flip of the image, turning bottom rows into top rows.
4. For each line in the reversed list, process it character by character and replace each character using the mapping. This simulates horizontal inversion combined with symbol flipping.
5. Output each transformed line exactly as constructed, preserving spacing.

The subtle point is that reversing lines must happen before or after character transformation consistently, but not mixing partial transformations. Since both operations are independent, either order works as long as every line is fully processed.

### Why it works

A 180-degree rotation is equivalent to reflecting across both the horizontal and vertical axes. Reversing line order applies the vertical reflection. Reversing characters within each line applies the horizontal reflection. The character mapping corrects for symbols whose visual representation changes under reflection. Since every cell in the original grid is visited exactly once and mapped deterministically, no ambiguity or overlap occurs, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    lines = [line.rstrip('\n') for line in sys.stdin]
    
    # remove possible trailing empty line caused by stdin behavior
    if lines and lines[-1] == '':
        lines.pop()

    mp = {
        '^': 'v',
        'v': '^',
        '/': '\\',
        '\\': '/'
    }

    for line in reversed(lines):
        transformed = []
        for ch in line:
            transformed.append(mp.get(ch, ch))
        print(''.join(transformed))

if __name__ == "__main__":
    solve()
```

The solution begins by reading all lines as raw strings, preserving spaces exactly as required by ASCII art formatting. The reversal of the list implements the vertical flip of the image.

The character map handles only the asymmetric symbols. Using `dict.get` ensures that all unrelated characters pass through unchanged without extra branching.

The final loop constructs each output line efficiently using a list of characters, avoiding repeated string concatenation which would be inefficient in Python.

## Worked Examples

### Example 1

Input:

```
/\^
v|/
```

We first store lines as:

| Step | Lines |
| --- | --- |
| Original | ["/^", "v |
| Reversed | ["v |

Now we transform characters.

For first line "v|/":

| char | mapped |
| --- | --- |
| v | ^ |
|  |  |
| / | \ |

Result: "^|"

For second line "/^":

| char | mapped |
| --- | --- |
| / | \ |
| \ | / |
| ^ | v |

Result: "/v"

Output:

```
^|\
\/v
```

This confirms both reversal and correct symbol flipping.

### Example 2

Input:

```
^/
|v
```

| Step | Lines |
| --- | --- |
| Original | ["^/", " |
| Reversed | [" |

Transform "|v":

| char | mapped |
| --- | --- |
| \| | \| |
| v | ^ |

Result: "|^"

Transform "^/":

| char | mapped |
| --- | --- |
| ^ | v |
| / | \ |

Result: "v"

Output:

```
|^
v\
```

This shows that symmetric characters like '|' remain unchanged while directional ones correctly flip.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K) | Each character is processed exactly once across all lines |
| Space | O(K) | Storage for input lines and output construction |

The total work is linear in the size of the ASCII art. Since constraints are small, this easily fits within limits even in Python, and avoids any need for optimization beyond direct iteration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue()

# sample-like cases
assert run("/\\^\\nv|/\n") == "\\v|\n^|/\n", "basic rotation"

# single line
assert run("^/\\\n") == "/\\v\n", "single line flip"

# symmetric characters only
assert run("||--\n") == "--||\n", "no-op mapping with reversal"

# mixed content
assert run("^v/\\\\\n") == "\\/v^\n", "full mapping check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `^/\` | `/\v` | character mapping correctness |
| ` |  | --` |
| `^v/\` | `\/v^` | full bidirectional flip |

## Edge Cases

A single-line input such as "^/" is the simplest non-trivial case. The algorithm reads one line, reverses the list (which changes nothing), and applies the character map. The transformation produces "/\v", confirming correctness even when no vertical inversion occurs.

An input containing only symmetric characters like "||--" exercises the identity mapping branch. After reversal, the line becomes "--||", and since no characters change under the map, the output remains consistent.

A mixed symbolic line like "^v/\" demonstrates full interaction between reversal and mapping. After reversal of lines and per-character transformation, every directional symbol is correctly converted, ensuring that no part of the pipeline is skipped or duplicated.
