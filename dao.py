# Description: This file contains the DAO classes for the application.
# The DAO classes are responsible for handling the database connections and queries.

# pacotes do BD
# /*
# Augusto Lescura Pinto Nusp 10677290
# Felipe Tanus Rodrigues Nusp 13692289

# */



# /*
# Package Oficial
# */
# CREATE OR REPLACE PACKAGE Oficial AS

#     --Relatorios
#     --a.i
#     PROCEDURE Relatorio_Habitantes(
#         p_CPI_Oficial IN VARCHAR2
#     );

# END Oficial;


# /

# /*
# Package Lider Faccao
# */


# CREATE OR REPLACE PACKAGE Pacote_Lider AS
#     -- Funcionalidades
#     --a.i
#     PROCEDURE Alterar_Nome_Faccao(
#         p_nome_faccao IN VARCHAR2,
#         p_novo_nome IN VARCHAR2
#     );
#     --a.ii
#     PROCEDURE Indicar_Novo_Lider(
#         p_CPI_lider in VARCHAR2,
#         p_CPI_novo_lider in VARCHAR2
#     );
#     --a.iii
#     PROCEDURE Lider_Insere_Pariticipa(
#         p_nome_faccao IN VARCHAR2,
#         p_especie IN VARCHAR2,
#         p_comunidade IN VARCHAR2
#     );
#     --b
#     PROCEDURE remover_faccao_de_nacao(
#         p_nome_faccao IN VARCHAR2,
#         p_nome_nacao IN VARCHAR2
#     );

#     --Relatorios
#     --a.i
#     PROCEDURE Relatorio_Comunidades(
#         p_nome_faccao IN VARCHAR2
#     );

# END Pacote_Lider;

# /

# CREATE OR REPLACE PACKAGE BODY Pacote_Lider AS

#     -- Funcionalidades
#     --a.i
#     PROCEDURE Alterar_Nome_Faccao(
#         p_nome_faccao IN VARCHAR2,
#         p_novo_nome IN VARCHAR2
#     )
#     IS
#     BEGIN
#         UPDATE FACCAO SET NOME = p_novo_nome
#         WHERE NOME = p_nome_faccao;

        

#         EXCEPTION
#         WHEN ACCESS_INTO_NULL THEN RAISE_APPLICATION_ERROR(-20099, 'Nao foi possivel acessar a tabela de Faccao');
#         WHEN DUP_VAL_ON_INDEX THEN RAISE_APPLICATION_ERROR(-20098, 'O nome fornecido ja foi cadastrado');
#         WHEN STORAGE_ERROR THEN RAISE_APPLICATION_ERROR(-20097, 'Ocorreu um erro ao salvar os dados');
#     END Alterar_Nome_Faccao;
#     --a.ii
#     PROCEDURE Indicar_Novo_Lider(
#         p_CPI_lider in VARCHAR2,
#         p_CPI_novo_lider in VARCHAR2
#     )
#     IS
#     BEGIN
#         UPDATE FACCAO SET LIDER = p_CPI_novo_lider
#         WHERE LIDER = p_CPI_lider;

#         EXCEPTION
#         WHEN ACCESS_INTO_NULL THEN RAISE_APPLICATION_ERROR(-20099, 'Nao foi possivel acessar a tabela de Faccao');
#         WHEN STORAGE_ERROR THEN RAISE_APPLICATION_ERROR(-20097, 'Ocorreu um erro ao salvar os dados');
#     END Indicar_Novo_Lider;
#     --a.iii
#     PROCEDURE Lider_Insere_Pariticipa(
#         p_nome_faccao IN VARCHAR2,
#         p_especie IN VARCHAR2,
#         p_comunidade IN VARCHAR2
#     )
#     IS
#     BEGIN
#         INSERT INTO LIDER_PARTICIPA(FACCAO,COMUNIDADE,ESPECIE)
#                     VALUES(p_nome_faccao,p_comunidade,p_especie);
#         EXCEPTION
#         WHEN STORAGE_ERROR THEN RAISE_APPLICATION_ERROR(-20097, 'Ocorreu um erro ao salvar os dados');
#     END Lider_Insere_Pariticipa;
#     --b
#     PROCEDURE remover_faccao_de_nacao(
#         p_nome_faccao IN VARCHAR2,
#         p_nome_nacao IN VARCHAR2
#     )
#     IS
#         v_faccao_existe NUMBER;
#         v_nacao_existe NUMBER;
#         v_associacao_existente NUMBER;
#     BEGIN
#         -- Verificar se a fac��o existe
#         SELECT COUNT(*)
#         INTO v_faccao_existe
#         FROM FACCAO
#         WHERE NOME = p_nome_faccao;

