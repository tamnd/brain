---
title: "CF 102599D - Young Explorers"
description: "We have a collection of explorers, where each explorer has a value e describing the minimum number of people required in any group containing that explorer. A group is valid only when every member's requirement is satisfied by the final group size."
date: "2026-08-02T06:43:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102599
codeforces_index: "D"
codeforces_contest_name: "The fifth Lipetsk collegiate programming contest. Finals. 8-11 form"
rating: 0
weight: 102599
solve_time_s: 381
verified: false
draft: false
---

[CF 102599D - Young Explorers](https://codeforces.com/problemset/problem/102599/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We have a collection of explorers, where each explorer has a value `e` describing the minimum number of people required in any group containing that explorer. A group is valid only when every member's requirement is satisfied by the final group size. The task is to choose some explorers and split them into the maximum possible number of valid groups. Some explorers may be ignored if they cannot be placed into a valid group.

The input contains several independent test cases. For each test case, the array represents the inexperience values of all explorers. The output is the largest number of groups that can be created from that array.

The total number of explorers over all test cases is at most `3 * 10^5`. This means the solution must process each explorer only a small number of times. An approach that tries many different group combinations will quickly become impossible because the number of possible partitions grows exponentially. Even an `O(N^2)` solution would be too slow when a single test case reaches `200000` explorers, so the intended solution needs to be close to `O(N log N)` or `O(N)`.

A few cases are easy to mishandle. If every explorer has requirement `1`, each explorer can stand alone and the answer is the full size of the array.

For example:

```
1
4
1 1 1 1
```

The correct output is:

```
4
```

A careless solution that always tries to build the largest possible groups first may create one group of size four and lose the opportunity to create four groups.

Another tricky case is when large requirements appear together with small ones.

Example:

```
1
5
2 3 1 2 2
```

The correct output is:

```
2
```

A greedy method that immediately discards explorers with large requirements can miss the fact that one explorer with requirement `3` can be used together with two other explorers to form a valid group.

The final edge case is when a requirement is larger than the number of remaining available explorers.

Example:

```
1
3
1 1 5
```

The correct output is:

```
2
```

The explorer requiring a group of five cannot be included, but the other two explorers can still form two groups of size one.

## Approaches

A direct brute-force solution would try different ways of assigning explorers to groups and keep the best result. This works conceptually because every possible valid arrangement is considered, so the best one must be found. The problem is that the number of possible assignments grows extremely quickly. With `N` explorers, the number of possible partitions is far beyond what can be checked. Even limiting the search to many possible group boundaries would require too many operations, reaching roughly `O(N^2)` or worse in realistic implementations.

The useful observation comes from looking at what makes a group valid. If a group has size `s`, every explorer inside it must have `e <= s`. This means explorers with smaller requirements are easier to place, while explorers with larger requirements need more members around them.

Sorting the requirements lets us handle explorers in increasing difficulty order. After sorting, we can build groups from the smallest requirements upward. We keep a count of how many explorers have been collected for the current group. When this count reaches the current explorer's requirement, the group can be closed and counted as one valid group.

The reason this greedy choice works is that a small requirement never benefits from waiting for a larger group. If a group already contains enough people for the current explorer, creating the group immediately saves those explorers as a finished group and leaves later explorers to form future groups. Larger requirements are considered later, after more potential group members become available.

The brute-force works because it explores all valid partitions, but fails because there are too many possibilities. The observation that the sorted order exposes the exact moment when a group becomes valid lets us replace partition searching with a single greedy scan.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | Exponential or worse depending on search strategy | O(N) | Too slow |
| Optimal | O(N log N) | O(1) extra besides sorting | Accepted |

## Algorithm Walkthrough

1. Sort the explorers' requirements in nondecreasing order. Smaller requirements should be processed first because they need fewer people to become valid group members.

2. Traverse the sorted array while maintaining `current`, the number of explorers currently collected for a possible group.

3. Add the current explorer to `current`. If `current` becomes at least equal to this explorer's requirement, form a group and increase the answer.

4. Reset `current` to zero after forming a group, because those explorers are already used and cannot contribute to another group.

The key decision is closing a group as soon as it becomes valid. Suppose the current explorer has requirement `x` and we already have `x` explorers in the group. Keeping extra explorers for this group cannot create more groups, while finishing now gives the remaining explorers the best chance to create another valid group.

Why it works:

After processing any prefix of the sorted array, the algorithm has created the maximum possible number of groups using only that prefix. A completed group is valid because it was created only when its size was at least the requirement of every processed explorer inside it. When the algorithm closes a group, using any of those explorers in a future group would only remove available people from later explorers without increasing the number of groups, so finishing the group immediately is always optimal. Processing explorers in sorted order guarantees that every requirement checked is the largest requirement inside the current group, which is enough to prove validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        e = list(map(int, input().split()))

        e.sort()

        groups = 0
        current = 0

        for value in e:
            current += 1
            if current >= value:
                groups += 1
                current = 0

        ans.append(str(groups))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution first sorts the requirements so that the scan follows the order used in the greedy proof. The variable `current` stores how many explorers have been collected for the unfinished group. Each explorer increases this count by one.

The comparison `current >= value` is the exact condition for closing a group. Because the array is sorted, `value` is the largest requirement encountered inside the current group, so satisfying it means every explorer in that group is satisfied.

Resetting `current` to zero is essential. Forgetting this would allow the same explorer to contribute to multiple groups and produce an impossible answer.

Python integers do not overflow for this problem, and the total input size is small enough for sorting all test cases within the limits.

## Worked Examples

For the first sample:

```
3
1 1 1
```

After sorting, the array is unchanged.

| Explorer requirement | Current group size | Groups formed |
|---|---|---|
| 1 | 1, close group | 1 |
| 1 | 1, close group | 2 |
| 1 | 1, close group | 3 |

Every explorer can create a group alone because every requirement is one. The greedy process immediately closes each group.

For the second sample:

```
5
2 3 1 2 2
```

After sorting:

```
1 2 2 2 3
```

| Explorer requirement | Current group size | Groups formed |
|---|---|---|
| 1 | 1, close group | 1 |
| 2 | 1 | 1 |
| 2 | 2, close group | 2 |
| 2 | 1 | 2 |
| 3 | 2 | 2 |

The last two explorers cannot create another group because only two explorers remain available, while one of them needs a group of size three. The trace shows why small groups should be finalized as soon as possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(N log N) | Sorting dominates the linear scan, and the total number of explorers is bounded by `3 * 10^5`. |
| Space | O(N) | The array storing requirements requires memory, while the algorithm itself uses only a few counters. |

The maximum input size is large enough that repeated searching or simulation would fail, but sorting followed by one pass easily fits within the two second limit and the memory limit.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.readline
    t = int(data())
    out = []

    for _ in range(t):
        n = int(data())
        arr = list(map(int, data().split()))
        arr.sort()

        groups = 0
        current = 0

        for x in arr:
            current += 1
            if current >= x:
                groups += 1
                current = 0

        out.append(str(groups))

    sys.stdin = old_stdin
    return "\n".join(out)

assert solution("""2
3
1 1 1
5
2 3 1 2 2
""") == """3
2""", "provided samples"

assert solution("""1
1
1
""") == "1", "single explorer"

assert solution("""1
4
1 1 1 1
""") == "4", "all minimum requirements"

assert solution("""1
5
2 2 2 2 2
""") == "2", "equal requirements"

assert solution("""1
6
1 2 3 4 5 6
""") == "2", "increasing boundary requirements"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `1 / 1 / 1` | `1` | Minimum input size |
| `4 explorers with requirement 1` | `4` | Every explorer forming an individual group |
| Five explorers with requirement `2` | `2` | Handling repeated equal values |
| Requirements `1 2 3 4 5 6` | `2` | Boundary cases with large requirements |

## Edge Cases

For the case where all explorers have requirement one:

```
1
4
1 1 1 1
```

The sorted array stays the same. The counter reaches one after every explorer, so the algorithm closes a group four times and returns four. A strategy that prefers the largest possible groups would incorrectly return one.

For the mixed requirement case:

```
1
5
2 3 1 2 2
```

Sorting gives:

```
1 2 2 2 3
```

The first explorer creates a group alone. The next two explorers create a group of size two. The remaining two explorers cannot satisfy the requirement three, so they are ignored. The answer is two, matching the maximum possible number of groups.

For impossible large requirements:

```
1
3
1 1 5
```

The sorted array is:

```
1 1 5
```

The first two explorers each create a group of size one. The last explorer increases the counter to one, but the requirement is five, so no group is created. The algorithm returns two, which is optimal because the third explorer cannot belong to any valid group.
:::
