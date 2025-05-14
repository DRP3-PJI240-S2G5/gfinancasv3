import logging
from decimal import Decimal
from django.core.paginator import Paginator
from typing import List, Dict
from django.db.models import Sum
from .models import (
    Departamento, Responsabilidade, Verba, Elemento, TipoGasto, Despesa, Subordinacao, ElementoTipoGasto, verificar_ciclo_subordinacao
)
from ..accounts.models import User
from gfinancas4.base.exceptions import BusinessError
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.db import models

logger = logging.getLogger(__name__)


def add_departamento(nome: str, description: str, tipoEntidade: str, responsavelId: int, done: bool = False) -> dict:
    """
    Adiciona um novo departamento.
    
    Args:
        nome: Nome do departamento
        description: Descrição do departamento
        tipoEntidade: Tipo de entidade
        responsavelId: ID do responsável
        done: Status de conclusão
        
    Returns:
        dict: Dados do departamento criado
        
    Raises:
        BusinessError: Se o responsável não for encontrado ou se campos obrigatórios estiverem vazios
    """
    logger.info("SERVICE add new departamento")
    
    # Validação dos campos obrigatórios
    if not nome:
        raise BusinessError("O campo 'nome' é obrigatório")
    if not description:
        raise BusinessError("O campo 'description' é obrigatório")
    if not tipoEntidade:
        raise BusinessError("O campo 'tipoEntidade' é obrigatório")
    
    try:
        responsavel = User.objects.get(id=responsavelId)
    except User.DoesNotExist:
        raise BusinessError(f"Responsável com ID {responsavelId} não encontrado.")
    
    departamento = Departamento(
        nome=nome, 
        description=description, 
        tipoEntidade=tipoEntidade, 
        responsavelId=responsavel, 
        done=done
    )
    
    departamento.save()
    logger.info("SERVICE departamento created.")

    return departamento.to_dict_json()

def update_departamento(departamento_id: int, nome: str = None, description: str = None, 
                        tipoEntidade: str = None, responsavelId: int = None, done: bool = None) -> dict:
    """
    Atualiza um departamento com os dados fornecidos.
    
    Args:
        departamento_id: ID do departamento a ser atualizado
        nome: Novo nome do departamento (opcional)
        description: Nova descrição do departamento (opcional)
        tipoEntidade: Novo tipo de entidade (opcional)
        responsavelId: Novo ID do responsável (opcional)
        done: Novo status de conclusão (opcional)
        
    Returns:
        dict: Dados do departamento atualizado
        
    Raises:
        BusinessError: Se o departamento ou o responsável não for encontrado
    """
    logger.info(f"SERVICE update departamento: {departamento_id}")
    
    try:
        departamento = Departamento.objects.get(id=departamento_id)
    except Departamento.DoesNotExist:
        raise BusinessError(f"Departamento com ID {departamento_id} não encontrado.")
    
    if nome is not None:
        departamento.nome = nome
    if description is not None:
        departamento.description = description
    if tipoEntidade is not None:
        departamento.tipoEntidade = tipoEntidade
    if responsavelId is not None:
        try:
            responsavel = User.objects.get(id=responsavelId)
            departamento.responsavelId = responsavel
        except User.DoesNotExist:
            raise BusinessError(f"Responsável com ID {responsavelId} não encontrado.")
    if done is not None:
        departamento.done = done
    
    departamento.save()
    logger.info(f"Departamento {departamento.id} atualizado com sucesso.")
    return departamento.to_dict_json()

def list_departamentos() -> List[dict]:
    logger.info("SERVICE list departamentos")
    return [item.to_dict_json() for item in Departamento.objects.all().order_by('id')]

def _verificar_ciclo_subordinacao(superior: Departamento, subordinado: Departamento, visitados=None) -> bool:
    """
    Verifica se existe um ciclo de subordinação entre dois departamentos.
    
    Args:
        superior: Departamento superior
        subordinado: Departamento subordinado
        visitados: Conjunto de IDs de departamentos já visitados na busca
        
    Returns:
        bool: True se existe um ciclo, False caso contrário
    """
    if visitados is None:
        visitados = set()
        
    # Se o departamento atual já foi visitado, temos um ciclo
    if subordinado.id in visitados:
        return True
        
    # Adiciona o departamento atual aos visitados
    visitados.add(subordinado.id)
    
    # Verifica subordinações diretas
    subordinacoes = Subordinacao.objects.filter(superior=subordinado)
    for sub in subordinacoes:
        # Se encontramos o superior em alguma subordinação, temos um ciclo
        if sub.subordinado.id == superior.id:
            return True
        # Verifica recursivamente as subordinações indiretas
        if _verificar_ciclo_subordinacao(superior, sub.subordinado, visitados):
            return True
            
    return False

def add_subordinacao(superior_id: int, subordinado_id: int, observacao: str = "") -> dict:
    """
    Adiciona uma relação de subordinação entre departamentos.
    
    Args:
        superior_id: ID do departamento superior
        subordinado_id: ID do departamento subordinado
        observacao: Observação sobre a subordinação
        
    Returns:
        dict: Dados da subordinação criada
        
    Raises:
        BusinessError: Se a subordinação já existir, se os departamentos não forem encontrados
                      ou se a subordinação criaria um ciclo
    """
    logger.info(f"SERVICE add subordinacao: {subordinado_id} subordinado a {superior_id}")
    
    try:
        superior = Departamento.objects.get(id=superior_id)
        subordinado = Departamento.objects.get(id=subordinado_id)
    except Departamento.DoesNotExist:
        raise BusinessError("Departamento não encontrado.")
    
    if Subordinacao.objects.filter(superior=superior, subordinado=subordinado).exists():
        raise BusinessError("Essa relação de subordinação já existe.")
    
    # Verifica se o departamento subordinado já possui uma subordinação direta
    if Subordinacao.objects.filter(subordinado=subordinado).exists():
        raise BusinessError("Este departamento já possui uma subordinação direta com outro departamento.")
        
    if verificar_ciclo_subordinacao(superior, subordinado):
        raise BusinessError("Não é possível criar esta subordinação pois ela criaria um ciclo na hierarquia.")
    
    subordinacao = Subordinacao(
        superior=superior, 
        subordinado=subordinado, 
        observacao=observacao)
    
    subordinacao.save()
    return subordinacao.to_dict_json()

