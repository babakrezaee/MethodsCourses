import pandas as pd

#Load: Daron Acemoglu, Simon Johnson, and James A Robinson. The colonial origins of comparative development: an empirical investigation. The American Economic Review, 91(5):1369–1401, 2001.
df1=pd.read_stata('https://github.com/QuantEcon/QuantEcon.lectures.code/raw/master/ols/maketable1.dta')

df1.head()

####
import matplotlib.pyplot as plt
#plt.style.use('seaborn')

df1.plot(x='avexpr', y='logpgp95', kind='scatter', color='crimson', marker='o')
plt.ylabel('log GDP per capita')
plt.xlabel('Protection against expropriation')
plt.xlim([3.3,10.5])
plt.ylim([4,10.5])
plt.xlabel('Average Expropriation Risk 1985-95')
plt.ylabel('Log GDP per capita, PPP, 1995')
plt.savefig('scatter.pdf', dpi=200)
plt.show()


### Now, let fit a linear function to this assoication using least square method, that is logpgp95i=β0+β1avexpri+u ###

# Dropping NA's is required to use numpy's polyfit
import numpy as np
df1_subset=df1.dropna(subset=['avexpr','logpgp95'])

#df1_subset.head()

df1_subset=df1_subset[df1_subset['baseco']==1]

X=df1_subset['avexpr']
y=df1_subset['logpgp95']
labels=df1_subset['shortnam']

####################Fit different polynomial models


plt.scatter(X,y, marker='')


for i, label in enumerate(labels):
    plt.annotate(label, (X.iloc[i], y.iloc[i]))

xp = np.linspace(3, 10, 100)

p2 = np.poly1d(np.polyfit(X, y, 2))
p3 = np.poly1d(np.polyfit(X, y, 3))
p10=np.poly1d(np.polyfit(X, y, 10))
p20=np.poly1d(np.polyfit(X, y, 20))


plt.plot(np.unique(X),
         np.poly1d(np.polyfit(X, y, 1))(np.unique(X)),
         color='red')

plt.plot(xp, p2(xp), 'y', xp, p3(xp), 'c', xp, p10(xp), 'g', xp, p20(xp), 'b')
plt.xlim([3.3,10.5])
plt.ylim([4,10.5])
plt.xlabel('Average Expropriation Risk 1985-95')
plt.ylabel('Log GDP per capita, PPP, 1995')
plt.title('Figure 2: OLS relationship between expropriation risk and income')
plt.savefig('Scatter_Models.pdf', dpi=200)

plt.show()



############Fitting OLS model#####


plt.scatter(X,y, marker='')


for i, label in enumerate(labels):
    plt.annotate(label, (X.iloc[i], y.iloc[i]))



plt.plot(np.unique(X),
         np.poly1d(np.polyfit(X, y, 1))(np.unique(X)),
         color='red')

plt.xlim([3.3,10.5])
plt.ylim([4,10.5])
plt.xlabel('Average Expropriation Risk 1985-95')
plt.ylabel('Log GDP per capita, PPP, 1995')
plt.title('Figure 2: OLS relationship between expropriation risk and income')
plt.savefig('Scatter_OLS.pdf', dpi=200)

plt.show()
