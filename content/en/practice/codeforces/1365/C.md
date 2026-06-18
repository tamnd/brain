---
problem: 1365C
contest_id: 1365
problem_index: C
name: "Rotation Matching"
contest_name: "Codeforces Round 648 (Div. 2)"
rating: 1400
tags: ["constructive algorithms", "data structures", "greedy", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 128
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e4979-4b48-83ec-8352-cdd9514f063c
---

# CF 1365C - Rotation Matching

**Rating:** 1400  
**Tags:** constructive algorithms, data structures, greedy, implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 8s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e4979-4b48-83ec-8352-cdd9514f063c  

---

## Solution

## Problem Understanding

We are given two permutations of the same set of numbers from 1 to n. Think of them as two different circular arrangements of the same labeled tiles. We are allowed to rotate each circle independently any number of times, and after doing so we align them in a fixed position. A position contributes to the answer if the same value appears in both arrays at that position.

So the real question is: after choosing two cyclic shifts, how many indices i can we make satisfy a[i] == b[i]?

Since both arrays contain exactly the same values, every value x has a fixed position in a and a fixed position in b. A rotation of an array simply shifts all these positions uniformly, so the relative ordering inside each permutation stays unchanged, only the global offset changes.

The constraint n up to 2 × 10^5 forces any quadratic comparison over all shifts to be impossible. Trying all n shifts for one array against n shifts for the other already gives O(n^2), which is too slow. Even O(n log n) or O(n sqrt n) approaches are acceptable, but we should expect a linear or near-linear transformation based on positions.

A subtle edge case appears when the permutations are identical up to rotation, in which case we can align all positions and get n matches. At the other extreme, there are cases where every alignment yields only one match, for example:

a = [1,2,3,4], b = [2,3,1,4]. No rotation can align more than two positions simultaneously, since the cyclic structure conflicts.

Another hidden detail is that rotating both arrays is equivalent to fixing one array and rotating the other in the opposite direction. This symmetry is essential, because it reduces the problem from two degrees of freedom to one.

## Approaches

A brute-force idea is straightforward. We fix a rotation of a, then try every rotation of b, compute how many indices match, and take the maximum. Each comparison costs O(n), and there are O(n^2) rotation pairs, leading to O(n^3) time if done naively or O(n^2) if we precompute comparisons carefully. Either way, it is too large for n = 2 × 10^5.

The key observation is that the value, not the position, drives the alignment. Each value x appears at some position pos_a[x] in a and pos_b[x] in b. If we rotate b so that b's position of x lands on a's position of x, then x contributes one match. For a fixed rotation, the number of matches is exactly the number of values whose required shift agrees.

So every value induces a “required rotation offset” between a and b. If we compute this offset for each x, the best alignment is simply the most frequent offset. This reduces the problem to counting frequencies over n computed differences.

This turns the problem from trying all alignments to grouping values by how much rotation they require.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) or O(n^2) | O(1)-O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the position of each value in the first permutation. For every value x, store where it occurs in a.
2. Compute the position of each value in the second permutation similarly. This gives us fast lookup for where each value needs to land.
3. For each value x, compute the rotation shift required to align b[x] with a[x]. If pos_a[x] is i and pos_b[x] is j, then shifting b by (i - j) modulo n aligns x correctly. This converts the problem into identifying which shift value is most common.
4. Count how many values produce each shift. We maintain a frequency array or hashmap indexed by the shift value modulo n.
5. The answer is the maximum frequency among all shifts.

Why this works is that each shift defines a global alignment between arrays. A value contributes to a shift only if that shift maps its position in b directly onto its position in a. Therefore, any valid rotation corresponds to one of these shift buckets, and all matches under that rotation are exactly the values falling into that bucket.

The invariant is that for any chosen rotation, the matched values are precisely those whose relative displacement between a and b equals that rotation. Since every value contributes independently to exactly one displacement, counting frequencies over all values captures all possible alignments exhaustively.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

pos_a = [0] * (n + 1)
pos_b = [0] * (n + 1)

for i, x in enumerate(a):
    pos_a[x] = i

for i, x in enumerate(b):
    pos_b[x] = i

freq = [0] * n

for x in range(1, n + 1):
    shift = (pos_a[x] - pos_b[x]) % n
    freq[shift] += 1

print(max(freq))
```

The first part builds inverse mappings from value to index, which avoids repeated scanning of arrays. The core loop computes the required rotation for each value. The modulo operation ensures that negative shifts are correctly wrapped into the range [0, n-1].

The frequency array is sized n because there are exactly n possible distinct rotations. The final maximum directly corresponds to the best alignment.

A common mistake is reversing the shift direction; both conventions work as long as consistency is maintained. Another is forgetting modulo normalization, which would split equivalent rotations into negative and positive buckets.

## Worked Examples

### Example 1

a = [1,2,3,4,5], b = [2,3,4,5,1]

| x | pos_a[x] | pos_b[x] | shift |
| --- | --- | --- | --- |
| 1 | 0 | 4 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 2 | 1 | 1 |
| 4 | 3 | 2 | 1 |
| 5 | 4 | 3 | 1 |

All values produce shift 1, so frequency[1] = 5 and answer is 5.

This confirms the case where one rotation perfectly aligns both permutations.

### Example 2

a = [1,3,2,4], b = [2,3,1,4]

| x | pos_a[x] | pos_b[x] | shift |
| --- | --- | --- | --- |
| 1 | 0 | 2 | 2 |
| 2 | 2 | 0 | 2 |
| 3 | 1 | 1 | 0 |
| 4 | 3 | 3 | 0 |

We get two shifts: 0 and 2, each with frequency 2. The answer is 2.

This shows that multiple optimal rotations can exist, and the algorithm correctly identifies the best among them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each value is processed once to compute its shift |
| Space | O(n) | Arrays store positions and frequency of shifts |

The linear complexity fits comfortably within constraints up to 2 × 10^5, and memory usage is minimal since we only store constant-factor auxiliary arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out

    # solution
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pos_a = [0] * (n + 1)
    pos_b = [0] * (n + 1)

    for i, x in enumerate(a):
        pos_a[x] = i

    for i, x in enumerate(b):
        pos_b[x] = i

    freq = [0] * n
    for x in range(1, n + 1):
        shift = (pos_a[x] - pos_b[x]) % n
        freq[shift] += 1

    print(max(freq))
    return out.getvalue().strip()

# provided samples
assert run("5\n1 2 3 4 5\n2 3 4 5 1\n") == "5"

# minimum size
assert run("1\n1\n1\n") == "1"

# already aligned
assert run("3\n1 2 3\n1 2 3\n") == "3"

# reverse-like alignment
assert run("4\n1 3 2 4\n2 3 1 4\n") == "2"

# random small case
assert run("5\n2 3 4 5 1\n1 2 3 4 5\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 identical | 1 | minimum boundary correctness |
| already equal | n | full alignment case |
| mixed permutation | 2 | multiple optimal shifts |
| rotated reverse pairing | 5 | cyclic shift correctness |

## Edge Cases

When n = 1, both permutations contain only a single element. The only shift is 0, and the frequency array collapses to a single bucket, so the answer is trivially 1.

When the arrays are identical, every value has shift 0. The frequency of shift 0 becomes n, and the algorithm returns full alignment without needing any special casing.

When permutations are perfect rotations of each other, every value produces the same shift value. The frequency table concentrates entirely in one bucket, showing that the method correctly captures global cyclic equivalence without explicitly simulating rotations.

When no single rotation aligns most elements except a small subset, the frequency table naturally spreads values across different shifts, and the maximum still corresponds to the best achievable alignment.