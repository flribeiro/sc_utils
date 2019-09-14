import os
import re
import string
import argparse
import sys
import uuid
from random import randint

def validar_cpf(ns):
   cpf = ns.cpf
   """
   Retorna o CPF válido sanitizado ou False.

   # CPFs corretos
   >>> validar_cpf('123.456.789-09')
   '12345678909'
   >>> validar_cpf('98765432100')
   '98765432100'
   >>> validar_cpf(' 123 123 123 87 ')
   '12312312387'

   # CPFs incorretos
   >>> validar_cpf('12345678900')
   False
   >>> validar_cpf('1234567890')
   False
   >>> validar_cpf('')
   False
   >>> validar_cpf(None)
   False
   """
   cpf = ''.join(re.findall(r'\d', str(cpf)))

   if not cpf or len(cpf) < 11:
      print('CPF inválido.')

   antigo = [int(d) for d in cpf]

   # Gera CPF com novos dígitos verificadores e compara com CPF informado
   novo = antigo[:9]
   while len(novo) < 11:
      resto = sum([v * (len(novo) + 1 - i) for i, v in enumerate(novo)]) % 11

      digito_verificador = 0 if resto <= 1 else 11 - resto

      novo.append(digito_verificador)

   if novo == antigo:
      print(f'CPF válido: {cpf}')
      return None

   print('CPF inválido.')

'''
 * Essa função gera um número de CPF válido.
 * @param {Boolean} formatar define se o número do CPF deve ser gerado com os pontos e hífen.
 * @return {String} CPF
 *
 * Regra de Formação
 *
 * O número de um CPF tem exatamente 9 algarismos em sua raiz e mais dois dígitos verificadores que são indicados por último.
 * Portanto, um CPF tem 11 algarismos. O número do CPF é escrito na forma abcdefghi-jk ou diretamente como abcdefghijk onde
 * os algarismos não podem ser todos iguais entre si.
 *
 *                  abc.def.ghi-jk
 *
 * O j é chamado 1° dígito verificador do número do CPF.
 *
 * O k é chamado 2° dígito verificador do número do CPF.
 *
 * Primeiro Dígito
 *
 * Para obter j multiplicamos a, b, c, d, e, f, g, h e i pelas constantes correspondentes, e somamos os resultados de cada multiplicação:
 *
 * S = 10a + 9b + 8c + 7d + 6e + 5f + 4g + 3h + 2i
 *
 * O resultado da soma é dividido por 11, e resto da divisão é tratada da seguinte forma:
 *
 * se o resto for igual a 0 ou 1, j será 0 (zero)
 * se o resto for 2, 3, 4, 5, 6, 7, 8, 9 ou 10, j será 11 - resto
 *
 * Para obter k, multiplicamos a, b, c, d, e, f, g, h, i e j pelas constantes correspondentes, e somamos os resultados de cada multiplicação:
 *
 * S = 11a + 10b + 9c + 8d + 7e + 6f + 5g + 4h + 3i + 2j
 *
 * O resultado da soma é dividido por 11, e resto da divisão é tratada da seguinte forma:
 *
 * se o resto for igual a 0 ou 1, k será 0 (zero)
 * se o resto for 2, 3, 4, 5, 6, 7, 8, 9 ou 10, k será 11 - resto
 *
 '''
def geradorDeCpf(ns):
   formatar = ns.format

   # 9 números aleatórios
   arNumeros = []
   for i in range(9):
      arNumeros.append( randint(0,9) )      

   
   # Calculado o primeiro DV
   somaJ = ( arNumeros[0] * 10 ) + ( arNumeros[1] * 9 ) + ( arNumeros[2] * 8 ) + ( arNumeros[3] * 7 )  + ( arNumeros[4] * 6 ) + ( arNumeros[5] * 5 ) + ( arNumeros[6] * 4 )  + ( arNumeros[7] * 3 ) + ( arNumeros[8] * 2 )

   restoJ = somaJ % 11

   if ( restoJ == 0 or restoJ == 1 ):
      j = 0
   else:
      j = 11 - restoJ   

   arNumeros.append( j )

   # Calculado o segundo DV
   somaK = ( arNumeros[0] * 11 ) + ( arNumeros[1] * 10 ) + ( arNumeros[2] * 9 ) + ( arNumeros[3] * 8 )  + ( arNumeros[4] * 7 )  + ( arNumeros[5] * 6 ) + ( arNumeros[6] * 5 )  + ( arNumeros[7] * 4 )  + ( arNumeros[8] * 3 ) + ( j * 2 )

   restoK = somaK % 11
   
   if ( restoK == 0 or restoK == 1 ):
      k = 0
   else:
      k = 11 - restoK      

   arNumeros.append( k )
   
   cpf = ''.join(str(x) for x in arNumeros)

   if formatar:
      return cpf[ :3 ] + '.' + cpf[ 3:6 ] + '.' + cpf[ 6:9 ] + '-' + cpf[ 9: ]
   else:
      return cpf

