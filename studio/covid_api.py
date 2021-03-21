import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import pandas as pd
from collections import namedtuple as nt

dd = {}

def data_from_path(city,path):
    print('lendo o arquivo...')
    data = pd.read_csv(path,sep=',')
    print('arquivo lido!')
    data.to_excel(f'data_{city}.xlsx')
    print('organizando informações...')
    confirmados = data['last_available_confirmed'][::-1]
    mortos = data['last_available_deaths'][::-1]
    casos_diarios = data['new_confirmed'][::-1]
    mortes_diarias = data['new_deaths'][::-1]
    population = data['estimated_population'][::-1]

    meses = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
    date = data['date'][::-1]
    date = [i[4:] for i in date]
    
    print('informações organizadas!')
    #print(int(date[0][2:3]))
    print('construindo um novo DataFrame...')
    date = [('/').join([i[4:],meses[int(i[1:3])-1]]) for i in date]

    dados = {'confirmados':np.array(confirmados),
         'mortos':np.array(mortos),
         'mortes_diarias':abs(np.array(mortes_diarias)),
         'casos_diarios':abs(np.array(casos_diarios)),
         'population':np.array(population),
         'date':date}
    dados = pd.DataFrame(dados,index=date)
    print('DataFrame construido com sucesso!')
    print('criando excel com os dados...')
    dados.to_excel(f'dados_{city}.xlsx')
    print('Excel criado com sucesso')
    print('dados ok!')
    return dados
    


def calcSma(data, smaPeriod):
    j = next(i for i, x in enumerate(data) if x is not None)
    our_range = range(len(data))[j + smaPeriod - 1:]
    empty_list = [None] * (j + smaPeriod - 1)
    sub_result = [np.mean(data[i - smaPeriod + 1: i + 1]) for i in our_range]
    
    return np.array(empty_list + sub_result)



def plot_media_(dados,city,state):
    ax = dados.plot(x='date',y='casos_diarios',kind='bar',color='black')
    print(f'encontrando a média móvel de casos confirmados em {city}-{state}...')
    casos_diarios = dados['casos_diarios']
    media = calcSma(casos_diarios,7)
    media_casos = media
    plt.plot(dados['date'],media,label='media móvel',c='red')
    
    print('configurando o plot...')
    ticklabels = ['']*len(dados.index)
    ticklabels[::20] = dados['date'][::20]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.gcf().autofmt_xdate()
    
    print(f'casos de covid-19 em {city}')
    plt.legend()
    plt.xlabel('data')
    plt.ylabel('numero de pessoas')
    plt.title(f'casos diarios em covid-19 em {city}-{state}')
    print('salvando plotagem de media movel de casos...')
    plt.savefig(f'plot_media_{city}.jpg',dpi=800)
    print('plotagem salva!')
    plt.show()
    
    plt_casos = plt
    
    print('limpando painel de plots...')
    plt.cla()
    plt.clf()
    
    print('recomeçando do zero!')
    ax = dados.plot(x='date',y='mortes_diarias',kind='bar',color='black')
    
    print(f'encontrando a média móvel de mortes em {city}-{state}...')
    mortes_diarias = dados['mortes_diarias']
    media = calcSma(mortes_diarias,7)
    media_mortes = media
    plt.plot(dados['date'],media,label='media móvel',c='red')
    
    print('configurando o ticklabels...')
    ticklabels = ['']*len(dados.index)
    ticklabels[::20] = dados['date'][::20]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.gcf().autofmt_xdate()
    
    print(f'media movel de mortos da covid-19 em {city}-{state}')
    plt.legend()
    plt.xlabel('data')
    plt.ylabel('numero de pessoas')
    plt.title(f'mortes diarias em covid-19 em {city}-{state}')
    print('salvando a plotagem de media movel de mortes...')
    plt.savefig(f'plot_mortes_media_{city}.jpg',dpi=800)
    print('plotagem salva!')
    plt.show()
    
    plt_mortes = plt
    
    print('Fim das plotagens!')
    print('organizando informações para envio...')
    media_ = nt('media_movel',['plt_casos','plt_mortes','media_casos','media_mortes'])
    print('pronto!')
    return media_(plt_casos,plt_mortes,media_casos,media_mortes)



#nome = 'reinan912'
#senha = 'imaginando912'


#############requisição dos dados do IO.Brasil
def get_io_data(city,state,name,password):
    #nome = 
    import requests as rq
    import mechanicalsoup as ms
    #from bs4 import beautifulsoup as bs
    import mechanicalsoup

    userAgent = 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36'

    br = mechanicalsoup.StatefulBrowser()
    print('modificando os agentes')
    br.session.headers = {"User-Agent":userAgent} #
    br.session.headers.update({"User-Agent":userAgent }) 
    
    print('abrindo site...')
    url = (f'https://brasil.io/dataset/covid19/caso_full/?state={state}&city={city}&format=csv')
    res = br.get(url)

    #salva os status da pagina
    res.raise_for_status()
    if ("entrar" in str(res.content)):
        #print(res.content)
        print('Atenção: login requerido!')
        
        br.open(url)
        print(f'enviando dados de login [nome:{name}, senha: {password}]...')
        
        br.select_form()
        br['username'] = name
        br['password'] = password
        br.launch_browser()
        print('Login enviado!')
        
        res = br.submit_selected()
        
        if('tente novamente' in str(res.content)):
            print("Login incorreto!")
            return False 
            
        else:
            print('Login aceito!')
            filename = f'{city}.csv'
            print(f'tentando baixar {filename}...')
            
            res = br.get(url)
            res.raise_for_status()
            
            with open(filename,'wb') as file:
                file.write(res.content)
            print('verifica ai se foi')
            
            return filename

        

