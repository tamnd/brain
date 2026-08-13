---
title: "CF 102341G - Gurdurr"
description: "Each layer can have only one of four stable configurations that matter to the game. A completely intact layer is III. A layer with two blocks is either II. or .II, and these two cases have identical game behavior, so we can treat them as one state."
date: "2026-08-14T05:08:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102341
codeforces_index: "G"
codeforces_contest_name: "Radewoosh+mnbvmar Contest (supported by AIM Tech)"
rating: 0
weight: 102341
solve_time_s: 237
verified: true
draft: false
---

[CF 102341G - Gurdurr](https://codeforces.com/problemset/problem/102341/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Each layer can have only one of four stable configurations that matter to the game. A completely intact layer is `III`. A layer with two blocks is either `II.` or `.II`, and these two cases have identical game behavior, so we can treat them as one state. The two one-block configurations are `I.I` and `.I.`.

The crucial difference between the last two states is that both are completely immovable, but `.I.` affects its neighbors because another `.I.` cannot be adjacent to it. An `I.I` layer does not impose that restriction.

A move from `III` can remove an exterior block and turn it into `II.` or `.II`, or remove the middle block and turn it into `I.I`. A `II.` or `.II` layer can remove its remaining exterior block and become `.I.`, but only when that does not create two neighboring singleton layers. Once a layer becomes `I.I` or `.I.`, it never changes again.

The input gives up to 30,000 independent towers. For every tower, `n` is at most 20, followed by the three-character configuration of each layer from top to bottom. We only need to decide whether the initial position is winning for the first player or losing for the first player.

The small value `n <= 20` is the main clue. A direct game-state search would have roughly four possibilities per layer, giving an upper bound of `4^20 = 1,099,511,627,776` stable-state encodings before even considering the stability restriction between neighboring singleton layers. Even memoization cannot make that remotely feasible. We need to exploit the fact that the interaction between layers is only local and that immutable layers split the game.

There are several edge cases that a solution must handle correctly. A single `I.I` layer has no legal move because removing either exterior block would leave an exterior singleton, so its answer is `Second`. A single `.I.` layer is also immovable, so `1 / .I.` is `Second`. A single `III` layer has two kinds of moves and is winning, so `1 / III` is `First`.

Another subtle case is a full layer next to `.I.`. For example,

```
2.I.III
```

is `First`. The `III` layer has two legal moves: removing its middle block creates `I.I`, while removing an exterior block creates `II.` or `.II`. In either resulting position the changed layer has no further move because it is next to `.I.`. Thus the whole local component has Grundy value 1. Treating every full layer as an ordinary independent `III` layer would give the wrong decomposition.

A second boundary case is two singleton layers. An input such as

```
2.I..I.
```

is not allowed at all, because the initial tower would be unstable. A careless implementation that does not preserve the promised stability condition might attempt to process it and accidentally allow illegal moves.

## Approaches

The brute-force approach is to represent every layer by its current configuration, enumerate every block that could be removed, reject moves that make the tower unstable, and recursively solve the resulting positions. Since every move removes one block, the recursion terminates, and the usual impartial-game recurrence correctly identifies winning and losing positions. Memoization would avoid solving the same position more than once.

The problem is the number of positions. Even if every layer were allowed to have four states independently, there would be `4^20`, about `1.1 * 10^12`, possible encodings. A memoized search over that state space is far beyond the limit. Without memoization, the recursion tree is even larger because the same configurations can be reached through different orders of removals.

The key observation is that `I.I` and `.I.` cannot themselves move. Such a layer permanently separates the game into independent parts. After a separator is fixed, the only layers that still need to be represented are `III` and the two-block state `II.` or `.II`.

There is one boundary effect. A `.I.` separator prevents its immediate neighbors from becoming singleton layers. If such a neighbor is already a two-block layer, it becomes completely immovable. If it is `III`, it has exactly one effective move, and its Grundy value is 1. This lets us remove those boundary layers from the complicated part of the game as well.

What remains is a segment consisting only of `III` and two-block layers. Encode `III` by bit 1 and `II.` or `.II` by bit 0. A segment of length `m` is now described by a bitmask with `m` bits. There are only `2^m` such masks.

For every mask we can compute its Grundy value directly from all legal moves. When a `III` position is selected, removing an exterior block clears its bit and keeps the segment connected. Removing the middle block creates `I.I`, which is an immovable separator, so the remaining prefix and suffix become independent games and their Grundy values are XORed.

When a two-block position is selected, its only legal move is to become `.I.`. That new singleton blocks its two neighbors. Consequently, those neighbors disappear from the active segment. If one of those neighbors was `III`, it contributes an independent Grundy value of 1 because it can make exactly one further move before becoming immovable.

Every resulting segment is shorter than the current one, or has the same length but a smaller mask, so the states can be precomputed in increasing length and mask order.

The resulting complexity is exponential only in `n`, not in the number of complete tower configurations. With `n <= 20`, the total number of segment states is

`2^1 + 2^2 + ... + 2^20 = 2^21 - 2`,

and each state examines at most 20 positions. This is the intended `O(n 2^n)` preprocessing, followed by linear processing of every input tower. The same `O(2^n n + tn)` complexity is described by independent contest analyses of the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with memoization | `O(n 4^n)` in the worst case | `O(4^n)` | Too slow |
| Optimal SG preprocessing | `O(n 2^n + tn)` | `O(2^n)` | Accepted |

## Algorithm Walkthrough

1. Read every layer and classify it as `F`, `D`, `T`, or `S`, where `F = III`, `D = II.` or `.II`, `T = I.I`, and `S = .I.`. The two orientations of the two-block state are equivalent because both have exactly one possible removal and become the middle singleton.
2. Mark every `T` and `S` as a separator. Also mark both neighbors of every `S`. A neighbor of a singleton cannot perform the move that would create another singleton beside it.
3. Every marked `F` next to an `S` contributes Grundy value 1. Such a layer has two legal removals, one producing `T` and the other producing `D`; both resulting states are immovable because the layer remains next to `S`. Thus its options all have Grundy value 0, giving `mex{0} = 1`.
4. Scan the unmarked layers and split them into maximal segments. Every layer in such a segment is either `F` or `D`, so encode `F` as bit 1 and `D` as bit 0. XOR the precomputed Grundy value of every segment into the answer.
5. To precompute a segment of length `m`, let `sg[m][mask]` be its Grundy value. For every position `k`, inspect its bit.
6. If bit `k` is 1, the layer is `F`. Removing an exterior block changes it to `D`, giving the state with bit `k` cleared. Removing the middle block changes it to `T`, which splits the remaining positions into an independent left segment and an independent right segment. Add both resulting Grundy values to the mex set.
7. If bit `k` is 0, the layer is `D`. Its only move changes it to `S`. That singleton makes positions `k-1` and `k+1` unable to continue toward singleton states, so they are removed from the active game. A neighboring `F` has exactly one remaining move and contributes 1, while a neighboring `D` contributes nothing. The portions beyond those neighbors remain independent segments.
8. Take the mex of all Grundy values obtained from legal moves. That is `sg[m][mask]`.
9. The entire tower is a disjoint sum of the components found during the scan. By the Sprague-Grundy theorem, the first player wins exactly when the XOR of all component Grundy values is nonzero.

### Why it works

The invariant is that every active segment contains only `III` and two-block layers, while every layer outside the segments is already immovable or is an immediate boundary effect caused by `.I.`. A `III` move either stays inside the same segment or creates `I.I` and splits it. A two-block move creates `.I.` and removes its two neighbors from future interaction. Thus every legal move from a segment corresponds exactly to one of the transitions used by the recurrence, and every transition produced by the recurrence corresponds to a legal move.

Since `I.I` and `.I.` cannot move, different components separated by them never interact again. Their Grundy values therefore combine by XOR. The precomputed `sg` value is consequently the exact Grundy value of every component, and a zero final XOR is exactly the condition for a losing position.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def build_sg(max_n):    # sg[m][mask] = Grundy value of a segment of length m.    # A bit 1 means III, a bit 0 means II. or .II.    sg = [bytearray(1 << m) for m in range(max_n + 1)]
    # Empty segment.    sg[0][0] = 0
    for m in range(1, max_n + 1):        cur = sg[m]
        for mask in range(1 << m):            seen = 0
            for k in range(m):                bit = 1 << k
                if mask & bit:                    # Move 1: III -> II. / .II.                    g = cur[mask ^ bit]                    seen |= 1 << g
                    # Move 2: III -> I.I.                    # The new I.I. is immovable and separates                    # the prefix and suffix.                    left_len = k                    left_mask = mask & (bit - 1)
                    right_len = m - k - 1                    right_mask = mask >> (k + 1)
                    g = sg[left_len][left_mask] ^ sg[right_len][right_mask]                    seen |= 1 << g
                else:                    # Move: II. / .II -> .I.                    # The new singleton blocks its immediate neighbors.                    g = 0
                    # Active part strictly to the left of k-1.                    if k >= 2:                        left_len = k - 1                        left_mask = mask & ((1 << (k - 1)) - 1)                        g ^= sg[left_len][left_mask]
                    # If k-1 exists and is III, it has exactly one                    # remaining move after k becomes a singleton.                    if k >= 1 and (mask & (1 << (k - 1))):                        g ^= 1
                    # Active part strictly to the right of k+1.                    if k + 2 < m:                        right_len = m - k - 2                        right_mask = mask >> (k + 2)                        g ^= sg[right_len][right_mask]
                    # Symmetric boundary contribution.                    if k + 1 < m and (mask & (1 << (k + 1))):                        g ^= 1
                    seen |= 1 << g
            # mex(seen)            g = 0            while seen & (1 << g):                g += 1
            cur[mask] = g
    return sg

def solve(data):    it = iter(data.split())    t = int(next(it))
    tests = []    max_n = 0
    for _ in range(t):        n = int(next(it))        layers = [next(it).decode() for _ in range(n)]        tests.append((n, layers))        max_n = max(max_n, n)
    sg = build_sg(max_n)
    out = []
    for n, layers in tests:        # 0 = singleton .I.        # 1 = I.I        # 2 = II. or .II        # 3 = III        a = [0] * n
        for i, s in enumerate(layers):            if s == b"III":                a[i] = 3            elif s == b".I.":                a[i] = 0            elif s == b"I.I":                a[i] = 1            else:                a[i] = 2
        # Mark layers that cannot belong to an ordinary active segment.        blocked = [False] * n
        for i in range(n):            if a[i] == 0:                blocked[i] = True                if i > 0:                    blocked[i - 1] = True                if i + 1 < n:                    blocked[i + 1] = True            elif a[i] == 1:                blocked[i] = True
        answer = 0        mask = 0        length = 0
        for i in range(n):            # A full layer adjacent to .I. is an independent SG-1 game.            if blocked[i] and a[i] == 3:                answer ^= 1
            if not blocked[i]:                # III -> 1, II. / .II -> 0                mask = (mask << 1) | (a[i] - 2)                length += 1            else:                if length:                    answer ^= sg[length][mask]                    length = 0                    mask = 0
        if length:            answer ^= sg[length][mask]
        out.append("First\n" if answer else "Second\n")
    return "".join(out)

def main():    data = sys.stdin.buffer.read().splitlines()    sys.stdout.write(solve(b"\n".join(data)))

if __name__ == "__main__":    main()
```

The preprocessing stores one `bytearray` for every segment length. Using a byte array matters in Python because there are about `2^21` precomputed states in total, and every Grundy value is small. A normal Python integer object for every table entry would consume substantially more memory.

The recurrence follows the two actual move types. For a set bit, `mask ^ bit` represents removing an exterior block from `III`, while the prefix and suffix masks represent removing the middle block and producing `I.I`. For a zero bit, the selected two-block layer becomes `.I.`, so the immediate neighbors are excluded from the remaining active segments.

The left and right masks use zero-based positions. After selecting position `k`, the left active part ends at `k - 2`, while the right active part starts at `k + 2`. That is why the two-block transition uses `k - 1` and `k + 2` when calculating the remaining segment lengths. These are the most likely places for an off-by-one error.

The input is read through `sys.stdin.buffer`, which is useful here because there can be 30,000 test cases. The preprocessing is done only up to the largest `n` appearing in the input, so small test files do not pay for unnecessary states.

The `seen` variable is an integer bitset. If a reachable position has Grundy value `g`, bit `g` is set. Computing the mex then only requires finding the first unset bit. This avoids allocating a temporary Python set for every one of the roughly two million states.

## Worked Examples

### Sample 1

Consider the first and fifth cases of the first sample.

For the first case, there is only one `III` layer. The corresponding one-bit segment has mask `1`.

| Segment length | Mask | Meaning | Reachable Grundy values | SG |
| --- | --- | --- | --- | --- |
| 1 | 0 | `II.` | `{0}` | 1 |
| 1 | 1 | `III` | `{1, 0}` | 2 |

The `III` layer can become a two-block layer, whose SG is 1, or it can become `I.I`, whose SG is 0. Hence its SG is `mex{0,1} = 2`, which is nonzero, so the output is `First`.

For the fifth case, the tower is two full layers.

| Segment length | Mask | Meaning | SG |
| --- | --- | --- | --- |
| 1 | 1 | `III` | 2 |
| 2 | 3 | `III / III` | 1 |

For the two-layer state, removing an exterior block leaves a state with SG 0, while removing a middle block splits the tower into two one-layer `III` games with SG `2 xor 2 = 0`. The reachable SG values include 0 but not 1, giving SG 1. The final XOR is nonzero, so the answer is `First`.

These traces show why treating `III` as simply "two moves remaining" is insufficient. Its two moves lead to positions with different future interactions, so the full Grundy recurrence is required.

### Sample 2

The second sample is

```
3II..IIIII
```

Both two-block layers are encoded as zero and the full layer as one, giving mask `100` if read from top to bottom in binary construction.

The three possible moves are easier to understand directly.

| Chosen layer | Current state | Resulting game | Result SG |
| --- | --- | --- | --- |
| 1 | `II.` | `.I.` blocks layer 2, leaving a one-layer `III` component | 2 |
| 2 | `.II` | `.I.` blocks layers 1 and 3, leaving one isolated full layer | 1 |
| 3, exterior | `III` | three two-block layers | 1 |
| 3, middle | `III` | `I.I` separates the two two-block layers | 1 |

The set of reachable Grundy values is `{1, 2}`, so the current position has SG value 0. The first player therefore loses, giving `Second`.

This example exercises the most delicate transition in the recurrence: when a two-block layer becomes `.I.`, its immediate neighbors cannot subsequently become singleton layers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Preprocessing time | `O(n 2^n)` | There are `2^m` masks for every `m <= n`, and each mask examines at most `m` positions |
| Each testcase | `O(n)` | The tower is classified and scanned once |
| Total time | `O(n 2^n + tn)` | Preprocessing is shared by all testcases |
| Space | `O(2^n)` | The SG table contains `2^(n+1) - 1` byte entries up to constant factors |

For `n = 20`, the preprocessing has about two million segment states and at most 20 transitions per state. The use of compact byte arrays keeps the memory footprint small, while the linear work per testcase is negligible compared with the shared preprocessing.

## Test Cases

```python
Pythonimport ioimport sys

def run(inp: str) -> str:    return solve(inp.encode()).strip()

# The solve() and build_sg() functions from the submitted solution# are assumed to be defined above.

sample1 = """\51III1I.I1.I.1.II2IIIIII"""
assert run(sample1) == """\FirstSecondSecondFirstFirst""".strip(), "sample 1"
sample2 = """\13II..IIIII"""
assert run(sample2) == "Second", "sample 2"

# Minimum-size positions.assert run("""\41III1II.1I.I1.I.""") == """\FirstFirstSecondSecond""".strip(), "single-layer states"

# Two full layers have SG 1, so the position is winning.assert run("""\12IIIIII""") == "First", "two full layers"

# Two full layers separated by singleton layers become two# independent SG-1 components, so their XOR is zero.assert run("""\13III.I.III""") == "Second", "singleton boundary decomposition"

# Maximum n, all layers are immovable I.I.assert run(    "1\n20\n" + "\n".join(["I.I"] * 20) + "\n") == "Second", "maximum-size all-equal terminal tower"

# Boundary case: a full layer immediately next to .I. has SG 1.assert run("""\12.I.III""") == "First", "full layer next to singleton"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / III`, `1 / II.`, `1 / I.I`, `1 / .I.` | `First, First, Second, Second` | Minimum size and all four fundamental layer states |
| `III / III` | `First` | Interaction between two active full layers |
| `III / .I. / III` | `Second` | Independent components separated by a singleton |
| Twenty `I.I` layers | `Second` | Maximum `n`, all equal terminal layers, and memory-safe preprocessing |
| `.I. / III` | `First` | Special handling of a full layer adjacent to a singleton boundary |

## Edge Cases

A single `I.I` layer is terminal. The only blocks that remain are the two exterior blocks, and removing either would leave a single exterior block, which violates the layer rule. The algorithm classifies it as a separator, creates no active segment, and leaves the XOR at zero.

```
1I.I
```

The execution marks the layer as blocked, finds no active layers, and outputs `Second`.

A single `.I.` layer is also terminal. There is no block that can be removed while leaving a valid nonempty layer, so the algorithm again creates no active segment.

```
1.I.
```

The answer is `Second`.

A full layer next to `.I.` requires special handling. Consider

```
2.I.III
```

The singleton marks itself and its neighbor as blocked. The `III` layer is consequently not put into the ordinary segment DP. Instead, it contributes XOR value 1. Its two possible moves both produce an immovable state, so its SG value really is 1. The final XOR is nonzero and the algorithm outputs `First`.

Finally, consider the sample-2 configuration:

```
3II..IIIII
```

No singleton exists initially, so all three layers belong to one active segment. The mask is `100`. Selecting either of the first two zero bits creates `.I.` and blocks its neighbors, while selecting the final full layer either changes it to a two-block layer or creates `I.I` and splits the segment. The resulting Grundy values are 2, 1, and 1, giving mex 0. The algorithm consequently outputs `Second`, exactly as required.
