# common-python-reporter
Shared library for implementing test result reporting to the Applause services. 

## Prerequisites

```bash
brew install pipenv   # installs pipenv
export PIPENV_VENV_IN_PROJECT=1
pipenv install        # installs python dependencies into pipenv
pipenv install --dev  # installs python dev-dependencies into pipenv
```

Add this to your .bashrc/.zshrc to stick python virtualenv to project directory.

```export PIPENV_VENV_IN_PROJECT=1```

## Building the Project

We use tox to automate our build pipeline. Running the default tox configuration will install dependencies, format and lint the project, run the unit test and run the build. This will verify the project builds correctly for python 3.8, 3.9, 3.10, and 3.11. 

```bash
pipenv run tox
```

Currently, our tox configuration relies on the existence of the requirements.txt files. If this file is not up to date with the Pipenv file, we could run into problems with the build. The tox-pipenv currently does not support Tox 4.0+. Once the plugin has been fixed under this issue: https://github.com/tox-dev/tox-pipenv/issues/73, we can resolve this limitation.

### Executing Unit Tests

The unit tests can be executed through tox `tox run -e test`

### Intellij setup

https://www.jetbrains.com/help/idea/pipenv.html

### Helpful commands

```bash
pipenv --py # shows python version for your venv
pipenv --venv # shows venv directory (packages will be installed there)

To activate this project's virtualenv, run the following:
$ pipenv shell

To exit the virtualenv shell:
$ exit

To install packages into this virtualenv:
$ pipenv install YOUR_PACKAGE


```

## Usage

### Configuration

```python
    from config import ApplauseConfig

    config = ApplauseConfig(kwArgs**)
```

Valid Options:
- auto_api_base_url: The base url for the auto api client
- public_api_base_url: The base url for the public api client
- api_key: The api key for the client
- product_id: The id of the product
- test_rail_options: The test rail options
- applause_test_cycle_id: The id of the test cycle

#### TestRail Configuration

Valie Options
project_id: The id of the project
suite_id: The id of the suite
plan_name: The name of the plan
run_name: The name of the run
add_all_tests_to_plan (optional): Flag to add all tests to the plan
override_test_rail_run_uniqueness (optional): Flag to override test rail run uniqueness check

### Direct HTTP Client Usage

#### Auto API

```python
    from config import ApplauseConfig
    from auto_api import AutoApi

    # Configure the AutoApi Client
    config = ApplauseConfig(api_key="your_api_key", product_id=12345, test_rail_options=None, applause_test_cycle_id=None)
    auto_api = AutoApi(config)

    # Start a Test Run
    tr_id = auto_api.start_test_run(TestRunCreateDto(tests=["test1", "test2"])).test_run_id

    # Submit Test Case Results
    test_case = auto_api.start_test_case(CreateTestCaseResultDto(test_run_id=tr_id, test_case_name="test1", provider_session_ids=[]))
    auto_api.submit_test_case_result(SubmitTestCaseResultDto(test_result_id=test_case.test_result_id, status=TestResultStatus.PASSED, provider_session_ids=[]))
    # Repeat for other test cases

    # End the Test Run
    auto_api.end_test_run(tr_id)
```

#### Public API

```python
config = ApplauseConfig(...)
public_api = PublicApi(config)
public_api.submit_result(123, TestRunAutoResultDto(...))
# Submit additional results as needed
```


### Common Reporter Interface

```python
from reporter import ApplauseReporter()

ApplauseReporter = ApplauseReporter(config)
run_id = ApplauseReporter.runner_start(tests=["test1", "test2"])
ApplauseReporter.start_test_case("test1", "test1", params=AdditionalTestCaseParams(...))
ApplauseReporter.submit_test_case_result("test1", TestResultStatus.PASSED, params=AdditionalTestCaseResultParams(...))
```

