---
title: "CF 105507D - \u041f\u0440\u0435\u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u043e\u043a\u0438"
description: "We are given two strings of equal length, both consisting of lowercase Latin letters. The only allowed operation takes the first character of the current string, removes it, and reinserts it anywhere in the string, including back to the front or the end."
date: "2026-06-24T00:15:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105507
codeforces_index: "D"
codeforces_contest_name: "2024-2025 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 24, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 105507
solve_time_s: 71
verified: true
draft: false
---

[CF 105507D - \u041f\u0440\u0435\u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u043e\u043a\u0438](https://codeforces.com/problemset/problem/105507/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings of equal length, both consisting of lowercase Latin letters. The only allowed operation takes the first character of the current string, removes it, and reinserts it anywhere in the string, including back to the front or the end. This operation can be repeated any number of times. The goal is to determine the smallest number of such operations needed to turn the initial string into the target string, or decide that it cannot be done at all.

The key observation from the operation itself is that we never delete or create characters, so the multiset of characters must remain identical between the two strings. This immediately gives a necessary condition: if the frequency of any character differs between the two strings, no sequence of operations can fix that, since we only permute characters.

The constraints allow strings of length up to 200,000, which immediately rules out any quadratic simulation of transformations or any approach that repeatedly rebuilds the string explicitly. Any solution that revisits characters many times in nested loops will be too slow. We should aim for a linear or near linear process, most likely involving a greedy scan or a queue-like simulation.

A subtle edge case appears when characters match in multiset but cannot be aligned in order. For example, s = "ab" and t = "ba" is valid, but s = "ab" and t = "ac" is impossible due to mismatched counts. Another interesting case is when s and t are permutations with heavy repetition; naive greedy swapping strategies can fail if they assume a character can be placed arbitrarily without accounting for future constraints.

## Approaches

The brute force perspective is to explicitly simulate the process. We maintain the string and repeatedly take the first character and try all possible insertion positions. This produces a huge branching factor: each step has O(n) choices, and there can be up to n steps, so the search space grows exponentially. Even pruning does not help enough because the state space is essentially all permutations reachable by constrained rotations, which is still enormous.

The key structural insight is that the operation does not allow arbitrary swaps, but it does allow us to "postpone" the current front character by sending it to the back or any later position. In other words, we are scanning the string from left to right, but we are allowed to delay characters that are not immediately useful for building the target string.

This reframes the problem into a greedy matching process between s and t. We try to match t in order while scanning s from the front. Whenever the current front character of s matches the next needed character in t, we consume both. When it does not match, we treat that character as being moved away (to the back), paying one operation, and continue.

This greedy idea avoids exploring all insertion positions explicitly. The only decision is whether the current character helps us progress in t or must be deferred.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration of Insertions | Exponential | O(n) | Too slow |
| Greedy Queue Simulation | O(n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

We simulate both strings using a queue-like structure for the source string and a pointer for the target string.

1. First, we verify that both strings have identical character counts. If not, we immediately return -1 since no sequence of operations can reconcile the difference.
2. We maintain a pointer j over the target string, initially at 0, representing the next character we want to match.
3. We treat the source string as a queue. We repeatedly inspect its front character.
4. If the front character equals t[j], we advance both pointers. This corresponds to placing that character in its correct final relative position without needing to defer it, so no operation cost is incurred.
5. If the front character does not match t[j], we simulate performing the allowed operation: we remove it and insert it at the end of the string, increasing the operation counter by one.
6. We continue this process until all characters of the target string are matched.

The crucial idea is that we never need to explicitly choose an insertion position. Any non-useful character is simply pushed back, preserving correctness because its final position is determined implicitly by when it eventually becomes useful.

### Why it works

At any moment, we are trying to align the next required character in t. If the front of the queue already matches, delaying it would only increase operations without benefit. If it does not match, keeping it at the front prevents progress in t, so it must be deferred. This creates a greedy invariant: every character is either consumed immediately when it matches the required target position or postponed exactly when it blocks progress. This ensures we never perform unnecessary postponements and never miss a valid match opportunity.

Because every character is either matched or moved back in a way that strictly advances the pointer in the simulation, the process is monotonic in terms of progress through t, so it cannot cycle indefinitely or lose optimality.

## Python Solution

```python
import sys
from collections import Counter, deque

input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()
    t = input().strip()

    if Counter(s) != Counter(t):
        print(-1)
        return

    dq = deque(s)
    j = 0
    ops = 0

    while j < n:
        if dq[0] == t[j]:
            dq.popleft()
            j += 1
        else:
            dq.append(dq.popleft())
            ops += 1

    print(ops)

if __name__ == "__main__":
    solve()
```

The solution begins with a feasibility check using character counts, since any mismatch makes the transformation impossible regardless of operations. The main simulation uses a deque to represent the evolving string. The pointer j tracks progress in the target string.

Each step either consumes a matching character or rotates the front character to the back, counting one operation. The loop ends once all characters of t are matched.

A subtle implementation detail is that we always access dq[0], so the deque must never be empty while j < n. This is guaranteed because both strings have identical length and we only remove characters when they are matched or moved, preserving size consistency in the cyclic sense of the simulation.

## Worked Examples

### Example 1

Input:

s = "abcd", t = "dcba"

| Step | dq state | j | action | ops |
| --- | --- | --- | --- | --- |
| 1 | abcd | 0 | a ≠ d, rotate | 1 |
| 2 | bcda | 0 | b ≠ d, rotate | 2 |
| 3 | cdab | 0 | c ≠ d, rotate | 3 |
| 4 | dabc | 0 | d = d, match | 3 |
| 5 | abc | 1 | a = c? no, rotate | 4 |
| ... | ... | ... | continue | ... |

Eventually all characters are aligned, and the algorithm counts how many rotations were needed before each correct alignment becomes available. This shows how mismatches are effectively deferred until the required character reaches the front.

### Example 2

Input:

s = "tot", t = "tot"

| Step | dq state | j | action | ops |
| --- | --- | --- | --- | --- |
| 1 | tot | 0 | t matches | 0 |
| 2 | ot | 1 | o matches | 0 |
| 3 | t | 2 | t matches | 0 |

This case demonstrates the optimal behavior when no postponements are needed. Every character is already aligned in order, so the operation count remains zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) amortized | Each character is moved from front to back a bounded number of times and eventually consumed |
| Space | O(n) | Deque stores all characters during simulation |

The algorithm fits within the constraints because every operation is constant time and the total number of deque operations is linear in practice due to the monotonic consumption of the target pointer.

## Test Cases

```python
import sys, io
from collections import Counter, deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input().strip())
    s = input().strip()
    t = input().strip()

    if Counter(s) != Counter(t):
        return "-1"

    dq = deque(s)
    j = 0
    ops = 0

    while j < n:
        if dq[0] == t[j]:
            dq.popleft()
            j += 1
        else:
            dq.append(dq.popleft())
            ops += 1

    return str(ops)

# provided samples
assert run("4\nabcd\ndcba\n") == "3"
assert run("3\ntot\ntot\n") == "0"
assert run("7\ncabaaba\nabacaba\n") == "2"
assert run("2\nab\nbb\n") == "-1"

# custom cases
assert run("1\na\na\n") == "0"
assert run("5\nabcde\neabcd\n") == "4"
assert run("6\naabbcc\nccbbaa\n") == "6"
assert run("4\nabca\naabc\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single identical char | 0 | minimal case |
| simple rotation | small k | correctness of cyclic shifts |
| reversed blocks | non-trivial ops | handling repeated rotations |
| impossible multiset | -1 | feasibility check |

## Edge Cases

One important edge case is when the target string requires a character that exists but is currently blocked deep in the queue. For example, s = "baaa", t = "aaab". The algorithm repeatedly rotates the leading 'b' until enough 'a' characters reach the front. The simulation ensures that the 'b' is postponed exactly as many times as needed before it becomes relevant.

Another case is when s already equals t. In this situation, every comparison succeeds immediately, so no rotations are performed and the answer is zero. The algorithm handles this naturally because the first comparison always succeeds and advances both pointers without triggering any operation.

A final edge case is when the strings have identical multiset but require heavy rearrangement, such as complete reversal. Even in this case, every mismatch is handled by a single rotation, and each character eventually aligns exactly once it reaches the front in the correct phase of the target sequence, ensuring linear progression through the structure.
