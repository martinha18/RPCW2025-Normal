import json
import re
from rdflib import Graph, Namespace, URIRef, RDF, OWL, Literal

# --------------------------------------------------------------------
# Carregar a ontologia base para o grafo em memória
# --------------------------------------------------------------------
n = Namespace("http://www.semanticweb.org/marta/ontologies/2025/sapientia#")
g = Graph()
g.parse("sapientia_base.ttl")

file_conceitos = "conceitos.json"
file_disciplinas = "disciplinas.json"
file_mestres = "mestres.json"
file_obras = "obras.json"
file_aprendizes = "pg55983.json"


disciplinas = {}
conceitos = {}
mestres = {}
obras = {}
aprendizes = {}
tipos = {}
aplicacoes = {}
periodos = {}

with open(file_disciplinas) as f:
    data_disciplinas = json.load(f)

with open(file_conceitos) as f:
    data_conceitos = json.load(f)

with open(file_mestres) as f:   
    data_mestres = json.load(f)

with open(file_obras) as f:
    data_obras = json.load(f)

with open(file_aprendizes) as f:
    data_aprendizes = json.load(f)

# --------------------------------------------------------------------

for conceito in data_conceitos['conceitos']:
    conceitoURI = URIRef(f"{n}Conceito_{len(conceitos)}")
    conceitos[conceito['nome']] = conceitoURI
    g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
    g.add((conceitoURI, RDF.type, n.Conceito))
    g.add((conceitoURI, n.nome, Literal(conceito['nome'])))

    if 'aplicações' in conceito:
        for aplicacao in conceito['aplicações']:
            if aplicacao not in aplicacoes.keys():
                aplicacaoURI = URIRef(f"{n}Aplicacao_{len(aplicacoes)}")
                aplicacoes[aplicacao] = aplicacaoURI
                g.add((aplicacaoURI, RDF.type, OWL.NamedIndividual))
                g.add((aplicacaoURI, RDF.type, n.Aplicacao))
                g.add((aplicacaoURI, n.nome, Literal(aplicacao)))
            else:
                aplicacaoURI = aplicacoes[aplicacao]

            g.add((conceitoURI, n.temAplicaçãoEm, aplicacaoURI))

    if 'períodoHistórico'in conceito:
        if conceito['períodoHistórico'] not in periodos.keys():
            periodoURI = URIRef(f"{n}Periodo_{len(periodos)}")
            periodos[conceito['períodoHistórico']] = periodoURI
            g.add((periodoURI, RDF.type, OWL.NamedIndividual))
            g.add((periodoURI, RDF.type, n.Periodo))
            g.add((periodoURI, n.nome, Literal(conceito['períodoHistórico'])))
        else:
            periodoURI = periodos[conceito['períodoHistórico']]

        g.add((conceitoURI, n.surgeEm, periodoURI))

    if 'conceitosRelacionados' in conceito:
        for conceito_relacionado in conceito['conceitosRelacionados']:
            if conceito_relacionado not in conceitos.keys():
                conceito_relacionadoURI = URIRef(f"{n}Conceito_{len(conceitos)}")
                conceitos[conceito_relacionado] = conceito_relacionadoURI
                g.add((conceito_relacionadoURI, RDF.type, OWL.NamedIndividual))
                g.add((conceito_relacionadoURI, RDF.type, n.Conceito))
                g.add((conceito_relacionadoURI, n.nome, Literal(conceito_relacionado)))
            else:
                conceito_relacionadoURI = conceitos[conceito_relacionado]

            g.add((conceitoURI, n.estáRelacionadoCom, conceito_relacionadoURI))



for disciplina in data_disciplinas['disciplinas']:
    disciplinaURI = URIRef(f"{n}Disciplina_{len(disciplinas)}")
    disciplinas[disciplina['nome']] = disciplinaURI
    g.add((disciplinaURI, RDF.type, OWL.NamedIndividual))
    g.add((disciplinaURI, RDF.type, n.Disciplina))
    g.add((disciplinaURI, n.nome, Literal(disciplina['nome'])))

    if 'tiposDeConhecimento' in disciplina:
        for tipo in disciplina['tiposDeConhecimento']:
            if tipo not in tipos.keys():
                tipoURI = URIRef(f"{n}TipoDeConhecimento_{len(tipos)}")
                tipos[tipo] = tipoURI
                g.add((tipoURI, RDF.type, OWL.NamedIndividual))
                g.add((tipoURI, RDF.type, n.TipoDeConhecimento))
                g.add((tipoURI, n.nome, Literal(tipo)))
            else:
                tipoURI = tipos[tipo]

            g.add((disciplinaURI, n.pertenceA, tipoURI))
    
    if 'conceitos' in disciplina:
        for conceito in disciplina['conceitos']:
            if conceito not in conceitos.keys():
                conceitoURI = URIRef(f"{n}Conceito_{len(conceitos)}")
                conceitos[conceito] = conceitoURI
                g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
                g.add((conceitoURI, RDF.type, n.Conceito))
                g.add((conceitoURI, n.nome, Literal(conceito)))
            else:
                conceitoURI = conceitos[conceito]

            g.add((conceitoURI, n.éEstudadoEm, disciplinaURI))


