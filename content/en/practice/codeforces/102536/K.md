---
title: "CF 102536K - I Brook the Code!"
description: "The input describes the same group of people in two parallel arrays. The value at position i in the weights array belongs to the person whose height is stored at position i in the heights array."
date: "2026-08-04T02:14:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102536
codeforces_index: "K"
codeforces_contest_name: "2020 UP ACM Algolympics Final Round"
rating: 0
weight: 102536
solve_time_s: 123
verified: true
draft: false
---

[CF 102536K - I Brook the Code!](https://codeforces.com/problemset/problem/102536/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes the same group of people in two parallel arrays. The value at position `i` in the weights array belongs to the person whose height is stored at position `i` in the heights array. The goal is to recover the hidden sequence by arranging these people from shortest height to tallest height and printing their weights in that new order.

The key detail is that the heights identify the ordering, while the weights are the values we need to move. The two arrays cannot be sorted independently because the relationship between a person's height and weight must stay together. A pair `(height, weight)` represents one person, and the answer is the list of weights after sorting these pairs by height.

The constraint `n <= 100000` means the solution needs to handle around one hundred thousand people efficiently. An algorithm that compares every pair of people would require about ten billion comparisons in the worst case, which is far beyond what a 2-second limit allows. A sorting-based approach with `O(n log n)` operations is appropriate because it performs roughly a few million comparisons for this input size.

The large values of weights and heights, up to `10^11`, rule out approaches that depend on small ranges such as counting sort. They also require using integer types that can store large values. Python integers already support arbitrary precision, so no special handling is required.

A common mistake is sorting only the weights or only the heights. For example, consider:

```
3
5 1 9
2 1 3
```

The correct output is:

```
1 5 9
```

The people sorted by height are `(height=1, weight=1)`, `(height=2, weight=5)`, and `(height=3, weight=9)`. If someone sorted the weights independently, they would accidentally lose the original pair information.

Another edge case is when the input is already ordered by height:

```
3
7 8 9
10 20 30
```

The output remains:

```
7 8 9
```

A solution that assumes some reordering must happen could incorrectly modify the answer.

A single person is also a valid case:

```
1
42
100000000000
```

The answer is:

```
42
```

There is no sorting work needed beyond handling the one existing pair.

## Approaches

The direct brute-force approach is to repeatedly find the person with the smallest remaining height, output their weight, and remove them from consideration. This is correct because each selection chooses exactly the next person in height order. However, finding the minimum among the remaining people costs linear time, and doing it for all `n` people costs:

$$n + (n-1) + (n-2) + \dots + 1 = O(n^2)$$

For `n = 100000`, this reaches approximately five billion comparisons, which cannot finish within the time limit.

The observation that makes the problem simple is that the only operation required is sorting people by one field while carrying another field along. Instead of searching for the next smallest height manually, we can let a comparison sort perform all ordering decisions. We create pairs containing each person's height and weight, sort the pairs by height, and read the weights in sorted order.

The brute-force method works because it reconstructs the sorted order one person at a time, but it fails because it repeatedly solves the same ordering problem. The sorting approach solves all ordering decisions together, reducing the complexity from quadratic to `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a list of pairs where each pair stores one person's height and weight. The height is the sorting key, while the weight is the information that must be recovered after sorting.
2. Sort the list of pairs by the height value in ascending order. Since every height is unique, this produces exactly one valid order of people.
3. Traverse the sorted pairs and collect their weight values. The collected sequence is the hidden code because it matches the order John would obtain after arranging the people by height.

Why it works:

The algorithm maintains the invariant that every pair remains connected throughout the process. Sorting changes only the positions of complete people, not the relationship between a height and its corresponding weight. After sorting, the first pair has the smallest height, the second pair has the second smallest height, and so on. Reading weights from these pairs therefore produces exactly the required sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    weights = list(map(int, input().split()))
    heights = list(map(int, input().split()))

    people = [(heights[i], weights[i]) for i in range(n)]
    people.sort()

    answer = [str(weight) for height, weight in people]
    print(" ".join(answer))

if __name__ == "__main__":
    solve()
```

The solution first reads both arrays separately because the input stores heights and weights in parallel positions. The list comprehension creates `(height, weight)` pairs so that sorting keeps each person's data together.

The call to `sort()` uses Python's tuple ordering. It compares the first element of each tuple, which is the height, and places smaller heights earlier. The problem guarantees all heights are different, so no secondary comparison can affect the result.

The final loop extracts only the weight from each sorted pair. Building strings before joining avoids repeated string concatenation and keeps output efficient for `100000` values.

Python integers handle the values up to `10^11` without overflow. There are no indexing edge cases because every index from `0` to `n-1` is used exactly once when building the pairs.

## Worked Examples

For the sample:

```
3
2 1 4
1 4 3
```

the pairs are `(1,2)`, `(4,1)`, and `(3,4)`.

| Step | Sorted pairs | Extracted answer |
| --- | --- | --- |
| Initial pairs | (1,2), (4,1), (3,4) | empty |
| After sorting | (1,2), (3,4), (4,1) | empty |
| Read weights | (1,2), (3,4), (4,1) | 2 4 1 |

The trace shows why storing pairs is necessary. The weights move because their corresponding heights move.

A second example:

```
4
30 10 40 20
50 10 40 30
```

The pairs are `(50,30)`, `(10,10)`, `(40,40)`, and `(30,20)`.

| Step | Sorted pairs | Extracted answer |
| --- | --- | --- |
| Initial pairs | (50,30), (10,10), (40,40), (30,20) | empty |
| After sorting | (10,10), (30,20), (40,40), (50,30) | empty |
| Read weights | (10,10), (30,20), (40,40), (50,30) | 10 20 40 30 |

This example exercises a completely shuffled input order and confirms that the original positions do not matter after pairing height with weight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting `n` height-weight pairs dominates the runtime. |
| Space | O(n) | The pair list and answer storage both grow linearly with the number of people. |

For `n = 100000`, sorting requires a manageable number of comparisons and fits comfortably within the time limit. The memory usage is also linear and remains within the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    weights = list(map(int, sys.stdin.readline().split()))
    heights = list(map(int, sys.stdin.readline().split()))

    people = [(heights[i], weights[i]) for i in range(n)]
    people.sort()

    result = " ".join(str(weight) for height, weight in people)

    sys.stdin = old_stdin
    return result

assert solve("""3
2 1 4
1 4 3
""") == "2 4 1", "sample 1"

assert solve("""1
42
100000000000
""") == "42", "single person"

assert solve("""4
30 10 40 20
50 10 40 30
""") == "10 20 40 30", "unordered heights"

assert solve("""5
8 8 8 8 8
5 1 4 3 2
""") == "8 8 8 8 8", "equal weights"

assert solve("""5
100 200 300 400 500
50000000000 1 99999999999 2 3
""") == "200 400 500 100 300", "large height values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` with one pair | `42` | Handles the smallest possible input. |
| Shuffled heights | `10 20 40 30` | Confirms sorting is based on height, not input order. |
| All weights equal | `8 8 8 8 8` | Confirms equal values do not affect ordering. |
| Very large heights | `200 400 500 100 300` | Checks handling of values near the upper bound. |

## Edge Cases

For the case where sorting only one array loses the relationship between values, consider:

```
3
5 1 9
2 1 3
```

The algorithm creates the pairs `(2,5)`, `(1,1)`, and `(3,9)`. Sorting gives `(1,1)`, `(2,5)`, and `(3,9)`, so the output is `1 5 9`. The weight values stay attached to the correct people, avoiding the mistake of independently sorting the arrays.

For the already sorted case:

```
3
7 8 9
10 20 30
```

The pairs are `(10,7)`, `(20,8)`, and `(30,9)`. Sorting does not change their order, and extracting weights gives `7 8 9`. The algorithm does not assume that movement is necessary.

For the single-person case:

```
1
42
100000000000
```

The pair list contains only `(100000000000,42)`. Sorting a one-element list leaves it unchanged, and the extracted weight is `42`, which matches the required output.
