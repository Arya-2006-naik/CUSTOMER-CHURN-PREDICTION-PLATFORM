import pandas as pd 
df =pd.read_csv('Telco-Customer-Churn.csv',sep='\t')
print(df.head())

#cleaning data
print(df.isnull().sum())
df['Churn']=df['Churn'].map({'Yes':1,'No':0})
print(df [['Churn']].head())

#dropping customerID and getting dummies(numeric values for text)
df=df.drop('customerID',axis=1)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df=pd.get_dummies(df)
X=df.drop('Churn',axis=1)
y=df['Churn']
print(X.shape)
print(y.shape)
print(df.columns)

#splitting data into training and testing data
from sklearn.model_selection import train_test_split
X_train,X_test,y_train, y_test=train_test_split(X,y,test_size=0.2,random_state=42)
print('Training features shape:',X_train.shape)
print('Training features shape :', X_test .shape )
print('Training labels shape:',y_train.shape)
print('Training labels shape :', y_test .shape)

#training the model
from sklearn.ensemble import RandomForestClassifier
model=RandomForestClassifier()
model.fit(X_train,y_train)
print('Model training completed')

#testing the model
y_pred=model.predict(X_test)
print('Prediction completed')

#Accuracy of the model
from sklearn.metrics import accuracy_score
accuracy= accuracy_score(y_test, y_pred)
print('Model Accuracy:',accuracy)

#Saving the model
import joblib
joblib.dump(model,'churn_model.pkl')
print('Model saved successfully as churn_model.pkl')


    