for mestre in data_mestres['mestres']:
    mestreURI = URIRef(f"{n}Mestre_{len(mestres)}")
    mestres[mestre['nome']] = mestreURI
    g.add((mestreURI, RDF.type, OWL.NamedIndividual))
    g.add((mestreURI, RDF.type, n.Mestre))
    g.add((mestreURI, n.nome, Literal(mestre['nome'])))

    if 'disciplinas' in mestre:
        for disciplina in mestre['disciplinas']:
            if disciplina not in disciplinas.keys():
                disciplinaURI = URIRef(f"{n}Disciplina_{len(disciplinas)}")
                disciplinas[disciplina] = disciplinaURI
                g.add((disciplinaURI, RDF.type, OWL.NamedIndividual))
                g.add((disciplinaURI, RDF.type, n.Disciplina))
                g.add((disciplinaURI, n.nome, Literal(disciplina)))
            else:
                disciplinaURI = disciplinas[disciplina]

            g.add((mestreURI, n.ensina, disciplinaURI))

    if 'períodoHistórico' in mestre:
        if mestre['períodoHistórico'] not in periodos.keys():
            periodoURI = URIRef(f"{n}Periodo_{len(periodos)}")
            periodos[mestre['períodoHistórico']] = periodoURI
            g.add((periodoURI, RDF.type, OWL.NamedIndividual))
            g.add((periodoURI, RDF.type, n.Periodo))
            g.add((periodoURI, n.nome, Literal(mestre['períodoHistórico'])))
        else:
            periodoURI = periodos[mestre['períodoHistórico']]

        g.add((mestreURI, n.viveuEm, periodoURI))

for obra in data_obras['obras']:
    obraURI = URIRef(f"{n}Obra_{len(obras)}")
    obras[obra['titulo']] = obraURI
    g.add((obraURI, RDF.type, OWL.NamedIndividual))
    g.add((obraURI, RDF.type, n.Obra))
    g.add((obraURI, n.título, Literal(obra['titulo'])))

    if 'autor' in obra:
        if obra['autor'] not in mestres.keys():
            mestreURI = URIRef(f"{n}Mestre_{len(mestres)}")
            mestres[obra['autor']] = mestreURI
            g.add((mestreURI, RDF.type, OWL.NamedIndividual))
            g.add((mestreURI, RDF.type, n.Mestre))
            g.add((mestreURI, n.nome, Literal(obra['autor'])))
        else:
            mestreURI = mestres[obra['autor']]

        g.add((obraURI, n.foiEscritaPor, mestreURI))

    if 'conceitos' in obra:
        for conceito in obra['conceitos']:
            if conceito not in conceitos.keys():
                conceitoURI = URIRef(f"{n}Conceito_{len(conceitos)}")
                conceitos[conceito] = conceitoURI
                g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
                g.add((conceitoURI, RDF.type, n.Conceito))
                g.add((conceitoURI, n.nome, Literal(conceito)))
            else:
                conceitoURI = conceitos[conceito]

            g.add((obraURI, n.explica, conceitoURI))

for aprendiz in data_aprendizes:
    aprendizURI = URIRef(f"{n}Aprendiz_{len(aprendizes)}")
    aprendizes[aprendiz['nome']] = aprendizURI
    g.add((aprendizURI, RDF.type, OWL.NamedIndividual))
    g.add((aprendizURI, RDF.type, n.Aprendiz))
    g.add((aprendizURI, n.nome, Literal(aprendiz['nome'])))

    if 'idade' in aprendiz:
        g.add((aprendizURI, n.idade, Literal(aprendiz['idade'])))

    if 'disciplinas' in aprendiz:
        for disciplina in aprendiz['disciplinas']:
            if disciplina not in disciplinas.keys():
                disciplinaURI = URIRef(f"{n}Disciplina_{len(disciplinas)}")
                disciplinas[disciplina] = disciplinaURI
                g.add((disciplinaURI, RDF.type, OWL.NamedIndividual))
                g.add((disciplinaURI, RDF.type, n.Disciplina))
                g.add((disciplinaURI, n.nome, Literal(disciplina)))
            else:
                disciplinaURI = disciplinas[disciplina]

            g.add((aprendizURI, n.aprende, disciplinaURI))

        
        

        
print(len(g))

final_ttl = g.serialize(format="turtle")
open("sapientia_ind.ttl", "w").write(final_ttl)

