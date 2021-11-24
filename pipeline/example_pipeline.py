from kfp import dsl


def random_num_op(low, high):
  """Generate a random number between low and high."""
  return dsl.ContainerOp(
      name='Generate random number',
      image='python:alpine3.6',
      command=['sh', '-c'],
      arguments=['python -c "import random; print(random.randint($0, $1))" | tee $2',
        str(low), str(high), '/tmp/output'],
      file_outputs={'output': '/tmp/output'}
    )


def flip_coin_op():
  """Flip a coin and output heads or tails randomly."""
  return dsl.ContainerOp(
    name='Flip coin',
    image='python:alpine3.6',
    command=['sh', '-c'],
    arguments=['python -c "import random; result = \'heads\' if random.randint(0,1) == 0 '
      'else \'tails\'; print(result)" | tee /tmp/output'],
      file_outputs={'output': '/tmp/output'}
    )


def print_op(msg):
  """Print a message."""
  return dsl.ContainerOp(
    name='Print',
    image='alpine:3.6',
    command=['echo', msg])


@dsl.pipeline(
  name='Conditional execution pipeline',
  description='Shows how to use dsl.Condition().'
)
def flipcoin_pipeline():
  flip = flip_coin_op()
  with dsl.Condition(flip.output == 'heads'):
    random_num_head = random_num_op(0, 9)
    with dsl.Condition(random_num_head.output > 5):
      print_op('heads and %s > 5!' % random_num_head.output)
    with dsl.Condition(random_num_head.output <= 5):
      print_op('heads and %s <= 5!' % random_num_head.output)

  with dsl.Condition(flip.output == 'tails'):
    random_num_tail = random_num_op(10, 19)
    with dsl.Condition(random_num_tail.output > 15):
      print_op('tails and %s > 15!' % random_num_tail.output)
    with dsl.Condition(random_num_tail.output <= 15):
      print_op('tails and %s <= 15!' % random_num_tail.output)
 

# Another pipeline

@dsl.pipeline(
    name="NLP", 
    description="A pipeline demonstrating reproducible steps for NLP"
)
def nlp_pipeline(
    csv_url="https://raw.githubusercontent.com/axsauze/reddit-classification-exploration/master/data/reddit_train.csv",
    csv_encoding="ISO-8859-1",
    features_column="BODY",
    labels_column="REMOVED",
    raw_text_path="/mnt/text.data",
    labels_path="/mnt/labels.data",
    clean_text_path="/mnt/clean.data",
    spacy_tokens_path="/mnt/tokens.data",
    tfidf_vectors_path="/mnt/tfidf.data",
    lr_prediction_path="/mnt/prediction.data",
    tfidf_model_path="/mnt/tfidf.model",
    lr_model_path="/mnt/lr.model",
    lr_c_param=0.1,
    tfidf_max_features=10000,
    tfidf_ngram_range=3,
    batch_size="100",
):

    vop = dsl.VolumeOp(
        name="my-pvc", resource_name="my-pvc", modes=dsl.VOLUME_MODE_RWO, size="20Mi"
    )

    download_step = dsl.ContainerOp(
        name="data_downloader",
        image="data_downloader:0.1",
        command="python",
        arguments=[
            "/microservice/pipeline_step.py",
            "--labels-path",
            labels_path,
            "--features-path",
            raw_text_path,
            "--csv-url",
            csv_url,
            "--csv-encoding",
            csv_encoding,
            "--features-column",
            features_column,
            "--labels-column",
            labels_column,
        ],
        pvolumes={"/mnt": vop.volume},
    )

    clean_step = dsl.ContainerOp(
        name="clean_text",
        image="clean_text_transformer:0.1",
        command="python",
        arguments=[
            "/microservice/pipeline_step.py",
            "--in-path",
            raw_text_path,
            "--out-path",
            clean_text_path,
        ],
        pvolumes={"/mnt": download_step.pvolume},
    )

    tokenize_step = dsl.ContainerOp(
        name="tokenize",
        image="spacy_tokenizer:0.1",
        command="python",
        arguments=[
            "/microservice/pipeline_step.py",
            "--in-path",
            clean_text_path,
            "--out-path",
            spacy_tokens_path,
        ],
        pvolumes={"/mnt": clean_step.pvolume},
    )

    vectorize_step = dsl.ContainerOp(
        name="vectorize",
        image="tfidf_vectorizer:0.1",
        command="python",
        arguments=[
            "/microservice/pipeline_step.py",
            "--in-path",
            spacy_tokens_path,
            "--out-path",
            tfidf_vectors_path,
            "--max-features",
            tfidf_max_features,
            "--ngram-range",
            tfidf_ngram_range,
            "--action",
            "train",
            "--model-path",
            tfidf_model_path,
        ],
        pvolumes={"/mnt": tokenize_step.pvolume},
    )

    predict_step = dsl.ContainerOp(
        name="predictor",
        image="lr_text_classifier:0.1",
        command="python",
        arguments=[
            "/microservice/pipeline_step.py",
            "--in-path",
            tfidf_vectors_path,
            "--labels-path",
            labels_path,
            "--out-path",
            lr_prediction_path,
            "--c-param",
            lr_c_param,
            "--action",
            "train",
            "--model-path",
            lr_model_path,
        ],
        pvolumes={"/mnt": vectorize_step.pvolume},
    )

   
    seldon_config = yaml.load(
            open("../deploy/merge.yaml")
        )

    deploy_step = dsl.ResourceOp(
        name="seldondeploy",
        k8s_resource=seldon_config,
        attribute_outputs={"name": "{.metadata.name}"},
    )
    


    deploy_step.after(predict_step)