#         IF v_faccao_existe = 0 THEN
#             RAISE_APPLICATION_ERROR(-20003, 'A fac��o especificada n�o foi encontrada.');
#         END IF;

#         -- Verificar se a na��o existe
#         SELECT COUNT(*)
#         INTO v_nacao_existe
#         FROM NACAO
#         WHERE NOME = p_nome_nacao;

#         IF v_nacao_existe = 0 THEN
#             RAISE_APPLICATION_ERROR(-20004, 'A na��o especificada n�o foi encontrada.');
#         END IF;

#         -- Verificar se a associa��o entre a fac��o e a na��o existe
#         SELECT COUNT(*)
#         INTO v_associacao_existente
#         FROM NACAO_FACCAO
#         WHERE FACCAO = p_nome_faccao
#         AND NACAO = p_nome_nacao;

#         IF v_associacao_existente = 0 THEN
#             RAISE_APPLICATION_ERROR(-20005, 'A fac��o n�o est� associada � na��o especificada.');
#         END IF;
        
#         -- Verificar se a fac��o j� foi removida anteriormente
#         SELECT COUNT(*)
#         INTO v_faccao_existe
#         FROM FACCAO
#         WHERE NOME = p_nome_faccao;

#         IF v_faccao_existe = 0 THEN
#             RAISE_APPLICATION_ERROR(-20006, 'A fac��o especificada j� foi removida anteriormente.');
#         END IF;

#         -- Remover a fac��o da na��o
#         DELETE FROM NACAO_FACCAO
#         WHERE FACCAO = p_nome_faccao
#         AND NACAO = p_nome_nacao;
        
#         DBMS_OUTPUT.PUT_LINE('A fac��o ' || p_nome_faccao || ' foi removida da na��o ' || p_nome_nacao);

#         EXCEPTION
#         WHEN NO_DATA_FOUND THEN
#             RAISE_APPLICATION_ERROR(-20001, 'Erro ao verificar a exist�ncia da fac��o ou da na��o.');
#         WHEN OTHERS THEN
#             RAISE_APPLICATION_ERROR(-20002, 'Erro ao remover a fac��o da na��o: ' || SQLERRM);
#     END remover_faccao_de_nacao;


#     --Relatorios
#     --a.i
#     PROCEDURE Relatorio_Comunidades(
#         p_nome_faccao IN VARCHAR2
#     )
#     IS
#         CURSOR C_COMUNIDADES IS SELECT H.PLANETA, H.COMUNIDADE, H.ESPECIE, C.QTD_HABITANTES, D.NACAO, H.DATA_INI
#                                 FROM PARTICIPA P 
#                                 JOIN HABITACAO H ON P.COMUNIDADE = H.COMUNIDADE AND P.ESPECIE = H.ESPECIE
#                                 JOIN COMUNIDADE C ON H.COMUNIDADE = C.NOME AND H.ESPECIE = C.ESPECIE
#                                 JOIN DOMINANCIA D ON H.PLANETA = D.PLANETA
#                                 WHERE P.FACCAO = p_nome_faccao
#                                 GROUP BY  H.PLANETA, H.COMUNIDADE, H.ESPECIE, C.QTD_HABITANTES, D.NACAO, H.DATA_INI
#                                 ORDER BY H.PLANETA;
#         V_COMUNIDADES C_COMUNIDADES%ROWTYPE;
#     BEGIN
#         OPEN C_COMUNIDADES;
#             LOOP
#                 FETCH C_COMUNIDADES INTO V_COMUNIDADES;
#                 EXIT WHEN C_COMUNIDADES%NOTFOUND;
#             END LOOP;
#         CLOSE C_COMUNIDADES;
#         EXCEPTION
#         WHEN ACCESS_INTO_NULL THEN RAISE_APPLICATION_ERROR(-20091, 'Nao foi possivel acessar as tabelas da busca');
#     END Relatorio_Comunidades;
# END Pacote_Lider;


# /
# --Comandante a.i

# CREATE OR REPLACE TRIGGER CHECK_VAZIO_FED
# BEFORE DELETE ON NACAO
# FOR EACH ROW
# DECLARE
#     PRAGMA AUTONOMOUS_TRANSACTION;
#     V_COUNT INTEGER;
# BEGIN
#     -- CONTAR QUANTAS NACOES AINDA REFERENCIAM A MESMA FEDERACAO
#     SELECT COUNT(*)
#     INTO V_COUNT
#     FROM NACAO
#     WHERE FEDERACAO = :OLD.FEDERACAO;

