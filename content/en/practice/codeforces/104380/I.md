---
title: "CF 104380I - Bad Grades"
description: "We are given a sequence of exam grades for a student, each grade being an integer between 0 and 100. The task is to produce a cleaned version of this sequence where every grade below 60 is removed, while keeping the relative order of the remaining grades exactly the same as in…"
date: "2026-07-01T17:07:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104380
codeforces_index: "I"
codeforces_contest_name: "The Andover Computing Open (TACO) 2023"
rating: 0
weight: 104380
solve_time_s: 53
verified: true
draft: false
---

[CF 104380I - Bad Grades](https://codeforces.com/problemset/problem/104380/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of exam grades for a student, each grade being an integer between 0 and 100. The task is to produce a cleaned version of this sequence where every grade below 60 is removed, while keeping the relative order of the remaining grades exactly the same as in the original list.

The input is essentially a list transformation problem: we scan through the list once and decide, for each element, whether it survives into the output or is discarded. There is no reordering, no aggregation, and no interaction between elements beyond filtering based on a threshold.

The constraint on the number of grades, up to 100,000, immediately rules out any approach that repeatedly shifts elements inside a list or performs nested scans. A naive implementation that removes elements from a Python list while iterating over it can degrade to quadratic behavior, because each deletion causes elements to be shifted. With 100,000 elements, that kind of behavior would be far too slow under a 1 second limit. The only safe direction is a single pass construction of the output.

Edge cases are mostly structural rather than numerical. If all grades are below 60, the output is empty, and nothing should be printed. If all grades are 60 or above, the output matches the input exactly. A subtle mistake often appears when printing an empty result: some implementations accidentally print an extra newline or fail to produce output at all. Another issue arises if one attempts in-place filtering with index removal, which can skip elements due to index shifting. For example, in `[59, 58, 61]`, removing 59 shifts 58 into its place, and an index-based loop may skip checking it depending on how iteration is structured.

## Approaches

The most direct way to think about this problem is to simulate the process literally: scan the list and delete any element below 60. In an abstract sense, this is correct because it matches the specification exactly. However, implementing deletion inside a Python list is expensive. Each removal shifts all subsequent elements one position to the left, costing O(n) per deletion in the worst case. If most elements are small, we may delete almost all entries, leading to O(n²) behavior.

The structural insight is that deletion is unnecessary if we never mutate the list in place. Instead, we can build a new list and append only valid elements. This converts each element’s processing cost to O(1), since appending to a list is amortized constant time. The problem reduces to a single linear scan where we test a condition and decide whether to copy the element forward.

The reason this works efficiently is that the output order is identical to the input order for retained elements. There is no dependency between decisions, so each grade can be evaluated independently. Once we stop trying to preserve the original container and instead construct a filtered one, the complexity collapses from potentially quadratic to linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| In-place removal during iteration | O(n²) | O(1) | Too slow |
| Build filtered list | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of grades `n`. This defines how many values we will inspect exactly once.
2. Initialize an empty list `result` that will store all grades that pass the threshold check.
3. Iterate over each of the `n` grades as they are read from input.
4. For each grade, compare it with 60.
5. If the grade is at least 60, append it to `result`. Otherwise, ignore it entirely.
6. After processing all grades, print each value in `result` on its own line in the same order they were added.

The key design choice is that we never modify the input sequence. Each decision is local to a single element, so we avoid any side effects that could affect future iterations.

### Why it works

At every step of the scan, `result` contains exactly the sequence of all grades seen so far that are at least 60, in the same order they appeared in the input. When we process a new grade, we either discard it if it is below 60, or append it to the end if it is valid. This preserves both correctness of filtering and stability of ordering. Since every element is examined exactly once and its inclusion depends only on its own value, no later operation can invalidate a previous decision.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    result = []

    for _ in range(n):
        x = int(input())
        if x >= 60:
            result.append(x)

    sys.stdout.write("\n".join(map(str, result)))

if __name__ == "__main__":
    main()
```

The solution uses fast input via `sys.stdin.readline` because reading up to 100,000 lines with standard `input()` can introduce unnecessary overhead. Each grade is processed immediately after reading, and only valid grades are stored.

A subtle implementation detail is the final output construction. Instead of printing line by line, we join all valid integers into a single string. This avoids repeated I/O calls, which can be slow in Python under tight limits.

Another point is handling the case where `result` is empty. The join operation naturally produces an empty string, which matches the required output format with no extra lines.

## Worked Examples

### Example 1

Input:

```
5
100
90
59
65
40
```

We process each grade sequentially:

| Step | Grade | Condition (>=60) | Result |
| --- | --- | --- | --- |
| 1 | 100 | True | [100] |
| 2 | 90 | True | [100, 90] |
| 3 | 59 | False | [100, 90] |
| 4 | 65 | True | [100, 90, 65] |
| 5 | 40 | False | [100, 90, 65] |

Output:

```
100
90
65
```

This trace shows that filtering never changes relative order and only removes elements locally based on value.

### Example 2

Input:

```
4
59
60
58
61
```

| Step | Grade | Condition (>=60) | Result |
| --- | --- | --- | --- |
| 1 | 59 | False | [] |
| 2 | 60 | True | [60] |
| 3 | 58 | False | [60] |
| 4 | 61 | True | [60, 61] |

Output:

```
60
61
```

This example highlights that valid elements remain correctly ordered even when surrounded by invalid ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each grade is read once and checked once |
| Space | O(k) | Stores only grades ≥ 60, where k ≤ n |

The algorithm scales linearly with the number of grades, which is optimal since every input element must be inspected at least once. With n up to 100,000, this comfortably fits within both time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import main
    main()
    return sys.stdout.getvalue().strip()

# sample
assert run("5\n100\n90\n59\n65\n40\n") == "100\n90\n65"

# all removed
assert run("3\n10\n20\n30\n") == ""

# all kept
assert run("3\n60\n70\n100\n") == "60\n70\n100"

# boundary values
assert run("4\n59\n60\n61\n0\n") == "60\n61"

# single element kept
assert run("1\n100\n") == "100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all < 60 | empty | correct handling of no output |
| all ≥ 60 | same list | stability and full retention |
| mixed boundaries | filtered list | correct threshold behavior |
| single element | same or empty | minimal input correctness |

## Edge Cases

When all grades are below 60, such as `10, 20, 30`, the algorithm still iterates through each value and simply never appends anything. The result remains an empty list, and the join operation produces an empty string, which correctly matches the required output format without extra lines.

When all grades are valid, such as `60, 80, 100`, every element satisfies the condition and is appended in order. The algorithm effectively becomes a direct copy of the input, confirming that no unintended transformations occur.

When values alternate around the threshold, such as `59, 60, 58, 61`, each decision is independent. The scan shows that rejected values do not affect later acceptance, and ordering is preserved exactly as required.
