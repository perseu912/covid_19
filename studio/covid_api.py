import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import pandas as pd
from collections import namedtuple as nt

def data_from_path(city,path):
    print('lendo o arquivo...')
    data = pd.read_csv(path,sep=',')
    print('arquivo lido!')
    print('organizando informações...')
    confirmados = data['last_available_confirmed'][::-1]
    mortos = data['last_available_deaths'][::-1]
    casos_diarios = data['new_confirmed'][::-1]
    mortes_diarias = data['new_deaths'][::-1]

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

        

def play_dados(city,state,login):
    path = get_io_data(city,state,login[0],login[1])
    if(path):
        dados = data_from_path(city,path)
        return plot_media_(dados,city,state),dados
    else:
        print('path não encontrado')
        
        