#     -- SE � A �LTIMA NACAO, LEVANTAR UMA EXCE��O
#     IF V_COUNT = 1 THEN
#         DELETE FROM FEDERACAO F WHERE F.NOME = :OLD.FEDERACAO;
#     END IF;
# EXCEPTION
#     WHEN TOO_MANY_ROWS THEN RAISE_APPLICATION_ERROR(-20090,'Existem muitas na��es que est�o vinculadas a essa federacao');
#     WHEN STORAGE_ERROR THEN RAISE_APPLICATION_ERROR(-20089,'Ocorreu um erro ao tentar deletar a federacao');
# END;



# /*

# Package Comandante

# */


# /
# create or replace PACKAGE COMANDANTE AS

#     --Funcionalidades
#     --a.i.1
#     PROCEDURE INSERE_FEDERACAO (
#         P_NACAO NACAO.NOME%TYPE,
#         P_FEDERACAO_NOVA FEDERACAO.NOME%TYPE
#     );
#     --a.i.2
#     PROCEDURE EXCLUI_FEDERACAO (
#         P_NACAO NACAO.NOME%TYPE
#     );
#     --a.ii
#     PROCEDURE CRIA_FEDERACAO (
#         P_NACAO NACAO.NOME%TYPE,
#         P_FEDERACAO FEDERACAO.NOME%TYPE
#     );
#     --b
#     PROCEDURE NOVA_DOMINANCIA (
#         P_NACAO NACAO.NOME%TYPE,
#         P_PLANETA PLANETA.ID_ASTRO%TYPE
#     );

#     --Relatorios
#     --a.i
#     PROCEDURE RECUPERA_INFORMACOES(
#         P_NACAO NACAO.NOME%TYPE
#     );
#     --a.ii
#     PROCEDURE PLANETAS_PONTENCIAIS(
#        P_CPI LIDER.CPI%TYPE
#     );
# END COMANDANTE;
# /
# create or replace PACKAGE BODY COMANDANTE AS

#     --Funcionalidades
#      --a.i.1
#     PROCEDURE INSERE_FEDERACAO (
#         P_NACAO NACAO.NOME%TYPE,
#         P_FEDERACAO_NOVA FEDERACAO.NOME%TYPE
#     )
#     IS
#     BEGIN
#         UPDATE NACAO SET FEDERACAO = P_FEDERACAO_NOVA
#         WHERE NOME = P_NACAO;

#         EXCEPTION 
#         WHEN ACCESS_INTO_NULL THEN RAISE_APPLICATION_ERROR(-20091, 'Nao foi possivel acessar as tabela de Nacoes');
#         WHEN STORAGE_ERROR THEN RAISE_APPLICATION_ERROR(-20088,'Ocorreu um erro ao tentar salvar a operacao');
#     END INSERE_FEDERACAO;
#     --a.i.2
#     PROCEDURE EXCLUI_FEDERACAO (
#         P_NACAO NACAO.NOME%TYPE
#     )
#     IS
#     BEGIN
#         UPDATE NACAO SET FEDERACAO = NULL
#         WHERE NOME = P_NACAO;
#         EXCEPTION 
#         WHEN ACCESS_INTO_NULL THEN RAISE_APPLICATION_ERROR(-20091, 'Nao foi possivel acessar as tabela de Nacoes');
#         WHEN STORAGE_ERROR THEN RAISE_APPLICATION_ERROR(-20088,'Ocorreu um erro ao tentar salvar a operacao');
#     END EXCLUI_FEDERACAO;
#     --a.ii
#     PROCEDURE CRIA_FEDERACAO(P_NACAO NACAO.NOME%TYPE, P_FEDERACAO FEDERACAO.NOME%TYPE)AS

#         E_JAEXISTE EXCEPTION;
#         E_INSERCAO EXCEPTION;
#         E_UPDATE EXCEPTION;
#         V_NACAO NACAO%ROWTYPE;
#         V_FEDERACAO FEDERACAO %ROWTYPE;

#         BEGIN



#         SELECT * INTO V_NACAO FROM NACAO N
#         WHERE N.NOME = P_NACAO;

#         IF V_NACAO.FEDERACAO IS NOT NULL
#         THEN RAISE E_JAEXISTE;        
#         END IF;


#         INSERT INTO FEDERACAO(NOME,DATA_FUND) 
#                     VALUES(P_FEDERACAO,SYSDATE);

#         UPDATE NACAO N SET FEDERACAO = P_FEDERACAO
#         WHERE N.NOME = P_NACAO;


