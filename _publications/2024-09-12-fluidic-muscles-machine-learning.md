---
title: "Modeling of Actuation Force, Pressure and Contraction of Fluidic Muscles Based on Machine Learning"
collection: publications
permalink: /publication/fluidic-muscles-machine-learning
excerpt: 'Four machine learning algorithms are applied to data collected from fluidic muscle datasheets in order to predict actuation force, pressure and contraction length, with a general model outperforming the individual ones.'
date: 2024-09-12
venue: 'Technologies'
paperurl: 'https://www.mdpi.com/2227-7080/12/9/161'
citation: 'Baressi Šegota, S., et al. (2024). "Modeling of Actuation Force, Pressure and Contraction of Fluidic Muscles Based on Machine Learning." <i>Technologies</i>, 12(9), 161.'
---

## Abstract

In this paper, the dataset is collected from the fluidic muscle datasheet. This dataset is then used to train models predicting the pressure, force, and contraction length of the fluidic muscle, as three separate outputs. This modeling is performed with four algorithms — extreme gradient boosted trees (XGB), ElasticNet (ENet), support vector regressor (SVR), and multilayer perceptron (MLP) artificial neural network. Each of the four models of fluidic muscles (5-100N, 10-100N, 20-200N, 40-400N) is modeled separately: first, for a later comparison. Then, the combined dataset consisting of data from all the listed datasets is used for training. The results show that it is possible to achieve quality regression performance with the listed algorithms, especially with the general model, which performs better than individual models. Still, room for improvement exists, due to the high variance of the results across validation sets, possibly caused by non-normal data distributions.
