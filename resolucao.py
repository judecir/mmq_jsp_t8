import random as rnd
import pandas as pd 
from pre_processamento import criar_instancias
                     
from pos_processamento import nome_arquivo_lp,\
                              exportar_solucao,\
                              nome_arquivo_log,\
                              criar_pasta_se_n_existe
                          
from modelos import jsp_get_dimensoes,\
                    jsp_disjuntivo_minla,\
                    jsp_disjuntivo_minla_favorito,\
                    jsp_disjuntivo_manne
                  
def escrever_solucao(s):
    if(s.has_objective()):
        print("Cmax=",round(s.get_objective_value(), 4))
        print("Detalhes", s.solve_details)
    else: 
        print("Problema inviavel")

def resolver(modelo, m, n, prefixo=""):
    with open(nome_arquivo_log(modelo.name, m, n, prefixo), 'w') as lout:
            sol= modelo.solve(log_output=lout)
    return sol

def teste_restricoes_minla(restricoes_manne, restricoes_minla, prefix_arq = "t_rest_", tam_amostra=20, intervalo_amostra=15):
    instancias = criar_instancias()
    amostra = rnd.sample(range(1, (len(instancias))-intervalo_amostra), tam_amostra)
    
    
    solucao = []
    
    f = open("solucoes/resultados.csv", "w")
    f.write("num_maquina; num_jobs; modelo; number_of_constraints; number_of_variables; best_bound; funcao_objetivo; number_of_var_values; has_hit_limit; mip_relative_gap; nb_iterations; nb_linear_nonzeros; status; time; fl_inteiro \n")
    f.close()
    
    for i in amostra: 
        for fl_inteiro in [True, False]:
        
            tempo_max=120
            id_inst = instancias[i]["id"]
            tempo = instancias[i]["tempo"]
            ordem = instancias[i]["ordem"]
            m,n = jsp_get_dimensoes(tempo)
    
            for r in range(len(restricoes_minla)):
                prefixo = "P"\
                        + "{:03d}".format(id_inst)\
                        +"M{:03d}".format(m)\
                        +"J{:03d}".format(n)\
                        +"_{:03d}".format(r)\
                        +"rest"+"_Zint"\
                        +str(fl_inteiro)
                
                print("Criando modelo: "+ prefixo)
                modelo = jsp_disjuntivo_minla(tempo,
                                             ordem, 
                                             tempo_max=tempo_max,
                                             fl_inteiro=fl_inteiro,
                                             restricoes=restricoes_manne + restricoes_minla[:r])
                print("Modelo criado!")
                #modelos.append(modelo)
                
                modelo.export(nome_arquivo_lp(modelo.name, m,n, prefixo))
                print("Resolvendo...")
                sol = resolver(modelo, m, n, prefixo)
                print("Modelo resolvido!")
                print(modelo.name, ": ")
                escrever_solucao(sol)
                exportar_solucao(sol, modelo.name, m, n, prefixo)
                solucao.append(dict({"num_maquina":m
                                     ,"num_jobs":n
                                     ,"modelo":prefixo
                                     ,"number_of_constraints":modelo.number_of_constraints
                                     ,"number_of_variables":modelo.number_of_variables
                                     ,"best_bound":sol.solve_details.best_bound
                                     ,"funcao_objetivo":sol.get_objective_value()
                                     ,"number_of_var_values":sol.number_of_var_values
                                     ,"has_hit_limit":sol.solve_details.has_hit_limit()
                                     ,"mip_relative_gap":sol.solve_details.mip_relative_gap
                                     ,"nb_iterations":sol.solve_details.nb_iterations
                                     ,"nb_linear_nonzeros":sol.solve_details.nb_linear_nonzeros
                                     ,"status":sol.solve_details.status
                                     ,"time":sol.solve_details.time
                                     ,"fl_inteiro":fl_inteiro}))
                linha = str(m)+ "; "+\
                        str(n)+ "; "+\
                        str(prefixo)+ "; "+\
                        str(modelo.number_of_constraints)+ "; "+\
                        str(modelo.number_of_variables)+ "; "+\
                        str(sol.solve_details.best_bound)+ "; "+\
                        str(sol.get_objective_value())+ "; "+\
                        str(sol.number_of_var_values)+ "; "+\
                        str(sol.solve_details.has_hit_limit())+ "; "+\
                        str(sol.solve_details.mip_relative_gap)+ "; "+\
                        str(sol.solve_details.nb_iterations)+ "; "+\
                        str(sol.solve_details.nb_linear_nonzeros)+ "; "+\
                        str(sol.solve_details.status)+ "; "+\
                        str(sol.solve_details.time)+ "; "+\
                        str(fl_inteiro)+ "; \n" 
                        
                f = open("solucoes/resultados.csv", "a")
                f.write(linha)
                f.close()
    
    
    df_sol = pd.DataFrame(solucao)
    df_sol.to_csv("solucoes/"+"info_sol"+".csv", index=False, sep=";", decimal=",")