#         COMMIT;        
#         EXCEPTION
#         WHEN DUP_VAL_ON_INDEX THEN RAISE_APPLICATION_ERROR(-20087,'J� existe uma federacao com este nome');
#         WHEN E_JAEXISTE THEN RAISE_APPLICATION_ERROR(-20086,'Nacao j� possui uma federacao');
#         WHEN ACCESS_INTO_NULL THEN RAISE_APPLICATION_ERROR(-20085,'Nacao n�o existe');
#         WHEN STORAGE_ERROR THEN RAISE_APPLICATION_ERROR(-20084,'Erro ao salvar a operacao');
#         WHEN ROWTYPE_MISMATCH THEN RAISE_APPLICATION_ERROR(-20083,'O nome inserido � muito grande');
#     END CRIA_FEDERACAO;
#     --b
#     PROCEDURE NOVA_DOMINANCIA (
#         P_NACAO NACAO.NOME%TYPE,
#         P_PLANETA PLANETA.ID_ASTRO%TYPE
#     )
#     IS
#         AUX NUMBER;
#     BEGIN

#         SELECT COUNT(*) INTO AUX
#         FROM PLANETA P 
#         JOIN DOMINANCIA D ON P.ID_ASTRO = D.PLANETA
#         WHERE P.ID_ASTRO = P_PLANETA;
#         IF AUX >=1 THEN
#             INSERT INTO DOMINANCIA(PLANETA,NACAO,DATA_INI)
#                         VALUES(P_PLANETA,P_NACAO,TO_DATE(SYSDATE,'DD/MM/YYYY'));
#         ELSE RAISE_APPLICATION_ERROR(-20082,'Esse planeta ja eh dominado por uma nacao');
#         END IF;
#         EXCEPTION
#         WHEN DUP_VAL_ON_INDEX THEN RAISE_APPLICATION_ERROR(-20081,'Esse planeta ja eh dominado por sua nacao');
#         WHEN STORAGE_ERROR THEN RAISE_APPLICATION_ERROR(-20080,'Erro ao salvar a operacao');
#     END NOVA_DOMINANCIA;

#     --Relatorios
#     --a.i
#     PROCEDURE RECUPERA_INFORMACOES(
#         P_NACAO NACAO.NOME%TYPE
#     )
#     IS
#         CURSOR C1 IS SELECT D.PLANETA, E.NOME AS ESPECIE, E.INTELIGENTE, C.NOME AS COMUNIDADE, C.QTD_HABITANTES, P.FACCAO
#                     FROM DOMINANCIA D 
#                     JOIN ESPECIE E ON D.PLANETA = E.PLANETA_OR
#                     JOIN COMUNIDADE C ON C.ESPECIE = E.NOME
#                     JOIN PARTICIPA P ON P.COMUNIDADE = C.NOME AND P.ESPECIE = C.ESPECIE
#                     WHERE D.NACAO = P_NACAO;
#         V_C1 C1%ROWTYPE; 
#     BEGIN   

#         OPEN C1;
#             LOOP
#                 FETCH C1 INTO V_C1;
#                 EXIT WHEN C1%NOTFOUND;
#             END LOOP;
#         CLOSE C1;
#         EXCEPTION
#         WHEN ACCESS_INTO_NULL THEN RAISE_APPLICATION_ERROR(-20079,'Nao foi possivel resgatar as informacoes da tabela');
#     END RECUPERA_INFORMACOES;
#     --a.ii
#     PROCEDURE PLANETAS_PONTENCIAIS(
#        P_CPI LIDER.CPI%TYPE
#     )
#     IS
#         CURSOR C1 IS SELECT PF.ID_ASTRO, PF.RAIO, (SELECT COUNT(*) FROM PLANETA P JOIN HABITACAO H ON P.ID_ASTRO = H.PLANETA WHERE PF.ID_ASTRO = P.ID_ASTRO) AS HABITACOES, NULL AS DIST_NACAO
#                         FROM PLANETA PF
#                         WHERE ROWNUM<=50
#                         MINUS 
#                         SELECT PF1.ID_ASTRO, PF1.RAIO, (SELECT COUNT(*) FROM PLANETA P1 JOIN HABITACAO H ON P1.ID_ASTRO = H.PLANETA WHERE PF1.ID_ASTRO = P1.ID_ASTRO)AS  HABITACOES, NULL AS DIST_NACAO
#                         FROM PLANETA PF1 JOIN DOMINANCIA D ON PF1.ID_ASTRO = D.PLANETA;
#         V_C1 C1%ROWTYPE;
#         x1 NUMBER;
#         y1 NUMBER;
#         z1 NUMBER;
#         x2 NUMBER;
#         y2 NUMBER;
#         z2 NUMBER;
#         distancia NUMBER;

