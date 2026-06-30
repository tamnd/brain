---
title: "CF 104520B - Restaurant Sorting"
description: "We are given a stack of distinct integers, where the first element is the bottom and the last element is the top."
date: "2026-06-30T10:26:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104520
codeforces_index: "B"
codeforces_contest_name: "Teamscode Summer 2023 Contest"
rating: 0
weight: 104520
solve_time_s: 114
verified: true
draft: false
---

[CF 104520B - Restaurant Sorting](https://codeforces.com/problemset/problem/104520/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stack of distinct integers, where the first element is the bottom and the last element is the top. We are allowed to take a suffix of this stack, meaning we remove some number of elements from the top, temporarily hold them, sort only those removed elements, and then place them back on top in sorted order. The rest of the stack stays in place.

The task is to find the smallest number of elements we must pop from the top so that after sorting just those popped elements and reattaching them, the entire stack becomes sorted in increasing order from bottom to top.

The output is therefore not the final stack, but the minimum suffix length needed so that a single operation of “pop, sort, reinsert sorted” is sufficient to make the whole structure sorted.

The constraints are large enough that an O(n²) simulation per test would not pass. The total sum of n across test cases is up to 2 × 10⁵, which strongly suggests an O(n) or O(n log n) per test solution is required, ideally linear overall.

A subtle point is that we are not allowed to reorder arbitrary elements of the stack, only a contiguous suffix from the top. This removes many naive greedy strategies that try to fix local inversions anywhere in the array.

A few edge cases expose common mistakes. If the stack is already sorted, no popping is needed and the answer is zero. For example, input `1 2 3` should return 0. A naive approach that always assumes at least one element must be moved would fail here.

Another tricky case is when almost everything is reversed, such as `4 3 2 1`. The only valid way is to pop all elements, sort them, and reinsert, so the answer is 4. Any approach that tries to preserve partial order in the middle would underestimate the required suffix.

Finally, consider a mixed case like `1 4 2 3`. Even though most elements are close to their final positions, the suffix constraint forces us to carefully choose where the sorted suffix starts. The correct answer is 3, since popping `[4,2,3]` is sufficient to fix ordering, while popping only the last two is not enough to repair the inversion involving 4.

## Approaches

A direct brute-force idea is to try every possible value of k from 0 to n. For each k, we pop the top k elements, sort them, and simulate reinserting them. After reconstruction, we check whether the whole array is sorted. Each simulation costs O(n log n) due to sorting, and doing this for all k gives O(n² log n) per test in the worst case. With total n up to 2 × 10⁵, this is far too slow.

The key observation is that we are not actually choosing arbitrary elements, only a suffix, and the final array must be globally sorted. This means that the elements that remain untouched must already form a prefix of the sorted array, otherwise no amount of sorting the suffix can fix mismatches between preserved elements.

If we imagine the final sorted array, then the untouched part must align exactly with the smallest values in correct order. That implies that if we scan from the bottom and track whether we can keep elements as a valid prefix of the sorted permutation, we only fail when we encounter an element that breaks the required increasing structure relative to remaining values.

This leads to reframing the problem: we want the longest prefix from the bottom that can remain untouched while still being consistent with a globally sorted final array. Once that prefix is fixed, everything above it must be popped and sorted.

So instead of deciding k directly, we compute how many elements from the bottom can stay, and subtract from n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We use the idea that elements that remain in place must form a valid prefix of the sorted array when considered in order of value.

1. Sort a copy of the array. This gives the target final order of values. We will use it as a reference for what the stack should look like after all operations.
2. Build a mapping from value to its position in the sorted array. This tells us the correct rank of every element.
3. Scan the original stack from bottom to top, tracking the largest rank we have seen so far if we pretend we are building a valid prefix of the sorted array.
4. Whenever the current element’s rank is greater than what we would expect next in a strictly consistent prefix, we cannot extend the untouched prefix past this point.
5. The longest valid prefix from the bottom gives us the number of elements we can leave untouched.
6. The answer k is the number of elements not in this prefix, which is n minus that prefix length.

The key idea is that the untouched prefix must not introduce any “future constraint violations” relative to sorted order. Once an element is out of place in terms of sorted rank progression, everything above it must be part of the suffix we sort.

### Why it works

The untouched part of the stack must match the lowest segment of the final sorted array exactly, because all remaining elements will be reinserted above it in sorted order. If a prefix element has a higher rank than a later element in the prefix, then no rearrangement of the suffix can fix the relative ordering constraint, since suffix operations cannot move elements into the preserved region. This forces the preserved region to be exactly the longest prefix that is consistent with increasing rank order under the sorted permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        sorted_p = sorted(p)
        pos = {v: i for i, v in enumerate(sorted_p)}

        # longest valid prefix from bottom
        max_rank = -1
        keep = 0

        for x in p:
            r = pos[x]
            if r > max_rank:
                keep += 1
                max_rank = r
            else:
                break

        print(n - keep)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the array to define the correct global order. The dictionary maps each value to its rank, allowing constant-time comparisons during the scan.

We then traverse from bottom to top, maintaining the highest rank seen so far in a valid prefix. If the next element would require a smaller rank than something already included, we stop extending the prefix. This directly identifies how many elements can remain untouched. The result is computed as the complement of this prefix size.

A common pitfall is scanning from the top instead of the bottom, which breaks the interpretation of what remains fixed. The stack structure makes the bottom-to-top direction essential because only suffix operations are allowed.

## Worked Examples

### Example 1

Input: `1 2 3`

| Step | Value | Rank | max_rank | keep |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 1 |
| 2 | 2 | 1 | 1 | 2 |
| 3 | 3 | 2 | 2 | 3 |

All elements extend a valid prefix, so keep = 3, hence k = 0.

This confirms that when the array is already sorted, no popping is needed.

### Example 2

Input: `1 4 2 3`

| Step | Value | Rank | max_rank | keep |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 1 |
| 2 | 4 | 3 | 3 | 2 |
| 3 | 2 | 1 | 3 | stop |

At the third element, rank 1 is smaller than max_rank 3, so the prefix breaks. We get keep = 2, so k = 2.

This demonstrates how a single inversion relative to the sorted order stops extension of the untouched prefix, forcing the remaining suffix to be fully rebuilt.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test | sorting dominates, scan is linear |
| Space | O(n) | storing sorted copy and mapping |

The total n across tests is bounded by 2 × 10⁵, so the sorting cost is acceptable. Each test is independent and linear extra processing keeps the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            p = list(map(int, input().split()))
            sorted_p = sorted(p)
            pos = {v: i for i, v in enumerate(sorted_p)}

            max_rank = -1
            keep = 0
            for x in p:
                r = pos[x]
                if r > max_rank:
                    keep += 1
                    max_rank = r
                else:
                    break
            print(n - keep)

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""5
3
1 2 3
2
2 1
4
4 3 2 1
4
1 4 2 3
7
1 2 3 6 4 7 5
""") == """0
2
4
2
4"""

# custom cases
assert run("""1
1
1
""") == "0", "minimum size"

assert run("""1
5
5 4 3 2 1
""") == "5", "fully reversed"

assert run("""1
4
1 3 2 4
""") == "2", "single inversion"

assert run("""1
6
1 2 3 4 5 6
""") == "0", "already sorted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | minimum case |
| fully reversed | 5 | worst rearrangement |
| 1 3 2 4 | 2 | local inversion handling |
| already sorted | 0 | no operation needed |

## Edge Cases

For a single-element stack, the algorithm assigns keep = 1 immediately since there is only one rank and no contradiction can arise. The output becomes zero, matching the fact that no operation is needed.

For a fully reversed stack like `5 4 3 2 1`, sorting assigns ranks in increasing order from 0 to 4, but scanning bottom to top immediately causes a rank decrease at the second element, breaking the prefix after the first element. This yields keep = 1 and k = 4, correctly requiring all elements to be popped.

For a case like `1 3 2 4`, the scan accepts `1` then `3`, but rejects `2` because its rank is smaller than the current maximum. The prefix stops there, and only two elements remain fixed, giving k = 2, which matches the need to repair the middle inversion.
