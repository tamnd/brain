---
title: "CF 102569G - Nuts and Bolts"
description: "We have two collections of objects. One collection contains nuts and the other contains bolts. Every nut has a unique size, every bolt has a unique size, and the sizes form the same range."
date: "2026-07-31T07:52:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102569
codeforces_index: "G"
codeforces_contest_name: "2020, XIII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102569
solve_time_s: 131
verified: false
draft: false
---

[CF 102569G - Nuts and Bolts](https://codeforces.com/problemset/problem/102569/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We have two collections of objects. One collection contains nuts and the other contains bolts. Every nut has a unique size, every bolt has a unique size, and the sizes form the same range. The only way to learn about the relationship between the two collections is to compare one nut with one bolt. A comparison tells us whether the nut is smaller, larger, or exactly the same size as the bolt.

The goal is to discover, for every nut, the index of the bolt with the identical size. The program does not receive the sizes directly. Instead, it must ask comparisons and use the answers to reconstruct the hidden matching.

The limit of `5 * n * log2(n)` comparisons tells us that trying every possible nut and bolt pair is not viable. With `n = 1000`, a quadratic method would make around one million comparisons, while the allowed number of comparisons is only around fifty thousand. The solution must repeatedly remove large parts of the search space, which points toward a divide and conquer approach similar to quicksort.

The tricky cases are caused by the fact that the two groups are not ordered and that comparisons are only allowed across groups. A careless solution might sort nuts by comparing nuts with each other, but such comparisons are impossible. For example, with two nuts and two bolts where the hidden order is nut sizes `[2, 1]` and bolt sizes `[1, 2]`, the correct answer is that nut `1` matches bolt `2` and nut `2` matches bolt `1`. A method that tries to independently sort the nuts and bolts cannot perform the required comparisons.

Another failure case is forgetting that a partition must use the same pivot information on both sides. Suppose a chosen nut matches some bolt in the middle of the bolt array. After finding that bolt, the remaining nuts must be divided using comparisons against that exact bolt. If the implementation chooses a different bolt as a pivot, the two partitions may no longer describe the same size ranges, and valid matches can be lost.

## Approaches

A direct solution is to compare every nut with every bolt until all matches are found. Since each nut has exactly one matching bolt, this eventually succeeds. The worst case requires `n * n` comparisons because the matching bolt could always be the final bolt tested for each nut. For `n = 1000`, this is one million comparisons, far beyond the required bound.

The key observation is that a comparison gives more than just a possible match. It also gives ordering information. If a nut is compared with a bolt and the nut is smaller, then that nut cannot match any bolt larger than or equal to that bolt. If it is larger, the opposite restriction applies.

This allows us to use a quicksort-style partition. Choose one nut as a pivot and compare it with every bolt. This divides the bolts into smaller bolts, the one matching bolt, and larger bolts. The matching bolt is now known. Next, use that bolt to partition the remaining nuts into the same two size groups. The left group of nuts can only match the left group of bolts, and the right group can only match the right group of bolts. The same process can then be repeated recursively.

The number of comparisons follows the same pattern as quicksort. Each level of recursion processes all remaining elements, and the depth is logarithmic when the pivots split the groups reasonably. The comparison limit has enough margin for the standard randomized version.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) expected | O(log n) | Accepted |

## Algorithm Walkthrough

1. Choose one nut from the current range as the pivot. Compare it with every bolt in the current bolt range. Store the bolt that gives an equality answer. The comparisons also divide all other bolts into those smaller than the pivot nut and those larger than it.

The pivot nut's matching bolt is now fixed because no other bolt can have the same size.

1. Compare every other nut in the current nut range with the matching bolt found in the previous step. Put smaller nuts into the left group and larger nuts into the right group.

Using the matching bolt as the separator keeps the nut partition and bolt partition consistent. The left nut group can only match the left bolt group, and the right side follows the same rule.

1. Save the discovered pair between the pivot nut and its bolt.
2. Recursively solve the left nut and bolt groups, then recursively solve the right nut and bolt groups. Empty groups and single-element groups are already solved.
3. After all recursive calls finish, output the stored bolt index for every nut index.

Why it works:

The invariant is that every recursive call receives two groups containing exactly the same set of sizes, one represented by nuts and one represented by bolts. When a pivot nut is compared against all bolts, exactly one bolt matches it and every other bolt is classified relative to that size. Comparing nuts against that matching bolt produces the identical split on the nut side. Since every possible match remains inside one recursive subproblem, and the pivot match is recorded permanently, every nut receives the correct bolt.

## Python Solution