#         V_LIDER LIDER%ROWTYPE;
#         V_COUNT NUMBER;

#     BEGIN

#     SELECT * INTO V_LIDER FROM LIDER WHERE CPI = P_CPI;

#     SELECT E.X, E.Y, E.Z INTO x1, y1, z1
#     FROM ESTRELA E
#     JOIN ORBITA_PLANETA O ON E.ID_ESTRELA = O.ESTRELA
#     JOIN ESPECIE ES ON ES.PLANETA_OR = O.PLANETA
#     WHERE ES.NOME = V_LIDER.ESPECIE;

#     OPEN C1;
#             LOOP
#                 FETCH C1 INTO V_C1;
#                 EXIT WHEN C1%NOTFOUND;
#                 SELECT E.X, E.Y, E.Z INTO x2, y2, z2
#                 FROM ESTRELA E
#                 JOIN ORBITA_PLANETA O ON E.ID_ESTRELA = O.ESTRELA
#                 JOIN PLANETA P ON P.ID_ASTRO = O.PLANETA
#                 WHERE P.ID_ASTRO = V_C1.ID_ASTRO AND ROWNUM<=15;
        
#                 distancia := SQRT(POWER(x2 - x1, 2) + POWER(y2 - y1, 2) + POWER(z2 - z1, 2));
#                 V_C1.DIST_NACAO := distancia;
                
#             END LOOP;            
#     CLOSE C1;
    

#     EXCEPTION
#         WHEN ACCESS_INTO_NULL THEN RAISE_APPLICATION_ERROR(-20078,'Nao foi possivel resgatar as informacoes da tabela');
#         WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20077,'Nao existem planetas validos');
#     END PLANETAS_PONTENCIAIS;
# END COMANDANTE;


# /*
# Package Cientista
# */

# /

# CREATE OR REPLACE PACKAGE CIENTISTA AS

# --OPERA��ES
# PROCEDURE CRIA_ESTRELA(P_ID ESTRELA.ID_ESTRELA%TYPE, P_NOME ESTRELA.NOME%TYPE, P_CLASSIFICACAO ESTRELA.CLASSIFICACAO%TYPE, 
#                         P_MASSA ESTRELA.MASSA%TYPE, P_X ESTRELA.X%TYPE, P_Y ESTRELA.Y%TYPE, P_Z ESTRELA.Z%TYPE);
                        
# PROCEDURE CRIA_SISTEMA(P_ESTRELA SISTEMA.ESTRELA%TYPE, P_NOME SISTEMA.NOME%TYPE);
# PROCEDURE CRIA_PLANETA(P_ID PLANETA.ID_ASTRO%TYPE, P_MASSA PLANETA.MASSA%TYPE, P_RAIO PLANETA.RAIO%TYPE, P_CLASSIFICACAO PLANETA.CLASSIFICACAO%TYPE);
# PROCEDURE CRIA_ORBITAPLANETA(P_PLANETA ORBITA_PLANETA.PLANETA%TYPE, P_ESTRELA ORBITA_PLANETA.ESTRELA%TYPE, P_MIN ORBITA_PLANETA.DIST_MIN%TYPE,
#                         P_MAX ORBITA_PLANETA.DIST_MAX%TYPE, P_PERIODO ORBITA_PLANETA.PERIODO%TYPE);
# PROCEDURE CRIA_ORBITAESTRELA(P_ORBITANTE ORBITA_ESTRELA.ORBITANTE%TYPE, P_ORBITADA ORBITA_ESTRELA.ORBITADA%TYPE, P_MIN ORBITA_ESTRELA.DIST_MIN%TYPE,
#                         P_MAX ORBITA_ESTRELA.DIST_MAX%TYPE, P_PERIODO ORBITA_ESTRELA.PERIODO%TYPE);



# --RELAT�RIOS

# PROCEDURE ESTRELA_NAO_CLASSIFICADA;


# END;

# /

# CREATE OR REPLACE PACKAGE BODY CIENTISTA AS


# --OPERA��ES
# PROCEDURE CRIA_ESTRELA (P_ID ESTRELA.ID_ESTRELA%TYPE, P_NOME ESTRELA.NOME%TYPE, P_CLASSIFICACAO ESTRELA.CLASSIFICACAO%TYPE, 
#                         P_MASSA ESTRELA.MASSA%TYPE, P_X ESTRELA.X%TYPE, P_Y ESTRELA.Y%TYPE, P_Z ESTRELA.Z%TYPE)AS
                    
    
#     E_VALOR_NULO EXCEPTION;
    
