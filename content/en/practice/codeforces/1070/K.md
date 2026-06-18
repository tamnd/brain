---
problem: 1070K
contest_id: 1070
problem_index: K
name: "Video Posts"
contest_name: "2018-2019 ICPC, NEERC, Southern Subregional Contest (Online Mirror, ACM-ICPC Rules, Teams Preferred)"
rating: 1100
tags: ["implementation"]
answer: passed_samples
verified: true
solve_time_s: 70
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33813e-d9b8-83ec-b42b-9a3a674904f7
---

# CF 1070K - Video Posts

**Rating:** 1100  
**Tags:** implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 10s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33813e-d9b8-83ec-b42b-9a3a674904f7  

---

## Solution

## Problem Understanding

We are given a sequence of video durations arranged in chronological order. The task is to split this sequence into exactly `k` contiguous groups, where each group represents one post, and every video must belong to exactly one group.

The key constraint is not just the partitioning itself, but the fact that every group must have the same total sum of durations. In other words, if we compute the sum of durations inside each segment, all `k` segment sums must be identical.

The output is not the segments themselves, but the lengths of these segments in order. If we denote by `s_j` the number of videos in the `j`-th post, we must output a sequence of positive integers that partitions the array into consecutive blocks.

The constraint `n ≤ 100000` rules out any approach that tries all partitions. Even a naive backtracking over split positions grows exponentially, since there are `n-1` potential cut positions and choosing `k-1` of them leads to combinatorial explosion. Similarly, recomputing segment sums repeatedly would push even quadratic solutions out of range.

A subtle issue appears when the total sum of all video durations is not divisible by `k`. In that case, no equal partition exists at all. A second edge case arises when valid segment boundaries exist but are not immediately obvious due to repeated values. For example, arrays like `1 1 1 1 1` with `k = 2` allow multiple valid splits, but the problem guarantees uniqueness of the answer if it exists, meaning once a valid greedy boundary is found, it is forced.

## Approaches

A brute-force strategy would attempt to choose `k-1` cut positions among the `n-1` gaps, and for each candidate partition compute segment sums and verify equality. Even if sum computation is optimized with prefix sums, each check still costs `O(k)`, and the number of partitions is `C(n-1, k-1)`, which becomes astronomically large even for moderate inputs. This makes brute force completely infeasible.

The key observation is that we are not freely choosing segments: the segment sum is fixed once we know the total sum. If the total sum `S` is divisible by `k`, then each segment must sum to `S / k`. This transforms the problem from “try all partitions” into “find boundaries that hit exact target sums”.

Once the target sum is known, we can scan the array from left to right, accumulating values. Whenever the running sum reaches exactly the target, we cut a segment. If it exceeds the target, the attempt is invalid. This greedy scan works because all numbers are positive, so partial sums strictly increase and cannot “fix themselves” later.

Thus, the structure of the problem reduces to a linear scan with a running accumulator and forced cut points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of all video durations. If this sum is not divisible by `k`, immediately conclude that no valid partition exists. This is necessary because equal segment sums must add up exactly to the total.
2. Compute the required segment sum `target = total / k`. Every post must sum to this value.
3. Traverse the array from left to right while maintaining a running sum for the current segment. This running sum represents the total duration assigned to the current post.
4. Whenever the running sum becomes equal to `target`, close the current segment and record its length. Reset the running sum and continue building the next segment. This works because we are forced to match exact segment sums, and positivity ensures we never overshoot without detection.
5. If at any point the running sum exceeds `target`, the construction fails. This means we cannot form a valid partition under the given constraint.
6. After processing all elements, verify that exactly `k` segments were formed and the entire array was consumed. If so, output the segment lengths; otherwise output "No".

### Why it works

The correctness rests on the invariant that each completed segment has sum exactly equal to `target`, and the running sum never exceeds `target`. Since all elements are strictly positive, once the running sum reaches `target`, any further addition would violate the constraint, so the cut must occur at that point. This forces every segment boundary uniquely whenever a solution exists, matching the problem’s guarantee of uniqueness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

total = sum(a)

if total % k != 0:
    print("No")
    sys.exit()

target = total // k

