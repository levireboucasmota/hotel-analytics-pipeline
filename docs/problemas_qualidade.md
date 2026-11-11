# Problemas de qualidade e decisões de tratamento

| # | Problema | Qtd | Decisão | Justificativa |
|---|---|---|---|---|
| 1 | `company` com 94,31% de nulos | - | Descartar coluna (criar flag `tem_empresa`) | Quase sem informação útil |
| 2 | `agent` com 13,69% de nulos | - | Preencher com 0 (sem agente) | Nulo significa venda sem agência |
| 3 | `country` com 0,41% de nulos | - | Preencher com "Desconhecido" | Mantém a reserva na análise |
| 4 | `children` com nulos | 4 | Preencher com 0 | Quantidade desprezível |
| 5 | `adr` negativo | 1 | Remover | Erro de registro |
| 6 | `adr` = 5400 | 1 | Remover | Outlier extremo, provável erro de digitação |
| 7 | `adr` = 0 | 1.959 | Manter + flag `adr_zero` | Cortesias e ajustes; excluir apenas de análises de preço |
| 8 | Reservas com 0 noites | 715 | Manter + flag `sem_noites` | 680 com check-out (provável day use) |
| 9 | Reservas com 0 hóspedes | 180 | Remover | Registro inconsistente |
| 10 | Linhas duplicadas | 31.994 | Remover (premissa documentada) | Sem ID de reserva; medir impacto na taxa de cancelamento |
| 11 | `meal`: "SC" e "Undefined" | - | Padronizar em "SC" | Significam a mesma coisa |
| 12 | `reservation_status*` | - | Não usar como preditora | Vazamento de dados (só conhecidas após o desfecho) |