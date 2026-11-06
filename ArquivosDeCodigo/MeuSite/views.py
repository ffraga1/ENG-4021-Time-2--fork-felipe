from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from datetime import date
from django.utils.dateparse import parse_date
from banco_de_dados.models import Usuario, Perfil, HistoricoFamiliar, Cuidado

def home(request):
    '''
    View function for home page of site.
    Renders the home.html template.
    '''
    return render(request, 'home.html')

def PerfilSaude(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('Login')

    usuario = get_object_or_404(Usuario, id=usuario_id)
    perfil = Perfil.objects.filter(usuario=usuario).first()
    mensagem = ''
    erro = ''

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        data_nascimento = parse_date(
            request.POST.get('data_nascimento', '')
        )
        sexo = request.POST.get('sexo', '').strip()

        if not nome or not data_nascimento or not sexo:
            erro = 'Preencha todos os campos do perfil.'
        else:
            if perfil:
                perfil.nome = nome
                perfil.data_nascimento = data_nascimento
                perfil.sexo = sexo
                perfil.save()
            else:
                perfil = Perfil.objects.create(
                    usuario=usuario,
                    nome=nome,
                    data_nascimento=data_nascimento,
                    sexo=sexo
                )

            mensagem = 'Perfil salvo com sucesso.'

    return render(request, 'PerfilSaude.html', {
        'usuario': usuario,
        'perfil': perfil,
        'mensagem': mensagem,
        'erro': erro
    })

def ComoUsar(request):


    return render(request, 'ComoUsar.html')


def EsqueciSenha (request):


    return render(request, 'EsqueciSenha.html')

def ConsentimentoDados(request):
    return render(request, 'ConsentimentoDados.html')

def CriarConta(request):

    if request.method == 'POST':

        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')

        
        if senha != confirmar_senha:
            return render(request, 'CriarConta.html', {
                'erro': 'As senhas não coincidem.',
                'nome': nome,
                'email': email
            })

        
        if len(senha) < 6:
            return render(request, 'CriarConta.html', {
                'erro': 'A senha deve ter pelo menos 6 caracteres.',
                'nome': nome,
                'email': email
            })

        
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'CriarConta.html', {
                'erro': 'Este e-mail já está cadastrado.',
                'nome': nome,
                'email': email
            })

        
        usuario = Usuario.objects.create(
            nome=nome,
            email=email,
            senha=make_password(senha)
        )
        request.session['usuario_id'] = usuario.id
        return redirect('InicioLogado')


    return render(request, 'CriarConta.html')

def Artigos (request):


    return render(request, 'Artigos.html')

def EdicaoUsuario(request, usuario_id):

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':

        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '')

        
        email_existente = Usuario.objects.filter(
            email=email
        ).exclude(id=usuario.id).exists()

        if email_existente:
            return render(request, 'EdicaoUsuario.html', {
                'usuario': usuario,
                'erro': 'Este e-mail já está sendo utilizado.'
            })

        if not nome or not email:
            return render(request, 'EdicaoUsuario.html', {
                'usuario': usuario,
                'erro': 'Nome e e-mail são obrigatórios.'
            })

        usuario.nome = nome
        usuario.email = email

        
        if senha:
            if len(senha) < 6:
                return render(request, 'EdicaoUsuario.html', {
                    'usuario': usuario,
                    'erro': 'A nova senha deve ter pelo menos 6 caracteres.'
                })

            usuario.senha = make_password(senha)

        usuario.save()

        return redirect('InicioLogado')

    return render(request, 'EdicaoUsuario.html', {
        'usuario': usuario
    })

def PreferenciasNotificacoes(request):
    return render(request, 'PreferenciasNotificacoes.html')

