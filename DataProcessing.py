# -*- coding: utf-8 -*-

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AkM2glgmrNOosWnesknVMyAAdljqcGUo
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

"""## Problem 1 -  Use of List Comprehensions

### a) Use list comprehensions to create a list of all the indices of the 2's in the *number_list* you randomly generate (numbers between 1 and 10). (1 point)
"""

from numpy.random import randint, seed

# Set the seed so the same random numbers will be generated.
seed(42)   # DON'T CHANGE

### YOUR CODE HERE ###
number_list = randint(0,10, 100, int)

indexlist = [x for (x,j) in enumerate(number_list) if j == 2]
print(indexlist)

"""### b) Generate a list of the sum of the numbers that come up when a pair of dice is cast 22 times. Find the mean and standard deviation of these numbers. (3 points)"""

from numpy import mean, std

seed(117)   # DON'T CHANGE
sums = []
for x in range(0,22):
  number1 = randint(1,7)
  number2 = randint(1,7)
  sums.append(number1 + number2)
  
print('mean =', mean(sums), '    std =', std(sums))

"""### c) Generate a list of the sum of the numbers that come up when a pair of dice is cast 100000 times. Find the mean and standard deviation of these numbers. (3 points)"""

seed(111)   # DON'T CHANGE

sums = []
for x in range(0,100000):
  number1 = randint(1,7)
  number2 = randint(1,7)
  sums.append(number1 + number2)

print('mean =', mean(sums), '    std =', std(sums))

"""### d) Write down your conclusion from the observations you made in this question. (6 points)

The conclusion I am able to draw from the observations in this question are that, when asking for the mean both numbers come out to be around the average of the two dice which is 6-7ish. Also having the pair of dice cast 100000 times is unnecessary since both results of the mean and standard deviation do not change by that much. There are no outliers in this question since it a set amount of dice we are told to choose from. The data received is fairly simple and straight forward and python is a good language to use since it is easy to analyze the data.

## Problem 2 - Data Processing on Heart Disease Data

When a data scientist first encounters a new dataset, the first step is data exploration. The dataset we will be using is derived from the Heart database from the UCI Machine Learning Repository.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""### a) Read in the Data (2 points)
We are showing you a way to load data into your Colab file! Just run the next couple of code blocks. You'll have to paste your authorization code at one point...

"""

!pip install PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

downloaded = drive.CreateFile({'id':"1qF_Ees7ETr5BiPnHTabyeIH1KQVkViUK"})   # Replace the id with id of file you want to access
downloaded.GetContentFile('Heart.csv')        # Replace the file name with your file

# Finally we can actually read in the data.
data = pd.read_csv('Heart.csv')

# How many rows and columns are in this dataset?

data.info()

"""Number of rows: 306

Number of columns: 15

### b) Using Dataframe functionalities, provide a brief description of the data. The description can include (but not limited to): number of features, data type of each feature, statistics on numerical features, potential data cleaning tasks that needs to be done based on the data. (8 points)
"""

data.describe(None, 'all', None, False)

"""The number of features are 14(not 15 because the first row is just numbering off each seperate data segment.) Most of the data types are integers, but some are objects. Almost all features have the max amount of results except for Ca and Thal, with Ca missing 4 and Thal missing 2. Some cleaning needs to be done since there are a few outliers spotted in the data. We also see the NaN throughout all the data basically meaning the specific type of the column is not found for the data provided.

### c) Understanding the Data (12 points)

Look for a data description file whenever you explore a new dataset. This is a codebook (or text file) that tells you what each data item represents. The following link includes the data dictionary for this dataset: [Data Codebook](https://archive.ics.uci.edu/ml/datasets/heart+Disease)
"""

# Show the first few rows of the data.
data1 = data.head(3)
print(data1)

# Print out the "info" of the dataset.
print(data.info())

"""The above output can help you to see how much missing data is in the dataset. How many null values (missing values) exists in the data?

There are 6 total null values also known as missing values, 4 from Ca and 2 from Thal.

What to do about missing values is very good question. Sometimes one replaces such missing values with the mean of all the values that are present for this variable. But to keep things simple here we will simply delete any rows with missing data.

Use the code cell below to drop null values from the data. [hint: you can use dropna() function]
"""

# Drop any rows with missing data
data.dropna(0)

"""Another useful Pandas dataframe method is describe(). The describe method gives summary statistics for each column, which can help you to identify outliers."""

# The describe method of a Pandas dataframe yields much useful information.
data.describe()

"""Outliers are values far from the other data values (the distribution of the data), and are usually typos or other errors (such as measurement error). Looking at the data description above, do you spot any possible outliers in the data?

Two outliers that I see are first the max Age is 222 which is almost 100 years more than anyone has ever lived. The second outlier spotted is RestBP is 2444 which is not possible making it an outlier. Not entirely sure, but another outlier is OldPeak when the max is 21.2 and the mean and std are both less than 2.

### d) Outlier Detection \& Elimination (15 points)
In this section, We'll remove any ages that are more than 4 standard deviations from the mean.

To accomplish this: 

1) You'll make a new column called AgeZ to hold the z-transformed values of the Age column. 


2) Then, any AgeZ value that's less than -4 or more than 4 should be flagged as an outlier. 


3) Remove those entries from the dataset.

Remember that standardizing the data (or z-transform) is making your data have a zero mean and unit variance. This can be done with:

$$x \to_{stdize}  \frac{x - \mu}{\sigma}$$
Where $\mu$ is your mean and $\sigma$ is your standard deviation.
"""

