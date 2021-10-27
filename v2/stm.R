source("functions_variables.R")
# install_package(packages)
load_package(packages)


# Set working directory
# rm(list=ls())
# setwd(here::here())

# Check the environment
# install.packages("reticulate")
# library(reticulate)
# conda_list(conda="auto") ## anaconda prompt?�� ?��같�?�?��..??

# Load Python
use_condaenv(condaenv = "jiseong", required = TRUE) ######?��기서부?�� ?��?��
# py_install("pandas")

# Load data
data = data.table(py_load_object('./data/cleansing/data_final_main'))[,c(1:5)]
colnames(data) = c("type", "no", "year", "text_raw", "text_cleansed")
head(data)

# Covert year into date object and integer
data = data %>%
    mutate(year = as.numeric(year)) %>%
    filter(year >= 2000 & year <= 2018)
    # transform(data, year=as.Date(as.character(year), "%Y"))
data$year_int = mapvalues(data$year, 
    from = c(2000:2018), 
    to = c(1:19))

# Sort by date
data = data %>% 
    arrange(year)

# Factorize
data$type = as.factor(data$type)

# Tokenize
data = data.frame(data)
myprocess = textProcessor(data$text_cleansed, metadata = data, wordLengths=c(2, Inf), lowercase = F, removenumbers = F, removepunctuation = F, removestopwords = F, stem = F)

# Text preparation
out = prepDocuments(myprocess$documents, myprocess$vocab, myprocess$meta, lower.thresh = as.integer(length(data$text_cleansed) * 0.001))

# Set working directory
setwd(here::here("data/stm")) ##error Ȯ�� �ʿ�
getwd()

# Find optinal number of K
search_k = T
if (search_k == F) {
  model_searchK = searchK(out$documents, out$vocab, K = c(5:100),
                          prevalence = ~type*s(year_int),
                          data = out$meta, seed=2020)
  saveRDS(model_searchK,'model_searchK.rds')
  plot(model_searchK)
} else {
  model_searchK = readRDS("model_searchK.rds")
}

png("model_searchK1.png", width = 750, height = 500)
plot(model_searchK)
dev.off()

png("model_searchK2.png", width = 1000, height = 1000)
model_candidates = data.frame(sapply(model_searchK$result[,2:3], function(x) as.numeric(x)))
rownames(model_candidates) = paste0("K=", unlist(model_searchK$result[,1]))
ggplot(data=model_candidates, mapping=aes(x=semcoh, y=exclus)) +
  geom_text_repel(label=rownames(model_candidates), size=4) +
  labs(title="Semantic Coherence-Exclusivity Plot by Number of Topics(K)", 
     x="Semantic Coherence",
     y="Exclusivity") +
  theme_classic() 
dev.off()

# Topic keywords (candidates: 19-28)
num_topic = 28

model = T
if (model == F) {
  stm_model = stm(out$documents, out$vocab, K=num_topic,
                  prevalence= ~type*s(year_int),
                  data=out$meta, init.type="Spectral",seed=2020,
                  verbose = F)
  model_name = paste0('model_topics_', num_topic ,'.rds')
  saveRDS(stm_model,model_name)
} else {
  model_name = paste0('model_topics_', num_topic ,'.rds')
  stm_model = readRDS(model_name)
}

# Summary
labelTopics(stm_model, n=20)

# Top topics
png("top_topics.png", width = 750, height = 500)
par(mfrow=c(1,1))
plot(stm_model, type='summary', labeltype = 'frex', n=5)
dev.off()

# Topic proportions
colSums(stm_model$theta)/sum(colSums(stm_model$theta))*100

# Topic correlation
stm_model_corr = topicCorr(stm_model, cutoff=0.05)
plot(stm_model_corr)

# Estimate effect
stm_effect_model = estimateEffect(1:num_topic ~type*s(year_int), stm_model, meta = out$meta, uncertainty = "Global")
summary(stm_effect_model, topics = 1)

# ?��?�� ?��?��블링
# topic_labels = paste0(paste0("T", stm_effect_model$topics, "-"), c("지방자�?&규제", "경제", "?���?(?���?)", "??�기업", "모빌리티갈등", 
#                                                                    "?��본시?��", "?���?(�??��)", "?���?(?��?��)", "?��?��관�?", "?��문사?��", 
#                                                                    "�??��무역", "?���?", "교육(?���?)", "중소벤처기업"))

