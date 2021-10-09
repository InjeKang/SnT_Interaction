# Variables
packages = c("here", "stm", "stminsights", "tidyverse", "data.table", "lubridate", "reticulate", "dplyr", "gridExtra", "ggrepel", "ggplot2", "plyr")

install_package <- function(packages) {
    for (package in packages) {
        if (!require(package)) {
            install.packages(package)
        }
    }
    }

load_package <- function(packages) {
    lapply(packages, require, character.only = TRUE)
}
    




