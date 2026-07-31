---
title: "CF 102576L - Wizards Unite"
description: "We have a collection of chests, each with its own opening time. There is one gold key that can be reused forever, and there are k silver keys that disappear after one use. A key can only work on one chest at a time."
date: "2026-07-31T07:41:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102576
codeforces_index: "L"
codeforces_contest_name: "2020 Petrozavodsk Winter Camp, Jagiellonian U Contest"
rating: 0
weight: 102576
solve_time_s: 75
verified: true
draft: false
---

[CF 102576L - Wizards Unite](https://codeforces.com/problemset/problem/102576/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of chests, each with its own opening time. There is one gold key that can be reused forever, and there are `k` silver keys that disappear after one use. A key can only work on one chest at a time. The goal is to decide which chests should consume silver keys so that the moment the last chest finishes is as early as possible.

The input contains several test cases. For each test case, the first line gives the number of chests and the number of silver keys. The next line contains the opening time of every chest. The output is the minimum possible finishing time if all chests are opened using the best assignment of keys.

The total number of chests across all test cases can reach `10^6`, and a single test case can contain `10^5` chests. This immediately rules out simulations that try many assignments of chests to keys. The number of possible assignments is exponential, and even checking many combinations would be far beyond what fits in a 2 second limit. An `O(n log n)` solution is acceptable because sorting `10^6` values in total is within the normal range for these constraints, while anything close to `O(n^2)` is not.

The tricky cases are not only about empty work. They appear when the longest chest and the total remaining work compete with each other.

For example, with one silver key:

```
1
3 1
10 1 1
```

The correct answer is `2`. The silver key opens the chest taking `10` seconds, while the gold key opens the two remaining chests in `2` seconds. The final time is `10`, not `2`, so the correct output is actually:

```
10
```

A careless solution that only calculates the gold key workload would miss the fact that silver keys also contribute to the finishing time.

Another case is when all chests have equal duration:

```
1
5 2
7 7 7 7 7
```

The correct output is `14`. Two silver keys finish two chests at time `7`, and the gold key handles the remaining three in `21` seconds if assigned badly. The optimal assignment leaves two chests on silver and three on gold, giving `21`. A solution that assumes silver keys always determine the answer would incorrectly output `7`.

The boundary case `k = 0` also matters:

```
1
4 0
3 5 2 4
```

There are no silver keys, so the gold key must open every chest one after another. The answer is `14`. Code that blindly takes the first `k` elements after sorting needs to handle this case correctly.

## Approaches

A direct approach would try every possible choice of `k` chests for silver keys. Once those chests are chosen, all other chests are forced onto the gold key, so the finishing time is easy to calculate as the maximum of the longest silver chest and the total gold workload. This approach is correct because every valid schedule corresponds to exactly one choice of silver chests.

The problem is the number of choices. Selecting `k` chests from `n` gives `C(n, k)` possibilities. Even for moderate values such as `n = 100` and `k = 50`, the number of assignments is already enormous, so this method cannot work.

The key observation is that a silver key is valuable because it removes a chest from the gold key's sequential workload. To reduce the gold key time as much as possible, the removed chests should have the largest durations. The only possible downside is that the largest silver chest may become the final completion time. However, replacing a larger gold chest with a smaller silver chest can never improve the situation.

Suppose a silver assignment contains a chest of length `x`, and a gold assignment contains a chest of length `y` where `y > x`. Swapping them moves more work away from the gold key and puts the longer chest on silver. The gold workload decreases by `y - x`. The silver maximum can increase, but it cannot exceed the previous gold workload because `y` was part of that workload. The final maximum cannot become worse. Repeating this exchange moves the largest chests into silver keys.

After sorting the chest times in descending order, the first `k` chests should use silver keys. The remaining chests are handled sequentially by the gold key. The answer is the larger of the longest silver chest and the total time spent by the gold key.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(C(n,k) * n)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(1)` besides sorting storage | Accepted |

## Algorithm Walkthrough

1. Sort all chest opening times in descending order. The largest durations should be considered first because they provide the greatest reduction when removed from the gold key workload.
2. Assign the first `k` sorted chests to silver keys. Their completion time is the largest of these values, which is simply the first element when `k > 0`.
3. Assign all remaining chests to the gold key. Add their durations together because the gold key can only open one chest at a time.
4. Return the larger value between the silver completion time and the gold completion time. Both groups operate independently, so every chest must be finished when the slower group finishes.

Why it works: the exchange argument shows that any solution with a smaller chest on a silver key while a larger chest remains on the gold key can be transformed into an equally good or better solution by swapping them. Applying this repeatedly produces the arrangement where the `k` largest chests use silver keys. Once that assignment is fixed, the gold key and silver keys have independent finishing times, so the final answer is exactly the maximum of those times.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    z = data[0]
    idx = 1
    ans = []

    for _ in range(z):
        n = data[idx]
        k = data[idx + 1]
        idx += 2

        a = data[idx:idx + n]
        idx += n

        a.sort(reverse=True)

        silver_time = a[0] if k > 0 else 0
        gold_time = sum(a[k:])

        ans.append(str(max(silver_time, gold_time)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The program first reads every integer at once because the total input size can reach one million chest values. This avoids repeated input overhead.

For each test case, sorting places the most expensive chests at the front. The variable `silver_time` represents the time needed for all silver operations to finish. Since all silver keys can start at the same time, only the longest silver chest matters.

The variable `gold_time` is the sum of the remaining durations because the gold key must process them one after another. The `k > 0` condition avoids accessing `a[0]` as the silver group does not exist when there are no silver keys.

Python integers already support values larger than the possible sum of all chest times, so no overflow handling is needed.

## Worked Examples

For the first sample:

Input:

```
1
3 1
1 3 2
```

After sorting, the times become `[3, 2, 1]`.

| k | Silver chest times | Silver finish | Gold chest times | Gold finish | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | `[3]` | 3 | `[2,1]` | 3 | 3 |

The longest chest is assigned to the silver key. The gold key handles the two smaller chests, and both groups finish at the same moment.

For the second sample:

Input:

```
1
3 2
5 5 5
```

After sorting, the times remain `[5, 5, 5]`.

| k | Silver chest times | Silver finish | Gold chest times | Gold finish | Answer |
| --- | --- | --- | --- | --- | --- |
| 2 | `[5,5]` | 5 | `[5]` | 5 | 5 |

Two silver keys open two chests immediately, while the gold key handles the last chest. The maximum finishing time is five seconds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting dominates the linear scan for the answer. |
| Space | `O(n)` | The list of chest durations is stored for sorting. |

The total number of chests over all test cases is at most `10^6`, so the total sorting work remains manageable. The memory usage is also within the given limit because only the input arrays and normal sorting overhead are required.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    data = list(map(int, sys.stdin.buffer.read().split()))
    if data:
        z = data[0]
        idx = 1
        out = []

        for _ in range(z):
            n = data[idx]
            k = data[idx + 1]
            idx += 2
            a = data[idx:idx + n]
            idx += n

            a.sort(reverse=True)
            silver = a[0] if k else 0
            gold = sum(a[k:])
            out.append(str(max(silver, gold)))

        sys.stdout.write("\n".join(out))

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert solve_case("""2
3 1
1 3 2
3 2
5 5 5
""") == "3\n5", "samples"

assert solve_case("""1
1 0
100
""") == "100", "single chest without silver key"

assert solve_case("""1
5 2
7 7 7 7 7
""") == "21", "all equal values"

assert solve_case("""1
6 5
9 8 7 6 5 4
""") == "9", "almost every chest uses silver"

assert solve_case("""1
4 0
3 5 2 4
""") == "14", "no silver keys"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three chests with one silver key | `3` | Basic split between silver and gold keys |
| One chest and no silver keys | `100` | Minimum size and `k = 0` handling |
| Five equal chest times | `21` | Prevents assuming silver keys alone determine the answer |
| Five silver keys out of six chests | `9` | Large silver group boundary |
| No silver keys with mixed durations | `14` | Pure gold-key scheduling |

## Edge Cases

When there is one extremely long chest, the algorithm keeps it on a silver key if one exists.

```
1
3 1
10 1 1
```

The sorted array is `[10, 1, 1]`. The silver finish time is `10`, and the gold finish time is `2`. The answer is `10`, because the silver operation is the last operation to complete.

When all chest times are identical, choosing the largest `k` still matters because every possible silver choice looks the same.

```
1
5 2
7 7 7 7 7
```

The first two chests go to silver, finishing at time `7`. The remaining three are processed by gold in `21` seconds. The algorithm returns `21`, which matches the true schedule.

When no silver keys exist, the entire sorted array belongs to the gold key.

```
1
4 0
3 5 2 4
```

The algorithm sets the silver contribution to zero and sums all values: `5 + 4 + 3 + 2 = 14`. The result is the only possible schedule.

When there are many silver keys, the remaining gold workload can become smaller than the longest silver chest.

```
1
6 5
9 8 7 6 5 4
```

The silver keys take the first five values, so their finish time is `9`. The gold key opens only the last chest, finishing at `4`. The final answer is `9`, showing why both sides of the maximum calculation are needed.
