---
title: "CF 125B - Simple XML"
description: "The input is a valid XML-like text built from tags of the form <a and </a, where the tag name is a single lowercase letter. Tags can be nested and multiple XML fragments can appear one after another. The task is not to validate the XML. Validity is already guaranteed."
date: "2026-06-02T16:18:01+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 125
codeforces_index: "B"
codeforces_contest_name: "Codeforces Testing Round 2"
rating: 1000
weight: 125
solve_time_s: 106
verified: true
draft: false
---

[CF 125B - Simple XML](https://codeforces.com/problemset/problem/125/B)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a valid XML-like text built from tags of the form `<a>` and `</a>`, where the tag name is a single lowercase letter. Tags can be nested and multiple XML fragments can appear one after another.

The task is not to validate the XML. Validity is already guaranteed. We only need to reformat it.

Each tag must be printed on its own line. The indentation depends on the nesting depth. A tag at depth `h` is preceded by `2 * h` spaces.

For example, in

```
<a><b></b></a>
```

the tag `<a>` is at depth `0`, `<b>` is inside `<a>` so it is at depth `1`, and `</b>` is also printed at depth `1`.

The input length is at most 1000 characters. This is tiny. Even an `O(n²)` solution would fit comfortably, but the structure of the problem naturally leads to a simple linear scan.

The main challenge is handling indentation correctly for closing tags. A common mistake is to print a closing tag using the current depth and only then decrease the depth. Consider:

```
<a></a>
```

Correct output:

```
<a>
</a>
```

If we print `</a>` before decreasing the nesting level, it would incorrectly appear indented by two spaces.

Another subtle case is a closing tag immediately following an opening tag:

```
<a><b></b></a>
```

Correct output:

```
<a>
  <b>
  </b>
</a>
```

The depth for `</b>` is the same as the depth for `<b>`. We must decrease the nesting level before printing the closing tag.

A third case is multiple sibling elements:

```
<a></a><b></b>
```

Correct output:

```
<a>
</a>
<b>
</b>
```

After finishing one element, the nesting level must return to its previous value so that the next sibling starts at the correct indentation.

## Approaches

A brute-force way to solve the problem is to repeatedly locate the next tag, determine its nesting level by examining all previously processed tags, and then print it. Such an approach recomputes depth information many times. With a string of length `n`, that can lead to `O(n²)` work.

The input size is small enough that even this would pass, but there is a much cleaner solution.

The key observation is that the nesting depth changes only when we encounter tags.

An opening tag increases the depth for everything inside it. A closing tag ends the current nested region and decreases the depth.

This means we can process the XML text from left to right exactly once. Whenever we encounter a tag, we determine whether it is opening or closing.

For an opening tag:

```
<a>
```

we print it using the current depth, then increase the depth.

For a closing tag:

```
</a>
```

we first decrease the depth, then print it.

That single rule automatically produces the correct indentation for every valid XML structure.

Because each character is examined only once while extracting tags, the solution runs in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted but unnecessary |
| Optimal | O(n) | O(n) | Accepted |

The `O(n)` auxiliary space comes from storing the output lines before printing them.

## Algorithm Walkthrough

1. Read the XML string.
2. Scan the string from left to right.
3. Whenever a `<` is found, continue until the matching `>` to extract the complete tag.
4. Check whether the tag is a closing tag. A closing tag starts with `</`.
5. If the tag is a closing tag, decrease the current depth by one before printing it. The element being closed belongs to the parent level, not to the level inside itself.
6. Print the tag preceded by `2 × depth` spaces.
7. If the tag is an opening tag, increase the depth by one after printing it. Everything inside that element is one level deeper.
8. Continue until the entire string has been processed.

### Why it works

Maintain the invariant that `depth` always equals the number of currently open tags whose closing tags have not yet been processed.

Before an opening tag is printed, it belongs to the current nesting level, so printing with the current depth is correct. After printing it, that tag becomes active, so the depth increases by one.

Before a closing tag is printed, the corresponding element is no longer considered active. Decreasing the depth first restores the nesting level of the parent element. Printing with this updated depth gives exactly the indentation required by the statement.

Since every tag updates the depth according to the XML nesting rules, every line is printed at its correct level.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    depth = 0
    lines = []

    i = 0
    n = len(s)

    while i < n:
        j = i
        while s[j] != '>':
            j += 1

        tag = s[i:j + 1]

        if tag.startswith("</"):
            depth -= 1
            lines.append("  " * depth + tag)
        else:
            lines.append("  " * depth + tag)
            depth += 1

        i = j + 1

    sys.stdout.write("\n".join(lines))

if __name__ == "__main__":
    solve()
```

The scan uses two pointers. `i` marks the beginning of the current tag, and `j` advances until the matching `>` is found.

The order of operations for closing tags is the most important detail in the implementation. The depth must be decreased before generating indentation. Reversing those two operations shifts every closing tag one level too far to the right.

For opening tags, the opposite order is required. The tag itself belongs to the current level, so it is printed first and only then increases the nesting depth for its contents.

The input is guaranteed to contain only valid XML text, so no stack or validation logic is needed.

## Worked Examples

### Example 1

Input:

```
<a><b><c></c></b></a>
```

| Tag | Closing? | Depth Before | Depth Used | Depth After |
| --- | --- | --- | --- | --- |
| `<a>` | No | 0 | 0 | 1 |
| `<b>` | No | 1 | 1 | 2 |
| `<c>` | No | 2 | 2 | 3 |
| `</c>` | Yes | 3 | 2 | 2 |
| `</b>` | Yes | 2 | 1 | 1 |
| `</a>` | Yes | 1 | 0 | 0 |

Output:

```
<a>
  <b>
    <c>
    </c>
  </b>
</a>
```

This trace shows the central invariant. Opening tags print at the current depth and then increase it. Closing tags decrease first and then print.

### Example 2

Input:

```
<a></a><b></b>
```

| Tag | Closing? | Depth Before | Depth Used | Depth After |
| --- | --- | --- | --- | --- |
| `<a>` | No | 0 | 0 | 1 |
| `</a>` | Yes | 1 | 0 | 0 |
| `<b>` | No | 0 | 0 | 1 |
| `</b>` | Yes | 1 | 0 | 0 |

Output:

```
<a>
</a>
<b>
</b>
```

This example demonstrates sibling elements. After one element closes, the depth returns to its previous value, so the next sibling starts with the correct indentation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited a constant number of times |
| Space | O(n) | Output lines are stored before printing |

With a maximum input length of only 1000 characters, the linear solution runs essentially instantly and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    s = inp.strip()

    depth = 0
    lines = []

    i = 0
    while i < len(s):
        j = i
        while s[j] != '>':
            j += 1

        tag = s[i:j + 1]

        if tag.startswith("</"):
            depth -= 1
            lines.append("  " * depth + tag)
        else:
            lines.append("  " * depth + tag)
            depth += 1

        i = j + 1

    return "\n".join(lines)

# provided sample
assert run("<a><b><c></c></b></a>") == (
    "<a>\n"
    "  <b>\n"
    "    <c>\n"
    "    </c>\n"
    "  </b>\n"
    "</a>"
), "sample 1"

# minimum valid non-empty XML
assert run("<a></a>") == (
    "<a>\n"
    "</a>"
), "single element"

# siblings
assert run("<a></a><b></b>") == (
    "<a>\n"
    "</a>\n"
    "<b>\n"
    "</b>"
), "siblings"

# deeper nesting
assert run("<a><b></b></a>") == (
    "<a>\n"
    "  <b>\n"
    "  </b>\n"
    "</a>"
), "nested pair"

# mixed nesting and siblings
assert run("<a><b></b><c></c></a>") == (
    "<a>\n"
    "  <b>\n"
    "  </b>\n"
    "  <c>\n"
    "  </c>\n"
    "</a>"
), "multiple children"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `<a></a>` | Two lines without indentation | Smallest non-empty XML |
| `<a></a><b></b>` | Two sibling elements | Depth reset after closing |
| `<a><b></b></a>` | One nested child | Correct indentation of closing tags |
| `<a><b></b><c></c></a>` | Two children inside parent | Mixing nesting and siblings |

## Edge Cases

Consider the smallest valid XML:

```
<a></a>
```

Processing `<a>` prints it at depth `0` and increases depth to `1`. When `</a>` is reached, the algorithm decreases depth back to `0` before printing. The output becomes:

```
<a>
</a>
```

which is exactly correct.

Consider immediate nesting:

```
<a><b></b></a>
```

After printing `<b>`, the depth becomes `2`. When `</b>` appears, the algorithm first decreases the depth to `1` and then prints. The output is:

```
<a>
  <b>
  </b>
</a>
```

If the decrement happened after printing, `</b>` would incorrectly receive four spaces.

Consider sibling elements:

```
<a></a><b></b>
```

After `</a>` is processed, the depth returns to `0`. The next tag `<b>` is printed with no indentation. The output is:

```
<a>
</a>
<b>
</b>
```

This confirms that closing a subtree completely restores the parent's nesting level before processing subsequent elements.