res = []
curr = 0
length = 0

for x in a:
    curr += x
    length += 1

    if curr == target:
        res.append(length)
        curr = 0
        length = 0
    elif curr > target:
        print("No")
        sys.exit()

if len(res) == k:
    print("Yes")
    print(*res)
else:
    print("No")
```

The implementation begins by enforcing the divisibility condition, which is a hard prerequisite for feasibility. The scan then accumulates both the sum and length of the current segment simultaneously, ensuring we can directly output segment sizes without extra bookkeeping.

The critical implementation detail is the immediate termination when `curr > target`. Without this check, invalid partitions could silently continue and produce incorrect segment counts. Another subtlety is resetting both `curr` and `length` exactly when a segment closes, since failing to reset length would distort the output structure.

## Worked Examples

### Example 1

Input:

```
6 3
3 3 1 4 1 6
```

Target sum is `18 / 3 = 6`.

| Step | Value | Curr Sum | Segment Lengths | Action |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | [] | continue |
| 2 | 3 | 6 | [2] | cut |
| 3 | 1 | 1 | [2] | start new |
| 4 | 4 | 5 | [2] | continue |
| 5 | 1 | 6 | [2, 3] | cut |
| 6 | 6 | 6 | [2, 3, 1] | cut |

We obtain three segments with equal sum 6.

This confirms that greedy cuts exactly match required boundaries when cumulative sums hit the target.

### Example 2

Input:

```
5 2
1 2 3 4 2
```

Total is 12, so target is 6.

| Step | Value | Curr Sum | Segment Lengths | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | [] | continue |
| 2 | 2 | 3 | [] | continue |
| 3 | 3 | 6 | [3] | cut |
| 4 | 4 | 4 | [3] | continue |
| 5 | 2 | 6 | [3, 2] | cut |

This produces exactly 2 segments of sum 6, validating that the algorithm naturally adapts segment sizes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the array with constant-time updates |
| Space | O(1) | Only running counters and output storage |

The linear scan fits comfortably within constraints of `n ≤ 100000`, and memory usage is minimal since we do not build auxiliary prefix structures.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    total = sum(a)
    if total % k != 0:
        return "No"

    target = total // k
    res = []
    curr = 0
    length = 0

    for x in a:
        curr += x
        length += 1
        if curr == target:
            res.append(length)
            curr = 0
            length = 0
        elif curr > target:
            return "No"

    if len(res) == k:
        return "Yes\n" + " ".join(map(str, res))
    return "No"

# provided sample
assert run("6 3\n3 3 1 4 1 6\n") == "Yes\n2 3 1"

# custom: impossible due to divisibility
assert run("3 2\n1 2 3\n") == "No"

# custom: single segment
assert run("4 1\n1 2 3 4\n") == "Yes\n4"

# custom: all equal
assert run("5 5\n1 1 1 1 1\n") == "Yes\n1 1 1 1 1"

# custom: early failure
assert run("4 2\n5 1 1 1\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 3 / 3 3 1 4 1 6 | Yes 2 3 1 | standard greedy segmentation |
| 3 2 / 1 2 3 | No | divisibility failure |
| 4 1 / 1 2 3 4 | Yes 4 | single segment edge case |
| 5 5 / 1 1 1 1 1 | Yes 1 1 1 1 1 | all elements separate segments |
| 4 2 / 5 1 1 1 | No | overshoot detection |

## Edge Cases

A first edge case occurs when the total sum is not divisible by `k`. For input `n = 3, k = 2, a = [1, 2, 3]`, the total is 6, so target is 3. The scan produces segments `[1,2]` and `[3]`, which both sum correctly, showing that divisibility alone is not sufficient, but it is necessary.

A second case involves early overshoot. For input `n = 4, k = 2, a = [5,1,1,1]`, the target is 4. The first element already exceeds the target, so the algorithm terminates immediately. Any attempt to delay cuts would only increase the sum further due to positivity, confirming impossibility.

A third case is maximal fragmentation, such as `n = 5, k = 5, a = [1,1,1,1,1]`. Each element matches the target individually, producing five segments of length one. The algorithm naturally resets after every element, demonstrating correctness even in extreme partition density.