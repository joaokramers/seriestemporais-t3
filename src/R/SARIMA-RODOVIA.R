# ========================================================
# An adapted program for forecasting total volume
# ========================================================
# last update: 05/Jul/2025
# 
# Time series analysis using the SARIMA model for total volume
#
# Raul Matsushita - Adapted by Gemini
# ========================================================

# ========================================================
# Load fonts & packages
# update.packages(checkBuilt=TRUE, ask=FALSE)
# ========================================================

if(!require(ggplot2)){
  install.packages("ggplot2")
  library(ggplot2)
}
if(!require(extrafont)){
  install.packages("extrafont")
  library(extrafont)
}
#loadfonts(device = "win") # Descomente se precisar carregar fontes específicas para Windows
if(!require(openxlsx)){
  install.packages("openxlsx")
  library(openxlsx)
}
if(!require(TSA)){
  install.packages("TSA")
  library(TSA)
}
if(!require(tseries)){
  install.packages("tseries")
  library(tseries)
}
if(!require(astsa)){
  install.packages("astsa")
  library(astsa)
}
if(!require(zoo)){
  install.packages("zoo")
  library(zoo)
}
if(!require(dplyr)){ # Adicionando dplyr para facilitar a manipulação de dados
  install.packages("dplyr")
  library(dplyr)
}
# ========================================================

# ========================================================
# Set the working folder
# ========================================================
# Certifique-se de que este caminho aponta para o diretório onde seu arquivo CSV está localizado
setwd("C:/Unb/series-temporais/seriestemporais-t3/src/dados") 

# ========================================================
# Data preparation
# ========================================================================

# Nome do arquivo do novo dataset
file_name <- 'fonte-dados-estudo.csv' # Assumindo que você salvou a imagem como CSV, ou o nome real do seu arquivo

# Lendo o arquivo CSV. O separador é vírgula por padrão, header=TRUE (ou 1) para primeira linha como cabeçalho.
# Se o arquivo for um .xlsx, você precisará usar read.xlsx do pacote openxlsx.
# Para este exemplo, assumirei que você salvou os dados da imagem em um CSV.
volume_data <- read.csv(file_name, header = TRUE, sep = ";", row.names = NULL,dec = ",")


# Renomear a coluna 'mes_ano' para 'Date' para consistência com o código original,
# ou simplesmente usar o nome original e adaptar as chamadas.
# Vamos usar o nome original 'mes_ano' e adaptar.

# Convertendo a coluna 'mes_ano' para o formato de data.
# O formato na imagem é DD/MM/YYYY.
volume_data$data <- as.Date(volume_data$mes_ano, format = "%d/%m/%Y")

volume_serie$month <- format(volume_serie$mes_ano, "%m")
volume_serie$year  <- format(volume_serie$mes_ano, "%Y")
t.mensal      <- aggregate(volume_serie$volume_total, 
                           by=list(month = volume_serie$month, year = volume_serie$year),
                           FUN=mean)
t.mensal$mes <- as.yearmon(paste(t.mensal$year, t.mensal$month), "%Y %m")
t.mensal$X.t <- t.mensal$x
# ========================================================================

# ========================================================================
# Figure 1: Plot da série temporal original
# ========================================================================
Fig.temp <- ggplot(data = t.mensal, aes(x = mes, y = X.t)) +
  geom_line(linewidth=1) +
  ggtitle("Fluxo Mensal") +
  xlab(expression(italic(t)))+
  ylab(expression(italic(Y[t])))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black")) 
# ========================================================================


Fig.temp


# ========================================================
# Sample ACF and Partial ACF
# ========================================================================

Y.t <- t.mensal$X.t 

fac   <- acf(Y.t, lag = 60, plot = FALSE)
Fig.2 <- with(fac, data.frame(lag, acf))
Fig.2 <- rbind(c(0,1),Fig.2)

facp   <- pacf(Y.t, lag = 60, plot = FALSE)
Fig.3 <- with(facp, data.frame(lag, acf))
Fig.3 <- rbind(c(0,1),Fig.3)
# ========================================================================

Fig.acf <- ggplot(data = Fig.2, mapping = aes(x = lag, y = acf)) +
  geom_hline(aes(yintercept = 0)) +
  geom_segment(mapping = aes(xend = lag, yend = 0), size=2)+
  ggtitle("FAC da série original") +
  xlab(expression(italic(h)))+
  ylab(expression(paste(rho)[italic(h)]))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black")) 
