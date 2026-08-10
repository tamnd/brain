---
title: "CF 102397J - AbuTahun and Flash Memories"
description: "We have n solution files, and every file occupies exactly x GB. A single flash memory can hold at most a GB, and a file must stay entirely inside one memory. The goal is to find the smallest number of flash memories needed to store all n files."
date: "2026-08-10T18:17:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "J"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 279
verified: true
draft: false
---

[CF 102397J - AbuTahun and Flash Memories](https://codeforces.com/problemset/problem/102397/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` solution files, and every file occupies exactly `x` GB. A single flash memory can hold at most `a` GB, and a file must stay entirely inside one memory. The goal is to find the smallest number of flash memories needed to store all `n` files.

The key quantity is not the total storage of one memory alone, but how many complete files fit inside it. Since every file has the same size, one memory can store exactly

`floor(a / x)`

files. Once this number is known, the problem becomes asking how many groups of that size are needed to contain all `n` files.

The constraint `n <= 10^5` means even a linear algorithm would be easily fast enough under a 1.5 second limit. However, the structure of the problem is much simpler than a general packing problem, so we can solve it in constant time. The bounds on `x` and `a` are also small enough for ordinary integer arithmetic, and Python integers have no overflow concern here.

There are several boundary cases that can expose an incorrect implementation. Consider `1 5 5`. One file exactly fills one memory, so the answer is `1`. A careless implementation that uses strict inequality instead of allowing equality could incorrectly reject the file.

Another important case is `5 2 5`. Each memory holds `floor(5 / 2) = 2` files, so three memories are required. The correct output is `3`. Simply dividing the total file size by the memory capacity gives `ceil(10 / 5) = 2`, which is wrong because the unused 1 GB in each memory cannot be combined to store a file.

Finally, when `x = a`, for example `4 7 7`, each memory can hold exactly one file, so the answer is `4`. Any formula that accidentally assumes more than one file can fit because of integer rounding would fail on this boundary.

## Approaches

A completely general brute-force solution could treat the problem as a packing problem and try possible assignments of files to memories. For a fixed number `k` of memories, every one of the `n` files could initially be assigned to any of those `k` memories, giving `k^n` possible assignments. Trying every possible `k` from `1` through `n` produces a total of

`1^n + 2^n + ... + n^n`

assignments. In the worst case `n = 10^5`, this is astronomically large, roughly dominated by `10^(500000)`, so such an approach is completely infeasible.

That brute-force approach is correct because it considers every possible way of distributing the files and can identify whether a valid packing exists. The problem is that it ignores the strongest structural property: every file has exactly the same size.

Because all files are equal, there is no reason to decide where individual files go. We only need to know the maximum number of complete files that fit in one memory. If that number is `k = floor(a / x)`, then every memory can accommodate at most `k` files, and we can always achieve exactly `k` files in a memory whenever enough files remain. Thus `n` files require the ceiling of `n / k` memories.

The ceiling division can be computed with integer arithmetic as `(n + k - 1) // k`. Since `x <= a`, we always have `k >= 1`, so the division is valid.

The brute-force works because it explicitly searches for a valid packing, but fails when the number of possible assignments becomes enormous. The observation that all files have identical size lets us discard the identities of the files entirely and reduce the problem to one integer division.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^n) or worse when all memory counts are considered | O(n) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `x`, and `a`. Here `n` is the number of files, `x` is the size of every file, and `a` is the capacity of one flash memory.
2. Compute `files_per_memory = a // x`. This is the largest integer number of complete files that can fit into one memory. Any fractional remainder of the capacity is unusable because files cannot be split.
3. Compute the number of memories using ceiling division: `answer = (n + files_per_memory - 1) // files_per_memory`. This rounds `n / files_per_memory` upward, because the final memory may contain fewer files than the others.
4. Print `answer`.

### Why it works

Let `k = floor(a / x)`. A memory cannot contain more than `k` files, because `k + 1` files would require `(k + 1) * x > a` GB. At the same time, any group of at most `k` files fits because `k * x <= a`. Thus the files can always be divided into groups of at most `k` files, and the minimum number of such groups is exactly `ceil(n / k)`. The algorithm computes precisely those two quantities, so it produces the minimum possible number of memories.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, x, a = map(int, input().split())

