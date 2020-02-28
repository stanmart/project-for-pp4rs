from os.path import join
configfile: "config.yaml"


FIGS = glob_wildcards(join(config["src_figures"], "{i_file}.py")).i_file
rule temp_top:
    input:
        figs = expand(join(config["figure_dir"], "{i_figure}.png"), i_figure = FIGS)


rule figures:
    input:
        script = join(config["src_figures"], "{i_figure}.py"),
        dataset = join(config["compiled_data_dir"], "plot_data.csv")
    output:
        png = "out/figures/{i_figure}.png"
    shell:
        "python {input.script} \
            --data {input.dataset} \
            --out {output} \
            --width 1600"


rule download_data:
    input:
        script = join(config["src_utils"], "obtain_data.py"),
        config = "config.yaml"
    output:
        files = expand(
            join(config["raw_data_dir"], "{gtfs_file}.txt"),
            gtfs_file = config["gtfs_contents"]
        )
    params:
        out_dir = config["raw_data_dir"],
        url = config["url"]
    shell:
        "python {input.script} \
            --url {params.url} \
            --out-dir {params.out_dir}"


rule create_shape_data:
    input:
        script = join(config["src_utils"], "reshape_data.py"),
        gtfs_files = expand(
            join(config["raw_data_dir"], "{gtfs_file}.txt"),
            gtfs_file = ["trips", "routes", "calendar", "calendar_dates"]
        )
    output:
        csv = join(config["compiled_data_dir"], "shape_data.csv")
    params:
        gtfs_dir = config["raw_data_dir"]
    shell:
        "python {input.script} shape \
            --gtfs-dir {params.gtfs_dir} \
            --out {output.csv}"


rule create_plot_data:
    input:
        script = join(config["src_utils"], "reshape_data.py"),
        shape_data = join(config["compiled_data_dir"], "shape_data.csv"),
        gtfs_shapes = join(config["raw_data_dir"], "shapes.txt")
    output:
        csv = join(config["compiled_data_dir"], "plot_data.csv")
    params:
        gtfs_dir = config["raw_data_dir"]
    shell:
        "python {input.script} plot \
            --gtfs-dir {params.gtfs_dir} \
            --shape-data {input.shape_data} \
            --out {output.csv}"


rule clean:
    shell:
        "rm -r out/*"


# --- Graphs --- #

rule filegraph:
    input:
        "Snakefile"
    output:
        "build_graphs/filegraph.pdf"
    shell:
        "snakemake --filegraph | dot -Tpdf > build_graphs/filegraph.pdf"

rule rulegraph:
    input:
        "Snakefile"
    output:
        "build_graphs/rulegraph.pdf"
    shell:
        "snakemake --rulegraph | dot -Tpdf > build_graphs/rulegraph.pdf"

rule dag:
    input:
        "Snakefile"
    output:
        "build_graphs/dag.pdf"
    shell:
        "snakemake --dag | dot -Tpdf > build_graphs/dag.pdf"