def update_subordinacao(subordinacao_id: int, superior_id: int, subordinado_id: int, observacao: str = "") -> dict:
    """
    Atualiza uma subordinação existente.
    
    Args:
        subordinacao_id: ID da subordinação a ser atualizada
        superior_id: ID do novo departamento superior
        subordinado_id: ID do novo departamento subordinado
        observacao: Nova observação
        
    Returns:
        dict: Dados da subordinação atualizada
        
    Raises:
        BusinessError: Se a subordinação não for encontrada ou se a atualização criaria um ciclo
    """
    logger.info(f"SERVICE update subordinacao: {subordinacao_id}")
    
    try:
        subordinacao = Subordinacao.objects.get(id=subordinacao_id)
        superior = Departamento.objects.get(id=superior_id)
        subordinado = Departamento.objects.get(id=subordinado_id)
    except (Subordinacao.DoesNotExist, Departamento.DoesNotExist):
        raise BusinessError("Subordinação ou departamento não encontrado para atualização.")
    
    # Verifica se já existe uma subordinação com os mesmos departamentos
    if Subordinacao.objects.filter(superior=superior, subordinado=subordinado).exclude(id=subordinacao_id).exists():
        raise BusinessError("Essa relação de subordinação já existe.")
    
    # Verifica se o departamento subordinado já possui uma subordinação direta com outro departamento
    if Subordinacao.objects.filter(subordinado=subordinado).exclude(id=subordinacao_id).exists():
        raise BusinessError("Este departamento já possui uma subordinação direta com outro departamento.")
    
    # Verifica se a atualização criaria um ciclo
    if verificar_ciclo_subordinacao(superior, subordinado):
        raise BusinessError("Não é possível criar esta subordinação pois ela criaria um ciclo na hierarquia.")
    
    subordinacao.superior = superior
    subordinacao.subordinado = subordinado
    subordinacao.observacao = observacao
    subordinacao.save()
    
    return subordinacao.to_dict_json()

def delete_subordinacao(id):
    """Remove uma relação de subordinação existente."""
    try:
        subordinacao = Subordinacao.objects.get(id=id)
        subordinacao.delete()
        return True
    except Subordinacao.DoesNotExist:
        raise BusinessError("Subordinação não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao remover subordinação: {str(e)}")
        raise BusinessError("Erro ao remover subordinação.")

def list_subordinacoes() -> list[dict]:
    """Busca e retorna todas as relações de subordinação no formato JSON."""
    logger.info("SERVICE list subordinacoes")
    return [sub.to_dict_json() for sub in Subordinacao.objects.all()]

# SERVIÇOS PARA RESPONSABILIDADES (implementados conforme modelo e práticas)
def add_responsabilidade(usuario_id: int, departamento_id: int, observacao: str = "") -> dict:
    """
    Adiciona uma responsabilidade a um usuário em um departamento.
    
    Args:
        usuario_id: ID do usuário
        departamento_id: ID do departamento
        observacao: Observação sobre a responsabilidade
        
    Returns:
        dict: Dados da responsabilidade criada
        
    Raises:
        BusinessError: Se o usuário já for responsável pelo departamento ou se o usuário/departamento não for encontrado
    """
    logger.info(f"SERVICE add responsabilidade: {usuario_id} responsável pelo {departamento_id}")
    
    try:
        usuario = User.objects.get(id=usuario_id)
        departamento = Departamento.objects.get(id=departamento_id)
    except User.DoesNotExist:
        raise BusinessError("Usuário não encontrado.")
    except Departamento.DoesNotExist:
        raise BusinessError("Departamento não encontrado.")
    
    if Responsabilidade.objects.filter(usuario=usuario, departamento=departamento).exists():
        raise BusinessError("O usuário já é responsável por este departamento.")
    
    responsabilidade = Responsabilidade(
        usuario=usuario, 
        departamento=departamento, 
        observacao=observacao
    )
    
    responsabilidade.save()
    return responsabilidade.to_dict_json()

def update_responsabilidade(responsabilidade_id: int, observacao: str = None) -> dict:
    """
    Atualiza a responsabilidade, alterando a observação.
    
    Args:
        responsabilidade_id: ID da responsabilidade a ser atualizada
        observacao: Nova observação
        
    Returns:
        dict: Dados da responsabilidade atualizada
        
    Raises:
        BusinessError: Se a responsabilidade não for encontrada
    """
    logger.info(f"SERVICE update responsabilidade: {responsabilidade_id}")
    
    try:
        responsabilidade = Responsabilidade.objects.get(id=responsabilidade_id)
    except Responsabilidade.DoesNotExist:
        raise BusinessError("Responsabilidade não encontrada para atualização.")
    
    if observacao:
        responsabilidade.observacao = observacao
    
    responsabilidade.save()
    return responsabilidade.to_dict_json()

def list_responsabilidades() -> List[dict]:
    logger.info("SERVICE list responsabilidades")
    return [resp.to_dict_json() for resp in Responsabilidade.objects.all()]

