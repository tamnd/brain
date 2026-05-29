---
title: "CF 266B - Queue at the School"
description: "We are given a queue made of boys and girls, represented as a string containing only B and G. Every second, each adjacent pair \"BG\" swaps positions and becomes \"GB\". The swaps happen simultaneously. That detail matters a lot."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graph-matchings", "implementation", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 266
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 163 (Div. 2)"
rating: 800
weight: 266
solve_time_s: 81
verified: true
draft: false
---

[CF 266B - Queue at the School](https://codeforces.com/problemset/problem/266/B)

**Rating:** 800  
**Tags:** constructive algorithms, graph matchings, implementation, shortest paths  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a queue made of boys and girls, represented as a string containing only `B` and `G`. Every second, each adjacent pair `"BG"` swaps positions and becomes `"GB"`.

The swaps happen simultaneously. That detail matters a lot. If a boy moves right because of one swap during the current second, he cannot immediately participate in another swap in the same second.

The task is to simulate the queue after exactly `t` seconds.

The constraints are very small. Both `n` and `t` are at most `50`, so even an `O(n * t)` simulation performs at most `2500` operations, which is trivial within the time limit. There is no need for advanced optimization or mathematical shortcuts.

The tricky part is not performance, it is implementing the simultaneous swaps correctly.

Consider this example:

```
3 1
BGG
```

The correct result is:

```
GBG
```

A careless left-to-right implementation might swap positions `0` and `1`, producing `GBG`, then continue scanning and swap the new `"BG"` again, producing `GGB`. That is wrong because a child may move at most once per second.

Another subtle case is consecutive boys:

```
5 1
BBGGG
```

The correct result is:

```
BGBGG
```

Only the second boy swaps with the first girl. The first boy cannot jump over two girls in one second.

The implementation must skip the next index after performing a swap, otherwise it may accidentally process newly created pairs during the same second.

## Approaches

The direct simulation approach mirrors the process described in the problem. For every second, scan the queue from left to right. Whenever we find `"BG"`, swap it into `"GB"`.

This works because the problem size is tiny. In the worst case we examine `n - 1` adjacent pairs during each of the `t` seconds, giving `O(n * t)` operations. With both values capped at `50`, the total work is extremely small.

The only challenge is preserving simultaneity. Suppose the queue is:

```
BGG
```

If we swap the first pair and then continue immediately to the next position, we would process the moved boy again in the same second. That changes the meaning of the simulation.

The key observation is that once we swap positions `i` and `i + 1`, the boy that moved to `i + 1` must not move again until the next second. So after performing a swap, we advance the pointer by `2` instead of `1`.

Because the constraints are already tiny, there is no need for a more complicated approach. The simulation itself is both simple and optimal for this problem size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(n * t) | O(n) | Accepted |
| Optimal simulation with index skipping | O(n * t) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `t`, and the queue string.
2. Convert the string into a mutable list of characters.

Strings are immutable in Python, so using a list makes swapping easy.
3. Repeat the simulation for `t` seconds.
4. During each second, scan the queue from left to right using index `i`.
5. If positions `i` and `i + 1` contain `"B"` and `"G"` respectively, swap them.

This represents the boy letting the girl move forward.
6. After a swap, increase `i` by `2`.

The boy that just moved right cannot participate in another swap during the same second.
7. Otherwise, increase `i` by `1`.
8. After all seconds are processed, join the character list back into a string and print it.

### Why it works

At every second, the algorithm processes exactly the pairs that were `"BG"` at the start of that moment. Skipping the next index after a swap prevents newly created pairs from being processed immediately, which matches the simultaneous-update rule from the problem statement.

Every valid swap is applied once, and no invalid extra movement is introduced. Since the algorithm reproduces the exact rules of the queue transformation for each second, the final queue is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, t = map(int, input().split())
    s = list(input().strip())

    for _ in range(t):
        i = 0

        while i < n - 1:
            if s[i] == 'B' and s[i + 1] == 'G':
                s[i], s[i + 1] = s[i + 1], s[i]
                i += 2
            else:
                i += 1

    print("".join(s))

solve()
```

The queue is stored as a list because Python strings cannot be modified in place. Swapping two characters in a list is constant time and keeps the implementation clean.

The outer loop simulates time passing one second at a time. The inner loop scans adjacent positions.

The most important implementation detail is the `i += 2` after a swap. Without it, the same boy could move multiple times during one second, which violates the rules.

The loop condition uses `i < n - 1` because we always inspect a pair `(i, i + 1)`. Accessing `i + 1` when `i == n - 1` would go out of bounds.

## Worked Examples

### Example 1

Input:

```
5 1
BGGBG
```

| Second | Queue | Action |
| --- | --- | --- |
| Start | BGGBG | Initial state |
| 1 | GBGGB | Swap positions 0-1, then 3-4 |

Output:

```
GBGGB
```

This trace shows why swaps are simultaneous. After the first swap, the moved boy is not processed again during the same second.

### Example 2

Input:

```
5 2
BGGBG
```

| Second | Queue |
| --- | --- |
| Start | BGGBG |
| 1 | GBGGB |
| 2 | GGBGB |

Output:

```
GGBGB
```

This demonstrates that boys gradually move right over multiple seconds, one position per second at most.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | We scan the queue once for each second |
| Space | O(n) | The queue is stored as a mutable character list |

With `n ≤ 50` and `t ≤ 50`, the algorithm performs at most a few thousand operations, which is far below the limit for a 2-second runtime.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, t = map(int, input().split())
    s = list(input().strip())

    for _ in range(t):
        i = 0

        while i < n - 1:
            if s[i] == 'B' and s[i + 1] == 'G':
                s[i], s[i + 1] = s[i + 1], s[i]
                i += 2
            else:
                i += 1

    return "".join(s)

# provided sample
assert run("5 1\nBGGBG\n") == "GBGGB", "sample 1"

# minimum size
assert run("1 1\nB\n") == "B", "single child"

# all equal values
assert run("5 3\nBBBBB\n") == "BBBBB", "all boys"

# multiple seconds
assert run("5 2\nBGGBG\n") == "GGBGB", "two-step simulation"

# catches incorrect double movement
assert run("3 1\nBGG\n") == "GBG", "simultaneous swap handling"

# boundary movement
assert run("4 1\nBBGG\n") == "BGBG", "adjacent boundary swaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / B` | `B` | Minimum-size input |
| `5 3 / BBBBB` | `BBBBB` | No swaps occur |
| `5 2 / BGGBG` | `GGBGB` | Multi-second simulation |
| `3 1 / BGG` | `GBG` | Prevents double movement in one second |
| `4 1 / BBGG` | `BGBG` | Correct adjacent swap handling |

## Edge Cases

Consider the input:

```
3 1
BGG
```

The algorithm starts at index `0` and sees `"BG"`, so it swaps them:

```
GBG
```

It then increases the index by `2`, moving directly past the swapped boy. The scan ends, and the final answer remains:

```
GBG
```

This correctly models simultaneous swaps. A buggy implementation using `i += 1` would continue scanning and incorrectly produce `GGB`.

Now consider:

```
5 1
BBGGG
```

The algorithm scans from left to right:

| Index | Pair | Action | Queue |
| --- | --- | --- | --- |
| 0 | BB | No swap | BBGGG |
| 1 | BG | Swap | BGBGG |
| 3 | GG | No swap | BGBGG |

The final answer is:

```
BGBGG
```

Only one boy moves during this second. The first boy does not jump across multiple girls, which matches the rules exactly.

Finally, consider a queue with no possible swaps:

```
4 5
GGGG
```

Every scanned pair is `"GG"`, so nothing changes during any second. The algorithm simply finishes with:

```
GGGG
```

This confirms that the implementation handles already-stable queues correctly.
