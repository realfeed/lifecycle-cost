# Life-cycle cost model

This tool automates Monte-Carlo estimation and generates an interactive web plot of the probability of life-cycle cost for a project using the `plotly` package.

Input assumptions into `2017-02-07_lifecycle Cost Model_AP`

Activate a virtual environment and install requirements:

`virtualenv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

Call each of the functions in class `Building()` in the order displayed in the `building.py` script.

`lifecycle-cost.ipnyb` is an example notebook that sets required variables for processing and reads data from the `2017-02-07_Lifecycle Cost Model` workbook. These two documents can be altered for project needs.

A `plotly` account is required to visualise the processed output. Sign-up here to generate a `username` and `api_key` before generating a credentials file.

Class `Building()` requires definition of the source workbook fully qualified filename from the root directory as `wb` and worksheet name as `name`.

This will require defining the variables `size_of_factor_sample` and `number_of_element_cost_samples` which affect rigour and processing time (default value = 1000).

This will also require definition of:

`building_life` when calling `Building.build_data_for_building_lifetime`, which should relate to the projects design operational life.

`n_estimates` when calling `Building.costs_for_building_lifes`, which relates to the number of estimations to conduct in the Monte-Carlo analysis.
