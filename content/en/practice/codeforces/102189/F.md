---
title: "CF 102189F - \u0421\u0438\u0433\u043d\u0430\u0442\u0443\u0440\u0430"
description: "We are given the lengths of consecutive blocks that a sequence must have. If the signature is (s1,s2,ldots,sn), then the final sequence must contain a block of (s1) equal values, followed by a different value repeated (s2) times, then another different value repeated (s3) times…"
date: "2026-08-19T06:20:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102189
codeforces_index: "F"
codeforces_contest_name: "12-\u0439 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0442\u0443\u0440\u043d\u0438\u0440 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0432 \u0410\u0431\u0430\u043a\u0430\u043d\u0435"
rating: 0
weight: 102189
solve_time_s: 94
verified: true
draft: false
---

[CF 102189F - \u0421\u0438\u0433\u043d\u0430\u0442\u0443\u0440\u0430](https://codeforces.com/problemset/problem/102189/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the lengths of consecutive blocks that a sequence must have. If the signature is (s_1,s_2,\ldots,s_n), then the final sequence must contain a block of (s_1) equal values, followed by a different value repeated (s_2) times, then another different value repeated (s_3) times, and so on. The values themselves are positive integers, and the task is to choose them so that the total sum of all elements is as small as possible.

For example, for the signature ([2,1,3,1]), the block values might be (1,2,1,2), giving the sequence ([1,1,2,1,1,1,2]). The four block values only need to differ from their immediate neighbors. Blocks that are not adjacent may use the same value.

There can be up to (10^5) blocks, while their total length is at most (10^6). Since the output itself can contain (10^6) integers, an (O(n)) algorithm is essentially the natural target. Algorithms with a quadratic factor in (n) would already require about (10^{10}) operations in the worst case, far beyond the intended time limit. The fact that the total signature length is bounded by (10^6) also means that constructing the answer explicitly is feasible, but we should avoid doing substantially more than a constant amount of work per output element.

The first edge case is a signature containing only one block. For input (n=1), (s=[5]), the answer is five copies of (1). There is no neighboring block to force a larger value, so using (2), (3), or any larger value would only increase the sum.

A second edge case is when the smallest value for the current block is not necessarily the best choice locally. For (s=[1,3]), choosing block values (1,2) gives a sum of (1+3\cdot2=7), while choosing (2,1) gives (2+3=5). Thus a greedy rule that always starts with (1) is wrong.

A third edge case occurs when many consecutive blocks have the same length. For (s=[2,2,2]), the optimal block values are (1,2,1), producing ([1,1,2,2,1,1]). Assigning (1,2,3) is valid, but its sum is larger. The construction only requires adjacent block values to differ, so alternating the two smallest values is sufficient.

Finally, the output contains repeated values, not the signature itself. For (s=[1,3]), outputting `2 1 1 1` is correct because its signature is ([1,3]). A common implementation mistake is to solve for the value of each block correctly but forget to expand that value according to its block length.

## Approaches

A direct brute-force approach would assign a positive integer to every block, check that neighboring assignments differ, expand the blocks, and compute the resulting sum. Because the signature lengths sum to at most (10^6), it is enough to consider values from (1) through (10^6), since no optimal answer needs a value larger than the total output length. Even with this artificial bound, there can be ((10^6)^n) assignments. At the maximum (n=10^5), that is (10^{600000}) candidates, so exhaustive search is completely infeasible.

A more structured brute force could observe that only small values are likely to matter and try several possible values for every block. This still has a multiplicative branching factor at every position, so it remains exponential. The real question is why values larger than (2) never have to appear.

Consider a dynamic programming state for a block whose chosen value is (x). Suppose that, for the previous block, the minimum achievable cost is attained by value (1). Then choosing (2) for the current block is legal and costs less than choosing any (x\ge3). If instead the minimum for the previous block is attained by value (2), then choosing (1) for the current block is legal and costs less than every (x\ge3). By induction, after every block the best state can be represented by one of the values (1) and (2). A value at least (3) is always dominated by one of those two choices.

Once only (1) and (2) remain, the problem becomes especially simple. Adjacent blocks must have different values, so after choosing the value of the first block, every later value is forced. There are only two possible patterns:

[
1,2,1,2,\ldots
]

and

[
2,1,2,1,\ldots
]

We can compute the cost of both patterns and choose the smaller one. The brute-force search over arbitrary values has thus collapsed to two candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^{6n})) candidates | (O(n)) | Too slow |
| Two-pattern DP | (O(n+\sum s_i)) | (O(n+\sum s_i)) for the output | Accepted |

