---
title: "CF 127B - Canvas Frames"
description: "We are given a collection of sticks, where each stick has an integer length. A rectangular frame needs four sticks arranged as two equal pairs. If the frame is a square, then all four sticks must have the same length."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 127
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 93 (Div. 2 Only)"
rating: 1000
weight: 127
solve_time_s: 106
verified: true
draft: false
---

[CF 127B - Canvas Frames](https://codeforces.com/problemset/problem/127/B)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of sticks, where each stick has an integer length. A rectangular frame needs four sticks arranged as two equal pairs. If the frame is a square, then all four sticks must have the same length.

The task is to build as many frames as possible without cutting or combining sticks. We may leave some sticks unused if they cannot contribute to another frame.

The key observation is that every frame consumes exactly two pairs of equal lengths. A length that appears four times can either create one square frame by itself, or contribute two separate pairs to different rectangles.

The constraints are very small. There are at most 100 sticks, and stick lengths are also at most 100. Even inefficient solutions would pass comfortably here, but the problem is mainly about recognizing the correct counting logic.

A common mistake is to think that four equal sticks always form exactly one frame and cannot help elsewhere. Consider this input:

```
6
5 5 5 5 2 2
```

The correct answer is:

```
1
```

We have three pairs total: two pairs of length 5 and one pair of length 2. Since each frame needs two pairs, we can build only one frame.

Another subtle case appears when many different lengths each contribute only one pair:

```
8
1 1 2 2 3 3 4 4
```

The correct answer is:

```
2
```

We have four pairs overall, so we can build two frames. A careless implementation that tries to greedily build squares first would still work here, but more complicated greedy constructions are unnecessary because only the total number of pairs matters.

The minimum edge case is:

```
1
7
```

The correct answer is:

```
0
```

A single stick cannot form even one pair.

## Approaches

A brute-force way to think about the problem is to repeatedly search for two pairs among the remaining sticks, remove them, and count one frame. Since the input size is tiny, we could even sort the sticks and simulate pair extraction directly.

For example, after sorting, we could scan for adjacent equal values, collect pairs, then every two collected pairs form one frame. This already hints at the real structure of the problem.

The brute-force perspective works because a frame depends only on pairs of equal lengths. The actual dimensions do not matter beyond that. Once we realize this, the problem becomes much simpler.

Suppose a stick length appears `cnt` times. Then it contributes `cnt // 2` usable pairs. Every frame consumes exactly two pairs. So if the total number of pairs is `P`, the answer is simply:

```
P // 2
```

This avoids any explicit frame construction.

The observation that unlocks the solution is that pair identity does not matter. A pair of length 2 and a pair of length 5 already form a valid rectangle. Four sticks of the same length simply contribute two pairs. The entire problem reduces to counting how many pairs exist overall.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(n) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of sticks and the stick lengths.
2. Count how many times each stick length appears.

Since stick lengths are at most 100, we can use a small frequency array or a dictionary.
3. For every distinct length, compute how many pairs it contributes.

If a length appears `cnt` times, it contributes `cnt // 2` pairs because each pair needs two equal sticks.
4. Sum all contributed pairs into a variable called `pairs`.
5. Compute `pairs // 2`.

Every frame consumes exactly two pairs, so dividing the total number of pairs by two gives the maximum number of frames.
6. Print the result.

### Why it works

Every valid frame requires exactly two equal-stick pairs. No frame can be built without two pairs, and any two pairs can always form a rectangle.

For a length appearing `cnt` times, using more than `cnt // 2` pairs is impossible because each pair consumes two sticks. Summing over all lengths gives the maximum number of pairs obtainable from the input.

Since each frame consumes two pairs independently of stick lengths, the maximum number of frames is exactly the total number of pairs divided by two.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

freq = [0] * 101

for x in a:
    freq[x] += 1

pairs = 0

for cnt in freq:
    pairs += cnt // 2

print(pairs // 2)
```

The solution starts by counting occurrences of each stick length. Because the maximum stick length is only 100, a fixed-size array is simpler and faster than a dictionary.

The variable `pairs` stores the total number of usable equal-stick pairs. For each frequency `cnt`, integer division by 2 gives the number of disjoint pairs we can extract.

The final answer is `pairs // 2` because every frame consumes two pairs.

One subtle point is that we never explicitly construct rectangles or squares. That is intentional. The proof shows that pair count alone completely determines the answer.

Another detail is that integer division naturally handles leftover sticks. For example, if a length appears 5 times, then `5 // 2 = 2`, meaning one stick remains unused.

## Worked Examples

### Example 1

Input:

```
5
2 4 3 2 3
```

| Length | Frequency | Pairs Added | Total Pairs |
| --- | --- | --- | --- |
| 2 | 2 | 1 | 1 |
| 3 | 2 | 1 | 2 |
| 4 | 1 | 0 | 2 |

Final computation:

```
frames = 2 // 2 = 1
```

Output:

```
1
```

This example shows the core idea clearly. We do not need four equal sticks. Two independent pairs already form one rectangle.

### Example 2

Input:

```
10
1 1 1 1 2 2 3 3 3 3
```

| Length | Frequency | Pairs Added | Total Pairs |
| --- | --- | --- | --- |
| 1 | 4 | 2 | 2 |
| 2 | 2 | 1 | 3 |
| 3 | 4 | 2 | 5 |

Final computation:

```
frames = 5 // 2 = 2
```

Output:

```
2
```

This trace demonstrates that square-capable lengths simply contribute multiple pairs. We never need special handling for squares.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the sticks once and then scan the small frequency array |
| Space | O(1) | The frequency array has fixed size 101 |

The solution easily fits within the limits. Even much slower approaches would pass for `n = 100`, but the counting approach is both simpler and optimal.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    freq = [0] * 101

    for x in a:
        freq[x] += 1

    pairs = 0

    for cnt in freq:
        pairs += cnt // 2

    print(pairs // 2)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("5\n2 4 3 2 3\n") == "1", "sample 1"

# minimum input
assert run("1\n7\n") == "0", "single stick"

# all equal
assert run("8\n5 5 5 5 5 5 5 5\n") == "2", "two square frames"

# many distinct pairs
assert run("8\n1 1 2 2 3 3 4 4\n") == "2", "four pairs total"

# leftover sticks
assert run("7\n1 1 1 2 2 2 3\n") == "1", "unused leftovers"

# maximum useful grouping
assert run("12\n1 1 1 1 2 2 2 2 3 3 3 3\n") == "3", "multiple squares"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Minimum-size input |
| `8 / 5 5 5 5 5 5 5 5` | `2` | Multiple square frames |
| `8 / 1 1 2 2 3 3 4 4` | `2` | Different lengths combine into rectangles |
| `7 / 1 1 1 2 2 2 3` | `1` | Leftover unpaired sticks are ignored |
| `12 / 1 1 1 1 2 2 2 2 3 3 3 3` | `3` | Several independent pair groups |

## Edge Cases

Consider the case where one stick length appears many times:

```
8
5 5 5 5 5 5 5 5
```

The frequency of length 5 is 8, so it contributes `8 // 2 = 4` pairs. Since every frame needs two pairs, the answer is `4 // 2 = 2`.

The algorithm correctly treats these as either two square frames or any equivalent arrangement. No special square handling is needed.

Now consider leftover sticks:

```
7
1 1 1 2 2 2 3
```

The frequencies are:

```
1 -> 3
2 -> 3
3 -> 1
```

The pair counts become:

```
1 -> 1 pair
2 -> 1 pair
3 -> 0 pairs
```

Total pairs equal 2, so the answer is 1 frame.

The extra sticks of lengths 1 and 2 are ignored automatically because integer division discards incomplete pairs.

Finally, consider many different lengths:

```
8
1 1 2 2 3 3 4 4
```

Each length contributes exactly one pair, giving four pairs total. The algorithm outputs `4 // 2 = 2`.

This confirms the central invariant of the solution: only the total number of pairs matters, not which lengths the pairs come from.
