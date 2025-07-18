# Lakra Sentences Extraction and Translation

This repository is used for extracting and translating sentences fromv arious domains, as part of our thesis project.


### Prerequisites
- Python >= 3.8
- Ollama CLI (install from [Ollama.com](https://ollama.com))

### Setup

Create a virtual environment

`python -m venv WMK`

Activate the virtual environment

`WMK\Scripts\activate`

Install the packages

`pip install -r requirements.txt`

### Experiment

##### Models

Pull a model from Ollama

`ollama pull <model_name>`

| Model       | Parameters | Developer  | Context Window | PHLs Supported |
| ------------| ---------- | ---------- | -------------- | -------------- | 
| Qwen 3      | 14B        | Alibaba    | 128K tokens    | CEB, ILO, TGL  |
| Gemma 3     | 12B        | Google     | 128K tokens    | CEB, ILO, TGL  |
| Sailor 2    | 20B        | Sea AI Lab | 128K tokens    | CEB, ILO, TGL  |

Ensure the model has been pulled

`ollama list`

Start running the model

`ollama run <model_name>`