# ========================================================================

Fig.acf

Fig.2

Fig.pacf <- ggplot(data = Fig.3, mapping = aes(x = lag, y = acf)) +
  geom_hline(aes(yintercept = 0)) +
  geom_segment(mapping = aes(xend = lag, yend = 0), size=2)+
  ggtitle("FACP da série original") +
  xlab(expression(italic(h)))+
  ylab(expression(paste(phi)[italic(hh)]))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black")) 
# ========================================================================

Fig.pacf

Fig.3

# ========================================================================
# Assessing seazonal nonstationarity
# ========================================================================
t.mensal$month <- as.numeric(t.mensal$month)
t.mensal$H1c<- cos(2*pi*t.mensal$month/12)
t.mensal$H1s<- sin(2*pi*t.mensal$month/12)
t.mensal$H2c<- cos(2*pi*t.mensal$month/6)
t.mensal$H2s<- sin(2*pi*t.mensal$month/6)
t.mensal$H3c<- cos(2*pi*t.mensal$month/4)
t.mensal$H3s<- sin(2*pi*t.mensal$month/4)
t.mensal$H4c<- cos(2*pi*t.mensal$month/3)
t.mensal$H4s<- sin(2*pi*t.mensal$month/3)


profile <- lm(X.t ~ H1c + H1s + H2c + H2s +
                H3c + H3s + H4c + H4s, 
              data = t.mensal)
summary(profile)

#H1c            21080       3871   5.446 1.92e-07 ***
#H1s            -4990       3871  -1.289  0.19922    
#H2c            20032       3871   5.175 6.79e-07 ***
#H2s            20104       3871   5.193 6.24e-07 ***
#H3c            11972       3871   3.093  0.00234 ** 
#H3s             5962       3871   1.540  0.12550    
#H4c             1939       3871   0.501  0.61717    
#H4s            21508       3871   5.556 1.14e-07 ***
  

profile <- lm(X.t ~ H1c + H2c + H2s + H3c + H4s,
              data = t.mensal)

summary(profile)


M   <- 1:12
H1c <- cos(2*pi*M/12)
H1s <- sin(2*pi*M/12)
H2c <- cos(2*pi*M/6)
H2s <- sin(2*pi*M/6)
H3c <- cos(2*pi*M/4)
H3s <- sin(2*pi*M/4)
H4c <- cos(2*pi*M/3)
H4s <- sin(2*pi*M/3)
Ano <- data.frame(H1c, H2c, H2s, H3c, H4s)
perfil <- predict(profile,Ano)
previsao <- data.frame(M, perfil)

# ========================================================================
# Figure 1
# ========================================================================
Fig.perfil <- ggplot(data = t.mensal) +
  geom_line(aes(x = month, y =X.t, color = as.factor(year)),linewidth=1) +
  ggtitle("Perfil Sazonal") +
  xlab(expression(italic(t)))+
  ylab(expression(italic(Y[t])))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black"), legend.position = "none"
  ) 
# ========================================================================

Fig.perfil

Fig.perfil + scale_x_discrete(limits = factor(1:12)) +   geom_line(data = previsao, aes(x =M, y = perfil), linewidth=3) 




# ========================================================================
# Differentiation
# ========================================================================

X.t         <- diff(t.mensal$X.t, lag = 12)
t.mensal$dif <- c(rep(NA,12),X.t)

# ========================================================================

Fig.dif <- ggplot(data = t.mensal, mapping = aes(x = mes, y = dif)) +
  geom_line(size=1.2) +
  ggtitle("Variação do Fluxo Mensal") +
  xlab(expression(italic(t)))+
  ylab(expression(paste(nabla)*italic(Y[t])))+
  geom_hline(yintercept=0, linetype="dashed", color = "blue", size=1)+
  theme(text = element_text(family = "Times New Roman", size=21,colour="black")
        ,axis.title.y = element_text(family = "Times New Roman", angle=90, size=22, colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,  unit = "pt"))
        ,axis.title.x = element_text(family = "Times New Roman",vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,colour="black")
  ) 
Fig.dif
# ========================================================================


# ========================================================
# Sample ACF and Partial ACF
# ========================================================================


