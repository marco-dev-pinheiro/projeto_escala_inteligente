
CREATE TABLE funcionarios (
    id SERIAL PRIMARY KEY,               
    nome VARCHAR(100) NOT NULL,                 
    cargo VARCHAR(100) NOT NULL,                 
    turno VARCHAR(50) NOT NULL,                     
    qtd_folgas_mensais INT NOT NULL,                
    qtd_folgas_compensatorias INT NOT NULL          
);