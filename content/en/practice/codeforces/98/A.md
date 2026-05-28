---
title: "CF 98A - Help Victoria the Wise"
description: "We have six gems, each with one of six possible colors. The six gems must be placed onto the six faces of a cube. Two placements are considered identical if one can be rotated into the other. The input is simply a string of length six."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 98
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 78 (Div. 1 Only)"
rating: 1700
weight: 98
solve_time_s: 132
verified: true
draft: false
---

[CF 98A - Help Victoria the Wise](https://codeforces.com/problemset/problem/98/A)

**Rating:** 1700  
**Tags:** brute force, implementation  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have six gems, each with one of six possible colors. The six gems must be placed onto the six faces of a cube. Two placements are considered identical if one can be rotated into the other.

The input is simply a string of length six. Each character represents the color of one gem. Equal characters mean indistinguishable gems. For example, the input `RGBRGB` means there are two red gems, two green gems, and two blue gems.

We must count how many fundamentally different cube colorings can be formed. Rotations of the cube do not create new answers.

The size of the input is tiny. There are only six positions on the cube, so even a brute-force permutation approach is feasible. The largest number of raw arrangements is `6! = 720`, which is extremely small. The real challenge is handling rotational equivalence correctly.

The dangerous part of this problem is that cube rotations are easy to underestimate. A naive implementation might count two rotated cubes separately even though they represent the same decoration.

Consider the input:

```
RGBYOV
```

All colors are distinct. A careless solution might answer `720`, because there are `6!` permutations. That is wrong. Every physical cube has 24 rotational symmetries, so many permutations collapse into the same equivalence class. The correct answer is `720 / 24 = 30`.

Another easy mistake appears when duplicate colors exist.

For example:

```
RRGGGG
```

If we only divide by 24 mechanically, we get nonsense because repeated colors create overlapping configurations. We must compare actual cube states under rotation, not rely on combinatorial formulas.

One more subtle case is when all colors are identical:

```
YYYYYY
```

There is only one valid decoration. Every permutation and every rotation produce the same cube. A permutation-based solution without deduplication would massively overcount.

## Approaches

The most direct idea is brute force. We generate every permutation of the six gems, interpret each permutation as a coloring of the cube faces, then group together all permutations that are equivalent under cube rotations.

This works because the total search space is tiny. Even with all colors distinct, there are only 720 permutations. For each permutation we can test all 24 cube rotations. The total work stays comfortably below a few tens of thousands of operations.

The real question is how to represent rotations cleanly.

A cube has exactly 24 distinct orientations. If we number the faces from 0 to 5, every rotation becomes a permutation of these indices. Once we precompute those 24 permutations, two colorings are equivalent if one can be transformed into the other using any of these permutations.

The brute-force version could compare every permutation against every previously seen permutation using all 24 rotations. That still passes because the input is so small, but we can make it cleaner.

The key observation is that every equivalence class has a canonical representative. For any coloring, we generate all 24 rotated versions and choose the lexicographically smallest one. Every cube in the same rotational class maps to the same canonical form.

That turns the problem into simple set deduplication.

The brute-force works because the state space is tiny, but it becomes awkward when checking pairwise equivalence repeatedly. The canonical-form observation reduces the entire task to:

1. Generate all distinct permutations.
2. Normalize each permutation.
3. Count unique normalized states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pairwise comparison | O(720² × 24) | O(720) | Accepted |
| Canonical representation | O(720 × 24) | O(720) | Accepted |

## Algorithm Walkthrough

1. Number the six cube faces from 0 to 5.

We only need consistency. One common convention is:

- 0 = top
- 1 = bottom
- 2 = front
- 3 = back
- 4 = left
- 5 = right
2. Precompute all 24 cube rotations.

Each rotation is represented as a permutation of the six face indices. For example, one rotation might move the top face to the front, the front to the bottom, and so on.

The correctness of the whole solution depends on generating exactly the 24 physical cube orientations, no more and no fewer.
3. Generate every distinct permutation of the input colors.

Since equal colors are indistinguishable, we use a set to remove duplicate permutations automatically.
4. For each permutation, generate all 24 rotated versions.

Applying a rotation means rearranging the six face colors according to the rotation permutation.
5. Choose the lexicographically smallest rotated version.

This becomes the canonical form of the cube coloring.

Every rotationally equivalent coloring produces the same canonical form because they all generate the same set of 24 rotated states.
6. Insert the canonical form into a set.

Sets automatically remove duplicates.
7. Print the size of the set.

That count equals the number of distinct cube decorations.

### Why it works

Two cube colorings belong to the same answer class exactly when one can be rotated into the other. Our normalization process explicitly enumerates all possible rotations of a cube coloring and selects a unique representative, the lexicographically smallest rotated state.

If two colorings are rotationally equivalent, their sets of rotated states are identical, so they obtain the same canonical form.

If two colorings are not rotationally equivalent, their rotation sets never intersect, so their canonical forms differ.

The set of canonical forms therefore contains one element per equivalence class, which is exactly the required answer.

## Python Solution

```python
import sys
from itertools import permutations
from collections import deque

input = sys.stdin.readline

def compose(a, b):
    return tuple(a[b[i]] for i in range(6))

def solve():
    s = input().strip()

    # Face order:
    # 0 = top
    # 1 = bottom
    # 2 = front
    # 3 = back
    # 4 = left
    # 5 = right

    # Basic cube rotations
    rot_x = (2, 3, 1, 0, 4, 5)
    rot_y = (0, 1, 4, 5, 3, 2)
    rot_z = (4, 5, 2, 3, 1, 0)

    rotations = set()
    q = deque()

    identity = (0, 1, 2, 3, 4, 5)
    rotations.add(identity)
    q.append(identity)

    # Generate all 24 cube rotations
    while q:
        cur = q.popleft()

        for rot in (rot_x, rot_y, rot_z):
            nxt = compose(rot, cur)

            if nxt not in rotations:
                rotations.add(nxt)
                q.append(nxt)

    rotations = list(rotations)

    canonicals = set()

    for p in set(permutations(s)):
        best = None

        for rot in rotations:
            transformed = tuple(p[rot[i]] for i in range(6))

            if best is None or transformed < best:
                best = transformed

        canonicals.add(best)

    print(len(canonicals))

if __name__ == "__main__":
    solve()
```

The first important part is the cube rotation generation. Instead of hardcoding all 24 orientations manually, the solution starts from the identity orientation and repeatedly applies three basic rotations around the coordinate axes. Breadth-first expansion eventually discovers all 24 unique cube orientations.

The `compose` function combines two permutations. This is the core operation that lets us build complex rotations from simple ones.

The permutation generation step uses:

```
set(permutations(s))
```

This is essential. If the input contains repeated colors, ordinary `permutations` would produce many duplicates.

The canonicalization step is the heart of the algorithm. For every arrangement, we apply all 24 rotations and keep the smallest tuple lexicographically. Using tuples instead of strings makes comparisons straightforward and efficient.

A common implementation mistake is reversing the permutation direction accidentally. The expression:

```
tuple(p[rot[i]] for i in range(6))
```

means "the color now appearing at face `i` came from face `rot[i]`". Consistency matters more than the exact convention.

## Worked Examples

### Example 1

Input:

```
YYYYYY
```

All permutations are identical.

| Permutation | Canonical Form |
| --- | --- |
| YYYYYY | YYYYYY |

Final set size:

```
1
```

This example shows that duplicate colors collapse many permutations into a single configuration. Every rotation also remains identical.

### Example 2

Input:

```
RGBYOV
```

All colors are distinct.

Suppose one permutation is:

| Original Faces | State |
| --- | --- |
| 0 1 2 3 4 5 | RGBYOV |

Some rotations produce:

| Rotation | Result |
| --- | --- |
| Identity | RGBYOV |
| Rotate X | BYGRVO |
| Rotate Y | RGOVYB |
| Rotate Z | OVRGBY |

Among all 24 rotated states, the lexicographically smallest one becomes the canonical form.

After processing all 720 permutations, exactly 30 distinct canonical forms remain.

| Quantity | Value |
| --- | --- |
| Raw permutations | 720 |
| Cube rotations | 24 |
| Distinct colorings | 30 |

This example demonstrates rotational collapsing. Many seemingly different face assignments actually represent the same physical cube.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(720 × 24) | At most 720 distinct permutations, each checked under 24 rotations |
| Space | O(720) | Storage for canonical states |

The total work is tiny. Even in the worst case with six distinct colors, the program performs only a few thousand operations. This easily fits within the 1 second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import permutations
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def compose(a, b):
        return tuple(a[b[i]] for i in range(6))

    s = input().strip()

    rot_x = (2, 3, 1, 0, 4, 5)
    rot_y = (0, 1, 4, 5, 3, 2)
    rot_z = (4, 5, 2, 3, 1, 0)

    rotations = set()
    q = deque()

    identity = (0, 1, 2, 3, 4, 5)

    rotations.add(identity)
    q.append(identity)

    while q:
        cur = q.popleft()

        for rot in (rot_x, rot_y, rot_z):
            nxt = compose(rot, cur)

            if nxt not in rotations:
                rotations.add(nxt)
                q.append(nxt)

    canonicals = set()

    for p in set(permutations(s)):
        best = None

        for rot in rotations:
            transformed = tuple(p[rot[i]] for i in range(6))

            if best is None or transformed < best:
                best = transformed

        canonicals.add(best)

    return str(len(canonicals)) + "\n"

# provided sample
assert run("YYYYYY\n") == "1\n", "sample 1"

# all distinct colors
assert run("ROYGBV\n") == "30\n", "all distinct"

# two groups of three
assert run("RRRGGG\n") == "2\n", "three and three"

# one unique gem
assert run("RBBBBB\n") == "1\n", "single special face"

# symmetric pair structure
assert run("RRGGBB\n") == "6\n", "pair symmetry"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `YYYYYY` | `1` | Fully identical configuration |
| `ROYGBV` | `30` | Maximum number of distinct states |
| `RRRGGG` | `2` | Nontrivial rotational equivalence |
| `RBBBBB` | `1` | Single unique face can always rotate anywhere |
| `RRGGBB` | `6` | Multiple repeated colors with partial symmetry |

## Edge Cases

Consider the fully symmetric case:

```
YYYYYY
```

There is only one distinct permutation. Every rotation also produces the same arrangement:

```
YYYYYY
```

The canonical set receives exactly one element, so the algorithm outputs `1`.

Now consider:

```
RBBBBB
```

At first glance, there seem to be six possibilities because the red gem could occupy any face. Rotations destroy this distinction. Any face can be rotated into any other face on a cube.

During canonicalization, all six raw permutations map to the same normalized state. The algorithm correctly outputs `1`.

Finally, consider:

```
RRRGGG
```

A naive combinatorial approach might assume all arrangements are equivalent, but that is false. There are actually two fundamentally different structures:

1. Three red faces meeting at a corner.
2. Three red faces surrounding one face cyclically.

The canonicalization process distinguishes these automatically because no cube rotation can transform one structure into the other. The final answer becomes `2`.
