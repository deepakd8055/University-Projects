# -*- coding: utf-8 -*-
"""ALC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mS9R1js7l_bi4NEQcM4DYZUWjrnge1Go
"""

from sklearn.svm import SVC, LinearSVC
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import imageio as io
import os
import warnings
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
from IPython.display import display
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import classification_report
from modAL.models import ActiveLearner
import matplotlib
from scipy import interp
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

def FeatureScaling(x_train, x_test):
    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)
    return x_train, x_test


def classification(classifier1,learner,x_new,y_new, cols):
  dicto = {}
  accuracyAvg = {}

  scores = []
  avgScores = 0.0
  count =1
  cv = KFold(n_splits=5, random_state=0, shuffle=True)
  print()
  for train_index, test_index in cv.split(x_new):
              print("Train and Test accuracy at",str(count)+"-Fold")
              x_train, x_test, y_train, y_test = x_new[train_index], x_new[test_index], y_new[train_index], y_new[test_index]
              x_train, x_test = FeatureScaling(x_train, x_test)
              classifier1.fit(x_train, y_train)
              y_pred = classifier1.predict(x_test)
              cm = confusion_matrix(y_test, y_pred)
              print("Train Accuracy: {:.2f}%".format(accuracy_score(y_train, classifier1.predict(x_train))*100))
              print("Test Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred)*100))
              print()
              scores.append(float("{:.2f}".format(accuracy_score(y_test, y_pred)*100)))
              avgScores += scores[-1]
              #cm = confusion_matrix(y_test, y_pred)
              cm = classification_report(y_test, y_pred)
              count += 1
  accuracyAvg["Test Accuracy"] = avgScores/5
  dicto["Test Accuracy"] = scores
  return avgScores/5, scores,cm

def ComparisionGraph(mean1, mean2):
  n_groups = 2
  means_allVariables = (mean1[0],mean1[1])
  means_subset_Variables = (mean2[0],mean2[1])

  # create plot

  fig, ax = plt.subplots(figsize=(8,10))
  ax.set_ylim([50, 100])
  index = np.arange(n_groups)
  bar_width = 0.25
  opacity = 0.8

  rects1 = plt.bar(index, means_allVariables, bar_width,
  alpha=opacity,
  color='b',
  label='All attributes')

  rects2 = plt.bar(index + bar_width, means_subset_Variables, bar_width,
  alpha=opacity,
  color='g',
  label='Subset attributes')

  
  plt.xlabel('Classification Algorithms')
  plt.ylabel('Accuracy')
  plt.title('Mean Accuracy Scores')
  plt.xticks(index + bar_width, ('RandomForest','K-Neighbors'))
  plt.legend()

  plt.tight_layout()
  plt.show()



cols=['MILLISEC', 'Acc_RKN_accX', 'Acc_RKN_accY', 'Acc_RKN_accZ', 'Acc_HIP_accX', 'Acc_HIP_accY', 'Acc_HIP_accZ', 'Acc_LUA_accX', 'Acc_LUA_accY', 'Acc_LUA_accZ', 'Acc_RUA_accX', 'Acc_RUA_accY', 'Acc_RUA_accZ', 'Acc_LH_accX', 'Acc_LH_accY', 'Acc_LH_accZ', 'Acc_BAC_accX', 'Acc_BAC_accY', 'Acc_BAC_accZ', 'Acc_RKN_accX_1', 'Acc_RKN_accY_1', 'Acc_RKN_accZ_1', 'Acc_RWR_accX', 'Acc_RWR_accY', 'Acc_RWR_accZ', 'Acc_RUA_accX_1', 'Acc_RUA_accY_1', 'Acc_RUA_accZ_1', 'Acc_LUA_accX_1', 'Acc_LUA_accY_1', 'Acc_LUA_accZ_1', 'Acc_LWR_accX', 'Acc_LWR_accY', 'Acc_LWR_accZ', 'Acc_RH_accX', 'Acc_RH_accY', 'Acc_RH_accZ', 'Ine_BAC_accX', 'Ine_BAC_accY', 'Ine_BAC_accZ', 'Ine_BAC_gyroX', 'Ine_BAC_gyroY', 'Ine_BAC_gyroZ', 'Ine_BAC_magneticX', 'Ine_BAC_magneticY', 'Ine_BAC_magneticZ', 'Ine_BAC_Quaternion1', 'Ine_BAC_Quaternion2', 'Ine_BAC_Quaternion3', 'Ine_BAC_Quaternion4', 'Ine_RUA_accX', 'Ine_RUA_accY', 'Ine_RUA_accZ', 'Ine_RUA_gyroX', 'Ine_RUA_gyroY', 'Ine_RUA_gyroZ', 'Ine_RUA_magneticX', 'Ine_RUA_magneticY', 'Ine_RUA_magneticZ', 'Ine_RUA_Quaternion1', 'Ine_RUA_Quaternion2', 'Ine_RUA_Quaternion3', 'Ine_RUA_Quaternion4', 'Ine_RLA_accX', 'Ine_RLA_accY', 'Ine_RLA_accZ', 'Ine_RLA_gyroX', 'Ine_RLA_gyroY', 'Ine_RLA_gyroZ', 'Ine_RLA_magneticX', 'Ine_RLA_magneticY', 'Ine_RLA_magneticZ', 'Ine_RLA_Quaternion1', 'Ine_RLA_Quaternion2', 'Ine_RLA_Quaternion3', 'Ine_RLA_Quaternion4', 'Ine_LUA_accX', 'Ine_LUA_accY', 'Ine_LUA_accZ', 'Ine_LUA_gyroX', 'Ine_LUA_gyroY', 'Ine_LUA_gyroZ', 'Ine_LUA_magneticX', 'Ine_LUA_magneticY', 'Ine_LUA_magneticZ', 'Ine_LUA_Quaternion1', 'Ine_LUA_Quaternion2', 'Ine_LUA_Quaternion3', 'Ine_LUA_Quaternion4', 'Ine_LLA_accX', 'Ine_LLA_accY', 'Ine_LLA_accZ', 'Ine_LLA_gyroX', 'Ine_LLA_gyroY', 'Ine_LLA_gyroZ', 'Ine_LLA_magneticX', 'Ine_LLA_magneticY', 'Ine_LLA_magneticZ', 'Ine_LLA_Quaternion1', 'Ine_LLA_Quaternion2', 'Ine_LLA_Quaternion3', 'Ine_LLA_Quaternion4', 'Ine_L-S_EuX', 'Ine_L-S_EuY', 'Ine_L-S_EuZ', 'Ine_L-S_Nav_Ax', 'Ine_L-S_Nav_Ay', 'Ine_L-S_Nav_Az', 'Ine_L-S_Body_Ax', 'Ine_L-S_Body_Ay', 'Ine_L-S_Body_Az', 'Ine_L-S_AngVelBodyFrameX', 'Ine_L-S_AngVelBodyFrameY', 'Ine_L-S_AngVelBodyFrameZ', 'Ine_L-S_AngVelNavFrameX', 'Ine_L-S_AngVelNavFrameY', 'Ine_L-S_AngVelNavFrameZ', 'Ine_L-S_Compass', 'Ine_R-S_EuX', 'Ine_R-S_EuY', 'Ine_R-S_EuZ', 'Ine_R-S_Nav_Ax', 'Ine_R-S_Nav_Ay', 'Ine_R-S_Nav_Az', 'Ine_R-S_Body_Ax', 'Ine_R-S_Body_Ay', 'Ine_R-S_Body_Az', 'Ine_R-S_AngVelBodyFrameX', 'Ine_R-S_AngVelBodyFrameY', 'Ine_R-S_AngVelBodyFrameZ', 'Ine_R-S_AngVelNavFrameX', 'Ine_R-S_AngVelNavFrameY', 'Ine_R-S_AngVelNavFrameZ', 'Ine_R-S_Compass', 'Acc_CUP_accX', 'Acc_CUP_accX_1', 'Acc_CUP_accX_1_1', 'Acc_CUP_gyroX', 'Acc_CUP_gyroY', 'Acc_SAL_accX', 'Acc_SAL_accX_1', 'Acc_SAL_accX_1_1', 'Acc_SAL_gyroX', 'Acc_SAL_gyroY', 'Acc_WAT_accX', 'Acc_WAT_accX_1', 'Acc_WAT_accX_1_1', 'Acc_WAT_gyroX', 'Acc_WAT_gyroY', 'Acc_CHE_accX', 'Acc_CHE_accX_1', 'Acc_CHE_accX_1_1', 'Acc_CHE_gyroX', 'Acc_CHE_gyroY', 'Acc_BRE_accX', 'Acc_BRE_accX_1', 'Acc_BRE_accX_1_1', 'Acc_BRE_gyroX', 'Acc_BRE_gyroY', 'Acc_KNI_accX', 'Acc_KNI_accX_1', 'Acc_KNI_accX_1_1', 'Acc_KNI_gyroX', 'Acc_KNI_gyroY', 'Acc_MIL_accX', 'Acc_MIL_accX_1', 'Acc_MIL_accX_1_1', 'Acc_MIL_gyroX', 'Acc_MIL_gyroY', 'Acc_SPO_accX', 'Acc_SPO_accX_1', 'Acc_SPO_accX_1_1', 'Acc_SPO_gyroX', 'Acc_SPO_gyroY', 'Acc_SUG_accX', 'Acc_SUG_accX_1', 'Acc_SUG_accX_1_1', 'Acc_SUG_gyroX', 'Acc_SUG_gyroY', 'Acc_KNI_accX_1_1_1', 'Acc_KNI_accX_1_1_1_1', 'Acc_KNI_accX_1_1_1_1_1', 'Acc_KNI_gyroX_1', 'Acc_KNI_gyroY_1', 'Acc_PLA_accX', 'Acc_PLA_accX_1', 'Acc_PLA_accX_1_1', 'Acc_PLA_gyroX', 'Acc_PLA_gyroY', 'Acc_GLA_accX', 'Acc_GLA_accX_1', 'Acc_GLA_accX_1_1', 'Acc_GLA_gyroX', 'Acc_GLA_gyroY', 'REE_SWI_DISHWASHE', 'REE_SWI_FRIDG', 'REE_SWI_FRIDG_1', 'REE_SWI_FRIDG_1_1', 'REE_SWI_MIDDLEDRAWE', 'REE_SWI_MIDDLEDRAWE_1', 'REE_SWI_MIDDLEDRAWE_1_1', 'REE_SWI_LOWERDRAWE', 'REE_SWI_LOWERDRAWE_1', 'REE_SWI_UPPERDRAWER', 'REE_SWI_DISHWASHE_1', 'REE_SWI_LOWERDRAWE_1_1', 'REE_SWI_DISHWASHE_1_1', 'Acc_DOO_accX', 'Acc_DOO_accY', 'Acc_DOO_accZ', 'Acc_LAZ_accX', 'Acc_LAZ_accY', 'Acc_LAZ_accZ', 'Acc_DOO_accX_1', 'Acc_DOO_accY_1', 'Acc_DOO_accZ_1', 'Acc_DIS_accX', 'Acc_DIS_accY', 'Acc_DIS_accZ', 'Acc_UPP_accX', 'Acc_UPP_accY', 'Acc_UPP_accZ', 'Acc_LOW_accX', 'Acc_LOW_accY', 'Acc_LOW_accZ', 'Acc_MID_accX', 'Acc_MID_accY', 'Acc_MID_accZ', 'Acc_FRI_accX', 'Acc_FRI_accY', 'Acc_FRI_accZ', 'LOC_TAG_X', 'LOC_TAG_Y', 'LOC_TAG_Z', 'LOC_TAG_X_1', 'LOC_TAG_Y_1', 'LOC_TAG_Z_1', 'LOC_TAG_X_1_1', 'LOC_TAG_Y_1_1', 'LOC_TAG_Z_1_1', 'LOC_TAG_X_1_1_1', 'LOC_TAG_Y_1_1_1', 'LOC_TAG_Z_1_1_1', 'Locomotion', 'HL_Activity', 'LL_Left_Arm', 'LL_Left_Arm_Object', 'LL_Right_Arm', 'LL_Right_Arm_Object', 'ML_Both_Arms']
filename = 'f1.dat'
warnings.filterwarnings('ignore')
indata1 = np.loadtxt(filename) # make sure the rest is ignored
dp1 = pd.DataFrame(data=indata1, columns=cols)

for i in range(2,7):
  filename = 'f'+str(i)+'.dat'
  indata2 = np.loadtxt(filename) # make sure the rest is ignored
  dp2=pd.DataFrame(data=indata2,columns=cols)
  dp1=pd.concat([dp1,dp2])



#Dropping the rows with no activities
dp1 = dp1.drop(dp1[((dp1['Locomotion']) == 0) & ((dp1['HL_Activity']) == 0) &((dp1['LL_Left_Arm']) == 0) &((dp1['LL_Left_Arm_Object']) == 0) &((dp1['LL_Right_Arm']) == 0) &((dp1['LL_Right_Arm_Object']) == 0) &((dp1['ML_Both_Arms']) == 0) ].index)

x = dp1.iloc[:,:-7].values
y = dp1.iloc[:,-7:].values


lis = list()
for i in y:
  string = ""
  left= "0,"
  right= "0,"
  both= "0,"
  hlact = "0,"
  
  if int(i[2]) != 0:
    left = "1,"
  if int(i[4]) != 0:
    right = "1,"
  if int(i[6]) != 0:
    both = "1," 
  string = str(int(i[0])) + ","  + left + right + both
  lis.append(string[:-1])
y_final = np.array(lis)



le = LabelEncoder()
y_final = le.fit_transform(y_final)


dp2 = dp1.drop(columns=['Locomotion', 'HL_Activity', 'LL_Left_Arm', 'LL_Left_Arm_Object', 'LL_Right_Arm', 'LL_Right_Arm_Object', 'ML_Both_Arms'])
dp2['label'] = y_final

x = dp2.iloc[:,:-1].values
y = dp2.iloc[:,-1].values

n_labeled_examples = x.shape[0]
training_indices = np.random.randint(low=0, high=n_labeled_examples -1, size=1000)


x_train = x[training_indices]
y_train = y[training_indices]

x_new = x[training_indices]
y_new = y[training_indices]

# Isolate the non-training examples we'll be querying.
x_pool = np.delete(x, training_indices, axis=0)
y_pool = np.delete(y, training_indices, axis=0)

#'''

classifier1 = RandomForestClassifier( n_estimators=50,n_jobs=-1,max_depth=50)
classifier2 = KNeighborsClassifier(n_neighbors=3)
learner = ActiveLearner(estimator=classifier1, X_training=x_train, y_training=y_train)


predictions = learner.predict(x)
is_correct = (predictions == y)
unqueried_score = learner.score(x, y)
print('Accuracy after first 1000 random rows: {acc:0.4f}%'.format(acc=unqueried_score*100))
performance_history = [unqueried_score]

count = 1
while(float(performance_history[-1]*100)<90):
    queryList = []
    query_index, query_instance = learner.query(x_pool,n_instances=1000)
    training_indices=np.concatenate([training_indices,query_index])
    x_temp, y_temp = x_pool[query_index], y_pool[query_index]
    x_new=np.concatenate([x_new,x_temp])
    y_new=np.concatenate([y_new,y_temp])
    learner.teach(X=x_temp, y=y_temp)
    x_pool, y_pool = np.delete(x_pool, queryList, axis=0), np.delete(y_pool, queryList)
    model_accuracy = learner.score(x, y)
    #if count%10 == 0:
    print('Accuracy after query {n}: {acc:0.2f}%'.format(n=count, acc=model_accuracy*100))

  # Save our model's performance for plotting.
    performance_history.append(model_accuracy)
    count += 1

fig, ax = plt.subplots(figsize=(8.5, 6), dpi=130)

ax.plot(performance_history)
ax.scatter(range(len(performance_history)), performance_history, s=13)

ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=5, integer=True))
ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=10))
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))

