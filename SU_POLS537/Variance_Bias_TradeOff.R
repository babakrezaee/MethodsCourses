library(kknn)
x=c()
y=c()
N=1000
set.seed(1364)
fn=function(x){return (cospi(x))}
for (i in 1:N){
x[i]=rnorm(1,2,1)
y[i]=fn(x[i])+rnorm(1,0,.5)
}
plot(x,y,col="gray45")


kvec=c(5,40,150)
nsim=30
fit1=rep(0,nsim)
fit2=rep(0,nsim)

fit3=rep(0,nsim)
train = data.frame(x,y)
test = data.frame(x=sort(x))
par(mfrow=c(2,3))
ntrain=200
fitind = 400
ylm = c(-.5,1.5)
kfit1_fitted=matrix(0,N,nsim)
kfit2_fitted=matrix(0,N,nsim)
kfit3_fitted=matrix(0,N,nsim)
#get good one
gknn = kknn(y~x,train,data.frame(x=test[fitind,1]),k=40,kernel = "rectangular")
set.seed(99)
for(i in 1:nsim) {
ii = sample(1:nrow(train),ntrain)
kfit1 = kknn(y~x,train[ii,],test,k=kvec[1],kernel = "rectangular")
kfit1_fitted[,i]=kfit1$fitted
fit1[i]=kfit1$fitted[fitind]
kfit2 = kknn(y~x,train[ii,],test,k=kvec[2],kernel = "rectangular")
kfit2_fitted[,i]=kfit2$fitted
fit2[i]=kfit2$fitted[fitind]
kfit3 = kknn(y~x,train[ii,],test,k=kvec[3],kernel = "rectangular")
kfit3_fitted[,i]=kfit3$fitted
fit3[i]=kfit3$fitted[fitind]
}
plot(x,y,col="gray45")
for (i in 1:nsim){
lines(test$x,kfit1_fitted[,i],col='royalblue2',lwd=.25)
points(test[fitind,1],fit1[i],col='black',pch=20,cex=1.5)
title(main=paste("k=", kvec[1], sep=""), font.main=1)
}
plot(x,y,col="gray45")
for (i in 1:nsim){
lines(test$x,kfit2_fitted[,i],col='royalblue2',lwd=.25)
points(test[fitind,1],fit2[i],col='black',pch=20,cex=1.5)
title(main=paste("k=", kvec[2], sep=""), font.main=1)
}
plot(x,y,col="gray45")
for (i in 1:nsim){
lines(test$x,kfit3_fitted[,i],col='royalblue2',lwd=.25)
points(test[fitind,1],fit3[i],col='black',pch=20,cex=1.5)
title(main=paste("k=", kvec[3], sep=""), font.main=1)
}


boxplot(fit1,ylim=ylm)
abline(h=fn(test[fitind,1]),col="red")
boxplot(fit2,ylim=ylm)
abline(h=fn(test[fitind,1]),col="red")
boxplot(fit3,ylim=ylm)
abline(h=fn(test[fitind,1]),col="red")
