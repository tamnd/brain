---
title: "CF 476B - Dreamoon and WiFi"
description: "Drazil sends a sequence of movement commands. Each '+' moves Dreamoon one step to the right and each '-' moves one step to the left. We know the original command string and also the string that Dreamoon receives. The received string may contain '?"
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "combinatorics", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 476
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 272 (Div. 2)"
rating: 1300
weight: 476
solve_time_s: 95
verified: true
draft: false
---

[CF 476B - Dreamoon and WiFi](https://codeforces.com/problemset/problem/476/B)

**Rating:** 1300  
**Tags:** bitmasks, brute force, combinatorics, dp, math, probabilities  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

Drazil sends a sequence of movement commands. Each `'+'` moves Dreamoon one step to the right and each `'-'` moves one step to the left.

We know the original command string and also the string that Dreamoon receives. The received string may contain `'?'` characters, representing commands that could not be recognized. For every `'?'`, Dreamoon independently chooses `'+'` or `'-'` with equal probability.

The task is to compute the probability that Dreamoon finishes at exactly the same position as he would have reached if he had followed the original command sequence.

The strings have length at most 10. That constraint completely changes the nature of the problem. Even if every character in the received string is `'?'`, there are only $2^{10} = 1024$ possible interpretations. Enumerating every possibility is trivial within the time limit.

The main challenge is not efficiency but correctly counting probabilities. Every assignment of `'?'` characters is equally likely because each unknown command is determined by an independent fair coin toss.

A common mistake is to compare the strings character-by-character instead of comparing final positions. For example:

```
s1 = "++--"
s2 = "+?+-"
```

Different command sequences may still produce the same final position. The destination matters, not the exact sequence of moves.

Another easy mistake is forgetting that all assignments are equally probable. Consider:

```
s1 = "+"
s2 = "?"
```

There are two possible outcomes, `'+'` and `'-'`. Only one reaches the target position, so the answer is `0.5`, not `1`.

A third edge case occurs when the target position is impossible to reach regardless of how the `'?'` characters are chosen:

```
s1 = "+++"
s2 = "?--"
```

The target position is `+3`. The received string can only end at positions `-1` or `-3`. The correct probability is `0`.

## Approaches

The most direct solution is brute force.

First compute the destination that Drazil intended. Then consider every possible replacement of the `'?'` characters in the received string. For each assignment, simulate the resulting movement sequence and compute its final position. Count how many assignments reach the target position.

If there are `k` unknown commands, there are exactly `2^k` assignments. Since the string length never exceeds 10, the worst case is only 1024 assignments. Even a straightforward recursive search is extremely fast.

The reason this brute-force approach works is that each assignment corresponds to one equally likely outcome of the coin tosses. If `good` assignments reach the target and there are `2^k` total assignments, the desired probability is:

$$\frac{good}{2^k}$$

There is also a combinatorial observation. Instead of enumerating assignments, one could compute how many `'+'` choices are needed among the unknown positions and use binomial coefficients. That works because only the final displacement matters.

For this problem, the tiny constraint makes enumeration simpler and easier to implement correctly. It is already optimal enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(2^k \cdot n) | O(k) | Accepted |
| Combinatorial Counting | O(n) | O(1) | Accepted |

Here `k` is the number of `'?'` characters and `n ≤ 10`.

## Algorithm Walkthrough

1. Compute the target position produced by the original string.

Treat `'+'` as `+1` and `'-'` as `-1`, then sum all movements.
2. Count how many `'?'` characters appear in the received string.

These positions are the only uncertain parts of the process.
3. Use depth-first search to generate every possible replacement of the unknown commands.

At each `'?'`, branch into two possibilities: `'+'` and `'-'`.
4. When all positions have been processed, compute the resulting final position.

If it equals the target position, increase the count of successful assignments.
5. Keep track of the total number of assignments explored.

Every leaf of the recursion corresponds to one equally likely outcome.
6. Output:

$$\frac{\text{successful assignments}}{\text{total assignments}}$$

### Why it works

Each `'?'` represents an independent fair coin toss. Replacing all unknown positions generates exactly the sample space of possible outcomes. The recursion visits every outcome once and only once.

For every outcome, we check whether its final position equals the target position. The number of successful outcomes divided by the total number of outcomes is precisely the definition of probability when all outcomes are equally likely. Since every assignment of the unknown commands has probability $(1/2)^k$, counting favorable assignments is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

s1 = input().strip()
s2 = input().strip()

target = 0
for ch in s1:
    target += 1 if ch == '+' else -1

good = 0
total = 0

def dfs(idx, pos):
    global good, total

    if idx == len(s2):
        global target
        total += 1
        if pos == target:
            good += 1
        return

    if s2[idx] == '+':
        dfs(idx + 1, pos + 1)
    elif s2[idx] == '-':
        dfs(idx + 1, pos - 1)
    else:
        dfs(idx + 1, pos + 1)
        dfs(idx + 1, pos - 1)

dfs(0, 0)

print("{:.12f}".format(good / total))
```

The first part computes the destination intended by Drazil.

The recursive function processes the received string from left to right. The parameter `pos` stores the position reached after processing the prefix ending at index `idx - 1`.

For known commands there is only one continuation. For `'?'` there are two continuations, corresponding to the two equally likely outcomes of the coin toss.

When the recursion reaches the end of the string, one complete assignment has been constructed. We increment the total count and check whether the resulting position matches the target.

The answer is the ratio of successful assignments to all assignments. Since the number of assignments is at most 1024, recursion is completely safe.

## Worked Examples

### Sample 1

Input:

```
++-+-
+-+-+
```

Target position:

| Character | Running Position |
| --- | --- |
| + | 1 |
| + | 2 |
| - | 1 |
| + | 2 |
| - | 1 |

Target = 1

Received string:

| Character | Running Position |
| --- | --- |
| + | 1 |
| - | 0 |
| + | 1 |
| - | 0 |
| + | 1 |

Final position = 1.

There are no unknown commands, so there is exactly one possible outcome. It reaches the target, giving probability `1/1 = 1`.

### Sample 2

Input:

```
+-+-
+-??
```

Target position:

| Character | Running Position |
| --- | --- |
| + | 1 |
| - | 0 |
| + | 1 |
| - | 0 |

Target = 0

Possible assignments of the two unknown commands:

| Assignment | Final Position | Success |
| --- | --- | --- |
| +-++ | 2 | No |
| +-+- | 0 | Yes |
| +--+ | 0 | Yes |
| +--- | -2 | No |

We have 2 successful assignments out of 4 total assignments.

$$\frac{2}{4}=0.5$$

This example shows why counting final positions is the key observation. Two different assignments reach the same destination and both contribute to the probability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^k · n) | Enumerate every assignment of the `k` unknown commands and process a string of length `n` |
| Space | O(k) | Recursion depth equals the number of processed characters |

Since `n ≤ 10`, the maximum number of assignments is only 1024. The algorithm runs comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s1 = input().strip()
    s2 = input().strip()

    target = sum(1 if c == '+' else -1 for c in s1)

    good = 0
    total = 0

    def dfs(idx, pos):
        nonlocal good, total

        if idx == len(s2):
            total += 1
            if pos == target:
                good += 1
            return

        if s2[idx] == '+':
            dfs(idx + 1, pos + 1)
        elif s2[idx] == '-':
            dfs(idx + 1, pos - 1)
        else:
            dfs(idx + 1, pos + 1)
            dfs(idx + 1, pos - 1)

    dfs(0, 0)
    return "{:.12f}".format(good / total)

# sample 1
assert run("++-+-\n+-+-+\n") == "1.000000000000"

# sample 2 from statement explanation
assert run("+-+-\n+-??\n") == "0.500000000000"

# minimum length
assert run("+\n+\n") == "1.000000000000"

# one unknown command
assert run("+\n?\n") == "0.500000000000"

# impossible target
assert run("+++\n?--\n") == "0.000000000000"

# all unknowns, target position 0
assert run("+-\n??\n") == "0.500000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `+\n+\n` | `1.000000000000` | Smallest possible instance |
| `+\n?\n` | `0.500000000000` | Single coin toss |
| `+++\n?--\n` | `0.000000000000` | Unreachable target position |
| `+-\n??\n` | `0.500000000000` | Multiple assignments reaching target |

## Edge Cases

Consider:

```
+
?
```

The target position is `+1`. The unknown command can become either `'+'` or `'-'`. The recursion generates exactly two assignments. One reaches position `+1`, the other reaches `-1`. The algorithm returns `1/2 = 0.5`.

Consider:

```
+++
?--
```

The target position is `+3`. The only possible final positions from the received string are `-1` and `-3`. During enumeration, none of the assignments match the target. The successful count remains zero, so the answer is `0.0`.

Consider:

```
+-
??
```

The target position is `0`. The recursion explores four assignments. Two end at position `0`, one at `+2`, and one at `-2`. The algorithm counts two successful assignments and outputs `2/4 = 0.5`.

These examples cover the tricky situations where probabilities are fractional, where the target is impossible, and where multiple distinct assignments lead to the same destination. The counting approach handles all of them naturally.
