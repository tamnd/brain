---
title: "CF 426A - Sereja and Mugs"
description: "We have a cup with capacity s and several mugs containing water. Players take turns choosing one non-empty mug and pouring all of its water into the cup. The cup starts empty and water is never removed."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 426
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 243 (Div. 2)"
rating: 800
weight: 426
solve_time_s: 80
verified: true
draft: false
---

[CF 426A - Sereja and Mugs](https://codeforces.com/problemset/problem/426/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a cup with capacity `s` and several mugs containing water. Players take turns choosing one non-empty mug and pouring all of its water into the cup. The cup starts empty and water is never removed. If at any moment the amount of water inside the cup becomes greater than its capacity, the player who made that move loses.

The question is whether the mugs can be poured in some order so that nobody ever loses.

The key detail is that every mug must eventually be poured completely. Since the cup only gains water, the amount of water after all moves equals the sum of all mug volumes. The order of pouring only changes the intermediate states.

The constraints are tiny. There are at most 100 mugs and each mug volume is at most 10. Even a brute-force search over many possibilities would run quickly enough here, but the problem has a much simpler observation that reduces everything to a single comparison.

A common mistake is to think that the pouring order matters. Consider this input:

```
3 5
4 1 1
```

The correct answer is:

```
NO
```

A careless approach might try pouring `1`, then `1`, then `4`, hoping a better order exists. But the final amount of water is always `6`, which exceeds the cup capacity `5`. Since all mugs must be poured eventually, some player must overflow the cup.

Another edge case appears when the total water exactly matches the cup capacity:

```
2 7
3 4
```

The correct answer is:

```
YES
```

Overflow happens only when the amount becomes strictly greater than the capacity. Reaching exactly `7` is allowed.

A third easy-to-miss situation is when there are many tiny mugs:

```
5 4
1 1 1 1 1
```

The correct answer is:

```
NO
```

Each individual move looks harmless, but after the fifth mug the cup contains `5`, which exceeds the capacity.

## Approaches

The most direct brute-force idea is to try every possible order of pouring. For each permutation, we simulate the process and check whether the cup ever overflows.

This works because the game is completely determined once we choose an ordering of mugs. If at least one ordering avoids overflow, the answer is `"YES"`.

The problem is that the number of permutations grows factorially. With `n = 100`, there are `100!` possible orders, which is astronomically large. Even for `n = 15`, exhaustive search is already impossible within one second.

The breakthrough observation is that the order actually does not matter.

The amount of water in the cup only increases. After all mugs are poured, the cup contains exactly the sum of all mug volumes. If this total exceeds the cup capacity, then at some step the overflow must occur. No ordering can avoid it.

On the other hand, if the total volume is at most the cup capacity, then pouring mugs in any order is safe. The water level never exceeds the final total, and the final total already fits.

This reduces the entire problem to checking:

```
sum(a) <= s
```

If true, print `"YES"`. Otherwise, print `"NO"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! × n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of mugs `n` and the cup capacity `s`.
2. Read the list of mug volumes.
3. Compute the sum of all mug volumes.
4. Compare the total water with the cup capacity.

If the total is less than or equal to `s`, print `"YES"`.

Otherwise, print `"NO"`.

### Why it works

The cup starts empty and water is only added, never removed. After all moves, the total amount of water inside the cup equals the sum of all mug volumes.

If this total exceeds the cup capacity, then overflow is unavoidable because the final state itself is invalid.

If the total fits inside the cup, then every intermediate state also fits, since intermediate amounts are always less than or equal to the final amount.

Because of this monotonic behavior, checking the total sum is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, s = map(int, input().split())
a = list(map(int, input().split()))

if sum(a) <= s:
    print("YES")
else:
    print("NO")
```

The program directly follows the mathematical observation from the algorithm.

The first line reads the number of mugs and the cup capacity. The second line reads all mug volumes into a list.

The crucial operation is `sum(a)`. This computes the total amount of water that will eventually end up inside the cup.

The comparison uses `<=`, not `<`. Reaching the exact capacity is allowed because the cup only overflows when the amount becomes strictly greater than the limit.

No special handling for ordering is needed, since the proof shows that ordering cannot change the outcome.

## Worked Examples

### Example 1

Input:

```
3 4
1 1 1
```

| Step | Current Mug | Water in Cup |
| --- | --- | --- |
| Start | - | 0 |
| Pour 1 | 1 | 1 |
| Pour 2 | 1 | 2 |
| Pour 3 | 1 | 3 |

The total water is `3`, which is less than the capacity `4`. Since the final amount fits, every intermediate amount also fits. The answer is `"YES"`.

### Example 2

Input:

```
3 5
4 1 1
```

| Step | Current Mug | Water in Cup |
| --- | --- | --- |
| Start | - | 0 |
| Pour 1 | 4 | 4 |
| Pour 2 | 1 | 5 |
| Pour 3 | 1 | 6 |

The total water is `6`, which exceeds the capacity `5`. No matter how we reorder the mugs, the final amount will still be `6`, so overflow is unavoidable. The answer is `"NO"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the mug volumes once to compute their sum |
| Space | O(1) | Only a few variables are used besides the input list |

With at most 100 mugs, the solution runs instantly. Both the time and memory usage are far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, s = map(int, input().split())
    a = list(map(int, input().split()))

    if sum(a) <= s:
        print("YES")
    else:
        print("NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("3 4\n1 1 1\n") == "YES\n", "sample 1"

# minimum valid input
assert run("2 1\n1 1\n") == "NO\n", "minimum size with overflow"

# exact boundary
assert run("2 7\n3 4\n") == "YES\n", "sum exactly equals capacity"

# all equal values
assert run("5 10\n2 2 2 2 2\n") == "YES\n", "all equal and fits exactly"

# overflow by one
assert run("4 9\n2 2 2 4\n") == "NO\n", "sum exceeds by one"

# large input within limits
assert run(
    "100 1000\n" + "10 " * 100 + "\n"
) == "YES\n", "maximum-sized input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 1` | `NO` | Smallest input size with unavoidable overflow |
| `2 7 / 3 4` | `YES` | Exact equality with capacity is allowed |
| `5 10 / 2 2 2 2 2` | `YES` | Uniform values and exact fit |
| `4 9 / 2 2 2 4` | `NO` | Overflow by a single unit |
| `100 1000 / 10 repeated 100 times` | `YES` | Maximum constraints |

## Edge Cases

Consider the case where the total volume is exactly equal to the cup capacity:

```
2 7
3 4
```

The algorithm computes `3 + 4 = 7`. Since `7 <= 7`, it prints `"YES"`.

Tracing the process:

| After Move | Water in Cup |
| --- | --- |
| Start | 0 |
| After first mug | 3 |
| After second mug | 7 |

The cup never exceeds capacity, so equality must be treated as safe.

Now consider a case where every mug is small but the combined total is too large:

```
5 4
1 1 1 1 1
```

The algorithm computes `1 + 1 + 1 + 1 + 1 = 5`. Since `5 > 4`, it prints `"NO"`.

Tracing the process:

| After Move | Water in Cup |
| --- | --- |
| Start | 0 |
| After first mug | 1 |
| After second mug | 2 |
| After third mug | 3 |
| After fourth mug | 4 |
| After fifth mug | 5 |

Overflow happens only at the final move, but it is still unavoidable.

Finally, consider a case where one mug is already close to the capacity:

```
3 5
4 1 1
```

The total is `6`, so the algorithm prints `"NO"` immediately.

Trying different orders does not help:

| Order | Final Water |
| --- | --- |
| `4,1,1` | 6 |
| `1,4,1` | 6 |
| `1,1,4` | 6 |

The final amount is always the same, which is exactly why the ordering is irrelevant.
