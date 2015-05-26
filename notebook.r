install.packages('forecast')
library('forecast')

# Automatically fits an ARIMA model based on BIC model selection and
#  returns the model's absolute error on the last n data points which 
#  are held out from training
auto_arima_prediction_error <- function(time_series, n = 18) {
  len <- length(time_series)
  train <- len - 18
  train_data <- time_series[1:train]
  test_data <- time_series[(train+1):len]
  predict <- forecast(auto.arima(train_data), h = n)$mean
  return(abs(predict - test_data))
}

# Takes a list of vectors and return the average prediction error
#  of an auto.arima model on the last n data points (held out from
#  training)
average_error_vector <- function(ts_list, n = 18) {
  errors <- matrix(nrow=length(ts_list), ncol=n)
  for (i in 1:length(ts_list)) {
    errors[i,] <- auto_arima_error_vector(ts_list[[i]])
  }
  return(colMeans(errors))
}

# Parse M3 file lines as simple data vectors.
read_line <- function(fr) {
  vec <- c(as.numeric(fr))
  # first 6 entries are metadata, fr$N gives the length of the timeseries
  return(vec[7:(7+fr$N-1)])
}

# Reads M3 files line by line and stores them in a list of vectors.
read_file <- function(filename) {
  table <- read.csv(filename)
  l <- list()
  for (i in 1:dim(table)[1]) {
    l[[i]] <- c(read_line(table[i,]))
  }
  return(l)
}

quart <- average_error_vector(read_file('Quart_M3C.csv'))
print("Saving quart to quart_predict_error.csv")
write.csv(quart, file="quart_predict_error.csv")

year <- average_error_vector(read_file('Year_M3C.csv'))
print("Saving year to year_predict_error.csv")
write.csv(year, file="year_predict_error.csv")

month <- average_error_vector(read_file('Month_M3C.csv'))
print("Saving month to month_predict_error.csv")
write.csv(month, file="month_predict_error.csv")

other <- average_error_vector(read_file('Other_M3C.csv'))
print("Saving other to other_predict_error.csv")
write.csv(other, file="other_predict_error.csv")