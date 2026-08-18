---
title: "CF 102190E - standard input/output"
description: "This problem is different from a normal algorithmic classification task. You are given the already trained parameters of a small convolutional neural network, followed by a collection of 28 by 28 binary images."
date: "2026-08-19T05:51:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102190
codeforces_index: "E"
codeforces_contest_name: "2019 ECNU Campus Invitational Contest"
rating: 0
weight: 102190
solve_time_s: 624
verified: true
draft: false
---

[CF 102190E - standard input/output](https://codeforces.com/problemset/problem/102190/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem is different from a normal algorithmic classification task. You are given the already trained parameters of a small convolutional neural network, followed by a collection of 28 by 28 binary images. Your job is to reproduce the network's forward pass and print the predicted letter for every image.

There are four possible classes. Output class 0 as `C`, class 1 as `E`, class 2 as `N`, and class 3 as `U`. The input starts with an irrelevant magic number, then gives all weights and biases of the network in a fixed order. After that comes the number of images and the pixels of every image.

The network itself has a fixed structure. A 28 by 28 image first passes through four 5 by 5 convolution filters, producing four 24 by 24 feature maps. Each map is reduced by 2 by 2 max-pooling to 12 by 12. ReLU is then applied. The result goes through nine 3 by 3 convolution filters, where each output filter combines all four input channels, producing nine 10 by 10 maps. Another 2 by 2 max-pooling operation reduces these to nine 5 by 5 maps, followed by ReLU. These 9 times 5 times 5 values are flattened into 225 numbers, passed through a 225 to 64 fully connected layer and ReLU, and finally through a 64 to 4 fully connected layer. The largest of the four final scores determines the class.

The convolution weights are stored in flattened two-dimensional form. For the first convolution, the 4 by 1 by 5 by 5 tensor becomes 4 rows of 25 values. For the second convolution, the 9 by 4 by 3 by 3 tensor becomes 9 rows of 36 values. The row order follows the natural channel, row, column order, so a flat kernel entry can be indexed directly with the appropriate arithmetic.

The fixed image size makes the computation manageable even with straightforward nested loops. There are only 2240 images in the intended test data, and each image contains 784 pixels. The largest repeated operation is the convolution, but its dimensions are small: the first convolution performs 4 times 24 times 24 times 25 multiply-adds, and the second performs 9 times 10 times 10 times 36. The fully connected layers are also small, with 225 times 64 and 64 times 4 multiply-adds per image. This is several million elementary operations per complete input set, not an asymptotically large computation.

The main danger is not asymptotic complexity but faithfully reproducing the network's tensor layout and operation order. A convolution must use valid windows with stride one, max-pooling must use non-overlapping 2 by 2 windows, and the second convolution must sum over all four input channels. Applying ReLU at the wrong stage changes the network.

A simple edge case is an image containing only zero pixels. Suppose every weight is zero and every bias is zero. Every intermediate value is zero, and all four final scores are equal to zero. The correct prediction is `C`, because class 0 wins the ordinary argmax when there is a tie. An implementation that initializes the best class to 1, for example, would incorrectly print `E`.

Another subtle case occurs when a convolution has a negative result. For example, if one output of the first convolution is `-3`, max-pooling is performed before the first ReLU, so that value can compete with the other values in its 2 by 2 pooling window. If the four values are `-3, -5, -7, -2`, max-pooling produces `-2`, and only then does ReLU change it to zero. Applying ReLU before pooling gives the same maximum in this particular example, but this is not a reason to move the operation casually through the network. The specified ordering should be implemented directly, especially because the second convolution is also followed by pooling and then ReLU.

The boundary of every convolution is another common source of errors. A 5 by 5 window over a 28 by 28 image has 24 valid starting positions in each direction, namely rows 0 through 23 and columns 0 through 23. Starting at row 24 would require accessing row 28, which is outside the image. Similarly, a 3 by 3 window over a 12 by 12 feature map has starting positions 0 through 9, giving a 10 by 10 result.

## Approaches

The direct approach is to implement the neural network exactly as described. For every output position of a convolution, iterate over the kernel rows and columns and, for the second convolution, over every input channel as well. Add the bias after the corresponding weighted sum. Then perform max-pooling with explicit 2 by 2 windows, apply ReLU, flatten the resulting tensor in channel-major lexicographical order, and evaluate the two dense layers.

This brute-force implementation is already fast enough because the network dimensions are fixed and small. For one image, the first convolution costs 4 times 24 times 24 times 25 = 57,600 multiply-adds. The second costs 9 times 10 times 10 times 4 times 9 = 32,400 multiply-adds. The first dense layer costs 14,400 multiply-adds and the second costs 256. The total is roughly 105,000 multiply-adds per image, or about 235 million multiply-adds for 2240 images.

That count looks large in Python, so the useful optimization is not a new mathematical algorithm. The key observation is that the architecture is fixed, the input is binary, and the same trained filters are reused for every image. We can keep the implementation as simple nested loops while reducing Python-level overhead by storing tensors as flat arrays and using local variables. Since the problem has no variable image dimension and only around two thousand images, a carefully written direct forward pass is the appropriate solution.

A more elaborate approach would attempt to infer the letters directly from the images or train a separate classifier. That is unnecessary and potentially much less reliable. The supplied parameters already encode a classifier with a guaranteed accuracy above the acceptance threshold, so reproducing those parameters is the intended deterministic solution.

The important implementation detail is the tensor layout. The convolution weights are already grouped by output channel, then input channel, then kernel row and column. Likewise, the flattened second convolution output must be ordered as channel 0's 5 by 5 values, followed by channel 1's 5 by 5 values, and so on. That exactly matches the stated lexicographical ordering of the tensor indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct neural-network forward pass | O(t) with a fixed constant of roughly 105,000 arithmetic operations per image | O(1) per image apart from the fixed network parameters | Accepted |
| Reconstructing or training another classifier | Depends on the method, potentially much larger | Depends on the model | Unnecessary |

## Algorithm Walkthrough

1. Read and discard the magic number. Then read the four groups of network parameters in their specified order: the first convolution's weights and biases, the second convolution's weights and biases, the first dense layer's weights and biases, and the final dense layer's weights and biases. Their dimensions are fixed, so each can be stored as a flat Python list.
2. Read the number of images and process each 28 by 28 image independently. Keeping only the current image avoids storing all 2240 images simultaneously.
3. Compute the first convolution. For every output channel and every valid 5 by 5 window, calculate the weighted sum of the corresponding 25 input pixels and add the channel's bias. Since the input has one channel, there is no channel loop here. The output has shape 4 by 24 by 24.
4. Apply 2 by 2 max-pooling independently to each of the four channels. The pooling windows are non-overlapping, so output position `(r, c)` reads rows `2*r` and `2*r+1` and columns `2*c` and `2*c+1`. The result has shape 4 by 12 by 12.
5. Apply ReLU to every pooled value. ReLU replaces every negative value with zero and leaves non-negative values unchanged.
6. Compute the second convolution. For each of the nine output channels, each 10 by 10 output position uses a 3 by 3 window from every one of the four input channels. The 36 kernel values corresponding to one output channel are multiplied by those four 3 by 3 windows and summed, followed by the output bias.
7. Apply another 2 by 2 max-pooling operation, reducing each 10 by 10 channel to 5 by 5. Then apply ReLU to all 225 resulting values.
8. Flatten the 9 by 5 by 5 tensor in channel-major order. All 25 values of channel 0 come first, then all 25 values of channel 1, and so forth. This produces exactly 225 inputs for the first fully connected layer.
9. Evaluate the first dense layer. For each of its 64 neurons, calculate the dot product between its 225 weights and the flattened feature vector, then add its bias. Apply ReLU to the resulting 64 values.
10. Evaluate the final dense layer. Each of the four output scores is a dot product of the 64-dimensional hidden vector with one row of the final weight matrix, plus the corresponding bias. The prediction is the index of the largest score.
11. Convert the winning index to its letter using the mapping `0 -> C`, `1 -> E`, `2 -> N`, and `3 -> U`, then print it.

### Why it works

The invariant is that after every stage, the program stores exactly the tensor that the specified neural network would produce for the current image. The first convolution computes every valid kernel-window dot product with the correct bias, so its four feature maps are exact. Max-pooling then selects the maximum from every specified 2 by 2 window, and ReLU performs the required element-wise transformation. The same argument applies to the second convolution and pooling stage. Because the flattened vector follows the required lexicographical channel, row, column order, both fully connected layers receive exactly the values expected by the trained network. The final argmax consequently selects the same class as the original model.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    magic = input()

    conv1_w = [list(map(float, input().split())) for _ in range(4)]
    conv1_b = list(map(float, input().split()))

    conv2_w = [list(map(float, input().split())) for _ in range(9)]
    conv2_b = list(map(float, input().split()))

    fc1_w = [list(map(float, input().split())) for _ in range(64)]
    fc1_b = list(map(float, input().split()))

    fc2_w = [list(map(float, input().split())) for _ in range(4)]
    fc2_b = list(map(float, input().split()))

    t = int(input())
    letters = "CENU"
    output = []

    for _ in range(t):
        image = []
        for _ in range(28):
            image.extend(map(float, input().split()))

        # Conv 1: 1 -> 4, 28x28 -> 24x24.
        conv1 = [0.0] * (4 * 24 * 24)

        for oc in range(4):
            kernel = conv1_w[oc]
            bias = conv1_b[oc]
            base_out = oc * 24 * 24

            for r in range(24):
                out_base = base_out + r * 24
                img_base = r * 28

                for c in range(24):
                    s = bias
                    k = 0
                    for kr in range(5):
                        row_base = img_base + kr * 28 + c
                        for kc in range(5):
                            s += kernel[k] * image[row_base + kc]
                            k += 1

                    conv1[out_base + c] = s

        # Max-pooling: 24x24 -> 12x12.
        pool1 = [0.0] * (4 * 12 * 12)

        for ch in range(4):
            src_base = ch * 24 * 24
            dst_base = ch * 12 * 12

            for r in range(12):
                sr = 2 * r
                for c in range(12):
                    sc = 2 * c

                    a = conv1[src_base + sr * 24 + sc]
                    b = conv1[src_base + sr * 24 + sc + 1]
                    d = conv1[src_base + (sr + 1) * 24 + sc]
                    e = conv1[src_base + (sr + 1) * 24 + sc + 1]

                    pool1[dst_base + r * 12 + c] = max(a, b, d, e)

        # ReLU.
        for i in range(len(pool1)):
            if pool1[i] < 0:
                pool1[i] = 0.0

        # Conv 2: 4 -> 9, 12x12 -> 10x10.
        conv2 = [0.0] * (9 * 10 * 10)

        for oc in range(9):
            kernel = conv2_w[oc]
            bias = conv2_b[oc]
            dst_base = oc * 100

            for r in range(10):
                for c in range(10):
                    s = bias

                    for ic in range(4):
                        src_base = ic * 144
                        kernel_base = ic * 9

                        for kr in range(3):
                            src_row = src_base + (r + kr) * 12 + c
                            krow = kernel_base + kr * 3

                            s += (
                                kernel[krow] * pool1[src_row]
                                + kernel[krow + 1] * pool1[src_row + 1]
                                + kernel[krow + 2] * pool1[src_row + 2]
                            )

                    conv2[dst_base + r * 10 + c] = s

        # Max-pooling: 10x10 -> 5x5, followed by ReLU.
        features = [0.0] * (9 * 25)

        for ch in range(9):
            src_base = ch * 100
            dst_base = ch * 25

            for r in range(5):
                sr = 2 * r
                for c in range(5):
                    sc = 2 * c

                    a = conv2[src_base + sr * 10 + sc]
                    b = conv2[src_base + sr * 10 + sc + 1]
                    d = conv2[src_base + (sr + 1) * 10 + sc]
                    e = conv2[src_base + (sr + 1) * 10 + sc + 1]

                    value = max(a, b, d, e)
                    if value < 0:
                        value = 0.0

                    features[dst_base + r * 5 + c] = value

        # FC 1: 225 -> 64, followed by ReLU.
        hidden = [0.0] * 64

        for i in range(64):
            row = fc1_w[i]
            s = fc1_b[i]

            for j in range(225):
                s += row[j] * features[j]

            if s < 0:
                s = 0.0

            hidden[i] = s

        # FC 2: 64 -> 4.
        scores = [0.0] * 4

        for i in range(4):
            row = fc2_w[i]
            s = fc2_b[i]

            for j in range(64):
                s += row[j] * hidden[j]

            scores[i] = s

        best = 0
        for i in range(1, 4):
            if scores[i] > scores[best]:
                best = i

        output.append(letters[best])

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The input parser first consumes exactly the fixed number of parameter rows. A convolution weight tensor is represented as one flat row for each output channel, so `conv1_w[oc]` contains the 25 values for one 5 by 5 filter, while `conv2_w[oc]` contains four consecutive 3 by 3 kernels.

The first convolution uses output dimensions 24 by 24 because a 5 by 5 kernel has to remain completely inside the 28 by 28 image. The loop limits `range(24)` are consequently not arbitrary constants, they are the exact number of valid window positions.

The first pooling stage accesses four neighboring values explicitly. This avoids creating temporary two-dimensional lists and also makes the non-overlapping stride of two obvious. ReLU is applied after pooling, matching the network definition.

The second convolution is the part most likely to be implemented incorrectly. One output channel has 4 input channels, and every input channel contributes a complete 3 by 3 dot product. The kernel offset `ic * 9` selects the appropriate 3 by 3 block from the flattened row.

After the second pooling stage, each channel contains exactly 25 values. Since the channels are stored consecutively, the resulting `features` list is already in the required flattening order. No transpose or reshaping operation is necessary.

The dense layers use the supplied matrices directly. Python integers are not an issue here because the weights are floating-point values, and the sums remain floating-point values. The final argmax deliberately uses `>` rather than `>=`, so ties remain assigned to the lowest class index, matching the usual argmax convention.

## Worked Examples

The statement's actual sample matrices are omitted in the supplied problem text, so their complete numeric forward pass cannot be reconstructed here. The following two small synthetic traces use simplified network parameters to demonstrate the same control flow.

### Example 1

Consider a conceptual input whose network produces the following four final scores:

| Stage | Values |
| --- | --- |
| FC2 score 0 | 2.5 |
| FC2 score 1 | -1.0 |
| FC2 score 2 | 0.7 |
| FC2 score 3 | 1.8 |
| Argmax | 0 |
| Output | `C` |

The winning score is the first one, so the classifier prints `C`. The trace demonstrates that the program does not apply softmax before choosing the class. Softmax preserves the ordering of the scores, so computing it would add work without changing the prediction.

### Example 2

Consider final scores where several classes tie:

| Stage | Values |
| --- | --- |
| FC2 score 0 | 0.0 |
| FC2 score 1 | 0.0 |
| FC2 score 2 | -2.0 |
| FC2 score 3 | 0.0 |
| Argmax after scanning | 0 |
| Output | `C` |

The initial best index is zero, and the program only replaces it when it encounters a strictly larger score. Equal scores consequently leave class zero selected. This is the correct deterministic behavior for an ordinary left-to-right argmax.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) with a fixed constant | Every image has the same 28 by 28 dimensions and passes through a fixed-size network |
| Space | O(1) per image | All network dimensions are fixed, and only one image's intermediate tensors are stored |