# SERVIÇOS PARA VERBAS (ajustes e implementação faltante)
def add_verba(valor: Decimal, departamento_id: int, user_id: int, ano: int, descricao: str = "") -> dict:
    """
    Adiciona uma nova verba.
    
    Args:
        valor: Valor da verba
        departamento_id: ID do departamento
        user_id: ID do usuário
        ano: Ano da verba
        descricao: Descrição da verba
        
    Returns:
        dict: Dados da verba criada
        
    Raises:
        BusinessError: Se o valor for inválido, o ano for inválido ou se algum dos objetos relacionados não for encontrado
    """
    logger.info(f"SERVICE add verba: valor={valor}, departamento_id={departamento_id}, ano={ano}")
    
    try:
        # Validação do ano
        if ano < 1900 or ano > 2100:
            raise BusinessError("O ano deve estar entre 1900 e 2100")
            
        # Validação do valor
        if valor <= 0:
            raise BusinessError("O valor da verba deve ser maior que zero")
            
        # Busca o departamento e usuário
        try:
            departamento = Departamento.objects.get(id=departamento_id)
            user = User.objects.get(id=user_id)
        except Departamento.DoesNotExist:
            raise BusinessError("Departamento não encontrado")
        except User.DoesNotExist:
            raise BusinessError("Usuário não encontrado")
            
        # Verifica se já existe verba para o departamento no ano
        if Verba.objects.filter(departamento=departamento, ano=ano).exists():
            raise BusinessError(f"Já existe verba para o departamento {departamento.nome} no ano {ano}")
            
        # Cria a verba
        verba = Verba.objects.create(
            valor=valor,
            departamento=departamento,
            user=user,
            ano=ano,
            descricao=descricao
        )
        
        logger.info(f"Verba {verba.id} criada com sucesso: valor={valor}, departamento={departamento.nome}, ano={ano}")
        return verba.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao adicionar verba: {str(e)}", exc_info=True)
        raise BusinessError(f"Erro ao adicionar verba: {str(e)}")

def update_verba(verba_id: int, valor: Decimal, ano: int, descricao: str, departamento_id: int) -> dict:
    """
    Atualiza uma verba existente.
    
    Args:
        verba_id: ID da verba
        valor: Novo valor da verba
        ano: Novo ano da verba
        descricao: Nova descrição da verba
        departamento_id: ID do novo departamento
        
    Returns:
        dict: Dados da verba atualizada
        
    Raises:
        BusinessError: Se a verba não for encontrada, o valor for inválido, o ano for inválido 
                      ou se o departamento não for encontrado
    """
    logger.info(f"SERVICE update verba: id={verba_id}, valor={valor}, ano={ano}")
    
    try:
        # Validação do ano
        if ano < 1900 or ano > 2100:
            raise BusinessError("O ano deve estar entre 1900 e 2100")
            
        # Validação do valor
        if valor <= 0:
            raise BusinessError("O valor da verba deve ser maior que zero")
            
        # Busca a verba
        try:
            verba = Verba.objects.get(id=verba_id)
        except Verba.DoesNotExist:
            raise BusinessError("Verba não encontrada")
            
        # Busca o departamento
        try:
            departamento = Departamento.objects.get(id=departamento_id)
        except Departamento.DoesNotExist:
            raise BusinessError("Departamento não encontrado")
            
        # Verifica se já existe verba para o departamento no ano (exceto a atual)
        if Verba.objects.filter(departamento=departamento, ano=ano).exclude(id=verba_id).exists():
            raise BusinessError(f"Já existe verba para o departamento {departamento.nome} no ano {ano}")
            
        # Atualiza a verba
        verba.valor = valor
        verba.ano = ano
        verba.descricao = descricao
        verba.departamento = departamento
        verba.save()
        
        logger.info(f"Verba {verba.id} atualizada com sucesso: valor={valor}, departamento={departamento.nome}, ano={ano}")
        return verba.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar verba: {str(e)}", exc_info=True)
        raise BusinessError(f"Erro ao atualizar verba: {str(e)}")

def delete_verba(verba_id: int) -> bool:
    """
    Remove uma verba.
    
    Args:
        verba_id: ID da verba
        
    Returns:
        bool: True se a verba foi removida com sucesso
        
    Raises:
        BusinessError: Se a verba não for encontrada
    """
    logger.info(f"SERVICE delete verba: id={verba_id}")
    
    try:
        # Busca a verba
        try:
            verba = Verba.objects.get(id=verba_id)
            departamento_nome = verba.departamento.nome
            ano = verba.ano
        except Verba.DoesNotExist:
            raise BusinessError("Verba não encontrada")
            
        # Remove a verba
        verba.delete()
        logger.info(f"Verba {verba_id} removida com sucesso: departamento={departamento_nome}, ano={ano}")
        return True
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover verba: {str(e)}", exc_info=True)
        raise BusinessError(f"Erro ao remover verba: {str(e)}")

def get_verba(verba_id: int) -> dict:
    """
    Retorna os dados de uma verba específica.
    
    Args:
        verba_id: ID da verba
        
    Returns:
        dict: Dados da verba
        
    Raises:
        BusinessError: Se a verba não for encontrada
    """
    logger.info(f"SERVICE get verba: id={verba_id}")
    
    try:
        # Busca a verba
        try:
            verba = Verba.objects.get(id=verba_id)
        except Verba.DoesNotExist:
            raise BusinessError("Verba não encontrada")
            
        logger.info(f"Verba {verba_id} recuperada com sucesso")
        return verba.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar verba: {str(e)}", exc_info=True)
        raise BusinessError(f"Erro ao buscar verba: {str(e)}")

