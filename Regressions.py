# -*- coding: utf-8 -*-

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/187zNlrg33RIVxe7bRi-jisxkg2dXqrnI
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

Turn in the assignment via Canvas.

To write legible answers you will need to be familiar with both [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) and [Latex](https://www.latex-tutorial.com/tutorials/amsmath/)

Before you turn this problem in, make sure everything runs as expected. First, restart the kernel (in the menubar, select Runtime→→Restart runtime) and then run all cells (in the menubar, select Runtime→→Run All).

Make sure you fill in any place that says "YOUR CODE HERE" or "YOUR ANSWER HERE", as well as your name below:
"""

NAME = "Suneet Bhandari"
STUDENT_ID = "1704322"

"""## Problem 1 - Yield Dataset with Polynomial Regression"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

"""This dataset of size $n = 15$ contains measurements of yield from an experiment done at five different temperature levels. The variables are $y = yield$ and $x = temperature$ in degrees Fahrenheit. Download the data from PyDrive."""

!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

downloaded = drive.CreateFile({'id':"1snU4nKrW72fgaEYzWvnrK0iRhsVX2W7N"})
downloaded.GetContentFile('yield.csv')

# Create pandas dataframe
data = pd.read_csv('yield.csv')

# Let's look at the data
data

# Look at data description
data.describe()

# Split data in X and y using pandas functionality.
X = data.iloc[:,0] # Create vector of explanatory variables
y = data.iloc[:,1] # Create vector of target variables

# Cast dataframes into numpy arrays
X = X.values
y = y.values

# Split data into X_train, Y_train, X_test y_test using sklearn
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 0)

# Reshape X_train, X_test for sklearn LinearRegression
X_train = X_train.reshape(-1,1)
X_test = X_test.reshape(-1,1)

"""### a) Linear Regression (10 points)

We will run a simple linear regression on this well-curated dataset using sklearn's **LinearRegression**.

Hint: Review the sklearn docs https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html and class exercise.
"""

from sklearn.linear_model import LinearRegression
from sklearn import datasets, linear_model
# Instantiate LinearRegression
regressor = LinearRegression()

# Fit the regressor using X_train and y_train

regressor.fit(X_train, y_train)

"""Let's now visually inspect the model and see how well this model predicts the yield. 
* First, plot the yield vs. temperature points from training set in black.
* Then, plot the regression line in red. Predictions from the regression model lie along the red line.
"""

# Plot the actual yield (y_train) vs. temperature values from training set
y_train_pred = regressor.predict(X_train)
plt.scatter(X_train, y_train, color='black')

# Plot the regression line

plt.plot(X_train, y_train_pred, color='red', linewidth=3)

"""Let's also visually inspect the prediction results from the test set.
* First, plot the yield vs. temperature points from the test set in black
* Then plot the regression line in red to see how prediction is similar to or different from the actual target.
"""

# Plot the actual yield (y_test) vs. temperature values  for the test set

y_test_pred = regressor.predict(X_test)
plt.scatter(X_test, y_test, color='black')

# Plot the regression line

plt.plot(X_test, y_test_pred, color='red', linewidth=3)

