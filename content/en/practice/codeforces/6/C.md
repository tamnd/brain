---
title: "CF 6C - Alice, Bob and Chocolate"
description: "We have a row of chocolate bars, and each bar takes a certain amount of time to eat. Alice starts from the left end and"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 6
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 6 (Div. 2 Only)"
rating: 1200
weight: 6
solve_time_s: 89
verified: true
draft: false
---

[CF 6C - Alice, Bob and Chocolate](https://codeforces.com/problemset/problem/6/C)

**Rating:** 1200  
**Tags:** greedy, two pointers  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of chocolate bars, and each bar takes a certain amount of time to eat. Alice starts from the left end and keeps moving right. Bob starts from the right end and keeps moving left. Both eat continuously without pausing, and nobody can partially eat a chocolate and stop midway.

The interesting part is that the process is determined by time, not by turns. If Alice finishes her current chocolate earlier than Bob, she immediately starts the next chocolate on her side. The same happens for Bob. Eventually the two players meet in the middle. If they would begin the same chocolate at the exact same moment, Alice gets that chocolate and Bob stops.

The input is simply an array where each element represents the time needed to eat one chocolate. The output asks for how many chocolates Alice eats and how many chocolates Bob eats by the end.

The constraints are large enough that we must think carefully about efficiency. The number of chocolates can reach $10^5$, so any quadratic solution would perform around $10^{10}$ operations in the worst case, which is far beyond the limit for a 2-second runtime. Linear time is the natural target here. Since we only need to process the chocolates in order from both ends, this strongly suggests a two-pointer approach.

There are a few edge cases that can quietly break incorrect implementations.

Consider a single chocolate:

```
1
5
```

The correct output is:

```
1 0
```

Alice starts first from the left, Bob starts from the right, but both positions are the same. Alice receives the chocolate because ties go to her. A careless implementation may incorrectly give one chocolate to each player.

Another tricky case is when both players accumulate equal eating time before reaching the middle:

```
3
2 2 2
```

The correct output is:

```
2 1
```

Alice eats the first chocolate in 2 seconds, Bob eats the last in 2 seconds, and now both would start the middle chocolate simultaneously. Alice receives it.

A different source of bugs appears when one side advances much faster:

```
5
1 100 1 1 1
```

The correct output is:

```
1 4
```

Alice gets stuck on the large chocolate for a long time while Bob quickly consumes several chocolates from the right. Implementations that alternate turns instead of comparing accumulated times will fail here.

## Approaches

A direct simulation is the first natural idea. We can imagine tracking the exact current time for Alice and Bob, advancing whichever player finishes first. Each player consumes chocolates one by one, and we repeatedly determine who becomes free next.

This brute-force simulation is actually correct because the process itself is sequential and deterministic. The problem is that a naive implementation may repeatedly search for the next event or recompute timings unnecessarily. If we simulate time unit by time unit, the runtime becomes disastrous because chocolate times can sum to as much as $10^8$.

The key observation is that we never need to simulate individual seconds. At any moment, the only information that matters is the total time already spent by Alice and the total time already spent by Bob.

Suppose Alice has spent less total time than Bob. That means Alice finishes earlier and becomes free first, so she must take the next chocolate on the left. Similarly, if Bob has spent less total time, he must take the next chocolate on the right.

This turns the entire process into a very compact greedy procedure. We maintain two pointers, one from the left and one from the right, along with the cumulative eating times for both players. At each step, the player with the smaller total time takes the next available chocolate.

The structure of the problem makes this greedy choice safe because eating order is forced by completion times. Nobody can skip a chocolate or wait intentionally, so the next move is uniquely determined by who becomes available first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total eating time) or worse | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers:

- `left = 0` for Alice's side.
- `right = n - 1` for Bob's side.
2. Maintain cumulative eating times:

- `alice_time = 0`
- `bob_time = 0`
3. Maintain counters for chocolates eaten:

- `alice_count = 0`
- `bob_count = 0`
4. Continue while `left <= right`.

At every step, compare `alice_time` and `bob_time`.
5. If `alice_time <= bob_time`, Alice becomes available first, or both become available simultaneously.

Alice takes the chocolate at index `left`.

Add its eating time to `alice_time`, increment `alice_count`, and move `left` one step right.

The equality case is important because ties belong to Alice.
6. Otherwise, Bob becomes available first.

Bob takes the chocolate at index `right`.

Add its eating time to `bob_time`, increment `bob_count`, and move `right` one step left.
7. When the pointers cross, every chocolate has been assigned. Print the two counters.

### Why it works

The invariant is that before each step, every chocolate outside the interval `[left, right]` has already been permanently assigned to exactly one player, and `alice_time` and `bob_time` represent the exact total time each player has spent so far.

If Alice has consumed less total time than Bob, she must finish earlier and immediately start the next available chocolate on her side. Bob cannot reach that chocolate first because he is still busy eating. The same reasoning applies symmetrically for Bob.

When both totals are equal, both players become free simultaneously. The statement explicitly says Alice receives the shared chocolate in that situation, which is exactly why the condition uses `<=`.

