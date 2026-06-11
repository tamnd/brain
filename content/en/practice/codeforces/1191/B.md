---
title: "CF 1191B - Tokitsukaze and Mahjong"
description: "We are given exactly three mahjong tiles. Each tile consists of a number from 1 to 9 and a suit, where the suit is one of m, p, or s. A winning hand in this simplified game only requires the existence of a single mentsu."
date: "2026-06-12T00:30:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1191
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 573 (Div. 2)"
rating: 1200
weight: 1191
solve_time_s: 162
verified: true
draft: false
---

[CF 1191B - Tokitsukaze and Mahjong](https://codeforces.com/problemset/problem/1191/B)

**Rating:** 1200  
**Tags:** brute force, implementation  
**Solve time:** 2m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given exactly three mahjong tiles. Each tile consists of a number from 1 to 9 and a suit, where the suit is one of `m`, `p`, or `s`.

A winning hand in this simplified game only requires the existence of a single mentsu. A mentsu can be either a triplet of identical tiles or a sequence of three consecutive numbers in the same suit.

We may draw any additional tiles we want, and there is no limit on how many copies of a tile exist. The task is to find the minimum number of extra tiles needed so that among the tiles we hold, there exists at least one valid triplet or sequence.

The input size is unusually small. We always receive exactly three tiles. There are only 27 distinct tile types in the game, so even fairly brute-force approaches are feasible. The challenge is not performance but correctly identifying how close the current hand already is to forming a valid meld.

Several edge cases can easily lead to incorrect implementations.

Consider:

```
1m 1m 2m
```

The correct answer is:

```
1
```

Drawing another `1m` completes a triplet. A solution that only checks sequences would incorrectly return 2.

Consider:

```
1m 2m 4m
```

The correct answer is:

```
1
```

Drawing `3m` creates the sequence `1m 2m 3m`. A careless implementation that only looks for adjacent numbers already present might miss this.

Consider:

```
1m 3m 5m
```

The correct answer is:

```
2
```

No pair of tiles is close enough to complete a sequence with a single draw. Any valid meld requires at least two additional tiles.

Consider:

```
9m 9m 9m
```

The correct answer is:

```
0
```

The hand already contains a triplet, so no draws are needed.

The key observation is that the answer can only be 0, 1, or 2. Starting with three tiles, if we choose any one tile, two additional copies always create a triplet. Thus two draws are always sufficient.

## Approaches

A brute-force approach would try all possible tiles that could be drawn. Since there are 27 tile types, we could test every possible one-tile extension and every possible two-tile extension, then check whether a meld exists. The total work is small:

- 27 possibilities for one draw.
- $27^2 = 729$ possibilities for two draws.

For each candidate hand we inspect only a handful of tiles. Even this approach easily fits within the limits.

The problem, however, has a much simpler structure. We never need to construct the actual future hand. We only need to know how close the current hand already is to some meld.

A meld consists of three tiles. Since we already hold three tiles, every potential meld must use one, two, or all three of them.

If all three current tiles already form a meld, the answer is 0.

If two current tiles can become part of a meld after adding one tile, the answer is 1.

Otherwise the answer is 2.

This reduces the task to measuring the largest number of tiles already contributing toward some meld.

For triplets, identical tiles contribute together. Two equal tiles need one more copy. Three equal tiles need none.

For sequences, only tiles of the same suit matter. Two tiles of the same suit can be:

- consecutive, such as `4m` and `5m`, needing one endpoint tile;
- separated by one gap, such as `4m` and `6m`, needing the middle tile;
- identical, which is not useful for sequences but may help triplets.

We evaluate every pair of tiles and determine how many tiles of a meld are already present. The best value found determines the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(27²) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three tiles.
2. Initialize the answer as 2.

Two draws are always sufficient because any tile can be turned into a triplet by drawing two more copies.
3. Check every tile individually.

A single tile already contributes one tile toward some future meld, so the answer cannot exceed 2.
4. Check every pair of tiles.

If the two tiles are identical, they already form two-thirds of a triplet. Update the answer to at most 1.
5. For every pair with the same suit, compare their numbers.

Let the difference between the numbers be `d`.
6. If `d = 0`, the pair contributes two tiles toward a triplet.

Update the answer to at most 1.
7. If `d = 1` or `d = 2`, the pair can become a sequence after adding one suitable tile.

Examples:

- `3m, 4m` needs `2m` or `5m`.
- `3m, 5m` needs `4m`.

Update the answer to at most 1.
8. Check whether all three tiles already form a triplet.

If so, the answer is 0.
9. Check whether all three tiles form a sequence in the same suit.

Sort the numbers and verify they are consecutive.

If so, the answer is 0.
10. Output the answer.

### Why it works

Every meld contains exactly three tiles. The hand already contains three tiles, so the only thing that matters is how many tiles of some meld are already present.

If all three tiles of a meld are present, no draw is required.

If two tiles of a meld are present, one draw completes it.

If no meld contains more than one current tile, at least two draws are necessary. Since two draws are always sufficient by completing a triplet from any existing tile, the answer is exactly two.

The algorithm explicitly checks every way in which two tiles can belong to the same triplet or sequence, and every way all three tiles can already form a meld. Thus it always returns the minimum number of required draws.

## Python Solution

```python
import sys
input = sys.stdin.readline

tiles = input().split()

ans = 2

for i in range(3):
    for j in range(i + 1, 3):
        a, sa = int(tiles[i][0]), tiles[i][1]
        b, sb = int(tiles[j][0]), tiles[j][1]

        if tiles[i] == tiles[j]:
            ans = min(ans, 1)

        if sa == sb:
            d = abs(a - b)
            if d <= 2:
                ans = min(ans, 1)

# triplet
if tiles[0] == tiles[1] == tiles[2]:
    ans = 0

# sequence
nums = []
suit = tiles[0][1]

same_suit = True
for t in tiles:
    if t[1] != suit:
        same_suit = False
        break
    nums.append(int(t[0]))

if same_suit:
    nums.sort()
    if nums[0] + 1 == nums[1] and nums[1] + 1 == nums[2]:
        ans = 0

print(ans)
```

The solution starts with the observation that the answer never exceeds 2. We initialize `ans = 2` and then look for evidence that only one draw or zero draws are needed.

The nested loop examines every pair of tiles. Since there are only three tiles, exactly three pairs exist. If two tiles are identical, they are already two-thirds of a triplet. If two tiles have the same suit and their numbers differ by at most two, a single tile can complete a sequence.

After processing pairs, we check whether the hand is already complete. A triplet is easy to detect because all three tile strings must be equal.

For a sequence, all three suits must match. We then sort the numbers and verify that they form consecutive values. Sorting avoids dependence on input order.

A common mistake is forgetting the case where the gap is exactly two, such as `3m` and `5m`. One tile, namely `4m`, completes the sequence. Checking `d <= 2` correctly handles both adjacent and one-gap pairs.

## Worked Examples

### Example 1

Input:

```
1s 2s 3s
```

| Step | Pair/State | Answer |
| --- | --- | --- |
| Initial | start | 2 |
| Pair (1s,2s) | diff = 1 | 1 |
| Pair (1s,3s) | diff = 2 | 1 |
| Pair (2s,3s) | diff = 1 | 1 |
| Sequence check | already 1,2,3 same suit | 0 |

Output:

```
0
```

This example shows that pair checks may indicate one draw is enough, but the final three-tile check can reduce the answer to zero.

### Example 2

Input:

```
7m 7m 7m
```

| Step | Pair/State | Answer |
| --- | --- | --- |
| Initial | start | 2 |
| Pair (7m,7m) | identical | 1 |
| Pair (7m,7m) | identical | 1 |
| Pair (7m,7m) | identical | 1 |
| Triplet check | all equal | 0 |

Output:

```
0
```

This example demonstrates the triplet condition
