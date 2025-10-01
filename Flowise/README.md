# Flowise

## Passo a passo para rodar

1. Criar um `docker-compose.yml`
2. Subir os serviços 
    1. No terminal, dentro da pasta:
        1. Use o comando `docker compose up -d` para rodar o docker.

3. Baixar os modelos no Ollama
    1. Entre no container do Ollama digitando: `docker exec -it ollama bash`.
    2. Escolha o modelo de linguagem (no meu caso testei o llama3.2:3b), então dentro do container: `ollama pull llama3.2:3b`.
    3. Escolha o modelo de embedding (no meu caso foi o nomic-embed-text), ainda dentro do container: `ollama pull nomic-embed-text`.
    4. Dar um `exit` para sair do container.
    5. Teste rápido: `curl http://localhost:11434/api/tags`, se listar os modelos, tá tudo certo.

4. Verificar se os serviços estão funcionando
    1. Acesse: [Ollama](http://localhost:11434), para verificar ser o Ollama está funcionando
        * Caso apareça "Ollama is running", deu certo!
    2. Acesse: [Qdrant](http://localhost:6333/dashboard), para verificar se o Qdrant está funcionando
        * Caso apareça uma tela semelhante a essa: ![Qdrant Home Page](qdrant.png)
        * Deu tudo certo!
    3. Acesse: [Flowise](http://localhost:3000), para verificar se o Flowise está funcionando
        * Caso apareça uma tela semelhante a essa: ![Flowise Login Page](flowise.png)
        * Deu tudo certo!
            * Login (se setou), exemplo: admin / admin123

5. Depois de logar no [Flowise](http://localhost:3000), vá até a aba **AgentFlow** e clique em **"+ Add New"**
    1. Nessa nova tela você verá que existe o botão ***"Start"***, usaremos ele logo.
    2. No canto superiror esquerdo, você verá que existe um botão de **+**
    3. Clicando nele, você arrastará a node ***"Agent"*** para tela, do lado do ***"Start"***
        1. Agora é só ligar o `Start` com o `Agent`

6. Agora vamos configurar nosso agente:
    1. Ao **clicar duas vezes no node**, aparecerá uma tela com vários campos e opções, mas vamos começar pelo **modelo** **`Model`**
    2. Selecione o modelo que você estiver usando, no meu caso é o `ChatOllama`
    3. Depois de selecionar o modelo aparecerá uma nova opção abaixo dele, `ChatOllama Parameters`
        1. Dentro dos parâmetros, já que estamos usando o docker, mudamos o `Base URL` para `http://Ollama:11434`
        2. Em `Model Name`, colocamos `llama3.2:3b`
        3. Já a temperatura, `Temperature`, depende do que você prefere para seu agente
            1. Explicando rapidamente, quanto maior mais "criatividade" o agente vai ter, mas com isso ele pode acabar inventando informações
            2. Eu recomendaria um 0.3 ou 0.4 normalmente.
        4. Os parâmetros `Top P` e `Top K` também trabalham nessa ideia de criatividade ou conservadorismo, mas não mexi neles.
        5. Os outros parâmetros não são tão relevantes, mas caso queria dar uma olhada melhor ![Parâmetros Ollama](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values)
    4. Por agora é isso no agente, mais tarde voltaremos nele.

7. Voltando para a tela inicial do Flowise, vamos agora para a aba **Document Store** para podermos aplicar o RAG
    1. Clique em **"+ Add New"** e dê um nome para esse armazenamento de documentos.
    2. Entrando nesse armazenamento clicamos em **"+ Add Document Loader"** 
        1. Agora selecione o **Document Loader** específico do tipo de arquivo que você quer utilizar
        2. Exemplo, para um .txt, pegue o Loader `Text File`
        3. Você entrará em uma tela semelhante a essa: ![Text File Loader](txt.png)
            1. Pode dar um nome caso queira (mas não é obrigatório)
            2. No `Upload File` você coloca o arquivo que será salvo
            3. E no campo `Select Text Splitter` depende que tipo de arquivo você está utilizando, mas para .txt e .pdf o recomendado é usar o `Recursive Character Text Splitter`
                1. E dentro do `Recursive Character Text Splitter`, existem campos como `Chunck Size` e `Chunck Overlap`, que seriam respectivamente, o tamanho das chuncks que serão salvas (em caracteres, que por padrão é 1000) e a quantidade de caracteres que serão sobrepostos entre as chuncks (no caso os caracteres que irão repetir para dar contexto).
            4. Pode clicar em `Preview` para ter uma noção de como estão os chuncks
            5. Por último clique me `Process` para salvar essa separação de chuncks do arquivo escolhido.

8. Agora vamos voltar para o [Qdrant](http://localhost:6333/dashboard)  
    1. Em qualquer uma das abas é possível ver que no canto superior direito tem uma chave (🔑) com o nome de **API Key**      
        1. Clique nela e de um nome para sua chave, para que assim consiga conectar o Qdrant no Flowise, por fim de um `Apply`
    2. Indo para a aba **Collections** clique em `+ Create Collection` 
        1. De um nome para a coleção e clique em `Continue`
        2. Na pergunta **What's your use case?** Clique em `Global Search`
        3. Na pergunta **What to use for search?** Clique em `Simple Single embedding`
        4. Em **Vector configuration** escreva **768** nas dimensões (pois é a quantidade que o nomic-embed-text usa) e a métrica use a `Cosine` (pois é a mais comum)
        5. Por fim clique em `Continue` e `Finish`




