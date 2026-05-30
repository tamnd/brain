---
title: "CF 469A - I Wanna Be the Guy"
description: "We have a game with levels numbered from 1 to n. Little X can complete some subset of these levels, and Little Y can complete another subset. They decide to cooperate, which means a level is considered passable if at least one of them can complete it."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 469
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 268 (Div. 2)"
rating: 800
weight: 469
solve_time_s: 98
verified: true
draft: false
---

[CF 469A - I Wanna Be the Guy](https://codeforces.com/problemset/problem/469/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a game with levels numbered from 1 to _n_. Little X can complete some subset of these levels, and Little Y can complete another subset. They decide to cooperate, which means a level is considered passable if at least one of them can complete it.

The task is simply to determine whether their combined abilities cover every level of the game. If every level from 1 through _n_ can be completed by either X or Y, we print `"I become the guy."`. Otherwise, at least one level remains impossible for both players, and we print `"Oh, my keyboard!"`.

The constraints are very small. The number of levels is at most 100, so even relatively inefficient approaches would run comfortably within the time limit. We do not need sophisticated data structures or advanced algorithms. A straightforward implementation that checks coverage of all levels is more than sufficient.

A few edge cases are easy to overlook.

Suppose one player can pass no levels at all.

Input:

```
1
0
1 1
```

The correct output is:

```
I become the guy.
```

Even though X contributes nothing, Y alone covers the only level.

Another case is when both players list some of the same levels.

Input:

```
4
2 1 2
2 2 3
```

The correct output is:

```
Oh, my keyboard!
```

Levels 1, 2, and 3 are covered, but level 4 is missing. A careless implementation that only counts how many numbers were read could incorrectly think four entries imply four covered levels.

A final edge case occurs when neither player covers every level individually, but together they do.

Input:

```
4
2 1 2
2 3 4
```

The correct output is:

```
I become the guy.
```

Checking each player separately would fail here. We must consider the union of their reachable levels.

## Approaches

The most direct brute-force idea is to examine every level from 1 through _n_. For each level, scan X's list and Y's list to see whether either player can complete it. If some level is absent from both lists, the answer is negative.

This approach is correct because it explicitly verifies the condition required by the problem: every level must be covered. With at most 100 levels and at most 100 entries per list, the worst case performs roughly 100 × 200 = 20,000 comparisons, which is already fast enough.

We can make the solution cleaner by observing that we only care whether a level appears at least once among both players' lists. Duplicate appearances do not matter. This naturally suggests using a set.

We insert every level that X can pass into a set, then insert every level that Y can pass into the same set. The set automatically stores each level only once. If the size of the set becomes _n_, then every level is represented. Otherwise, some level is missing.

The brute-force method works because it directly checks coverage level by level. The key observation is that coverage is exactly the same as the union of the two players' level sets. Representing that union explicitly lets us answer the question with a single size comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(p + q)) | O(1) | Accepted |
| Optimal | O(p + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of levels, `n`.
2. Read Little X's line. The first number is `p`, followed by the `p` levels X can complete.
3. Read Little Y's line. The first number is `q`, followed by the `q` levels Y can complete.
4. Create an empty set.
5. Insert all levels from X's list into the set.

The set keeps only unique levels, which is exactly what we need.
6. Insert all levels from Y's list into the same set.

After this step, the set represents the union of levels passable by either player.
7. Compare the size of the set with `n`.

If the set contains exactly `n` distinct levels, every level from 1 through `n` is covered.
8. Print `"I become the guy."` if all levels are covered. Otherwise print `"Oh, my keyboard!"`.

### Why it works

The set contains precisely the levels that at least one player can pass. Every level inserted by X or Y appears in the set, and no other levels appear there.

If the set size equals `n`, then all levels from 1 through `n` are present in the union, meaning the players can collectively complete the entire game.

If the set size is smaller than `n`, at least one level is absent from the union. Neither player can complete that level, so finishing the entire game is impossible.

Since the algorithm checks exactly the union required by the problem statement, it always produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    x_data = list(map(int, input().split()))
    y_data = list(map(int, input().split()))

    levels = set()

    for level in x_data[1:]:
        levels.add(level)

    for level in y_data[1:]:
        levels.add(level)

    if len(levels) == n:
        print("I become the guy.")
    else:
        print("Oh, my keyboard!")

solve()
```

The first line reads the total number of levels. The next two lines contain the players' information. The first value on each line is a count and is not itself a level number, so we skip it by slicing from index 1 onward.

A set is used because we only care whether a level is covered, not how many times it appears. If both players can pass level 2, the set still stores only one copy of 2.

The final comparison checks whether the union contains all `n` levels. Since levels are numbered from 1 through `n`, having `n` distinct covered levels means every level is covered.

One subtle detail is avoiding use of the count values `p` and `q` as levels. Including them accidentally would produce incorrect answers on some inputs. Using `x_data[1:]` and `y_data[1:]` cleanly avoids that mistake.

## Worked Examples

### Example 1

Input:

```
4
3 1 2 3
2 2 4
```

| Step | Current Set |
| --- | --- |
| Start | {} |
| Add 1 | {1} |
| Add 2 | {1, 2} |
| Add 3 | {1, 2, 3} |
| Add 2 | {1, 2, 3} |
| Add 4 | {1, 2, 3, 4} |

Final state:

| n | Size of Set |
| --- | --- |
| 4 | 4 |

Output:

```
I become the guy.
```

This trace shows how duplicate level 2 is automatically ignored by the set. After combining both players' abilities, all four levels are covered.

### Example 2

Input:

```
4
2 1 2
1 3
```

| Step | Current Set |
| --- | --- |
| Start | {} |
| Add 1 | {1} |
| Add 2 | {1, 2} |
| Add 3 | {1, 2, 3} |

Final state:

| n | Size of Set |
| --- | --- |
| 4 | 3 |

Output:

```
Oh, my keyboard!
```

Level 4 never appears in either player's list. The set contains only three distinct levels, so completing the game is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(p + q) | Each listed level is inserted into the set once |
| Space | O(n) | The set may store all game levels |

Since `n ≤ 100`, the algorithm runs essentially instantly. Both the time and memory usage are far below the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())

    x_data = list(map(int, input().split()))
    y_data = list(map(int, input().split()))

    levels = set(x_data[1:]) | set(y_data[1:])

    if len(levels) == n:
        return "I become the guy."
    return "Oh, my keyboard!"

# provided sample
assert run("4\n3 1 2 3\n2 2 4\n") == "I become the guy.", "sample 1"

# minimum size
assert run("1\n0\n1 1\n") == "I become the guy.", "minimum n"

# missing one level
assert run("4\n2 1 2\n1 3\n") == "Oh, my keyboard!", "level 4 missing"

# one player covers everything
assert run("5\n5 1 2 3 4 5\n0\n") == "I become the guy.", "single player sufficient"

# maximum-style coverage
assert run(
    "100\n50 " + " ".join(map(str, range(1, 51))) +
    "\n50 " + " ".join(map(str, range(51, 101))) + "\n"
) == "I become the guy.", "full coverage across both players"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1`, only Y knows level 1 | `I become the guy.` | Minimum-size input |
| Levels 1,2,3 covered, level 4 missing | `Oh, my keyboard!` | Missing level detection |
| X covers all levels, Y covers none | `I become the guy.` | One player alone is enough |
| Split coverage across 100 levels | `I become the guy.` | Large boundary case |

## Edge Cases

Consider the case where one player contributes nothing.

Input:

```
1
0
1 1
```

The set starts empty. X adds no levels. Y adds level 1, producing `{1}`. The set size becomes 1, which equals `n`, so the algorithm prints:

```
I become the guy.
```

Now consider overlapping levels.

Input:

```
4
2 1 2
2 2 3
```

After processing X, the set is `{1, 2}`. Processing Y adds level 2 again and level 3, producing `{1, 2, 3}`. The duplicate level does not increase the set size. Since the final size is 3 instead of 4, the algorithm correctly prints:

```
Oh, my keyboard!
```

Finally, consider a case where cooperation is necessary.

Input:

```
4
2 1 2
2 3 4
```

X contributes `{1, 2}` and Y contributes `{3, 4}`. Their union becomes `{1, 2, 3, 4}`. The set size equals `n`, so the output is:

```
I become the guy.
```

This demonstrates why we must evaluate the combined coverage rather than checking each player individually.
