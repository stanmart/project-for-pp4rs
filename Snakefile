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
        script = join(config["src_utils"], "obtain_data.py")
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


rule reshape_data:
    input:
        script = join(config["src_utils"], "reshape_data.py"),
        files = expand(
            join(config["raw_data_dir"], "{gtfs_file}.txt"),
            gtfs_file = config["gtfs_contents"]
        )
    output:
        datasets = expand(
            join(config["compiled_data_dir"], "{reshaped_file}.csv"),
            reshaped_file = ["shape_data", "plot_data"]
        )
    params:
        data_dir = config["raw_data_dir"]
    shell:
        "python {input.script} \
            --gtfs-dir {params.data_dir} \
            --out-dir {params.data_dir}"


rule clean:
    shell:
        "rm -r out/*"


# --- Graphs --- #

rule filegraph:
    input:
        "Snakefile"
    output:
        "filegraph.pdf"
    shell:
        "snakemake --filegraph | dot -Tpdf > filegraph.pdf"

rule rulegraph:
    input:
        "Snakefile"
    output:
        "filegraph.pdf"
    shell:
        "snakemake --rulegraph | dot -Tpdf > rulegraph.pdf"

rule dag:
    input:
        "Snakefile"
    output:
        "filegraph.pdf"
    shell:
        "snakemake --dag | dot -Tpdf > dag.pdf"
