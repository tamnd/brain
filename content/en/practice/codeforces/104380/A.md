---
title: "CF 104380A - 01 (Easy Version)"
description: "We are given a binary string consisting only of characters 0 and 1. We are allowed to repeatedly find any adjacent pattern \"01\" and remove it completely from the string, closing the gap left by the deletion."
date: "2026-07-01T03:06:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104380
codeforces_index: "A"
codeforces_contest_name: "The Andover Computing Open (TACO) 2023"
rating: 0
weight: 104380
solve_time_s: 57
verified: true
draft: false
---

[CF 104380A - 01 (Easy Version)](https://codeforces.com/problemset/problem/104380/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string consisting only of characters `0` and `1`. We are allowed to repeatedly find any adjacent pattern `"01"` and remove it completely from the string, closing the gap left by the deletion. We continue doing this until no `"01"` substring exists anywhere in the string. The task is to output the final stable string and its length.

The key observation about the process is that deletions are local but the effects are global. Removing one `"01"` can create new `"01"` pairs across the boundary of what remains, so the order of deletions matters in implementation but not in the final result.

The input size can be up to `10^5`, which rules out any approach that repeatedly scans the string and deletes substrings in the middle in a naive way. A single deletion may cost O(n), and in the worst case we could perform O(n) deletions, leading to O(n^2) behavior, which is too slow under the constraints. This immediately suggests we need a linear or near-linear simulation.

A subtle edge case appears when zeros and ones are interleaved in a way that cascading removals happen. For example, in `"0101"`, removing the first `"01"` leaves `"01"` again, and another deletion is possible. A naive left-to-right single pass that does not reconsider newly formed boundaries would fail here.

Another important observation is that the operation only removes `"01"`, never `"10"`. This asymmetry is what drives the structure of the final string.

## Approaches

A direct simulation approach maintains the string and repeatedly scans it for `"01"`, deleting occurrences until none remain. This is correct because it mirrors the allowed operation exactly. However, each scan is O(n), and each deletion shifts the string, which is also O(n). In the worst case where deletions occur many times, such as alternating patterns, the total runtime becomes quadratic.

The key insight is to avoid explicit deletion and instead simulate cancellations using a stack-like process. When scanning left to right, whenever we see a `1`, it can potentially cancel a previous unmatched `0` if that `0` is immediately available in a stack. Each `"01"` deletion corresponds to pairing a `0` that appeared earlier with a later `1`. This suggests that we only need to track how many unmatched zeros are still available, and decide whether a `1` cancels one of them or survives.

This reduces the problem to maintaining a single counter or stack of zeros. Each `0` is pushed as a candidate for future cancellation, and each `1` removes one such candidate if it exists. What remains are unmatched zeros followed by unmatched ones that could not cancel anything to their left.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Repeated Deletion | O(n²) | O(n) | Too slow |
| Stack / Counter Simulation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the string from left to right while maintaining a stack that stores unmatched characters that could not yet be removed.

The stack represents the current reduced form of the processed prefix.
2. For each character, decide whether it forms a removable `"01"` pattern with the top of the stack.

We only remove `"01"`, so the only useful cancellation is when we see `1` and the stack top is `0`.
3. If the current character is `0`, push it onto the stack because it might be removed later by a future `1`.
4. If the current character is `1`, check whether the stack is non-empty and its top is `0`. If so, pop that `0`, representing deletion of the `"01"` pair. Otherwise push `1` onto the stack.
5. After processing the entire string, the stack contains the final irreducible string. Output its length and its contents.

Why it works: at any point in the scan, the stack maintains a reduced form of the prefix with no internal `"01"` pairs remaining. Any future `1` can only interact with earlier `0`s, and the stack ensures we always pair a `1` with the most recent available `0`, which is exactly the only situation where a `"01"` deletion can occur. Since every valid deletion is simulated exactly once and no invalid pairing is introduced, the final stack is the unique fixed point where no `"01"` remains.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    stack = []

    for ch in s:
        if ch == '0':
            stack.append('0')
        else:
            if stack and stack[-1] == '0':
                stack.pop()
            else:
                stack.append('1')

    print(len(stack))
    print(''.join(stack))

if __name__ == "__main__":
    solve()
```

The solution reads the string once and processes each character in order. The stack is used purely as a simulation tool for unmatched symbols. The only non-trivial decision is when processing a `1`: we check whether it can cancel a preceding `0`. This is the only valid deletion pattern, so no other cases are needed.

The final output is constructed directly from the stack without any post-processing.

## Worked Examples

### Example 1: `00011`

We process each character while maintaining the stack.

| Step | Char | Stack Before | Action | Stack After |
| --- | --- | --- | --- | --- |
| 1 | 0 | [] | push 0 | [0] |
| 2 | 0 | [0] | push 0 | [0,0] |
| 3 | 0 | [0,0] | push 0 | [0,0,0] |
| 4 | 1 | [0,0,0] | pop 0 (form 01) | [0,0] |
| 5 | 1 | [0,0] | pop 0 (form 01) | [0] |

Final stack is `[0]`, so output is length `1` and string `"0"`.

This demonstrates how multiple `1`s can repeatedly cancel earlier zeros, and how the process naturally converges without explicit deletion.

### Example 2: `11010101011011111110101`

We show a condensed trace focusing on stack evolution.

| Prefix | Char | Stack Top Action | Stack |
| --- | --- | --- | --- |
| 1 | 1 | push | [1] |
| 2 | 1 | push | [1,1] |
| 3 | 0 | push | [1,1,0] |
| 4 | 1 | pop 0 | [1,1] |
| 5 | 0 | push | [1,1,0] |
| 6 | 1 | pop 0 | [1,1] |
| ... | ... | repeated cancellations | ... |
| final | - | stabilized | [1,1,1,1,1,1,1,1,1] |

The process repeatedly removes every opportunity for a `1` to consume a preceding `0`. Once all such pairs are exhausted, only unmatched `1`s remain, matching the expected output `"111111111"`.

This trace highlights that long alternating structures collapse into a monotone block of ones because every zero eventually finds a matching one to its right.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is pushed and popped at most once |
| Space | O(n) | Stack stores remaining unmatched characters |

The algorithm runs in linear time, which is sufficient for strings up to length `10^5`. Memory usage is also linear in the worst case when no cancellations occur.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("00011\n") == "1\n0", "sample 1"
assert run("11010101011011111110101\n") == "9\n111111111", "sample 2"

# single character cases
assert run("0\n") == "1\n0"
assert run("1\n") == "1\n1"

# already stable (no 01)
assert run("111000\n") == "6\n111000"

# alternating case
assert run("010101\n") == "0\n"

# long collapse to ones
assert run("000000111111\n") == "0\n"

# mixed case
assert run("0010110\n") == "2\n10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1 0` | minimum size |
| `1` | `1 1` | no operation possible |
| `010101` | `0` | full cancellation cascade |
| `111000` | `6 111000` | no `"01"` pairs present |
| `000000111111` | `0` | full reduction to empty |

## Edge Cases

A critical edge case is when deletions cascade across previously separated regions. Consider `0101`. The first `"01"` removal leaves `"01"`, which again forms a removable pair. The stack handles this automatically: after processing `0`, stack is `[0]`, then `1` pops it, leaving `[]`, then next `0` pushes, then last `1` pops again, resulting in an empty stack. The output is correct without needing repeated scans.

Another edge case is a string starting with many ones followed by zeros, such as `111000`. Since no `"01"` ever appears, the stack only grows, and the algorithm preserves the entire string. This confirms that the method does not over-aggressively remove `"10"` patterns, which are not allowed operations.

A final edge case is when the string becomes empty. Any sequence like `000111` reduces completely because every zero eventually finds a matching one to its right. The stack becomes empty naturally, and the algorithm correctly outputs length `0` and an empty string.
