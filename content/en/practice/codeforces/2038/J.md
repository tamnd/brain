---
title: "CF 2038J - Waiting for..."
description: "We process a timeline of events at a bus stop. There are two kinds of events. A P x event means x ordinary passengers arrive and start waiting. A B x event means a bus arrives with x free seats. When a bus arrives, ordinary passengers always board before Monocarp."
date: "2026-06-08T10:07:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2038
codeforces_index: "J"
codeforces_contest_name: "2024-2025 ICPC, NERC, Southern and Volga Russian Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 800
weight: 2038
solve_time_s: 108
verified: true
draft: false
---

[CF 2038J - Waiting for...](https://codeforces.com/problemset/problem/2038/J)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We process a timeline of events at a bus stop.

There are two kinds of events. A `P x` event means `x` ordinary passengers arrive and start waiting. A `B x` event means a bus arrives with `x` free seats.

When a bus arrives, ordinary passengers always board before Monocarp. If there are more waiting passengers than seats, only as many passengers as possible board and the rest stay in the queue. If all waiting passengers fit, they all leave the stop.

Monocarp is special because he may choose whether to board a bus that still has a free seat after all ordinary passengers have boarded. He can skip such a bus and continue waiting for a later one.

For every bus event, we must determine whether there exists some sequence of choices by Monocarp that allows him to board that specific bus.

The number of events is at most 1000, which is very small. Even an $O(n^2)$ solution would perform at most about one million operations. That means we do not need sophisticated data structures or advanced optimization. The challenge is understanding what information actually matters.

The subtle part is that Monocarp's decisions affect only one thing: whether he is still waiting when a future bus arrives. Ordinary passengers behave deterministically. Their queue evolves the same way regardless of Monocarp's choices.

A common mistake is to simulate Monocarp greedily, for example always boarding the first available bus. Consider:

```
P 2
B 3
B 1
```

The correct answers are:

```
YES
YES
```

Monocarp can board the first bus because one seat remains after the two passengers enter. He can also choose to skip it and board the second bus. A simulation that permanently commits him to the first bus would incorrectly print `NO` for the second bus.

Another easy mistake is forgetting that passengers who cannot fit remain waiting:

```
P 10
B 3
B 8
```

The correct answers are:

```
NO
YES
```

After the first bus, seven passengers are still waiting. When the second bus arrives, all seven board, leaving one free seat for Monocarp.

A third edge case occurs when no ordinary passengers are waiting:

```
B 1
```

The answer is:

```
YES
```

The bus has a free seat immediately, so Monocarp may board it.

## Approaches

A brute-force view is to consider every bus independently. For a particular bus, we could replay all previous events, track the number of waiting passengers, and check whether that bus has a spare seat after serving them. This is correct because ordinary passengers are the only factor determining seat availability. If the bus has at least one spare seat, Monocarp can simply choose not to board any earlier bus and take this one instead.

With $m$ buses and $n$ total events, replaying the history for every bus costs $O(nm)$, which becomes $O(n^2)$ in the worst case. With $n \le 1000$, this is already fast enough.

The key observation is that we do not even need to recompute histories. The queue of ordinary passengers evolves independently of Monocarp. We can process events once, maintaining the current number of waiting passengers.

Suppose a bus arrives with `b` seats and there are `wait` passengers currently at the stop.

If `b > wait`, then after all ordinary passengers board, at least one seat remains. Monocarp can take this bus by simply continuing to wait until now. The answer is `YES`.

If `b <= wait`, every seat is consumed by ordinary passengers. Monocarp has no chance to board this bus, so the answer is `NO`.

After answering, the ordinary queue must be updated. The bus removes `min(wait, b)` passengers, leaving `max(0, wait - b)`.

This single-pass simulation gives the result immediately for every bus.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `wait = 0`, the number of ordinary passengers currently waiting.
2. Process events in chronological order.
3. If the event is `P x`, add these passengers to the queue by setting `wait += x`.
4. If the event is `B x`, compare the bus capacity with the current queue size.
5. If `x > wait`, then some seat remains after all ordinary passengers board. Output `YES`.

Monocarp can always choose to ignore every earlier opportunity and still be present for this bus.
6. Otherwise output `NO`.

Every seat is occupied by ordinary passengers, so Monocarp never gets a chance to enter.
7. Update the passenger queue after the bus leaves by setting `wait = max(0, wait - x)`.

This removes exactly the passengers who managed to board.

### Why it works

The crucial invariant is that `wait` always equals the number of ordinary passengers currently waiting at the stop.

Monocarp never affects this quantity because ordinary passengers board before him and his decisions do not change how many ordinary passengers arrive or leave.

For a bus with `b` seats, ordinary passengers occupy exactly `min(wait, b)` seats. A free seat exists for Monocarp exactly when

$$b - \min(wait, b) > 0$$

which is equivalent to `b > wait`.

If `b > wait`, Monocarp may board this bus. If `b <= wait`, all seats are consumed before his turn arrives. Since the algorithm checks precisely this condition for every bus while maintaining the correct passenger count, every answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    wait = 0
    ans = []

    for _ in range(n):
        typ, val = input().split()
        val = int(val)

        if typ == 'P':
            wait += val
        else:
            if val > wait:
                ans.append("YES")
            else:
                ans.append("NO")

            wait = max(0, wait - val)

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The variable `wait` stores exactly the number of ordinary passengers currently waiting.

For passenger events we simply add to this count.

For bus events we first answer the query using the current queue size. The order matters. The decision depends on how many passengers are waiting before anyone boards the arriving bus.

After producing the answer, we update the queue. If the bus has enough seats, all waiting passengers leave and `wait` becomes zero. Otherwise, exactly `val` passengers board and `wait` decreases by `val`.

All arithmetic easily fits into Python integers. Even though a single event may add up to $10^6$ passengers, the total remains far below Python's limits.

## Worked Examples

### Example 1

Input:

```
10
P 2
P 5
B 8
P 14
B 5
B 9
B 3
P 2
B 1
B 2
```

| Event | wait before | Action | Output | wait after |
| --- | --- | --- | --- | --- |
| P 2 | 0 | add passengers | - | 2 |
| P 5 | 2 | add passengers | - | 7 |
| B 8 | 7 | 8 > 7 | YES | 0 |
| P 14 | 0 | add passengers | - | 14 |
| B 5 | 14 | 5 ≤ 14 | NO | 9 |
| B 9 | 9 | 9 ≤ 9 | NO | 0 |
| B 3 | 0 | 3 > 0 | YES | 0 |
| P 2 | 0 | add passengers | - | 2 |
| B 1 | 2 | 1 ≤ 2 | NO | 1 |
| B 2 | 1 | 2 > 1 | YES | 0 |

Outputs:

```
YES
NO
NO
YES
NO
YES
```

This trace shows that only the current passenger queue matters. Monocarp's earlier choices never affect future seat availability.

### Example 2

Input:

```
5
P 10
B 3
B 8
P 1
B 1
```

| Event | wait before | Action | Output | wait after |
| --- | --- | --- | --- | --- |
| P 10 | 0 | add passengers | - | 10 |
| B 3 | 10 | 3 ≤ 10 | NO | 7 |
| B 8 | 7 | 8 > 7 | YES | 0 |
| P 1 | 0 | add passengers | - | 1 |
| B 1 | 1 | 1 ≤ 1 | NO | 0 |

Outputs:

```
NO
YES
NO
```

This example demonstrates the case where a bus removes only part of the queue. The remaining passengers continue waiting and affect later buses.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each event is processed exactly once |
| Space | O(1) | Only a few variables are maintained, excluding output storage |

With at most 1000 events, the linear solution is easily within the time limit. Memory usage is constant and negligible compared to the available 512 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    wait = 0
    ans = []

    for _ in range(n):
        typ, val = input().split()
        val = int(val)

        if typ == "P":
            wait += val
        else:
            ans.append("YES" if val > wait else "NO")
            wait = max(0, wait - val)

    return "\n".join(ans)

# provided sample
assert run(
"""10
P 2
P 5
B 8
P 14
B 5
B 9
B 3
P 2
B 1
B 2
"""
) == """YES
NO
NO
YES
NO
YES""", "sample 1"

# minimum input
assert run(
"""1
B 1
"""
) == "YES", "single bus"

# exact equality
assert run(
"""2
P 5
B 5
"""
) == "NO", "no seat remains for Monocarp"

# passengers remain after first bus
assert run(
"""3
P 10
B 3
B 8
"""
) == """NO
YES""", "carry-over queue"

# consecutive buses with empty stop
assert run(
"""3
B 1
B 2
B 3
"""
) == """YES
YES
YES""", "all buses available"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `B 1` | `YES` | Smallest valid input |
| `P 5, B 5` | `NO` | Equality case, no spare seat |
| `P 10, B 3, B 8` | `NO YES` | Remaining passengers persist |
| `B 1, B 2, B 3` | `YES YES YES` | Empty queue across multiple buses |

## Edge Cases

Consider the equality case:

```
2
P 5
B 5
```

Before the bus arrives, `wait = 5`. The bus has exactly five seats. All five seats are occupied by ordinary passengers, leaving zero seats. The algorithm checks `5 > 5`, which is false, and outputs:

```
NO
```

This avoids the common mistake of using `>=` instead of `>`.

Consider a partially served queue:

```
3
P 10
B 3
B 8
```

Initially `wait = 10`. After the first bus, the algorithm outputs `NO` and updates `wait` to `7`. For the second bus, `8 > 7`, so it outputs `YES`. The remaining passengers from the first bus are correctly preserved.

Consider multiple available buses:

```
3
P 2
B 3
B 1
```

At the first bus, `3 > 2`, so the answer is `YES`. After the bus departs, the queue becomes empty. At the second bus, `1 > 0`, so the answer is also `YES`.

This confirms that we are not simulating a single fixed decision by Monocarp. Each bus is evaluated independently under the question "could Monocarp choose to take this bus?", which is exactly what the problem asks.