ax.set_ylim(bottom=0, top=1)
ax.grid(True)

ax.set_title('Classification accuracy at each iteration')
ax.set_xlabel('Iteration')
ax.set_ylabel('Classification Accuracy')

plt.show()

acc1 = []
new_cols = dp2.columns.tolist()
accu1, scores, cms = classification(classifier1,learner,x_new,y_new,new_cols)
print("Random Forest Classification:")
print("Scores at each fold:",scores)
print("Average Accuracy:",accu1)
print("Confusion matrix:",cms)

acc1.append(accu1)

#'''
accu1, scores, cms = classification(classifier2,learner,x_new,y_new,new_cols)
print("K-Means:")
print("Scores at each fold:",scores)
print("Average Accuracy:",accu1)
print("Confusion matrix:",cms)
acc1.append(accu1)



query_index, query_instance = learner.query(x_pool,n_instances=5000)
training_indices=np.concatenate([training_indices,query_index])
x_temp, y_temp = x_pool[query_index], y_pool[query_index]
x_new=np.concatenate([x_new,x_temp])
y_new=np.concatenate([y_new,y_temp])
#'''

feats = {}
for feature, importance in zip(dp1.columns, classifier1.feature_importances_):
	feats[feature] = importance
importances = pd.DataFrame.from_dict(feats, orient='index').rename(columns={0: 'Gini-Importance'})
importances = importances.sort_values(by='Gini-Importance', ascending=False)
importances = importances.reset_index()
importances = importances.rename(columns={'index': 'Features'})
sns.set(font_scale = 5)
sns.set(style="whitegrid", color_codes=True, font_scale = 1.7)
fig, ax = plt.subplots()
fig.set_size_inches(30,15)
sns.barplot(x=importances['Gini-Importance'], y=importances['Features'], data=importances, color='skyblue')
plt.xlabel('Importance', fontsize=25, weight = 'bold')
plt.ylabel('Features', fontsize=25, weight = 'bold')
plt.title('Feature Importance', fontsize=25, weight = 'bold')
display(plt.show())
display(importances)
print(type(importances))

