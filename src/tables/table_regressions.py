import argparse
import pickle
from stargazer.stargazer import Stargazer


def create_table(models, out):
    """Creates a table of regression results.

    Args:
        models: regression results
        out: the generated table is saved here

    Returns:
        None
    """

    results = []
    model_names = []
    covariate_names = {}

    for model in models:
        with open(model, 'rb') as file:
            result = (pickle.load(file))
        results.append(result)
        model_names.append(result.model_name)
        covariate_names.update(result.var_names)

    table = Stargazer(results)
    table.dependent_variable_name(covariate_names[results[0].model.endog_names])
    table.custom_columns(model_names, [1] * len(model_names))
    table.rename_covariates(covariate_names)

    with open(out, 'w') as file:
        file.write(table.render_latex())


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-r', '--reg-results',
        help="List of regression results",
        nargs='+',
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

    create_table(args.reg_results, args.out)


if __name__ == "__main__":
    main()
