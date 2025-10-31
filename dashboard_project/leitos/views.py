import io
import pandas as pd
import math
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .utils_notebook_loader import load_df

# Carregar DataFrame inicial
try:
    DF = load_df()
    LOAD_ERROR = None
except Exception as e:
    DF = None
    LOAD_ERROR = str(e)


def dashboard_view(request):
    if LOAD_ERROR:
        return HttpResponse(f"Erro ao carregar dados: {LOAD_ERROR}", status=500)
    return render(request, "leitos/dashboard.html", {})


def _col(name):
    return DF.attrs["cols_map"].get(name)


# Função auxiliar para aplicar filtros de região e CEP
def _apply_filters(df, request):
    zone_col = _col("zone")
    cep_col = _col("cep")

    q_zone = request.GET.get("zone", "").strip()
    q_cep = request.GET.get("cep", "").replace("-", "").strip()

    if q_zone and zone_col:
        df = df[df[zone_col].astype(str).str.upper() == q_zone.upper()]

    if q_cep and cep_col:
        df = df[df[cep_col].astype(str).str.replace("-", "").str.startswith(q_cep)]

    return df


# API: Zona Leitos
def api_zona_leitos(request):
    if DF is None:
        return JsonResponse({"error": "Dados não carregados"}, status=500)

    zone_col = _col("zone")
    leitos_exist_col = _col("leitos_exist")
    leitos_sus_col = _col("leitos_sus")

    if not zone_col:
        return JsonResponse({"error": "Coluna região não encontrada"}, status=400)

    df = _apply_filters(DF.copy(), request)

    # Converter leitos para numérico
    for col in [leitos_exist_col, leitos_sus_col]:
        if col:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(r"[^\d\-\.]", "", regex=True),
                errors="coerce"
            ).fillna(0)

    agg = {}
    for _, row in df.iterrows():
        zone = row[zone_col] if zone_col else "N/A"
        if not zone or str(zone).strip() == "":
            zone = "Sem Região"
        if zone not in agg:
            agg[zone] = {"leitos_exist": 0.0, "leitos_sus": 0.0}
        if leitos_exist_col:
            agg[zone]["leitos_exist"] += float(row[leitos_exist_col])
        if leitos_sus_col:
            agg[zone]["leitos_sus"] += float(row[leitos_sus_col])

    out = [{"zone": z, **v} for z, v in agg.items()]
    out = sorted(out, key=lambda x: x["zone"])
    return JsonResponse(out, safe=False)


# API: Zona Especialidades (UTIs específicas)
def api_zona_especialidades(request):
    if DF is None:
        return JsonResponse({"error": "Dados não carregados"}, status=500)

    zone_col = _col("zone")
    leitos_uti_adulto_sus_col = _col("leitos_uti_adulto_sus")
    leitos_uti_coronariana_sus_col = _col("leitos_uti_coronariana_sus")
    leitos_uti_neonatal_sus_col = _col("leitos_uti_neonatal_sus")
    leitos_uti_pediatrico_sus_col = _col("leitos_uti_pediatrico_sus")
    leitos_uti_queimado_sus_col = _col("leitos_uti_queimado_sus")

    if not zone_col:
        return JsonResponse({"error": "Coluna região não encontrada"}, status=400)

    df = _apply_filters(DF.copy(), request)

    # Converter leitos para numérico
    for col in [leitos_uti_adulto_sus_col, leitos_uti_coronariana_sus_col,
                leitos_uti_neonatal_sus_col, leitos_uti_pediatrico_sus_col,
                leitos_uti_queimado_sus_col]:
        if col:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(r"[^\d\-\.]", "", regex=True),
                errors="coerce"
            ).fillna(0)

    agg = {}
    for _, row in df.iterrows():
        zone = row[zone_col] if zone_col else "N/A"
        if not zone or str(zone).strip() == "":
            zone = "Sem Região"
        if zone not in agg:
            agg[zone] = {
                "leitos_uti_adulto_sus": 0.0,
                "leitos_uti_coronariana_sus": 0.0,
                "leitos_uti_neonatal_sus": 0.0,
                "leitos_uti_pediatrico_sus": 0.0,
                "leitos_uti_queimado_sus": 0.0
            }
        if leitos_uti_adulto_sus_col:
            agg[zone]["leitos_uti_adulto_sus"] += float(row[leitos_uti_adulto_sus_col])
        if leitos_uti_coronariana_sus_col:
            agg[zone]["leitos_uti_coronariana_sus"] += float(row[leitos_uti_coronariana_sus_col])
        if leitos_uti_neonatal_sus_col:
            agg[zone]["leitos_uti_neonatal_sus"] += float(row[leitos_uti_neonatal_sus_col])
        if leitos_uti_pediatrico_sus_col:
            agg[zone]["leitos_uti_pediatrico_sus"] += float(row[leitos_uti_pediatrico_sus_col])
        if leitos_uti_queimado_sus_col:
            agg[zone]["leitos_uti_queimado_sus"] += float(row[leitos_uti_queimado_sus_col])

    out = [{"zone": z, **v} for z, v in agg.items()]
    out = sorted(out, key=lambda x: x["zone"])
    return JsonResponse(out, safe=False)


