---
title: "CF 250A - Paper Work"
description: "Polycarpus needs to organize daily profit reports into folders, where each folder contains consecutive days. The key restriction is that a folder cannot contain three or more days with negative profit, because the boss cannot tolerate more than two loss days per folder."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 250
codeforces_index: "A"
codeforces_contest_name: "CROC-MBTU 2012, Final Round (Online version, Div. 2)"
rating: 1000
weight: 250
solve_time_s: 189
verified: false
draft: false
---

[CF 250A - Paper Work](https://codeforces.com/problemset/problem/250/A)

**Rating:** 1000  
**Tags:** greedy  
**Solve time:** 3m 9s  
**Verified:** no  

## Solution
## Problem Understanding

Polycarpus needs to organize daily profit reports into folders, where each folder contains consecutive days. The key restriction is that a folder cannot contain three or more days with negative profit, because the boss cannot tolerate more than two loss days per folder. The goal is to minimize the total number of folders and output both the number of folders and the size of each folder in sequence.

The input is an integer `n` representing the number of days, followed by a sequence of integers representing profits for each day. The output is an integer representing the minimum number of folders and a sequence showing the number of days in each folder.

With `n` up to 100, we know the algorithm can afford nested loops of moderate size, as O(n²) is still feasible. However, we should aim for a linear O(n) approach, because we only need to scan the array sequentially and maintain a simple count of negative days.

A subtle edge case arises when negative days appear consecutively. For example, in the sequence `[1, -1, -2, -3, 4]`, we cannot include all three negative days in a single folder. A naive greedy that only looks at cumulative folder size without tracking negative counts might mistakenly place all three together, producing an invalid folder. Another edge case is sequences with fewer than three negative days; they can all fit into a single folder regardless of their position.

## Approaches

The brute-force method would generate all possible partitions of the array into consecutive segments and test each partition for validity. Each segment is valid if it contains at most two negative days. With `n` up to 100, the number of partitions grows exponentially, making this infeasible.

The key insight is that we do not need to consider complicated partitioning. The only constraint is that a folder cannot have three negative days. We can scan the array from left to right, keeping track of how many negative days are in the current folder. Whenever adding the next day would result in three negatives, we start a new folder. This greedy approach works because the constraint depends solely on the count of negative days, not on absolute positions or sums. By grouping as many consecutive days as possible while keeping negative counts below three, we ensure the minimal number of folders.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy scan by negative count | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list `folders` to store the sizes of each folder. Set `current_folder_size` and `neg_count` to zero.
2. Iterate through each day's profit `a[i]` from the first to the last.
3. Increment `current_folder_size` by 1 to account for the current day.
4. If `a[i]` is negative, increment `neg_count`.
5. After including the day, check if `neg_count` reached 3. If it has, the current folder cannot include this day. We finalize the previous folder with size `current_folder_size - 1` and start a new folder with the current day. Reset `neg_count` to 1 if the current day is negative, otherwise 0, and set `current_folder_size` to 1.
6. After the loop, append the size of the last folder to `folders`.
7. Print the number of folders and the folder sizes in order.

The algorithm works because we maintain an invariant that no folder ever contains more than two negative days. By starting a new folder exactly when the negative count reaches three, we guarantee both validity and minimality: no folder could have been extended without violating the constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

folders = []
current_folder_size = 0
neg_count = 0

for x in a:
    if x < 0:
        neg_count += 1
    current_folder_size += 1
    if neg_count == 3:
        folders.append(current_folder_size - 1)
        current_folder_size = 1
        neg_count = 1 if x < 0 else 0

folders.append(current_folder_size)

print(len(folders))
print(' '.join(map(str, folders)))
```

We iterate through each day, updating the folder size and negative count. When the negative count hits three, we close the folder before the current day, start a new one, and reset counters appropriately. At the end, we append the final folder. Off-by-one errors are avoided by adjusting the folder size before resetting.

## Worked Examples

Sample Input 1:

```
11
1 2 3 -4 -5 -6 5 -5 -6 -7 6
```

| Day | Profit | neg_count | current_folder_size | Action | folders |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | continue | [] |
| 2 | 2 | 0 | 2 | continue | [] |
| 3 | 3 | 0 | 3 | continue | [] |
| 4 | -4 | 1 | 4 | continue | [] |
| 5 | -5 | 2 | 5 | continue | [] |
| 6 | -6 | 3 | 6 | neg_count=3 → split | [5] |
| 6 | -6 | 1 | 1 | start new | [5] |
| 7 | 5 | 1 | 2 | continue | [5] |
| 8 | -5 | 2 | 3 | continue | [5] |
| 9 | -6 | 3 | 4 | split | [5,3] |
| 9 | -6 | 1 | 1 | start new | [5,3] |
| 10 | -7 | 2 | 2 | continue | [5,3] |
| 11 | 6 | 2 | 3 | end | [5,3,3] |

The table confirms that negative counts never exceed 2 in any folder, and all days are included.

Sample Input 2:

```
5
1 2 3 4 5
```

All profits are positive, so the folder never splits. Output is `[5]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each day is processed exactly once, constant operations per day |
| Space | O(n) | The `folders` list stores at most n entries in the worst case |

With n ≤ 100, this algorithm executes trivially within 2 seconds, and memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    folders = []
    current_folder_size = 0
    neg_count = 0
    for x in a:
        if x < 0:
            neg_count += 1
        current_folder_size += 1
        if neg_count == 3:
            folders.append(current_folder_size - 1)
            current_folder_size = 1
            neg_count = 1 if x < 0 else 0
    folders.append(current_folder_size)
    return f"{len(folders)}\n{' '.join(map(str, folders))}"

# Provided samples
assert run("11\n1 2 3 -4 -5 -6 5 -5 -6 -7 6\n") == "3\n5 3 3", "sample 1"
assert run("5\n1 2 3 4 5\n") == "1\n5", "sample 2"

# Custom cases
assert run("3\n-1 -2 -3\n") == "2\n2 1", "all negatives split"
assert run("1\n0\n") == "1\n1", "single day, zero"
assert run("6\n-1 2 -3 4 -5 6\n") == "3\n3 2 1", "interleaved negatives"
assert run("100\n" + " ".join(["1"]*100) + "\n") == "1\n100", "all positives max size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 negatives | 2 folders | splitting when negatives exceed 2 |
| 1 day zero | 1 folder | minimal size input |
| interleaved negatives | 3 folders | correct splitting with gaps |
| all positives length 100 | 1 folder | maximum size, no splits |

## Edge Cases

For `[ -1, -2, -3 ]`, the algorithm tracks negative count. After the second day, `neg_count = 2`, next day brings `neg_count = 3`, triggering a split. Folder sizes `[2,1]` satisfy the constraint.

For `[1, 2, 3, 4, 5]`, all positive, `neg_count` never reaches 3, so only one folder of size 5 is created.

For a single day `[0]`, `current_folder_size = 1`, `neg_count = 0`, and the final append gives `[1]`, correctly handling the minimal input.

The algorithm systematically manages negative counts and folder splits, covering all possible edge cases without special-case code.
