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
### 2.1 Pac-Man data generation and pre-processing
#### Implementing the new printLineData function
In order to make the `printLineData()` function work, we needed to modify the `headers.py` file to introduce a method that creates **Weka**'s `.arff` file headers (@RELATION, @ATTRIBUTE, etc). This new method was called `generateArffHeaders()` and is called the same way we added the headers for the csv files in `game.py`.

It is important to note that we converted the `header_vals` list to be a dictionary containing the name of the header as the key, and the type of **Weka** variable (`NUMERIC` or set of possible values) so that everything is procedurally printed and formatted by the method:

```py
def generateArffHeaders(relationName: str) -> str:
    # Create the header with the relation name
    arffHeaders = f"@RELATION {relationName}\n\n"

    # Add the headers with the attributes and their types
    for key, val in zip(header_vals.keys(), header_vals.values()):
        arffHeaders += f"   @ATTRIBUTE {key} {val}\n"

    # Add the start data section header
    arffHeaders += "\n   @data\n"

    return arffHeaders
```

`printLineData()` itself received no modifications more than a few checks so that in `NUMERIC` variables a `-1` appeared instead of a `None`, which if not changed, would make Weka incapable of reading the generated files.

Unfortunately, we had to copy the whole `printLineData()` method over to the `KeyboardAgent` class, instead of making it a `@classmethod` for the `BasicAgentAA` to be accessed from outside the class. This could be possible because in order to record the tick number, we had to access the `self.countActions` attribute of the class, which would always be 0 because it wouldn't even be an instance.

#### Generate two new files from the one you just have created. On each of them you should select a subset of different attributes.
In relation to the last section, as we have to generate data with the purpose of predicting Pac-man's current movement, we changed where we placed our `printLineData()` method inside the `game.py` file.

We noticed that we called the method before Pac-man's action was chosen for that particular turn. If we hadn't changed it, we will be scraping last tick's movement instead of the current tick's. 

That's why when filtering the two `.arff` files, we removed the variable `pacman_dir` and left the variable `pacman_action`, as it was the updated one.

Our first division comes from the Select attributes with weka Explorer. We select `BestFirst` Method with `CfSubsetEval`
The variables would be: `ticks, pacman_pos_x,pacman_pos_y,legal_North, legal_South,legal_East,legal_West,ghost4_y,ghost1_dir,ghost4_dir,nearestpacdot_dist,score`.

For the second data set we will choose manually the **variables which seem more reasonable**, the pacman position, ghost position, ticks, score and which ghost are alive. Apart from legal movements

### 2.2 Design and execution of the experiment
We saved the experiment with the name `Experiment2.2Final.exp`.

### 2.3 Results analysis
#### 2.3.5 
The best data seems seems the one filtered manually by us, which contains more attributes than the one chosen by Weka, and make way more sense. This works for all algorithms except Bayesian models.

#### 2.3.6 
In our opinion the best algorithms in terms of accuracy looks to be `J48` followed by `Ibk` with `k=1`. as we see it perform better than default.

We think that out of these two algorithms, the most suitable one is `J48` because it performs the best in our filtered dataset. Also, we think that k = 1 is too simple of a model to have accurate predictions in the long term.

#### 2.3.7 
The difference between algorithms isn't significant enough to say that an algorithm would perform better than rest.

#### 2.3.9
We think that the Experimenter is suitable to compare whether the effect of some variables inside a dataset is significant or not, and if they even help on the performance of methods. 

Furthermore some methods tend to perform better on *Nominal* or *Numerical* data, so inside heterogeneous datasets this would be a good to tool to discern what algorithms and variables would be optimal for our use case.

## Conclusion
Weka is overall a good tool for **learning**, **planning** and **visualizing** the whole data science and Machine learning workflow. 
It allows for organization and testing of both datasets and different Machine Learning and Statistical models and quick development of projects.