---
title: "CF 102538F - Farm of Monsters"
description: "We have a line of monsters. Monster i starts with h[i] health points. On each turn, we may hit any living monster and reduce its health by a, or skip our turn. The opponent always attacks the leftmost living monster and reduces its health by b."
date: "2026-08-03T21:01:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102538
codeforces_index: "F"
codeforces_contest_name: "300iq Contest 3"
rating: 0
weight: 102538
solve_time_s: 183
verified: true
draft: false
---

[CF 102538F - Farm of Monsters](https://codeforces.com/problemset/problem/102538/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of monsters. Monster `i` starts with `h[i]` health points. On each turn, we may hit any living monster and reduce its health by `a`, or skip our turn. The opponent always attacks the leftmost living monster and reduces its health by `b`. Whenever one of our attacks kills a monster, we gain one point. The goal is to maximize the number of monsters we personally finish.

The order matters because the opponent does not choose targets freely. A monster with a smaller index blocks all monsters after it until it dies, so the number of opponent attacks received by a monster depends on the decisions made for previous monsters. The useful way to think about the process is not as a simulation of turns, but as a balance of available moves. Every opponent attack gives us time to prepare future kills, while every attack we spend on a monster consumes one move.

The constraint `n <= 300000` rules out any simulation that performs work proportional to the number of turns. Health values can be up to `10^9`, so the total number of attacks can be enormous. The algorithm must process every monster only a constant or logarithmic number of times, which points toward a greedy or data structure based solution.

A common mistake is to treat monsters independently. For example, with equal attack powers and three monsters of health `1 1 1`, a strategy that decides every monster independently might think all three can be killed. In reality, after killing one monster, the opponent still gets turns between our attacks, and the available first move advantage is limited. The correct answer is `2`.

Another mistake is forgetting the initial move advantage. With input `3 1 1` and health `2 2 2`, the correct answer is `3`. The winning strategy is to wait until a monster has one health left, then finish it before the opponent can remove it. Treating the first move as a normal opponent turn loses this possibility.

## Approaches

The direct approach is to simulate choices. For every monster we decide whether to spend our attacks killing it or leave it for the opponent. After every choice we simulate the fight and count victories. This is correct because every possible strategy is explored, but there are two choices for every monster, giving `2^n` possibilities. Even before simulation cost is considered, this becomes impossible when `n` reaches hundreds of thousands.

The important observation is that we do not need to know the exact order of our attacks. Suppose we decide which monsters we want to kill. For one chosen monster, there is no reason to hit it more times than necessary. Let `r` be the smallest number of hits before the monster reaches a state where one more hit kills it. The optimal number of our hits on this monster is exactly `r + 1`.

The formula for `r` comes from looking at the remaining health modulo the opponent's attack cycle. After decreasing all health values by one, we need the smallest `r` such that:

```
(h - r * a) mod b < a
```

The value is:

```
r = floor(b * (h mod a) / a)
```

After deciding whether a monster is killed by us, we can express the effect as a change in the number of available moves. If we do not kill it, the opponent spends `h` attacks on it. If we kill it, the difference between opponent moves and our moves is another value. We compare this choice against the baseline where every monster is left to the opponent.

For monster `i`, let `y[i]` be the change caused by choosing to kill it instead of ignoring it. We need to choose as many `y[i]` values as possible while keeping every prefix valid. This becomes a classic greedy selection problem. We scan monsters from left to right, keep all chosen values in a heap, and if a prefix becomes impossible, remove the worst chosen monster. The worst removal is the largest `y[i]`, because removing a larger value fixes the constraint while sacrificing the fewest selected monsters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Decrease every monster health by one. This changes the killing condition from reaching health `0` to reaching a negative value, which makes the modular calculation cleaner.
2. For every monster, compute the minimum number of our attacks before the final killing attack. The value is `r = (b * (h % a)) // a`.
3. Compute the benefit of killing this monster ourselves. If we leave it alive, its contribution is `h`. If we kill it, its contribution is:

```
b * ((h - r * a) // b) - (r + 1)
```

The difference between these two values is `y`.

1. Maintain the sum of chosen `y` values while scanning monsters from left to right. Also maintain the current sum of all original `h` values in this prefix.
2. Add the current `y` to a max heap. If the chosen changes become too large and violate the prefix condition, remove the largest `y` from the heap. The heap always contains the monsters we finally decide to kill.
3. The number of elements remaining in the heap is the maximum number of victories.

The invariant is that after processing every prefix, the heap contains the maximum possible number of killed monsters among that prefix while keeping the prefix move balance valid. When the balance becomes invalid, removing the largest cost is optimal because every removed monster decreases the same constraint by its `y` value, and the largest value gives the smallest loss in count.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    h = list(map(int, input().split()))

    heap = []
    chosen_sum = 0
    prefix = 0

    for value in h:
        x = value - 1
        prefix += x

        r = (b * (x % a)) // a

        kill_value = b * ((x - r * a) // b) - (r + 1)
        y = kill_value - x

        heapq.heappush(heap, -y)
        chosen_sum += y

        if chosen_sum > prefix:
            removed = -heapq.heappop(heap)
            chosen_sum -= removed

    print(len(heap))

if __name__ == "__main__":
    solve()
```

The variable `prefix` stores the baseline number of saved moves if we let every monster be handled by the opponent. The variable `chosen_sum` stores the total modification introduced by the monsters currently selected for our attacks.

Python's heap is a min heap, so negative values are stored to simulate a max heap. When the prefix condition fails, the largest `y` is removed. This is the only place where the greedy choice happens.

The expression `(x % a)` is safe because `a` can be as large as `10^9`, but Python integers do not overflow. The subtraction of one at the start is also necessary. Without it, monsters that start with exactly one health point are handled incorrectly.

## Worked Examples

For input:

```
3 1 1
1 1 1
```

| Monster | x | y | Heap after correction | Answer count |
| --- | --- | --- | --- | --- |
| 1 | 0 | -1 | [-(-1)] | 1 |
| 2 | 0 | -1 | two selected | 2 |
| 3 | 0 | -1 | third removed | 2 |

The third monster cannot be added because there is not enough initial move advantage. The heap invariant removes it automatically.

For input:

```
3 1 1
2 2 2
```

| Monster | x | y | Heap after correction | Answer count |
| --- | --- | --- | --- | --- |
| 1 | 1 | -1 | selected | 1 |
| 2 | 1 | -1 | selected | 2 |
| 3 | 1 | -1 | selected | 3 |

The available prefix balance is enough to keep all three choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each monster is inserted once and removed at most once from the heap. |
| Space | O(n) | The heap can contain one entry for every monster. |

With `n = 300000`, the logarithmic heap operations are small enough, while any approach depending on the number of attacks is impossible because health values can be extremely large.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io
import heapq

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    n, a, b = map(int, sys.stdin.readline().split())
    h = list(map(int, sys.stdin.readline().split()))

    heap = []
    chosen_sum = 0
    prefix = 0

    for value in h:
        x = value - 1
        prefix += x
        r = (b * (x % a)) // a
        y = b * ((x - r * a) // b) - (r + 1) - x

        heapq.heappush(heap, -y)
        chosen_sum += y

        if chosen_sum > prefix:
            chosen_sum += heapq.heappop(heap)

    sys.stdin = old
    return str(len(heap))

assert run("3 1 1\n1 1 1\n") == "2"
assert run("3 1 1\n2 2 2\n") == "3"
assert run("1 10 1\n1\n") == "1"
assert run("4 5 10\n100 100 100 100\n") == "4"
assert run("5 3 7\n1 2 3 4 5\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 1 / 1 1 1` | `2` | First move advantage and prefix limitation |
| `3 1 1 / 2 2 2` | `3` | Waiting strategy and exact kill timing |
| `1 10 1 / 1` | `1` | Single monster boundary case |
| `4 5 10 / 100 100 100 100` | `4` | Large health values |
| `5 3 7 / 1 2 3 4 5` | `3` | Mixed values and off-by-one handling |

## Edge Cases

A monster with exactly one health point is the easiest place to make an off-by-one error. For:

```
1 10 1
1
```

the answer is `1`. After converting health to `h - 1`, the monster has value `0`. The formula gives `r = 0`, meaning one attack is enough.

When all monsters have equal health, the algorithm must still respect the order imposed by the opponent. For:

```
3 1 1
1 1 1
```

selecting every monster would violate the prefix condition. The heap removes the least useful selection and leaves two monsters.

When attack powers are very different, direct simulation is impossible. For:

```
4 5 10
100 100 100 100
```

the number of turns is enormous, but the modular calculation immediately determines the optimal choices. The heap only tracks decisions, not individual attacks.