def play_data_full(city,state,login):
    path = get_io_data(city,state,login[0],login[1])
    if(path):
        dados = data_from_path(city,path)
        return plot_media_(dados,city,state),dados
    else:
        print('path não encontrado')
        

        
def data_from_city(city,state,login):
   path = get_io_data(city,state,login[0],login[1])
   if(path):
      dados = data_from_path(city,path)
      return dados
   else:
      print('path não encontrado')

med_movel = calcSma



####
# plot periodo passado de casos
####
def plot_media_period_cases(dados,city,state,size=30):
   dados = dados[-size:]
   ax = dados.plot(x='date',y='casos_diarios',kind='bar',color='black')
   print(f'encontrando a média móvel de casos confirmados em {city}-{state}...')
   casos_diarios = dados['casos_diarios']
   media = calcSma(casos_diarios,7)
   media_casos = media
   plt.plot(dados['date'],media,label='media móvel',c='red')
   
   print('configurando o plot...')
   ticklabels = ['']*len(dados.index)
   ticklabels[::3] = dados['date'][::3]
   ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
   plt.gcf().autofmt_xdate()
   
   print(f'casos de covid-19 em {city}')
   plt.legend()
   plt.xlabel('data')
   plt.ylabel('numero de pessoas')
   plt.title(f'casos diarios em covid-19 em {city}-{state} nos últimos {size} dias')
   print('salvando plotagem de media movel de casos...')
   plt.savefig(f'plot_media_period_cases_{size}_{city}.jpg',dpi=800)
   print('plotagem salva!')
   plt.show()
   
   plt_casos = plt
   
   return plt_casos



####
#plotagem de periodo de mortes
####
def plot_media_period_deaths(dados,city,state,size=30):
    dados = dados[-size:]
    ax = dados.plot(x='date',y='mortes_diarias',kind='bar',color='black')
    
    print(f'encontrando a média móvel de mortes em {city}-{state}...')
    mortes_diarias = dados['mortes_diarias']
    media = calcSma(mortes_diarias,7)
    media_mortes = media
    plt.plot(dados['date'],media,label='media móvel',c='red')
    
    print('configurando o ticklabels...')
    ticklabels = ['']*len(dados.index)
    ticklabels[::3] = dados['date'][::3]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.gcf().autofmt_xdate()
    
    print(f'media movel de mortos da covid-19 em {city}-{state} nos últimos 30 dias')
    plt.legend()
    plt.xlabel('data')
    plt.ylabel('numero de pessoas')
    plt.title(f'mortes diarias em covid-19 em {city}-{state} nos últimos 30 dias')
    print('salvando a plotagem de media movel de mortes...')
    plt.savefig(f'plot_mortes_media_deaths_{size}_{city}.jpg',dpi=800)
    print('plotagem salva!')
    plt.show()
    
    plt_mortes = plt
    
    return plt_mortes
#calcula a porcentagem do crescimento da lista em um
#determinado periodo
####
def per_size(lis,size):
   init = float(lis[-(size)])
  # print(init)
   end = float(lis[-1])
  # print(end)
   return float((end-init)/init) * 100
   
   
   
####
#porcentagem do crescimento de casos confirmados
####
def percent_mortes(dados,size):
   mortes_mov = med_movel(dados['mortes_diarias'],7)
   per_mortes = per_size(mortes_mov,size)
   per_mortes = round(per_mortes,2)
   param_mortes = 'subiu' if(per_mortes>0) else 'caiu'
   return per_mortes, param_mortes



####
#porcentagem do crescimento de mortes
####
def percent_casos(dados,size):
   casos_mov = med_movel(dados['casos_diarios'],7)
   per_casos = per_size(casos_mov,size)
   per_casos = round(per_casos,2)
   param_casos = 'subiu' if(per_casos>0) else 'caiu'
   return per_casos, param_casos



####
#porcentagem basica do crescimento de mortos
####
def percent_mortes_basic(dados,size):
   list_mortos = dados['mortos']
   diff = (int(list_mortos[-1]) - int(list_mortos[-size]))
   per_mortes_basic = diff/int(list_mortos[-size])
   per_mortes_basic = round(per_mortes_basic*100,2)
   return per_mortes_basic,diff



####
#porcentagem basicado do crescimento de casos
####
def percent_casos_basic(dados,size):
   list_casos = dados['confirmados']
   diff = (int(list_casos[-1]) - int(list_casos[-size]))
   per_casos_basic = diff/int(list_casos[-size])
   per_casos_basic = round(per_casos_basic*100,2)
   return per_casos_basic,diff

#path_city = dd['path_city']
def puts(inpt):
   path_city = dd['path_city']
   print(inpt)
   with open(path_city,'a') as file:
      file.write(f'{inpt}\n')