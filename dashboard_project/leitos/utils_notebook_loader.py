from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

CSV_CANDIDATES = [
    DATA_DIR / "Consolidado_SP.csv",
    DATA_DIR / "consolidado_sp.csv",
    DATA_DIR / "consolidado.csv",
]


def find_csv():
    for p in CSV_CANDIDATES:
        if p.exists():
            return str(p)
    raise FileNotFoundError(f"Arquivo CSV não encontrado em {DATA_DIR}. Coloque 'Consolidado_SP.csv' em {DATA_DIR}")


def try_cols(df, possibilities):
    for p in possibilities:
        if p in df.columns:
            return p
    return None


def load_df():
    csv_path = find_csv()
    # tenta ler com ; (mais comum) e se falhar tenta ,
    try:
        df = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig", dtype=str, low_memory=False)
    except Exception:
        df = pd.read_csv(csv_path, sep=",", encoding="utf-8-sig", dtype=str, low_memory=False)

    # clean column names
    df.columns = [c.strip() for c in df.columns]

    region_col = try_cols(df, ["ZONA", "REGIAO", "REGIÃO", "ZONA_REGIONAL", "Zona"])
    cep_col = try_cols(df, ["CO_CEP", "CEP", "Co_CEP", "CEP_OLD"])
    municipio_col = try_cols(df, ["MUNICIPIO", "MUNICÍPIO", "Municipio"])
    nome_col = try_cols(df, ["NOME_ESTABELECIMENTO", "NOME DO ESTABELECIMENTO", "NOME", "RAZAO_SOCIAL"])
    especialidade_col = try_cols(df, ["ESPECIALIDADE", "ESPECIALIDADES", "TIPO", "SERVICO", "UTI"])

    leitos_exist_col = try_cols(df, [
        "LEITOS_EXISTENTES", "QT_LEITOS_EXISTENTES", "LEITOS EXISTENTES",
        "LEITOS_TOTAL", "TOTAL_LEITOS", "QT_LEITOS_TOTAL", "LEITOS"
    ])
    leitos_sus_col = try_cols(df, [
        "LEITOS_SUS", "QT_LEITOS_SUS", "LEITOS SUS", "LEITOS_HOSP_SUS", "QT_LEITOS_HOSP_SUS"
    ])
    leitos_uti_adulto_sus_col = try_cols(df, [
        "UTI_ADULTO_SUS"
    ])

    leitos_uti_coronariana_sus_col = try_cols(df, [
        "UTI_CORONARIANA_SUS"
    ])

    leitos_uti_neonatal_sus_col = try_cols(df, [
        "UTI_NEONATAL_SUS"
    ])

    leitos_uti_pediatrico_sus_col = try_cols(df, [
        "UTI_PEDIATRICO_SUS"
    ])

    leitos_uti_queimado_sus_col = try_cols(df, [
        "UTI_QUEIMADO_SUS"
    ])

    df = df.fillna("")

    df.attrs["cols_map"] = {
        "zone": region_col,
        "cep": cep_col,
        "municipio": municipio_col,
        "nome": nome_col,
        "especialidade": especialidade_col,
        "leitos_exist": leitos_exist_col,
        "leitos_sus": leitos_sus_col,
        "leitos_uti_adulto_sus": leitos_uti_adulto_sus_col,
        "leitos_uti_coronariana_sus": leitos_uti_coronariana_sus_col,
        "leitos_uti_neonatal_sus": leitos_uti_neonatal_sus_col,
        "leitos_uti_pediatrico_sus": leitos_uti_pediatrico_sus_col,
        "leitos_uti_queimado_sus": leitos_uti_queimado_sus_col
    }
    return df
