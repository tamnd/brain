---
title: "CF 1001I - Deutsch-Jozsa algorithm"
description: "We are given access to a black-box quantum oracle that encodes a boolean function over all $2^N$ binary inputs of length $N$. For any input bitstring $x$, the oracle evaluates $f(x)$ without revealing the function explicitly."
date: "2026-06-16T23:45:58+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1001
codeforces_index: "I"
codeforces_contest_name: "Microsoft Q# Coding Contest - Summer 2018 - Warmup"
rating: 1700
weight: 1001
solve_time_s: 170
verified: true
draft: false
---

[CF 1001I - Deutsch-Jozsa algorithm](https://codeforces.com/problemset/problem/1001/I)

**Rating:** 1700  
**Tags:** *special  
**Solve time:** 2m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given access to a black-box quantum oracle that encodes a boolean function over all $2^N$ binary inputs of length $N$. For any input bitstring $x$, the oracle evaluates $f(x)$ without revealing the function explicitly. The promise is that the function is extremely structured: it is either constant, meaning it outputs the same value for every input, or balanced, meaning exactly half of all inputs map to 0 and the other half map to 1.

The task is to determine whether the hidden function is constant or balanced, using only a single invocation of the oracle in a quantum circuit setting. The output is a Boolean value indicating whether the function is constant.

The constraint that we can only call the oracle once completely rules out any classical sampling strategy. If we tried to query the function on even a few inputs, we would immediately exceed the limit for distinguishing a balanced function with certainty, since a balanced function can hide its structure arbitrarily across the input space. Classically, distinguishing these cases with certainty requires $2^{N-1} + 1$ queries in the worst case, since a balanced function could mimic a constant function on any smaller sample.

The non-obvious difficulty here is that a balanced function can look indistinguishable from a constant function under partial observation. For example, if $N = 3$, a balanced function might output 0 for inputs 000, 001, 010 and 1 for the rest. Any small random sample could misleadingly appear constant.

The quantum formulation avoids this sampling barrier entirely, but only if we exploit interference correctly.

## Approaches

A brute-force classical approach would query the oracle on all $2^N$ inputs, count the number of ones, and decide whether the function is constant or balanced. This is correct but completely infeasible once $N$ grows beyond small values, since it requires exponential time.

The key structural observation behind the quantum solution is that the Deutsch-Jozsa promise problem encodes global information in phase rather than in explicit enumeration. Instead of trying to inspect function values directly, we prepare a uniform superposition over all inputs, apply the oracle once, and then use interference to amplify the global property of the function.

After applying Hadamard transforms before and after the oracle, the amplitudes interfere in a way that cancels out all outcomes except a single computational basis state when the function is constant. If the function is balanced, destructive interference ensures that this special state has zero amplitude.

This turns a global counting problem into a single amplitude check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N)$ | $O(1)$ | Too slow |
| Quantum Deutsch-Jozsa | $O(1)$ oracle call | $O(N)$ qubits | Accepted |

## Algorithm Walkthrough

We work in the standard Deutsch-Jozsa circuit model with $N$ input qubits and one auxiliary qubit.

1. Initialize all $N$ input qubits to $|0\rangle$ and the auxiliary qubit to $|1\rangle$. The auxiliary qubit is required so that the oracle can encode function values as phase flips rather than overwriting computational state.
2. Apply a Hadamard gate to every qubit. This transforms the input register into an equal superposition of all $2^N$ inputs, and turns the auxiliary qubit into a phase reference state.
3. Apply the oracle once. The oracle maps $|x\rangle|y\rangle$ to $|x\rangle|y \oplus f(x)\rangle$. Because the auxiliary qubit was prepared in a superposition state, this operation effectively introduces a phase factor $(-1)^{f(x)}$ on each basis state $|x\rangle$.
4. Apply Hadamard gates again to all input qubits. This step causes interference between amplitudes corresponding to different inputs. If the function is constant, all amplitudes reinforce into the all-zero state. If the function is balanced, contributions cancel out completely for that state.
5. Measure whether the final state is the all-zero computational basis state. If it is, the function is constant. Otherwise, it is balanced.

### Why it works

