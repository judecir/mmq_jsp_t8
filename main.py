# Universidade Federal do Ceará
# Departamento de Estatística e Matemática Aplicada
# Mestrado em Modelagem e Métodos Quantitativos
# Aluno: Judecir Cavalcante (judecir@gmail.com)
# Orientador: Rafael Andrade (rca.ufc@gmail.com)
import os
import pandas as pd

#os.chdir("C:/Users/User/Google Drive/UFC/MMQ/PESQUISA/MODELO DO ARRANJO LINEAR MÍNIMO PARA JOB SHOP/CODIGOS/scripts")
#os.chdir("C:/Users/User/Documents/Python Scripts/teste_mmq_jsp_minla") 
  
from pre_processamento import criar_instancias

from modelos import jsp_get_dimensoes,\
                    jsp_disjuntivo_minla,\
                    jsp_manne_rest_ordem_maq_job,\
                    jsp_manne_rest_precedencia,\
                    jsp_manne_rest_makespan,\
                    jsp_minla_rest_soma_z_1,\
                    jsp_minla_rest_desig_triang,\
                    jsp_minla_rest_permut,\
                    jsp_minla_rest_arc_in_out,\
                    jsp_minla_rest_soma_trivial,\
                    jsp_minla_rest_1_maq_j,\
                    jsp_minla_rest_ub_x,\
                    jsp_minla_rest_linear_y,\
                    jsp_minla_rest_ub_cmax,\
                    jsp_minla_rest_lb_1_maq_j,\
                    jsp_minla_rest_lb_1_maq_j_p_menos,\
                    jsp_minla_rest_lb_cmax_p_mais,\
                    jsp_minla_rest_lb_cmax_x_p_mais

from resolucao import teste_restricoes_minla, teste_manne_minlafav

from pos_processamento import criar_df_comparacao

restricoes_manne = [jsp_manne_rest_ordem_maq_job
                    ,jsp_manne_rest_precedencia
                    ,jsp_manne_rest_makespan]
        
restricoes_minla =  [jsp_minla_rest_soma_z_1
                    ,jsp_minla_rest_desig_triang
                    ,jsp_minla_rest_permut
                    ,jsp_minla_rest_arc_in_out
                    ,jsp_minla_rest_soma_trivial
                    ,jsp_minla_rest_1_maq_j
                    ,jsp_minla_rest_ub_x
                    ,jsp_minla_rest_linear_y
                    ,jsp_minla_rest_ub_cmax
                    ,jsp_minla_rest_lb_1_maq_j
                    ,jsp_minla_rest_lb_1_maq_j_p_menos
                    ,jsp_minla_rest_lb_cmax_p_mais
                    ,jsp_minla_rest_lb_cmax_x_p_mais]     
             
#teste_restricoes_minla(restricoes_manne, restricoes_minla, prefix_arq = "t_rest_", tam_amostra=1, intervalo_amostra=1)

df = teste_manne_minlafav(prefixo_arq="1a_sol_viavel_", 
                          tam_amostra=35,
                          tempo_max=3600, 
                          fl_primeira_sol=True)
df_comp = criar_df_comparacao(df)

flags = 100*df_comp[["fl_funcao_objetivo",\
             "fl_best_bound", \
             "fl_mip_relative_gap", \
             "rel_fl_funcao_objetivo"]].sum()/df_comp["problema"].count()

print(" >>>>>>>>>> Resultados gerais: <<<<<<<<<<<<\n", flags)
