get_split <- function(x) {
  len <- length(x)
  train <- as.integer(0.8*len)
  return(c(x[1:train], x[(train+1):len]))
}

read_file <- function(x) {
  table <- read.csv(x)
  l <- list()
  for (i in 1:dim(table)[1]) {
    l[[i]] <- c(read_line(table[i,]))
  }
  return(l)
}

read_line <- function(fr) {
  vec <- c(as.numeric(fr))
  return(vec[7:(7+fr$N-1)])
}
