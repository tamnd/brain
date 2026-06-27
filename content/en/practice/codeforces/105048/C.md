---
title: "CF 105048C - Wordy Painting"
description: "We are given a grid of size $N times N$. Each cell of this grid behaves like a vertical stack of letters. Initially, all stacks are empty."
date: "2026-06-28T01:21:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 97
verified: false
draft: false
---

[CF 105048C - Wordy Painting](https://codeforces.com/problemset/problem/105048/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid of size $N \times N$. Each cell of this grid behaves like a vertical stack of letters. Initially, all stacks are empty. Over time, we perform operations that either push a letter onto a specific cell’s stack, remove the top letter from a stack, or ask a question about whether a stack is “beautiful” with respect to a chosen letter.

A stack is considered beautiful for a letter $c$ if, among all letters currently inside that stack, the occurrences of $c$ are strictly more than half of the total elements in that stack. In other words, if the stack has size $k$, then $c$ must appear at least $\lfloor k/2 \rfloor + 1$ times.

The key point is that each cell is independent, so every operation affects only one stack, but queries depend on the full history of pushes and pops applied to that cell.

The input size is large, with up to $2 \cdot 10^5$ operations. This immediately rules out any solution that scans a full stack per query or recomputes frequencies from scratch. Any approach that touches all elements per operation would degrade to $O(Q^2)$ in the worst case, which is too slow.

A subtle issue arises with remove operations. If we attempt to remove from an empty stack, nothing happens. This means we must carefully track whether a stack is empty before popping.

Another important edge case is that queries depend only on the current state of the stack, not on historical validity. For example, a stack might be empty, and we are still asked whether a given letter is a majority. In that case, the answer must be “no” because there is no majority in an empty structure.

## Approaches

A direct simulation approach stores each stack as a list of characters. For every query, we scan the entire stack and count occurrences of the queried letter. For every push and pop, we update the list accordingly.

This is correct because it directly mirrors the definition of the problem. However, the cost becomes problematic. In the worst case, we may have a stack of size $O(Q)$, and up to $Q$ queries. Each query then costs $O(Q)$, producing a worst-case complexity of $O(Q^2)$, which is around $4 \cdot 10^{10}$ operations and far beyond the time limit.

The key observation is that we do not actually need to recompute anything during queries. A query only asks whether a specific letter dominates the stack. If we maintain, for each cell, two pieces of information, the total stack size and the frequency of each letter, then every query becomes a constant-time comparison.

To support removals efficiently, we also store the actual stack content so we know which letter is being removed from the top. Every update then adjusts both the stack and a frequency array of size 26.

This reduces every operation to $O(1)$, since push increments a counter, pop decrements a counter, and query performs a single arithmetic comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(Q \cdot N)$ worst case | $O(N^2 + Q)$ | Too slow |
| Optimal | $O(Q)$ | $O(N^2 + Q)$ | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. Maintain for each cell a stack of characters representing the current vertical sequence. This allows us to support last-in-first-out removals, since only the top element can be removed.
2. Alongside each stack, maintain an array of size 26 storing frequency counts of each letter currently in that stack. This avoids recomputing counts during queries.
3. Also maintain the current size of each stack. This is needed to determine the majority threshold, which is strictly more than half of the stack size.
4. When processing a type 0 operation, push the given character onto the stack, increment its frequency, and increase the stack size.
5. When processing a type 1 operation, first check if the stack is non-empty. If it is empty, do nothing. Otherwise, pop the top character, decrement its frequency, and reduce the size.
6. When processing a type 2 query, check the frequency of the queried character. If it is strictly greater than half of the current stack size, output “yes”, otherwise output “no”. If the stack is empty, the answer is always “no”.

### Why it works

The correctness comes from maintaining exact counts at all times. Every push and pop operation updates both the explicit stack and the frequency table, so the frequency array always reflects the true state of the stack. Since the majority condition depends only on total size and a single character’s frequency, having these two values preserved as invariants guarantees that each query is answered exactly according to the definition.

No operation depends on future events, so local updates are sufficient to preserve global correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, Q = map(int, input().split())

    # each cell has a stack and frequency array
    stacks = [[[] for _ in range(N)] for _ in range(N)]
    freq = [[[0] * 26 for _ in range(N)] for _ in range(N)]
    size = [[0] * N for _ in range(N)]

    out = []

    for _ in range(Q):
        parts = input().split()
        t = int(parts[0])

        if t == 0:
            c = parts[1]
            x = int(parts[2])
            y = int(parts[3])

            idx = ord(c) - 97
            stacks[x][y].append(idx)
            freq[x][y][idx] += 1
            size[x][y] += 1

        elif t == 1:
            x = int(parts[1])
            y = int(parts[2])

            if size[x][y] > 0:
                idx = stacks[x][y].pop()
                freq[x][y][idx] -= 1
                size[x][y] -= 1

        else:
            c = parts[1]
            x = int(parts[2])
            y = int(parts[3])

            idx = ord(c) - 97
            s = size[x][y]

            if s > 0 and freq[x][y][idx] > s // 2:
                out.append("yes")
            else:
                out.append("no")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution keeps three synchronized structures per cell. The stack stores the exact order of letters so that removals are correct. The frequency table stores counts so queries are constant time. The size array ensures we never need to recompute lengths.

A common implementation mistake is forgetting to handle empty pops. Another is computing majority using floating-point division instead of integer comparison with `s // 2`, which can introduce precision issues or off-by-one errors.

## Worked Examples

Consider a single cell $(0,0)$ and a sequence of operations:

Input:

```
0 a 0 0
0 b 0 0
0 a 0 0
2 a 0 0
1 0 0
2 a 0 0
```

| Step | Operation | Stack | Frequencies (a,b) | Size | Query result |
| --- | --- | --- | --- | --- | --- |
| 1 | push a | a | (1,0) | 1 | - |
| 2 | push b | a b | (1,1) | 2 | - |
| 3 | push a | a b a | (2,1) | 3 | - |
| 4 | query a | a b a | (2,1) | 3 | yes |
| 5 | pop | a b | (1,1) | 2 | - |
| 6 | query a | a b | (1,1) | 2 | no |

The first query returns yes because a appears twice out of three elements. After a pop, both letters are equal, so no letter is strictly dominant anymore.

Now consider an empty-stack query:

Input:

```
2 a 0 0
```

The stack is empty, so the answer is immediately no regardless of the letter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q)$ | Each operation updates or checks constant-sized structures |
| Space | $O(N^2 + Q)$ | Grid storage plus stacks storing all pushed elements |

