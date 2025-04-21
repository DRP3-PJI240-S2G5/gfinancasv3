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
        BusinessError: Se o responsável não for encontrado
    """
    logger.info("SERVICE add new departamento")
    
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
    return [item.to_dict_json() for item in Departamento.objects.all()]

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
def add_verba(valor, departamento_id: int, user_id: int, ano: int, descricao: str) -> dict:
    """
    Adiciona uma nova verba para um departamento.
    
    Args:
        valor: Valor da verba
        departamento_id: ID do departamento
        user_id: ID do usuário
        ano: Ano da verba
        descricao: Descrição da verba
        
    Returns:
        dict: Dados da verba criada
        
    Raises:
        BusinessError: Se já existir uma verba para o departamento no ano ou se o departamento/usuário não for encontrado
    """
    logger.info(f"SERVICE add verba: {valor} para {departamento_id} no ano {ano}")
    
    try:
        departamento = Departamento.objects.get(id=departamento_id)
        user = User.objects.get(id=user_id)
    except Departamento.DoesNotExist:
        raise BusinessError("Departamento não encontrado.")
    except User.DoesNotExist:
        raise BusinessError("Usuário não encontrado.")
    
    if Verba.objects.filter(departamento=departamento, ano=ano).exists():
        raise BusinessError("Já existe uma verba estipulada para este departamento neste ano.")
    
    if valor is not None:
        valor = Decimal(valor)

    verba = Verba(
        valor=valor, 
        departamento=departamento, 
        user=user, 
        ano=ano, 
        descricao=descricao
    )
    
    verba.save()
    return verba.to_dict_json()

def update_verba(verba_id: int, valor: Decimal = None, descricao: str = None) -> dict:
    """
    Atualiza os valores ou descrição de uma verba.
    
    Args:
        verba_id: ID da verba a ser atualizada
        valor: Novo valor da verba (opcional)
        descricao: Nova descrição da verba (opcional)
        
    Returns:
        dict: Dados da verba atualizada
        
    Raises:
        BusinessError: Se a verba não for encontrada
    """
    logger.info(f"SERVICE update verba: {verba_id}")
    
    try:
        verba = Verba.objects.get(id=verba_id)
    except Verba.DoesNotExist:
        raise BusinessError("Verba não encontrada para atualização.")
    
    if valor is not None:
        verba.valor = Decimal(valor)
    if descricao:
        verba.descricao = descricao
    
    verba.save()
    return verba.to_dict_json()

def list_verbas() -> List[dict]:
    logger.info("SERVICE list verbas")
    return [verba.to_dict_json() for verba in Verba.objects.all()]

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
    
# SERVIÇOS PARA ELEMENTOS (implementados conforme práticas)
def add_elemento(novo_elemento: str, descricao: str) -> dict:
    logger.info(f"SERVICE add elemento: {novo_elemento}")
    elemento = Elemento(elemento=novo_elemento, descricao=descricao)
    elemento.save()
    return elemento.to_dict_json()

def update_elemento(elemento: Elemento, descricao: str = None) -> dict:
    """Atualiza a descrição de um elemento existente."""
    logger.info(f"SERVICE update elemento: {elemento.id}")
    
    if not elemento.pk:
        raise BusinessError("Elemento não encontrado para atualização.")
    
    if descricao:
        elemento.descricao = descricao
    
    elemento.save()
    return elemento.to_dict_json()

def list_elementos() -> List[dict]:
    logger.info("SERVICE list elementos")
    return [el.to_dict_json() for el in Elemento.objects.all()]

# SERVIÇOS PARA TIPOS DE GASTO (implementados conforme práticas)
def add_tipo_gasto(novo_tipo_gasto: str, descricao: str) -> dict:
    logger.info(f"SERVICE add tipo_gasto: {novo_tipo_gasto}")
    tipo_gasto = TipoGasto(tipoGasto=novo_tipo_gasto, descricao=descricao)
    tipo_gasto.save()
    return tipo_gasto.to_dict_json()

def update_tipo_gasto(tipo_gasto: TipoGasto, descricao: str = None) -> dict:
    """Atualiza a descrição de um tipo de gasto existente."""
    logger.info(f"SERVICE update tipo_gasto: {tipo_gasto.id}")
    
    if not tipo_gasto.pk:
        raise BusinessError("Tipo de gasto não encontrado para atualização.")
    
    if descricao:
        tipo_gasto.descricao = descricao
    
    tipo_gasto.save()
    return tipo_gasto.to_dict_json()

def list_tipo_gastos() -> List[dict]:
    logger.info("SERVICE list tipos_gasto")
    return [tg.to_dict_json() for tg in TipoGasto.objects.all()]

def list_tipo_gastos_por_elemento(elemento_id: int) -> List[dict]:
    logger.info(f"SERVICE list tipos_gasto por elemento {elemento_id}")
    
    relacoes = ElementoTipoGasto.objects.filter(elemento_id=elemento_id).select_related("tipo_gasto")
    return [
        {
            "id": r.tipo_gasto.id,
            "tipoGasto": r.tipo_gasto.tipoGasto,
            "descricao": r.tipo_gasto.descricao,
        }
        for r in relacoes
    ]

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