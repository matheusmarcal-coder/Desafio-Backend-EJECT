class Cliente: 
    nome = ''
    email = ''
    endereco = ''
    cpf = ''

cliente1= Cliente()
cliente1.nome ='fulano de tal' 
cliente1.email= 'emailaleatorio@gmail.com'
cliente1.endereco='rua tanto faz'
cliente1.cpf = '123.456.789-00'


print(vars(cliente1))