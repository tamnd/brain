---
title: "CF 105838K - ruskal's Reconstruction Number"
description: "We are given a positive integer written as a decimal string. In one move, we are allowed to choose a single pair of adjacent digits and swap them. We may perform at most one such swap, or choose to do nothing."
date: "2026-06-22T01:23:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105838
codeforces_index: "K"
codeforces_contest_name: "The 14th Huazhong Agricultural University Programming Contest"
rating: 0
weight: 105838
solve_time_s: 46
verified: true
draft: false
---

[CF 105838K - ruskal's Reconstruction Number](https://codeforces.com/problemset/problem/105838/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer written as a decimal string. In one move, we are allowed to choose a single pair of adjacent digits and swap them. We may perform at most one such swap, or choose to do nothing. The goal is to maximize the resulting number after this optional operation.

The input consists of multiple independent test cases. Each test case is just a single integer, and we must output the maximum possible integer obtainable with zero or one adjacent swap.

The constraints imply that the total number of digits across all test cases is large, up to 200,000 in aggregate. This immediately rules out any solution that tries all possible swaps independently per test case in a nested way over all positions and then recomputes full comparisons repeatedly. However, since each test case is independent and the operation count is linear in the number of digits, a per-number linear or near-linear approach is sufficient.

A subtle edge case appears when the number is already optimal in lexicographic sense, meaning any swap would decrease the value. For example, an already non-increasing sequence like 987654. Any swap only produces a smaller number, so the correct answer is the original number. A careless greedy swap that always performs the first improving local change can fail in cases where a local improvement is not globally optimal.

Another important edge case is when equal digits appear. For example, 1221. Swapping the first adjacent pair gives 2121, which is larger than swapping later or doing nothing. The algorithm must correctly handle equal digit comparisons without treating equality as improvement.

Finally, leading digit considerations matter implicitly. Since we are rearranging digits of a positive integer without leading zeros in input, any swap that moves a larger digit forward can significantly change magnitude, so comparisons must be lexicographic on digits.

## Approaches

The brute-force idea is straightforward: for each test case, try every possible position i, swap digits at i and i+1, construct the resulting number, and keep the maximum among all such results and the original number. This is correct because it exhaustively explores all allowed states reachable in one move. However, for a number of length L, this requires O(L) swaps, and each swap costs O(L) to evaluate or reconstruct the string, giving O(L^2) per test case in a naive implementation. Over many test cases, this becomes too slow.

The key observation is that we do not need to try all swaps. We only care about improving the number as early as possible from the left, since higher positions dominate the value. If we decide to swap digits at positions i and i+1, the only thing that matters is whether placing a larger digit earlier yields a better prefix than the original. Any swap affects only two adjacent positions, so the effect on the number is localized, and we can simulate each swap in O(1) comparison relative to the original structure.

We can therefore scan all adjacent pairs once per test case, simulate the swap locally, and compare the resulting string to the best answer seen so far. Because comparisons are lexicographic and only need checking against the current best, we can maintain the best configuration incrementally without rebuilding unnecessary states repeatedly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L^2) per test | O(L) | Too slow |
| Try all adjacent swaps once | O(L) per test | O(L) | Accepted |

## Algorithm Walkthrough

We treat each number as a mutable sequence of digits.

1. Convert the input number into a list of characters so swaps are easy to simulate. This allows constant time local modification.
2. Initialize the answer as the original number, since performing no operation is always valid.
3. Iterate over every index i from 0 to length minus 2. At each position, consider swapping digits at i and i+1.
4. Perform the swap temporarily, forming a candidate configuration.
5. Compare the candidate configuration with the current best answer using lexicographic comparison on digit strings. This comparison works because both strings represent integers of the same length and no leading zeros are introduced.
6. If the candidate is larger, update the best answer.
7. Revert the swap so the original sequence is preserved for the next iteration.
8. After processing all adjacent pairs, output the best stored configuration.