def teste_manne_minlafav(prefixo_arq = "t_minlafav_", tam_amostra=20, tempo_max=120, fl_primeira_sol = False):
    instancias = criar_instancias()
    solucao = []
    
    criar_pasta_se_n_existe("solucoes")
    arquivo_solucao = "solucoes/"+prefixo_arq+ "_results.csv"
    f = open(arquivo_solucao, "w")
    f.write("problema;  modelo;  num_jobs;  num_maquina;  fl_inteiro;  best_bound;  funcao_objetivo;  mip_relative_gap; number_of_contraints; number_of_variables; number_of_var_values; nb_interations; nb_linear_nonzeros; status; time; has_hit_limit \n")
    f.close()
    
    for i in range(tam_amostra): 
        for fl_inteiro in [True, False]:
            id_inst = instancias[i]["id"]
            tempo = instancias[i]["tempo"]
            ordem = instancias[i]["ordem"]
            m,n = jsp_get_dimensoes(tempo)
    
            for mod in [jsp_disjuntivo_manne, jsp_disjuntivo_minla_favorito]:
                nome_problema = "ID{:03d}".format(id_inst)\
                        +"_M{:03d}".format(m)\
                        +"_J{:03d}".format(n)
                print("Criando modelo: ")
               
                modelo = mod(tempo, ordem, tempo_max=tempo_max, fl_inteiro=fl_inteiro)
                 
                if fl_primeira_sol:
                    modelo.parameters.mip.limits.solutions = 1
                
                prefixo = prefixo_arq\
                        + "_ID{:03d}".format(id_inst)\
                        +"M{:03d}".format(m)\
                        +"J{:03d}".format(n)\
                        +"_Zint"\
                        +str(fl_inteiro)\
                        +"_"+modelo.name   
                print("Modelo "+ prefixo + " criado!")
                #modelos.append(modelo)
                
                modelo.export(nome_arquivo_lp(modelo.name, m,n, prefixo))
                print("Resolvendo...")
                sol = resolver(modelo, m, n, prefixo)
                print("Modelo resolvido!")
                print(modelo.name, ": ")
                
                print(modelo.get_solve_status())
                
                escrever_solucao(sol)
                exportar_solucao(sol, modelo.name, m, n, prefixo)
                solucao.append(dict({"problema":nome_problema
                                     ,"num_maquina":m
                                     ,"num_jobs":n
                                     ,"modelo":modelo.name
                                     ,"number_of_constraints":modelo.number_of_constraints
                                     ,"number_of_variables":modelo.number_of_variables
                                     ,"best_bound":sol.solve_details.best_bound
                                     ,"funcao_objetivo":sol.get_objective_value()
                                     ,"number_of_var_values":sol.number_of_var_values
                                     ,"has_hit_limit":sol.solve_details.has_hit_limit()
                                     ,"mip_relative_gap":sol.solve_details.mip_relative_gap
                                     ,"nb_iterations":sol.solve_details.nb_iterations
                                     ,"nb_linear_nonzeros":sol.solve_details.nb_linear_nonzeros
                                     ,"status":sol.solve_details.status
                                     ,"time":sol.solve_details.time
                                     ,"fl_inteiro":fl_inteiro}))
    
                linha = nome_problema + "; "+\
                        modelo.name+ "; "+\
                        str(m)+ "; "+\
                        str(n)+ "; "+\
                        str(fl_inteiro)+ "; " +\
                        str(sol.solve_details.best_bound)+ "; "+\
                        str(sol.get_objective_value())+ "; "+\
                        str(sol.solve_details.mip_relative_gap)+ "; "+\
                        str(modelo.number_of_constraints)+ "; "+\
                        str(modelo.number_of_variables)+ "; "+\
                        str(sol.number_of_var_values)+ "; "+\
                        str(sol.solve_details.nb_iterations)+ "; "+\
                        str(sol.solve_details.nb_linear_nonzeros)+ "; "+\
                        str(sol.solve_details.status)+ "; "+\
                        str(sol.solve_details.time)+ "; "+\
                        str(sol.solve_details.has_hit_limit())+ "; "+\
                        " \n"
                        
                f = open(arquivo_solucao, "a")
                f.write(linha)
                f.close()
                
                    
    df_sol = pd.DataFrame(solucao)
    #df_sol.to_csv("solucoes/"+prefixo_arq+"_df_results"+".csv", index=False, sep=";", decimal=",")
    return df_sol

    