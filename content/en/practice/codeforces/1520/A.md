---
title: "CF 1520A - Do Not Be Distracted!"
description: "Each test case gives a sequence of days, where every day is labeled with the task Polycarp worked on that day. The rule is simple: once he stops working on a task and switches to another one, he is never allowed to return to the old task."
date: "2026-06-10T18:04:53+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1520
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 719 (Div. 3)"
rating: 800
weight: 1520
solve_time_s: 150
verified: true
draft: false
---

[CF 1520A - Do Not Be Distracted!](https://codeforces.com/problemset/problem/1520/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a sequence of days, where every day is labeled with the task Polycarp worked on that day. The rule is simple: once he stops working on a task and switches to another one, he is never allowed to return to the old task.

Viewed differently, every task letter must appear in a single continuous block. A task may last for one day or many consecutive days, but all occurrences of that task must be adjacent.

For example, `"AABBBCC"` is valid because every letter forms one uninterrupted segment. On the other hand, `"ABA"` is invalid because task `A` appears, disappears, and then appears again.

For each test case we must determine whether the recorded sequence follows this rule. If every task appears in exactly one contiguous segment, we print `"YES"`. Otherwise we print `"NO"`.

The constraints are extremely small. There are at most 1000 test cases, and each string has length at most 50. Even an $O(n^2)$ solution would perform at most about 2.5 million operations across all tests, which is easily fast enough. This means correctness and simplicity matter more than aggressive optimization.

A subtle edge case is consecutive repetitions of the same task. Consider:

```
4
AAAA
```

The correct answer is `"YES"` because Polycarp never switched away from task `A`. A careless implementation that treats every occurrence separately instead of every segment could incorrectly reject it.

Another easy mistake appears when a task returns after a gap:

```
3
ABA
```

The correct answer is `"NO"`. Polycarp worked on `A`, switched to `B`, then returned to `A`. An implementation that only checks whether adjacent characters differ would miss this violation.

A slightly less obvious case is:

```
6
AABBCC
```

The correct answer is `"YES"`. Once a task's block ends, it never appears again. A solution that incorrectly assumes every letter may appear only once in the string would reject valid inputs like this.

Finally, consider:

```
7
ABCDCBA
```

The correct answer is `"NO"`. Several letters reappear after other tasks have been started. The violation is not limited to returning immediately after one task; returning after any number of intermediate tasks is forbidden.

## Approaches

A straightforward brute-force idea is to examine every letter and verify that all of its occurrences form one continuous interval. For each character, we can find its first and last position, then check whether every position between them contains that same character. Since there are at most 26 letters and at most 50 positions, this works comfortably within the limits.

There is, however, a cleaner way to think about the problem. The only moments that matter are task switches. Consecutive equal characters belong to the same work segment and do not provide new information.

Suppose we compress the string by keeping only the first character of every segment. For example:

```
AABBBCCAA  ->  ABCA
```

Now each character in the compressed string represents a distinct task segment. The rule becomes very simple: no letter may appear twice in the compressed string.

If a letter appears twice after compression, then there were at least two separate segments of that task, which means Polycarp returned to it later. If every letter appears at most once, then each task occupies exactly one contiguous block.

The brute-force approach checks contiguity directly. The optimized approach observes that only segment boundaries matter and reduces the problem to detecting duplicate letters among the segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Create an empty set called `seen`.
2. Process the string from left to right.
3. For each position, determine whether it starts a new segment. A position starts a new segment if it is the first character of the string or its character differs from the previous character.
4. Whenever a new segment starts, check whether its letter is already in `seen`.
5. If the letter is already present, return `"NO"` immediately. This means the task has appeared in an earlier segment and is now being revisited.
6. Otherwise, add the letter to `seen` and continue scanning.
7. If the entire string is processed without finding a repeated segment letter, return `"YES"`.

### Why it works

The set `seen` contains exactly the task letters whose segments have already begun.

Whenever a new segment starts, there are only two possibilities. Either this is the first segment of that task, in which case adding it to `seen` is valid, or the task already appeared in an earlier segment. In the second case, Polycarp must have left that task and later returned to it, which violates the rule.

Conversely, if no segment-start letter is repeated, then every task appears in exactly one segment. Since each segment is contiguous by construction, every task occupies one continuous block and the schedule is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        seen = set()
        ok = True

        for i in range(n):
            if i == 0 or s[i] != s[i - 1]:
                if s[i] in seen:
                    ok = False
                    break
                seen.add(s[i])

        print("YES" if ok else "NO")

solve()
```

The implementation follows the algorithm directly.

The set `seen` stores letters whose segments have already started. The condition

```
i == 0 or s[i] != s[i - 1]
```

detects the beginning of a new segment. Consecutive equal letters are ignored because they belong to the same uninterrupted task.

The order of operations matters. We first check whether the segment letter has appeared before, and only then add it to the set. Reversing that order would incorrectly reject the very first occurrence of every task.

No special handling is needed for strings of length one. The first character naturally starts a segment, is added to the set, and the answer becomes `"YES"`.

Since only uppercase letters appear, the set never contains more than 26 elements.

## Worked Examples

### Example 1

Input:

```
ABA
```

| i | s[i] | New Segment? | Seen Before? | seen after step |
| --- | --- | --- | --- | --- |
| 0 | A | Yes | No | {A} |
| 1 | B | Yes | No | {A, B} |
| 2 | A | Yes | Yes | violation |

The third character starts a new segment for task `A`. Since `A` already started a segment earlier, Polycarp returned to a finished task. The answer is `"NO"`.

### Example 2

Input:

```
FFGZZZY
```

| i | s[i] | New Segment? | Seen Before? | seen after step |
| --- | --- | --- | --- | --- |
| 0 | F | Yes | No | {F} |
| 1 | F | No | - | {F} |
| 2 | G | Yes | No | {F, G} |
| 3 | Z | Yes | No | {F, G, Z} |
| 4 | Z | No | - | {F, G, Z} |
| 5 | Z | No | - | {F, G, Z} |
| 6 | Y | Yes | No | {F, G, Z, Y} |

No segment-start letter repeats. Every task occupies exactly one block, so the answer is `"YES"`.

This example shows why consecutive equal letters must be ignored. The repeated `F` and `Z` days belong to the same segment and do not represent returning to a task.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(26) | The set stores at most one entry per task letter |

With $n \le 50$, even slower solutions would fit comfortably. The linear scan is trivial for the given limits and uses only a tiny amount of memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        seen = set()
        ok = True

        for i in range(n):
            if i == 0 or s[i] != s[i - 1]:
                if s[i] in seen:
                    ok = False
                    break
                seen.add(s[i])

        ans.append("YES" if ok else "NO")

    return "\n".join(ans)

# provided sample
assert run(
"""5
3
ABA
11
DDBBCCCBBEZ
7
FFGZZZY
1
Z
2
AB
"""
) == """NO
NO
YES
YES
YES""", "sample 1"

# minimum size
assert run(
"""1
1
A
"""
) == "YES", "single task"

# all equal
assert run(
"""1
6
AAAAAA
"""
) == "YES", "single continuous segment"

# returns to a task
assert run(
"""1
5
ABCBA
"""
) == "NO", "task reappears"

# boundary between segments
assert run(
"""1
6
AABBCC
"""
) == "YES", "multiple valid segments"

# maximum-length style case
assert run(
"""1
50
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
"""
) == "YES", "long uniform string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A` | `YES` | Minimum possible input |
| `AAAAAA` | `YES` | Repeated days within one segment |
| `ABCBA` | `NO` | Returning to a previously completed task |
| `AABBCC` | `YES` | Multiple valid contiguous segments |
| 50 copies of `A` | `YES` | Largest length with one continuous task |

## Edge Cases

Consider:

```
1
4
AAAA
```

The scan starts one segment at index 0 and adds `A` to `seen`. The remaining positions do not start new segments because each character equals the previous one. No repeated segment letter is found, so the answer is `"YES"`. This confirms that long continuous work on one task is valid.

Consider:

```
1
3
ABA
```

At index 0, `A` starts a segment and is inserted into `seen`. At index 1, `B` starts a segment and is inserted. At index 2, another segment begins with `A`. Since `A` is already in `seen`, the algorithm immediately returns `"NO"`. This is exactly the forbidden situation of returning to a previous task.

Consider:

```
1
6
AABBCC
```

The segment starts are `A`, `B`, and `C`. Each appears exactly once among segment beginnings, so the set grows as `{A}`, `{A,B}`, `{A,B,C}`. No repetition occurs, and the answer is `"YES"`. This demonstrates that multiple tasks are allowed as long as each occupies one contiguous block.

Consider:

```
1
7
ABCDCBA
```

The segment starts are `A`, `B`, `C`, `D`, `C`, `B`, `A`. When the second `C` segment begins, `C` is already in `seen`, so the algorithm outputs `"NO"` immediately. The violation is detected at the first task that reappears, even if several different tasks are involved.