"""### b) Inspecting Linear Regression Model (5 points)

After inspecting the results visually, does this model appear to be a good or bad fit on the test set and training set?

The model looks to be a bad fit since there are points from the line which are fair meaning they could be outliers and not needed.

Does the model display signs of underfitting? If so, why?

Yes the model does have signs of underfitting because the data is not able to fully base its linear regression off of all the data points.

### c) Polynomial Regression (10 points)

Data may not follow a linear relationship from the independent variable $X$ to the dependent variable $y$. Fitting a linear model to this would be inaccurate and yield a high loss. 

If we want to model an order $d$ polynomial relationship between $X$ and $y$ we can augment our initial linear model where instead of having:
$$
y^{(i)} = \theta_0 + \theta_1 x^{(i)}
$$

We have:

$$
y^{(i)} = \theta_0 + \theta_1 x^{(i)} + \theta_2 {x^{(i)}}^2 + \cdots + \theta_d {x^{(i)}}^d
$$

We can use the same linear regression algorithm we if we first augment $X$ and add extra columns (or dimensions). 

$$ \textbf X =
\begin{bmatrix}
    x^{(1)}       & {x^{(1)}}^2 & \cdots & {x^{(1)}}^d \\
    x^{(2)}       & {x^{(2)}}^2 & \cdots & {x^{(2)}}^d \\
    \vdots       & \vdots & \ddots & \vdots \\
    x^{(n)}       & {x^{(n)}}^2 & \cdots & {x^{(n)}}^d
\end{bmatrix}$$

Then our new higher order $\hat Y$ is computed same as before.

$$ \hat Y =  X \theta =
\begin{bmatrix}
    1 & x^{(1)}       & {x^{(1)}}^2 & \cdots & {x^{(1)}}^d \\
    1 & x^{(2)}       & {x^{(2)}}^2 & \cdots & {x^{(2)}}^d \\
    \vdots & \vdots       & \vdots & \ddots & \vdots \\
    1 & x^{(n)}       & {x^{(n)}}^2 & \cdots & {x^{(n)}}^d
\end{bmatrix}
\begin{bmatrix}\theta_0 \\ \theta_1 \\ \vdots \\ \theta_{d} 
\end{bmatrix}=
\begin{bmatrix}
    \theta_0 + \theta_1 x^{(1)} + \theta_2 {x^{(1)}}^2 + \cdots + \theta_{d}  {x^{(1)}}^d \\
    \theta_0 + \theta_1 x^{(2)} + \theta_2 {x^{(2)}}^2 + \cdots + \theta_{d}  {x^{(2)}}^d  \\
    \vdots   \\
    \theta_0 + \theta_1 x^{(n)} + \theta_2 {x^{(n)}}^2 + \cdots + \theta_{d}  {x^{(n)}}^d
\end{bmatrix} 
= \begin{bmatrix}\hat y^{(1)} \\ \hat y^{(2)} \\ \vdots \\ \hat y^{(n)} 
\end{bmatrix}$$

Using sklearn's **PolynomialFeatures** functionality, we will now transform X_train and X_test into second order polynomial space.

For more info: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html
"""

# First, lets look at the values of X_train
print(X_train)
print(y_train)

from sklearn.preprocessing import PolynomialFeatures

# Creates polynomial transform of degree 2
poly = PolynomialFeatures(2)

# Transform X_train X_test
X_train_pol = poly.fit_transform(X_train)
X_test_pol = poly.fit_transform(X_test)

# Print X_train_pol
print(X_train_pol)
print(y_train)

"""We can now fit a second degree polynomial regression model to the transformed data."""

from sklearn.linear_model import LinearRegression

# Instantiate LinearRegression

regressor2 = LinearRegression()


# Fit the regressor using X_train_pol and y_train

regressor2.fit(X_train_pol, y_train)

"""Now, visually inspect the polynomial regression model and see how well this model predicts the yield on the training set. 

Plot the yield vs. temperature points in black along with the polynomial regression line in red. Hint: For plotting the regression line, you can use the plot function to interpolate the regression line based on the model's prediction on data points.
"""

# Plot the actual yield (y_train) vs temp. values from training set

X_train.sort()
y_train.sort()

plt.scatter(X_train, y_train, color='black')

# Plot the regression line

plt.plot(X_train, regressor2.predict(poly.fit_transform(X_train)), color='red', linewidth=3)
plt.show()

"""Lastly, let's plot the test set yield vs. temperature points along with the polynomial regression line."""

# Plot the actual yield (y_test) vs temp. values from test set

X_test.sort()
y_test.sort()

plt.scatter(X_test, y_test, color='black')

# Plot the regression line

plt.plot(X_test, regressor2.predict(poly.fit_transform(X_test)), color='red', linewidth=3)
plt.show()

