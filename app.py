import streamlit as st

st.title('Machine Learning for Data Analysis Tutorial')


tasks = ['Choose a step', 'Data Preprocessing and Analysis', 'Model Building and Training', 'Model Evaluation and Interpretation', 'Model Deployment', 'Model Monitoring']

st.sidebar.markdown('#### Select the step in machine learning pipeline')
node = st.sidebar.selectbox('', tasks)

# all the processing code should be here, below should just display


st.text('')

if node == 'Choose a step':
    st.write('In contrast to rule-based analysis solutions, machine learning solution is mainly for data without clear patten or rules to follow. This tutorial gives common machine learning techeniques for data analysis.')

    st.header('Lifecycle of a machine learning model')

    

    st.write('The entire machine learning process for data analysis includes many steps. Developing model is just small part of the entire system.')
    st.image('sys.png', caption='from paper "Hidden Technical Debt in Machine Learning Systems"', use_column_width=True)

    st.write('In order to better control the whole process, we need some tools.')
    st.subheader('Machine Learning Pipeline')

    st.write('A famous solution for the machine learning lifecycle is Kubeflow from Google, it offers the pipeline for developing the machine learning model from data processing to model deloyment. In this tutorial, we will use Kubeflow to build the machine learning pipeline.')

    st.subheader('Tracking and Monitoring for Model Training')

    st.write('Mlflow is one of the most convenient tool for tracking the training of the machine learning models. we will also use this tool to track training results with different parameters.')

    st.subheader('Data Privacy')

    st.write('Not all data can leave their machine or building. Like some medical images in different hospitals')

    st.markdown('#### Federated Learning')

    


    
    

elif node == 'Data Preprocessing and Analysis':
    st.header('Data Preprocessing and Analysis')
    st.text('')
    st.write('There are two major tasks in machine learning for data analysis. One is classification and the other is regression. We will use Heart Disease Dataset as classification example in this tutorial.')
    
    st.write('For regression example please check th tutorial using Boston house price dataset')
    st.image('h.jpg')
    st.write(' The heart disease dataset include 14 features.')

    st.write('Here we can use some data analysis techniques to interpretate the data')



elif node == 'Model Building and Training':
    st.header('Model Building and Training')
    st.text('')
    
    st.write('In the machine learning era, the most famous library for model building is Scikit learn. However, after deep learning era, you can also use tensorflow or pytorch to build deep learning model')
    st.write('Scikit learn offers many machine learning algorithms')

    st.write('In the real environment, tracking and registering the model training and versioning is very important')

    st.subheader('AutoML')
    st.write('Another interesting solution is AutoML, which human is not involved in the model developing loop. A famous example is Goole AutoML Table')

elif node == 'Model Evaluation and Interpretation':
    st.header('Model Evaluation and Interpretation')
    st.text('')
    st.subheader('Model Evaluation')
    st.write('Test set is used to evaluate the performance of the model. However, machine learning models are often refered to black box models. There are also couple of model interpretation methods that allows us explore and reveal more information of the model')
    st.subheader('Model Interpretation')
    st.write('There are many ways to interpretate and explore the model. Three major methods include SHAP, permutation importance, partial dependance plot')

    st.subheader('Tools and Resources')
    st.markdown('[1. Manifold from Uber](https://github.com/uber/manifold#manifold)')
    st.text('A model-agnostic visual debugging tool for machine learning.')

elif node == 'Model Deployment':
    st.header('Model Deployment')
    st.text('')
    st.write('After the model is trained and evaluated. The best model will be deployed in the real world applications. The model can be deployed on the server, at the edge devices like smartphone or just run in your browser.')
    st.subheader('Model server side deployment solutions on the market')
    st.write('TF serving, KFserving, Cortex')
    st.write('Here the model is deployed using TFserving on GCP')

elif node == 'Model Monitoring':
    st.header('Model Monitoring')
    st.text('')
    st.write('Continuing monitor the performance of the model is very important.')