def list_verbas(page=1, per_page=10) -> List[dict]:
    """
    Lista todas as verbas cadastradas com paginação.
    
    Args:
        page (int): Número da página (começando em 1)
        per_page (int): Quantidade de itens por página
        
    Returns:
        dict: Dicionário com verbas paginadas e informações de paginação
    """
    try:
        logger.info(f"Iniciando listagem de verbas - página {page}, {per_page} itens por página")
        verbas = Verba.objects.select_related('departamento', 'user').all()
        
        # Aplicar paginação
        paginator = Paginator(verbas, per_page)
        page_obj = paginator.get_page(page)
        
        result = []
        for verba in page_obj:
            try:
                verba_dict = verba.to_dict_json()
                result.append(verba_dict)
            except Exception as e:
                logger.error(f"Erro ao serializar verba {verba.id}: {str(e)}", exc_info=True)
                continue
                
        logger.info(f"Listagem de verbas concluída com sucesso. Página {page} de {paginator.num_pages}")
        
        return {
            'verbas': result,
            'paginacao': {
                'total': paginator.count,
                'total_paginas': paginator.num_pages,
                'pagina_atual': page,
                'itens_por_pagina': per_page
            }
        }
    except Exception as e:
        logger.error(f"Erro ao listar verbas: {str(e)}", exc_info=True)
        raise BusinessError(f"Erro ao listar verbas: {str(e)}")

def list_verbas_departamento(departamento_id: int) -> List[dict]:
    """
    Lista todas as verbas de um departamento específico.
    
    Args:
        departamento_id (int): ID do departamento
        
    Returns:
        list: Lista de verbas do departamento serializadas
    """
    try:
        logger.info(f"Iniciando listagem de verbas do departamento {departamento_id}")
        
        # Verifica se o departamento existe
        try:
            departamento = Departamento.objects.get(id=departamento_id)
            logger.info(f"Departamento encontrado: {departamento.nome}")
        except Departamento.DoesNotExist:
            logger.error(f"Departamento {departamento_id} não encontrado")
            raise BusinessError(f"Departamento {departamento_id} não encontrado")
            
        verbas = Verba.objects.select_related('departamento', 'user').filter(departamento=departamento)
        logger.info(f"Encontradas {len(verbas)} verbas para o departamento {departamento.nome}")
        
        result = []
        for verba in verbas:
            try:
                verba_dict = verba.to_dict_json()
                result.append(verba_dict)
            except Exception as e:
                logger.error(f"Erro ao serializar verba {verba.id}: {str(e)}", exc_info=True)
                continue
                
        logger.info(f"Listagem de verbas do departamento {departamento.nome} concluída com sucesso. Total: {len(result)}")
        return result
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar verbas do departamento {departamento_id}: {str(e)}", exc_info=True)
        raise BusinessError(f"Erro ao listar verbas do departamento: {str(e)}")

def get_verba_departamento_ano(departamento_id: int, ano: int) -> dict:
    """
    Retorna a verba de um departamento para um ano específico.
    
    Args:
        departamento_id: ID do departamento
        ano: Ano da verba
        
    Returns:
        dict: Dados da verba
        
    Raises:
        BusinessError: Se o departamento não for encontrado, o ano for inválido 
                      ou não houver verba para o ano especificado
    """
    logger.info(f"SERVICE get verba departamento ano: departamento_id={departamento_id}, ano={ano}")
    
    try:
        # Validação do ano
        if ano < 1900 or ano > 2100:
            raise BusinessError("O ano deve estar entre 1900 e 2100")
            
        # Busca o departamento
        try:
            departamento = Departamento.objects.get(id=departamento_id)
        except Departamento.DoesNotExist:
            raise BusinessError("Departamento não encontrado")
            
        # Busca a verba
        try:
            verba = Verba.objects.get(departamento=departamento, ano=ano)
        except Verba.DoesNotExist:
            raise BusinessError(f"Não há verba para o departamento {departamento.nome} no ano {ano}")
            
        logger.info(f"Verba recuperada com sucesso: departamento={departamento.nome}, ano={ano}")
        return verba.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar verba do departamento: {str(e)}", exc_info=True)
        raise BusinessError(f"Erro ao buscar verba do departamento: {str(e)}")
    
def get_ultima_verba_departamento(departamento_id: int) -> dict:
    """
    Retorna a última verba definida para um departamento.
    
    Args:
        departamento_id: ID do departamento
        
    Returns:
        dict: Dados da última verba do departamento
        
    Raises:
        BusinessError: Se o departamento não for encontrado ou se não houver verba registrada
    """
    logger.info(f"SERVICE get ultima verba departamento: departamento_id={departamento_id}")
    
    try:
        # Busca o departamento
        try:
            departamento = Departamento.objects.get(id=departamento_id)
        except Departamento.DoesNotExist:
            raise BusinessError("Departamento não encontrado")
        
        # Busca a última verba registrada para o departamento (ordenado pelo ano de forma decrescente)
        verba = Verba.objects.filter(departamento=departamento).order_by('-ano', '-id').first()
        
        if not verba:
            raise BusinessError(f"Não há verba registrada para o departamento {departamento.nome}")
        
        logger.info(f"Última verba recuperada com sucesso: departamento={departamento.nome}, ano={verba.ano}")
        return verba.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar última verba do departamento: {str(e)}", exc_info=True)
        raise BusinessError(f"Erro ao buscar última verba do departamento: {str(e)}")

