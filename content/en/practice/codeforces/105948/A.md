---
title: "CF 105948A - Executable Log"
description: "We are given a list of files, where each file has a name and a permission string. The permission string encodes whether the file can be read, written, or executed using the familiar three-character format."
date: "2026-06-22T16:05:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105948
codeforces_index: "A"
codeforces_contest_name: "CCF CAT NAEC 2025 (Provincial)"
rating: 0
weight: 105948
solve_time_s: 51
verified: true
draft: false
---

[CF 105948A - Executable Log](https://codeforces.com/problemset/problem/105948/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of files, where each file has a name and a permission string. The permission string encodes whether the file can be read, written, or executed using the familiar three-character format. Our task is to count how many of these files satisfy two conditions at the same time: the filename corresponds to a log file, and the permission string grants execute access.

A file is considered a log file if its name matches the pattern “S.log”, meaning it ends exactly with “.log” and the part before it can be any string, including the empty string. This immediately includes names like “.log”, “a.log”, and “123.log”, but excludes anything where “.log” is not the final suffix, such as “a.log.zip” or “logfile”.

The permission string is always one of eight fixed possibilities built from the characters r, w, x, and -. We only care whether the third character is ‘x’, since that indicates execute permission.

The input size is small, with at most 1000 files and filename length at most 100. This means a direct scan over all files is already efficient enough, and we do not need any advanced data structures or preprocessing. Any solution that checks each file in linear time will comfortably run within limits.

The main edge cases come from correctly identifying the “.log” suffix rather than checking whether the substring “.log” appears anywhere in the filename. For example, “a.log.zip” contains “.log” but is not a log file.

Another subtle case is the empty prefix. The filename “.log” is valid and should be counted if it has execute permission. A naive implementation that assumes at least one character before “.log” could incorrectly reject it.

## Approaches

A brute-force approach is already essentially optimal for this problem. For each file, we check whether its name ends with “.log” and whether its permission string has an ‘x’ in the third position. Each check is O(1) given the constraints, since string length is bounded and permission format is fixed. Over n files, this yields O(n) total work.

One might imagine more complex parsing, such as scanning substrings or attempting to validate patterns in a generalized way. However, nothing about the problem requires preprocessing or searching across files. The structure is flat: each file is independent, and the condition is local to the string itself.

The key observation is that suffix checking and fixed-position permission checking both reduce to constant-time operations per file. That collapses the problem into a simple filter over the input list.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. Read the number of files n, then iterate over each file entry one by one. We do this because each file is independent and no global structure is needed.
2. For each file, extract the filename f and permission string p. The decision for this file depends only on these two strings.
3. Check whether f ends with the substring “.log”. This ensures we only consider valid log files and avoids false matches where “.log” appears in the middle or earlier in the filename.
4. Check whether the permission string p has ‘x’ as its third character. Since p is always length 3 and uses fixed format, this directly tells us whether execute permission is granted.
5. If both conditions are true, increment a counter. This counter tracks how many files satisfy the combined condition.
6. After processing all files, output the counter as the final answer.

### Why it works

The algorithm relies on the fact that both constraints are independent and locally checkable. The log-file condition is entirely determined by a suffix comparison, and the execute permission is determined by a fixed-position character in a constant-format string. Since every file is evaluated independently and no transformation depends on previous results, counting valid files after per-item filtering guarantees correctness. There is no overlap case where partial matching could cause ambiguity, because the suffix rule and permission encoding are both exact and unambiguous.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    ans = 0

    for _ in range(n):
        f, p = input().split()

        if len(f) >= 4 and f[-4:] == ".log":
            if p[2] == "x":
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the algorithm. The suffix check uses slicing f[-4:] which is safe even when the string is exactly “.log” because length 4 is the minimum valid case. The permission check uses direct indexing p[2], which is safe because all permission strings are guaranteed to have length 3.

The counter accumulates matches without storing any extra state, ensuring constant memory usage.

## Worked Examples

Consider the sample input:

```
.log rwx
a.log.zip r-x
proj.logger.cpp r-x
main rwx
b.log rw-
```

We process each file step by step.

| File | Name ends with ".log" | p[2] == 'x' | Count |
| --- | --- | --- | --- |
| .log | Yes | Yes | 1 |
| a.log.zip | No | Yes | 1 |
| proj.logger.cpp | No | Yes | 1 |
| main | No | Yes | 1 |
| b.log | Yes | No | 1 |

The final answer is 1, since only “.log rwx” satisfies both conditions simultaneously.

Now consider a second example:

```
a.log r-x
log.log rwx
.log r--
x.log rwx
```

| File | Ends with ".log" | p[2] == 'x' | Count |
| --- | --- | --- | --- |
| a.log | Yes | Yes | 1 |
| log.log | Yes | Yes | 2 |
| .log | Yes | No | 2 |
| x.log | Yes | Yes | 3 |

The output is 3, showing that multiple valid log files can be counted independently.

These traces confirm that each file is treated in isolation and only exact suffix and permission checks matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each file is processed once with constant-time string checks |
| Space | O(1) | Only a single counter is maintained regardless of input size |

Given n ≤ 1000, this is trivially fast and runs well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n = int(input().strip())
    ans = 0
    for _ in range(n):
        f, p = input().split()
        if len(f) >= 4 and f[-4:] == ".log" and p[2] == "x":
            ans += 1
    print(ans)

# provided sample
assert run(".log rwx\na.log.zip r-x\nproj.logger.cpp r-x\nmain rwx\nb.log rw-\n") == "1"

# minimum size, single valid
assert run("1\n.log rwx\n") == "1"

# minimum size, invalid permission
assert run("1\n.log r--\n") == "0"

# boundary: tricky suffix false positive
assert run("2\na.log.zip rwx\na.log rwx\n") == "1"

# all valid
assert run("3\n.log rwx\na.log rwx\nx.log rwx\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single valid log | 1 | basic positive case |
| invalid permission | 0 | permission filter correctness |
| mixed suffixes | 1 | avoids false “.log” substring matches |
| all valid files | 3 | aggregation correctness |

## Edge Cases

One edge case is the filename being exactly “.log”. The algorithm checks suffix using f[-4:] == ".log", so for f = ".log", the slice is valid and matches correctly. If p = "rwx", the file is counted. This confirms that empty prefix handling is naturally supported.

Another edge case is filenames containing “.log” internally, such as “a.log.zip”. Here f[-4:] equals “.zip”, not “.log”, so the file is correctly excluded even though the substring appears earlier.

A third edge case is a log file without execute permission, such as “x.log rw-”. Even though the suffix condition passes, p[2] is ‘-’, so it is not counted. This confirms that both conditions must hold simultaneously, and neither dominates the other.
