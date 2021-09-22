# Leon Silva - 10th Place Solution - Meli Data Challenge 2021

First of all I'd like to thank Mercado Libre for this great contest. I'd also like to thank Mário Filho for sharing so much of his approach which gave me a huge head start: most of my solution got the ideas (and implementation) from him. With a litte feature engineering + ensemble with non-ML predictions + post processing I was able to get to the 10th place.

#### Business Understanding

Given the sales of 600k+ products between february and march of 2021, we were asked to predict the inventory days of these products in april of 2021. The items were sold in three countries: Argentina, Brazil and Mexico. 

Moreover, the predictions should be presented in terms of the probability of selling out in the 30 days of April. It's given that all products are sold within 30 days.

The task as stated in the Challenge:

"Your task is to predict how long it will take for the inventory of a certain item to be sold completely. In inventory management theory this concept is known as inventory days.

In the evaluation set you will be given the item target stock, and you will have to provide a prediction for the number of days it will take to run out. Possible values range from 1 to 30. Rather than giving a point estimate, you are expected to provide a score for each the possible outcomes.

To put it simply, you need to answer the following question:

'What are the odds that the target stock will be sold out in one day?', 'What about in two days?' and so on until day 30."

#### Data Understanding

We were given three files:
* The first file has the information about the sales in Februrary and March of 2021 of 600k+ products, with features regarding the products in each day: price, minutes active in the last 24 hours and number os itens sold that day
* The second had the metadata of the products
* Finally, the test file has the skus (unique id for each product) with the inventory to predict the inventory days

#### Modeling

I used a simple regressor (XGBoost) to find how many items were sold in the last day of the given period (31/03/2021). With this information, we can calculate the inventory days: items_sold_prediction / inventory_in_test

The validation used was the mean RDS between the traning in February and validating in March and vice-versa.

Besides the creation of features that helped improving the solution, the different approaches I did different from other solutions were:
* I've created an ensemble model with XGBRegressor and a naive predictor (average sales)
* I've done post processing setting 30 inventory days to the skus which stock were too big considering the sales on the previous months

I tryed different distributions, but in the end, tweedie was the best one to calculate the submissions.