# SERVIÇOS PARA DESPESAS (existentes e já adequados)
def add_despesa(user_id: int, departamento_id: int, valor: float, elemento_id: int, 
                tipo_gasto_id: int, justificativa: str = "") -> dict:
    """
    Adiciona uma nova despesa.
    
    Args:
        user_id: ID do usuário
        departamento_id: ID do departamento
        valor: Valor da despesa
        elemento_id: ID do elemento
        tipo_gasto_id: ID do tipo de gasto
        justificativa: Justificativa da despesa
        
    Returns:
        dict: Dados da despesa criada
        
    Raises:
        BusinessError: Se o valor da despesa for inválido ou se algum dos objetos relacionados não for encontrado
    """
    logger.info(f"SERVICE add despesa: {valor} para o departamento {departamento_id}")
    
    try:
        user = User.objects.get(id=user_id)
        departamento = Departamento.objects.get(id=departamento_id)
        elemento = Elemento.objects.get(id=elemento_id)
        tipo_gasto = TipoGasto.objects.get(id=tipo_gasto_id)
    except User.DoesNotExist:
        raise BusinessError("Usuário não encontrado.")
    except Departamento.DoesNotExist:
        raise BusinessError("Departamento não encontrado.")
    except Elemento.DoesNotExist:
        raise BusinessError("Elemento não encontrado.")
    except TipoGasto.DoesNotExist:
        raise BusinessError("Tipo de gasto não encontrado.")
    
    # Verificando se o valor da despesa é válido
    if valor <= 0:
        raise BusinessError("O valor da despesa deve ser maior que zero.")
    
    valor = round(Decimal(valor), 2)
    logger.debug(f"valor: {valor}")

    # Criando uma nova instância de Despesa
    nova_despesa = Despesa(
        user=user,
        departamento=departamento,
        valor=valor,
        elemento=elemento,
        tipoGasto=tipo_gasto,
        justificativa=justificativa
    )

    # Tentando salvar a despesa
    try:
        nova_despesa.save()
    except ValidationError as e:
        raise BusinessError(f"Error de validação: {e.messages}")
    
    # Retornando o dicionário com os dados da despesa
    return nova_despesa.to_dict_json()

def _converter_valor_br_para_decimal(valor_str: str) -> Decimal:
    """
    Converte um valor no formato brasileiro (ex: 1.234,56) para Decimal.
    
    Args:
        valor_str: String contendo o valor no formato brasileiro
        
    Returns:
        Decimal: Valor convertido
        
    Raises:
        BusinessError: Se o valor não puder ser convertido
    """
    try:
        # Remove pontos de milhar e substitui vírgula por ponto
        valor_limpo = valor_str.replace('.', '').replace(',', '.')
        return Decimal(valor_limpo)
    except (ValueError, TypeError, InvalidOperation):
        raise BusinessError("Valor inválido. Use o formato brasileiro (ex: 1.234,56)")

def update_despesa(nova_despesa: Despesa) -> dict:
    """
    Atualiza os valores, justificativa, elemento e tipoGasto de uma despesa existente.
    Espera uma instância de Despesa.
    """
    logger.info(f"SERVICE update despesa: {nova_despesa.id}")
    
    if not nova_despesa.pk:
        raise BusinessError("Despesa não encontrada para atualização.")
    
    # Verificando e atualizando o valor, se fornecido
    if nova_despesa.valor is not None:
        # Se o valor for uma string, tenta converter do formato brasileiro
        if isinstance(nova_despesa.valor, str):
            nova_despesa.valor = _converter_valor_br_para_decimal(nova_despesa.valor)
        else:
            nova_despesa.valor = round(Decimal(str(nova_despesa.valor)), 2)
            
        if nova_despesa.valor <= 0:
            raise BusinessError("O valor da despesa deve ser maior que zero.")
    
    # Atualizando a justificativa, se fornecida
    if nova_despesa.justificativa:
        nova_despesa.justificativa = nova_despesa.justificativa
    
    # Atualizando o elemento, se fornecido
    if nova_despesa.elemento:
        nova_despesa.elemento = nova_despesa.elemento
    
    # Atualizando o tipoGasto, se fornecido
    if nova_despesa.tipoGasto:
        nova_despesa.tipoGasto = nova_despesa.tipoGasto
    
    # Tentando salvar as alterações
    try:
        nova_despesa.save()
    except ValidationError as e:
        raise BusinessError(f"Erro de validação: {e.messages}")
    
    # Retornando o dicionário com os dados atualizados da despesa
    return nova_despesa.to_dict_json()

def list_despesas(page=1, per_page=10) -> List[dict]:
    """Retorna todas as despesas paginadas, independentemente do departamento."""
    despesas = Despesa.objects.select_related(
        'user', 'elemento', 'tipoGasto', 'departamento'
    ).order_by("-created_at")

    paginator = Paginator(despesas, per_page)
    page_obj = paginator.get_page(page)

    despesas_serializadas = [d.to_dict_json() for d in page_obj.object_list]

    return {
        "despesas": despesas_serializadas,
        "paginacao": {
            "pagina_atual": page_obj.number,
            "total_paginas": paginator.num_pages,
            "total_despesas": paginator.count,
            "tem_proxima": page_obj.has_next(),
            "tem_anterior": page_obj.has_previous(),
        }
    }

def list_despesas_departamento(departamento_id, page=1, per_page=10) -> List[dict]:
    """Retorna todas as despesas de um departamento específico com paginação."""
    try:
        departamento = Departamento.objects.get(id=departamento_id)
        
        # Filtra as despesas do departamento
        despesas = Despesa.objects.filter(departamento=departamento).select_related(
            'user', 'elemento', 'tipoGasto'
        ).order_by("-created_at")

        # Pagina as despesas
        paginator = Paginator(despesas, per_page)
        page_obj = paginator.get_page(page)

        # Serializa as despesas da página atual
        despesas_serializadas = [despesa.to_dict_json() for despesa in page_obj.object_list]

        # Retorna o resultado com a paginação
        return {
            "despesas": despesas_serializadas,
            "paginacao": {
                "pagina_atual": page_obj.number,
                "total_paginas": paginator.num_pages,
                "total_despesas": paginator.count,
                "tem_proxima": page_obj.has_next(),
                "tem_anterior": page_obj.has_previous(),
            }
        }

    except Departamento.DoesNotExist:
        raise ValueError("Departamento não encontrado")

