---
title: "CF 102297A - Find the Twins"
description: "Each test case describes the jersey numbers of exactly 10 soccer players. Mack always wears number 18, while Zack always wears number 17. For every set of 10 numbers, we must determine whether the set contains Mack, Zack, both, or neither."
date: "2026-08-13T08:22:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102297
codeforces_index: "A"
codeforces_contest_name: "UCF Locals 2015"
rating: 0
weight: 102297
solve_time_s: 135
verified: true
draft: false
---

[CF 102297A - Find the Twins](https://codeforces.com/problemset/problem/102297/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes the jersey numbers of exactly 10 soccer players. Mack always wears number 18, while Zack always wears number 17. For every set of 10 numbers, we must determine whether the set contains Mack, Zack, both, or neither.

The output has two parts for every test case. First, we print the ten jersey numbers exactly as they were given. Then we print `mack` if only 18 appears, `zack` if only 17 appears, `both` if both appear, and `none` if neither appears. A blank line separates the result of each test case.

The input contains a positive number `n` followed by `n` sets, each containing exactly 10 distinct integers. Every jersey number is between 11 and 99. The fixed size of each set is the key constraint here. Even if `n` were as large as `10^5`, processing one set requires only a constant amount of work, so an O(n) solution performs roughly a few million simple operations and is easily suitable for a normal contest time limit. There is no need for sorting, hashing, or any more complicated data structure.

There are a few cases where careless logic can give the wrong classification. If the set contains only 17, such as `11 12 13 14 15 16 17 19 20 21`, the answer is `zack`, not `both`, because 18 is absent. If the set contains only 18, such as `11 12 13 14 15 16 18 19 20 21`, the answer is `mack`. If both values occur, such as `11 12 13 14 15 16 17 18 20 21`, the answer is `both`. Finally, if neither occurs, such as `11 12 13 14 15 16 19 20 21 22`, the answer is `none`.

The statement guarantees that the ten numbers are distinct, so an all-equal input is not valid according to the official constraints. A robust implementation can still handle it naturally. For example, `17 17 17 17 17 17 17 17 17 17` would be classified as `zack`, since only the presence of 17 and 18 matters.

## Approaches

The most direct approach is to search the ten numbers for 17 and search them again for 18. The first search answers whether Zack is present, and the second answers whether Mack is present. Since each set contains exactly 10 numbers, the worst case performs 10 comparisons for the search for 17 and another 10 for the search for 18, for at most 20 membership comparisons per test case. With `n` test cases, that is at most `20n` comparisons, which is O(n). It is already fast enough because the set size never grows with `n`.

We can make the scan slightly cleaner by looking at every number only once and maintaining two Boolean flags. Whenever a number is 17, we mark Zack as found. Whenever a number is 18, we mark Mack as found. After all ten numbers have been read, the two flags completely determine the answer.

The key observation is that the actual values of the other eight numbers are irrelevant. We do not need to order the numbers or count anything beyond whether 17 and 18 have appeared. A single pass gives us exactly the two facts needed for the final classification.

Unlike many problems where a brute-force approach becomes too slow as the input grows, there is no meaningful asymptotic gap here because every test case always contains exactly ten numbers. The separate-search version is already accepted. The one-pass version is preferable because it expresses the problem's structure directly and uses at most ten checks per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) auxiliary | Accepted |
| One Pass | O(n) | O(1) auxiliary | Accepted |

Here `n` is the number of test cases. The hidden constant differs between the two approaches, but both are linear because every test case contains exactly 10 values.

## Algorithm Walkthrough

1. Read the number `n` of test cases. We need this value so that exactly the required number of ten-number sets are processed.
2. For each test case, read its ten jersey numbers into a list. Keeping the list lets us print the original set after processing it.
3. Initialize two Boolean variables, `has_mack` and `has_zack`, to `False`. At this point we have inspected no jersey numbers, so neither twin has been found.
4. Scan all ten numbers once. If the current number is 18, set `has_mack` to `True`. If it is 17, set `has_zack` to `True`. Other values require no action because they cannot change the answer.
5. Print the ten numbers in their original order. The problem explicitly requires the input set itself to appear in the output, so sorting or modifying the list would be unnecessary and potentially incorrect.
6. Use the two flags to choose the result. If both are true, print `both`. If only `has_mack` is true, print `mack`. If only `has_zack` is true, print `zack`. If both are false, print `none`.
7. Print a blank line after the result of the test case. This matches the required output format.

### Why it works

After processing any prefix of the ten numbers, `has_mack` is true exactly when 18 has appeared in that prefix, and `has_zack` is true exactly when 17 has appeared. This property is preserved whenever another number is processed because only 17 can change the Zack flag and only 18 can change the Mack flag. After all ten numbers have been examined, the two flags exactly describe which twins are present. The four possible combinations of the flags correspond one-to-one with `none`, `mack`, `zack`, and `both`, so the reported result cannot be wrong.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    for _ in range(n):
        nums = list(map(int, input().split()))

        has_mack = False
        has_zack = False

        for x in nums:
            if x == 18:
                has_mack = True
            elif x == 17:
                has_zack = True

        print(*nums)

        if has_mack and has_zack:
            print("both")
        elif has_mack:
            print("mack")
        elif has_zack:
            print("zack")
        else:
            print("none")

        print()

if __name__ == "__main__":
    solve()
```

The first line of `solve` reads the number of datasets. The loop then handles one complete set at a time, matching the structure of the input.

`nums` stores exactly the ten values needed both for detection and for reproducing the input set in the output. `print(*nums)` prints them space-separated without changing their order.

The two flags start as `False`. During the scan, encountering 18 sets `has_mack`, while encountering 17 sets `has_zack`. The `elif` is safe because a number cannot simultaneously equal 17 and 18. The flags are never reset during the scan, so once a twin has been found, that information is retained.

The final conditional checks the combination of flags from most specific to least specific. Both true must be checked first, otherwise a case containing both twins would be incorrectly classified as only Mack or only Zack. The remaining three cases then follow directly.

There are no indexing boundaries to manage because the code iterates over the values themselves. Integer overflow is impossible because every input number is between 11 and 99. The final `print()` produces the required blank line after every dataset.

The official sample contains four datasets, with the first line `4` specifying their count.

## Worked Examples

### Sample 1

The first dataset is:

`11 99 88 17 19 20 12 13 33 44`

The algorithm starts with both flags false. When it reaches 17, it marks Zack as present. None of the remaining values is 18.

| Position | Jersey number | has_mack | has_zack |
| --- | --- | --- | --- |
| 1 | 11 | False | False |
| 2 | 99 | False | False |
| 3 | 88 | False | False |
| 4 | 17 | False | True |
| 5 | 19 | False | True |
| 6 | 20 | False | True |
| 7 | 12 | False | True |
| 8 | 13 | False | True |
| 9 | 33 | False | True |
| 10 | 44 | False | True |

At the end, `has_mack` is false and `has_zack` is true, so the answer is `zack`.

### Sample 2

The second dataset is:

`11 12 13 14 15 16 66 88 19 20`

Neither 17 nor 18 occurs. Both flags remain false throughout the scan.

| Position | Jersey number | has_mack | has_zack |
| --- | --- | --- | --- |
| 1 | 11 | False | False |
| 2 | 12 | False | False |
| 3 | 13 | False | False |
| 4 | 14 | False | False |
| 5 | 15 | False | False |
| 6 | 16 | False | False |
| 7 | 66 | False | False |
| 8 | 88 | False | False |
| 9 | 19 | False | False |
| 10 | 20 | False | False |

Both flags are false, so the algorithm prints `none`. This trace demonstrates that values close to the target numbers, such as 16, 19, and 20, do not count. The comparison must be exact.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every test case contains exactly 10 numbers, so processing costs O(10) = O(1) per case. |
| Space | O(1) auxiliary | Only two Boolean flags are needed beyond the ten-number input set. |

The actual work per test case is tiny, since the scan always processes exactly ten integers. Even for a very large number of datasets, the total work grows linearly with `n`. The memory used for the algorithm itself does not grow with the number of test cases.

## Test Cases

The following tests use a small wrapper around the same `solve` logic. The all-equal case is outside the official distinct-number constraint, but it is useful as a robustness test. The large case checks that processing many datasets remains linear.

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())

    for _ in range(n):
        nums = list(map(int, input().split()))

        has_mack = False
        has_zack = False

        for x in nums:
            if x == 18:
                has_mack = True
            elif x == 17:
                has_zack = True

        print(*nums)

        if has_mack and has_zack:
            print("both")
        elif has_mack:
            print("mack")
        elif has_zack:
            print("zack")
        else:
            print("none")

        print()

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample_input = """4
11 99 88 17 19 20 12 13 33 44
11 12 13 14 15 16 66 88 19 20
20 18 55 66 77 88 17 33 44 11
12 23 34 45 56 67 78 89 91 18
"""

sample_output = """11 99 88 17 19 20 12 13 33 44
zack

11 12 13 14 15 16 66 88 19 20
none

20 18 55 66 77 88 17 33 44 11
both

12 23 34 45 56 67 78 89 91 18
mack

"""

assert run(sample_input) == sample_output, "official sample"

assert run(
    """1
11 12 13 14 15 16 17 19 20 21
"""
) == """11 12 13 14 15 16 17 19 20 21
zack

""", "zack only"

assert run(
    """1
11 12 13 14 15 16 18 19 20 21
"""
) == """11 12 13 14 15 16 18 19 20 21
mack

""", "mack only"

assert run(
    """1
11 12 13 14 15 16 17 18 20 21
"""
) == """11 12 13 14 15 16 17 18 20 21
both

""", "both twins"

assert run(
    """1
11 12 13 14 15 16 19 20 21 22
"""
) == """11 12 13 14 15 16 19 20 21 22
none

""", "neither twin"

assert run(
    """1
17 17 17 17 17 17 17 17 17 17
"""
) == """17 17 17 17 17 17 17 17 17 17
zack

""", "all equal values"

assert run(
    """1
11 12 13 14 15 16 17 18 98 99
"""
) == """11 12 13 14 15 16 17 18 98 99
both

""", "boundary values and both twins"

large_input = "100000\n" + (
    "11 12 13 14 15 16 19 20 21 99\n" * 100000
)
large_output = (
    "11 12 13 14 15 16 19 20 21 99\nnone\n\n" * 100000
)
assert run(large_input) == large_output, "large number of test cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` followed by a set containing 17 but not 18 | `zack` | Zack-only classification |
| `1` followed by a set containing 18 but not 17 | `mack` | Mack-only classification |
| `1` followed by a set containing both 17 and 18 | `both` | Both flags being true |
| `1` followed by a set containing neither | `none` | Both flags remaining false |
| Ten copies of 17 | `zack` | Robustness even when the distinctness guarantee is violated |
| A set containing 11, 99, 17, and 18 | `both` | Lowest and highest allowed values plus both target values |
| 100000 identical datasets | 100000 corresponding outputs | Linear behavior in the number of test cases |

## Edge Cases

A dataset containing only Zack is `11 12 13 14 15 16 17 19 20 21`. During the scan, `has_zack` becomes true when 17 is encountered, while `has_mack` never changes. The final state is `(False, True)`, which maps to `zack`. A careless implementation that checks only whether one of the target numbers exists and immediately prints `both` would fail here.

A dataset containing only Mack is `11 12 13 14 15 16 18 19 20 21`. The scan changes only `has_mack`, producing `(True, False)`. The correct result is `mack`. This case catches code that accidentally swaps the meanings of 17 and 18, since 17 belongs to Zack and 18 belongs to Mack.

A dataset containing both twins is `11 12 13 14 15 16 17 18 20 21`. The scan first sets `has_zack` when it sees 17 and then sets `has_mack` when it sees 18. The final state is `(True, True)`, so the result is `both`. Checking the combined case before the individual cases prevents the code from incorrectly printing only `mack` or only `zack`.

A dataset containing neither twin is `11 12 13 14 15 16 19 20 21 22`. No comparison succeeds, so both flags remain false and the result is `none`. This is also why nearby values such as 16 and 19 cannot be treated as approximate matches.

The boundary values 11 and 99 do not have any special behavior. For example, `11 12 13 14 15 16 17 18 98 99` contains both target numbers, so it produces `both`. The algorithm compares the values directly and never relies on them being inside a narrower range.

Finally, the ten numbers are guaranteed to be distinct, but even an invalid all-equal dataset does not break the algorithm. With `17 17 17 17 17 17 17 17 17 17`, every comparison against 17 succeeds and the Zack flag becomes true, while the Mack flag stays false. The output is still correctly classified as `zack`.
