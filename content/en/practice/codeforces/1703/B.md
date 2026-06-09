---
title: "CF 1703B - ICPC Balloons"
description: "The contest system processes a sequence of problem solves in time order. Each character in the input string represents a problem label from A to Z, and each occurrence means some team solved that problem at that moment."
date: "2026-06-09T21:35:07+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1703
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 806 (Div. 4)"
rating: 800
weight: 1703
solve_time_s: 98
verified: true
draft: false
---

[CF 1703B - ICPC Balloons](https://codeforces.com/problemset/problem/1703/B)

**Rating:** 800  
**Tags:** data structures, implementation  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The contest system processes a sequence of problem solves in time order. Each character in the input string represents a problem label from A to Z, and each occurrence means some team solved that problem at that moment. Every time a solve happens, the solving team receives one balloon. Additionally, if this is the first time that particular problem has ever been solved in the entire sequence, the team gets one extra balloon.

So the task is to compute a running total over the string: every character contributes at least one balloon, and contributes an additional one the first time that letter appears.

The constraints are small enough that even a direct simulation over the string is trivial. With at most 100 test cases and string length up to 50, the total number of operations is at most a few thousand. Any solution that tracks state per character is easily fast enough.

The main subtlety is understanding that “first solve” is global across the entire sequence, not per team or per position. Once a problem letter appears, all later occurrences should only give one balloon.

A common mistake would be to try recomputing whether a solve is “first” by scanning the prefix each time. For example, for input `BAAAA`, if we incorrectly recomputed from scratch for each character, we might accidentally miscount or complicate logic unnecessarily. Another mistake is forgetting that repeated letters still give one balloon each time.

## Approaches

A brute-force interpretation is to process each position in the string and, for each character, scan all previous positions to check whether it has appeared before. If it has never appeared, we add two to the answer, otherwise we add one.

This works because the definition of “first occurrence” is purely prefix-based. However, checking the entire prefix for every character makes each step O(n), leading to O(n²) per test case. With n up to 50 this is still fine, but it is unnecessary complexity for such a small constraint problem.

The observation that simplifies everything is that we only need to remember whether we have seen each problem letter before. A fixed-size boolean array of length 26 is sufficient. Once a letter is seen, we mark it, and all future occurrences are automatically known to be non-first.

This reduces the entire problem to a single linear scan per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted but overkill |
| Optimal (set/array) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a structure that records which problem letters have already appeared.

1. Initialize a boolean array of size 26 set to false, representing that no problems have been solved yet. Also initialize a counter for total balloons at zero.
2. Iterate through each character in the string in order. Each character corresponds to a specific problem.
3. For each character, check whether it has been seen before using the boolean array. If it has not been seen, this is the first solve of that problem, so we add 2 to the answer and mark it as seen.
4. If it has been seen already, we add only 1 to the answer since it is not the first solve anymore.
5. After processing all characters, output the accumulated total.

The key idea is that the boolean array encodes all necessary historical information in constant space, so each decision can be made in constant time.

### Why it works

At any point in the scan, the boolean array exactly represents the set of problems that have appeared at least once in the prefix ending at the current index. This ensures that when we process a character, the check for “first time seen” is correct by definition: it is first if and only if it is not yet marked. Since marking happens immediately after first encounter and never resets, the invariant holds throughout the scan, making every decision consistent with the problem rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()

        seen = [False] * 26
        total = 0

        for ch in s:
            idx = ord(ch) - ord('A')
            if not seen[idx]:
                total += 2
                seen[idx] = True
            else:
                total += 1

        print(total)

if __name__ == "__main__":
    solve()
```

The solution loops over each test case and maintains a fixed-size array `seen` for the alphabet. The mapping `ord(ch) - ord('A')` converts characters into indices from 0 to 25. The conditional branch directly encodes the scoring rule: unseen characters contribute two, seen ones contribute one. The order of marking matters conceptually but is handled correctly because we only mark after recognizing a first occurrence.

## Worked Examples

### Example 1: `ABA`

We track which letters are seen and the running total.

| Step | Character | Seen Before | Action | Total | Seen Set |
| --- | --- | --- | --- | --- | --- |
| 1 | A | No | +2, mark A | 2 | {A} |
| 2 | B | No | +2, mark B | 4 | {A, B} |
| 3 | A | Yes | +1 | 5 | {A, B} |

The final result is 5, matching the rule that only the first occurrence of each letter gets a bonus.

### Example 2: `BAAAA`

| Step | Character | Seen Before | Action | Total | Seen Set |
| --- | --- | --- | --- | --- | --- |
| 1 | B | No | +2, mark B | 2 | {B} |
| 2 | A | No | +2, mark A | 4 | {A, B} |
| 3 | A | Yes | +1 | 5 | {A, B} |
| 4 | A | Yes | +1 | 6 | {A, B} |
| 5 | A | Yes | +1 | 7 | {A, B} |

This demonstrates repeated contributions of 1 after the initial discovery of a problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is processed once with O(1) lookup and update |
| Space | O(1) | Fixed array of size 26 |

The total number of operations across all test cases is bounded by 5000 characters, so the solution runs instantly within the constraints.

## Test Cases

```python
import sys, io

def solve_io(data: str) -> str:
    sys.stdin = io.StringIO(data)
    import sys as _sys
    from io import StringIO

    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        seen = [False] * 26
        total = 0

        for ch in s:
            idx = ord(ch) - ord('A')
            if not seen[idx]:
                total += 2
                seen[idx] = True
            else:
                total += 1

        out.append(str(total))

    return "\n".join(out)

# provided samples
assert solve_io("6\n3\nABA\n1\nA\n3\nORZ\n5\nBAAAA\n4\nBKPT\n10\nCODEFORCES\n") == "5\n2\n6\n7\n8\n17"

# minimum size
assert solve_io("1\n1\nA\n") == "2"

# all same letters
assert solve_io("1\n5\nAAAAA\n") == "6"

# alternating new letters
assert solve_io("1\n4\nABCD\n") == "8"

# mixed pattern
assert solve_io("1\n6\nABACBC\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A` | 2 | Minimum input case |
| `AAAAA` | 6 | Repeated letters only |
| `ABCD` | 8 | All unique letters |
| `ABACBC` | 10 | Mixed repeats and first occurrences |

## Edge Cases

A key edge case is when the string consists of a single repeated character. For input `AAAAA`, the algorithm marks `A` as unseen at the first step and then treats all subsequent occurrences as already seen. The trace shows the first step contributes 2, and the remaining four contribute 1 each, producing 6.

Another case is when all characters are distinct like `ABCD`. Each character is unseen at first encounter, so every step adds 2. The algorithm marks each letter immediately, ensuring no later confusion, and the final result becomes 8.

A mixed alternating pattern such as `ABACBC` confirms that once a letter is marked, it never regains “unseen” status, which guarantees consistency even when characters reappear after long gaps.
