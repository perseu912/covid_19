from covid_api import play_data_full as pf
from covid_api import data_from_city as dc 
from covid_api import med_movel
from covid_api import data_from_path as dp
from covid_api import percent_casos
from covid_api import percent_mortes 
from covid_api import percent_mortes_basic
from covid_api import percent_casos_basic
from covid_api import plot_media_period_cases
from covid_api import plot_media_period_deaths
from covid_api import puts as p
from covid_api import dd 
import os 

city = "Juazeiro"
st = "BA"



login=('reinan912','imaginando912')

dd['path_city'] = f'{city}.txt'
os.system(f'rm {dd["path_city"]}')

pf(city,st,login)



#dados = dc(city,st,('reinan912','imaginando912'))
dados = dp(city,f'{city}.csv')
print(dados)

################## casos ###############
per_casos,param_casos = percent_casos(dados,14)

################ mortes #################
per_mortes, param_mortes = percent_mortes(dados,14)

############### mortalidades ################
mortos = float(dados['mortos'][-1])
confirmados = float(dados['confirmados'][-1])
N = float(dados['population'][-1])
per_mortes_hab = round((mortos*100)/N,2)
per_morte_casos = round((mortos*100)/confirmados,2)

############# crescimento basico ##############
cresc_mortes,diff_mortes = percent_mortes_basic(dados,30)
cresc_casos,diff_casos  = percent_casos_basic(dados,30)



'''
               PRINTANDO A INFORMATION 
'''
print('Dados capturados do site IO.Brasil by *Reinan.Br*')
p(f'*dados atualizados às 20:30 do dia {dados["date"][-1]}* da cidade de *{city}-{st}*')


######### printando a media movel de casos e mortes ########
path_city=f'{city}.txt'
p(10*'=+=')
#print('[ *média móvel de casos e mortes* ]')
p(f'A *média móvel de mortes* em {city} *{param_mortes} {per_mortes}%* em duas semanas')
p(10*'=+=')
p(f'A *média móvel de casos confirmados* em {city} *{param_casos} {per_casos}%* em duas semanas')


######### printando a mortalidade ######### 
p(10*'=+=')
#print('[ *mortalidade* ]')
p(f'*mortalidade* em relação aos casos confirmados *(mortes/casos)* : *{per_morte_casos}%*')
p(10*'=+=')
p(f'*mortalidade* em relação ao numero de habitantes *(mortes/hab.)* : *{per_mortes_hab}%*')

############ dados simples ############
p(10*'=+=')
#print('[ *dados simples* ]')
p(f'nos *último 30 dias*, o número de *casos confirmados* pela covid-19 subiram *{cresc_casos}%*')
p(10*'=+=')
p(f'nos *últimos 30 dias*, o número de *mortes confirmadas* pela covid-19 cresceu *{cresc_mortes}%*')
p(10*'=+=')
p(f'*número total de mortes*: *{int(mortos)} mortes*')
p(10*'=+=')
p(f'*número total de casos confirmados*: *{int(confirmados)} casos*')
p(10*'=+=')



'''
plotagens
'''
print(10*'=+=','plotagens',10*'=+=')
plot_media_period_cases(dados,city,st)
plot_media_period_deaths(dados,city,st)