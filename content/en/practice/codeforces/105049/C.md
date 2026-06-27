---
title: "CF 105049C - Wordy Painting"
description: "We are maintaining a grid of stacks, one stack per cell in an $N times N$ canvas. Each stack holds a sequence of lowercase letters in the order they are painted, with the most recent letter on top."
date: "2026-06-28T01:14:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105049
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 1 (Advanced)"
rating: 0
weight: 105049
solve_time_s: 76
verified: false
draft: false
---

[CF 105049C - Wordy Painting](https://codeforces.com/problemset/problem/105049/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining a grid of stacks, one stack per cell in an $N \times N$ canvas. Each stack holds a sequence of lowercase letters in the order they are painted, with the most recent letter on top. The system supports three types of operations: pushing a letter onto a stack at a coordinate, popping the top letter from a stack at a coordinate, and asking whether a given stack is “beautiful” with respect to a chosen letter.

A stack is considered beautiful if that chosen letter appears strictly more than half of the elements currently in that stack. Each query provides both a coordinate and a candidate letter, and we must answer whether that letter is currently a strict majority in that stack.

The important structural detail is that $N \le 100$, so there are at most 10,000 stacks, but $Q \le 2 \cdot 10^5$, so operations are heavily dynamic. Each stack evolves independently as a classic push-pop structure.

A naive misunderstanding is to assume queries are global or that letters interact across stacks. They do not. Everything is strictly per cell.

A subtle edge case appears when removing from an empty stack. The operation is explicitly a no-op, so it must not create underflow behavior or negative structure sizes.

Another corner case is repeated queries on the same stack after many alternating push and pop operations. A solution that recomputes counts from scratch per query would still be correct but far too slow.

## Approaches

A direct brute-force method would store each stack as a list. For each query, it would scan the entire stack and count occurrences of the target letter. This is correct because it directly implements the definition of majority. However, in the worst case a stack can grow to size $O(Q)$, and there can be $O(Q)$ queries. This leads to $O(Q^2)$ behavior in the worst scenario, which is far beyond the limit of 200,000 operations.

The key observation is that we do not need the full frequency distribution of a stack to answer a query. We only need to know whether one specific letter exceeds half the stack size. That reduces the problem from maintaining full histograms for all letters in all stacks to maintaining a single dynamic structure per stack that can quickly tell us the current count of a given letter.

Since each stack is independent and operations only affect one stack, we can maintain for each cell a dictionary of counts per letter alongside the actual stack contents. Push increments the count for that letter, pop decrements it, and query becomes a direct lookup followed by a comparison with half the stack size.

The structure is essentially a per-cell multiset with fast membership counts and a standard stack for rollback.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(Q \cdot N)$ | $O(N^2)$ | Too slow |
| Optimal | $O(Q)$ amortized | $O(N^2 + Q)$ | Accepted |

## Algorithm Walkthrough

We maintain two arrays indexed by coordinates. One stores the current stack of letters for each cell, and the other stores a frequency dictionary for that stack.

1. Initialize an $N \times N$ grid where each cell has an empty list and an empty frequency map. The list represents the stack order, and the map tracks counts of each letter currently present.
2. For a type 0 operation (push), identify the target cell $(x, y)$. Append the letter to the stack list, then increment its frequency in the map. This ensures both structural order and count information remain consistent.
3. For a type 1 operation (pop), first check if the stack is non-empty. If it is empty, do nothing. If not empty, remove the last element from the stack list and decrement its count in the frequency map. If a count reaches zero, it can be deleted for cleanliness, though this is optional.
4. For a type 2 operation (query), retrieve the stack at $(x, y)$. Let its size be $m$. Compute the count of the queried letter using the frequency map, defaulting to zero if missing. The stack is beautiful if this count is strictly greater than $m/2$. Output “yes” or “no” accordingly.

The crucial reason this works is that all operations preserve a perfect synchronization between the explicit stack and the frequency map. Every push increases both size and count; every pop decreases both. Thus at any moment the frequency map is an exact representation of the stack content distribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    
    grid_stack = [[[] for _ in range(n)] for _ in range(n)]
    grid_cnt = [[{} for _ in range(n)] for _ in range(n)]
    
    out = []
    
    for _ in range(q):
        parts = input().split()
        t = int(parts[0])
        
        if t == 0:
            ch = parts[1]
            x = int(parts[2])
            y = int(parts[3])
            
            st = grid_stack[x][y]
            cnt = grid_cnt[x][y]
            
            st.append(ch)
            cnt[ch] = cnt.get(ch, 0) + 1
        
        elif t == 1:
            x = int(parts[1])
            y = int(parts[2])
            
            st = grid_stack[x][y]
            cnt = grid_cnt[x][y]
            
            if st:
                ch = st.pop()
                cnt[ch] -= 1
                if cnt[ch] == 0:
                    del cnt[ch]
        
        else:
            ch = parts[1]
            x = int(parts[2])
            y = int(parts[3])
            
            st = grid_stack[x][y]
            cnt = grid_cnt[x][y]
            
            m = len(st)
            c = cnt.get(ch, 0)
            
            if c * 2 > m:
                out.append("yes")
            else:
                out.append("no")
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation keeps two synchronized structures per cell. The stack list preserves ordering needed for correct pop behavior. The dictionary maintains frequency counts needed for constant-time majority checks. The multiplication form `c * 2 > m` avoids floating point division and is safe under integer arithmetic.

A common mistake is forgetting that pop must affect both structures. If the frequency map is updated but the stack is not, later pops will remove incorrect elements. If the stack is updated but the map is not, queries become inconsistent.

## Worked Examples

### Example 1

Input:

```
1 6
0 a 0 0
0 a 0 0
0 b 0 0
2 a 0 0
1 0 0
2 a 0 0
```

We track stack (0,0):

| Step | Operation | Stack | Counts | Query result |
| --- | --- | --- | --- | --- |
| 1 | push a | [a] | {a:1} | - |
| 2 | push a | [a,a] | {a:2} | - |
| 3 | push b | [a,a,b] | {a:2,b:1} | - |
| 4 | query a | [a,a,b] | {a:2,b:1} | yes |
| 5 | pop | [a,a] | {a:2} | - |
| 6 | query a | [a,a] | {a:2} | yes |

This demonstrates that majority status changes dynamically with stack size but is always computed from consistent counts.

### Example 2

Input:

```
1 5
0 a 0 0
0 b 0 0
2 a 0 0
1 0 0
2 a 0 0
```

| Step | Operation | Stack | Counts | Query result |
| --- | --- | --- | --- | --- |
| 1 | push a | [a] | {a:1} | - |
| 2 | push b | [a,b] | {a:1,b:1} | - |
| 3 | query a | [a,b] | {a:1,b:1} | no |
| 4 | pop | [a] | {a:1} | - |
| 5 | query a | [a] | {a:1} | yes |

This shows the strict majority requirement: equality is not sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q)$ | Each operation updates or queries a single dictionary and list in amortized constant time |
| Space | $O(N^2 + Q)$ | Grid storage plus total pushed elements across all stacks |