def list_despesas_departamento_apartir_data(departamento_id: int, data_inicio: date, page=1, per_page=10) -> dict:
    """
    Lista despesas de um departamento a partir de uma data específica, com paginação.
    
    Args:
        departamento_id: ID do departamento.
        data_inicio: Data inicial (inclusive) para filtragem.
        page: Número da página.
        per_page: Quantidade de itens por página.
    
    Returns:
        dict: Dicionário contendo despesas paginadas.
    
    Raises:
        ValueError: Se o departamento não existir.
    """
    try:
        departamento = Departamento.objects.get(id=departamento_id)

        despesas = Despesa.objects.filter(
            departamento=departamento,
            created_at__date__gte=data_inicio
        ).select_related(
            'user', 'elemento', 'tipoGasto'
        ).order_by("-created_at")

        paginator = Paginator(despesas, per_page)
        page_obj = paginator.get_page(page)

        despesas_serializadas = [d.to_dict_json() for d in page_obj.object_list]

        return {
            "despesas": despesas_serializadas,
            "paginacao": {
                "pagina_atual": page_obj.number,
                "total_paginas": paginator.num_pages,
                "total_despesas": paginator.count,
                "tem_proxima": page_obj.has_next(),
                "tem_anterior": page_obj.has_previous(),
            }
        }

    except Departamento.DoesNotExist:
        raise ValueError("Departamento não encontrado.")

def list_despesas_departamento_periodo(departamento_id, data_inicio, data_termino, page=1, per_page=10):
    """Lista despesas de um departamento em um período específico com paginação"""
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_termino = datetime.strptime(data_termino, '%Y-%m-%d')
        
        # Calcula o offset para paginação
        offset = (page - 1) * per_page
        
        # Busca as despesas do departamento no período
        despesas = Despesa.objects.filter(
            departamento_id=departamento_id,
            created_at__range=[data_inicio, data_termino]
        ).order_by('-created_at')
        
        # Aplica paginação
        total = despesas.count()
        despesas = despesas[offset:offset + per_page]
        
        # Converte para dicionário
        despesas_list = [despesa.to_dict_json() for despesa in despesas]
        
        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "results": despesas_list
        }
    except ValueError as e:
        raise BusinessError("Formato de data inválido. Use o formato YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Erro ao listar despesas do departamento: {str(e)}")
        raise BusinessError("Erro ao listar despesas do departamento")

def total_despesas_departamento_periodo(departamento_id, data_inicio, data_termino):
    """Calcula o valor total das despesas de um departamento em um período específico"""
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_termino = datetime.strptime(data_termino, '%Y-%m-%d')
        
        # Soma o valor das despesas do departamento no período
        total = Despesa.objects.filter(
            departamento_id=departamento_id,
            created_at__range=[data_inicio, data_termino]
        ).aggregate(total=models.Sum('valor'))['total'] or Decimal('0.00')
        
        return total
    except ValueError as e:
        raise BusinessError("Formato de data inválido. Use o formato YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Erro ao calcular total de despesas do departamento: {str(e)}")
        raise BusinessError("Erro ao calcular total de despesas do departamento")

# SERVIÇOS PARA ELEMENTOS (implementados conforme práticas)
def _normalizar_texto(texto: str) -> str:
    """
    Normaliza um texto removendo acentos e caracteres especiais.
    
    Args:
        texto: Texto a ser normalizado
        
    Returns:
        str: Texto normalizado
    """
    import unicodedata
    # Remove acentos
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn')
    # Converte para minúsculas
    texto = texto.lower()
    # Remove espaços extras
    texto = ' '.join(texto.split())
    return texto

def add_elemento(elemento: str, descricao: str) -> dict:
    """Adiciona um novo elemento."""
    logger.info("SERVICE add new elemento")
    
    try:
        # Validação dos campos obrigatórios
        if not elemento:
            raise BusinessError("O campo 'elemento' é obrigatório")
            
        if not descricao:
            raise BusinessError("O campo 'descricao' é obrigatório")
            
        # Normaliza o nome do elemento para comparação
        elemento_normalizado = _normalizar_texto(elemento)
            
        # Verifica se já existe um elemento com o mesmo nome (considerando normalização)
        elementos_existentes = Elemento.objects.all()
        for elem in elementos_existentes:
            if _normalizar_texto(elem.elemento) == elemento_normalizado:
                raise BusinessError(f"Já existe um elemento com o nome '{elem.elemento}'. Use um nome diferente.")
            
        elemento_obj = Elemento(
            elemento=elemento,
            descricao=descricao
        )
        
        elemento_obj.save()
        logger.info("SERVICE elemento created.")
        return elemento_obj.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao adicionar elemento: {str(e)}")
        raise BusinessError("Erro ao adicionar elemento")

