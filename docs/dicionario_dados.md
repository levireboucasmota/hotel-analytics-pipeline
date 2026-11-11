# Dicionário de dados

Fonte: Hotel Booking Demand (Kaggle), com reservas de dois hotéis em Portugal entre 2015 e 2017.

| Coluna | Tipo | Nulos (%) | Descrição | Observações |
|:--|:--|--:|:--|:--|
| hotel | str | 0 | Tipo de hotel: Resort Hotel ou City Hotel | |
| is_canceled | int64 | 0 | Indica se a reserva foi cancelada (1) ou não (0) | Variável-alvo do modelo de cancelamento |
| lead_time | int64 | 0 | Dias entre a data da reserva e a data de chegada | Antecedência da reserva |
| arrival_date_year | int64 | 0 | Ano da data de chegada | |
| arrival_date_month | str | 0 | Mês da data de chegada (nome em inglês) | Converter para número no ETL |
| arrival_date_week_number | int64 | 0 | Número da semana do ano da data de chegada | |
| arrival_date_day_of_month | int64 | 0 | Dia do mês da data de chegada | Junto com ano e mês, permite montar a data de chegada |
| stays_in_weekend_nights | int64 | 0 | Noites de sábado ou domingo reservadas | |
| stays_in_week_nights | int64 | 0 | Noites de segunda a sexta reservadas | 715 reservas com 0 noites no total (fim de semana + semana) |
| adults | int64 | 0 | Número de adultos | |
| children | float64 | 0 | Número de crianças | 4 nulos (arredondados para 0%); tipo float por causa dos nulos |
| babies | int64 | 0 | Número de bebês | |
| meal | str | 0 | Tipo de refeição reservada: SC/Undefined (sem refeição), BB (café da manhã), HB (meia pensão), FB (pensão completa) | SC e Undefined significam o mesmo; padronizar |
| country | str | 0,41 | País de origem do hóspede (código ISO de 3 letras) | Nulos: preencher com "Desconhecido" |
| market_segment | str | 0 | Segmento de mercado da reserva (Online TA, Offline TA/TO, Direct, Corporate, Groups, Complementary, etc.) | TA = agências de viagem, TO = operadoras de turismo |
| distribution_channel | str | 0 | Canal de distribuição pelo qual a reserva chegou (TA/TO, Direct, Corporate, GDS) | Parecido com market_segment, mas não igual |
| is_repeated_guest | int64 | 0 | Indica se o hóspede já se hospedou antes (1) ou não (0) | |
| previous_cancellations | int64 | 0 | Número de reservas anteriores canceladas pelo hóspede | |
| previous_bookings_not_canceled | int64 | 0 | Número de reservas anteriores não canceladas pelo hóspede | |
| reserved_room_type | str | 0 | Código do tipo de quarto reservado | Códigos anonimizados (A, B, C...) |
| assigned_room_type | str | 0 | Código do tipo de quarto efetivamente atribuído | Pode diferir do reservado (upgrade, overbooking, etc.) |
| booking_changes | int64 | 0 | Número de alterações feitas na reserva até o check-in ou cancelamento | |
| deposit_type | str | 0 | Tipo de depósito: No Deposit, Non Refund (não reembolsável) ou Refundable (reembolsável) | |
| agent | float64 | 13,69 | ID da agência de viagens que fez a reserva | Nulo = reserva sem agência (venda direta), não é erro; é um ID, não um número para cálculo |
| company | float64 | 94,31 | ID da empresa responsável pela reserva ou pelo pagamento | 94% nulos: descartar a coluna ou criar flag tem_empresa |
| days_in_waiting_list | int64 | 0 | Dias que a reserva ficou em lista de espera antes de ser confirmada | |
| customer_type | str | 0 | Tipo de cliente: Contract, Group, Transient ou Transient-party | Transient = reservas individuais, não ligadas a contrato ou grupo |
| adr | float64 | 0 | Average Daily Rate: diária média (receita de hospedagem dividida pelo total de noites) | Valores ≤ 0 (1.960 registros), mínimo -6,38 e outlier de 5400 |
| required_car_parking_spaces | int64 | 0 | Vagas de estacionamento solicitadas | |
| total_of_special_requests | int64 | 0 | Número de pedidos especiais (cama extra, andar alto, etc.) | |
| reservation_status | str | 0 | Último status da reserva: Canceled, Check-Out ou No-Show | Não usar como variável preditora (ver nota abaixo) |
| reservation_status_date | str | 0 | Data em que o último status foi definido | Está como texto: converter para data no ETL |