def RemocaoUsuario(request, usuario_id):

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':

        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '')
        confirmacao = request.POST.get('confirmacao')

        
        if email != usuario.email:
            return render(request, 'RemocaoUsuario.html', {
                'usuario': usuario,
                'erro': 'O e-mail informado não corresponde à conta.'
            })

        
        if not check_password(senha, usuario.senha):
            return render(request, 'RemocaoUsuario.html', {
                'usuario': usuario,
                'erro': 'Senha incorreta.'
            })

        
        if confirmacao != 'sim':
            return render(request, 'RemocaoUsuario.html', {
                'usuario': usuario,
                'erro': 'Você precisa confirmar a exclusão.'
            })

        
        usuario.delete()
        request.session.flush()
        return redirect('home')

    return render(request, 'RemocaoUsuario.html', {
        'usuario': usuario
    })

def Tela(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario.objects.filter(email=email).first()

        if usuario and check_password(senha, usuario.senha):
            request.session['usuario_id'] = usuario.id
            return redirect('InicioLogado')

        return render(request, 'Tela.html', {'erro': 'E-mail ou senha incorretos.'})

    return render(request, 'Tela.html')

def HistoricoFamiliar(request):

    return render(request, 'HistoricoFamiliar.html')

def CheckupInteligente(request):
    return render(request, 'CheckupInteligente.html')

def ListarUsuarios(request):

    usuarios = Usuario.objects.all()

    return render(request, 'ListarUsuarios.html', {'usuarios': usuarios})


def CalendarioCuidados(request):
    
    cuidados = Cuidado.objects.all()
    tipos_validos = ('Consulta', 'Exame', 'Vacina')

    tipo = request.GET.get('tipo', '')
    if tipo not in tipos_validos:
        tipo = ''
    if tipo:
        cuidados = cuidados.filter(tipo=tipo)

    inicio = request.GET.get('inicio', '')
    fim = request.GET.get('fim', '')
    mensagem_erro = ''

    try:
        inicio_data = parse_date(inicio) if inicio else None
    except ValueError:
        inicio_data = None

    try:
        fim_data = parse_date(fim) if fim else None
    except ValueError:
        fim_data = None

    if inicio and inicio_data is None:
        mensagem_erro = 'A data inicial informada é inválida.'
        inicio = ''
    if fim and fim_data is None:
        mensagem_erro = 'A data final informada é inválida.'
        fim = ''

    if inicio_data and fim_data and inicio_data > fim_data:
        mensagem_erro = 'A data inicial deve ser anterior ou igual à data final.'
        cuidados = Cuidado.objects.none()
    else:
        if inicio_data:
            cuidados = cuidados.filter(data__gte=inicio_data)
        if fim_data:
            cuidados = cuidados.filter(data__lte=fim_data)

    ordem = request.GET.get('ordem', 'asc')
    if ordem not in ('asc', 'desc'):
        ordem = 'asc'
    cuidados = cuidados.order_by('-data' if ordem == 'desc' else 'data', 'id')

    contexto = {
        'cuidados': cuidados,
        'hoje': date.today(),
        'tipos_cuidado': tipos_validos,
        'tipo_selecionado': tipo,
        'inicio': inicio,
        'fim': fim,
        'ordem': ordem,
        'mensagem_erro': mensagem_erro,
        'total_cuidados': cuidados.count(),
    }
    return render(request, 'CalendarioCuidados.html', contexto)

def RelatorioPreventivo(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('Login')

    usuario = get_object_or_404(Usuario, id=usuario_id)
    perfil = Perfil.objects.filter(usuario=usuario).first()

    if perfil:
        historicos = HistoricoFamiliar.objects.filter(
            perfil=perfil
        ).order_by('parente', 'doenca')
        cuidados = Cuidado.objects.filter(
            perfil=perfil
        ).order_by('data')
    else:
        historicos = HistoricoFamiliar.objects.none()
        cuidados = Cuidado.objects.none()

    return render(request, 'RelatorioPreventivo.html', {
        'usuario': usuario,
        'perfil': perfil,
        'historicos': historicos,
        'cuidados': cuidados
    })

def Familiares(request):

    return render(request, 'Familiares.html')


def CadastroCuidados(request):
    return render(request, 'CadastroCuidados.html')

def InicioLogado(request):
    usuario_id = request.session.get('usuario_id')
    usuario = get_object_or_404(Usuario, id=usuario_id)

    return render(request, 'InicioLogado.html', {
        'usuario': usuario
    })