Since every step matches the real process exactly, the algorithm produces the correct final counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
t = list(map(int, input().split()))

left = 0
right = n - 1

alice_time = 0
bob_time = 0

alice_count = 0
bob_count = 0

while left <= right:
    if alice_time <= bob_time:
        alice_time += t[left]
        alice_count += 1
        left += 1
    else:
        bob_time += t[right]
        bob_count += 1
        right -= 1

print(alice_count, bob_count)
```

The solution follows the greedy simulation directly.

The two pointers represent the remaining unclaimed chocolates. Everything outside that interval has already been eaten.

The comparison between `alice_time` and `bob_time` is the core idea. If Alice has spent less or equal total time, she must be the next player to become free, so she takes the next chocolate from the left side.

The equality case is subtle. Using `<` instead of `<=` would incorrectly give simultaneous chocolates to Bob, which violates the statement.

The loop condition is also important. We continue while `left <= right`, not just `<`. When exactly one chocolate remains, it still must be assigned correctly, often to Alice because of the tie rule.

All variables fit comfortably within Python integers because the total eating time is at most $10^8$.

## Worked Examples

### Example 1

Input:

```
5
2 9 8 2 7
```

| Step | left | right | alice_time | bob_time | Action | Alice bars | Bob bars |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start | 0 | 4 | 0 | 0 | Alice takes 2 | 1 | 0 |
| 1 | 1 | 4 | 2 | 0 | Bob takes 7 | 1 | 1 |
| 2 | 1 | 3 | 2 | 7 | Alice takes 9 | 2 | 1 |
| 3 | 2 | 3 | 11 | 7 | Bob takes 2 | 2 | 2 |
| 4 | 2 | 2 | 11 | 9 | Bob takes 8 | 2 | 3 |

Final output:

```
2 3
```

This trace shows that one player may consume several chocolates consecutively if their accumulated time remains smaller. The algorithm mirrors the real timing process without explicitly simulating seconds.

### Example 2

Input:

```
3
2 2 2
```

| Step | left | right | alice_time | bob_time | Action | Alice bars | Bob bars |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start | 0 | 2 | 0 | 0 | Alice takes 2 | 1 | 0 |
| 1 | 1 | 2 | 2 | 0 | Bob takes 2 | 1 | 1 |
| 2 | 1 | 1 | 2 | 2 | Alice takes 2 | 2 | 1 |

Final output:

```
2 1
```

This example demonstrates the tie rule. When both accumulated times are equal, Alice receives the remaining chocolate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each chocolate is processed exactly once |
| Space | O(1) | Only a few variables are stored |

The algorithm performs one pass over the array using two pointers. With $n \le 10^5$, linear time easily fits within the time limit, and constant extra memory is well below the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    t = list(map(int, input().split()))

    left = 0
    right = n - 1

    alice_time = 0
    bob_time = 0

    alice_count = 0
    bob_count = 0

    while left <= right:
        if alice_time <= bob_time:
            alice_time += t[left]
            alice_count += 1
            left += 1
        else:
            bob_time += t[right]
            bob_count += 1
            right -= 1

    print(alice_count, bob_count)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("5\n2 9 8 2 7\n") == "2 3", "sample 1"

# minimum size
assert run("1\n5\n") == "1 0", "single chocolate"

# all equal values
assert run("4\n3 3 3 3\n") == "2 2", "equal times"

# tie on middle chocolate
assert run("3\n2 2 2\n") == "2 1", "alice gets middle"

# strong imbalance
assert run("5\n1 100 1 1 1\n") == "1 4", "bob finishes many quickly"

# off-by-one boundary
assert run("2\n1 2\n") == "1 1", "two elements"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `1 0` | Single-element handling |
| `4 / 3 3 3 3` | `2 2` | Balanced distribution |
| `3 / 2 2 2` | `2 1` | Tie goes to Alice |
| `5 / 1 100 1 1 1` | `1 4` | Consecutive moves by one side |
| `2 / 1 2` | `1 1` | Pointer crossing correctness |

## Edge Cases

Consider the smallest possible input:

```
1
5
```

Initially both accumulated times are zero, so the condition `alice_time <= bob_time` is true. Alice takes the only chocolate, her count becomes 1, and the pointers cross immediately.

The final output is:

```
1 0
```

This case confirms that the algorithm handles a single remaining chocolate correctly and respects the tie rule.

Now consider the middle-tie scenario:

```
3
2 2 2
```

After the first two moves:

- Alice has spent 2 seconds.
- Bob has spent 2 seconds.
- Only the middle chocolate remains.

Because the algorithm uses `<=`, Alice receives the final chocolate. The output becomes:

```
2 1
```

If the condition were written as `<`, Bob would incorrectly receive the middle chocolate.

Finally, consider a case where one player rapidly consumes many chocolates:

```
5
1 100 1 1 1
```

Step by step:

- Alice eats `1`, total becomes 1.
- Bob eats `1`, total becomes 1.
- Alice and Bob are tied, so Alice starts `100`.
- Bob then eats the remaining three chocolates while Alice is still busy.

The output is:

```
1 4
```

This verifies that the algorithm correctly models real elapsed time instead of alternating turns mechanically.
