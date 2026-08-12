---
title: "CF 102330B - \u041f\u043e\u0435\u0437\u0434\u043a\u0430 \u043d\u0430 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0443"
description: "There are n train cars. In car i, a[i] seats are still free after the chemistry team has bought its tickets. The informatics team has exactly k participants and wants to buy tickets so that every car in which they travel becomes completely full."
date: "2026-08-13T03:56:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102330
codeforces_index: "B"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2019.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102330
solve_time_s: 54
verified: true
draft: false
---

[CF 102330B - \u041f\u043e\u0435\u0437\u0434\u043a\u0430 \u043d\u0430 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0443](https://codeforces.com/problemset/problem/102330/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` train cars. In car `i`, `a[i]` seats are still free after the chemistry team has bought its tickets. The informatics team has exactly `k` participants and wants to buy tickets so that every car in which they travel becomes completely full. Since nobody except the chemistry participants is allowed to share such a car, every remaining free seat in a chosen car must be occupied by an informatics participant.

Consequently, if the team uses a set of cars, the total number of free seats in those cars must be exactly `k`. The chosen cars should form the smallest possible contiguous segment in terms of its first and last car numbers. A car with `a[i] = 0` can occur between two relevant cars, because it is already full and needs no new ticket. We only have to output the endpoints of the optimal segment.

For example, with `a = [1, 2, 3, 4]` and `k = 5`, cars 2 and 3 contain exactly five free seats, so the answer is `2 3`. With `a = [1, 0, 2]` and `k = 3`, the whole segment from car 1 through car 3 has exactly three free seats, and the middle car is already full.

The number of cars is at most `10^5`. A quadratic algorithm would consider about `n(n+1)/2`, which is close to `5 * 10^9` intervals at the maximum size. That is far beyond what a one-second competitive programming limit can handle. The values of `a[i]` and `k` can reach `10^9`, and their sum can also reach `10^9`, so the implementation should conceptually use integer arithmetic that safely handles sums of this size. Python integers have no overflow issue here.

There are several edge cases that can make a careless implementation fail. First, the answer can consist of one car. For input

```
1 5
5
```

the correct output is `1 1`. An implementation that only checks segments of length at least two would miss it.

Second, completely full cars can occur inside the answer. For

```
3 3
1 0 2
```

the correct output is `1 3`. The zero in the middle contributes nothing, but the endpoints still have to be reported as `1` and `3`.

Third, an exact sum is required. For

```
2 5
2 2
```

the correct output is `-1`. The entire train has only four free seats, so buying five tickets cannot fill every selected car.

Finally, zero-valued cars can create several segments with the same number of nonzero cars but different endpoint distances. For

```
5 3
0 1 0 2 0
```

the correct output is `2 4`. The segment contains three free seats, while extending it to include either zero-valued endpoint would make the interval longer and therefore worse.

## Approaches

A direct solution can enumerate every possible interval `[l, r]` and calculate its sum. Using prefix sums, each interval sum can be obtained in constant time, so the algorithm takes `O(n^2)` time and `O(n)` memory. It is correct because every possible choice of first and last car is explicitly examined, and among those whose sum is `k`, we can keep the shortest one.

The problem is the number of intervals. For `n = 100000`, there are

`n(n + 1) / 2 = 5,000,050,000`

different intervals. Even though each sum lookup is constant time, several billion iterations are much too slow.

The key observation is that every `a[i]` is nonnegative. This gives the interval sum a monotonic behavior. If we extend an interval to the right, its sum can only stay the same or increase. If we move its left endpoint to the right, its sum can only stay the same or decrease.

That is exactly the structure needed for a two-pointer sliding window. We maintain a window `[l, r]` and its sum. We extend `r` until the sum reaches or passes `k`. If the sum is exactly `k`, the current window is a candidate. Then we remove elements from the left while possible, because removing a positive value makes the window shorter and can reveal a better answer. Zero-valued cars require special care, since removing them does not change the sum and can shorten the answer even though the sum stays equal to `k`.

The brute-force works because every interval independently answers the question "does this segment contain exactly `k` free seats?" The observation that nonnegative values make the sum monotonic lets us reuse the information from one interval while moving to the next, reducing the work to linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2)` | `O(n)` | Too slow |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read `n`, `k`, and the array `a`. We need to find an interval whose sum is exactly `k`, with minimum length.
2. Initialize the left pointer `l = 0`, the current sum `s = 0`, and variables storing the best interval found so far.
3. Move the right pointer `r` from left to right. Add `a[r]` to `s`, because the current window now includes this car.
4. While `s > k`, remove `a[l]` from `s` and increment `l`. Since all values are nonnegative, the only way to reduce an excessive sum is to move the left boundary forward.
5. After reducing the window, if `s == k`, the current interval is valid. Compare its length with the best interval found so far and keep it if it is shorter.
6. When `s == k`, repeatedly removing leading zeroes is useful because they do not change the sum. In the implementation, this is naturally handled by the same left-boundary movement logic before comparing candidate lengths, or by explicitly shrinking zeroes after finding an exact sum. This matters because `[0, 1, 2]` and `[1, 2]` have the same sum, but the latter is the better interval.
7. After processing every right endpoint, if no interval with sum `k` was found, print `-1`. Otherwise print the best interval's endpoints using one-based car numbering.

### Why it works

At every moment, the window contains a contiguous sequence of cars and `s` is exactly the sum of their free seats. Because all `a[i]` are nonnegative, extending the right endpoint never decreases `s`, while advancing the left endpoint never increases it. Thus, once a window has sum greater than `k`, keeping its current left endpoint cannot produce a valid larger right endpoint, so the left endpoint can safely advance. Whenever the window has sum exactly `k`, it is a valid solution, and removing leading zeroes gives the shortest interval with that same right endpoint. Since every right endpoint is processed and every pointer only moves forward, the algorithm considers the shortest possible valid interval associated with every position and therefore finds a globally shortest one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    left = 0
    current_sum = 0

    best_left = -1
    best_right = -1
    best_len = n + 1

    for right in range(n):
        current_sum += a[right]

        while left <= right and current_sum > k:
            current_sum -= a[left]
            left += 1

        if current_sum == k:
            while left <= right and a[left] == 0:
                left += 1

            length = right - left + 1

            if length < best_len:
                best_len = length
                best_left = left
                best_right = right

    if best_left == -1:
        print(-1)
    else:
        print(best_left + 1, best_right + 1)

if __name__ == "__main__":
    solve()
```

