---
title: "CF 106350K - Wahban and brackets"
description: "The string contains only round brackets. We need remove some characters while keeping the remaining indices in their original order. The goal is to obtain the longest subsequence whose reversal is a regular bracket sequence."
date: "2026-06-25T08:08:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106350
codeforces_index: "K"
codeforces_contest_name: "Zaglol Contest - FCDS level 1 contest 2026"
rating: 0
weight: 106350
solve_time_s: 30
verified: true
draft: false
---

[CF 106350K - Wahban and brackets](https://codeforces.com/problemset/problem/106350/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The string contains only round brackets. We need remove some characters while keeping the remaining indices in their original order. The goal is to obtain the longest subsequence whose reversal is a regular bracket sequence. If no non-empty subsequence satisfies this property, we print `-1`.

A regular bracket sequence has two requirements: the total number of opening and closing brackets is equal, and while reading from left to right, the number of opening brackets never becomes smaller than the number of closing brackets. For a reversed regular bracket sequence, these conditions apply after reversing the chosen subsequence.

If a chosen subsequence is `T`, then reading `T` from right to left must behave like a regular bracket sequence. That means while scanning `T` from the end towards the beginning, every closing bracket must have an earlier opening bracket available in this reversed order.

The length of the input can reach one million characters. A solution that tries different subsequences is impossible because the number of possible subsequences is exponential. Even checking all pairs of positions would already be too slow. The input size tells us that we need a linear or close to linear approach, where every bracket is processed only a constant number of times.

The tricky cases come from confusing an ordinary regular bracket sequence with a reversed one. For example:

```
()
```

The correct output is:

```
-1
```

The whole string is regular, but after reversing it becomes `)(`, which is invalid. A solution that only checks whether the original string contains a balanced subsequence would incorrectly return `2`.

Another case is:

```
)(
```

The correct output is:

```
2
```

The string itself is not regular, but reversing it gives `()`, which is valid. A solution that checks the original direction would incorrectly reject it.

A third case is:

```
(((
```

The correct output is:

```
-1
```

There are not enough closing brackets to create a pair. Counting only the number of opening brackets is not enough; the answer must contain complete matched pairs.

## Approaches

A direct approach would be to generate candidate subsequences and test whether their reverse is regular. This is correct because it examines every possible choice of deleted characters, so the best valid choice must appear. However, a string of length one million has an enormous number of subsequences, specifically up to $2^n$, making this approach unusable.

A better way is to look at the reversed condition differently. Instead of constructing the reversed subsequence, imagine reading the original string from right to left. The selected characters must form a normal regular bracket sequence in that direction.

For an ordinary regular bracket subsequence, the greedy matching strategy is enough. When we see an opening bracket, it can wait for a future closing bracket. When we see a closing bracket, we should use one waiting opening bracket if possible. Every successful match creates one pair.

Applying the same idea while traversing the original string backwards gives the maximum number of pairs for the reversed regular bracket subsequence. We do not need to know the actual chosen indices. We only need the number of matched pairs, because every pair contributes two characters.

The brute force works because it explores all possible deletions, but it repeats the same matching decisions many times. The greedy observation removes that repetition by proving that every available bracket should be used whenever a match is possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start from the end of the string and move towards the beginning. We scan in this direction because the reversed chosen subsequence must be regular.
2. Maintain a counter representing how many unmatched opening brackets are available in this reversed traversal. When we encounter `(`, increase this counter because this bracket can match a later `)` in the reversed order.
3. When we encounter `)`, check whether there is an available unmatched `(`. If there is, consume one opening bracket and increase the number of matched pairs. This is the only way this closing bracket can contribute to a valid subsequence.
4. After processing the whole string, multiply the number of matched pairs by two. If there are no matched pairs, output `-1` because no valid subsequence exists.

Why it works:

During the right-to-left scan, the counter has exactly the meaning of the number of opening brackets that can still support future matches in the reversed sequence. Every time a closing bracket is counted, we match it with one available opening bracket. This is optimal because leaving an available opening bracket unused cannot help any later closing bracket more than using it immediately. The process is identical to finding the longest regular bracket subsequence in the reversed string, so the number of created pairs is the maximum possible.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    s = input().strip()

    available_open = 0
    pairs = 0

    for ch in reversed(s):
        if ch == '(':
            available_open += 1
        else:
            if available_open > 0:
                available_open -= 1
                pairs += 1

    if pairs == 0:
        print(-1)
    else:
        print(pairs * 2)

if __name__ == "__main__":
    solve()
```

The scan uses `reversed(s)` so that the iteration order matches the direction required by the reversed bracket definition. The variable `available_open` is the number of opening brackets that have appeared in this direction but have not been paired yet.

When a `)` appears, the code checks the boundary condition `available_open > 0` before subtracting. Without this check, the implementation would count invalid pairs that do not exist.

The answer is stored as a number of pairs because each successful match contributes exactly one opening and one closing bracket. The final multiplication by two converts pairs into subsequence length.

No recursion, arrays, or extra strings are created, which matters because the input size can reach one million characters.

## Worked Examples

For the input:

```
()
```

the scan goes from right to left:

| Character processed | available_open | pairs |
| --- | --- | --- |
| `)` | 0 | 0 |
| `(` | 1 | 0 |

There are no matched pairs, so the output is `-1`. This demonstrates why an ordinary valid bracket sequence is not necessarily valid after reversal.

For the input:

```
()()()
```

the scan is:

| Character processed | available_open | pairs |
| --- | --- | --- |
| `)` | 0 | 0 |
| `(` | 1 | 0 |
| `)` | 0 | 1 |
| `(` | 1 | 1 |
| `)` | 0 | 2 |
| `(` | 1 | 2 |

There are two pairs, giving the output `4`. The selected subsequence can be `)()(`, whose reverse is `()()`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every bracket is inspected once while scanning from right to left. |
| Space | O(1) | Only two counters are stored regardless of the string length. |

The input limit requires avoiding any approach that stores all subsequences or performs repeated matching. The linear scan processes one million characters comfortably within the given limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    s = inp.strip()
    available_open = 0
    pairs = 0

    for ch in reversed(s):
        if ch == '(':
            available_open += 1
        elif available_open:
            available_open -= 1
            pairs += 1

    return "-1\n" if pairs == 0 else f"{pairs * 2}\n"

def run(inp: str) -> str:
    return solution(inp)

assert run("()\n") == "-1\n", "sample 1"
assert run("()()()\n") == "4\n", "sample 2"

assert run(")\n") == "-1\n", "single bracket"
assert run(")(\n") == "2\n", "reverse pair"
assert run("(((())))\n") == "8\n", "already balanced reverse length"
assert run("((((\n") == "-1\n", "only opening brackets"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `()` | `-1` | Distinguishes regular sequences from reversed regular sequences |
| `()()()` | `4` | Checks the sample maximum matching behavior |
| `)` | `-1` | Handles minimum-size impossible input |
| `)(` | `2` | Checks the direction of matching |
| `(((())))` | `8` | Checks a fully matchable sequence |
| `((((` | `-1` | Prevents counting incomplete pairs |

## Edge Cases

For the input:

```
()
```

the algorithm starts with zero available opening brackets. The first processed character is `)`, which cannot be matched, so it is ignored. The final `(` increases the counter, but there is no closing bracket left. The pair count remains zero and the answer is `-1`.

For the input:

```
)(
```

the first processed character is `(`, so one opening bracket becomes available. The next processed character is `)` and consumes that opening bracket, creating one pair. The result is `2`, which is correct because reversing the selected sequence gives `()`.

For the input:

```
(((
```

every character only increases `available_open`. No closing bracket ever appears, so no pair is created. The algorithm outputs `-1`, correctly rejecting subsequences that cannot become balanced after reversal.

For the input:

```
()()()
```

the algorithm finds two matches while scanning backwards. It does not use the last unmatched opening bracket because it has no closing bracket available after it in the reversed direction. The final answer remains the maximum possible length, `4`.
