---
title: "CF 105048C - Wordy Painting"
description: "We are maintaining a grid of stacks. Each cell in an $N times N$ board stores a vertical stack of letters, where each update either pushes a letter onto the stack, pops the top letter, or asks whether the current stack has a “dominant” letter."
date: "2026-06-28T05:41:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 104
verified: false
draft: false
---

[CF 105048C - Wordy Painting](https://codeforces.com/problemset/problem/105048/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining a grid of stacks. Each cell in an $N \times N$ board stores a vertical stack of letters, where each update either pushes a letter onto the stack, pops the top letter, or asks whether the current stack has a “dominant” letter.

A stack is considered beautiful under a query if the queried letter appears strictly more than half of the elements currently in that stack.

So each operation is localized to a single cell, but the key difficulty is that the sequence is dynamic: pushes and pops change the stack height over time, and queries must reflect the current multiset of letters in that stack.

The constraints are the real signal. The grid is small ($N \le 100$), so there are at most 10,000 independent stacks. However, the number of operations can reach $2 \cdot 10^5$. This rules out any per-query scan of a stack, since a single stack could grow linearly with operations. In the worst case, repeatedly pushing to one cell creates a stack of size $2 \cdot 10^5$, and scanning it per query would immediately exceed time limits.

A naive approach that counts frequencies in the stack for every query would cost $O(k)$ per query, where $k$ is stack height, leading to $O(Q^2)$ in the worst case.

A subtle edge case comes from deletions on empty stacks. A remove operation on an untouched cell does nothing, but a careless implementation that assumes the stack exists may raise errors or incorrectly decrement counts below zero.

Another tricky scenario is interleaving operations on the same cell:

Input:

```
0 a 0 0
0 b 0 0
2 a 0 0
1 0 0
2 a 0 0
```

The correct behavior requires tracking exact order: after pushing `a`, then `b`, the stack is `[a, b]`, so neither letter is a majority; after popping, the stack is `[a]`, so `a` becomes dominant.

## Approaches

The brute-force solution is straightforward: for each cell, maintain a list representing its stack. A push appends, a pop removes the last element if present, and a query counts occurrences of the target letter in the entire stack and checks whether it exceeds half the stack size.

This is correct because it directly simulates the definition. The issue is performance. Each query requires scanning up to the stack size, and in adversarial cases the stack size grows to $O(Q)$. With up to $2 \cdot 10^5$ operations, this becomes $O(Q^2)$, which is too slow.

The key observation is that we do not need full frequency information for all letters, only for the queried candidate letter at that moment. However, even maintaining counts alone is insufficient if we want to verify majority dynamically under deletions, because removing arbitrary letters from a stack changes the balance over time.

The structure becomes simpler if we maintain, for each cell, a frequency map of letters in the current stack. Then each push increments one count, each pop decrements the count of the removed top letter, and we also maintain the current stack size. This makes each operation $O(1)$ on average, and each query is also $O(1)$: we only check whether `freq[l] > size/2`.

The only missing piece is knowing what letter to decrement during a pop, which requires storing the actual stack content, not just counts.

This leads to the optimal design: each cell stores both a stack (for order) and a frequency dictionary (for counts).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (scan stack per query) | $O(Q^2)$ | $O(Q)$ | Too slow |
| Stack + frequency map per cell | $O(Q)$ | $O(N^2 + Q)$ | Accepted |

## Algorithm Walkthrough

1. Initialize a grid of size $N \times N$, where each cell contains an empty stack and an empty frequency map.

This allows us to isolate operations per coordinate so that no global recomputation is required.
2. For a paint operation at $(x, y)$, push the letter onto the stack at that cell and increment its frequency counter.

The stack ensures we can undo this correctly later, and the counter keeps aggregate information in constant time.
3. For a remove operation at $(x, y)$, check whether the stack is non-empty. If it is empty, do nothing.

If not empty, pop the top element and decrement its frequency. This guarantees consistency between order and counts.
4. For a query at $(x, y)$ with letter $l$, compute the current stack size. If it is zero, output “no”.

Otherwise check whether `frequency[l] * 2 > size`. This directly encodes strict majority without floating-point operations.

### Why it works

At every moment, each cell’s stack is exactly represented by its stored list, and the frequency map exactly matches the multiset of letters in that stack. Push and pop operations preserve this invariant because every insertion or deletion updates both structures consistently. Therefore, when answering a query, the frequency map provides the exact count of the queried letter in the current stack, and comparing it against half the stack size correctly determines whether it forms a strict majority.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, Q = map(int, input().split())
    
    grid = [[[] for _ in range(N)] for _ in range(N)]
    freq = [[dict() for _ in range(N)] for _ in range(N)]
    size = [[0 for _ in range(N)] for _ in range(N)]
    
    out = []
    
    for _ in range(Q):
        parts = input().split()
        s = int(parts[0])
        
        if s == 0:
            l = parts[1]
            x = int(parts[2])
            y = int(parts[3])
            
            grid[x][y].append(l)
            size[x][y] += 1
            freq[x][y][l] = freq[x][y].get(l, 0) + 1
        
        elif s == 1:
            x = int(parts[1])
            y = int(parts[2])
            
            if size[x][y] == 0:
                continue
            
            ch = grid[x][y].pop()
            size[x][y] -= 1
            freq[x][y][ch] -= 1
            if freq[x][y][ch] == 0:
                del freq[x][y][ch]
        
        else:
            l = parts[1]
            x = int(parts[2])
            y = int(parts[3])
            
            if size[x][y] == 0:
                out.append("no")
            else:
                if freq[x][y].get(l, 0) * 2 > size[x][y]:
                    out.append("yes")
                else:
                    out.append("no")
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution keeps a per-cell stack to maintain order and support correct popping behavior. The frequency dictionary is updated in lockstep with stack changes, ensuring constant-time majority checks during queries. The separate `size` array avoids recomputing lengths repeatedly.

One subtle implementation detail is deleting dictionary entries when their count drops to zero. This is not required for correctness, but it keeps memory bounded and avoids misleading keys during `.get()` checks.

## Worked Examples

### Example 1

Consider a single cell $(0,0)$:

| Step | Operation | Stack | Frequency | Size | Query result |
| --- | --- | --- | --- | --- | --- |
| 1 | push a | [a] | {a:1} | 1 | - |
| 2 | push b | [a,b] | {a:1,b:1} | 2 | - |
| 3 | query a | [a,b] | {a:1,b:1} | 2 | no |
| 4 | pop | [a] | {a:1} | 1 | - |
| 5 | query a | [a] | {a:1} | 1 | yes |

This shows that majority depends on current stack state, not historical dominance.

### Example 2

Single cell with repeated pushes:

| Step | Operation | Stack | Frequency | Size | Query l='a' |
| --- | --- | --- | --- | --- | --- |
| 1 | push a | [a] | {a:1} | 1 | yes |
| 2 | push b | [a,b] | {a:1,b:1} | 2 | no |
| 3 | push a | [a,b,a] | {a:2,b:1} | 3 | yes |

This demonstrates that the frequency structure correctly tracks evolving majority.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q)$ | Each operation updates or queries constant-time structures per cell |
| Space | $O(N^2 + Q)$ | Grid storage plus total pushed elements across all stacks |

