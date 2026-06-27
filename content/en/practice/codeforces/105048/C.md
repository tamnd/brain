---
title: "CF 105048C - Wordy Painting"
description: "The canvas consists of $N times N$ independent positions, and each position behaves like a vertical stack of letters. Every time a letter is “painted” onto a position, it is pushed onto the top of that stack."
date: "2026-06-28T05:07:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 86
verified: false
draft: false
---

[CF 105048C - Wordy Painting](https://codeforces.com/problemset/problem/105048/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

The canvas consists of $N \times N$ independent positions, and each position behaves like a vertical stack of letters. Every time a letter is “painted” onto a position, it is pushed onto the top of that stack. Later, Shakespeare may remove the top letter from a chosen stack, or ask whether a certain letter is currently dominant in that stack.

A stack is considered “beautiful” for a given query letter if that letter appears strictly more than half of the elements currently in the stack at that position. So for a stack of size $k$, we need the frequency of the queried letter to exceed $k/2$.

The key point is that all operations are online. We must process up to $2 \cdot 10^5$ operations, each of which either modifies a single stack or queries it.

The constraint $N \le 100$ implies at most $10^4$ stacks exist, but the total number of pushed letters across all stacks is still $O(Q)$. This means any solution must treat each operation as essentially constant time per affected stack. Any approach that scans an entire stack for every query will fail because a single stack can grow to size $2 \cdot 10^5$, and repeated scanning would lead to quadratic behavior.

A subtle edge case is removing from an empty or never-used stack. In that case, the operation is ignored. For example, if we attempt a removal at $(x,y)$ before any insertion:

Input:

```
1 2
1 0 0
2 a 0 0
```

The stack is empty when queried, so the answer must be “no” because the frequency of any letter is zero while the size is zero, and zero is not strictly greater than zero.

A naive implementation that assumes every stack exists and blindly pops without checking emptiness may raise errors or corrupt state.

## Approaches

The brute-force idea is straightforward. For each query, we look at the entire stack at position $(x,y)$, count how many times the queried letter appears, and compare it to half the stack size. This is correct because it directly follows the definition of “majority”.

However, this becomes too slow because a stack can contain up to $O(Q)$ elements. If we repeatedly scan it for each query, the worst case becomes $O(Q^2)$, which is around $4 \cdot 10^{10}$ operations and far beyond limits.

The key observation is that we never need the full distribution of letters per query, only the frequency of a single letter and the total stack size. Both of these can be maintained incrementally. Each stack behaves independently, so we can store for each cell its current stack and a frequency table of size 26. Every push updates both structures, every pop reverses them, and each query becomes a constant-time comparison.

This reduces the problem from repeated recomputation to maintaining a dynamic frequency structure per stack.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(Q \cdot H)$ worst-case per query leading to $O(Q^2)$ | $O(Q)$ | Too slow |
| Incremental frequency maintenance | $O(Q)$ | $O(N^2 + Q)$ | Accepted |

## Algorithm Walkthrough

We treat each grid position as an independent stack with auxiliary frequency counts.

1. Initialize for every cell an empty list representing the stack and an array of 26 zeros representing letter frequencies. This allows constant-time updates without recomputation.
2. For a paint operation at $(x,y)$, append the letter to the stack and increment its frequency counter. This keeps both the order and aggregate information consistent.
3. For a removal operation at $(x,y)$, check whether the stack is non-empty. If it is empty, do nothing. Otherwise, remove the last element and decrement its frequency. This ensures the frequency table always matches the actual stack content.
4. For a query at $(x,y)$ with letter $c$, compute the current stack size and compare the stored frequency of $c$ against half the size. If it is strictly greater, output “yes”, otherwise output “no”.
5. Repeat until all operations are processed.

### Why it works

The correctness relies on maintaining a strict invariant: at every moment, for each cell, the stack list exactly represents the sequence of inserted letters, and the frequency array exactly matches the multiset of letters in that stack. Every operation preserves this invariant because push adds one element consistently to both structures, and pop removes the same element from both. Since queries depend only on total size and a single frequency count, both derived values are always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def idx(c):
    return ord(c) - 97

def main():
    N, Q = map(int, input().split())

    stacks = [[[] for _ in range(N)] for _ in range(N)]
    freq = [[[0] * 26 for _ in range(N)] for _ in range(N)]

    for _ in range(Q):
        parts = input().split()
        if not parts:
            continue
        t = int(parts[0])

        if t == 0:
            c = idx(parts[1])
            x = int(parts[2])
            y = int(parts[3])

            stacks[x][y].append(c)
            freq[x][y][c] += 1

        elif t == 1:
            x = int(parts[1])
            y = int(parts[2])

            if stacks[x][y]:
                c = stacks[x][y].pop()
                freq[x][y][c] -= 1

        else:
            c = idx(parts[1])
            x = int(parts[2])
            y = int(parts[3])

            sz = len(stacks[x][y])
            if sz == 0:
                print("no")
            else:
                print("yes" if freq[x][y][c] > sz // 2 else "no")

if __name__ == "__main__":
    main()
```

The implementation mirrors the algorithm directly. Each grid cell stores two synchronized structures: a Python list for stack order and a 26-element array for counts. The most important detail is handling empty removals safely, since popping from an empty list would otherwise cause an error.

Integer division with `sz // 2` is safe because the condition requires a strict majority, so we never need floating-point comparisons.

## Worked Examples

Consider a single cell $(0,0)$:

Input:

```
0 1 a 0 0
0 1 a 0 0
0 1 b 0 0
2 a 0 0
```

| Step | Operation | Stack | freq(a) | freq(b) | Size | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | push a | [a] | 1 | 0 | 1 | - |
| 2 | push a | [a,a] | 2 | 0 | 2 | - |
| 3 | push b | [a,a,b] | 2 | 1 | 3 | - |
| 4 | query a | [a,a,b] | 2 | 1 | 3 | yes |

The query checks whether $2 > 3/2$, which holds.

Now consider removal behavior:

Input:

```
1 0 0
1 0 0
2 a 0 0
```

| Step | Operation | Stack | freq(a) | Size | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | pop empty | [] | 0 | 0 | - |
| 2 | pop empty | [] | 0 | 0 | - |
| 3 | query a | [] | 0 | 0 | no |

This confirms that safe handling of empty stacks is required and correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q)$ | Each operation updates or queries a single stack in constant time |
| Space | $O(N^2 + Q)$ | Each cell stores a stack whose total size over all cells is bounded by total pushes |

The constraints allow up to $2 \cdot 10^5$ operations, so linear time processing is comfortably within limits. The memory usage remains safe because stacks collectively store at most one entry per paint operation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N, Q = map(int, input().split())

    stacks = [[[] for _ in range(N)] for _ in range(N)]
    freq = [[[0] * 26 for _ in range(N)] for _ in range(N)]

    out = []

    for _ in range(Q):
        parts = input().split()
        t = int(parts[0])

        if t == 0:
            c = ord(parts[1]) - 97
            x, y = map(int, parts[2:4])
            stacks[x][y].append(c)
            freq[x][y][c] += 1

        elif t == 1:
            x, y = map(int, parts[1:3])
            if stacks[x][y]:
                c = stacks[x][y].pop()
                freq[x][y][c] -= 1

        else:
            c = ord(parts[1]) - 97
            x, y = map(int, parts[2:4])
            sz = len(stacks[x][y])
            out.append("yes" if sz and freq[x][y][c] > sz // 2 else "no")

    return "\n".join(out)

# custom cases

assert run("1 3\n0 a 0 0\n0 a 0 0\n2 a 0 0\n") == "yes"
assert run("1 3\n0 a 0 0\n0 b 0 0\n2 a 0 0\n") == "no"
assert run("1 4\n0 a 0 0\n1 0 0\n2 a 0 0\n2 b 0 0\n") == "no\nno"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| push-only majority | yes | majority detection |
| mixed letters | no | correct frequency tracking |
| empty after pop | no, no | safe empty handling |

## Edge Cases

A critical edge case is repeated removals from an empty stack. The algorithm explicitly checks for emptiness before popping, so the state remains unchanged and queries still return based on an empty structure, producing “no”.

Another case is stacks that oscillate heavily between insertions and deletions. Because every update modifies both the stack and frequency array synchronously, the invariant never breaks, even under adversarial sequences.

Finally, queries on empty stacks always return “no”. The implementation enforces this by checking size before comparing frequencies, avoiding invalid majority checks on zero-length structures.
