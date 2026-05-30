---
title: "CF 493B - Vasya and Wrestling"
description: "We are given a chronological log of wrestling techniques. Each entry is an integer that describes both who performed the move and how many points it contributed."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 493
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 281 (Div. 2)"
rating: 1400
weight: 493
solve_time_s: 654
verified: false
draft: false
---

[CF 493B - Vasya and Wrestling](https://codeforces.com/problemset/problem/493/B)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 10m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a chronological log of wrestling techniques. Each entry is an integer that describes both who performed the move and how many points it contributed. A positive value means the first wrestler performed a move worth that many points, while a negative value means the second wrestler performed a move worth the absolute value of that number.

From this stream, we reconstruct two sequences: one sequence of points earned by the first wrestler in the order they appear, and another sequence for the second wrestler. At the end, the winner is determined in three stages. First, we compare total points. If one wrestler has a larger sum, they win immediately. If totals are equal, we compare the two sequences lexicographically, and the larger sequence wins. If both sequences are identical in both values and length, the winner is the wrestler who performed the last move in the input.

The constraint n up to 2·10^5 implies that any solution must be linear or near linear in time. A quadratic approach that compares prefixes repeatedly or repeatedly re-scans sequences would be too slow because it could reach 10^10 operations in the worst case. We need to process the input in a single pass and avoid repeated comparisons.

A subtle edge case appears when totals are equal but sequences differ only at the last differing element. For example, if one sequence is a prefix of the other, lexicographic comparison depends on length. Another edge case is when sequences are identical in value and length, where the winner is decided only by the last non-zero event, which may belong to either wrestler.

## Approaches

A brute-force interpretation would explicitly build both sequences, then compute their sums and finally compare them lexicographically. This works conceptually, but the lexicographic comparison itself can degrade. In the worst case, both sequences may contain up to n elements, and comparing them from scratch for every decision point or multiple passes over the data still remains linear, but the real inefficiency appears if one tries to simulate comparisons repeatedly while processing.

The key observation is that we do not need to repeatedly compare sequences. We only need to construct them once and then perform three deterministic comparisons at the end: total sum comparison, lexicographic comparison, and last-move comparison. Since constructing the sequences is already O(n), all remaining operations must also be O(n) or O(1) per comparison.

We maintain two arrays, one for each wrestler, and two running sums. We also track the index of the last move. Once input is fully processed, we compare sums. If equal, we compare lists using Python’s native lexicographic comparison, which is optimal and implemented in C. If still equal, we check which player made the last move.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted but unnecessary overhead |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read n, then iterate through all moves in order. For each value aᵢ, determine which wrestler performed it by checking its sign. This step is necessary to reconstruct both scoring sequences faithfully.
2. If aᵢ is positive, append it to the first wrestler’s sequence and add it to their running sum. If aᵢ is negative, append its absolute value to the second wrestler’s sequence and add it to their sum. This keeps both score accumulation and sequence reconstruction synchronized in one pass.
3. Track the index of the last move and which player performed it. This information is only needed if all other comparisons end in a tie.
4. After processing all moves, compare the total sums of both wrestlers. If one is larger, we can immediately decide the winner without considering sequence structure.
5. If the sums are equal, compare the two sequences lexicographically. This comparison follows standard dictionary order: first differing element decides, otherwise the longer sequence wins if one is a prefix of the other.
6. If both sequences are identical, return the winner based on who performed the last move.

### Why it works

The algorithm directly mirrors the problem’s decision hierarchy: sum comparison dominates lexicographic comparison, which dominates last-move tie-breaking. Because each piece of information (sequences, sums, last move) is preserved exactly as defined in the problem, no transformation or approximation is introduced. The correctness follows from the fact that lexicographic order depends only on the first differing position, and we preserve full sequences, so no information needed for comparison is lost.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
first = []
second = []
sum1 = 0
sum2 = 0

last = 0  # 1 for first, 2 for second

for _ in range(n):
    x = int(input())
    if x > 0:
        first.append(x)
        sum1 += x
        last = 1
    else:
        x = -x
        second.append(x)
        sum2 += x
        last = 2

if sum1 > sum2:
    print("first")
elif sum2 > sum1:
    print("second")
else:
    if first > second:
        print("first")
    elif second > first:
        print("second")
    else:
        print("first" if last == 1 else "second")
```

The code constructs both sequences while computing their sums in a single pass over the input. The variable last stores who performed the most recent move, which is only used if both sequences end up identical in value and structure.

The comparison `first > second` leverages Python’s built-in lexicographic list comparison, which matches the problem definition exactly. This avoids manual element-by-element comparison and keeps the implementation compact and safe from indexing errors.

The final tie-break uses the stored last mover, ensuring correctness when sequences are fully identical.

## Worked Examples

### Example 1

Input:

```
5
1
2
-3
-4
3
```

| Step | First seq | Second seq | sum1 | sum2 | last |
| --- | --- | --- | --- | --- | --- |
| 1 | [1] | [] | 1 | 0 | first |
| 2 | [1,2] | [] | 3 | 0 | first |
| 3 | [1,2] | [3] | 3 | 3 | second |
| 4 | [1,2] | [3,4] | 3 | 7 | second |
| 5 | [1,2,3] | [3,4] | 6 | 7 | first |

Sums are 6 and 7, so the second wrestler wins immediately without needing lexicographic comparison. The trace shows how the second wrestler builds a stronger total score despite the first having more elements.

### Example 2

Input:

```
4
1
2
-1
-2
```

| Step | First seq | Second seq | sum1 | sum2 | last |
| --- | --- | --- | --- | --- | --- |
| 1 | [1] | [] | 1 | 0 | first |
| 2 | [1,2] | [] | 3 | 0 | first |
| 3 | [1,2] | [1] | 3 | 1 | second |
| 4 | [1,2] | [1,2] | 3 | 3 | second |

Now sums are equal. Lexicographic comparison shows both sequences are identical, so the decision moves to the last move rule. The last move belongs to the second wrestler, so they win.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass construction plus O(n) lexicographic comparison in worst case |
| Space | O(n) | storing both sequences explicitly |

The constraints allow up to 2·10^5 moves, and both time and memory usage scale linearly with n, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    output = []

    def fake_print(*args):
        output.append(" ".join(map(str, args)))

    # backup
    orig_print = builtins.print
    builtins.print = fake_print

    try:
        n = int(input())
        first = []
        second = []
        sum1 = 0
        sum2 = 0
        last = 0

        for _ in range(n):
            x = int(input())
            if x > 0:
                first.append(x)
                sum1 += x
                last = 1
            else:
                x = -x
                second.append(x)
                sum2 += x
                last = 2

        if sum1 > sum2:
            print("first")
        elif sum2 > sum1:
            print("second")
        else:
            if first > second:
                print("first")
            elif second > first:
                print("second")
            else:
                print("first" if last == 1 else "second")

        return "\n".join(output)
    finally:
        builtins.print = orig_print

# provided sample
assert run("""5
1
2
-3
-4
3
""") == "second"

# minimum case
assert run("""1
5
""") == "first"

# second wins by sum
assert run("""3
1
-10
2
""") == "second"

# lexicographic tie, different structure
assert run("""4
1
2
-1
-3
""") == "second"

# identical sequences, last move decides
assert run("""2
1
-1
""") == "second"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 moves sample | second | standard mixed case |
| single positive | first | minimum size |
| second dominates sum | second | sum dominance |
| prefix-based tie behavior | second | lexicographic edge |
| identical sequences | second | last-move tie-break |

## Edge Cases

One edge case occurs when both sequences are identical but constructed in different orders of moves. Consider input:

```
2
1
-1
```

First sequence is [1], second is [1]. Sums are equal and lexicographic comparison yields equality. The algorithm correctly falls back to the last move, which is second, producing "second".

Another edge case is when one sequence is a strict prefix of the other:

```
3
1
2
-1
```

Here first = [1,2], second = [1]. Sums differ, so the answer is already determined as "first". If sums were artificially equal in a modified scenario, lexicographic comparison would correctly favor the longer sequence, since Python list comparison handles prefix ordering exactly as required by the problem definition.
