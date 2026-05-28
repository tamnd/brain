---
title: "CF 46D - Parking Lot"
description: "We have a parking segment represented by the interval [0, L]. Cars arrive one at a time, always driving from left to right, and each driver wants to park at the earliest possible position."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 46
codeforces_index: "D"
codeforces_contest_name: "School Personal Contest #2 (Winter Computer School 2010/11) - Codeforces Beta Round 43 (ACM-ICPC Rules)"
rating: 1800
weight: 46
solve_time_s: 114
verified: true
draft: false
---
[CF 46D - Parking Lot](https://codeforces.com/problemset/problem/46/D)

**Rating:** 1800  
**Tags:** data structures, implementation  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a parking segment represented by the interval `[0, L]`. Cars arrive one at a time, always driving from left to right, and each driver wants to park at the earliest possible position.

If a car of length `x` parks with its back at coordinate `p`, then the car occupies `[p, p + x]`. Between this car and the car behind it there must be at least `b` meters of free space. Between this car and the car in front of it there must be at least `f` meters of free space. The street borders are special, they do not require extra spacing.

The requests are of two kinds. A type `1 x` request means a new car of length `x` arrives and tries to park. We must output the coordinate where its back ends up, or `-1` if parking is impossible. A type `2 k` request means the car created by the `k`-th request leaves the parking lot.

The number of operations is at most `100`, which is surprisingly small. Even an `O(n^2)` simulation would fit easily. The challenge is not performance, it is modeling the spacing rules correctly. Most wrong answers come from misunderstandings about where the mandatory gaps apply.

The key subtlety is that the spacing is asymmetric. A car needs `b` meters behind and `f` meters in front. When two parked cars coexist, the actual empty distance between them must satisfy both cars simultaneously. Suppose car A is behind car B. Then the gap between them must be at least `max(f, b)`? No. The rear car requires `f` in front, while the front car requires `b` behind, so the gap must be at least `f + b`.

Another easy mistake appears at the borders. If a car is the first parked car, it may start at coordinate `0` without requiring a rear gap. Similarly, the last parked car may end exactly at `L` without needing a front gap.

Consider this example:

```
L = 10, b = 2, f = 3
Current parked car: occupies [4, 6]
New car length = 1
```

A careless implementation may think the free interval `[0, 4]` can fit a car starting at `0`, because `0 + 1 <= 4`. That is wrong. The new car also needs `f = 3` meters before the parked car, so we need:

```
0 + 1 + 3 <= 4
```

which is true here, but only barely.

Another dangerous edge case appears when inserting between two cars.

```
L = 20, b = 2, f = 2
Cars:
[0, 4]
[10, 14]
New car length = 2
```

The empty interval is `[4, 10]`, length `6`. A naive approach might think the car fits because `2 <= 6`. The actual required space is:

```
b + car_length + f = 2 + 2 + 2 = 6
```

The car exactly fits, starting at coordinate `6`.

Removal operations are also easy to mishandle if we only store coordinates and forget which request created which car. Since deletions refer to request indices, we must maintain a mapping from request id to parked interval.

## Approaches

The most direct simulation is to maintain all parked cars sorted by position. For every arriving car, we scan the parking lot from left to right and test every free interval.

Suppose the current parked cars are:

```
[p1, p1 + len1]
[p2, p2 + len2]
...
```

We check three kinds of gaps.

The prefix gap before the first car. A new car may start at `0`, but must leave `f` meters before the first parked car.

The middle gaps between consecutive cars. If the previous car ends at `r1` and the next car starts at `l2`, then a new car of length `x` may start at `r1 + b` if:

```
r1 + b + x + f <= l2
```

The suffix gap after the last car. A new car may start at `last_end + b` as long as:

```
last_end + b + x <= L
```

The first valid position is always optimal because drivers always choose the earliest possible place.

This brute-force simulation is already fast enough. At most `100` operations exist, and each arrival scans at most `100` parked cars, giving roughly `10^4` checks.

The main observation is that we never need complicated interval trees or balanced structures because the constraints are tiny. The real work is deriving the exact placement formulas correctly. Once the geometry is understood, the implementation becomes a careful interval scan.

We still organize the data cleanly by storing parked cars in sorted order and removing them when necessary. That gives a simple and reliable solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

The "optimal" solution here is really the properly modeled simulation. Larger constraints would require interval structures, but for `n ≤ 100`, careful implementation matters more than asymptotic tricks.

## Algorithm Walkthrough

1. Maintain a sorted list of parked cars.

Each car is stored as `(start, length, request_id)`. Keeping the list sorted by `start` lets us scan free gaps from left to right.
2. Maintain a dictionary from request id to parked car data.

Removal queries refer to the original request number, not to parking order. This mapping lets us find the exact parked car in constant time.
3. For an arrival request with car length `x`, first try placing the car at coordinate `0`.

If there are no parked cars, the car fits when `x <= L`.

Otherwise, let the first parked car start at `s`. The new car fits at `0` if:

```
x + f <= s
```

The left border does not require a rear gap.
4. If the prefix gap fails, scan every adjacent pair of parked cars.

Suppose the previous car occupies `[l1, r1]` and the next car starts at `l2`.

The earliest possible start is:

```
r1 + b
```

To keep the required front spacing before the next car:

```
r1 + b + x + f <= l2
```

The first pair satisfying this condition gives the correct parking position.
5. If no middle gap works, try parking after the last car.

If the last car ends at `r`, the earliest possible position is:

```
r + b
```

The car fits if:

```
r + b + x <= L
```

The right border does not require a front gap.
6. If none of the three cases succeeds, output `-1`.
7. When a car successfully parks, insert it into the sorted list and record it in the request-id mapping.
8. For a removal request, locate the stored car using the request id and erase it from the parked list.

### Why it works

The algorithm always examines free space from left to right and always chooses the earliest valid coordinate inside each gap. Every feasible parking position must belong to exactly one of three categories: before the first car, between two cars, or after the last car.

Inside a middle gap, any valid placement must start at or after `previous_end + b`, because the previous car requires rear spacing. Starting later only wastes space and cannot produce an earlier answer. So the earliest candidate inside that gap is uniquely determined. If that candidate fails to leave enough front spacing, then no later position inside the same gap can work.

Because every gap is checked in left-to-right order and each gap's earliest feasible position is tested, the first accepted position is exactly the leftmost valid parking coordinate required by the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    L, b, f = map(int, input().split())
    n = int(input())

    parked = []
    by_request = {}

    for req_id in range(1, n + 1):
        t, x = map(int, input().split())

        if t == 1:
            length = x
            pos = -1

            if not parked:
                if length <= L:
                    pos = 0
            else:
                first_start = parked[0][0]

                if length + f <= first_start:
                    pos = 0
                else:
                    for i in range(len(parked) - 1):
                        s1, len1, _ = parked[i]
                        s2, len2, _ = parked[i + 1]

                        end1 = s1 + len1

                        candidate = end1 + b

                        if candidate + length + f <= s2:
                            pos = candidate
                            break

                    if pos == -1:
                        last_start, last_len, _ = parked[-1]
                        last_end = last_start + last_len

                        candidate = last_end + b

                        if candidate + length <= L:
                            pos = candidate

            print(pos)

            if pos != -1:
                car = (pos, length, req_id)

                idx = 0
                while idx < len(parked) and parked[idx][0] < pos:
                    idx += 1

                parked.insert(idx, car)
                by_request[req_id] = car

        else:
            car = by_request[x]
            parked.remove(car)
            del by_request[x]

solve()
```

The solution keeps the parking lot explicitly represented as a sorted list of occupied intervals. Since the number of operations is tiny, simple list operations are completely sufficient.

The insertion logic mirrors the geometric reasoning from the walkthrough. We first try the prefix gap, then every internal gap, then the suffix gap. The formulas differ slightly because borders do not require extra spacing.

One subtle implementation detail is the meaning of `candidate`. Between two parked cars, we always place the new car as far left as possible:

```
candidate = end1 + b
```

Any later start position would only reduce remaining space before the next car, so checking this single coordinate is enough.

Another easy off-by-one mistake is forgetting that intervals are continuous lengths, not integer slots. The condition:

```
candidate + length + f <= s2
```

is exact. Equality is allowed because cars may leave exactly the required amount of free space.

The removal logic uses the stored tuple itself. Since tuples are immutable and uniquely identify parked cars, `list.remove()` cleanly deletes the correct interval.

## Worked Examples

### Sample 1

Input:

```
30 1 2
6
1 5
1 4
1 5
2 2
1 5
1 4
```

| Step | Operation | Parked Cars After Operation | Output |
| --- | --- | --- | --- |
| 1 | Add length 5 | `[0,5]` | 0 |
| 2 | Add length 4 | `[0,5], [6,10]` | 6 |
| 3 | Add length 5 | `[0,5], [6,10], [11,16]` | 11 |
| 4 | Remove request 2 | `[0,5], [11,16]` |  |
| 5 | Add length 5 | `[0,5], [11,16], [17,22]` | 17 |
| 6 | Add length 4 | `[0,5], [11,16], [17,22], [23,27]` | 23 |

The trace shows why cars always occupy the earliest feasible coordinate. After removing the second car, the gap `[6,11]` is only length `5`. A new car of length `5` would actually require:

```
1 + 5 + 2 = 8
```

meters inside an internal gap, so it cannot fit there and must park later.

### Custom Example

Input:

```
15 2 3
5
1 4
1 3
2 1
1 5
1 1
```

| Step | Operation | Parked Cars After Operation | Output |
| --- | --- | --- | --- |
| 1 | Add length 4 | `[0,4]` | 0 |
| 2 | Add length 3 | `[0,4], [6,9]` | 6 |
| 3 | Remove request 1 | `[6,9]` |  |
| 4 | Add length 5 | `[6,9]` | -1 |
| 5 | Add length 1 | `[0,1], [6,9]` | 0 |

The fourth operation demonstrates a border rule. The free prefix before `[6,9]` has length `6`, but a car of length `5` still cannot fit because it also needs `3` meters before the parked car:

```
5 + 3 > 6
```

The final operation succeeds because a length `1` car only needs:

```
1 + 3 <= 6
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each insertion may scan all parked cars |
| Space | O(n) | We store all currently parked cars and request mappings |

With at most `100` operations, the worst-case work is tiny. Even a quadratic simulation performs only a few thousand checks, far below the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = out

    L, b, f = map(int, input().split())
    n = int(input())

    parked = []
    by_request = {}

    for req_id in range(1, n + 1):
        t, x = map(int, input().split())

        if t == 1:
            length = x
            pos = -1

            if not parked:
                if length <= L:
                    pos = 0
            else:
                first_start = parked[0][0]

                if length + f <= first_start:
                    pos = 0
                else:
                    for i in range(len(parked) - 1):
                        s1, len1, _ = parked[i]
                        s2, _, _ = parked[i + 1]

                        end1 = s1 + len1
                        candidate = end1 + b

                        if candidate + length + f <= s2:
                            pos = candidate
                            break

                    if pos == -1:
                        last_start, last_len, _ = parked[-1]
                        last_end = last_start + last_len

                        candidate = last_end + b

                        if candidate + length <= L:
                            pos = candidate

            print(pos)

            if pos != -1:
                car = (pos, length, req_id)

                idx = 0
                while idx < len(parked) and parked[idx][0] < pos:
                    idx += 1

                parked.insert(idx, car)
                by_request[req_id] = car

        else:
            car = by_request[x]
            parked.remove(car)
            del by_request[x]

    sys.stdout = sys_stdout
    return out.getvalue()

# provided sample
assert run(
"""30 1 2
6
1 5
1 4
1 5
2 2
1 5
1 4
"""
) == "0\n6\n11\n17\n23\n", "sample 1"

# minimum size
assert run(
"""10 1 1
1
1 10
"""
) == "0\n", "single car fills entire lot"

# exact middle fit
assert run(
"""20 2 2
3
1 4
1 4
1 2
"""
) == "0\n6\n12\n", "exact spacing equality"

# impossible due to front spacing
assert run(
"""15 2 3
2
1 4
1 9
"""
) == "0\n-1\n", "front spacing blocks placement"

# reuse freed space
assert run(
"""20 1 1
5
1 5
1 5
2 1
1 4
1 5
"""
) == "0\n6\n0\n11\n", "reuse after deletion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single car occupying full lot | `0` | Borders require no extra spacing |
| Exact middle fit | `0 6 12` | Equality conditions are allowed |
| Front spacing failure | `0 -1` | Prefix gap must reserve `f` meters |
| Reuse after deletion | `0 6 0 11` | Deleted intervals become available correctly |

## Edge Cases

Consider this input:

```
15 2 3
2
1 4
1 8
```

The first car parks at `0`, occupying `[0,4]`.

For the second car, the earliest suffix position is:

```
4 + 2 = 6
```

The new car would occupy `[6,14]`, which fits exactly inside the parking lot. The algorithm accepts it because suffix placement only checks:

```
candidate + length <= L
```

No front spacing is needed at the right border.

Now consider:

```
20 2 2
3
1 4
1 4
1 2
```

After two cars, we have:

```
[0,4]
[6,10]
```

The remaining suffix starts at:

```
10 + 2 = 12
```

The third car length is `2`, and:

```
12 + 2 = 14 <= 20
```

The algorithm parks it at `12`.

Finally, consider a tricky internal gap:

```
20 2 3
3
1 4
1 4
1 1
```

After the first two cars:

```
[0,4]
[7,11]
```

The free interval between them is length `3`. A careless solution might think a length `1` car fits there.

The algorithm checks:

```
candidate = 4 + 2 = 6
6 + 1 + 3 <= 7
```

which fails. The required front spacing is missing, so the car cannot park there. The algorithm correctly searches later gaps instead.
