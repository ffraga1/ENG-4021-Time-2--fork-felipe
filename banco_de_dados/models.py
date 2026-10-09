from django.conf import settings
from django.db import models


class HistoricoFamiliar(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="historicos_familiares",
    )

    nome_parente = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=50)
    lado_familia = models.CharField(max_length=20, blank=True)

    condicao_saude = models.CharField(max_length=150)
    idade_diagnostico = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    esta_vivo = models.BooleanField(default=True)
    idade_obito = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "historico_familiar"
        ordering = ["nome_parente"]
        verbose_name = "histórico familiar"
        verbose_name_plural = "históricos familiares"

    def __str__(self):
        return f"{self.nome_parente} - {self.condicao_saude}"
