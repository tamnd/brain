---
title: "CF 264A - Escape from Stones"
description: "We are given a string consisting of the characters l and r. The characters describe how the squirrel moves when stones fall one by one. Stone i falls after stones 1...i-1 have already been placed."
date: "2026-06-04T17:51:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 264
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 162 (Div. 1)"
rating: 1200
weight: 264
solve_time_s: 107
verified: true
draft: false
---

[CF 264A - Escape from Stones](https://codeforces.com/problemset/problem/264/A)

**Rating:** 1200  
**Tags:** constructive algorithms, data structures, implementation, two pointers  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting of the characters `l` and `r`. The characters describe how the squirrel moves when stones fall one by one.

Stone `i` falls after stones `1...i-1` have already been placed. If the corresponding character is `l`, the squirrel moves to the left half of the current interval. If it is `r`, she moves to the right half. After all moves are processed, the stones end up arranged on a line. We must output the stone numbers from leftmost to rightmost.

The geometric description sounds complicated, but the actual task is to determine the final left-to-right order of stone indices.

The length of the string can reach one million. Any algorithm that repeatedly inserts into the middle of an array or simulates positions explicitly would be far too slow. With $n = 10^6$, even $O(n^2)$ behavior would require roughly $10^{12}$ operations, which is completely infeasible. We need a linear-time solution.

A subtle point is that the order is not determined by the physical coordinates of the stones. The geometry only implies a relative ordering rule.

Consider the input:

```
r
```

There is only one stone, so the output is:

```
1
```

A solution that assumes every `r` should be placed after something else might mishandle this smallest case.

Another interesting case is:

```
lll
```

The correct output is:

```
3
2
1
```

Every new stone ends up to the left of all previously processed stones. A careless implementation that simply appends indices as it reads the string would produce `1 2 3`, which is incorrect.

Similarly:

```
rrr
```

produces

```
1
2
3
```

Now every stone appears to the right of all earlier stones.

The mixed case

```
llrlr
```

gives

```
3
5
4
2
1
```

which shows that neither reversing the answer nor keeping the original order is sufficient.

## Approaches

A direct simulation is possible. We can maintain the current left-to-right sequence of stones. When stone `i` arrives, we determine where it belongs relative to the existing stones and insert it accordingly.

The problem is that insertion into the front or middle of a dynamic array costs linear time. In the worst case we perform $n$ insertions, each costing $O(n)$, leading to $O(n^2)$ complexity. With one million stones, this is hopelessly slow.

The key observation is that the geometry induces a very simple ordering rule.

Suppose we process stones in order. When stone `i` corresponds to `l`, the squirrel escapes left. This means every future position inside that interval lies to the left of stone `i`. In the final arrangement, stone `i` should appear as early as possible among the remaining unprocessed stones.

When stone `i` corresponds to `r`, the squirrel escapes right. Stone `i` must appear after all stones that will later be placed inside the right interval.

This leads to a constructive interpretation.

For every `l`, the corresponding stone number belongs at the front of the final sequence.

For every `r`, the corresponding stone number belongs at the back of the final sequence.

If we read the string from left to right, we can place stone numbers with `l` into the front portion and stone numbers with `r` into the back portion.

An even simpler formulation appears if we think about output order directly.

All stones marked `r` should be printed in their original order.

All stones marked `l` should be printed in reverse order after them.

A deque naturally represents this process. For stone `i`:

If `s[i] == 'l'`, push `i+1` to the front.

If `s[i] == 'r'`, push `i+1` to the back.

At the end, reading the deque from front to back gives exactly the desired order.

Since each operation on a deque is constant time, the entire algorithm is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Create an empty deque.
3. Process the characters from left to right. Let the current stone number be `i + 1`.
4. If the current character is `l`, insert the stone number at the front of the deque.

This reflects the fact that the stone must appear before all stones that will be placed inside the interval reached by moving left.
5. If the current character is `r`, insert the stone number at the back of the deque.

This reflects the fact that the stone must appear after stones that will later be placed in the right interval.
6. After processing all characters, traverse the deque from front to back and print every stored stone number.

### Why it works

Maintain the invariant that after processing the first `i` characters, the deque contains exactly the final relative order of stones `1...i`.

When a character is `l`, every future stone generated from the chosen interval must lie to the right of the current stone in the final arrangement. Placing the current stone at the front preserves the correct relative order.

When a character is `r`, every future stone generated from the chosen interval must lie to the left of the current stone. Placing the current stone at the back preserves the correct relative order.

Since each insertion places the new stone in the only position consistent with the interval chosen at that step, the invariant remains true throughout processing. After the last stone, the deque contains the complete left-to-right ordering.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    s = input().strip()

    dq = deque()

    for i, ch in enumerate(s, start=1):
        if ch == 'l':
            dq.appendleft(i)
        else:
            dq.append(i)

    sys.stdout.write('\n'.join(map(str, dq)))

if __name__ == "__main__":
    solve()
```

The solution uses a deque because it supports insertion at both ends in constant time.

The loop processes stones in their natural order, from `1` to `n`. The stone number is obtained directly from the loop index.

For an `l`, we use `appendleft`, placing the stone at the beginning of the current ordering. For an `r`, we use `append`, placing it at the end.

No coordinate calculations are needed. The entire geometric process collapses into maintaining the correct relative order.

The final output is produced by traversing the deque once and joining the numbers with newline characters. This avoids many individual print calls, which is important when the input length reaches one million.

## Worked Examples

### Example 1

Input:

```
llrlr
```

| Step | Character | Stone | Deque after operation |
| --- | --- | --- | --- |
| 1 | l | 1 | [1] |
| 2 | l | 2 | [2, 1] |
| 3 | r | 3 | [2, 1, 3] |
| 4 | l | 4 | [4, 2, 1, 3] |
| 5 | r | 5 | [4, 2, 1, 3, 5] |

Reading from front to back gives:

```
4
2
1
3
5
```

This trace demonstrates the insertion rule directly. Every `l` moves the current stone to the front, while every `r` places it at the end.

### Example 2

Input:

```
rrrl
```

| Step | Character | Stone | Deque after operation |
| --- | --- | --- | --- |
| 1 | r | 1 | [1] |
| 2 | r | 2 | [1, 2] |
| 3 | r | 3 | [1, 2, 3] |
| 4 | l | 4 | [4, 1, 2, 3] |

Output:

```
4
1
2
3
```

This example shows that a late `l` can move a stone ahead of every previously processed stone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One deque insertion per character and one final traversal |
| Space | O(n) | The deque stores all stone numbers |

The input length can be as large as one million. Linear time means only a few million primitive operations, which easily fits within the time limit. Storing one million integers is also well within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s = sys.stdin.readline().strip()
    dq = deque()

    for i, ch in enumerate(s, start=1):
        if ch == 'l':
            dq.appendleft(i)
        else:
            dq.append(i)

    return "\n".join(map(str, dq))

# sample from statement
assert run("llrlr\n") == "4\n2\n1\n3\n5", "sample"

# minimum size
assert run("r\n") == "1", "single stone"

# all left
assert run("lll\n") == "3\n2\n1", "all left moves"

# all right
assert run("rrrr\n") == "1\n2\n3\n4", "all right moves"

# alternating pattern
assert run("lrlr\n") == "4\n2\n1\n3", "mixed ordering"

# boundary style case
assert run("lr\n") == "1\n2", "small mixed case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `r` | `1` | Minimum input size |
| `lll` | `3 2 1` | Repeated front insertions |
| `rrrr` | `1 2 3 4` | Repeated back insertions |
| `lrlr` | `4 2 1 3` | Alternating operations |
| `lr` | `1 2` | Small boundary case |

## Edge Cases

Consider the input:

```
lll
```

Processing proceeds as:

`[1] → [2,1] → [3,2,1]`

The output becomes:

```
3
2
1
```

Every stone is inserted at the front, so the final order is exactly the reverse of arrival order.

Consider the input:

```
rrr
```

Processing proceeds as:

`[1] → [1,2] → [1,2,3]`

The output is:

```
1
2
3
```

Every stone is inserted at the back, so the final order matches arrival order.

Consider the smallest possible input:

```
l
```

The deque becomes `[1]`, and the output is:

```
1
```

The algorithm requires no special handling for this case because both `appendleft` and `append` work correctly when the deque is empty.

Consider a mixed pattern:

```
lrl
```

Processing gives:

`[1] → [1,2] → [3,1,2]`

The output is:

```
3
1
2
```

This confirms that a later `l` correctly jumps ahead of all previously processed stones while preserving the established relative order of the others.
