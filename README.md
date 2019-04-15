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

```
python escarafuncho --md5 -v -d E:\ -r "C:\Relatórios\CASO-20190401-Contrutora Abdala"


C:\Desenvolvimento\forensicTolls\python escarafuncho.py --md5 -v -d E:\ -r "C:\Relatórios\CASO-20190401-Contrutora Abdala"
Linha de comando processada com sucesso
Bemvindo ao Escarafunchador ... version 0.1
E:\call_09-50-16_OUT_0411430103660.amr......................Nada Consta
E:\TELEFONEMA_01_20171206_145311_Ivo Es.3gpp................Nada Consta
E:\20180311_083146_Beatriz.mp3..............................Nada Consta
E:\20180312_141149_Ivo Es.3gpp..............................Nada Consta
E:\20180320_150131_38824000.3gpp............................Nada Consta
E:\orchid-3479539_960_720.jpg...............................Nada Consta
E:\orch-233.jpg.............................................Nada Consta
E:\tipos-de-flores-orquídeas.jpg............................Nada Consta
E:\orquideas.jpg............................................Arquivo suspeito
E:\orch-yellow.jpg..........................................Nada Consta
E:\20180321_135421_Beatriz.3gpp.............................Nada Consta
E:\20180321_141303_941919520.3gpp...........................Nada Consta
E:\20180409_143005_30554560.3gpp............................Nada Consta
E:\20180411_134847_30554560.3gpp............................Nada Consta
E:\orquideas_brasil.jpg.....................................Arquivo suspeito
E:\System Volume Information\IndexerVolumeGuid..............Nada Consta
E:\System Volume Information\WPSettings.dat.................Nada Consta
Fim de execução
```
## TODO
Procurar outros tipos de arquivos.