# API: Evolução Temporal (Mês) Leitos
def api_evolucao_leitos(request):
    if DF is None:
        return JsonResponse({"error": "Dados não carregados"}, status=500)

    comp_col = _col("comp") or "COMP"
    zone_col = _col("zone")
    leitos_exist_col = _col("leitos_exist")
    leitos_sus_col = _col("leitos_sus")

    if not zone_col:
        return JsonResponse({"error": "Coluna região não encontrada"}, status=400)

    df = _apply_filters(DF.copy(), request)

    # Normaliza COMP para formato AAAA-MM
    df[comp_col] = df[comp_col].astype(str).str.extract(r"(\d{4})[-/]?(\d{2})")\
        .apply(lambda x: f"{x[0]}-{x[1]}" if pd.notnull(x[0]) and pd.notnull(x[1]) else None, axis=1)
    df = df.dropna(subset=[comp_col])

    # Converter leitos para numérico
    for col in [leitos_exist_col, leitos_sus_col]:
        if col:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(r"[^\d\-\.]", "", regex=True),
                errors="coerce"
            ).fillna(0)

    # Agrupa por região e mês
    grouped = df.groupby([zone_col, comp_col], as_index=False).agg({
        leitos_exist_col: "sum",
        leitos_sus_col: "sum"
    })

    grouped = grouped.rename(columns={
        zone_col: "zone",
        comp_col: "comp",
        leitos_exist_col: "leitos_exist",
        leitos_sus_col: "leitos_sus"
    })

    return JsonResponse(grouped.to_dict(orient="records"), safe=False)


# API: Taxa Média de Ocupação SUS (%) por Região
def api_taxa_ocupacao_sus(request):

    if DF is None:
        return JsonResponse({"error": "Dados não carregados"}, status=500)

    zone_col = _col("zone")
    leitos_exist_col = _col("leitos_exist")
    leitos_sus_col = _col("leitos_sus")

    if not zone_col or not leitos_exist_col or not leitos_sus_col:
        return JsonResponse({"error": "Colunas obrigatórias ausentes"}, status=400)

    df = _apply_filters(DF.copy(), request)

    # Converter colunas numéricas
    for col in [leitos_exist_col, leitos_sus_col]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r"[^\d\-\.]", "", regex=True),
            errors="coerce"
        ).fillna(0)

    # Agrupar por zona
    grouped = (
        df.groupby(zone_col, as_index=False)
        .agg({leitos_exist_col: "sum", leitos_sus_col: "sum"})
    )

    # Calcular taxa
    # Fórmula: (Leitos SUS / Leitos Existentes) * 100
    grouped["taxa_ocupacao_sus"] = grouped.apply(
        lambda x: round((x[leitos_sus_col] / x[leitos_exist_col]) * 100, 2)
        if x[leitos_exist_col] > 0 else 0,
        axis=1
    )

    grouped = grouped.rename(columns={zone_col: "zone"})
    grouped = grouped.sort_values("zone")

    return JsonResponse(grouped.to_dict(orient="records"), safe=False)


