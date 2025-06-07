library(DBI)
library(RSQLite)
library(ggplot2)

# Conexão com o banco SQLite na nova pasta
con <- dbConnect(RSQLite::SQLite(), "alerta_enchente_br/database/banco_dados.sqlite")

# Leitura dos dados
dados <- dbGetQuery(con, "SELECT * FROM alertas")

# Conversão de data
dados$data_hora <- as.POSIXct(dados$data_hora, format="%Y-%m-%d %H:%M:%S")

# Gráfico 1 - Frequência de riscos
ggplot(dados, aes(x = risco)) +
  geom_bar(fill = "tomato") +
  labs(title = "Frequência de Riscos de Enchente", x = "Risco", y = "Contagem") +
  theme_minimal()

# Gráfico 2 - Nível x Tempo
ggplot(dados, aes(x = data_hora, y = nivel_cm, color = risco)) +
  geom_point(size = 3) +
  labs(title = "Evolução do Nível de Água no Tempo", x = "Data/Hora", y = "Nível (cm)") +
  theme_minimal()

# Fecha a conexão
dbDisconnect(con)
