import dsd, os

path = 'ADItotal\\'
lista = os.listdir(path)

dsd.limpar_arquivo('ADItotal.txt')

partes_total = []
dados_csv = []
dsd.limpar_arquivo('ADItotalpartes.txt')
dsd.write_csv_header('ADItotalpartes.txt', 'nome, tipo, processo')
contador=0



for item in lista:
    contador = contador +1
    nome_arquivo = path+item
    processo = item.replace('.html','')
         
    # carrega dados do arquivo
    html = dsd.carregar_arquivo(nome_arquivo)
    
    html = html.replace(',',';')
    html = html.replace('\n','')
    html = html.replace('  ',' ')
    
    # extrai as partes
    partes_string = dsd.extrair(html,'partes>>>>', '<div id="partes-resumidas">')
    partes = dsd.extrair_partes(partes_string)
    
    lista_das_partes = []
    lista_das_partes = dsd.listar_partes(partes_string, item.replace('.html',''))
    
    for n in lista_das_partes:
        dsd.write_csv_line('ADItotalpartes.txt',n)
    
    # extrai os andamentos
    andamentos = dsd.extrair(html,'andamentos>>>>', 'pauta>>>>')
    andamentos = dsd.extrair_andamentos(andamentos)
    
    
    #extrai os elementos do código fonte
    codigofonte =dsd.extrair(html,'fonte>>>>', 'partes>>>>')
    
    eletronico_fisico =dsd.extrair(codigofonte,'bg-primary">','</span>')
    
    sigilo =dsd.extrair(codigofonte,'bg-success">','</span>')
    
    nome_processo =dsd.extrair(codigofonte,'-processo" value="','">')
    
    numerounico  = dsd.extrair(codigofonte,'-rotulo">','</div>')
    numerounico = dsd.extrair(numerounico,': ', '')
    
    relator = dsd.extrair(codigofonte,'"Relator:','</div>')
    
    redator_acordao = dsd.extrair(codigofonte,'>Redator do acórdão:','</div>')
    
    relator_ultimo_incidente = dsd.extrair(codigofonte,
                                      'Relator do último incidente:'
                                      ,'</div>')
    
    
    #extrai os elementos da aba informações
    informacoes = dsd.extrair(html,'informacoes>>>>', '>>>>')
    
    assuntos = dsd.extrair(informacoes, '<ul style="list-style:none;">', '</ul>')
    
    procedencia = dsd.extrair(informacoes,'<div class="col-md-12 m-t-8 m-b-8">', '<div class="col-md-7 processo-detalhes-bold p-l-0">')
    
    protocolo_data = dsd.extrair(informacoes, '<div class="col-md-5 processo-detalhes-bold m-l-0">', '</div>')
    
    orgaodeorigem = dsd.extrair(informacoes, '''Órgão de Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
    
    numerodeorigem = dsd.extrair(informacoes, '''Número de Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
    
    origem  = dsd.extrair(informacoes, '''Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
                
    procedencia = dsd.extrair(informacoes, '''<span id="descricao-procedencia">''', '</span>')
    
    # extrai campos CC
    if 'ADI' in nome_processo or 'ADPF' in nome_processo or 'ADC' in nome_processo or 'ADO' in nome_processo:
        
        cc = dsd.extrair(html, 'cc>>>','')
    
            # extrai campo incidente
        incidentecc = dsd.extrair (cc, 
                                 'verProcessoAndamento.asp?incidente=',
                                 '">')   
        
        # extrai campos classe + liminar + numero
        cln = dsd.extrair(cc, 
                          '<div><h3><strong>', 
                          '</strong>')
        dsd.limpar_cln(cln)
        cln = cln.upper()
        
        # extrai numero
        numerocc = dsd.extrair (cln, ' - ', '')
        numerocc = dsd.limpar_numero(numerocc)
        
        # extrai liminar e classe    
        if 'LIMINAR' in cln:
            liminarcc = 'sim'
            classecc = dsd.extrair(cln, '', ' (MED') 
        else:
            liminarcc = 'não'
            classecc = dsd.extrair(cln, '', ' - ') 
        
        dsd.limpar_classe(classecc)
        classecc.upper()
        classecc = classecc.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
        classecc = classecc.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE','ADI')
        
        # definição de campo: origem     
        origemcc = dsd.extrair(cc,'Origem:</td><td><strong>','</strong>')
        
               
        ## definição de campo: entrada
        entradacc = dsd.extrair(cc,'Entrada no STF:</td><td><strong>','</strong>')
        entradacc = dsd.substituir_data(entradacc)
        
        ## definição de campo: relator
        relatorcc = dsd.extrair(cc,'Relator:</td><td><strong>','</strong>')
        relatorcc = relatorcc.replace('MINISTRO','')
        relatorcc = relatorcc.replace('MINISTRA','')
        
        
        ## definição de campo: distribuição
        distribuicaocc = dsd.extrair(cc,'Distribuído:</td><td><strong>','</strong>')
        distribuicaocc = dsd.substituir_data(distribuicaocc)
        
        
        ## definição de campo: requerente
        requerentecc = dsd.extrair(cc,'Requerente: <strong>','</strong>')
        requerentecc = requerentecc.replace('  ',' ')
        requerentecc = requerentecc.replace(' ;',';')
        requerentecc = requerentecc.replace('; ',';')

        requerentecc = requerentecc.replace('( CF','(CF')
        if '(CF' in requerentecc:
            requerentesplit = requerentecc.split('(CF')
            requerentecc = requerentesplit[0]
            requerentecc = requerentecc.strip()
            requerentetipo = requerentesplit[1]
            requerentetipo = dsd.extrair(requerentetipo, ';','')
            requerentetipo = requerentetipo.replace(')','')
            requerentetipocc = requerentetipo.replace('0','')
            requerentetipocc = requerentetipocc.replace(' 2','')

        else:
            requerentesplit = 'NA'
            requerentetipocc = 'NA'
        
        ## definição de campo: requerido
        requeridocc = dsd.extrair(cc,
                            'Requerido :<strong>',
                            '</strong>')
        
        ## definição de campo: dispositivo questionado
        dispositivoquestionadocc = dsd.extrair(cc,
                                         'Dispositivo Legal Questionado</b></strong><br /><pre>',
                                         '</pre>')
        dispositivoquestionadocc = dsd.limpar(dispositivoquestionadocc)
        
        ## definição de campo: resultado da liminar
        resultadoliminarcc = dsd.extrair(cc,
                                       'Resultado da Liminar</b></strong><br /><br />',
                                       '<br />')
        
        ## definição de campo: resultado final
        resultadofinalcc = dsd.extrair(cc,
                                     'Resultado Final</b></strong><br /><br />',
                                     '<br />')
        
        ## definição de campo: decisão monocrática final
        if 'Decisão Monocrática Final</b></strong><br /><pre>' in cc:
            decisaomonofinal = dsd.extrair(cc,
                                           'Decisão Monocrática Final</b></strong><br /><pre>',
                                           '</pre>')
            decisaomonofinalcc = dsd.limpar(decisaomonofinal)
        else: 
            decisaomonofinalcc = 'NA'
             
        ## definição de campo: fundamento    
        if 'Fundamentação Constitucional</b></strong><br /><pre>' in cc:
            fundamentocc = dsd.extrair(cc,
                                 'Fundamentação Constitucional</b></strong><br /><pre>',
                                 '</pre>')
            fundamentocc = dsd.limpar(fundamentocc)
        else:
            fundamentocc = 'NA'
        
        ## definição de campo: indexação
        if 'Indexação</b></strong><br /><pre>' in cc:
            indexacaocc = dsd.extrair(cc,
                                'Indexação</b></strong><br /><pre>',
                                '</pre>')
            indexacaocc = dsd.limpar(indexacaocc)        
        else:
            indexacaocc = 'NA'
            
    # criação da variável dados extraídos, com uma lista de dados
    dados = [processo, nome_processo, classecc, numerocc, incidentecc, requerentecc, 
             requerentetipocc, requeridocc, len(lista_das_partes), lista_das_partes ,len(andamentos),
             andamentos, codigofonte, eletronico_fisico, sigilo, 
             numerounico, relatorcc, relator, redator_acordao, 
             relator_ultimo_incidente, assuntos, procedencia, protocolo_data, 
             entradacc, distribuicaocc, orgaodeorigem, 
             numerodeorigem, origem, origemcc, procedencia,  
             liminarcc, dispositivoquestionadocc, resultadoliminarcc, resultadofinalcc, 
             decisaomonofinalcc, fundamentocc, indexacaocc]
    #inserir aqui o conteúdo da lista acima, trocando [] por ''
    campos = '''processo, nome_processo, classecc, numerocc, incidentecc, requerentecc, 
             requerentetipocc, requeridocc, len(partes),partes,len(andamentos),
             andamentos, codigofonte, eletronico_fisico, sigilo, 
             numerounico, relatorcc, relator, redator_acordao, 
             relator_ultimo_incidente, assuntos, procedencia, protocolo_data, 
             entradacc, distribuicaocc, orgaodeorigem, 
             numerodeorigem, origem, origemcc, procedencia,  
             liminarcc, dispositivoquestionadocc, resultadoliminarcc, resultadofinalcc, 
             decisaomonofinalcc, fundamentocc, indexacaocc'''
    campos = campos.replace('\n','')
    campos = campos.replace('             ','')
    
    dsd.write_csv_header('ADItotal.txt',campos)
    
    # grava de 500 em 500
    dados_csv.append(dados)
    if (contador)%(500) == 0:
        dsd.write_csv_lines('ADItotal.txt',dados_csv)
        dados_csv = []
        
    print(nome_processo)
    

dsd.write_csv_lines('ADItotal.txt',dados_csv)
    
print ('Gravado arquivo ADItotal.txt')
