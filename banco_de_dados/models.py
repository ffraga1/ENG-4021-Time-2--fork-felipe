from django.conf import settings
from django.db import models


class HistoricoFamiliar(models.Model):
    # Usuário que está cadastrando as informações da família
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Informações básicas do familiar
    nome_parente = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=50)
    lado_familia = models.CharField(max_length=20, blank=True)

    # Informações sobre a saúde do familiar
    condicao_saude = models.CharField(max_length=150)
    idade_diagnostico = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Informações opcionais sobre falecimento
    esta_vivo = models.BooleanField(default=True)
    idade_obito = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    observacoes = models.TextField(blank=True)

    # Datas preenchidas automaticamente pelo sistema
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "historico_familiar"

    def __str__(self):
        return f"{self.nome_parente} - {self.condicao_saude}"
