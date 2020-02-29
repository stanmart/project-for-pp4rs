import argparse
import pandas as pd
import statsmodels.formula.api as smf
import pickle
import yaml


def estimate_ols(data, specs, out):
    """Estimates a linear model.

    Args:
        data: a csv file containing the data used for the estimation
        specs: A YAML file containing model specifications
        out: the pickledmodel object is saved here

    Returns:
        None
    """

    dataset = pd.read_csv(data, low_memory=False)
    with open(specs, 'r') as specs_yaml:
        specs_dict = yaml.load(specs_yaml, Loader=yaml.FullLoader)

    formula = "{dep_var} ~ {indep_vars}".format(
        dep_var=list(specs_dict["dep_var"].keys())[0],
        indep_vars=" + ".join(specs_dict["indep_vars"].keys())
    )

    model = smf.ols(formula, dataset)
    model_result = model.fit(cov_type=specs_dict["cov_type"])

    model_result.model_name = specs_dict["name"]
    model_result.var_names = {**specs_dict["dep_var"], **specs_dict["indep_vars"]}

    with open(out, 'wb') as out_file:
        pickle.dump(model_result, out_file)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d', '--data',
        help="A csv file containing regression data",
        type=str,
        required=True
    )
    parser.add_argument(
        '-s', '--specs',
        help="A YAML file containing model specifications",
        type=str,
        required=True
    )
    parser.add_argument(
        '-o', '--out',
        help="The path of the output file",
        type=str,
        required=True
    )

    args = parser.parse_args()

    estimate_ols(args.data, args.specs, args.out)


if __name__ == "__main__":
    main()
