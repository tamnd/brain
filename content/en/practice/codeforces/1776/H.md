---
title: "CF 1776H - Beppa and SwerChat"
description: "The list shown by SwerChat is ordered by recency. The member who was online most recently appears first, the second most recent appears second, and so on. At 9:00, Beppa records an ordering a. At 22:00, she records another ordering b."
date: "2026-06-09T11:47:00+07:00"
tags: ["codeforces", "competitive-programming", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1776
codeforces_index: "H"
codeforces_contest_name: "SWERC 2022-2023 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1300
weight: 1776
solve_time_s: 133
verified: true
draft: false
---

[CF 1776H - Beppa and SwerChat](https://codeforces.com/problemset/problem/1776/H)

**Rating:** 1300  
**Tags:** two pointers  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The list shown by SwerChat is ordered by recency. The member who was online most recently appears first, the second most recent appears second, and so on.

At 9:00, Beppa records an ordering `a`. At 22:00, she records another ordering `b`.

Between those two moments, the only thing that can change the ordering is that a member comes online. Since nobody is online simultaneously, every online event is processed one at a time. When a member comes online, they become the most recently seen member, so they move to the front of the list.

We must determine the minimum number of distinct members who must have been online at least once to transform the ordering from `a` into `b`.

The total size of all test cases is at most `10^5`, so any solution that compares all pairs of members or repeatedly simulates large list operations will be too slow. An `O(n)` or `O(n log n)` solution per test case is easily fast enough.

The subtle part is that a member may appear in a different position without necessarily having been online. They can be pushed backward when other people come online. A naive approach that counts everyone whose position changed would overestimate the answer.

Consider:

```
a = [1, 2, 3]
b = [2, 1, 3]
```

Only member `2` needs to come online. Member `1` changes position, but never has to be online.

Another easy mistake is assuming that every inversion between the two permutations corresponds to an online event.

For example:

```
a = [1, 2, 3, 4]
b = [3, 4, 1, 2]
```

Members `3` and `4` can come online, producing the final order. The answer is `2`, not `4`.

A different edge case occurs when the lists are already identical:

```
a = [1, 2, 3, 4]
b = [1, 2, 3, 4]
```

Nobody needs to come online, so the correct answer is `0`.

## Approaches

A brute-force viewpoint is to guess which members were online and check whether some sequence of front-move operations can produce `b`.

That idea is correct in principle, but completely impractical. There are `2^n` possible subsets of members, and even verifying one candidate subset would require simulating list operations. With `n` up to `10^5`, this is impossible.

The key observation comes from looking at members who were **never online**.

Suppose a member never comes online. They are never moved to the front. The only thing that can happen to them is that other members jump ahead of them.

Because of that, all never-online members keep their relative order from the original permutation `a`.

This means the final list `b` has a very specific structure:

```
[ all members who were online ]
[ all members who were never online ]
```

The second part must appear in exactly the same relative order as in `a`.

To minimize the number of online members, we want to maximize the number of never-online members.

Let `pos[x]` be the position of member `x` in `a`.

Replace every element of `b` by its position in `a`.

For example:

```
a = [1, 4, 2, 5, 3]

pos:
1 -> 1
4 -> 2
2 -> 3
5 -> 4
3 -> 5

b = [4, 5, 1, 2, 3]

positions in a:
[2, 4, 1, 3, 5]
```

The never-online members must form a suffix of `b`, and their positions in `a` must be strictly increasing. That is exactly the condition for preserving relative order.

So we need the longest suffix of the transformed sequence that is strictly increasing.

If that suffix has length `L`, then `L` members can be never-online, and the answer is:

```
n - L
```

### Approach Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the permutation `a`.
2. Build an array `pos` where `pos[x]` stores the position of member `x` in `a`.
3. Traverse `b` from right to left.
4. Maintain the invariant that the currently examined suffix of `b` corresponds to a strictly increasing sequence of positions in `a`.
5. Starting from the end, continue moving left while:

```
pos[b[i-1]] < pos[b[i]]
```

This means the relative order of those members matches the order in `a`, so they could all be never-online.
6. The first place where this condition fails is the boundary between the online prefix and the never-online suffix.
7. If the increasing suffix starts at index `s`, then its length is `n - s`.
8. Output:

```
s
```

because exactly the first `s` members of `b` must belong to the online set.

### Why it works

Every member who never comes online keeps their relative order from `a`. Since all online members end up before all never-online members, the never-online members must form a suffix of `b`.

A suffix of `b` preserves relative order from `a` precisely when the corresponding positions in `a` are strictly increasing. Any longer suffix would violate this condition and cannot consist entirely of never-online members.

Conversely, if a suffix is increasing, we can realize the permutation by declaring all members before that suffix as online. Process those online members from right to left according to their order in `b`, moving each to the front once. This produces exactly the required prefix while leaving the suffix in its original relative order.

Hence the longest increasing suffix gives the maximum possible number of never-online members, which minimizes the number of online members.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos = [0] * (n + 1)

        for i, x in enumerate(a):
            pos[x] = i

        s = n - 1

        while s > 0 and pos[b[s - 1]] < pos[b[s]]:
            s -= 1

        answers.append(str(s))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The `pos` array converts relative-order questions into simple integer comparisons. Instead of repeatedly searching for members inside `a`, we can check order preservation in constant time.

The variable `s` tracks the start of the longest valid suffix. We begin at the end because every suffix of length one is automatically increasing.

The condition

```
pos[b[s - 1]] < pos[b[s]]
```

checks whether extending the suffix one position to the left still preserves the order from `a`.

When the condition fails, we have found the largest possible never-online suffix. The answer is exactly the number of elements before it, which is `s`.

No list simulation is required.

## Worked Examples

### Example 1

```
a = [1, 4, 2, 5, 3]
b = [4, 5, 1, 2, 3]
```

Positions in `a`:

| Member | Position |
| --- | --- |
| 1 | 0 |
| 4 | 1 |
| 2 | 2 |
| 5 | 3 |
| 3 | 4 |

Converted sequence:

```
[1, 3, 0, 2, 4]
```

| s | Compare | Result |
| --- | --- | --- |
| 4 | 2 < 4 | continue |
| 3 | 0 < 2 | continue |
| 2 | 3 < 0 | false |

The longest increasing suffix starts at index `2`.

| Quantity | Value |
| --- | --- |
| Suffix length | 3 |
| Answer | 2 |

Output:

```
2
```

This demonstrates that members `1, 2, 3` can remain never-online while `4` and `5` are sufficient to explain the change.

### Example 2

```
a = [1, 2, 3, 4, 5, 6]
b = [1, 2, 3, 4, 5, 6]
```

Converted sequence:

```
[0, 1, 2, 3, 4, 5]
```

| s | Compare | Result |
| --- | --- | --- |
| 5 | 4 < 5 | continue |
| 4 | 3 < 4 | continue |
| 3 | 2 < 3 | continue |
| 2 | 1 < 2 | continue |
| 1 | 0 < 1 | continue |

The suffix expands to the entire array.

| Quantity | Value |
| --- | --- |
| Suffix length | 6 |
| Answer | 0 |

Output:

```
0
```

This confirms that no online events are required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to build positions and one backward scan |
| Space | O(n) | Position array |

Across all test cases, the sum of `n` is at most `10^5`. The algorithm performs only a constant amount of work per element, so it comfortably fits within the time limit and uses very little memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos = [0] * (n + 1)

        for i, x in enumerate(a):
            pos[x] = i

        s = n - 1
        while s > 0 and pos[b[s - 1]] < pos[b[s]]:
            s -= 1

        out.append(str(s))

    return "\n".join(out)

# provided sample
assert run(
"""4
5
1 4 2 5 3
4 5 1 2 3
6
1 2 3 4 5 6
1 2 3 4 5 6
8
8 2 4 7 1 6 5 3
5 6 1 4 8 2 7 3
1
1
1
"""
) == """2
0
4
0"""

# minimum size
assert run(
"""1
1
1
1
"""
) == "0"

# single move to front
assert run(
"""1
3
1 2 3
2 1 3
"""
) == "1"

# entire array reversed
assert run(
"""1
5
1 2 3 4 5
5 4 3 2 1
"""
) == "4"

# suffix of length one only
assert run(
"""1
4
1 2 3 4
3 4 2 1
"""
) == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1` | `0` | Smallest possible case |
| `[1,2,3] -> [2,1,3]` | `1` | Position changes do not imply online activity |
| Reversed permutation | `4` | Longest increasing suffix may have length one |
| `[1,2,3,4] -> [3,4,2,1]` | `3` | Boundary detection in backward scan |

## Edge Cases

Consider the already-sorted case:

```
1
4
1 2 3 4
1 2 3 4
```

The transformed position sequence is:

```
[0, 1, 2, 3]
```

Every adjacent comparison is increasing, so the suffix expands to the whole array. The algorithm returns `0`, correctly identifying that nobody had to come online.

Now consider a case where only one member was online:

```
1
3
1 2 3
2 1 3
```

The transformed sequence is:

```
[1, 0, 2]
```

Scanning from the end:

```
0 < 2   -> valid
1 < 0   -> invalid
```

The longest increasing suffix starts at index `1`, so the answer is `1`. Member `2` comes online and moves to the front, while `1` and `3` remain offline.

Finally, consider a highly shuffled ordering:

```
1
5
1 2 3 4 5
5 4 3 2 1
```

The transformed sequence is:

```
[4, 3, 2, 1, 0]
```

The very first comparison from the right already fails, so the longest increasing suffix has length `1`. The algorithm returns `4`, meaning four members must belong to the online set. This is the minimum possible because no larger suffix preserves the original relative order.