compression_opts = dict(method='zip',
                        archive_name='out2.csv')  
importances.to_csv('out2.zip', index=False,
          compression=compression_opts) 

#'''
sum1=0
for i in range(len(importances)):
  if sum1 >0.9:
    print("New attributes count: ",i+1)
    sum1=i+1
    break
  else:
    sum1+= importances.loc[i][-1]

new_cols = cols[:-7]
new_cols.append('label')
ds = np.concatenate((x_new, y_new.reshape(-1,1)), axis=1)
df = pd.DataFrame(data=ds, columns=new_cols)

feat = importances.iloc[:sum1,:-1].values
indexAttr = []
for elementIndex in range(0, len(feat)):
    indexAttr.append(cols.index(feat[elementIndex][-1]))


nIndex = []
for i in range(0,len(new_cols)):
  if i not in indexAttr:
    nIndex.append(i)

df = df.drop(df.columns[nIndex], axis=1)
x_new = df.iloc[:,:].values

acc2 = []

accu1, scores, cms = classification(classifier1,learner,x_new,y_new,new_cols)
print("Random Forest Classification:")
print("Scores at each fold:",scores)
print("Average Accuracy:",accu1)
print("Confusion matrix:",cms)
acc2.append(accu1)

accu1, scores, cms = classification(classifier2,learner,x_new,y_new,new_cols)
print("K-Means:")
print("Scores at each fold:",scores)
print("Average Accuracy:",accu1)
print("Confusion matrix:",cms)
acc2.append(accu1)

ComparisionGraph(acc1,acc2)
#'''