data['AgeZ'] = (data['Age'] - data['Age'].mean())/data['Age'].std()

# Delete any rows for which AgeZ is greater than 4 or less than -4.

indexes = data[ data['AgeZ'] > 4 ].index
data.drop(indexes, inplace=True) 
indexes1 = data[ data['AgeZ'] < -4 ].index
data.drop(indexes1, inplace=True) 

# Cleanup - delete the z-tranform column since we don't need it any more.
data = data.drop(columns = ['AgeZ'])

# Let's take another look using the describe function.

data.describe()

"""Notice that now the Age column is much more reasonable. Report Mean, Standard Deviation, Q1, Q2, and Q3 of the age column before outlier removal and after outlier removal.

(Before) The mean is 54.924837 and the std is 13.164193 Q1 is 47.25, Q2 is 55.5, and Q3 is 61. (After) The mean is 54.377049 and the std is 9.041141. Q1 is 47, Q2 is 55, and Q3 is 61.

Perform the same process to eliminate any extreme outliers (more than 4 standard deviations away from the mean) for RestBP, MaxHR, and the Oldpeak variables. Delete those exta columns after you have removed the outliers.
"""

data['RestBPZ'] = (data['RestBP'] - data['RestBP'].mean())/data['RestBP'].std()
data['MaxHRZ'] = (data['MaxHR'] - data['MaxHR'].mean())/data['MaxHR'].std()
data['OldpeakZ'] = (data['Oldpeak'] - data['Oldpeak'].mean())/data['Oldpeak'].std()

# Delete any rows for which AgeZ is greater than 4 or less than -4.

indexes0 = data[ data['RestBPZ'] > 4 ].index
data.drop(indexes0, inplace=True) 
indexes11 = data[ data['RestBPZ'] < -4 ].index
data.drop(indexes11, inplace=True) 
indexes2 = data[ data['MaxHRZ'] > 4 ].index
data.drop(indexes2, inplace=True) 
indexes3 = data[ data['MaxHRZ'] < -4 ].index
data.drop(indexes3, inplace=True)
indexes4 = data[ data['OldpeakZ'] > 4 ].index
data.drop(indexes4, inplace=True) 
indexes5 = data[ data['OldpeakZ'] < -4 ].index
data.drop(indexes5, inplace=True)

# Cleanup - delete the z-tranform column since we don't need it any more.
data = data.drop(columns = ['RestBPZ'])
data = data.drop(columns = ['MaxHRZ'])
data = data.drop(columns = ['OldpeakZ'])


# Leave this for your last line.
data.describe()

"""For the columns RestBP, MaxHR, and Oldpeak, report Mean, Standard Deviation, Q1, Q2, and Q3 of the age column before outlier removal and after outlier removal.

RestBP(Before) The mean is 139.267974 and the std is 133.345625 Q1 is 120, Q2 is 130, and Q3 is 140. (After) The mean is 131.634551 and the std is 17.569462. Q1 is 120, Q2 is 130, and Q3 is 140.
MaxHR(Before) The mean is 150.075163 and the std is 26.962832 Q1 is 133, Q2 is 153, and Q3 is 166.75. (After) The mean is 149.594684 and the std is 22.944466. Q1 is 133, 153 is 55, and 166 is Q3.
Oldpeak(Before) The mean is 1.113072 and the std is 1.634994 Q1 is 0, Q2 is 0.8, and Q3 is 1.6. (After) The mean is 1.020598 and the std is 1.125570. Q1 is 0, Q2 is 0.8, and Q3 is 1.6.

### e) Data Visualization (4 points)

Sometimes it is useful to look at a pairwise plot of all the variables. Below we do this for all but the first column. Be patient, this takes a minute to complete. Notice that the main diagonal has histogram plots for each variable, which gives you a sense of the distribution of values of each variable.
"""

# Make a pairplot of all the variables (columns), excepting the first column.
plt.rcParams['figure.figsize'] = (15, 15)
sns.pairplot(data.drop(columns='Unnamed: 0'))

"""Let's look at a larger plot of the patient age distribution for the patients in this dataset."""

# Plot the patient age distribution.
plt.rcParams['figure.figsize'] = (7, 4)
sns.distplot(data['Age'])
plt.title('Age Distribution')

"""Plot the distribution of patient cholesterol levels."""

plt.rcParams['figure.figsize'] = (7, 4)
sns.distplot(data['Chol'])
plt.title('Patient Cholesterol Levels')

"""### f) Data Normalization (6 points)

We have already seen how the z-transform can be used to rescale values. We used this to help eliminate outliers, but such transforms can also be useful prior to applying machine learning algorithms, and often improves the algorithms performance. 

Another common transform is to map all the variable values into the interval $[0,1]$, via the transform:

$$x \to  \frac{x - \min}{\max - \min}$$

Let's create a new column ('NewAge') mapping all ages into the interval $[0,1]$.
"""