"""### d) Inpsecting Polynomial Regression Model (5 points)

After inspecting the polynomial regression model, does the model appear to be a better fit than simple linear regression?

Yes the model does appear to fit better than the linear regression because it curves to reach most of the points properly, or in other words the points are in a more proper distance from the line.

Does the model address display more or less underfitting than the simple linear regression model and why?

This model address displays less underfitting than simple linear regression because the curving of the line allows for more points to be related to the line.

## Problem 2 - Fish Dataset

## Importing the Dataset

We will now perform different variations of linear regression to predict fish weight given species type, weight, and physical measurements. The different attributes of the data are:

- Species: species name of fish

- Weight: weight of fish in Gram (g)

- Length1: vertical length in (cm)

- Length2: diagonal length in (cm)

- Length3: cross length in (cm)

- Height: height in (cm)

- Width: diagonal width in (cm)

Begin by downloading the Fish.csv file from google drive. Make sure to select your @ucsc.edu email when authorizing access to your account.
"""

!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

# Download the Fish data
downloaded = drive.CreateFile({'id':"1AtMi-xCejVlhYS5qjgjjW4gH-TLuWJjC"})
downloaded.GetContentFile('Fish.csv')

import pandas as pd

# Create pandas dataframe
fish_data = pd.read_csv('Fish.csv')

"""Let's look at some of the data and check some of the dataset descriptors."""

# Let's print out the first few rows
fish_data.head()

# Let's get the data shape
fish_data.shape

# Let's describe the data
fish_data.describe()

# Lastly, let's get data info
fish_data.info()

"""### a) Removing 0's from data (5 points)

We can see that there aren't any null values in this dataset by using the .info() function. However, .describe() shows us there are weights of 0.0g which is ambiguous and is likely a recording error. 

Drop any row that has a weight of 0.0.
"""

# Delete any rows for which there is a measurement of 0.0 for weight.
indexes = fish_data[fish_data['Weight'] == 0.0].index
fish_data.drop(indexes, inplace=True) 

# Let's take another look.
fish_data.describe()

"""### b) Outlier Detection \& Elimination (5 points)

Using 4 standard deviations from the mean as our cut-off, and using the data listed using the describe function above, are there any outliers?
"""

fish_data.describe()

"""There are no outliers in this data as each of the maxes are within 4 standard deviations.

## Problem 3 - Fish Linear Regression

You will now run different versions of linear regression in order to predict fish Weight using the 6 explanatory variables.

### a) Multiple Linear Regression (6 points)

First, run a multiple linear regression using only the height, width, and length measurements to predict weight. We will begin by splitting the data into features **X_fish** and target variable **y_fish**.
"""

y_fish = fish_data.iloc[:, 1] # Get Fish Weights
X_fish = fish_data.drop(columns=['Weight']) # Get Fish measurements plus species
X_fish = X_fish.drop(columns=['Species']) # Drop the Fish Species for now

# Print X.head(), you should have 5 features for each sample
print("X_fish.head():")
print(X_fish.head())

# Print y.head(), you should have one label for each sample
print("\ny_fish.head()")
print(y_fish.head())

"""Now, we are almost ready to run regression with scikit-learn. We need to first convert **X_fish** and **y_fish** into numpy arrays and split the data into training and validation splits using sklearn **train_test_split**. 

sklearn's train_test_split offers customizable functionality when creating training and test sets. For more information, checkout https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html .
"""

# Convert X, and y into np arrays
X_fish = X_fish.values
y_fish = y_fish.values

# Split data into train test split
from sklearn.model_selection import train_test_split
X_fish_train, X_fish_test, y_fish_train, y_fish_test = train_test_split(X_fish, y_fish, test_size = 0.2, random_state = 0)

"""Now we are ready to run a multiple linear regression. Use sklearn's **LinearRegression** to carry out the regression."""

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