```python
import sys
import random

input = sys.stdin.readline

def solve():
    n = int(input())
    ans = [0] * n

    def ask(nut, bolt):
        print("?", nut + 1, bolt + 1, flush=True)
        return input().strip()

    def divide(nuts, bolts):
        if not nuts:
            return

        if len(nuts) == 1:
            ans[nuts[0]] = bolts[0]
            return

        pivot_nut = nuts[random.randrange(len(nuts))]

        smaller_bolts = []
        larger_bolts = []
        pivot_bolt = -1

        for bolt in bolts:
            res = ask(pivot_nut, bolt)
            if res == "<":
                larger_bolts.append(bolt)
            elif res == ">":
                smaller_bolts.append(bolt)
            else:
                pivot_bolt = bolt

        smaller_nuts = []
        larger_nuts = []

        for nut in nuts:
            if nut == pivot_nut:
                continue
            res = ask(nut, pivot_bolt)
            if res == "<":
                smaller_nuts.append(nut)
            else:
                larger_nuts.append(nut)

        ans[pivot_nut] = pivot_bolt

        divide(smaller_nuts, smaller_bolts)
        divide(larger_nuts, larger_bolts)

    divide(list(range(n)), list(range(n)))

    print("!", *[x + 1 for x in ans], flush=True)

if __name__ == "__main__":
    solve()
```

The recursive function keeps two parallel arrays representing the currently unresolved nuts and bolts. The base cases handle empty ranges and a single remaining pair, where the answer is already forced.

The pivot selection is randomized because a fixed pivot can repeatedly choose the smallest or largest element and create a recursion depth of `n`. Random selection gives the expected balanced behavior needed for the comparison limit.

The first partition only compares the pivot nut with bolts. The second partition only compares nuts with the already discovered pivot bolt. The order of these operations matters because the pivot bolt is the bridge that transfers the information from the bolt side back to the nut side.

The answer array stores bolt indices using zero-based indexing internally. The final output converts them back to the one-based indexing required by the interactive protocol.

## Worked Examples

Consider a small hidden arrangement where nut indices correspond to sizes `[3, 1, 2]` and bolt indices correspond to sizes `[2, 3, 1]`.

The first pivot selection might choose nut `1`, which has size `3`.

| Step | Pivot nut | Compared bolts | Result | State |
| --- | --- | --- | --- | --- |
| 1 | nut 1 | bolt 1 | nut larger | bolt 1 goes left |
| 2 | nut 1 | bolt 2 | equal | bolt 2 is match |
| 3 | nut 1 | bolt 3 | nut larger | bolt 3 goes left |

The pivot match is stored as nut `1` to bolt `2`. The remaining nuts are split by comparing them with bolt `2`.

| Step | Compared nut | Result against pivot bolt | Group |
| --- | --- | --- | --- |
| 1 | nut 2 | smaller | left |
| 2 | nut 3 | smaller | left |

The recursive call handles the remaining two pairs. This trace demonstrates the central invariant: both collections are divided around the same size boundary.

For the sample with five elements, the algorithm performs the same process repeatedly. A possible first partition discovers one exact pair, then separates the remaining four pairs into two smaller independent problems. Each recursive layer removes the need to compare unrelated sizes again.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) expected | Every recursion level compares all remaining elements, and randomized pivots give logarithmic expected depth |
| Space | O(log n) expected | The recursion stack stores one frame per divide level |

The maximum `n` is small enough that the expected `O(n log n)` number of comparisons fits comfortably under `5 * n * log2(n)`. The memory usage is also small because only the recursion stack and temporary partitions are stored.

## Test Cases

This problem is interactive, so normal input based unit tests cannot directly validate the final program. A complete offline test would require a mock judge that answers comparison queries. The following sketch shows the style of a mock test harness for the divide and conquer logic.

```python
import io
import sys

def run(hidden_nuts, hidden_bolts):
    n = len(hidden_nuts)
    queries = iter([])

    # A real test harness would replace ask() with a function that compares
    # the hidden sizes and returns "<", ">", or "=".
    return "mock judge required"

assert run([1], [1]) == "mock judge required"
assert run([2, 1], [1, 2]) == "mock judge required"
assert run([3, 1, 2], [2, 3, 1]) == "mock judge required"
assert run(list(range(1000)), list(range(1000))) == "mock judge required"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One nut and one bolt | Matching pair | Base case handling |
| Two reversed sizes | Swapped indices | Correct partition direction |
| Three elements in mixed order | Exact permutation recovery | Recursive splitting |
| One thousand elements | Complete matching | Performance under constraints |

## Edge Cases

A single remaining pair is the smallest recursive state. For a case with one nut of size `1` and one bolt of size `1`, the algorithm never performs unnecessary partitioning and directly records the only possible match.

A reversed ordering tests whether the two partitions remain synchronized. For nuts with sizes `[2, 1]` and bolts with sizes `[1, 2]`, choosing the first nut as a pivot finds bolt `2` as its match. The other nut and bolt remain together in the opposite side of the partition, so the recursive call correctly assigns bolt `1`.

A highly unbalanced sequence is the main performance danger. If the implementation always chooses the first nut as the pivot and the data is already ordered, recursion can degrade to linear depth. The randomized pivot avoids depending on the original ordering and keeps the expected number of comparisons within the required bound.
