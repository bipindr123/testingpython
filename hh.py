import json
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression

months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
          "Nov": 11, "Dec": 12}
monthAsString = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
output = {}
with open('data.json') as data_file:
  data = json.load(data_file)


# for using linear regression
def predict_price2(dates, prices, dates2):
  genius_regression_model = LinearRegression()
  genius_regression_model.fit(dates, prices)
  return genius_regression_model.predict(dates2)


# for using rbf regression
def predict_price(dates, prices, dates2):
  # defining the support vector regression models
  svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
  svr_rbf.fit(dates, prices)  # fitting the data points in the models

  return svr_rbf.predict(dates2)


flag = 0
for i in data:
  flag = 0
  for j in data[i]:
    output2 = {}
    # print(j)
    dates = []
    values = []
    dates2 = []
    for k, v in data[i][j].items():
      x = ([months[k.split('-')[0]], int(k.split('-')[1])])
      dates.append(x)
      values.append(v)
    dates2.append([dates[-1][0], dates[-1][1]])
    dates2[0][0] = dates2[0][0] + 1
    dates2.append([dates2[0][0] + 1, dates2[0][1]])
    # print(dates2)
    # print(dates)
    # print(values)
    dates3 = []

    try:
      next_val = predict_price(dates, values, dates2)
    except:
      pass
    dates3 = []
    for e in range(0, len(dates2)):
      dates3.append(monthAsString[dates2[e][0]] + '-' + str(dates2[e][1]))
      output2.update({dates3[e]: next_val[e]})
    # print(output2)
    for l in dates3:
      flag2 = 0
      if flag == 0:
        output.update({i: {j: output2}})
      else:
        output[i].update({j: output2})
      flag = 1

j = json.dumps(output)

# Write to file
with open('data2.json', 'w') as f:
  f.write(j)
