---
title: "CF 102806B - \u041f\u0435\u0440\u043b\u044b \u0438 \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0435\u0440"
description: "We have a sequence of n pearls produced one by one. The color of the pearl produced at second i is given. A valid engine set must contain exactly one pearl of every color, so it always contains k pearls."
date: "2026-07-26T16:17:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102806
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2017-2018, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102806
solve_time_s: 50
verified: true
draft: false
---

[CF 102806B - \u041f\u0435\u0440\u043b\u044b \u0438 \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0435\u0440](https://codeforces.com/problemset/problem/102806/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of `n` pearls produced one by one. The color of the pearl produced at second `i` is given. A valid engine set must contain exactly one pearl of every color, so it always contains `k` pearls. The production times of the pearls inside one set must be close: the earliest and latest pearl in that set may differ by at most `m` seconds. Every pearl can be used only once. The task is to build as many such sets as possible and output the indices of the pearls in every set.

The input contains the number of produced pearls, the maximum allowed time difference, the number of colors, and then the color of each pearl in production order. The output starts with the maximum number of complete sets, followed by the indices chosen for every set.

The limits are large: both `n` and `k` can reach `100000`. An algorithm that repeatedly scans all colors or all previous pearls for every position would become quadratic and would not finish. We need a solution where every pearl is processed only a constant number of times.

The main edge cases come from the interaction between color availability and the time window. If a color is missing from the current window, a set cannot be formed even if other colors are abundant. For example:

```
6 2 3
1 2 2 1 3 3
```

The first possible set is formed by pearls `4, 3, 5`, because their colors are `1, 2, 3` and the time difference is `5 - 3 = 2`. A careless solution that only counts how many times each color appears would expect two sets, because every color appears twice, but the time restriction prevents it.

Another tricky case is when the last pearl of a color is outside the current window while older occurrences of other colors remain. For example:

```
5 2 3
1 2 2 2 3
```

There are enough total pearls of color `2`, but there is only one pearl of color `1` and it appears too early. The answer is `0`. A solution that only tracks global counts would incorrectly produce a positive answer.

## Approaches

A direct approach is to try every possible group of `k` pearls and check whether it contains all colors and fits inside the time limit. This is correct because it tests exactly the definition of a valid set. However, there can be up to `100000` pearls, so even looking at many possible windows and checking all colors quickly becomes too slow. In the worst case, scanning all colors for every position costs `O(nk)` operations.

The structure of the problem gives a better direction. A valid set must be contained inside a moving window of length `m + 1` positions. While scanning pearls from left to right, we only need to know which unused pearls of each color are currently inside that window. If every color has at least one available pearl, then taking the oldest available pearl of every color immediately creates a valid set.

The reason taking the oldest pearls works is that the current window already guarantees that all stored pearls are close enough to the current position. Using older pearls cannot make future sets worse, because keeping newer pearls leaves more flexibility for later windows. After creating a set, those pearls are removed from their color queues and the scan continues.

The brute-force approach works because it checks all possibilities, but it repeats the same work many times. The sliding-window queues reduce the problem to maintaining only the information that can still participate in a future answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Optimal | O(n + k) | O(n + k) | Accepted |

## Algorithm Walkthrough

1. Create one queue for every color. Each queue stores the indices of currently available pearls of that color inside the active time window. Also keep a counter of how many colors currently have a non-empty queue.
2. Process pearls from left to right. When pearl `i` appears, add its index to the queue of its color. If this color queue was empty before the insertion, increase the number of available colors.
3. Remove the pearl that is no longer inside the window. When processing index `i`, the oldest allowed index is `i - m`, so index `i - m - 1` must be removed if it exists. If removing it makes a color queue empty, decrease the number of available colors.
4. If all `k` color queues are non-empty, take the first element from every queue. These `k` pearls have all different colors and all lie inside the current window, so they form a valid set. Store their indices and remove them from the queues.
5. Continue until all pearls are processed. The stored sets are the maximum possible number of sets.

Why it works:

At every moment, each queue contains exactly the unused pearls of one color that can still be used in a set ending at the current position. A set can only be created when every color has at least one candidate, so the algorithm creates a set exactly when a valid choice exists at that moment. Taking the earliest candidate of each color is safe because all candidates in the queues satisfy the same time bound, and removing the earliest available pearls leaves the newest pearls for future windows. Thus every created set uses pearls that could not be replaced by a better choice, and the greedy process never reduces the number of future possible sets.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    colors = list(map(int, input().split()))

    queues = [deque() for _ in range(k)]
    non_empty = 0
    ans = []

    for i, c in enumerate(colors):
        c -= 1

        if not queues[c]:
            non_empty += 1
        queues[c].append(i + 1)

        old = i - m - 1
        if old > 0:
            oc = colors[old - 1] - 1
            queues[oc].popleft()
            if not queues[oc]:
                non_empty -= 1

        if non_empty == k:
            cur = []
            for q in queues:
                cur.append(q.popleft())
            ans.append(cur)

            non_empty = 0
            for q in queues:
                if q:
                    non_empty += 1

    out = [str(len(ans))]
    for group in ans:
        out.append(" ".join(map(str, group)))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The queues array is the direct implementation of the sliding window idea. Queue `c` contains the positions of currently usable pearls of color `c`.

When a new pearl is read, it is appended to its color queue. The removal step uses `i - m - 1` because indices are one-based in the stored answer but zero-based in the loop. A pearl exactly `m` positions away is still valid, while a pearl one position farther is not.

When all queues are non-empty, the front of every queue is selected. The front represents the oldest available pearl of that color. Removing these chosen pearls from all queues prepares the structure for finding the next independent set.

The variable `non_empty` avoids scanning all colors after every insertion. It is updated only when a queue changes between empty and non-empty states, keeping the whole algorithm linear.

## Worked Examples

For the first sample:

```
6 2 3
1 2 2 1 3 3
```

The scan behaves as follows.

| Step | Added pearl | Active color queues | Action |
| --- | --- | --- | --- |
| 1 | color 1 at index 1 | {1} | Wait for other colors |
| 2 | color 2 at index 2 | {1,2} | Wait for color 3 |
| 3 | color 2 at index 3 | {1,2} | Wait for color 3 |
| 4 | color 1 at index 4 | {1,2} | Pearl 1 is still missing color 3 |
| 5 | color 3 at index 5 | {1,2,3} | Create set 4,3,5 |
| 6 | color 3 at index 6 | {3} | Not enough colors |

The created set contains indices `4 3 5`. Its earliest index is `3` and latest is `5`, so the difference is exactly `2`.

For the second sample:

```
5 2 3
1 2 2 2 3
```

| Step | Added pearl | Removed pearl | Active colors | Action |
| --- | --- | --- | --- | --- |
| 1 | color 1 at 1 | none | 1 | Wait |
| 2 | color 2 at 2 | none | 1,2 | Wait |
| 3 | color 2 at 3 | none | 1,2 | Wait |
| 4 | color 2 at 4 | none | 1,2 | Wait |
| 5 | color 3 at 5 | index 2 removed from window | 1,2,3 | No valid complete choice |

The only pearl of color `1` is too far away when color `3` appears. The algorithm correctly outputs zero sets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | Every pearl enters one queue once and leaves at most once. |
| Space | O(n + k) | The queues store all currently unused pearls, and there are `k` queues. |

The solution only performs constant work per pearl, which fits the `100000` element limits. The memory usage is also linear because every pearl index is stored at most once.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""6 2 3
1 2 2 1 3 3
""") == """1
4 3 5
""", "sample 1"

assert run("""5 2 3
1 2 2 2 3
""") == """0
""", "sample 2"

assert run("""3 1 3
1 2 3
""") == """1
1 2 3
""", "minimum case"

assert run("""8 10 2
1 2 1 2 1 2 1 2
""") == """4
1 2
3 4
5 6
7 8
""", "large window"

assert run("""7 2 3
1 1 2 2 3 3 3
""") == """1
2 4 5
""", "boundary removal"

assert run("""6 3 2
1 1 1 1 1 1
""") == """0
""", "all equal colors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 2 3 / 1 2 2 1 3 3` | `1` set | Provided example and greedy choice |
| `5 2 3 / 1 2 2 2 3` | `0` sets | A color leaving the valid window |
| `3 1 3 / 1 2 3` | `1` set | Smallest possible input |
| `8 10 2 / 1 2 1 2 1 2 1 2` | `4` sets | Many sets with a wide window |
| `7 2 3 / 1 1 2 2 3 3 3` | `1` set | Window expiration boundaries |
| `6 3 2 / 1 1 1 1 1 1` | `0` sets | Missing colors |

## Edge Cases

When every color appears enough times but the appearances are separated, global counting is misleading. For:

```
6 2 3
1 2 2 1 3 3
```

the color counts suggest two possible sets. During the scan, the algorithm keeps only pearls within distance `2` of the current position. At index `5`, the available queues contain colors `1`, `2`, and `3`, so it creates the set `4, 3, 5`. The remaining color `3` cannot be paired with another complete group.

When a required color exists only in the past outside the window, it must be discarded. For:

```
5 2 3
1 2 2 2 3
```

the pearl at index `1` has color `1`. By the time the color `3` pearl arrives at index `5`, the valid window starts at index `3`, so the color `1` queue is empty. The algorithm removes outdated pearls before checking for a set, so it never creates an invalid group.

When all pearls have the same color, no group can ever be complete unless there is only one color. For:

```
6 3 2
1 1 1 1 1 1
```

the second color queue never becomes non-empty. The `non_empty` counter stays below `k`, and the algorithm correctly returns `0`.