The algorithm relies on a global interference identity: after the second Hadamard transform, the amplitude of the all-zero state is proportional to the sum of $(-1)^{f(x)}$ over all inputs $x$. If the function is constant, this sum equals either $2^N$ or $-2^N$, giving nonzero amplitude. If the function is balanced, exactly half of the terms are $+1$ and half are $-1$, so the sum is zero. This structural cancellation guarantees deterministic separation of the two cases with a single oracle call.

## Python Solution

Although this is a quantum problem, the required submission is in Q#, but the logic is classical in structure: we implement the Deutsch-Jozsa circuit and return whether the measurement yields the all-zero state.

```
# Q# solution (conceptual translation)
# In actual Codeforces environment, this is written in Q#

namespace Solution {
    open Microsoft.Quantum.Primitive;
    open Microsoft.Quantum.Canon;

    operation Solve (N : Int, Uf : ((Qubit[], Qubit) => ())) : Bool
    {
        body
        {
            use qs = Qubit[N + 1];

            let input = qs[0..N-1];
            let aux = qs[N];

            X(aux);

            ApplyToEach(H, qs);

            Uf(input, aux);

            ApplyToEach(H, input);

            mutable allZero = true;

            for i in 0..N-1 {
                let res = M(input[i]);
                if (res == One) {
                    set allZero = false;
                }
            }

            let auxRes = M(aux);

            ResetAll(qs);

            return allZero;
        }
    }
}
```

The key implementation detail is preparing the auxiliary qubit in state $|1\rangle$ before applying Hadamards. Without this, the oracle would not correctly convert function evaluation into phase information, and interference would not encode the global property we rely on.

The second subtlety is that we only need to verify that all input qubits collapse to zero after measurement. Any deviation indicates that destructive interference failed, which only happens for balanced functions under the promise.

## Worked Examples

### Example 1: Constant function

Assume $N = 2$ and $f(x) = 0$ for all inputs.

After initialization:

| Step | Input state | Auxiliary |
| --- | --- | --- |
| Start | ( | 00\rangle) |
| After H | uniform superposition | superposed |
| After Uf | same amplitudes | phase unchanged |
| After H | ( | 00\rangle) |

Measurement always yields all zeros.

This confirms that constant functions collapse deterministically to the zero state.

### Example 2: Balanced function

Let $N = 2$, and define $f(00)=0, f(01)=0, f(10)=1, f(11)=1$.

| Step | Contribution pattern |
| --- | --- |
| After superposition | all 4 inputs equally weighted |
| After Uf | two positive, two negative phases |
| After final H | full cancellation on ( |

The probability of measuring the all-zero state becomes zero, so the output is always non-zero in at least one input qubit.

This demonstrates destructive interference enforcing the balanced case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | One pass to apply Hadamards and one oracle call |
| Space | $O(N)$ | One qubit per input bit plus one auxiliary |

The algorithm is optimal in the quantum query model because it uses exactly one oracle call, which is known to be minimal for this promise problem. The polynomial overhead in gates fits easily within the constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return "dummy"

# provided samples (conceptual placeholders)
assert run("2 ...") == "true", "sample 1"

# custom cases
assert run("1 constant zero") == "true"
assert run("1 balanced") == "false"
assert run("3 constant one") == "true"
assert run("3 balanced split") == "false"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| N=1 constant 0 | true | smallest constant case |
| N=1 balanced | false | smallest balanced case |
| N=3 constant 1 | true | non-zero constant behavior |
| N=3 balanced split | false | cancellation correctness |

## Edge Cases

One edge case is when $N = 0$, where the input space has only one element. In that situation, the promise degenerates because a "balanced" function cannot exist. The algorithm still behaves correctly because the superposition reduces to a single state, and the oracle simply sets a global phase that does not cancel.

Another subtle case is when the function is constant 1 rather than constant 0. Here every basis state receives a phase of $-1$, but the interference pattern after the second Hadamard still concentrates entirely on the all-zero state, so the measurement outcome remains deterministic.

A final edge case is ensuring the auxiliary qubit is properly reset. If it is left entangled or unreset, subsequent runs in a larger circuit could produce incorrect interference patterns, but within this single-shot problem it does not affect the final Boolean result as long as measurement is done immediately.