The input is read once and stored in `a`, after which `left` and `right` represent the current sliding window. `current_sum` is updated whenever either boundary moves, so no prefix-sum array is necessary.

The `while current_sum > k` loop is safe because all values are nonnegative. Once the sum is too large, moving the left boundary is the only operation that can reduce it. Every element is removed from the window at most once, so this loop contributes only `O(n)` total work rather than `O(n)` work for every right endpoint.

The second loop removes zero-valued cars from the left after an exact sum has been found. This is a subtle boundary condition. Suppose the current window is `[0, 1, 2]` and `k = 3`. Its sum is already correct, but `[1, 2]` is a strictly shorter valid interval. Because removing zero does not change `current_sum`, we can discard such cars safely.

The answer is stored using zero-based indices internally and converted to one-based indices only when printing. No special integer type is required in Python because Python integers automatically grow as needed.

## Worked Examples

### Sample 1

The input is:

```
7 5
1 2 3 4 2 1 2
```

The relevant state while moving the right endpoint is:

| `right` | Added `a[right]` | `left` | `current_sum` | Candidate |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | none |
| 1 | 2 | 0 | 3 | none |
| 2 | 3 | 0 | 6 | too large |
| 2 | removed `1` | 1 | 5 | `[1, 2]` |
| 3 | 4 | 1 | 9 | too large |
| 3 | removed `2` | 2 | 7 | too large |
| 3 | removed `3` | 3 | 4 | none |
| 4 | 2 | 3 | 6 | too large |
| 4 | removed `4` | 4 | 2 | none |
| 5 | 1 | 4 | 3 | none |
| 6 | 2 | 4 | 5 | `[4, 6]` |

The first valid window is cars 2 through 3, with `2 + 3 = 5`. Later, cars 5 through 7 also sum to five, but that interval is longer. The answer is therefore `2 3`.

This trace demonstrates the main sliding-window invariant: when the sum becomes too large, advancing `left` eventually restores a sum at most `k`, and no possible shorter valid interval is skipped.

### Sample 2

The input is:

```
5 3
1 0 2 10 10
```

The trace is:

| `right` | Added `a[right]` | `left` | `current_sum` | Candidate |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | none |
| 1 | 0 | 0 | 1 | none |
| 2 | 2 | 0 | 3 | `[0, 2]` |
| 3 | 10 | 0 | 13 | too large |
| 3 | removed `1` | 1 | 12 | too large |
| 3 | removed `0` | 2 | 12 | too large |
| 3 | removed `2` | 3 | 10 | too large |
| 3 | removed `10` | 4 | 0 | none |
| 4 | 10 | 4 | 10 | too large |
| 4 | removed `10` | 5 | 0 | none |

