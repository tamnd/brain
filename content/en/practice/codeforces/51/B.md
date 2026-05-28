---
title: "CF 51B - bHTML Tables Analisys"
description: "We are given a string that represents a simplified HTML table language. The language contains only three kinds of tags: <table>, <tr>, and <td>, together with their matching closing tags."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "expression-parsing"]
categories: ["algorithms"]
codeforces_contest: 51
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 48"
rating: 1700
weight: 51
solve_time_s: 217
verified: true
draft: false
---
[CF 51B - bHTML Tables Analisys](https://codeforces.com/problemset/problem/51/B)

**Rating:** 1700  
**Tags:** expression parsing  
**Solve time:** 3m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string that represents a simplified HTML table language. The language contains only three kinds of tags: `<table>`, `<tr>`, and `<td>`, together with their matching closing tags. A table contains rows, each row contains cells, and a cell is either empty or contains another complete table.

The task is to find the number of direct cells inside every table that appears in the document, including nested tables. For each table, we count how many `<td>...</td>` elements belong directly to that table, not to tables nested inside its cells. After collecting all counts, we print them in non-decreasing order.

The input length is at most 5000 characters. That is small enough for linear or quadratic algorithms, but recursive reparsing of large substrings can still become expensive if implemented carelessly. A cubic parser would already be dangerous because 5000³ operations are far beyond the time limit. A clean single pass parser with a stack easily fits within the constraints.

The grammar guarantees that the input is valid, so we never need to recover from malformed tags. Every opening tag has a matching closing tag, and nesting is always correct.

A subtle part of the problem is distinguishing between direct cells and cells belonging to nested tables.

Consider this input:

```
<table><tr><td><table><tr><td></td></tr></table></td></tr></table>
```

The outer table has exactly one cell, even though another cell exists inside the nested table. The correct output is:

```
1 1
```

A naive counter that simply counts all `<td>` tags inside a table range would incorrectly report `2` for the outer table.

Another easy mistake is forgetting that tables are not necessarily rectangular.

Example:

```
<table><tr><td></td><td></td></tr><tr><td></td></tr></table>
```

This table has three cells total, not four. The rows may have different lengths.

A third pitfall is processing the input line by line instead of concatenating all lines first. The statement explicitly allows arbitrary line breaks.

For example:

```
<table><tr>
<td></td>
</tr></table>
```

These lines together form a single valid string. Treating lines independently would break the parser.

## Approaches

The most straightforward approach is to parse every table independently. Whenever we encounter a `<table>`, we search for its matching `</table>`, extract that substring, and count how many direct `<td>` tags belong to it. To avoid counting nested tables' cells, we would need another nesting counter while scanning the substring.

This works logically, but it repeats work many times. In the worst case, deeply nested tables force us to rescan almost the entire remaining string for every table. If the nesting depth is `n`, the total work becomes roughly:

```
n + (n - 1) + (n - 2) + ...
```

which is quadratic.

With length 5000, even `O(n²)` probably passes, but the implementation becomes messy because we repeatedly search for matching tags and repeatedly traverse the same regions.

The structure of the grammar gives us a cleaner idea. Every tag appears in properly nested order, exactly like parentheses. That means we can process the string once from left to right using a stack.

The key observation is that a table's cell count becomes known exactly when we close that table. Every direct `<td>` encountered while the table is active belongs to it. Nested tables do not interfere because they are handled by deeper stack levels.

So instead of reparsing substrings, we maintain a stack of currently open tables. When we see `<table>`, we create a new counter. When we see `<td>`, we increment the counter of the current table. When we see `</table>`, we finalize that table and store its count.

This turns the problem into a simple linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted but inefficient |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all input lines and concatenate them into one string.

The grammar ignores line boundaries, so the parser must operate on the combined string.
2. Scan the string from left to right.

Every meaningful token is a complete tag such as `<table>` or `</td>`. Since the tag set is tiny and fixed, we can identify tags using string prefix checks.
3. Maintain a stack where each element stores the current number of direct cells for an open table.

The top of the stack always represents the table we are currently inside.
4. When encountering `<table>`, push `0` onto the stack.

A new table starts with zero cells counted so far.
5. When encountering `<td>`, increment the top element of the stack.

Every `<td>` belongs directly to the currently active table. Even if this cell later contains another table, it is still one direct cell of the current table.
6. Ignore `<tr>`, `</tr>`, and `</td>`.

They affect structure validity but do not change cell counts.
7. When encountering `</table>`, pop the top value from the stack and append it to the answer list.

At this moment, the table is fully processed, so its direct cell count is final.
8. After finishing the scan, sort the collected counts.
9. Print the counts separated by spaces.

### Why it works

At any position during the scan, the stack exactly represents the chain of currently open tables from outermost to innermost. Every `<td>` tag belongs to the innermost open table because the grammar allows cells only inside rows of the current table. Nested tables create new stack levels, so their cells never affect parent counters. When `</table>` appears, all content of that table has already been processed, meaning the stored counter is complete and correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = "".join(line.strip() for line in sys.stdin)

    stack = []
    ans = []

    i = 0
    n = len(s)

    while i < n:
        if s.startswith("<table>", i):
            stack.append(0)
            i += 7

        elif s.startswith("</table>", i):
            ans.append(stack.pop())
            i += 8

        elif s.startswith("<td>", i):
            stack[-1] += 1
            i += 4

        elif s.startswith("</td>", i):
            i += 5

        elif s.startswith("<tr>", i):
            i += 4

        elif s.startswith("</tr>", i):
            i += 5

    ans.sort()
    print(*ans)

if __name__ == "__main__":
    solve()
```

The first step concatenates all input lines into one continuous string. Using `strip()` removes newline characters while preserving the actual markup.

The parser works with a single index `i`. Since every valid token has fixed length, we can advance the pointer immediately after matching a tag.

The stack stores one integer per open table. When a new table starts, we push `0`. Every `<td>` increments only the top element because direct ownership always belongs to the current table.

The order of conditions matters slightly because `<table>` and `</table>` share prefixes. Checking opening tags before closing tags keeps matching unambiguous.

We ignore row tags entirely because they do not affect the required answer. Their only role is enforcing grammar validity, which the statement already guarantees.

When a table closes, its counter is complete, so we pop it and save it into `ans`.

Finally, sorting produces the required non-decreasing order.

## Worked Examples

### Example 1

Input:

```
<table><tr><td></td></tr></table>
```

Trace:

| Position | Tag | Stack Before | Action | Stack After | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | `<table>` | `[]` | push 0 | `[0]` | `[]` |
| 7 | `<tr>` | `[0]` | ignore | `[0]` | `[]` |
| 11 | `<td>` | `[0]` | increment top | `[1]` | `[]` |
| 15 | `</td>` | `[1]` | ignore | `[1]` | `[]` |
| 20 | `</tr>` | `[1]` | ignore | `[1]` | `[]` |
| 25 | `</table>` | `[1]` | pop to answer | `[]` | `[1]` |

Sorted result:

```
1
```

This example confirms the basic invariant that every `<td>` increments the currently open table exactly once.

### Example 2

Input:

```
<table><tr><td><table><tr><td></td><td></td></tr></table></td></tr></table>
```

Trace:

| Position | Tag | Stack Before | Action | Stack After | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | `<table>` | `[]` | push 0 | `[0]` | `[]` |
| 11 | `<td>` | `[0]` | increment top | `[1]` | `[]` |
| 15 | `<table>` | `[1]` | push 0 | `[1, 0]` | `[]` |
| 26 | `<td>` | `[1, 0]` | increment top | `[1, 1]` | `[]` |
| 35 | `<td>` | `[1, 1]` | increment top | `[1, 2]` | `[]` |
| 53 | `</table>` | `[1, 2]` | pop to answer | `[1]` | `[2]` |
| 72 | `</table>` | `[1]` | pop to answer | `[]` | `[2, 1]` |

Sorted result:

```
1 2
```

This trace demonstrates why nested tables require a stack. The inner table's cells affect only the inner counter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each character is processed once through fixed-length tag checks |
| Space | O(n) | stack depth can reach the nesting depth of tables |

The input length is at most 5000, so a linear scan is extremely fast. Memory usage is also tiny because even maximal nesting requires only one integer per open table.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = "".join(line.strip() for line in sys.stdin)

    stack = []
    ans = []

    i = 0
    n = len(s)

    while i < n:
        if s.startswith("<table>", i):
            stack.append(0)
            i += 7

        elif s.startswith("</table>", i):
            ans.append(stack.pop())
            i += 8

        elif s.startswith("<td>", i):
            stack[-1] += 1
            i += 4

        elif s.startswith("</td>", i):
            i += 5

        elif s.startswith("<tr>", i):
            i += 4

        elif s.startswith("</tr>", i):
            i += 5

    ans.sort()
    print(*ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("<table><tr><td></td></tr></table>\n") == "1", "sample 1"

# nested table
assert run(
    "<table><tr><td><table><tr><td></td></tr></table></td></tr></table>\n"
) == "1 1", "nested table"

# non-rectangular rows
assert run(
    "<table><tr><td></td><td></td></tr><tr><td></td></tr></table>\n"
) == "3", "different row sizes"

# multiple nesting levels
assert run(
    "<table><tr><td><table><tr><td><table><tr><td></td></tr></table></td></tr></table></td></tr></table>\n"
) == "1 1 1", "deep nesting"

# multiline input
assert run(
    "<table><tr>\n<td></td>\n</tr></table>\n"
) == "1", "line concatenation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single empty cell table | `1` | minimum valid structure |
| Nested table inside one cell | `1 1` | nested counts stay separate |
| Uneven row lengths | `3` | tables are not rectangular |
| Deep recursive nesting | `1 1 1` | stack handling of recursion |
| Input split across lines | `1` | correct concatenation of lines |

## Edge Cases

Consider the nested-table case again:

```
<table><tr><td><table><tr><td></td></tr></table></td></tr></table>
```

Execution begins with the outer table counter `[0]`. The first `<td>` changes it to `[1]`. When the inner table starts, the stack becomes `[1, 0]`. The inner `<td>` increments only the top level, producing `[1, 1]`. After closing the inner table, the answer list contains `[1]`, and the outer counter remains unchanged. Closing the outer table adds another `1`. The final sorted output is:

```
1 1
```

This confirms that nested cells never leak into parent counts.

Now consider a non-rectangular table:

```
<table><tr><td></td><td></td></tr><tr><td></td></tr></table>
```

The parser encounters three `<td>` tags while the same table is active, so its counter evolves as:

```
0 -> 1 -> 2 -> 3
```

Rows do not matter for counting. The final output is:

```
3
```

This avoids the common mistake of assuming all rows have equal width.

Finally, consider multiline input:

```
<table><tr>
<td></td>
</tr></table>
```

The algorithm first concatenates all stripped lines into:

```
<table><tr><td></td></tr></table>
```

After that, parsing proceeds normally and produces:

```
1
```

Without concatenation, the parser would incorrectly treat newline boundaries as meaningful structure.