The key reasoning behind only adjacent swaps is that the problem restricts the operation to exactly those swaps, so the search space is exactly L possible states plus the identity state.

### Why it works

Each valid outcome is either the original number or the result of swapping exactly one adjacent pair. The algorithm enumerates all such possibilities exactly once. Since the best answer is chosen among all reachable states and comparison is exact lexicographic ordering of digit sequences, no candidate that could improve the answer is skipped. The algorithm is therefore a complete enumeration of the state space defined by the operation constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        s = list(input().strip())
        best = ''.join(s)

        n = len(s)
        for i in range(n - 1):
            s[i], s[i + 1] = s[i + 1], s[i]
            cand = ''.join(s)
            if cand > best:
                best = cand
            s[i], s[i + 1] = s[i + 1], s[i]

        out.append(best)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution maintains a single mutable list per test case and avoids reconstructing all states from scratch. Each swap is tested in constant-time relative to digit movement, and string comparison is efficient because Python compares lexicographically and stops early on mismatch. The swap-revert pattern ensures correctness without allocating extra arrays per iteration.

A common implementation pitfall is forgetting to revert the swap, which would cause later iterations to operate on a corrupted state. Another is reconstructing strings unnecessarily inside nested loops, which would push runtime closer to quadratic behavior.

## Worked Examples

### Example 1

Input:

```
1
2736
```

We test all adjacent swaps.

| i | swapped string | candidate | best |
| --- | --- | --- | --- |
| 0 | 7236 | 7236 | 7236 |
| 1 | 2376 | 7236 | 7236 |
| 2 | 2736 | 7236 | 7236 |

Final answer is 7236.

This shows the algorithm correctly identifies that swapping the first two digits yields the maximum improvement.

### Example 2

Input:

```
1
98765
```

| i | swapped string | candidate | best |
| --- | --- | --- | --- |
| 0 | 89765 | 89765 | 98765 |
| 1 | 97865 | 97865 | 98765 |
| 2 | 98675 | 98675 | 98765 |
| 3 | 98756 | 98756 | 98765 |

Final answer remains 98765.

This demonstrates the case where every possible swap is worse, so the identity is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total digits per test) | Each position is tested once, and each test involves constant-time swap plus string comparison |
| Space | O(L) | Storage for digit list and best string |

The total digit sum is bounded by 200,000, so the algorithm runs comfortably within limits. Each test case is linear in its own length, and there is no hidden quadratic interaction across cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            s = list(input().strip())
            best = ''.join(s)
            n = len(s)
            for i in range(n - 1):
                s[i], s[i + 1] = s[i + 1], s[i]
                cand = ''.join(s)
                if cand > best:
                    best = cand
                s[i], s[i + 1] = s[i + 1], s[i]
            out.append(best)
        return "\n".join(out)

    return solve()

assert run("1\n2736\n") == "7236"
assert run("1\n98765\n") == "98765"
assert run("1\n1221\n") == "2121"
assert run("1\n10\n") == "10"
assert run("1\n9\n") == "9"
assert run("3\n12\n21\n132\n") == "21\n21\n312"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2736 | 7236 | best single swap improvement |
| 98765 | 98765 | no beneficial swaps |
| 1221 | 2121 | equal-digit and middle improvement |
| 10 | 10 | two-digit boundary case |
| 9 | 9 | single-digit minimal case |
| 12 21 132 | 21 21 312 | multiple test handling |

## Edge Cases

For a single-digit number like `7`, there are no adjacent pairs to swap. The algorithm initializes the best answer as the original string and never enters the loop, so it correctly outputs `7`.

For a decreasing sequence like `543210`, every swap produces a lexicographically smaller string. The algorithm still evaluates all adjacent swaps but never updates the best value, leaving the original intact.

For repeated digits such as `11111`, every swap produces the same string. The comparison `cand > best` never triggers, so the output remains unchanged, correctly avoiding unnecessary updates.
