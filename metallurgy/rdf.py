import numpy as np
from ovito.io import import_file, export_file
from ovito.modifiers import CoordinationAnalysisModifier


def rdf(structure_path):

    pipeline = import_file(structure_path)
    pipeline.modifiers.append(
        CoordinationAnalysisModifier(cutoff=10, number_of_bins=150)
    )

    data = pipeline.compute()

    return data.tables["coordination-rdf"]["g(r)"]


def smoothness(structure_path, filter=False):

    RDF = rdf(structure_path)

    RDF_diffs = []
    for i in range(1, len(RDF)):
        RDF_diffs.append(RDF[i] - RDF[i - 1])

    smoothness = np.abs(np.mean(RDF_diffs)) / np.std(RDF_diffs)

    return smoothness
