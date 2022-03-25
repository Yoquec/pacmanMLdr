Alvaro Viejo and Alejandro Mayo
# Pacman Assignment 1
This is the report for the first assignment on the Pacman proyect.

## Phase 1: Instances collection
Our `printLineData` function already generated `.arff` files for us, so the only modification we did was to add the next tick attribute in.

To accomplish this we modified the function to not jump to a new line when finishing.

Each time the function is called, it introduces the first tick before adding a new line and continuing. We just need to account for the fact that when the game ends, we will need to add 199 to last's score. 
That's why the method also returns the current score, so that in the event of exiting the *main game loop*, it will add the new score before closing the file.

```py
		if self.countActions != 1:
			returnstr = f",{str(gameState.getScore())}\n"
			returnstr += ",".join(gameInfo)
		else:
			returnstr = ",".join(gameInfo)
		return (returnstr, gameState.getScore()) 
```
## Phase 2.1: Feature selection and extraction
### Weka's Attribute selection
Weka's attribute selection gave us results with little to no sense whatsoever.
For example, when testing for the best attributes in the keyboard dataset, the **tick number** rose up first, which is more likely to be independent from the best move than not.

Also the **current Tick Score** and the **Remaining pacdots** appeared to be suitable variables when testing with both training datasets, which is also ought to be unlikely. 

Finally we decided to ditch *Weka*'s results and to select features ourselves.

### Feature selection
We will first need to dispose ourselves from a couple of variables:

- **ticks** -> Aren't very correlated to the movement selection