The first valid interval is cars 1 through 3. The zero-valued second car is already full, so the three free seats are exactly the one seat in car 1 and two seats in car 3. The output is `1 3`.

This example demonstrates why zero-valued cars must be allowed inside the interval. They consume no tickets, but they do not prevent the informatics team from occupying the cars on either side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | The right pointer moves from left to right once, and the left pointer also moves only forward. |
| Space | `O(n)` | The array of `n` free-seat counts is stored in memory. |

With `n <= 100000`, a linear scan performs only a small number of operations per car. The memory usage is also comfortably within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    left = 0
    current_sum = 0

    best_left = -1
    best_right = -1
    best_len = n + 1

    for right in range(n):
        current_sum += a[right]

        while left <= right and current_sum > k:
            current_sum -= a[left]
            left += 1

        if current_sum == k:
            while left <= right and a[left] == 0:
                left += 1

            length = right - left + 1

            if length < best_len:
                best_len = length
                best_left = left
                best_right = right

    if best_left == -1:
        print(-1)
    else:
        print(best_left + 1, best_right + 1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run("""7 5
1 2 3 4 2 1 2
""") == "2 3", "sample 1"

assert run("""5 3
1 0 2 10 10
""") == "1 3", "sample 2"

# Minimum-size input
assert run("""1 5
5
""") == "1 1", "single car"

# Impossible case
assert run("""2 5
2 2
""") == "-1", "total free seats are insufficient"

# All equal values, answer spans the whole array
assert run("""5 3
1 1 1 1 1
""") == "1 3", "all equal values"

# Zeroes around a valid segment
assert run("""5 3
0 1 0 2 0
""") == "2 4", "zero boundaries"

# Exact boundary after shrinking from the left
assert run("""4 6
2 4 1 5
""") == "1 2", "exact prefix"

# Maximum-size style case
n = 100000
assert run(f"{n} {n}\n" + " ".join(["1"] * n) + "\n") == "1 100000", "large input"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 / 5` | `1 1` | Minimum size and single-car answer |
| `2 5 / 2 2` | `-1` | Correctly detects that no exact sum exists |
| `5 3 / 1 1 1 1 1` | `1 3` | All-equal values and ordinary sliding-window movement |
| `5 3 / 0 1 0 2 0` | `2 4` | Zero-valued cars at both boundaries |
| `4 6 / 2 4 1 5` | `1 2` | Exact prefix and boundary handling |
| `100000` ones with `k = 100000` | `1 100000` | Maximum `n` and linear-time behavior |

## Edge Cases

### A single car

For

```
1 5
5
```

the right pointer visits the only car, producing `current_sum = 5`. Since this equals `k`, the interval `[0, 0]` becomes the best answer. After converting to one-based indexing, the program prints `1 1`.

The common mistake here is to initialize the best answer as though at least two cars must be selected. Nothing in the problem requires that, so a single car is a valid and often optimal interval.

### An already full car inside the answer

For

```
3 3
1 0 2
```

the window grows as `[1]`, then `[1, 0]`, then `[1, 0, 2]`. Its sum becomes exactly three. The zero-valued car is already full, but it lies between the two cars containing the informatics participants, so the endpoints are `1` and `3`.

The zero cannot simply be treated as an obstacle. Doing so would incorrectly conclude that no contiguous interval has the required sum.

### No possible exact sum

For

```
2 5
2 2
```

the total number of free seats in the entire train is four. Since every `a[i]` is nonnegative, no subarray can have a sum larger than the total sum, so reaching five is impossible. The right pointer eventually processes the entire array without producing `current_sum == 5`, and the program prints `-1`.

A careless implementation that searches for the smallest sum at least `k` could incorrectly accept the whole array. The requirement is equality, not `sum >= k`.

### Zero-valued boundaries

For

```
5 3
0 1 0 2 0
```

the first exact window is `[0, 1, 0, 2]`, whose sum is three. The algorithm then removes the leading zero without changing the sum, leaving `[1, 0, 2]`. The resulting answer is cars `2` through `4`.

The trailing zero is not included because the right pointer has not advanced to it when the candidate is evaluated. Including either zero boundary would produce a longer interval without adding any useful seats.
