# Tutorial 3: Multiple Experimentation
This is the report to back up the third lab in Machine Learning I using **Weka**'s *KnowledgeFlow* and *Experimenter*

<br>

## Exercise 1: KnowledgeFlow

### 1. Execute the KnowledgeFlow. After that, select the  option `Show Results` from the `TextViewer` node What information is shown on each of them? 

Inside the `TextViewer` node associated to the `J48 tree node` we can find **decision rules**, **number of leaves**, and the **size** of the trees created in each Cross-validation fold.
Thus, we have 10 different buffer outputs in total with information about the 10 created trees.

Inside the `TextViewer` node associated to the `Classifier Performance Evaluation` node we can find statistics about the performance of our trained J48 tree, such as the *precision*, the *kappa statistic*, the *confusion matrix*, etc.

### 1.1 What is percentage of correctly classified instances?

The tree correctly classified 28071 instances, which account for a 86.2105% **prediction accuracy**.

### 13. What is the utility of creating knowledge flows with this Weka interface?
KnowledgeFlow eases the understanding and visualization of the data science workflow, making possible the quick creation of drafts for ML and DS projects.

We can see it being very useful when approaching the design of a classifier before it's real implementation in platforms as python's `scikit-learn` for example.

<br>

## Exercise 2: Experimenter