fac   <- acf(X.t, lag = 60, plot = FALSE)
Fig.2 <- with(fac, data.frame(lag, acf))
Fig.2 <- rbind(c(0,1),Fig.2)

facp   <- pacf(X.t, lag = 60, plot = FALSE)
Fig.3 <- with(facp, data.frame(lag, acf))
Fig.3 <- rbind(c(0,1),Fig.3)

# ========================================================================

Fig.acf <- ggplot(data = Fig.2, mapping = aes(x = lag, y = acf)) +
  geom_hline(aes(yintercept = 0)) +
  geom_segment(mapping = aes(xend = lag, yend = 0), size=2)+
  ggtitle("FAC da primeira diferença") +
  xlab(expression(italic(h)))+
  ylab(expression(paste(rho)[italic(h)]))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black")) 
# ========================================================================

conf.lim <- 2/sqrt(fac$n.used)
Fig.acf + geom_hline(aes(yintercept =  conf.lim), linetype="dotted", 
                     size = 2, color = "red") +
  geom_hline(aes(yintercept = -conf.lim), linetype="dotted", 
             size = 2, color = "red") 

# ========================================================================

Fig.2

Fig.pacf <- ggplot(data = Fig.3, mapping = aes(x = lag, y = acf)) +
  geom_hline(aes(yintercept = 0)) +
  geom_segment(mapping = aes(xend = lag, yend = 0), size=2)+
  ggtitle("FACP da primeira diferença") +
  xlab(expression(italic(h)))+
  ylab(expression(paste(phi)[italic(hh)]))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black")) 
# ========================================================================

Fig.pacf + geom_hline(aes(yintercept =  conf.lim), linetype="dotted", 
                      size = 2, color = "red") +
  geom_hline(aes(yintercept = -conf.lim), linetype="dotted", 
             size = 2, color = "red") 

Fig.3


# ========================================================================
# Treinamento
# ------------------------------------------
n.size          <- dim(t.mensal)[1]
t.size          <- ceiling(n.size/2)
X.t             <- t.mensal$x[1:t.size]


# -----------------------------------------------------------------------------------------
# determinação da ordem do modelo da série de treinamento
# -----------------------------------------------------------------------------------------
BIC     <- NULL
grid    <- 0:5
Grid    <- 0:2
for (p.grid in rev(grid)){
  for (q.grid in rev(grid)){
    for (P.grid in Grid){
      for (Q.grid in Grid){
        tryCatch({
          draft <-sarima( X.t, p.grid,  0,  q.grid,
                          P=P.grid,D = 1 ,Q=Q.grid,S=12,
                          no.constant=TRUE,details=FALSE)
          
          BIC   <- rbind( BIC, c(BIC = unlist(draft[4])[3], 
                                 p = p.grid, q = q.grid, P = P.grid, Q = Q.grid))
        }, error=function(e){})
      }}}}


# listagem dos 10 melhores modelos
# ----------------------------------
BIC <- data.frame(BIC) 
BIC <- BIC[order(BIC$BIC.ICs.BIC),]
BIC[1:10,]
# ----------------------------------



# -----------------------------------------------------------------------------------------



fit  <- sarima(X.t,BIC[1,2],0,BIC[1,3],
               P=BIC[1,4],D=1,Q=BIC[1,5],S=12,no.constant=TRUE)

fit  <- sarima(X.t,BIC[2,2],0,BIC[2,3],
               P=BIC[2,4],D=1,Q=BIC[2,5],S=12,no.constant=TRUE)


# Teste de Ljung-Box
LB  <- NULL
for (lag in 1:30)
{
  LB[lag] <- Box.test(resid(fit$fit), lag = lag, type='Ljung-Box')$p.value
}
data.frame(p.values = LB)



r.t <- resid(fit$fit)
fac   <- acf(r.t, lag = 60, plot = FALSE)
Fig.2 <- with(fac, data.frame(lag, acf))
Fig.2 <- rbind(c(0,1),Fig.2)

facp   <- pacf(r.t, lag = 60, plot = FALSE)
Fig.3 <- with(facp, data.frame(lag, acf))
Fig.3 <- rbind(c(0,1),Fig.3)


# ========================================================================