## Algorithm Walkthrough

1. Read the signature (s_1,s_2,\ldots,s_n). Each (s_i) tells us how many copies of the value assigned to block (i) must be written.
2. Compute the cost of making the first block have value (1) and the cost of making it have value (2). These are (s_1) and (2s_1).
3. For every following block (i), swap the values used by the two previous states. If the previous block used (1), the current block must use (2). If the previous block used (2), the current block must use (1). The cost of a block of length (s_i) is its length multiplied by its chosen value.
4. Keep the total cost of both alternating patterns. At the end, choose the pattern with the smaller total cost.
5. Expand the selected pattern. If the chosen block value is (1), append (s_i) copies of `1`; if it is (2), append (s_i) copies of `2`. The total number of appended integers is exactly (\sum s_i), which is at most (10^6).

Why it works can be stated as an invariant. After processing block (i), the two maintained costs are exactly the minimum costs among solutions using the two possible alternating patterns ending with values (1) and (2). Any optimal solution can be restricted to values (1) and (2), because whenever a state with value at least (3) could be optimal, one of (1) or (2) is available from the preceding optimal state and has a strictly smaller contribution for the current positive block length. With values (1) and (2), the path constraint forces one of exactly two alternating patterns. Comparing those two patterns therefore finds the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = list(map(int, input().split()))

    # cost1: pattern 1,2,1,2,...
    # cost2: pattern 2,1,2,1,...
    cost1 = 0
    cost2 = 0

    for i, length in enumerate(s):
        if i % 2 == 0:
            cost1 += length
            cost2 += 2 * length
        else:
            cost1 += 2 * length
            cost2 += length

    first = 1 if cost1 <= cost2 else 2

    ans = []
    value = first

    for length in s:
        ans.extend([str(value)] * length)
        value = 3 - value

    sys.stdout.write(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The first loop computes both possible total sums without constructing the full sequence. For an even zero-based index, the first pattern uses value (1) and the second uses (2); for an odd index, their roles are reversed.

The comparison uses `<=`, so ties consistently select the first pattern. Any minimum is accepted, so the particular tie-breaking rule does not affect correctness.

The second loop reconstructs exactly the selected pattern. The expression `3 - value` switches `1` to `2` and `2` to `1`, avoiding a separate conditional.

The `ans` list contains strings because joining strings at the end is considerably more efficient than repeatedly concatenating to one large Python string. Its size is bounded by the total signature length, at most (10^6).

Python integers do not overflow, and the largest possible sum is at most (2\cdot10^6) for the constructed two-value solution, so integer arithmetic is trivial here. The dominant memory usage is the output itself.

## Worked Examples

### Sample 1

The sample signature is (s=[1,2,2]). The two possible patterns have the following costs.

| Block | Length | Pattern 1 value | Pattern 1 cost | Pattern 2 value | Pattern 2 cost |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 2 | 2 |
| 2 | 2 | 2 | 4 | 1 | 2 |
| 3 | 2 | 1 | 2 | 2 | 4 |
| Total | 5 |  | 7 |  | 8 |

Pattern 1 is cheaper, so the block values are (1,2,1). Expanding them according to the signature gives `1 2 2 1 1`, but the provided sample uses the signature `1 2 3`, yielding `1 2 2 1 1 1`. For the actual sample input (s=[1,2,3]), the calculation is:

| Block | Length | Pattern 1 value | Pattern 1 cost | Pattern 2 value | Pattern 2 cost |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 2 | 2 |
| 2 | 2 | 2 | 4 | 1 | 2 |
| 3 | 3 | 1 | 3 | 2 | 6 |
| Total | 6 |  | 8 |  | 10 |

The first pattern wins, giving `1 2 2 1 1 1`. Its blocks have lengths (1,2,3), exactly matching the signature.

### Sample 2

Consider (s=[1,3]). This example catches the mistake of always starting with value (1).

| Block | Length | Pattern 1 value | Pattern 1 cost | Pattern 2 value | Pattern 2 cost |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 2 | 2 |
| 2 | 3 | 2 | 6 | 1 | 3 |
| Total | 4 |  | 7 |  | 5 |

The second pattern is better, so the answer is `2 1 1 1`. Its first block has one `2`, and its second block has three `1`s. The sum is (5), which is smaller than the (7) obtained by starting with `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+\sum s_i)) | One pass computes the two costs, and one pass expands the output |
| Space | (O(\sum s_i)) | The explicit answer contains exactly (\sum s_i) integers |

The constraints give (n\le10^5) and (\sum s_i\le10^6). The algorithm performs only a constant amount of arithmetic per signature element and then writes at most (10^6) output values, so it fits comfortably within the intended limits.

## Test Cases

```python
import sys
import io

def solve():
    n = int(input())
    s = list(map(int, input().split()))

    cost1 = 0
    cost2 = 0

    for i, length in enumerate(s):
        if i % 2 == 0:
            cost1 += length
            cost2 += 2 * length
        else:
            cost1 += 2 * length
            cost2 += length

    first = 1 if cost1 <= cost2 else 2

    ans = []
    value = first

    for length in s:
        ans.extend([str(value)] * length)
        value = 3 - value

    sys.stdout.write(" ".join(ans))

input = sys.stdin.readline

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    stream = io.StringIO(inp)
    sys.stdin = stream
    input = stream.readline

    old_stdout = sys.stdout
    output = io.StringIO()
    sys.stdout = output

    try:
        solve()
        return output.getvalue()
    finally:
        sys.stdin = old_stdin
        input = old_input
        sys.stdout = old_stdout

def signature(arr):
    if not arr:
        return []

    result = []
    current = arr[0]
    count = 1

    for x in arr[1:]:
        if x == current:
            count += 1
        else:
            result.append(count)
            current = x
            count = 1

    result.append(count)
    return result

# Provided sample
assert run("3\n1 2 3\n") == "1 2 2 1 1 1", "sample 1"

# Minimum-size input
assert run("1\n1\n") == "1", "minimum size"

# A greedy-start counterexample
assert run("2\n1 3\n") == "2 1 1 1", "starting with 1 is not always optimal"

# All blocks have the same length
assert run("3\n2 2 2\n") == "1 1 2 2 1 1", "equal block lengths"

# Boundary case with a large single block
assert run("1\n1000000\n") == " ".join(["1"] * 1000000), "maximum output length"

# Maximum number of blocks
large = " ".join(["1"] * 100000)
out = run("100000\n" + large + "\n")
arr = list(map(int, out.split()))

assert len(arr) == 100000
assert signature(arr) == [1] * 100000
assert sum(arr) == 150000
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Minimum input and single-block handling |
| `2 / 1 3` | `2 1 1 1` | Correctly choosing the better starting value |
| `3 / 2 2 2` | `1 1 2 2 1 1` | Alternation and equal neighboring block lengths |
| `1 / 1000000` | One million `1`s | Maximum output size and expansion logic |
| `100000 / 1 1 ... 1` | Alternating `1 2 1 2 ...` | Maximum number of blocks and boundary handling |

## Edge Cases

For a single block, such as `1 / 5`, there are no adjacency restrictions at all. The algorithm compares the two nominal patterns, but pattern 1 has cost (5) while pattern 2 has cost (10), so it chooses value `1` and outputs `1 1 1 1 1`. The signature remains `[5]`.

For the local-greedy counterexample `2 / 1 3`, the first pattern has values (1,2) and cost (1+6=7). The second has values (2,1) and cost (2+3=5), so the algorithm chooses the second pattern and outputs `2 1 1 1`. This demonstrates why the first block cannot simply be assigned the smallest possible value without considering its neighbors.

For repeated block lengths, `3 / 2 2 2`, the two patterns have costs (2+4+2=8) and (4+2+4=10). The first pattern is selected, giving `1 1 2 2 1 1`. The middle block differs from both neighbors, while the first and third blocks may safely use the same value because they are not adjacent.

For the maximum output length, `1 / 1000000`, the answer consists of one million copies of `1`. The algorithm never creates unnecessary alternative values, and the output size is exactly the allowed maximum. The expansion loop performs one append operation per output element, so its work is linear in the unavoidable output size.

For the maximum number of blocks, take (100000) blocks of length (1). Every neighboring block must differ, so the optimal sequence alternates between `1` and `2`. There are two possible alternating sequences, and because there are an even number of blocks, the pattern beginning with `1` has total sum (50000\cdot1+50000\cdot2=150000). The algorithm computes exactly this choice without any special handling for the boundary between the first and last block, because only consecutive blocks are constrained.