# Fit the regressor using X_fish_train and y_fish_train
regressor.fit(X_fish_train, y_fish_train)

"""Now let's see how we did and generate predictions for X_fish_test. Then print predicted values and actual target values side-by-side for a visual comparison."""

# Generate predictions using X_fish_test
y_fish_pred = regressor.predict(X_fish_test) 

# Print the predictions along with actual weights
print(y_fish_pred)
print(y_fish_test)

"""### b) Computing MSE and R-squared for MLR (5 points)

The model appears to do an okay job predicting some weights while missing the mark on others. Let's quantify the results by computing mean squared error (MSE) and the coefficient of determination (R-squared). sklearn's metrics package provides functions to compute the values for you. 

More info can be found here: 

https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
"""

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# Compute the mean squared error using y_fish_test and y_fish_pred
x = mean_squared_error(y_fish_test, y_fish_pred)
print(x)

# Compute the coefficient of determination using y_fish_test and y_fish_pred
y = r2_score(y_fish_test, y_fish_pred)
print(y)

"""Using the y_fish_test and y_fish_pred, what was the mean squared error for this model?

the mean squared error was 31561.773067541344

Using the y_fish_test and y_fish_pred, what was the coefficient of detemination for this model?

the r2score/coefficient of determination is 0.8245122776931352

### c) Polynomial Multiple Linear Regression (12 points)

We have seen how polynomial regression can increase the predictive power of linear regression models. We will now run a polynomial multiple linear regression model in order to gain a more accurate model. Begin by transforming the features X_fish_test and X_fish_train into second order polynomial space. There will be interaction terms in the transformed dataset as well. For more on interaction terms visit the sklearn docs.
"""

from sklearn.preprocessing import PolynomialFeatures


# Create polynomial transform of degree 2. hint: problem 1
poly = PolynomialFeatures(2)

# Transform X_fish_train X_fish_test to second order polynomial space
X_fish_train_pol = poly.fit_transform(X_fish_train)
X_fish_test_pol = poly.fit_transform(X_fish_test)

# Print 5 rows of X_fish_train_poly, shape should be (5,21)
new = X_fish_train_pol[0:5,0:21]
print(new)

"""Next run the second order polynomial regression using the transformed data. Instantiate a new regression model and use X_fish_train_pol and y_fish_train to fit the model."""

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

# Fit the regressor using X_fish_train_pol and y_fish_train
regressor.fit(X_fish_train_pol, y_fish_train)

"""Now let's see how we did with the second model and generate predictions using X_fish_test_pol. Then print predicted values and actual target values side-by-side for a visual comparison."""

# generate predictions using X_test
y_fish_pol_pred = regressor.predict(X_fish_test_pol)

# Print the predictions along with actual weights
print(y_fish_pol_pred)
print(y_fish_test)

"""### d) Computing MSE and R-squared for Polynomial Regression (5 points)

Now, compute the MSE and R-squared using y_fish_test and y_fish_pol_pred
"""

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score 

# Compute the mean squared error using y_fish_test and y_fish_pol_pred
a = mean_squared_error(y_fish_test, y_fish_pol_pred)
print(a)
# Compute the coefficient of determination using y_fish_test and y_fish_pol_pred
r2_score(y_fish_test,y_fish_pol_pred)

"""Using the y_fish_test and y_fish_pol_pred, what was the mean squared error for this model?

12552.64579521197

Using the y_fish_test and y_fish_pol_pred, what was the coefficient of detemination for this model?

0.9302055934939845

### e) Multiple Linear Regression With Categorical Variable (12 points)

Now that we have done multiple linear regression, and polynomial multiple linear regression, we will now do a multiple linear regression that takes into account the species of fish by creating numeric levels.
"""

# Create a copy of fish_data
fish_data_species = fish_data

# Begin by generating a dictionary that maps all unique species in fish_data to a unique id
level_dict = {level_name:i for i,level_name in enumerate(fish_data['Species'].unique())}

