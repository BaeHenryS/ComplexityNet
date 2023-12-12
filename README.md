## Introduction 
We present ComplexityNet, a streamlined language
model designed for assessing task complexity. This model predicts
the likelihood of accurate output by various language models,
each with different capabilities. Our initial application of Com-
plexityNet involves the Mostly Basic Python Problems (MBPP)
dataset. We pioneered the creation of the first set of labels to
define task complexity. ComplexityNet achieved a notable 79%
accuracy in determining task complexity, a significant improve-
ment over the 34% accuracy of the original model. Furthermore,
ComplexityNet effectively reduces computational resource usage
by 57% , while maintaining a high code generation accuracy of
90%. This study demonstrates that fine-tuning smaller models to
categorize tasks based on their complexity can lead to a more
balanced trade-off between accuracy and efficiency in the use
of Large Language Models. Our findings suggest a promising
direction for optimizing LLM applications, especially in resource-
constrained environments.

![A chart explaining the setup](./Methodology.png)

## Repository Structure
The dataset folder includes the Jupyter Notebooks that create the dataset for all of `Code Llama`, `GPT-3.5`, and `GPT-4`. Different versions of the dataset we generated can be found there too.

The fine-tuning folders contain the Jupyter Notebooks used to fine-tune the complexity model. There's one version for fine-tuning completion models, like `Davinice-002` and another for fine-tuning chat-based models like `GPT-3.5`