files_per_memory = a // x
answer = (n + files_per_memory - 1) // files_per_memory

print(answer)
```

The first line reads all three input values. There is only one test case, so no loop over test cases is needed.

The expression `a // x` uses floor division, which is essential. For example, if a memory has capacity `7` GB and each file uses `2` GB, `7 // 2` is `3`, meaning only three complete files fit. The remaining 1 GB cannot be used for a fourth file.

The final expression performs ceiling division without using floating-point arithmetic. Using `(n + files_per_memory - 1) // files_per_memory` avoids precision issues and handles exact divisibility correctly. For example, `10` files with `3` files per memory gives `(10 + 3 - 1) // 3 = 4`, while `9` files gives `(9 + 3 - 1) // 3 = 3`.

There is no integer overflow issue in Python, and the largest intermediate value here is tiny compared with Python's integer capacity.

## Worked Examples

For the first sample, the input is `10 2 7`.

| `n` | `x` | `a` | `a // x` | Answer |
| --- | --- | --- | --- | --- |
| 10 | 2 | 7 | 3 | 4 |

Each memory holds at most three files because `3 * 2 = 6` GB fits while `4 * 2 = 8` GB does not. Ten files form three complete groups of three and one remaining file, so four memories are necessary. This demonstrates why the unused capacity of a memory cannot be combined with another memory.

For the second sample, the input is `3 5 15`.

| `n` | `x` | `a` | `a // x` | Answer |
| --- | --- | --- | --- | --- |
| 3 | 5 | 15 | 3 | 1 |

One memory can hold exactly three files because `3 * 5 = 15` GB. All three files therefore fit into a single memory. This confirms that equality with the capacity is allowed and that the ceiling division correctly returns `1` when the number of files is exactly divisible by the per-memory capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed. |
| Space | O(1) | Only a few integer variables are stored. |

With `n` as large as `10^5`, constant time is comfortably within the 1.5 second limit. The algorithm also uses constant memory, far below the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n, x, a = map(int, input().split())

    files_per_memory = a // x
    answer = (n + files_per_memory - 1) // files_per_memory

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    output = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output

# Provided samples
assert run("10 2 7\n") == "4", "sample 1"
assert run("3 5 15\n") == "1", "sample 2"

# Minimum-size input
assert run("1 1 1\n") == "1", "minimum values"

# Every file exactly fills one memory
assert run("100000 100000 100000\n") == "100000", "x equals a"

# Exact divisibility
assert run("12 3 10\n") == "4", "exact number of groups"

# Remainder after full groups
assert run("10 2 5\n") == "4", "off-by-one remainder case"

# Maximum n with one file per memory
assert run("100000 99999 99999\n") == "100000", "maximum n boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Minimum-size input |
| `100000 100000 100000` | `100000` | Maximum `n` and `x = a` |
| `12 3 10` | `4` | Exact divisibility into groups of four |
| `10 2 5` | `4` | Capacity remainder and ceiling division |
| `100000 99999 99999` | `100000` | Large boundary with one file per memory |

## Edge Cases

When a file exactly matches the memory capacity, the algorithm correctly allows it. For input `1 5 5`, `a // x` is `5 // 5 = 1`, so `(1 + 1 - 1) // 1 = 1`. The output is `1`. This catches implementations that accidentally use `<` instead of `<=` when reasoning about capacity.

When the memory has unused space that is too small for another file, that space cannot help any other memory. For input `5 2 5`, each memory holds `5 // 2 = 2` files. The calculation becomes `(5 + 2 - 1) // 2 = 3`, so the output is `3`. Two memories provide room for four files, and the fifth file requires a third memory.

When `x = a`, only one file fits in each memory. For input `4 7 7`, `a // x = 1`, so the answer is `(4 + 1 - 1) // 1 = 4`. Every file needs its own memory, which is exactly what the algorithm reports.

When all files fit into one memory, the ceiling division naturally returns one. For input `3 5 15`, the per-memory capacity is `15 // 5 = 3`, giving `(3 + 3 - 1) // 3 = 1`. No special case is required for this situation, which is a useful property of the formula.
