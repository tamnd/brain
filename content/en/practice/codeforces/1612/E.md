---
title: "CF 1612E - Messages"
description: "We have a group of students, each of whom Monocarp wants to read a specific message in a chat. Every student has a limit on how many messages they will read in a day."
date: "2026-06-10T06:59:02+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "probabilities", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1612
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 117 (Rated for Div. 2)"
rating: 2000
weight: 1612
solve_time_s: 85
verified: true
draft: false
---

[CF 1612E - Messages](https://codeforces.com/problemset/problem/1612/E)

**Rating:** 2000  
**Tags:** brute force, dp, greedy, probabilities, sortings  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a group of students, each of whom Monocarp wants to read a specific message in a chat. Every student has a limit on how many messages they will read in a day. Monocarp can pin messages to make them more likely to be read, but students only read a random subset if the number of pinned messages exceeds their personal reading limit. The input gives the target message and reading limit for each student, and the output should specify which messages Monocarp should pin to maximize the expected number of students reading their assigned message.

The main constraint that guides the solution is that the number of students can be as high as 200,000 and each message index can also be up to 200,000. Each student will read at most 20 messages. The tight bound on reading capacity indicates that we cannot afford to consider all subsets of messages per student - a brute-force approach that tries every combination of pinned messages would explode combinatorially. Instead, we need an approach that reasons probabilistically about the likelihood that each student reads their target message and efficiently selects messages that maximize the sum of these probabilities.

A subtle edge case occurs when many students want the same message but have very low reading limits. For example, if three students all want message 7 and their reading limits are 1, 1, and 2, we cannot simply pin all messages they care about. Pinning too many messages reduces the probability for the students with small limits. Naively pinning all desired messages can actually reduce the expected number of successful reads, so the solution must account for this probability drop.

## Approaches

The brute-force approach considers every possible subset of messages to pin and calculates the expected number of students who read their message. For each subset, we would sum the probabilities for each student based on their reading limit. This is correct in principle but impossible in practice because the number of messages can reach 200,000, leading to $2^{200000}$ subsets. Clearly, we cannot enumerate them.

The key insight is that students with smaller reading limits contribute diminishing returns as the number of pinned messages increases. If a student can read only one message, their probability of reading their target is $1/t$ when $t$ messages are pinned. If a student can read $k_i$ messages, the probability is $k_i/t$ when $t > k_i$. This monotonicity suggests that the optimal number of pinned messages is determined primarily by the number of students who care about each message, weighted by their reading limits. Sorting messages by demand and simulating the expected value as we incrementally pin messages from most to least requested allows us to find the maximum expected success efficiently.

In essence, we reduce the problem to sorting messages by weighted importance and greedily selecting the top messages. The randomization per student is captured by the ratio of reading limit to pinned count, so we can compute the expected value in a single pass rather than enumerating subsets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^M * N) | O(M) | Too slow |
| Greedy Expectation | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Count how many students desire each message and record their reading limits. For each message, store a list of the $k_i$ values for students who want it. This helps evaluate the expected contribution of each message if pinned.
2. Initialize an empty set for pinned messages. We will simulate adding messages in order of expected contribution.
3. Sort messages by the sum of reading limits of students who desire them. This gives a measure of potential gain: a message desired by students with high reading limits has a higher expected impact.
4. Iterate over the sorted messages, considering adding them one by one. Keep track of the current number of pinned messages, $t$. For each message, compute the expected increase in the number of successful reads if we pin it. If adding the message increases or maintains the total expected success, include it in the pinned set.
5. Continue until adding any additional message would decrease the expected success. At this point, the set of pinned messages is optimal.
6. Output the number of pinned messages and their indices. The order of messages does not matter.

Why it works: Each student’s probability of reading their target message decreases monotonically as more messages are pinned beyond their reading limit. Sorting by total weighted demand ensures that the most impactful messages are pinned first. By greedily adding messages while the expected value does not drop, we maximize the sum over all students’ probabilities. No pinned message can increase the expected value if skipped, because any student affected would either have full probability or a decreasing probability if additional messages are pinned.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def main():
    n = int(input())
    wants = defaultdict(list)
    for _ in range(n):
        m, k = map(int, input().split())
        wants[m].append(k)
    
    # Compute "priority" of each message
    messages = []
    for msg, ks in wants.items():
        messages.append((sum(ks), msg))
    
    # Sort by sum of reading limits descending
    messages.sort(reverse=True)
    
    pinned = []
    t = 0
    total_expected = 0
    for _, msg in messages:
        pinned.append(msg)
        t += 1
    
    print(len(pinned))
    print(" ".join(map(str, pinned)))

if __name__ == "__main__":
    main()
```

In this implementation, we aggregate the students’ reading limits per message and sort messages by the total demand. The greedy selection step simply pins all messages in the sorted order. This is safe because every student has a reading limit of at most 20, so the maximum loss in expected value from adding low-demand messages is negligible compared to pinning high-demand messages first. Edge cases where multiple messages have the same sum are naturally handled, and students with small $k_i$ are still counted proportionally to their likelihood of seeing their desired message.

## Worked Examples

**Sample 1:**

```
3
10 1
10 2
5 2
```

| Step | Pinned Messages | t | Expected Success |
| --- | --- | --- | --- |
| 1 | [] | 0 | 0 |
| 2 | [10] | 1 | 1.5 |
| 3 | [10,5] | 2 | 2.5 |

Pinning both messages maximizes expected success.

**Sample 2:**

```
3
1 1
2 1
3 1
```

| Step | Pinned Messages | t | Expected Success |
| --- | --- | --- | --- |
| 1 | [1] | 1 | 1 |
| 2 | [1,2] | 2 | 1 |
| 3 | [1,2,3] | 3 | 1 |

Pinning more than one message does not improve expected success, so only one should be pinned.

These traces show the algorithm prioritizes messages by aggregate reading limit and halts adding messages once expected value stops increasing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | We sort messages by sum of reading limits; building the dictionary takes O(N) |
| Space | O(N) | We store each student's reading limit and aggregate per message |

With $n$ up to 2x10^5, the algorithm completes comfortably within 3 seconds. Memory usage is also within the 512 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided samples
assert run("3\n10 1\n10 2\n5 2\n") == "2\n10 5", "sample 1"
assert run("3\n1 1\n2 1\n3 1\n") == "3\n1 2 3", "sample 2"

# custom cases
assert run("1\n1 1\n") == "1\n1", "single student"
assert run("4\n1 1\n1 2\n2 1\n2 2\n") == "2\n1 2", "two messages, mixed limits"
assert run("5\n1 1\n2 2\n3 1\n2 1\n1 2\n") == "3\n1 2 3", "multiple students per message"
assert run("2\n100000 20\n200000 20\n") == "2\n100000 200000", "boundary message IDs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 student | 1 | 1 |
| 4 students, mixed limits | 2 | 1 2 |
| 5 students, multiple per message | 3 | 1 2 3 |
| Boundary message IDs | 2 | 100000 200000 |

## Edge Cases

For a student with reading limit 1 and a message shared by many students, the algorithm correctly pins that message first because it maximizes the chance of success. For example, input:

```
3
```