# Uses the level dictionary to retrieve the id
def integer_encode_level(level):
    return level_dict[level]

# Apply the function to the Species column and store in Species column (you should overwrite the species current data with the numeric representations)
fish_data_species['Species'] = fish_data_species['Species'].apply(integer_encode_level)

# Check data
fish_data_species

"""We will now create a dataset with 1 target column and 6 feature columns: Species, Length1, Length2, Length3, Height, Width. """

# Split fish_data into 
y_fish_categorical = fish_data_species.iloc[:, 1] # Get Fish Weights
X_fish_categorical = fish_data_species.drop(columns=['Weight']) # Get Fish measurements plus species

# Print X_fish_categorical.head(), you should have 6 features for each sample
print("X_fish_categorical.head():")
print(X_fish_categorical.head())

# Print y_fish_categorical.head(), you should have one label for each sample
print("\ny_fish_categorical.head()")
print(y_fish_categorical.head())

"""Create training and test sets for the fish data with categorical species variable:"""

# Convert X, and y into np arrays
X_fish_categorical = X_fish_categorical.values
y_fish_categorical = y_fish_categorical.values

# Split data into train test split
from sklearn.model_selection import train_test_split
X_fish_train_categorical, X_fish_test_categorical, y_fish_train_categorical, y_fish_test_categorical = train_test_split(X_fish_categorical, y_fish_categorical, test_size = 0.2, random_state = 0)

"""Now we are ready to run a our final multiple linear regression. As a recap, we added a categorical variable to represent the species of fish. We encoded the species as levels, and overwrote the species column with the numeric representations of the species. Now, use sklearn's **LinearRegression** to carry out regression one last time."""

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

# Fit the regressor using X_fish_train_categorical and y_fish_train_categorical
regressor.fit(X_fish_train_categorical, y_fish_train_categorical)

"""Let's check the predictions for this model and generate predictions using X_fish_test_categorical. Then print target and estimated weight values side-by-side."""

# generate predictions using X_fish_test_categorical
y_fish_pred_categorical = regressor.predict(X_fish_test_categorical) 


# Print the predictions along with actual weights
print(y_fish_pred_categorical)
print(y_fish_test_categorical)

"""### f) Computing MSE and R-squared for MLR with Categorical Variable (5 points)"""

# Compute the mean squared error using y_fish_test_categorical and y_fish_pred_categorical
msr = mean_squared_error(y_fish_test_categorical, y_fish_pred_categorical)
print(msr)


# Compute the coefficient of determination using y_fish_test_categorical and y_fish_pred_categorical
r2_score(y_fish_test_categorical, y_fish_pred_categorical)

"""Using y_fish_test_categorical and y_fish_pred_categorical, what was the mean squared error for this model?

34678.46536821308

Using y_fish_test_categorical and y_fish_pred_categorical, what was the coefficient of detemination for this model?

0.807183047430761

### g) Researching for the Best Model (15 points)

Read [this](https://www.datarobot.com/blog/regularized-linear-regression-with-scikit-learn/) tutorial to see how you can control the degree of the polynomial and train a **Regularized** linear regression model.

In the cell below, investigate and show your observations on:
1. Which features are important?
2. What polynomial order is appropriate for the model to have an appropriate fit (no overfitting or underfitting)?
3. The impact of regularization (L2 norm or L1 norm) and the regularizer factor/parameter on model's generalization capability.
4. Finally, report your best model (including model's cost function, regularizer, regularizer factor, and polynomial order) along with a plot of model's performance on the training data and test data. We expect this model to perform better than all prior models you trained.
"""

### YOUR CODE HERE ###

"""1. The features that are important are the Species since that is how we are going to identify them, the weight, Height, and width. These four features are the best due to the information they provide.
2. The polynomial order that is appropriate would be that of the degree of 2. The higher the degree the more polynomial complexity.
3. Regularization is very important and its impact is great since it makes sure that the variance of the model is small without really increasing its bias.
4. 
"""