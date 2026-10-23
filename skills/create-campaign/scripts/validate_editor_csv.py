#!/usr/bin/env python3
"""Valida um CSV de importação do Google Ads Editor antes de publicar.

Uso: python3 validate_editor_csv.py arquivo.csv [--json]
Saída 0 = sem erros (pode haver avisos); 1 = há erros; 2 = arquivo ilegível.
Só usa a biblioteca padrão.
"""
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict

HEADLINE_MAX, DESCRIPTION_MAX, PATH_MAX = 30, 90, 15
KEYWORD_MAX_CHARS, KEYWORD_MAX_WORDS = 80, 10
POSITIVE_TYPES = {"exact", "phrase", "broad"}
NEGATIVE_TYPES = {"negative exact", "negative phrase", "negative broad"}
CAMPAIGN_NEGATIVE_TYPES = {"campaign negative exact", "campaign negative phrase", "campaign negative broad"}
KEYWORD_ALLOWED = re.compile(r"^[\w\s\-&.'+]+$", re.UNICODE)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿←-⇿⬀-⯿]")


def display_len(text):
    # {KeyWord:padrão} conta pelo texto padrão
    text = re.sub(r"\{(?:keyword|KeyWord|Keyword|KEYWORD):([^}]*)\}", r"\1", text)
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def norm(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, row, msg):
        self.errors.append({"row": row, "msg": msg})

    def warn(self, row, msg):
        self.warnings.append({"row": row, "msg": msg})


def check_text(rep, row, label, text, limit):
    n = display_len(text)
    if n > limit:
        rep.error(row, f"{label} com {n} caracteres (máx. {limit}): {text!r}")
    if EMOJI.search(text):
        rep.error(row, f"{label} contém emoji/símbolo decorativo: {text!r}")
    if re.search(r"([!?.])\1", text):
        rep.error(row, f"{label} com pontuação repetida: {text!r}")
    if any(w.isupper() for w in re.findall(r"\w{4,}", text)):
        rep.warn(row, f"{label} tem palavra em CAIXA ALTA (pode ser reprovado se não for sigla): {text!r}")


def check_rsa(rep, row, r):
    headlines = [r.get(f"Headline {i}", "").strip() for i in range(1, 16)]
    headlines = [h for h in headlines if h]
    descriptions = [r.get(f"Description {i}", "").strip() for i in range(1, 5)]
    descriptions = [d for d in descriptions if d]

    if len(headlines) < 3:
        rep.error(row, f"RSA com {len(headlines)} títulos (mín. 3)")
    elif len(headlines) < 10:
        rep.warn(row, f"RSA com só {len(headlines)} títulos; 12-15 melhora a força do anúncio")
    if len(descriptions) < 2:
        rep.error(row, f"RSA com {len(descriptions)} descrições (mín. 2)")
    elif len(descriptions) < 4:
        rep.warn(row, f"RSA com {len(descriptions)} descrições; use 4")

    for h in headlines:
        check_text(rep, row, "Título", h, HEADLINE_MAX)
        if "!" in h:
            rep.error(row, f"Título com '!' (não permitido): {h!r}")
    for d in descriptions:
        check_text(rep, row, "Descrição", d, DESCRIPTION_MAX)

    seen = {}
    for h in headlines:
        k = norm(h)
        if k in seen:
            rep.error(row, f"Títulos duplicados: {seen[k]!r} e {h!r}")
        seen[k] = h
    if len({norm(d) for d in descriptions}) < len(descriptions):
        rep.error(row, "Descrições duplicadas")

    for p in ("Path 1", "Path 2"):
        v = r.get(p, "").strip()
        if v and display_len(v) > PATH_MAX:
            rep.error(row, f"{p} com {display_len(v)} caracteres (máx. {PATH_MAX}): {v!r}")
        if v and " " in v:
            rep.error(row, f"{p} não pode ter espaço: {v!r}")
    if r.get("Path 2", "").strip() and not r.get("Path 1", "").strip():
        rep.error(row, "Path 2 preenchido sem Path 1")

    url = r.get("Final URL", "").strip()
    if not url:
        rep.error(row, "RSA sem Final URL")
    elif not url.startswith("https://"):
        rep.warn(row, f"Final URL sem https: {url}")
    return headlines


