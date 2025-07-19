from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from inep_models import Curso_censo, Censo_es, db  # Importe suas tabelas e a instância do SQLAlchemy

# Configure o banco de dados
engine = create_engine('sqlite:///INEP.db')
Session = sessionmaker(bind=engine)
session = Session()

def transfer_data(batch_size=1000):
    try:
        # Contador para controlar quantos registros já foram inseridos
        count = 0

        # Ler os dados da tabela Curso_censo em lotes
        cursos_censo = session.query(Curso_censo).yield_per(batch_size)

        # Iterar sobre os dados e inserir na tabela Censo_es
        for curso in cursos_censo:
            censo = Censo_es(
                ano_censo=curso.ano_censo,
                regiao=curso.regiao,
                estado=curso.estado,
                municipio=curso.municipio,
                dimensao=curso.dimensao,
                org_academica=curso.org_academica,
                categoria=curso.categoria,
                tp_rede=curso.tp_rede,
                ies=curso.ies,
                curso=curso.curso,
                cine_rotulo=curso.cine_rotulo,
                area_geral=curso.area_geral,
                area_especifica=curso.area_especifica,
                area_detalhada=curso.area_detalhada,
                tp_grau_academico=curso.tp_grau_academico,
                in_gratuito=curso.in_gratuito,
                tp_modalidade_ensino=curso.tp_modalidade_ensino,
                tp_nivel_academico=curso.tp_nivel_academico,
                qt_curso=curso.qt_curso,
                qt_vg_total=curso.qt_vg_total,
                qt_vg_total_diurno=curso.qt_vg_total_diurno,
                qt_vg_total_noturno=curso.qt_vg_total_noturno,
                qt_vg_total_ead=curso.qt_vg_total_ead,
                qt_ing=curso.qt_ing,
                qt_ing_fem=curso.qt_ing_fem,
                qt_ing_masc=curso.qt_ing_masc,
                qt_ing_diurno=curso.qt_ing_diurno,
                qt_ing_noturno=curso.qt_ing_noturno,
                qt_ing_vestibular=curso.qt_ing_vestibular,
                qt_ing_enem = curso.qt_ing_enem,
                qt_ing_0_24=(curso.qt_ing_0_17 + curso.qt_ing_18_24),
                qt_ing_25_29=curso.qt_ing_25_29,
                qt_ing_30_49=(curso.qt_ing_30_34 + curso.qt_ing_35_39 + curso.qt_ing_40_49),
                qt_ing_50_mais=(curso.qt_ing_50_59 + curso.qt_ing_60_mais),
                qt_ing_branca=curso.qt_ing_branca,
                qt_ing_preta = curso.qt_ing_preta,
                qt_ing_parda = curso.qt_ing_parda,
                qt_ing_amarela = curso.qt_ing_amarela,
                qt_ing_indigena = curso.qt_ing_indigena,
                qt_ing_cornd = curso.qt_ing_cornd,
                qt_ing_nacbras = curso.qt_ing_nacbras,
                qt_ing_nacestrang = curso.qt_ing_nacestrang,
                qt_ing_financ = curso.qt_ing_financ,
                qt_ing_financ_reemb = curso.qt_ing_financ_reemb,
                qt_ing_fies = curso.qt_ing_fies,
                qt_ing_rpfies = curso.qt_ing_rpfies,
                qt_ing_financ_reemb_outros = curso.qt_ing_financ_reemb_outros,
                qt_ing_financ_nreemb = curso.qt_ing_financ_nreemb,
                qt_ing_prounii = curso.qt_ing_prounii,
                qt_ing_prounip = curso.qt_ing_prounip,
                qt_ing_nrpfies = curso.qt_ing_nrpfies,
                qt_ing_financ_nreemb_outros = curso.qt_ing_financ_nreemb_outros,
                qt_ing_reserva_vaga = curso.qt_ing_reserva_vaga,
                qt_ing_rvredepublica = curso.qt_ing_rvredepublica,
                qt_ing_rvetnico = curso.qt_ing_rvetnico,
                qt_ing_rvpdef = curso.qt_ing_rvpdef,
                qt_ing_rvsocial_rf = curso.qt_ing_rvsocial_rf,
                qt_ing_rvoutros = curso.qt_ing_rvoutros,
                qt_ing_deficiente = curso.qt_ing_deficiente,
                qt_ing_procescpublica = curso.qt_ing_procescpublica,
                qt_ing_procescprivada = curso.qt_ing_procescprivada,
                qt_ing_procnaoinformada = curso.qt_ing_procnaoinformada,
                qt_ing_mob_academica = curso.qt_ing_mob_academica,
                qt_mat_branca=curso.qt_mat_branca,
                qt_mat_preta=curso.qt_mat_preta,
                qt_mat_parda=curso.qt_mat_parda,
                qt_mat_amarela=curso.qt_mat_amarela,
                qt_mat_indigena=curso.qt_mat_indigena,
                qt_mat_cornd=curso.qt_mat_cornd,
                qt_mat_nacbras=curso.qt_mat_nacbras,
                qt_mat_nacestrang=curso.qt_mat_nacestrang,
                qt_mat_deficiente=curso.qt_mat_deficiente,
                qt_mat_financ=curso.qt_mat_financ,
                qt_mat_financ_reemb=curso.qt_mat_financ_reemb,
                qt_mat_fies=curso.qt_mat_fies,
                qt_mat_rpfies=curso.qt_mat_rpfies,
                qt_mat_financ_reemb_outros=curso.qt_mat_financ_reemb_outros,
                qt_mat_financ_nreemb=curso.qt_mat_financ_nreemb,
                qt_mat_prounii=curso.qt_mat_prounii,
                qt_mat_prounip=curso.qt_mat_prounip,
                qt_mat_nrpfies=curso.qt_mat_nrpfies,
                qt_mat_financ_nreemb_outros=curso.qt_mat_financ_nreemb_outros,
                qt_mat_reserva_vaga=curso.qt_mat_reserva_vaga,
                qt_mat_rvredepublica=curso.qt_mat_rvredepublica,
                qt_mat_rvetnico=curso.qt_mat_rvetnico,
                qt_mat_rvpdef=curso.qt_mat_rvpdef,
                qt_mat_rvsocial_rf=curso.qt_mat_rvsocial_rf,
                qt_mat_rvoutros=curso.qt_mat_rvoutros,
                qt_mat_procescpublica=curso.qt_mat_procescpublica,
                qt_mat_procescprivada=curso.qt_mat_procescprivada,
                qt_mat_procnaoinformada=curso.qt_mat_procnaoinformada,
                qt_mat_mob_academica=curso.qt_mat_mob_academica,
                qt_conc=curso.qt_conc,
                qt_conc_fem=curso.qt_conc_fem,
                qt_conc_masc=curso.qt_conc_masc,
                qt_conc_diurno=curso.qt_conc_diurno,
                qt_conc_noturno=curso.qt_conc_noturno,
                qt_conc_0_24=(curso.qt_conc_0_17 + curso.qt_conc_18_24),
                qt_conc_25_29=curso.qt_conc_25_29,
                qt_conc_30_49=(curso.qt_conc_30_34 + curso.qt_conc_35_39 + curso.qt_conc_40_49),
                qt_conc_50_mais=(curso.qt_conc_50_59 + curso.qt_conc_60_mais),
                qt_conc_branca=curso.qt_conc_branca,
                qt_conc_preta=curso.qt_conc_preta,
                qt_conc_parda=curso.qt_conc_parda,
                qt_conc_amarela=curso.qt_conc_amarela,
                qt_conc_indigena=curso.qt_conc_indigena,
                qt_conc_cornd=curso.qt_conc_cornd,
                qt_conc_nacbras=curso.qt_conc_nacbras,
                qt_conc_nacestrang=curso.qt_conc_nacestrang,
                qt_conc_deficiente=curso.qt_conc_deficiente,
                qt_conc_financ=curso.qt_conc_financ,
                qt_conc_financ_reemb=curso.qt_conc_financ_reemb,
                qt_conc_fies=curso.qt_conc_fies,
                qt_conc_rpfies=curso.qt_conc_rpfies,
                qt_conc_financ_reemb_outros=curso.qt_conc_financ_reemb_outros,
                qt_conc_financ_nreemb=curso.qt_conc_financ_nreemb,
                qt_conc_prounii=curso.qt_conc_prounii,
                qt_conc_prounip=curso.qt_conc_prounip,
                qt_conc_nrpfies=curso.qt_conc_nrpfies,
                qt_conc_financ_nreemb_outros=curso.qt_conc_financ_nreemb_outros,
                qt_conc_reserva_vaga=curso.qt_conc_reserva_vaga,
                qt_conc_rvredepublica=curso.qt_conc_rvredepublica,
                qt_conc_rvetnico=curso.qt_conc_rvetnico,
                qt_conc_rvpdef=curso.qt_conc_rvpdef,
                qt_conc_rvsocial_rf=curso.qt_conc_rvsocial_rf,
                qt_conc_rvoutros=curso.qt_conc_rvoutros,
                qt_conc_procescpublica=curso.qt_conc_procescpublica,
                qt_conc_procescprivada=curso.qt_conc_procescprivada,
                qt_conc_procnaoinformada=curso.qt_conc_procnaoinformada,
                qt_sit_trancada=curso.qt_sit_trancada,
                qt_sit_desvinculado=curso.qt_sit_desvinculado,
                qt_sit_transferido=curso.qt_sit_transferido,
                qt_sit_falecido=curso.qt_sit_falecido,
                qt_aluno_deficiente=curso.qt_aluno_deficiente,
                qt_mob_academica=curso.qt_mob_academica,
                qt_conc_mob_academica=curso.qt_conc_mob_academica
                # Continue mapeando as outras colunas conforme necessário...
            )

            # Adicionar o registro à sessão
            session.add(censo)
            count += 1

            # Fazer commit a cada 'batch_size' registros
            if count % batch_size == 0:
                session.commit()
                print(f"{count} registros transferidos até agora...")

        # Fazer o commit dos registros restantes
        session.commit()
        print(f"Transferência completa! Total de registros: {count}")
    except Exception as e:
        session.rollback()  # Em caso de erro, desfazer a transação
        print(f"Erro ao transferir dados: {e}")

    finally:
        session.close()

# Chame a função para realizar a transferência
transfer_data(batch_size=1000)