#     BEGIN
#     IF P_ID IS NOT NULL AND P_X IS NOT NULL AND P_Y IS NOT NULL AND P_Z IS NOT NULL
#     THEN
#     INSERT INTO ESTRELA(ID_ESTRELA,NOME,CLASSIFICACAO,MASSA,X,Y,Z)
#                 VALUES(P_ID, P_NOME, P_CLASSIFICACAO, P_MASSA, P_X, P_Y, P_Z);
#     ELSE
#         RAISE E_VALOR_NULO;
#     END IF;
#     COMMIT;
#     EXCEPTION
#     WHEN E_VALOR_NULO THEN DBMS_OUTPUT.PUT_LINE('Algum dos atributos principais � nulo');
#     WHEN DUP_VAL_ON_INDEX THEN DBMS_OUTPUT.PUT_LINE('J� existe uma estrela com este ID');
#     WHEN STORAGE_ERROR THEN DBMS_OUTPUT.PUT_LINE('Erro ao salvar a operacao');
#     WHEN ROWTYPE_MISMATCH THEN DBMS_OUTPUT.PUT_LINE('O nome inserido � muito grande');
#     END CRIA_ESTRELA;
    
    
#     PROCEDURE CRIA_SISTEMA(P_ESTRELA SISTEMA.ESTRELA%TYPE, P_NOME SISTEMA.NOME%TYPE) AS
        
#         E_VALOR_NULO EXCEPTION;
        
#         BEGIN
        
#         IF P_ESTRELA IS NOT NULL
#         THEN
#         INSERT INTO SISTEMA(ESTRELA, NOME)
#                     VALUES(P_ESTRELA, P_NOME);
#         ELSE
#         RAISE E_VALOR_NULO;
#         END IF;
#         COMMIT;

#         EXCEPTION
#         WHEN E_VALOR_NULO THEN DBMS_OUTPUT.PUT_LINE('O atributo estrela � nulo');
#         WHEN DUP_VAL_ON_INDEX THEN DBMS_OUTPUT.PUT_LINE('J� existe um sistema com essa estrela');
#         WHEN STORAGE_ERROR THEN DBMS_OUTPUT.PUT_LINE('Erro ao salvar a operacao');
#         WHEN ROWTYPE_MISMATCH THEN DBMS_OUTPUT.PUT_LINE('O nome inserido � muito grande');
#         END CRIA_SISTEMA;


#     PROCEDURE CRIA_PLANETA (P_ID PLANETA.ID_ASTRO%TYPE, P_MASSA PLANETA.MASSA%TYPE, P_RAIO PLANETA.RAIO%TYPE, P_CLASSIFICACAO PLANETA.CLASSIFICACAO%TYPE) AS
        
#         E_VALOR_NULO EXCEPTION;
        
#         BEGIN
        
#         IF P_ID IS NOT NULL 
#         THEN
#         INSERT INTO PLANETA(ID_ASTRO, MASSA, RAIO,  CLASSIFICACAO)
#                     VALUES(P_ID, P_MASSA, P_RAIO, P_CLASSIFICACAO);
#         ELSE RAISE E_VALOR_NULO;
#         END IF;
#         COMMIT;
#         EXCEPTION
#         WHEN E_VALOR_NULO THEN DBMS_OUTPUT.PUT_LINE('O atributo ID � nulo');
#         WHEN DUP_VAL_ON_INDEX THEN DBMS_OUTPUT.PUT_LINE('J� existe um planeta com esse ID');
#         WHEN STORAGE_ERROR THEN DBMS_OUTPUT.PUT_LINE('Erro ao salvar a operacao');
#         WHEN ROWTYPE_MISMATCH THEN DBMS_OUTPUT.PUT_LINE('O nome inserido � muito grande');
        
        
#         END CRIA_PLANETA;


#     PROCEDURE CRIA_ORBITAPLANETA(P_PLANETA ORBITA_PLANETA.PLANETA%TYPE, P_ESTRELA ORBITA_PLANETA.ESTRELA%TYPE, P_MIN ORBITA_PLANETA.DIST_MIN%TYPE,
#                             P_MAX ORBITA_PLANETA.DIST_MAX%TYPE, P_PERIODO ORBITA_PLANETA.PERIODO%TYPE) AS
        
#         E_VALOR_NULO EXCEPTION;
        
#         BEGIN
        
