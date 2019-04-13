# Escarafuncho-Tools
Ferramenta de esteganografia. Verifica um local especificado na linha de comando a procura de arquivos compactados encondidos dentro de imagens.

>Esteganografia (do grego "escrita escondida") é o estudo e uso das técnicas para ocultar a existência de uma mensagem dentro de outra, uma forma de segurança por obscurantismo. O primeiro uso registrado da palavra data do ano de 1499, no livro Steganographia, de Johannes Trithemius.
Esteganografia é o ramo particular da criptologia que consiste em fazer com que uma forma escrita seja camuflada em outra a fim de mascarar o seu verdadeiro sentido. É importante frisar a diferença entre criptografia e esteganografia. Enquanto a primeira oculta o significado da mensagem, a segunda oculta a existência da mensagem.
Um exemplo básico de técnica moderna de esteganografia é a alteração do bit menos significativo de cada pixel de uma imagem colorida de forma a que ele corresponda a um bit da mensagem. Essa técnica, apesar de não ser ideal, pouco afeta o resultado final de visualização da imagem. (WIKIPEDIA, 2019)


## Uso

>escarafuncho [-h] (--md5 | --sha256 | --sha512) [-v] -d ROOTPATH -r REPORTPATH


```
Optional arguments:
  -h, --help            show this help message and exit
  --md5                 specifies MD5 algorithm
  --sha256              specifies SHA256 algorithm
  --sha512              specifies SHA512 algorithm
  -v, --verbose         allows progress messages to be displayed
  -d ROOTPATH, --rootPath ROOTPATH
                        specify the root path for hashing
  -r REPORTPATH, --reportPath REPORTPATH
                        specify the path for reports and logs will be written
```
## Exemplos
### Escarafunchar o pendrive conectado a porta USB

´´´
python escarafuncho --md5 -v -d E:\ -r C:\Relatórios\CASO-20190401-Contrutora Abdala

´´´

## TODO
Procurar outros tipos de arquivos.