topic_labels = paste0("T", stm_effect_model$topics, "-")

# Document by topics
doc_topic = make.dt(stm_model, meta = NULL)
doc_topic[,topic_class :=  names(.SD)[max.col(.SD)], .SDcols = 2:(num_topic+1)]
doc_topic = subset(doc_topic, select=c(docnum, topic_class))

for (i in 1:num_topic) {
  filter_by_topic = filter(doc_topic, topic_class == paste0("Topic", i))
  index_by_topic = filter_by_topic$docnum
  types_by_topic = out$meta$type[index_by_topic]
  no_by_topic = out$meta$no[index_by_topic]
  years_by_topic = out$meta$year[index_by_topic]
  docs_by_topic = out$meta$text_cleansed[index_by_topic]
  topic_name = rep(topic_labels[i], dim(doc_topic[doc_topic$topic_class==paste0("Topic",i)])[1])
  doc_date = data.frame(index_by_topic, types_by_topic, no_by_topic, years_by_topic, docs_by_topic, topic_name)
  colnames(doc_date) = c("index", "type", "no", "year", "text", "topic")
  write.csv(doc_date, paste0("./doc_by_topics/", topic_labels[i], ".csv"), fileEncoding = "cp949")
}

# S-T comparison
val1 = unique(data$type)[1]
val2 = unique(data$type)[2]
png(paste0("./comparison/", val1, " vs. ", val2, ".png"), width = 750, height = 500)
par(mfrow=c(1,1))
effect_plot = plot.estimateEffect(stm_effect_model, covariate = "type",
                                  topics = c(1:num_topic), method = "difference",
                                  model = stm_model, 
                                  main = '',
                                  cov.value1 = val1, cov.value2 = val2,
                                  xlab = paste(val1, "vs.", val2),
                                  xlim = c(-.2, .2),
                                  labeltype = "custom", n = 5,
                                  width = 100,  verbose.labels = F,
                                  custom.labels = topic_labels)
dev.off()

# Topic prevalence
effects = get_effects(estimates = stm_effect_model,
                      variable = 'year_int',
                      type = 'continuous',
                      moderator = 'type',
                      modval = 'S') %>%
  bind_rows(
    get_effects(estimates = stm_effect_model,
                variable = 'year_int',
                type = 'continuous',
                moderator = 'type',
                modval = 'T'))

knots = c(attr(stm_effect_model$modelframe$`s(year_int)`, 'Boundary.knots')[1], as.vector(attr(stm_effect_model$modelframe$`s(year_int)`, 'knots')), attr(stm_effect_model$modelframe$`s(year_int)`, 'Boundary.knots')[2])
year_names = unique(data$year)
plot_list = list()
for (t in c(1:num_topic)) {
  effects_topic = filter(effects, topic == t)
  effects_topic = mutate(effects_topic, moderator = as.factor(effects_topic$moderator))
  p = ggplot(effects_topic, aes(x = value, y = proportion, color = moderator,
             group = moderator, fill = moderator)) +
  geom_line() +
  geom_hline(yintercept = 0, size=0.75) +
  geom_vline(xintercept = knots, size=0.5, color="darkgrey", linetype="dashed") +
  geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.2)  +
  theme(legend.position = "none") +
  labs(title=paste0(topic_labels[t]), x = 'years_int', y = 'Topic Proportion',
       color = 'type', group = 'type', fill = 'type') +
  scale_x_continuous(name="Year", 
                     breaks = seq(min(effects_topic$value), max(effects_topic$value), length.out=length(year_names)),
                     labels = year_names) +
  theme_classic()+
  theme(axis.text.x = element_text(angle=90, size=rel(0.9), hjust=1, vjust=0.5),
        legend.box.margin = margin(2.5,unit="pt"))
  plot_list[[t]] = p
}

ml = marrangeGrob(plot_list, nrow=1, ncol=1)
pdf.options(family = "Korea1deb")
ggsave("./plots/stm_topic_prevalence.pdf", plot=ml, width = 12, height = 8, units="in")