#         IF P_PLANETA IS NOT NULL AND P_ESTRELA IS NOT NULL
#         THEN
#         INSERT INTO ORBITA_PLANETA(PLANETA, ESTRELA, DIST_MIN, DIST_MAX, PERIODO)
#                     VALUES(P_PLANETA,P_ESTRELA,P_MIN,P_MAX,P_PERIODO);
#         ELSE RAISE E_VALOR_NULO;
#         END IF;
#         COMMIT;
#         EXCEPTION
#         WHEN E_VALOR_NULO THEN DBMS_OUTPUT.PUT_LINE('Um dos atributos � nulo');
#         WHEN DUP_VAL_ON_INDEX THEN DBMS_OUTPUT.PUT_LINE('J� existe uma orbita entre esses Astros');
#         WHEN STORAGE_ERROR THEN DBMS_OUTPUT.PUT_LINE('Erro ao salvar a operacao');
#         WHEN ROWTYPE_MISMATCH THEN DBMS_OUTPUT.PUT_LINE('O nome inserido � muito grande');
        
#         END CRIA_ORBITAPLANETA;


#     PROCEDURE CRIA_ORBITAESTRELA(P_ORBITANTE ORBITA_ESTRELA.ORBITANTE%TYPE, P_ORBITADA ORBITA_ESTRELA.ORBITADA%TYPE, P_MIN ORBITA_ESTRELA.DIST_MIN%TYPE,
#                             P_MAX ORBITA_ESTRELA.DIST_MAX%TYPE, P_PERIODO ORBITA_ESTRELA.PERIODO%TYPE)AS
        
#         E_VALOR_NULO EXCEPTION;
        
#         BEGIN
        
#         IF P_ORBITANTE IS NOT NULL AND P_ORBITADA IS NOT NULL
#         THEN
#         INSERT INTO ORBITA_ESTRELA(ORBITANTE, ORBITADA, DIST_MIN, DIST_MAX, PERIODO)
#                     VALUES(P_ORBITANTE, P_ORBITADA, P_MIN, P_MAX, P_PERIODO);
#         ELSE RAISE E_VALOR_NULO;
#         END IF;
#         COMMIT;
        
#         EXCEPTION
#         WHEN E_VALOR_NULO THEN DBMS_OUTPUT.PUT_LINE('Um dos atributos � nulo');
#         WHEN DUP_VAL_ON_INDEX THEN DBMS_OUTPUT.PUT_LINE('J� existe uma orbita entre esses Astros');
#         WHEN STORAGE_ERROR THEN DBMS_OUTPUT.PUT_LINE('Erro ao salvar a operacao');
#         WHEN ROWTYPE_MISMATCH THEN DBMS_OUTPUT.PUT_LINE('O nome inserido � muito grande');
#         END CRIA_ORBITAESTRELA;


#     --RELAT�RIOS


        
#     PROCEDURE ESTRELA_NAO_CLASSIFICADA AS
#         CURSOR C1 IS SELECT * FROM ESTRELA
#         WHERE CLASSIFICACAO IS NULL;
#         V_ESTRELA C1%ROWTYPE;
#         BEGIN
        
#         OPEN C1;
#         LOOP
#             FETCH C1 INTO V_ESTRELA;
#             EXIT WHEN C1%NOTFOUND;
#             DBMS_OUTPUT.PUT_LINE('ID: ' || V_ESTRELA.ID_ESTRELA||
#                                 ' Nome: ' || V_ESTRELA.NOME||
#                                 ' Massa: ' || V_ESTRELA.MASSA||
#                                 ' X: ' || V_ESTRELA.X||
#                                 ' Y: ' || V_ESTRELA.Y||
#                                 ' Z: ' || V_ESTRELA.Z);
#         END LOOP;
#         CLOSE C1;
#         EXCEPTION
#         WHEN NO_DATA_FOUND THEN DBMS_OUTPUT.PUT_LINE('A busca retornou vazia');
        
#         END ESTRELA_NAO_CLASSIFICADA;

# END;

from config import AccessConfig
import oracledb

class DataBaseActions:
    def __init__(self):
        self.config = AccessConfig()
        self.config.get_db_credentials()
        try:
            self.connection = oracledb.connect(
                user=self.config.ORACLE_USER,
                password=self.config.ORACLE_PASSWORD,
                dsn=self.config.ORACLE_DSN
            )
        except oracledb.DatabaseError as e:
            print(f"Erro ao conectar ao banco de dados: {e.args[0].message}")
            exit(1)

# As funcoes devem chamar os procedimentos e funcoes do banco de dados
########### funcoes de oficial #######################################

    def relatorio_habitantes(self, p_CPI_Oficial):
        with self.connection.cursor() as cursor:
            cursor.callproc('Oficial.Relatorio_Habitantes', [p_CPI_Oficial])
            print("Relatório de habitantes gerado com sucesso!")

