---
title: "CF 125B - Simple XML"
description: "We are given a string that represents a valid XML-like structure. Every tag is either an opening tag like <a or a closing tag like </a, where the tag name is a single lowercase letter."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 125
codeforces_index: "B"
codeforces_contest_name: "Codeforces Testing Round 2"
rating: 1000
weight: 125
solve_time_s: 101
verified: true
draft: false
---

[CF 125B - Simple XML](https://codeforces.com/problemset/problem/125/B)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string that represents a valid XML-like structure. Every tag is either an opening tag like `<a>` or a closing tag like `</a>`, where the tag name is a single lowercase letter.

The string is guaranteed to be valid, which means every opening tag has a matching closing tag, and nesting is properly balanced. Our job is not to validate the structure, only to print it in a readable indented format.

Each tag must appear on its own line. The indentation depends on how deeply nested the tag is. If a tag is inside one other tag, it gets two leading spaces. If it is inside two tags, it gets four spaces, and so on.

The input length is at most 1000 characters, which is very small. Even an $O(n^2)$ solution would pass comfortably, since $1000^2 = 10^6$ operations is trivial for a 2-second limit. Still, the structure of the problem naturally leads to a linear scan, and that is the cleanest solution.

The tricky part is handling indentation correctly for closing tags. An opening tag increases the nesting depth after it is printed, while a closing tag decreases the nesting depth before it is printed.

Consider this example:

```
<a></a>
```

The correct output is:

```
<a>
</a>
```

A careless implementation might print the closing tag with one indentation level because it forgets to decrease the depth first.

Another easy mistake appears with sibling tags:

```
<a><b></b><c></c></a>
```

The correct output is:

```
<a>
  <b>
  </b>
  <c>
  </c>
</a>
```

If we fail to reduce the nesting level after `</b>`, then `<c>` would be printed too deeply.

A final subtle case is an empty XML-text inside a tag:

```
<a></a>
```

There are no inner tags, so the opening and closing tags must align at the same indentation level. This only works if the depth update order is correct.

## Approaches

The most direct brute-force idea is to repeatedly search for the next tag, determine its nesting depth by examining all previous tags, and then print it with the corresponding indentation.

For every tag, we could scan the entire prefix of the string and count how many unmatched opening tags exist before it. Since there are $O(n)$ tags and each computation may scan $O(n)$ characters, the total complexity becomes $O(n^2)$.

This works because the nesting depth at any point is exactly the number of currently open tags. The problem is not correctness, the problem is unnecessary repeated work. Every time we compute the depth from scratch, we reprocess information we already knew from the previous tag.

The key observation is that the XML text is naturally processed from left to right. While scanning the string once, we always know the current nesting depth. Opening tags increase it, closing tags decrease it.

This transforms the problem into a simple state machine:

- Read one complete tag.
- Decide whether it is opening or closing.
- Print it using the current depth.
- Update the depth appropriately.

Because each character is processed once, the complexity becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the XML string.
2. Scan the string from left to right using an index `i`.
3. Whenever we encounter `<`, continue moving forward until reaching the matching `>`. The substring between these positions is one complete tag.
4. Check whether the tag is a closing tag. A closing tag starts with `</`.
5. If the tag is a closing tag, decrease the current depth before printing.

This is necessary because the closing tag belongs to the parent level, not the child level.
6. Print the tag with `2 * depth` leading spaces.
7. If the tag is an opening tag, increase the depth after printing.

Any future tags inside this element must appear one level deeper.
8. Continue until the entire string has been processed.

### Why it works

The algorithm maintains one invariant throughout the scan:

`depth` always equals the number of currently open tags before processing the next tag.

For an opening tag, the tag itself belongs to the current depth, and only its children belong deeper, so we print first and increment afterward.

For a closing tag, the corresponding opening tag is no longer active at this level, so we decrement first and then print.

Because the input is guaranteed valid, the depth never becomes negative and always returns to zero at the end.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    depth = 0
    i = 0
    ans = []

    while i < len(s):
        j = i
        while s[j] != '>':
            j += 1

        tag = s[i:j + 1]

        if tag[1] == '/':
            depth -= 1

        ans.append('  ' * depth + tag)

        if tag[1] != '/':
            depth += 1

        i = j + 1

    print('\n'.join(ans))

solve()
```

The solution keeps a single variable `depth`, which tracks the current nesting level.

The outer loop walks through the string. Since every meaningful token is enclosed by `<` and `>`, we extract tags by expanding `j` until we reach the next `>` character.

The order of operations around `depth` is the most important detail in the implementation.

For closing tags:

```
if tag[1] == '/':
    depth -= 1
```

This happens before printing because the closing tag belongs to the outer level.

For opening tags:

```
if tag[1] != '/':
    depth += 1
```

This happens after printing because only nested content should move deeper.

Another subtle implementation choice is:

```
tag[1] == '/'
```

The first character is always `<`, so checking the second character cleanly distinguishes between `<a>` and `</a>`.

The algorithm never needs a stack because the problem guarantees valid XML nesting. We only need the current depth count.

## Worked Examples

### Example 1

Input:

```
<a><b><c></c></b></a>
```

| Step | Tag | Depth Before | Printed Line | Depth After |
| --- | --- | --- | --- | --- |
| 1 | `<a>` | 0 | `<a>` | 1 |
| 2 | `<b>` | 1 | `  <b>` | 2 |
| 3 | `<c>` | 2 | `    <c>` | 3 |
| 4 | `</c>` | 3 | `    </c>` | 2 |
| 5 | `</b>` | 2 | `  </b>` | 1 |
| 6 | `</a>` | 1 | `</a>` | 0 |

This trace shows the central invariant of the algorithm. Opening tags increase depth only after printing, while closing tags decrease depth before printing. That keeps matching opening and closing tags aligned.

### Example 2

Input:

```
<a><b></b><c></c></a>
```

| Step | Tag | Depth Before | Printed Line | Depth After |
| --- | --- | --- | --- | --- |
| 1 | `<a>` | 0 | `<a>` | 1 |
| 2 | `<b>` | 1 | `  <b>` | 2 |
| 3 | `</b>` | 2 | `  </b>` | 1 |
| 4 | `<c>` | 1 | `  <c>` | 2 |
| 5 | `</c>` | 2 | `  </c>` | 1 |
| 6 | `</a>` | 1 | `</a>` | 0 |

This example demonstrates sibling tags. After finishing `</b>`, the depth returns to 1, so `<c>` is printed at the same indentation level as `<b>`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is scanned once |
| Space | O(n) | Output storage |

The input length is at most 1000, so the solution easily fits within the limits. Even quadratic approaches would pass, but the linear scan is simpler and cleaner.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    s = input().strip()

    depth = 0
    i = 0
    ans = []

    while i < len(s):
        j = i
        while s[j] != '>':
            j += 1

        tag = s[i:j + 1]

        if tag[1] == '/':
            depth -= 1

        ans.append('  ' * depth + tag)

        if tag[1] != '/':
            depth += 1

        i = j + 1

    return '\n'.join(ans) + '\n'

# provided sample
assert run("<a><b><c></c></b></a>\n") == (
    "<a>\n"
    "  <b>\n"
    "    <c>\n"
    "    </c>\n"
    "  </b>\n"
    "</a>\n"
), "sample 1"

# minimum valid structure
assert run("<a></a>\n") == (
    "<a>\n"
    "</a>\n"
), "single tag pair"

# sibling tags
assert run("<a><b></b><c></c></a>\n") == (
    "<a>\n"
    "  <b>\n"
    "  </b>\n"
    "  <c>\n"
    "  </c>\n"
    "</a>\n"
), "siblings"

# deeper nesting
assert run("<a><b><c><d></d></c></b></a>\n") == (
    "<a>\n"
    "  <b>\n"
    "    <c>\n"
    "      <d>\n"
    "      </d>\n"
    "    </c>\n"
    "  </b>\n"
    "</a>\n"
), "deep nesting"

# repeated same tag names
assert run("<a><a></a></a>\n") == (
    "<a>\n"
    "  <a>\n"
    "  </a>\n"
    "</a>\n"
), "same tag names"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `<a></a>` | Two aligned lines | Correct handling of empty content |
| `<a><b></b><c></c></a>` | Sibling tags align equally | Proper depth restoration |
| `<a><b><c><d></d></c></b></a>` | Four nesting levels | Deep indentation correctness |
| `<a><a></a></a>` | Nested identical tags | Tag names do not affect logic |

## Edge Cases

### Empty inner XML

Input:

```
<a></a>
```

Execution:

- `<a>` is printed at depth 0, then depth becomes 1.
- `</a>` decreases depth back to 0 before printing.

Output:

```
<a>
</a>
```

If we decreased depth after printing the closing tag, the output would incorrectly become:

```
<a>
  </a>
```

### Sibling structures

Input:

```
<a><b></b><c></c></a>
```

After processing `</b>`, the depth returns from 2 to 1. This is why `<c>` appears at the same indentation level as `<b>`.

Correct output:

```
<a>
  <b>
  </b>
  <c>
  </c>
</a>
```

This confirms that closing tags must update the depth before printing.

### Deep nesting

Input:

```
<a><b><c></c></b></a>
```

The depth evolves as:

```
0 -> 1 -> 2 -> 3 -> 2 -> 1 -> 0
```

Every opening tag increases nesting only for future tags, and every closing tag restores the previous level before output. Matching opening and closing tags end up perfectly aligned.