# Create a new column, NewAge, to hold the normalized Age variable.
data['NewAge'] = (data['Age'] - data['Age'].min())/(data['Age'].max() - data['Age'].min())

# Take a look at the new age column.
data['NewAge']
data.describe()

# We don't need this column, so we delete it. (It was just to show you how to do this.)
data = data.drop(columns=['NewAge'])

"""Map the minimum to 0 and maximum to 1 (in other words, normalize the column) for the RestBP, Chol, and MaxHR columns. Don't create new columns, just replace the existing ones with the transformed data."""

data['RestBP'] = (data['RestBP'] - data['RestBP'].min())/(data['RestBP'].max() - data['RestBP'].min())
data['MaxHR'] = (data['MaxHR'] - data['MaxHR'].min())/(data['MaxHR'].max() - data['MaxHR'].min())
data['Chol'] = (data['Chol'] - data['Chol'].min())/(data['Chol'].max() - data['Chol'].min())


# Leave this for your last line.
data.describe(None, 'all', None, False)

"""### g) Converting Categorical Data to Numeric Values (3 points)

It is frequently useful to convert categorical (non-numeric) values to numeric ones. The last variable in the data frame, AHD, has categorical values 'No' if the patient has no heart disease, and 'Yes' if they do. Convert these values to 0 for 'No' and 1 for 'Yes'.
"""

AHD_dict = {AHD_name:i for i,AHD_name in enumerate(data['AHD'].unique())}
def integer_encode_AHD_name(AHD_name):
    return AHD_dict[AHD_name]
data['AHD'] = data['AHD'].apply(integer_encode_AHD_name)
data.describe(None, 'all', None, False)

"""### h) One-Hot-Encoding (10 points)

One-hot-encoding is another often used way of converting categorical data to numeric. For example, instead of the categories 'cold', 'warm', 'hot', we form a seperate column for each of these attributes, so that what was represented as 'cold' is now $[1,0,0]$ and what was 'hot' is now $[0,0,1]$.  There is a built in command for doing this in the sklearn package.

Similar to what you have learned from the class exercise of lecture 2, add new columns for one-hot-encoding of 'Thal' column. Use 'Thal' as the prefix. Then drop the original column.
"""

# Concatentate new one-hot encodings with the original dataframe.
data = pd.concat([data,pd.get_dummies(data['Thal'], prefix='Thal')],axis=1)

# Now drop the original 'Thal' column (you don't need it anymore)

data = data.drop(columns=['Thal'])

data.head()

"""Create a one-hot-encoding for the ChestPain column, just as we did above for the Thal column, deleting the original column as before."""

data = pd.concat([data,pd.get_dummies(data['ChestPain'], prefix='ChestPain')],axis=1)

data = data.drop(columns=['ChestPain'])


# Leave this for your last line.
data.head()

"""### i) Feature Engineering (7 points)

Feature engineering is central to much of machine learning. Traditionally such features needed to be hand crafted, which is as much an art as it is engineering. One of the huge advantages of neural networks over traditional machine learning techniques is that neural networks can learn optimal features.

Create a new column (feature) called AgeC, which will be the product of the patient's age and the patient's cholesterol level.
"""

data['AgeC'] = data['Age']*data['Chol']


# Leave this for your last line.
data.head()

"""###  j) Balanced or Unbalanced Classes (8 points)

For this dataset, one variable that we might like to predict is the presence of heart disease, the AHD column, using all the other columns. Some datasets are highly imbalanced.  Suppose that 95% of a set of subjects were healthy, with only 5% having heart disease. A machine learning model can attain 95% accuracy by simply ALWAYS predicting no heart disease. It sounds like a fairly accurate model, but it would miss predicting any heart disease! 

There are techniques for dealing with this, but first we have to ascertain if our data is unbalanced. Use the code cell below to see if the data is imbalanced or not and describe your observations in the next text cell.
"""

data.hist(column='AHD')
#sns.distplot(data['AHD'])

"""Here we see a histogram of the column AHD which shows that just over 160 people of data points do not have AHD while just under 140 do. This to me seems like balanced data since there are just two options for the data and they are both relatively near each other in terms of the amounts of people who have AHD and the people who do not.

### k) Outline potential solutions to banalnce the data in the next cell, and implement one of those techniques in the code cell that follows. By plotting the distribution or in some other way, indicate how your technique helped create a more balanced dataset. (12 points)

A couple ways to balance the data are resample the training set, resample the data using different ratios, as well as undersampling and oversampling. Using undersampling I was able to balance the data seen in the histogram below, where both data bars are the same producing the same data.
"""

from sklearn.utils import resample
data_majority = data[data['AHD']==0]
data_minority = data[data['AHD']==1]
 
data_majority_downsampled = resample(data_majority, 
                                 replace=False,    
                                 n_samples=138)
 
data_downsampled = pd.concat([data_majority_downsampled, data_minority])
 
data_downsampled['AHD'].value_counts()
data_downsampled.hist(column='AHD')