########### funções lider faccao #####################################

    def alterar_nome_faccao(self, p_nome_faccao, p_novo_nome):
        with self.connection.cursor() as cursor:
            cursor.callproc('Pacote_Lider.Alterar_Nome_Faccao', [p_nome_faccao, p_novo_nome])
            print("Nome da facção alterado com sucesso!")


########### funções gerais de gerencia de login #####################################
    

    def fill_table_users(self):
        # criar um procedimento (PL/SQL) para encontrar líderes sem respectivas tuplas na tabela USERS e inserí-los com uma senha padrão
        # o procedimento pode ser executado manualmente, via SQL Developer
        # Userid é um id sintetico
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO USERS (Userid, Password, IdLider)
                SELECT round(DBMS_RANDOM.VALUE(1000, 9999)), standard_hash('123456', 'MD5'), Lider.CPI
                FROM Lider
                WHERE Lider.CPI NOT IN (SELECT IdLider FROM USERS)
            """)
            print("Tabela USERS preenchida com sucesso!")

    def create_table_users(self):
        # se a tabela ainda nao existir, criar
        # se existir, informar que a tabela ja existe
        # usar a funcao md5 do SGBD para armazenar os dados
        # MD5 hash tem 32 caracteres hexadecimais
        if not self.table_exists('USERS'):
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE USERS (
                            Userid NUMBER PRIMARY KEY,
                            Password VARCHAR2(32), 
                            IdLider CHAR(14) UNIQUE,
                            CONSTRAINT FK_USERS_TABLE_SG FOREIGN KEY (IdLider) REFERENCES Lider(CPI) ON DELETE CASCADE
                        )
                    """)
                    print("Tabela USERS criada com sucesso!")
                   
            except oracledb.DatabaseError as e:
                print(f"Falha na criação da USERS (tabela): {e.args[0].message}")
        else:
            print("Tabela USERS já existe! Continuando...")

        try:
            self.fill_table_users()
        except oracledb.DatabaseError as e:
            print(f"Falha no preenchimento da tabela USERS: {e.args[0].message}")
    
    def create_log_table(self):
        # se a tabela ainda nao existir, criar
        # se existir, informar que a tabela ja existe
        if not self.table_exists('LOG_TABLE'):
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE LOG_TABLE (
                            Userid NUMBER,
                            Timestamp TIMESTAMP,
                            Message VARCHAR2(255),
                            CONSTRAINT FK_LOG_TABLE_SG FOREIGN KEY (Userid) REFERENCES USERS(Userid) ON DELETE CASCADE
                        )
                    """)
                    print("Tabela LOG_TABLE criada com sucesso!")
            except oracledb.DatabaseError as e:
                print(f"Falha na criação da LOG_TABLE: {e.args[0].message}")
        else:
            print("Tabela LOG_TABLE já existe! Continuando...")
    
    def insert_log(self, user_id, message):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO LOG_TABLE (Userid, Timestamp, Message)
                VALUES (:user_id, SYSTIMESTAMP, :message)
            """, user_id=user_id, message=message)
            print("Log inserido com sucesso!")
    
    def table_exists(self, table_name):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM USER_TABLES
                WHERE TABLE_NAME = UPPER(:table_name)
            """, {'table_name': table_name})
            result = cursor.fetchone()
            return result[0] > 0

    def select(self, sql):
        with self.connection.cursor() as cursor:
            for r in cursor.execute(sql):
                print(r)

    def get_login_info(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM USERS
                WHERE UserId = :username
            """, username=username)
            return cursor.fetchone()
    
    def get_role_by_CPI(self, CPI):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT Cargo
                FROM Lider
                WHERE CPI = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] if result else 'ZEH_NGM'
        
    def get_CPI_by_userid(self, userid):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT Lider.CPI
                FROM Lider
                JOIN USERS
                ON USERS.IdLider = Lider.CPI
                WHERE USERS.Userid = :userid
            """, userid=userid)
            result = cursor.fetchone()
            return result[0] if result else None
        
    def get_name_by_userid(self, userid):
        CPI = self.get_CPI_by_userid(userid)
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome
                FROM Lider
                WHERE CPI = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] if result else None
        
    def get_faccao_by_userid(self, userid):
        CPI = self.get_CPI_by_userid(userid)
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome
                FROM faccao
                WHERE lider = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] if result else None
    
    def get_nacao_by_userid(self, userid):
        CPI = self.get_CPI_by_userid(userid)
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT nacao
                FROM lider
                WHERE CPI = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] if result else None
    
    def is_user_a_faction_leader(self, CPI):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM faccao
                WHERE lider = :CPI
            """, CPI=CPI)
            result = cursor.fetchone()
            return result[0] > 0