- **<mark style="background: #BDB42EA6;">Pacman direction</mark>** -> This is a controversial variable to remove, because when evaluating attributes using *Weka* this variable **ranks first in importance** out of all of them. If we conduct a brief study on why is this the case we conclude that the big majority of the moves are likely to continue the current direction until we get too close to the ghost, or until the ghost moves abruptly in a non-planed direction. Either way, this current direction **DOES NOT help us decide which movement is the most optimal** to take when following a ghost, but **helps predicting how a human player would play** (which normally don't change direction as much as a machine would). As the goal for this project is to build a model that plays pacman, this feature will not be of help, even though models look like they perform better with it.

- **Screen dimensions** -> Is not correlated in any way with the current movement. Does not change in time and does not offer lots of information.
- Information about **pacdots** -> Not interested in pacdots.

- **Ghost Num** -> Is redundant if we have the variable `Ghost Alive`.

- **Ghost directions** -> As ghosts move randomly, this variable is of no use because movements are assumed to be independent from one another.

- **Current tick score** -> Won't need it in the classification phase.

- **NextTick score** -> Won't need it in the classification phase

#### Side note on testing KNN models.
The `KNN` algorithm works only with numerical data, so we will have to transform the *Nominal* attributes using the filter `NominalToBinary`
- Binaritize ghost alive
- Binaritize legal positions

### Feature extraction
We created two new features, one that **encapsulates ghost's distances and $x$ components**, and another one with the **$y$ components**.
#### Difference between $x$ and $y$ components
This new feature will be the difference between all the ghosts and Pac-man's $x$ and $y$ components, and will allow us to **encapsulate both ghost distances and $x$ and $y$ in the same variable**

$$\large \forall_{i = 1}^4\ \ diff_i^x = ghost_i^x - pacman^x$$
$$\large \forall_{i = 1}^4\ \ diff_i^y = ghost_i^y - pacman^y$$

This will provide the same information that the previous data in less variables.

Once we created this feature we can remove both ghost's position components and distances.

#### Dataset Normalization and binaritization.
In order for `KNN` algorithms to work best, data should be normalized to make variables comparable between them.

Also, as mentioned in the end of Feature selection, we binaritized *Nominal* variables in order to be able to use them 

## Phase 2.2: Classification
### Algorithm selection
When using *Weka's* experimenter, the normalized and feature extracted datasets for both `keyboard` and `tutorial` were used to compare between different models.

![[Pasted image 20220320171154.png]]

![[Pasted image 20220320171346.png]]

We chose `ZeroR` as the base model to quantify how much better or worse models where, and the chose models where `KNN` for both $\large k = 1$ $\large k = 3$, two `J48` pruned and unpruned trees, a `NaiveBayes` model and a `PART` rule decision model.

It was quickly apparent that the models that better stood out where the `3NN` and both `J48` trees, with a special mention to the `PART` model.

With these models chosen we need to advance to the testing.

### Algorithm testing
As both `KNN` and `J48` trees performed significantly well, we tested both, and added the `RPART` model and a new `Random Forest` model. As `J48` did well in the model selection, choosing the `Random Forest` model to test with is a good try, because it is very **resilient against overfitting** and is also based in `Decision Trees`.

Due to the data being **normalized** for the KNN algorithm, we tested the tree-based models using both normalized variables and non-normalized datasets

#### Normalized dataset
<span class=centerImg>![[Pasted image 20220322183551.png|500]]</span>

It can be seen that the best performing model is the `KNN` model, as it is the most accurate and the one with the highest **Kappa statistic**; being followed by both `J48` and `Random Forest`, which shared a similar result.

>There is an important thing to point out, which is that even though train and test datasets are normalized, they have been normalized using a different scale and center. 

>The correct approach would have been to use the training set's scale and center to scale the testing dataset, but we weren't able to accomplish this using weka.

#### Non-normalized dataset (no KNN)
As this dataset was not normalized, `KNN` could not be compared, so only tree algorithms `J48` and `Random Forest`, and the `PART` algorithm will be included.

<span class=centerImg>![[Pasted image 20220322192011.png|500]]</span>

It is apparent that the `Random Forest` algorithm out-classifies both `J48` models, with a very similar performance to the `KNN` algorithm with normalization applied.

They only differ in the prediction accuracy of the automatic agent, where it seems that the normalized dataset performs slightly better in general.

#### Final selection
After seeing the results in both datasets, it can be seen that both `KNN` and `Random Forest` algorithms have a similar predictive power, but the slight superiority of the `Random Forest` and the complication of scaling the dataset using *Weka* from within *python* makes us choose the `Random Forest` model as a possible candidate to build the automatic agent.

## Phase 4: Building an automatic agent
In order to build the automatic Agent, we used the `Random Forest` model we talked about in the end of [[#Phase 2 2 Classification|Phase 2.2]], due to  it's apparently decent prediction accuracy and ease of use.

It uses `Pac-man's position`, current `legal movements`, and the `difference in the coordinates` as attributes to predict, being a very simple model.

It was implemented by creating the [[#Difference between x and y components]] feature within python itself for each of the ticks and feeding the necessary `gamestate` data to *Weka* through the `javabridge` package alongside `python-weka-wrapper3` with an intermediate API class inside the `WekaI.py` file.

We created a new Agent class called `AutomaticAgent` which inherits from the `BustersAgent` class and whose `chooseAction()` method contains a call to create the class `Weka` from the file `WekaI.py` which is only executed once when the method is first called.

Thanks to that established connection to *Weka*, we can use *Weka*'s models inside python.

```py
    def chooseAction(self, gameState):
        """Class which will be implementing the automatic
        movement"""

        if self.countActions == 0: 
            # Initialize weka
            self.weka = Weka()
            self.weka.start_jvm()

        # Increment the tick counter
        self.countActions = self.countActions + 1

        # NOTE: Scraping and preparing the data for the
        # prediction model
        predictInstance = [
                pacman_pos[0],
                pacman_pos[1],
                str(legal[0]),                      #legal_North
                str(legal[1]),                      #legal_South
                str(legal[2]),                      #legal_East
                str(legal[3]),                      #legal_West
                str(legal[4]),                      #legal_Stop
                str(ghost_living[0]),               #ghost1_alive
                str(ghost_living[1]),               #ghost2_alive
                str(ghost_living[2]),               #ghost3_alive
                str(ghost_living[3]),               #ghost4_alive
                diff_xs[0],
                diff_xs[1],
                diff_xs[2],
                diff_xs[3],
                diff_ys[0],
                diff_ys[1],
                diff_ys[2],
                diff_ys[3]
                ]

        # NOTE: Call the model for the prediction
        strAction = self.weka.predict(
                "./RFmodel_final.model",
                predictInstance,
                "./trainRF_treated.arff"
                )

        return strAction

```

Above there's a brief summary on how the method was built. It can stand out the fact that `self.weka` was declared inside this method instead of inside `__init__()`. This is due to the fact that the `jvm` library was in some way conflicting with `Tkinter` and the game window wasn't showing up if `self.weka.start_jvm()` was called before the creation of the window.

We gathered up instances from 20 manual games (`KeyboardAgent`) and 50 automatic games (`BasicAgentAA` from the first tutorial) and trained a `RandomForest` model that can be found with the name `RFmodel_final.model` with the training data file `trainRF_treated.arff`.

### Comparison to the other Agents
In comparison to the others, this new model stands out poorly. The reason is that it tries to imitate the behavior of the first tutorial's agent in a "human way", due to us adding our own training data from the `KeyboardAgent`. It starts working apparently fine, but when it encounters an unseen situation in the training set, caused by prior wrong movements, the model is finds itself with no clue on what to do.

It also seems that the model struggles when it is between two ghosts. This causes a situation where the model seems indecisive on which ghost to attack.

It is apparent that the model needs either more training or more complexity to really be useful compared to the other agents.

So it can be said that it performs worse than humans, and even worse to our programmed agent from the first tutorial.

## Questions
#### What is the difference between learning these models with instances coming from a human-controlled agent?
Even thought human-controlled agents always tend to know the most optimal route to each of the ghosts, they may make errors when pressing the keys. The result is a training data-set with the most likely optimal route, but with a lot of noise.

As a result of this models could over-fit to this noise and do nonsensical movements 

#### If you wanted to transform the regression task into classification, what would you have to do? What do you think could be the practical application of predicting the score?

#### What are the advantages of predicting the score over classifying the action? Justify your answer.
If we predict the score instead of the movement we could be able to run **Reinforcement Learning techniques** to reward/punish the model for optimal/bad decisions. This would turn our problem of classifying the movement into deciding which movement maximizes our reward.

#### Do you think that some improvement in the ranking could be achieved by incorporating an attribute that would indicate whether the score at the current time has dropped?
