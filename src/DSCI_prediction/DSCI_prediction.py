import pandas as pd
import numpy as np
import argparse
from plot_hist import plot_hist_overlay
from plot_boxplot import boxplot_plotting
import matplotlib.pyplot as plt


import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (confusion_matrix, ConfusionMatrixDisplay)


import seaborn as sns


import sklearn


def EDA_plot(train_df, hist_output, boxplot_output):
    train_df = pd.read_csv(str(train_df))
    X_train = train_df.drop(columns=["class"])
    numeric_looking_columns = X_train.select_dtypes(
        include=np.number).columns.tolist()
    benign_cases = train_df[train_df["class"] == 0]
    malignant_cases = train_df[train_df["class"] == 1]
    #plot histogram
    fig = plot_hist_overlay(df0=benign_cases, df1=malignant_cases,
                 columns=numeric_looking_columns, labels=["0 - benign", "1 - malignant"],
                 fig_no="1")
    fig.savefig(str(hist_output), facecolor="white")
    #plot boxplot 
    fig2 = boxplot_plotting(3, 3, 20, 25, numeric_looking_columns, train_df, 2)
    fig2.savefig(str(boxplot_output), facecolor="white")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plots EDA")
    parser.add_argument("train_df", help="Path to train_df")
    parser.add_argument("hist_output", help="Path to histogram output")
    parser.add_argument("boxplot_output", help="Path to boxplot output")
    args = parser.parse_args()
    EDA_plot(args.train_df, args.hist_output, args.boxplot_output)
    
    
    
def plot_cm(model, X_train, y_train, X_test, y_test, title):
    """
    Returns confusion matrix on predictions of y_test with given title 
    of given model fitted X_train and y_train 
    -----------
    PARAMETERS:
    model :
        scikit-learn model or sklearn.pipeline.Pipeline
    X_train : numpy array or pandas DataFrame/Series
        X in the training data
    y_train : numpy array or pandas DataFrame/Series
        y in the training data
    X_test : numpy array or pandas DataFrame/Series
        X in the testing data
    y_test : numpy array or pandas DataFrame/Series
        y in the testing data
    -----------
    REQUISITES:
    X_train, y_train, X_test, y_test cannot be empty.
    -----------
    RETURNS:
    A sklearn.metrics._plot.confusion_matrix.ConfusionMatrixDisplay object 
    -----------
    Examples

    plot_cm(DecisionTreeClassifier(), X_train, y_train, X_test, y_test, "Fig")
    """
    if not isinstance(X_train, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'X_train' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(y_train, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'y_train' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(X_test, (pd.core.series.Series,
                               pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'X_test' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(y_test, (pd.core.series.Series,
                               pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'y_test' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(title, str):
        raise TypeError("'title' should be of 'str'")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    cm = confusion_matrix(y_test, predictions, labels=model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=model.classes_)
    disp.plot()
    plt.title(title)
    return disp


def boxplot_plotting (num_rows,num_columns,width,height,variables,datafr,number):
    """
    A function which returns a given number of boxplots for different target  against each numerical feature. The returning objects are seaborn.boxplot types. 
    
    -------------------
    PARAMETERS:
    A dataframe containing the variables and their correspondent labels
    Variables: A list of each variable's name
    num_rows and num_columns: An integer and positive number for both num_rows and num_columns for the
    boxplot fig "canvas" object where our boxplots will go,
    width: A positive width measure 
    length: A positive length measure 
    A binary class label 
    A column array for managing variable names
    A training dataframe object
    Integer positive number for correct ordering  of graphs 
    -------------------
    REQUISITES:
    The target labels ("class label") must be within the data frame 
    The multiplication between num_rows and num_columns must return be equal to num_variables.
    It is possible for num_rows & num_columns to be values that when multiplied don't equal the "variables" numeric value,
    but that will create more boxplots which will be empty. 
    

    --------------------
    RETURNS:
    It returns a fixed number "num_variables" of boxplot objects. Each Boxplot represents both Target Class
    Labels according to a given Variable

    --------------------
    Examples

    datafr=train_df
    --------
    boxplot_plotting (3,3,20,25,numeric_column,datafr,number)
    """
    fig,ax= plt.subplots(num_rows,num_columns,figsize=(width,height))
    for idx, (var,subplot) in enumerate(zip(variables,ax.flatten())):
        a = sns.boxplot(x='class',y=var,data=datafr,ax=subplot).set_title(f"Figure {number}.{idx}: Boxplot of {var} for each target class label")
    return fig



def tuned_para_table(search, X_train, y_train):
    """
    A function which returns a panda dataframe of tuned hyperparameters
    and its best score given GridSearchCV object fitted X_train and y_train
    -------------------
    PARAMETERS:
    search: A sklearn.model_selection._search.GridSearchCV that has been
    specified estimator, param_grid, **kwargs
    X_train : numpy array or pandas DataFrame/Series
        X in the training data
    y_train : numpy array or pandas DataFrame/Series
        y in the training data
    --------------------
    REQUISITES:
    X_train, y_train must at least n_splits (specified in cv in search)
    observations for each target class.
    search must be GridSearchCV object that is clearly specified with
    estimator, param_grid, cv, and so on.
    --------------------
    RETURNS:
    Returns a pandas.core.frame.DataFrame object that specifies
    the tuned hyperaparameters and the best score produced by GridSearchCV
    --------------------
    Examples

    search = GridSearchCV(KNeighborsClassifier(),
                      param_grid={'kneighborsclassifier__n_neighbors':
                      range(1, 10)},
                      cv=10, 
                      n_jobs=-1,  
                      scoring="recall", 
                      return_train_score=True)
    --------
    tuned_para_table(search, X_train, y_train)
    """
    if not isinstance(search, sklearn.model_selection._search.GridSearchCV):
        raise TypeError("'search' should be of type GridSearchCV")
    if not isinstance(X_train, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'X_train' should be of type np.array or pd.Dataframe")
    if not isinstance(y_train, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'y_train' should be of type np.array or pd.Dataframe")
    search.fit(X_train, y_train)
    best_score = search.best_score_.astype(type('float', (float,), {}))
    tuned_para = pd.DataFrame.from_dict(search.best_params_, orient='index')
    tuned_para = tuned_para.rename(columns = {0 : "Value"})
    tuned_para = tuned_para.T
    tuned_para['best_score'] = best_score
    return tuned_para