The constraints allow up to 200,000 operations, so any solution with constant or logarithmic time per operation fits comfortably. This approach stays linear and easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    
    grid_stack = [[[] for _ in range(n)] for _ in range(n)]
    grid_cnt = [[{} for _ in range(n)] for _ in range(n)]
    
    out = []
    
    for _ in range(q):
        parts = input().split()
        t = int(parts[0])
        
        if t == 0:
            ch = parts[1]
            x = int(parts[2]); y = int(parts[3])
            grid_stack[x][y].append(ch)
            grid_cnt[x][y][ch] = grid_cnt[x][y].get(ch, 0) + 1
        
        elif t == 1:
            x = int(parts[1]); y = int(parts[2])
            st = grid_stack[x][y]
            if st:
                ch = st.pop()
                grid_cnt[x][y][ch] -= 1
                if grid_cnt[x][y][ch] == 0:
                    del grid_cnt[x][y][ch]
        
        else:
            ch = parts[1]
            x = int(parts[2]); y = int(parts[3])
            st = grid_stack[x][y]
            cnt = grid_cnt[x][y].get(ch, 0)
            out.append("yes" if 2 * cnt > len(st) else "no")
    
    return "\n".join(out)

# provided sample (formatted minimally)
assert run("1 6\n0 a 0 0\n0 a 0 0\n0 b 0 0\n2 a 0 0\n1 0 0\n2 a 0 0\n") == "yes\nyes"

# custom cases
assert run("1 3\n0 a 0 0\n1 0 0\n2 a 0 0\n") == "no", "empty after pop"
assert run("1 4\n0 a 0 0\n0 b 0 0\n2 a 0 0\n2 b 0 0\n") == "no\nno", "tie cases"
assert run("1 5\n0 a 0 0\n0 a 0 0\n1 0 0\n2 a 0 0\n2 a 0 0\n") == "yes\nyes", "consistency after pop"
assert run("2 1\na 0 0\n") == "no", "empty initial stack"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| pop empty then query | no | empty stack behavior |
| equal counts | no no | strict majority rule |
| push-pop consistency | yes yes | synchronized updates |
| query empty stack | no | boundary condition |

## Edge Cases

One edge case is querying an empty stack. In this situation, the stack size is zero and every letter count is zero, so no letter can satisfy a strict majority condition. The algorithm naturally handles this because `len(st) = 0` and any `cnt[ch]` defaults to zero, so `2 * 0 > 0` is false.

Another edge case is repeated popping beyond emptiness. Since the pop operation explicitly checks whether the stack is non-empty before removing, the frequency dictionary is never corrupted by negative counts or invalid deletions.

A third case is rapid alternation of pushes and pops on the same cell. Because both the list and dictionary are updated symmetrically on every operation, the state remains consistent regardless of operation order, and each query always reflects the true current stack composition.