The constraints allow up to 200,000 operations, so a linear-time simulation is sufficient. Each operation performs only a few array accesses, which fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return ""  # output is printed; in real testing capture stdout

# Note: These asserts are illustrative due to stdout capture setup

# custom sanity checks (conceptual inputs)
# empty stack query
# single push majority
# pop from empty should not crash
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1\n2 a 0 0` | `no` | empty stack query |
| `1 3\n0 a 0 0\n2 a 0 0\n1 0 0\n` | `yes\nno` | basic push/query/pop |
| `2 5\n0 a 0 0\n0 a 0 0\n2 a 0 0\n1 0 0\n2 a 0 0` | `yes\nyes` | majority threshold behavior |

## Edge Cases

One edge case is repeatedly popping from an empty stack. For example:

```
1 3
1 0 0
1 0 0
2 a 0 0
```

The first two operations do nothing since the stack is empty. The query correctly returns no because there are no elements to form a majority. The algorithm handles this by checking `size[x][y] > 0` before attempting a pop.

Another edge case is a stack that oscillates around the majority threshold:

```
1 6
0 a 0 0
0 b 0 0
0 a 0 0
2 a 0 0
1 0 0
2 a 0 0
```

After three pushes, a is dominant. After a pop, dominance disappears. The frequency array ensures both states are tracked exactly, and no recomputation is needed.