Fig.acf <- ggplot(data = Fig.2, mapping = aes(x = lag, y = acf)) +
  geom_hline(aes(yintercept = 0)) +
  geom_segment(mapping = aes(xend = lag, yend = 0), size=2)+
  ggtitle("FAC residual") +
  xlab(expression(italic(h)))+
  ylab(expression(paste(rho)[italic(h)]))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black")) 
# ========================================================================

conf.lim <- 2/sqrt(fac$n.used)
Fig.acf + geom_hline(aes(yintercept =  conf.lim), linetype="dotted", 
                     size = 2, color = "red") +
  geom_hline(aes(yintercept = -conf.lim), linetype="dotted", 
             size = 2, color = "red") 

# ========================================================================

Fig.2

Fig.pacf <- ggplot(data = Fig.3, mapping = aes(x = lag, y = acf)) +
  geom_hline(aes(yintercept = 0)) +
  geom_segment(mapping = aes(xend = lag, yend = 0), size=2)+
  ggtitle("FACP residual") +
  xlab(expression(italic(h)))+
  ylab(expression(paste(phi)[italic(hh)]))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black")) 
# ========================================================================

Fig.pacf + geom_hline(aes(yintercept =  conf.lim), linetype="dotted", 
                      size = 2, color = "red") +
  geom_hline(aes(yintercept = -conf.lim), linetype="dotted", 
             size = 2, color = "red") 

Fig.3



# teste
# ----------------------------------------------
X.t             <- t.mensal$X.t
fit <- sarima(X.t,BIC[2,2],0,BIC[2,3],P=BIC[2,4],
              D=1,Q=BIC[2,5],S=12,no.constant=TRUE)
fit

residuals <-  as.numeric(unlist(fit$fit[8]))
shapiro.test(residuals)
# ----------------------------------------------


quantis <- quantile(na.omit(residuals), c(0.025, 0.975))



t.mensal$X.hat     <- X.t - residuals
t.mensal$X.hat[1:t.size] <- NA
Fig.temp + geom_line(data=t.mensal,mapping = aes(x = mes, y = X.hat), linewidth=1.2, col = "red")

(MAPE <- mean(abs((t.mensal$X.hat-t.mensal$X.t)/t.mensal$X.t),na.rm=T)*100)


# ----------------------------------------------
# Previsao
# ----------------------------------------------
fit <- sarima.for(as.ts(t.mensal$X.t),n.ahead = 12, 
                  BIC[2,2],0,BIC[2,3],P=BIC[2,4],D=1,Q=BIC[2,5],S=12,
                  no.constant=TRUE, plot.all = TRUE)
X.t   <- c(t.mensal$X.t[(n.size - 11):n.size], rep(NA,12))
X.hat <- c(rep(NA,12), as.numeric(fit$pred))
se    <- c(rep(NA,12), as.numeric(fit$se))
mes   <- seq(1:length(X.t))
Preds <- data.frame(mes,X.t,X.hat,se)

# ========================================================================
# Figure pred
# ========================================================================
Fig.pred <- ggplot(data = Preds, aes(x = mes, y = X.t)) +
  geom_line(linewidth=1.2) +
  ggtitle("Fluxo Mensal (últimos 12 meses)") +
  xlab(expression(italic(t)))+
  ylab(expression(italic(Y[t])))+
  theme(text=element_text(family="Times New Roman",size=21,colour="black")
        ,axis.title.y=element_text(family="Times New Roman",angle=90,size=22, 
                                   colour="black", vjust=0.5, margin=margin(t = 0, r = 15, b = 0, l = 0,
                                                                            unit = "pt")),axis.title.x = element_text(family = "Times New Roman",
                                                                                                                      vjust=-1.5, margin=margin(t = 0, r = 0, b = 15, l = 0,  unit = "pt"))
        ,plot.title = element_text(family = "Times New Roman", hjust = 0.5,
                                   colour="black")) 
# ========================================================================

Fig.pred + 
  geom_line(data=Preds, aes(x = mes, y = X.hat), linewidth=1.2, col = "red") +
  #geom_line(data=Preds, aes(x = mes, y = X.hat +2*se), linetype="dotted",  color = "blue", size=1.5) +
  #geom_line(data=Preds, aes(x = mes, y = X.hat -2*se), linetype="dotted",  color = "blue", size=1.5) +
  geom_ribbon(data=Preds,aes(ymin=X.hat -2*se,ymax=X.hat +2*se), fill="grey", alpha=0.5)


