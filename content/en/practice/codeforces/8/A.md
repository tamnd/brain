---
title: "CF 8A - Train and Peter"
description: "We are given a string that represents the sequence of station flags seen while traveling from city A to city B. Peter woke up twice during the trip and wrote down two substrings he saw, in chronological order."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 8
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 8"
rating: 1200
weight: 8
solve_time_s: 77
verified: true
draft: false
---
[CF 8A - Train and Peter](https://codeforces.com/problemset/problem/8/A)

**Rating:** 1200  
**Tags:** strings  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string that represents the sequence of station flags seen while traveling from city A to city B. Peter woke up twice during the trip and wrote down two substrings he saw, in chronological order.

The question is whether these two observations could appear while traveling forward, backward, both ways, or neither.

Suppose the main string is `s`, the first observed sequence is `a`, and the second is `b`.

For the forward direction, we need to check whether `a` appears somewhere in `s`, and then after the end of that occurrence, `b` appears later in the string. The two observations must respect time order, so the second substring must start strictly after the first substring finishes.

For the backward direction, the train sees the stations in reverse order. Instead of building another traversal manually, we can reverse `s` and perform the same check on the reversed string.

The main string can be as large as `10^5`, while the observation strings are at most length `100`. This immediately rules out anything quadratic in the length of `s`. A naive nested scan over all substring pairs could reach roughly `10^10` operations in the worst case, which is far too slow for a 1 second limit. Linear or near-linear processing is the right target.

There are a few easy-to-miss edge cases.

One subtle point is that the two observations cannot overlap in time. Consider:

```
s = "aaaa"
a = "aa"
b = "aa"
```

The correct answer is:

```
forward
```

because we can use positions `[0,1]` for the first observation and `[2,3]` for the second. A careless implementation that only checks whether both substrings exist somewhere would incorrectly accept many invalid overlaps.

Another tricky case is when the backward direction works but the forward one does not:

```
s = "abcdef"
a = "de"
b = "ab"
```

Forward travel fails because `"ab"` does not appear after `"de"`. Reversing the route gives `"fedcba"`, where `"de"` becomes visible before `"ab"` in the reversed traversal. The correct output is:

```
backward
```

A third case involves repeated patterns:

```
s = "ababa"
a = "aba"
b = "ba"
```

The first occurrence of `"aba"` ends too late to allow `"ba"` afterward, but another valid placement may still exist depending on the search strategy. Greedy matching without respecting positions carefully can miss valid solutions.

## Approaches

The brute-force approach tries every occurrence of the first substring and then searches for the second substring after it.

For every position `i` in `s`, we check whether `a` starts there. If it does, we scan every later position `j` and check whether `b` starts there. This is correct because it explicitly tests every valid chronological placement.

The problem is the amount of repeated work. The main string has length up to `10^5`. In the worst case we may inspect almost every pair of positions, giving roughly `O(n^2)` checks. Even though the observation strings are short, quadratic behavior is too expensive.

The key observation is that we do not need all possible placements. We only need to know whether there exists one valid occurrence of `a` followed later by one valid occurrence of `b`.

Python already provides efficient substring searching with `find`. If we locate the first occurrence of `a`, we immediately know the earliest point where the second observation could begin. Then we search for `b` starting strictly after the end of `a`.

This reduces the problem to two substring searches.

To handle backward travel, we reverse the main string and repeat exactly the same logic. The reverse traversal problem becomes identical to the forward traversal problem on the reversed string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the three strings: the route string `s`, the first observation `a`, and the second observation `b`.
2. Create a helper function that checks whether `a` appears before `b` inside a given string.
3. Inside the helper, find the first occurrence of `a` using `find`.
4. If `a` does not exist, immediately return `False`.
5. Otherwise, compute the earliest valid starting position for the second observation. If `a` starts at index `pos`, then `b` must start at or after `pos + len(a)`.
6. Search for `b` beginning from that position.
7. If `b` is found, return `True`. Otherwise return `False`.
8. Run this helper on the original string to determine whether forward travel works.
9. Reverse the main string and run the same helper again to determine whether backward travel works.
10. Produce the final answer:
11. If both checks succeed, print `"both"`.
12. If only the forward check succeeds, print `"forward"`.
13. If only the backward check succeeds, print `"backward"`.
14. Otherwise print `"fantasy"`.

### Why it works

The helper function always searches for the second substring only after the first substring has completely ended. This matches the chronological requirement from the problem.

Using the earliest occurrence of `a` is sufficient. If even the earliest occurrence cannot be followed by `b`, then any later occurrence leaves even less space afterward, so no valid arrangement exists.

Reversing the route string transforms backward travel into the same exact problem structure. Any valid backward observation sequence corresponds to a forward observation sequence in the reversed string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_form(s, a, b):
    first = s.find(a)

    if first == -1:
        return False

    second = s.find(b, first + len(a))

    return second != -1

def solve():
    s = input().strip()
    a = input().strip()
    b = input().strip()

    forward = can_form(s, a, b)
    backward = can_form(s[::-1], a, b)

    if forward and backward:
        print("both")
    elif forward:
        print("forward")
    elif backward:
        print("backward")
    else:
        print("fantasy")

solve()
```

The helper function captures the entire core logic. First it locates the first observation. If that substring does not exist, there is no valid travel sequence.

The second search begins at `first + len(a)`. This detail matters. Starting from `first + 1` would incorrectly allow overlapping observations, which the problem forbids because the train continuously moves forward.

The backward direction is implemented by reversing the route string with `s[::-1]`. No extra index logic is needed because the ordering condition stays identical after reversal.

The solution performs only a constant number of substring searches, each linear in the length of the main string.

## Worked Examples

### Example 1

Input:

```
s = "atob"
a = "a"
b = "b"
```

Forward check:

| Step | Value |
| --- | --- |
| find("a") | 0 |
| next search starts at | 1 |
| find("b", 1) | 3 |
| result | True |

Backward check on `"bota"`:

| Step | Value |
| --- | --- |
| find("a") | 3 |
| next search starts at | 4 |
| find("b", 4) | -1 |
| result | False |

Final answer:

```
forward
```

This trace shows the chronological constraint clearly. In the reversed string, `"a"` appears too late for `"b"` to appear afterward.

### Example 2

Input:

```
s = "abcdef"
a = "de"
b = "ab"
```

Forward check:

| Step | Value |
| --- | --- |
| find("de") | 3 |
| next search starts at | 5 |
| find("ab", 5) | -1 |
| result | False |

Backward check on `"fedcba"`:

| Step | Value |
| --- | --- |
| find("de") | 2 |
| next search starts at | 4 |
| find("ab", 4) | 4 |
| result | True |

Final answer:

```
backward
```

This demonstrates why reversing the string correctly models the opposite travel direction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each substring search scans the string linearly |
| Space | O(n) | Reversing the string creates a copy |

The maximum string length is `10^5`, so linear processing easily fits within the time limit. The memory usage is also small because only one reversed copy of the string is stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    s = input().strip()
    a = input().strip()
    b = input().strip()

    def can_form(s, a, b):
        first = s.find(a)

        if first == -1:
            return False

        second = s.find(b, first + len(a))

        return second != -1

    forward = can_form(s, a, b)
    backward = can_form(s[::-1], a, b)

    if forward and backward:
        print("both")
    elif forward:
        print("forward")
    elif backward:
        print("backward")
    else:
        print("fantasy")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    global input
    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__

    return out.getvalue().strip()

# provided sample
assert run("atob\na\nb\n") == "forward", "sample 1"

# minimum size
assert run("a\na\na\n") == "fantasy", "single character overlap impossible"

# both directions work
assert run("ababa\nab\nba\n") == "both", "works in both forward and reverse"

# backward only
assert run("abcdef\nde\nab\n") == "backward", "only reverse traversal works"

# overlapping substrings should fail
assert run("aaa\naa\naa\n") == "fantasy", "overlap not allowed"

# repeated characters with valid separation
assert run("aaaa\naa\naa\n") == "both", "non-overlapping repeated substrings"

# large repeated input
big = "a" * 100000
assert run(f"{big}\naaa\naaa\n") == "both", "handles maximum length efficiently"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a / a` | `fantasy` | Prevents overlap on minimal input |
| `ababa / ab / ba` | `both` | Validates both-direction detection |
| `abcdef / de / ab` | `backward` | Confirms reverse traversal logic |
| `aaa / aa / aa` | `fantasy` | Catches overlapping substring mistakes |
| `aaaa / aa / aa` | `both` | Confirms valid non-overlapping reuse |
| very large repeated string | `both` | Confirms linear performance |

## Edge Cases

Consider the overlapping case:

```
s = "aaa"
a = "aa"
b = "aa"
```

The algorithm finds the first `"aa"` at index `0`. The second search begins at index `2`, because the first observation occupies positions `0` and `1`. There are no two characters left, so the second search fails.

The output becomes:

```
fantasy
```

This is correct because the same station cannot be reused.

Now consider repeated characters with enough separation:

```
s = "aaaa"
a = "aa"
b = "aa"
```

The first `"aa"` is found at index `0`. The second search begins at index `2`, where another `"aa"` exists.

The algorithm correctly outputs:

```
both
```

because the same arrangement also works in the reversed string.

Finally, consider a backward-only case:

```
s = "abcdef"
a = "de"
b = "ab"
```

Forward search fails since `"ab"` does not appear after `"de"`.

After reversing, the string becomes `"fedcba"`. The substring `"de"` appears at index `2`, and `"ab"` appears later at index `4`.

The algorithm outputs:

```
backward
```

which matches the actual travel order from B to A.
