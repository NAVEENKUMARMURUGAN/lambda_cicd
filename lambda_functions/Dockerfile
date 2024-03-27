# Use Ubuntu as base image
FROM ubuntu:latest

# Set environment variable to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

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
RUN if [ ! -e /usr/bin/python3 ]; then \
        ln -s /usr/bin/python3.10 /usr/bin/python3; \
    fi && \
    ln -sf /usr/bin/pip3.10 /usr/bin/pip3

# Create the directory structure
RUN mkdir -p $LAMBDA_FUNCTIONS_DIR

COPY export_rds_to_s3 /lambda_functions/export_rds_to_s3
COPY get_secret /lambda_functions/get_secret
COPY Dockerfile /lambda_functions/Dockerfile
COPY teamcity-services.yml /lambda_functions/teamcity-services.yml

# Set the working directory
WORKDIR $LAMBDA_FUNCTIONS_DIR

# Install Python dependencies for each Lambda function
RUN for function_dir in $(find . -maxdepth 1 -mindepth 1 -type d -not -name '.*'); do \
        cd $function_dir && \
        pip3 install -r requirements.txt -t . && \
        cd ..; \
    done

# Package Lambda functions and put them in NuGet packages
RUN for function_dir in $(find . -maxdepth 1 -mindepth 1 -type d -not -name '.*'); do \
        cd $function_dir && \
        zip -r "$function_dir.zip" * && \
        nuget pack "$function_dir.nuspec" -OutputDirectory $OUTPUT_DIR && \
        cd ..; \
    done

# Copy NuGet packages to the output directory
RUN cp $LAMBDA_FUNCTIONS_DIR/**/*.nupkg $OUTPUT_DIR

# Set the output directory as the working directory
WORKDIR $OUTPUT_DIR
