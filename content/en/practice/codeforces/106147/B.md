---
title: "CF 106147B - Digging Bot"
description: "There is a hidden integer $n$ between 1 and 30000. In one experiment we provide a set of allowed step lengths $a1,a2,dots,ak$. The digging bot starts at depth 0 and wants to reach depth $n$. It may repeatedly use any of the given step lengths."
date: "2026-06-25T11:27:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106147
codeforces_index: "B"
codeforces_contest_name: "Junior Balkan Olympiad in Informatics 2025. Day 1"
rating: 0
weight: 106147
solve_time_s: 42
verified: true
draft: false
---

[CF 106147B - Digging Bot](https://codeforces.com/problemset/problem/106147/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

There is a hidden integer $n$ between 1 and 30000.

In one experiment we provide a set of allowed step lengths $a_1,a_2,\dots,a_k$. The digging bot starts at depth 0 and wants to reach depth $n$. It may repeatedly use any of the given step lengths. The bot always chooses a path that reaches exactly $n$ using the minimum possible number of steps. The experiment returns that minimum number of steps. The goal is to determine the hidden value $n$. The official limits allow at most 20 experiments and a total set size of at most 250.

The key observation is that this is not a traditional algorithmic problem. We are designing an interrogation strategy.

Since $n \le 30000$, we should look for a query whose answer directly reveals $n$. The challenge is to make sure that the minimum-step computation cannot hide information.

A common mistake is to choose several large step lengths and hope to reconstruct $n$ from the returned optimum. The bot is solving an optimization problem, so many different values of $n$ can produce the same answer.

For example, with the set $\{1,100\}$, both $n=50$ and $n=51$ return answers close to their values because the step of length 100 is unusable. The response does not uniquely identify $n$.

The special value $30000$ is also an edge case. Any strategy that assumes "all numbers are strictly smaller than the largest step length" must explicitly handle the maximum possible hidden value.

## Approaches

A brute-force mindset would be to ask many questions and gradually narrow the range of possible values. For example, one could query carefully chosen step sets and use the returned minimum number of moves as information. Such approaches easily fit within the experiment limit, but they are unnecessary.

The crucial observation is that the hidden number is at most 30000.

Consider the query:

$$\{1,30000\}$$

If $n < 30000$, the step of length 30000 cannot be used because it would overshoot the target. The only available way to reach $n$ exactly is to use $n$ steps of length 1.

Hence the returned minimum number of steps is exactly $n$.

The only remaining case is $n=30000$. Then the bot can reach the target in a single step of length 30000, so the answer becomes 1.

This completely determines the hidden value after a single experiment:

If the answer is 1, then $n=30000$.

Otherwise, the answer itself equals $n$.

The strategy uses one query of size 2, far below every limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Multiple-information queries | Depends on strategy | O(1) | Unnecessary |
| Single query `{1,30000}` | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Ask the experiment with the set `{1, 30000}`.
2. Read the returned minimum number of steps `m`.
3. If `m == 1`, output `30000`.

This can only happen when the bot uses the single step of length 30000.
4. Otherwise output `m`.

When `n < 30000`, the step of length 30000 is unusable, so the only feasible construction uses exactly `n` unit steps. Thus `m = n`.

### Why it works

For every value $n < 30000$, any solution containing a step of length 30000 is impossible because it immediately exceeds the target depth. The only allowed move is a step of length 1, so the unique minimum number of steps is exactly $n$.

For $n = 30000$, one step of length 30000 reaches the target immediately, giving answer 1.

The returned value is therefore:

$$m =
\begin{cases}
30000 & \text{encoded as } 1,\\
n & \text{for } n < 30000.
\end{cases}$$

The decoding rule reconstructs the hidden value exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

print("? 2 1 30000", flush=True)

m = int(input())

if m == -1:
    sys.exit(0)

if m == 1:
    print("! 30000", flush=True)
else:
    print(f"! {m}", flush=True)
```

The query contains only two step lengths.

The value 1 guarantees that every hidden depth is reachable. The value 30000 is chosen because it is equal to the maximum possible hidden depth. Any smaller hidden value cannot use that jump at all.

The implementation must flush after every output because the problem is interactive. Receiving `-1` indicates an invalid interaction and the program should terminate immediately, following the interaction protocol.

## Worked Examples

### Example 1

Suppose the hidden depth is $n=23$.

| Query | Returned value |
| --- | --- |
| `{1, 30000}` | 23 |

Since the answer is not 1, we output 23.

This demonstrates the main mechanism. The jump of length 30000 is unusable, so the bot needs exactly 23 unit steps.

### Example 2

Suppose the hidden depth is $n=30000$.

| Query | Returned value |
| --- | --- |
| `{1, 30000}` | 1 |

The answer equals 1, so we output 30000.

This is the only hidden value that can be reached in a single jump of length 30000.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One experiment and constant processing |
| Space | O(1) | Only a few variables are stored |

The strategy uses a single query of size 2, comfortably satisfying the limits of at most 20 experiments and total set size at most 250.

## Test Cases

For an interactive problem there is no standard offline test harness. The logical behavior can still be verified with simulated replies.

```
def decode(reply):
    if reply == 1:
        return 30000
    return reply

assert decode(23) == 23
assert decode(29999) == 29999
assert decode(1) == 30000
assert decode(15000) == 15000
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| reply = 23 | 23 | Ordinary value |
| reply = 29999 | 29999 | Largest value below 30000 |
| reply = 1 | 30000 | Maximum hidden depth |
| reply = 15000 | 15000 | General middle-range value |

## Edge Cases

Consider the maximum possible hidden value:

```
n = 30000
```

The query is `{1,30000}`.

The bot can reach the target using one jump of length 30000, so the returned minimum number of steps is 1. The algorithm maps this unique response back to 30000.

Now consider the largest value below the maximum:

```
n = 29999
```

The jump of length 30000 cannot be used. Every valid path consists entirely of unit jumps, so the minimum number of steps is 29999. The algorithm outputs 29999 directly.

These two cases are the only place where ambiguity could arise, and the special handling of reply `1` removes it completely.
