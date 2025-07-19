import pandas as pd

# Exemplo de DataFrame inicial
df = pd.DataFrame({'municipio': ['Abadia de Goiás (GO)', 'Outro Município (SP)', 'Cidade sem estado']})

# Criar uma nova coluna 'estado' e atribuir o valor da coluna 'municipio'
df['estado'] = df['municipio']  # Inicialmente, o estado recebe o valor do município

# Atualizar a coluna 'municipio' para conter apenas o texto até o primeiro parêntese
df['municipio'] = df['municipio'].apply(lambda x: x.split(' (')[0])  # Pega o texto até o primeiro parêntese

# Atualizar a coluna 'estado' para pegar os 2 caracteres após o primeiro parêntese
df['estado'] = df['estado'].apply(lambda x: x[x.find('(') + 1:x.find('(') + 3] if '(' in x else None)

# Exibir o resultado final
print(df)