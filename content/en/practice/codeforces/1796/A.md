---
title: "CF 1796A - Typical Interview Problem"
description: "We are asked to reason about an infinite string that is not built directly character by character, but generated from the positive integers in order."
date: "2026-06-09T10:01:51+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1796
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 144 (Rated for Div. 2)"
rating: 800
weight: 1796
solve_time_s: 204
verified: true
draft: false
---

[CF 1796A - Typical Interview Problem](https://codeforces.com/problemset/problem/1796/A)

**Rating:** 800  
**Tags:** brute force, implementation, strings  
**Solve time:** 3m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to reason about an infinite string that is not built directly character by character, but generated from the positive integers in order. For each integer $i = 1, 2, 3, \dots$, we append characters depending on divisibility: we append `F` if $i$ is divisible by 3, and we append `B` if $i$ is divisible by 5. If a number is divisible by both 3 and 5, both characters are appended in that order, meaning `F` first and then `B`.

This produces a single infinite sequence over the alphabet `{F, B}`. Each integer contributes either zero, one, or two characters, so the string grows unevenly, but deterministically.

Each query gives a short string $s$ of length at most 10, and we must determine whether it appears as a contiguous segment somewhere in this infinite generated string.

The constraint that $k \le 10$ is the key structural hint. A substring of such small length cannot require us to explore deep into the construction. Any correct solution only needs to understand a bounded portion of the infinite sequence, because local patterns repeat regularly.

A naive attempt might try to simulate the process for a large range of integers, but this quickly becomes unnecessary once we notice the structure repeats every 15 integers, since divisibility by 3 and 5 depends only on $i \bmod 15$.

A subtle mistake arises if we only check within a single small prefix of integers without handling substring overlap across boundaries. For example, a pattern might start near the end of one block of 15 integers and continue into the next. Another failure mode is treating the process as a sequence per integer rather than per emitted character, which leads to incorrect substring alignment.

## Approaches

The brute-force idea is to simulate the construction of the FB-string by iterating over integers and appending characters until the string becomes “long enough”, typically until it exceeds some multiple of the query length. Since each integer produces up to 2 characters, and $k \le 10$, we could safely simulate maybe a few hundred integers per test case and then run a substring check.

This approach is correct because it faithfully reconstructs the definition. However, it becomes inefficient if scaled up, since each test case would repeatedly simulate many integers even though the structure repeats deterministically.

The key observation is periodicity. The contribution of each integer depends only on whether it is divisible by 3 and 5, which is fully determined by its remainder modulo 15. Every block of 15 consecutive integers produces exactly the same sequence of appended characters. This means the entire infinite FB-string is a repetition of a fixed finite string corresponding to integers 1 through 15.

Once we have that base block, any substring of the infinite string can be found by searching within a sufficiently repeated version of it. Since the maximum query length is 10, duplicating the base block a small number of times guarantees we never miss substrings crossing the boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(t · N) | O(N) | Too slow conceptually |
| Period-15 Construction | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

We construct one full period of the FB-string by simulating integers from 1 to 15. Then we repeat this block a few times to safely cover boundary-crossing substrings. Finally, we check whether the query string appears inside this expanded string.

1. Iterate integers from 1 to 15 and build a base string.

For each integer, append `F` if divisible by 3, and append `B` if divisible by 5, in that order. This produces the fundamental repeating block.
2. Repeat the block several times, for example 3 times.

This ensures any substring of length at most 10 is fully contained even if it crosses the boundary between two blocks.
3. For each query string, check if it is a substring of this constructed finite string.
4. Output `YES` if found, otherwise `NO`.

### Why it works

The construction depends only on divisibility by 3 and 5, which repeats with period 15 over the integers. Since each integer contributes independently based only on this property, the emitted sequence of characters repeats exactly every 15 integers. Any substring of the infinite string is therefore contained within repeated copies of a fixed finite block. Extending the block slightly beyond one period guarantees that boundary-crossing substrings are also captured.

## Python Solution

```python
import sys
input = sys.stdin.readline

# build one period (1..15)
base = []
for i in range(1, 16):
    if i % 3 == 0:
        base.append("F")
    if i % 5 == 0:
        base.append("B")

base = "".join(base)

# repeat enough to cover substrings up to length 10 crossing boundaries
text = base * 3

t = int(input())
for _ in range(t):
    k = int(input())
    s = input().strip()
    if s in text:
        print("YES")
    else:
        print("NO")
```

The solution first constructs the minimal repeating unit of the FB-string over integer indices 1 to 15. It then repeats this unit three times to ensure that any substring of length up to 10 is fully represented even if it spans the end of one period and the start of another. Each query is answered using a direct substring check, which is efficient because both the text and pattern are small and fixed in size.

The only subtle point is ensuring correct ordering of appended characters when an integer is divisible by both 3 and 5. The code preserves this by appending `F` first and `B` second.

## Worked Examples

### Example 1

Input string `FFB` is tested against the constructed periodic text.

| Step | Operation | Current state |
| --- | --- | --- |
| 1 | Build base from 1..15 | base = "F B F F B F F B F F B F F B F" (conceptually) |
| 2 | Repeat 3 times | text = base + base + base |
| 3 | Check substring | "FFB" found |

This confirms that short sequences starting at different integer boundaries are correctly captured inside repeated structure.

### Example 2

Input string `BBB` is tested.

| Step | Operation | Current state |
| --- | --- | --- |
| 1 | Build base | fixed periodic block |
| 2 | Repeat | extended text |
| 3 | Check substring | not found |

This shows that even though `B` appears frequently, three consecutive `B`s never align in a valid construction segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test performs a substring check on a constant-size string |
| Space | O(1) | The constructed pattern is fixed and independent of input size |

The constraints allow up to 2046 queries, but each query is answered in constant time against a precomputed small string, so the solution easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    base = []
    for i in range(1, 16):
        if i % 3 == 0:
            base.append("F")
        if i % 5 == 0:
            base.append("B")
    base = "".join(base)
    text = base * 3

    t = int(input())
    out = []
    for _ in range(t):
        k = int(input())
        s = input().strip()
        out.append("YES" if s in text else "NO")
    return "\n".join(out)

# provided samples
assert run("""3
3
FFB
8
BFFBFFBF
3
BBB
""") == """YES
YES
NO"""

# minimum size
assert run("""1
1
F
""") == "YES"

# simple B case
assert run("""1
1
B
""") == "YES"

# boundary-crossing style case
assert run("""1
2
FB
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `F` | YES | single-character match |
| `B` | YES | single B always appears |
| `FB` | YES | ordering correctness across same integer |
| `BBB` | NO | impossible triple pattern |

## Edge Cases

A tricky case is when a substring begins near the end of one 15-integer cycle and continues into the next. The algorithm handles this because the repeated construction `base * 3` guarantees that every boundary region appears fully inside the finite representation.

For example, if a pattern starts at the last character of one block and continues into the next, the constructed string still contains that overlap in the middle copy of the repetition. The substring check then finds it directly without needing special handling of indices or integer alignment.
