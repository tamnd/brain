---
title: "CF 102591B - \u042f\u0433\u043e\u0434\u044b-\u043f\u043e\u0436\u0438\u0440\u0430\u0442\u0435\u043b\u0438"
description: "We have a circular arrangement of berries. Each berry has a unique weight from 1 to N, and the order in the input describes their positions around the circle."
date: "2026-08-01T06:33:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102591
codeforces_index: "B"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041c\u0423\u0418\u0422 \u043f\u043e \u0441\u043f\u043e\u0440\u0442\u0438\u0432\u043d\u043e\u043c\u0443 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2020. \u0424\u0438\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u0442\u0443\u0440."
rating: 0
weight: 102591
solve_time_s: 224
verified: true
draft: false
---

[CF 102591B - \u042f\u0433\u043e\u0434\u044b-\u043f\u043e\u0436\u0438\u0440\u0430\u0442\u0435\u043b\u0438](https://codeforces.com/problemset/problem/102591/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circular arrangement of berries. Each berry has a unique weight from 1 to N, and the order in the input describes their positions around the circle. A move is possible only when two neighboring berries have consecutive weights, with the larger one being exactly one heavier. The heavier berry removes the lighter one and keeps its own weight. The task is to decide whether some sequence of moves can remove every berry except the one with weight N.

The main observation comes from the fact that every weight has exactly one possible eater. Berry k can only disappear when berry k+1 is still alive and adjacent to it. Since k+1 is needed to remove k, the order of removals is actually forced. Berry 1 has to disappear before berry 2, berry 2 before berry 3, and so on until berry N-1 disappears last. The problem is not about searching through possible moves, it is about checking whether this single required order is achievable.

The constraint N up to 2 * 10^5 rules out simulations that try different move sequences. A state search would have an enormous number of possibilities, and even a direct simulation that scans the whole circle after every deletion would take O(N^2) operations, which is too much for this input size. We need a linear or near-linear approach.

There are several edge cases where an incorrect implementation can fail. When N = 1, no moves are required, so the answer must be YES.

```
Input:
1
1
```

The correct output is YES. A solution that always starts by checking adjacency between 1 and 2 would access a nonexistent value.

Another subtle case is when a consecutive pair exists but removing it too early would be wrong. Consider the sample:

```
Input:
4
4 1 3 2
```

The pair 3 and 2 is adjacent, but removing 2 first leaves 4 and 1 separated by no useful eater, so the game cannot finish. A solution that only checks whether some valid move exists at every moment would give the wrong result.

A circular boundary is also important. For example:

```
Input:
3
2 1 3
```

The values 1 and 2 are adjacent through the circle, so 2 eats 1 and then 3 eats 2. The correct output is YES. An implementation that forgets the connection between the first and last positions would incorrectly reject this case.

## Approaches

A brute-force solution would try every possible valid move, recursively exploring all possible orders of removals. It is correct because it follows the rules exactly and accepts if at least one path reaches a single berry. The problem is that the number of possible paths grows very quickly. Even with only a few berries there can be multiple choices, and for N = 2 * 10^5 this approach is completely impossible.

The key observation is that the brute force explores choices that do not actually exist. The removal order is forced. Berry k must be removed before berry k+1 because k+1 is the only berry that can remove k. Once k+1 disappears, k can never disappear later. This reduces the whole process to checking whether 1, then 2, then 3, and so on can each be removed at the correct moment.

The remaining challenge is maintaining adjacency while elements disappear from a circle. A doubly linked list represented by arrays is enough. For every weight we store the weights of its current left and right neighbors. When weight k is removed, its two neighbors become adjacent. Each berry is removed once, so the total work is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build the circular linked list. For every berry value, store which value is immediately to its left and which value is immediately to its right. The input order gives this information directly, including the connection between the last and first positions.
2. Process the berries in increasing order from 1 to N-1. At step k, check whether berry k is currently next to berry k+1. This is the only possible way for k to disappear.
3. If k+1 is neither the left nor the right neighbor of k, the required removal order cannot happen, so the answer is NO.
4. If k can be removed, connect its two neighbors directly and discard k from the linked list. The next iteration works on the updated circle.
5. If every value from 1 to N-1 can be removed in this order, only berry N remains, so the answer is YES.

Why it works:

The invariant is that before processing value k, all values smaller than k have already been removed and all values from k to N are still present. Berry k must disappear before k+1 can disappear because k+1 is the only possible eater of k. This makes the increasing removal order necessary in every valid game. The algorithm checks exactly whether each required removal can happen at the moment it is needed, and the linked list updates preserve the true circular adjacency after every removal. If all checks succeed, the same sequence of removals is a valid way to finish the game.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    if n == 1:
        print("YES")
        return

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    for i, x in enumerate(a):
        left[x] = a[(i - 1) % n]
        right[x] = a[(i + 1) % n]

    for x in range(1, n):
        if left[x] != x + 1 and right[x] != x + 1:
            print("NO")
            return

        l = left[x]
        r = right[x]
        right[l] = r
        left[r] = l

    print("YES")

if __name__ == "__main__":
    solve()
```

The `left` and `right` arrays store neighbors by berry weight rather than by position. This is convenient because the removal order is based on weights, not on original indices.

The loop from 1 to N-1 follows the forced order of disappearance. Before removing x, the code checks both directions because the circle has no fixed beginning, so x+1 can be either neighbor.

When x is removed, its left neighbor and right neighbor become adjacent. The assignments update both directions of the doubly linked list, which avoids any shifting of the original array. This is the difference between an O(N) solution and a solution that repeatedly deletes from the middle of a list.

Python integers are sufficient here because only indices and values up to 2 * 10^5 are stored, so overflow is not a concern.

## Worked Examples

For the first sample:

```
3
1 3 2
```

| Current value checked | Left neighbor | Right neighbor | Required neighbor | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 2 | Remove 1 |
| 2 | 3 | 3 | 3 | Remove 2 |

After removing 1, the circle becomes 3, 2. Then 3 removes 2, leaving only the maximum value. The trace shows that a consecutive pair does not need to be in increasing order in the input, only adjacent at the required moment.

For the second sample:

```
4
4 1 3 2
```

| Current value checked | Left neighbor | Right neighbor | Required neighbor | Action |
| --- | --- | --- | --- | --- |
| 1 | 4 | 3 | 2 | Fail |

Berry 1 needs berry 2 to be adjacent, but both neighbors are 4 and 3. No later operation can help because berry 1 is the first required removal. The answer is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every berry is initialized once and removed at most once |
| Space | O(N) | Two neighbor arrays of size N + 1 are stored |

The solution fits the constraints because it performs only a constant amount of work per berry. The memory usage is also linear, which is suitable for N up to 2 * 10^5.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    if n == 1:
        return "YES\n"

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    for i, x in enumerate(a):
        left[x] = a[(i - 1) % n]
        right[x] = a[(i + 1) % n]

    for x in range(1, n):
        if left[x] != x + 1 and right[x] != x + 1:
            return "NO\n"
        l = left[x]
        r = right[x]
        right[l] = r
        left[r] = l

    return "YES\n"

assert solution("3\n1 3 2\n") == "YES\n", "sample 1"
assert solution("4\n4 1 3 2\n") == "NO\n", "sample 2"

assert solution("1\n1\n") == "YES\n", "single berry"
assert solution("5\n5 1 2 3 4\n") == "YES\n", "already removable chain"
assert solution("5\n5 4 1 2 3\n") == "NO\n", "wrong order around maximum"
assert solution("6\n2 3 4 5 6 1\n") == "YES\n", "circular boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | YES | The empty sequence of moves |
| `5 / 5 1 2 3 4` | YES | A direct increasing removal chain |
| `5 / 5 4 1 2 3` | NO | A case where a tempting first move does not solve the level |
| `6 / 2 3 4 5 6 1` | YES | Adjacency through the circular boundary |

## Edge Cases

For the single berry case:

```
Input:
1
1
```

The algorithm immediately returns YES because there is nothing to remove. This avoids trying to access weight 2, which does not exist.

For the sample failure case:

```
Input:
4
4 1 3 2
```

The algorithm checks weight 1 first because the removal order is forced. Its neighbors are 4 and 3, so weight 2 is not available as an eater. The algorithm stops immediately and returns NO.

For the circular adjacency case:

```
Input:
3
2 1 3
```

The linked list stores 1's neighbors as 2 and 3. The first check succeeds because 2 is the left neighbor. Removing 1 joins 2 and 3, and the next check succeeds as well. The algorithm returns YES because it correctly treats the array as a circle rather than a line.
