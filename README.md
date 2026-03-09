# Cybersecurity Incident Analysis using Fine-Tuned Language Models

## Project Overview

This project explores the use of **Large Language Models (LLMs)** to support **cybersecurity incident analysis and classification**. The objective is to investigate how fine-tuned language models can assist in interpreting textual descriptions of security incidents and automatically map them to structured cybersecurity knowledge.

The models developed in this project are designed to perform tasks such as:

- Mapping incident descriptions to **MITRE ATT&CK tactics and techniques**
- Estimating **incident severity**
- Supporting structured analysis of security events

The research evaluates the impact of **model size** and **training data quality** on the performance of cybersecurity-specific natural language tasks.

The models were fine-tuned using the **LoRA (Low-Rank Adaptation)** technique, which allows efficient adaptation of large language models while significantly reducing the number of trainable parameters.

## Objectives

The main goals of this project include:

- Investigating the applicability of **LLMs in cybersecurity incident analysis**
- Comparing the performance of **two models with different sizes**
- Evaluating model capability across multiple cybersecurity classification tasks
- Demonstrating a **practical deployment** of the trained model using an interactive interface

## Methodology

The workflow followed in this project includes:

1. **Dataset preparation**  
   Creation and preprocessing of a cybersecurity-focused dataset containing incident descriptions and structured labels.

2. **Model selection**  
   Two models from the same architecture family were selected to analyze the effect of model scale.

3. **Fine-tuning**  
   Models were fine-tuned using **LoRA** to efficiently adapt them for cybersecurity tasks.

4. **Evaluation**  
   The models were evaluated using multiple metrics across different classification tasks.

5. **Deployment**  
   A trained model was deployed as an interactive application using **Gradio**, allowing users to submit incident descriptions and receive automated analysis.

## Repository Structure

├── data/ # Dataset files and preprocessing scripts
├── training/ # Model training scripts
├── evaluation/ # Evaluation notebooks and metrics
├── app/ # Gradio application code
└── README.md

## Models and Resources

The following resources are associated with this project:

### Model 1
[Model 1 Link "Based on SmolLM2-1.7B-Instruct"](https://huggingface.co/madox81/SmolLM2-Cyber-Insight)

### Model 2
[Model 2 Link "Based on SmolLM2-135M-Instruct"](https://huggingface.co/madox81/SmolLM2-Cyber)

### Dataset
[Dataset Link](https://huggingface.co/datasets/madox81/mittre_severity_ds)

### Gradio Demo Application
[Gradio App Link](https://madox81-cyber-insight.hf.space/)

## Example Use Case

A user can provide a textual description of a cybersecurity incident such as:

> "Suspicious PowerShell execution followed by credential dumping activity detected on a workstation."

The system analyzes the text and can return outputs such as:

- Possible **MITRE ATT&CK tactic**
- Related **attack technique**
- Estimated **incident severity**

## Technologies Used

- Python
- Hugging Face Transformers
- LoRA (Parameter-Efficient Fine-Tuning)
- Pandas
- Gradio
- PyTorch

## Research Context

This project was developed as part of a research study investigating the integration of **natural language processing techniques into cybersecurity analysis workflows**.

The work demonstrates how specialized training data and efficient fine-tuning techniques can enable language models to assist security analysts in interpreting incident reports and threat intelligence data.

## Future Work

Potential improvements include:

- Expanding the cybersecurity training dataset
- Integrating threat intelligence reports
- Improving technique classification accuracy
- Integrating the system into **Security Operations Center (SOC)** workflows
- Evaluating additional model architectures

## License

Specify the license for this repository here.

## Acknowledgments

This project builds upon open-source tools and frameworks provided by the machine learning and cybersecurity communities.    
