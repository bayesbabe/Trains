#Script to take in schedule data and fill in data for stations trains do not stop at and the estimated speed the train is travelling when it passes the station

schedule=read.csv("/Users/Rachel/Desktop/caltrain_schedule_with_mph.csv", header=TRUE)

###function to get stations train doesn't stop at (takes in subset)
missing.stations=function(subs)
{
  missing=NULL
  for(i in 1:max(subs$station_order))
  {
    if(length(which(subs$station_order==i))==0){missing=c(missing,i)}
    else{missing=missing}
  }
  return(missing)
}

add_station_info=function(station_order)
{
  addcols=NULL
  addrows=NULL
  for(i in 1:length(station_order))
  {
    index=which(key$station_order==station_order[i])
    addcols=cbind(station_order[i],key[index,])
    addrows=rbind(addrows,addcols)
    final=addrows[,-1]
  }
  return(final)
}

get_train_info=function(subs)
{
  train.keyvalues=subs[,c(4,6,7,8,9)]
  train.key=unique(train.keyvalues)
  names=colnames(train.key)
  train.key=cbind(train.key, "N", "NA", "NA")
  colnames(train.key)=c(names,"stop", "station_id", "schedule_time")
  train_info=NULL
  for(i in 1:dim(station_info)[1])
  {
    train_info=rbind(train_info,train.key)
  }
  return(train_info)
}

getspeedkeySB=function(nostop, stops)
{
  speed.key=NULL
  for(i in 1:length(nostop))
  {
    nextstop=min(stops[which(stops>nostop[i])])
    est.speed=subs[which(subs$station_order==nextstop),]$avg.speed
    speed.keyvalue=c(nostop[i],est.speed)
    speed.key=rbind(speed.key,speed.keyvalue)
  }
  colnames(speed.key)=c("station_order", "avg.speed")
  return(speed.key)
}

getspeedkeyNB=function(nostop, stops)
{
  speed.key=NULL
  for(i in 1:length(nostop))
  {
    nextstop=max(stops[which(stops<nostop[i])])
    est.speed=subs[which(subs$station_order==nextstop),]$avg.speed
    speed.keyvalue=c(nostop[i],est.speed)
    speed.key=rbind(speed.key,speed.keyvalue)
  }
  colnames(speed.key)=c("station_order", "avg.speed")
  return(speed.key)
}

getspeeds=function(combdata,speeds)
{
  x=NULL
  for(i in 1:dim(combdata)[1])
  {
    index=which(speeds$station_order==combdata[i,]$station_order)
    est.speed=speeds$avg.speed[index]
    x=c(x,est.speed)
  }
  return(x)
}

##subset data by train_num
scheduleNORTH=schedule[which(schedule$train_direction=="NORTHBOUND"),]
scheduleSOUTH=schedule[which(schedule$train_direction=="SOUTHBOUND"),]
trainsNORTH=unique(scheduleNORTH$train_num)
trainsSOUTH=unique(scheduleSOUTH$train_num)

newdatasb=NULL
##create key for station order values
keyvalues=schedule[,c(1,2,3,11)]
key=unique(keyvalues)
for(i in 1:length(trainsSOUTH)){
  subs=scheduleSOUTH[which(scheduleSOUTH$train_num==trainsSOUTH[i]),]
  nostop=missing.stations(subs)
  station_info=add_station_info(nostop)
  train_info=get_train_info(subs)
  combdata=cbind(station_info,train_info)
  stops=unique(subs$station_order)
  speeds=getspeedkeySB(nostop,stops)
  speeds=as.data.frame(speeds)
  est.speeds=getspeeds(combdata,speeds)
  names=colnames(combdata)
  combdata2=cbind(combdata,est.speeds)
  colnames(combdata2)=c(names,"avg.speed")
  filleddata=rbind(subs,combdata2) #remove schedule_time
  newdatasb=rbind(newdatasb,filleddata)
}

newdatanb=NULL
##create key for station order values
keyvalues=schedule[,c(1,2,3,11)]
key=unique(keyvalues)
for(i in 1:length(trainsNORTH)){
  subs=scheduleNORTH[which(scheduleNORTH$train_num==trainsNORTH[i]),]
  nostop=missing.stations(subs)
  station_info=add_station_info(nostop)
  train_info=get_train_info(subs)
  combdata=cbind(station_info,train_info)
  stops=unique(subs$station_order)
  speeds=getspeedkeyNB(nostop,stops)
  speeds=as.data.frame(speeds)
  est.speeds=getspeeds(combdata,speeds)
  names=colnames(combdata)
  combdata2=cbind(combdata,est.speeds)
  colnames(combdata2)=c(names,"avg.speed")
  filleddata=rbind(subs,combdata2) #remove schedule_time
  newdatanb=rbind(newdatanb,filleddata)
}

newdata=rbind(newdatanb, newdatasb)
write.csv(newdata, "/Users/Rachel/Desktop/filledcaltrain.csv")
