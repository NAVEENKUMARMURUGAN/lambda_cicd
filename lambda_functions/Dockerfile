# Use Ubuntu as base image
FROM ubuntu:latest

# Set up environment variables
ENV LAMBDA_FUNCTIONS_DIR /lambda_functions
ENV OUTPUT_DIR /output

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    python3.10 \
    python3.10-distutils \
    python3.10-dev \
    python3.10-venv \
    zip \
    nuget

# Alias python3.10 to python3 and pip3.10 to pip3
RUN ln -s /usr/bin/python3.10 /usr/bin/python3 && \
    ln -s /usr/bin/pip3.10 /usr/bin/pip3

# Copy the lambda_functions directory into the container
COPY ../lambda_functions $LAMBDA_FUNCTIONS_DIR

# Set the working directory
WORKDIR $LAMBDA_FUNCTIONS_DIR

# Install Python dependencies for each Lambda function
RUN for function_dir in $(find . -maxdepth 1 -type d -not -name '.*'); do \
        cd $function_dir && \
        pip3 install -r requirements.txt -t . && \
        cd ..; \
    done

# Package Lambda functions and put them in NuGet packages
RUN for function_dir in $(find . -maxdepth 1 -type d -not -name '.*'); do \
        cd $function_dir && \
        zip -r "$function_dir.zip" * && \
        nuget pack "$function_dir.nuspec" -OutputDirectory $OUTPUT_DIR && \
        cd ..; \
    done

# Copy NuGet packages to the output directory
RUN cp *.nupkg $OUTPUT_DIR

# Set the output directory as the working directory
WORKDIR $OUTPUT_DIR

# Entry point command (optional)
# CMD ["/bin/bash"]