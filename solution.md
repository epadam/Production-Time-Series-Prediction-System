## CI:

In this setup, the pipeline and its components are built, tested, and packaged when new code is committed or pushed to the source code repository. Besides building packages, container images, and executables, the CI process can include the following tests:

Unit testing your feature engineering logic.

Unit testing the different methods implemented in your model. For example, you have a function that accepts a categorical data column and you encode the function as a one-hot feature.

Testing that your model training converges (that is, the loss of your model goes down by iterations and overfits a few sample records).

Testing that your model training doesn't produce NaN values due to dividing by zero or manipulating small or large values.

Testing that each component in the pipeline produces the expected artifacts.

Testing integration between pipeline components.

Continuous delivery


## Continuous delivery
In this level, your system continuously delivers new pipeline implementations to the target environment that in turn delivers prediction services of the newly trained model. For rapid and reliable continuous delivery of pipelines and models, you should consider the following:

Verifying the compatibility of the model with the target infrastructure before you deploy your model. For example, you need to verify that the packages that are required by the model are installed in the serving environment, and that the memory, compute, and accelerator resources that are available.

Testing the prediction service by calling the service API with the expected inputs, and making sure that you get the response that you expect. This test usually captures problems that might occur when you update the model version and it expects a different input.

Testing prediction service performance, which involves load testing the service to capture metrics such as queries per seconds (QPS) and model latency.

Validating the data either for retraining or batch prediction.

Verifying that models meet the predictive performance targets before they are deployed.

Automated deployment to a test environment, for example, a deployment that is triggered by pushing code to the development branch.

Semi-automated deployment to a pre-production environment, for example, a deployment that is triggered by merging code to the main branch after reviewers approve the changes.

Manual deployment to a production environment after several successful runs of the pipeline on the pre-production environment.