The constraints allow up to $2 \cdot 10^5$ operations, so linear time with hash map updates is sufficient within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# minimal single cell behavior
assert run("""1 5
0 a 0 0
0 b 0 0
2 a 0 0
1 0 0
2 a 0 0
""") == "no\nyes"

# all same letter always majority
assert run("""2 4
0 a 0 0
0 a 0 0
2 a 0 0
2 b 0 0
""") == "yes\nno"

# empty stack query
assert run("""2 1
2 a 0 0
""") == "no"

# push-pop stability
assert run("""1 6
0 a 0 0
0 b 0 0
0 a 0 0
1 0 0
1 0 0
2 a 0 0
""") == "yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty query | no | handles empty stacks safely |
| alternating pushes | yes/no | correctness of majority updates |
| repeated letters | yes | strict majority condition |
| push-pop cycles | yes | consistency of stack + frequency sync |

## Edge Cases

A critical edge case is querying an empty stack. The implementation explicitly checks size before accessing the frequency map. Without this guard, a naive division or lookup could incorrectly treat missing keys as zero and still proceed, which is correct only if the size is handled carefully.

Another case is repeated pop operations on empty stacks. Since the operation must be a no-op, the implementation avoids underflow by checking `size[x][y] == 0` before popping. This ensures that stack and frequency map never diverge.

A final subtle case is when a letter disappears completely from a stack. Removing dictionary entries when count reaches zero prevents stale keys from misleading future logic that assumes key presence implies positivity.
