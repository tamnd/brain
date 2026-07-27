---
title: "CF 102784D - Ghost-or-Treat"
description: "We have a line of ghosts, where each ghost has an integer age. A move consists of choosing two neighboring ghosts whose ages are different. The older ghost defeats the younger one and remains in the line, but surviving makes it one year older. The younger ghost disappears."
date: "2026-07-27T19:54:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102784
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 1"
rating: 0
weight: 102784
solve_time_s: 81
verified: true
draft: false
---

[CF 102784D - Ghost-or-Treat](https://codeforces.com/problemset/problem/102784/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a line of ghosts, where each ghost has an integer age. A move consists of choosing two neighboring ghosts whose ages are different. The older ghost defeats the younger one and remains in the line, but surviving makes it one year older. The younger ghost disappears.

The question is whether Boo can choose the fights in some order so that eventually only one ghost remains.

The input gives the number of ghosts followed by their ages in their current order. The output is `YES` if there exists some sequence of fights that leaves exactly one ghost, and `NO` otherwise.

The constraint is small enough that we do not need advanced data structures. With at most 10,000 ghosts, a linear scan is easily affordable, but simulating fights directly is unnecessary because the operation has a very strong property. Any solution that tries every possible sequence of fights would explode because the number of possible choices grows rapidly after each removal.

The main edge cases come from situations where a fight cannot even begin. If there is only one ghost, the answer is immediately `YES` because no one needs to be removed. For example:

```
Input:
1
7

Output:
YES
```

A careless implementation that only searches for a possible fight would incorrectly return `NO`.

The other important case is when every ghost has the same age. For example:

```
Input:
3
5
5
5

Output:
NO
```

No two adjacent ghosts have different ages, so no operation is legal. The process stops with three ghosts instead of one.

A common mistake is to only check whether there are multiple different ages somewhere in the line. Adjacency matters for the first move. For example:

```
Input:
4
3
3
3
4

Output:
YES
```

The last two ghosts can fight immediately. However, if all values are equal, no such starting point exists.

# Approaches

The direct approach would be to simulate the process. We could try every possible adjacent pair, remove the younger ghost, increase the older one, and recursively continue until the line has one ghost or no moves are possible. This would be correct because it explores every possible sequence of choices.

The problem is that this search tree is enormous. In the worst case, many different pairs can be chosen at every stage. With 10,000 ghosts, even considering a tiny fraction of all possible sequences is impossible.

The key observation is that the first successful fight completely changes the situation. Suppose two adjacent ghosts have different ages. The older one wins and increases its age by one. If the older age was `x`, the survivor becomes `x + 1`, which is strictly larger than every age that existed before the fight.

This creates a unique strongest ghost. That ghost can now defeat any neighbor because it is always older than them. After every victory it becomes even older, so it can continue moving through the line until everyone else is gone.

Because of this, we do not need to find the exact sequence of fights. We only need to know whether a first fight exists. A first fight exists exactly when there is an adjacent pair with different ages.

The brute-force works because it follows all possible valid fight orders, but fails because there are too many choices. The observation that the first successful fight creates an unstoppable winner reduces the entire problem to checking adjacent differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of ghosts | O(N) recursion depth | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the ages of all ghosts. If there is only one ghost, return `YES` because the required final state is already reached.
2. Scan every adjacent pair of ghosts and compare their ages. If any pair has different ages, return `YES`.

The first unequal adjacent pair can fight. After that fight, the survivor becomes older than every ghost that existed before, so it can eliminate the entire remaining line.
3. If the scan finishes without finding any unequal adjacent pair, return `NO`.

In this situation every ghost has the same age, meaning no legal move exists at the start.

Why it works: If an unequal adjacent pair exists, the first fight creates a ghost whose age is larger than all original ages. Since every later opponent is no older than this ghost, it can always win the next fight and become even older. Thus every other ghost can eventually be removed. If no unequal adjacent pair exists, all ghosts have the same age and no fight is possible, so reducing the line is impossible.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ages = [int(input()) for _ in range(n)]

    if n == 1:
        print("YES")
        return

    for i in range(n - 1):
        if ages[i] != ages[i + 1]:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The code first handles the single-ghost case because no comparisons are needed there. Then it checks neighboring ghosts only, because a legal first move requires two adjacent ghosts with different ages.

The scan stops as soon as it finds a possible first fight. There is no need to simulate the remaining process because the winning ghost after that fight is guaranteed to dominate every future fight.

The loop uses `n - 1` comparisons, so the boundary is chosen carefully to avoid accessing an element past the end of the list.

# Worked Examples

For the first sample:

```
5
5
3
4
4
5
```

The scan behaves as follows:

| Index checked | Left age | Right age | Result |
| --- | --- | --- | --- |
| 0 | 5 | 3 | Different, answer is YES |

The first two ghosts can fight. The age `5` ghost survives and becomes age `6`, which is older than every other ghost. The trace demonstrates why only the existence of one valid first move matters.

For the second sample:

```
3
1
1
1
```

The scan checks every neighboring pair:

| Index checked | Left age | Right age | Result |
| --- | --- | --- | --- |
| 0 | 1 | 1 | No fight |
| 1 | 1 | 1 | No fight |

No legal move exists, so the answer is `NO`. This confirms the all-equal edge case.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each adjacent pair is checked once. |
| Space | O(N) | The input ages are stored in a list. |

The algorithm performs only a single pass over the ghosts, which easily fits the limit for `N = 10000`.

# Test Cases

```python
import sys
import io

def solve_input(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    n = int(input())
    ages = [int(input()) for _ in range(n)]

    if n == 1:
        ans = "YES"
    else:
        ans = "NO"
        for i in range(n - 1):
            if ages[i] != ages[i + 1]:
                ans = "YES"
                break

    sys.stdin = old_stdin
    return ans + "\n"

# provided samples
assert solve_input("""5
5
3
4
4
5
""") == "YES\n", "sample 1"

assert solve_input("""3
1
1
1
""") == "NO\n", "sample 2"

# custom cases
assert solve_input("""1
10
""") == "YES\n", "single ghost"

assert solve_input("""5
7
7
7
7
7
""") == "NO\n", "all equal values"

assert solve_input("""4
2
2
2
3
""") == "YES\n", "difference at boundary"

assert solve_input("""6
9
9
8
9
9
9
""") == "YES\n", "middle unequal pair"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 10` | `YES` | A line already containing one ghost is finished. |
| `5 / all 7s` | `NO` | No legal first move exists. |
| `2 2 2 3` | `YES` | A fight at the end of the line is enough. |
| `9 9 8 9 9 9` | `YES` | Any adjacent difference creates the final winner. |

# Edge Cases

When there is only one ghost, the algorithm returns `YES` immediately. For input:

```
1
42
```

there are no fights to perform, but the line already contains exactly one remaining ghost.

When all ghosts have identical ages, every adjacent comparison fails. For input:

```
4
6
6
6
6
```

the scan checks three pairs, and every pair has equal ages. Since the first fight cannot happen, the final state can never contain one ghost, so the algorithm returns `NO`.

When the only difference is near a boundary, the algorithm still succeeds. For input:

```
4
3
3
3
8
```

the last pair is unequal. The age `8` ghost defeats the age `3` ghost and becomes age `9`, after which it can defeat the remaining ghosts one by one. The scan finds this pair and returns `YES`.
