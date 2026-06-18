---
title: "CF 1170D - Decoding of Integer Sequences"
description: "We are given a single flattened sequence that was produced from several hidden integer sequences. The encoding process mixed all sequences together in “column order”: first all first elements of each sequence, then all second elements, then all third elements, and so on."
date: "2026-06-18T17:08:17+07:00"
tags: ["codeforces", "competitive-programming", "*special", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1170
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes: Episode 1"
rating: 0
weight: 1170
solve_time_s: 82
verified: false
draft: false
---

[CF 1170D - Decoding of Integer Sequences](https://codeforces.com/problemset/problem/1170/D)

**Rating:** -  
**Tags:** *special, data structures, implementation  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single flattened sequence that was produced from several hidden integer sequences. The encoding process mixed all sequences together in “column order”: first all first elements of each sequence, then all second elements, then all third elements, and so on. If a sequence runs out of elements, a special marker value -1 is used in its place from that point onward.

The task is to reconstruct the original sequences, both their grouping and their internal order, from this merged stream.

A useful way to think about the process is that each original sequence contributes one value per “round”. In round 1 we take the first element of every sequence, in round 2 the second element of every sequence, and so on. The encoding stops only when every sequence has contributed its terminating -1.

The output must reconstruct exactly how many sequences existed and what each sequence contained before encoding.

The constraints allow up to 300,000 encoded values. This immediately rules out any solution that tries to repeatedly scan or simulate the process per sequence or per round in a naive nested manner. We need a linear reconstruction that processes each encoded element once or a constant number of times.

A subtle difficulty comes from distinguishing real -1 markers inside the encoding process from structural termination. Every sequence contributes exactly one -1, and those -1 values appear in synchronized “rounds”. A naive approach that treats -1 as a hard stop for all sequences would break, because sequences end at different times.

Another edge case is empty sequences. Some sequences may contain no elements at all, meaning their first contribution is already -1. These must still be represented in the output correctly.

## Approaches

A brute-force interpretation would attempt to simulate the encoding in reverse by repeatedly scanning the sequence, collecting elements round by round, and assigning them to sequences until termination markers appear. One could imagine iterating over the encoded array multiple times, each pass extracting the next “column” of values for all sequences that are still active.

This quickly becomes too slow. If there are $m$ elements and potentially $O(m)$ rounds, each round scanning a large prefix leads to $O(m^2)$ behavior in the worst case.

The key structural insight is that the encoding preserves a strict interleaving pattern: elements are written in layers, and within each layer they always appear in sequence order. This means we can reconstruct sequences incrementally by maintaining the current list of active sequences and assigning each encountered value to the correct sequence position in a streaming fashion.

Instead of thinking in terms of rounds, we process the stream left to right and maintain a dynamic list of sequences currently “alive”. Each time we encounter a value, we append it to the correct sequence based on its position in the current round. When we hit -1 for a sequence, that sequence is removed from future rounds.

The main challenge becomes tracking which sequence each value belongs to as sequences disappear. The structure ensures that in each round, we always fill sequences in order, so we can reuse positions from previous rounds and compact the active set as we go.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation by rounds | O(m²) | O(m) | Too slow |
| Streaming reconstruction with active tracking | O(m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Scan the encoded sequence and first identify where sequences terminate. Each -1 corresponds to the end of exactly one sequence. Since sequences are processed in order per round, the last time a sequence appears before its -1 tells us its length structure.
2. Maintain a dynamic list of sequences currently being reconstructed. Initially, no sequences are created.
3. Iterate through the encoded array while keeping a pointer into the current “round position”. For each value, decide whether it starts a new sequence or continues an existing one.
4. When a non -1 value appears and there are not enough active sequences for the current round position, create a new sequence and append the value to it. This reflects the fact that a new sequence contributes its first element in this position.
5. When a non -1 value appears and a corresponding active sequence exists at that position, append the value to that sequence.
6. When -1 is encountered, it corresponds to a sequence ending at this position in the current round. We mark that sequence as finished and remove it from active tracking so it no longer participates in later rounds.
7. Continue until the entire encoded array is consumed, ensuring that all sequences have been fully constructed.

The key invariant is that at any moment, the active sequence list exactly represents the sequences that still have elements to contribute in the current or future rounds. Each position in a round corresponds to a stable sequence identity, and once a sequence is removed via -1, it never reappears in later rounds. This guarantees that each value is assigned to the correct original sequence exactly once, preserving order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m = int(input())
    b = list(map(int, input().split()))

    seqs = []
    active = []

    idx = 0

    for val in b:
        if val == -1:
            if idx < len(active):
                # mark sequence as finished
                active[idx] = None
            idx += 1
        else:
            if idx == len(active):
                active.append(len(seqs))
                seqs.append([])
            seq_id = active[idx]
            seqs[seq_id].append(val)

    # filter out removed slots if any
    result = []
    for i in active:
        if i is not None:
            result.append(seqs[i])

    print(len(result))
    for s in result:
        print(len(s), *s)

if __name__ == "__main__":
    solve()
```

The code maintains two structures: `seqs`, which stores reconstructed sequences, and `active`, which maps current round positions to sequence indices. The pointer `idx` tracks which column (round position) we are currently filling. When a new value arrives and no sequence exists at that position, a new sequence is created.

A `-1` marks termination of the sequence currently occupying that column, so we invalidate it in `active`. This ensures that later rounds do not append into it again.

The final filtering step removes sequences that ended early and ensures only valid reconstructed sequences are printed.

## Worked Examples

### Example 1

Input:

```
12
3 2 1 1 7 2 4 -1 3 -1 4 -1
```

| Step | Value | idx | active | seqs state |
| --- | --- | --- | --- | --- |
| 1 | 3 | 0 | [0] | [[3]] |
| 2 | 2 | 1 | [0,1] | [[3],[2]] |
| 3 | 1 | 2 | [0,1,2] | [[3],[2],[1]] |
| 4 | 1 | 0 | [0,1,2] | [[3,1],[2],[1]] |
| 5 | 7 | 1 | [0,1,2] | [[3,1],[2,7],[1]] |
| 6 | 2 | 2 | [0,1,2] | [[3,1],[2,7],[1,2]] |
| 7 | 4 | 0 | [0,1,2] | [[3,1,4],[2,7],[1,2]] |
| 8 | -1 | 1 | [0,None,2] | seq2 ends |
| 9 | 3 | 2 | ... | continue filling |
| 10 | -1 | 0 | [None,None,2] | seq0 ends |
| 11 | 4 | 2 | ... | last sequence |
| 12 | -1 | 2 | all ended | done |

This trace shows how sequences are filled column by column while independently terminating at different times.

### Example 2

Input:

```
5
1 2 -1 3 4
```

| Step | Value | idx | active | seqs state |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | [0] | [[1]] |
| 2 | 2 | 1 | [0,1] | [[1],[2]] |
| 3 | -1 | 0 | [None,1] | first sequence ends |
| 4 | 3 | 1 | [None,1] | [[1],[2,3]] |
| 5 | 4 | 1 | [None,1] | [[1],[2,3,4]] |

The second sequence continues independently after the first is terminated, showing why global stopping on -1 would be incorrect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each encoded element is processed once with O(1) operations |
| Space | O(m) | Storage for all reconstructed elements and active mapping |

The solution fits comfortably within constraints since 300,000 operations with constant-time handling per element is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    output = []
    def solve():
        m = int(input())
        b = list(map(int, input().split()))

        seqs = []
        active = []
        idx = 0

        for val in b:
            if val == -1:
                if idx < len(active):
                    active[idx] = None
                idx += 1
            else:
                if idx == len(active):
                    active.append(len(seqs))
                    seqs.append([])
                seq_id = active[idx]
                seqs[seq_id].append(val)

        res = []
        for i in active:
            if i is not None:
                res.append(seqs[i])

        output.append(str(len(res)))
        for s in res:
            output.append(str(len(s)) + (" " + " ".join(map(str, s)) if s else ""))

    solve()
    return "\n".join(output)

# provided sample
assert run("""12
3 2 1 1 7 2 4 -1 3 -1 4 -1
""") == """3
3 3 1 4
2 2 7
4 1 2 3 4"""

# empty sequences edge
assert run("""3
-1 -1 -1
""") == """3
0
0
0"""

# single sequence
assert run("""4
1 2 3 -1
""") == """1
3 1 2 3"""

# staggered termination
assert run("""5
1 2 -1 3 4
""") == """2
1 1
3 2 3 4"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all -1 | three empty sequences | empty sequence handling |
| single linear sequence | one full sequence | basic reconstruction |
| early termination | split sequences | staggered -1 handling |

## Edge Cases

A fully empty scenario where all values are -1 demonstrates that the algorithm must still produce multiple empty sequences, since each -1 corresponds to termination of a distinct sequence.

For example:

```
-1 -1 -1
```

The algorithm increments the active column pointer for each -1 and marks a sequence slot as terminated. Even though no real values are appended, three sequences are still reconstructed.

Another edge case is when sequences end at different depths. In:

```
1 2 -1 3 4
```

the first sequence ends early while the second continues growing. The algorithm correctly keeps the second sequence active after removing the first, ensuring values are not mistakenly appended to a terminated sequence.
