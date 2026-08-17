# Load packages
library(ggplot2)
library(dplyr)

# All k values
ks <- seq(6, 24, by = 2)

# Read all files and add number of vertices
data <- lapply(ks, function(k) {
  df <- read.csv(paste0("runtime_", k, ".csv"))
  df$n_vertices <- k
  return(df)
})

# Combine all dataframes
data <- bind_rows(data)

head(data)

summary <- data %>%
  group_by(n_vertices) %>%
  summarise(
    mean_runtime = mean(runtime_seconds),
    sd_runtime = sd(runtime_seconds)
  )

print(summary)

ggplot(summary, aes(x = n_vertices, y = mean_runtime)) +
  geom_point() +
  geom_line() +
  labs(
    x = "Number of vertices",
    y = "Mean runtime (seconds)"
  ) +
  theme_minimal()

ggplot(data, aes(x = factor(n_vertices), y = runtime_seconds)) +
  geom_boxplot() +
  labs(
    x = "Number of vertices",
    y = "Runtime (seconds)"
  ) +
  theme_minimal()

ggplot(data, aes(
  x=n_vertices,
  y=runtime_seconds
)) +
  geom_jitter(width=0.2, alpha=0.3) +
  scale_y_log10() +
  theme_minimal()

ggplot(data, aes(
  x = factor(n_vertices),
  y = runtime_seconds
)) +
  geom_boxplot(
    alpha = 0.6,
    outlier.shape = NA
  ) +
  geom_jitter(
    width = 0.15,
    alpha = 0.1,
    size = 1
  ) +
  labs(
    x = "Number of vertices",
    y = "Runtime (seconds)"
  ) +
  scale_y_log10()+
  theme_minimal()

summary <- data %>%
  group_by(n_vertices) %>%
  summarise(
    mean_runtime = mean(runtime_seconds),
    sd_runtime = sd(runtime_seconds)
  )

