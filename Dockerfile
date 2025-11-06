FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# Install dependencies
COPY requirements_local.txt .
RUN pip install --no-cache-dir -r requirements_local.txt

# Copy application code
COPY . .

# Set environment variable to avoid tokenizer warnings
ENV TOKENIZERS_PARALLELISM=false

# Make main script executable
RUN chmod +x main_local.py

# Default command
CMD ["python", "main_local.py", "--model", "meta-llama/Llama-3.2-3B-Instruct"]
