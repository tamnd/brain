---
problem: 982B
contest_id: 982
problem_index: B
name: "Bus of Characters"
contest_name: "Codeforces Round 484 (Div. 2)"
rating: 1300
tags: ["data structures", "greedy", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 64
date: 2026-06-18
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a337532-184c-83ec-bd9a-f66c9654df9d
---

# CF 982B - Bus of Characters

**Rating:** 1300  
**Tags:** data structures, greedy, implementation  
**Model:** gpt-5-5  
**Solve time:** 1m 4s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a337532-184c-83ec-bd9a-f66c9654df9d  

---

## Solution

## Problem Understanding

The bus consists of $n$ independent rows, each row containing exactly two seats. Each row has a fixed width $w_i$, and all widths are distinct, so we can always compare rows without ambiguity.

Passengers arrive one by one in a fixed order. There are two types of behavior. An introvert always insists on sitting in a completely empty row, and among all such rows chooses the one with the smallest width. An extrovert can only sit in a row that already has exactly one occupied seat, and among those partially filled rows chooses the one with the largest width.

The task is to simulate this process and output, for every passenger in arrival order, which row they take.

The constraints go up to $n = 200{,}000$, so the simulation involves up to $2n = 400{,}000$ operations. Any solution that scans all rows for each passenger would behave like $O(n^2)$, which is far beyond feasible limits. This immediately forces us to maintain ordered sets of candidate rows so that each decision can be made in logarithmic time.

A subtle issue appears in the interaction between the two groups. Introverts remove rows from the “empty set” and move them into a “half-filled set”. Extroverts consume from that half-filled set. A naive implementation that recomputes these sets by scanning all rows will fail not because of correctness, but because it will time out long before finishing.

Edge cases arise when the smallest-width empty row and largest-width half-filled row evolve in interleaving ways. For example, if widths are $[1,2,3]$ and the order is $010101$, the structure of available sets changes after every move, and correctness depends on always picking from the correct dynamic frontier rather than recomputing from scratch.

## Approaches

A brute-force simulation would, for each passenger, scan all rows and check whether they are empty or half-occupied, then apply the selection rule. For an introvert, this means scanning all $n$ rows to find the minimum width among empty ones, and for an extrovert scanning again to find the maximum among half-filled ones. Each passenger costs $O(n)$, leading to $O(n^2)$ total operations, roughly $1.6 \times 10^{11}$ checks at worst, which is infeasible.

The key observation is that both choices depend on maintaining a dynamically changing ordered structure. Introverts always need the minimum among available empty rows, and extroverts always need the maximum among partially filled rows. This is exactly what priority queues (heaps) or balanced ordered sets are designed for. If we store empty rows in a min-heap keyed by width, and half-filled rows in a max-heap keyed by width, each operation becomes a single push or pop in logarithmic time.

We also need to remember which row a given width corresponds to, so that when we output assignments we can map back to row indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal (heaps) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain two priority structures. One stores all currently empty rows ordered by increasing width. The other stores all rows that already have one passenger, ordered by decreasing width.

We also maintain a mapping from width to row index, since selection is based on width but output requires row numbers.

### Steps

1. Initialize a mapping from each width $w_i$ to its row index $i$. This ensures we can convert a chosen width back to the correct output row.
2. Insert all rows into a min-heap of empty rows keyed by width. At the start, every row is empty.
3. Maintain an empty max-heap for half-occupied rows. This heap will store rows after an introvert takes the first seat.
4. Process passengers in order from the input string.
5. If the current passenger is an introvert, extract the row with the smallest width from the empty heap. Assign this row to the passenger, then push it into the half-occupied heap. The reasoning is that this row is no longer empty and should now become eligible for extroverts.
6. If the current passenger is an extrovert, extract the row with the largest width from the half-occupied heap. Assign this row to the passenger and remove it completely, since both seats are now filled. The choice rule guarantees correctness because extroverts always prefer the largest width among partially filled rows.

### Why it works

At any moment, every row belongs to exactly one of three states: completely unused, partially filled, or fully filled. The introvert rule only interacts with unused rows, and the extrovert rule only interacts with partially filled rows. The heaps enforce that the best candidate according to each rule is always available in $O(1)$ access time and removable in $O(\log n)$. Since rows never move backward between states, the structure remains consistent throughout the process, preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    w = list(map(int, input().split()))
    s = input().strip()

    import heapq

    # min-heap for empty rows: (width, row_index)
    empty = []
    # max-heap for half-occupied rows: (-width, row_index)
    half = []

    for i, wi in enumerate(w, 1):
        heapq.heappush(empty, (wi, i))

    res = []

    for c in s:
        if c == '0':
            wi, idx = heapq.heappop(empty)
            res.append(idx)
            heapq.heappush(half, (-wi, idx))
        else:
            wi_neg, idx = heapq.heappop(half)
            res.append(idx)

    print(*res)

if __name__ == "__main__":
    solve()
```

The empty heap stores all unused rows sorted by width so that introverts can always take the smallest available row. Once a row is chosen, it is moved into the half-filled heap with its width negated so that Python’s min-heap behaves like a max-heap.

The half-filled heap ensures extroverts always retrieve the row with maximum width among those available. Once an extrovert takes a seat, the row is fully occupied and removed entirely.

The key implementation detail is that rows are never reinserted into the empty heap, and each row moves exactly once into the half-filled heap, guaranteeing correct state transitions.

## Worked Examples

### Example 1

Input:

```
n = 2
w = [3, 1]
s = 0011
```

We track both heaps.

| Step | Passenger | Empty heap | Half heap | Chosen row |
| --- | --- | --- | --- | --- |
| 1 | 0 | [(1,2),(3,1)] | [] | 2 |
| 2 | 0 | [(3,1)] | [(1,2)] | 1 |
| 3 | 1 | [(3,1)] | [(1,2)] | 1 |
| 4 | 1 | [(3,1)] | [] | 2 |

The first introvert takes row 2 because it has width 1, the smallest. The second introvert takes row 1. The first extrovert takes row 1 since it is the only partially filled row. The last extrovert takes row 2.

### Example 2

Input:

```
n = 3
w = [5, 2, 4]
s = 010110
```

| Step | Passenger | Empty heap | Half heap | Chosen row |
| --- | --- | --- | --- | --- |
| 1 | 0 | [(2,2),(5,1),(4,3)] | [] | 2 |
| 2 | 1 | [(4,3),(5,1)] | [(2,2)] | 2 |
| 3 | 0 | [(4,3),(5,1)] | [(2,2)] | 3 |
| 4 | 1 | [(5,1)] | [(2,2),(4,3)] | 3 |
| 5 | 1 | [(5,1)] | [(2,2)] | 3 |
| 6 | 0 | [] | [(2,2)] | 1 |

These traces show that each heap independently maintains the correct extremum for its state, and transitions preserve ordering without needing rescans.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each row is pushed and popped at most once per heap transition |
| Space | $O(n)$ | Two heaps store at most all rows |

The logarithmic overhead is small enough for $2 \cdot 10^5$ rows, and total operations stay well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("2\n3 1\n0011\n") == "2 1 1 2"

# minimum size
assert run("1\n10\n01\n") == "1 1"

# already sorted small
assert run("3\n1 2 3\n000111\n") == "1 2 3 3 2 1"

# reverse order
assert run("3\n3 2 1\n000111\n") == "3 2 1 1 2 3"

# alternating pattern
assert run("2\n5 10\n0101\n") == "1 1 2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single row | 1 1 | minimal boundary handling |
| increasing widths | 1 2 3 3 2 1 | correct ordering transitions |
| decreasing widths | 3 2 1 1 2 3 | symmetry correctness |
| alternating pattern | 1 1 2 2 | interleaving heap updates |

## Edge Cases

A key edge case is when the smallest empty row becomes the largest among future half-filled rows later in the sequence. Since widths are distinct and state transitions are one-way, the algorithm does not need to reconcile conflicts between heaps; once a row leaves the empty heap, it never competes there again.

For input:

```
n = 2
w = [2, 1]
s = 0101
```

Step-by-step:

Introvert picks row 2 first (width 1), then extrovert must choose row 2 or 1 depending on half heap. The heaps ensure row 2 is correctly in the half-filled structure, so the extrovert behavior remains consistent.

This confirms that state separation, not recomputation, is what preserves correctness throughout the full simulation.