def update_elemento(elemento_id: int, elemento: str, descricao: str) -> dict:
    """Atualiza um elemento existente."""
    logger.info(f"SERVICE update elemento {elemento_id}")
    
    try:
        # Validação dos campos obrigatórios
        if not elemento:
            raise BusinessError("O campo 'elemento' é obrigatório")
            
        if not descricao:
            raise BusinessError("O campo 'descricao' é obrigatório")
            
        # Verifica se o elemento existe
        try:
            elemento_obj = Elemento.objects.get(id=elemento_id)
        except Elemento.DoesNotExist:
            raise BusinessError(f"Elemento com ID {elemento_id} não encontrado")
            
        # Verifica se já existe outro elemento com o mesmo nome (exceto o atual)
        if Elemento.objects.filter(elemento=elemento).exclude(id=elemento_id).exists():
            raise BusinessError(f"Já existe um elemento com o nome '{elemento}'")
            
        elemento_obj.elemento = elemento
        elemento_obj.descricao = descricao
        elemento_obj.save()
        
        logger.info("SERVICE elemento updated.")
        return elemento_obj.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar elemento: {str(e)}")
        raise BusinessError("Erro ao atualizar elemento")

def delete_elemento(elemento_id: int) -> None:
    """Deleta um elemento."""
    logger.info(f"SERVICE delete elemento {elemento_id}")
    
    try:
        elemento = Elemento.objects.get(id=elemento_id)
        elemento.delete()
        logger.info("SERVICE elemento deleted.")
    except Elemento.DoesNotExist:
        raise BusinessError(f"Elemento com ID {elemento_id} não encontrado.")

def list_elementos() -> List[dict]:
    """Lista todos os elementos ordenados alfabeticamente por nome."""
    logger.info("SERVICE list elementos")
    try:
        return [item.to_dict_json() for item in Elemento.objects.all().order_by('elemento')]
    except Exception as e:
        logger.error(f"Erro ao listar elementos: {str(e)}")
        raise BusinessError("Erro ao listar elementos")

# SERVIÇOS PARA TIPOS DE GASTO (implementados conforme práticas)
def add_tipo_gasto(tipo_gasto: str, descricao: str) -> dict:
    """Adiciona um novo tipo de gasto."""
    logger.info("SERVICE add new tipo_gasto")
    
    try:
        # Validação dos campos obrigatórios
        if not tipo_gasto:
            raise BusinessError("O campo 'tipoGasto' é obrigatório")
            
        if not descricao:
            raise BusinessError("O campo 'descricao' é obrigatório")
            
        # Verifica se já existe um tipo de gasto com o mesmo nome
        if TipoGasto.objects.filter(tipoGasto=tipo_gasto).exists():
            raise BusinessError(f"Já existe um tipo de gasto com o nome '{tipo_gasto}'")
            
        tipo_gasto_obj = TipoGasto(
            tipoGasto=tipo_gasto,
            descricao=descricao
        )
        
        tipo_gasto_obj.save()
        logger.info("SERVICE tipo_gasto created.")
        return tipo_gasto_obj.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao adicionar tipo de gasto: {str(e)}")
        raise BusinessError("Erro ao adicionar tipo de gasto")

def update_tipo_gasto(tipo_gasto_id: int, tipo_gasto: str, descricao: str) -> dict:
    """Atualiza um tipo de gasto existente."""
    logger.info(f"SERVICE update tipo_gasto {tipo_gasto_id}")
    
    try:
        # Validação dos campos obrigatórios
        if not tipo_gasto:
            raise BusinessError("O campo 'tipoGasto' é obrigatório")
            
        if not descricao:
            raise BusinessError("O campo 'descricao' é obrigatório")
            
        # Verifica se o tipo de gasto existe
        try:
            tipo_gasto_obj = TipoGasto.objects.get(id=tipo_gasto_id)
        except TipoGasto.DoesNotExist:
            raise BusinessError(f"Tipo de Gasto com ID {tipo_gasto_id} não encontrado")
            
        # Verifica se já existe outro tipo de gasto com o mesmo nome (exceto o atual)
        if TipoGasto.objects.filter(tipoGasto=tipo_gasto).exclude(id=tipo_gasto_id).exists():
            raise BusinessError(f"Já existe um tipo de gasto com o nome '{tipo_gasto}'")
            
        tipo_gasto_obj.tipoGasto = tipo_gasto
        tipo_gasto_obj.descricao = descricao
        tipo_gasto_obj.save()
        
        logger.info("SERVICE tipo_gasto updated.")
        return tipo_gasto_obj.to_dict_json()
        
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar tipo de gasto: {str(e)}")
        raise BusinessError("Erro ao atualizar tipo de gasto")

def delete_tipo_gasto(tipo_gasto_id: int) -> None:
    """Deleta um tipo de gasto."""
    logger.info(f"SERVICE delete tipo_gasto {tipo_gasto_id}")
    
    try:
        tipo_gasto = TipoGasto.objects.get(id=tipo_gasto_id)
        tipo_gasto.delete()
        logger.info("SERVICE tipo_gasto deleted.")
    except TipoGasto.DoesNotExist:
        raise BusinessError(f"Tipo de Gasto com ID {tipo_gasto_id} não encontrado.")

def add_elemento_tipo_gasto(elemento_id: int, tipo_gasto_id: int) -> dict:
    """Adiciona um relacionamento entre elemento e tipo de gasto."""
    logger.info(f"SERVICE add elemento_tipo_gasto {elemento_id} - {tipo_gasto_id}")
    
    try:
        # Primeiro verifica se o elemento existe
        try:
            elemento = Elemento.objects.get(id=elemento_id)
        except Elemento.DoesNotExist:
            raise BusinessError(f"Elemento com ID {elemento_id} não encontrado.")
            
        # Depois verifica se o tipo de gasto existe
        try:
            tipo_gasto = TipoGasto.objects.get(id=tipo_gasto_id)
        except TipoGasto.DoesNotExist:
            raise BusinessError(f"Tipo de Gasto com ID {tipo_gasto_id} não encontrado.")
        
        # Por fim, verifica se o relacionamento já existe
        if ElementoTipoGasto.objects.filter(elemento=elemento, tipo_gasto=tipo_gasto).exists():
            raise BusinessError("Este relacionamento já existe.")
        
        elemento_tipo_gasto = ElementoTipoGasto(
            elemento=elemento,
            tipo_gasto=tipo_gasto
        )
        
        elemento_tipo_gasto.save()
        logger.info("SERVICE elemento_tipo_gasto created.")
        return elemento_tipo_gasto.to_dict_json()
    except BusinessError:
        raise
    except Exception as e:
        logger.error(f"Erro ao adicionar relacionamento elemento-tipo_gasto: {str(e)}")
        raise BusinessError("Erro ao adicionar relacionamento elemento-tipo_gasto")

