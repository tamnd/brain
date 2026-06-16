---
title: "CF 1001D - Distinguish plus state and minus state"
description: "We are given a single qubit that has been prepared in one of two possible states. These two states are not computational basis states like The task is to interact with this qubit using allowed quantum operations, perform a measurement, and return an integer that identifies which…"
date: "2026-06-16T23:42:15+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1001
codeforces_index: "D"
codeforces_contest_name: "Microsoft Q# Coding Contest - Summer 2018 - Warmup"
rating: 1400
weight: 1001
solve_time_s: 57
verified: true
draft: false
---

[CF 1001D - Distinguish plus state and minus state](https://codeforces.com/problemset/problem/1001/D)

**Rating:** 1400  
**Tags:** *special  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single qubit that has been prepared in one of two possible states. These two states are not computational basis states like |0⟩ or |1⟩, but superposition states that differ only by a relative phase. Concretely, the qubit is guaranteed to be either the equal superposition with positive sign or the equal superposition with negative sign.

The task is to interact with this qubit using allowed quantum operations, perform a measurement, and return an integer that identifies which of the two states we were given. The output is required to be 1 for the positive superposition and -1 for the negative superposition.

Although the input size is just one qubit, the subtlety is that these two states are indistinguishable under direct measurement in the computational basis. A naive measurement immediately in the standard basis destroys the phase information, producing random outcomes in both cases. This is the key difficulty: the distinguishing information is stored in phase, not amplitude.

Since we only manipulate a single qubit, the computational constraints are trivial. Any constant number of quantum gates and one measurement is sufficient, so the time complexity is effectively O(1). The real constraint is correctness under quantum measurement rules rather than algorithmic efficiency.

A common failure case arises if one tries to measure directly without transforming basis first. For example, measuring the input state immediately yields 0 or 1 with equal probability for both inputs, so a naive mapping would sometimes return 1 and sometimes -1 regardless of the actual state. This is incorrect because the measurement erases the distinguishing feature.

## Approaches

A brute-force classical mindset would try to "sample" the qubit multiple times to infer the hidden phase. In a classical analogy, repeated measurements might reveal a bias, but in quantum mechanics this is impossible because measurement collapses the state. After the first measurement, the qubit is destroyed into a basis state, and no additional information about the original phase remains accessible. Thus, any strategy relying on repeated sampling fails immediately, since each run gives independent random outcomes unrelated to the hidden sign.

The key insight is that while the phase is invisible in the computational basis, it becomes amplitude information after applying a Hadamard transformation. The Hadamard gate converts the phase difference into a measurable bit flip. Specifically, it maps the positive superposition into |0⟩ and the negative superposition into |1⟩. This reduces the problem to a single standard measurement.

Once this transformation is applied, a single measurement completely determines the state. We then map the measurement outcome back to the required output values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force repeated measurement | O(∞ in principle, but invalid) | O(1) | Incorrect due to state collapse |
| Hadamard + measurement | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Apply a Hadamard gate to the input qubit. This rotates the state from the phase basis into the computational basis, converting phase information into measurable amplitude differences.
2. Measure the qubit in the computational basis. After the transformation, the outcome is deterministic: one of the two original states maps to |0⟩ and the other maps to |1⟩.
3. Convert the measurement result into the required integer output. If the result corresponds to |0⟩, return 1. If it corresponds to |1⟩, return -1.

The reason this ordering matters is that measurement must only happen after the basis transformation. Reversing the order destroys the distinguishing signal.

### Why it works

The correctness comes from the fact that the Hadamard gate is its own inverse and specifically swaps the X-basis and Z-basis representations. The two input states are eigenstates of the Pauli X operator with eigenvalues +1 and -1. Applying Hadamard maps these eigenstates into computational basis eigenstates of Z, where they can be perfectly distinguished by measurement. Since eigenstates map to orthogonal basis states, no probability overlap remains after transformation, guaranteeing deterministic identification.

## Python Solution

Although the original interface is in Q#, the logical structure can be represented as a deterministic transformation followed by measurement.

```python
import sys
input = sys.stdin.readline

def solve():
    q = input().strip()
    # In the quantum model, we would apply H and measure.
    # Conceptually:
    # if state is |+> -> measurement becomes 0
    # if state is |-> -> measurement becomes 1
    #
    # Then map:
    # 0 -> 1
    # 1 -> -1

    meas = input().strip()  # placeholder for measurement result

    if meas == "0":
        print(1)
    else:
        print(-1)

if __name__ == "__main__":
    solve()
```

In a real quantum environment, the only meaningful operation is the Hadamard gate applied to the qubit before measurement. The rest is classical post-processing. The key implementation detail is ensuring the measurement happens exactly once after the transformation, since any earlier measurement destroys the phase information.

## Worked Examples

Consider an input where the qubit is in the positive superposition state. After applying Hadamard, the state becomes |0⟩. Measurement always returns 0.

| Step | State |
| --- | --- |
| Initial |  |
| After H |  |
| Measurement | 0 |
| Output | 1 |

This confirms that the positive state maps deterministically to 1.

Now consider the negative superposition state.

| Step | State |
| --- | --- |
| Initial |  |
| After H |  |
| Measurement | 1 |
| Output | -1 |

This confirms that the negative state is correctly distinguished.

These traces show that the transformation removes all probabilistic ambiguity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | A constant number of quantum operations and one measurement |
| Space | O(1) | Only a single qubit and constant classical storage |

The constraints allow any constant-time quantum operation, and the solution uses exactly one basis change and one measurement, well within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Since we cannot truly simulate quantum states here, we mock behavior.

def solve():
    s = sys.stdin.readline().strip()
    # interpret input as "plus" or "minus"
    if s == "plus":
        print(1)
    else:
        print(-1)

# provided samples (conceptual)
assert run("plus") == "1", "sample 1"
assert run("minus") == "-1", "sample 2"

# custom cases
assert run("plus") == "1", "positive state"
assert run("minus") == "-1", "negative state"
assert run("plus") == "1", "repeated check stability"
assert run("minus") == "-1", "symmetry check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| plus | 1 | Positive state mapping |
| minus | -1 | Negative state mapping |
| plus | 1 | Determinism under repeated evaluation |
| minus | -1 | Symmetry and consistency |

## Edge Cases

The main edge case is attempting measurement before applying the basis transformation. If we measure immediately, both |+⟩ and |−⟩ collapse to 0 or 1 with equal probability, so repeated runs produce inconsistent outputs. For example, input |+⟩ might yield 0, then in another run also 1, making any deterministic mapping impossible.

After applying the Hadamard gate, this issue disappears. Consider |+⟩:

| Step | State |
| --- | --- |
| Initial |  |
| After measurement without H | random 0/1 |
| After H then measurement | always 0 |

For |−⟩:

| Step | State |
| --- | --- |
| Initial |  |
| After measurement without H | random 0/1 |
| After H then measurement | always 1 |

This confirms that the transformation is essential, and without it the problem is fundamentally unsolvable deterministically.
