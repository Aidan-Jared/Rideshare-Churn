## Case Study

Today we are going to use all the skills we have learned to tackle a real
problem in industry. The problem is churn prediction with a ride-sharing
company in San Francisco.  Since the data is sourced from a real company, we
ask you not to share the dataset. See more about the problem in
[group.md](group.md). 

# Rideshare Churn
### Aidan Jared, Derek Lorenzen, Nathan James

## EDA
As any good data scientist we first did some EDA to understand the data structure and what the featers are. Thankfully the [included markdown](group.md) explained the data which speed up the EDA. The data set was made up of 11 features and the point at which and individual churned was if they had not used the rideshare for more than 30 days. With this information we moved onto the data cleaning.

## Cleaning
For the cleaning our first dessision was to remove the surge_pct feature because there was also a surge_avg column and we felt that including both features would have produced multicolinarity in the model which is never desired. After this dessision we developed a cleaning function in order to clean both the training and testing data the same way. 
```python
def clean(df, drop_list):
    df_ = df.drop(drop_list, axis=1)
    cities = list(df_['city'].unique())
    for index, i in enumerate(cities):
        df_['city'].where(df_['city'] != i, index + 1, inplace=True)
    phones = df_['phone'].unique()
    for index, i in enumerate(phones):
        df_['phone'].where(df_['phone'] != i, index + 1, inplace=True)
    df_['signup_date'] = pd.to_datetime(df_['signup_date'], infer_datetime_format=True)
    df_['last_trip_date'] = pd.to_datetime(df_['last_trip_date'], infer_datetime_format=True)
    date = pd.to_datetime('20140601', infer_datetime_format=True)
    df_['churn'] = df_['last_trip_date'] >= date
    df_ = df_.drop(['signup_date','last_trip_date'], axis=1)
    df_ = df_.fillna(0)
    return df_
```

The thing the cleaning function did is that it when through the two catigorical features, city and phone, and then changed the values into intigers so that sklearn could take them as inputs and produce a model. After this we changed to last_trip_date column to a date time object so we could start the creation of our y column. Then we took the cutoff date and made the y by figuring out which individuals haven't used rideshare for more than 30 days. With this done it was time to move onto random forest.

## Random Forest

As a group we decided that random forest would be a good model to work with first because it is easy to set up and produce a good random forest in the time that we had.

```python
rf = RandomForestClassifier(n_estimators=100, random_state=1, oob_score=True, bootstrap=True)
rf.fit(X_train_s, y_train_s)
y_pred = rf.predict(X_test_s)

```
We set the number of estimators to be 100 and left the max number of features to be the default. The following is a plot of the feature importance that the model produced
![alt text](images/random_forest_feature_imp.png)

on top of this we found the following performance metrix that we started using to tune our model
|Metrics|
|:-----:|
|acc:  0.755|
|pres:  0.6741225051617343|
|recall:  0.6591520861372813|
|oob:  0.751625|
and the confusion matrix:

![alt text](images/confusion.png)

What these values show is that our first model predicts better than random guessing but still produces a lot of false negatives and nees more fine tuning to produce a better model.

Our last step in random forest was to fine tune our model to see if we could produce better results. As such we ran a for loop iterating through multiple max features to find what we should set this to be in our final model. After our test of this we found that only using one feature produced the hightest acuracy which couldn't be right. After talking it over and getting some help we tested the same code with multiple random states to see how noise effects the acuracy.
![alt text](images/acc_v_feats.png)
as you can see there flutuations depending on the random state that is used but, it seems to be that using 8 features tends to produce the highest acuracy even though there is very little difference between the models.

## Roc Curve

## Boosting

## Conclusion