For the intended 2240 images, the direct implementation performs roughly 235 million floating-point multiply-adds, together with the pooling and dense-layer work. The architecture is fixed and the input size is tiny compared with ordinary machine-learning workloads, so the straightforward forward pass is the natural competitive-programming solution. The implementation also avoids storing the entire test set, keeping memory proportional only to the fixed network and one image.

## Test Cases

Because the official sample matrices are omitted from the supplied statement, they cannot be reproduced as executable assertions without inventing parameter data. The following tests exercise the complete forward-pass implementation with generated parameter blocks.

```python
import sys
import io

def build_case():
    parts = []

    # Magic number.
    parts.append("0")

    # Conv1 weights: 4 x 25.
    for _ in range(4):
        parts.append(" ".join(["0"] * 25))

    # Conv1 bias.
    parts.append("0 0 0 0")

    # Conv2 weights: 9 x 36.
    for _ in range(9):
        parts.append(" ".join(["0"] * 36))

    # Conv2 bias.
    parts.append("0 0 0 0 0 0 0 0 0")

    # FC1 weights: 64 x 225.
    for _ in range(64):
        parts.append(" ".join(["0"] * 225))

    # FC1 bias.
    parts.append(" ".join(["0"] * 64))

    # FC2 weights: 4 x 64.
    for _ in range(4):
        parts.append(" ".join(["0"] * 64))

    # FC2 bias.
    parts.append("0 0 0 0")

    parts.append("1")

    # One all-zero 28 x 28 image.
    for _ in range(28):
        parts.append(" ".join(["0"] * 28))

    return "\n".join(parts) + "\n"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# All parameters and pixels are zero, so all four scores tie at zero.
assert run(build_case()) == "C\n", "all-zero tie case"

def build_bias_case():
    parts = []

    parts.append("0")

    for _ in range(4):
        parts.append(" ".join(["0"] * 25))
    parts.append("0 0 0 0")

    for _ in range(9):
        parts.append(" ".join(["0"] * 36))
    parts.append("0 0 0 0 0 0 0 0 0")

    for _ in range(64):
        parts.append(" ".join(["0"] * 225))
    parts.append(" ".join(["0"] * 64))

    for _ in range(4):
        parts.append(" ".join(["0"] * 64))

    # Class 3 has the largest final bias.
    parts.append("0 0 0 10")

    parts.append("1")
    for _ in range(28):
        parts.append(" ".join(["0"] * 28))

    return "\n".join(parts) + "\n"

assert run(build_bias_case()) == "U\n", "final bias case"

def build_negative_hidden_case():
    parts = []

    parts.append("0")

    # Conv1 produces zero everywhere.
    for _ in range(4):
        parts.append(" ".join(["0"] * 25))
    parts.append("0 0 0 0")

    # Conv2 produces zero everywhere.
    for _ in range(9):
        parts.append(" ".join(["0"] * 36))
    parts.append("0 0 0 0 0 0 0 0 0")

    # FC1 has negative bias, so ReLU makes every hidden value zero.
    for _ in range(64):
        parts.append(" ".join(["0"] * 225))
    parts.append(" ".join(["-5"] * 64))

    # FC2 has distinct biases.
    for _ in range(4):
        parts.append(" ".join(["0"] * 64))
    parts.append("1 2 3 4")

    parts.append("1")
    for _ in range(28):
        parts.append(" ".join(["0"] * 28))

    return "\n".join(parts) + "\n"

assert run(build_negative_hidden_case()) == "U\n", "ReLU before final layer"

def build_two_images_case():
    parts = []

    parts.append("0")

    for _ in range(4):
        parts.append(" ".join(["0"] * 25))
    parts.append("0 0 0 0")

    for _ in range(9):
        parts.append(" ".join(["0"] * 36))
    parts.append("0 0 0 0 0 0 0 0 0")

    for _ in range(64):
        parts.append(" ".join(["0"] * 225))
    parts.append("0 " * 63 + "0")

    for _ in range(4):
        parts.append(" ".join(["0"] * 64))
    parts.append("0 0 0 0")

    parts.append("2")

    for _ in range(28):
        parts.append(" ".join(["0"] * 28))

    for _ in range(28):
        parts.append(" ".join(["1"] * 28))

    return "\n".join(parts) + "\n"

assert run(build_two_images_case()) == "C\nC\n", "multiple images"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All parameters and pixels zero | `C` | Tie handling and zero-valued ReLU |
| Final bias `0 0 0 10` | `U` | Final argmax and class mapping |
| Negative FC1 biases | `U` | ReLU after the first dense layer |
| Two consecutive images | `C`, `C` | Per-image state reset and input consumption |

## Edge Cases

The all-zero case is handled by initializing `best` to zero and replacing it only when a later score is strictly greater. With four final scores equal to zero, the loop never changes `best`, so the output is `C`. This matters because an arbitrary tie-breaking rule could produce a different answer even though every network computation was otherwise correct.

The convolution boundary is handled by iterating the first convolution's row and column positions over `range(24)`. The final valid window starts at coordinate 23 and covers coordinates 23 through 27. No iteration begins at 24, so the implementation never reads outside the 28 by 28 image. The second convolution similarly uses `range(10)`, with its last window beginning at coordinate 9 and ending at 11 in the 12 by 12 input.

The second convolution's channel dimension is another edge case. For one output channel, the code reads a 3 by 3 region from input channel 0, then another from channel 1, channel 2, and channel 3. Omitting this loop would effectively treat the four-channel tensor as one channel and would produce completely different scores.

The flattening order is also significant. Suppose the nine pooled channels contain values `0, 1, ..., 224`, with each channel occupying 25 consecutive positions. The first dense neuron must receive the first 25 values from channel 0, followed by the 25 values from channel 1, and so on. The storage layout used by `features` is exactly that order, so the dense matrix can be applied without an additional permutation.

Finally, the implementation processes each image from scratch. Intermediate convolution and feature arrays are newly allocated for every image, so values from one test image cannot leak into the next. This is especially easy to get wrong when trying to optimize allocations by reusing buffers without explicitly overwriting every position.
