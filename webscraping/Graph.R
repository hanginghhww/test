library(plotly)
avgprice=read.csv('avg.csv')
brandd=read.csv('brandd.csv')
top10price=read.csv('top10_price.csv')
top10rating=read.csv('top10_rating.csv')

price=plot_ly(avgprice, x = ~subcat,y=~price,type='bar') 
rating=plot_ly(avgprice, x = ~subcat,y=~rate,type='bar') 

brandd1=plot_ly(brandd, x = ~subcat) %>%
  add_trace(y = ~productname, name = 'number of product') %>%
  add_trace(y = ~brand, name = 'number of brand')

Ctoprate=plot_ly(topprice,x=~brandname,y=~rate,type='bar',name='rate of Product') %>%
  add_trace(y = ~Avg.rate, name = 'AVG.Rate of Category') 

Ctoprate=plot_ly(topprice,x=~brandname,y=~rate,type='bar',name='Rate of Product') %>%
  add_trace(y = ~AVG.rate, name = 'AVG Rate of Category') 