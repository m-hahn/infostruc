
# Plots medians with confidence intervals

fullData = read.csv("../results/tradeoff/ngrams/listener-curve-ci-median.tsv", sep="\t")

memListenerSurpPlot_onlyWordForms_boundedVocab = function(language) {
    library(tidyr)
    library(dplyr)
    library(ggplot2)
    dataL = read.csv(paste("../raw/ngrams/",language,"_ngrams_infostruc_decay_after_tuning.tsv", sep=""), sep="\t")
    UnigramCE = mean(dataL$UnigramCE)
    data = fullData %>% filter(Language == language)
    plot = ggplot(data, aes(x=Memory, y=UnigramCE-MedianEmpirical, fill=Type, color=Type)) + geom_line(size=2)+ theme_classic()
 #   plot = plot + theme(legend.position="none")
    plot = plot + geom_line(aes(x=Memory, y=UnigramCE-MedianLower), linetype="dashed") + geom_line(aes(x=Memory, y=UnigramCE-MedianUpper), linetype="dashed")
    plot = plot + xlab("Memory") + ylab("Median Surprisal")
    plot = plot + theme(text = element_text(size=30))
    ggsave(plot, file=paste("figures/",language,"-listener-surprisal-memory-MEDIANS_onlyWordForms_boundedVocab.pdf", sep=""))
    return(plot)
}


for(language in c("Czech-PDT")) {
   memListenerSurpPlot_onlyWordForms_boundedVocab(language)
}