def geradorDeUuid(ns):
   return uuid.uuid4()

def pontes_comandos(ns):
   switcher = {
      'cartao': f'ssh -L {ns.porta}:10.215.226.71:3306 {ns.user}@bastion-sa-vpc-shared.gcp.luizalabs.com',
      'antifraude': f'ssh -L {ns.porta}:10.215.226.72:3306 {ns.user}@bastion-sa-vpc-shared.gcp.luizalabs.com',
      'nickfury': f'ssh -L {ns.porta}:10.215.226.45:3306 {ns.user}@bastion-sa-vpc-shared.gcp.luizalabs.com',
      'cdc': f'echo Ponte indisponível.',
      'valecompra': f'echo Ponte indisponível.'
   }
   return switcher.get(ns.nome, lambda: 'Ponte não definida.')

def ponte(ns):
   print(f'Estabelecendo a ponte {ns.nome} com o usuário {ns.user} na porta {ns.porta}.')
   os.system(pontes_comandos(ns))

def estabelece_vpn(ns):
   os.system(f'sudo vpnc vpn-ML.conf')

def select_generators(ns):
   switcher = {
      'cpf': geradorDeCpf,
      'uuid': geradorDeUuid
   }
   func = switcher.get(ns.type, lambda: 'Tipo inválido de gerador.')
   for n in range(ns.num):
      print(func(ns))

def parse_calling(choice, ns):
   switcher = {
      'gen': select_generators,
      'val': validar_cpf,
      'p': ponte,
      'vpn': estabelece_vpn,
   }
   func = switcher.get(choice, lambda: 'Opção inválida.')
   func(ns)

def main():
   parser = argparse.ArgumentParser(
      prog='sc_utils',
      description='App CLI destinado a automações cotidianas '
                  'para a Squad Crédito.',
      epilog='Squad Crédito - Luizalabs, 2019.'
   )
   subparsers = parser.add_subparsers(
      title='sub-comandos', 
      description='comandos válidos',
      help='help adicional', 
      dest='sp_name'
   )
   
   g_parser = subparsers.add_parser(
      'gen', 
      help='gerador de CPF/UUID'
   )
   
   g_parser.add_argument(
      '-t', '--type', 
      help='Gera um CPF válido ou UUID', 
      choices=[
         'cpf', 
         'uuid'
      ]
   )
   g_parser.add_argument(
      '-n', '--num', 
      help='Quantidade de itens a gerar', 
      type=int, 
      default=1
   )
   g_parser.add_argument(
      '-f', '--format',
      help='Formata saída para CPFs gerados', 
      action='store_true'
   )
   
   v_parser = subparsers.add_parser(
      'val', 
      help='validador de CPF'
   )
   v_parser.add_argument(
      'cpf', 
      help='CPF a ser validado (somente números)', 
      type=str
   )

   p_parser = subparsers.add_parser(
      'p', 
      help='estabelece uma das pontes'
   )
   p_parser.add_argument(
      '-n', '--nome', 
      help='nome da ponte que será estabelecida',
      choices=['cartao', 'antifraude', 'nickfury', 'cdc', 'valecompra']
   )
   p_parser.add_argument(
      '-p', '--porta', 
      help='porta usada para conexão pela ponte',
      type=int, 
      default=3390
   )
   p_parser.add_argument(
      '-u', '--user', 
      help='usuário para autenticação', 
      type=str
   )

   vpn_parser = subparsers.add_parser(
      'vpn', 
      help='estabelece vpn'
   )
   vpn_parser.add_argument(
      'vpn', 
      action='store_true', 
      default=True, 
      help=argparse.SUPPRESS
   )

   parser.add_argument(
      '--version', 
      action='version', 
      version='%(prog)s 1.0'
   )

   if len(sys.argv) == 1:
      parser.print_help(sys.stderr)
      sys.exit(1)

   args = parser.parse_args()
   # print(vars(args))

   parse_calling(args.sp_name, args)

if __name__ == "__main__":
   main()