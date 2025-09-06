# 5. Create project structure
echo "📂 Setting up project structure..."

mkdir -p app
touch app/mainapp.py

mkdir -p drafts
mkdir -p graphs
touch .env

mkdir -p drafts
touch drafts/test.ipynb

mkdir -p .github
touch .github/deploy.yml

mkdir -p app/graphs
touch app/graphs/__init__.py
touch app/graphs/save_graphs.py

mkdir -p app/llms
touch app/llms/__init__.py
touch app/llms/groq_client.py
touch app/llms/openai_client.py

mkdir -p app/services
touch app/services/__init__.py
touch app/services/gmail_service.py

mkdir -p app/utils
touch app/utils/__init__.py
touch app/utils/helpers.py

mkdir -p app/workers
touch app/workers/__init__.py
touch app/workers/campaign_graph.py

touch app/__init__.py
touch app/mainapp.py

# 4. Create requirements.txt if not exists & add libraries
if [ ! -f "requirements.txt" ]; then
    echo "📄 Creating requirements.txt..."
    cat <<EOL > requirements.txt
langchain
python-dotenv
langchain_huggingface
langchain-tavily
reportlab
google-api-python-client
google_auth_oauthlib
langchain-openai
streamlit
langchain-groq
pytest
langgraph
EOL
    echo "✅ requirements.txt created with default libraries."
else
    echo "📄 requirements.txt already exists, skipping creation."
fi

set -e  # Exit if any command fails

echo "🚀 Initializing Finance Health Report project with Conda..."
conda create --prefix ./venv python=3.12 -y

# 1. Create Conda environment in local folder (./venv)
if [ ! -d "venv" ]; then
    echo "📦 Creating Conda environment in ./venv ..."
    conda create --prefix ./venv python=3.12 -y
else
    echo "✅ Conda environment already exists in ./venv"
fi

# 2. Activate Conda environment
echo "🔗 Activating Conda environment..."
# Conda environments created with --prefix are activated like this:
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ./venv

echo "🚀 Creating setup.py file with the Project information as needed..."
touch setup.py

# Create setup.py
echo "📝 Creating setup.py..."
cat > setup.py <<EOL
from setuptools import setup, find_packages

setup(
    name="Routing_Agentic_AI_Workflow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-groq",
        "langgraph",
        "python-dotenv",
        "langchain",
        "langchain_huggingface",
        "langchain-tavily",
        "reportlab",
        "google-api-python-client",
        "google_auth_oauthlib",
        "langchain-openai",
        "langchain-groq",
        "pytest"
            ],

    author="Sushant Sur",
    description="ROuting Agentic AI Workflow",
    python_requires=">=3.12",
)
EOL

echo "✅ Setup complete and ready to run! 

echo "✅ Project structure is ready."

echo "⚙️  Installing project in editable mode..."
pip install -e .

#Run the file using the command as ./init.sh in gitbash terminal
