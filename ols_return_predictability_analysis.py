# -*- coding: utf-8 -*-
"""OLS Return Predictability Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dXxcwRFSRfrbyOxC8MfMbATzK7iCcz9l

# OLS Return Predictability Analysis

In this notebook we will analyze some of the more popular variables used to predict equity market returns.

The packages I will use are mostly the same as before.  Regressions are done with statsmodels.api.  This is slightly different from statsmodels.formula.api.  They each have an OLS regression function, but they are used in different ways.  Both are useful in certain situations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

"""The data we're going to read in comes from Amit Goyal's website.  It includes a number of variables that are useful in predicting future returns.  It also includes the returns themselves."""

predictors = pd.read_excel('PredictorData2023.xlsx',sheet_name='Monthly',index_col=[0])
predictors.head()

"""The data go back a long way!  Let's focus on a more modern sample to try to make this more relevant."""

predictors = predictors.loc[195001:]
predictors.head()

"""The predictors dataset represents my entire sample.  If I am running a backtest, I want to pretend that today is sometime during that sample and perform the data analysis that would have been feasible at that time.

Before we get into a full analysis, let's look at an example. Suppose it is the very end of 2012.  I will create a data frame pred2012 that includes this data. NOte that this includes everything from 1950 up until 2012. We could also use a rolling window -- say, the last 10 years. In that case we would select the data from [200212:201212].
"""

pred2012 = predictors.loc[:201212]

"""Next, I will add a few variables that might be interesting.  One is the ratio of earnings to prices.  The other is the 12-month MA of inflation:"""

pred2012['ep']     = pred2012['e12']/pred2012['price']
pred2012['infl12'] = pred2012['infl'].rolling(12).mean()

"""Now I will just keep the data that I care about, which includes these columns, a few other predictors, and the market return:"""

pred2012 = pred2012[['ep','infl12','lty','ntis','ret']]

"""Predictive regressions are of the form
$$ R_{t+1} = \alpha + \beta X_t + \epsilon_{t+1}$$
It is important that the dependent variable is later than the independent variable.  We are trying to predict returns with X, so we need to be able to see X before the investment is made.

I can either _lag_ the X variables or _lead_ the returns.  Either way is fine.  I usually do the former, but this time I'll do the latter, which is accomplished with shift(-1):
"""

pred2012['ret']=predictors['ret'].shift(-1)

"""Since shift(-1) will create some missing values, I will use dropna:"""

pred2012.dropna(inplace=True)

"""Let's run a regression.  I'll use statsmodels.formula.api, which allows you to specify your regression equation.  Also, smf.ols automatically adds a constant to the regression, which is usually convenient.

In my regression, I will regress future returns on the current E/P ratio:
"""

results = smf.ols('ret ~ ep + infl12', data=pred2012).fit()
print(results.summary())

"""The t-stats indicate strong statistical significance, but the R-square is not super high.  The predictability here is not huge.

Maybe we will find more predictability using the other two predictors, lty (long-term bond yield) and ntis (net share issuance).
"""

results = smf.ols('ret ~ ep + infl12 + lty + ntis', data=pred2012).fit()
print(results.summary())

"""The same OLS regression can also be run using sm.OLS.  (The capitalization in "sm.OLS" is required.)  This time, we give the function our dependent variable and our independent variables as separate arguments.  In addition, the function does not automatically assume that we want to include a constant.  Instead, we have to use the sm.add_constant function to add a constant to our predictors."""

Y = pred2012['ret']
X = pred2012[['ep','infl12','lty','ntis']]
X.head()

sm.add_constant(X).head()

"""We can run the regression using sm.OLS as follows:"""

results2 = sm.OLS(Y, sm.add_constant(X)).fit()
print(results2.summary())

"""The results turn out to be the same, of course.

Let's now consider briefly how you would run a regression on a subset of the variables in the dataframe, for example those that have a higher correlation with the dependent variable. This is in line with what Hull and Qiao recommend.

We can compute the correlation between Y and each column of X with
"""

rho=X.corrwith(Y)
print(rho)

"""Note that rho is a series:"""

type(rho)

"""We can therefore use the loc property to subset the rows of rho, for example to find rows that have a high enough absolute correlation.  (I'm using .05 here instead of .1 since there aren't any correlations above .1 in absolute value.)"""

rhokeep = rho.loc[np.abs(rho)>.05]
print(rhokeep)

"""If we want to know what the indexes are of the high correlation variables, we can see them by typing"""

rhokeep.index

"""It looks like we might want to drop lty and ntis.  We can pull out the desired columns out of the X dataframe using the standard method:"""

Xsub=X[rhokeep.index]
Xsub.head()

"""With the subset of predictors that we want to keep, we can come up with a slightly more parsimonious regression.  

The nice thing about sm.OLS, as opposed to smf.ols, is that we can just give it the entire Xsub dataframe without having to write out the model describing which independent variables we want it to include:
"""

results4 = sm.OLS(Y, sm.add_constant(Xsub)).fit()
print(results4.summary())

"""__Now let's Look at the larger set of predictors. We won't do anything too fancy but will consider a "kitchen sink" approach.__

I'll pull the data through 2014 and drop the fields where there are no monthly values.
"""

pred2014 = predictors.loc[:201214]
pred2014.drop(['gpce','gip','house','eqis','cay','i/k','pce','govik','skew','crdstd','accrul','cfacc'],axis=1,inplace=True)
pred2014['infl12'] = pred2014['infl'].rolling(12).mean()
pred2014['ret']=predictors['ret'].shift(-1)
pred2014.dropna(inplace=True)
print(pred2014.columns)

Y=pred2014['ret']
X=pred2014.drop(['retx','ret','price'],axis=1)

Y.head()

"""This gives us a pretty good r-squared. But we have some problems still. First, this is not a true walk-forward analysis. This is using data all the way through 2014 to estimate the coefficients, and the r-squared applies those coefficients to predictions made at every month along the way. But we don't know the information used to estimate the coefficients yet. A true walk-forward analysis will reestimate the coefficients every month along the way."""

results5 = sm.OLS(Y, sm.add_constant(X)).fit()
print(results5.summary())

"""Also note that there is strong multicollinarity problems -- we have a bunch of redundant regressors in here. That's shown through the correlation of the x-variables with one another.

First let's thin down the list of regressors a little bit more
"""

rho=X.corrwith(Y)
print(rho)

rhokeep = rho.loc[np.abs(rho)>.15]
Xsub=X[rhokeep.index]
Xsub.head()

results6 = sm.OLS(Y, sm.add_constant(Xsub)).fit()
print(results6.summary())

Xsub.corr()

"""We can see a lot of very correlated regressors in here. Something like principle components could be one way to distill this list down to a smaller handful of regressors while maintaining high r-squared."""