def delete_elemento_tipo_gasto(id: int) -> None:
    """Deleta um relacionamento entre elemento e tipo de gasto."""
    logger.info(f"SERVICE delete elemento_tipo_gasto {id}")
    
    try:
        elemento_tipo_gasto = ElementoTipoGasto.objects.get(id=id)
        elemento_tipo_gasto.delete()
        logger.info("SERVICE elemento_tipo_gasto deleted.")
    except ElementoTipoGasto.DoesNotExist:
        raise BusinessError(f"Relacionamento com ID {id} não encontrado.")

def get_total_despesas_departamento(departamento_id: int) -> dict:
    """
    Calcula o total de despesas de um departamento específico.
    Retorna um dicionário com o total de despesas e outras informações relevantes.
    """
    logger.info(f"SERVICE get total despesas departamento: {departamento_id}")
    
    try:
        departamento = Departamento.objects.get(id=departamento_id)
        
        # Calcula o total de despesas
        resultado = Despesa.objects.filter(departamento=departamento).aggregate(
            total_despesas=Sum('valor')
        )
        
        total_despesas = resultado['total_despesas'] or Decimal('0.00')
        
        return {
            "departamento_id": departamento_id,
            "departamento_nome": departamento.nome,
            "total_despesas": float(total_despesas),
            "total_despesas_formatado": f"R$ {total_despesas:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        }
        
    except Departamento.DoesNotExist:
        raise ValueError("Departamento não encontrado")
    except Exception as e:
        logger.error(f"Erro ao calcular total de despesas: {str(e)}")
        raise BusinessError(f"Erro ao calcular total de despesas: {str(e)}")
    
def get_total_despesas_departamento_apartir_data(departamento_id: int, data_inicio: date) -> dict:
    """
    Retorna o total de despesas de um departamento a partir de uma data específica.
    
    Args:
        departamento_id: ID do departamento.
        data_inicio: Data inicial (inclusive) para filtragem.
    
    Returns:
        dict: Total das despesas em formato decimal.
    
    Raises:
        ValueError: Se o departamento não existir.
    """
    try:
        departamento = Departamento.objects.get(id=departamento_id)

        total = Despesa.objects.filter(
            departamento=departamento,
            created_at__date__gte=data_inicio
        ).aggregate(
            total=Sum("valor")
        )["total"] or Decimal("0.00")

        return {"total": round(total, 2)}

    except Departamento.DoesNotExist:
        raise ValueError("Departamento não encontrado.")

def delete_despesa(despesa_id: int) -> bool:
    """
    Remove uma despesa existente.
    
    Args:
        despesa_id: ID da despesa a ser removida
        
    Returns:
        bool: True se a despesa foi removida com sucesso
        
    Raises:
        BusinessError: Se a despesa não for encontrada
    """
    try:
        despesa = Despesa.objects.get(id=despesa_id)
        despesa.delete()
        return True
    except Despesa.DoesNotExist:
        raise BusinessError("Despesa não encontrada.")
    except Exception as e:
        logger.error(f"Erro ao remover despesa: {str(e)}")
        raise BusinessError("Erro ao remover despesa.")

def list_tipo_gastos() -> List[dict]:
    """Lista todos os tipos de gasto."""
    logger.info("SERVICE list tipo_gastos")
    try:
        return [tg.to_dict_json() for tg in TipoGasto.objects.all()]
    except Exception as e:
        logger.error(f"Erro ao listar tipos de gasto: {str(e)}")
        raise BusinessError("Erro ao listar tipos de gasto")

def list_tipo_gastos_por_elemento(elemento_id: int) -> List[dict]:
    """Lista todos os tipos de gasto associados a um elemento."""
    logger.info(f"SERVICE list tipo_gastos por elemento {elemento_id}")
    try:
        elemento = Elemento.objects.get(id=elemento_id)
        return [tg.to_dict_json() for tg in elemento.tipos_gasto.all()]
    except Elemento.DoesNotExist:
        raise BusinessError(f"Elemento com ID {elemento_id} não encontrado")
    except Exception as e:
        logger.error(f"Erro ao listar tipos de gasto do elemento: {str(e)}")
        raise BusinessError("Erro ao listar tipos de gasto do elemento")

def delete_departamento(departamento_id: int) -> None:
    """
    Remove um departamento existente.
    
    Args:
        departamento_id: ID do departamento a ser removido
        
    Raises:
        BusinessError: Se o departamento não for encontrado
    """
    logger.info(f"SERVICE delete departamento: {departamento_id}")
    
    try:
        departamento = Departamento.objects.get(id=departamento_id)
        departamento.delete()
        logger.info(f"Departamento {departamento_id} removido com sucesso.")
    except Departamento.DoesNotExist:
        raise BusinessError(f"Departamento com ID {departamento_id} não encontrado.")
    except Exception as e:
        logger.error(f"Erro ao remover departamento: {str(e)}")
        raise BusinessError("Erro ao remover departamento.")