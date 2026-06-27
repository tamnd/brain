---
title: "CF 104974E - Intern Florist"
description: "We are simulating a very small file system that supports three operations applied sequentially. Each operation either creates a named file, deletes a named file, or asks how many files currently exist."
date: "2026-06-28T06:10:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104974
codeforces_index: "E"
codeforces_contest_name: "Codentines Day"
rating: 0
weight: 104974
solve_time_s: 49
verified: true
draft: false
---

[CF 104974E - Intern Florist](https://codeforces.com/problemset/problem/104974/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a very small file system that supports three operations applied sequentially. Each operation either creates a named file, deletes a named file, or asks how many files currently exist. A file is uniquely identified by its name, and names behave like exact strings, so `"abc"` and `"ABC"` are different and spaces are part of the name.

The state starts empty. When a `touch name` command appears, we try to insert that name into the current set of files. If it already exists, nothing changes. When an `rm name` command appears, we remove that name if it is present; if it is absent, we again do nothing. When an `ask` command appears, we output the current number of files stored.

The key difficulty is scale. The number of commands can be up to one million, and file names are arbitrary strings whose total length can reach two million characters. This immediately rules out any solution that scans all stored names for every query, because even a linear scan per `ask` would degenerate into quadratic behavior in the worst case.

A naive implementation would maintain a list of strings and, on `ask`, recompute how many distinct strings exist by scanning the entire list and checking membership manually. This breaks down when there are many operations and many stored files.

A more subtle failure mode comes from mishandling duplicates. For example, if we treat `touch` as “append to a list” without checking existence, repeated touches of the same name would inflate the count incorrectly. Similarly, if we simply decrement a counter on every `rm`, we can go negative if deletions target non-existent files.

## Approaches

The brute-force idea is straightforward: maintain a list of all file names currently alive. For `touch`, we check whether the name is already in the list; if not, we append it. For `rm`, we search the list, and if found we remove it. For `ask`, we compute the size of the list.

The correctness is immediate because the list mirrors the active set exactly. The issue is performance. Both `touch` existence checks and `rm` lookups require scanning up to O(n) strings, and removals may also require shifting elements. With up to 10^6 operations, this leads to roughly O(n^2) behavior in the worst case, which is far beyond limits.

The key observation is that we only ever need membership and cardinality, not ordering or structure. That is exactly what a hash-based set is designed for. If we store file names in a Python `set`, all three operations become average O(1): insertion, deletion, and membership checking are constant time on average, and the size of the set gives us the answer for `ask` directly.

We also avoid recomputation entirely. The set always represents the current state, so counting is just reading a stored integer internally maintained by the structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force List Scan | O(N²) | O(N) | Too slow |
| Hash Set | O(N) total | O(N) | Accepted |

## Algorithm Walkthrough

We process commands one by one while maintaining a set of active file names.

1. Initialize an empty set `files`. This represents all currently existing filenames at any point in time.
2. Read each command line and split it into parts. The first token determines the operation type.
3. If the command is `touch name`, insert `name` into the set. If it already exists, the set remains unchanged, which matches the requirement that duplicates are ignored.
4. If the command is `rm name`, remove `name` from the set if present. If it is not present, do nothing. This can be safely implemented using `discard` so no error is raised.
5. If the command is `ask`, output the current size of the set.

The logic works because every file name is represented at most once in the set, and every valid state transition is captured by either adding or removing that element.

### Why it works

At every step, the set `files` contains exactly the names that have been inserted by `touch` but not removed by `rm`. This is preserved inductively: `touch` adds a missing element without duplication, `rm` removes only existing elements without affecting others, and `ask` does not modify state. Therefore, the size of the set is always equal to the number of active files at that moment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    files = set()
    out = []

    for _ in range(n):
        parts = input().strip().split()
        if parts[0] == "touch":
            files.add(parts[1])
        elif parts[0] == "rm":
            files.discard(parts[1])
        else:
            out.append(str(len(files)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution relies on Python’s built-in hash set to store filenames. The use of `discard` instead of `remove` is intentional, since it avoids exceptions when deleting a non-existent file, matching the problem statement’s “do nothing” behavior.

We accumulate answers in a list rather than printing immediately to reduce I/O overhead, which becomes significant at the upper limit of queries.

## Worked Examples

Consider the sample input:

```
7
touch love_is_in_the_air
ask
touch Valentine
rm love_is_in_the_air
ask
rm Danny_is_cool
ask
```

We track the set step by step.

| Step | Command | Set State | Output |
| --- | --- | --- | --- |
| 1 | touch love_is_in_the_air | {love_is_in_the_air} |  |
| 2 | ask | {love_is_in_the_air} | 1 |
| 3 | touch Valentine | {love_is_in_the_air, Valentine} |  |
| 4 | rm love_is_in_the_air | {Valentine} |  |
| 5 | ask | {Valentine} | 1 |
| 6 | rm Danny_is_cool | {Valentine} |  |
| 7 | ask | {Valentine} | 1 |

This trace shows that duplicate-safe insertion and no-op deletion are both handled correctly, and that `ask` simply reads the current state without recomputation.

Now consider a second scenario with repeated operations:

```
6
touch a
touch a
touch b
rm c
ask
rm a
ask
```

| Step | Command | Set State | Output |
| --- | --- | --- | --- |
| 1 | touch a | {a} |  |
| 2 | touch a | {a} |  |
| 3 | touch b | {a, b} |  |
| 4 | rm c | {a, b} |  |
| 5 | ask | {a, b} | 2 |
| 6 | rm a | {b} |  |
| 7 | ask | {b} | 1 |

This confirms that repeated `touch` does not inflate counts and deleting non-existent names is safely ignored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) average | Each operation is a hash set update or lookup, which is amortized constant time |
| Space | O(M) | M is the number of distinct file names stored simultaneously |

The constraints allow up to one million operations, so linear-time processing with constant-time updates is comfortably within limits. The memory usage is bounded by the number of active filenames, which is at most the number of distinct `touch` operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = int(sys.stdin.readline())
    files = set()
    out = []

    for _ in range(n):
        parts = sys.stdin.readline().strip().split()
        if parts[0] == "touch":
            files.add(parts[1])
        elif parts[0] == "rm":
            files.discard(parts[1])
        else:
            out.append(str(len(files)))

    return "\n".join(out)

# provided sample
assert run("""7
touch love_is_in_the_air
ask
touch Valentine
rm love_is_in_the_air
ask
rm Danny_is_cool
ask
""") == "1\n1\n1"

# empty-ish behavior
assert run("""3
ask
touch a
ask
""") == "0\n1"

# duplicate touches
assert run("""5
touch x
touch x
ask
rm x
ask
""") == "1\n0"

# remove non-existent
assert run("""4
rm a
touch b
ask
ask
""") == "1\n1"

# larger mixed
assert run("""8
touch a
touch b
touch c
rm b
ask
rm a
ask
rm c
ask
""") == "2\n1\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 1 1 1 | basic correctness |
| empty-ish | 0 1 | initial state handling |
| duplicate touches | 1 0 | idempotent insertion |
| remove non-existent | 1 1 | safe deletion |
| larger mixed | 2 1 0 | sequential consistency |

## Edge Cases

One edge case is repeated `touch` of the same filename. Since a set ignores duplicates, the state remains stable. For example:

Input:

```
touch a
touch a
ask
```

The set becomes `{a}` after both operations, so output is `1`. A list-based implementation would incorrectly store two copies unless explicitly checked.

Another edge case is removing a file that was never created. Using `discard` ensures no exception and no state change:

Input:

```
rm missing
ask
```

The set stays empty and output is `0`. A naive `remove` call would crash, while a manual counter approach might go negative.

A final edge case is large-scale churn where files are constantly added and removed. Because each operation is O(1) amortized, the algorithm maintains linear performance even when the state oscillates heavily.
