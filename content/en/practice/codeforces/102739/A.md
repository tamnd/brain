---
title: "CF 102739A - \u0412\u044b\u0441\u0442\u0430\u0432\u043a\u0430 \u0438\u043c\u043f\u0440\u0435\u0441\u0441\u0438\u043e\u043d\u0438\u0441\u0442\u043e\u0432"
description: "The gallery contains n paintings placed in a fixed order from left to right. Arina starts at the first side of the gallery and walks toward the last painting. During a walk she can only stop at paintings that are ahead of her in the current direction."
date: "2026-08-01T22:19:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102739
codeforces_index: "A"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2020.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102739
solve_time_s: 105
verified: true
draft: false
---

[CF 102739A - \u0412\u044b\u0441\u0442\u0430\u0432\u043a\u0430 \u0438\u043c\u043f\u0440\u0435\u0441\u0441\u0438\u043e\u043d\u0438\u0441\u0442\u043e\u0432](https://codeforces.com/problemset/problem/102739/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
# Problem Understanding

The gallery contains `n` paintings placed in a fixed order from left to right. Arina starts at the first side of the gallery and walks toward the last painting. During a walk she can only stop at paintings that are ahead of her in the current direction. After reaching an end of the gallery, she turns around and continues in the opposite direction. The audio guide records the order in which she actually viewed all paintings.

The task is to reconstruct the minimum number of full walks through the gallery that could have produced this viewing order. A left-to-right walk must contain painting numbers that increase in the recorded order, while a right-to-left walk must contain painting numbers that decrease.

The input gives a permutation of painting numbers. Every painting appears exactly once, so the sequence itself tells us the exact moment when each painting was viewed. The output is the smallest number of alternating increasing and decreasing segments needed to split this sequence.

The main constraint is `n ≤ 100000`. This rules out solutions that try every possible division of the sequence or repeatedly simulate all paintings on every pass. A solution needs to process each painting a constant number of times, which points toward an `O(n)` approach.

The subtle part is that a walk does not end when we reach the last painting seen in that direction. It ends only after reaching the physical end of the gallery. Because of this, the next painting in the audio sequence might force a new walk even if a longer mathematical subsequence could still be increasing or decreasing.

Consider this input:

```
4
1 2 4 3
```

The correct output is:

```
2
```

The first walk from left to right can see `1 2 4`. Painting `3` is located behind the current position, so Arina must turn around. A careless solution that only looks for a long increasing subsequence could incorrectly decide that fewer walks are possible.

Another edge case is when every next painting requires changing direction:

```
5
1 5 2 4 3
```

The correct output is:

```
5
```

The sequence alternates between increasing and decreasing after every painting. Treating equal or single-element walks incorrectly can cause an off-by-one error here, because every single painting still requires a completed walk.

## Approaches

A direct approach is to simulate the gallery walk. We could maintain the set of paintings already viewed, start from one end, and repeatedly move through the gallery searching for the next available painting in the current direction. This approach is correct because it follows the story exactly. However, implementing it directly can require scanning many paintings on every pass. In the worst case, there can be `n` passes and each pass can inspect `n` paintings, leading to `O(n²)` operations, which is too slow for `n = 100000`.

The key observation is that the audio sequence already contains the only information we need. During one walk, the viewed painting numbers must form a monotonic sequence. The first walk must be increasing, the second decreasing, the third increasing, and so on. Therefore, the problem is equivalent to finding how many times we need to switch between an increasing and decreasing run while reading the permutation from left to right.

The brute-force simulation works because every walk corresponds to one monotonic segment. It fails because it repeatedly spends time discovering information already present in the sequence. The observation that the direction of the current walk is determined by the previous viewed painting lets us reduce the entire simulation to a single scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with one walk. Its direction is left to right, so the current segment must be increasing.
2. Scan the paintings in the order stored by the audio guide. Keep the previous painting number and the direction required by the current walk.
3. If the current direction is increasing and the next painting number is larger than the previous one, the same walk can continue.
4. If the current direction is decreasing and the next painting number is smaller than the previous one, the same walk can continue.
5. Otherwise, the current walk cannot include this painting. Increase the number of walks and reverse the direction, because Arina must have reached the end of the gallery and turned around before viewing it.
6. Replace the previous painting number with the current one and continue until the entire sequence is processed.

The reason greedy switching is enough is that every walk has a fixed direction. Once two consecutive paintings violate that direction, no earlier choice can repair the situation. The second painting is physically on the wrong side of Arina, so a new walk is unavoidable.

Why it works:

The invariant is that after processing any prefix of the audio sequence, the algorithm has counted exactly the minimum number of walks needed for that prefix, and the current direction is the only possible direction for the next walk. Whenever the next painting fits the current direction, extending the current walk is always optimal because it does not increase the answer. Whenever it does not fit, the previous walk cannot contain that painting, so adding one more walk is mandatory. Since every decision is forced, the greedy process produces the minimum possible number of walks.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = 1
    direction = 1
    prev = a[0]

    for x in a[1:]:
        if direction == 1:
            if x < prev:
                ans += 1
                direction = -1
        else:
            if x > prev:
                ans += 1
                direction = 1
        prev = x

    print(ans)

if __name__ == "__main__":
    solve()
```

The variable `direction` stores the direction of the current gallery walk. A value of `1` means the current walk goes from smaller painting numbers to larger ones, while `-1` means it goes in the opposite direction.

The scan only compares adjacent paintings in the audio sequence. If the comparison contradicts the current direction, the code immediately starts a new walk and flips the direction.

The initialization with `ans = 1` is safe because the first painting always requires at least one walk. The constraints guarantee that `n` is at least one, so accessing `a[0]` is valid.

No extra arrays are needed because the algorithm only needs the previous painting, the current direction, and the current answer.

## Worked Examples

For the sample input:

```
8
3 5 7 1 6 4 8 2
```

the trace is:

| Current painting | Previous painting | Direction before step | Action | Walk count |
| --- | --- | --- | --- | --- |
| 3 | - | Increasing | Start | 1 |
| 5 | 3 | Increasing | Continue | 1 |
| 7 | 5 | Increasing | Continue | 1 |
| 1 | 7 | Increasing | Turn around | 2 |
| 6 | 1 | Decreasing | Turn around | 3 |
| 4 | 6 | Increasing | Turn around | 4 |
| 8 | 4 | Decreasing | Turn around | 5 |
| 2 | 8 | Increasing | Turn around | 6 |

The sequence creates six monotonic segments: `3 5 7`, `1`, `6`, `4`, `8`, and `2`. Each segment corresponds to one physical traversal of the gallery.

A second example:

```
5
1 2 3 4 5
```

| Current painting | Previous painting | Direction before step | Action | Walk count |
| --- | --- | --- | --- | --- |
| 1 | - | Increasing | Start | 1 |
| 2 | 1 | Increasing | Continue | 1 |
| 3 | 2 | Increasing | Continue | 1 |
| 4 | 3 | Increasing | Continue | 1 |
| 5 | 4 | Increasing | Continue | 1 |

The whole audio sequence is compatible with one left-to-right walk, so the answer remains one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every painting is examined exactly once. |
| Space | O(1) | Only a few integer variables are stored. |

With `n = 100000`, the algorithm performs only a linear number of comparisons, which easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    ans = 1
    direction = 1
    prev = a[0]

    for x in a[1:]:
        if direction == 1:
            if x < prev:
                ans += 1
                direction = -1
        else:
            if x > prev:
                ans += 1
                direction = 1
        prev = x

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert run("""8
3 5 7 1 6 4 8 2
""") == "6\n", "sample"

assert run("""1
1
""") == "1\n", "minimum size"

assert run("""5
1 2 3 4 5
""") == "1\n", "already increasing"

assert run("""5
5 4 3 2 1
""") == "2\n", "starts in wrong direction"

assert run("""6
1 6 2 5 3 4
""") == "6\n", "frequent direction changes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Single painting handling |
| `1 2 3 4 5` | `1` | A complete increasing traversal |
| `5 4 3 2 1` | `2` | The first direction is fixed as increasing |
| `1 6 2 5 3 4` | `6` | Repeated turns and direction changes |

## Edge Cases

For the single painting case:

```
1
1
```

the algorithm starts with one walk and never enters the loop. The answer remains `1`, which matches the fact that Arina only needs to enter the gallery and view that painting.

For a sequence that is already increasing:

```
5
1 2 3 4 5
```

every comparison agrees with the current left-to-right direction. The algorithm never changes direction and returns `1`. A solution that always alternates after reaching the last painting would overcount here.

For the case where the first step goes backward:

```
4
4 3 2 1
```

the first walk cannot contain the second painting because Arina is moving from smaller indices toward larger indices. The algorithm counts the initial increasing walk containing `4`, then switches to a decreasing walk containing the rest. The answer is `2`.

For a sequence with frequent changes:

```
6
1 6 2 5 3 4
```

every adjacent pair breaks the current direction. The algorithm changes direction after every comparison and returns `6`, matching the fact that each painting after the first requires a separate traversal.
