rendaM = float(input("Digite a renda mensal: "))
parcela = int(input("Digite o valor da parcela desejada: "))

if rendaM > 2000 and parcela <= 0.3 *  rendaM:
    print("Empréstimo aprovado!")
elif rendaM <= 2000:
    print("Empréstimo negado!: renda insuficiente.")
else:
    print("Empréstimo negado: parcela acima de 30% da renda. ")