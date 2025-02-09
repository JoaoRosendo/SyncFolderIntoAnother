# SyncFolderIntoAnother

Notes:
Every file that is in folder 1, will be also found in folder 2, while this program runs.
This program is built for linux file system

# Verificar se replica já e igual ao source (pela hash, por exemplo)

# Se nao for:
# Ver cada um dos ficheiros no original; ver se a path existe tambem na replica e por ultimo ver se os ficheiros sao iguais
# Se forem iguais seguir para o proximo ficheiro
# Se nao forem iguais, rescrever ficheiro
# Se a path nao existir, criar e copiar ficheiro

# No final, percorrer todos os ficheiros no diretorio replica e ver se existem no diretorio source
# Se nao existirem, apagar
# Recorrentemente apagar diretorios vazios

# Ter atencao a edge cases por exemplo um ficheiro que nao devia existir mas dentro dum diretorio que DEVIA existir
