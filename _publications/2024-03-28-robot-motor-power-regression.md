---
title: "Regression Model for the Prediction of Total Motor Power Used by an Industrial Robot Manipulator during Operation"
collection: publications
permalink: /publication/robot-motor-power-regression
excerpt: 'A multilayer perceptron is trained to predict the total motor power of an ABB IRB 120 industrial robot, with the input variable set pruned using random forest importance scores and Pearson correlation.'
date: 2024-03-28
venue: 'Machines'
paperurl: 'https://www.mdpi.com/2075-1702/12/4/225'
citation: 'Baressi Šegota, S., Anđelić, N., Štifanić, J., & Car, Z. (2024). "Regression Model for the Prediction of Total Motor Power Used by an Industrial Robot Manipulator during Operation." <i>Machines</i>, 12(4), 225.'
---

## Abstract

Motor power models are a key tool in robotics for modeling and simulations related to control and optimization. The authors collect the dataset of motor power using the ABB IRB 120 industrial robot. This paper applies a multilayer perceptron (MLP) model to the collected dataset. Before the training of MLP models, each of the variables in the dataset is evaluated using the random forest (RF) model, observing two metrics — mean decrease in impurity (MDI) and feature permutation score difference (FP). Pearson's correlation coefficient was also applied. Based on the scores of these values, a total of 15 variables, mainly static variables connected with the position and orientation of the robot, are eliminated from the dataset. The scores demonstrate that while both MLPs achieve good scores, the model trained on the pruned dataset performs better. With the model trained on the pruned dataset achieving R²=0.99924, σ=0.00007 and MAPE=0.33589, σ=0.00955, the model trained on the original, non-pruned data achieves R²=0.98796, σ=0.00081 and MAPE=0.46895, σ=0.05636. These scores show that by eliminating the variables with a low influence from the dataset, a higher scoring model is achieved, and the created model achieves a better generalization performance across five folds used for evaluation.
