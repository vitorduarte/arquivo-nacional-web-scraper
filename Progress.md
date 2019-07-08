## Obtenção de dados do Arquivo Nacional

- [x] Entender o identificador de arquivos
    - A obtenção dos arquivos é dada via pesquisa digital.
    - Na [pesquisa](http://sian.an.gov.br/sianex/Consulta/resultado_pesquisa_pdf.asp) é possível selecionar diversos fundos.
    - A lista de todos os fundos e coleções possíveis foi disponibilizada no arquivo `collections.txt`
- [x] Iterar ao longo das páginas de pesquisa dos fundos para obter informações sobre os arquivos
- [x] Entender como realizar o download a partir dos dados de cada arquivo
- [ ] Testar em pequena escala
- [ ] Realizar validações
- [ ] Inserir logs


## Informações obtidas

- O site do arquivo nacional precisa de um login para o acesso. Como é dada a autenticação?
    R.: Podemos acessar o site utilizando cookies, não consegui obter o cookie via código, estou obtendo via navegador, caso deseje utilizar, siga esse [tutorial](https://curl.trillworks.com/)