def validate(path):
    rep = Report()
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        print(f"Não consegui ler {path}: {e}", file=sys.stderr)
        sys.exit(2)

    if not rows:
        rep.error(1, "Arquivo sem linhas de dados")
        return rep, {}

    campaigns, ad_groups = {}, set()
    positives = defaultdict(list)          # campanha -> [(grupo, kw, tipo, linha)]
    group_neg = defaultdict(list)          # (campanha, grupo) -> [(kw, tipo, linha)]
    camp_neg = defaultdict(list)           # campanha -> [(kw, tipo, linha)]
    rsa_count = defaultdict(int)
    kw_count = defaultdict(int)
    seen_kw = set()

    for i, r in enumerate(rows, start=2):  # linha 1 = cabeçalho
        r = {k.strip(): (v or "") for k, v in r.items() if k}
        camp = r.get("Campaign", "").strip()
        group = r.get("Ad Group", "").strip()
        kw = r.get("Keyword", "").strip()
        ctype = r.get("Criterion Type", "").strip().lower()
        ad_type = r.get("Ad type", "").strip().lower()

        if not camp:
            rep.error(i, "Linha sem Campaign")
            continue

        if r.get("Campaign Type", "").strip() or r.get("Budget", "").strip():
            campaigns[camp] = i
            status = r.get("Campaign Status", "").strip().lower()
            if status != "paused":
                rep.error(i, f"Campanha {camp!r} deve subir com Campaign Status = Paused (está {status or 'vazio'!r})")
            budget = r.get("Budget", "").strip()
            try:
                if float(budget) <= 0:
                    raise ValueError
            except ValueError:
                rep.error(i, f"Budget inválido para {camp!r}: {budget!r} (use ponto decimal, ex.: 50.00)")
            if not r.get("Location", "").strip():
                rep.warn(i, f"Campanha {camp!r} sem Location: vai segmentar todos os países")
            if not r.get("Languages", "").strip():
                rep.warn(i, f"Campanha {camp!r} sem Languages")
            if not r.get("Bid Strategy Type", "").strip():
                rep.warn(i, f"Campanha {camp!r} sem Bid Strategy Type")

        if kw:
            if ctype in CAMPAIGN_NEGATIVE_TYPES:
                camp_neg[camp].append((kw, ctype, i))
            elif ctype in NEGATIVE_TYPES:
                if not group:
                    rep.error(i, f"Negativa de grupo sem Ad Group (use 'Campaign Negative ...' para campanha): {kw!r}")
                group_neg[(camp, group)].append((kw, ctype, i))
            elif ctype in POSITIVE_TYPES:
                if not group:
                    rep.error(i, f"Palavra-chave sem Ad Group: {kw!r}")
                positives[camp].append((group, kw, ctype, i))
                kw_count[(camp, group)] += 1
                key = (camp, group, kw.lower(), ctype)
                if key in seen_kw:
                    rep.warn(i, f"Palavra-chave repetida no grupo: {kw!r} ({ctype})")
                seen_kw.add(key)
            else:
                rep.error(i, f"Criterion Type inválido para {kw!r}: {r.get('Criterion Type')!r}")

            if re.search(r'^[\["+]|[\]"]$', kw):
                rep.error(i, f"Remova colchetes/aspas da Keyword (a correspondência vai em Criterion Type): {kw!r}")
            if len(kw) > KEYWORD_MAX_CHARS:
                rep.error(i, f"Palavra-chave com {len(kw)} caracteres (máx. {KEYWORD_MAX_CHARS}): {kw!r}")
            if len(kw.split()) > KEYWORD_MAX_WORDS:
                rep.error(i, f"Palavra-chave com mais de {KEYWORD_MAX_WORDS} palavras: {kw!r}")
            if not KEYWORD_ALLOWED.match(kw.strip('[]"')):
                rep.error(i, f"Palavra-chave com caractere não permitido: {kw!r}")
        elif ad_type:
            if ad_type != "responsive search ad":
                rep.warn(i, f"Ad type {r.get('Ad type')!r} não é verificado por este validador")
            else:
                if not group:
                    rep.error(i, "RSA sem Ad Group")
                check_rsa(rep, i, r)
                rsa_count[(camp, group)] += 1
        elif group:
            ad_groups.add((camp, group))

    # Referências e cobertura
    for camp, grp in set(kw_count) | set(rsa_count) | ad_groups:
        if camp not in campaigns:
            rep.warn(0, f"Campanha {camp!r} não tem linha de campanha neste arquivo (ok se já existe na conta)")
        if grp and kw_count[(camp, grp)] == 0:
            rep.warn(0, f"Grupo {camp} › {grp} sem palavras-chave")
        if grp and rsa_count[(camp, grp)] == 0:
            rep.error(0, f"Grupo {camp} › {grp} sem anúncio RSA")
        if grp and kw_count[(camp, grp)] > 30:
            rep.warn(0, f"Grupo {camp} › {grp} com {kw_count[(camp, grp)]} palavras-chave; considere dividir")

    # Conflitos negativa × positiva
    def blocks(neg, ntype, pos):
        n, p = neg.lower().split(), pos.lower().split()
        if "exact" in ntype:
            return n == p
        if "phrase" in ntype:
            return any(p[j:j + len(n)] == n for j in range(len(p) - len(n) + 1))
        return set(n) <= set(p)

    for camp, items in positives.items():
        for grp, kw in sorted({(g, k) for g, k, _, _ in items}):
            for neg, ntype, nrow in camp_neg.get(camp, []):
                if blocks(neg, ntype, kw):
                    rep.error(nrow, f"Negativa de campanha {neg!r} ({ntype}) bloqueia a palavra-chave {kw!r} em {grp!r}")
            for neg, ntype, nrow in group_neg.get((camp, grp), []):
                if blocks(neg, ntype, kw):
                    rep.error(nrow, f"Negativa de grupo {neg!r} ({ntype}) bloqueia a palavra-chave {kw!r}")

    summary = {
        "campanhas": len(campaigns),
        "grupos": len(set(kw_count) | set(rsa_count) | ad_groups),
        "palavras_chave": sum(kw_count.values()),
        "negativas": sum(len(v) for v in camp_neg.values()) + sum(len(v) for v in group_neg.values()),
        "anuncios_rsa": sum(rsa_count.values()),
    }
    return rep, summary


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    rep, summary = validate(args[0])
    if "--json" in sys.argv:
        print(json.dumps({"summary": summary, "errors": rep.errors, "warnings": rep.warnings}, ensure_ascii=False, indent=2))
    else:
        print("Resumo: " + ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in summary.items()))
        for label, items in (("ERRO", rep.errors), ("AVISO", rep.warnings)):
            for it in items:
                where = f"linha {it['row']}" if it["row"] else "geral"
                print(f"[{label}] {where}: {it['msg']}")
        print(f"\n{len(rep.errors)} erro(s), {len(rep.warnings)} aviso(s).")
    sys.exit(1 if rep.errors else 0)


if __name__ == "__main__":
    main()