# API: Estabelecimentos (Tabela com Paginação e Export)
def api_estabelecimentos_table(request):
    if DF is None:
        return JsonResponse({"error": "Dados não carregados"}, status=500)

    page = int(request.GET.get("page", "1"))
    page_size = int(request.GET.get("page_size", "25"))
    page = max(page, 1)
    page_size = max(page_size, 1)

    zone_col = _col("zone")
    municipio_col = _col("municipio")
    cep_col = _col("cep")
    nome_col = _col("nome")
    leitos_exist_col = _col("leitos_exist")
    leitos_sus_col = _col("leitos_sus")

    if not all([zone_col, municipio_col, cep_col, nome_col]):
        return JsonResponse({"error": "Colunas obrigatórias ausentes no CSV."}, status=400)

    df = _apply_filters(DF.copy(), request)

    for col in [leitos_exist_col, leitos_sus_col]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r"[^\d]", "", regex=True).replace("", "0").astype(float)

    group_cols = [municipio_col, zone_col, cep_col, nome_col]
    agg_dict = {leitos_exist_col: "sum", leitos_sus_col: "sum"}

    df_grouped = df.groupby(group_cols, dropna=False, as_index=False).agg(agg_dict)
    df_grouped = df_grouped.rename(columns={
        municipio_col: "Município",
        zone_col: "Zona",
        cep_col: "CEP",
        nome_col: "Hospital",
        leitos_exist_col: "Leitos Existentes",
        leitos_sus_col: "Leitos SUS",
    })

    total = len(df_grouped)
    total_pages = math.ceil(total / page_size)
    start, end = (page - 1) * page_size, (page * page_size)
    page_df = df_grouped.iloc[start:end]

    return JsonResponse({
        "results": page_df.to_dict(orient="records"),
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    })


def api_estabelecimentos_export_csv(request):
    if DF is None:
        return HttpResponse("Dados não carregados", status=500)

    zone_col = _col("zone")
    municipio_col = _col("municipio")
    cep_col = _col("cep")
    nome_col = _col("nome")
    leitos_exist_col = _col("leitos_exist")
    leitos_sus_col = _col("leitos_sus")

    df = _apply_filters(DF.copy(), request)

    for col in [leitos_exist_col, leitos_sus_col]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r"[^\d]", "", regex=True).replace("", "0").astype(float)

    group_cols = [municipio_col, zone_col, cep_col, nome_col]
    agg_dict = {leitos_exist_col: "sum", leitos_sus_col: "sum"}

    df_grouped = df.groupby(group_cols, dropna=False, as_index=False).agg(agg_dict)
    df_grouped = df_grouped.rename(columns={
        municipio_col: "Município",
        zone_col: "Região",
        cep_col: "CEP",
        nome_col: "Hospital",
        leitos_exist_col: "Leitos Totais",
        leitos_sus_col: "Leitos SUS",
    })

    buf = io.StringIO()
    df_grouped.to_csv(buf, index=False, sep=";", encoding="utf-8-sig")
    response = HttpResponse(buf.getvalue(), content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="Relacao_Hospitais_Regiao.csv"'
    return response


# APIs adicionais (por Município, Região e CEP)
def api_por_municipio(request, municipio):
    if DF is None:
        return JsonResponse({"error": "Dados não carregados"}, status=500)
    df = _apply_filters(DF.copy(), request)
    return JsonResponse(df.to_dict(orient="records"), safe=False)


def api_por_zona(request, zona):
    if DF is None:
        return JsonResponse({"error": "Dados não carregados"}, status=500)
    df = _apply_filters(DF.copy(), request)
    return JsonResponse(df.to_dict(orient="records"), safe=False)


def api_por_cep(request, cep):
    if DF is None:
        return JsonResponse({"error": "Dados não carregados"}, status=500)
    df = _apply_filters(DF.copy(), request)
    return JsonResponse(df.to_dict(orient="records"), safe=False)


def api_filters(request):
    if DF is None:
        return JsonResponse({"zones": [], "ceps": []}, safe=False)
    zone_col = _col("zone")
    cep_col = _col("cep")
    data = {
        "zones": sorted(DF[zone_col].dropna().astype(str).unique().tolist()) if zone_col else [],
        "ceps": sorted(DF[cep_col].astype(str).str.replace("-", "").dropna().unique().tolist()) if cep_col else [],
    }
    return JsonResponse(data)
