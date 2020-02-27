FIGS = glob_wildcards("src/figures/{i_file}.py").i_file
rule temp_top:
    input:
        figs = expand("out/figures/{i_figure}.png", i_figure = FIGS)


rule figures:
    input:
        script = "src/figures/{i_figure}.py",
        dataset = "out/data/plot_data.csv"
    output:
        png = "out/figures/{i_figure}.png"
    shell:
        "python {input.script} \
            --data {input.dataset} \
            --out {output} \
            --width 1600"


rule download_data:
    input:
        script = "src/utils/obtain_data.py"
    output:
        files = expand(
            "out/data/{gtfs_file}.txt",
            gtfs_file = ["trips", "routes", "calendar", "calendar_dates", "shapes"]
        )
    params:
        out_dir = "out/data",
        url = "https://data.stadt-zuerich.ch/dataset/ec7bb57c-f0aa-4e8e-9266-f0b7112f6355/resource/8756b31e-7d2c-4a31-bf16-ab23adbf41b4/download/2020_google_transit.zip"
    shell:
        "python {input.script} \
            --url {params.url} \
            --out-dir {params.out_dir}"


rule reshape_data:
    input:
        script = "src/utils/reshape_data.py",
        files = expand(
            "out/data/{gtfs_file}.txt",
            gtfs_file = ["trips", "routes", "calendar", "calendar_dates", "shapes"]
        )
    output:
        datasets = expand(
            "out/data/{reshaped_file}.csv",
            reshaped_file = ["shape_data", "plot_data"]
        )
    params:
        data_dir = "out/data",
        url = "https://data.stadt-zuerich.ch/dataset/ec7bb57c-f0aa-4e8e-9266-f0b7112f6355/resource/8756b31e-7d2c-4a31-bf16-ab23adbf41b4/download/2020_google_transit.zip"
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
